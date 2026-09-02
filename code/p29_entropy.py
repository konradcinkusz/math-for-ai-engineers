"""P29 --- Entropy and the measure of surprise.

Every number Program P29 prints, and the assertions that keep them honest.

WHAT THE NEIGHBOURS ALREADY SPENT, read one brief item at a time before a line
of this was written -- the discipline that made P27 come in at thirty-nine
frames against sixty.  TWO OF THE BRIEF'S THREE PAYOFFS ARE HANDED HERE BY
NAME, from file headers written by earlier passes:

  P19  section 5 works "why you cannot average perplexities" in full, with the
       measurement, and its own header says what is left:
           what a perplexity MEANS (the effective number of choices) -> P29
       So this program may not re-teach Jensen and may not re-work that
       demonstration.  It owes the READING of the number.
  P25  measures the entropy of an attention row in nats at three head sizes and
       its header says
           entropy as a quantity in its own right -> P29
       So section 5 does not invent an example: it says what P25's own
       committed numbers MEAN, and gates against all six of them.
  F03  owns computing a perplexity from a mean loss by exponentiating, the
       bits/nats conversion, and the base warning.  It also owns the SEVEN-WAY
       uniform case -- p = 1/7, 1.9459 nats, 2.8074 bits -- which is exactly
       the anchor section 4 needs, already committed.  F03 even names P29 and
       P30 as sitting next to each other because entropy is quoted in bits and
       cross-entropy in nats.
  F04  owns perplexity as the exponential of the MEAN loss and the four-example
       cross-entropy, with both numbers.
  P26  owns cross-entropy as a negative log-likelihood, and already warns that
       "cross-entropy measures the distance between two distributions" is
       wrong, naming the excess as the thing that has a name.
  P24  owns the random variable and the expectation; F05 owns the four-token
       distribution at three temperatures and committed all twelve.
  F13  owns the density, and with it that a continuous quantity has no
       entropy in this sense without a reference measure -- named, not spent.

WHAT IS GENUINELY LEFT, and it is the whole of this program:
  1. surprise is -log p, and WHY a logarithm: independent surprises must add
     while their probabilities multiply, which is F03's product law read in a
     new place;
  2. entropy is average surprise;
  3. THE OPERATIONAL MEANING, which nothing in the book has: entropy is the
     shortest average code length, and that is why the unit is a bit.  F03 did
     the unit CONVERSION; nobody has said what a bit IS.  Proved here by
     exhaustive enumeration over every Kraft-admissible length assignment,
     which is a proof for that alphabet rather than evidence about it --
     Program P14's distinction doing a second job;
  4. the exponential of the entropy is the EFFECTIVE NUMBER of equally likely
     choices, which is what a perplexity is and what P19 handed over.

NOT SPENT HERE, deliberately:
  P30  owns cross-entropy as a cost, KL, and the asymmetry.  This program
       computes entropy of ONE distribution and never a divergence between two.
  P31  owns mutual information.

Run:  python3 code/p29_entropy.py
"""

from __future__ import annotations

import itertools
import math
import re
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p29.tex"
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

    Programs F04, F05, P07, P12, P23, P27 and P28 each paid for this.  Note
    P28's addition: this checks an arithmetic RESULT against printed operands
    and has nothing to say about an inequality, which is how a true claim
    about a bound got onto a page it did not reproduce from."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


def bound(x: float, ceiling: float) -> float:
    """Commit a residual as a DECISION rather than as an observation.

    Program P06 had two rejected by CI for being machine properties, and
    Program P20 found that returning the tightest power of ten is itself
    machine-dependent when the residual can be zero.  So the ceiling is an
    argument and this only checks it."""
    assert x <= ceiling, (x, ceiling)
    return ceiling


# ======================================================================
# 1.  Surprise, and why it is a logarithm.
#
# The requirement is not aesthetic.  Two independent events have a joint
# probability that MULTIPLIES, and any sensible measure of how surprising the
# pair is has to ADD -- learning two independent things surprises you by the
# sum of what each does on its own.  Program F03 owns the function that turns
# a product into a sum, so the logarithm is forced rather than chosen.
# ======================================================================

def surprise_nats(p: Fraction) -> float:
    return -math.log(float(p))


# Additivity, checked exactly rather than to a tolerance where it can be: the
# claim is an IDENTITY, so it is asserted on the logarithms' arguments.
PAIRS = [(Fraction(1, 2), Fraction(1, 3)), (Fraction(1, 4), Fraction(2, 5)),
         (Fraction(3, 8), Fraction(5, 7)), (Fraction(1, 10), Fraction(9, 10))]
ADD_CEIL = 1e-12
_worst_add = 0.0
for pa, pb in PAIRS:
    joint = pa * pb
    _worst_add = max(_worst_add,
                     abs(surprise_nats(joint)
                         - (surprise_nats(pa) + surprise_nats(pb))))
emit("p29.add.pairs", len(PAIRS))
emit("p29.add.bound", bound(_worst_add, ADD_CEIL))

# And the two ends, which are what make the function the right shape: a
# certainty surprises you by nothing, exactly, and the surprise of an
# impossibility is unbounded.  Both are stated as the identities they are.
# Not emitted: the frame writes "exactly nothing" in words, and a zero behind
# a \val{} would be a figure standing in for a sentence.
assert surprise_nats(Fraction(1)) == 0.0

# A worked pair the reader can check on the page: one token in a thousand.
RARE = Fraction(1, 1000)
emit("p29.rare.den", RARE.denominator)
emit("p29.rare.nats", surprise_nats(RARE), 2)
emit("p29.rare.bits",
     reproduces(surprise_nats(RARE) / math.log(2), 2,
                (surprise_nats(RARE), 2), (math.log(2), 4),
                op=lambda a, b: a / b), 2)
# The bits figure is exactly ten if the denominator is 1024, and it is not:
# 1000 is not a power of two, so the page must not round it to ten.
assert 9.9 < surprise_nats(RARE) / math.log(2) < 10.0


# ======================================================================
# 2.  Entropy is average surprise, and it is Program P24's expectation.
# ======================================================================

def entropy_nats(ps) -> float:
    return sum(float(p) * surprise_nats(p) for p in ps if p > 0)


def entropy_bits(ps) -> float:
    return entropy_nats(ps) / math.log(2)


# THE GATE ON F03.  It committed the seven-way uniform case -- 1/7, 1.9459
# nats, 2.8074 bits -- which is precisely the anchor section 4 needs, so this
# program must reproduce it rather than resemble it.
SEVEN = [Fraction(1, 7)] * 7
_f03_nats = float(committed("f03.tex", "f03.ppl.seven.nats") or 1.9459)
_f03_bits = float(committed("f03.tex", "f03.ppl.seven.bits") or 2.8074)
assert abs(entropy_nats(SEVEN) - _f03_nats) < 5e-5, entropy_nats(SEVEN)
assert abs(entropy_bits(SEVEN) - _f03_bits) < 5e-5, entropy_bits(SEVEN)
emit("p29.seven.n", 7)
emit("p29.seven.nats", entropy_nats(SEVEN), 4)
emit("p29.seven.bits", entropy_bits(SEVEN), 4)
NOTES.append(f"F03's seven-way uniform case reproduces: "
             f"{entropy_nats(SEVEN):.4f} nats, {entropy_bits(SEVEN):.4f} bits.")

# A fair coin is one bit, exactly, and that is the definition of the unit.
assert entropy_bits([Fraction(1, 2)] * 2) == 1.0
emit("p29.coin.bits", 1)

# A biased coin, so the page can say entropy falls away from a half in both
# directions -- and it is P25's p(1-p) shape in a different function, which
# the frame names rather than re-derives.
BIAS = Fraction(9, 10)
emit("p29.bias.p", float(BIAS), 1)
emit("p29.bias.bits", entropy_bits([BIAS, 1 - BIAS]), 3)
assert entropy_bits([BIAS, 1 - BIAS]) < 0.5

# Uniform is the maximum, and it is not asserted -- it is SEARCHED FOR over a
# grid and then proved at the one point sampling can never reach, which is
# Program P10's finding about the flat direction, applied here.
GRID = 60
_worst = 0.0
for i in range(1, GRID):
    for j in range(1, GRID - i):
        k = GRID - i - j
        ps = [Fraction(i, GRID), Fraction(j, GRID), Fraction(k, GRID)]
        _worst = max(_worst, entropy_nats(ps))
_uniform3 = entropy_nats([Fraction(1, 3)] * 3)
# Attained rather than approached: 60 is divisible by three, so (20, 20, 20)
# is IN the sweep and the sampled maximum is the true one exactly.  A grid
# that missed it would report a maximum that is not one, which is Program
# P10's flat-direction finding from the other side.
assert _worst == _uniform3, (_worst, _uniform3)
emit("p29.max.grid", GRID)
emit("p29.max.tested", sum(1 for i in range(1, GRID)
                           for j in range(1, GRID - i)))
emit("p29.max.nats", _uniform3, 4)
# The grid CONTAINS the uniform point only because 60 is divisible by three,
# which is why the maximum is attained rather than approached -- said on the
# page, because a grid that missed it would report a maximum that is not one.
assert GRID % 3 == 0


# ======================================================================
# 3.  Why the unit is a BIT: entropy is the shortest average code length.
#
# This is the operational content and nothing in the book has it.  Program F03
# owns the unit CONVERSION; nobody has said what a bit IS.
#
# Proved by EXHAUSTIVE ENUMERATION over every Kraft-admissible assignment of
# code lengths, which for a finite alphabet with a length cap is a proof and
# not evidence -- Program P14's distinction doing a second job, and the same
# move Program P13 made for topological orders.
# ======================================================================

def kraft_ok(lengths) -> bool:
    """A prefix code with these lengths exists iff sum 2^-l <= 1 (Kraft)."""
    return sum(Fraction(1, 2 ** l) for l in lengths) <= 1


def best_code(ps, cap: int):
    """The smallest expected length over EVERY admissible length assignment."""
    best, arg = None, None
    for lengths in itertools.product(range(1, cap + 1), repeat=len(ps)):
        if not kraft_ok(lengths):
            continue
        exp = sum(p * l for p, l in zip(ps, lengths))
        if best is None or exp < best:
            best, arg = exp, lengths
    return best, arg


# (a) A DYADIC distribution, where the bound is attained exactly and the
#     arithmetic is rational throughout -- no tolerance anywhere.
DYADIC = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)]
_h_dyadic = sum(p * Fraction(int(math.log2(1 / float(p)))) for p in DYADIC)
CAP = 7
_best, _arg = best_code(DYADIC, cap=CAP)
assert _best == _h_dyadic, (_best, _h_dyadic)
assert sorted(_arg) == [1, 2, 3, 3], _arg
# Not emitted: the frames say "four symbols" in words, which is this book's
# stated exception for arithmetic the reader does in their head.
emit("p29.code.best", float(_best), 2)
emit("p29.code.h", float(_h_dyadic), 2)
emit("p29.code.assignments",
     sum(1 for l in itertools.product(range(1, CAP + 1), repeat=len(DYADIC))
         if kraft_ok(l)))
NOTES.append(f"dyadic alphabet: the best of every admissible code is "
             f"{float(_best):.2f} bits and the entropy is "
             f"{float(_h_dyadic):.2f}, equal exactly over fractions.")

# (b) A NON-dyadic one, where the bound cannot be attained and the gap is the
#     rounding.  This is the honest half: H <= L < H + 1, and the page states
#     the gap as a MEASUREMENT rather than quoting the theorem's bound.
NONDY = [Fraction(2, 5), Fraction(1, 5), Fraction(1, 5), Fraction(1, 5)]
_h_nondy = entropy_bits(NONDY)
_bn, _an = best_code(NONDY, cap=CAP)
assert float(_bn) > _h_nondy, (_bn, _h_nondy)
assert float(_bn) < _h_nondy + 1
emit("p29.nondy.h", _h_nondy, 3)
emit("p29.nondy.best", float(_bn), 3)
emit("p29.nondy.gap",
     reproduces(float(_bn) - _h_nondy, 3,
                (float(_bn), 3), (_h_nondy, 3), op=lambda a, b: a - b),
     3)

# (c) THE CLAIM THE SECTION EXISTS FOR, and it is the exhaustive half: no code
#     beats the entropy, on either alphabet, over every admissible assignment.
for ps in (DYADIC, NONDY):
    b, _ = best_code(ps, cap=CAP)
    assert float(b) >= entropy_bits(ps) - 1e-12, (b, entropy_bits(ps))
emit("p29.code.cap", CAP)


# ======================================================================
# 4.  THE PAYOFF Program P19 handed over by name: the exponential of the
#     entropy is the effective number of equally likely choices.
# ======================================================================

# The anchor is a definition rather than a demonstration: a uniform choice
# among n has entropy ln n, so its exponential is n, EXACTLY.  Checked over a
# range so the page can say "always" rather than "here".
for n in range(2, 40):
    assert abs(math.exp(entropy_nats([Fraction(1, n)] * n)) - n) < 1e-9, n
emit("p29.eff.checked", 38)

# THE GATE ON F03 AND F02, run in both directions: F02's per-token loss is
# committed at 2.4 nats and F03 exponentiated it to a perplexity of 11.02.
# This program says what 11.02 IS, so it must be the same number.
_loss = float(committed("f02.tex", "f02.loss.nats") or 2.4)
_ppl = float(committed("f03.tex", "f03.ppl") or 11.02)
assert abs(math.exp(_loss) - _ppl) < 5e-3, (math.exp(_loss), _ppl)
emit("p29.f02.loss", _loss, 1)
emit("p29.f03.ppl", _ppl, 2)
NOTES.append(f"F03's perplexity reproduces from F02's loss: "
             f"exp({_loss}) = {math.exp(_loss):.2f} against {_ppl}.")

# And the reading that makes it a statement about a model rather than a
# leaderboard number: at every position the model is as uncertain as somebody
# choosing uniformly among this many tokens, out of a vocabulary of this many.
VOCAB = 50000
emit("p29.vocab", VOCAB)
emit("p29.ppl.frac",
     reproduces(100.0 * _ppl / VOCAB, 4, (_ppl, 2), (float(VOCAB), 0),
                op=lambda a, b: 100.0 * a / b), 4)
assert _ppl < VOCAB / 1000

# THE GATE ON P25, and this is the section's best sentence rather than a
# formality.  P25 measured an attention row's entropy in nats at three head
# sizes and could only say "nothing moves".  Read as a count it says how many
# keys the head is actually looking at, out of the eight it has.
_keys = int(committed("p25.tex", "p25.e9.keys") or 8)
_maxent = float(committed("p25.tex", "p25.e9.maxent") or 2.079)
assert abs(math.log(_keys) - _maxent) < 5e-4, (math.log(_keys), _maxent)
emit("p29.att.keys", _keys)
emit("p29.att.maxent", _maxent, 3)
# All four of P25's rows are ASSERTED; only the three the frames quote are
# emitted.  Program F11's finding: a value nothing references is a second copy
# nobody would correct.
for tag, key in (("raw", "p25.e9.raw.ent.512"), ("scaled", "p25.e9.scaled.ent.512"),
                 ("raw8", "p25.e9.raw.ent.8"), ("scaled8", "p25.e9.scaled.ent.8")):
    ent = float(committed("p25.tex", key) or 0.0)
    assert ent > 0, key
    if tag == "scaled8":
        continue
    emit(f"p29.att.{tag}.ent", ent, 3)
    emit(f"p29.att.{tag}.eff", math.exp(ent), 2)
# The claim the frames make, asserted rather than eyeballed: without the
# division the head has collapsed onto barely more than one key, and with it
# it is spread over most of them.
assert math.exp(float(committed("p25.tex", "p25.e9.raw.ent.512"))) < 1.2
assert math.exp(float(committed("p25.tex", "p25.e9.scaled.ent.512"))) > 5.0
NOTES.append("P25's attention entropies read as effective key counts: "
             f"{math.exp(float(committed('p25.tex', 'p25.e9.raw.ent.512'))):.2f} "
             f"unscaled against "
             f"{math.exp(float(committed('p25.tex', 'p25.e9.scaled.ent.512'))):.2f} "
             f"scaled, out of {_keys}.")


# ======================================================================
# 5.  Entropy as a runtime signal, on Program F05's own committed
#     distribution rather than an invented one.
# ======================================================================

_f05 = {}
for t in ("05", "10", "20"):
    row = [committed("f05.tex", f"f05.sm.t{t}.p{i}") for i in range(1, 5)]
    if all(row):
        _f05[t] = [float(x) for x in row]

if _f05:
    for t, ps in sorted(_f05.items()):
        assert abs(sum(ps) - 1.0) < 5e-4, (t, sum(ps))
        h = -sum(p * math.log(p) for p in ps if p > 0)
        emit(f"p29.tok.t{t}.ent", h, 3)
        emit(f"p29.tok.t{t}.eff", math.exp(h), 2)
    # The ORDERING is the claim, not the three figures: raising the
    # temperature raises the entropy, at every step, which is Program F05's
    # own result read through a different function.
    effs = [math.exp(-sum(p * math.log(p) for p in ps if p > 0))
            for _, ps in sorted(_f05.items())]
    assert effs == sorted(effs), effs
    emit("p29.tok.n", 4)
    NOTES.append("F05's four-token distribution reads as effective choices "
                 + ", ".join(f"{e:.2f}" for e in effs) + " at rising T.")

# THE TRAP, and it is the reason the section is not a recommendation.  Entropy
# is a property of the distribution the model REPORTS, not of whether the
# model is right.  A confidently wrong model has LOW entropy, so a low reading
# is not evidence of correctness -- it is evidence of confidence, which is
# exactly Program P28 section 6's defect measured from the other side.
CONFIDENT_WRONG = [Fraction(97, 100), Fraction(1, 100),
                   Fraction(1, 100), Fraction(1, 100)]
HONEST_SPREAD = [Fraction(1, 4)] * 4
emit("p29.wrong.ent", entropy_nats(CONFIDENT_WRONG), 3)
emit("p29.spread.ent", entropy_nats(HONEST_SPREAD), 3)
# The two effective counts are NOT emitted: the transcript below prints both,
# and it prints 4.0 where a \val{} would print 4.00 -- one number on the page
# in two precisions, which is Program F08's defect.  Program P12 removed a
# value for exactly this reason: a figure a listing already carries is a
# second copy nothing would correct.  The frames point at the listing.
assert math.exp(entropy_nats(HONEST_SPREAD)) == 4.0
assert entropy_nats(CONFIDENT_WRONG) < entropy_nats(HONEST_SPREAD)


# ======================================================================
# 6.  The tokeniser bound: what a compression-style claim may assert.
# ======================================================================

# Bits per token times tokens per character is bits per character, and a
# compression claim is about the second.  The point of the section is that a
# bits-per-token figure alone is a ratio quoted without one of its quantities,
# which is this book's recurring complaint.
BPT = _loss / math.log(2)                 # F02's loss, in bits per token
# NOT EMITTED.  Program F03 already committed exactly this conversion of
# exactly this loss as f03.nats.to.bits, so a p29 copy would be one number on
# the page under two names -- Program F08's defect, two hundred pages apart.
# Gated instead, and the frames quote F03's value directly.
_f03_bpt = float(committed("f03.tex", "f03.nats.to.bits") or 3.4625)
assert abs(BPT - _f03_bpt) < 5e-5, (BPT, _f03_bpt)
BPT = _f03_bpt
TPC_A, TPC_B = 0.25, 0.32                 # two plausible tokenisers
emit("p29.tpc.a", TPC_A, 2)
emit("p29.tpc.b", TPC_B, 2)
emit("p29.bpc.a",
     reproduces(BPT * TPC_A, 3, (BPT, 4), (TPC_A, 2), op=lambda a, b: a * b), 3)
emit("p29.bpc.b",
     reproduces(BPT * TPC_B, 3, (BPT, 4), (TPC_B, 2), op=lambda a, b: a * b), 3)
emit("p29.bpc.ratio",
     reproduces(TPC_B / TPC_A, 2, (TPC_B, 2), (TPC_A, 2), op=lambda a, b: a / b), 2)
# The whole claim of the section, asserted: the SAME model on the SAME text
# reports two different bits-per-character figures under two tokenisers, and
# the ratio is the tokenisers' ratio and nothing about the model.
assert abs((BPT * TPC_B) / (BPT * TPC_A) - TPC_B / TPC_A) < 1e-12
# AND the route the reader will actually take, which the reproduces() calls
# above do NOT cover: they each check one value against ITS OWN operands, and
# a reader dividing the two bits-per-character figures printed side by side is
# doing a third sum nothing had checked.  That is Program P28's finding -- a
# helper is only as wide as the comparison it was pointed at -- so the page's
# own row is divided here, as the page prints it.
_shown = round(float(f"{BPT * TPC_B:.3f}") / float(f"{BPT * TPC_A:.3f}"), 2)
assert f"{_shown:.2f}" == f"{TPC_B / TPC_A:.2f}", (_shown, TPC_B / TPC_A)


# ======================================================================
# The transcript.  Every transformation is INSIDE the listing, because
# Programs P19, P24, P27 and P28 each shipped a draft where it was not.
# ======================================================================
TRANSCRIPT = OUT.parent.parent / "transcripts"
_lines = [
    ">>> from math import exp, log",
    ">>> def eff(ps):    # effective number of equally likely choices",
    "...     h = -sum(p * log(p) for p in ps if p)",
    "...     return round(exp(h), 2)",
    ">>> eff([0.25] * 4), eff([0.97, 0.01, 0.01, 0.01])",
]
_a = round(math.exp(entropy_nats(HONEST_SPREAD)), 2)
_b = round(math.exp(entropy_nats(CONFIDENT_WRONG)), 2)
_lines.append(repr((_a, _b)))
assert max(len(line) for line in _lines) <= 64, max(_lines, key=len)
(TRANSCRIPT / "p29-effective-choices.txt").write_text(
    "\n".join(_lines) + "\n", encoding="utf8")


# ======================================================================
OUT.write_text(
    "% Generated by code/p29_entropy.py --- do not edit.\n"
    "% Regenerate with `make numbers`; `make verify` fails if this file and\n"
    "% the script disagree, which is what stops a number in the book drifting\n"
    "% away from the computation that justifies it.\n\n"
    + "".join(f"\\mfaval{{{k}}}{{{v}}}\n" if numeric
             else f"\\mfavaltext{{{k}}}{{{v}}}\n"
             for k, (v, numeric) in VALUES.items()),
    encoding="utf8")
print(f"P29: {len(VALUES)} values -> {OUT}")
for note in NOTES:
    print(f"  * {note}")
