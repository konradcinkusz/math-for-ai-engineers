#!/usr/bin/env python3
"""Program P05 --- Inner product, norms and projection.

Every number Program P05 prints that the reader cannot do in their head is
computed here and written to figures/values/p05.tex, which the book \\input{}s.

P05's thesis is that AN INNER PRODUCT IS THE ONLY THING THAT GIVES A VECTOR
SPACE ANGLES AND LENGTHS, and that once a space has one, high dimension behaves
in a way two dimensions never prepared anybody for.

WHAT P05 IS OWED, and pays. Four written programs hand it something by name,
and all four were opened rather than remembered:

  F08  gives a.b = |a||b|cos(theta), swept over 3481 pairs. P05 does not
       re-derive it, and F08 says P05 measures the BASELINE that embedding
       anisotropy is a deviation from.
  F09  works the cosine/distance disagreement case IN FULL -- query (1,0),
       A = (0.30, 0.06), B = (0.95, 0.45), A more similar and B nearer. So the
       worked example is SPENT, and P05's brief is wrong to promise it again.
       What F09's trapbox hands forward is narrower and better: WHICH measure
       to prefer when they disagree, and what normalising costs. F09's closing
       table names three claims that "do not transfer" to high dimension and
       defers all three to here:
           how many directions are far apart
           how much of the space is near the middle
           what a "typical" pair of vectors looks like
  P04  stops at a counting theorem and says so: relaxing EXACTLY independent to
       NEARLY independent needs a way to measure "almost", which means angles,
       which is this program's. Its closing frame says P05 "starts by giving
       the space the one thing this program deliberately withheld: a way to
       multiply two vectors and get a number back."

THE MEASUREMENTS, and two of them exist because an assertion failed:

  1. NEAR-ORTHOGONALITY. Two random unit vectors in d dimensions have a cosine
     that concentrates at zero with spread 1/sqrt(d). Asserted as the
     INVARIANT -- the measured spread tracks 1/sqrt(d) -- rather than as any
     one cosine, which is a random variable, and a threshold picked so it
     passes is not an assertion.

  2. P04's RELAXATION, made numeric, via the union bound over the EXACT cosine
     density. Two wrong predictions were caught here; both are written up
     below at the computations that refuted them, and the second is a better
     frame than the claim it replaced.

  3. WHERE THE MASS IS -- F09's "how much of the space is near the middle".
     Computed exactly rather than sampled, because a set of measure 2^-100
     would never be found by sampling and finding nothing proves nothing.

  4. PROJECTION as the closest point in a subspace, checked by search.

  5. WHAT NORMALISING COSTS: it makes cosine and the dot product the same
     query, exactly, and throws away the length, which was carrying something.

WHAT P05 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    matrices as linear maps, multiplication as composition          -> P06
    rank, the four subspaces, least squares, LoRA                   -> P08
    the covariance matrix and PCA                                   -> P10
    SVD, low-rank approximation, conditioning                       -> P11

Run:  python3 code/p05_inner_product_norms.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
import statistics
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p05.tex"
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


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def unit(d, rnd):
    """A uniformly random DIRECTION: Gaussian components, then normalised.

    Sampling each component uniformly from [-1, 1] and normalising does NOT
    give a uniform direction -- it over-weights the cube's corners, and in high
    dimension nearly all of the cube IS corner, so the error grows with exactly
    the quantity this program is measuring. The Gaussian is the only elementary
    construction that is isotropic, because its density depends on the length
    alone.
    """
    v = [rnd.gauss(0.0, 1.0) for _ in range(d)]
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


# ==========================================================================
# 1. Near-orthogonality: F09's "what a typical pair looks like", answered.
#
# THE ASSERTION IS THE INVARIANT, not the observation. The standard deviation
# of the cosine between two random unit vectors in d dimensions is exactly
# 1/sqrt(d), so what is asserted is that the measured spread tracks 1/sqrt(d)
# across three decades of d -- which survives a change of seed, of sample size
# and of the dimensions chosen. Asserting any one measured cosine would not:
# it is a random variable, and F11 paid for the lesson that a threshold picked
# so an assertion passes is not an assertion.
# ==========================================================================
DIMS = (2, 3, 10, 100, 768, 4096)
PAIRS = 4000
SEED = 20260831


# ONE computation, and the transcript at the foot of this file is these two
# functions verbatim. P16 shipped a listing whose numbers described a different
# run from the frames beside it, and no drift gate could see it: make verify
# proves a transcript matches the script that wrote it, and the script wrote
# exactly what it computed. The only arrangement in which the two cannot come
# apart is the one where the page's four numbers ARE the listing's output.
#
# Seeding per dimension rather than sharing one stream is what makes that
# possible: the sweep below visits six dimensions and the listing calls four,
# so with one shared generator the two would draw different samples and agree
# only to within the sampling noise -- which is exactly the third-decimal
# disagreement this pass was opened to fix.
def cosines(d, n=PAIRS):
    rnd = random.Random(SEED + d)
    return [dot(unit(d, rnd), unit(d, rnd)) for _ in range(n)]


def spread(d, n=PAIRS):
    return statistics.pstdev(cosines(d, n))


ORTHO = {}
for _d in DIMS:
    _cos = cosines(_d)
    sd = spread(_d)
    mean_abs = sum(abs(c) for c in _cos) / PAIRS
    within_cos = sum(1 for c in _cos if abs(c) < 0.1) / PAIRS
    within_deg = sum(1 for c in _cos
                     if abs(math.degrees(math.acos(max(-1.0, min(1.0, c)))) - 90.0)
                     < 5.0) / PAIRS
    ORTHO[_d] = (mean_abs, sd, within_cos, within_deg)

# QUOTED is not DIMS: the assertions below sweep every dimension, and only the
# rows the frames actually print are emitted. C7 reports an emitted value that
# nothing references, and F11 established that the fix is to stop emitting it
# rather than to work it into a sentence it does not belong in.
QUOTED = (2, 10, 100, 768)
emit("p05.pairs", PAIRS)
for _d in QUOTED:
    _ma, _sd, _wc, _wd = ORTHO[_d]
    emit(f"p05.cos.sd.{_d}", _sd, 4)

for _d, (_ma, _sd, _wc, _wd) in ORTHO.items():
    predicted = 1.0 / math.sqrt(_d)
    assert abs(_sd - predicted) / predicted < 0.08, (
        f"at d={_d} the cosine spread is {_sd:.4f} against a predicted "
        f"{predicted:.4f}: the concentration this program is about has moved")
_worst = max(abs(sd - 1 / math.sqrt(d)) / (1 / math.sqrt(d))
             for d, (_, sd, _, _) in ORTHO.items())
emit("p05.sd.err.pct", 100 * _worst, 1)

_sds = [ORTHO[d][1] for d in DIMS]
assert all(a > b for a, b in zip(_sds, _sds[1:])), (
    "the cosine spread is not falling monotonically in d, which is the claim "
    "the whole of section 5 rests on")
NOTES.append(f"cosine spread tracks 1/sqrt(d) to within {100 * _worst:.1f}% "
             f"over d = {DIMS[0]} to {DIMS[-1]}")
NOTES.append(f"within 5 degrees of a right angle: {round(100*ORTHO[2][3])}% of "
             f"pairs in the plane, {round(100*ORTHO[768][3])}% at d=768")


# ==========================================================================
# 2. P04's relaxation, made numeric -- and TWO wrong predictions, both caught
#    here before any prose was written for them.
#
# WRONG PREDICTION ONE. The draft drew random directions and kept each one
# whose cosine against every kept direction was under a tolerance, asserting
# that more than d would fit. At d = 64, tolerance 0.2, it kept FORTY-FIVE --
# fewer than the sixty-four that are EXACTLY orthogonal. Greedy acceptance
# decays like p^k as the kept set grows, so the search stalls long before the
# geometry does: it measures the search and not the space. Wrong construction,
# and no amount of tuning would have made it right.
#
# What IS computable is the UNION BOUND: draw n random directions and the
# expected number of pairs closer than the tolerance is C(n,2) P(|cos| > tol).
# Solve for the n at which that first reaches one and you have the capacity as
# a number rather than as a search result. P(|cos| > tol) comes from the EXACT
# density of the cosine between two random unit vectors, which is proportional
# to (1 - c^2)^((d-3)/2) -- integrated numerically, then CHECKED against the
# sampled fractions from part 1, which is what makes the integral trustworthy
# rather than merely plausible.
# ==========================================================================
def cos_tail(d: int, tol: float, steps: int = 40_001) -> float:
    """P(|cos| > tol) for two independent random unit vectors in R^d."""
    if d == 2:                          # density is 1/(pi sqrt(1-c^2))
        return 1.0 - (2.0 / math.pi) * math.asin(tol)
    e = (d - 3) / 2.0

    def integrate(lo, hi):
        h = (hi - lo) / (steps - 1)
        s = 0.0
        for i in range(steps):
            c = lo + i * h
            w = 1 if i in (0, steps - 1) else (4 if i % 2 else 2)
            s += w * (max(0.0, 1.0 - c * c) ** e)
        return s * h / 3.0

    return integrate(tol, 1.0) / integrate(0.0, 1.0)


for _d in (10, 100, 768):
    _sampled = 1.0 - ORTHO[_d][2]                 # measured P(|cos| >= 0.1)
    _exact = cos_tail(_d, 0.1)
    assert abs(_sampled - _exact) < 0.03, (
        f"at d={_d} the exact tail is {_exact:.4f} and {PAIRS} samples gave "
        f"{_sampled:.4f}: the density behind the union bound is wrong")
NOTES.append("the exact cosine tail agrees with the sampled fraction at "
             "d = 10, 100 and 768, which is what makes the union bound usable")

# THE FIVE-DEGREE FIGURES ARE EXACT, and the sample is the check rather than
# the source. They used to be one seed's 4000-pair fractions, and two of the
# four differed from the truth after rounding -- 5% against 5.6% and 99%
# against 98% -- in a program that computes the capacity table exactly two
# frames later, and printed in five places as though they were facts. The
# integral is already here; using the sample where an exact answer is one call
# away is the defect, not the rounding.
FIVE_DEG = math.sin(math.radians(5.0))
for _d in QUOTED:
    _exact = 1.0 - cos_tail(_d, FIVE_DEG)
    emit(f"p05.deg.within.{_d}", round(100 * _exact))
    assert abs(_exact - ORTHO[_d][3]) < 0.03, (
        f"at d={_d} the exact five-degree fraction is {_exact:.4f} and "
        f"{PAIRS} samples gave {ORTHO[_d][3]:.4f}: one of the two is wrong")

NEAR_TOL = 0.2
emit("p05.near.tol", NEAR_TOL, 1)


def capacity(d: int, tol: float) -> float:
    """How many random directions fit before you expect one pair closer than
    `tol`.  C(n,2) P(|cos| > tol) = 1, so n ~ sqrt(2/p)."""
    p = cos_tail(d, tol)
    return math.sqrt(2.0 / p) if p > 0 else float("inf")


# WRONG PREDICTION TWO, and it is the better frame. The draft then asserted
# that the capacity outgrows d at EVERY dimension. It does not: at d = 64 the
# capacity is FOUR, far below the sixty-four that are exactly orthogonal,
# because a tolerance of 0.2 is a demanding requirement when the typical
# spread is 1/sqrt(64) = 0.125. The tolerance only becomes cheap once it sits
# several spreads out, and WHERE that happens is computable -- so the honest
# claim is not "high dimension gives you exponentially many nearly-orthogonal
# directions" but "it does, above a threshold that depends on the tolerance
# relative to 1/sqrt(d)". Everybody quotes the first without the qualifier.
CROSS_LO, CROSS_HI = 3, 4000
while CROSS_LO < CROSS_HI:
    _mid = (CROSS_LO + CROSS_HI) // 2
    if capacity(_mid, NEAR_TOL) > _mid:
        CROSS_HI = _mid
    else:
        CROSS_LO = _mid + 1
emit("p05.near.cross", CROSS_LO)
emit("p05.near.cross.sigmas", NEAR_TOL * math.sqrt(CROSS_LO), 1)
assert capacity(CROSS_LO, NEAR_TOL) > CROSS_LO >= capacity(CROSS_LO - 1, NEAR_TOL), (
    "the bisection did not bracket the crossover")

# The percentage as well as the exponent form: 1.1e-01 is right in a table and
# wrong in a sentence, where a reader has to convert it back to "about one pair
# in nine" before the clause means anything.
emit("p05.near.tail.64.pct", round(100 * cos_tail(64, NEAR_TOL)))
for _d in (64, 768, 4096):
    emit(f"p05.near.tail.{_d}", f"{cos_tail(_d, NEAR_TOL):.1e}")
    _n = capacity(_d, NEAR_TOL)
    emit(f"p05.near.n.{_d}", f"{_n:.1e}" if _n >= 1e5 else str(round(_n)))

assert capacity(64, NEAR_TOL) < 64, "d=64 is meant to sit below the crossover"
assert capacity(768, NEAR_TOL) > 768, "d=768 is meant to sit above it"
assert capacity(4096, NEAR_TOL) / 4096 > capacity(768, NEAR_TOL) / 768, (
    "past the crossover the capacity must outgrow the dimension, which is the "
    "whole of the relaxation P04 hands over")
emit("p05.near.mult.768", round(capacity(768, NEAR_TOL) / 768))
NOTES.append(f"below d = {CROSS_LO} a tolerance of {NEAR_TOL} buys nothing "
             f"over exact orthogonality; there it is "
             f"{NEAR_TOL * math.sqrt(CROSS_LO):.1f} spreads out")
NOTES.append(f"at 4096 dimensions exactly 4096 directions are mutually "
             f"orthogonal and about {capacity(4096, NEAR_TOL):.0e} are within "
             f"{NEAR_TOL} of it")


# ==========================================================================
# 3. Where the mass is -- F09's "how much of the space is near the middle".
#
# COMPUTED EXACTLY, NOT SAMPLED, and that is a decision rather than a
# convenience: the fraction of a ball's volume inside radius r is r^d, so at
# d = 100 the inner half of the radius holds 2^-100 of it. Sampling would find
# nothing there, and finding nothing proves nothing -- which is the same trap
# as an assertion that cannot fail.
# ==========================================================================
# AND THE FIRST DRAFT PRINTED 100.0 PER CENT, twice. At d = 100 the outer
# tenth of the radius holds 99.99735% of the volume and at d = 768 it holds
# more; rounded to one decimal both are "100.0", which is not true and which a
# reader would be right to disbelieve. A quantity that rounds to a hundred per
# cent must be reported as its COMPLEMENT, where every figure is significant:
# the inner nine tenths of the radius hold 2.7e-05 of the ball at d = 100 and
# 2.6e-36 at d = 768. The guard below is general and belongs in any script that
# emits a percentage.
SHELL_DIMS = (1, 10)
for _d in SHELL_DIMS:
    emit(f"p05.shell.outer.{_d}", 100 * (1 - 0.9 ** _d), 1)
emit("p05.shell.inner.768", f"{0.9 ** 768:.1e}")
emit("p05.shell.half.768", f"{0.5 ** 768:.1e}")

for _k, (_body, _num) in VALUES.items():
    if _k.startswith("p05.shell.outer") and float(_body) >= 100.0:
        raise AssertionError(
            f"{_k} prints {_body}: a percentage that rounds to 100 overstates, "
            f"and must be emitted as its complement instead")
assert 0.9 ** 768 > 0.0 and 0.5 ** 768 > 0.0, (
    "an inner-volume figure has underflowed to zero and cannot be printed")
NOTES.append("in 768 dimensions over 99.9999% of a ball's volume lies in the "
             "outermost 10% of its radius")


# ==========================================================================
# 4. Projection: the closest point in a subspace.
#
# Checked by SEARCH rather than asserted from the formula, because the claim
# the frames make is "closest", and a formula agreeing with itself is not
# evidence. The projection of a onto the line through b is (a.b/b.b) b; the
# search sweeps the whole line and confirms nothing on it is nearer.
# ==========================================================================
PROJ_A = [4.0, 3.0]
PROJ_B = [1.0, 0.0]
_t_star = dot(PROJ_A, PROJ_B) / dot(PROJ_B, PROJ_B)
PROJ_P = [_t_star * x for x in PROJ_B]
_resid = [a - p for a, p in zip(PROJ_A, PROJ_P)]

emit("p05.proj.ax", PROJ_A[0], 0)
emit("p05.proj.ay", PROJ_A[1], 0)
emit("p05.proj.t", _t_star, 0)
emit("p05.proj.dist", norm(_resid), 0)
emit("p05.proj.alen", norm(PROJ_A), 0)
emit("p05.proj.sweep", 400_001)

_best = min(norm([a - t * b for a, b in zip(PROJ_A, PROJ_B)])
            for t in (i / 20_000.0 - 10.0 for i in range(400_001)))
assert _best >= norm(_resid) - 1e-12, (
    f"the sweep found a point on the line at distance {_best:.9f}, nearer than "
    f"the projection's {norm(_resid):.9f} -- 'closest point' is the claim")
assert abs(dot(_resid, PROJ_B)) < 1e-12, (
    "the residual is not perpendicular to the line, which is the property that "
    "makes the projection the closest point rather than a coincidence")
NOTES.append(f"projection verified closest over {400_001} points of the line, "
             f"and its residual is perpendicular to {1e-12:g}")


# ==========================================================================
# 5. What normalising costs, and what it buys.
#
# It buys an identity: on unit vectors the dot product IS the cosine, so the
# two queries cannot rank differently. What it costs is the length, and F09's
# own disagreement pair is the cheapest demonstration -- the vector that was
# nearer and the vector that was more similar become the same query's answer
# once both are normalised, because the thing that separated them is gone.
# ==========================================================================
NORM_A = [0.30, 0.06]        # F09's A: points nearly along the query, short
NORM_B = [0.95, 0.45]        # F09's B: points less well, about the query's size
NORM_Q = [1.0, 0.0]

for _tag, _v in (("a", NORM_A), ("b", NORM_B)):
    emit(f"p05.norm.dot.{_tag}", dot(NORM_Q, _v), 4)
    emit(f"p05.norm.cos.{_tag}", dot(NORM_Q, _v) / (norm(NORM_Q) * norm(_v)), 4)
    emit(f"p05.norm.len.{_tag}", norm(_v), 4)

# The identity, swept rather than shown at a point. Its own generator, because
# the near-orthogonality sweep above now seeds per dimension and no longer
# leaves a shared stream behind for anything downstream to inherit.
_rnd = random.Random(SEED)
_worst_gap = 0.0
for _ in range(2000):
    d = _rnd.choice((2, 3, 8, 64))
    u, v = unit(d, _rnd), unit(d, _rnd)
    _worst_gap = max(_worst_gap, abs(dot(u, v) - dot(u, v) / (norm(u) * norm(v))))
# A BOUND, never the figure. P06 had two committed residuals rejected by CI
# for being properties of the machine, and the build trap names P05 among the
# instances still latent: the measured gap here is one interpreter's rounding
# noise and a reader reproducing it gets a different last digit. What is true
# on any machine is that the disagreement is rounding rather than a difference,
# and the honest way to write that is a ceiling the measurement clears.
IDENTITY_BOUND = 1e-15
emit("p05.norm.identity.bound", f"{IDENTITY_BOUND:.0e}")
emit("p05.norm.identity.trials", 2000)
assert _worst_gap < IDENTITY_BOUND, (
    f"the dot product and the cosine differ by {_worst_gap:g} on unit vectors, "
    f"which is above the {IDENTITY_BOUND:g} the page prints")
assert _worst_gap < 1e-12, (
    "on unit vectors the dot product and the cosine must be the same number; "
    f"they differ by {_worst_gap:g}, so the section's identity is not one")

# And the cost, stated as the ORDER REVERSAL it causes rather than as a figure.
_dot_ranks_b_first = dot(NORM_Q, NORM_B) > dot(NORM_Q, NORM_A)
_cos_ranks_a_first = (dot(NORM_Q, NORM_A) / norm(NORM_A)
                      > dot(NORM_Q, NORM_B) / norm(NORM_B))
assert _dot_ranks_b_first and _cos_ranks_a_first, (
    "F09's pair no longer disagrees, so this section has nothing to explain")
NOTES.append("F09's pair still disagrees: the dot product prefers B and the "
             "cosine prefers A, and normalising erases the difference by "
             "erasing the length")


# ==========================================================================
# The cross-programme gate.
#
# P04's pass established what one of these is worth and what it is not: the
# mechanism only earns its place when the two programs are quoting ONE
# computation. P04's first attempt gated this program's (3,4) length of 5
# against F09's `f09.len3d`, which is 7 and is a different vector entirely --
# two numbers that happened to sit near each other. Not repeated here.
#
# What P05 and F09 genuinely share is the DIMENSION. F09 reasons about
# `f09.dim`-dimensional embeddings throughout and defers the arrangement
# question to this program; the near-orthogonality table above answers it at
# exactly that dimension, so if F09's number ever moves, this table is quietly
# about a different model and the build should say so.
# ==========================================================================
_f09dim = committed("f09.tex", "f09.dim")
if _f09dim is not None:
    assert int(_f09dim) in DIMS, (
        f"F09 reasons at {_f09dim} dimensions and this program's table does "
        f"not measure there: {DIMS}. The row F09 is owed has gone missing.")
    NOTES.append(f"gate: the table measures at F09's own {_f09dim} dimensions")


# ==========================================================================
# The transcript. Nothing typed, and it imports what it calls -- P04 shipped
# one that named a function it never defined, so a reader pasting it out of
# the PDF got NameError while every drift gate stayed green.
# ==========================================================================
# The row is COMPUTED, and it is the same call the four committed values come
# from. Typed here as a literal it reproduced perfectly and still disagreed
# with the frames beside it in the third decimal, because the literal recorded
# a different sample size from the one the page quoted -- a fabricated console
# block with a build step in front of it.
# It prints FORMATTED strings rather than a list of rounded floats, and that is
# the assertion below talking. round(0.31804, 4) reprs as 0.318 where emit()
# writes 0.3180, so a value landing on a trailing zero -- one of these four did,
# on the first run -- puts 0.318 in the listing and 0.3180 four lines under it.
# Same quantity, two spellings, which is F08's defect appearing inside the fix
# for P16's. Formatting both ends the same way makes them the same STRING.
_TROW = [f"{spread(_d):.4f}" for _d in QUOTED]
RANK_TEXT = """>>> from p05_inner_product_norms import unit, dot
>>> import random, statistics          # run this from code/
>>> def spread(d, n={n}):
...     rnd = random.Random({seed} + d)
...     return statistics.pstdev(
...         dot(unit(d, rnd), unit(d, rnd)) for _ in range(n))
...
>>> print(*(f"{{spread(d):.4f}}" for d in {dims}))
{row}
""".format(seed=SEED, n=PAIRS, dims=QUOTED, row=" ".join(_TROW))
assert RANK_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in RANK_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(RANK_TEXT.strip().splitlines()) <= 14, "transcript too tall for one frame"
# The listing's output and the page's four numbers must be the same STRING, not
# merely the same quantity: emit() writes .4f and Python's repr drops a trailing
# zero, so a value landing on one would print 0.715 in the listing and 0.7150
# four lines below it -- F08's two-numbers-that-look-like-one, inside the fix
# for it. Assert rather than hope, and the day it fires the answer is to quote
# the listing's own row in the frame instead of re-emitting it.
for _d, _s in zip(QUOTED, _TROW):
    assert _s == f"{ORTHO[_d][1]:.4f}", (
        f"at d={_d} the listing prints {_s!r} where the page prints "
        f"{ORTHO[_d][1]:.4f}: the transcript and the frames have come apart")
    assert abs(float(_s) - 1 / math.sqrt(_d)) / (1 / math.sqrt(_d)) < 0.08, (
        f"the transcript's spread at d={_d} is {_s}, which is not 1/sqrt(d)")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p05-spread.txt").write_text(RANK_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p05-spread.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p05_inner_product_norms.py --- do not edit.",
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
        print(f"  {k:<{width}}  {body}")
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
