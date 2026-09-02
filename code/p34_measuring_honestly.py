"""P34 --- Measuring a model honestly.

Every number Program P34 prints, and the assertions that keep them honest.

PART IX'S CONTRACT IS THAT IT INTRODUCES NO NEW MATHEMATICS, so the first
question is P32's and P33's: not "what is left of the subject" but "which
lines of the brief have already been delivered".  The brief brackets six
handovers and FIVE OF THEM ARE ON THE PAGE:

  [P27] the confidence interval and the bootstrap   P27's own outcome
  the paired comparison                             P27 section 3, exactly
  [P28] the judge as a miscalibrated instrument     P28 section 6, in odds
  [P3]  cost per token                              P03, four places
  [P29--P31] the information measures and limits    P29 section 6, P31 4--5

THE ONE THAT IS GENUINELY THIS PROGRAM'S is the first: [P26] evaluation
design as an ESTIMATION PROBLEM.  Program P26 owns bias, variance and
maximum likelihood and never uses the word evaluation, so the framing is
P34's to supply -- an evaluation set is a sample, a score is an estimator,
and every question about a benchmark is then a question P26 and P27 already
answer.  That is what P27's and P28's headers mean when they both close their
NOT-SPENT lists with "P34 owns evaluation design end to end".

Four programs defer here BY NAME and each hands over something different:
  F01  a claim about a model is "a ratio quoted without its two quantities";
       P34 is about reading those claims properly.          -> section 5
  F04  P27 asks whether a gap beats the noise, "and P34 makes that the
       standard a reported number has to meet."             -> section 8
  F08  P34 says "how to find out whether a score means anything on your
       data."                                               -> sections 1--2
  P17  the sharpness claim needs trained models, "which is P34's subject
       and not this one's."                                 -> section 7

METHOD, from P30, P31, P32 and P33: derive in closed form wherever possible.
NOTHING HERE IS SAMPLED.  The re-mix, the attenuation, the bill and the
crossover are all exact statements about rational numbers, computed over
`Fraction` with no tolerance anywhere; the two interval figures are read back
from Program P27 and recomputed rather than quoted.

Run:  python3 code/p34_measuring_honestly.py
"""

from __future__ import annotations

import math
import re
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p34.tex"
TRANSCRIPT = OUT.parent.parent / "transcripts"
VALUES: dict[str, tuple[str, bool]] = {}


def not_on_a_boundary(x: float, digits: int) -> float:
    """Refuse a value whose printed form depends on the last bit.

    Program P20's `p20.cos.area` printed 0.501 here and 0.500 on CI because
    the quantity sat exactly on a rounding boundary.  Program P27 wrote a
    guard for it and THE GUARD MEASURED THE WRONG DISTANCE -- |frac - round|
    is zero on an exactly representable value and one half on the boundary,
    so it refused the safe case and passed 0.5005 at three decimals, which is
    the number its own docstring names.  Found by this program's pass and
    corrected in both files; a rounding boundary is a HALF-step.

    Every float this program prints goes through here, which is how the
    judge's agreement of 92.15 was caught: at one decimal it prints 92.2 and
    3.15 prints 3.1, from the binary representation alone."""
    step = 10.0 ** -digits
    frac = abs(x) / step
    half = abs((frac % 1.0) - 0.5)
    assert half > 0.02, (
        f"{x!r} is {half:.4f} of a step from the {digits}-decimal rounding "
        f"boundary; a different libm will print it differently.")
    return x


def emit(key: str, value, digits: int | None = None) -> None:
    if isinstance(value, float) and digits is not None:
        not_on_a_boundary(value, digits)
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
    """Refuse a percentage that rounds to 0 or 100 and so reads as exact."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not.")
    return x


def reproduces(value: float, digits: int, *operands, op) -> float:
    """Refuse a quantity that does not come back out of its own printed page."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


# ======================================================================
# SECTION 1 --- AN EVALUATION SET IS A SAMPLE, SO A SCORE IS AN ESTIMATOR.
#
# The whole of the framing is Program P26's decomposition with one word
# changed.  P26 splits an estimator's mean squared error into bias squared
# plus variance and proves the split exactly over fractions; read on an
# evaluation set, the VARIANCE is the sampling of items (Program P27 owns it
# and prints an interval for it) and the BIAS is the distance between what
# the benchmark measures and what you care about.
#
# The consequence is the section, and it is arithmetic rather than a warning:
# the variance falls as 1/n and the bias does not fall at all, so past some
# item count the reported figure's error is dominated by a quantity NO
# INTERVAL ON THE REPORT MENTIONS.  More items buy precision; they never buy
# validity.
# ======================================================================

# The accuracy is section 2's model B, so the two sections describe one
# evaluation rather than two that resemble each other.
P_TRUE = F(143, 200)
MIS_PTS = 2                              # the benchmark is two points off task
BIAS = F(MIS_PTS, 100)

# P26's identity, checked exactly at every size rather than asserted once.
for _n in (50, 100, 510, 1000, 5000):
    _var = P_TRUE * (1 - P_TRUE) / _n
    _mse = BIAS * BIAS + _var
    assert _mse == BIAS ** 2 + P_TRUE * (1 - P_TRUE) / _n
    assert _var > 0

# The crossover: the first whole item count at which the mis-specification
# contributes at least as much as the sampling.  Exact over fractions.
MIS_N = 1
while P_TRUE * (1 - P_TRUE) / MIS_N > BIAS * BIAS:
    MIS_N += 1
assert P_TRUE * (1 - P_TRUE) / MIS_N <= BIAS ** 2
assert P_TRUE * (1 - P_TRUE) / (MIS_N - 1) > BIAS ** 2
_exact = P_TRUE * (1 - P_TRUE) / BIAS ** 2
assert MIS_N - 1 < _exact <= MIS_N, (_exact, MIS_N)

# And at Program P27's own leaderboard size the ratio is already about two.
LB_N = int(committed("p27.tex", "p27.lb.n") or 1000)
MIS_RATIO = float(BIAS ** 2 / (P_TRUE * (1 - P_TRUE) / LB_N))
assert MIS_RATIO > 1.0, MIS_RATIO

emit("p34.mis.pts", MIS_PTS)
emit("p34.mis.n", MIS_N)
emit("p34.mis.ratio", MIS_RATIO, 2)


# ======================================================================
# SECTION 2 --- THE RE-MIX.  THE HEADLINE.
#
# Program P27 committed a leaderboard's top two at 71.5 and 71.0 per cent on
# 200 items -- the achievable neighbours of the published 71.4 and 70.9 --
# and asked whether the gap beats the noise.  This section asks the question
# P27 could not, because P27 holds the evaluation set fixed: WHAT ELSE ABOUT
# THE SET WAS A CHOICE?
#
# Split the same 200 items into two kinds, hold both models completely fixed,
# and re-weight.  The two subset scores are the SAME MEASUREMENTS; only the
# mix changes.  This is Program P12's third kind of gate -- the same worked
# example continued -- so the even-mix scores must reproduce P27's own
# committed figures to the digit or this section is about a different
# leaderboard.
# ======================================================================

ITEMS = int(committed("p27.tex", "p27.items") or 200)
assert ITEMS == 200, ITEMS
HALF = ITEMS // 2

# per-kind counts, out of a hundred each: B is better on the short items and
# worse on the long ones, which is the ordinary case and not a contrivance.
B_SHORT, B_LONG = 80, 63
A_SHORT, A_LONG = 74, 68


def mixed(short: int, long_: int, w: F) -> F:
    """Score at a mix carrying weight w on the short items.  Exact."""
    return w * F(short, 100) + (1 - w) * F(long_, 100)


EVEN = F(1, 2)
B_EVEN, A_EVEN = mixed(B_SHORT, B_LONG, EVEN), mixed(A_SHORT, A_LONG, EVEN)
assert B_EVEN == F(B_SHORT + B_LONG, ITEMS)
assert A_EVEN == F(A_SHORT + A_LONG, ITEMS)

# THE GATE.  Both must reproduce Program P27's committed figures exactly.
for _key, _score in (("p27.near.hi", B_EVEN), ("p27.near.lo", A_EVEN)):
    _c = committed("p27.tex", _key)
    assert _c is not None, _key
    assert f"{float(_score) * 100:.1f}" == _c, (_key, _c, float(_score) * 100)

# The gap is linear in the mix, so the tie point is one division.
#   gap(w) = (B_LONG - A_LONG)/100 + w * ((B_SHORT - A_SHORT) - (B_LONG - A_LONG))/100
GAP0 = F(B_LONG - A_LONG, 100)
SLOPE = F((B_SHORT - A_SHORT) - (B_LONG - A_LONG), 100)
for _num in range(0, 101):
    _w = F(_num, 100)
    assert mixed(B_SHORT, B_LONG, _w) - mixed(A_SHORT, A_LONG, _w) == GAP0 + _w * SLOPE

assert SLOPE != 0
TIE_W = -GAP0 / SLOPE
assert F(2, 5) < TIE_W < F(3, 5), TIE_W          # a mix nobody would call different
assert mixed(B_SHORT, B_LONG, EVEN) > mixed(A_SHORT, A_LONG, EVEN)

# The largest whole count of short items at which the ORDERING HAS REVERSED.
SHIFT_TO = ITEMS
while mixed(B_SHORT, B_LONG, F(SHIFT_TO, ITEMS)) > mixed(A_SHORT, A_LONG, F(SHIFT_TO, ITEMS)):
    SHIFT_TO -= 1
SHIFT = HALF - SHIFT_TO
assert SHIFT > 0
assert mixed(B_SHORT, B_LONG, F(SHIFT_TO + 1, ITEMS)) > mixed(A_SHORT, A_LONG, F(SHIFT_TO + 1, ITEMS))

ALT = F(SHIFT_TO, ITEMS)
B_ALT, A_ALT = mixed(B_SHORT, B_LONG, ALT), mixed(A_SHORT, A_LONG, ALT)
assert A_ALT > B_ALT
ALT_GAP = float((A_ALT - B_ALT) * 100)

# B's own score over every mix, against the gap it is being compared on and
# against Program P27's own threshold for a difference that means anything.
SWING = float((F(max(B_SHORT, B_LONG), 100) - F(min(B_SHORT, B_LONG), 100)) * 100)
EVEN_GAP = float((B_EVEN - A_EVEN) * 100)
assert SWING > EVEN_GAP > 0

NEEDED = float(committed("p27.tex", "p27.net.needed.pts") or 6.5)
assert SWING > NEEDED, (SWING, NEEDED)
SWING_TIMES = SWING / NEEDED

emit("p34.mix.short", HALF)
emit("p34.mix.b.short", float(B_SHORT), 1)
emit("p34.mix.b.long", float(B_LONG), 1)
emit("p34.mix.a.short", float(A_SHORT), 1)
emit("p34.mix.a.long", float(A_LONG), 1)
emit("p34.mix.tie.w", pct(float(TIE_W) * 100), 1)
emit("p34.mix.shift", SHIFT)
emit("p34.mix.alt.b", float(B_ALT) * 100, 2)
emit("p34.mix.alt.a", float(A_ALT) * 100, 2)
emit("p34.mix.alt.gap", ALT_GAP, 2)
emit("p34.mix.swing", SWING, 1)
emit("p34.mix.swing.times", reproduces(SWING_TIMES, 1, (SWING, 1), (NEEDED, 1),
                                       op=lambda a, b: a / b), 1)

# The two alternative scores are printed side by side, so a reader subtracts
# them.  P28's finding: a helper that checks a quotient says nothing about a
# difference, so the difference is checked in the form the page prints it.
assert (f"{float(A_ALT) * 100:.2f}" != f"{float(B_ALT) * 100:.2f}"), "the flip must be visible"
_shown = float(f"{float(A_ALT) * 100:.2f}") - float(f"{float(B_ALT) * 100:.2f}")
assert f"{_shown:.2f}" == f"{ALT_GAP:.2f}", (_shown, ALT_GAP)


# ======================================================================
# SECTION 3 --- THE INTERVAL, AND WHAT NARROWING IT COSTS.
#
# Program P27 owns the interval and commits one: 70 per cent on a thousand
# items, a standard error of 1.45 points and a margin of 3.1 under its own
# multiple-comparison correction.  What is left is the BUDGET reading, which
# is a consequence of the square root and of nothing else: precision goes as
# one over the root of the item count, so halving an interval is four times
# the annotation bill and four times the inference bill.
# ======================================================================

LB_P = float(committed("p27.tex", "p27.lb.p.pct") or 70) / 100.0
E_MAX = float(committed("p27.tex", "p27.emax") or 2.16)
LB_SE = 100.0 * math.sqrt(LB_P * (1 - LB_P) / LB_N)
LB_MARGIN = E_MAX * LB_SE

# THE GATE: recomputed here, and it must reproduce P27's committed pair.
assert f"{LB_SE:.2f}" == committed("p27.tex", "p27.lb.se"), LB_SE
assert f"{LB_MARGIN:.1f}" == committed("p27.tex", "p27.lb.margin"), LB_MARGIN

HALVE_TIMES = 4
assert abs(E_MAX * 100.0 * math.sqrt(LB_P * (1 - LB_P) / (HALVE_TIMES * LB_N))
           - LB_MARGIN / 2.0) < 1e-9

# The count that states one model's accuracy to within a single point.
ONE_PT = 1.0
ONE_PT_N = math.ceil((E_MAX ** 2) * LB_P * (1 - LB_P) * 10000.0 / (ONE_PT ** 2))
assert E_MAX * 100.0 * math.sqrt(LB_P * (1 - LB_P) / ONE_PT_N) <= ONE_PT
assert E_MAX * 100.0 * math.sqrt(LB_P * (1 - LB_P) / (ONE_PT_N - 1)) > ONE_PT

# And Program P27's own count for TELLING TWO MODELS APART at one point.
DETECT_N = int(committed("p27.tex", "p27.n.rho00") or 12293)
DETECT_RATIO = DETECT_N / ONE_PT_N
assert 1.0 < DETECT_RATIO < 2.0, DETECT_RATIO

# A THRESHOLD CHOSEN SO A CLAIM WOULD PASS IS NOT AN ASSERTION.  The draft
# had `ONE_PT_N > 10 * LB_N`, which fails at 9798 against 10000 -- and the
# invariant it was reaching for needs no constant at all: the item count
# scales as the SQUARE of the margin it buys, so going from P27's own margin
# to one point costs exactly that ratio squared.
assert ONE_PT_N == math.ceil(LB_N * (LB_MARGIN / ONE_PT) ** 2), ONE_PT_N

emit("p34.halve.times", HALVE_TIMES)
emit("p34.halve.n", HALVE_TIMES * LB_N)
emit("p34.one.pt.n", ONE_PT_N)
emit("p34.detect.ratio", reproduces(DETECT_RATIO, 2, (float(DETECT_N), 0),
                                    (float(ONE_PT_N), 0), op=lambda a, b: a / b), 2)


# ======================================================================
# SECTION 4 --- THE JUDGE AS AN INSTRUMENT, AND WHAT IT DOES TO A GAP.
#
# Program P28 section 6 prices a judge's STATED PROBABILITY: it says ninety
# and means seventy, and the correction is an odds ratio.  That is a
# calibration statement about a number the judge reports.  This section is
# about the judge's VERDICT, which is a different failure of the same
# instrument, and the two must not be merged -- P04's rule about a gate wired
# to a coincidence rather than to a shared computation.
#
# Write a = P(judge marks correct | actually correct) and
#          b = P(judge marks correct | actually wrong).
# The reported accuracy of a model whose true accuracy is p is then
#          p*a + (1 - p)*b,
# so the reported GAP between two models is exactly (a - b) times the true
# gap.  An imperfect judge multiplies every effect size by one constant, and
# THE CONSTANT DOES NOT DEPEND ON p.
# ======================================================================

J_A, J_B = F(95, 100), F(15, 100)
ATTEN = J_A - J_B
assert 0 < ATTEN < 1


def reported(p: F, a: F, b: F) -> F:
    return p * a + (1 - p) * b


# The identity, exactly, over a grid rather than at a point.
for _p1 in range(30, 100, 7):
    for _p2 in range(30, 100, 11):
        for _a in range(60, 101, 8):
            for _b in range(0, 41, 8):
                p1, p2 = F(_p1, 100), F(_p2, 100)
                a, b = F(_a, 100), F(_b, 100)
                assert reported(p1, a, b) - reported(p2, a, b) == (a - b) * (p1 - p2)

TRUE_GAP = 4.0
SEEN_GAP = TRUE_GAP * float(ATTEN)
ITEMS_TIMES = 1.0 / float(ATTEN) ** 2
assert SEEN_GAP < TRUE_GAP and ITEMS_TIMES > 1.0

# THE TRAP.  A judge's card reports AGREEMENT with human labels, which is
#   A = p*a + (1 - p)*(1 - b),
# and that pins p*a - (1 - p)*b.  It pins a - b only when the coefficients
# of a and b are equal in magnitude, which happens at p = 1/2 and nowhere
# else -- so agreement determines the attenuation exactly when the model is
# right half the time.
P_J = P_TRUE                                    # section 2's own accuracy
AGREE = reported(P_J, J_A, 1 - J_B)
assert AGREE == P_J * J_A + (1 - P_J) * (1 - J_B)


def atten_at(a: F, p: F, agree: F) -> F:
    """a - b for the b that reproduces this agreement at this accuracy."""
    b = (p * a - (agree - (1 - p))) / (1 - p)
    assert abs(reported(p, a, 1 - b) - agree) < F(1, 10 ** 12)
    return a - b


# a - b is monotone in a, so the two ends of the admissible range are the
# extremes; both are found by the constraint b in [0, 1], a in [0, 1].
A_HI = F(1, 1)
B_AT_HI = (P_J * A_HI - (AGREE - (1 - P_J))) / (1 - P_J)
assert 0 <= B_AT_HI <= 1
A_LO = (AGREE - (1 - P_J)) / P_J                # the a that makes b exactly 0
assert 0 <= A_LO <= 1
assert abs((P_J * A_LO - (AGREE - (1 - P_J))) / (1 - P_J)) < F(1, 10 ** 12)

ATT_LO, ATT_HI = atten_at(A_HI, P_J, AGREE), A_LO
assert ATT_LO < ATTEN < ATT_HI, (ATT_LO, ATTEN, ATT_HI)
_seen = 0
for _num in range(0, 1001):                     # nothing outside the two ends
    _a = F(_num, 1000)
    _b = (P_J * _a - (AGREE - (1 - P_J))) / (1 - P_J)
    if not (0 <= _b <= 1):                      # this pair cannot occur
        continue
    _seen += 1
    assert ATT_LO <= _a - _b <= ATT_HI, (_a, _a - _b)
assert _seen > 100, _seen

SPREAD = (float(ATT_HI) / float(ATT_LO)) ** 2 - 1.0
assert SPREAD > 0

# And the pinned case: at p = 1/2 the attenuation is the same for every a.
_half, _agree_half = F(1, 2), F(3, 4)
_pinned = {atten_at(F(_n, 100), _half, _agree_half)
           for _n in range(50, 101, 5)}
assert len(_pinned) == 1, _pinned
assert _pinned.pop() == 2 * _agree_half - 1

emit("p34.judge.a", float(J_A) * 100, 0)
emit("p34.judge.b", float(J_B) * 100, 0)
emit("p34.judge.atten", float(ATTEN), 2)
emit("p34.judge.true.gap", TRUE_GAP, 1)
emit("p34.judge.seen.gap", reproduces(SEEN_GAP, 1, (TRUE_GAP, 1),
                                      (float(ATTEN), 2), op=lambda g, a: g * a), 1)
emit("p34.judge.items.times", reproduces(ITEMS_TIMES, 2, (float(ATTEN), 2),
                                         op=lambda a: 1.0 / a ** 2), 2)
emit("p34.judge.agree.pct", pct(float(AGREE) * 100), 2)
emit("p34.judge.atten.lo", float(ATT_LO), 3)
emit("p34.judge.atten.hi", float(ATT_HI), 3)
emit("p34.judge.spread.pct", reproduces(pct(SPREAD * 100), 0,
                                        (float(ATT_HI), 3), (float(ATT_LO), 3),
                                        op=lambda h, l: ((h / l) ** 2 - 1.0) * 100), 0)


# ======================================================================
# SECTION 5 --- THE BILL, WHICH IS THE PRODUCT OF TWO QUANTITIES AND NEVER
# ONE OF THEM.
#
# Program F01's aibox defers here by name: almost every claim about a model
# is "a ratio quoted without its two quantities".  This is that sentence
# priced.  Program P03 owns cost per token; what it cannot say is that the
# denominator is wrong -- nobody buys tokens, they buy answered tasks, and
#     cost per task = price per token  x  tokens per task,
# so a model can be half again as dear per token and cheaper per task.
#
# It is Program P29's own identity in a different currency, and that is the
# gate: bits per character is bits per token times tokens per character, and
# THERE the model's contribution cancels exactly.  Here neither factor
# cancels, which is precisely why one of them alone decides nothing.
# ======================================================================

PRICE_TIMES = F(3, 2)                            # B's price per token, over A's
TOK_A, TOK_B = 900, 520
TOK_TIMES = F(TOK_B, TOK_A)
TASK_TIMES = PRICE_TIMES * TOK_TIMES
assert PRICE_TIMES > 1 and TASK_TIMES < 1, (PRICE_TIMES, TASK_TIMES)

BREAKEVEN = TOK_A / PRICE_TIMES
assert TOK_B < BREAKEVEN, (TOK_B, BREAKEVEN)
assert PRICE_TIMES * F(int(BREAKEVEN), TOK_A) == 1

# P29's gate: its committed ratio is the tokeniser's alone, because the model
# cancels.  Recomputed from its two committed tokens-per-character figures.
_tpc_a = float(committed("p29.tex", "p29.tpc.a") or 0.25)
_tpc_b = float(committed("p29.tex", "p29.tpc.b") or 0.32)
_bpc_ratio = committed("p29.tex", "p29.bpc.ratio")
assert f"{_tpc_b / _tpc_a:.2f}" == _bpc_ratio, (_tpc_b / _tpc_a, _bpc_ratio)

# P03's gate: the cache is per token in flight, so a longer task costs
# memory linearly and the memory is what caps concurrency.
KV_MIB = float(committed("p03.tex", "p03.kv.per.token.mib") or 0.5)
CACHE_A, CACHE_B = TOK_A * KV_MIB, TOK_B * KV_MIB
CONC_TIMES = CACHE_A / CACHE_B
assert abs(CONC_TIMES - TOK_A / TOK_B) < 1e-12   # the cache cancels, the length does not

emit("p34.bill.price.times", float(PRICE_TIMES), 2)
emit("p34.bill.tok.a", TOK_A)
emit("p34.bill.tok.b", TOK_B)
emit("p34.bill.tok.times", float(TOK_TIMES), 3)
emit("p34.bill.task.times", reproduces(float(TASK_TIMES), 3,
                                       (float(PRICE_TIMES), 2), (float(TOK_TIMES), 3),
                                       op=lambda p, t: p * t), 3)
emit("p34.bill.saving.pct", reproduces(pct((1 - float(TASK_TIMES)) * 100), 1,
                                       (float(TASK_TIMES), 3),
                                       op=lambda t: (1 - t) * 100), 1)
emit("p34.bill.breakeven", int(BREAKEVEN))
emit("p34.bill.cache.a", reproduces(CACHE_A, 0, (float(TOK_A), 0), (KV_MIB, 1),
                                    op=lambda t, m: t * m), 0)
emit("p34.bill.cache.b", CACHE_B, 0)
emit("p34.bill.conc.times", reproduces(CONC_TIMES, 2, (CACHE_A, 0), (CACHE_B, 0),
                                       op=lambda a, b: a / b), 2)


# ======================================================================
# SECTION 6 --- THE MEASURES THAT LOOK LIKE MEASUREMENTS.
#
# Programs P29 and P31 each found one, and neither wrote a P34 pointer, so
# this bracket is inferred from content rather than handed over.  Both are
# read back rather than re-derived.
#
#   P29 section 6  bits per character is a ratio missing its second quantity,
#                  and the model's contribution cancels out of it entirely.
#   P31 section 4  the plug-in estimator returns a POSITIVE number on data
#                  with no dependence at all, in expectation, at every N.
#   P31 section 5  a better probe cannot mean more information, and a weak
#                  probe does not mean little.  One inequality, both ends.
# ======================================================================

BIAS_50 = float(committed("p31.tex", "p31.bias.n50") or 0.010332)
BIAS_100 = float(committed("p31.tex", "p31.bias.n100") or 0.005079)

# The 1/N law, checked between P31's own two committed sizes.
LAW = BIAS_50 / BIAS_100
assert 1.9 < LAW < 2.1, LAW

PROBE_I = 0.05                                  # what a probe reports at N = 50
PROBE_SHARE = 100.0 * BIAS_50 / PROBE_I
assert 0 < PROBE_SHARE < 100, PROBE_SHARE

# The count at which the artefact is under a twentieth of the reported figure.
PROBE_TOL = 0.05 * PROBE_I
PROBE_N = math.ceil(BIAS_100 * 100.0 / PROBE_TOL)
assert BIAS_100 * 100.0 / PROBE_N <= PROBE_TOL
assert BIAS_100 * 100.0 / (PROBE_N - 1) > PROBE_TOL
assert PROBE_N > 50

# P31's data-processing gap, read back and left as a bound rather than a figure.
DPI_BEST = float(committed("p31.tex", "p31.dpi.best") or 0.0647)
DPI_IXY = float(committed("p31.tex", "p31.dpi.ixy") or 0.0872)
assert DPI_BEST < DPI_IXY
assert 1.0 - DPI_BEST / DPI_IXY > 0.25

emit("p34.probe.i", PROBE_I, 2)
emit("p34.probe.share.pct", reproduces(pct(PROBE_SHARE), 1, (BIAS_50, 6),
                                       (PROBE_I, 2), op=lambda b, i: 100.0 * b / i), 1)
emit("p34.probe.n", PROBE_N)


# ======================================================================
# THE TRANSCRIPT.  Section 2's flip, in the only form a reader can check:
# both models fixed, both subset scores fixed, one weight changed.
#
# The rounding is INSIDE the listing, which is P19's rule -- a transcript is
# a claim about what a session prints, so every transformation applied to a
# value has to be visible in it.
# ======================================================================

def _repl(short: float, long_: float, w: float) -> float:
    return round(100 * (w * short + (1 - w) * long_), 2)


_bs, _bl = B_SHORT / 100, B_LONG / 100
_as, _al = A_SHORT / 100, A_LONG / 100
_w = float(ALT)
_even = [_repl(_bs, _bl, 0.5), _repl(_as, _al, 0.5)]
_alt = [_repl(_bs, _bl, _w), _repl(_as, _al, _w)]
assert f"{_even[0]:.1f}" == committed("p27.tex", "p27.near.hi")
assert f"{_even[1]:.1f}" == committed("p27.tex", "p27.near.lo")
assert _alt[1] > _alt[0], _alt
assert f"{_alt[0]:.2f}" == f"{float(B_ALT) * 100:.2f}", _alt
assert f"{_alt[1]:.2f}" == f"{float(A_ALT) * 100:.2f}", _alt

_lines = [
    ">>> def score(short, long_, w):",
    "...     return round(100 * (w*short + (1-w)*long_), 2)",
    "...",
    f">>> [score({_bs:.2f}, {_bl:.2f}, 0.5), "
    f"score({_as:.2f}, {_al:.2f}, 0.5)]",
    repr(_even),
    f">>> [score({_bs:.2f}, {_bl:.2f}, {_w}), "
    f"score({_as:.2f}, {_al:.2f}, {_w})]",
    repr(_alt),
]
for _l in _lines:
    assert len(_l) <= 64, (len(_l), _l)


# ======================================================================
# WRITE
# ======================================================================

def main() -> None:
    TRANSCRIPT.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPT / "p34-remix.txt").write_text("\n".join(_lines) + "\n",
                                              encoding="utf8")
    rows = []
    for key, (body, numeric) in VALUES.items():
        macro = "mfaval" if numeric else "mfavaltext"
        rows.append(f"\\{macro}{{{key}}}{{{body}}}")
    OUT.write_text("%% generated by code/p34_measuring_honestly.py\n"
                   + "\n".join(rows) + "\n", encoding="utf8")
    print(f"wrote {len(VALUES)} values to {OUT}")
    for key, (body, _) in VALUES.items():
        print(f"  {key:32s} {body}")


if __name__ == "__main__":
    main()
