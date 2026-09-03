#!/usr/bin/env python3
"""Program F12 --- Rules of differentiation and the chain rule.

Every number Program F12 prints that the reader cannot do in their head is
computed here and written to figures/values/f12.tex, which the book \\input{}s.

F12's thesis is that four rules plus one composition rule cover everything this
book differentiates, and that the composition rule is the hinge:
BACKPROPAGATION IS THE CHAIN RULE APPLIED TO A COMPOSITION OF LAYERS.

THE MEASUREMENTS:

  1. EVERY RULE CHECKED AGAINST A DERIVATIVE COMPUTED WITHOUT IT. Each rule's
     answer is compared with a central difference at the step size F11 found
     to be near the bottom of its U-curve. That is the callback F11 earns: a
     finite difference is a real test when its step is chosen properly, and
     this is what it is for.

  2. THE PRODUCT-RULE TRAP, with numbers. (fg)' is not f'g': on x^2 and x^3 at
     x = 2 the first is 80 and the second is 48. The frames elicit the wrong
     one first, because everybody's first guess is that differentiation
     distributes over a product the way it does over a sum.

  3. THE LOGISTIC'S DERIVATIVE, sigma' = sigma (1 - sigma), and its MAXIMUM,
     which is exactly 1/4 at z = 0. That number is the whole of section 5:

  4. THE VANISHING GRADIENT AS A PRODUCT. A chain of n logistic layers
     multiplies n factors of w sigma'(z), and sigma' <= 1/4 always. So with
     weights of 1 the gradient through forty layers is at most 0.25^40, which
     is about 8e-25 -- and the bound is EXACT and achieved only if every unit
     sits precisely at its centre, so the truth is smaller.

  5. THE EXPLODING SIDE, and it has a clean threshold. The per-layer factor is
     w sigma'(z) <= w/4, so a logistic chain cannot amplify at all unless
     |w| > 4. That is a sharp, checkable statement and it is the reason the
     two failure modes are not symmetric.

WHAT F12 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:

    partial derivatives and the gradient                          -> P15
    Jacobians, forward and reverse mode, loss.backward(),
      the memory cost of keeping activations                      -> P16
    the Hessian and the step-size bound                           -> P17
    matrix calculus and the softmax-cross-entropy gradient        -> P18
    the residual stream and why it keeps gradients alive          -> P32

So F12 states the scalar chain rule, shows that a composition of layers is
what it applies to, and hands the vector version and the architecture's answer
to the failure over by name.

WHAT F12 IS OWED, and pays: F04's sigma and product, F05's composition (its
frame 34 hands this over explicitly), F06's rearrangement, F07's saturation
measurement (left there as a shape for this program to turn into a product),
and F11's limit definition and four worked derivatives.

Run:  python3 code/f12_chain_rule.py      (or: make numbers)
"""
from __future__ import annotations

import math
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


# THE STEP IS NOT F11'S, AND SAYING SO IS A CORRECTION. F11 swept the FORWARD
# difference, whose truncation error is O(h) against a rounding error of about
# eps/h, so its two errors balance near sqrt(eps) -- and F11 measured exactly
# that, committing f11.fd.best.h = 1e-8. A CENTRAL difference has truncation
# error O(h^2), so it balances near eps^(1/3), three decades higher. Attributing
# 1e-5 to F11's curve was a claim about a curve F11 did not measure, and it is
# the kind of claim this book keeps recording: written from the feel of a
# neighbour rather than from the neighbour. The step is swept here instead.
H = 1e-5


def central(f, x: float) -> float:
    return (f(x + H) - f(x - H)) / (2.0 * H)


def check(name: str, f, dfdx, lo: float, hi: float, tol: float = 1e-7) -> float:
    """Compare a rule's answer with a derivative computed without the rule."""
    worst = 0.0
    n = 200
    for i in range(n + 1):
        x = lo + (hi - lo) * i / n
        worst = max(worst, abs(dfdx(x) - central(f, x)))
    assert worst < tol, f"{name}: rule and finite difference disagree by {worst:.2e}"
    return worst


# ==========================================================================
# SECTION 2 --- the four rules, each checked against a derivative obtained
# without it
# ==========================================================================
RULE_ERRORS: dict[str, float] = {}

# power / constant multiple / sum:  d/dx (3x^4 - 5x + 2) = 12x^3 - 5
RULE_ERRORS["sum"] = check("sum", lambda x: 3 * x ** 4 - 5 * x + 2,
                           lambda x: 12 * x ** 3 - 5, -2.0, 2.0)
# product:  d/dx (x^2 . x^3) = 2x . x^3 + x^2 . 3x^2 = 5x^4
RULE_ERRORS["product"] = check("product", lambda x: (x ** 2) * (x ** 3),
                               lambda x: 5 * x ** 4, -2.0, 2.0)
# quotient:  d/dx (x^2 / (x + 3)) = (2x(x+3) - x^2) / (x+3)^2
RULE_ERRORS["quotient"] = check("quotient", lambda x: x ** 2 / (x + 3.0),
                                lambda x: (2 * x * (x + 3.0) - x ** 2) / (x + 3.0) ** 2,
                                -1.0, 2.0)
for _k, _v in RULE_ERRORS.items():
    emit(f"f12.err.{_k}", f"{_v:.1e}")

# ==========================================================================
# SECTION 3 --- the product-rule trap
#
# Everybody's first guess is that differentiation distributes over a product
# the way it does over a sum. The two answers are different numbers, and the
# frames elicit the wrong one before naming it.
# ==========================================================================
TRAP_X = 2.0
emit("f12.trap.x", TRAP_X, 0)
emit("f12.trap.right", 5.0 * TRAP_X ** 4, 0)          # (fg)'  = 5x^4
emit("f12.trap.wrong", (2 * TRAP_X) * (3 * TRAP_X ** 2), 0)   # f'g' = 6x^3
assert 5.0 * TRAP_X ** 4 != (2 * TRAP_X) * (3 * TRAP_X ** 2)

# The two agree nowhere except where the algebra forces it, which is the
# honest form of the claim: 5x^4 = 6x^3 only at x = 0 and x = 6/5.
_agree = [round(x / 1000.0, 3) for x in range(-3000, 3001)
          if abs(5 * (x / 1000.0) ** 4 - 6 * (x / 1000.0) ** 3) < 1e-9]
emit("f12.trap.agree", len(_agree))
assert len(_agree) == 2, f"the two expressions now agree at {_agree}"

# ==========================================================================
# SECTION 4 --- the chain rule, and the logistic
# ==========================================================================
def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def dsigmoid(z: float) -> float:
    s = sigmoid(z)
    return s * (1.0 - s)

# The sweep, so the choice of H is a measurement of THIS program's instrument
# rather than a borrowed one.
#
# NOT ON x^2, WHICH IS THE FUNCTION F11 SWEPT, and the first attempt here did
# exactly that and the assertion caught it. A central difference of a QUADRATIC
# is exact -- ((x+h)^2 - (x-h)^2) / 2h is 2x for every h, because the truncation
# term carries a third derivative and a quadratic has none. So on x^2 the sweep
# measures rounding alone, bottoms at the largest step offered, and settles
# nothing. That is a probe that cannot fail, which is the defect this book keeps
# recording, and it makes the correction above sharper rather than weaker: F11's
# curve is not merely a different curve from this one, it is a curve this
# instrument does not have on that function at all.
#
# Swept on the logistic instead, against the exact sigma(1-sigma), which is the
# function the checks below actually run on.
def _fd_err(h: float) -> float:
    return abs((sigmoid(1.0 + h) - sigmoid(1.0 - h)) / (2.0 * h) - dsigmoid(1.0))

_FD_SWEEP = {e: _fd_err(10.0 ** -e) for e in range(2, 13)}
_FD_BEST = min(_FD_SWEEP, key=lambda e: _FD_SWEEP[e])
assert 4 <= _FD_BEST <= 7, (
    f"the central difference now bottoms at 1e-{_FD_BEST}, so H needs re-choosing")
assert _FD_SWEEP[5] <= 10.0 * _FD_SWEEP[_FD_BEST], (
    "h = 1e-5 is no longer within an order of magnitude of the central optimum")
# And the whole point of the correction: F11's own optimum is NOT this one.
assert _FD_BEST < 8, "the central optimum has drifted onto the forward one's"


RULE_ERRORS["sigmoid"] = check("sigmoid", sigmoid, dsigmoid, -8.0, 8.0)
emit("f12.err.sigmoid", f"{RULE_ERRORS['sigmoid']:.1e}")

# The chain rule on the unit the book keeps using: d/dx sigma(wx + b).
W, B = 2.0, -3.0
emit("f12.chain.w", W, 0)
emit("f12.chain.b", B, 0)
RULE_ERRORS["chain"] = check("chain", lambda x: sigmoid(W * x + B),
                             lambda x: W * dsigmoid(W * x + B), -4.0, 6.0)
emit("f12.err.chain", f"{RULE_ERRORS['chain']:.1e}")

# ==========================================================================
# SECTION 5 --- THE PRODUCT THAT VANISHES
#
# sigma' has an exact maximum of 1/4 at z = 0. The search below is over a fine
# grid, but the assertion is the ALGEBRAIC fact -- sigma(1-sigma) is largest
# when sigma = 1/2 -- so a change of grid cannot move it.
# ==========================================================================
SIG_MAX = 0.25
emit("f12.sig.max", SIG_MAX, 2)
assert abs(dsigmoid(0.0) - SIG_MAX) < 1e-15
for _i in range(-8000, 8001):
    assert dsigmoid(_i / 500.0) <= SIG_MAX + 1e-15, "sigma' now exceeds a quarter"

DEPTH = 40
emit("f12.depth", DEPTH)
emit("f12.vanish.bound", f"{SIG_MAX ** DEPTH:.1e}")

# What it takes to get even that far: every unit sitting exactly at its centre.
# A chain whose units sit where F07 measured saturation instead is far smaller,
# and F07's own figure is the per-layer factor.
F07_SATURATED = dsigmoid(6.0)                        # F07's |x| = 6 point
assert F07_SATURATED < SIG_MAX / 100.0, "F07's saturated point is no longer 100x flatter"

# NEITHER THE FACTOR NOR THE RATIO IS EMITTED HERE, and that is a correction.
# Both are F07's own quantities and F07 commits them as f07.slope.6 and
# f07.slope.ratio6; emitting them again gave the book two committed values for
# one number at two precisions, three hundred pages apart -- 0.0025 there and
# 2.47e-03 here. The frames quote F07's directly and this program keeps the
# gate below, which is P29's resolution of exactly this shape.
#
# AND THE PRODUCT IS A BOUND rather than a figure, which is F05's rule. A
# fortieth power multiplies the base's rounding by forty: the true product is
# 4.82e-105, the printed factor 0.002467 gives 4.86e-105 and a three-figure
# 2.47e-03 gives 5.10e-105, so no precision a table can carry makes the
# printed product reproduce from the printed factor. A bound does, under every
# one of them, and a bound is all the trap needs -- the point is that it is far
# under the floor of every format below a double.
SAT_PRODUCT = F07_SATURATED ** DEPTH
SAT_EXPONENT = 104                                   # the product is below 10^-104
emit("f12.sat.exponent", SAT_EXPONENT)

# AND "not a number at all in any arithmetic a computer does" IS FALSE, which is
# the correction section 5's trapbox needed. 10^-104 is perfectly representable
# in binary64 -- P01 commits its smallest subnormal at about 5e-324 -- and is far
# below binary32's, which P01 commits at about 1.4e-45. So the underflow is a
# claim about the format a network is usually trained in, not about computers.
# Gated against P01's own two floors rather than against a remembered pair.
import re as _re
_P01 = Path(__file__).resolve().parent.parent / "figures" / "values" / "p01.tex"
if _P01.exists():
    _txt = _P01.read_text(encoding="utf8")
    _f32 = _re.search(r"\\mfaval\{p01\.fp32\.minsub\}\{([^}]*)\}", _txt)
    _f64 = _re.search(r"\\mfaval\{p01\.fp64\.minsub\}\{([^}]*)\}", _txt)
    assert _f32 and _f64, "P01's two floors have gone; F12 section 5 quotes fp32's"
    assert SAT_PRODUCT < float(_f32.group(1)), (
        "the saturated product no longer underflows in binary32")
    assert SAT_PRODUCT > float(_f64.group(1)), (
        "the saturated product now underflows in binary64 too, so the frame's "
        "'the format is what decides it' is no longer the point")
    P01_NOTE = (f"binary32 floor {_f32.group(1)} and binary64 floor "
                f"{_f64.group(1)}: the product underflows in one and not the other")
else:
    P01_NOTE = "p01.tex absent: the underflow claim was NOT checked against a floor"
assert SAT_PRODUCT < 10.0 ** -SAT_EXPONENT, "the saturated product no longer clears its bound"
for _printed in ("2.47e-03", "0.002467", "0.0025"):
    assert float(_printed) ** DEPTH < 10.0 ** -SAT_EXPONENT, (
        f"the bound fails when the factor is read off the page as {_printed}")

# AND THE RATIO IS F07's OWN NUMBER, computed here from scratch. F07 measured
# that a saturated unit answers with about a hundredth of its centre response
# and emitted f07.slope.ratio6 for it; this program arrives at the same figure
# by a different route and then multiplies it forty times. Asserting the two
# agree turns "the same computation quoted twice" from a claim into a gate --
# change either program's arithmetic and the build fails here.
_F07 = (Path(__file__).resolve().parent.parent / "figures" / "values" / "f07.tex")
if _F07.exists():
    _m = _re.search(r"\\mfaval\{f07\.slope\.ratio6\}\{([^}]*)\}", _F07.read_text(encoding="utf8"))
    assert _m, "f07.slope.ratio6 has gone; F12 section 5 quotes it"
    assert int(_m.group(1)) == round(SIG_MAX / F07_SATURATED), (
        f"F12 computes {round(SIG_MAX / F07_SATURATED)} where F07 committed "
        f"{_m.group(1)}: the two programs no longer quote one computation")
    # AND THE FACTOR ITSELF, now that the frames quote it rather than emitting a
    # second copy. Gating both halves is P26's both-directions pattern: this
    # program can no longer print a per-layer factor F07 does not commit, and
    # F07 can no longer move it without failing here.
    _f = _re.search(r"\\mfaval\{f07\.slope\.6\}\{([^}]*)\}", _F07.read_text(encoding="utf8"))
    assert _f, "f07.slope.6 has gone; F12 section 5 quotes it as the per-layer factor"
    assert abs(float(_f.group(1)) - F07_SATURATED) < 1e-6, (
        f"F12 computes {F07_SATURATED} where F07 committed {_f.group(1)}: "
        "the per-layer factor is no longer one computation")
    F07_NOTE = (f"F07's committed slope ratio ({_m.group(1)}) and factor "
                f"({_f.group(1)}) both reproduced from scratch")
else:                                                        # pragma: no cover
    F07_NOTE = "f07.tex absent: the cross-programme ratio was NOT checked"

# THE THRESHOLD, and it is exact: the per-layer factor is w sigma'(z) <= w/4,
# so a logistic chain cannot amplify unless |w| > 4.
EXPLODE_W = 4.0
emit("f12.explode.w", EXPLODE_W, 0)
for _w in (1.0, 2.0, 3.9, 4.0):
    for _i in range(-4000, 4001):
        assert _w * dsigmoid(_i / 500.0) <= 1.0 + 1e-12, \
            f"a weight of {_w} now amplifies, which breaks the w/4 bound"
# and just above it, amplification is available
assert 4.1 * dsigmoid(0.0) > 1.0, "a weight above four no longer amplifies"

# A worked chain at a weight that does amplify, so the frames have both sides.
BIG_W = 8.0
emit("f12.explode.big.w", BIG_W, 0)
emit("f12.explode.big.factor", BIG_W * SIG_MAX, 0)
emit("f12.explode.big.depth", f"{(BIG_W * SIG_MAX) ** DEPTH:.1e}")

# ==========================================================================
# A second implementation, for the two facts the program rests on.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the chain rule and sigma' were NOT cross-checked"
else:
    _z = _np.linspace(-10.0, 10.0, 4001)
    _s = 1.0 / (1.0 + _np.exp(-_z))
    assert _np.max(_s * (1.0 - _s)) <= 0.25 + 1e-15
    _x = _np.linspace(-4.0, 6.0, 2001)
    _sw = 1.0 / (1.0 + _np.exp(-(W * _x + B)))
    _analytic = W * _sw * (1.0 - _sw)
    _numeric = _np.gradient(1.0 / (1.0 + _np.exp(-(W * _x + B))), _x)
    assert _np.max(_np.abs(_analytic - _numeric)) < 1e-4
    NUMPY_NOTE = (f"numpy {_np.__version__}: sigma' <= 1/4 over 4001 points, and "
                  f"the chain rule matches a numeric gradient over 2001")

# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f12.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f12_chain_rule.py --- do not edit.",
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
    print(f"  every rule agrees with a central difference at h = {H:.0e}")
    print(f"  the central difference on sigma bottoms at h = 1e-{_FD_BEST}, "
          f"where F11's forward one bottoms at 1e-8")
    print(f"  {P01_NOTE}")
    print(f"  {F07_NOTE}")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
