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


# The step F11 measured as near the bottom of its U-curve, used here for what
# a finite difference is actually good for: checking a rule against an answer
# obtained without it.
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
emit("f12.sat.factor", f"{F07_SATURATED:.2e}")
emit("f12.sat.ratio", round(SIG_MAX / F07_SATURATED))
emit("f12.sat.bound", f"{F07_SATURATED ** DEPTH:.1e}")
assert F07_SATURATED < SIG_MAX / 100.0, "F07's saturated point is no longer 100x flatter"

# AND THE RATIO IS F07's OWN NUMBER, computed here from scratch. F07 measured
# that a saturated unit answers with about a hundredth of its centre response
# and emitted f07.slope.ratio6 for it; this program arrives at the same figure
# by a different route and then multiplies it forty times. Asserting the two
# agree turns "the same computation quoted twice" from a claim into a gate --
# change either program's arithmetic and the build fails here.
_F07 = (Path(__file__).resolve().parent.parent / "figures" / "values" / "f07.tex")
if _F07.exists():
    import re as _re
    _m = _re.search(r"\\mfaval\{f07\.slope\.ratio6\}\{([^}]*)\}", _F07.read_text(encoding="utf8"))
    assert _m, "f07.slope.ratio6 has gone; F12 section 5 quotes it"
    assert int(_m.group(1)) == round(SIG_MAX / F07_SATURATED), (
        f"F12 computes {round(SIG_MAX / F07_SATURATED)} where F07 committed "
        f"{_m.group(1)}: the two programs no longer quote one computation")
    F07_NOTE = f"F07's committed slope ratio ({_m.group(1)}) reproduced from scratch"
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
    print(f"  {F07_NOTE}")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
