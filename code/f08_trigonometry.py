#!/usr/bin/env python3
"""Program F8 --- Trigonometry and the unit circle.

Every number Program F8 prints that the reader cannot do in their head is
computed here and written to figures/values/f08.tex, which the book \\input{}s.

F8's thesis is that sine and cosine are the coordinates of a point going round
a circle, and everything the reader needs from trigonometry follows from that
one picture. The program's two payoffs are both IDENTITIES rather than tables,
so both are asserted over a sweep here rather than shown at a point:

  * COSINE SIMILARITY IS THE COSINE OF AN ANGLE. Not an analogy and not a
    coincidence of naming: (a . b) / (|a| |b|) is cos of the angle between
    them, and the script checks it against the angle computed independently.
  * A ROTATION LEAVES THE DOT PRODUCT ALONE WHEN BOTH VECTORS TURN BY THE SAME
    ANGLE, AND MAKES IT DEPEND ONLY ON THE DIFFERENCE WHEN THEY DO NOT. That
    second half is the whole of why rotating a query and a key by an angle
    proportional to position encodes RELATIVE position, and it is the sentence
    the brief asks this program to make sayable.

STDLIB ONLY, as in F3 to F7. numpy is opened only at the bottom to cross-check
the two identities, and it announces itself when absent.

NOT EMITTED, and none of it should be -- these are the values a reader must be
able to produce from the circle itself, and looking them up would defeat the
program:

    cos 0 = 1, sin 0 = 0;  cos(pi/2) = 0, sin(pi/2) = 1;
    cos pi = -1, sin pi = 0;  cos^2 + sin^2 = 1;
    a full turn is 2 pi radians.

THE TRAP IS THE UNITS, and it is computed rather than described: math.sin(90)
is not 1, because 90 is read as radians and is nearly fourteen and a half full
turns. The script prints what it actually is, which is the persuasive part --
a number that looks like nothing rather than an error.

Run:  python3 code/f08_trigonometry.py      (or: make numbers)
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


# ==========================================================================
# SECTION 1 --- radians, and the trap that comes with them
#
# math.sin(90) is the sine of ninety RADIANS. The frame elicits "1" and the
# answer is a number with no obvious meaning, which is exactly what makes the
# bug expensive: nothing raises, nothing warns, and the result is plausible.
# ==========================================================================
emit("f08.sin90rad", math.sin(90.0), 4)
emit("f08.turns90", 90.0 / (2.0 * math.pi), 2)
assert abs(math.sin(math.radians(90.0)) - 1.0) < 1e-15, "sin of 90 DEGREES is not 1"
assert abs(math.sin(90.0)) < 0.9, "sin(90 radians) is no longer visibly not 1"

# The Pythagorean identity, which is the circle's own equation and is checked
# rather than asserted in prose.
_worst_pyth = max(abs(math.cos(t / 100.0) ** 2 + math.sin(t / 100.0) ** 2 - 1.0)
                  for t in range(-700, 700))
emit("f08.pyth.err", f"{_worst_pyth:.1e}")
assert _worst_pyth < 1e-15, "cos^2 + sin^2 is no longer 1"

# ==========================================================================
# SECTION 2 --- one curve, shifted
#
# cos(t) = sin(t + pi/2). F05's horizontal shift applied to a wave, so the two
# curves are one curve and the reader has already met the move.
# ==========================================================================
_worst_shift = max(abs(math.cos(t / 100.0) - math.sin(t / 100.0 + math.pi / 2))
                   for t in range(-700, 700))
emit("f08.shift.err", f"{_worst_shift:.1e}")
assert _worst_shift < 1e-15, "cos is no longer sin shifted by a quarter turn"

# ==========================================================================
# SECTION 4 --- COSINE SIMILARITY IS THE COSINE OF AN ANGLE
#
# Three pairs the frames work with, chosen so the three answers are recognisably
# "the same direction", "unrelated" and "opposite" without being contrived.
# ==========================================================================
PAIRS = {
    "same": ((3.0, 4.0), (6.0, 8.0)),
    "right": ((3.0, 4.0), (-4.0, 3.0)),
    "opposite": ((3.0, 4.0), (-3.0, -4.0)),
}


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def cossim(a, b):
    return dot(a, b) / (norm(a) * norm(b))


for _name, (_a, _b) in PAIRS.items():
    emit(f"f08.cos.{_name}", cossim(_a, _b), 4)
    emit(f"f08.ang.{_name}", math.degrees(math.acos(max(-1.0, min(1.0, cossim(_a, _b))))), 1)

# The identity itself, over a sweep rather than at those four points: the
# cosine-similarity formula agrees with the angle computed from the two
# vectors' own directions. This is what makes "literally the cosine of an
# angle" a statement rather than a slogan.
_worst_cos = 0.0
for _i in range(1, 60):
    for _j in range(1, 60):
        _u = (math.cos(_i / 9.0), math.sin(_i / 9.0))
        _v = (math.cos(_j / 7.0), math.sin(_j / 7.0))
        _theta = _j / 7.0 - _i / 9.0                    # the angle between them
        _worst_cos = max(_worst_cos, abs(cossim(_u, _v) - math.cos(_theta)))
emit("f08.cossim.err", f"{_worst_cos:.1e}")
assert _worst_cos < 1e-14, "cosine similarity is no longer the cosine of the angle"

# The two cutoffs the trap frame compares, and the angles they admit. Written
# as a computation rather than as arithmetic in prose, because the frame's
# whole point is that the reader cannot do this conversion in their head.
for _tag, _sim in (("hi", 0.99), ("lo", 0.98)):
    emit(f"f08.cos.{_tag}", _sim, 2)
    emit(f"f08.ang.{_tag}", math.degrees(math.acos(_sim)), 1)

# The invariant behind the trap: cosine is FLAT near zero, so the same drop in
# similarity buys far more angle near 1 than it does in the middle of the range.
# Asserting the shape rather than the two figures means a change of cutoff
# cannot quietly falsify the frame.
_near_one = math.degrees(math.acos(0.98) - math.acos(0.99))
_mid = math.degrees(math.acos(0.49) - math.acos(0.50))
assert _near_one > 3.0 * _mid, "cosine is no longer flat near zero"

# Length is irrelevant to it, which is the property people actually rely on:
# doubling a vector changes nothing.
assert abs(cossim((3.0, 4.0), (6.0, 8.0)) - 1.0) < 1e-15
assert abs(cossim((3.0, 4.0), (30.0, 40.0)) - 1.0) < 1e-15

# ==========================================================================
# SECTION 5 --- ROTATION, AND WHY IT ENCODES A DIFFERENCE
#
# Rotating (x, y) by theta:  x' = x cos - y sin,  y' = x sin + y cos.
#
# Two facts, both asserted over a sweep:
#   rotating BOTH vectors by the SAME angle leaves the dot product unchanged;
#   rotating them by DIFFERENT angles gives a dot product that depends only on
#     the DIFFERENCE of the two angles.
# The second is the whole of why a rotation proportional to position encodes
# relative position, and it is the sentence the brief wants made sayable.
# ==========================================================================
def rotate(v, theta):
    x, y = v
    return (x * math.cos(theta) - y * math.sin(theta),
            x * math.sin(theta) + y * math.cos(theta))


Q, K = (1.0, 2.0), (3.0, -1.0)

_worst_len = max(abs(norm(rotate(Q, t / 50.0)) - norm(Q)) for t in range(-300, 300))
emit("f08.rot.len.err", f"{_worst_len:.1e}")
assert _worst_len < 1e-14, "a rotation no longer preserves length"

_worst_same = max(abs(dot(rotate(Q, t / 50.0), rotate(K, t / 50.0)) - dot(Q, K))
                  for t in range(-300, 300))
emit("f08.rot.same.err", f"{_worst_same:.1e}")
assert _worst_same < 1e-13, "rotating both vectors together no longer preserves the dot product"

# The relative-position identity: R(a)q . R(b)k depends only on b - a.
_worst_rel = 0.0
for _m in range(0, 40):
    for _n in range(0, 40):
        _a, _b = _m / 6.0, _n / 6.0
        lhs = dot(rotate(Q, _a), rotate(K, _b))
        rhs = dot(Q, rotate(K, _b - _a))
        _worst_rel = max(_worst_rel, abs(lhs - rhs))
emit("f08.rot.rel.err", f"{_worst_rel:.1e}")
assert _worst_rel < 1e-13, "the rotated dot product no longer depends only on the difference"

# A worked instance the frames print: the same pair at two positions a fixed
# distance apart gives the same score wherever the pair sits.
emit("f08.rot.score.near", dot(rotate(Q, 1.0), rotate(K, 2.0)), 4)
emit("f08.rot.score.far", dot(rotate(Q, 9.0), rotate(K, 10.0)), 4)
assert abs(dot(rotate(Q, 1.0), rotate(K, 2.0)) - dot(rotate(Q, 9.0), rotate(K, 10.0))) < 1e-12

# ==========================================================================
# SECTION 3 --- the four moves on a wave, and the frequency ladder
#
# A positional encoding uses many frequencies at once. The point the frame
# makes is that the wavelengths span an enormous range, so a short wave
# distinguishes neighbours and a long one distinguishes distant positions.
# ==========================================================================
D_MODEL = 512
for _i, _tag in ((0, "first"), (D_MODEL // 4, "mid"), (D_MODEL // 2 - 1, "last")):
    _wavelength = 2.0 * math.pi * (10000.0 ** (2.0 * _i / D_MODEL))
    emit(f"f08.pe.{_tag}", _wavelength, 1 if _wavelength < 1000 else 0)
assert 2.0 * math.pi * (10000.0 ** 0) < 10.0 < 2.0 * math.pi * (10000.0 ** (2.0 * (D_MODEL // 2 - 1) / D_MODEL))

# ==========================================================================
# A second implementation, for the two identities the program rests on.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the two identities were NOT cross-checked"
else:
    _t = _np.linspace(-7.0, 7.0, 2001)
    assert _np.allclose(_np.cos(_t) ** 2 + _np.sin(_t) ** 2, 1.0, atol=1e-15)
    _qa = _np.array(Q); _ka = _np.array(K)
    for _ang in _np.linspace(-6.0, 6.0, 601):
        _R = _np.array([[math.cos(_ang), -math.sin(_ang)],
                        [math.sin(_ang), math.cos(_ang)]])
        assert abs(float((_R @ _qa) @ (_R @ _ka)) - float(_qa @ _ka)) < 1e-12
    NUMPY_NOTE = (f"numpy {_np.__version__}: the Pythagorean identity and the "
                  f"rotation-invariance of the dot product cross-checked")

# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f08.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f08_trigonometry.py --- do not edit.",
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
    print(f"  cosine similarity IS cos(angle): worst {_worst_cos:.1e} over 3481 pairs")
    print(f"  R(a)q . R(b)k depends only on b - a: worst {_worst_rel:.1e} over 1600 pairs")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
