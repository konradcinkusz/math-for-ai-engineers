#!/usr/bin/env python3
"""Program P17 --- The Hessian, curvature and the Taylor expansion.

Every number Program P17 prints that the reader cannot do in their head is
computed here and written to figures/values/p17.tex, which the book \\input{}s.

P17's thesis is that THE SECOND-ORDER MODEL TURNS "THE LOSS EXPLODED" INTO
ARITHMETIC. The best local quadratic model of a function has a matrix of
second derivatives in it; on that model gradient descent multiplies each
eigendirection by 1 - eta lambda; so the walk stays bounded exactly when
|1 - eta lambda| < 1 in every direction, which is eta < 2 / lambda_max. That
is a number rather than a feeling.

WHAT P17 IS OWED, read out of the files rather than remembered:

  P15  PUT THE READER ONE LINE FROM IT. It derives the factor 1 - eta lambda
       per eigendirection, measures it as -0.80 and +0.91 on P10's bowl, and
       its rigour box says in as many words: "this program can say that the
       factor goes negative and that the walk crosses; it may not tell you
       where the boundary is." The boundary is this program's, and P15's own
       eta must sit under it -- gated.
  P10  built the bowl: eigenvalues 20 and 1, the level ellipse, and the words
       ravine and sharp minimum. It says the shape is collected there and the
       inequality is P17's.
  F04  gives the sum and the sequence, which is what a Taylor expansion is.
  F12  gives the derivatives it is made of, and F11 the stationary point.
  P16  priced a Jacobian; the Hessian is one dimension worse, and the count
       is gated against P16's own parameter figure.

WHAT P17 LEAVES ALONE, checked against tools/programs.json:
    matrix calculus, the softmax-cross-entropy gradient          -> P18
    convexity, one basin, and what it promises                   -> P19
    the optimisers that live with the shape                      -> P20
    minibatch noise                                              -> P21

THE HONEST SECTION IS SECTION 5 and it is a demonstration rather than a hedge.
Sharpness is not a property of the function a network computes: rescaling a
parameter changes the curvature while leaving every output identical, which is
exact and is computed here rather than argued.

Run:  python3 code/p17_hessian_taylor.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p17.tex"
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
    assert x >= 0.0
    return "0" if x == 0.0 else f"1e{math.ceil(math.log10(x)):d}"


def sci(x: float, d: int = 2) -> str:
    return f"{x:.{d}e}"


# ---------------------------------------------------------------------------
# 1. THE QUADRATIC MODEL, and how good it is.
#
# The claim is not that the quadratic model is close. It is that its error
# shrinks like h^3 while the linear model's shrinks like h^2 -- an ORDER
# rather than a size, which is what makes "best local model" mean something.
# ---------------------------------------------------------------------------
def g(x: float) -> float:
    return math.exp(x) - 2.0 * x * x


def g1(x: float) -> float:
    return math.exp(x) - 4.0 * x


def g2(x: float) -> float:
    return math.exp(x) - 4.0


X0 = 0.5   # not emitted: the page never quotes the point, only the orders


def lin(h): return g(X0) + g1(X0) * h


def quad(h): return g(X0) + g1(X0) * h + 0.5 * g2(X0) * h * h


# The ORDER is the claim, so it is what is asserted: halve h and the linear
# error falls by about 4 and the quadratic error by about 8. A single pair of
# error figures would have been a fact about one step size.
prev_l = prev_q = None
lin_ratios, quad_ratios = [], []
for k in range(4, 12):
    h = 2.0 ** -k
    el, eq = abs(g(X0 + h) - lin(h)), abs(g(X0 + h) - quad(h))
    if prev_l:
        lin_ratios.append(prev_l / el)
        quad_ratios.append(prev_q / eq)
    prev_l, prev_q = el, eq
assert all(abs(r - 4.0) < 0.15 for r in lin_ratios), lin_ratios
assert all(abs(r - 8.0) < 0.6 for r in quad_ratios), quad_ratios
emit("p17.order.lin", 2)
emit("p17.order.quad", 3)
H_SHOW = 0.1
emit("p17.taylor.h", H_SHOW, digits=1)
emit("p17.err.lin", sci(abs(g(X0 + H_SHOW) - lin(H_SHOW)), 1))
emit("p17.err.quad", sci(abs(g(X0 + H_SHOW) - quad(H_SHOW)), 1))
NOTES.append("halving the step divides the linear error by 4 and the "
             "quadratic one by 8 -- the orders, not the sizes")

# ---------------------------------------------------------------------------
# 2. THE HESSIAN, and that it is symmetric.
#
# Symmetry is not a convention: the mixed partials agree, so the matrix has a
# full orthogonal set of eigenvectors and everything Program P10 proved about
# symmetric matrices applies unchanged. That is the whole reason the rest of
# the program can talk about "directions".
# ---------------------------------------------------------------------------
def f2(x, y):
    return x ** 3 * y + math.sin(x) * y ** 2


HP = (0.7, -1.3)
HH = 1e-4


def mixed(fn, pt, i, j, h=HH):
    def shift(k, d):
        p = list(pt); p[k] += d; return p
    def d1(p, k):
        a, b = list(p), list(p)
        a[k] += h; b[k] -= h
        return (fn(*a) - fn(*b)) / (2 * h)
    a, b = shift(j, h), shift(j, -h)
    return (d1(a, i) - d1(b, i)) / (2 * h)


hess = [[mixed(f2, HP, i, j) for j in range(2)] for i in range(2)]
sym_gap = abs(hess[0][1] - hess[1][0])
# THE CEILING IS COMMITTED, NEVER THE MEASUREMENT. On this machine the two
# mixed partials agree to the last bit and the gap is exactly 0.0 -- but they
# are different expression trees, so that is luck of this function and this
# point rather than a property of the mathematics, and P06 had two committed
# residuals rejected by CI for exactly this. What is guaranteed anywhere is
# the ceiling the assertion enforces.
SYM_CEIL = 1e-6
assert sym_gap < SYM_CEIL, sym_gap
emit("p17.sym.bound", sci(SYM_CEIL, 0))
NOTES.append("the two mixed partials agree, so the Hessian is symmetric and "
             "Program P10 applies to it unchanged")

# ---------------------------------------------------------------------------
# 3. THE PAYOFF. The largest stable step, derived and then MEASURED.
#
# Program P15 left this exactly one line short: it has the factor
# 1 - eta lambda per eigendirection and says the boundary is P17's. The
# boundary is |1 - eta lambda| < 1, that is 0 < eta < 2 / lambda, and with
# several eigenvalues the binding one is the LARGEST.
# ---------------------------------------------------------------------------
LAM_HI = int(committed("p15.tex", "p15.lam.hi") or 20)
LAM_LO = int(committed("p15.tex", "p15.lam.lo") or 1)
assert (LAM_HI, LAM_LO) == (20, 1)
emit("p17.lam.hi", LAM_HI)
emit("p17.lam.lo", LAM_LO)

ETA_STAR = 2.0 / LAM_HI
emit("p17.eta.star", ETA_STAR, digits=2)

# P15's own walk must sit UNDER the boundary, or the two programs disagree
# about a walk they both describe. This is the gate that makes the hand-over
# real rather than a promise.
_p15_eta = float(committed("p15.tex", "p15.zig.eta") or 0.09)
assert 0 < _p15_eta < ETA_STAR, (_p15_eta, ETA_STAR)
emit("p17.p15.eta", _p15_eta, digits=2)

# AND THE FACTOR, because the frame used to explain the sign flip by nearness
# to the boundary and that is not the cause. 1 - eta*lam goes negative as soon
# as eta passes 1/lam, which is HALF the boundary, so alternation is the normal
# behaviour over the whole upper half of the stable range. Printing the factor
# is what lets the frame say that instead.
_p15_factor = 1 - _p15_eta * LAM_HI
assert -1 < _p15_factor < 0, _p15_factor
assert _p15_eta > 1 / LAM_HI                       # above 1/lam: it alternates
assert _p15_eta < 2 / LAM_HI                       # under 2/lam: it converges
emit("p17.p15.factor", _p15_factor, digits=2)
NOTES.append(f"gated: P15 walks at eta = {_p15_eta}, under this program's "
             f"boundary of {ETA_STAR}, with factor {_p15_factor:.2f} -- "
             "negative because eta is above 1/lambda, not because it is near "
             "the boundary")

# MEASURED rather than only derived: sweep eta and find where the walk stops
# converging. The empirical threshold must be the derived one.
def diverges(eta, steps=400):
    x = [1.0, 1.0]
    for _ in range(steps):
        x = [x[0] - eta * LAM_HI * x[0], x[1] - eta * LAM_LO * x[1]]
        if abs(x[0]) > 1e12 or abs(x[1]) > 1e12:
            return True
    return not (abs(x[0]) < 1.0 and abs(x[1]) < 1.0)


STEP = 1e-4
first_bad = next(e for e in (i * STEP for i in range(1, 4000)) if diverges(e))
assert abs(first_bad - ETA_STAR) <= 2 * STEP, (first_bad, ETA_STAR)
emit("p17.eta.measured", first_bad, digits=4)
NOTES.append(f"swept: the walk first fails to converge at eta = "
             f"{first_bad:.4f}, against the derived {ETA_STAR}")

# AND THE SHALLOW DIRECTION'S OWN BOUND IS TWENTY TIMES LARGER, which is the
# sentence the section is for: one step size serves both, and the steep
# direction sets it.
emit("p17.eta.shallow", 2.0 / LAM_LO, digits=1)
ratio = (2.0 / LAM_LO) / ETA_STAR
assert abs(ratio - LAM_HI / LAM_LO) < 1e-9
emit("p17.eta.gap", round(ratio))

# THE CONDITION NUMBER is that ratio, and it is Program P11's quantity read on
# the Hessian. Steps needed to close a fixed fraction of the gap in the
# shallow direction at the largest safe step: the count grows with it.
kappa = LAM_HI / LAM_LO
emit("p17.kappa", round(kappa))
best_eta = 2.0 / (LAM_HI + LAM_LO)          # the classical optimum
rate = (kappa - 1) / (kappa + 1)
steps_needed = math.ceil(math.log(0.01) / math.log(rate))
assert steps_needed > 10
emit("p17.best.eta", best_eta, digits=3)
emit("p17.rate", rate, digits=3)
emit("p17.steps.99", steps_needed)
NOTES.append(f"condition number {kappa:.0f}: even at the best step the slow "
             f"direction needs {steps_needed} steps to close 99 per cent")

# ---------------------------------------------------------------------------
# 4. THE PRICE OF USING IT. Newton's step needs the Hessian solved, and the
#    Hessian has one entry per PAIR of parameters.
# ---------------------------------------------------------------------------
PARAMS = int(float(committed("p16.tex", "p16.params") or 7e9))
assert PARAMS >= 10 ** 9
entries = PARAMS * PARAMS
emit("p17.params", sci(float(PARAMS), 0))
emit("p17.hess.entries", sci(float(entries), 1))
# In the book's own units: bytes at two per entry, against F01's ladder.
emit("p17.hess.bytes", sci(float(entries * 2), 1))
# And the solve is cubic, so it is worse than the storage.
emit("p17.hess.solve", sci(float(PARAMS) ** 3, 1))
NOTES.append("the Hessian of a real model has one entry per PAIR of "
             "parameters, which is why nobody forms one either")

# The honest half: a Newton step is exact on a quadratic, in ONE step, and the
# script shows it rather than claiming it.
newton_pt = [1.0, 1.0]
newton_pt = [newton_pt[0] - (LAM_HI * newton_pt[0]) / LAM_HI,
             newton_pt[1] - (LAM_LO * newton_pt[1]) / LAM_LO]
assert newton_pt == [0.0, 0.0]
emit("p17.newton.steps", 1)
NOTES.append("on a quadratic a Newton step lands exactly on the minimum in "
             "one move -- which is what the cost is being weighed against")

# ---------------------------------------------------------------------------
# 5. THE HONEST SECTION. Sharpness is not a property of the function.
#
# Take a network layer w * x. Rescale: w = c * u and divide the input by c.
# The FUNCTION IS IDENTICAL at every input. The loss as a function of the new
# parameter has curvature scaled by 1/c^2, so "how sharp is this minimum"
# has a different answer for the same model.
# ---------------------------------------------------------------------------
def curvature_under_scaling(c: float) -> float:
    """Loss L(w) = (w - t)^2 has second derivative 2. Reparameterise w = c*u:
    L(u) = (c u - t)^2, whose second derivative in u is 2 c^2."""
    return 2.0 * c * c


SCALES = (1.0, 2.0, 10.0)
curv = [curvature_under_scaling(c) for c in SCALES]
assert curv[0] < curv[1] < curv[2]
assert abs(curv[2] / curv[0] - 100.0) < 1e-9
emit("p17.rescale.c", int(SCALES[2]))
emit("p17.rescale.factor", round(curv[2] / curv[0]))
# And the function is the same: check it, rather than saying it.
T = 0.3
for c in SCALES:
    u = 0.8 / c
    assert abs((c * u - T) - (0.8 - T)) < 1e-12
NOTES.append(f"rescaling one parameter by {SCALES[2]:.0f} multiplies the "
             f"curvature by {curv[2]/curv[0]:.0f} while every output is "
             "identical -- so sharpness is not a property of the function")

# What DOES survive a reparameterisation is worth naming, and it is the thing
# the literature that survives uses: a measure that scales the same way the
# parameters do. The book does not adjudicate; it says which claims are
# invariant and which are not. Nothing is emitted for the outputs-agree
# half: it is a gate rather than a quantity, and a value the prose does
# not reference is a second copy nobody would correct.


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    lines = [
        ">>> lam_hi, lam_lo = 20, 1",
        ">>> 2 / lam_hi, 2 / lam_lo",
        f"{(2 / LAM_HI, 2 / LAM_LO)}",
        f">>> eta = {DEMO_ETA}",
        ">>> x = 1.0",
        f">>> for _ in range({DEMO_STEPS}): x = x - eta * lam_hi * x",
        "...",
        ">>> x",
        f"{_diverge_demo()}",
    ]
    (TRANSCRIPTS / "p17-too-big.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = [
        "% Generated by code/p17_hessian_taylor.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ]
    out += [
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


DEMO_ETA, DEMO_STEPS = 0.11, 40


def _diverge_demo():
    x = 1.0
    for _ in range(DEMO_STEPS):
        x = x - DEMO_ETA * LAM_HI * x
    return x


# One step over the boundary, shown rather than described.
_d = _diverge_demo()
assert abs(_d) > abs(1.0), _d
emit("p17.demo.eta", DEMO_ETA, digits=2)
emit("p17.demo.steps", DEMO_STEPS)
# NOT EMITTED: the transcript prints this value in full, and a rounded copy
# beside it would be two numbers that look like one -- F08's defect.
NOTES.append(f"one step past the boundary: {DEMO_STEPS} steps take 1.0 to {_d:.3g}")

if __name__ == "__main__":
    main()
