#!/usr/bin/env python3
"""Program P22 --- Constrained optimisation and Lagrange multipliers.

Every number Program P22 prints that the reader cannot do in their head is
computed here and written to figures/values/p22.tex, which the book \\input{}s.

P22's thesis is that A LAGRANGE MULTIPLIER IS A PRICE: how much objective you
buy per unit of constraint relaxed. Read that way it stops being a device for
solving a class of exercise and becomes a number with units that appears, under
other names, in every objective anybody trains.

WHAT P22 IS OWED, read out of the files rather than remembered:

  P15  owns the gradient and, in its own section 4, the fact that the gradient
       is PERPENDICULAR TO THE CONTOUR -- derived from P05's cosine rather than
       drawn. That is the whole geometric content of "at a constrained optimum
       the two gradients are parallel", so this program does not re-derive it;
       it reads the same sentence about two functions instead of one.
  P19  owns convexity, so "the constrained optimum is THE optimum" has its
       condition already, and the honest hedge for the non-convex case is
       written there rather than here.
  P05  owns PROJECTION ONTO A SUBSPACE in full, including that the answer is
       the closest point rather than merely a point. Projection is one of the
       two ways to enforce a constraint, so it arrives here as an object the
       reader has rather than as a new construction.
  P17  owns the second-order picture, and P20 owns the optimisers, so nothing
       here has to say how the constrained problem is actually solved.

THE DECLARED FORWARD REFERENCE. The payoff is stated for a KL-penalised
objective and KL is not defined until P30. The manifest gives two routes and
says it may not be left undeclared; this program takes P18's route -- state the
one fact the payoff needs in the Learning outcomes with a pointer:

    KL is a non-negative measure of how far one distribution sits from
    another, and it is zero only when they agree.

Nothing else about it is used, and P30 defines it properly.

TWO MEASUREMENTS, both free and both EXACT where exactness is available.

  1. THE PRICE IS THE DERIVATIVE, over the rationals. For a quadratic under a
     linear constraint the multiplier equals d f* / dc at every level c, and a
     central difference over Fraction is exact because a quadratic's third
     derivative is zero. So "price" is an identity rather than an analogy.
  2. BETA IS AN EXCHANGE RATE. For the KL-penalised objective the solution is
     the tilted distribution p ∝ q exp(r/beta), and d E_p[r] / d KL(p||q)
     equals beta. That is the same reading in the setting people actually meet
     it in, and it turns beta from a tuning knob into reward per nat.

Run:  python3 code/p22_constrained_optimisation.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p22.tex"
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


def bound(x: float, ceiling: float) -> str:
    """Commit the CEILING the caller states and check the measurement clears
    it -- Program P20's correction to P06's rule."""
    assert 0.0 <= x < ceiling, (x, ceiling)
    return f"1e{round(math.log10(ceiling)):d}"


# ---------------------------------------------------------------------------
# 1. THE STATIONARITY CONDITION, on a problem small enough to solve by hand.
#
#     minimise  f(x, y) = x^2 + 2 y^2      subject to   g(x, y) = x + y = c
#
# grad f = (2x, 4y) and grad g = (1, 1), and the condition is that they are
# parallel: grad f = lambda grad g. Everything below is over Fractions, so the
# whole section is exact and the word "exactly" is earned.
# ---------------------------------------------------------------------------
A, B = Fraction(1), Fraction(2)            # f = A x^2 + B y^2


def solve(c: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Stationary point of f on the line x + y = c, with its multiplier.
    2Ax = lam and 2By = lam and x + y = c give lam directly."""
    lam = Fraction(2, 1) * A * B * c / (A + B)
    x = lam / (2 * A)
    y = lam / (2 * B)
    assert x + y == c, (x, y, c)
    return x, y, lam, A * x * x + B * y * y


C0 = Fraction(3)
X0, Y0, LAM0, F0 = solve(C0)

# The condition itself, checked rather than assumed: the two gradients are
# parallel, which for two dimensions is a determinant that vanishes.
gf = (2 * A * X0, 2 * B * Y0)
gg = (Fraction(1), Fraction(1))
assert gf[0] * gg[1] - gf[1] * gg[0] == 0, gf
assert gf == (LAM0 * gg[0], LAM0 * gg[1]), (gf, LAM0)

emit("p22.c", float(C0), 0)
emit("p22.x", float(X0), 0)
emit("p22.y", float(Y0), 0)
emit("p22.lam", float(LAM0), 0)
emit("p22.fstar", float(F0), 0)
NOTES.append(f"on x + y = {float(C0):.0f} the optimum is "
             f"({float(X0):.0f}, {float(Y0):.0f}) with multiplier "
             f"{float(LAM0):.0f} and value {float(F0):.0f}, and the two "
             "gradients are parallel exactly, over fractions")

# And the constrained answer is WORSE than the unconstrained one, which is what
# a constraint is for and is the sanity check that the problem is not vacuous.
assert F0 > 0, F0
NOTES.append("the unconstrained minimum is 0 at the origin, which the "
             "constraint excludes -- a constraint that changed nothing would "
             "not need a multiplier")


# ---------------------------------------------------------------------------
# 2. THE PRICE, and it is an identity rather than an analogy.
#
# d f* / dc = lambda, at every c. For a quadratic the central difference is
# EXACT -- the error term carries a third derivative and a quadratic has none
# -- so this is checked over Fractions with no tolerance at all.
# ---------------------------------------------------------------------------
H = Fraction(1, 1000)
LEVELS = [Fraction(1), Fraction(2), Fraction(3), Fraction(6)]
price_rows = []
for c in LEVELS:
    slope = (solve(c + H)[3] - solve(c - H)[3]) / (2 * H)
    lam = solve(c)[2]
    assert slope == lam, (c, slope, lam)                # EXACT, no tolerance
    price_rows.append((c, lam, solve(c)[3]))

emit("p22.price.levels", len(LEVELS))
emit("p22.c.lo", float(LEVELS[0]), 0)
emit("p22.c.hi", float(LEVELS[-1]), 0)
emit("p22.lam.lo", float(price_rows[0][1]), 2)
emit("p22.lam.hi", float(price_rows[-1][1]), 0)
emit("p22.fstar.lo", float(price_rows[0][2]), 2)
emit("p22.fstar.hi", float(price_rows[-1][2]), 0)
NOTES.append(f"the multiplier equals d f*/dc EXACTLY at all "
             f"{len(LEVELS)} constraint levels, over fractions, which is what "
             "makes 'price' an identity rather than an analogy")

# One unit of relaxation, priced. Moving c by one changes f* by about lambda,
# and the "about" is the second-order term, which is also exact here.
c1, c2 = Fraction(3), Fraction(4)
gain = solve(c2)[3] - solve(c1)[3]
emit("p22.relax.from", float(c1), 0)
emit("p22.relax.to", float(c2), 0)
emit("p22.relax.gain", float(gain), 2)
emit("p22.relax.lam", float(solve(c1)[2]), 0)
assert gain > solve(c1)[2], (gain, solve(c1)[2])   # curvature makes it more
NOTES.append(f"relaxing c from {float(c1):.0f} to {float(c2):.0f} costs "
             f"{float(gain):.2f} against a multiplier of "
             f"{float(solve(c1)[2]):.0f}: the multiplier is the price of the "
             "FIRST unit and the curvature is what the rest costs")


# ---------------------------------------------------------------------------
# 3. PROJECTION, which is Program P05's object doing the other job.
#
# The constraint set here is a line, and the other way to enforce a constraint
# is to step freely and then project back onto it. The projection of a point
# onto x + y = c is the closest point of the line, which is P05's derivation
# with the line's normal in place of a vector.
# ---------------------------------------------------------------------------
def project(p: tuple[Fraction, Fraction], c: Fraction) -> tuple[Fraction, Fraction]:
    """Closest point of x + y = c to p. Normal is (1,1), so subtract the
    excess spread equally between the coordinates."""
    excess = (p[0] + p[1] - c) / 2
    return (p[0] - excess, p[1] - excess)


P_OFF = (Fraction(5), Fraction(0))
P_ON = project(P_OFF, C0)
assert P_ON[0] + P_ON[1] == C0, P_ON
# and it IS the closest point: any other point of the line is further, checked
# on a sweep rather than asserted, because "closest" is the property that makes
# it a projection at all.
d2 = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
base = d2(P_OFF, P_ON)
for k in range(-20, 21):
    if k == 0:
        continue
    t = Fraction(k, 4)
    other = (P_ON[0] + t, P_ON[1] - t)                  # still on the line
    assert other[0] + other[1] == C0
    assert d2(P_OFF, other) > base, (t, other)
emit("p22.proj.from.x", float(P_OFF[0]), 0)
emit("p22.proj.from.y", float(P_OFF[1]), 0)
# The projection is exact over fractions -- both components are integers here
# -- so it is printed as integers.  "4.0, -1.0" reads as the floating-point
# result of a computation that never touched a float.
assert P_ON[0].denominator == 1 and P_ON[1].denominator == 1, P_ON
emit("p22.proj.to.x", float(P_ON[0]), 0)
emit("p22.proj.to.y", float(P_ON[1]), 0)
emit("p22.proj.tried", 40)
NOTES.append("the projection of (5, 0) onto x + y = 3 is (4, -1), and it beats "
             "40 other points of the same line on distance -- Program P05's "
             "'closest point rather than merely a point', with the line's "
             "normal in place of a vector")

# The distinction the section is for: the projection is the nearest FEASIBLE
# point and it is NOT the constrained optimum. Two different questions.
assert (P_ON[0], P_ON[1]) != (X0, Y0), P_ON
emit("p22.proj.f", float(A * P_ON[0] ** 2 + B * P_ON[1] ** 2), 0)
assert A * P_ON[0] ** 2 + B * P_ON[1] ** 2 > F0
NOTES.append("that projection has objective value 18 against the constrained "
             "optimum's 6, so projecting is a way to STAY feasible and not a "
             "way to be optimal")


# ---------------------------------------------------------------------------
# 4. BETA IS AN EXCHANGE RATE, in the setting people meet it in.
#
#     maximise  E_p[r] - beta * KL(p || q)     over distributions p
#
# The solution is the tilted distribution p ∝ q exp(r/beta), which is stated
# rather than derived (P26 and P30 are better placed). What is MEASURED is the
# reading: d E_p[r] / d KL(p||q) = beta, so beta is reward per nat -- and each
# beta corresponds to one KL level, which is the equivalence between a penalty
# and a hard constraint.
# ---------------------------------------------------------------------------
Q = [0.4, 0.3, 0.2, 0.1]
R = [0.0, 1.0, 2.0, 3.0]
assert abs(sum(Q) - 1.0) < 1e-12


def tilt(beta: float):
    w = [qi * math.exp(ri / beta) for qi, ri in zip(Q, R)]
    z = sum(w)
    p = [wi / z for wi in w]
    kl = sum(pi * math.log(pi / qi) for pi, qi in zip(p, Q))
    return p, kl, sum(pi * ri for pi, ri in zip(p, R))


BETAS = (4.0, 2.0, 1.0, 0.5, 0.25)
kl_rows, last_kl = [], None
for b in BETAS:
    p, kl, er = tilt(b)
    assert abs(sum(p) - 1.0) < 1e-12
    assert kl >= 0.0, kl                      # the one fact P30 is quoted for
    if last_kl is not None:
        assert kl > last_kl, (b, kl, last_kl)  # a smaller beta buys more KL
    last_kl = kl
    kl_rows.append((b, kl, er))

# THE EXCHANGE RATE, measured: the slope of reward against KL along the family
# of solutions is beta itself, at every beta.
worst = 0.0
h = 1e-6
for b in (2.0, 1.0, 0.5):
    _, k1, e1 = tilt(b + h)
    _, k2, e2 = tilt(b - h)
    worst = max(worst, abs((e1 - e2) / (k1 - k2) - b))
assert worst < 1e-4, worst
emit("p22.kl.betas", len(BETAS))
emit("p22.kl.beta.hi", BETAS[0], 0)
emit("p22.kl.beta.lo", BETAS[-1], 2)
emit("p22.kl.hi", kl_rows[0][1], 3)
emit("p22.kl.lo", kl_rows[-1][1], 2)
# THREE decimals, not two, and the reason is the recorded rule rather than
# taste: the frames divide these two to get p22.kl.buy, and at two decimals
# the page prints 1.27 and 2.96, which divide to 133 against an exact 134.
# The assertion below holds the printed forms to the printed answer.
emit("p22.kl.r.hi", kl_rows[0][2], 3)
emit("p22.kl.r.lo", kl_rows[-1][2], 3)
emit("p22.kl.slope.bound", bound(worst, 1e-4))
NOTES.append("the slope of expected reward against KL along the family of "
             f"solutions is beta itself, to better than 1e-4 -- so beta is "
             "reward per nat, and each beta names one KL level, which is the "
             "equivalence between a penalty and a hard constraint")

# The consequence worth stating: beta has UNITS, so a beta carried between two
# reward models means something different in each. Measured as the ratio of
# reward bought at the two ends of the sweep.
assert kl_rows[-1][2] > kl_rows[0][2]
emit("p22.kl.spend", kl_rows[-1][1] / kl_rows[0][1], 0)
emit("p22.kl.buy",
     100 * (kl_rows[-1][2] - kl_rows[0][2]) / kl_rows[0][2], 0)

# The chord between the two printed rows, which is what a reader who divides
# the table gets.  It is not beta: the slope is a local derivative running
# from BETAS[0] down to BETAS[-1], and this average of it sits between them.
_chord = ((kl_rows[-1][2] - kl_rows[0][2])
          / (kl_rows[-1][1] - kl_rows[0][1]))
assert BETAS[-1] < _chord < BETAS[0], (_chord, BETAS)
emit("p22.kl.chord", _chord, 2)

# Both multiples have to reproduce from the table the page prints, not only
# from the floats behind it -- divide the two numbers as the page prints them.
_khi, _klo = float(f"{kl_rows[0][1]:.3f}"), float(f"{kl_rows[-1][1]:.2f}")
_rhi, _rlo = float(f"{kl_rows[0][2]:.3f}"), float(f"{kl_rows[-1][2]:.3f}")
assert (f"{_klo / _khi:.0f}"
        == f"{kl_rows[-1][1] / kl_rows[0][1]:.0f}"), (_khi, _klo)
assert (f"{100 * (_rlo - _rhi) / _rhi:.0f}"
        == f"{100 * (kl_rows[-1][2] - kl_rows[0][2]) / kl_rows[0][2]:.0f}"), (
            _rhi, _rlo)
assert f"{(_rlo - _rhi) / (_klo - _khi):.2f}" == f"{_chord:.2f}", _chord
NOTES.append(f"dropping beta from {BETAS[0]:.0f} to {BETAS[-1]:.2f} spends "
             f"{kl_rows[-1][1]/kl_rows[0][1]:.0f} times the KL to buy "
             f"{100*(kl_rows[-1][2]-kl_rows[0][2])/kl_rows[0][2]:.0f} per cent "
             "more reward, which is what a falling exchange rate looks like")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    lines = [
        ">>> from p22_constrained_optimisation import solve",
        ">>> from fractions import Fraction as F",
        ">>> h = F(1, 1000)",
        ">>> [solve(F(c))[2] for c in (1, 2, 3)]      # lambda",
        f"{[solve(Fraction(c))[2] for c in (1, 2, 3)]}",
        ">>> [(solve(F(c)+h)[3]-solve(F(c)-h)[3])/(2*h)",
        "...  for c in (1, 2, 3)]                     # d f*/dc",
        f"{[(solve(Fraction(c)+H)[3]-solve(Fraction(c)-H)[3])/(2*H) for c in (1,2,3)]}",
    ]
    for line in lines:
        assert len(line) <= 64, (len(line), line)
    (TRANSCRIPTS / "p22-lambda-is-slope.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    out = [
        "% Generated by code/p22_constrained_optimisation.py --- do not edit.",
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
        print("  " + "   ".join(f"{k:{w}s} {b:>10s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
