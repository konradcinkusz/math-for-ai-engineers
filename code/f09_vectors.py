#!/usr/bin/env python3
"""Program F9 --- Vectors in the plane and in space.

Every number Program F9 prints that the reader cannot do in their head is
computed here and written to figures/values/f09.tex, which the book \\input{}s.

F9's thesis is that a vector is a list of numbers you may ALSO draw as an
arrow, and that the drawing is a convenience of two and three dimensions
rather than part of the definition. The arithmetic never needed the picture,
which is why it survives into 768 dimensions unchanged and the picture does
not.

THE PAYOFF IS A BRIDGE, and it is an identity rather than a table:

    |a - b|^2 = |a|^2 + |b|^2 - 2 (a . b)

which is F8's cosine result rearranged. Two consequences the program is built
on, both asserted over a sweep here:

  * ON THE UNIT SPHERE, DISTANCE AND COSINE SIMILARITY RANK IDENTICALLY.
    |a - b|^2 = 2 - 2 cos(theta), a strictly decreasing function of the
    cosine, so on unit vectors the two measures CANNOT disagree.
  * OFF IT, THEY CAN. The script finds a concrete triple where the nearest
    neighbour by Euclidean distance is not the nearest by cosine, so the trap
    fires on real numbers rather than on a warning. The general treatment of
    that disagreement is P05's, by its brief; F9 owns the identity that says
    exactly when it cannot happen.

WHAT F9 DELIBERATELY DOES NOT DO, because the manifest gives it to somebody
else -- checked against tools/programs.json rather than remembered:

    vector spaces, span, independence, basis, dimension     -> P04
    inner products in general, projection, L1 vs L2,
      the disagreement case worked out, normalising's cost,
      near-orthogonality in high dimension                  -> P05
    broadcasting rules, reshape, axes                       -> P07

STDLIB ONLY, as in F3 to F8. numpy is opened only at the bottom to cross-check
the identity, and it announces itself when absent.

NOT EMITTED, and none of it should be -- a reader who cannot do these in their
head has not read the frames:

    (1,2) + (3,4) = (4,6);  3(1,2) = (3,6);  |(3,4)| = 5.

Run:  python3 code/f09_vectors.py      (or: make numbers)
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


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(k, a):
    return tuple(k * x for x in a)


def unit(a):
    n = norm(a)
    return tuple(x / n for x in a)


def cossim(a, b):
    return dot(a, b) / (norm(a) * norm(b))


# ==========================================================================
# SECTION 3 --- length, and the vector nobody can normalise
#
# |(3,4)| = 5 is in the frames and is not emitted. What IS emitted is the
# three-dimensional case, where the reader has to see Pythagoras applied
# twice, and the length of a 768-component vector of ones, which is the frame
# that makes "the arithmetic does not care about the dimension" concrete.
# ==========================================================================
emit("f09.len3d", norm((2.0, 3.0, 6.0)), 0)
assert norm((2.0, 3.0, 6.0)) == 7.0, "2-3-6 is no longer a Pythagorean triple in 3-D"

D_EMBED = 768
emit("f09.dim", D_EMBED)
emit("f09.len.ones", math.sqrt(D_EMBED), 2)

# The zero vector has no direction, and the operation that reveals it is
# normalising. Stated as the exception it is, because a reader WILL write this.
try:
    unit((0.0, 0.0))
except ZeroDivisionError:
    ZERO_NOTE = "ZeroDivisionError"
else:                                                        # pragma: no cover
    raise AssertionError("normalising the zero vector no longer raises")

# ==========================================================================
# SECTION 4 --- the triangle inequality, and where the reader's arithmetic
# goes wrong
#
# |a + b| <= |a| + |b|, with equality exactly when the two point the same way.
# The frames elicit "add the lengths", so the gap is the number that matters.
# ==========================================================================
TA, TB = (3.0, 0.0), (0.0, 4.0)
emit("f09.tri.sum", norm(TA) + norm(TB), 0)
emit("f09.tri.actual", norm(add(TA, TB)), 0)
assert norm(add(TA, TB)) < norm(TA) + norm(TB), "the triangle inequality is no longer strict here"

# Equality holds exactly when one is a non-negative multiple of the other, and
# the assertion is the INVARIANT rather than the two figures above: no pair
# anywhere may break the inequality, and a parallel pair must meet it exactly.
_worst_slack = 0.0
for _i in range(-12, 13):
    for _j in range(-12, 13):
        for _k in range(-12, 13):
            for _l in range(-12, 13):
                _u, _v = (_i / 3.0, _j / 3.0), (_k / 3.0, _l / 3.0)
                assert norm(add(_u, _v)) <= norm(_u) + norm(_v) + 1e-12
for _t in range(1, 40):
    _u = (1.0, 2.0)
    _v = scale(_t / 7.0, _u)
    _worst_slack = max(_worst_slack, abs(norm(add(_u, _v)) - (norm(_u) + norm(_v))))
emit("f09.tri.parallel.err", f"{_worst_slack:.1e}")
assert _worst_slack < 1e-13, "parallel vectors no longer meet the triangle inequality exactly"

# ==========================================================================
# SECTION 5 --- THE BRIDGE: |a - b|^2 = |a|^2 + |b|^2 - 2 (a . b)
#
# This is F8's a.b = |a||b|cos(theta) rearranged, and it is the identity the
# whole of section 5 rests on. Swept rather than shown at a point.
# ==========================================================================
_worst_law = 0.0
for _i in range(-20, 21):
    for _j in range(-20, 21):
        for _k in range(-20, 21):
            _a = (_i / 4.0, _j / 4.0)
            _b = (_k / 4.0, 1.0 + _k / 9.0)
            lhs = norm(sub(_a, _b)) ** 2
            rhs = norm(_a) ** 2 + norm(_b) ** 2 - 2.0 * dot(_a, _b)
            _worst_law = max(_worst_law, abs(lhs - rhs))
emit("f09.law.err", f"{_worst_law:.1e}")
assert _worst_law < 1e-12, "the law of cosines in vector form no longer holds"

# On the UNIT SPHERE the identity collapses to |a - b|^2 = 2 - 2 cos(theta),
# so distance is a strictly decreasing function of the cosine and the two
# measures cannot rank differently. Both halves are swept.
_worst_unit = 0.0
for _i in range(0, 240):
    for _j in range(0, 240, 7):
        _a = (math.cos(_i / 38.0), math.sin(_i / 38.0))
        _b = (math.cos(_j / 38.0), math.sin(_j / 38.0))
        _worst_unit = max(_worst_unit,
                          abs(norm(sub(_a, _b)) ** 2 - (2.0 - 2.0 * cossim(_a, _b))))
emit("f09.unit.err", f"{_worst_unit:.1e}")
assert _worst_unit < 1e-12, "on the unit sphere the distance is no longer 2 - 2 cos"

# The consequence, asserted as the RANKING it is: over many random-ish triples
# of unit vectors, whichever of two candidates is nearer by distance is also
# the more similar by cosine. This is the property the frames claim, so this is
# what is checked -- not the two numbers a particular triple happens to give.
_checked = 0
for _q in range(0, 120):
    for _m in range(0, 120, 11):
        for _n in range(0, 120, 13):
            if _m == _n:
                continue
            _query = (math.cos(_q / 19.0), math.sin(_q / 19.0))
            _c1 = (math.cos(_m / 19.0), math.sin(_m / 19.0))
            _c2 = (math.cos(_n / 19.0), math.sin(_n / 19.0))
            _d1, _d2 = norm(sub(_query, _c1)), norm(sub(_query, _c2))
            _s1, _s2 = cossim(_query, _c1), cossim(_query, _c2)
            if abs(_d1 - _d2) > 1e-9:
                assert (_d1 < _d2) == (_s1 > _s2), "unit vectors now rank differently"
                _checked += 1
emit("f09.rank.checked", _checked)

# ==========================================================================
# The disagreement, off the sphere. ONE concrete triple, because the frame
# needs the reader to compute it and be wrong; the general case is P05's.
#
# The query points along (1, 0). Candidate A points almost the same way but is
# short; candidate B points less the same way but has close to the query's own
# length, so it lands nearer in the plane.
# ==========================================================================
QUERY = (1.0, 0.0)
CAND_A = (0.30, 0.06)                       # nearly the same direction, short
CAND_B = (0.95, 0.45)                       # further round, but a similar size
for _tag, _c in (("a", CAND_A), ("b", CAND_B)):
    emit(f"f09.dis.cos.{_tag}", cossim(QUERY, _c), 4)
    emit(f"f09.dis.dist.{_tag}", norm(sub(QUERY, _c)), 4)
assert cossim(QUERY, CAND_A) > cossim(QUERY, CAND_B), "A is no longer the more similar"
assert norm(sub(QUERY, CAND_A)) > norm(sub(QUERY, CAND_B)), "B is no longer the nearer"

# And the same two candidates NORMALISED, where by the identity above the
# disagreement is impossible. This is the frame's payoff, so it is asserted.
_ua, _ub = unit(CAND_A), unit(CAND_B)
emit("f09.dis.ndist.a", norm(sub(QUERY, _ua)), 4)
emit("f09.dis.ndist.b", norm(sub(QUERY, _ub)), 4)
assert norm(sub(QUERY, _ua)) < norm(sub(QUERY, _ub)), "normalising no longer settles it"

# ==========================================================================
# SECTION 6 --- the picture runs out, and the arithmetic does not
#
# The operations cost one pass over the components whatever the dimension.
# What stops at three is the drawing. The figure the frames quote is the
# number of components an embedding of this size has against the number a
# reader can draw.
# ==========================================================================
DRAWABLE = 3
emit("f09.drawable", DRAWABLE)
emit("f09.undrawn", D_EMBED - DRAWABLE)

# ==========================================================================
# A second implementation, for the identity the program rests on.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the identity was NOT cross-checked"
else:
    _rng = _np.random.default_rng(0)
    _A = _rng.normal(size=(500, 5))
    _B = _rng.normal(size=(500, 5))
    _lhs = ((_A - _B) ** 2).sum(axis=1)
    _rhs = (_A ** 2).sum(axis=1) + (_B ** 2).sum(axis=1) - 2.0 * (_A * _B).sum(axis=1)
    assert _np.allclose(_lhs, _rhs, atol=1e-10)
    NUMPY_NOTE = (f"numpy {_np.__version__}: |a-b|^2 = |a|^2 + |b|^2 - 2 a.b "
                  f"cross-checked on 500 pairs in five dimensions")

# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f09.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f09_vectors.py --- do not edit.",
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
    print(f"  normalising the zero vector: {ZERO_NOTE}")
    print(f"  unit-sphere ranking agreed on {_checked} comparisons")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
