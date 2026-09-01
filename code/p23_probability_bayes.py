#!/usr/bin/env python3
"""Program P23 --- Probability and Bayes' theorem.

Every number Program P23 prints that the reader cannot do in their head is
computed here and written to figures/values/p23.tex, which the book \\input{}s.

P23's thesis is that PROBABILITY IS A MEASURE ON A SAMPLE SPACE OBEYING THREE
RULES, that conditioning is restricting the space, and that Bayes' theorem is
one line of algebra from the definition. It is derived here and never asserted.

WHAT P23 IS OWED, read out of the files rather than remembered:

  F10  hands this program over BY NAME -- "probability itself: the sample
       space, conditioning, Bayes -> P23" -- and its closing frame says what
       the reader already has: "the numerator and the denominator, and the
       knowledge that CHOOSING THE DENOMINATOR WAS A DECISION". That is the
       on-ramp, because CONDITIONING IS EXACTLY THAT DECISION MADE
       DELIBERATELY: restricting the sample space is changing the denominator.
       F10 also owns the counting rules, the mask, and and/or/not.
  F13  owns the density, the fact that a density's HEIGHT is not a probability
       while its AREA is, and the shape of a weighted average. So nothing here
       has to build the continuous case.
  P12  owns the counting formally, so a naive probability's numerator and
       denominator are objects the reader can already compute.

WHAT P23 LEAVES ALONE, checked against tools/programs.json:
    random variables, expectation and variance                -> P24
    sums of random variables, the CLT, concentration          -> P25
    estimation and maximum likelihood                         -> P26
    what a p-value is                                         -> P27
    KL and cross-entropy                                      -> P30

EVERYTHING HERE IS EXACT, over Fractions, and that is a deliberate choice
rather than a flourish: every claim this program makes is about equality of
two expressions, and a tolerance would weaken each one into a resemblance.

THE HEADLINE IS THE BASE RATE, and the brief calls it "the calculation an
engineer must be able to do in a meeting". A classifier at 99 per cent on a
fault occurring once in a thousand requests has a positive predictive value of
11/122 -- NINE PER CENT of its alarms are real. The sweep either side of it is
the real lesson: the answer is 91.7 per cent at one in ten, EXACTLY a half at
one in a hundred, 9.0 at one in a thousand and 1.0 at one in ten thousand. The
classifier did not change.

Run:  python3 code/p23_probability_bayes.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p23.tex"
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


# ---------------------------------------------------------------------------
# 1. THE THREE RULES, on a space small enough to write out.
#
# A probability is a function from subsets of a sample space to numbers with
# three properties: never negative, one over the whole space, and additive on
# disjoint pieces. Everything in this program follows from those and from
# nothing else, so they are checked on an explicit space rather than recited.
# ---------------------------------------------------------------------------
# A request is (fault, alarm): the space of the classifier example, weighted.
PREV = Fraction(1, 1000)                # a fault once in a thousand requests
SENS = Fraction(99, 100)                # P(alarm | fault)
SPEC = Fraction(99, 100)                # P(no alarm | no fault)

SPACE = {
    ("fault", "alarm"):     PREV * SENS,
    ("fault", "quiet"):     PREV * (1 - SENS),
    ("clean", "alarm"):     (1 - PREV) * (1 - SPEC),
    ("clean", "quiet"):     (1 - PREV) * SPEC,
}


def P(pred) -> Fraction:
    return sum(v for k, v in SPACE.items() if pred(k))


for _v in SPACE.values():
    assert _v >= 0, _v                                       # rule 1
assert sum(SPACE.values()) == 1, sum(SPACE.values())          # rule 2
# rule 3, on every disjoint pair of the four outcomes
keys = list(SPACE)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        a, b = keys[i], keys[j]
        assert P(lambda k: k in (a, b)) == SPACE[a] + SPACE[b]

emit("p23.space.outcomes", len(SPACE))
emit("p23.prev.num", 1)
emit("p23.prev.den", 1000)
emit("p23.sens.pct", 99)
NOTES.append(f"the three rules hold on the {len(SPACE)}-outcome space, checked "
             "over fractions rather than recited")

# And the rule people forget, which is the one that makes the rest work:
# additivity needs the pieces DISJOINT. Two overlapping events do not add --
# which is Program F10's two-set union rule arriving as a probability.
fault = lambda k: k[0] == "fault"
alarm = lambda k: k[1] == "alarm"
assert P(lambda k: fault(k) or alarm(k)) != P(fault) + P(alarm)
assert (P(lambda k: fault(k) or alarm(k))
        == P(fault) + P(alarm) - P(lambda k: fault(k) and alarm(k)))
NOTES.append("adding two overlapping events double-counts the overlap, which "
             "is Program F10's union rule arriving as a probability")


# ---------------------------------------------------------------------------
# 2. CONDITIONING IS CHANGING THE DENOMINATOR.
#
# Program F10 ends by saying the reader now owns the numerator, the denominator
# and the knowledge that CHOOSING the denominator was a decision. Conditioning
# is that decision made deliberately: P(A|B) is A's share of B rather than of
# everything, which is the definition and not a consequence of it.
# ---------------------------------------------------------------------------
def cond(a, b) -> Fraction:
    """P(a | b): the measure of a inside b, divided by the measure of b."""
    pb = P(b)
    assert pb > 0, "conditioning on an impossible event"
    return P(lambda k: a(k) and b(k)) / pb


P_ALARM = P(alarm)
PPV = cond(fault, alarm)                 # P(fault | alarm) -- the headline
NPV = cond(lambda k: not fault(k), lambda k: not alarm(k))

# The definition, checked as the identity it is: the conditional times the
# condition is the joint, which is the whole of what conditioning means and is
# the line Bayes' theorem is read out of.
assert cond(fault, alarm) * P(alarm) == P(lambda k: fault(k) and alarm(k))
assert cond(alarm, fault) * P(fault) == P(lambda k: fault(k) and alarm(k))

emit("p23.alarm.num", P_ALARM.numerator)
emit("p23.alarm.den", P_ALARM.denominator)
emit("p23.alarm.pct", float(100 * P_ALARM), 1)
emit("p23.ppv.num", PPV.numerator)
emit("p23.ppv.den", PPV.denominator)
emit("p23.ppv.pct", float(100 * PPV), 1)
emit("p23.false.pct", float(100 * (1 - PPV)), 1)
NOTES.append(f"P(fault | alarm) is exactly {PPV} = {float(PPV):.4f}, so "
             f"{float(100*(1-PPV)):.1f} per cent of the alarms are false -- "
             "over fractions, with no rounding anywhere in it")


# ---------------------------------------------------------------------------
# 3. BAYES, DERIVED. The brief says "derived, never asserted".
#
# The joint can be written two ways, so setting them equal and dividing is the
# theorem. Both routes are computed and asserted equal, which is the derivation
# executed rather than a check on a formula somebody else wrote.
# ---------------------------------------------------------------------------
left = cond(fault, alarm) * P(alarm)
right = cond(alarm, fault) * P(fault)
assert left == right, (left, right)
bayes = cond(alarm, fault) * P(fault) / P(alarm)
assert bayes == PPV, (bayes, PPV)

# And the denominator written the long way, which is where the base rate hides:
#     P(alarm) = P(alarm|fault)P(fault) + P(alarm|clean)P(clean)
clean = lambda k: k[0] == "clean"
total = cond(alarm, fault) * P(fault) + cond(alarm, clean) * P(clean)
assert total == P(alarm), (total, P(alarm))
_real, _false = cond(alarm, fault) * P(fault), cond(alarm, clean) * P(clean)
assert _real.denominator == _false.denominator, (_real, _false)
emit("p23.alarm.real", _real.numerator)
emit("p23.alarm.false", _false.numerator)
emit("p23.alarm.den.long", _real.denominator)
emit("p23.alarm.ratio", _false.numerator / _real.numerator, 1)
NOTES.append("the alarms decompose into 99/100000 real and 999/100000 false, "
             "which is the whole of why the answer is what it is: there are "
             "far more clean requests to be wrong about")


# ---------------------------------------------------------------------------
# 4. THE SWEEP, which is the lesson rather than the single figure.
#
# The classifier does not change. Only the base rate does.
# ---------------------------------------------------------------------------
def ppv_at(prev: Fraction, sens=SENS, spec=SPEC) -> Fraction:
    tp = prev * sens
    fp = (1 - prev) * (1 - spec)
    return tp / (tp + fp)


RATES = [Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10000)]
sweep = [(r, ppv_at(r)) for r in RATES]
# The landmark worth having: at a prevalence equal to the error rate the
# answer is EXACTLY a half, which is checkable and is easy to carry.
assert ppv_at(Fraction(1, 100)) == Fraction(1, 2)
for (_, a), (_, b) in zip(sweep, sweep[1:]):
    assert a > b
emit("p23.sweep.n", len(RATES))
emit("p23.ppv.10", float(sweep[0][1]), 3)
emit("p23.ppv.100", float(sweep[1][1]), 1)
emit("p23.ppv.1000", float(sweep[2][1]), 3)
emit("p23.ppv.10000", float(sweep[3][1]), 4)
NOTES.append("the same classifier is right about 91.7 per cent of its alarms "
             "at one fault in ten and 1.0 per cent at one in ten thousand; "
             "EXACTLY half at one in a hundred, where the base rate meets the "
             "error rate")

# The accuracy paradox, which is the same arithmetic read from the other end.
ACC = P(lambda k: (fault(k) and alarm(k)) or (clean(k) and not alarm(k)))
NEVER = P(clean)                       # a classifier that never raises an alarm
assert NEVER > ACC, (NEVER, ACC)
emit("p23.acc.pct", float(100 * ACC), 1)
emit("p23.never.pct", float(100 * NEVER), 1)
NOTES.append(f"the classifier is {float(100*ACC):.1f} per cent accurate and a "
             f"model that never raises an alarm is {float(100*NEVER):.1f} per "
             "cent accurate while catching nobody")


# ---------------------------------------------------------------------------
# 5. INDEPENDENCE IS NOT CONDITIONAL INDEPENDENCE, and the example is exact.
#
# Two fair coins, and a third event that is their exclusive or. A and B are
# independent. Given C they are PERFECTLY DEPENDENT -- knowing one settles the
# other -- so the joint conditional is zero where the product of conditionals
# is a quarter. Nothing is approximate in that.
# ---------------------------------------------------------------------------
COINS = {(a, b): Fraction(1, 4) for a in (0, 1) for b in (0, 1)}


def Q(pred) -> Fraction:
    return sum(v for k, v in COINS.items() if pred(k))


A = lambda k: k[0] == 1
B = lambda k: k[1] == 1
C = lambda k: (k[0] ^ k[1]) == 1                     # exactly one of the two

assert Q(lambda k: A(k) and B(k)) == Q(A) * Q(B)      # independent
pc = Q(C)
a_c = Q(lambda k: A(k) and C(k)) / pc
b_c = Q(lambda k: B(k) and C(k)) / pc
ab_c = Q(lambda k: A(k) and B(k) and C(k)) / pc
assert ab_c != a_c * b_c, (ab_c, a_c, b_c)            # and NOT, given C
assert ab_c == 0                                      # in fact impossible

emit("p23.ind.pa.den", Q(A).denominator)
emit("p23.ind.pab.den", Q(lambda k: A(k) and B(k)).denominator)
emit("p23.ind.pab.c", int(ab_c))
emit("p23.ind.product.den", (a_c * b_c).denominator)
NOTES.append("two independent coins become perfectly dependent given their "
             "exclusive or: the joint conditional is 0 where the product of "
             "the conditionals is 1/4, so independence survives nothing")

# And the other direction, which is what makes the pair worth teaching: two
# events can be dependent and become independent once you condition on the
# common cause. Same space, C as the cause and A, B as two noisy readings.
CAUSE = {}
for c in (0, 1):
    for x in (0, 1):
        for y in (0, 1):
            px = Fraction(3, 4) if x == c else Fraction(1, 4)
            py = Fraction(3, 4) if y == c else Fraction(1, 4)
            CAUSE[(c, x, y)] = Fraction(1, 2) * px * py


def R(pred) -> Fraction:
    return sum(v for k, v in CAUSE.items() if pred(k))


X = lambda k: k[1] == 1
Y = lambda k: k[2] == 1
Z = lambda k: k[0] == 1
assert R(lambda k: X(k) and Y(k)) != R(X) * R(Y)      # dependent
pz = R(Z)
assert (R(lambda k: X(k) and Y(k) and Z(k)) / pz
        == (R(lambda k: X(k) and Z(k)) / pz) * (R(lambda k: Y(k) and Z(k)) / pz))
_pxy, _prod = R(lambda k: X(k) and Y(k)), R(X) * R(Y)
emit("p23.cause.pxy.num", _pxy.numerator)
emit("p23.cause.pxy.den", _pxy.denominator)
emit("p23.cause.prod.num", _prod.numerator)
emit("p23.cause.prod.den", _prod.denominator)
NOTES.append("and two dependent readings become conditionally independent "
             "given the cause they share, which is the naive Bayes assumption "
             "stated as the thing it assumes")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    lines = [
        ">>> from p23_probability_bayes import ppv_at",
        ">>> from fractions import Fraction as F",
        ">>> [ppv_at(F(1, d)) for d in (10, 100, 1000)]",
        f"{[ppv_at(Fraction(1, d)) for d in (10, 100, 1000)]}",
        ">>> float(ppv_at(F(1, 1000)))",
        f"{float(ppv_at(Fraction(1, 1000)))}",
    ]
    for line in lines:
        assert len(line) <= 64, (len(line), line)
    (TRANSCRIPTS / "p23-base-rate.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    out = [
        "% Generated by code/p23_probability_bayes.py --- do not edit.",
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
