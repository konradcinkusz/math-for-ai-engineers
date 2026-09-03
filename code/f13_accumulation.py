#!/usr/bin/env python3
"""Program F13 --- Accumulation, area and expectation.

Every number Program F13 prints that the reader cannot do in their head is
computed here and written to figures/values/f13.tex, which the book \\input{}s.

F13's thesis is that an integral ACCUMULATES, and that it is the continuous
twin of the sigma of Program F4. Twenty frames rather than forty-five, and the
difference is the point: this is not a course in integration technique, and
substitution, parts and partial fractions are excluded deliberately and by
name.

THE MEASUREMENTS, all free and all deterministic:

  1. A RIEMANN SUM CONVERGING. Rectangles under x^2 from 0 to 1 at n = 10,
     100, 1000, 10000. The frames elicit the limit and the script asserts the
     exact error, which is 1/(2n) + 1/(6n^2) for the right-hand rule -- so the
     convergence is not a numerical accident and the reader can check it.

  2. A DENSITY WHOSE HEIGHT EXCEEDS ONE. Uniform on [0, 0.1] has height 10.
     That is the trap the whole of section 4 exists for: an AREA is bounded by
     one and a HEIGHT is not, so a density is not a probability and reading it
     as one is a category error rather than an approximation.

  3. THE NORMALISING CONSTANT, computed. An unnormalised curve accumulates to
     something that is not one, and dividing by it is the whole operation --
     the same division the reader has already met in a softmax.

  4. THE WEIGHTED-AVERAGE SHAPE. Integral of x p(x) over a density, by Riemann
     sum, against the value the algebra gives. F13 supplies the SHAPE and hands
     the object it is an expectation OF to P24.

WHAT F13 DELIBERATELY LEAVES ALONE, checked against tools/programs.json rather
than remembered -- three programs declare F13 as a dependency:

    probability as a measure, the three rules, conditioning, Bayes   -> P23
    random variables, expectation and variance as summaries, the six
      distributions, categorical sampling                           -> P24
    convexity and Jensen's inequality                               -> P19

So F13 supplies the accumulation, the area, the density and the weighted-
average shape, and hands over every object those shapes turn out to be about.

Run:  python3 code/f13_accumulation.py      (or: make numbers)
"""
from __future__ import annotations

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


# ==========================================================================
# SECTION 1 --- a sum of many small pieces
#
# Right-hand rectangles under x^2 from 0 to 1. The exact sum is
#     (1/n^3) * n(n+1)(2n+1)/6  =  1/3 + 1/(2n) + 1/(6n^2)
# so the error is KNOWN in closed form, and asserting it is stronger than
# asserting that four numbers look like they are heading somewhere.
# ==========================================================================
def right_sum(n: int) -> float:
    w = 1.0 / n
    return sum((i * w) ** 2 * w for i in range(1, n + 1))


EXACT = 1.0 / 3.0    # written on the page as \frac{1}{3}, not emitted

for n in (10, 100, 1000, 10000):
    emit(f"f13.rect.{n}", right_sum(n), 6)
    predicted = EXACT + 1.0 / (2 * n) + 1.0 / (6 * n * n)
    assert abs(right_sum(n) - predicted) < 1e-9, (
        f"the right-hand sum at n = {n} no longer equals 1/3 + 1/(2n) + 1/(6n^2)")

# The invariant rather than the four rows: the error halves when n doubles,
# because the leading term is 1/(2n). A frame claiming "it converges" is
# weaker than one that says HOW FAST and can be checked.
for n in (10, 100, 1000):
    e1 = right_sum(n) - EXACT
    e2 = right_sum(2 * n) - EXACT
    assert 1.9 < e1 / e2 < 2.1, f"the error no longer halves when n doubles at n = {n}"
emit("f13.err.10", right_sum(10) - EXACT, 4)
emit("f13.err.10000", f"{right_sum(10000) - EXACT:.1e}")

# ==========================================================================
# SECTION 4 --- a density is not a probability
#
# THE TRAP. A uniform density on a narrow interval has a height above one,
# which no probability can have. Area is bounded and height is not.
# ==========================================================================
NARROW = 0.1
emit("f13.narrow", NARROW, 1)
emit("f13.narrow.height", 1.0 / NARROW, 0)
assert 1.0 / NARROW > 1.0, "the narrow uniform density no longer has a height above one"
# and its area is one, exactly, which is the whole point of the contrast
assert abs(NARROW * (1.0 / NARROW) - 1.0) < 1e-15

# ==========================================================================
# SECTION 4 --- the normalising constant
#
# An unnormalised curve, its accumulated total, and the division that fixes
# it. The curve is x(1-x) on [0, 1], whose exact integral is 1/6.
# ==========================================================================
def unnormalised(x: float) -> float:
    return x * (1.0 - x)


def integrate(f, lo: float, hi: float, n: int = 200000) -> float:
    """Midpoint rule, which is accurate enough that the frames' figures are
    the algebra's figures rather than the method's."""
    w = (hi - lo) / n
    return sum(f(lo + (i + 0.5) * w) * w for i in range(n))


# NEITHER THE TOTAL NOR ITS RECIPROCAL IS EMITTED, and that is a correction on
# this book's own rule that arithmetic the program is teaching is written
# inline. The total is exactly 1/6 -- which the reader can produce from the
# power rule six frames earlier -- and 0.1667 is what it printed instead, so
# the reader who divided the page's own two numbers got 1/0.1667 = 5.9988 and
# had to guess that 6 was meant. An exact fraction reproduces exactly, and it
# is the form the frame is teaching the reader to reach.
TOTAL = integrate(unnormalised, 0.0, 1.0)
assert abs(TOTAL - 1.0 / 6.0) < 1e-9, "the unnormalised curve no longer accumulates to 1/6"

# And after dividing, the area is one. Asserted, because that is the defining
# property rather than a check of the arithmetic.
NORM = 1.0 / TOTAL
assert abs(integrate(lambda x: NORM * unnormalised(x), 0.0, 1.0) - 1.0) < 1e-9

# ==========================================================================
# SECTION 5 --- the weighted-average shape
#
# Integral of x p(x). For the symmetric density above it is 1/2, which the
# reader can see from the symmetry before computing it -- so the number
# confirms an argument rather than replacing one.
# ==========================================================================
CENTRE = integrate(lambda x: x * NORM * unnormalised(x), 0.0, 1.0)
emit("f13.centre", CENTRE, 4)
assert abs(CENTRE - 0.5) < 1e-9, "the symmetric density's weighted average is no longer 1/2"

# A lopsided one, where symmetry gives nothing and the integral has to be done.
# 2x on [0, 1] is a density (area 1); its weighted average is 2/3.
def lopsided(x: float) -> float:
    return 2.0 * x


assert abs(integrate(lopsided, 0.0, 1.0) - 1.0) < 1e-9, "2x on [0,1] is no longer a density"
LOP = integrate(lambda x: x * lopsided(x), 0.0, 1.0)
emit("f13.lop.centre", LOP, 4)
assert abs(LOP - 2.0 / 3.0) < 1e-9
# and it is NOT the midpoint of the interval, which is the point of including it
assert abs(LOP - 0.5) > 0.1, "the lopsided density's average is no longer off centre"

# ==========================================================================
# A second implementation, for the two facts the program rests on.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the sums were NOT cross-checked"
else:
    _x = _np.linspace(0.0, 1.0, 1000001)
    assert abs(_np.trapezoid(_x ** 2, _x) - EXACT) < 1e-9
    _p = NORM * _x * (1.0 - _x)
    assert abs(_np.trapezoid(_p, _x) - 1.0) < 1e-9
    assert abs(_np.trapezoid(_x * _p, _x) - 0.5) < 1e-9
    NUMPY_NOTE = (f"numpy {_np.__version__}: the area under x^2, the normalised "
                  f"density's area and its weighted average all cross-checked")

# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f13.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f13_accumulation.py --- do not edit.",
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
    print(f"  the right-hand sum's error is 1/(2n) + 1/(6n^2) at every n tried")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
