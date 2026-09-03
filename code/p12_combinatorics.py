#!/usr/bin/env python3
"""Program P12 --- Combinatorics and counting.

Every number Program P12 prints that the reader cannot do in their head is
computed here and written to figures/values/p12.tex, which the book \\input{}s.

P12's thesis is that four counting rules settle almost every "how big is this
going to be" question an engineer meets, and that the two questions to ask
first --- does order matter, are repeats allowed --- decide which rule applies.

WHAT P12 IS OWED, read out of the written files rather than remembered:

  F10  is the elementary layer under this program and says so. It supplies the
       PRODUCT RULE with its independence condition, 2^n SUBSETS, the PAIR
       COUNT n(n-1)/2 with its "halve it because a set discards order" step,
       and INCLUSION-EXCLUSION FOR TWO SETS -- and it defers, by name, "the
       four rules formally, pigeonhole, the birthday calculation" to here.
       Two of its committed values are gated against below, because this
       program re-derives both of them from the general rules.
  F04  gives the factorial as a pi with the index in the body, n! = prod i,
       AND the empty product, which is why 0! = 1 needs no separate rule.
  F03  gives logarithms, which is the only way to hold 32000^20 in a head.
  P02  section 4 is "Never form a probability", and section 4 here is that
       finding arriving in a place nobody expects it: the textbook expression
       for a collision probability returns EXACTLY ZERO in float64 at 128
       bits, which reads as a proof of safety and is a rounding artefact.
  P03  owns O-notation. This program counts; it never says "quadratic".

WHAT THIS PROGRAM LEAVES ALONE, checked against tools/programs.json:
  what a probability IS, and conditioning                          -> P23
  random variables, expectation, variance                          -> P24
  graphs and their counting arguments                              -> P13
  writing a proof, quantifiers, induction                          -> P14

THE BRIEF SAYS "simple recurrences", and this program reads that narrowly and
on purpose: a counting program's recurrence should COUNT something. Two do.
Pascal's rule is one -- and it is also why math.comb is exact -- and the
birthday product is the other, since P(m) = P(m-1) x (1 - (m-1)/N) is exactly
how the number is computed. Neither was invented to discharge the brief.

Run:  python3 code/p12_combinatorics.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p12.tex"
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


def sci(x: float, digits: int = 2) -> str:
    """A number too large or too small to write out, in the book's own form."""
    return f"{x:.{digits}e}"


def committed(fname: str, key: str) -> str | None:
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    import re
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


# =====================================================================
# 1. The two questions, and the four counts they pick out
# =====================================================================
# Ten features, choose three. The whole of section 1 is this one table, and
# every cell is small enough that a reader can check it by hand -- which is
# the reason n and k are 10 and 3 rather than anything more impressive.
N_FEAT, K_PICK = 10, 3

ORDERED_REPEATS = N_FEAT ** K_PICK                       # n^k
ORDERED_NOREP = math.perm(N_FEAT, K_PICK)                # n!/(n-k)!
UNORDERED_NOREP = math.comb(N_FEAT, K_PICK)              # C(n, k)
UNORDERED_REPEATS = math.comb(N_FEAT + K_PICK - 1, K_PICK)   # stars and bars

# Checked by ENUMERATION rather than by trusting the formulas, because the
# whole point of the table is that the four cells count four different sets of
# things and it is the SETS that differ, not the arithmetic.
_prod = [t for t in __import__("itertools").product(range(N_FEAT), repeat=K_PICK)]
assert len(_prod) == ORDERED_REPEATS
assert len(list(permutations(range(N_FEAT), K_PICK))) == ORDERED_NOREP
assert len(list(combinations(range(N_FEAT), K_PICK))) == UNORDERED_NOREP
assert len({tuple(sorted(t)) for t in _prod}) == UNORDERED_REPEATS, \
    "the fourth cell counts SORTED tuples with repeats, and stars and bars " \
    "must give the same number as collapsing every ordering of them"

for k, v in (("n", N_FEAT), ("k", K_PICK), ("ordrep", ORDERED_REPEATS),
             ("ordnorep", ORDERED_NOREP), ("unordnorep", UNORDERED_NOREP),
             ("unordrep", UNORDERED_REPEATS)):
    emit(f"p12.four.{k}", v)

# =====================================================================
# 2. Arrangements and choices
# =====================================================================
FACT_N = math.factorial(N_FEAT)                  # 10! orderings of ten things
emit("p12.fact.n", FACT_N)
assert FACT_N == ORDERED_NOREP * math.factorial(N_FEAT - K_PICK), \
    "n! = n!/(n-k)! x (n-k)!, which is the shrinking pool read backwards"

# The division that turns an arrangement into a choice is by k!, and that is
# F10's "halve it" generalised: F10 halved because 2! = 2.
assert ORDERED_NOREP // math.factorial(K_PICK) == UNORDERED_NOREP
emit("p12.kfact", math.factorial(K_PICK))

# --- CROSS-PROGRAMME GATE (a shared computation, not a coincidence) --------
# F10 counts pairs as n(n-1)/2 and says the halving is a set fact. This
# program counts them as C(n, 2). The two must name the same number, or one of
# the programs is wrong about what a pair is.
_f10_docs = committed("f10.tex", "f10.docs")
_f10_pairs = committed("f10.tex", "f10.pairs")
if _f10_docs and _f10_pairs:
    assert math.comb(int(_f10_docs), 2) == int(_f10_pairs), \
        "C(n,2) must reproduce Program F10's committed pair count exactly"
    NOTES.append(f"gate: C({_f10_docs}, 2) == F10's {_f10_pairs} pairs")
else:                                                        # pragma: no cover
    NOTES.append("F10's values not built yet; the pair gate did not run")

# The symmetry, which surprises people and has a one-line reason.
SYM_N, SYM_K = 20, 3
assert math.comb(SYM_N, SYM_K) == math.comb(SYM_N, SYM_N - SYM_K), \
    "choosing k to keep IS choosing n-k to drop"
emit("p12.sym.n", SYM_N)
emit("p12.sym.k", SYM_K)
emit("p12.sym.val", math.comb(SYM_N, SYM_K))
emit("p12.sym.rest", SYM_N - SYM_K)
emit("p12.sym.peak", math.comb(SYM_N, SYM_N // 2))

# An ablation study is the choice count doing a design decision. Every subset
# of the features is 2^n runs; every subset of at most three is a sum of four
# binomial coefficients, and the two numbers are the whole argument.
ABL_N, ABL_K = 20, 3
ABL_ALL = 2 ** ABL_N
ABL_UPTO = sum(math.comb(ABL_N, k) for k in range(ABL_K + 1))
assert ABL_UPTO == 1 + ABL_N + math.comb(ABL_N, 2) + math.comb(ABL_N, 3)
emit("p12.abl.n", ABL_N)
emit("p12.abl.k", ABL_K)
emit("p12.abl.all", ABL_ALL)
emit("p12.abl.upto", ABL_UPTO)
emit("p12.abl.frac", sci(ABL_UPTO / ABL_ALL, 1))
emit("p12.abl.singles", ABL_N)
emit("p12.abl.pairs", math.comb(ABL_N, 2))
# NOT emitted: C(20,3) is p12.sym.val two frames earlier, and one number
# under two names is one number only one of which will ever be corrected.
assert math.comb(ABL_N, ABL_K) == math.comb(SYM_N, SYM_K)

# =====================================================================
# 3. The rules that are not products
# =====================================================================
# Pascal's rule: a recurrence, and the reason math.comb is exact -- it never
# forms a factorial it then has to divide away.
for n in range(1, 31):
    for k in range(1, n):
        assert math.comb(n, k) == math.comb(n - 1, k - 1) + math.comb(n - 1, k)

# --- CROSS-PROGRAMME GATE ------------------------------------------------
# Summing a row of Pascal's triangle gives 2^n, so this program's choices and
# F10's subsets are two ways of counting one thing: pick the SIZE, then pick
# WHICH. If they disagree, one of the two programs is wrong.
_f10_feat = committed("f10.tex", "f10.features")
_f10_sub = committed("f10.tex", "f10.subsets")
if _f10_feat and _f10_sub:
    _n = int(_f10_feat)
    assert sum(math.comb(_n, k) for k in range(_n + 1)) == int(_f10_sub), \
        "sum_k C(n,k) must reproduce Program F10's committed subset count"
    NOTES.append(f"gate: sum_k C({_f10_feat},k) == F10's {_f10_sub} subsets")
else:                                                        # pragma: no cover
    NOTES.append("F10's values not built yet; the subset gate did not run")

# --- inclusion-exclusion for three sets, checked against a REAL union -----
# Built out of its seven regions as explicit sets rather than as arithmetic, so
# what is verified is the FORMULA and not the author's ability to add three
# numbers. All seven regions are non-empty on purpose: a Venn diagram with an
# empty cell makes the alternating sign look like decoration.
#
# The first two sets are Program F10's two evaluation sets, to the element, so
# this is a continuation of a worked example the reader has already seen rather
# than a fresh one -- and the gate below says so in code.
REGIONS = {"a": 700, "b": 800, "c": 500,
           "ab": 150, "ac": 100, "bc": 200, "abc": 50}
_pos, _R = 0, {}
for _k, _n in REGIONS.items():
    _R[_k] = set(range(_pos, _pos + _n))
    _pos += _n
_A = _R["a"] | _R["ab"] | _R["ac"] | _R["abc"]
_B = _R["b"] | _R["ab"] | _R["bc"] | _R["abc"]
_C = _R["c"] | _R["ac"] | _R["bc"] | _R["abc"]

IE_A, IE_B, IE_C = len(_A), len(_B), len(_C)
IE_AB, IE_AC, IE_BC = len(_A & _B), len(_A & _C), len(_B & _C)
IE_ABC = len(_A & _B & _C)
IE_UNION = len(_A | _B | _C)
IE_NAIVE = IE_A + IE_B + IE_C
assert IE_UNION == (IE_A + IE_B + IE_C
                    - IE_AB - IE_AC - IE_BC
                    + IE_ABC), "inclusion-exclusion must give the real union"
assert min(len(v) for v in _R.values()) > 0, "every region must be occupied"
assert len({IE_AB, IE_AC, IE_BC}) == 3, \
    "the three overlaps must differ, or a reader cannot tell which is which"

# --- CROSS-PROGRAMME GATE: this IS Program F10's example, with a third set --
_pairs = [("f10.eval.a", IE_A), ("f10.eval.b", IE_B),
          ("f10.eval.shared", IE_AB), ("f10.eval.union", IE_A + IE_B - IE_AB)]
if committed("f10.tex", "f10.eval.a"):
    for _key, _here in _pairs:
        assert int(committed("f10.tex", _key)) == _here, \
            f"{_key} must be the same set it was in Program F10"
    NOTES.append("gate: the first two sets ARE F10's two evaluation sets")
else:                                                        # pragma: no cover
    NOTES.append("F10's values not built yet; the eval-set gate did not run")

for k, v in (("a", IE_A), ("b", IE_B), ("c", IE_C), ("ab", IE_AB),
             ("ac", IE_AC), ("bc", IE_BC), ("abc", IE_ABC),
             ("union", IE_UNION), ("naive", IE_NAIVE),
             ("over", IE_NAIVE - IE_UNION),
             ("pairsum", IE_AB + IE_AC + IE_BC)):
    emit(f"p12.ie.{k}", v)

# How many terms the general rule has: every non-empty subset of the sets
# contributes one, so 2^n - 1. That is why nobody writes it out past three.
emit("p12.ie.terms3", 2 ** 3 - 1)
IE_SETS = 10
emit("p12.ie.sets", IE_SETS)
emit("p12.ie.terms10", 2 ** IE_SETS - 1)
assert 2 ** IE_SETS - 1 == sum(math.comb(IE_SETS, k)
                               for k in range(1, IE_SETS + 1)), \
    "the term count is the subset count without the empty one"

# --- pigeonhole ----------------------------------------------------------
PIG_ITEMS, PIG_BUCKETS = 1000, 256
PIG_FLOOR = -(-PIG_ITEMS // PIG_BUCKETS)          # ceil
emit("p12.pig.items", PIG_ITEMS)
emit("p12.pig.buckets", PIG_BUCKETS)
emit("p12.pig.floor", PIG_FLOOR)
# Tested rather than searched: as in Program P04, a random sweep here is
# testing the CODE, because a counterexample would refute a proof.
import random
random.seed(12)
for _ in range(2000):
    counts = [0] * PIG_BUCKETS
    for _ in range(PIG_ITEMS):
        counts[random.randrange(PIG_BUCKETS)] += 1
    assert max(counts) >= PIG_FLOOR, "pigeonhole cannot fail"
emit("p12.pig.trials", 2000)

# =====================================================================
# 4. The birthday calculation, and how many bits a hash needs
# =====================================================================
def collision_naive(m: int, N: int) -> float:
    """1 - prod_{i<m} (1 - i/N): the textbook expression, in float64.

    Written as the recurrence it is -- P(m) = P(m-1) x (1 - (m-1)/N) -- which
    is the second of this program's two counting recurrences.
    """
    p = 1.0
    for i in range(m):
        p *= (1 - i / N)
    return 1 - p


def collision(m: int, N: int) -> float:
    """The closed form, which is Program P02's rule applied to the same job.

    The exponent is the PAIR COUNT over N: m(m-1)/2 pairs, each colliding with
    probability 1/N. That is where Program F10's pair formula does the work,
    and it is the whole of why the answer is about sqrt(N) rather than N.
    """
    return -math.expm1(-m * (m - 1) / (2 * N))


def collision_ref(m: int, N: int) -> float:
    """A reference neither frame quotes: the product summed in log space.

    Not an approximation -- log1p and fsum are each accurate to a rounding,
    and expm1 undoes the log without subtracting anything from one. It is how
    the OTHER two are scored below, and it exists only for that.
    """
    return -math.expm1(math.fsum(math.log1p(-i / N) for i in range(m)))


# --- WHICH EXPRESSION IS RIGHT DEPENDS ON THE REGIME, and this is the
# measurement the section is built on. The two forms fail for OPPOSITE
# reasons: the product is destroyed by cancellation exactly when the answer is
# near zero, and the closed form drops a second-order term that matters only
# when the individual terms are large, which is exactly when the answer is
# near a half. Neither is the safe default.
BDAY_N, BDAY_M = 365, 23
BITS64, BITS128 = 64, 128
N64, N128 = 2 ** BITS64, 2 ** BITS128
CHECK_M, TRAP_M = 100_000, 10 ** 6

REGIMES = [
    ("bday", BDAY_M, BDAY_N),
    ("mid", CHECK_M, N64),
    ("tiny", TRAP_M, N128),
]
for _tag, _m, _N in REGIMES:
    _r = collision_ref(_m, _N)
    _n, _c = collision_naive(_m, _N), collision(_m, _N)
    emit(f"p12.reg.{_tag}.naive", sci(abs(_n - _r) / _r, 1))
    emit(f"p12.reg.{_tag}.closed", sci(abs(_c - _r) / _r, 1))

# The three claims the table makes, each asserted rather than read off:
assert collision_naive(BDAY_M, BDAY_N) == collision_ref(BDAY_M, BDAY_N), \
    "on the classic case the product must be right to the last bit"
assert abs(collision(BDAY_M, BDAY_N) - collision_ref(BDAY_M, BDAY_N)) \
    / collision_ref(BDAY_M, BDAY_N) > 0.01, \
    "and the closed form must be visibly out there, or the table has no point"
assert abs(collision(CHECK_M, N64) - collision_ref(CHECK_M, N64)) \
    / collision_ref(CHECK_M, N64) < 1e-9, \
    "at hash scale the closed form must be right to more digits than are printed"
assert abs(collision_naive(CHECK_M, N64) - collision_ref(CHECK_M, N64)) \
    / collision_ref(CHECK_M, N64) > 1e-6, \
    "and the product must ALREADY have lost digits at 64 bits, before it fails"
assert collision_naive(TRAP_M, N128) == 0.0, \
    "at 128 bits the product must return exactly zero, or the frame is wrong"
assert collision(TRAP_M, N128) > 0, "and the closed form must not"

BDAY_P = collision_ref(BDAY_M, BDAY_N)
emit("p12.bday.n", BDAY_N)
emit("p12.bday.m", BDAY_M)
emit("p12.bday.p", BDAY_P * 100, digits=1)
emit("p12.bday.closed", collision(BDAY_M, BDAY_N) * 100, digits=1)
# and the number people expect instead: one pair's chance, once per person
emit("p12.bday.naive", BDAY_M / BDAY_N * 100, digits=1)
emit("p12.bday.pairs", math.comb(BDAY_M, 2))
emit("p12.check.m", CHECK_M)
emit("p12.trap.m", sci(float(TRAP_M), 0))
# NOT emitted: the transcript prints this number itself, and a value that a
# listing already carries is a second copy nothing would correct.
NOTES.append(f"1 - prod at 128 bits, m={TRAP_M}: {collision_naive(TRAP_M, N128)!r} "
             f"against {collision(TRAP_M, N128):.3e} -- P02's finding, in a hash")

# The 50% point: m ~ sqrt(2 ln 2) sqrt(N), and the constant is worth printing.
HALF_C = math.sqrt(2 * math.log(2))
emit("p12.half.c", HALF_C, digits=4)
assert abs(collision(round(HALF_C * math.sqrt(N64)), N64) - 0.5) < 1e-6, \
    "the stated 50% point must actually give a half"

M_DEDUP = 10 ** 9                       # a billion documents: a real corpus
P64 = collision(M_DEDUP, N64)
NAIVE64 = M_DEDUP / N64                 # the quantity people reason with
emit("p12.hash.m", sci(float(M_DEDUP), 0))
emit("p12.bits64", BITS64)
emit("p12.hash.n64", sci(float(N64), 2))
emit("p12.hash.p64", P64 * 100, digits=2)
emit("p12.hash.naive64", sci(NAIVE64, 2))
emit("p12.hash.half64", sci(HALF_C * math.sqrt(N64), 2))

# THE RATIO MUST REPRODUCE FROM THE PAGE. Divide the two numbers as the page
# prints them, not as they sit in memory -- the rule F04, F05 and P07 each
# paid for.
_printed_p = float(f"{P64 * 100:.2f}") / 100
_printed_naive = float(sci(NAIVE64, 2))
RATIO64 = _printed_p / _printed_naive
emit("p12.hash.ratio", sci(RATIO64, 2))
assert abs(RATIO64 - P64 / NAIVE64) / RATIO64 < 0.01, \
    "the printed ratio must be the ratio of the printed numbers"

M_BIG = 10 ** 12                        # a trillion, well past any real corpus
P128 = collision(M_BIG, N128)
emit("p12.bits128", BITS128)
emit("p12.hash.m2", sci(float(M_BIG), 0))
emit("p12.hash.p128", sci(P128, 2))
emit("p12.hash.half128", sci(HALF_C * math.sqrt(float(N128)), 2))
assert P128 < 1e-12 < P64, "128 bits must be out of reach where 64 is not"

# Pigeonhole's certainty against the birthday's likelihood, on one hash.
emit("p12.pig.certain64", sci(float(N64) + 1, 2))

# =====================================================================
# 5. Two counts that decide a design
# =====================================================================
VOCAB, LENGTH = 32_000, 20
SPACE = VOCAB ** LENGTH
emit("p12.beam.vocab", VOCAB)
emit("p12.beam.len", LENGTH)
emit("p12.beam.space", sci(float(SPACE), 2))

BEAM_A, BEAM_B = 4, 8
def scored(b: int) -> int:
    """Continuations a beam of width b scores in total: b x V per step."""
    return LENGTH * b * VOCAB


emit("p12.beam.a", BEAM_A)
emit("p12.beam.b", BEAM_B)
emit("p12.beam.scored.a", sci(float(scored(BEAM_A)), 2))
emit("p12.beam.scored.b", sci(float(scored(BEAM_B)), 2))
emit("p12.beam.frac.a", sci(scored(BEAM_A) / float(SPACE), 2))
emit("p12.beam.frac.b", sci(scored(BEAM_B) / float(SPACE), 2))
# The width a further problem asks for: the b that scores one per cent of the
# space, b = 0.01 * V^L / (L*V). Exact in Fractions, because V^L has ninety
# digits and a float cannot hold the numerator.
BEAM_PCT = Fraction(1, 100) * Fraction(SPACE) / Fraction(LENGTH * VOCAB)
emit("p12.beam.pct.width", sci(float(BEAM_PCT), 2))
# And the property that makes the exercise work rather than the figure: the
# width needed is astronomically larger than anything nameable, and it scales
# with the space rather than with the beam.
assert float(BEAM_PCT) > 1e80, float(BEAM_PCT)
assert abs(float(scored(int(1)) * BEAM_PCT / Fraction(SPACE)) - 0.01) < 1e-12

# The invariant, not the figure: doubling the beam doubles the coverage, and
# doubling a number that small is what makes the coverage argument worthless.
assert scored(BEAM_B) == 2 * scored(BEAM_A)
assert scored(BEAM_B) / float(SPACE) < 1e-80, \
    "a doubled beam must still see essentially none of the space"

# --- Shapley: the identity, proved by enumeration over Fractions ---------
# Six features, each covering some of eight signals; the worth of a coalition
# is how many distinct signals it covers. Submodular, with real redundancy --
# features 4 and 5 cover the same two signals, which is what makes the
# attribution interesting rather than additive.
COVER = {0: {0, 1}, 1: {1, 2, 3}, 2: {3, 4}, 3: {5, 6, 7}, 4: {0, 2}, 5: {0, 2}}
NF = len(COVER)


def worth(S) -> int:
    return len(set().union(*(COVER[i] for i in S))) if S else 0


def shapley_by_orderings(i: int):
    """The definition: average marginal contribution over all n! orderings."""
    tot = Fraction(0)
    for order in permutations(range(NF)):
        before = set(order[:order.index(i)])
        tot += worth(before | {i}) - worth(before)
    return tot / math.factorial(NF)


def shapley_by_subsets(i: int):
    """The same number as a weighted sum over the 2^(n-1) subsets."""
    others = [j for j in range(NF) if j != i]
    tot = Fraction(0)
    for r in range(len(others) + 1):
        w = Fraction(math.factorial(r) * math.factorial(NF - r - 1),
                     math.factorial(NF))
        for S in combinations(others, r):
            tot += w * (worth(set(S) | {i}) - worth(set(S)))
    return tot


PHI = [shapley_by_orderings(i) for i in range(NF)]
assert PHI == [shapley_by_subsets(i) for i in range(NF)], \
    "the two forms must be the SAME number, exactly -- that identity is why " \
    "exact Shapley is 2^n rather than n!, and it is the only thing standing " \
    "between a definition nobody could evaluate and one merely nobody can"
assert sum(PHI) == worth(range(NF)) - worth(set()), \
    "the attributions must add up to what the full set is worth (efficiency)"
assert PHI[4] == PHI[5], \
    "two features covering the same signals must be given the same credit"
assert PHI[4] < Fraction(len(COVER[4])), \
    "and each must get LESS than it covers alone, because it is redundant"

emit("p12.shap.n", NF)
emit("p12.shap.orderings", math.factorial(NF))
emit("p12.shap.coalitions", 2 ** NF)
emit("p12.shap.total", worth(range(NF)))
emit("p12.shap.redundant", float(PHI[4]), digits=3)
emit("p12.shap.alone", len(COVER[4]))
emit("p12.shap.top", float(max(PHI)), digits=3)

SHAP_BIG = 20
emit("p12.shap.big", SHAP_BIG)
emit("p12.shap.big.ord", sci(float(math.factorial(SHAP_BIG)), 2))
emit("p12.shap.big.coal", 2 ** SHAP_BIG)
emit("p12.shap.big.ratio", sci(math.factorial(SHAP_BIG) / 2 ** SHAP_BIG, 2))
SHAP_HUGE = 40
_coal = 2 ** SHAP_HUGE
_years = _coal * 1e-3 / (365.25 * 24 * 3600)      # one millisecond apiece
emit("p12.shap.huge", SHAP_HUGE)
emit("p12.shap.huge.coal", sci(float(_coal), 2))
emit("p12.shap.huge.years", round(_years))
assert _years > 20, "the point is that the reduced form is still out of reach"

# =====================================================================
# The transcript: P02's finding, in a hash
# =====================================================================
TRAP_TEXT = f""">>> N = 2 ** 128
>>> m = {TRAP_M}
>>> p = 1.0
>>> for i in range(m):
...     p *= (1 - i / N)
...
>>> 1 - p
{collision_naive(TRAP_M, N128)!r}
>>> -math.expm1(-m * (m - 1) / (2 * N))
{collision(TRAP_M, N128)!r}
"""
assert TRAP_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(line) for line in TRAP_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(TRAP_TEXT.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p12-collision-zero.txt").write_text(TRAP_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p12-collision-zero.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p12_combinatorics.py --- do not edit.",
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

    w = max(len(k) for k in VALUES)
    items = list(VALUES.items())
    for i in range(0, len(items), 3):
        print("  " + "   ".join(f"{k:{w}s} {b:>12s}" for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
