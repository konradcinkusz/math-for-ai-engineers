#!/usr/bin/env python3
"""Program P21 --- Stochastic optimisation and differentiating through randomness.

Every number Program P21 prints that the reader cannot do in their head is
computed here and written to figures/values/p21.tex, which the book \\input{}s.

P21's thesis is that A MINIBATCH GRADIENT IS AN ESTIMATOR, and that almost
every complaint about training noise is a statement about that estimator's
variance rather than about the model. The noise is a property of the algorithm
and not a defect in it.

WHAT P21 IS OWED, read out of the files rather than remembered:

  P20  hands over the batch BY NAME. Its trap list sends item 24 -- "I halved
       the batch size, so I'll keep the learning rate" -- here, because P20
       owns the schedules and this program owns the batch. P20 also leaves the
       optimiser itself entirely settled, so nothing here has to re-derive one.
  F06  OWNS CLIPPING OUTRIGHT, both operations and the measurement: on
       (6, 0.5, -0.25) at a threshold of 1, clipping by value leaves the length
       at 1.1456 and turns the vector 23.9 degrees, clipping by norm lands on
       1.0000 exactly and turns it not at all. F06 says in as many words that
       Program P21 "owns the question properly -- it has the noise model that
       says why the occasional enormous step happens at all". So this program
       owes the WHY, never the two operations.
  F04  OWNS THE AVERAGE-OF-AVERAGES ERROR and works it three times -- pooled
       loss, sharded accuracy, token rate. Trap item 25 (accumulation) is the
       TRAINING instance of it, and the difference worth paying for is that
       there it changes a report and here it changes the GRADIENT.
  F04  also owns the exponential moving average, so the smoothed loss curve is
       its machinery doing a new job.

  P24 and P25 own VARIANCE ITSELF, two parts later. That is the book's one
  deliberate forward prerequisite: it is declared in the Learning outcomes with
  a pointer, recorded in notes/01 section 12, and it must not be "fixed" by
  reordering the parts, which would break six other dependencies.

WHAT P21 LEAVES ALONE, checked against tools/programs.json:
    the optimisers, the schedules, AdamW                      -> P20
    what a variance IS, and concentration                     -> P24, P25
    the multiplier as the price of a constraint               -> P22
    KL and the asymmetry                                      -> P30

THE HEADLINE IS THE FORK. Two estimators of one gradient through a sampling
step: the score-function estimator and the reparameterisation trick. Both are
unbiased. One's variance is FLAT in the dimension and the other's grows without
bound -- measured, and it is the whole reason policy-gradient methods need
baselines and a VAE does not.

Run:  python3 code/p21_stochastic_optimisation.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
import statistics
from fractions import Fraction
from itertools import combinations
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p21.tex"
TRANSCRIPTS = Path(__file__).resolve().parents[1] / "figures" / "transcripts"
VALUES: dict[str, tuple[str, bool]] = {}
NOTES: list[str] = []


def emit(key: str, value, digits: int | None = None) -> None:
    if isinstance(value, float) and digits is not None:
        body = f"{value:.{digits}f}"
    elif isinstance(value, float):
        body = repr(value)
    else:
        body = str(value)
    try:
        numeric = math.isfinite(float(body.replace("e", "E")))
    except ValueError:
        numeric = False
    VALUES[key] = (body, numeric)


def committed(fname: str, key: str) -> str | None:
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    import re
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


def bound(x: float, ceiling: float) -> str:
    """Commit the CEILING the caller states and merely check the measurement
    clears it. Program P20's pass established the second half of this: a
    helper that returns the tightest power of ten above a residual is itself
    machine-dependent when the residual can be exactly zero."""
    assert 0.0 <= x < ceiling, (x, ceiling)
    return f"1e{round(math.log10(ceiling)):d}"


# ---------------------------------------------------------------------------
# 1. UNBIASED, PROVED RATHER THAN SAMPLED.
#
# "The minibatch gradient is unbiased" is a statement about an average over
# EVERY batch that could have been drawn, so on a small population it can be
# checked by drawing every one of them -- which is a proof for that case, not
# evidence. Program P14 makes exactly this distinction; the arithmetic is over
# Fractions so there is no tolerance anywhere in it.
# ---------------------------------------------------------------------------
POP = [Fraction(g) for g in (3, -1, 4, 1, -5, 9, 2, -6, 5, 8)]
POP_MEAN = sum(POP) / len(POP)
BATCH = 3

subsets = list(combinations(POP, BATCH))
mean_of_means = sum(sum(s) / BATCH for s in subsets) / len(subsets)
assert mean_of_means == POP_MEAN, (mean_of_means, POP_MEAN)

emit("p21.pop.n", len(POP))
emit("p21.pop.b", BATCH)
emit("p21.pop.subsets", len(subsets))
emit("p21.pop.mean", float(POP_MEAN), 1)
NOTES.append(f"every one of the {len(subsets)} batches of {BATCH} was drawn "
             f"and their means average to {float(POP_MEAN)} exactly, over "
             "fractions -- a proof for this population rather than evidence")

# And the individual batches are spread all over, which is the point: unbiased
# says nothing whatever about any single draw.
#
# --- A DRAFT ASSERTED THE WORST BATCH IS "MORE THAN FOUR TIMES THE MEAN AWAY"
# AND IT FAILED, at 6 against 8. That is a threshold chosen so a claim would
# pass, which is the failure mode Programs F11, P15 and P20 have each paid for.
# What is asserted instead needs no threshold at all: the average of the batch
# means is exactly the population mean, and the batch means STRADDLE it -- the
# smallest is below and the largest above, so no single draw can be trusted and
# the exactness is a statement about the ensemble only.
batch_means = [sum(s) / BATCH for s in subsets]
LO, HI = min(batch_means), max(batch_means)
assert LO < POP_MEAN < HI, (LO, POP_MEAN, HI)
emit("p21.pop.lo", float(LO), 2)
emit("p21.pop.hi", float(HI), 2)
emit("p21.pop.span", float(HI - LO), 2)

# A REVIEW FOUND THE PROSE SAYING "one of them has the wrong sign", in three
# places, one of them a \result{} that Appendix C replays.  Counted rather
# than eyeballed: it is a fifth of them, and four more report no direction at
# all, which is the worse half and was the half nobody had looked for.  The
# population's own sign is asserted so the sentence cannot invert under a
# change of numbers.
assert POP_MEAN > 0, POP_MEAN
WRONG = sum(1 for m in batch_means if m < 0)
NODIR = sum(1 for m in batch_means if m == 0)
assert WRONG > 0 and NODIR > 0, (WRONG, NODIR)
emit("p21.pop.wrong", WRONG)
emit("p21.pop.nodir", NODIR)
emit("p21.pop.wrong.pct", 100 * WRONG / len(batch_means), 0)
NOTES.append(f"{WRONG} of the {len(subsets)} batch means point the opposite "
             f"way to the population mean and {NODIR} more are exactly zero, "
             "so a draft that said one of them has the wrong sign was out by "
             "a factor of twenty-four and silent about the four")


# ---------------------------------------------------------------------------
# 2. THE VARIANCE FALLS LIKE 1/B, and that is the whole noise model.
# ---------------------------------------------------------------------------
random.seed(20260901)
BIG = [random.gauss(1.0, 3.0) for _ in range(20_000)]
POP_VAR = statistics.pvariance(BIG)
TRIALS = 4000
SIZES = (1, 4, 16, 64, 256)


def batch_variance(b: int, trials: int = TRIALS) -> float:
    means = [sum(random.choice(BIG) for _ in range(b)) / b for _ in range(trials)]
    return statistics.pvariance(means)


rows, ratios = [], []
for b in SIZES:
    measured = batch_variance(b)
    predicted = POP_VAR / b
    rows.append((b, measured, predicted))
    ratios.append(measured / predicted)

# The INVARIANT is that the measurement tracks sigma^2/B, not any one figure:
# a single variance is a random quantity and would move with the seed.
assert max(abs(r - 1.0) for r in ratios) < 0.08, ratios
emit("p21.noise.pop", len(BIG))
emit("p21.noise.trials", TRIALS)
emit("p21.noise.sd", math.sqrt(POP_VAR), 2)
emit("p21.noise.b.lo", SIZES[0])
emit("p21.noise.b.hi", SIZES[-1])
emit("p21.noise.sd1", math.sqrt(rows[0][1]), 2)
emit("p21.noise.sd256", math.sqrt(rows[-1][1]), 3)
emit("p21.noise.drop", math.sqrt(rows[0][1] / rows[-1][1]), 1)
emit("p21.noise.tol", 8)
NOTES.append("the variance of a batch mean tracks sigma^2/B to within 8 per "
             f"cent over B from {SIZES[0]} to {SIZES[-1]}, so the SPREAD falls "
             "like one over the square root of the batch")

# The consequence people misread: sixteen times the batch buys FOUR times less
# noise, not sixteen. The square root is where "diminishing returns" comes from
# and it is not a heuristic.
assert abs(math.sqrt(rows[0][1] / rows[2][1]) - 4.0) < 0.3
emit("p21.noise.b16", 16)
emit("p21.noise.spread16", math.sqrt(rows[0][1] / rows[2][1]), 1)


# ---------------------------------------------------------------------------
# 3. THE TWO SCALING RULES, and what each one holds fixed.
#
# The UPDATE is eta * ghat, so its variance is eta^2 * sigma^2 / B. Scale the
# batch by k and ask what to do with eta:
#     eta -> k eta      multiplies the update's variance by k
#     eta -> sqrt(k)eta leaves it exactly where it was
# Both are exact, both are one line, and they disagree -- which is why the
# linear rule is contested rather than derived. This program states both
# invariants and does not adjudicate the empirical question.
# ---------------------------------------------------------------------------
ETA0, B0 = 0.1, 16
KS = (1, 2, 4, 8)


def update_var(eta: float, b: int) -> float:
    return eta * eta * POP_VAR / b


base = update_var(ETA0, B0)
lin = [update_var(k * ETA0, k * B0) / base for k in KS]
sqr = [update_var(math.sqrt(k) * ETA0, k * B0) / base for k in KS]
for k, l, s in zip(KS, lin, sqr):
    assert abs(l - k) < 1e-12, (k, l)                  # linear: grows like k
    assert abs(s - 1.0) < 1e-12, (k, s)                # sqrt: exactly fixed
emit("p21.scale.k", KS[-1])
emit("p21.scale.linear", lin[-1], 0)
emit("p21.scale.sqrt", sqr[-1], 0)
NOTES.append(f"scaling the batch by {KS[-1]} and the step size with it "
             f"multiplies the update's variance by {lin[-1]:.0f}; scaling the "
             "step size by the square root leaves it exactly unchanged")


# ---------------------------------------------------------------------------
# 4. WHAT A MOVING AVERAGE HIDES.
#
# Program F04's exponential moving average, doing a new job. A smoothed loss
# curve is easier to read and it LAGS: after a genuine step change the smoothed
# curve needs about a half-life to cover half the distance, by construction.
# ---------------------------------------------------------------------------
BETA = 0.9
HALFLIFE = math.log(0.5) / math.log(BETA)
_f04_hl = committed("f04.tex", "f04.ema.halflife")
if _f04_hl:
    assert abs(float(_f04_hl) - HALFLIFE) < 5e-4, (_f04_hl, HALFLIFE)

BEFORE, AFTER, N_STEP = 2.0, 1.0, 400
m, lagged = 0.0, None
for t in range(1, 2 * N_STEP + 1):
    truth = BEFORE if t <= N_STEP else AFTER
    m = BETA * m + (1 - BETA) * truth
    mhat = m / (1 - BETA ** t)
    if t > N_STEP and lagged is None and mhat <= (BEFORE + AFTER) / 2:
        lagged = t - N_STEP
assert lagged is not None
# The lag IS the half-life, by construction rather than by coincidence.
assert abs(lagged - HALFLIFE) <= 1.0, (lagged, HALFLIFE)
emit("p21.ema.beta", BETA, 1)
emit("p21.ema.halflife", HALFLIFE, 2)
emit("p21.ema.lag", lagged)
NOTES.append(f"after a genuine step change the smoothed curve takes "
             f"{lagged} steps to report half of it, which is the half-life "
             f"of {HALFLIFE:.2f} and not a property of the change")


# ---------------------------------------------------------------------------
# 5. THE ACCUMULATION DENOMINATOR.
#
# Program F04 elicits the average-of-averages error and works it three times.
# This is the TRAINING instance, and the difference is that there it changes a
# report and here it changes the GRADIENT. Exact over fractions, because the
# claim is that two expressions differ rather than that they differ by much.
# ---------------------------------------------------------------------------
MICRO = [(1000, Fraction(2)), (10, Fraction(8)), (500, Fraction(3))]
tokens = sum(n for n, _ in MICRO)
pooled = sum(n * loss for n, loss in MICRO) / tokens          # the large batch
accumulated = sum(loss for _, loss in MICRO) / len(MICRO)     # mean of means
assert pooled != accumulated, (pooled, accumulated)

emit("p21.acc.tokens", tokens)
emit("p21.acc.pooled", float(pooled), 4)
emit("p21.acc.accumulated", float(accumulated), 4)
emit("p21.acc.ratio", float(accumulated / pooled), 2)
NOTES.append(f"three micro-batches holding {tokens} tokens between them give "
             f"a pooled loss of {float(pooled):.4f} and an accumulated one of "
             f"{float(accumulated):.4f}, a factor of "
             f"{float(accumulated / pooled):.2f} -- and it is the gradient "
             "rather than a report")

# And the invariant that says WHEN it is safe, which is the useful half:
# equal token counts make the two expressions identical, exactly.
EQUAL = [(500, Fraction(2)), (500, Fraction(8)), (500, Fraction(3))]
p_eq = sum(n * l for n, l in EQUAL) / sum(n for n, _ in EQUAL)
a_eq = sum(l for _, l in EQUAL) / len(EQUAL)
assert p_eq == a_eq, (p_eq, a_eq)
NOTES.append("with equal token counts the two are identical over fractions, "
             "which is why the defect hides: it appears only when the "
             "micro-batches are ragged, and padding hides that")


# ---------------------------------------------------------------------------
# 6. TWO WAYS THROUGH A SAMPLING STEP, and the fork they make.
#
# Estimate d/dtheta E_{x ~ N(theta, 1)}[ ||x||^2 ] with respect to one
# component of theta. The truth is 2*theta.
#
#   score function     f(x) * d/dtheta log p(x; theta)   -- needs no gradient
#                                                          of f at all
#   reparameterisation x = theta + eps, differentiate straight through
#
# Both are unbiased. The point of the section is what happens to their
# VARIANCES as the dimension grows, because that is the fork between a
# policy-gradient method and a VAE.
# ---------------------------------------------------------------------------
random.seed(20260902)
THETA, SIGMA = 0.3, 1.0
TRUE_GRAD = 2 * THETA
DIMS = (1, 10, 100)
SAMPLES = 40_000

grad_rows = []
for d in DIMS:
    sc, rp = [], []
    for _ in range(SAMPLES):
        eps = [random.gauss(0.0, 1.0) for _ in range(d)]
        x = [THETA + SIGMA * e for e in eps]
        fx = sum(xi * xi for xi in x)
        sc.append(fx * (x[0] - THETA) / SIGMA ** 2)
        rp.append(2 * x[0])
    grad_rows.append((d, statistics.pvariance(sc), statistics.pvariance(rp),
                      sum(sc) / SAMPLES, sum(rp) / SAMPLES))

# THE INVARIANT, and it is two statements rather than one figure.
# (a) reparameterisation's variance is 4*sigma^2 at EVERY dimension, exactly,
#     because the estimator is 2x_1 and nothing else enters it;
# (b) the score function's grows without bound.
for d, sv, rv, sm, rm in grad_rows:
    assert abs(rv - 4 * SIGMA ** 2) < 0.15, (d, rv)
assert [r[1] for r in grad_rows] == sorted(r[1] for r in grad_rows)
assert grad_rows[-1][1] > 100 * grad_rows[0][1], grad_rows

emit("p21.grad.samples", SAMPLES)
emit("p21.grad.true", TRUE_GRAD, 1)
emit("p21.grad.d.lo", DIMS[0])
emit("p21.grad.d.hi", DIMS[-1])
emit("p21.grad.score.lo", grad_rows[0][1], 1)
emit("p21.grad.score.hi", grad_rows[-1][1], 0)
emit("p21.grad.repar", 4.0 * SIGMA ** 2, 1)
# THE RATIO IS AGAINST THE EXACT DENOMINATOR, NOT THE SAMPLED ONE.  The table
# prints 4*sigma^2, which is exact -- Var(2x_1) with x_1 = theta + sigma*eps
# is 4*sigma^2 and nothing else enters it -- and a draft divided by the
# SAMPLED variance instead, so the page printed a ratio a reader dividing the
# two printed numbers could not reproduce.  Asserted on the printed forms,
# which is the only form anybody checks.
REPAR_EXACT = 4.0 * SIGMA ** 2
emit("p21.grad.ratio.hi", grad_rows[-1][1] / REPAR_EXACT, 0)
assert (f"{grad_rows[-1][1] / REPAR_EXACT:.0f}"
        == f"{float(f'{grad_rows[-1][1]:.0f}') / float(f'{REPAR_EXACT:.1f}'):.0f}")
emit("p21.grad.score.est", grad_rows[-1][3], 2)
NOTES.append(f"at {DIMS[-1]} dimensions the score-function estimator's "
             f"variance is {grad_rows[-1][1]/REPAR_EXACT:.0f} times the "
             "reparameterised one's, and the reparameterised variance has not "
             "moved from 4 at any dimension")

# The consequence, and it is the sentence the section is for: unbiased is not
# the same as usable. After SAMPLES draws the score-function estimate is still
# visibly off while the reparameterised one has settled.
off_score = abs(grad_rows[-1][3] - TRUE_GRAD) / TRUE_GRAD
off_repar = abs(grad_rows[-1][4] - TRUE_GRAD) / TRUE_GRAD
assert off_score > 5 * off_repar, (off_score, off_repar)
emit("p21.grad.off.score", 100 * off_score, 0)
emit("p21.grad.off.repar", 100 * off_repar, 1)


# ---------------------------------------------------------------------------
# 7. WHY THE ENORMOUS STEP HAPPENS, which is Program F06's IOU.
#
# F06 owns the two clipping operations and measured them. What it hands here is
# the noise model: a batch mean has a spread, so an occasional batch is far
# from the population's gradient, and how often depends only on that spread.
# The threshold is then a decision about a distribution rather than a constant.
# ---------------------------------------------------------------------------
_f06_norm = committed("f06.tex", "f06.grad.norm")
_f06_by_norm = committed("f06.tex", "f06.clip.norm.norm")
if _f06_by_norm:                       # clipping by norm lands ON the threshold
    assert abs(float(_f06_by_norm) - 1.0) < 1e-9, _f06_by_norm

norms = [abs(sum(random.choice(BIG) for _ in range(16)) / 16) for _ in range(20_000)]
typical = statistics.median(norms)
clip_rows = []
for mult in (0.5, 1.0, 2.0, 4.0):
    thr = mult * typical
    frac = sum(1 for n in norms if n > thr) / len(norms)
    clip_rows.append((mult, frac))
# Below the typical size almost every step is clipped, which is a different
# algorithm; well above it, almost none is, which is the intended one.
assert clip_rows[0][1] > 0.5, clip_rows
assert clip_rows[-1][1] < 0.05, clip_rows
emit("p21.clip.typical", typical, 3)
emit("p21.clip.half", 100 * clip_rows[0][1], 0)
emit("p21.clip.one", 100 * clip_rows[1][1], 0)
# A percentage that rounds to zero is Program P05's "rounds to a hundred"
# defect in a mirror: it reads as EXACTLY none and it is not. Report the count
# out of the sample instead, where every figure means something.
emit("p21.clip.trials", len(norms))
emit("p21.clip.four.n", round(clip_rows[-1][1] * len(norms)))
NOTES.append(f"a threshold at half the typical size clips "
             f"{100*clip_rows[0][1]:.0f} per cent of steps and one at four "
             f"times it clips {round(clip_rows[-1][1]*len(norms))} of "
             f"{len(norms)} -- the same word for two different algorithms")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    # The rounding is written INTO the listing rather than applied to its
    # output, on P19's finding.
    lines = [
        ">>> from p21_stochastic_optimisation import POP, POP_MEAN",
        ">>> from itertools import combinations",
        ">>> b3 = [sum(s)/3 for s in combinations(POP, 3)]",
        ">>> sum(b3)/len(b3) == POP_MEAN",
        f"{sum(sum(s)/3 for s in combinations(POP, 3))/len(subsets) == POP_MEAN}",
        ">>> float(min(b3)), float(max(b3))",
        f"{(float(min(sum(s)/3 for s in combinations(POP, 3))), float(max(sum(s)/3 for s in combinations(POP, 3))))}",
    ]
    for line in lines:
        assert len(line) <= 64, (len(line), line)
    (TRANSCRIPTS / "p21-every-batch.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    out = [
        "% Generated by code/p21_stochastic_optimisation.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ] + [
        f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}"
        for k, (body, numeric) in VALUES.items()
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf8")

    w = max(len(k) for k in VALUES)
    items = list(VALUES.items())
    for i in range(0, len(items), 3):
        print("  " + "   ".join(f"{k:{w}s} {b:>10s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
