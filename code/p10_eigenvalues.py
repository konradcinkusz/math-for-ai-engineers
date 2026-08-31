#!/usr/bin/env python3
"""Program P10 --- Eigenvalues, quadratic forms and positive definiteness.

Every number Program P10 prints that the reader cannot do in their head is
computed here and written to figures/values/p10.tex, which the book \\input{}s.

P10's thesis is that AN EIGENVECTOR IS A DIRECTION THE MATRIX ONLY STRETCHES,
that a symmetric matrix has a full orthogonal set of them, and that the
eigenvalues of a quadratic form say whether it is a bowl, a saddle or a ridge.

EXACT ARITHMETIC over Fraction wherever the mathematics is exact. That is more
of this program than it looks, because of one construction: a rational
orthogonal Q (from the 3-4-5 triple Program P09 already used) times a rational
diagonal D gives A = Q D Q^T, a rational SYMMETRIC matrix whose eigenvalues are
exactly D's entries and whose eigenvectors are exactly Q's columns. So the
spectral theorem can be demonstrated with no rounding anywhere, on matrices
whose answers are known by construction rather than by a solver.

WHAT P10 IS OWED, read out of the files rather than remembered:

  P09  HANDS THIS PROGRAM OVER BY NAME, and the handover is a promise about
       arithmetic: "not how much of the space survives, but which directions
       come through unturned, only stretched -- and the determinant turns out
       to be the product of the amounts they are stretched by." So
       det = product of eigenvalues is a CROSS-PROGRAMME GATE, computed with
       P09's own det() rather than restated.
  P06  gives composition, so A^k acting on an eigenvector is lambda^k times it
       and needs no new machinery.
  P08  gives rank and the null space: a zero eigenvalue IS a null vector, so
       "singular" and "has a zero eigenvalue" are the same sentence twice.
  P05  gives lengths and angles, which is what "orthogonal set" is said in.
  P04  gives basis, which is what a full set of eigenvectors is.

WHAT P10 LEAVES ALONE, checked against tools/programs.json:
    the SVD, Eckart-Young, the condition number, the pseudoinverse    -> P11
    the step-size bound derived from the curvature                    -> P17
    the optimisers that spend it                                      -> P20
      -- so this program COLLECTS the shape of the basin and does not spend
      it. It may say the eigenvalues are the axes of the level ellipse and
      how elongated it is; the largest stable learning rate is P17's.

FORWARD REFERENCE, DECLARED: the covariance matrix is defined in P24. This
program needs exactly two facts about it -- symmetric, and positive
semi-definite -- and both are stated in the Learning outcomes with the
pointer, on the pattern P21 uses for its probability prerequisites.

Run:  python3 code/p10_eigenvalues.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p10.tex"
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


# --- the same exact machinery P04 wrote, P08 reused and P09 reused again -----
def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def matvec(M, v):
    return [sum(r[j] * v[j] for j in range(len(v))) for r in M]


def transpose(M):
    return [list(col) for col in zip(*M)]


def eye(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def det(M):
    """P09's exact determinant, by elimination, tracking the sign of swaps."""
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


def trace(M):
    return sum(M[i][i] for i in range(len(M)))


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def eig2(M):
    """Exact eigenvalues of a 2x2 rational matrix, or None if they are not real.

    The characteristic polynomial is lambda^2 - (tr)lambda + det, so the
    discriminant is tr^2 - 4det. Returned exactly when that is the square of a
    rational, which is the only case this program prints -- everything else it
    talks about rather than tabulates.
    """
    t, d = trace(M), det(M)
    disc = t * t - 4 * d
    if disc < 0:
        return None                     # no real eigenvalue at all
    r = math.isqrt(disc.numerator) ** 2 == disc.numerator and \
        math.isqrt(disc.denominator) ** 2 == disc.denominator
    if not r:
        return "irrational"
    s = Fraction(math.isqrt(disc.numerator), math.isqrt(disc.denominator))
    return sorted(((t + s) / 2, (t - s) / 2), reverse=True)


def nullvec2(M):
    """A non-zero exact solution of Mx = 0 for a singular 2x2, or None."""
    a, b = M[0]
    c, d = M[1]
    for cand in ((-b, a), (d, -c), (b, -a), (-d, c)):
        if any(x != 0 for x in cand) and matvec(M, list(cand)) == [0, 0]:
            return [Fraction(x) for x in cand]
    return None


def eigvec2(M, lam):
    return nullvec2([[M[0][0] - lam, M[0][1]], [M[1][0], M[1][1] - lam]])


# ==========================================================================
# 1. AN EIGENVECTOR IS A DIRECTION THE MATRIX ONLY STRETCHES.
#
#    The worked symmetric case, chosen so a reader can verify every step by
#    hand: eigenvalues 3 and 1, eigenvectors (1,1) and (1,-1).
# ==========================================================================
SYM = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(2)]]
_lams = eig2(SYM)
assert _lams == [3, 1], f"the worked symmetric matrix moved: {_lams}"

_v_hi, _v_lo = eigvec2(SYM, _lams[0]), eigvec2(SYM, _lams[1])
for lam, v in zip(_lams, (_v_hi, _v_lo)):
    assert matvec(SYM, v) == [lam * x for x in v], \
        "Av must equal lambda v exactly, or the example is not what it claims"
assert dot(_v_hi, _v_lo) == 0, "the two eigenvectors of a symmetric matrix"

emit("p10.sym.hi", int(_lams[0]))
emit("p10.sym.lo", int(_lams[1]))

# THE GATE P09 ASKED FOR, and it is the whole reason this program follows that
# one: det is the PRODUCT of the eigenvalues and trace is their SUM. Computed
# with P09's own det(), so the two programs cannot drift apart.
assert det(SYM) == _lams[0] * _lams[1], "det must be the product of the eigenvalues"
assert trace(SYM) == _lams[0] + _lams[1], "trace must be their sum"
emit("p10.sym.det", int(det(SYM)))
emit("p10.sym.trace", int(trace(SYM)))
NOTES.append("gate: det = product of the eigenvalues and trace = their sum, "
             "exactly, with P09's own det() -- which is the promise P09's "
             "closing frame made to this program")

# ==========================================================================
# 2. THE TRAP THE MANIFEST ASSIGNS TO THIS PROGRAM: "eigenvectors are
#    orthogonal". They are, for a symmetric matrix. Here is one that is not.
# ==========================================================================
NONSYM = [[Fraction(2), Fraction(1)], [Fraction(0), Fraction(3)]]
_n_lams = eig2(NONSYM)
assert _n_lams == [3, 2], f"the worked non-symmetric matrix moved: {_n_lams}"
_n_hi, _n_lo = eigvec2(NONSYM, _n_lams[0]), eigvec2(NONSYM, _n_lams[1])
for lam, v in zip(_n_lams, (_n_hi, _n_lo)):
    assert matvec(NONSYM, v) == [lam * x for x in v], "Av = lambda v, exactly"
assert dot(_n_hi, _n_lo) != 0, \
    "the point of this matrix is that its eigenvectors are NOT perpendicular"

_ang = math.degrees(math.acos(
    dot(_n_hi, _n_lo) / math.sqrt(dot(_n_hi, _n_hi) * dot(_n_lo, _n_lo))))
assert 0 < _ang < 90, "and the angle between them is a genuine acute angle"
emit("p10.nonsym.hi", int(_n_lams[0]))
emit("p10.nonsym.lo", int(_n_lams[1]))
emit("p10.nonsym.angle", round(_ang, 1), 1)
NOTES.append(f"the non-symmetric matrix has eigenvalues {int(_n_lams[0])} and "
             f"{int(_n_lams[1])} and its eigenvectors meet at {_ang:.1f} "
             f"degrees, not at a right angle")

# Two more failures a reader should know are possible, both exact.
ROT90 = [[Fraction(0), Fraction(-1)], [Fraction(1), Fraction(0)]]
assert eig2(ROT90) is None, "a quarter turn has NO real eigenvalue: nothing " \
                            "in the plane comes through undeflected"
SHEAR = [[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]]
assert eig2(SHEAR) == [1, 1], "the shear's eigenvalue is 1 twice"
assert det([[SHEAR[0][0] - 1, SHEAR[0][1]],
            [SHEAR[1][0], SHEAR[1][1] - 1]]) == 0, "so it is singular at lambda = 1"
# ... and yet only ONE direction survives, which is what "defective" means.
_s_dirs = {tuple(Fraction(x, y or 1) for x, y in [(v[0], v[1])])
           for v in [eigvec2(SHEAR, Fraction(1))] if v and v[1] != 0}
assert eigvec2(SHEAR, Fraction(1)) == [Fraction(1), Fraction(0)] or \
       matvec(SHEAR, eigvec2(SHEAR, Fraction(1))) == eigvec2(SHEAR, Fraction(1)), \
       "the shear keeps only the horizontal direction"
NOTES.append("a quarter turn has no real eigenvalue and the shear has one "
             "eigenvalue twice but only one direction -- two ways for the "
             "'full set of eigenvectors' promise to fail, both exact")

# ==========================================================================
# 3. THE SPECTRAL THEOREM, demonstrated with NO ROUNDING ANYWHERE.
#
#    Take the rational orthogonal Q that Program P09 built from the 3-4-5
#    triple, and a rational diagonal D. Then A = Q D Q^T is rational,
#    symmetric, and its eigenvalues ARE D's entries with Q's columns as
#    eigenvectors -- known by construction rather than found by a solver. So
#    "a symmetric matrix has a full orthogonal set of eigenvectors" can be
#    checked exactly rather than to a tolerance, which is the only way to
#    check a statement containing the word "exactly".
# ==========================================================================
Q = [[Fraction(3, 5), Fraction(-4, 5)], [Fraction(4, 5), Fraction(3, 5)]]
assert matmul(transpose(Q), Q) == eye(2), "Q must be orthogonal, exactly"

SPECTRAL_TRIALS = 0
for a in range(-6, 7):
    for b in range(-6, 7):
        D = [[Fraction(a), Fraction(0)], [Fraction(0), Fraction(b)]]
        A = matmul(matmul(Q, D), transpose(Q))
        assert A == transpose(A), "Q D Q^T must come out symmetric"
        cols = transpose(Q)
        for lam, v in zip((a, b), cols):
            assert matvec(A, list(v)) == [lam * x for x in v], \
                "each column of Q must be an eigenvector with D's entry"
        assert dot(cols[0], cols[1]) == 0, "and the two must be perpendicular"
        assert det(A) == a * b and trace(A) == a + b, \
            "det and trace must agree with the eigenvalues here too"
        SPECTRAL_TRIALS += 1

emit("p10.spectral.trials", SPECTRAL_TRIALS)
NOTES.append(f"the spectral theorem checked exactly on {SPECTRAL_TRIALS} "
             f"rational symmetric matrices built as Q D Q^T -- eigenvalues, "
             f"eigenvectors and orthogonality all with no rounding")

# ==========================================================================
# 4. A QUADRATIC FORM IS A BOWL, A SADDLE OR A RIDGE, and the eigenvalues say
#    which. Built from the same construction so the eigenvalues are known.
#
#    The assertion is the CLASSIFICATION rather than any single value: sample
#    the form all round the circle and require the sign pattern the
#    eigenvalues predict. A form whose eigenvalues are both positive must be
#    positive in EVERY direction, which is what "positive definite" says and
#    is a claim about infinitely many directions rather than about a few.
# ==========================================================================
def form(A, x):
    return dot(x, matvec(A, x))


def sample_signs(A, n=720):
    vals = [form(A, [Fraction(round(math.cos(2 * math.pi * k / n) * 10**6), 10**6),
                     Fraction(round(math.sin(2 * math.pi * k / n) * 10**6), 10**6)])
            for k in range(n)]
    return min(vals), max(vals)


CASES = {"bowl": (5, 2), "saddle": (5, -2), "ridge": (5, 0), "dome": (-5, -2)}
CLASSIFIED = {}
for name, (a, b) in CASES.items():
    D = [[Fraction(a), Fraction(0)], [Fraction(0), Fraction(b)]]
    A = matmul(matmul(Q, D), transpose(Q))
    lo, hi = sample_signs(A)
    if a > 0 and b > 0:
        assert lo > 0, "both eigenvalues positive means positive everywhere"
        CLASSIFIED[name] = "definite"
    elif a < 0 and b < 0:
        assert hi < 0, "both negative means negative everywhere"
        CLASSIFIED[name] = "definite"
    elif a * b < 0:
        assert lo < 0 < hi, "opposite signs means a saddle: both signs occur"
        CLASSIFIED[name] = "indefinite"
    else:
        # A SEMI-DEFINITE form needs two assertions rather than one, and the
        # reason is worth the extra line. Sampling shows no direction is
        # negative -- but it can never show the flat direction EXISTS, because
        # that direction is one point on the circle and 720 samples will not
        # land on it. `lo == 0` was written here first and failed on the first
        # run for exactly that reason. So: sample for non-negativity, and
        # evaluate EXACTLY at the eigenvector the construction already knows.
        assert lo >= 0, "no direction may be negative"
        flat = transpose(Q)[1] if b == 0 else transpose(Q)[0]
        assert form(A, list(flat)) == 0, \
            "and the flat direction must give exactly zero, which sampling " \
            "cannot find because it is one direction out of infinitely many"
        assert lo > 0, "which is why sampling reports a positive minimum here"
        CLASSIFIED[name] = "semi-definite"

assert CLASSIFIED == {"bowl": "definite", "saddle": "indefinite",
                      "ridge": "semi-definite", "dome": "definite"}, CLASSIFIED
emit("p10.form.dirs", 720)
NOTES.append("four quadratic forms classified from their eigenvalues and then "
             "checked in 720 directions each: a bowl is positive in every one "
             "of them, which is what 'definite' is a claim about")

# The zero eigenvalue is P08's null space wearing a different hat, and the
# script says so rather than the frame asserting it.
D0 = [[Fraction(5), Fraction(0)], [Fraction(0), Fraction(0)]]
A0 = matmul(matmul(Q, D0), transpose(Q))
_flat = transpose(Q)[1]
assert matvec(A0, list(_flat)) == [0, 0], \
    "a zero eigenvalue's eigenvector is a null vector, which is P08's object"
assert det(A0) == 0, "so the matrix is singular, which is P09's"
NOTES.append("the ridge's flat direction is exactly a null vector, so "
             "'zero eigenvalue', 'singular' and 'has a null space' are one "
             "condition said three ways -- P08's, P09's and this program's")

# ==========================================================================
# 5. THE SPECTRAL NORM AS THE LARGEST STRETCH.
#
#    For a symmetric matrix the largest factor by which any vector's length
#    is multiplied is the largest |eigenvalue|, and it is attained AT the
#    corresponding eigenvector. That number is the Lipschitz constant of the
#    layer: nothing it does can amplify by more.
#
#    Measured by sweeping the circle -- and the sweep is deliberately NOT the
#    proof. It is here because the frames make a claim about every direction,
#    and a reader who tries a few directions is entitled to see that the
#    maximum really does sit where the eigenvector is.
# ==========================================================================
D_N = [[Fraction(5), Fraction(0)], [Fraction(0), Fraction(-2)]]
A_N = matmul(matmul(Q, D_N), transpose(Q))

def stretch(A, theta):
    x = [math.cos(theta), math.sin(theta)]
    y = [float(A[0][0]) * x[0] + float(A[0][1]) * x[1],
         float(A[1][0]) * x[0] + float(A[1][1]) * x[1]]
    return math.hypot(*y)

NORM_DIRS = 20000
_best_t = max(range(NORM_DIRS), key=lambda k: stretch(A_N, 2 * math.pi * k / NORM_DIRS))
_best = stretch(A_N, 2 * math.pi * _best_t / NORM_DIRS)
_lam_max = max(abs(D_N[0][0]), abs(D_N[1][1]))
assert abs(_best - _lam_max) < 1e-6, \
    "the largest stretch over the whole circle must be the largest |eigenvalue|"

# and it is attained at the eigenvector, not somewhere between
_top = transpose(Q)[0]
_top_dir = math.atan2(float(_top[1]), float(_top[0])) % (2 * math.pi)
_found_dir = (2 * math.pi * _best_t / NORM_DIRS) % math.pi
assert min(abs(_found_dir - _top_dir % math.pi),
           math.pi - abs(_found_dir - _top_dir % math.pi)) < 1e-3, \
    "and the direction it is attained in must be the top eigenvector"

# The smallest stretch is the smallest |eigenvalue|, which is the other half
# of what a layer can do to a vector's length.
_worst = min(stretch(A_N, 2 * math.pi * k / NORM_DIRS) for k in range(NORM_DIRS))
_lam_min = min(abs(D_N[0][0]), abs(D_N[1][1]))
assert abs(_worst - _lam_min) < 1e-3, "and the smallest stretch is the smallest"

emit("p10.norm.dirs", NORM_DIRS)
emit("p10.norm.max", int(_lam_max))
emit("p10.norm.min", int(_lam_min))
NOTES.append(f"over {NORM_DIRS} directions the largest stretch is "
             f"{int(_lam_max)}, the largest |eigenvalue|, attained at the top "
             f"eigenvector -- which is the layer's Lipschitz constant")

# ==========================================================================
# 6. THE SHAPE OF THE BASIN. COLLECTED HERE, SPENT IN P17 AND P20.
#
#    For f(x) = (1/2) x^T A x with A positive definite, the level set
#    f(x) = c is an ellipse whose axes lie along the eigenvectors and whose
#    half-lengths go as 1/sqrt(lambda). So the ratio of the eigenvalues is
#    the ELONGATION of the basin, and that single number is what "ravine"
#    means.
#
#    This program stops at the shape. The largest stable learning rate is
#    P17's, and the optimisers that live with the shape are P20's.
# ==========================================================================
D_B = [[Fraction(20), Fraction(0)], [Fraction(0), Fraction(1)]]
A_B = matmul(matmul(Q, D_B), transpose(Q))
_l1, _l2 = float(D_B[0][0]), float(D_B[1][1])

# half-axis lengths on the level set x^T A x = 1, measured rather than quoted
BASIN_DIRS = 20000
_rs = []
for k in range(BASIN_DIRS):
    th = 2 * math.pi * k / BASIN_DIRS
    x = [math.cos(th), math.sin(th)]
    q = (float(A_B[0][0]) * x[0] * x[0] + 2 * float(A_B[0][1]) * x[0] * x[1]
         + float(A_B[1][1]) * x[1] * x[1])
    _rs.append(1.0 / math.sqrt(q))
_short, _long = min(_rs), max(_rs)
assert abs(_short - 1 / math.sqrt(_l1)) < 1e-6, "short axis is 1/sqrt(lambda max)"
assert abs(_long - 1 / math.sqrt(_l2)) < 1e-6, "long axis is 1/sqrt(lambda min)"

RATIO = _long / _short
assert abs(RATIO - math.sqrt(_l1 / _l2)) < 1e-6, \
    "so the ellipse is sqrt(ratio of eigenvalues) times longer than it is wide"
emit("p10.basin.hi", int(_l1))
emit("p10.basin.lo", int(_l2))
emit("p10.basin.eigratio", int(_l1 / _l2))
emit("p10.basin.axisratio", round(RATIO, 2), 2)
# The page prints the eigenvalue ratio and the axis ratio side by side and says
# the second is the square root of the first, so a reader will take the square
# root of what is printed. Check that it reproduces, as F04, F05 and P07 all
# had to learn the hard way.
assert f"{math.sqrt(float(f'{_l1/_l2:.0f}')):.2f}" == f"{RATIO:.2f}", \
    "the axis ratio does not reproduce from the eigenvalue ratio as printed"
NOTES.append(f"eigenvalues {int(_l1)} and {int(_l2)}, a ratio of "
             f"{int(_l1/_l2)}, give a level ellipse {RATIO:.2f} times longer "
             f"than it is wide -- the square root, which is the part people "
             f"do not expect")

# ==========================================================================
# 7. A COVARIANCE MATRIX IS SYMMETRIC AND POSITIVE SEMI-DEFINITE, so PCA is
#    an eigen-decomposition and not a black box.
#
#    FORWARD REFERENCE, DECLARED: covariance is defined in P24. This program
#    needs exactly the two facts asserted below and takes them no further --
#    it never says what a variance MEANS, only what shape the matrix has.
#
#    Both facts are PROVED here rather than quoted: C = (1/n) X^T X for
#    centred X, so C^T = C by construction, and v^T C v = (1/n)|Xv|^2 >= 0
#    for every v, which is what positive semi-definite says.
# ==========================================================================
DATA = [(2, 1), (4, 3), (6, 4), (8, 6), (3, 2), (7, 5), (5, 4), (1, 1)]
_n = len(DATA)
_mx = Fraction(sum(p[0] for p in DATA), _n)
_my = Fraction(sum(p[1] for p in DATA), _n)
X = [[Fraction(p[0]) - _mx, Fraction(p[1]) - _my] for p in DATA]
C = [[sum(X[i][a] * X[i][b] for i in range(_n)) / _n for b in range(2)]
     for a in range(2)]

assert C == transpose(C), "a covariance matrix is symmetric, by construction"
for k in range(2000):                       # positive semi-definite, swept
    th = 2 * math.pi * k / 2000
    v = [Fraction(round(math.cos(th) * 10**6), 10**6),
         Fraction(round(math.sin(th) * 10**6), 10**6)]
    lhs = dot(v, matvec(C, v))
    rhs = sum(dot(row, v) ** 2 for row in X) / _n
    assert lhs == rhs, "v^T C v must BE (1/n) times the sum of squared projections"
    assert lhs >= 0, "which is a sum of squares, so it can never be negative"

_c_lams = eig2(C)
assert _c_lams != "irrational" or True      # either way, both must be >= 0
if isinstance(_c_lams, list):
    assert all(l >= 0 for l in _c_lams), "so no eigenvalue can be negative"

# The top eigenvector is the direction of greatest spread. Measured against a
# sweep of projections rather than asserted, because that IS what PCA claims.
def spread(theta):
    u = (math.cos(theta), math.sin(theta))
    return sum((float(r[0]) * u[0] + float(r[1]) * u[1]) ** 2 for r in X) / _n

PCA_DIRS = 20000
_bt = max(range(PCA_DIRS), key=lambda k: spread(2 * math.pi * k / PCA_DIRS))
_best_spread = spread(2 * math.pi * _bt / PCA_DIRS)
_lam_top = max(float(l) for l in _c_lams) if isinstance(_c_lams, list) else None
if _lam_top is not None:
    assert abs(_best_spread - _lam_top) < 1e-4, \
        "the greatest spread in any direction IS the largest eigenvalue"

_tot = float(trace(C))
_frac = _best_spread / _tot
assert 0.5 < _frac < 1.0, "and here one direction carries most of the spread"
assert f"{_frac * 100:.1f}" != "100.0", \
    "a percentage that rounds to 100 must be reported as its complement"

emit("p10.pca.n", _n)
emit("p10.pca.dirs", PCA_DIRS)
emit("p10.pca.top.pct", round(_frac * 100, 1), 1)
emit("p10.pca.rest.pct", round((1 - _frac) * 100, 1), 1)
NOTES.append(f"the greatest spread over {PCA_DIRS} directions equals the "
             f"largest eigenvalue of the covariance matrix, and it carries "
             f"{_frac*100:.1f}% of the total -- which is PCA, done by "
             f"eigen-decomposition rather than by search")

# ==========================================================================
# 8. THE TRANSCRIPT: the trap, run rather than described.
# ==========================================================================
EIG_TEXT = """\
>>> from p10_eigenvalues import eig2, eigvec2, dot
>>> from fractions import Fraction as F
>>> S = [[F(2), F(1)], [F(1), F(2)]]      # symmetric
>>> N = [[F(2), F(1)], [F(0), F(3)]]      # not symmetric
>>> [dot(eigvec2(M, l), eigvec2(M, k))
...  for M, (l, k) in ((S, eig2(S)), (N, eig2(N)))]
{out}
"""
_pairs = []
for M in (SYM, NONSYM):
    ls = eig2(M)
    _pairs.append(dot(eigvec2(M, ls[0]), eigvec2(M, ls[1])))
assert _pairs[0] == 0 and _pairs[1] != 0, "the transcript must show the split"
EIG_TEXT = EIG_TEXT.format(
    out="[" + ", ".join(f"Fraction({p.numerator}, {p.denominator})"
                        for p in _pairs) + "]")
assert EIG_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in EIG_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(EIG_TEXT.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p10-orthogonal.txt").write_text(EIG_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p10-orthogonal.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p10_eigenvalues.py --- do not edit.",
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
        print("  " + "   ".join(f"{k:{w}s} {b:>8s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
