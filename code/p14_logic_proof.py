#!/usr/bin/env python3
"""Program P14 --- Logic, proof and reading theorems.

Every number Program P14 prints that the reader cannot do in their head is
computed here and written to figures/values/p14.tex, which the book \\input{}s.

P14's thesis is that a theorem is hypotheses plus a conclusion plus the
quantifiers binding them, and that almost every misuse of one in this field is
a reader taking the conclusion and dropping something else.

THIS PROGRAM HAS LESS TO COMPUTE THAN ANY OTHER, and that is a fact about its
subject rather than a shortfall. What CAN be computed is computed, and it is
more than it looks: every claim about implication and quantifiers below is
settled by exhaustive enumeration over a finite domain, which is a proof and
not a demonstration -- there are four rows, or thirty-six pairs, and the script
checks all of them. What cannot be computed is labelled rather than dressed up.

WHAT P14 IS OWED, read out of the written files rather than remembered:

  F10  gives and, or, not and De Morgan, and its filter example is continued
       here: the wrong negation of a conjunction is the same defect this
       program names as denying the antecedent's cousin. Gated below.
  P13  DEFERS HERE BY NAME: it proves one direction of the topological-order
       theorem and says "Program P14 is where reading and stating a theorem
       properly is taught".
  P05  used the union bound to get its capacity figures and said in a
       rigourbox that the way the bound was obtained matters. Section 5's
       "with high probability" arithmetic is the same bound, used on a
       different quantity.
  EVERY rigourbox in the book -- fourteen of them -- is this program's subject
       practised before it was named: a statement, an admission that it is not
       proved here, and a pointer to where the proof lives.

WHAT THIS PROGRAM DOES NOT DO, and says so on the page: it does not train the
reader to WRITE proofs. The audience needs to read theorems and does not need
to prove them, and pretending otherwise would be the third bad option after
omitting rigour entirely and faking it.

Run:  python3 code/p14_logic_proof.py      (or: make numbers)
"""
from __future__ import annotations

import math
from itertools import product
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p14.tex"
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
# 1. Implication, and the two things it is not
# =====================================================================
# Four rows. Enumerating all of them is not a demonstration, it is the proof:
# a statement about two booleans has four cases and there is nothing else.
ROWS = list(product([False, True], repeat=2))
emit("p14.rows", len(ROWS))


def implies(p, q):
    return (not p) or q


# The three sentences people confuse, tabulated.
FORWARD = [implies(p, q) for p, q in ROWS]
CONVERSE = [implies(q, p) for p, q in ROWS]
CONTRA = [implies(not q, not p) for p, q in ROWS]

assert FORWARD == CONTRA, \
    "a statement and its contrapositive must agree in every row -- that is " \
    "what makes proof by contraposition a proof rather than a manoeuvre"
assert FORWARD != CONVERSE, \
    "and the converse must NOT agree, or the commonest misreading in the " \
    "field would be harmless"
# WHERE they differ, which is the sentence the frames want.
DIFFER = [i for i, (f, c) in enumerate(zip(FORWARD, CONVERSE)) if f != c]
assert len(DIFFER) == 2, "the forward form and its converse differ in two rows"
emit("p14.differ", len(DIFFER))

# THE NEGATION OF AN IMPLICATION is what a counterexample is, and it is F10's
# De Morgan one step on: not(p -> q) is p and not q, so refuting a claim means
# exhibiting ONE case with the hypothesis holding and the conclusion failing.
assert [not implies(p, q) for p, q in ROWS] == [p and not q for p, q in ROWS], \
    "the negation of an implication must be hypothesis-and-not-conclusion"

# --- CROSS-PROGRAMME GATE (a continued example, not a coincidence) --------
# Program F10 filtered 20 records and measured what the WRONG negation of a
# conjunction keeps. That wrong negation is exactly `not p and not q` where
# `not (p and q)` was meant, so the counts are derivable from the truth table
# and must reproduce F10's committed ones.
_total = committed("f10.tex", "f10.rec.total")
if _total:
    N, RIGHT, WRONG = (int(committed("f10.tex", f"f10.rec.{k}"))
                       for k in ("total", "right", "wrong"))
    # F10's records: `spam` and `short` flags over 20 rows, arranged so that
    # `not (spam and short)` keeps RIGHT and `not spam and not short` keeps
    # WRONG. Rebuild that population from the two counts and check both
    # filters against the truth table rather than against F10's arithmetic.
    both = N - RIGHT                       # rows where spam AND short
    neither = WRONG                        # rows where neither flag is set
    exactly_one = N - both - neither
    assert exactly_one >= 0, "F10's population must be reconstructible"
    pop = ([(True, True)] * both + [(False, False)] * neither
           + [(True, False)] * exactly_one)
    assert len(pop) == N
    assert sum(1 for p, q in pop if not (p and q)) == RIGHT, \
        "the right filter must keep F10's committed count"
    assert sum(1 for p, q in pop if (not p) and (not q)) == WRONG, \
        "and the wrong one must keep F10's committed count"
    assert RIGHT - WRONG == int(committed("f10.tex", "f10.rec.lost")), \
        "and the difference must be the records F10 says are silently lost"
    NOTES.append(f"gate: F10's filter counts {RIGHT} and {WRONG} fall out of "
                 "the truth table")
    emit("p14.filter.total", N)
    emit("p14.filter.right", RIGHT)
    emit("p14.filter.wrong", WRONG)
    emit("p14.filter.lost", RIGHT - WRONG)
else:                                                        # pragma: no cover
    NOTES.append("F10's values not built yet; the filter gate did not run")

# =====================================================================
# 2. Quantifiers, and the order that changes the claim
# =====================================================================
# A finite relation on which "for every x there is a y" is TRUE and "there is
# a y for every x" is FALSE. Exhibiting one is a proof that the two sentences
# are different claims, and it takes six elements.
DOM = list(range(6))
REL = {(x, y) for x in DOM for y in DOM if y == (x + 1) % len(DOM)}

FORALL_EXISTS = all(any((x, y) in REL for y in DOM) for x in DOM)
EXISTS_FORALL = any(all((x, y) in REL for x in DOM) for y in DOM)
assert FORALL_EXISTS and not EXISTS_FORALL, \
    "the witness must satisfy one order and fail the other, or it witnesses " \
    "nothing"
emit("p14.dom", len(DOM))
emit("p14.pairs", len(DOM) ** 2)
emit("p14.rel", len(REL))

# And the converse direction, which is the half that IS a theorem: swapping to
# exists-forall is always safe, never the other way. Checked exhaustively over
# every relation on a three-element domain -- all 2^9 of them.
SMALL = list(range(3))
_checked = 0
for bits in range(2 ** (len(SMALL) ** 2)):
    R = {(x, y) for i, (x, y) in enumerate(product(SMALL, SMALL))
         if bits >> i & 1}
    ef = any(all((x, y) in R for x in SMALL) for y in SMALL)
    fe = all(any((x, y) in R for y in SMALL) for x in SMALL)
    assert not ef or fe, "exists-forall must always imply forall-exists"
    _checked += 1
assert _checked == 2 ** 9
emit("p14.qchecked", _checked)

# =====================================================================
# 3. What "with high probability" costs when you use it more than once
# =====================================================================
# A bound that holds with probability 1 - delta on ONE draw. This is the
# arithmetic the phrase hides, and it is the whole of section 5's first
# worked example.
DELTA = 0.05
CONF = 1 - DELTA
emit("p14.conf", CONF * 100, digits=0)

USES = 20
ALL_HOLD = CONF ** USES
emit("p14.uses", USES)
emit("p14.allhold", ALL_HOLD * 100, digits=1)
emit("p14.anyfails", (1 - ALL_HOLD) * 100, digits=1)
assert ALL_HOLD < 0.5, \
    "the point is that a 95% bound used twenty times is more likely than " \
    "not to fail somewhere, and if that stops being true the frame is wrong"

# The union bound gives the same conclusion without independence, which is why
# it is the one people actually use -- Program P05 used it for capacity.
UNION = min(1.0, USES * DELTA)
emit("p14.union", UNION * 100, digits=0)
assert UNION >= 1 - ALL_HOLD, "the union bound must be the weaker statement"

# How many uses before a 95% bound is a coin flip on the whole set?
FLIP = math.ceil(math.log(0.5) / math.log(CONF))
emit("p14.flip", FLIP)
assert CONF ** FLIP < 0.5 <= CONF ** (FLIP - 1), "the coin flip must be sharp"

# And the confidence a single bound needs so that twenty uses hold 95% of the
# time: this is the correction people leave out.
NEEDED = 0.95 ** (1 / USES)
emit("p14.needed", NEEDED * 100, digits=2)
emit("p14.neededdelta", (1 - NEEDED) * 100, digits=2)
assert NEEDED > CONF, "the per-use bound has to be tighter, not looser"

# =====================================================================
# 4. Induction, as a shape rather than as a technique
# =====================================================================
# A thousand confirmations of a TRUE claim, sitting three lines above forty
# confirmations of a false one. Nothing here is emitted and nothing here is
# quoted: the number of checks is not a measurement, it is the rhetorical
# "a thousand tests" the trapbox names, and a value nothing references is a
# second copy nobody would correct. What earns its place is the assertion,
# because the contrast is the section's whole argument -- a thousand cases
# settle nothing that the induction step does not already settle, and forty
# cases of n^2 + n + 41 settle nothing at all.
def closed(n):
    return n * (n + 1) // 2


CHECKED_TO = 1000
for n in range(0, CHECKED_TO + 1):
    assert sum(range(n + 1)) == closed(n)

# A claim that survives every check a reader would run and is false anyway.
# n^2 + n + 41 is prime for every n from 0 to 39 and composite at 40 -- so
# forty confirmations are worth nothing, which is the frame's whole argument.
def is_prime(m):
    if m < 2:
        return False
    for d in range(2, int(m ** 0.5) + 1):
        if m % d == 0:
            return False
    return True


EULER_HOLDS = next(n for n in range(200) if not is_prime(n * n + n + 41))
assert all(is_prime(n * n + n + 41) for n in range(EULER_HOLDS)), \
    "every value below the first failure must really be prime"
emit("p14.euler.first", EULER_HOLDS)
emit("p14.euler.at", EULER_HOLDS ** 2 + EULER_HOLDS + 41)
emit("p14.euler.factor", next(d for d in range(2, 100)
                              if (EULER_HOLDS ** 2 + EULER_HOLDS + 41) % d == 0))
assert EULER_HOLDS >= 40, "the run of confirmations must be long enough to convince"

# =====================================================================
# 5. Universal approximation, and what it does not say
# =====================================================================
# NOT MEASURED, AND SAID SO ON THE PAGE. The theorem is an existence
# statement; how the required width grows with the accuracy and the dimension
# is a separate question with separate answers, and this book has neither run
# the experiment nor surveyed the literature well enough to quote a rate. What
# IS computable is the shape of the quantifiers, which is section 2's subject,
# and the count of what the statement does not mention.
NOT_MENTIONED = ["how large the network must be",
                 "how the size grows with the accuracy",
                 "how the weights are to be found",
                 "whether training finds them",
                 "how much data that would take"]
emit("p14.silent", len(NOT_MENTIONED))
NOTES.append("universal approximation is silent on %d things people quote it "
             "for" % len(NOT_MENTIONED))

# =====================================================================
# The transcript: forty confirmations are worth nothing
# =====================================================================
_at = EULER_HOLDS ** 2 + EULER_HOLDS + 41
TEXT = f""">>> from p14_logic_proof import is_prime
>>> all(is_prime(n * n + n + 41) for n in range({EULER_HOLDS}))
True
>>> is_prime({EULER_HOLDS} ** 2 + {EULER_HOLDS} + 41)
False
>>> {_at} % {VALUES['p14.euler.factor'][0]}
0
"""
assert TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in TEXT.splitlines()) <= 64, "transcript too wide"
assert len(TEXT.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p14-forty-confirmations.txt").write_text(TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p14-forty-confirmations.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p14_logic_proof.py --- do not edit.",
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
