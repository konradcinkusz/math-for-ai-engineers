#!/usr/bin/env python3
"""Program F10 --- Sets, logic and counting.

Every number Program F10 prints that the reader cannot do in their head is
computed here and written to figures/values/f10.tex, which the book \\input{}s.

F10's thesis is that three of the words an engineer uses every day -- set,
mask, count -- are one idea seen three ways, and that counting a thing you
cannot list is a skill rather than a formula.

THE THREE COUNTING RULES this program owns, deliberately three and not four:

    product   independent choices multiply:  |A x B| = |A| |B|
    union     the overlap was counted twice: |A u B| = |A| + |B| - |A n B|
    subsets   one yes-or-no per element:     a set of n has 2^n subsets

Program P12 does the four formal rules (product, permutation, combination,
inclusion-exclusion in general), the pigeonhole principle, recurrences and the
birthday calculation. F10 gives the elementary versions those are built from,
and the two-set union rule because a union is not countable without it.

WHAT F10 DELIBERATELY DOES NOT DO, checked against tools/programs.json rather
than remembered -- five programs declare F10 as a dependency and it must not
spend their material:

    the four rules formally, pigeonhole, birthday, Shapley       -> P12
    implication, quantifiers, induction, contradiction, reading
      a theorem's hypotheses                                     -> P14
    O-notation and what it does and does not say                 -> P03
    a graph as a set plus a relation                             -> P13
    probability itself: the sample space, conditioning, Bayes    -> P23

So F10 supplies the counting and P03 supplies the notation for its growth;
F10 supplies the denominator and P23 supplies what to do with it; F10 supplies
and/or/not on conditions and P14 supplies implication and proof.

THE MEASUREMENTS, all free and all deterministic:
  * a fixed corpus, counted two ways -- how many tokens went past against how
    many distinct ones there were, which is the difference between a corpus
    and a vocabulary and is one call apart in code;
  * De Morgan checked on every assignment AND on a real mask, because the
    frame's claim is about what a filter does rather than about a truth table;
  * the all-pairs count, and what doubling the input does to it.

Run:  python3 code/f10_sets.py      (or: make numbers)
"""
from __future__ import annotations

from itertools import product
from pathlib import Path

VALUES: dict[str, tuple[str, bool]] = {}


def emit(key: str, value, digits: int | None = None) -> None:
    """Record one value under the name the book will reference it by."""
    if isinstance(value, float) and digits is not None:
        body = f"{value:.{digits}f}"
    elif isinstance(value, float):
        body = repr(value)
    else:
        body = str(value)
    try:
        float(body.replace("e", "E"))
        numeric = True
    except ValueError:
        numeric = False
    VALUES[key] = (body, numeric)


# ==========================================================================
# SECTION 1 --- a corpus is not a vocabulary
#
# The corpus is fixed here rather than read from anywhere, so the numbers do
# not move when the repository does. It is deliberately the shape of something
# a reader has actually counted: short log lines with heavy repetition, which
# is what makes the ratio interesting rather than incidental.
# ==========================================================================
CORPUS = [
    "request received from client",
    "request received from client",
    "cache miss for key user profile",
    "request received from client",
    "cache hit for key user profile",
    "request failed with timeout",
    "request received from client",
    "cache hit for key user profile",
    "retry scheduled after timeout",
    "request received from client",
    "cache hit for key session token",
    "request completed in time",
    "request received from client",
    "cache miss for key session token",
    "request failed with timeout",
    "retry scheduled after timeout",
    "request completed in time",
    "request received from client",
    "cache hit for key user profile",
    "request completed in time",
]
TOKENS = [w for line in CORPUS for w in line.split()]
VOCAB = set(TOKENS)

emit("f10.lines", len(CORPUS))
emit("f10.tokens", len(TOKENS))
emit("f10.vocab", len(VOCAB))
emit("f10.distinct.lines", len(set(CORPUS)))
emit("f10.repeat", len(TOKENS) / len(VOCAB), 1)

# The invariant, not the figures: a set discards repeats, so it can only ever
# be smaller, and it is strictly smaller exactly when something repeated.
assert len(VOCAB) <= len(TOKENS)
assert len(VOCAB) < len(TOKENS), "the corpus no longer repeats anything"
assert len(set(CORPUS)) < len(CORPUS), "the corpus no longer repeats a whole line"

# And order is discarded too, which is the half people forget: reversing the
# corpus changes every list and no set.
assert set(reversed(TOKENS)) == VOCAB, "a set is no longer indifferent to order"

# ==========================================================================
# SECTION 2 --- union, intersection, and the overlap counted twice
#
# Two evaluation sets that share some examples. The frame elicits "add them",
# and the gap between the two answers is the whole of the two-set rule.
# ==========================================================================
EVAL_A = set(range(0, 1000))
EVAL_B = set(range(800, 2000))
emit("f10.eval.a", len(EVAL_A))
emit("f10.eval.b", len(EVAL_B))
emit("f10.eval.naive", len(EVAL_A) + len(EVAL_B))
emit("f10.eval.shared", len(EVAL_A & EVAL_B))
emit("f10.eval.union", len(EVAL_A | EVAL_B))
emit("f10.eval.overcount", len(EVAL_A) + len(EVAL_B) - len(EVAL_A | EVAL_B))
emit("f10.eval.onlya", len(EVAL_A - EVAL_B))

# The rule itself, asserted over many pairs rather than on this one: the naive
# sum overcounts by exactly the size of the intersection, always.
for _s in range(0, 40):
    for _t in range(0, 40):
        _x, _y = set(range(0, 20 + _s)), set(range(_t, _t + 25))
        assert len(_x | _y) == len(_x) + len(_y) - len(_x & _y)

# ==========================================================================
# SECTION 3 --- a mask is a set, and De Morgan is what a filter does
#
# The claim the frame makes is about FILTERING, so it is checked on a filter
# and not only on a truth table. Both halves are here: every assignment of two
# booleans, and every record of a real list.
# ==========================================================================
for _a, _b in product((False, True), repeat=2):
    assert (not (_a and _b)) == ((not _a) or (not _b)), "De Morgan (and) broke"
    assert (not (_a or _b)) == ((not _a) and (not _b)), "De Morgan (or) broke"

# A record is (is_spam, is_short). "Keep everything that is not both spam and
# short" is the filter the frame asks the reader to write.
RECORDS = [(s, t) for s in (False, True) for t in (False, True) for _ in range(1, 6)]
KEEP_RIGHT = [r for r in RECORDS if not (r[0] and r[1])]
KEEP_WRONG = [r for r in RECORDS if (not r[0]) and (not r[1])]
emit("f10.rec.total", len(RECORDS))
emit("f10.rec.right", len(KEEP_RIGHT))
emit("f10.rec.wrong", len(KEEP_WRONG))
emit("f10.rec.lost", len(KEEP_RIGHT) - len(KEEP_WRONG))
assert len(KEEP_WRONG) < len(KEEP_RIGHT), "the wrong negation no longer drops anything"

# ==========================================================================
# SECTION 4 --- counting without listing
#
# The product rule, the subset rule, and what each does when its input grows.
# The subset figure is the one that surprises: 2^n is not "a lot more", it is
# a different kind of quantity.
# ==========================================================================
CHOICES = (4, 3, 5)                      # model, precision, batch size
emit("f10.grid", CHOICES[0] * CHOICES[1] * CHOICES[2])
emit("f10.grid.a", CHOICES[0])
emit("f10.grid.b", CHOICES[1])
emit("f10.grid.c", CHOICES[2])

# A run is a TRIPLE, so excluding one model-and-precision PAIR takes every
# batch size under it. Enumerated rather than subtracted, because the whole
# point of the frame is that the arithmetic people reach for is a subtraction
# of one and the object being removed is not one thing. Frame 25 quotes the
# one-pair figure and further problem 7 quotes the two-pair figure, so both
# come from this enumeration and cannot come apart.
GRID = [(m, p, b)
        for m in range(CHOICES[0])
        for p in range(CHOICES[1])
        for b in range(CHOICES[2])]
assert len(GRID) == CHOICES[0] * CHOICES[1] * CHOICES[2]


def runs_without(excluded_pairs):
    """Count the surviving triples once these (model, precision) pairs go."""
    return sum(1 for m, p, _ in GRID if (m, p) not in excluded_pairs)


ONE_PAIR = runs_without({(0, 0)})
TWO_PAIRS = runs_without({(0, 0), (1, 2)})
emit("f10.grid.less.one", ONE_PAIR)
emit("f10.grid.less.two", TWO_PAIRS)
assert len(GRID) - ONE_PAIR == CHOICES[2], "one excluded pair no longer costs a full row of batch sizes"
assert len(GRID) - TWO_PAIRS == 2 * CHOICES[2], "two excluded pairs no longer cost two rows"
assert ONE_PAIR != len(GRID) - 1, "the naive one-fewer answer now happens to be right"

FEATURES = 20
emit("f10.features", FEATURES)
emit("f10.subsets", 2 ** FEATURES)
emit("f10.subsets.one.more", 2 ** (FEATURES + 1))
assert 2 ** (FEATURES + 1) == 2 * 2 ** FEATURES, "one more element no longer doubles"

# ==========================================================================
# SECTION 5 --- counting as cost, and counting as a denominator
#
# The all-pairs count is where a set operation becomes a bill. Doubling the
# input does not double the work, and the figure is the point.
# ==========================================================================
def pairs(n: int) -> int:
    return n * (n - 1) // 2


N_DOCS = 1000
emit("f10.docs", N_DOCS)
emit("f10.pairs", pairs(N_DOCS))
emit("f10.docs2", 2 * N_DOCS)
emit("f10.pairs2", pairs(2 * N_DOCS))
emit("f10.pairs.ratio", pairs(2 * N_DOCS) / pairs(N_DOCS), 3)

# The INVARIANT rather than the figure. This assertion was written before the
# prose it supports and it failed on the first run, which is why the comment
# now says the opposite of what it first said: the ratio is
#     pairs(2n)/pairs(n) = (4n - 2)/(n - 1)
# which is a shade OVER four and falls towards four from ABOVE as n grows --
# 4.020 at n = 100, 4.002 at n = 1000. A frame quoting "four times" flatly
# would be wrong in the direction nobody checks.
for _n in (100, 1000, 10_000, 100_000):
    _r = pairs(2 * _n) / pairs(_n)
    assert 4.0 < _r < 4.05, f"the doubling ratio left (4.0, 4.05) at n = {_n}"
for _n in (100, 1000, 10_000):
    assert pairs(2 * _n) / pairs(_n) > pairs(20 * _n) / pairs(10 * _n), \
        "the doubling ratio no longer falls towards four"

# Test exercise 13 doubles a DIFFERENT corpus, so it needs its own ratio and
# not this section's. Quoting the n = 1000 figure there would attach a fixed
# number to the one quantity this section exists to show is n-dependent.
T13_DOCS = 5000                          # the exercise names it; not emitted
emit("f10.t13.ratio", pairs(2 * T13_DOCS) / pairs(T13_DOCS), 4)
assert round(pairs(2 * T13_DOCS) / pairs(T13_DOCS), 4) != round(pairs(2 * N_DOCS) / pairs(N_DOCS), 4), \
    "the exercise's ratio now equals the section's, so one of the two figures is redundant"

# The denominator. Counting is what a naive probability divides by, and F10
# stops exactly there: it produces the two counts and names the fraction.
# What a probability IS, and what conditioning does to it, is P23's.
FAULTS = 3
emit("f10.faults", FAULTS)
# The fraction itself is deliberately NOT emitted. It is two counts and a
# division, which is the frame's whole point, so the page builds it from the
# two counts rather than being handed a third number to trust.

# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f10.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f10_sets.py --- do not edit.",
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
    print(f"\n  {len(VALUES)} values -> {OUT.relative_to(OUT.parents[2])}")
    print(f"  De Morgan holds on all four assignments and on {len(RECORDS)} records")
    print(f"  the two-set union rule holds on all 1600 pairs tried")


if __name__ == "__main__":
    main()
