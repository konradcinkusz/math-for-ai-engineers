#!/usr/bin/env python3
"""Program P18 --- Matrix calculus.

Every number Program P18 prints that the reader cannot do in their head is
computed here and written to figures/values/p18.tex, which the book \\input{}s.

P18's thesis is that DIFFERENTIATING WITH RESPECT TO A VECTOR OR A MATRIX IS
BOOKKEEPING PLUS A LAYOUT CONVENTION, and that most of the pain in the
literature is the convention rather than the mathematics. Nothing new is
defined: Program P15 gave the gradient, Program P16 gave the Jacobian and its
shape, and this program only says how to arrange them and then derives the
identities once each.

WHAT P18 IS OWED, read out of the files rather than remembered:

  P16  owns the SHAPE rule -- one row per output, one column per input -- and
       "nobody forms a Jacobian", and the finite-difference check at h = 1e-5.
       Its own header names matrix calculus and the softmax-cross-entropy
       gradient as this program's. Every identity here is checked by P16's
       method, at P16's step.
  F07  owns softmax as exponentials over their sum AND the two-score identity
       softmax(a, b) = sigma(a - b). Differentiating an identity gives an
       identity, so the softmax Jacobian at n = 2 must be sigma'(a - b) --
       gated, because the two programs are quoting one computation.
  P06  owns the matrix as a function and the cost of bracketing, and already
       notes that frameworks stack a batch on the first axis and compute XW^T.
  P15  owns the gradient; P17 owns the Hessian. Both derivative objects exist
       already, so this program defines no new one.

WHAT P18 LEAVES ALONE, checked against tools/programs.json:
    convexity and what one basin promises                        -> P19
    the optimisers                                               -> P20
    minibatch noise                                              -> P21
    cross-entropy JUSTIFIED, and KL                              -> P30
    maximum likelihood, of which the loss is a case               -> P26

THE FORWARD REFERENCE IS DECLARED, not discovered. Cross-entropy is not
defined until P30 and this program carries the derivation that uses it most,
so P18 gives it a definitional frame -- minus the sum of y log p, stated as a
definition to be justified later -- and says so in its Learning outcomes.

THE HEADLINE IS FUSION, AND IT HAS TWO INDEPENDENT REASONS. The gradient of
cross-entropy through a softmax is p - y. Against the two-step route (form
dL/dp = -y/p, then apply the softmax Jacobian) that is a factor of 50 001 in
operations at a realistic vocabulary -- and, which matters more, it is DEFINED
where the two-step route divides by zero, because a probability underflows and
p - y never forms the reciprocal. The first is a cost argument; the second is
P02's "safe for inputs you have not tried".

Run:  python3 code/p18_matrix_calculus.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p18.tex"
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


def bound(x: float) -> str:
    """A residual is a property of the machine, so commit a CEILING it clears
    on any of them. CI rejected two of P06's for being figures instead."""
    assert x >= 0.0
    return "0" if x == 0.0 else f"1e{math.ceil(math.log10(x)):d}"


def sci(x: float, d: int = 2) -> str:
    return f"{x:.{d}e}"


# ---------------------------------------------------------------------------
# Small dense-linear-algebra helpers. No numpy: `make numbers` must run on a
# plain python3, and every one of these is three lines.
# ---------------------------------------------------------------------------
def mv(W, x):
    return [sum(W[i][j] * x[j] for j in range(len(x))) for i in range(len(W))]


def softmax(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


# P16's method, at P16's step: the bottom of the U-curve F11 measured, which
# is where a finite difference is an excellent CHECK and a bad definition.
H = 1e-5

# ONE ceiling for all five identities, and it comes from the method rather
# than from taste. A central difference at this step carries an h^2 term and a
# rounding term, and for the layer-norm gradient -- which divides by a standard
# deviation and so has a large third derivative -- that floor is measured at
# 1.7e-08. The first draft asserted 1e-08 and the layer norm refused it, which
# was the threshold being chosen to make a check pass rather than derived, the
# failure mode Program F11 paid for. A shared 1e-06 sits an order above every
# one of the five measured gaps and orders BELOW any real error: a dropped term
# or a wrong sign disagrees by O(1), not by a decimal place. The per-identity
# bounds are committed separately, and each is the measurement rounded up.
CHECK_CEILING = 1e-6


def cdiff(f, x, i):
    a, b = list(x), list(x)
    a[i] += H
    b[i] -= H
    return (f(a) - f(b)) / (2 * H)


def worst(u, v):
    return max(abs(a - b) for a, b in zip(u, v))


random.seed(18)
N_OUT, N_IN = 4, 3
W = [[random.uniform(-1, 1) for _ in range(N_IN)] for _ in range(N_OUT)]
X = [random.uniform(-1, 1) for _ in range(N_IN)]
T = [random.uniform(-1, 1) for _ in range(N_OUT)]
TRUE = 2                                    # the true class, for cross-entropy

emit("p18.n.out", N_OUT)
emit("p18.n.in", N_IN)


def flat(M):
    return [v for row in M for v in row]


def unflat(v):
    return [v[i * N_IN:(i + 1) * N_IN] for i in range(N_OUT)]


# ---------------------------------------------------------------------------
# 1. THE LAYOUT, and it is the whole of what is new.
#
# In numerator layout d(Wx)/dx IS W: one row per output, one column per input,
# which is P16's shape rule read off a linear map. Denominator layout is its
# transpose and nothing else, so the two differ by exactly one transpose and
# neither is more correct. What is wrong is mixing them inside one derivation.
# ---------------------------------------------------------------------------
jac_num = [[cdiff(lambda v, i=i: mv(W, v)[i], X, j) for j in range(N_IN)]
           for i in range(N_OUT)]
gap_layout = max(abs(jac_num[i][j] - W[i][j])
                 for i in range(N_OUT) for j in range(N_IN))
assert gap_layout < CHECK_CEILING, gap_layout
emit("p18.layout.bound", bound(gap_layout))
NOTES.append("d(Wx)/dx in numerator layout is W itself, to better than "
             f"{bound(gap_layout)}")

# The two shapes are the point -- a transpose, and nothing else -- and the
# page builds them from n.out and n.in rather than being handed a third value
# to trust. That is F10's finding: a shape is arithmetic the reader does.


# ---------------------------------------------------------------------------
# 2. WITH RESPECT TO A MATRIX, and the rule that makes it checkable.
#
# THE ANSWER TO THIS PROGRAM'S TRAP -- "some shape or other; I'll transpose
# until it runs" -- is that the gradient of a SCALAR has the same shape as the
# thing it is taken with respect to. Every identity below is asserted to have
# that shape as well as the right entries, because the shape is what the
# reader is being taught to use as a check.
# ---------------------------------------------------------------------------
def sq_loss(wf):
    r = [a - b for a, b in zip(mv(unflat(wf), X), T)]
    return sum(v * v for v in r)


resid = [a - b for a, b in zip(mv(W, X), T)]
sq_analytic = [[2 * resid[i] * X[j] for j in range(N_IN)] for i in range(N_OUT)]
sq_numeric = [cdiff(sq_loss, flat(W), k) for k in range(N_OUT * N_IN)]
gap_sq = worst(sq_numeric, flat(sq_analytic))
assert gap_sq < CHECK_CEILING, gap_sq
# the shape claim, asserted rather than asserted-in-prose
assert len(sq_analytic) == len(W) and len(sq_analytic[0]) == len(W[0])
emit("p18.sq.bound", bound(gap_sq))


# ---------------------------------------------------------------------------
# 3. THE SOFTMAX JACOBIAN, and the gate that ties it to Program F07.
#
# diag(p) - p p^T. It is square and symmetric, its rows sum to zero -- which
# is the derivative form of "the probabilities sum to one" -- and at n = 2 it
# must reduce to sigma'(a - b), because F07 PROVED softmax(a, b) = sigma(a-b)
# and differentiating an identity gives an identity. That is a shared
# computation rather than a resemblance, which is P04's rule for a gate.
# ---------------------------------------------------------------------------
def softmax_jac(z):
    p = softmax(z)
    n = len(p)
    return [[p[i] * ((i == j) - p[j]) for j in range(n)] for i in range(n)]


Z = mv(W, X)
J = softmax_jac(Z)
J_num = [[cdiff(lambda v, i=i: softmax(v)[i], Z, j) for j in range(N_OUT)]
         for i in range(N_OUT)]
gap_jac = max(abs(J[i][j] - J_num[i][j])
              for i in range(N_OUT) for j in range(N_OUT))
assert gap_jac < CHECK_CEILING, gap_jac
emit("p18.jac.bound", bound(gap_jac))

# COLUMNS sum to zero, and that is the one the sum-to-one argument gives.
# d(sum_i p_i)/dz_j is the sum DOWN column j, so "the probabilities sum to one
# whatever the scores are" forces the column sums, not the row sums. The rows
# sum to zero as well, for a different reason -- softmax is unchanged by adding
# a constant to every score, so J times the all-ones vector is zero -- and the
# two coincide only because J is symmetric, which is asserted immediately
# below. The frame used to give the row sums the column argument, in the one
# program whose whole subject is which index runs down the rows.
col_gap = max(abs(sum(J[i][j] for i in range(N_OUT))) for j in range(N_OUT))
assert col_gap < 1e-15, col_gap
emit("p18.jac.colsum", bound(col_gap))

row_gap = max(abs(sum(row)) for row in J)
assert row_gap < 1e-15, row_gap
emit("p18.jac.rowsum", bound(row_gap))

# Symmetric, because p_i (delta_ij - p_j) is symmetric in i and j off the
# diagonal. Worth asserting because the reader is about to be asked for it.
sym_gap = max(abs(J[i][j] - J[j][i])
              for i in range(N_OUT) for j in range(N_OUT))
assert sym_gap < 1e-18, sym_gap

# THE GATE. F07 committed the two-score softmax; its Jacobian must be
# sigma'(a - b) over a whole grid, not at one point.
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


GRID = [v / 4 for v in range(-24, 25)]
gate = 0.0
for a in GRID:
    for b in GRID:
        j2 = softmax_jac([a, b])
        s = sigmoid(a - b)
        gate = max(gate, abs(j2[0][0] - s * (1 - s)), abs(j2[0][1] + s * (1 - s)))
assert gate < 1e-12, gate
emit("p18.gate.f07.bound", bound(gate))
emit("p18.gate.f07.pairs", len(GRID) ** 2)
# F07's own committed pair must still be what this program's softmax returns,
# or the two programs are quoting different computations.
_f07a = committed("f07.tex", "f07.softmax2.a")
if _f07a is not None:
    assert abs(softmax([2.0, 0.5])[0] - float(_f07a)) < 5e-4, _f07a
NOTES.append(f"softmax Jacobian at n=2 equals sigma'(a-b) over "
             f"{len(GRID) ** 2} pairs, F07's identity differentiated")


# ---------------------------------------------------------------------------
# 4. THE HEADLINE. Cross-entropy through a softmax is p - y.
#
# Derived, then checked against a central difference, then checked again one
# layer further back -- dL/dW = (p - y) x^T -- because that is the form a
# reader writes in a training loop.
# ---------------------------------------------------------------------------
def ce_of_logits(z):
    return -math.log(softmax(z)[TRUE])


P = softmax(Z)
ce_analytic = [P[i] - (1.0 if i == TRUE else 0.0) for i in range(N_OUT)]
ce_numeric = [cdiff(ce_of_logits, Z, i) for i in range(N_OUT)]
gap_ce = worst(ce_numeric, ce_analytic)
assert gap_ce < CHECK_CEILING, gap_ce
emit("p18.ce.bound", bound(gap_ce))

# the same loss one layer back, wrt W
def ce_of_W(wf):
    return -math.log(softmax(mv(unflat(wf), X))[TRUE])


ceW_analytic = [[ce_analytic[i] * X[j] for j in range(N_IN)]
                for i in range(N_OUT)]
ceW_numeric = [cdiff(ce_of_W, flat(W), k) for k in range(N_OUT * N_IN)]
gap_ceW = worst(ceW_numeric, flat(ceW_analytic))
assert gap_ceW < CHECK_CEILING, gap_ceW
assert len(ceW_analytic) == len(W) and len(ceW_analytic[0]) == len(W[0])
emit("p18.cew.bound", bound(gap_ceW))

# Layer normalisation, the fifth identity the brief names. Its gradient is
# the one people get wrong, because two correction terms come from the mean
# and the variance both depending on every input.
LN_EPS = 1e-5


def layer_norm(v):
    mu = sum(v) / len(v)
    var = sum((a - mu) ** 2 for a in v) / len(v)
    s = math.sqrt(var + LN_EPS)
    return [(a - mu) / s for a in v], s


def ln_scalar(v):
    zh, _ = layer_norm(v)
    return sum(a * b for a, b in zip(zh, T))


zhat, sigma_ln = layer_norm(Z)
mean_t = sum(T) / N_OUT
mean_tz = sum(a * b for a, b in zip(T, zhat)) / N_OUT
ln_analytic = [(T[i] - mean_t - zhat[i] * mean_tz) / sigma_ln
               for i in range(N_OUT)]
ln_numeric = [cdiff(ln_scalar, Z, i) for i in range(N_OUT)]
gap_ln = worst(ln_numeric, ln_analytic)
assert gap_ln < CHECK_CEILING, gap_ln
emit("p18.ln.bound", bound(gap_ln))
emit("p18.check.ceiling", bound(CHECK_CEILING))
NOTES.append("all five identities agree with a central difference at "
             f"h = {H:g}, each within its committed bound")


# ---------------------------------------------------------------------------
# 5. WHY THEY ARE FUSED, and the two reasons are different in kind.
#
# COST: the two-step route forms and applies an n x n Jacobian; p - y is n
# subtractions and no multiplication at all.
# DEFINEDNESS: the two-step route forms dL/dp = -y/p, and a probability
# underflows to exactly zero. p - y never forms the reciprocal. That is P02's
# sense of "numerically stable" -- safe for inputs you have not tried -- and
# it is the reason that survives, because the cost one is only about speed.
# ---------------------------------------------------------------------------
VOCAB = 50_000
ops_two_step = VOCAB * VOCAB + VOCAB
ops_fused = VOCAB
emit("p18.vocab", VOCAB)
# FIVE DIGITS, NOT TWO, because the page prints this beside the ratio and a
# reader divides them. At "2.5e+09" against 50000 the quotient is 50000, and
# the page said 50001 -- the reproduce-from-the-printed-operands defect F04,
# F05, P07, P12, P23 and P27 have each paid for. The count is n^2 + n, so the
# +1 in the ratio is real and it is the operand that has to carry it.
emit("p18.fuse.twostep", sci(float(ops_two_step), 5))
emit("p18.fuse.fused", VOCAB)
assert ops_two_step % ops_fused == 0
emit("p18.fuse.ratio", ops_two_step // ops_fused)
_printed = float(f"{float(ops_two_step):.5e}") / float(VOCAB)
assert round(_printed) == ops_two_step // ops_fused, _printed

# GB, NOT GiB, and the distinction is this book's own. VOCAB^2 * 2 is exactly
# 5.0e9 bytes, which is 5 GB and 4.66 GiB; the old key computed GiB correctly
# and then rounded it to 5, so the page printed the GiB label over what a
# reader computes as the GB figure. That is precisely the confusion P03's
# summary warns about, and P32 had to rename a MiB key for the same reason.
_bytes = VOCAB * VOCAB * 2
emit("p18.fuse.gb", round(_bytes / 10 ** 9))
assert abs(_bytes / 1024 ** 3 - 4.66) < 0.01           # 4.66 GiB, not 5
assert _bytes == 5 * 10 ** 9                           # exactly 5 GB
assert ops_two_step / ops_fused > VOCAB, "the ratio is at least the vocabulary"


def two_step_grad(z, y):
    """The route a reader writes when they follow the chain rule literally."""
    p = softmax(z)
    dp = [-(1.0 if i == y else 0.0) / p[i] for i in range(len(p))]   # -y / p
    jac = softmax_jac(z)
    return [sum(dp[k] * jac[k][j] for k in range(len(p))) for j in range(len(p))]


def fused_grad(z, y):
    p = softmax(z)
    return [p[i] - (1.0 if i == y else 0.0) for i in range(len(p))]


# At ordinary logits the two agree to rounding, so this is NOT a claim that
# the fused one is more accurate.
ORD = [2.0, 0.5, -1.0, 0.25]
gap_ord = worst(fused_grad(ORD, TRUE), two_step_grad(ORD, TRUE))
assert gap_ord < 1e-14, gap_ord
emit("p18.agree.bound", bound(gap_ord))

# And then the row that is not ordinary: the model puts essentially no mass on
# the right answer, which is the row a training run meets early and often.
# Three classes rather than four, so that the gradient the fused route returns
# is a number the reader can read off the page: two thirds is not wrong, but
# a half is what makes "an ordinary, maximally informative gradient" land.
BAD, BAD_TRUE = [0.0, 0.0, -800.0], 2
fused_bad = fused_grad(BAD, BAD_TRUE)
try:
    two_step_grad(BAD, BAD_TRUE)
    raise AssertionError("expected the two-step route to divide by zero")
except ZeroDivisionError:
    pass
assert softmax(BAD)[BAD_TRUE] == 0.0                   # underflowed, exactly
assert abs(fused_bad[BAD_TRUE] + 1.0) < 1e-12          # a perfectly good -1
emit("p18.bad.logit", round(BAD[BAD_TRUE]))

# WHERE the cliff is: exp underflows below about -745, which is Program P01's
# floor arriving in the book's most reused derivation. Found rather than
# quoted, so that changing the format changes the number on the page.
lo, hi = -800.0, 0.0
for _ in range(200):
    mid = (lo + hi) / 2
    if softmax([0.0, 0.0, mid])[BAD_TRUE] == 0.0:
        lo = mid
    else:
        hi = mid
emit("p18.cliff", round(hi))
assert -760 < hi < -700, hi

# AND WHERE exp ITSELF UNDERFLOWS, which is a DIFFERENT number and about one
# unit lower. The bisection above finds where the softmax PROBABILITY rounds to
# zero; between the two, exp is still returning a subnormal and it is the
# division by the sum of the exponentials that finishes it off. The frame used
# to say the exponential was zero at the first threshold, which is false over
# the whole band between them -- and a reader who checks in a REPL, the reader
# Program P01 trains them to be, finds it wrong.
elo, ehi = -800.0, 0.0
for _ in range(200):
    emid = (elo + ehi) / 2
    if math.exp(emid) == 0.0:
        elo = emid
    else:
        ehi = emid
emit("p18.cliff.exp", round(ehi))
assert ehi < hi, (ehi, hi)             # exp survives lower than the ratio does
assert math.exp(hi) > 0.0              # subnormal at the probability's cliff
NOTES.append(f"the two-step gradient divides by zero once a logit falls about "
             f"{abs(round(hi))} below the largest; the fused one returns "
             f"{fused_bad[BAD_TRUE]:.0f}. exp itself survives to "
             f"{round(ehi)}, so the band between them is the division "
             "rounding a subnormal to zero")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    # Self-contained on purpose: P04 shipped a transcript naming a function it
    # never imported, so this one imports what it calls.
    lines = [
        ">>> from p18_matrix_calculus import softmax, fused_grad",
        ">>> from p18_matrix_calculus import two_step_grad",
        f">>> z, true = {BAD}, {BAD_TRUE}",
        ">>> softmax(z)[true]",
        f"{softmax(BAD)[BAD_TRUE]!r}",
        ">>> fused_grad(z, true)",
        f"{fused_grad(BAD, BAD_TRUE)!r}",
        ">>> two_step_grad(z, true)",
        "Traceback (most recent call last):",
        "  ...",
        "ZeroDivisionError: float division by zero",
    ]
    for line in lines:
        assert len(line) <= 64, (len(line), line)
    (TRANSCRIPTS / "p18-fused-or-not.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    out = [
        "% Generated by code/p18_matrix_calculus.py --- do not edit.",
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
        print("  " + "   ".join(f"{k:{w}s} {b:>12s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
