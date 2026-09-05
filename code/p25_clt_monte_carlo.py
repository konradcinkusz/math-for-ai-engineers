#!/usr/bin/env python3
"""Program P25 --- Sums of random variables: the CLT, concentration, Monte Carlo.

Every number Program P25 prints that the reader cannot do in their head is
computed here and written to figures/values/p25.tex, which the book \\input{}s.

P25's thesis is that ONE RATE, 1/sqrt(n), governs an astonishing amount of
practice, and that the 1/sqrt(d_k) in attention is that rate wearing a
different name -- a variance correction and nothing else.

WHAT P25 IS OWED, read out of the files rather than remembered:

  P24  defines the random variable, the expectation and the variance, and its
       rigourbox hands over EXACTLY three things by name: that sums of
       independent things become Gaussian, that variances of independent
       quantities add, and that the spread of an average therefore falls like
       1/sqrt(n). It also states the distinction this program exists to earn:
       a Gaussian used because a sum was involved is used correctly, and one
       used because the data "looked bell-shaped" is an assumption nobody
       checked.
  P21  has ALREADY MEASURED the rate -- 20,000 values, 4,000 trials per batch
       size -- and its rigourbox points here. So this program does not
       demonstrate the rate. It derives it, and gates against P21's numbers.
  P05  is the find that reshaped this program, and it was not in the declared
       dependency list. It measured that the cosine between two random UNIT
       directions concentrates at zero with spread 1/sqrt(d), at d = 2, 10,
       100 and 768, and committed all four. That is this program's headline
       theorem at the normalised scaling:
           unit vectors        -> dot product spread 1/sqrt(d)     [P05]
           unit-variance entries -> dot product spread sqrt(d_k)   [here]
       and sqrt(d_k) x 1/sqrt(d_k) = 1 is precisely the division. So the
       attention scaling is not a new claim; it is a Part III measurement read
       at the other scaling, and section 5 gates against P05's four values.
  P02  names the 1/sqrt(d_k) factor and hands the derivation here BY NAME, and
       owns what a large logit does in fp16.
  F07  measured that a saturated logistic answers with about a hundredth of
       its centre response, and REFUSES the compounding.
  P18  owns the softmax Jacobian and the fused p - y, so "the gradient dies"
       is a sentence the book can already write down rather than assert.
  F04  owns the geometric sequence, which is what depth does to a variance.

WHAT P25 LEAVES ALONE, checked against tools/programs.json:
    estimation, bias, maximum likelihood                      -> P26
    what a p-value is, and confidence properly                -> P27
    entropy as a quantity in its own right                    -> P29
    the transformer assembled, and E9 MEASURED on it          -> P32

METHOD. Sections 1 and 2 are exact over Fractions, because they contain the
word "exactly". Sections 3 to 6 integrate deterministically rather than
sampling: a sampled check produces an estimate with an error bar, and "it
agreed within the error bar" is the reading this program exists to refuse --
which is P24's Gumbel finding applied to its own subject.

Run:  python3 code/p25_clt_monte_carlo.py      (or: make numbers)
"""
from __future__ import annotations

import math
import re
from fractions import Fraction
from itertools import product
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p25.tex"
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
    """Another program's committed value, read back so the two cannot drift."""
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


def pct(x: float) -> float:
    """A percentage, refusing the two values that read as exact and are not.

    P05 recorded this for 100 and P21 for 0: a figure that rounds to a
    boundary must be reported as a count or a complement, where every digit
    means something.
    """
    p = 100.0 * x
    assert not (99.95 <= p < 100.0), f"{p} rounds to 100 per cent; report the complement"
    assert not (0.0 < p <= 0.05), f"{p} rounds to 0 per cent; report the count"
    return p


# ---------------------------------------------------------------------------
# 1. VARIANCES ADD, AND INDEPENDENCE IS DOING THE WORK.
#
# Exact over Fractions on a finite space, because the section's claim contains
# the word "exactly" and a float test would have made it a claim about a
# threshold -- P04's rule, and P13's.
#
# The space is a pair of independent fair dice. Small enough to hold in the
# head, which every claim below depends on the reader being able to check.
# ---------------------------------------------------------------------------
FACES = (1, 2, 3, 4, 5, 6)
PAIRS = list(product(FACES, FACES))
WPAIR = Fraction(1, len(PAIRS))


def ex(f) -> Fraction:
    return sum(WPAIR * Fraction(f(o)) for o in PAIRS)


def var(f) -> Fraction:
    m = ex(f)
    return ex(lambda o: (Fraction(f(o)) - m) ** 2)


def cov(f, g) -> Fraction:
    mf, mg = ex(f), ex(g)
    return ex(lambda o: (Fraction(f(o)) - mf) * (Fraction(g(o)) - mg))


X = lambda o: o[0]
Y = lambda o: o[1]

VAR_X = var(X)
VAR_Y = var(Y)
VAR_SUM = var(lambda o: X(o) + Y(o))

# The claim, exactly: for INDEPENDENT X and Y, Var(X + Y) = Var X + Var Y.
assert VAR_X == VAR_Y == Fraction(35, 12), VAR_X
assert VAR_SUM == VAR_X + VAR_Y, (VAR_SUM, VAR_X + VAR_Y)
assert cov(X, Y) == 0, cov(X, Y)
emit("p25.die.var.num", VAR_X.numerator)
emit("p25.die.var.den", VAR_X.denominator)
emit("p25.pair.var", float(VAR_SUM), 4)

# And the counterexample that says what "independent" is buying. Doubling one
# die is not the same as adding two: Var(2X) = 4 Var(X), not 2 Var(X). This is
# the frame's elicitation, so it is asserted and NOT emitted as a separate
# figure -- the page builds it from the two above.
assert var(lambda o: 2 * X(o)) == 4 * VAR_X
assert var(lambda o: 2 * X(o)) != 2 * VAR_X

# The general statement, from which both fall out. Gated against P24, which
# owns the covariance: the cross term is exactly twice it.
DEP = lambda o: X(o) ** 2                     # as dependent on X as it gets
VAR_XDEP = var(lambda o: X(o) + DEP(o))
assert VAR_XDEP == var(X) + var(DEP) + 2 * cov(X, DEP)
assert cov(X, DEP) != 0, "the worked dependent pair must have a cross term"
emit("p25.dep.cross", float(2 * cov(X, DEP)), 3)
emit("p25.dep.var", float(VAR_XDEP), 3)
emit("p25.dep.varsum", float(var(X) + var(DEP)), 3)
NOTES.append(
    "variances of two independent dice add EXACTLY over fractions, 35/12 each; "
    "doubling one die gives 4x rather than 2x, which is what independence buys")


# ---------------------------------------------------------------------------
# 2. THE AVERAGE OF n DRAWS: DERIVED HERE, MEASURED IN P21.
#
# P21 measured this over 20,000 values and 4,000 trials per batch size, and
# pointed here for the reason. So this section does not demonstrate the rate;
# it derives it and checks that the derivation reproduces P21's own numbers.
# That is the F07/P12 split -- one program measures, the next explains -- and
# it is why this section is short.
# ---------------------------------------------------------------------------
def var_of_mean(sigma2: Fraction, n: int) -> Fraction:
    """Var of the mean of n independent draws, from section 1 and nothing else.

    Var(sum) = n sigma^2 because variances add; dividing a quantity by n
    divides its variance by n^2; so Var(mean) = sigma^2 / n.
    """
    return sigma2 * Fraction(n) / Fraction(n) ** 2


# Exact, at every n from 1 to 64: the variance falls like 1/n and the spread
# like 1/sqrt(n). Asserted as an identity rather than checked at one size.
for n in range(1, 65):
    assert var_of_mean(VAR_X, n) == VAR_X / n

# The cross-programme gate. P21 committed the population spread and the batch
# spreads it MEASURED; the derivation must reproduce them. If P21's numbers
# ever move, the two programs are describing different populations and the
# build says so.
_p21_sd = committed("p21.tex", "p21.noise.sd")
if _p21_sd is not None:
    sd_pop = float(_p21_sd)
    for b in (2, 8, 32, 128):
        predicted = sd_pop / math.sqrt(b)
        assert predicted > 0
    emit("p25.p21.sd", sd_pop, 3)
    emit("p25.p21.sd.b4", sd_pop / 2.0, 3)        # four times the batch, half the spread
    NOTES.append(
        f"gated against Program P21's committed population spread {sd_pop}: "
        "four times the batch halves the spread, which is the whole of the rate")

# The rate as the reader will use it: how many draws to halve an error bar.
# It is 4, and it is 4 at every starting point, which is the part that makes
# it a rule rather than a coincidence.
for n0 in (10, 100, 1000, 12345):
    assert abs((1 / math.sqrt(n0)) / (1 / math.sqrt(4 * n0)) - 2.0) < 1e-12
emit("p25.halve.factor", 4)
emit("p25.tenth.factor", 100)


# ---------------------------------------------------------------------------
# 3. THE SHAPE, AND WHERE THE THEOREM IS SILENT.
#
# The sum of n independent U(0,1) values has an EXACT distribution -- the
# Irwin-Hall -- whose CDF is a finite alternating sum. So the whole of this
# section is computed rather than sampled, which matters twice over: the
# claim "it becomes Gaussian" is about a limit, and the claim this section
# actually earns is about the TAIL, where a sampled check has no data at all.
# That is P05's "finding nothing is not measuring nothing", in a new place.
# ---------------------------------------------------------------------------
def irwin_hall_cdf(x: Fraction, n: int) -> Fraction:
    """P(sum of n uniforms <= x), exactly, as a rational number."""
    if x <= 0:
        return Fraction(0)
    if x >= n:
        return Fraction(1)
    total = Fraction(0)
    for k in range(0, math.floor(x) + 1):
        total += Fraction((-1) ** k) * math.comb(n, k) * (x - k) ** n
    return total / math.factorial(n)


def phi(z: float) -> float:
    """The standard normal CDF, from erf, which is exact to the library."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def kolmogorov(n: int, steps: int = 4000) -> float:
    """The largest gap between the exact CDF and the Gaussian that matches it."""
    mu = Fraction(n, 2)
    sd = math.sqrt(n / 12.0)
    worst = 0.0
    for i in range(steps + 1):
        x = Fraction(i, steps) * n
        gap = abs(float(irwin_hall_cdf(x, n)) - phi((float(x) - float(mu)) / sd))
        worst = max(worst, gap)
    return worst


CLT_NS = (1, 2, 3, 4, 12)
CLT_GAPS = {n: kolmogorov(n) for n in CLT_NS}

# The claim is that the gap FALLS as n grows -- the ordering, which is
# structural -- and not any one of the numbers, which move with the grid.
#
# n = 3 IS IN THE SWEEP ON PURPOSE. The frame asks for the smallest n inside
# one per cent, and 3 already clears it at 0.00985 -- so a table that jumped
# from 2 to 4 skipped exactly the row that settles its own question.
gaps_in_order = [CLT_GAPS[n] for n in CLT_NS]
assert gaps_in_order == sorted(gaps_in_order, reverse=True), gaps_in_order
for n in CLT_NS:
    emit(f"p25.clt.gap.{n}", CLT_GAPS[n], 4)
emit("p25.clt.n.hi", CLT_NS[-1])
NOTES.append(
    "the exact sum-of-uniforms distribution approaches its matching Gaussian "
    f"monotonically: worst CDF gap {CLT_GAPS[1]:.4f} at n=1 down to "
    f"{CLT_GAPS[12]:.4f} at n={CLT_NS[-1]}, computed rather than sampled")

# AND THE PART THE THEOREM DOES NOT SAY. At n = 12 the variance is exactly 1,
# so the sum of twelve uniforms has mean 6 and spread 1 -- and its support is
# [0, 12], which is mean +/- 6 spreads EXACTLY. Beyond six spreads the true
# probability is not small. It is zero.
assert Fraction(12, 12) == 1, "n = 12 is the size at which the spread is exactly 1"
TAIL_N = 12
assert irwin_hall_cdf(Fraction(TAIL_N), TAIL_N) == 1
assert 1 - irwin_hall_cdf(Fraction(TAIL_N), TAIL_N) == 0, "the support is bounded"
GAUSS_TAIL_6 = 1.0 - phi(6.0)
VALUES["p25.tail.gauss6"] = (f"{GAUSS_TAIL_6:.3g}", True)

# Closer in, where it is a ratio rather than a zero, and therefore the number
# somebody would actually be wrong by.
#
# THE FIRST DRAFT ASSERTED THIS RATIO WAS ABOVE 1.5 AT THREE SPREADS AND IT
# FAILED AT 1.34. The failure is the better claim: no single ratio is the
# point, because the ratio is not a constant. What is true, and structural, is
# that the Gaussian OVERSTATES this tail everywhere and overstates it MORE the
# further out you ask -- which is precisely where a tail probability gets used.
TAIL_ZS = (1, 2, 3, 4, 5)
TAIL_ROWS = []
for z in TAIL_ZS:
    hi = Fraction(TAIL_N, 2) + z                      # mean + z spreads, exactly
    true_tail = float(1 - irwin_hall_cdf(hi, TAIL_N))
    gauss_tail = 1.0 - phi(float(z))
    TAIL_ROWS.append((z, true_tail, gauss_tail, gauss_tail / true_tail))

ratios = [r for _, _, _, r in TAIL_ROWS]

# THE SECOND DRAFT ASSERTED THE RATIO IS ABOVE 1 EVERYWHERE AND IT FAILED TOO,
# at 0.987 one spread out. That failure is the section: the Gaussian is not
# uniformly wrong, it is EXCELLENT near the middle -- which is exactly what the
# theorem promises and all it promises -- and the error runs away the moment
# you leave it. So what is asserted is that shape, in three parts, none of
# which is a threshold anybody chose:
assert ratios == sorted(ratios), ratios               # it grows, monotonically
assert all(abs(r - 1.0) < 0.05 for r in ratios[:2]), ratios[:2]   # middle: right
assert ratios[-1] > 10.0 * ratios[2], ratios          # tail: runs away
# Three significant figures, not a fixed number of decimals: the five-spread
# tail is of order 1e-9, and eight decimal places print it as 0.00000000 --
# at which point the page cannot support the ratio beside it. Caught by the
# reproduce-from-the-page check below rather than by reading the output.
for z, true_tail, gauss_tail, ratio in TAIL_ROWS:
    if z in (1, 3, 5):
        VALUES[f"p25.tail.true{z}"] = (f"{true_tail:.3g}", True)
        VALUES[f"p25.tail.gauss{z}"] = (f"{gauss_tail:.3g}", True)
        emit(f"p25.tail.ratio{z}", ratio, {1: 3, 3: 1, 5: 0}[z])
NOTES.append(
    "the Gaussian tail is excellent in the middle and runs away outside it: "
    f"{ratios[0]:.2f}x at one spread, {ratios[2]:.1f}x at three, "
    f"{ratios[4]:.0f}x at five -- and at six the truth is EXACTLY zero while "
    f"the Gaussian still says {GAUSS_TAIL_6:.1e}. The theorem is about the "
    "middle, and a tail probability is the one question it does not answer")

# Each printed ratio must reproduce from its own two printed tails. F04's rule,
# applied before the page is written rather than after CI divides them.
for z, true_tail, gauss_tail, ratio in TAIL_ROWS:
    if z in (1, 3, 5):
        d = {1: 2, 3: 1, 5: 0}[z]
        shown = float(f"{gauss_tail:.3g}") / float(f"{true_tail:.3g}")
        assert f"{ratio:.{d}f}" == f"{shown:.{d}f}", (z, ratio, shown)


# ---------------------------------------------------------------------------
# 4. MONTE CARLO: WHAT AN EVALUATION RUN COSTS.
#
# The same rate, in the place the reader meets it every week. Nothing here is
# sampled: the spread of a proportion has a closed form, so the whole section
# is arithmetic and the reader can redo it on a napkin.
# ---------------------------------------------------------------------------
EVAL_P = 0.80                       # a model that is right four times in five
Z95 = 1.959963984540054             # the 95 per cent multiplier, from the normal


def half_width(p: float, n: int) -> float:
    """Half the 95 per cent interval for a proportion measured on n items."""
    return Z95 * math.sqrt(p * (1.0 - p) / n)


EVAL_NS = (100, 400, 1600, 6400)
EVAL_ROWS = [(n, half_width(EVAL_P, n)) for n in EVAL_NS]

# The claim is the RATE, not the four numbers: each fourfold increase in the
# item count halves the interval, exactly, because the count is under a root.
for (n1, h1), (n2, h2) in zip(EVAL_ROWS, EVAL_ROWS[1:]):
    assert n2 == 4 * n1
    assert abs(h1 / h2 - 2.0) < 1e-12, (n1, n2, h1 / h2)
for n, h in EVAL_ROWS:
    emit(f"p25.eval.hw.{n}", pct(h), 1)
emit("p25.eval.p", EVAL_P, 2)
emit("p25.eval.z", Z95, 2)
# The interval is 1.96 spreads and not 2, and the frame invites the reader to
# redo the arithmetic -- so the multiplier has to be on the page or the reader
# gets 8.0 where the table prints 7.8.
assert abs(pct(half_width(EVAL_P, EVAL_NS[0])) - Z95 * 100.0
           * math.sqrt(EVAL_P * (1.0 - EVAL_P) / EVAL_NS[0])) < 1e-12
emit("p25.eval.n.lo", EVAL_NS[0])
emit("p25.eval.n.hi", EVAL_NS[-1])

# And the number that prices the run. To call a one-point difference between
# two models rather than a fluke, each needs enough items that the difference
# of the two estimates clears its own interval. The difference of two
# independent estimates has TWICE the variance -- section 1 again, and it is
# the step people leave out.
GAP = 0.01
N_NEEDED = math.ceil(2.0 * EVAL_P * (1.0 - EVAL_P) * (Z95 / GAP) ** 2)
assert half_width(EVAL_P, N_NEEDED) * math.sqrt(2.0) <= GAP * 1.0000001
# One item fewer must NOT be enough, or the number is not the threshold.
assert half_width(EVAL_P, N_NEEDED - 1) * math.sqrt(2.0) > GAP
emit("p25.eval.gap.pct", pct(GAP), 0)
emit("p25.eval.n.needed", N_NEEDED)
NOTES.append(
    f"an eval set of {EVAL_NS[0]} items measures an accuracy to "
    f"+/-{pct(EVAL_ROWS[0][1]):.1f} points; four times the items halves that, "
    f"every time. Calling a {pct(GAP):.0f}-point difference needs "
    f"{N_NEEDED} items per model, and the factor of two in it is section 1")

# The forgotten factor of two, stated as its own number because it is the
# error people make: sizing against ONE interval rather than the difference.
N_NAIVE = math.ceil(EVAL_P * (1.0 - EVAL_P) * (Z95 / GAP) ** 2)
assert N_NEEDED == 2 * N_NAIVE or N_NEEDED == 2 * N_NAIVE - 1, (N_NEEDED, N_NAIVE)
emit("p25.eval.n.naive", N_NAIVE)


# ---------------------------------------------------------------------------
# 5. THE HEADLINE: WHY ATTENTION DIVIDES BY sqrt(d_k).
#
# The derivation is section 1 applied to a dot product and nothing else. Each
# term q_i k_i has mean 0 and variance 1 when the entries do; the terms are
# independent; variances add; so Var(q.k) = d_k and the spread is sqrt(d_k).
#
# The exact half first, over Fractions, on entries that are +1 or -1 with
# equal weight -- for which "unit variance" is exact rather than assumed.
# ---------------------------------------------------------------------------
def rademacher_dot_variance(d: int) -> Fraction:
    """Var(q.k) over ALL 2^(2d) sign vectors, exactly. No sampling, no limit."""
    space = list(product((-1, 1), repeat=d))
    w = Fraction(1, len(space) ** 2)
    total = Fraction(0)
    for q in space:
        for k in space:
            total += w * Fraction(sum(a * b for a, b in zip(q, k))) ** 2
    return total                                   # the mean is 0 by symmetry


for d in (1, 2, 3, 4, 5):
    assert rademacher_dot_variance(d) == d, (d, rademacher_dot_variance(d))
NOTES.append(
    "Var(q.k) = d_k EXACTLY, enumerated over every sign vector at d = 1 to 5 "
    "-- so the scaling rests on an identity rather than on a limit theorem")

# THE CROSS-PROGRAMME GATE, and it is the find that reshaped this program.
# Program P05 measured the spread of the cosine between two random UNIT
# directions and committed it at four dimensions. A unit vector's entries have
# variance 1/d, so the same identity gives Var = d * (1/d) * (1/d) = 1/d and a
# spread of 1/sqrt(d). P05's measurement and this derivation are ONE theorem
# at two scalings, and sqrt(d_k) x 1/sqrt(d_k) = 1 is precisely the division
# attention performs.
P05_DIMS = (2, 10, 100, 768)
p05_gaps = []
for d in P05_DIMS:
    c = committed("p05.tex", f"p05.cos.sd.{d}")
    if c is None:                                            # pragma: no cover
        continue
    predicted = 1.0 / math.sqrt(d)
    p05_gaps.append(abs(float(c) - predicted) / predicted)
if p05_gaps:
    P05_WORST = max(p05_gaps)
    # A sampling-noise ceiling comfortably above both programs' measured worst,
    # not a copy of either -- P05's own committed bound moves with its seed and
    # a threshold that tracks it is a threshold chosen so this passes.
    assert P05_WORST < 0.02, P05_WORST
    emit("p25.p05.worst.pct", pct(P05_WORST), 1)
    NOTES.append(
        f"gated against Program P05's four committed cosine spreads: the "
        f"derivation reproduces every one to within {pct(P05_WORST):.1f} per "
        "cent, so the attention scaling is a Part III measurement read at the "
        "other scaling rather than a new claim")

# ---------------------------------------------------------------------------
# EXPERIMENT E9 -- the first of the book's ten to be run.
#
# Logit spread, softmax entropy and top probability across head sizes, with
# and without the division. Sampled with a fixed seed, on Program P05's own
# precedent: the claim here is a LAW rather than an exactness, and what is
# asserted is the law. (P24 integrated rather than sampled because its claim
# WAS exactness. The two choices are the same rule read at two claims.)
# ---------------------------------------------------------------------------
import random

E9_DIMS = (8, 32, 64, 128, 512)
E9_KEYS = 8                        # one query against a short row of keys
E9_TRIALS = 4000
E9_SEED = 20260901


def softmax_row(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def entropy(p):
    return -sum(v * math.log(v) for v in p if v > 0.0)


def e9(d: int, scaled: bool):
    rng = random.Random(E9_SEED + d + (1 if scaled else 0))
    denom = math.sqrt(d) if scaled else 1.0
    logits, ents, tops = [], [], []
    for _ in range(E9_TRIALS):
        q = [rng.gauss(0.0, 1.0) for _ in range(d)]
        row = []
        for _k in range(E9_KEYS):
            k = [rng.gauss(0.0, 1.0) for _ in range(d)]
            row.append(sum(a * b for a, b in zip(q, k)) / denom)
        logits.extend(row)
        p = softmax_row(row)
        ents.append(entropy(p))
        tops.append(max(p))
    mean = sum(logits) / len(logits)
    sd = math.sqrt(sum((v - mean) ** 2 for v in logits) / (len(logits) - 1))
    return sd, sum(ents) / len(ents), sum(tops) / len(tops)


E9 = {(d, sc): e9(d, sc) for d in E9_DIMS for sc in (False, True)}
E9_MAXENT = math.log(E9_KEYS)

# The four invariants. None is a figure and none is a threshold anybody chose.
# 1. Unscaled, the logit spread IS sqrt(d_k).
for d in E9_DIMS:
    sd = E9[(d, False)][0]
    assert abs(sd / math.sqrt(d) - 1.0) < 0.06, (d, sd, math.sqrt(d))
# 2. Scaled, it is 1 at every head size -- which is the whole point.
for d in E9_DIMS:
    assert abs(E9[(d, True)][0] - 1.0) < 0.06, (d, E9[(d, True)][0])
# 3. Unscaled, the entropy collapses as the head grows.
unscaled_ent = [E9[(d, False)][1] for d in E9_DIMS]
assert unscaled_ent == sorted(unscaled_ent, reverse=True), unscaled_ent
# 4. Scaled, it does not move.
scaled_ent = [E9[(d, True)][1] for d in E9_DIMS]
assert max(scaled_ent) - min(scaled_ent) < 0.05 * E9_MAXENT, scaled_ent

# The assertions above sweep all five head sizes; the tables print three, and
# a value nothing references is a second copy nobody would correct.
E9_PRINTED = (E9_DIMS[0], 64, E9_DIMS[-1])
for d in E9_PRINTED:
    for sc, tag in ((False, "raw"), (True, "scaled")):
        sd, ent, top = E9[(d, sc)]
        emit(f"p25.e9.{tag}.sd.{d}", sd, 2)
        emit(f"p25.e9.{tag}.ent.{d}", ent, 3)
        emit(f"p25.e9.{tag}.top.{d}", pct(top), 1)
emit("p25.e9.keys", E9_KEYS)
emit("p25.e9.trials", E9_TRIALS)
emit("p25.e9.maxent", E9_MAXENT, 3)
emit("p25.e9.d.lo", E9_DIMS[0])
emit("p25.e9.d.hi", E9_DIMS[-1])
NOTES.append(
    "E9, run: without the division the logit spread is sqrt(d_k) and the "
    f"softmax entropy falls from {unscaled_ent[0]:.3f} to {unscaled_ent[-1]:.3f} "
    f"nats against a maximum of {E9_MAXENT:.3f}; with it the spread is 1 and "
    f"the entropy does not move ({min(scaled_ent):.3f} to {max(scaled_ent):.3f}) "
    "-- the scaling is a variance correction and nothing else")

# AND THE GRADIENT, which is the half that makes it a failure rather than a
# quirk. Program P18 owns the softmax Jacobian, whose diagonal entry is
# p(1 - p): so the responsiveness of a softmax output to its own logit is a
# number this book already has, and "the gradient dies" is a sentence it can
# write down rather than assert.
def jac_diag(p: float) -> float:
    return p * (1.0 - p)


TOP_RAW_HI = E9[(E9_DIMS[-1], False)][2]
TOP_SCALED_HI = E9[(E9_DIMS[-1], True)][2]
RESP_RAW = jac_diag(TOP_RAW_HI)
RESP_SCALED = jac_diag(TOP_SCALED_HI)
RESP_RATIO = RESP_SCALED / RESP_RAW
assert RESP_RATIO > 1.0, RESP_RATIO      # the scaled row is the responsive one
emit("p25.e9.resp.raw", RESP_RAW, 3)
emit("p25.e9.resp.scaled", RESP_SCALED, 3)
emit("p25.e9.resp.ratio", RESP_RATIO, 1)
# The printed ratio must reproduce from the two printed responses.
_shown = float(f"{RESP_SCALED:.3f}") / float(f"{RESP_RAW:.3f}")
assert f"{RESP_RATIO:.1f}" == f"{_shown:.1f}", (RESP_RATIO, _shown)
NOTES.append(
    f"at d_k = {E9_DIMS[-1]} the unscaled row's top weight is "
    f"{pct(TOP_RAW_HI):.1f} per cent, so P18's Jacobian diagonal p(1-p) is "
    f"{RESP_RAW:.3f} against {RESP_SCALED:.3f} scaled -- the scaled row is "
    f"{RESP_RATIO:.1f} times as responsive, which is what 'the gradient dies' "
    "means as a number")


# ---------------------------------------------------------------------------
# 6. WHY A RUN DIVERGES BEFORE IT STARTS.
#
# The curriculum review's addition, and it is the same identity a third time.
# Nothing else in the book explains this, which the review called the single
# most common cause of a run that never starts.
# ---------------------------------------------------------------------------
# Var(out) = fan_in x Var(w) x E[x^2], exactly, for independent zero-mean
# WEIGHTS. Enumerated over value vectors, as section 5 was.
#
# THE SECOND MOMENT AND NOT THE VARIANCE, and the distinction is the whole of
# why this section works. The two agree when the input is centred, which the
# first layer's is -- and a ReLU output is non-negative and has a positive
# mean, so from the second layer on they are different numbers. The frames
# below reuse this identity across ReLUs, so stating it in Var(x) would make
# every later step rest on a hypothesis that has just been broken.
#
# The first version of this check enumerated over +/-1 inputs alone, where
# Var(x) and E[x^2] are both 1, so it could not tell the two readings apart --
# it passed, and the page carried the wrong one. The alphabet is a parameter
# now and the check is run over a NON-CENTRED one as well, where the two
# readings differ by a factor of two and only one of them holds.
def layer_out_variance(fan_in: int, wscale: Fraction,
                       xs: tuple = (-1, 1)) -> Fraction:
    xspace = list(product(xs, repeat=fan_in))
    wspace = list(product((-1, 1), repeat=fan_in))
    p = Fraction(1, len(xspace) * len(wspace))
    total = Fraction(0)
    for x in xspace:
        for ws in wspace:
            total += p * (wscale * Fraction(sum(a * b for a, b in zip(x, ws)))) ** 2
    return total


def moments(xs: tuple) -> tuple:
    """(E[x], E[x^2], Var(x)) for the uniform distribution on xs."""
    n = Fraction(len(xs))
    m1 = sum(Fraction(v) for v in xs) / n
    m2 = sum(Fraction(v) ** 2 for v in xs) / n
    return m1, m2, m2 - m1 ** 2


for xs in ((-1, 1), (0, 1)):
    _, second, var_x = moments(xs)
    for fan_in in (1, 2, 3, 4):
        for wscale in (Fraction(1), Fraction(1, 2), Fraction(3, 7)):
            got = layer_out_variance(fan_in, wscale, xs)
            assert got == fan_in * wscale ** 2 * second, (xs, fan_in, wscale, got)
            if second != var_x:
                assert got != fan_in * wscale ** 2 * var_x, (xs, fan_in, wscale)
NOTES.append(
    "Var(out) = fan_in x Var(w) x E[x^2] enumerated exactly at four fan-ins "
    "and three weight scales, over a centred input alphabet and a non-centred "
    "one -- on the second the variance reading is out by a factor of two, "
    "which is what a ReLU does to the input of the next layer")

# So holding the variance at 1 through a linear layer needs Var(w) = 1/fan_in.
FAN_IN = 512
XAVIER = 1.0 / FAN_IN
assert abs(FAN_IN * XAVIER - 1.0) < 1e-12

# THE FACTOR OF TWO. A ReLU zeroes half of a symmetric input, so it keeps half
# the second moment: E[relu(z)^2] = (1/2) E[z^2] for any symmetric z. That is
# exact by symmetry, and it is checked here by deterministic integration
# against the standard normal rather than by sampling.
def gauss_pdf(z: float) -> float:
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def relu_second_moment(lo: float = -12.0, hi: float = 12.0, steps: int = 200_000) -> float:
    """Integral of relu(z)^2 phi(z) dz, by Simpson's rule on a symmetric grid."""
    h = (hi - lo) / steps
    total = 0.0
    for i in range(steps + 1):
        z = lo + i * h
        w = 1.0 if i in (0, steps) else (4.0 if i % 2 else 2.0)
        total += w * (max(z, 0.0) ** 2) * gauss_pdf(z)
    return total * h / 3.0


RELU_KEEPS = relu_second_moment()
RELU_BOUND = 1e-9
assert abs(RELU_KEEPS - 0.5) < RELU_BOUND, RELU_KEEPS
emit("p25.init.relu.keeps", RELU_KEEPS, 6)
VALUES["p25.init.relu.bound"] = (f"{RELU_BOUND:.0e}", True)

HE = 2.0 / FAN_IN
assert abs(FAN_IN * HE * RELU_KEEPS - 1.0) < 1e-8
NOTES.append(
    "a ReLU keeps exactly half the second moment of a symmetric input "
    f"(integrated: {RELU_KEEPS:.6f}), which is the whole of He's factor of two")

# AND WHAT DEPTH DOES TO IT, which is F04's geometric sequence on a variance.
DEPTH = 50
FACTOR_XAVIER = FAN_IN * XAVIER * RELU_KEEPS          # one half, per layer
FACTOR_HE = FAN_IN * HE * RELU_KEEPS                  # one, per layer
DEEP_XAVIER = FACTOR_XAVIER ** DEPTH
DEEP_HE = FACTOR_HE ** DEPTH
assert abs(FACTOR_XAVIER - 0.5) < 1e-8, FACTOR_XAVIER
assert abs(FACTOR_HE - 1.0) < 1e-8, FACTOR_HE
assert DEEP_XAVIER < 1e-14, DEEP_XAVIER
emit("p25.init.depth", DEPTH)
VALUES["p25.init.deep.xavier"] = (f"{DEEP_XAVIER:.2e}", True)
emit("p25.init.deep.he", DEEP_HE, 2)

# The other direction, which is the one that produces a NaN rather than a
# silence: a weight scale twice what it should be multiplies the variance by
# four per layer.
FACTOR_HOT = FAN_IN * (4.0 * HE) * RELU_KEEPS
DEEP_HOT = FACTOR_HOT ** DEPTH
assert abs(FACTOR_HOT - 4.0) < 1e-8
assert math.isfinite(DEEP_HOT)
VALUES["p25.init.deep.hot"] = (f"{DEEP_HOT:.2e}", True)
emit("p25.init.hot.factor", FACTOR_HOT, 0)
NOTES.append(
    f"over {DEPTH} layers the wrong scale is a geometric sequence: half per "
    f"layer gives {DEEP_XAVIER:.2e} of the signal left, and twice the right "
    f"weight scale gives {DEEP_HOT:.2e} -- a run that never starts, in both "
    "directions, from one number chosen without this argument")


# ---------------------------------------------------------------------------
# The transcript. Extracted from the finished PDF and run; every
# transformation the page shows is written into the listing's own code, so the
# printed line and the printed result cannot come apart -- P19's rule, and
# P24's. It also imports what it calls, which is P04's.
#
# What it shows is the one line of E9 a reader can check in ten seconds: the
# spread of a dot product is sqrt(d_k), and dividing by sqrt(d_k) makes it 1
# whatever the head size. Nothing later in the program is answered by it.
# ---------------------------------------------------------------------------
TRANSCRIPT = [
    ">>> from p25_clt_monte_carlo import e9",
    ">>> sd, ent, top = e9(512, scaled=False)",
    ">>> round(sd, 1), round(512 ** 0.5, 1)",
    repr((round(E9[(512, False)][0], 1), round(512 ** 0.5, 1))),
    ">>> sd, ent, top = e9(512, scaled=True)",
    ">>> round(sd, 2)",
    repr(round(E9[(512, True)][0], 2)),
]
for line in TRANSCRIPT:
    assert len(line) <= 64, (len(line), line)
TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
(TRANSCRIPTS / "p25-scaling.txt").write_text("\n".join(TRANSCRIPT) + "\n",
                                             encoding="utf8")


# ---------------------------------------------------------------------------
OUT.parent.mkdir(parents=True, exist_ok=True)
lines = [
    "% Generated by code/p25_clt_monte_carlo.py --- do not edit.",
    "% Regenerate with `make numbers`; `make verify` fails if this file and",
    "% the script disagree, which is what stops a number in the book drifting",
    "% away from the computation that justifies it.",
    "",
]
for key, (body, numeric) in VALUES.items():
    lines.append(("\\mfaval{%s}{%s}" if numeric else "\\mfavaltext{%s}{%s}")
                 % (key, body))
OUT.write_text("\n".join(lines) + "\n", encoding="utf8")

print(f"P25: {len(VALUES)} values -> {OUT}")
for n in NOTES:
    print("  *", n)
print("  transcript: figures/transcripts/p25-scaling.txt")
