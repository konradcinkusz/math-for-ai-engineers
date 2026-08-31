#!/usr/bin/env python3
"""Program P04 --- Vectors, vector spaces and basis.

Every number Program P04 prints that the reader cannot do in their head is
computed here and written to figures/values/p04.tex, which the book \\input{}s.

P04's thesis is that SPAN, LINEAR INDEPENDENCE, BASIS AND DIMENSION ARE FOUR
WORDS FOR ONE IDEA, and that dimension is the number of independent directions
rather than the length of the list.

WHAT P04 IS OWED, and pays. Program F09 defined the arithmetic of vectors and
then said, in a warning box, that how vectors are ARRANGED in high dimension is
a different class of question, that Program P05 measures it, and that measuring
it properly needs the vocabulary THIS program sets up. Program P03's closing
frame says P04 is the first program in the book needing a new OBJECT rather
than a new question.

THE MEASUREMENTS:

  1. RANK SATURATES. A set of n random vectors in d dimensions has rank
     min(n, d), always -- so past d vectors the extra ones are combinations of
     the earlier ones, however many you add. Computed by elimination in pure
     Python, so `make numbers` needs no numpy.

  2. THE COUNTING FACT, applied. A vocabulary of 20,000 tokens embedded in
     4,096 dimensions cannot be linearly independent, and the number of
     dependent ones is the subtraction anybody can do. That is the payoff and
     it is a THEOREM rather than an experiment.

  3. DIMENSION IS NOT LENGTH. Eight vectors whose span has dimension two.

  4. A BASIS IS NOT UNIQUE. The same vector in two bases, with different
     coordinates and the same length -- which is what makes "embedding
     dimension 4096" a statement about the space and not about the numbers.

WHAT P04 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    inner products, norms, projection, near-orthogonality in high
      dimension -- which is the measurement F09 deferred            -> P05
    matrices as linear maps, and multiplication as composition      -> P06
    rank as a property of a matrix, and LoRA                        -> P08
P04 gives the vocabulary and the counting fact. It never measures an angle,
because it has not been given one.

Run:  python3 code/p04_vector_spaces.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p04.tex"
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


# ==========================================================================
# Rank by exact elimination over the rationals.
#
# EXACT, not floating point, and deliberately: this program's whole claim is
# that independence is a yes-or-no property, and P01 has just spent thirty
# frames establishing that a float comparison is not a yes-or-no question.
# Fraction costs nothing at these sizes and removes the tolerance argument
# entirely -- there is no epsilon in this file.
# ==========================================================================
def rank(rows: list[list[Fraction]]) -> int:
    rows = [r[:] for r in rows]
    n_rows, n_cols, r = len(rows), len(rows[0]), 0
    for c in range(n_cols):
        pivot = next((i for i in range(r, n_rows) if rows[i][c] != 0), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(n_rows):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == n_rows:
            break
    return r


# --- 1. rank saturates at the dimension, whatever you add ---
DIM_SMALL = 8
random.seed(20260831)


def random_rows(n: int, d: int) -> list[list[Fraction]]:
    return [[Fraction(random.randint(-99, 99)) for _ in range(d)] for _ in range(n)]


SATURATION = [(n, rank(random_rows(n, DIM_SMALL))) for n in (2, 4, 8, 12, 20, 40)]
emit("p04.sat.dim", DIM_SMALL)
for _n, _r in SATURATION:
    emit(f"p04.sat.rank.{_n}", _r)
for _n, _r in SATURATION:
    assert _r == min(_n, DIM_SMALL), (
        f"{_n} random vectors in {DIM_SMALL} dimensions gave rank {_r}, not "
        f"{min(_n, DIM_SMALL)}: the saturation the frames are about has gone")
NOTES.append(f"rank saturates at {DIM_SMALL}: " +
             ", ".join(f"{n}->{r}" for n, r in SATURATION))

# The claim asserted is the THEOREM, not one seed's luck: a set of more than d
# vectors in d dimensions is dependent, always. Checked over many draws so the
# frames can say "always" rather than "we tried one".
_trials = 300
for _ in range(_trials):
    d = random.randint(2, 6)
    n = d + random.randint(1, 4)
    assert rank(random_rows(n, d)) <= d, "more than d independent vectors in d dimensions"
emit("p04.sat.trials", _trials)
NOTES.append(f"over {_trials} random draws no set ever exceeded rank d, as it cannot")


# --- 2. the counting fact, applied to a vocabulary ---
VOCAB, EMBED = 20_000, 4_096
emit("p04.vocab", VOCAB)
emit("p04.embed", EMBED)
emit("p04.dependent", VOCAB - EMBED)
emit("p04.dependent.pct", f"{(VOCAB - EMBED) / VOCAB * 100:.0f}")
assert VOCAB > EMBED, "the vocabulary no longer exceeds the embedding dimension"
NOTES.append(f"at least {VOCAB - EMBED:,} of {VOCAB:,} embeddings are combinations of the others")


# --- 3. dimension is not the length of the list ---
# Eight vectors in five dimensions, every one of them built from two.
BASE_A = [Fraction(x) for x in (1, 0, 2, -1, 3)]
BASE_B = [Fraction(x) for x in (0, 1, -1, 4, 2)]
COMBOS = [(1, 0), (0, 1), (2, 3), (-1, 5), (4, -2), (7, 7), (-3, 1), (10, -6)]
FAMILY = [[a * x + b * y for x, y in zip(BASE_A, BASE_B)] for a, b in COMBOS]
emit("p04.family.count", len(FAMILY))
emit("p04.family.ambient", len(BASE_A))
emit("p04.family.dim", rank(FAMILY))
assert rank(FAMILY) == 2, "the eight-vector family no longer spans exactly two dimensions"
assert len(FAMILY) == 8 and len(BASE_A) == 5, "the family's shape changed under the frames"
NOTES.append(f"{len(FAMILY)} vectors, {len(BASE_A)} components each, span of dimension {rank(FAMILY)}")


# --- 4. a basis is not unique; coordinates change, the vector does not ---
# The same point of the plane, written against the standard axes and against a
# rotated pair. Exact where it can be, and the rotation is the one place this
# program needs a real number at all.
POINT = (3.0, 4.0)
THETA = math.radians(30)
NEW_1 = (math.cos(THETA), math.sin(THETA))
NEW_2 = (-math.sin(THETA), math.cos(THETA))
COORD_1 = POINT[0] * NEW_1[0] + POINT[1] * NEW_1[1]
COORD_2 = POINT[0] * NEW_2[0] + POINT[1] * NEW_2[1]
emit("p04.basis.x", f"{POINT[0]:.0f}")
emit("p04.basis.y", f"{POINT[1]:.0f}")
emit("p04.basis.angle", f"{math.degrees(THETA):.0f}")
emit("p04.basis.c1", f"{COORD_1:.4f}")
emit("p04.basis.c2", f"{COORD_2:.4f}")
emit("p04.basis.len", f"{math.hypot(*POINT):.0f}")
# THE INVARIANT, not the coordinates: a change of basis by a rotation leaves
# the length alone, and that is what makes it the SAME vector.
assert abs(math.hypot(COORD_1, COORD_2) - math.hypot(*POINT)) < 1e-12, (
    "the new coordinates no longer describe a vector of the same length, so "
    "they are not a change of basis")
assert abs(COORD_1 - POINT[0]) > 0.5 and abs(COORD_2 - POINT[1]) > 0.5, (
    "the two coordinate pairs are too close to make the frame's point")
NOTES.append(f"({POINT[0]:.0f}, {POINT[1]:.0f}) becomes ({COORD_1:.4f}, {COORD_2:.4f}); "
             f"length {math.hypot(*POINT):.0f} either way")

# A CROSS-PROGRAMME GATE HAS TO BE ON THE SAME COMPUTATION, and the first
# attempt here was not. It compared this basis example's length against F09's
# committed `f09.len3d` on the reasoning that both are "a length" -- and the
# assertion failed on the first run, because F09's is a different vector
# entirely. Two numbers that merely look alike are not a gate; they are a
# coincidence waiting to break a build for no reason.
#
# What IS shared is F09's embedding dimension, which this program's counting
# fact applies to unchanged. The frames quote it, so it is checked.
_f09dim = committed("f09.tex", "f09.dim")
if _f09dim is None:                                          # pragma: no cover
    NOTES.append("f09.tex absent: F09's embedding dimension was NOT checked")
else:
    assert int(_f09dim) < VOCAB, (
        f"F09's {_f09dim} dimensions no longer sit below a {VOCAB}-token "
        f"vocabulary, so the frame's second example has stopped working")
    emit("p04.f09.dependent", VOCAB - int(_f09dim))
    NOTES.append(f"at F09's {_f09dim} dimensions the same vocabulary leaves "
                 f"{VOCAB - int(_f09dim):,} dependent, which is the frame's second case")

# ==========================================================================
# The transcript. Nothing typed.
# ==========================================================================
# `rank` is imported rather than retyped, and that is not tidiness. A
# transcript is a promise that what is printed is what ran, so the test that
# matters is extracting it from the finished PDF and running what comes out.
# Without the import line a reader gets NameError on the last line, which is
# the fabricated-console-block defect wearing a generated file's clothes.
RANK_TEXT = """>>> from fractions import Fraction as F
>>> from p04_vector_spaces import rank    # run this from code/
>>> import random
>>> random.seed({seed})
>>> def draw(n, d):
...     return [[F(random.randint(-99, 99)) for _ in range(d)]
...             for _ in range(n)]
...
>>> [rank(draw(n, {d})) for n in (2, 4, 8, 12, 20, 40)]
{ranks}
""".format(seed=20260831, d=DIM_SMALL, ranks=[r for _, r in SATURATION])
assert RANK_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in RANK_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(RANK_TEXT.strip().splitlines()) <= 14, "transcript too tall for one frame"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p04-rank.txt").write_text(RANK_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p04-rank.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p04_vector_spaces.py --- do not edit.",
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
    print(f"\n  {len(VALUES)} values -> figures/values/p04.tex")
    for note in NOTES:
        print(f"  {note}")


if __name__ == "__main__":
    main()
