#!/usr/bin/env python3
"""Program F6 --- Equations, inequalities and the straight line.

Every number Program F6 prints that the reader cannot do in their head is
computed here and written to figures/values/f06.tex, which the book \\input{}s.

F6's thesis is that solving is undoing, and undoing is something the reader can
check: substitute the answer back. That is what most of this script does. Where
the program solves an equation, the solution is computed AND substituted, and
the build asserts the substitution closes. A worked solution nobody put back
into the original is the same shape of defect as a console block nobody ran.

STDLIB ONLY, as in F3, F4 and F5: `make numbers` must run on a plain python3.
numpy is opened only at the bottom, to cross-check the clipping comparison
against code this script did not write, and it announces itself when absent.

NOT EMITTED, and none of it should be --- this program teaches rearrangement,
so its arithmetic is the thing being taught and stays inline as digits:

    3x + 7 = 22 -> x = 5;  2x + 1 = 0 -> x = -1/2;
    y = wx + b -> x = (y - b)/w;  the gradient (5-3)/(2-1) = 2;
    -2x > 6 -> x < -3;  the clip bounds -1 and 1;
    sigma(z) > 1/2 <-> z > 0, which is F5's crossing at -b/w with b = 0.

THE TWO MEASURED CLAIMS, and both are here because an adjective would not do:

  * SOLVING A LOGISTIC BACKWARDS. The program has the reader recover the input
    that produces a stated probability, which is F5's logit arriving as an
    equation rather than as a graph. The solution is substituted back and the
    residual is asserted, so "check by substituting" is demonstrated by the
    build and not merely recommended.
  * CLIPPING BY VALUE AGAINST CLIPPING BY NORM. Trap 26 of the catalogue, and
    the one place in this program where the reader's intuition is actively
    wrong: the two operations have the same API shape, the same threshold, and
    different results. One preserves direction and one does not, and the angle
    between the two answers is computed rather than described.

ONE OWNER RE-DERIVED RATHER THAN COPIED. The trap catalogue routes gradient
clipping to "P19", which was written before P7 was inserted and everything
after it moved up one; §3 of that file carries a blanket warning to that
effect. Re-derived from tools/programs.json, the owner is P21, "Stochastic
optimisation and differentiating through randomness", whose brief undertakes
clipping. Do not copy an owner out of notes/02.

Run:  python3 code/f06_equations.py      (or: make numbers)
"""
from __future__ import annotations

import math
from pathlib import Path

VALUES: dict[str, tuple[str, bool]] = {}


def emit(key: str, value, digits: int | None = None) -> None:
    """Record one value under the name the book will reference it by.

    Also decides here whether the value is a number, because this end knows for
    free and the LaTeX end does not. \\val passes its body to siunitx, which
    raises a fatal error on anything that is not a number; the book's \\val
    refuses a value emitted as text and names \\valtext instead.
    """
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


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


# ==========================================================================
# SECTION 2 --- rearranging a formula, and checking by substitution
#
# The unit is sigma(wx + b) with w = 2 and b = -3, and the reader is asked for
# the input at which it reads 0.8. Undoing in reverse order gives
#
#     x = (logit(p) - b) / w
#
# and the whole point of the section is that you may then CHECK it. So the
# script checks it, at every probability the program prints, and asserts the
# residual rather than trusting the algebra.
# ==========================================================================
W, B = 2.0, -3.0


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def solve_for_x(p: float) -> float:
    return (logit(p) - B) / W


# p = 0.5 is NOT emitted: it is (0 - (-3))/2 = 1.5, which the reader does in
# their head and which the frame therefore writes inline. The other two are
# not head arithmetic and are computed.
TARGETS = (0.5, 0.8, 0.99)
for _p in TARGETS:
    _tag = str(_p).replace("0.", "p")            # p5, p8, p99
    if _p != 0.5:
        emit(f"f06.solve.{_tag}", solve_for_x(_p), 4)
    # Substituted back. This is the section's own instruction, executed.
    assert abs(sigmoid(W * solve_for_x(_p) + B) - _p) < 1e-12, \
        f"the solution does not satisfy the original equation at p={_p}"

# The crossing, which is F5's -b/w and must agree with it to the digit. Quoted
# in the frame as the p = 0.5 case of the same formula rather than as a new
# fact, so the two programs are provably doing one thing.
assert abs(solve_for_x(0.5) - (-B / W)) < 1e-15, "the p = 0.5 solution is not -b/w"

# ==========================================================================
# SECTION 4 --- two equations, two unknowns
#
# A deliberately small system, solved by elimination in the frames and by
# Cramer here, so that the two routes are checked against each other:
#
#     3x + 2y = 12
#      x -  y =  1
#
# Both equations are then evaluated at the solution. "Two lines crossing" is
# the picture the section sells, so the crossing point had better be on both
# lines.
# ==========================================================================
A1, B1, C1 = 3.0, 2.0, 12.0
A2, B2, C2 = 1.0, -1.0, 1.0

DET = A1 * B2 - A2 * B1
SOL_X = (C1 * B2 - C2 * B1) / DET
SOL_Y = (A1 * C2 - A2 * C1) / DET
# NOT emitted, and this is the section the rule was written for: the reader is
# being TAUGHT to solve this by elimination, so 5y = 9 and x = y + 1 are the
# work, not a result to look up. The assertions stay, because what is being
# checked is that the frames' answer really is on both lines.
assert abs(A1 * SOL_X + B1 * SOL_Y - C1) < 1e-12, "the solution misses the first line"
assert abs(A2 * SOL_X + B2 * SOL_Y - C2) < 1e-12, "the solution misses the second line"

# The two gradients, which is what "they cross exactly once" MEANS. A pair with
# equal gradients would be parallel and the determinant would be zero; the
# frames make that the reason rather than a separate case to memorise.
assert DET != 0 and (-A1 / B1) != (-A2 / B2), "the demonstration system is parallel"

# ==========================================================================
# SECTION 6 --- clipping by value against clipping by norm
#
# Trap 26. The two operations take the same threshold and the same-shaped
# argument, their names differ by one word, and they do different things:
# clipping by NORM rescales the whole vector and preserves direction; clipping
# by VALUE truncates each component on its own and turns the vector.
#
# The gradient below is chosen so that the difference is visible rather than
# marginal: one large component and two small ones, which is what a gradient
# on the step before a spike actually looks like.
# ==========================================================================
GRAD = (6.0, 0.5, -0.25)
CLIP = 1.0


def norm(v) -> float:
    return math.sqrt(sum(c * c for c in v))


def clip_by_value(v, t):
    return tuple(max(-t, min(t, c)) for c in v)


def clip_by_norm(v, t):
    n = norm(v)
    return tuple(c * t / n for c in v) if n > t else tuple(v)


BY_VALUE = clip_by_value(GRAD, CLIP)
BY_NORM = clip_by_norm(GRAD, CLIP)

emit("f06.grad.norm", norm(GRAD), 4)
emit("f06.clip.value.norm", norm(BY_VALUE), 4)
emit("f06.clip.norm.norm", norm(BY_NORM), 4)
for _i, _c in enumerate(BY_VALUE):
    emit(f"f06.clip.value.c{_i + 1}", _c, 4)
for _i, _c in enumerate(BY_NORM):
    emit(f"f06.clip.norm.c{_i + 1}", _c, 4)

# The angle, which is the quantity the trap is actually about. Clipping by norm
# is a scaling, so it turns the vector through exactly zero; clipping by value
# turns it, and the frame quotes how far.
def angle_deg(u, v) -> float:
    dot = sum(a * b for a, b in zip(u, v))
    return math.degrees(math.acos(max(-1.0, min(1.0, dot / (norm(u) * norm(v))))))


ANGLE_VALUE = angle_deg(GRAD, BY_VALUE)
ANGLE_NORM = angle_deg(GRAD, BY_NORM)
emit("f06.clip.value.angle", ANGLE_VALUE, 1)

# Two INVARIANTS rather than two observations, so a change of GRAD cannot make
# the frame quietly wrong: clipping by norm preserves direction exactly, and
# clipping by value does not.
assert ANGLE_NORM < 1e-9, "clipping by norm no longer preserves direction"
assert ANGLE_VALUE > 1.0, "clipping by value no longer turns this gradient visibly"
assert abs(norm(BY_NORM) - CLIP) < 1e-12, "clipping by norm did not land on the threshold"

# And the sentence the trap turns on: after clipping BY VALUE the norm is still
# above the threshold, so "clipped at 1.0" did not cap the size of the step.
assert norm(BY_VALUE) > CLIP, "the by-value example no longer exceeds the threshold"

# ==========================================================================
# A second implementation, for the one comparison the section rests on.
#
# numpy is used in no arithmetic above; it is opened here only to check the two
# clipping results against code this script did not write, and it ANNOUNCES
# itself when skipped -- F3's np.logspace lesson, where a check that silently
# did not run was worse than no check.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the clipping comparison was NOT cross-checked"
else:
    _g = _np.array(GRAD, dtype=_np.float64)
    assert _np.allclose(_np.clip(_g, -CLIP, CLIP), BY_VALUE)
    _scaled = _g * CLIP / _np.linalg.norm(_g)
    assert _np.allclose(_scaled, BY_NORM)
    NUMPY_NOTE = (f"numpy {_np.__version__}: both clipping results cross-checked "
                  f"(by value {BY_VALUE}, by norm {tuple(round(c, 4) for c in BY_NORM)})")

# ==========================================================================
# Write the file the book reads.
# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f06.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f06_equations.py --- do not edit.",
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
    print(f"  every solution substituted back into its own equation: residual < 1e-12")
    print(f"  clipping: by norm turns the gradient {ANGLE_NORM:.1e} degrees, "
          f"by value {ANGLE_VALUE:.1f} degrees")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
