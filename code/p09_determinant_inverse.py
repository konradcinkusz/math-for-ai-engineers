#!/usr/bin/env python3
"""Program P09 --- Determinant, inverse and change of basis.

Every number Program P09 prints that the reader cannot do in their head is
computed here and written to figures/values/p09.tex, which the book \\input{}s.

P09's thesis is that THE DETERMINANT IS A SIGNED VOLUME SCALE FACTOR, that zero
means information was destroyed -- which is Program P08's null space seen from
the other side -- and that an inverse exists exactly when nothing was.

EXACT ARITHMETIC over Fraction wherever the mathematics is exact, which is
almost everywhere here: the determinant of a rational matrix is rational, the
inverse of a rational matrix is rational, and the signed area of a polygon with
rational corners is rational. P04's decision carries and P08 reused it; a
determinant computed with a tolerance would make "zero means destroyed" depend
on a threshold nobody can defend, in the one program where that sentence is the
whole point.

WHAT P09 IS OWED, read out of the files rather than remembered:

  P04  ALREADY DOES CHANGE OF BASIS AS A WORKED EXAMPLE: the point (3, 4)
       against axes turned by 30 degrees becomes (4.5981, 1.9641), with the
       coordinates changing and the length not. So the IDEA is spent, and what
       is left is better -- the change is itself a MATRIX, it is invertible
       exactly because nothing was destroyed, and P04's closing question
       ("does this method survive a change of basis") becomes a computation.
  P06  gives composition and non-commutativity, so det(AB) = det(A)det(B) is a
       statement about composing scale factors rather than an identity to check.
  P08  hands this program over by name: "rank says HOW MANY directions survive;
       the determinant says HOW MUCH of the space does, in one number that is
       zero exactly when something was destroyed -- which is this program's
       null space seen from the other side." So the det = 0 frame is a gate
       against P08's own rank, not a new fact.
  F08  has rotation matrices and that R(a)x . R(b)y depends only on b - a.

WHAT P09 LEAVES ALONE, checked against tools/programs.json:
    eigenvalues, the spectral theorem, positive definiteness        -> P10
    the SVD, the condition number, the pseudoinverse                -> P11
      -- and note that P09's brief says the cost of inv() is "measured in
      P10". P10's brief undertakes no such measurement; P11's undertakes
      "why the normal equations square the condition number and a QR solve
      does not, which is the concrete form of do not invert". So the pointer
      in the brief is stale by one and the program points at P11.

Run:  python3 code/p09_determinant_inverse.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p09.tex"
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


# --- the same elimination P04 wrote and P08 reused, so three programs cannot
# --- disagree about what a rank is
def rank(rows):
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


def det(M):
    """Exact determinant by elimination, tracking the sign of row swaps."""
    rows = [r[:] for r in M]
    n = len(rows)
    d = Fraction(1)
    for c in range(n):
        pivot = next((i for i in range(c, n) if rows[i][c] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != c:
            rows[c], rows[pivot] = rows[pivot], rows[c]
            d = -d
        d *= rows[c][c]
        for i in range(c + 1, n):
            f = rows[i][c] / rows[c][c]
            rows[i] = [a - f * b for a, b in zip(rows[i], rows[c])]
    return d


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def matvec(M, v):
    return [sum(r[j] * v[j] for j in range(len(v))) for r in M]


def eye(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def rand_mat(n, m, rnd, lo=-6, hi=6):
    return [[Fraction(rnd.randint(lo, hi)) for _ in range(m)] for _ in range(n)]


_rnd = random.Random(20260831)

# ==========================================================================
# 1. THE DETERMINANT IS A SIGNED AREA, and the sign is not decoration.
#
# Map the unit square's four corners and measure the parallelogram they land
# on with the shoelace formula. The SIGNED shoelace area equals the
# determinant exactly -- not its absolute value -- so a matrix that flips the
# plane over gives a negative one, and that is what "signed" is for.
# ==========================================================================
def shoelace(poly):
    n = len(poly)
    return Fraction(1, 2) * sum(
        poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
        for i in range(n))


UNIT = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)), (Fraction(0), Fraction(1))]

AREA_TRIALS = 300
for _ in range(AREA_TRIALS):
    A = rand_mat(2, 2, _rnd)
    img = [tuple(matvec(A, list(p))) for p in UNIT]
    assert shoelace(img) == det(A), \
        "the signed area of the image square must BE the determinant"

# The two worked cases the frames use, chosen so a reader can draw them.
STRETCH = [[Fraction(2), Fraction(0)], [Fraction(0), Fraction(3)]]
FLIP = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
assert det(STRETCH) == 6 and det(FLIP) == -1, "the worked matrices moved"
assert shoelace([tuple(matvec(FLIP, list(p))) for p in UNIT]) == -1, \
    "a swap of the axes must reverse the orientation, not merely preserve area"

emit("p09.area.trials", AREA_TRIALS)
emit("p09.stretch.det", int(det(STRETCH)))
emit("p09.flip.det", int(det(FLIP)))
NOTES.append(f"the signed shoelace area of the image of the unit square equals "
             f"the determinant exactly, on all {AREA_TRIALS} random matrices")

# ==========================================================================
# 2. ZERO MEANS DESTROYED, and this is a GATE AGAINST P08 rather than a new
#    fact: det(A) == 0 exactly when rank(A) < n, which is exactly when the
#    null space is not just the zero vector.
# ==========================================================================
SING_TRIALS = 300
_singular = 0
for _ in range(SING_TRIALS):
    n = _rnd.choice((2, 3, 4))
    if _rnd.random() < 0.5:
        A = rand_mat(n, n, _rnd)
    else:                                   # forced singular: a thin middle
        r = _rnd.randint(1, n - 1)
        A = matmul(rand_mat(n, r, _rnd), rand_mat(r, n, _rnd))
    is_zero, deficient = det(A) == 0, rank(A) < n
    assert is_zero == deficient, \
        "det = 0 and rank deficiency must be the same condition, always"
    _singular += is_zero

emit("p09.sing.trials", SING_TRIALS)
NOTES.append(f"det = 0 and rank < n agreed on all {SING_TRIALS} matrices "
             f"({_singular} of them singular), which is P08's null space seen "
             f"from the other side")

# ==========================================================================
# 3. det(AB) = det(A) det(B), so scale factors COMPOSE -- and one singular
#    factor makes the whole chain singular, which is P08's bottleneck told in
#    volumes rather than in directions.
# ==========================================================================
for _ in range(200):
    n = _rnd.choice((2, 3))
    A, B = rand_mat(n, n, _rnd), rand_mat(n, n, _rnd)
    assert det(matmul(A, B)) == det(A) * det(B), \
        "determinants must multiply along a product"

_flat = matmul(rand_mat(3, 2, _rnd), rand_mat(2, 3, _rnd))
assert det(_flat) == 0, "a matrix through a thin middle is singular"
_chain = _flat
for _ in range(4):
    _chain = matmul(rand_mat(3, 3, _rnd), _chain)
    assert det(_chain) == 0, "and nothing downstream can give the volume back"

# ==========================================================================
# 4. THE INVERSE, exactly -- and what it costs against just solving.
#
#    Both routines count their own multiplications and divisions, so the ratio
#    on the page is measured rather than quoted from a textbook's O(n^3/3).
# ==========================================================================
class Counter:
    def __init__(self):
        self.n = 0

    def mul(self, a, b):
        self.n += 1
        return a * b

    def div(self, a, b):
        self.n += 1
        return a / b


def solve(A, b, c: Counter):
    """Gaussian elimination with back substitution, counting its own work."""
    n = len(A)
    M = [row[:] + [rhs] for row, rhs in zip(A, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if M[i][k] != 0)
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, n):
            f = c.div(M[i][k], M[k][k])
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - c.mul(f, M[k][j])
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s = s - c.mul(M[i][j], x[j])
        x[i] = c.div(s, M[i][i])
    return x


def inverse(A, c: Counter):
    """Gauss-Jordan on [A | I], counting its own work."""
    n = len(A)
    M = [row[:] + e[:] for row, e in zip(A, eye(n))]
    for k in range(n):
        p = next(i for i in range(k, n) if M[i][k] != 0)
        M[k], M[p] = M[p], M[k]
        piv = M[k][k]
        M[k] = [c.div(v, piv) for v in M[k]]
        for i in range(n):
            if i != k and M[i][k] != 0:
                f = M[i][k]
                for j in range(2 * n):
                    M[i][j] = M[i][j] - c.mul(f, M[k][j])
    return [row[n:] for row in M]


def nonsingular(n, rnd):
    while True:
        A = rand_mat(n, n, rnd)
        if det(A) != 0:
            return A


# Exactness first: the inverse is exact over the rationals, so assert it.
for _ in range(60):
    n = _rnd.choice((2, 3, 4))
    A = nonsingular(n, _rnd)
    assert matmul(A, inverse(A, Counter())) == eye(n), \
        "A times its inverse must be the identity exactly, over the rationals"

# Then the cost. The comparison is like for like: ONE right-hand side, solved
# directly, against forming the inverse and multiplying it by the same vector.
COST_N = 50
_A = nonsingular(COST_N, _rnd)
_b = [Fraction(_rnd.randint(-6, 6)) for _ in range(COST_N)]

_c_solve = Counter()
_x_solve = solve(_A, _b, _c_solve)

_c_inv = Counter()
_Ainv = inverse(_A, _c_inv)
_x_inv = [sum(_Ainv[i][j] * _b[j] for j in range(COST_N)) for i in range(COST_N)]
_c_inv.n += COST_N * COST_N          # the multiply-through, counted honestly

assert _x_solve == _x_inv, "the two routes must agree exactly, or the point is lost"

RATIO = _c_inv.n / _c_solve.n
assert RATIO > 2.5, "inverting should cost several times what solving costs"
emit("p09.cost.n", COST_N)
emit("p09.cost.solve", f"{_c_solve.n:.2e}")
emit("p09.cost.invert", f"{_c_inv.n:.2e}")
emit("p09.cost.ratio", f"{RATIO:.1f}")
assert (f"{float(f'{_c_inv.n:.2e}') / float(f'{_c_solve.n:.2e}'):.1f}"
        == f"{RATIO:.1f}"), \
    "the ratio does not reproduce from the two numbers the page prints"
NOTES.append(f"at n = {COST_N}, solving costs {_c_solve.n} multiplications and "
             f"inverting-then-multiplying {_c_inv.n}, a factor of {RATIO:.1f} "
             f"-- for the same answer, exactly")

# ==========================================================================
# 5. CHANGE OF BASIS. P04 did this with numbers; here it is a matrix, and the
#    gate ties the two together: the same point, the same angle, the same two
#    coordinates. If P04's example ever moves, this build says so.
# ==========================================================================
_px, _py = committed("p04.tex", "p04.basis.x"), committed("p04.tex", "p04.basis.y")
_ang = committed("p04.tex", "p04.basis.angle")
_c1, _c2 = committed("p04.tex", "p04.basis.c1"), committed("p04.tex", "p04.basis.c2")
if all((_px, _py, _ang, _c1, _c2)):
    th = math.radians(float(_ang))
    R = [[math.cos(th), math.sin(th)], [-math.sin(th), math.cos(th)]]
    got = [R[0][0] * float(_px) + R[0][1] * float(_py),
           R[1][0] * float(_px) + R[1][1] * float(_py)]
    assert f"{got[0]:.4f}" == _c1 and f"{got[1]:.4f}" == _c2, \
        f"the change-of-basis matrix does not reproduce P04's coordinates"
    NOTES.append(f"gate: the change-of-basis matrix at {_ang} degrees sends "
                 f"P04's ({_px}, {_py}) to ({_c1}, {_c2}), which is P04's own "
                 f"committed pair")
else:                                                        # pragma: no cover
    NOTES.append("P04's values are absent, so the change-of-basis gate was skipped")

# An ORTHOGONAL change of basis, exactly, using the 3-4-5 triple so that every
# entry is rational and the reader can check the determinant by hand.
# NOTE the convention. This is the CHANGE-OF-BASIS matrix the section derived
# three frames earlier -- rows (cos, sin) and (-sin, cos) -- at cos = 3/5 and
# sin = 4/5, so a reader substituting into that formula gets exactly this
# matrix. It used to be written the other way round, which is the same rotation
# through -theta and the active convention rather than the passive one, so the
# page displayed the transpose of the formula it told the reader to check
# against. Both are rotations and every number below is unchanged; what was
# wrong was that the two frames disagreed with nothing said about it.
ROT345 = [[Fraction(3, 5), Fraction(4, 5)], [Fraction(-4, 5), Fraction(3, 5)]]
assert det(ROT345) == 1, "a rotation must preserve signed area exactly"
assert matmul(ROT345, [[Fraction(3, 5), Fraction(-4, 5)],
                       [Fraction(4, 5), Fraction(3, 5)]]) == eye(2), \
    "the transpose of a rotation must be its inverse"
_v = [Fraction(3), Fraction(4)]
_rv = matvec(ROT345, _v)
assert sum(x * x for x in _v) == sum(x * x for x in _rv) == 25, \
    "a rotation must preserve length exactly"
emit("p09.rot.det", int(det(ROT345)))
emit("p09.rot.len2", int(sum(x * x for x in _v)))

# A reflection has determinant -1 and preserves length just as well, which is
# why "determinant 1" and "preserves length" are two conditions rather than one.
REFLECT = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(-1)]]
assert det(REFLECT) == -1, "a reflection reverses orientation"
_fv = matvec(REFLECT, _v)
assert sum(x * x for x in _fv) == 25, "and it preserves length anyway"
emit("p09.reflect.det", int(det(REFLECT)))

# And the counterexample the other way, so the closing trapbox is gated rather
# than argued: a SHEAR has determinant 1 and preserves almost no length. The
# two conditions are independent, and the page says so with one example each.
SHEAR = [[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]]
assert det(SHEAR) == 1, "a shear preserves area"
_sv = matvec(SHEAR, [Fraction(0), Fraction(1)])
assert _sv == [Fraction(1), Fraction(1)], "the shear must send (0,1) to (1,1)"
assert sum(x * x for x in _sv) == 2, "and lengthen it, which is the whole point"

DET_TEXT = """\
>>> from p09_determinant_inverse import det, rank
>>> from fractions import Fraction as F
>>> A = [[F(1), F(2), F(3)],
...      [F(4), F(5), F(6)],
...      [F(7), F(8), F(9)]]    # rows 1, 2, 3 in arithmetic
>>> det(A), rank(A)
{out}
"""
_A3 = [[Fraction(1), Fraction(2), Fraction(3)],
       [Fraction(4), Fraction(5), Fraction(6)],
       [Fraction(7), Fraction(8), Fraction(9)]]
_out = (det(_A3), rank(_A3))
assert _out == (Fraction(0), 2), "the worked singular matrix moved"
DET_TEXT = DET_TEXT.format(out=f"(Fraction(0, 1), {_out[1]})")
assert DET_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in DET_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(DET_TEXT.strip().splitlines()) <= 14, "transcript too tall"
emit("p09.worked.rank", _out[1])


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p09-singular.txt").write_text(DET_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p09-singular.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p09_determinant_inverse.py --- do not edit.",
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
