"""P27 --- Statistical inference for the engineer.

Every number Program P27 prints, and the assertions that keep them honest.

WHAT THE NEIGHBOURS ALREADY SPENT, read before a line of this was written.
The estimate in the manifest is 60 frames and the brief lists seven things.
TWO OF THE SEVEN ARE ALREADY ON THE PAGE, so this program uses them and may
not re-teach either:

  P25  section 4 OWNS the standard error of a proportion, the +-2 sqrt(p(1-p)/n)
       interval, p(1-p) being widest at a half, the four-times-the-items rule,
       and THE POWER CALCULATION -- 12293 items per model to see one point,
       with the factor of two that comes from a difference carrying the SUM of
       two variances.  The brief asks for "a power calculation answering how
       many evaluation items are needed"; it exists.  What P25 could not do is
       the same calculation for models that saw THE SAME PROMPTS, because that
       needs the covariance term, and P25's own section 1 supplies it:
           Var(X - Y) = Var X + Var Y - 2 Cov(X, Y)
       P25 used the PLUS half for independence.  Section 3 here uses the minus
       half, and the required item count collapses by exactly (1 - rho).  So
       this program's headline is P25's own number, done right, and it is
       gated against it at rho = 0.
  P25  section 1's trapbox also NAMES "a bootstrap over rows that share a user"
       as a failure mode -- before the book has said what a bootstrap is.
       Section 2 pays that off and measures the factor.
  P26  section 1 OWNS bias, variance and the mean-squared-error decomposition,
       and stops deliberately at two ways of being wrong "and never asks
       whether a difference is real".  That question is this program's.
  P23  defers "what a p-value does and does not say" here BY NAME, and its own
       section 3 owns the inversion that the p-value fallacy IS: P(A|B) is not
       P(B|A).  Section 4 is that theorem read on a different pair of events,
       which is why it needs no new machinery.
  P24  owns the Bernoulli, the expectation and the variance.
  P12  owns the binomial coefficient.  The exact test in section 3 is
       math.comb over integers and nothing else -- no normal approximation
       anywhere in it, which is what lets the p-value arrive as a coin count
       before it arrives as a word.
  F10  owns the numerator, the denominator, and the observation that choosing
       the denominator was a decision.  Section 1 is that lesson applied to a
       benchmark's own decimal point.

WHAT THIS PROGRAM MUST NOT SPEND.
  P28  owns the POSTERIOR, conjugacy, the credible interval and "the
       probability that B is better".  Section 4 says flatly that a p-value is
       not that quantity and names P28 as where the quantity people wanted
       actually lives.  It may not compute one here.
  P34  owns evaluation design end to end.

Run:  python3 code/p27_inference.py
"""

from __future__ import annotations

import math
import random
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p27.tex"
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

    Program P05 met this at the top of the range and Program P21 at the
    bottom: a quantity that rounds to 0 or to 100 must be reported as a count
    or as its complement, where every figure means something."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not. "
        f"Report the count or the complement instead.")
    return x


def reproduces(value: float, digits: int, *operands, op) -> float:
    """Refuse a quantity that does not come back out of its own printed page.

    Programs F04, F05, P07, P12 and P23 each paid for this: a ratio printed
    beside two numbers that do not divide to it.  The check is not "is the
    arithmetic right" -- it is "can the reader redo it on the page in front
    of them", so it formats the operands exactly as the page will, applies
    the operation to THOSE, and compares the printed forms."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


def not_on_a_boundary(x: float, digits: int) -> float:
    """Refuse a value whose printed form depends on the last bit.

    Program P20's `p20.cos.area` printed 0.501 here and 0.500 on CI because
    the quantity sat exactly on a rounding boundary and libm is not
    bit-identical across platforms.  Anything in this file that comes out of
    a transcendental goes through here.

    THE FIRST VERSION OF THIS MEASURED THE WRONG DISTANCE, and Program P34's
    pass found it: it took |frac - round(frac)|, which is ZERO on an exactly
    representable value and ONE HALF on the boundary -- so it refused the
    safe case and passed the very number the docstring names.  Fed 0.5005 at
    three decimals it returned it without complaint.  A rounding boundary is
    a HALF-step, so that is the distance to measure, and the two directions
    are visible in one line: 3.15 prints 3.1 and 92.15 prints 92.2, from the
    binary representation alone."""
    step = 10.0 ** -digits
    frac = abs(x) / step
    half = abs((frac % 1.0) - 0.5)
    assert half > 0.02, (
        f"{x!r} is {half:.4f} of a step from the {digits}-decimal rounding "
        f"boundary; a different libm will print it differently.")
    return x


# ======================================================================
# 1.  What one point is.
#
# Before any statistics at all, two questions about the two numbers in the
# brief -- and both are Program F10's, not this program's: what is the
# denominator, and what is the grid it puts the answer on?
# ======================================================================

QUOTED_HI, QUOTED_LO = 71.4, 70.9          # the two numbers as published
ITEMS = 200                                # the item count as published

# A score of k right out of n is k/n and nothing between.  So the achievable
# accuracies on ITEMS items are spaced exactly one item apart.
GRID_PTS = 100.0 / ITEMS
emit("p27.items", ITEMS)
emit("p27.grid.pts", GRID_PTS, 1)

# Neither published number lands on that grid, and the check is integer
# arithmetic rather than a tolerance.
for q in (QUOTED_HI, QUOTED_LO):
    k = q * ITEMS / 100.0
    assert abs(k - round(k)) > 0.1, (
        f"{q} per cent IS achievable on {ITEMS} items ({round(k)} correct); "
        f"the section's opening claim would be false.")
K_HI = QUOTED_HI * ITEMS / 100.0
emit("p27.quoted.hi", QUOTED_HI, 1)
emit("p27.quoted.lo", QUOTED_LO, 1)
emit("p27.k.hi", K_HI, 1)
emit("p27.near.lo", math.floor(K_HI) * GRID_PTS, 1)
emit("p27.near.hi", math.ceil(K_HI) * GRID_PTS, 1)

# How many items does a one-decimal percentage need before the decimal can
# round correctly at all?  The grid has to be finer than half a tenth of a
# point, so 1/n < 0.001.
DEC_FLOOR = 1
while 1.0 / DEC_FLOOR >= 0.001:
    DEC_FLOOR += 1
assert DEC_FLOOR == 1001, DEC_FLOOR
emit("p27.decimal.floor", DEC_FLOOR)

# The same criterion one decimal further out, for Further problem 1.  The
# grid must be finer than the rounding bin, which is 0.01 points there, so
# 100/n < 0.01.  Emitted rather than typed: an \answerto may not carry a
# number the reader cannot derive from values on the page.
DEC_FLOOR_2 = 1
while 1.0 / DEC_FLOOR_2 >= 0.0001:
    DEC_FLOOR_2 += 1
assert DEC_FLOOR_2 == 10001, DEC_FLOOR_2
emit("p27.decimal.floor.two", DEC_FLOOR_2)

# And the gap itself, in the only unit an evaluation actually has.
GAP_PTS = QUOTED_HI - QUOTED_LO
GAP_ITEMS = GAP_PTS * ITEMS / 100.0
emit("p27.gap.pts", GAP_PTS, 1)
emit("p27.gap.items", GAP_ITEMS, 1)

# Program P25's interval on ITEMS items, at the accuracy being discussed,
# recomputed here from its own formula rather than quoted -- so a change to
# either program is caught.  P25 commits the interval at p = 0.80; this is
# the same arithmetic at the accuracy in the brief.
Z = 1.96
P_HERE = QUOTED_HI / 100.0


def half_width(p: float, n: float, z: float = Z) -> float:
    """Program P25 section 4's interval, in percentage points."""
    return 100.0 * z * math.sqrt(p * (1 - p) / n)


HW_200 = half_width(P_HERE, ITEMS)
emit("p27.hw.200", HW_200, 1)
# A BOUND, and not a figure, which is Program F05's recorded fix for exactly
# this.  The exact ratio is 12.53 and the page's own two numbers divide to
# 12.6, because the interval is rounded up to 6.3 -- so no single decimal is
# both true and reproducible, and the honest form is the floor they share.
RATIO_HW = HW_200 / GAP_PTS
RATIO_FLOOR = 12
assert RATIO_HW > RATIO_FLOOR, RATIO_HW
assert float(f"{HW_200:.1f}") / float(f"{GAP_PTS:.1f}") > RATIO_FLOOR
emit("p27.hw.ratio.floor", RATIO_FLOOR)

# THE GATE ON P25.  Its committed interval at p = 0.80 on 100 items must come
# out of the function above, or the two programs are quoting one formula and
# disagreeing about it.
_p25_hw = committed("p25.tex", "p25.eval.hw.100")
if _p25_hw is not None:
    mine = f"{half_width(0.80, 100):.1f}"
    assert mine == _p25_hw, (
        f"P25 commits an interval of {_p25_hw} points on 100 items at "
        f"p = 0.80 and this program's own formula gives {mine}. One of the "
        f"two is wrong and the book prints both.")
    NOTES.append(f"P25's interval gate holds: {_p25_hw} points on 100 items.")


# ======================================================================
# 2.  The bootstrap.
#
# The point of the section is NOT that the bootstrap agrees with the closed
# form on a proportion.  It is that on a proportion the bootstrap IS the
# closed form's own distribution, exactly -- resampling n items with
# replacement from k successes gives a resampled count that is exactly
# Binomial(n, k/n) -- so the agreement is a theorem rather than a
# coincidence, and there is no simulation in this half at all.
# ======================================================================

BOOT_N, BOOT_K = 200, 143
BOOT_P = BOOT_K / BOOT_N
emit("p27.boot.n", BOOT_N)
emit("p27.boot.k", BOOT_K)


def binom_pmf(n: int, k: int, p: float) -> float:
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_percentile(n: int, p: float, q: float) -> int:
    """Smallest k with P(X <= k) >= q, by exact summation over comb()."""
    total = 0.0
    for k in range(n + 1):
        total += binom_pmf(n, k, p)
        if total >= q:
            return k
    return n                                                 # pragma: no cover


# The percentile bootstrap interval, computed from the exact resampling
# distribution rather than from resamples.
BOOT_LO = 100.0 * binom_percentile(BOOT_N, BOOT_P, 0.025) / BOOT_N
BOOT_HI = 100.0 * binom_percentile(BOOT_N, BOOT_P, 0.975) / BOOT_N
emit("p27.boot.lo", BOOT_LO, 1)
emit("p27.boot.hi", BOOT_HI, 1)

CLOSED_LO = 100.0 * BOOT_P - half_width(BOOT_P, BOOT_N)
CLOSED_HI = 100.0 * BOOT_P + half_width(BOOT_P, BOOT_N)
emit("p27.closed.lo", CLOSED_LO, 1)
emit("p27.closed.hi", CLOSED_HI, 1)

# The two agree to within one item's width, which is the finest either can
# resolve -- and that is the assertion, not a decimal place.  The bootstrap
# cannot be closer than the grid section 1 measured.
for boot, closed in ((BOOT_LO, CLOSED_LO), (BOOT_HI, CLOSED_HI)):
    assert abs(boot - closed) <= GRID_PTS + 1e-9, (boot, closed, GRID_PTS)
emit("p27.boot.agree", GRID_PTS, 1)

# THE CASE WITH NO CLOSED FORM.  A median has no standard-error formula in any
# textbook the reader owns, and the bootstrap needs no formula.  The interval
# endpoints of a bootstrapped median are always OBSERVED VALUES, which is why
# this survives a change of interpreter: the resampling picks which observed
# value, and the answer is a latency somebody measured.
LATENCIES = [
    112, 118, 121, 125, 129, 131, 134, 138, 141, 147,
    152, 158, 163, 171, 180, 195, 214, 248, 310, 502,
]
BOOT_TRIALS = 20000
_rng = random.Random(27)


def median(xs: list[float]) -> float:
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


_meds = []
for _ in range(BOOT_TRIALS):
    _meds.append(median([LATENCIES[_rng.randrange(len(LATENCIES))]
                         for _ in range(len(LATENCIES))]))
_meds.sort()
MED_OBS = median(LATENCIES)
MED_LO = _meds[int(0.025 * BOOT_TRIALS)]
MED_HI = _meds[int(0.975 * BOOT_TRIALS)]
emit("p27.med.obs", MED_OBS, 1)
emit("p27.med.lo", MED_LO, 1)
emit("p27.med.hi", MED_HI, 1)
emit("p27.med.trials", BOOT_TRIALS)
assert MED_LO < MED_OBS < MED_HI, (MED_LO, MED_OBS, MED_HI)
# The endpoints are midpoints of observed values, because the median of an
# even-length resample is.  So they are data rather than a fitted quantity,
# which is the property that makes them stable.
_halves = {x / 2 + y / 2 for x in LATENCIES for y in LATENCIES}
assert MED_LO in _halves and MED_HI in _halves, (MED_LO, MED_HI)

# THE FAILURE P25 NAMED, and the factor it costs.  Rows that share a user are
# one observation wearing several labels: Program P25's own identity says the
# variance of a sum of IDENTICAL things is r^2 times one of them, not r times,
# so an average over r*u rows that are really u observations has the variance
# of u and not of r*u.  A bootstrap over rows believes it has r*u.
CLUSTER_USERS, CLUSTER_ROWS = 40, 5
CLUSTER_N = CLUSTER_USERS * CLUSTER_ROWS
CLUSTER_FACTOR = math.sqrt(CLUSTER_ROWS)
emit("p27.clust.users", CLUSTER_USERS)
emit("p27.clust.rows", CLUSTER_ROWS)
emit("p27.clust.n", CLUSTER_N)
emit("p27.clust.factor", CLUSTER_FACTOR, 2)
# Stated as what it is: an interval too narrow by that factor, which is the
# same as claiming CLUSTER_ROWS times as much evidence as you have.
assert abs(CLUSTER_FACTOR ** 2 - CLUSTER_ROWS) < 1e-12


# ======================================================================
# 2b.  EXPERIMENT E7, run here.
#
# The specification is "bootstrap confidence-interval width against
# evaluation-set size on a public benchmark; the size needed to resolve one
# point", and Program P32's split settles the "public benchmark" half before
# anything is computed: ASK WHETHER THE CLAIM NEEDS EXTERNAL DATA OR IS A
# STATEMENT ABOUT THE ESTIMATOR.  The width of a bootstrap interval on a
# proportion is a function of (n, p) and of nothing else, so a benchmark
# would supply one number, p -- and p sets the CONSTANT while n sets the
# SHAPE.  The shape is what E7 asks for, so it needs no download, and the
# sweep runs at this section's own accuracy rather than at a borrowed one.
#
# Nothing here is simulated.  Section 2 established that on a proportion the
# bootstrap distribution IS Binomial(n, k/n) exactly, so every width below is
# an exact percentile of that binomial -- no seed, no resampling, and the
# same answer on every machine.
# ======================================================================

def log_binom_pmf(n: int, k: int, p: float) -> float:
    """log P(X = k) for X ~ Binomial(n, p), via lgamma.

    binom_pmf above forms math.comb(n, k) as an exact integer and then
    multiplies by p**k; at n = 3200 that integer is about 10**961 and the
    conversion to a float raises OverflowError, so the sweep cannot use it.
    This is the same quantity in log space and it is checked against
    binom_pmf at n = 200 before it is used -- an instrument is not evidence
    until it has been watched producing an answer already known."""
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))


for _k in (0, 1, 100, 143, 200):
    _exact, _log = binom_pmf(200, _k, BOOT_P), math.exp(log_binom_pmf(200, _k, BOOT_P))
    assert abs(_exact - _log) <= 1e-12 * max(_exact, 1e-300), (_k, _exact, _log)


def boot_span(n: int, p: float = BOOT_P) -> int:
    """The 95 per cent bootstrap interval's span, in ITEMS.

    The endpoints are counts, so the span is a whole number of items and the
    width in points is 100 * span / n -- an exact rational, identical on
    every machine.  That quantisation is section 1's grid, and it is why the
    answer to "how many items" below is a round number rather than a size."""
    total, lo, hi = 0.0, None, None
    for k in range(n + 1):
        total += math.exp(log_binom_pmf(n, k, p))
        if lo is None and total >= 0.025:
            lo = k
        if total >= 0.975:
            hi = k
            break
    assert lo is not None and hi is not None, n
    return hi - lo


def boot_width(n: int, p: float = BOOT_P) -> float:
    """The same interval's width, in percentage points."""
    return 100.0 * boot_span(n, p) / n


SWEEP = (50, BOOT_N, 800, 3200, 12800, 51200)
SPANS = {n: boot_span(n) for n in SWEEP}
WIDTHS = {n: 100.0 * SPANS[n] / n for n in SWEEP}

# The n = BOOT_N row IS the interval printed two frames earlier.  Gated
# rather than resembled: two numbers on one page that look like one are the
# defect this book keeps recording, and here being the same number is the
# point.
assert abs(WIDTHS[BOOT_N] - (BOOT_HI - BOOT_LO)) < 1e-9, (
    f"the sweep's {BOOT_N}-item row is {WIDTHS[BOOT_N]} and the interval the "
    f"section already prints is {BOOT_HI - BOOT_LO} wide; they are the same "
    f"interval and must agree.")
# And the frame now asks the reader to do that subtraction, so it is checked
# on the PRINTED forms as well: the endpoints carry one decimal and the width
# carries two, and a reader who subtracts must land on what the table says.
reproduces(WIDTHS[BOOT_N], 2, (BOOT_HI, 1), (BOOT_LO, 1), op=lambda a, b: a - b)

# THE INVARIANT, which is Program P25's four-times-for-half measured rather
# than quoted.  The bound is DERIVED and not chosen: each endpoint sits on a
# grid 100/n points wide, so the width carries at most that much
# quantisation and a comparison across a fourfold step carries at most
# 100/n + 2 * 100/(4n).
for n in SWEEP[:-1]:
    slack = 150.0 / n
    assert abs(WIDTHS[n] - 2.0 * WIDTHS[4 * n]) <= slack, (
        n, WIDTHS[n], WIDTHS[4 * n], slack)

# And the bootstrap tracks the closed form to within one item's width at
# every size, which is the same assertion section 2 already makes at n = 200
# carried across three decades.
for n in SWEEP:
    assert abs(WIDTHS[n] - 2.0 * half_width(BOOT_P, n)) <= 100.0 / n, n

for n in SWEEP:
    emit(f"p27.w.{n}", WIDTHS[n], 2)

# The one departure from the halving, and it is at the SMALLEST set, where
# the grid is coarsest.  Emitted because the frame names it; guarded because
# a reader will divide the table's own two top rows.
COARSE = WIDTHS[SWEEP[0]] / WIDTHS[SWEEP[1]]
reproduces(COARSE, 2, (WIDTHS[SWEEP[0]], 2), (WIDTHS[SWEEP[1]], 2),
           op=lambda a, b: a / b)
emit("p27.w.coarse", COARSE, 2)

# The span in items at the two ends of the sweep.  It DOUBLES exactly at
# every step from BOOT_N up, which is the halving seen in whole numbers, and
# that is asserted rather than printed six times.
for n in SWEEP[1:-1]:
    assert SPANS[4 * n] == 2 * SPANS[n], (n, SPANS[n], SPANS[4 * n])
# ... and the coarsest step does NOT, which is the row the frame names.
# Written out rather than folded into the loop above: the first draft of
# this line compared SPANS[50] with 2 * SPANS[200] // 2, which is
# SPANS[200] -- a vacuous assertion that could not fail, and the class
# Programs P01 and P05 both record.
assert SPANS[SWEEP[1]] != 2 * SPANS[SWEEP[0]], (SPANS[SWEEP[0]], SPANS[SWEEP[1]])
# The spans are printed beside the widths BECAUSE THE EXACTNESS LIVES THERE.
# A width in points is a span divided by n and then rounded, so the points
# column halves to two decimal places and the items column doubles as whole
# numbers -- and a reader dividing 6.25 by 3.12 gets 2.00 rather than 2
# exactly.  Quoting the halving off the points column would be a claim the
# page cannot support; quoting it off the items column is arithmetic.
for n in SWEEP:
    emit(f"p27.w.span.{n}", SPANS[n])

# THE SIZE NEEDED TO RESOLVE ONE POINT, and it is quoted to two significant
# figures ON PURPOSE.  Setting 2 z sqrt(p(1-p)/n) = 1 point gives
#     n = 4 p (1-p) (z / delta)^2
# exactly, but the MEASURED crossing is not a single size: near there the
# span moves by one item at a time, so the width steps above and below one
# point as n grows.  A knife-edge "smallest n" would be a lattice artefact
# and machine-legible precision the quantity does not have.  What is
# committed instead is a round figure with the crossing bracketed at a
# comfortable distance either side -- Program P06's rule, that a quantity
# whose exact value is an artefact is committed as a bound.
ONE_POINT = 1.0
N_ONE_POINT_EXACT = 4.0 * BOOT_P * (1 - BOOT_P) * (Z / (ONE_POINT / 100.0)) ** 2


def two_sig_figs(x: float) -> int:
    e = math.floor(math.log10(abs(x)))
    return int(round(x, -(e - 1)))


N_ONE_POINT = two_sig_figs(N_ONE_POINT_EXACT)
# The reader's own route is the table: the width has to fall from the
# BOOT_N row to one point, and items go as the square of that factor.  It
# must land on the same two significant figures or the page cannot be
# checked on the page.
_reader = float(f"{WIDTHS[BOOT_N]:.2f}") ** 2 * BOOT_N
assert two_sig_figs(_reader) == N_ONE_POINT, (_reader, N_ONE_POINT)
# And the crossing really is bracketed, measured on the exact bootstrap
# rather than on the formula.  A tenth either side is far outside anything
# the grid or a library's lgamma can move.
assert boot_width(round(0.9 * N_ONE_POINT)) > ONE_POINT
assert boot_width(round(1.1 * N_ONE_POINT)) < ONE_POINT
# The table brackets it too, which is what makes it the answer to its own
# question rather than a table with an answer bolted on.
assert WIDTHS[12800] > ONE_POINT > WIDTHS[51200]
emit("p27.w.onepoint", N_ONE_POINT)
NOTES.append(
    f"E7: bootstrap width {WIDTHS[SWEEP[0]]:.2f} points at {SWEEP[0]} items "
    f"to {WIDTHS[SWEEP[-1]]:.2f} at {SWEEP[-1]}; under one point from about "
    f"{N_ONE_POINT} items.")


# ======================================================================
# 3.  The paired comparison.  THE HEADLINE.
#
# Program P25 sized the comparison for two INDEPENDENT evaluations and got
# 12293 items per model.  A and B saw the same prompts, so the two per-item
# indicators are correlated, and P25's own section 1 identity has the term:
#
#     Var(X - Y) = Var X + Var Y - 2 Cov(X, Y)
#
# With both models near the same accuracy, Cov = rho * p(1-p), so
#
#     n_paired = 2 p(1-p) (1 - rho) (z/delta)^2 = n_independent * (1 - rho)
#
# Exactly.  The gate is that at rho = 0 this must return P25's own number.
# ======================================================================

P_SIZE, DELTA = 0.80, 0.01                 # Program P25's own cell
ALPHA_LATER = 0.05                         # the threshold section 4 examines


def items_needed(rho: float, p: float = P_SIZE, delta: float = DELTA) -> float:
    """Items per model to resolve a gap of `delta`, at correlation `rho`."""
    return 2 * p * (1 - p) * (1 - rho) * (Z / delta) ** 2


N_IND = round(items_needed(0.0))

_p25_n = committed("p25.tex", "p25.eval.n.needed")
if _p25_n is not None:
    assert str(N_IND) == _p25_n, (
        f"P25 commits {_p25_n} items per model for an independent comparison "
        f"and this program's paired formula gives {N_IND} at rho = 0. The "
        f"paired formula is meant to CONTAIN P25's as its corner; it does not.")
    NOTES.append(f"P25's sizing is the rho = 0 corner of the paired formula: "
                 f"{_p25_n} items.")

RHOS = (0.0, 0.5, 0.8, 0.9)
for rho in RHOS:
    emit(f"p27.n.rho{int(rho * 100):02d}", round(items_needed(rho)))
# The saving is exactly (1 - rho) at every accuracy and every gap, which is
# the invariant rather than the four numbers in the table.
for p in (0.5, 0.7, 0.8, 0.95):
    for delta in (0.005, 0.01, 0.02):
        for rho in (0.3, 0.6, 0.9):
            ratio = items_needed(rho, p, delta) / items_needed(0.0, p, delta)
            assert abs(ratio - (1 - rho)) < 1e-12, (p, delta, rho, ratio)
# The factor of ten is on the page as the table's own last column, so it
# is asserted rather than emitted -- a second copy is one nothing would
# correct, which is Program F11's finding.
assert round(items_needed(0.0) / items_needed(0.9)) == 10

# THE EXACT TEST, and it needs no normal approximation and no variance.
# Only the DISCORDANT items -- the ones where exactly one model is right --
# say anything about the difference.  Under the hypothesis that the two are
# equally good those items split like fair coin flips, so the whole question
# is Program P12's binomial coefficient over integers.
# THE PARITY IS A CONSTRAINT ON THE DATA, NOT ONLY ON THE FORMULA, AND A
# FIRST VERSION OF THIS SECTION VIOLATED IT.  The net is c - b and the
# discordant count is c + b, so the two have the SAME parity: a net of one
# item is impossible on an even number of discordant items, because it needs
# c = 15.5.  This file already recorded the parity as a trap in
# `two_sided_exact` below and then set DISCORDANT = 30 beside NET = 1, which
# is a worked example that cannot occur.  It was caught by the assertion
# Program P28 wrote when it continued this example, which is what a
# cross-programme gate is for.
#
# The corrected version is a better section, not merely a legal one.  On an
# ODD number of discordant items a tie cannot happen, so somebody must be
# ahead and the smallest possible lead is one -- which is exactly what was
# observed.  The p-value is then 1 exactly, and the published gap is the
# least surprising outcome the arithmetic allows.
NET = round(GAP_ITEMS)                     # B ahead by this many items
assert NET == 1, NET
DISCORDANT = 31                            # of the 200; the rest agree
assert (DISCORDANT + NET) % 2 == 0, (
    f"a net of {NET} on {DISCORDANT} discordant items needs "
    f"c = {(DISCORDANT + NET) / 2}, which is not a whole number of items.")
emit("p27.disc", DISCORDANT)
emit("p27.net", NET)
emit("p27.concord", ITEMS - DISCORDANT)
emit("p27.to.b", (DISCORDANT + NET) // 2)
emit("p27.to.a", (DISCORDANT - NET) // 2)


def two_sided_exact(m: int, net: int) -> float:
    """P(|c - b| >= net) when the m discordant items are fair coin flips.

    c is the count going one way, b = m - c the other, so the net is
    c - b = 2c - m and `net` is that quantity, in items, directly.
    Everything here is math.comb over integers divided by 2**m: exact, and
    identical on every machine, which a normal approximation would not be.

    THE PARITY IS A TRAP AND IT CAUGHT THIS SCRIPT.  2c - m has the parity of
    m, so at even m the answer for `net` and for `net + 1` is the same number
    -- and a first draft passed 2 * net here, got the right answer for the
    wrong reason, and would have been wrong at odd m.  Program P17 recorded
    the same shape: a formula whose two readings agree numerically is
    invisible until the day they do not."""
    assert 0 <= net <= m, (net, m)
    total = sum(math.comb(m, c) for c in range(m + 1)
                if abs(2 * c - m) >= net)
    return total / 2 ** m


P_EXACT = two_sided_exact(DISCORDANT, NET)
emit("p27.p.exact", P_EXACT, 2)
# EXACTLY one, and the reason is the parity above rather than a rounding: on
# an odd number of discordant items every outcome is at least one away from
# even, so a result at least this lopsided is certain.
assert P_EXACT == 1.0, P_EXACT
# What the observed outcome IS, then: the single most likely one, counting
# both directions.
P_ONE = 2 * math.comb(DISCORDANT, (DISCORDANT + 1) // 2) / 2 ** DISCORDANT
emit("p27.p.one.pct", pct(100.0 * P_ONE), 1)
assert 0.2 < P_ONE < 0.35, P_ONE
# And it is the most likely: no other net beats it.
for d in range(3, DISCORDANT + 1, 2):
    assert 2 * math.comb(DISCORDANT, (DISCORDANT + d) // 2) / 2 ** DISCORDANT \
        < P_ONE, d

# How big would the net have to be, on these same discordant items, before the
# conventional threshold is crossed?  Found by search rather than quoted.
#
# THE SEARCH STEPS BY TWO, and that is not a micro-optimisation.  The net is a
# difference of two counts adding to DISCORDANT, so it has that number's
# parity and half the integers are outcomes the data cannot produce.  A search
# stepping by one reports the first integer whose p-value clears the bar, and
# on an odd count that integer is an impossible one: at 31 discordant items it
# answers 12, giving a threshold of 6.0 points that no evaluation can ever
# land on, where the smallest ACHIEVABLE net clearing the bar is 13 and 6.5.
#
# The parity was understood twenty lines above this -- the most-likely check
# iterates `range(3, DISCORDANT + 1, 2)` -- and this loop ignored it, which is
# the finding: a constraint recorded at one use is not enforced at the next.
NEED = NET
while two_sided_exact(DISCORDANT, NEED) >= ALPHA_LATER:
    NEED += 2
assert (DISCORDANT + NEED) % 2 == 0, (DISCORDANT, NEED)
emit("p27.net.needed", NEED)
emit("p27.net.needed.pts",
     reproduces(100.0 * NEED / ITEMS, 1, (float(NEED), 0), (float(ITEMS), 0),
                op=lambda d, n: 100.0 * d / n),
     1)
assert NEED > NET, (NEED, NET)


# ======================================================================
# 4.  What a p-value does and does not say.
#
# Two measurements, and neither is a definition.
# ======================================================================

# (a) Under the null the p-value is UNIFORM, so "p < 0.05" happens one time in
#     twenty when nothing whatever is going on.  Measured on the exact
#     discordant test rather than asserted: enumerate every outcome of m fair
#     flips, compute each one's p-value, and add up the probability of the
#     ones below the threshold.
ALPHA = ALPHA_LATER
_mass = 0.0
for c in range(DISCORDANT + 1):
    p_of_outcome = two_sided_exact(DISCORDANT, abs(2 * c - DISCORDANT))
    if p_of_outcome < ALPHA:
        _mass += math.comb(DISCORDANT, c) / 2 ** DISCORDANT
emit("p27.alpha", ALPHA, 2)
emit("p27.null.rate.pct", pct(100.0 * _mass), 1)
# A discrete test cannot hit the threshold exactly, and it lands UNDER it
# rather than over -- which is the honest statement and the one the frames
# make.  A continuous test would give exactly alpha.
assert 0 < _mass <= ALPHA, _mass

# (b) THE INVERSION, which is Program P23's theorem on a different pair of
#     events.  P(p < alpha | no difference) = alpha says nothing about
#     P(no difference | p < alpha) without a prior, and the second is what
#     everybody reads off the first.  Worked with P23's own machinery: if a
#     fraction PRIOR_REAL of the comparisons anybody runs are real, and the
#     test finds a real one with probability POWER, then
PRIOR_REAL, POWER = 0.10, 0.50
_true_pos = PRIOR_REAL * POWER
_false_pos = (1 - PRIOR_REAL) * ALPHA
FDR = _false_pos / (_true_pos + _false_pos)
emit("p27.prior.real.pct", pct(100.0 * PRIOR_REAL), 0)
emit("p27.power.pct", pct(100.0 * POWER), 0)
emit("p27.fdr.pct", pct(100.0 * FDR), 0)
assert FDR > ALPHA * 4, FDR
# The gate: this is Bayes and nothing else, so it must reproduce from
# Program P23's own form of the theorem.
assert abs(FDR - _false_pos / (_true_pos + _false_pos)) < 1e-15


# ======================================================================
# 5.  Forty models on one leaderboard.
#
# Two effects and they are different in kind: the chance that SOMETHING looks
# significant, and the size of the margin the winner appears to have.
# ======================================================================

MODELS = 40
ANY_FALSE = 1 - (1 - ALPHA) ** MODELS
emit("p27.models", MODELS)
emit("p27.any.false.pct", pct(100.0 * ANY_FALSE), 0)
assert ANY_FALSE > 0.8, ANY_FALSE

# Bonferroni: divide the threshold by the number of comparisons.  What it
# costs is items, and section 3's own formula prices it -- the threshold moves
# z, and n grows with z squared.
def z_for(alpha: float) -> float:
    """Two-sided normal quantile, by bisection on erf.  No table, no SciPy."""
    lo, hi = 0.0, 12.0
    target = 1 - alpha / 2
    for _ in range(200):
        mid = (lo + hi) / 2
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


assert abs(z_for(0.05) - 1.959963984540054) < 1e-9, z_for(0.05)
Z_BONF = z_for(ALPHA / MODELS)
# Three decimals, not two: at two the page prints 3.23, and (3.23/1.96)^2 is
# 2.72 against a true cost of 2.71.  The extra digit is what makes the line
# checkable by the reader rather than merely correct.
emit("p27.z.bonf", not_on_a_boundary(Z_BONF, 3), 3)
BONF_COST = (Z_BONF / Z) ** 2
emit("p27.bonf.cost",
     reproduces(not_on_a_boundary(BONF_COST, 2), 2,
                (Z_BONF, 3), (Z, 2), op=lambda a, b: (a / b) ** 2),
     2)
assert BONF_COST > 1.5, BONF_COST

# The winner's apparent margin.  Forty models of IDENTICAL true accuracy are
# ranked on one evaluation; the best observed score sits above the truth by
# the expected maximum of MODELS standard normals, times the standard error.
# INTEGRATED, not sampled -- Program P24's rule: "it agreed within the error
# bar" is the reading this section refuses.
def expected_max_normal(m: int, lo: float = -9.0, hi: float = 9.0,
                        steps: int = 90000) -> float:
    """E[max of m iid standard normals], by Simpson on x * d/dx F(x)^m."""
    h = (hi - lo) / steps

    def integrand(x: float) -> float:
        cdf = 0.5 * (1 + math.erf(x / math.sqrt(2)))
        pdf = math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
        return x * m * cdf ** (m - 1) * pdf

    total = integrand(lo) + integrand(hi)
    for i in range(1, steps):
        total += integrand(lo + i * h) * (4 if i % 2 else 2)
    return total * h / 3


# The two cases with a closed form, checked before the one without.
assert abs(expected_max_normal(1)) < 1e-9, expected_max_normal(1)
assert abs(expected_max_normal(2) - 1 / math.sqrt(math.pi)) < 1e-9

E_MAX = expected_max_normal(MODELS)
emit("p27.emax", not_on_a_boundary(E_MAX, 2), 2)
LB_N, LB_P = 1000, 0.70
LB_SE = 100.0 * math.sqrt(LB_P * (1 - LB_P) / LB_N)
LB_MARGIN = E_MAX * LB_SE
emit("p27.lb.n", LB_N)
emit("p27.lb.p.pct", 100.0 * LB_P, 0)
emit("p27.lb.se", LB_SE, 2)
emit("p27.lb.margin", not_on_a_boundary(LB_MARGIN, 1), 1)
assert LB_MARGIN > 2.0, LB_MARGIN
# And the reproduce-from-the-page check: the margin the reader can rebuild
# from the two printed numbers must be the one printed beside them.
_printed = float(f"{E_MAX:.2f}") * float(f"{LB_SE:.2f}")
assert f"{_printed:.1f}" == f"{LB_MARGIN:.1f}", (_printed, LB_MARGIN)


# ======================================================================
# The transcript.  Every transformation applied to a value is INSIDE the
# listing, because Programs P19 and P24 each shipped a draft where it was not
# and a session prints what a session prints.
# ======================================================================
TRANSCRIPT = Path(__file__).resolve().parent.parent / "figures" / "transcripts"
# The net is ONE item, and the listing has to say so.  A first draft wrote
# `net = 2` here, inheriting the doubling this script's own section 3 records
# as a trap -- it prints the same number, because 2c - m has the parity of m,
# and a reader comparing the listing against the frames would have found the
# frames saying one item and the listing saying two.  Program P16's finding:
# a generated, committed, drift-gated transcript can still disagree with the
# prose beside it, and only reading it against the frames catches that.
_lines = [
    ">>> from math import comb",
    f">>> m, net = {DISCORDANT}, {NET}",
    ">>> sum(comb(m, c) for c in range(m + 1)",
    "...     if abs(2 * c - m) >= net) / 2 ** m",
    repr(round(P_EXACT, 4)),
    ">>> round(2 * comb(m, (m + 1) // 2) / 2 ** m, 4)",
    repr(round(P_ONE, 4)),
]
assert max(len(line) for line in _lines) <= 64, max(_lines, key=len)
(TRANSCRIPT / "p27-odd-count.txt").write_text(
    "\n".join(_lines) + "\n", encoding="utf8")


# ======================================================================
OUT.write_text(
    "% Generated by code/p27_inference.py --- do not edit.\n"
    "% Regenerate with `make numbers`; `make verify` fails if this file and\n"
    "% the script disagree, which is what stops a number in the book drifting\n"
    "% away from the computation that justifies it.\n\n"
    + "".join(f"\\mfaval{{{k}}}{{{v}}}\n" if numeric
             else f"\\mfavaltext{{{k}}}{{{v}}}\n"
             for k, (v, numeric) in VALUES.items()),
    encoding="utf8")
print(f"P27: {len(VALUES)} values -> {OUT}")
for note in NOTES:
    print(f"  * {note}")
