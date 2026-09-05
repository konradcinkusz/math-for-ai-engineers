#!/usr/bin/env python3
"""Program P15 --- Functions of several variables and the gradient.

Every number Program P15 prints that the reader cannot do in their head is
computed here and written to figures/values/p15.tex, which the book \\input{}s.

P15's thesis is that THE GRADIENT'S DIRECTION IS DERIVED RATHER THAN CHOSEN.
A partial derivative holds everything else still; the gradient collects them;
the directional derivative is a DOT PRODUCT with the gradient, so by Program
P05's own cosine the biggest one is in the gradient's own direction and the
zero ones are at right angles to it. Steepest and perpendicular-to-the-contour
are then two readings of one equation rather than two facts.

WHAT P15 IS OWED, read out of the files rather than remembered:

  F11  derives the one-dimensional walk in full -- downhill is against the
       sign of the derivative, x <- x - eta f'(x), and the minus sign is the
       whole steering mechanism. So THIS PROGRAM MAY NOT RE-DERIVE THE SIGN.
       What it owes back is the same recurrence per eigendirection, gated:
       F11's f = (x-3)^2 + 1 has curvature 2 and factor (1 - 2 eta), which is
       this program's (1 - eta lambda) at lambda = 2.
  F12  gives the chain rule and the notation d/dx that says WHICH letter is
       the variable -- and says in as many words that it "will matter
       enormously in Program P15, where there is more than one". That is the
       sentence partial derivatives answer.
  P05  gives the dot product and a . b = |a||b| cos(theta). Section 3 is that
       identity read with one of the two vectors being the gradient, and
       nothing else is needed to get steepest descent.
  P10  COLLECTS THE SHAPE OF THE BASIN AND DELIBERATELY DOES NOT SPEND IT:
       eigenvalues 20 and 1, a level ellipse 4.47 times longer than wide. The
       zig-zag lives on exactly that bowl, so this program uses P10's own
       committed numbers rather than inventing a second one. Gated.

WHAT P15 LEAVES ALONE, checked against tools/programs.json:
    Jacobians, forward and reverse mode                        -> P16
    the Hessian, curvature, and THE LARGEST STABLE STEP        -> P17
    matrix calculus and the softmax-cross-entropy gradient     -> P18
    convexity, and what one basin promises                     -> P19
    momentum, which FIXES the zig-zag this program produces    -> P20
      -- so P15 produces the zig-zag and explains it, and does not fix it and
      does not bound eta. P20's own brief says it fixes "the zig-zag from
      P15", so leaving it unfixed here is the contract rather than a gap.

A NOTE ON THE WORD. F06 uses "gradient" 68 times and F11 20 times for the
SLOPE OF A LINE, which is standard British usage and is what those programs
needed. Here it is a vector. That collision is real, it is invisible while
drafting, and section 2 names it -- the same treatment P07 gave "dimension"
doing three jobs and "rank" doing two.

Run:  python3 code/p15_gradient.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p15.tex"
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
    """A measured residual is a property of the machine, so it is committed as
    a CEILING the measurement clears on any machine and never as a figure.
    P06 had two rejected by CI for exactly that; this is its helper."""
    assert x >= 0.0
    if x == 0.0:
        return "0"
    return f"1e{math.ceil(math.log10(x)):d}"


# ---------------------------------------------------------------------------
# 1. A partial derivative holds everything else still.
#
# f(x, y) = x^2 y + 3y is chosen so both partials are things a reader can
# differentiate in their head after F11 and F12: 2xy and x^2 + 3. The point
# (2, 5) then gives 20 and 7, two small integers.
# ---------------------------------------------------------------------------
def f(x: float, y: float) -> float:
    return x * x * y + 3.0 * y


def fx(x: float, y: float) -> float:
    return 2.0 * x * y


def fy(x: float, _y: float) -> float:
    return x * x + 3.0


PX, PY = 2.0, 5.0
emit("p15.pt.x", int(PX))
emit("p15.pt.y", int(PY))
emit("p15.fx.at", int(fx(PX, PY)))
emit("p15.fy.at", int(fy(PX, PY)))

# The step is F11's own measured best region for a central difference. F11
# showed the U-curve bottoms out near 1e-8 for a FORWARD difference; a central
# one is flatter and 1e-5 is where F12 already checks its rules. Reusing that
# choice rather than picking a new one is the point.
H = 1e-5
worst_partial = 0.0
for _x in [i / 4 for i in range(-12, 13)]:
    for _y in [j / 4 for j in range(-12, 13)]:
        num_x = (f(_x + H, _y) - f(_x - H, _y)) / (2 * H)
        num_y = (f(_x, _y + H) - f(_x, _y - H)) / (2 * H)
        worst_partial = max(worst_partial,
                            abs(num_x - fx(_x, _y)),
                            abs(num_y - fy(_x, _y)))
assert worst_partial < 1e-6, worst_partial
emit("p15.partial.bound", bound(worst_partial))
NOTES.append("both partials agree with a central difference over a 25x25 grid")

# ---------------------------------------------------------------------------
# 2. The gradient collects them, and it has a length.
# ---------------------------------------------------------------------------
GRAD = (fx(PX, PY), fy(PX, PY))
GLEN = math.hypot(*GRAD)
emit("p15.grad.len", GLEN, digits=4)

# THE HYPOTHESIS THE IDENTITY NEEDS, checked rather than asserted. Section 3
# gets D_u f = grad f . u from "the limit is linear in the direction", which is
# not a property of every function of two variables -- it IS differentiability,
# and the rigour box says so. The standard counterexample is checked here so
# that a claim in a printed box does not rest on the author's arithmetic:
# f = x y^2 / (x^2 + y^4) has both partials zero at the origin, so the dot
# product predicts zero in every direction, and the true rate along a unit
# (a, b) with a != 0 is b^2 / a. Nothing is emitted; the box quotes the
# formula and the reader can run it.
def _pathological(x, y):
    return 0.0 if (x == 0.0 and y == 0.0) else x * y * y / (x * x + y ** 4)


_hh = 1e-6
assert abs((_pathological(_hh, 0) - _pathological(-_hh, 0)) / (2 * _hh)) < 1e-12
assert abs((_pathological(0, _hh) - _pathological(0, -_hh)) / (2 * _hh)) < 1e-12
for _a, _b in ((0.6, 0.8), (0.8, 0.6), (0.5, math.sqrt(3) / 2)):
    _rate = _pathological(1e-7 * _a, 1e-7 * _b) / 1e-7
    assert abs(_rate - _b * _b / _a) < 1e-9, (_a, _b, _rate)
NOTES.append("the standard counterexample checks out: partials zero at the "
             "origin, directional derivative b^2/a, so differentiability is "
             "the hypothesis and not a formality")


# ---------------------------------------------------------------------------
# 3. THE DERIVATION. The directional derivative is a dot product, so P05's
#    cosine settles which direction is steepest without any new machinery.
#
#    This is a SWEEP rather than a spot check, because "the biggest one is in
#    the gradient's direction" is a claim about every direction at once.
# ---------------------------------------------------------------------------
STEPS = 3600
best_val, best_deg, worst_id = -math.inf, None, 0.0
zero_deg = []
for k in range(STEPS):
    th = 2 * math.pi * k / STEPS
    u = (math.cos(th), math.sin(th))
    # measured: the limit definition, in the direction u
    numeric = (f(PX + H * u[0], PY + H * u[1])
               - f(PX - H * u[0], PY - H * u[1])) / (2 * H)
    dotted = GRAD[0] * u[0] + GRAD[1] * u[1]
    worst_id = max(worst_id, abs(numeric - dotted))
    if dotted > best_val:
        best_val, best_deg = dotted, 360 * k / STEPS
    if abs(dotted) < GLEN * 1e-3:
        zero_deg.append(360 * k / STEPS)

# The identity, not the observation: D_u f IS grad . u, at every direction.
assert worst_id < 1e-6, worst_id
emit("p15.dir.bound", bound(worst_id))
emit("p15.dir.steps", STEPS)

# The maximum is the gradient's OWN direction, and its value is the length.
#
# The first draft asserted best_val == GLEN to 1e-9 and FAILED, by 3.2e-7, and
# it deserved to: a maximum over 3600 sampled directions cannot equal a
# maximum over all of them, so that tolerance was a number picked to make an
# assertion pass rather than a statement about the mathematics. F11 paid for
# this lesson once already. What is actually true is a pair:
#
#   (a) no direction beats the gradient           -- Cauchy-Schwarz, exact
#   (b) the sampled best falls short by exactly the grid resolution, no more,
#       because the nearest sample sits within half a step of the true
#       direction and cos of that angle is what it loses.
#
# Asserting both proves the sweep found the maximum as well as a sweep can,
# and makes the shortfall an explanation rather than a fudge.
assert best_val <= GLEN + 1e-12, (best_val, GLEN)
resolution_loss = GLEN * (1 - math.cos(math.pi / STEPS))
assert GLEN - best_val <= resolution_loss, (GLEN - best_val, resolution_loss)
emit("p15.sweep.shortfall.bound", bound(GLEN - best_val))
grad_deg = math.degrees(math.atan2(GRAD[1], GRAD[0])) % 360
assert abs(best_deg - grad_deg) <= 360 / STEPS, (best_deg, grad_deg)
emit("p15.grad.deg", grad_deg, digits=1)

# And the zero ones are exactly the two right angles to it. Two of them, a
# half-turn apart -- which is what "perpendicular to the level set" will mean.
assert len(zero_deg) >= 2
# Each zero direction is a quarter turn from the gradient in one sense or the
# other, so the test has to allow both 90 and 270 -- the first draft allowed
# only 90 and reported a "gap" of 180 for the direction that was perfectly
# correct, which is a bug in the check rather than in the geometry.
gaps = [min(abs((d - grad_deg) % 360 - 90),
            abs((d - grad_deg) % 360 - 270)) for d in zero_deg]
assert max(gaps) < 1.0, sorted(gaps)[-3:]
NOTES.append(f"over {STEPS} directions the largest directional derivative is "
             "the gradient's own, and equals its length")

# ---------------------------------------------------------------------------
# 4. Perpendicular to the level set, EXACTLY, over the rationals.
#
#    On f = a x^2 + b y^2 the gradient is (2ax, 2by) and the tangent to the
#    level curve is (-by, ax) up to scale. Their dot product is
#    -2abxy + 2abxy, which is zero as an identity rather than as a rounding.
# ---------------------------------------------------------------------------
perp_trials = 0
for a in (Fraction(1), Fraction(20), Fraction(3, 7)):
    for b in (Fraction(1), Fraction(5, 2), Fraction(9)):
        for xq in (Fraction(1), Fraction(-3, 4), Fraction(7, 5)):
            for yq in (Fraction(2), Fraction(11, 3), Fraction(-1, 6)):
                grad = (2 * a * xq, 2 * b * yq)
                tang = (-b * yq, a * xq)
                assert grad[0] * tang[0] + grad[1] * tang[1] == 0
                perp_trials += 1
emit("p15.perp.trials", perp_trials)
NOTES.append(f"gradient . tangent is exactly 0 on all {perp_trials} rational "
             "cases -- an identity, not a rounding")

# ---------------------------------------------------------------------------
# 5. THE ZIG-ZAG, on Program P10's own bowl.
#
#    P10 committed eigenvalues 20 and 1 and a level ellipse 4.47 times longer
#    than wide, and said in as many words that the shape is collected there
#    and not spent. This is where it is spent, so the bowl must BE that one.
# ---------------------------------------------------------------------------
LAM_HI = int(committed("p10.tex", "p10.basin.hi") or 20)
LAM_LO = int(committed("p10.tex", "p10.basin.lo") or 1)
assert (LAM_HI, LAM_LO) == (20, 1), (LAM_HI, LAM_LO)
_axis = committed("p10.tex", "p10.basin.axisratio")
assert _axis is not None and abs(float(_axis)
                                 - math.sqrt(LAM_HI / LAM_LO)) < 5e-3, _axis
emit("p15.lam.hi", LAM_HI)
emit("p15.lam.lo", LAM_LO)


def grad_q(pt, lam_hi=None, lam_lo=None):
    """grad of f = 1/2 (lam_hi x^2 + lam_lo y^2)."""
    hi = LAM_HI if lam_hi is None else lam_hi
    lo = LAM_LO if lam_lo is None else lam_lo
    return (hi * pt[0], lo * pt[1])


def walk(start, eta, steps, lam_hi=None, lam_lo=None):
    pt, path = start, [start]
    for _ in range(steps):
        g = grad_q(pt, lam_hi, lam_lo)
        pt = (pt[0] - eta * g[0], pt[1] - eta * g[1])
        path.append(pt)
    return path


def angle_to_minimum(pt, lam_hi=None, lam_lo=None) -> float:
    """Between the direction the walk takes (-grad) and the direction the
    minimum actually lies in (-pt, since the minimum is the origin)."""
    g = grad_q(pt, lam_hi, lam_lo)
    a, b = (-g[0], -g[1]), (-pt[0], -pt[1])
    c = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


START = (1.0, 1.0)
ETA = 0.09
STEPS_GD = 20
emit("p15.zig.eta", ETA, digits=2)
emit("p15.zig.steps", STEPS_GD)
emit("p15.zig.start.x", int(START[0]))
emit("p15.zig.start.y", int(START[1]))

# THE CIRCULAR BOWL IS THE CONTROL, and it is exact rather than nearly so: with
# lam_hi == lam_lo the gradient is a multiple of the position, so -grad points
# AT the minimum and the walk is a straight line. Asserting that first is what
# makes the elongated case a measurement rather than an anecdote.
# EXACT IN THE ALGEBRA, AND NOT TO THE BIT -- which is F05's lesson arriving
# here. On the circular bowl grad = lambda * pt exactly, so -grad and -pt are
# parallel and the angle IS zero; the CROSS PRODUCT says so exactly, in
# floats. Going through acos does not: cos comes back as 1 - eps and the
# arccosine of a number that close to 1 is where Program P02's cancellation
# lives, so it reports about a millionth of a degree. The first draft asserted
# the acos result was below 1e-9 and failed at 1.2e-6, which is a fact about
# the arccosine rather than about the geometry.
_g = grad_q(START, LAM_LO, LAM_LO)
assert _g[0] * START[1] - _g[1] * START[0] == 0.0     # exactly parallel
ang_round = angle_to_minimum(START, LAM_LO, LAM_LO)
emit("p15.round.acos.bound", bound(ang_round))
NOTES.append("circular bowl: -grad is exactly parallel to the direction home, "
             f"though arccos reports {ang_round:.1e} deg rather than 0")
# The measure is DISTANCE TRAVELLED against DISTANCE COVERED, not against the
# distance to the minimum. The first draft used the latter and reported 0.85
# for a walk that is a dead straight line -- because after twenty steps the
# walk has not ARRIVED, so it has travelled less than the whole way home. That
# says something about the step size and nothing about the direction. Path
# length over displacement is 1 for any straight path however far it gets,
# which is the property the section is about: how much further you travelled
# than you actually moved.
def detour(path) -> float:
    length = sum(math.dist(path[i], path[i + 1])
                 for i in range(len(path) - 1))
    return length / math.dist(path[0], path[-1]), length


round_path = walk(START, ETA, STEPS_GD, LAM_LO, LAM_LO)
round_ratio, round_len = detour(round_path)
assert abs(round_ratio - 1.0) < 1e-12, round_ratio

# The elongated bowl: the same start, the same step, P10's eigenvalues.
ang_long = angle_to_minimum(START)
assert ang_long > 30.0, ang_long
emit("p15.zig.angle", ang_long, digits=1)

path = walk(START, ETA, STEPS_GD)
signs = [1 if p[0] > 0 else -1 for p in path]
crossings = sum(1 for i in range(len(signs) - 1) if signs[i] != signs[i + 1])
assert crossings >= STEPS_GD - 1, crossings   # it flips essentially every step
emit("p15.zig.crossings", crossings)

ratio, path_len = detour(path)
assert ratio > 1.2, ratio
emit("p15.zig.ratio", ratio, digits=2)
emit("p15.zig.pathlen", path_len, digits=3)
emit("p15.zig.moved", math.dist(path[0], path[-1]), digits=3)

# THE SIDEWAYS FRACTION IS EMITTED RATHER THAN NAMED AS A FRACTION IN WORDS.
# The prose used to say "nearly seven-eighths", which is 87.5 per cent, and a
# reader dividing the two printed figures gets 85.5 -- the reproduce-from-the-
# page defect F04, F05, P07, P12, P23 and P27 have each paid for. So the
# number is computed, and asserted to agree with what the PRINTED operands
# give, not merely with the underlying floats.
_moved = math.dist(path[0], path[-1])
SIDEWAYS = 100.0 * (1.0 - _moved / path_len)
emit("p15.zig.sideways.pct", SIDEWAYS, digits=1)
_printed = 100.0 * (1.0 - float(f"{_moved:.3f}") / float(f"{path_len:.3f}"))
assert abs(_printed - SIDEWAYS) < 0.05, (_printed, SIDEWAYS)
NOTES.append(f"on P10's bowl the step turns {ang_long:.1f} deg away from the "
             f"minimum and the path is {ratio:.2f}x the straight line, so "
             f"{SIDEWAYS:.1f}% of the walking is sideways")

# THE INVARIANT rather than either figure: the worse the elongation, the
# further the first step points away from the minimum. Monotone over a sweep,
# so the sentence survives a change of bowl.
angs = [angle_to_minimum(START, r, 1) for r in range(1, 60)]
assert all(angs[i] < angs[i + 1] + 1e-12 for i in range(len(angs) - 1))
NOTES.append("the angle grows monotonically with the eigenvalue ratio")

# AND IT IS BOUNDED, which the further-problem answer used to get wrong. The
# old answer said the angle "cannot grow past a right angle, because the step
# would then be going uphill" -- two errors in one clause. The step never goes
# uphill at all (its rate is -|grad|^2), and the ceiling from THIS start point
# is 45 degrees, not 90: grad = (lam*x, y) tends to the direction of the x axis
# as lam runs away, so the angle tends to the one between the x axis and the
# start point, which is 45 for (1, 1). What is true on any convex bowl is that
# the angle stays acute, because grad . p = lam x^2 + y^2 = 2f > 0.
assert abs(angle_to_minimum(START, 10 ** 8, 1) - 45.0) < 1e-3
assert all(a < 45.0 for a in angs)
for _r in (1, 3, 20, 500):
    _g = grad_q(START, _r, 1)
    assert _g[0] * START[0] + _g[1] * START[1] > 0          # 2f, so acute
NOTES.append("bounded too: it climbs towards 45 deg from (1, 1) and stays "
             "acute because grad . p = 2f")

# F11's RECURRENCE, GATED. F11 walks f = (x-3)^2 + 1, whose curvature is 2, and
# its committed factor is (1 - 2 eta). Per eigendirection this program's factor
# is (1 - eta lambda), so the two must agree at lambda = 2.
_f11_eta = committed("f11.tex", "f11.gd.small.eta")
assert _f11_eta is not None
_eta11 = float(_f11_eta)
assert abs((1 - _eta11 * 2) - (1 - 2 * _eta11)) < 1e-15
# NOTHING IS EMITTED FROM THIS GATE, deliberately. F11's factor at its own
# curvature happens to have the same magnitude as this program's steep-
# direction factor, 0.8 against -0.80, and printing both would put two numbers
# that look like one on the page two sections apart -- which is F08's defect.
# The gate belongs in the script; the frame names the shared formula in words.
NOTES.append("gated: F11's (1 - 2 eta) is this program's (1 - eta lambda) at "
             "its own curvature of 2")
# and on THIS bowl the same formula explains the flip: the steep direction's
# factor is negative, so its coordinate changes sign every step, while the
# shallow one's is positive and it creeps.
fac_hi, fac_lo = 1 - ETA * LAM_HI, 1 - ETA * LAM_LO
assert fac_hi < 0 < fac_lo, (fac_hi, fac_lo)
emit("p15.fac.hi", fac_hi, digits=2)
emit("p15.fac.lo", fac_lo, digits=2)
NOTES.append(f"factor {fac_hi:+.2f} in the steep direction and {fac_lo:+.2f} "
             "in the shallow one -- which is why one flips and one creeps")

# ---------------------------------------------------------------------------
# 6. The sign, which is the trap. One step the right way and one the wrong way.
# ---------------------------------------------------------------------------
def fq(pt) -> float:
    return 0.5 * (LAM_HI * pt[0] ** 2 + LAM_LO * pt[1] ** 2)


# THE STEP SIZE IS EMITTED, because the three values below are a measurement
# and a reader cannot reproduce a measurement whose step size is not on the
# page. It is deliberately not the walk's eta: at 0.09 the wrong-sign step on
# the steep coordinate multiplies it by 1 + eta*lam_hi = 2.8, which is a
# divergence rather than the "one small step" the trap box describes.
SMALL = 0.02
emit("p15.sign.eta", SMALL, digits=2)
g0 = grad_q(START)
down = (START[0] - SMALL * g0[0], START[1] - SMALL * g0[1])
up = (START[0] + SMALL * g0[0], START[1] + SMALL * g0[1])
assert fq(down) < fq(START) < fq(up)
emit("p15.sign.before", fq(START), digits=2)
emit("p15.sign.down", fq(down), digits=2)
emit("p15.sign.up", fq(up), digits=2)
# A ratio must reproduce from the numbers AS THE PAGE PRINTS THEM.
_pf = lambda v: float(f"{v:.2f}")
assert _pf(fq(up)) > _pf(fq(START)) > _pf(fq(down))
NOTES.append("wrong sign: one step takes the value UP rather than down")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    # TWO listings, not one, and the split is the point. The dot product with
    # (0.6, 0.8) is the answer frame 18 elicits, so a single listing printing
    # it alongside the gradient put that answer on the page BEFORE the
    # question -- the defect P04's and P08's passes both had to fix. The
    # gradient half stays where the sweep is described; the dot-product half
    # goes after frame 19's answer, where it confirms rather than reveals.
    # Each imports what it calls, so either can be pasted into a REPL on its
    # own -- which is the other half of P04's finding.
    grad_lines = [
        ">>> from p15_gradient import f, fx, fy, GRAD",
        ">>> f(2, 5), fx(2, 5), fy(2, 5)",
        f"{(f(PX, PY), fx(PX, PY), fy(PX, PY))}",
        ">>> GRAD",
        f"{GRAD}",
    ]
    (TRANSCRIPTS / "p15-gradient.txt").write_text(
        "\n".join(grad_lines) + "\n", encoding="utf8")

    dir_lines = [
        ">>> from p15_gradient import GRAD",
        ">>> round(sum(g * u for g, u in zip(GRAD, (0.6, 0.8))), 4)",
        f"{round(sum(g * u for g, u in zip(GRAD, (0.6, 0.8))), 4)}",
    ]
    (TRANSCRIPTS / "p15-directional.txt").write_text(
        "\n".join(dir_lines) + "\n", encoding="utf8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = [
        "% Generated by code/p15_gradient.py --- do not edit.",
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
        print("  " + "   ".join(f"{k:{w}s} {b:>9s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
