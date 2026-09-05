#!/usr/bin/env python3
"""Program P11 --- SVD, low-rank approximation and conditioning.

Every number Program P11 prints that the reader cannot do in their head is
computed here and written to figures/values/p11.tex, which the book \\input{}s.

P11's thesis is that EVERY matrix, square or not, factors into rotate-stretch-
rotate; that truncating the stretch gives the best approximation of a given
rank; and that the ratio of the largest to the smallest stretch is the number
that predicts how much error a solve will amplify.

TWO KINDS OF ARITHMETIC HERE, and the split is deliberate.

  EXACT over Fraction, for everything the mathematics makes exact: the SVD of a
  constructed matrix, sigma_i(A)^2 = lambda_i(A^T A), the Eckart-Young error,
  and kappa(A^T A) = kappa(A)^2. The construction is P10's, one step further:
  pick rational orthogonal U and V from two Pythagorean triples and a rational
  diagonal Sigma, and A = U Sigma V^T is a rational matrix whose singular
  values ARE Sigma's entries. Known by construction rather than found by a
  solver, so "exactly" can be checked with arithmetic that is itself exact.

  FLOATING POINT, for the one claim that is ABOUT floating point: how many
  digits a normal-equations solve loses against a QR solve on the same system.
  That claim would be invisible over the rationals, where both are perfect.
  This is Program P01's and P02's subject arriving as a consequence.

WHAT P11 IS OWED, read out of the files rather than remembered:

  P10  HANDS THIS PROGRAM OVER BY NAME: "every matrix, of any shape, turns out
       to be a rotation, then a stretch along perpendicular axes, then another
       rotation -- so the picture survives even where the theorem does not, and
       the numbers it produces are the ones this program's non-symmetric
       examples had no eigenvalues to give." So P10's THREE FAILURES are this
       program's motivation, and its QDQ^T construction is reused and extended.
  P09  hands over the accuracy half of "do not invert" twice and by name: the
       operation count was measured there, "the accuracy is P11's, and it is
       the half that decides the argument". That debt is paid in section 4.
  P08  names a debt in a WARNING BOX: rank collapse in deep attention stacks
       "needs Program P11's machinery and a real model". This program supplies
       the machinery. It does not have a real model, and says so -- see the
       note under UNMEASURED below.
  P05  gives norms and projection, and least squares onto a subspace.

UNMEASURED, AND SAID SO ON THE PAGE:
  The brief asks for "the singular-value spectrum of a real embedding matrix,
  plotted". That needs a real model, which this book does not have and does not
  download. Constructing a matrix with a plausible spectrum and calling the
  result a measurement would be exactly the fabrication this book's own rules
  forbid -- so the spectrum here is CONSTRUCTED and labelled as such, the
  mechanism is shown on it, and the empirical claim is left open with what
  would settle it, on Program P08's precedent.

Run:  python3 code/p11_svd_conditioning.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p11.tex"
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


# --- the exact machinery P04 wrote and P08, P09 and P10 each reused ---------
def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def matvec(M, v):
    return [sum(r[j] * v[j] for j in range(len(v))) for r in M]


def transpose(M):
    return [list(c) for c in zip(*M)]


def eye(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def frob2(M):
    """Squared Frobenius norm, exactly."""
    return sum(x * x for row in M for x in row)


def sub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


# Two rational rotations, from the 3-4-5 and 5-12-13 triples, so that U and V
# can be DIFFERENT orthogonal matrices -- which is the whole point of the SVD
# against P10's QDQ^T, where they were forced to be the same.
U2 = [[Fraction(3, 5), Fraction(-4, 5)], [Fraction(4, 5), Fraction(3, 5)]]
V2 = [[Fraction(5, 13), Fraction(-12, 13)], [Fraction(12, 13), Fraction(5, 13)]]
assert matmul(transpose(U2), U2) == eye(2), "U must be orthogonal, exactly"
assert matmul(transpose(V2), V2) == eye(2), "V must be orthogonal, exactly"
assert U2 != V2, "and they must differ, or this is P10 again"


# ==========================================================================
# 1. ROTATE, STRETCH, ROTATE -- constructed so the answer is known.
#
#    A = U Sigma V^T with rational orthogonal U and V and rational diagonal
#    Sigma. Then A is rational, its singular values ARE Sigma's entries, and
#    the right and left singular vectors ARE V's and U's columns. Nothing is
#    found by a solver, so every claim below is checked exactly.
# ==========================================================================
SIG = [Fraction(10), Fraction(2)]
SIGMA = [[SIG[0], Fraction(0)], [Fraction(0), SIG[1]]]
A = matmul(matmul(U2, SIGMA), transpose(V2))
assert A != transpose(A), "and A is NOT symmetric, which is the point"

# The defining property, exactly: A sends each right singular vector to sigma
# times the matching left one. That is the whole of the SVD in one line.
for i, v in enumerate(transpose(V2)):
    assert matvec(A, list(v)) == [SIG[i] * x for x in transpose(U2)[i]], \
        "A v_i must be exactly sigma_i u_i"

emit("p11.sig.hi", int(SIG[0]))
emit("p11.sig.lo", int(SIG[1]))
NOTES.append(f"A = U Sigma V^T is rational and NOT symmetric, and A v_i = "
             f"sigma_i u_i exactly for both i -- rotate, stretch, rotate, with "
             f"the answer known by construction")

# ==========================================================================
# 2. SINGULAR VALUES ARE NOT EIGENVALUES, and the catalogue's item 15 is this
#    program's to deliver.
#
#    sigma_i(A)^2 = lambda_i(A^T A), for EVERY matrix including rectangular
#    ones -- and A's own eigenvalues here are a different pair entirely.
# ==========================================================================
ATA = matmul(transpose(A), A)
assert ATA == transpose(ATA), "A^T A is symmetric whatever A was"
# its eigenvalues are sigma^2, exactly, by construction: A^T A = V Sigma^2 V^T
assert ATA == matmul(matmul(V2, [[SIG[0] ** 2, Fraction(0)],
                                 [Fraction(0), SIG[1] ** 2]]),
                     transpose(V2)), \
    "A^T A = V Sigma^2 V^T, so its eigenvalues are the squared singular values"

# A's OWN eigenvalues, from the characteristic polynomial, using P10's route.
_tr = A[0][0] + A[1][1]
_det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
_disc = _tr * _tr - 4 * _det
assert _det == SIG[0] * SIG[1] or _det == -SIG[0] * SIG[1], \
    "det A is plus or minus the product of the singular values"
emit("p11.detA", int(abs(_det)))
# A's OWN eigenvalues are real here, and they are the strongest possible form
# of the trap: NEARLY the singular values, and provably not them. That is why
# the confusion survives -- on a tidy example the two pairs sit close together.
assert _disc > 0, "this example is chosen to have real eigenvalues"
_s = math.sqrt(float(_disc))
_lam = sorted(((float(_tr) + _s) / 2, (float(_tr) - _s) / 2), reverse=True)
for lam, sig in zip(_lam, SIG):
    assert lam != float(sig), "the eigenvalues must NOT be the singular values"
    assert abs(lam - float(sig)) / float(sig) < 0.06, \
        "but they must be close enough that the confusion is understandable"
assert abs(_lam[0] * _lam[1] - float(_det)) < 1e-9, "they multiply to det A"
assert abs(sum(_lam) - float(_tr)) < 1e-9, "and add to the trace"
emit("p11.lam.hi", round(_lam[0], 4), 4)
emit("p11.lam.lo", round(_lam[1], 4), 4)
# The page says the eigenvalues and the singular values differ by UNDER 5%, and
# that is stated as a bound rather than as "a 5% difference" because the two
# pairs give different figures -- 4.67% at the top and 4.90% at the bottom, so
# no single percentage reproduces from both. The bound is asserted on the
# PRINTED forms as well as the exact ones, since a reader divides what is on
# the page.
for _e, _sv in ((_lam[0], SIG[0]), (_lam[1], SIG[1])):
    for _a, _b in ((_e, float(_sv)), (float(f"{_e:.4f}"), float(_sv))):
        assert abs(_a - _b) / _b < 0.05, (
            f"the eigenvalue/singular-value gap reached {abs(_a - _b) / _b:.2%}, "
            "so the page's 'under 5%' no longer holds")

NOTES.append(f"|det A| = {int(abs(_det))} = product of the singular values. "
             f"A's OWN eigenvalues are {_lam[0]:.4f} and {_lam[1]:.4f} against "
             f"singular values {int(SIG[0])} and {int(SIG[1])} -- close enough "
             f"to look the same, provably not the same")

# The rectangular case, where the word "eigenvalue" does not apply at all.
R = [[Fraction(1), Fraction(2), Fraction(3)],
     [Fraction(0), Fraction(1), Fraction(1)]]
RTR = matmul(transpose(R), R)
RRT = matmul(R, transpose(R))
assert len(RTR) == 3 and len(RRT) == 2, "the two Grams have different sizes"
assert RTR == transpose(RTR) and RRT == transpose(RRT), "both are symmetric"
# The non-zero eigenvalues of the two agree, which is why sigma is unambiguous.
_tr2, _det2 = RRT[0][0] + RRT[1][1], RRT[0][0] * RRT[1][1] - RRT[0][1] * RRT[1][0]
assert sum(RTR[i][i] for i in range(3)) == _tr2, \
    "trace(R^T R) = trace(R R^T): the two Grams carry the same total energy"
emit("p11.rect.rows", len(R))
emit("p11.rect.cols", len(R[0]))
emit("p11.rect.energy", int(_tr2))
NOTES.append(f"for a {len(R)} by {len(R[0])} matrix the two Grams are "
             f"{len(RRT)} by {len(RRT)} and {len(RTR)} by {len(RTR)}, and their "
             f"traces agree at {int(_tr2)} -- so a rectangular matrix has "
             f"singular values where it cannot have eigenvalues")


# ==========================================================================
# 3. ECKART-YOUNG: truncating the stretch is the BEST approximation of that
#    rank, and the error it leaves is exactly the next singular value.
#
#    Stated in the book, not proved. Checked here two ways: the error of the
#    truncation is sigma_2 exactly, and a few thousand OTHER rank-1 matrices
#    are all worse -- which is not a proof and is the right shape of evidence
#    for a theorem the book states rather than proves.
# ==========================================================================
def rank1(u, s, v):
    return [[s * u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


A1 = rank1(transpose(U2)[0], SIG[0], transpose(V2)[0])
_err2 = frob2(sub(A, A1))
assert _err2 == SIG[1] ** 2, \
    "the error left by truncating to rank 1 must be exactly sigma_2 squared"
# TWO quantities, and the section's whole difficulty is that they are not the
# same one. frame 13 defines size as a SUM OF SQUARES, so what truncation
# leaves "measured the same way" is sigma_2 SQUARED; its square root is the
# Frobenius norm of the error matrix, and that is the norm Eckart-Young is
# stated in. The page used to print the root under a name that said error and
# a sentence that said "measured the same way", which are different units one
# clause apart. Both are emitted now, under names that say which is which.
emit("p11.ey.err2", int(_err2))          # 4  -- the squared error
emit("p11.ey.err", int(SIG[1]))          # 2  -- its root, the Frobenius norm
assert int(_err2) == int(SIG[1]) ** 2, "the two measures must stay one square apart"

# and nothing else of rank 1 does better. Sweep rank-1 matrices built from
# rational direction pairs; every one must be at least as bad.
EY_TRIALS = 0
_best = _err2
for a in range(-6, 7):
    for b in range(-6, 7):
        if a == 0 and b == 0:
            continue
        for c in range(-6, 7):
            for d in range(-6, 7):
                if c == 0 and d == 0:
                    continue
                u = [Fraction(a), Fraction(b)]
                v = [Fraction(c), Fraction(d)]
                # best scale for this direction pair, exactly: project A onto it
                num = sum(A[i][j] * u[i] * v[j] for i in range(2) for j in range(2))
                den = dot(u, u) * dot(v, v)
                cand = rank1(u, num / den, v)
                e = frob2(sub(A, cand))
                assert e >= _err2, "Eckart-Young: nothing of rank 1 beats the truncation"
                EY_TRIALS += 1
emit("p11.ey.trials", EY_TRIALS)
NOTES.append(f"truncating to rank 1 leaves exactly sigma_2 = {int(SIG[1])}, and "
             f"none of {EY_TRIALS} other rank-1 matrices does better -- evidence "
             f"for a theorem this book states and does not prove")

# ==========================================================================
# 4. THE CONDITION NUMBER, and the debt P09 handed over by name.
#
#    kappa(A) = sigma_max / sigma_min, EXACTLY here. And the fact that makes
#    "do not invert" more than folklore: forming A^T A SQUARES it.
# ==========================================================================
KAPPA = SIG[0] / SIG[1]
assert KAPPA == 5, "the constructed example has a tidy condition number"
# A^T A has singular values sigma^2, so its condition number is kappa^2 --
# exactly, not approximately, and that is the whole argument.
KAPPA_ATA = (SIG[0] ** 2) / (SIG[1] ** 2)
assert KAPPA_ATA == KAPPA ** 2, "kappa(A^T A) = kappa(A)^2, exactly"
emit("p11.kappa", int(KAPPA))
emit("p11.kappa.sq", int(KAPPA_ATA))
NOTES.append(f"kappa(A) = {int(KAPPA)} and kappa(A^T A) = {int(KAPPA_ATA)} = "
             f"kappa(A)^2, exactly -- which is why the normal equations are the "
             f"wrong way to solve a least-squares problem")

# ==========================================================================
# 5. WHAT THAT SQUARING COSTS, MEASURED. This is the debt Program P09 handed
#    over by name -- "the accuracy is P11's, and it is the half that decides
#    the argument" -- and it is the one claim in this program that is ABOUT
#    floating point, so it is the one place floats are used.
#
#    A real least-squares problem: fit a polynomial through points on [0, 1].
#    The exact coefficients are chosen, the right-hand side is built EXACTLY
#    over fractions, and then the same system is solved twice in float64 --
#    once through the normal equations A^T A x = A^T b, once through a
#    Householder QR. The error is measured against the exact answer.
#
#    EVERY NUMBER THIS SECTION EMITS IS A BOUND OR A COUNT, never a measured
#    residual. A residual is a property of the machine -- CI rejected two of
#    P06's for exactly that -- and the invariant here is the GAP between the
#    two methods, not either one's value.
# ==========================================================================
DEG, NPTS = 9, 24
_xs = [Fraction(j, NPTS - 1) for j in range(NPTS)]
_Aex = [[x ** k for k in range(DEG)] for x in _xs]
_xtrue = [Fraction(k + 1) for k in range(DEG)]
_bex = [dot(row, _xtrue) for row in _Aex]

_Af = [[float(v) for v in row] for row in _Aex]
_bf = [float(v) for v in _bex]
_xt = [float(v) for v in _xtrue]


def gauss(M, rhs):
    """Plain Gaussian elimination with partial pivoting, in float."""
    n = len(M)
    aug = [row[:] + [r] for row, r in zip(M, rhs)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(aug[i][k]))
        aug[k], aug[p] = aug[p], aug[k]
        for i in range(k + 1, n):
            f = aug[i][k] / aug[k][k]
            for j in range(k, n + 1):
                aug[i][j] -= f * aug[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / aug[i][i]
    return x


def normal_equations(Af, bf):
    n = len(Af[0])
    ATA = [[sum(Af[r][i] * Af[r][j] for r in range(len(Af))) for j in range(n)]
           for i in range(n)]
    ATb = [sum(Af[r][i] * bf[r] for r in range(len(Af))) for i in range(n)]
    return gauss(ATA, ATb)


def qr_solve(Af, bf):
    """Householder QR applied to [A | b]; A is never squared."""
    m, n = len(Af), len(Af[0])
    R = [row[:] + [bf[i]] for i, row in enumerate(Af)]
    for k in range(n):
        norm = math.sqrt(sum(R[i][k] ** 2 for i in range(k, m)))
        if norm == 0.0:                                      # pragma: no cover
            continue
        alpha = -norm if R[k][k] > 0 else norm
        v = [0.0] * m
        v[k] = R[k][k] - alpha
        for i in range(k + 1, m):
            v[i] = R[i][k]
        vv = sum(x * x for x in v)
        if vv == 0.0:                                        # pragma: no cover
            continue
        for j in range(k, n + 1):
            s = sum(v[i] * R[i][j] for i in range(k, m))
            f = 2.0 * s / vv
            for i in range(k, m):
                R[i][j] -= f * v[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = R[i][n] - sum(R[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / R[i][i]
    return x


def relerr(got, want):
    num = math.sqrt(sum((g - w) ** 2 for g, w in zip(got, want)))
    den = math.sqrt(sum(w * w for w in want))
    return num / den


_e_ne = relerr(normal_equations(_Af, _bf), _xt)
_e_qr = relerr(qr_solve(_Af, _bf), _xt)

# The invariant is the GAP between the two methods, and it is committed as two
# CEILINGS rather than as either measurement. A residual is a property of the
# machine -- CI rejected two of P06's for exactly that -- and what is universal
# here is that the QR solve clears one bound and the normal equations fail the
# other by a wide margin. Measured on this container: about 4e-12 and 1e-05,
# so both bounds below carry more than an order of magnitude of headroom.
QR_CAP, NE_FLOOR = 1e-10, 1e-6
assert _e_qr < QR_CAP, f"the QR solve must clear {QR_CAP}, got {_e_qr:.2e}"
assert _e_ne > NE_FLOOR, f"the normal equations must fail {NE_FLOOR}, got {_e_ne:.2e}"
assert _e_qr < _e_ne, "and the ordering is the point"

# DIGITS is derived from the two COMMITTED bounds, not from the measurement, so
# it cannot drift between machines even by one.
DIGITS = int(round(math.log10(NE_FLOOR / QR_CAP)))
assert DIGITS == 4, "the gap between the committed bounds is four decades"

emit("p11.ls.points", NPTS)
emit("p11.ls.deg", DEG - 1)
emit("p11.ls.qr.bound", f"1e{int(math.log10(QR_CAP))}")
emit("p11.ls.ne.floor", f"1e{int(math.log10(NE_FLOOR))}")
emit("p11.ls.digits", DIGITS)
NOTES.append(f"least squares, degree {DEG-1} through {NPTS} points: the QR "
             f"solve clears 1e{int(math.log10(QR_CAP))} while the normal "
             f"equations fail 1e{int(math.log10(NE_FLOOR))} -- at least "
             f"{DIGITS} decimal digits given away for forming A^T A. Both are "
             f"committed as bounds, because a residual belongs to the machine; "
             f"measured here at {_e_qr:.0e} and {_e_ne:.0e}")

# ==========================================================================
# 6. THE SPECTRUM, AND WHAT THIS BOOK MAY NOT CLAIM ABOUT IT.
#
#    The brief asks for the singular-value spectrum of a REAL embedding
#    matrix, showing how few directions carry the energy. That needs a real
#    model, which this book does not have and does not download.
#
#    So the spectrum below is CONSTRUCTED, and the frames say so in as many
#    words. What it demonstrates is the MECHANISM -- that the energy a rank-r
#    truncation keeps is the sum of the first r squared singular values, so a
#    spectrum that decays fast is what makes a low-rank approximation cheap.
#    Whether a real embedding matrix HAS such a spectrum is an empirical
#    question and is left open, on Program P08's precedent with rank collapse.
# ==========================================================================
SPEC = [Fraction(100), Fraction(40), Fraction(16), Fraction(6),
        Fraction(2), Fraction(1)]
_energy = [s * s for s in SPEC]
_total = sum(_energy)
_kept2 = sum(_energy[:2])
FRAC2 = _kept2 / _total
assert FRAC2 > Fraction(9, 10), "two of six directions carry most of the energy"
assert f"{float(FRAC2)*100:.1f}" != "100.0", \
    "a percentage that rounds to 100 must be reported as its complement"

emit("p11.spec.n", len(SPEC))
emit("p11.spec.keep", 2)
emit("p11.spec.pct", round(float(FRAC2) * 100, 1), 1)
emit("p11.spec.rest.pct", round(100 - float(FRAC2) * 100, 1), 1)
emit("p11.spec.kappa", int(SPEC[0] / SPEC[-1]))
NOTES.append(f"on a CONSTRUCTED spectrum of {len(SPEC)} singular values, the "
             f"top 2 carry {float(FRAC2)*100:.1f}% of the energy -- the "
             f"mechanism, on a matrix chosen to have it. Whether a real "
             f"embedding matrix does is empirical and this book does not "
             f"measure it")

# ==========================================================================
# 7. THE TRANSCRIPT: item 15 of the trap catalogue, run rather than described.
# ==========================================================================
SVD_TEXT = """\
>>> from p11_svd_conditioning import A, ATA, SIG
>>> [s * s for s in SIG]        # the squared singular values
{sq}
>>> tr = ATA[0][0] + ATA[1][1]  # and A^T A's eigenvalues:
>>> dt = ATA[0][0]*ATA[1][1] - ATA[0][1]*ATA[1][0]
>>> tr, dt                      # they sum and multiply to these
{td}
"""
_sq = [s * s for s in SIG]
_tr = ATA[0][0] + ATA[1][1]
_dt = ATA[0][0] * ATA[1][1] - ATA[0][1] * ATA[1][0]
assert _tr == sum(_sq) and _dt == _sq[0] * _sq[1], \
    "trace and determinant of A^T A must be the sum and product of sigma^2"
SVD_TEXT = SVD_TEXT.format(
    sq="[" + ", ".join(f"Fraction({s.numerator}, {s.denominator})" for s in _sq) + "]",
    td=f"(Fraction({_tr.numerator}, {_tr.denominator}), "
       f"Fraction({_dt.numerator}, {_dt.denominator}))")
assert SVD_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in SVD_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(SVD_TEXT.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p11-singular-vs-eigen.txt").write_text(SVD_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p11-singular-vs-eigen.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p11_svd_conditioning.py --- do not edit.",
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
        print("  " + "   ".join(f"{k:{w}s} {b:>10s}" for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
