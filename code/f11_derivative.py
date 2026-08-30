#!/usr/bin/env python3
"""Program F11 --- The derivative: rate of change.

Every number Program F11 prints that the reader cannot do in their head is
computed here and written to figures/values/f11.tex, which the book \\input{}s.

F11's thesis is that a derivative is a slope you get by shrinking a chord,
that shrinking it is a limit rather than a small number, and that once you can
read the sign and size of one you already have the mechanism of gradient
descent -- before the word.

FOUR MEASUREMENTS, all free, all deterministic, all stdlib:

  1. THE CHORD CONVERGES. Slopes of the chord to y = x^2 at x = 3 over
     h = 1, 0.1, 0.01, 0.001. The frames elicit the limit from the pattern.

  2. THE U-CURVE, and it is the program's best measurement. Shrink h in a
     forward difference and the error falls, bottoms out, and then RISES:
     the mathematics says smaller is always better and the machine says
     otherwise, and the crossover is near the square root of machine epsilon.
     F11 measures it and hands the reason for the right-hand branch to P01,
     whose subject it is.

  3. GRADIENT DESCENT IN ONE VARIABLE, on f(x) = (x - 3)^2 + 1 from x = 10 at
     three step sizes: one that walks in, one that overshoots and still
     converges, one that diverges. The INVARIANT is asserted rather than the
     three traces: the update is x <- x - eta f'(x), which on this f is
     x - 3 <- (1 - 2 eta)(x - 3), so it converges exactly when
     |1 - 2 eta| < 1, i.e. 0 < eta < 1. That is derivable by the reader and
     survives a change of f in a way three traces would not.

  4. STEEP IS NOT THE SAME AS FAR. Two points on one curve where the steeper
     one is the NEARER to the minimum, which is the misconception the whole
     of section 5 has to defeat.

WHAT F11 DELIBERATELY DOES NOT DO, checked against tools/programs.json rather
than remembered:

    the four rules and the chain rule                             -> F12
    partial derivatives, the gradient, steepest descent           -> P15
    the second derivative, curvature, the step-size bound,
      the Taylor expansion                                        -> P17
    convexity, local against global minima                        -> P19
    momentum, Adam, and every optimiser by name                   -> P20
    why the U-curve's right-hand branch exists                    -> P01

So F11 derives two derivatives from the definition and notices a pattern
WITHOUT stating the power rule as a rule, because stating it is F12's job and
noticing it is what makes F12's statement land.

Run:  python3 code/f11_derivative.py      (or: make numbers)
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
# SECTION 2 --- the chord, shrinking
#
# f(x) = x^2 at x = 3. The chord slope is exactly 6 + h, which is why the
# frames can elicit the limit from four rows: the pattern is visible and the
# algebra behind it is one line the reader does themselves.
# ==========================================================================
def sq(x: float) -> float:
    return x * x


X0 = 3.0
for _tag, _h in (("1", 1.0), ("01", 0.1), ("001", 0.01), ("0001", 0.001)):
    emit(f"f11.chord.{_tag}", (sq(X0 + _h) - sq(X0)) / _h, 3)

# The algebra the frames do by hand, asserted: the chord slope is 6 + h
# exactly, for every h, so the limit is not a guess from four rows.
for _i in range(1, 400):
    _h = _i / 100.0
    assert abs((sq(X0 + _h) - sq(X0)) / _h - (2 * X0 + _h)) < 1e-12
emit("f11.deriv.at3", 2 * X0, 0)

# ==========================================================================
# SECTION 3 --- the U-curve
#
# THE PROGRAM'S BEST MEASUREMENT. The forward difference of x^2 at x = 3 has
# error exactly h in exact arithmetic, so it should fall forever. It does not.
# ==========================================================================
TRUE = 2 * X0
ROWS: list[tuple[str, float, float]] = []
_best_h, _best_err = None, None
_h = 1.0
while _h > 1e-17:
    approx = (sq(X0 + _h) - sq(X0)) / _h
    err = abs(approx - TRUE)
    ROWS.append((f"{_h:.0e}", approx, err))
    if _best_err is None or err < _best_err:
        _best_h, _best_err = _h, err
    _h /= 10.0

# Only the rows the frames quote. Every row is in the transcript, so emitting
# the rest as values would be a second copy of a committed number that nobody
# reads -- and C7 reports an unused value for exactly that reason.
for _tag, _h in (("8", "1e-08"), ("12", "1e-12"), ("16", "1e-16")):
    _row = next(r for r in ROWS if r[0] == _h)
    emit(f"f11.fd.err.{_tag}", f"{_row[2]:.1e}")
emit("f11.fd.approx.16", next(r for r in ROWS if r[0] == "1e-16")[1], 6)

emit("f11.fd.best.h", f"{_best_h:.0e}")
emit("f11.fd.best.err", f"{_best_err:.1e}")

# The INVARIANT, which is the shape and not the figures: the error falls, then
# rises, and the smallest h tried is far WORSE than the best one. A frame that
# claimed "smaller is always better" is falsified by this and by nothing else.
_first, _last = ROWS[0][2], ROWS[-1][2]
assert _best_err < _first, "the error no longer falls as h shrinks"
assert _last > _best_err * 100, "the error no longer rises again at tiny h"
assert 1e-10 < _best_h < 1e-6, f"the turning point moved to h = {_best_h}"

# At h = 1e-16 the difference underflows to nothing at all: x + h is x.
assert (X0 + 1e-16) == X0, "1e-16 is no longer lost against 3.0"
emit("f11.fd.vanishes", "1e-16")

# The frame claims the turning point moves with the SIZE of the numbers being
# subtracted rather than being a constant of the arithmetic. That is a claim,
# so it is measured: the same sweep at x = 3000, where f(x) is nine million
# and the digits left over to record a difference are far fewer.
X_BIG = 3000.0
_bh, _be = None, None
_h = 1.0
while _h > 1e-17:
    _e = abs((sq(X_BIG + _h) - sq(X_BIG)) / _h - 2 * X_BIG)
    if _be is None or _e < _be:
        _bh, _be = _h, _e
    _h /= 10.0
emit("f11.fd.big.x", X_BIG, 0)
emit("f11.fd.big.h", f"{_bh:.0e}")
assert _bh > _best_h * 100, "the turning point no longer moves with the size of x"

# ==========================================================================
# SECTION 4 --- steep is not the same as far
#
# On f(x) = x^4 - 4x^2 the point x = 1.9 is NEARER the right-hand minimum than
# x = 0.4 is to the middle, and it is much steeper. The misconception this
# defeats -- "a big gradient means a long way to go" -- is the one section 5
# has to clear before gradient descent makes sense.
# ==========================================================================
def quartic(x: float) -> float:
    return x ** 4 - 4.0 * x * x


def dquartic(x: float) -> float:
    return 4.0 * x ** 3 - 8.0 * x


MIN_RIGHT = 2.0 ** 0.5                       # where 4x^3 - 8x = 0, x > 0
assert abs(dquartic(MIN_RIGHT)) < 1e-12
emit("f11.min.x", MIN_RIGHT, 4)

STEEP_X, SHALLOW_X = 1.9, 0.4
emit("f11.steep.x", STEEP_X, 1)
emit("f11.steep.slope", dquartic(STEEP_X), 3)
emit("f11.steep.dist", abs(STEEP_X - MIN_RIGHT), 3)
emit("f11.shallow.x", SHALLOW_X, 1)
emit("f11.shallow.slope", dquartic(SHALLOW_X), 3)
emit("f11.shallow.dist", abs(SHALLOW_X - MIN_RIGHT), 3)

assert abs(dquartic(STEEP_X)) > abs(dquartic(SHALLOW_X)), "the steep point is no longer steeper"
assert abs(STEEP_X - MIN_RIGHT) < abs(SHALLOW_X - MIN_RIGHT), "the steep point is no longer nearer"

# ==========================================================================
# SECTION 5 --- walking downhill, before the word
#
# f(x) = (x - 3)^2 + 1, f'(x) = 2(x - 3), started at x = 10.
# ==========================================================================
def bowl(x: float) -> float:
    return (x - 3.0) ** 2 + 1.0


def dbowl(x: float) -> float:
    return 2.0 * (x - 3.0)


START = 10.0
STEPS = 8
emit("f11.gd.start", START, 0)
emit("f11.gd.steps", STEPS)

for _tag, _eta in (("small", 0.1), ("big", 0.9), ("toobig", 1.1)):
    x = START
    for _ in range(STEPS):
        x -= _eta * dbowl(x)
    emit(f"f11.gd.{_tag}.eta", _eta, 1)
    emit(f"f11.gd.{_tag}.end", x, 3)

# Three traces are an illustration; the INVARIANT is the thing the reader can
# derive and check. On this f the update is exactly
#     x - 3  <-  (1 - 2 eta) (x - 3)
# so the distance to the minimum is multiplied by |1 - 2 eta| every step.
#
# The first version of this assertion checked whether the walk had "converged"
# after sixty steps and compared that against |1 - 2 eta| < 0.85. It failed on
# the first run, at eta = 0.08, and it deserved to: it conflated CONVERGES
# with CONVERGES FAST ENOUGH TO NOTICE, and 0.85 was a fudge chosen to make
# the two agree. What is actually true is the recurrence, so that is what is
# asserted -- one step at a time, and then compounded over sixty.
for _i in range(1, 300):
    _eta = _i / 200.0
    x = START
    for _n in range(60):
        _before = x - 3.0
        x -= _eta * dbowl(x)
        assert abs((x - 3.0) - (1.0 - 2.0 * _eta) * _before) <= 1e-9 * max(1.0, abs(_before)), \
            f"the one-step recurrence broke at eta = {_eta}"
    _predicted = abs(1.0 - 2.0 * _eta) ** 60 * (START - 3.0)
    assert abs(abs(x - 3.0) - _predicted) <= 1e-6 * max(1.0, _predicted), \
        f"sixty steps no longer compound the recurrence at eta = {_eta}"
    # and the consequence the frames state: the walk shrinks the distance
    # exactly when the factor is below one, and grows it when it is above.
    if abs(1.0 - 2.0 * _eta) < 1.0:
        assert abs(x - 3.0) < abs(START - 3.0)
    elif abs(1.0 - 2.0 * _eta) > 1.0:
        assert abs(x - 3.0) > abs(START - 3.0)
emit("f11.gd.factor.small", abs(1.0 - 2.0 * 0.1), 1)
emit("f11.gd.factor.big", abs(1.0 - 2.0 * 0.9), 1)
emit("f11.gd.factor.toobig", abs(1.0 - 2.0 * 1.1), 1)

# The step size at which it lands on the minimum in ONE step, which is what
# makes "how far" a different question from "which way".
emit("f11.gd.perfect", 0.5, 1)
assert abs((START - 0.5 * dbowl(START)) - 3.0) < 1e-12, "eta = 0.5 no longer lands exactly"

# ==========================================================================
# A second implementation, for the two claims the program rests on.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the chord and the U-curve were NOT cross-checked"
else:
    _hs = _np.logspace(0, -16, 200)
    _errs = _np.abs(((X0 + _hs) ** 2 - X0 ** 2) / _hs - TRUE)
    _i = int(_np.argmin(_errs))
    assert 0 < _i < len(_hs) - 1, "the U-curve no longer turns strictly inside the range"
    assert _errs[-1] > _errs[_i] * 100
    NUMPY_NOTE = (f"numpy {_np.__version__}: the U-curve turns at "
                  f"h = {_hs[_i]:.1e} over 200 points, and rises again after it")

# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f11.tex"
TRANSCRIPT = (Path(__file__).resolve().parent.parent / "figures" / "transcripts"
              / "f11-shrinking-h.txt")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f11_derivative.py --- do not edit.",
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

    # The whole U-curve, written out, because the shape is the argument and a
    # table of five rows would let a reader think the middle was interpolated.
    out = ["         h            (f(3+h) - f(3)) / h         error"]
    for tag, approx, err in ROWS:
        out.append(f"  {tag:>8}   {approx:>22.12f}   {err:>12.1e}")
    TRANSCRIPT.write_text("\n".join(out) + "\n", encoding="utf8")

    width = max(len(k) for k in VALUES)
    for k, (body, numeric) in VALUES.items():
        print(f"  {k:<{width}}  {body}{'' if numeric else '   (text)'}")
    print(f"\n  {len(VALUES)} values -> {OUT.relative_to(OUT.parents[2])}")
    print(f"  {len(ROWS)} rows      -> {TRANSCRIPT.relative_to(TRANSCRIPT.parents[2])}")
    print(f"  the forward difference is best at h = {_best_h:.0e}, error {_best_err:.1e}")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
