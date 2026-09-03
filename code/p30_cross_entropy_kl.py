"""P30 --- Cross-entropy and the Kullback--Leibler divergence.

Every number Program P30 prints, and the assertions that keep them honest.

WHAT THE NEIGHBOURS ALREADY SPENT.  Every debt this program is owed is written
down in the program that owes it -- `grep -rn 'prog:P30' programs/en/*.tex`
prints the list with its contexts, and that grep was the first thing run.  Do
not restate it as a count here; the list is what is checkable.  What it names:

  P29  built the whole of the machinery: surprise, entropy, Kraft, and entropy
       as the SHORTEST AVERAGE CODE LENGTH, enumerated exhaustively.  It says
       in section 4 and again in its closing frame that it computes the entropy
       of ONE distribution and never a quantity between two -- so this program
       may not re-teach any of it, and must not contradict that sentence.
       AND ITS TWO ALPHABETS ARE THIS PROGRAM'S ARRIVAL.  P29 reports that the
       best code for (2/5, 1/5, 1/5, 1/5) averages 2.000 bits against an
       entropy of 1.922 and calls the 0.078 gap "the rounding of a length to a
       whole number".  The winning lengths are (1, 2, 3, 3), whose Kraft sum is
       exactly 1, so the code implies q_i = 2^-l_i = (1/2, 1/4, 1/8, 1/8) --
       which is P29's OTHER row.  The gap IS KL(p||q).  Nothing new is computed
       to arrive: this program says what a number already on the page is.
  P26  says in as many words that "what vanishes is the EXCESS of the
       cross-entropy over the target's own entropy, and that excess has a name
       and is P30's".  It also owns cross-entropy as a negative log-likelihood,
       so section 8 closes its loop rather than re-deriving it.
  P19  owns Jensen in both directions.  So KL >= 0 is two lines from a theorem
       the reader already has, not a new proof -- and P19's own file header
       says `KL, Jensen-Shannon, the asymmetry -> P30`.
  P22  declares the one KL fact its whole payoff rests on (non-negative, zero
       only when the two agree) in a rigourbox naming this program.
  P18  gives cross-entropy a definitional frame and says WHAT IT MEASURES is
       P30's -- "the cost of coding one distribution with another's code",
       which is section 1's sentence, already written for it.
  P28  prices a miscalibrated judge in ODDS deliberately and hands the reading
       in nats over.  P02 says P30 gives cross-entropy its meaning in bits.
       F02 and F03 both point here for units and meaning.
  F09  gives the reader the TRIANGLE INEQUALITY and its equality condition, and
       P05 confirms it for a norm.  That is why section 6 lands: the reader
       knows what the word "distance" was promising before it is taken away.
  F05  owns the four-token distribution at three temperatures and committed all
       twelve probabilities, including that the tail rises MORE THAN FIFTYFOLD
       -- which is exactly why the two directions differ, readable off its own
       table rather than asserted here.

WHAT IS GENUINELY LEFT, and nothing in the book mentions any of it:
  1. the asymmetry, and what it costs when you pick a loss;
  2. forward KL mode-covering against reverse KL mode-seeking, MEASURED;
  3. that KL is not a distance, against a property F09 gave the reader;
  4. Jensen--Shannon, and what the symmetry costs.

METHOD.  Program P05's greedy-packing failure is the standing warning: a
demonstration whose answer depends on where an optimiser stopped MEASURES THE
SEARCH rather than the geometry.  So every candidate here is ENUMERATED and
every divergence is exact where the arithmetic allows.  Two designs were probed
and thrown away before a line of prose existed, and both failures are in the
frames because they are the mechanism:
  * a target with ZEROS makes reverse KL infinite too, which destroys the
    asymmetry the section exists to show -- the target must be strictly
    positive everywhere;
  * a target whose modes are not sharp enough leaves reverse KL preferring a
    WIDE candidate, because -H(q) dominates.

NOT SPENT HERE, deliberately:
  P31  owns mutual information and the data-processing inequality.

Run:  python3 code/p30_cross_entropy_kl.py
"""

from __future__ import annotations

import itertools
import math
import re
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p30.tex"
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
    """Refuse a percentage that rounds to 0 or 100 and so reads as exact."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not.")
    return x


def reproduces(value: float, digits: int, *operands, op) -> float:
    """Refuse a quantity that does not come back out of its own printed page.

    P28 added the half that matters and P29 paid for it again: this checks an
    arithmetic RESULT against printed operands, and says nothing about the
    route a reader actually takes.  Where the page prints a row, divide THAT
    row as well -- see the ratio in section 3."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


# ======================================================================
# The three quantities.  KL returns inf where q is zero and p is not, and
# that infinity is not an edge case to be smoothed away -- it is section
# 4's whole mechanism and section 5's whole finding.
# ======================================================================
LOG2 = math.log(2)


def entropy(p) -> float:
    return -sum(float(x) * math.log(float(x)) for x in p if x)


def cross_entropy(p, q) -> float:
    for pi, qi in zip(p, q):
        if pi and not qi:
            return math.inf
    return -sum(float(pi) * math.log(float(qi)) for pi, qi in zip(p, q) if pi)


def kl(a, b) -> float:
    t = 0.0
    for ai, bi in zip(a, b):
        if ai == 0:
            continue
        if bi == 0:
            return math.inf
        t += float(ai) * math.log(float(ai) / float(bi))
    return t


def js(a, b) -> float:
    m = [(x + y) / 2 for x, y in zip(a, b)]
    return (kl(a, m) + kl(b, m)) / 2


# ======================================================================
# 1.  THE ARRIVAL.  Program P29's own two alphabets are the source and the
#     code of ONE divergence, and its "rounding" gap IS that divergence.
#     Nothing is computed here that P29 did not already print; what is new
#     is what the number is.  Gated three ways so the two cannot drift.
# ======================================================================
DYADIC = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)]
NONDY = [Fraction(2, 5), Fraction(1, 5), Fraction(1, 5), Fraction(1, 5)]
LENGTHS = (1, 2, 3, 3)                       # P29's winning code, in bits

# The code is COMPLETE -- its Kraft sum is exactly one -- which is what makes
# q_i = 2^-l_i a distribution and the identity below an identity rather than
# an inequality.  Assert it rather than assume it.
assert sum(Fraction(1, 2 ** l) for l in LENGTHS) == 1
assert [Fraction(1, 2 ** l) for l in LENGTHS] == DYADIC

H_SRC = entropy(NONDY) / LOG2
CE_SRC = cross_entropy(NONDY, DYADIC) / LOG2
KL_SRC = kl(NONDY, DYADIC) / LOG2

emit("p30.src.h", H_SRC, 3)
emit("p30.src.ce", CE_SRC, 3)
emit("p30.src.kl", KL_SRC, 3)

# The identity, exactly: the code length IS the entropy plus the divergence.
assert abs(CE_SRC - (H_SRC + KL_SRC)) < 1e-12, (CE_SRC, H_SRC, KL_SRC)
# And the code length is literally the average of the lengths, which is what
# makes "cross-entropy is a code length" a statement rather than a metaphor.
assert abs(CE_SRC - sum(float(p) * l for p, l in zip(NONDY, LENGTHS))) < 1e-12

# GATE on P29, three values.  If any of them moves, this program is quietly
# about a different pair of alphabets and the build says so.
for key, got in (("p29.nondy.h", H_SRC),
                 ("p29.nondy.best", CE_SRC),
                 ("p29.nondy.gap", KL_SRC)):
    _c = committed("p29.tex", key)
    if _c is not None:
        assert abs(float(_c) - got) < 5e-4, (key, _c, got)
NOTES.append(
    f"  * P29's 'rounding' gap IS a divergence: {H_SRC:.3f} + {KL_SRC:.3f}"
    f" = {CE_SRC:.3f} bits, and the two alphabets are the source and the code.")


# ======================================================================
# 2.  The excess cannot be negative, and it is zero only when the two
#     agree.  Program P19 owns Jensen, so this is a check rather than a
#     proof: the proof is two lines of the reader's own theorem.
# ======================================================================
GRID_D = 12
_simplex3 = [(Fraction(i, GRID_D), Fraction(j, GRID_D),
              Fraction(GRID_D - i - j, GRID_D))
             for i in range(1, GRID_D) for j in range(1, GRID_D)
             if GRID_D - i - j > 0]
emit("p30.simplex.n", len(_simplex3))

_neg = [(a, b) for a in _simplex3 for b in _simplex3 if kl(a, b) < -1e-12]
assert not _neg, _neg[:1]
_zero = [(a, b) for a in _simplex3 for b in _simplex3
         if kl(a, b) == 0.0 and a != b]
assert not _zero, _zero[:1]
assert all(kl(a, a) == 0.0 for a in _simplex3)
NOTES.append(
    f"  * over all {len(_simplex3)**2} ordered pairs on the grid, the excess is"
    f" never negative and is zero only where the two agree.")


# ======================================================================
# 3.  It is not symmetric.  Measured on Program F05's own four-token
#     distribution, whose twelve probabilities are already committed and
#     which the reader met twenty-five programs ago -- so the REASON is
#     readable off a table the book already printed.
# ======================================================================
def _f05(t: str) -> list[float]:
    return [float(committed("f05.tex", f"f05.sm.t{t}.p{i}") or 0.0)
            for i in (1, 2, 3, 4)]


T05, T20 = _f05("05"), _f05("20")
assert abs(sum(T05) - 1) < 1e-3 and abs(sum(T20) - 1) < 1e-3, (T05, T20)

FWD = kl(T05, T20)          # the peaked one on top
REV = kl(T20, T05)          # the broad one on top
emit("p30.f05.fwd", FWD, 4)
emit("p30.f05.rev", REV, 4)
# The ratio is the thing the frame quotes, so it is checked against the two
# figures AS THE PAGE PRINTS THEM and not only against the exact values --
# which is P28's finding and the reason P29's helper carries the note it does.
emit("p30.f05.ratio",
     reproduces(REV / FWD, 2, (REV, 4), (FWD, 4), op=lambda a, b: a / b), 2)
assert REV > FWD, (FWD, REV)

# And the reason, from F05's own tail: the broad distribution puts mass where
# the peaked one has almost none.  F05 measured that rise as "more than
# fiftyfold"; this asserts it rather than repeating the phrase.
# NOT EMITTED, deliberately.  Program F05 states this as a BOUND -- "more
# than fiftyfold" -- because its exact ratio is 51.7 and the ratio of its own
# printed table is 53.1, so a figure here would put two numbers that look like
# one on two pages.  That is Program F08's defect, and F05 already solved it.
TAIL_RATIO = T20[3] / T05[3]
assert TAIL_RATIO > 50, TAIL_RATIO

# P29's own pair is NEARLY symmetric -- 0.0781 against 0.0719 -- which is the
# second half of the section: the size of one direction tells you nothing
# about the other, so the choice is made on the mechanism and never on a
# measurement.  Emitted because the frame quotes both.
emit("p30.src.klrev", kl(DYADIC, NONDY) / LOG2, 3)
assert abs(kl(DYADIC, NONDY) / LOG2 - KL_SRC) < 0.02
NOTES.append(
    f"  * F05's own distribution, both directions: {FWD:.4f} against {REV:.4f}"
    f" nats, a ratio of {REV / FWD:.2f} -- while P29's pair is nearly equal.")


# ======================================================================
# 4-5.  MODE-COVERING AGAINST MODE-SEEKING, enumerated.
#
#   Program P05's greedy-packing failure is the warning this design was
#   built against: a fit found by an optimiser measures the SEARCH.  So
#   the candidate family is finite and EVERY member is evaluated, which
#   makes the result a proof over that family -- P14's distinction.
#
#   The mechanism is an infinity and needs no optimiser at all.  Forward
#   KL(p||q) contains p_i log(p_i/q_i), so a q that is zero where p is
#   positive costs +inf.  Reverse KL(q||p) contains q_i log(q_i/p_i), so
#   the same omission costs it NOTHING.  That is the whole asymmetry and
#   it is a property of which distribution sits in the numerator.
#
#   TWO DESIGNS WERE PROBED AND THROWN AWAY, and both failures are in the
#   frames because they are the mechanism seen from the side:
#     * a target with ZEROS makes reverse KL infinite too (77 of 81), so
#       the asymmetry disappears -- the target must be strictly positive;
#     * a target whose modes are not sharp enough leaves reverse KL
#       preferring a WIDE candidate, because -H(q) dominates.
# ======================================================================
BINS = 9
MODE_A, MODE_B = 1, 7


def bump(centre: int, half: int) -> list[Fraction]:
    """A triangular candidate: half = 0 is a point mass, 8 spans the row."""
    w = [max(0, half + 1 - abs(i - centre)) for i in range(BINS)]
    return [Fraction(x, sum(w)) for x in w]


FAMILY = [(c, h) for c in range(BINS) for h in range(BINS)]
emit("p30.fam.n", len(FAMILY))
emit("p30.bins", BINS)

TARGETS = {
    "tall+short": [1, 60, 1, 1, 1, 1, 1, 30, 1],
    "two sharp": [1, 50, 2, 1, 1, 1, 2, 40, 1],
    "spike+hump": [1, 70, 1, 1, 2, 4, 8, 10, 3],
    "near-equal": [1, 45, 1, 1, 1, 1, 1, 45, 1],
    "wide gap": [1, 100, 3, 1, 1, 1, 3, 60, 1],
}
emit("p30.targets.n", len(TARGETS))

_headline = None
for _name, _w in TARGETS.items():
    P = [Fraction(x, sum(_w)) for x in _w]
    assert all(x > 0 for x in P), _name          # strictly positive, on purpose
    qf = bump(*min(FAMILY, key=lambda ch: kl(P, bump(*ch))))
    qr = bump(*min(FAMILY, key=lambda ch: kl(bump(*ch), P)))
    # THE FINDING, asserted rather than reported, so a change of target
    # cannot quietly falsify the section:
    assert sum(1 for x in qf if x) == BINS, (_name, "forward did not spread")
    assert sum(1 for x in qr if x) == 1, (_name, "reverse did not collapse")
    assert sum(qr[MODE_B:]) == 0, (_name, "reverse kept mass on mode 2")
    assert sum(qf[MODE_B:]) > 0, (_name, "forward abandoned mode 2")
    if _name == "near-equal":
        _headline = (P, qf, qr)

P_HEAD, QF, QR = _headline
emit("p30.head.mode2", pct(100 * float(sum(P_HEAD[MODE_B:]))), 1)
emit("p30.fwd.mode2", pct(100 * float(sum(QF[MODE_B:]))), 1)
emit("p30.fwd.width", sum(1 for x in QF if x))
emit("p30.rev.width", sum(1 for x in QR if x))
# The reverse answer is EXACTLY zero, so it is a count and never a percentage:
# "0.0 per cent" reads as rounding and this is not rounding.  P21's rule.
assert sum(QR[MODE_B:]) == 0

FIN_FWD = sum(1 for ch in FAMILY if kl(P_HEAD, bump(*ch)) < math.inf)
FIN_REV = sum(1 for ch in FAMILY if kl(bump(*ch), P_HEAD) < math.inf)
emit("p30.fin.fwd", FIN_FWD)
emit("p30.fin.rev", FIN_REV)
assert FIN_REV == len(FAMILY) and FIN_FWD < len(FAMILY)
NOTES.append(
    f"  * over {len(FAMILY)} candidates on {len(TARGETS)} targets: forward"
    f" always takes the widest and keeps {100 * float(sum(QF[MODE_B:])):.1f}%"
    f" on the second mode; reverse always takes a point mass and keeps none.")
NOTES.append(
    f"  * candidates with a finite value: forward {FIN_FWD}, reverse {FIN_REV},"
    f" of {len(FAMILY)} -- the infinity is the mechanism.")


# ======================================================================
# 6.  It is not a distance, and it fails as the COMMON CASE rather than
#     in a corner.  Program F09 gave the reader the triangle inequality
#     and its equality condition and P05 confirmed it for a norm, so the
#     contrast is against a property they can check -- which is what
#     makes "KL distance" a misnomer rather than pedantry.
# ======================================================================
_triples = list(itertools.permutations(_simplex3, 3))
_bad = [(a, b, c) for a, b, c in _triples if kl(a, c) > kl(a, b) + kl(b, c)]
emit("p30.tri.total", len(_triples))
emit("p30.tri.bad", len(_bad))
emit("p30.tri.pct", pct(100 * len(_bad) / len(_triples)), 1)
assert _bad, "no counterexample -- the section has nothing to show"

TA, TB, TC = max(_bad, key=lambda t: kl(t[0], t[2]) - kl(t[0], t[1]) - kl(t[1], t[2]))
emit("p30.tri.direct", kl(TA, TC), 4)
emit("p30.tri.via", kl(TA, TB) + kl(TB, TC), 4)
emit("p30.tri.gap", kl(TA, TC) - kl(TA, TB) - kl(TB, TC), 4)
emit("p30.tri.den", GRID_D)
NOTES.append(
    f"  * the triangle inequality fails for {len(_bad)} of {len(_triples)}"
    f" ordered triples -- {100 * len(_bad) / len(_triples):.1f} per cent, so"
    f" it is the common case; the worst detour is SHORTER by"
    f" {kl(TA, TC) - kl(TA, TB) - kl(TB, TC):.4f} nats.")


# ======================================================================
# 7.  Why not just symmetrise it.  Jensen--Shannon is symmetric and
#     bounded, and the bound IS the cost: it saturates, so it says the
#     same thing however far apart two distributions are -- which is no
#     signal at all in the regime a training run starts in.
# ======================================================================
def _point(i: int, n: int = 10) -> list[Fraction]:
    return [Fraction(1) if j == i else Fraction(0) for j in range(n)]


_seps = (1, 2, 3, 4)
_js = [js(_point(0), _point(s)) for s in _seps]
assert all(abs(x - _js[0]) < 1e-12 for x in _js), _js       # exactly equal
assert abs(_js[0] - math.log(2)) < 1e-12, _js[0]            # and it is ln 2
assert all(kl(_point(0), _point(s)) == math.inf for s in _seps)
emit("p30.js.cap", _js[0], 4)
emit("p30.js.seps", len(_seps))
emit("p30.js.far", max(_seps))
NOTES.append(
    f"  * Jensen--Shannon puts point masses {min(_seps)} and {max(_seps)} bins"
    f" apart at exactly the same distance, ln 2 = {_js[0]:.4f}, where KL is"
    f" infinite for both.")

# The OVERLAPPING pair a further problem asks about, gated for the same reason.
# Disjoint support attains the bound; sharing an outcome does not, and the gap
# is a factor of three rather than a rounding.
_half = [Fraction(1, 2), Fraction(1, 2)]
_mass = [Fraction(1), Fraction(0)]
JS_OVERLAP = js(_half, _mass)
emit("p30.js.overlap", JS_OVERLAP, 4)
assert JS_OVERLAP < 0.5 * math.log(2), (JS_OVERLAP, math.log(2))
assert math.log(2) / JS_OVERLAP > 3.0, math.log(2) / JS_OVERLAP
# And the two halves of the same answer: one direction is infinite because q
# is zero where p has weight, the other is exactly ln 2.
assert kl(_half, _mass) == math.inf
assert abs(kl(_mass, _half) - math.log(2)) < 1e-12, kl(_mass, _half)


# ======================================================================
# 8.  Where the choice is already made for you.  Minimising cross-entropy
#     against a fixed dataset IS minimising forward KL to the empirical
#     distribution, because H(empirical) does not depend on the model --
#     so every run the reader has launched minimised the mode-covering
#     direction.  This closes the loop Program P26 opened.
# ======================================================================
EMP = [Fraction(3, 10), Fraction(4, 10), Fraction(2, 10), Fraction(1, 10)]
H_EMP = entropy(EMP)
emit("p30.emp.h", H_EMP, 4)

_models = {
    "uniform": [Fraction(1, 4)] * 4,
    "exact": list(EMP),
    "swapped": [Fraction(4, 10), Fraction(3, 10), Fraction(2, 10), Fraction(1, 10)],
}
for _n, _m in _models.items():
    # the identity, exactly, at every model: CE = H(emp) + KL(emp || model)
    assert abs(cross_entropy(EMP, _m) - (H_EMP + kl(EMP, _m))) < 1e-12, _n
_CE_UNI = cross_entropy(EMP, _models["uniform"])
_KL_UNI = kl(EMP, _models["uniform"])
# Section 8 prints all three of these on one page as an instance of the
# identity, so the reader will ADD the two on the right.  The assertion
# above is on the underlying floats and says nothing about that -- which is
# exactly the gap P28 found and P29 found again.  So check the sum in the
# form the page prints it, which is the only form anybody will check.
reproduces(_CE_UNI, 4, (H_EMP, 4), (_KL_UNI, 4), op=lambda a, b: a + b)
emit("p30.emp.ce.uniform", _CE_UNI, 4)
emit("p30.emp.kl.uniform", _KL_UNI, 4)
# The perfect model drives the excess to EXACTLY zero, which is a count and
# not a rounding, so the frame says so rather than printing 0.0000.
assert kl(EMP, _models["exact"]) == 0.0
assert abs(cross_entropy(EMP, _models["exact"]) - H_EMP) < 1e-12
NOTES.append(
    f"  * cross-entropy against a fixed dataset is H(emp) + forward KL, at"
    f" every model tried, and H(emp) = {H_EMP:.4f} nats does not move -- so"
    f" training minimises the MODE-COVERING direction.")


# ======================================================================
# The transcript.  Every transformation is INSIDE the listing, because
# Programs P19, P24, P27 and P28 each shipped a draft where it was not --
# a file generated by code/ and gated for drift is STILL a fabrication if
# the rounding happened to its output rather than in its code.
#
# It prints the two directions on one pair and the infinity, which is the
# whole of sections 3 and 4 in five lines.  It answers nothing asked
# after it: section 5's question is which CANDIDATE each direction picks,
# and the listing contains no candidates.
# ======================================================================
TRANSCRIPT = OUT.parent.parent / "transcripts"
_lines = [
    ">>> from math import log, inf",
    ">>> def kl(a, b):    # nats; inf if b is 0 where a is not",
    "...     if any(x and not y for x, y in zip(a, b)):",
    "...         return inf",
    "...     s = sum(x * log(x / y) for x, y in zip(a, b) if x)",
    "...     return round(s, 4)",
    ">>> p, q = [0.9, 0.1], [0.5, 0.5]",
    ">>> kl(p, q), kl(q, p)",
]
_p, _q = [0.9, 0.1], [0.5, 0.5]
_kl = lambda a, b: round(sum(x * math.log(x / y) for x, y in zip(a, b) if x), 4)
_lines.append(repr((_kl(_p, _q), _kl(_q, _p))))
_lines += [
    ">>> kl([0.5, 0.5], [1.0, 0.0]), kl([1.0, 0.0], [0.5, 0.5])",
    repr((math.inf, round(math.log(2), 4))),
]
assert max(len(x) for x in _lines) <= 64, max(_lines, key=len)
TRANSCRIPT.mkdir(parents=True, exist_ok=True)
(TRANSCRIPT / "p30-both-directions.txt").write_text(
    "\n".join(_lines) + "\n", encoding="utf8")


# ======================================================================
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf8") as fh:
    fh.write("% Generated by code/p30_cross_entropy_kl.py -- do not edit.\n")
    for k, (body, numeric) in VALUES.items():
        fh.write(f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}\n")

print(f"P30: {len(VALUES)} values -> {OUT}")
for n in NOTES:
    print(n)
