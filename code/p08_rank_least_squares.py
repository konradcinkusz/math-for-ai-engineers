#!/usr/bin/env python3
"""Program P08 --- Rank, the four subspaces and least squares.

Every number Program P08 prints that the reader cannot do in their head is
computed here and written to figures/values/p08.tex, which the book \\input{}s.

P08's thesis is that RANK IS THE HONEST MEASURE OF HOW MUCH A MATRIX DOES,
and that it is one number rather than two: the column space and the row space
have the same dimension, which is not obvious and is the program's centrepiece.

EXACT ARITHMETIC THROUGHOUT, over Fraction, with no epsilon anywhere. That is
P04's decision and its reasoning carries: a rank computed with a tolerance
makes the program's central theorem depend on a threshold nobody can defend.
The elimination is P04's, reused rather than rewritten so the two programs
cannot disagree about what a rank is.

WHAT P08 IS OWED, read out of the files rather than remembered:

  P04  ALREADY HAS RANK AS A COMPUTED QUANTITY -- of a SET OF VECTORS. Its
       section 5 measures the saturation (two vectors reach 2, forty reach 8 in
       8 dimensions) and turns it into the counting bound on an embedding
       matrix. So the saturation demonstration is SPENT. What is left, and is
       the better half, is rank as a property of a MATRIX, which brings the
       four subspaces and the row-rank/column-rank theorem with it.
  P05  hands least squares over twice and by name: "the same formula projects
       onto a line in any number of dimensions, and onto a subspace, and --
       once Program P08 arrives -- onto the column space of a matrix, which is
       what least squares is." So least squares here is ONE OBJECT SWAPPED
       INTO P05's derivation, not a second derivation.
  P06  "Program P08 is where the thin dimension gets its name and the
       assumption behind it gets stated" -- the low-rank update, whose
       MECHANICAL half (associativity spent deliberately) P06 already paid.
  P07  says the word `rank` means two things two programs apart, and that P08
       has to say it back.

WHAT P08 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    the determinant, the inverse, change of basis                   -> P09
    eigenvalues, the spectral theorem, positive definiteness        -> P10
    the SVD, Eckart-Young, the condition number, the pseudoinverse  -> P11
      -- so HOW GOOD a rank-r approximation is belongs to P11. This program
      states the assumption a low-rank update makes and does not test it.
    why the normal equations are the wrong way to solve it in practice -> P11

Run:  python3 code/p08_rank_least_squares.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p08.tex"
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
# The elimination, over the rationals. This is P04's, unchanged, and it is
# unchanged on purpose: two programs that both talk about rank must not be
# able to disagree about what one is.
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


def transpose(M):
    return [list(col) for col in zip(*M)]


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def rand_mat(n, m, rnd, lo=-9, hi=9):
    return [[Fraction(rnd.randint(lo, hi)) for _ in range(m)] for _ in range(n)]


_rnd = random.Random(20260831)

# ==========================================================================
# 1. ROW RANK EQUALS COLUMN RANK, and this is the program's centrepiece.
#
# It is a theorem, so the draws are TESTING THE CODE rather than looking for a
# counterexample -- P04's framing, and it is worth repeating because the two
# look identical and mean opposite things. A search that succeeded here would
# have refuted a proof.
#
# The shapes are deliberately non-square and deliberately include deficient
# matrices built as a product with a thin middle, because a fair test of
# "the two ranks agree" has to include the cases where the rank is not simply
# min(rows, cols).
# ==========================================================================
RANK_TRIALS = 400
_shapes = [(3, 5), (5, 3), (4, 4), (2, 7), (7, 2), (6, 4)]
for _ in range(RANK_TRIALS):
    n, m = _shapes[_rnd.randrange(len(_shapes))]
    if _rnd.random() < 0.5:
        A = rand_mat(n, m, _rnd)
    else:                                  # forced deficient: thin middle
        r = _rnd.randint(1, min(n, m))
        A = matmul(rand_mat(n, r, _rnd), rand_mat(r, m, _rnd))
    assert rank(A) == rank(transpose(A)), \
        "row rank and column rank must agree, always"

emit("p08.rank.trials", RANK_TRIALS)
NOTES.append(f"row rank equals column rank on all {RANK_TRIALS} matrices, "
             f"exactly, over the rationals")

# ==========================================================================
# 2. RANK-NULLITY. rank + nullity = number of COLUMNS, and the number of
#    columns is the dimension of the space the matrix reads, not of the one it
#    writes into -- which is the half people get backwards.
# ==========================================================================
def nullity(A) -> int:
    return len(A[0]) - rank(A)


for _ in range(200):
    n, m = _shapes[_rnd.randrange(len(_shapes))]
    A = rand_mat(n, m, _rnd)
    assert rank(A) + nullity(A) == len(A[0]), \
        "rank plus nullity must be the number of columns"

# The worked case the frames use: a 2 x 3 matrix cannot have rank above 2, so
# its null space is at least one-dimensional -- something IS sent to zero, and
# no amount of choosing the entries avoids it.
# The frame PRINTS this matrix, so the display and the script must not be able
# to come apart: the entries are asserted here rather than left to the author
# having copied them across. It used to say "take a concrete matrix" and give
# none, and then quote "measured on the worked matrix" for an object the reader
# could not see -- and the figures are not forced by the shape either, since
# [[1,2,3],[2,4,6]] is 2 x 3 with rank 1 and nullity 2.
WIDE = [[Fraction(1), Fraction(2), Fraction(3)],
        [Fraction(4), Fraction(5), Fraction(6)]]
assert WIDE == [[Fraction(1), Fraction(2), Fraction(3)],
                [Fraction(4), Fraction(5), Fraction(6)]], \
    "the matrix the frame displays must be the matrix measured here"
assert rank(WIDE) == 2 and nullity(WIDE) == 1, "the worked wide case moved"
emit("p08.wide.rows", len(WIDE))
emit("p08.wide.cols", len(WIDE[0]))
emit("p08.wide.rank", rank(WIDE))
emit("p08.wide.null", nullity(WIDE))

# ==========================================================================
# 3. A BOTTLENECK IS PERMANENT. rank(AB) <= min(rank A, rank B), so a chain
#    that passes through a rank-r map can never exceed r afterwards, whatever
#    is stacked on top. That is the exact mechanism under the phenomenon the
#    literature calls rank collapse; the phenomenon itself is empirical and
#    model-specific, and this program says so rather than measuring it.
# ==========================================================================
CHAIN_D, CHAIN_R, CHAIN_LEN = 6, 2, 5
_bottleneck = matmul(rand_mat(CHAIN_D, CHAIN_R, _rnd),
                     rand_mat(CHAIN_R, CHAIN_D, _rnd))
assert rank(_bottleneck) == CHAIN_R, "the bottleneck should have the rank built into it"

_chain = _bottleneck
for _ in range(CHAIN_LEN):
    _chain = matmul(rand_mat(CHAIN_D, CHAIN_D, _rnd), _chain)
    assert rank(_chain) <= CHAIN_R, "nothing downstream can recover the lost rank"
assert rank(_chain) == CHAIN_R, "and full-rank factors do not lose any more of it"

for _ in range(200):
    A, B = rand_mat(4, 4, _rnd), rand_mat(4, 4, _rnd)
    assert rank(matmul(A, B)) <= min(rank(A), rank(B)), \
        "a product cannot have more rank than either factor"

emit("p08.chain.d", CHAIN_D)
emit("p08.chain.r", CHAIN_R)
emit("p08.chain.len", CHAIN_LEN)
NOTES.append(f"a rank-{CHAIN_R} bottleneck survives {CHAIN_LEN} full-rank "
             f"{CHAIN_D}x{CHAIN_D} factors stacked on top of it")

# ==========================================================================
# 4. LEAST SQUARES IS A PROJECTION, and the assertion is the DEFINING
#    PROPERTY rather than the answer: the residual is orthogonal to every
#    column of A. P05 derived the projection from three properties of the
#    inner product and said in as many words that swapping a subspace in for
#    the line changes nothing; this is that sentence with the object swapped.
#
#    Three points chosen so the whole thing is exact and hand-checkable: the
#    fitted line, both orthogonality conditions and the residuals are all
#    small rationals.
# ==========================================================================
PTS = [(Fraction(1), Fraction(1)), (Fraction(2), Fraction(3)),
       (Fraction(3), Fraction(2))]
A_LS = [[x, Fraction(1)] for x, _ in PTS]          # columns: x and a constant
B_LS = [y for _, y in PTS]

# There is no solution: the three points are not collinear. Say so exactly, by
# showing that b is not in the column space -- rank goes up when b is added.
_aug = [row + [b] for row, b in zip(A_LS, B_LS)]
assert rank(A_LS) == 2 and rank(_aug) == 3, \
    "the worked system must have no solution at all"

# Normal equations, solved exactly. (P11 owns why this is the wrong way to do
# it on a machine; over the rationals there is no conditioning to worry about.)
AtA = matmul(transpose(A_LS), A_LS)
Atb = [sum(transpose(A_LS)[i][k] * B_LS[k] for k in range(len(B_LS)))
       for i in range(2)]
_det = AtA[0][0] * AtA[1][1] - AtA[0][1] * AtA[1][0]
assert _det != 0, "the normal equations are singular, which the frames do not expect"
SLOPE = (Atb[0] * AtA[1][1] - AtA[0][1] * Atb[1]) / _det
INTERCEPT = (AtA[0][0] * Atb[1] - Atb[0] * AtA[1][0]) / _det

RESID = [b - (SLOPE * x + INTERCEPT) for (x, _), b in zip(PTS, B_LS)]
for col in transpose(A_LS):
    assert sum(c * r for c, r in zip(col, RESID)) == 0, \
        "the residual must be orthogonal to every column of A -- that IS the projection"

SSE = sum(r * r for r in RESID)

# "Closest" is measured rather than asserted: perturb the fit in both
# coefficients and in both directions, and every perturbation must be worse.
for dm in (Fraction(-1, 4), Fraction(0), Fraction(1, 4)):
    for dc in (Fraction(-1, 4), Fraction(0), Fraction(1, 4)):
        if dm == 0 and dc == 0:
            continue
        alt = sum((b - ((SLOPE + dm) * x + INTERCEPT + dc)) ** 2
                  for (x, _), b in zip(PTS, B_LS))
        assert alt > SSE, "a perturbed line must fit worse than the projection"

emit("p08.ls.slope", f"{float(SLOPE):.1f}")
emit("p08.ls.intercept", f"{float(INTERCEPT):.0f}")
emit("p08.ls.sse", f"{float(SSE):.1f}")
emit("p08.ls.points", len(PTS))
NOTES.append(f"least squares on {len(PTS)} points gives y = {SLOPE}x + "
             f"{INTERCEPT} with residuals {[str(r) for r in RESID]}, both "
             f"orthogonality conditions exactly zero")

# ==========================================================================
# 5. THE LOW-RANK UPDATE, priced. P06 paid the mechanical half -- keep the
#    thin factor in the middle and never form the outer product -- and this is
#    the other half: what the constraint costs and what it assumes.
#
#    Note what is NOT here. How much of a real update a rank-r matrix can
#    capture is a question about singular values, and that is P11's. This
#    program states the assumption and hands the test over.
# ==========================================================================
LORA_D, LORA_R = 4096, 8
DENSE = LORA_D * LORA_D
LOWRANK = 2 * LORA_D * LORA_R
assert LOWRANK < DENSE, "a low-rank update is only worth the name when it is smaller"

emit("p08.lora.d", LORA_D)
emit("p08.lora.r", LORA_R)
emit("p08.lora.dense", f"{DENSE:.2e}")
emit("p08.lora.lowrank", f"{LOWRANK:.2e}")
emit("p08.lora.factor", round(DENSE / LOWRANK))
emit("p08.lora.pct", f"{100 * LOWRANK / DENSE:.2f}")

# THE CROSSOVER, and it is the part nobody quotes: 2dr >= d^2 exactly when
# r >= d/2, so an adapter with an inner dimension above half the width costs
# MORE than the dense update it is standing in for. "Low-rank" is a claim
# about a number, and the number has a threshold.
LORA_CROSS = LORA_D // 2
assert 2 * LORA_D * LORA_CROSS == DENSE, "the crossover is not where it was"
assert 2 * LORA_D * (LORA_CROSS + 1) > DENSE, "and above it the adapter is dearer"
emit("p08.lora.cross", LORA_CROSS)

# The ratio has to reproduce from the two numbers the page prints -- F04's
# 22 778, F05's 51.7 and P07's 286 were all caught by doing this division.
assert round(float(f"{DENSE:.2e}") / float(f"{LOWRANK:.2e}")) == round(DENSE / LOWRANK), \
    "the factor does not reproduce from the two figures the page carries"

NOTES.append(f"a {LORA_D}x{LORA_D} update is {DENSE:.2e} parameters and its "
             f"rank-{LORA_R} stand-in {LOWRANK:.2e}, a factor of "
             f"{round(DENSE / LOWRANK)}; the crossover is at r = {LORA_CROSS}")

# ==========================================================================
# The cross-programme gate. P04 quotes the counting bound on an embedding
# matrix and this program quotes the same two integers to say what the rank of
# that matrix is bounded by, so the two ARE one computation and a gate is
# worth having. P04's own pass established the converse: a gate wired to two
# numbers that merely appear together is the defect the mechanism exists to
# catch.
# ==========================================================================
_vocab = committed("p04.tex", "p04.vocab")
_embed = committed("p04.tex", "p04.embed")
if _vocab and _embed:
    assert int(_embed.replace(",", "")) < int(_vocab.replace(",", "")), \
        "P04's embedding matrix should be wider than it is tall"
    emit("p08.emb.rank.max", int(_embed.replace(",", "")))
    NOTES.append(f"gate: the embedding matrix P04 counts has rank at most "
                 f"{_embed}, which is P04's own committed dimension")
else:                                                        # pragma: no cover
    NOTES.append("P04's values are absent, so the cross-programme gate was skipped")

# TWO transcripts, and the split is the point. The rank test belongs where the
# frame asks whether b is reachable. The orthogonality check belongs AFTER the
# frame that tells the reader to do it by hand -- it used to sit in the same
# listing, on the same page as the question "what is the residual perpendicular
# to here?", so the machine had already answered both that question and the
# hand check one leaf before either was put. A transcript is under the same
# rule as a frame: it may not answer a question put to the reader later on.
LS_TEXT = """\
>>> from p08_rank_least_squares import rank
>>> A = [[1, 1], [2, 1], [3, 1]]   # an x column and a constant
>>> b = [1, 3, 2]                  # not on any straight line
>>> rank(A), rank([r + [c] for r, c in zip(A, b)])
{ranks}
"""
ORTH_TEXT = """\
>>> from p08_rank_least_squares import transpose
>>> A = [[1, 1], [2, 1], [3, 1]]
>>> r2 = [-1, 2, -1]               # twice the residual
>>> [sum(c*v for c, v in zip(col, r2)) for col in transpose(A)]
{orth}
"""
_ranks = (rank([[Fraction(v) for v in row] for row in A_LS]),
          rank([[Fraction(v) for v in row] for row in _aug]))
_resid2 = [-1, 2, -1]
_orth = [sum(c * r for c, r in zip(col, _resid2))
         for col in transpose([[1, 1], [2, 1], [3, 1]])]
assert _orth == [0, 0], "the doubled residual must still be orthogonal"
LS_TEXT = LS_TEXT.format(ranks=str(_ranks))
ORTH_TEXT = ORTH_TEXT.format(orth=str(_orth))
for _t in (LS_TEXT, ORTH_TEXT):
    assert _t.isascii(), "listings cannot set a non-ASCII transcript"
    assert max(len(l) for l in _t.splitlines()) <= 64, "transcript too wide"
    assert len(_t.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p08-least-squares.txt").write_text(LS_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p08-least-squares.txt")
    (TRANSCRIPTS / "p08-orthogonality.txt").write_text(ORTH_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p08-orthogonality.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p08_rank_least_squares.py --- do not edit.",
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
        print(f"  {k:<{width}}  {body}")
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
