#!/usr/bin/env python3
"""Program P19 --- Convexity and Jensen's inequality.

Every number Program P19 prints that the reader cannot do in their head is
computed here and written to figures/values/p19.tex, which the book \\input{}s.

P19's thesis is that CONVEXITY IS A PROMISE ABOUT THE PROBLEM, NOT ABOUT THE
ALGORITHM. A convex function has one basin, so every local minimum is global
and the answer an optimiser stops at is THE answer. Deep learning breaks that
promise, and what survives anyway is worth naming precisely rather than
hand-waving past.

WHAT P19 IS OWED, read out of the files rather than remembered:

  F04  ALREADY WORKS THE PERPLEXITY DEMONSTRATION IN FULL -- both numbers,
       and which one a leaderboard should print -- and hands the general
       statement here BY NAME: "what happens when you average a curved
       function of a quantity rather than the quantity itself is Jensen's
       inequality, and it belongs to Program P19". So this program owes the
       INEQUALITY and its direction, not the demonstration.
       F04 also draws the contrast with the macro/micro average: same smell,
       different mechanism, because there every step is linear and the
       WEIGHTS do the damage. Worth reusing rather than repeating.
  F03  owns computing a perplexity from a mean loss, and the base warning.
  F11  hands over "convexity, local against global minima" by name.
  F13  hands over "convexity and Jensen's inequality" by name, and owns the
       weighted average, which is the shape Jensen is about.
  P17  owns the second derivative and the bowl, so the convexity TEST is an
       object the reader already has doing a new job.
  P05  owns the norm, and a norm is the standard convex function.

WHAT P19 LEAVES ALONE, checked against tools/programs.json:
    the optimisers that live with a non-convex surface        -> P20
    minibatch noise                                           -> P21
    constrained optimisation and the multiplier               -> P22
    what a perplexity MEANS (effective number of choices)     -> P29
    KL, Jensen--Shannon, the asymmetry                        -> P30

THE HEADLINE IS THAT THE ERROR'S SIZE IS SET BY THE EVALUATION SET. The ratio
of the wrong average to the right one is exp(Var/2) for Gaussian losses, so it
is 1.00 on a homogeneous corpus and over 7 on a diverse one. An evaluation
harness with this bug therefore passes every test on a toy set and misreports
on the real one, which is Program P02's "safe for inputs you have not tried"
arriving in published evaluation code.

Run:  python3 code/p19_convexity_jensen.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p19.tex"
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


def bound(x: float) -> str:
    """A residual is a property of the machine, so commit a CEILING it clears
    on any of them -- P06's rule, which CI enforced the hard way."""
    assert x >= 0.0
    return "0" if x == 0.0 else f"1e{math.ceil(math.log10(x)):d}"


# ---------------------------------------------------------------------------
# 1. THE DEFINITION, checked rather than drawn.
#
# A function is convex when the chord lies on or above the curve:
#     f(t a + (1-t) b) <= t f(a) + (1-t) f(b)
# That is the whole definition, and it is checkable on a grid. The point of
# checking it is not to establish the theorem -- it is to show that the test
# is arithmetic rather than a picture, which is what lets it be applied to a
# function nobody can draw.
# ---------------------------------------------------------------------------
def chord_gap(f, a: float, b: float, t: float) -> float:
    """How far the chord sits ABOVE the curve. Convex means never negative."""
    return t * f(a) + (1 - t) * f(b) - f(t * a + (1 - t) * b)


GRID = [x / 8 for x in range(-24, 25)]          # -3 .. 3
TS = [k / 10 for k in range(1, 10)]


def sweep_chord(f):
    return min(chord_gap(f, a, b, t) for a in GRID for b in GRID for t in TS)


CONVEX = {
    "x^2": lambda x: x * x,
    "e^x": math.exp,
    "|x|": abs,
}
for name, f in CONVEX.items():
    worst = sweep_chord(f)
    assert worst >= -1e-12, (name, worst)
CHORD_TESTS = len(GRID) * len(GRID) * len(TS)
emit("p19.chord.tests", CHORD_TESTS)
emit("p19.chord.fns", len(CONVEX))

# And one that is NOT convex, because a test that cannot fail is not a test.
# P05's rule: finding nothing is not measuring nothing.
def wiggle(x: float) -> float:
    return x ** 4 - 3.0 * x * x + 0.5 * x


worst_wiggle = sweep_chord(wiggle)
assert worst_wiggle < -0.1, worst_wiggle
emit("p19.chord.counterexample", round(-worst_wiggle, 2))
NOTES.append(f"the chord test passes for {len(CONVEX)} convex functions over "
             f"{CHORD_TESTS} triples and fails by "
             f"{-worst_wiggle:.2f} for a quartic that is not convex")

# ---------------------------------------------------------------------------
# 2. THE PROMISE, counted rather than asserted.
#
# A convex function has one basin. The quartic above has two, and the count is
# what the promise is about: an optimiser that stops at a local minimum has
# found THE answer on the first and one of several on the second.
# ---------------------------------------------------------------------------
def local_minima(f, lo=-3.0, hi=3.0, n=600_001):
    step = (hi - lo) / (n - 1)
    ys = [f(lo + i * step) for i in range(n)]
    return [lo + i * step
            for i in range(1, n - 1)
            if ys[i] < ys[i - 1] and ys[i] < ys[i + 1]]


mins_convex = local_minima(lambda x: x * x)
mins_wiggle = local_minima(wiggle)
assert len(mins_convex) == 1, mins_convex
assert len(mins_wiggle) == 2, mins_wiggle
emit("p19.basins.convex", len(mins_convex))
emit("p19.basins.wiggle", len(mins_wiggle))

# The two basins of the quartic do NOT have the same value, which is the
# whole point: on a non-convex surface where you start decides what you get.
vals = sorted(wiggle(x) for x in mins_wiggle)
emit("p19.wiggle.lo", round(vals[0], 3))
emit("p19.wiggle.hi", round(vals[1], 3))
gap = vals[1] - vals[0]
assert gap > 0.5, gap
emit("p19.wiggle.gap", round(gap, 3))
NOTES.append(f"the quartic's two local minima differ by {gap:.3f}, so on it "
             "the starting point decides the answer")

# ---------------------------------------------------------------------------
# 3. JENSEN, AND THE HEADLINE.
#
# For a convex f and any weights, f(mean of x) <= mean of f(x). Applied to
# exp, that says the exponential of the mean loss is at most the mean of the
# per-example perplexities -- so the two numbers a leaderboard might print
# are ORDERED, always, and the wrong one is always the larger.
#
# What is new here, and what makes the section worth writing, is the SIZE:
# the ratio is exp(Var/2) for Gaussian losses. So the discrepancy is set by
# the heterogeneity of the evaluation set, which is why an implementation
# carrying it passes on a toy corpus and misreports on a real one.
# ---------------------------------------------------------------------------
def ppl_of_mean(losses):
    return math.exp(sum(losses) / len(losses))


def mean_of_ppl(losses):
    return sum(math.exp(v) for v in losses) / len(losses)


random.seed(19)
MEAN_LOSS = 2.5
N_TOKENS = 200_000
SPREADS = [0.0, 0.5, 1.0, 2.0]
rows = []
for sd in SPREADS:
    losses = [random.gauss(MEAN_LOSS, sd) for _ in range(N_TOKENS)]
    right, wrong = ppl_of_mean(losses), mean_of_ppl(losses)
    # JENSEN ITSELF, which is exact for any sample and any distribution.
    assert wrong >= right - 1e-9, (sd, right, wrong)
    mu = sum(losses) / len(losses)          # once, not once per term:
    var = sum((v - mu) ** 2 for v in losses) / len(losses)
    rows.append((sd, right, wrong, wrong / right, math.exp(var / 2)))

emit("p19.ppl.tokens", N_TOKENS)
emit("p19.ppl.meanloss", MEAN_LOSS, digits=1)
for sd, right, wrong, ratio, pred in rows:
    tag = f"{sd:.1f}".replace(".", "")
    emit(f"p19.ppl.right.{tag}", right, digits=1)
    emit(f"p19.ppl.wrong.{tag}", wrong, digits=1)
    emit(f"p19.ppl.ratio.{tag}", ratio, digits=2)

# The prediction is REPORTED rather than asserted as a law: exp(Var/2) is
# exact for a log-normal and second-order otherwise, so asserting it in
# general would be asserting something false. What IS asserted is Jensen.
worst_pred = max(abs(r - p) / p for _, _, _, r, p in rows)
assert worst_pred < 0.02, worst_pred
emit("p19.ppl.pred.bound", f"{math.ceil(worst_pred * 100):d}")
assert abs(rows[0][3] - 1.0) < 1e-9                # zero spread, zero gap
assert rows[-1][3] > 5.0, rows[-1][3]              # and it runs away
NOTES.append(f"the wrong average is {rows[-1][3]:.2f}x the right one at a "
             f"spread of {SPREADS[-1]:.0f} nats and exactly equal at zero: "
             "the error is a property of the evaluation set")

# The gate: F04 committed this program's own worked example, and the two
# programs must not be able to disagree about which number is which.
_f04_right = committed("f04.tex", "f04.ce.ppl")
_f04_wrong = committed("f04.tex", "f04.ce.ppl.naive")
if _f04_right and _f04_wrong:
    assert float(_f04_wrong) > float(_f04_right), (_f04_wrong, _f04_right)
    NOTES.append("gate: F04's own two perplexities are ordered the way "
                 "Jensen says they must be")

# ---------------------------------------------------------------------------
# 4. THE SAME INEQUALITY, ONE STEP FURTHER.
#
# ln is CONCAVE, so the inequality turns round: ln(mean) >= mean(ln). That one
# line is the ELBO, and naming it is the point rather than deriving anything
# about variational inference, which this book does not undertake.
# ---------------------------------------------------------------------------
POS = [x / 4 for x in range(1, 41)]                # 0.25 .. 10
worst_concave = (math.log(sum(POS) / len(POS))
                 - sum(math.log(v) for v in POS) / len(POS))
assert worst_concave > 0, worst_concave
emit("p19.elbo.gap", worst_concave, digits=3)

# and the general form, checked on random positive samples rather than one
random.seed(190)
worst_flip = None
for _ in range(20_000):
    k = random.randint(2, 8)
    xs = [random.uniform(0.05, 20.0) for _ in range(k)]
    g = math.log(sum(xs) / k) - sum(math.log(v) for v in xs) / k
    assert g >= -1e-12, (xs, g)
    worst_flip = g if worst_flip is None else min(worst_flip, g)
emit("p19.elbo.trials", 20_000)
assert worst_flip >= -1e-12
NOTES.append("ln is concave, so the inequality turns round: ln of the mean is "
             "at least the mean of the ln, over 20 000 random samples")

# ---------------------------------------------------------------------------
# 5. WHAT SURVIVES. The honest section.
#
# The promise is broken and the arithmetic still says something. A convex
# function's Hessian is positive semi-definite everywhere -- P17's object,
# used as a TEST -- and a network's is not, which is why P17's counting
# argument about saddles applies at all.
# ---------------------------------------------------------------------------
def second_derivative(f, x, h=1e-4):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)


neg_curv = [x for x in GRID if second_derivative(wiggle, x) < -1e-6]
assert neg_curv, "the quartic must curve downwards somewhere"
emit("p19.curv.negative", len(neg_curv))
emit("p19.curv.tested", len(GRID))
worst_convex_curv = min(second_derivative(lambda v: v * v, x) for x in GRID)
assert worst_convex_curv > 0, worst_convex_curv
NOTES.append(f"the quartic curves downwards at {len(neg_curv)} of "
             f"{len(GRID)} grid points, which is the second-derivative test "
             "from Program P17 used as a convexity test")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    # The rounding is written INTO the listing rather than applied to its
    # output: a transcript claiming Python printed 12.1825 when it prints
    # 12.182493960703473 is a fabricated console block, which is the one
    # defect this book's whole transcript mechanism exists to prevent.
    FLAT = [MEAN_LOSS] * 4
    MIXED = [0.5, 1.0, 3.5, 5.0]
    assert abs(sum(FLAT) / 4 - sum(MIXED) / 4) < 1e-12   # the SAME mean loss
    lines = [
        ">>> from p19_convexity_jensen import ppl_of_mean, mean_of_ppl",
        f">>> flat = {FLAT}      # every token alike",
        ">>> round(ppl_of_mean(flat), 2), round(mean_of_ppl(flat), 2)",
        f"{(round(ppl_of_mean(FLAT), 2), round(mean_of_ppl(FLAT), 2))}",
        f">>> mixed = {MIXED}    # same mean, spread out",
        ">>> round(ppl_of_mean(mixed), 2), round(mean_of_ppl(mixed), 2)",
        f"{(round(ppl_of_mean(MIXED), 2), round(mean_of_ppl(MIXED), 2))}",
    ]
    for line in lines:
        assert len(line) <= 64, (len(line), line)
    (TRANSCRIPTS / "p19-two-averages.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    out = [
        "% Generated by code/p19_convexity_jensen.py --- do not edit.",
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
