#!/usr/bin/env python3
"""Program P02 --- Numerical error, stability and computing in log-space.

Every number Program P02 prints that the reader cannot do in their head is
computed here and written to figures/values/p02.tex, which the book \\input{}s.

P02's thesis is that AN ALGORITHM CAN BE CORRECT IN EXACT ARITHMETIC AND
USELESS IN FLOATING POINT. Program P01 established what the arithmetic is;
this program asks the engineering question -- given that, which algorithms
survive it and which do not -- and the answer is a small catalogue rather
than a principle.

WHAT P02 IS OWED, and pays. Six programs promise it by name, and every one of
the six was read before this script was written rather than remembered:

  * F01 -- "a per-layer error bound in P02 much worse than you expect after
    ninety-six layers", and that lining up exponents loses the small number.
  * F02 -- what a layer-norm epsilon protects against, and how much of it a
    given format can absorb.
  * F03 -- "why the maximum is the term taken outside, and what it costs when
    it is not"; and how a per-token log-probability is computed WITHOUT EVER
    FORMING A PROBABILITY. F03 already derived the two-term identity, so this
    program owes the generalisation and the pivot question, not the algebra.
  * F05 -- why log and sigmoid are done as one operation.
  * F06 -- why two rows differing enormously in scale matters to a solver.
  * F07 -- "the exact score at which a naive softmax overflows", and the
    consequence of sigma rounding to exactly 1.0 at x = 36.8. F07 already
    established that subtracting the maximum is an IDENTITY and not a trick,
    so this program may not re-derive it; it quantifies it.
  * P01 -- the accumulated summation loss and its catalogue of fixes, and
    catastrophic cancellation by name, both handed over explicitly.

THE MEASUREMENTS:

  1. THE TWO CLIFFS OF THE EXPONENTIAL, exactly. ln of each format's ceiling
     is the score at which a naive softmax overflows, and ln of each format's
     floor is where its terms underflow. fp16's ceiling arrives at a logit of
     about eleven, which is an ordinary score.

  2. WHY THE MAXIMUM. Any pivot is algebraically valid; only the maximum
     bounds every exponent at or below zero. Measured by pivoting on each
     entry in turn and recording which choices overflow.

  3. NEGATIVE VARIANCE, from the one-pass formula, on data a reader would not
     think twice about. Welford's on the same data, for comparison.

  4. FIVE WAYS TO ADD A MILLION NUMBERS, against the exact answer computed in
     integers so that the reference is not itself a floating-point result.

  5. LOG-SIGMOID, and the two ends at which the composed form fails while the
     single operation does not.

WHAT P02 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    the matrix condition number, ill-conditioned systems           -> P10
    FLOPs, bytes, arithmetic intensity                             -> P03
    what a probability IS, and why cross-entropy is the loss       -> P26, P30
P02 owns the SCALAR story: relative error in, relative error out, and the
operations that amplify it.

Run:  python3 code/p02_numerical_stability.py      (or: make numbers)
"""
from __future__ import annotations

import math
import struct
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p02.tex"
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
        # math.isfinite, not merely a successful parse: float() accepts
        # "inf", "-inf" and "nan", so the plain try/except classified them as
        # numbers and \val{} handed them to siunitx, which rejects them with
        # `Invalid number '-inf'` and no PDF. Latent here and fatal in P02.
        numeric = math.isfinite(float(body.replace("e", "E")))
    except ValueError:
        numeric = False
    VALUES[key] = (body, numeric)


def committed(fname: str, key: str) -> str | None:
    """A value another program has committed, AS WRITTEN."""
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    import re
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


def f32(x: float) -> float:
    """x rounded to fp32, which is how this script reasons about that format."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


# ==========================================================================
# SECTION 3 --- the two cliffs of the exponential
#
# P01 derived every format from its two budgets. The scores at which exp()
# leaves a format are the logarithms of that format's ceiling and floor, so
# they follow from P01 rather than being new facts.
# ==========================================================================
FORMATS = {"fp64": (11, 52), "fp32": (8, 23), "fp16": (5, 10), "bf16": (8, 7)}


def largest(ebits: int, mbits: int) -> float:
    return (2.0 - 2.0 ** -mbits) * 2.0 ** ((1 << (ebits - 1)) - 1)


def smallest_subnormal(ebits: int, mbits: int) -> float:
    return 2.0 ** (1 - ((1 << (ebits - 1)) - 1) - mbits)


for _name, (_e, _m) in FORMATS.items():
    emit(f"p02.over.{_name}", math.log(largest(_e, _m)), 1)
    emit(f"p02.under.{_name}", math.log(smallest_subnormal(_e, _m)), 1)
    # THE MAGNITUDE, under its own name. The signed value above is what the
    # table prints; a sentence saying "more than X below the maximum" needs
    # the positive number, and the draft used the signed one -- which reads as
    # "the gap exceeds -16.6" and is not a statement at all.
    # Only fp16's, because it is the only one the frames quote as a drop. The
    # other three would be emitted values nothing references, and the ledger is
    # right to say so.
    if _name == "fp16":
        emit(f"p02.drop.{_name}", -math.log(smallest_subnormal(_e, _m)), 1)

# The smallest term that survives a max-subtracted softmax, as a fraction of
# the largest. The draft said "less than one part in 10^5", which is true and
# is two orders of magnitude weaker than the truth.
emit("p02.drop.fp16.frac", f"{smallest_subnormal(5, 10):.0e}")

# The claim the frames make is a bound, so it is asserted as one -- and the
# upper half is asserted IN LOGARITHMS, because the direct form
# `exp(ceil(cliff)) > largest` overflows a Python float for fp64 and raises
# rather than answering. Which is the program's own lesson arriving inside its
# own script: when the quantity does not fit, compare the exponents.
for _name, (_e, _m) in FORMATS.items():
    _cliff = math.log(largest(_e, _m))
    assert math.exp(math.floor(_cliff)) < largest(_e, _m), f"{_name}: cliff too high"
    assert math.floor(_cliff) < _cliff < math.ceil(_cliff), (
        f"{_name}: the cliff landed on a whole logit, so the next one up is "
        f"not strictly past it")

# fp16's is the number worth printing on its own, because it is an ordinary
# score rather than an exotic one. Rounded UP to the next whole logit, so the
# page can say "a score of this size overflows" and be right.
FP16_OVER = math.ceil(math.log(largest(5, 10)))
emit("p02.over.fp16.int", FP16_OVER)
assert f32(math.exp(FP16_OVER)) > largest(5, 10), "a logit of 12 no longer overflows fp16"
assert math.exp(FP16_OVER - 1) < largest(5, 10), "a logit of 11 now overflows fp16 too"

# --- the cross-programme gate: these ARE P01's ceilings, in logarithms ---
for _key, _name in (("p01.fp32.max", "fp32"), ("p01.fp16.max", "fp16")):
    _raw = committed("p01.tex", _key)
    if _raw is None:                                         # pragma: no cover
        NOTES.append(f"p01.tex absent: {_key} was NOT checked against P02")
        continue
    _e, _m = FORMATS[_name]
    assert abs(float(_raw) / largest(_e, _m) - 1.0) < 1e-3, (
        f"P02's {_name} ceiling disagrees with P01's committed {_raw}")
NOTES.append("P01's ceilings are the same numbers these cliffs are logarithms of")


# ==========================================================================
# WHY THE MAXIMUM, AND WHAT ANOTHER PIVOT COSTS.
#
# This is F03's question, left open by name. F03 took "the larger of two"
# outside, which for two terms is the maximum by accident. For a row of many
# the choice is real: ANY pivot is algebraically valid, because the identity
#
#     ln sum_i e^{z_i} = c + ln sum_i e^{z_i - c}
#
# holds for every c. Only c = max bounds every remaining exponent at or below
# zero, so only c = max is guaranteed not to overflow.
# ==========================================================================
SCORES = [12.0, 9.0, 3.0, -4.0, -18.0]
EXACT_LSE = math.log(sum(math.exp(s - max(SCORES)) for s in SCORES)) + max(SCORES)
emit("p02.lse.exact", EXACT_LSE, 4)

# Pivot on each entry in turn, in fp16's range, and record which survive.
_survived, _failed = [], []
for pivot in SCORES:
    try:
        terms = [f32(math.exp(s - pivot)) for s in SCORES]
        if any(t > largest(5, 10) for t in terms):
            raise OverflowError
        _survived.append(pivot)
    except OverflowError:
        _failed.append(pivot)
emit("p02.pivot.total", len(SCORES))
emit("p02.pivot.safe", len(_survived))

# THE FIRST VERSION ASSERTED THAT ONLY THE MAXIMUM SURVIVES, AND IT FAILED ON
# THE FIRST RUN -- three of these five pivots keep every term inside fp16,
# because fp16 tolerates a shortfall of up to ln(65504) = 11.09 and the scores
# are not spread much wider than that.
#
# The failure is the better frame, and it is why the choice is worth a section
# rather than a footnote. A pivot c is safe exactly when max - c <= ln(ceiling),
# so whether a NON-MAXIMAL pivot works is a property of the data. The maximum
# is the only choice that is safe for every row, every spread and every format,
# because it makes the shortfall zero. Everything else works until the batch
# that does not, and then reports `nan` rather than an error.
CLIFF16 = math.log(largest(5, 10))
for pivot in SCORES:
    predicted_safe = max(SCORES) - pivot <= CLIFF16
    assert predicted_safe == (pivot in _survived), (
        f"pivot {pivot}: the rule max - c <= ln(ceiling) no longer predicts "
        f"which pivots survive, and that rule is the section's argument")
assert max(SCORES) in _survived, "the maximum pivot no longer survives, which cannot be"
assert min(SCORES) in _failed, "the smallest pivot no longer overflows this row"
assert len(_failed) > 0, "no pivot fails on this row, so the frame demonstrates nothing"
NOTES.append(
    f"{len(_survived)} of {len(SCORES)} pivots happen to keep every term in fp16 "
    f"on this row -- the maximum is the only one that does so on every row")

# And the cost of the worst pivot, as a number rather than as "it overflows":
# the largest term the smallest pivot has to form.
_worst = max(math.exp(s - min(SCORES)) for s in SCORES)
emit("p02.pivot.worst", f"{_worst:.2e}")
assert _worst > largest(5, 10), "the worst pivot no longer overflows fp16"


# ==========================================================================
# SECTION 1 --- an algorithm correct in exact arithmetic
#
# The one-pass variance formula, E[x^2] - E[x]^2, on data nobody would look at
# twice: five readings a second apart from a counter that has been running a
# while. The spread is real and the mean is large, which is the whole recipe.
# ==========================================================================
# Five latency readings in microseconds, a whole millisecond apart from zero
# and one microsecond apart from each other. Nothing about them is extreme.
#
# THE OFFSET WAS CHOSEN BY SEARCH, NOT BY TASTE. The first draft used a
# counter near 1e9 on the reasoning that a bigger offset cancels harder; it
# cancels so hard that every reading rounds to the SAME fp32 value (the gap
# there is 64) and the one-pass formula returns exactly 0.0 rather than
# anything negative. The offset has to be large enough for the squares to
# cancel and small enough for the readings to stay distinct, and 30000 is in
# that window: the readings differ by 1 and the formula reports -64.
READINGS = [30_000.0 + d for d in (0.0, 1.0, 2.0, 3.0, 4.0)]
N = len(READINGS)
TRUE_VAR = sum((x - sum(READINGS) / N) ** 2 for x in READINGS) / N


def one_pass_f32(xs: list[float]) -> float:
    """E[x^2] - E[x]^2, evaluated the way a single-precision loop would."""
    s = sx2 = f32(0.0)
    for x in xs:
        s = f32(s + f32(x))
        sx2 = f32(sx2 + f32(f32(x) * f32(x)))
    mean = f32(s / f32(len(xs)))
    return f32(f32(sx2 / f32(len(xs))) - f32(mean * mean))


def welford_f32(xs: list[float]) -> float:
    """Welford: one pass, and it never forms the sum of squares."""
    n, mean, m2 = 0, f32(0.0), f32(0.0)
    for x in xs:
        n += 1
        delta = f32(f32(x) - mean)
        mean = f32(mean + f32(delta / f32(n)))
        m2 = f32(m2 + f32(delta * f32(f32(x) - mean)))
    return f32(m2 / f32(n))


NAIVE_VAR = one_pass_f32(READINGS)
WELFORD_VAR = welford_f32(READINGS)
emit("p02.var.true", TRUE_VAR, 1)
emit("p02.var.naive", f"{NAIVE_VAR:.1f}")
emit("p02.var.welford", f"{WELFORD_VAR:.1f}")
emit("p02.var.offset", f"{READINGS[0]:.0f}")

# THE ASSERTION IS THE INVARIANT, NOT THE FIGURE. What must hold is that the
# one-pass formula returns something a variance cannot be and Welford's does
# not -- so changing the readings cannot quietly falsify the frame.
assert NAIVE_VAR < 0.0, (
    f"the one-pass formula no longer returns a negative variance on these "
    f"readings (got {NAIVE_VAR}); the frame's elicitation depends on it")
assert WELFORD_VAR >= 0.0, "Welford's has started returning a negative variance"
assert abs(WELFORD_VAR - TRUE_VAR) < 0.5 * TRUE_VAR, (
    "Welford's is no longer close to the true variance on these readings")
NOTES.append(f"one-pass variance in fp32: {NAIVE_VAR}; Welford: {WELFORD_VAR}; true: {TRUE_VAR}")

# The mechanism, in one number: the two quantities being subtracted, and how
# many significant figures they share. That is what "catastrophic" names.
_ex2 = sum(x * x for x in READINGS) / N
_ex_2 = (sum(READINGS) / N) ** 2
emit("p02.var.ex2", f"{_ex2:.6e}")
emit("p02.var.exsq", f"{_ex_2:.6e}")
_shared = -math.log10(abs(_ex2 - _ex_2) / _ex2)
emit("p02.var.shared", round(_shared))
assert round(_shared) > 7, "the two quantities no longer agree to more than fp32 can hold"

# It is exactly ONE gap at the magnitude of the quantities being subtracted,
# not "a multiple of the gap" as the draft said -- and one gap is the smallest
# non-zero answer the subtraction could possibly have given, which is a better
# sentence and a checkable one.
_gap_there = 2.0 ** math.floor(math.log2(_ex2)) * 2.0 ** -23
emit("p02.var.gap", f"{_gap_there:.0f}")
assert NAIVE_VAR == -_gap_there, (
    f"the one-pass result is {NAIVE_VAR} where one fp32 gap at {_ex2:.3e} is "
    f"{_gap_there}: the frame says it is exactly one gap")



# ==========================================================================
# SECTION 5 --- five ways to add a million numbers
#
# Program P01 handed this over by name. The reference is computed IN INTEGERS
# so that the thing every method is scored against is not itself a floating-
# point result -- which is the methodological error the sibling volume records
# for its own load tests, in a different denomination.
# ==========================================================================
BIG = 1.0
SMALL_NUM, SMALL_DEN = 1, 10 ** 8          # exactly 1e-8 as a rational
COUNT = 1_000_000
EXACT_SUM = BIG + COUNT * SMALL_NUM / SMALL_DEN     # 1 + 0.01, exactly
SMALL = SMALL_NUM / SMALL_DEN


def add_naive(acc32: bool) -> float:
    total = f32(BIG) if acc32 else BIG
    for _ in range(COUNT):
        total = f32(total + f32(SMALL)) if acc32 else total + SMALL
    return total


def add_sorted() -> float:
    """Smallest first: the million small values combine before meeting BIG."""
    total = f32(0.0)
    for _ in range(COUNT):
        total = f32(total + f32(SMALL))
    return f32(total + f32(BIG))


def add_kahan() -> float:
    """Compensated summation: carry the lost low-order bits forward."""
    total, comp = f32(BIG), f32(0.0)
    for _ in range(COUNT):
        y = f32(f32(SMALL) - comp)
        t = f32(total + y)
        comp = f32(f32(t - total) - y)
        total = t
    return total


def add_pairwise(values, base: float) -> float:
    """Add in a balanced tree, which is what a library reduction does."""
    def rec(lo, hi):
        if hi - lo <= 128:
            s = f32(0.0)
            for i in range(lo, hi):
                s = f32(s + values[i])
            return s
        mid = (lo + hi) // 2
        return f32(rec(lo, mid) + rec(mid, hi))
    return f32(base + rec(0, len(values)))


_vals = [f32(SMALL)] * COUNT
RESULTS = {
    "naive32": add_naive(True),
    "sorted": add_sorted(),
    "kahan": add_kahan(),
    "pairwise": add_pairwise(_vals, f32(BIG)),
    "wide": add_naive(False),
}
emit("p02.sum.n", COUNT)
emit("p02.sum.small", f"{SMALL:.0e}")
emit("p02.sum.exact", f"{EXACT_SUM:.6f}")
for _k, _v in RESULTS.items():
    emit(f"p02.sum.{_k}", f"{_v:.6f}")
    # Only the two shortfalls the frames quote. The other three rows are given
    # as a recovered PERCENTAGE, which is the comparable quantity, and the
    # value ledger is right to report an emitted number nothing references.
    if _k in ("naive32", "sorted"):
        emit(f"p02.sum.err.{_k}", f"{abs(_v - EXACT_SUM):.1e}")

# Naive fp32 must lose every one of them; every fix must recover the total to
# a tolerance the page can print. Both are invariants, not observations.
# THE INVARIANT IS THE RECOVERED FRACTION, not a tolerance on the total. The
# first version demanded every fix land within 1e-5 of the exact answer and
# SORTED FAILED IT -- it recovers the contribution to about three parts in a
# hundred thousand, which is a million roundings' worth of drift and is real.
# Ranking them pass/fail would have hidden the interesting half: the fixes are
# not equivalent, and two of them are much better than the other two.
for _k, _v in RESULTS.items():
    emit(f"p02.sum.got.{_k}", f"{(_v - BIG) / (EXACT_SUM - BIG) * 100:.4f}")
assert RESULTS["naive32"] == f32(BIG), (
    f"naive fp32 accumulation no longer loses every contribution "
    f"(got {RESULTS['naive32']}); each 1e-8 is below half a gap at 1.0")
for _k in ("sorted", "kahan", "pairwise", "wide"):
    _got = (RESULTS[_k] - BIG) / (EXACT_SUM - BIG)
    assert _got > 0.99, f"{_k} now recovers only {_got:.4f} of the contribution"
for _better, _worse in (("kahan", "sorted"), ("pairwise", "sorted")):
    assert abs(RESULTS[_better] - EXACT_SUM) < abs(RESULTS[_worse] - EXACT_SUM), (
        f"{_better} is no longer more accurate than {_worse}, which is the "
        f"whole reason the catalogue has more than one entry")
NOTES.append("naive fp32 loses all " + f"{COUNT:,}" + "; the four fixes recover "
             + ", ".join(f"{_k} {(RESULTS[_k]-BIG)/(EXACT_SUM-BIG)*100:.4f}%"
                         for _k in ("sorted", "kahan", "pairwise", "wide")))


# ==========================================================================
# SECTION 4 --- never form a probability
#
# F05 and F07 each left a promise here. The composed form fails at BOTH ends
# and the single operation fails at neither, which is why the libraries ship
# one function rather than two.
# ==========================================================================
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x)) if x >= 0 else math.exp(x) / (1.0 + math.exp(x))


def log_sigmoid(x: float) -> float:
    """-softplus(-x), which never forms the probability."""
    return -math.log1p(math.exp(-x)) if x >= 0 else x - math.log1p(math.exp(x))


# The lower end: sigma underflows to exactly zero, so ln(sigma) is -inf.
_lo = 1
while sigmoid(-_lo) > 0.0:
    _lo += 1
emit("p02.logsig.under", -_lo)
assert sigmoid(-_lo) == 0.0 and sigmoid(-_lo + 1) > 0.0, "the underflow point moved"
assert math.isfinite(log_sigmoid(float(-_lo))), "log_sigmoid stopped surviving it"
# -inf is not a computed value, it is what the REPL prints, so the page
# writes \code{-inf} directly rather than routing a name through \val{}.
emit("p02.logsig.stable", f"{log_sigmoid(float(-_lo)):.1f}")

# The upper end is F07's, and it is the one that bites in a binary
# cross-entropy: sigma rounds to exactly 1, so ln(1 - p) is ln(0).
_hi = 1
while sigmoid(float(_hi)) < 1.0:
    _hi += 1
emit("p02.logsig.saturates", _hi)
assert sigmoid(float(_hi)) == 1.0, "sigma no longer reaches exactly 1.0"
assert 1.0 - sigmoid(float(_hi)) == 0.0, "1 - sigma is no longer exactly zero there"
assert math.isfinite(log_sigmoid(float(-_hi))), "the stable form fails at the mirror point"

# F07 committed the point at which sigma ROUNDS to 1.0 to one decimal place;
# this program finds the first whole number past it. They must agree.
_f07 = committed("f07.tex", "f07.sig.saturates")
if _f07 is None:                                             # pragma: no cover
    NOTES.append("f07.tex absent: F07's saturation point was NOT checked")
else:
    assert float(_f07) <= _hi < float(_f07) + 1.0, (
        f"P02 finds sigma saturating at {_hi} where F07 committed {_f07}")
    NOTES.append(f"F07's saturation point {_f07} brackets P02's whole-number {_hi}")


# ==========================================================================
# SECTION 2 --- how much a relative error grows
#
# F01 asked for the per-layer bound after ninety-six layers and warned it
# would be worse than expected. It is, as a BOUND -- and the frames say in as
# many words that a bound is not a prediction, because errors of random sign
# accumulate like the square root of the count rather than the count.
# ==========================================================================
LAYERS = 96
for _name, (_e, _m) in FORMATS.items():
    _eps = 2.0 ** -_m
    emit(f"p02.grow.{_name}", f"{((1 + _eps) ** LAYERS - 1) * 100:.2f}")
    emit(f"p02.walk.{_name}", f"{_eps * math.sqrt(LAYERS) * 100:.4f}")
emit("p02.layers", LAYERS)
assert (1 + 2.0 ** -10) ** LAYERS - 1 > 0.09, "fp16's worst case over 96 layers moved"
_bound = (1 + 2.0 ** -10) ** LAYERS - 1
_walk = 2.0 ** -10 * math.sqrt(LAYERS)
emit("p02.grow.ratio", f"{_bound / _walk:.0f}")
assert _bound / _walk > 5, "the bound and the random-walk estimate have converged"
NOTES.append(f"over {LAYERS} layers fp16's worst case is {_bound*100:.1f}% and its random walk {_walk*100:.2f}%")


# ==========================================================================
# The transcripts. Nothing typed: every value is interpolated from above.
# ==========================================================================
# ==========================================================================
# The transcripts. Nothing typed: every number below is computed above and
# interpolated, and every line is wrapped in float() ON PURPOSE.
#
# numpy 2 reprs a scalar as `np.float32(-64.0)` where numpy 1 printed `-64.0`,
# so a transcript quoting either is a claim about a numpy version rather than
# about the arithmetic -- which is F03's `np.logspace` defect wearing a new
# coat. float() hands back a plain Python float whose repr is stable, and it
# is what anybody comparing two of these would type anyway.
# ==========================================================================
VAR_TEXT = f""">>> import numpy as np
>>> xs = [{READINGS[0]:.0f} + d for d in range(5)]
>>> a = np.array(xs, dtype=np.float32)
>>> float((a * a).mean() - a.mean() ** 2)   # one-pass
{NAIVE_VAR!r}
>>> float(a.var())                          # the library
{WELFORD_VAR!r}
"""

CLIFF_TEXT = f""">>> import math, numpy as np
>>> math.log(float(np.finfo(np.float16).max))
{math.log(largest(5, 10))!r}
>>> float(np.exp(np.float16({FP16_OVER})))  # RuntimeWarning: overflow
inf
>>> math.exp({FP16_OVER})
{math.exp(FP16_OVER)!r}
"""

for _t in (VAR_TEXT, CLIFF_TEXT):
    assert _t.isascii(), "listings cannot set a non-ASCII transcript"
    assert max(len(l) for l in _t.splitlines()) <= 64, "transcript too wide"
    assert len(_t.strip().splitlines()) <= 14, "transcript too tall for one frame"

# And the transcripts are CHECKED against the library where it is installed,
# announcing themselves when it is not, because `make numbers` must run on a
# plain python3. This is F03's pattern and it exists because a claim that was
# only ever run on one machine is a claim about that machine.
try:
    import numpy as _np
    _a = _np.array(READINGS, dtype=_np.float32)
    assert float((_a * _a).mean() - _a.mean() ** 2) == NAIVE_VAR, (
        "numpy's one-pass result disagrees with this script's fp32 emulation")
    assert float(_a.var()) == WELFORD_VAR, (
        "numpy's float32 var disagrees with Welford's here")
    assert float(_np.finfo(_np.float16).max) == largest(5, 10), (
        "numpy's fp16 ceiling disagrees with the one derived from the budgets")
    # THE CHECK ABOVE WAS ONCE THE ONLY ONE, AND IT MISSED THE LINE THAT WAS
    # WRONG. The draft's last transcript line printed f32(exp(12)) -- the fp64
    # exponential rounded down -- and labelled it np.exp(np.float32(12)), which
    # is the exponential computed IN fp32 and a different number: 162754.796875
    # against 162754.78125. A fabricated console line, in the program about not
    # trusting what a number looks like. The line is now plain math.exp, which
    # needs no numpy and is exactly reproducible; and every remaining numpy
    # claim in the transcripts is checked here.
    import warnings as _w
    with _w.catch_warnings():
        _w.simplefilter("ignore")
        assert math.isinf(float(_np.exp(_np.float16(FP16_OVER)))), (
            f"exp of {FP16_OVER} in fp16 is no longer inf")
    assert math.exp(FP16_OVER) < largest(8, 23), (
        "the same score no longer fits comfortably in fp32, which is the "
        "contrast the transcript is for")
    NUMPY_NOTE = "numpy: both transcripts reproduce exactly, values and reprs"
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the two transcripts were NOT cross-checked"

def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    for _stem, _text in (("p02-variance", VAR_TEXT), ("p02-cliff", CLIFF_TEXT)):
        (TRANSCRIPTS / f"{_stem}.txt").write_text(_text, encoding="ascii")
        print(f"  transcript -> figures/transcripts/{_stem}.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p02_numerical_stability.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ]
    lines += [
        f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}"
        for k, (body, numeric) in VALUES.items()
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf8")
    width = max(len(k) for k in VALUES)
    for k, (body, numeric) in VALUES.items():
        print(f"  {k:<{width}}  {body}{'' if numeric else '   (text)'}")
    print(f"\n  {len(VALUES)} values -> figures/values/p02.tex")
    for note in NOTES:
        print(f"  {note}")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
