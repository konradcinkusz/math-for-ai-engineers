#!/usr/bin/env python3
"""Program P06 --- Matrices as linear maps.

Every number Program P06 prints that the reader cannot do in their head is
computed here and written to figures/values/p06.tex, which the book \\input{}s.

P06's thesis is that A MATRIX IS A FUNCTION THAT RESPECTS ADDITION AND SCALING,
and that matrix multiplication is composition of those functions -- which is
why it is associative, why it does not commute, and why shape is a type
signature rather than bookkeeping.

WHAT P06 IS OWED, and pays. Read out of the four files rather than remembered:

  F05  ALREADY DERIVES THE COLLAPSE, in one dimension and in full, including
       the relu argument: two hundred linear layers collapse to one, and the
       activation is there because without it the composition is provably a
       waste of parameters. So the brief's promise to derive it again is
       SPENT. What F06 names as this program's job is narrower and is the
       right one: "P06 makes the weights a matrix and shows that matrix
       multiplication is composition, which is F05's collapse argument done in
       more than one dimension."
  F06  the sentence above, by name.
  P03  needs shapes and what a matrix is before a transformer block can be
       counted -- and says the count itself is P32's.
  P04  a rotation is itself a matrix, so "does this method survive a change of
       basis" is a question about this program's object.
  P05  "P06 adds the next object, and the pattern repeats: one definition, and
       a great deal follows."

THE MEASUREMENTS:

  1. THE COLLAPSE IN n DIMENSIONS, exact. Composing two affine layers gives
     W2 W1 x + (W2 b1 + b2), verified against the composed function over many
     random inputs. And the relu between them breaks it, demonstrated by three
     COLLINEAR inputs whose outputs are not collinear -- which no affine map
     can do, so no single matrix reproduces the pair.

  2. NON-COMMUTATIVITY, which one dimension cannot show at all, because
     scalars commute. Measured as a fraction over random pairs, and worked on
     one pair a reader can check by hand.

  3. ASSOCIATIVITY AND ITS COST. (AB)C and A(BC) agree to machine precision
     and cost wildly different numbers of multiplications. Associativity is a
     theorem; the cost is a measurement, and P03 built the vocabulary for it.

WHAT P06 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    index notation, einsum, broadcasting, reshape against transpose against
      permute, and the axes of a rank-4 attention tensor            -> P07
    rank, the four subspaces, least squares, LoRA                   -> P08
    the determinant, the inverse and change of basis                -> P09
    counting a transformer block's parameters                       -> P32

Run:  python3 code/p06_matrices_as_maps.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p06.tex"
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


# --- the smallest linear algebra that will do, in plain Python ---
def matvec(M, v):
    return [sum(r[j] * v[j] for j in range(len(v))) for r in M]


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def rand_mat(n, m, rnd):
    return [[rnd.uniform(-1, 1) for _ in range(m)] for _ in range(n)]


def relu(v):
    return [x if x > 0 else 0.0 for x in v]


# ==========================================================================
# A MEASURED FLOATING-POINT RESIDUAL IS A PROPERTY OF THE MACHINE, so it is
# reported as a BOUND and never as a figure.
#
# This was learnt from CI rejecting this file. The committed values said
# p06.assoc.err = 4.4e-16 and p06.bend.affine = 2.7e-16; CI recomputed them as
# 2.2e-16 and 2.6e-16 and failed the drift gate, correctly. Nothing was wrong
# with either number -- they are the rounding noise left over from summing a
# few dozen doubles, and the order those additions happen in is a property of
# the interpreter and the build, not of the mathematics.
#
# It is the same defect as F03's np.logspace claim wearing different clothes:
# an OBSERVATION committed where an INVARIANT was meant. The invariant here is
# "the disagreement is rounding rather than a difference", and the honest way
# to write that is a ceiling the measurement clears on any machine.
def bound(x: float) -> str:
    """The next power of ten strictly above x, as a string for \\val{}."""
    assert x > 0, "a bound is only meaningful for a positive residual"
    e = math.ceil(math.log10(x))
    if 10.0 ** e <= x:                                   # pragma: no cover
        e += 1
    out = f"1e{e}"
    assert float(out) > x, "the bound must clear the measurement"
    return out


_rnd = random.Random(20260831)

# ==========================================================================
# 1. The collapse, in more than one dimension.
#
# F05 did this in one dimension and the reader has it. What one dimension
# CANNOT show is that the collapsed weight is a PRODUCT OF MATRICES rather
# than a product of numbers, which is where everything else in this program
# comes from. The assertion is the identity, over many random inputs, so a
# change of seed cannot make it pass by luck.
# ==========================================================================
DIN, DMID, DOUT = 5, 4, 3
W1, B1 = rand_mat(DMID, DIN, _rnd), [_rnd.uniform(-1, 1) for _ in range(DMID)]
W2, B2 = rand_mat(DOUT, DMID, _rnd), [_rnd.uniform(-1, 1) for _ in range(DOUT)]

W = matmul(W2, W1)
B = [sum(W2[i][j] * B1[j] for j in range(DMID)) + B2[i] for i in range(DOUT)]

COLLAPSE_TRIALS = 2000
_worst = 0.0
for _ in range(COLLAPSE_TRIALS):
    x = [_rnd.uniform(-3, 3) for _ in range(DIN)]
    two = [a + b for a, b in zip(matvec(W2, [a + b for a, b in
                                             zip(matvec(W1, x), B1)]), B2)]
    one = [a + b for a, b in zip(matvec(W, x), B)]
    _worst = max(_worst, max(abs(p - q) for p, q in zip(two, one)))
emit("p06.din", DIN)
emit("p06.dmid", DMID)
emit("p06.dout", DOUT)
emit("p06.collapse.trials", COLLAPSE_TRIALS)
emit("p06.collapse.err", bound(_worst))
assert _worst < 1e-12, (
    f"two affine layers do not collapse to one: worst disagreement {_worst:g}. "
    f"That identity is the whole of section 4.")
NOTES.append(f"two affine layers collapse to one over {COLLAPSE_TRIALS} random "
             f"inputs, worst disagreement {_worst:.1e}")

# And the relu breaks it -- shown the way that admits no argument. An affine
# map sends collinear points to collinear points, always. Find three collinear
# inputs whose relu-separated outputs are not collinear and no single matrix
# can reproduce the pair, whatever it is.
def with_relu(x):
    h = relu([a + b for a, b in zip(matvec(W1, x), B1)])
    return [a + b for a, b in zip(matvec(W2, h), B2)]


def collinearity_defect(p, q, r):
    """How far r sits off the line through p and q, as a fraction of |q - p|."""
    d = [b - a for a, b in zip(p, q)]
    e = [c - a for a, c in zip(p, r)]
    nd = math.sqrt(sum(t * t for t in d))
    t = sum(a * b for a, b in zip(d, e)) / (nd * nd)
    off = [c - t * a for a, c in zip(d, e)]
    return math.sqrt(sum(o * o for o in off)) / nd


_base = [_rnd.uniform(-3, 3) for _ in range(DIN)]
_dir = [_rnd.uniform(-3, 3) for _ in range(DIN)]
_pts = [[b + s * d for b, d in zip(_base, _dir)] for s in (-1.0, 0.0, 1.0)]
_bend = collinearity_defect(*[with_relu(p) for p in _pts])
_straight = collinearity_defect(*[[a + b for a, b in zip(matvec(W, p), B)]
                                  for p in _pts])
emit("p06.bend", f"{_bend:.2f}")
emit("p06.bend.affine", bound(_straight))
assert _bend > 0.05, (
    f"the relu-separated pair bends collinear inputs by only {_bend:g}, which "
    f"is not enough for the frames to call it a different kind of function")
assert _straight < 1e-12, (
    "the affine map does not preserve collinearity, so the contrast the frame "
    "draws is not the one being measured")
NOTES.append(f"three collinear inputs come out collinear through the collapsed "
             f"matrix ({_straight:.0e}) and bent through the relu ({_bend:.2f})")


# ==========================================================================
# 2. Non-commutativity. One dimension cannot show this AT ALL, because scalars
#    commute, so the entire phenomenon is invisible until the weights become
#    matrices -- which is the sharpest argument for why this program exists.
#
# The worked pair is chosen so a reader can do it in their head: a quarter turn
# and a flattening onto the horizontal axis. Do them in the two orders and the
# same input goes to two different places.
# ==========================================================================
ROT = [[0, -1], [1, 0]]          # quarter turn anticlockwise
PROJ = [[1, 0], [0, 0]]          # flatten onto the horizontal axis
PT = [1, 0]

RP = matmul(ROT, PROJ)           # project first, then rotate
PR = matmul(PROJ, ROT)           # rotate first, then project
_rp, _pr = matvec(RP, PT), matvec(PR, PT)

for _tag, _v in (("rp", _rp), ("pr", _pr)):
    emit(f"p06.order.{_tag}.x", int(_v[0]))
    emit(f"p06.order.{_tag}.y", int(_v[1]))
assert _rp != _pr, (
    "the worked pair commutes on this point, so the frame has nothing to show")
NOTES.append(f"project-then-rotate sends (1,0) to {tuple(map(int,_rp))}; "
             f"rotate-then-project sends it to {tuple(map(int,_pr))}")

# And the general case, so the worked pair is not read as a curiosity.
COMMUTE_TRIALS = 5000
_commuting = 0
for _ in range(COMMUTE_TRIALS):
    A, Bm = rand_mat(3, 3, _rnd), rand_mat(3, 3, _rnd)
    ab, ba = matmul(A, Bm), matmul(Bm, A)
    if max(abs(ab[i][j] - ba[i][j]) for i in range(3) for j in range(3)) < 1e-9:
        _commuting += 1
emit("p06.commute.trials", COMMUTE_TRIALS)
emit("p06.commute.found", _commuting)
assert _commuting == 0, (
    f"{_commuting} of {COMMUTE_TRIALS} random pairs commuted, which they should "
    f"not: commuting is a measure-zero condition and finding one means the "
    f"draw is not what the frame says it is")
NOTES.append(f"none of {COMMUTE_TRIALS} random 3x3 pairs commute, as they "
             f"cannot except on a measure-zero set")


# ==========================================================================
# 3. Associativity, and what it costs.
#
# Associativity is a THEOREM and is asserted, not measured. What is measured is
# the consequence P03 built the vocabulary for: the two bracketings compute the
# same thing and do wildly different amounts of work. This is the one place in
# the program where the mathematics is free and the engineering is not.
# ==========================================================================
CHAIN = (1000, 1000, 1, 1000)          # A: n x m, B: m x p, C: p x q
_n, _m, _p, _q = CHAIN
A = rand_mat(4, 4, _rnd)
Bm = rand_mat(4, 4, _rnd)
C = rand_mat(4, 4, _rnd)
_left, _right = matmul(matmul(A, Bm), C), matmul(A, matmul(Bm, C))
_assoc = max(abs(_left[i][j] - _right[i][j]) for i in range(4) for j in range(4))
emit("p06.assoc.err", bound(_assoc))
assert _assoc < 1e-12, (
    f"(AB)C and A(BC) disagree by {_assoc:g}: associativity is a theorem and "
    f"the arithmetic must not be contradicting it")

# multiplications for (n x m)(m x p) is n*m*p
_ab_c = _n * _m * _p + _n * _p * _q
_a_bc = _m * _p * _q + _n * _m * _q
for _k, _v in (("dims.n", _n), ("dims.m", _m), ("dims.p", _p), ("dims.q", _q)):
    emit(f"p06.{_k}", _v)
emit("p06.cost.left", f"{_ab_c:.1e}")
emit("p06.cost.right", f"{_a_bc:.1e}")
emit("p06.cost.ratio", round(_a_bc / _ab_c))
assert _a_bc > 100 * _ab_c, (
    f"the two bracketings cost {_ab_c} and {_a_bc}, a ratio of "
    f"{_a_bc/_ab_c:.0f}, which is not striking enough to build a frame on")
NOTES.append(f"same product, two bracketings: {_ab_c:.1e} multiplications "
             f"against {_a_bc:.1e}, a factor of {_a_bc // _ab_c}")


# ==========================================================================
# 4. What the collapse costs in parameters, which is F05's argument priced.
# ==========================================================================
STACK_LAYERS, STACK_WIDTH = 8, 512
_stacked = STACK_LAYERS * (STACK_WIDTH * STACK_WIDTH + STACK_WIDTH)
_collapsed = STACK_WIDTH * STACK_WIDTH + STACK_WIDTH
emit("p06.stack.layers", STACK_LAYERS)
emit("p06.stack.width", STACK_WIDTH)
emit("p06.stack.params", f"{_stacked:.2e}")
emit("p06.stack.collapsed", f"{_collapsed:.2e}")
# One decimal, not zero: with 8 layers the waste is exactly 7/8, and a reader
# dividing the two figures on the page gets 87.5. Rounding to 88 would be a
# number that does not reproduce from what is printed beside it -- F04's defect.
emit("p06.stack.wasted.pct", 100 * (1 - _collapsed / _stacked), 1)
assert abs((1 - _collapsed / _stacked) - (STACK_LAYERS - 1) / STACK_LAYERS) < 1e-12, (
    "the waste is not (layers-1)/layers, so the frame's fraction is wrong")
assert _collapsed * STACK_LAYERS == _stacked, (
    "the stack's parameter count is not the per-layer count times the depth, "
    "so the percentage the frame quotes is not what it says it is")
NOTES.append(f"{STACK_LAYERS} linear layers of width {STACK_WIDTH} hold "
             f"{_stacked:.2e} parameters and express what "
             f"{_collapsed:.2e} express: "
             f"{100*(1-_collapsed/_stacked):.1f}% bought nothing")


# ==========================================================================
# The transcript. Nothing typed, and it imports what it calls.
# ==========================================================================
ORDER_TEXT = """>>> from p06_matrices_as_maps import matmul, matvec
>>> rot  = [[0, -1], [1, 0]]      # a quarter turn
>>> proj = [[1, 0], [0,  0]]      # flatten onto the x axis
>>> matvec(matmul(rot, proj), [1, 0])     # project, then rotate
{rp}
>>> matvec(matmul(proj, rot), [1, 0])     # rotate, then project
{pr}
""".format(rp=[int(v) for v in _rp], pr=[int(v) for v in _pr])
assert ORDER_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in ORDER_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(ORDER_TEXT.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p06-order.txt").write_text(ORDER_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p06-order.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p06_matrices_as_maps.py --- do not edit.",
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
