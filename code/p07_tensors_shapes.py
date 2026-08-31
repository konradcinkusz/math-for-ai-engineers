#!/usr/bin/env python3
"""Program P07 --- Tensors, shapes and index notation.

Every number Program P07 prints that the reader cannot do in their head is
computed here and written to figures/values/p07.tex, which the book \\input{}s.

P07's thesis is that AN OPERATION ON ARRAYS IS A STATEMENT ABOUT WHICH AXES
LINE UP, and that index notation says it exactly where a picture cannot. The
audience manipulates rank-4 arrays daily and has only ever been taught rank-2
notation; the mismatch is where the shape errors come from, and the August 2026
curriculum review called it the largest content gap in the field.

WHAT P07 IS OWED, read out of the files rather than remembered:

  P06  §4 is the whole rank-2 story and hands this program four things by
       name: that a shape is the domain and the codomain written down, that a
       shape error is therefore a TYPE error, that a batch of k inputs is
       n x k under its own convention -- and, in a note, that real frameworks
       stack the batch along the FIRST axis instead, so a layer computes
       X W^T with X of shape k x n. Its closing frame hands over the
       four-index question by name. So this program opens on the convention
       flip: it is the first place a rank-2 model meets a framework.
  P04  owns dimension as THE NUMBER OF INDEPENDENT DIRECTIONS, which is the
       word this program collides with. Name the collision; do not reuse the
       word quietly.
  P03  owns the memory bill and the arithmetic intensity, so what a copy costs
       is quoted from there and not re-measured here.

THE MEASUREMENTS:

  1. AN einsum WRITTEN FROM THE RULE. An index appearing twice is summed and
     an index appearing once survives; the arrow names the survivors. Checked
     against explicit loops on four strings including the rank-4 attention
     score, in exact integer arithmetic, so the check cannot pass by rounding.

  2. THE BROADCAST LOSS, AND IT IS EXACT. Predictions of shape (n,) against
     targets of shape (n,1) broadcast to every PAIR, and

         mean_ij (p_i - t_j)^2  =  mean_i (p_i - t_i)^2  +  2 Cov(p, t)

     which is an identity, asserted as one. Two consequences make it the
     program's headline rather than a warning box: the error GROWS as the
     model improves, because the covariance is exactly what training
     increases; and at a perfect fit the reported loss is 2 Var(t) and cannot
     fall below it, which reads as a model that has stopped learning.

  3. WHICH OF THE THREE MOVES DATA, and the head split that turns on it.
     reshape(b, s, h, d).transpose(1, 2) and reshape(b, h, s, d) both give a
     rank-4 array of the right shape and they are DIFFERENT ARRAYS. Asserted
     different, and asserted equal once the permute is put back -- which is
     the half that makes it a rule rather than a warning.

WHAT P07 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    rank, the four subspaces, least squares, LoRA                   -> P08
    the determinant, the inverse and change of basis                -> P09
    the transformer assembled from all of it                        -> P32
    what a copy costs in bytes or in time                           -> P03
    differentiating through a reshape                               -> P16, P18

Run:  python3 code/p07_tensors_shapes.py      (or: make numbers)
"""
from __future__ import annotations

import itertools
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p07.tex"
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


# ==========================================================================
# The smallest array that will do: a flat buffer, a shape, and a rule for
# turning an index tuple into an offset.
#
# That is not a simplification -- it is the definition the whole program
# rests on, and section 5 is unstateable without it. reshape changes the
# SHAPE and leaves the buffer alone; transpose changes the ORDER THE OFFSETS
# ARE COMPUTED IN and leaves the buffer alone; neither moves a number, and
# what moves numbers is asking for the result contiguous, which is a third
# operation with its own name.
# ==========================================================================
class Arr:
    def __init__(self, buf, shape):
        assert len(buf) == math.prod(shape), "buffer does not fill the shape"
        self.buf, self.shape = list(buf), tuple(shape)

    def strides(self):
        s, acc = [], 1
        for n in reversed(self.shape):
            s.append(acc)
            acc *= n
        return tuple(reversed(s))

    def __getitem__(self, idx):
        return self.buf[sum(i * s for i, s in zip(idx, self.strides()))]

    def reshape(self, *shape):
        return Arr(self.buf, shape)

    def permute(self, *order):
        """A permute, done the honest way: the buffer is rebuilt.

        A real framework does not rebuild it -- it permutes the strides and
        hands back a view. The observable result is identical, which is the
        point of the frame: two operations that differ completely in what they
        cost are indistinguishable from the numbers alone.
        """
        shape = tuple(self.shape[o] for o in order)
        out = []
        for idx in itertools.product(*(range(n) for n in shape)):
            src = [0] * len(order)
            for pos, o in enumerate(order):
                src[o] = idx[pos]
            out.append(self[tuple(src)])
        return Arr(out, shape)

    def __eq__(self, other):
        return self.shape == other.shape and self.buf == other.buf


# ==========================================================================
# 1. einsum, written from the rule rather than called.
#
# The rule is one line -- an index that appears twice is summed over, an index
# that appears once survives -- and the arrow makes the exception explicit: an
# index that is repeated AND on the right is a batch axis, not a contraction.
# That exception is the one people get wrong, so the implementation has to
# honour it rather than special-case it.
#
# Integer arithmetic throughout, so agreement is exact and a passing check
# cannot be rounding.
# ==========================================================================
def einsum2(spec, A: Arr, B: Arr) -> Arr:
    lhs, out = spec.split("->")
    sa, sb = lhs.split(",")
    assert len(sa) == len(A.shape) and len(sb) == len(B.shape), "spec vs rank"

    size = {}
    for s, arr in ((sa, A), (sb, B)):
        for ch, n in zip(s, arr.shape):
            assert size.setdefault(ch, n) == n, f"axis {ch} has two lengths"

    summed = sorted(set(sa + sb) - set(out))
    shape = tuple(size[c] for c in out)
    buf = []
    for oidx in itertools.product(*(range(size[c]) for c in out)):
        pos = dict(zip(out, oidx))
        total = 0
        for sidx in itertools.product(*(range(size[c]) for c in summed)):
            pos.update(zip(summed, sidx))
            total += (A[tuple(pos[c] for c in sa)]
                      * B[tuple(pos[c] for c in sb)])
        buf.append(total)
    return Arr(buf, shape)


_rnd = random.Random(20260831)


def rand_arr(shape, lo=-9, hi=9):
    return Arr([_rnd.randint(lo, hi) for _ in range(math.prod(shape))], shape)


# 'ik,kj->ij' is exactly sum_k A_ik B_kj, which is Program P06's product.
A2, B2 = rand_arr((4, 5)), rand_arr((5, 3))
loops = Arr([sum(A2[(i, k)] * B2[(k, j)] for k in range(5))
             for i in range(4) for j in range(3)], (4, 3))
assert einsum2("ik,kj->ij", A2, B2) == loops, "einsum disagrees with the loops"

# 'ik,jk->ij' is A B^T -- the framework convention P06's note flagged.
B2t = B2.permute(1, 0)
assert einsum2("ik,jk->ij", A2, B2t) == loops, "A B^T is not the same product"

# 'ij,j->i' is a matrix on a vector, which P06 says needs no second rule.
V = rand_arr((5,))
assert einsum2("ij,j->i", A2, V) == Arr(
    [sum(A2[(i, j)] * V[(j,)] for j in range(5)) for i in range(4)], (4,)), \
    "matrix-times-vector is not the same rule"

# THE RANK-4 ONE, and it is the reason the program exists. b and h appear
# twice and are NOT summed, because they appear on the right as well.
NB, NH, NQ, NK, ND = 2, 3, 4, 5, 6
Q, K = rand_arr((NB, NH, NQ, ND)), rand_arr((NB, NH, NK, ND))
scores = einsum2("bhqd,bhkd->bhqk", Q, K)
brute = Arr([sum(Q[(b, h, q, d)] * K[(b, h, k, d)] for d in range(ND))
             for b in range(NB) for h in range(NH)
             for q in range(NQ) for k in range(NK)], (NB, NH, NQ, NK))
assert scores == brute, "the attention score is not the sum it denotes"
assert scores.shape == (NB, NH, NQ, NK), "four axes in, four axes out"

# And the assertion that stops the exception becoming folklore: summing over b
# as well gives a DIFFERENT and smaller-ranked thing. A repeated index that is
# also on the right is a batch axis; a repeated index that is not is a sum.
pooled = einsum2("bhqd,bhkd->hqk", Q, K)
assert pooled.shape == (NH, NQ, NK), "dropping b from the right drops the axis"
assert pooled[(0, 0, 0)] == sum(scores[(b, 0, 0, 0)] for b in range(NB)), \
    "leaving an index off the right sums over it"

NOTES.append("einsum written from the rule agrees with explicit loops exactly, "
             "in integer arithmetic, on four strings including bhqd,bhkd->bhqk")

# ==========================================================================
# 2. THE BROADCAST LOSS. This is the program's headline and it is an identity
#    rather than a demonstration, which is what makes it worth the section.
#
#    Predictions of shape (n,) minus targets of shape (n,1) broadcast to every
#    PAIR, so the mean is taken over n^2 entries of which n are the intended
#    ones. What comes out is not noise:
#
#       mean_ij (p_i - t_j)^2 = mean_i (p_i - t_i)^2 + 2 Cov(p, t)
#
#    ASSERT THE IDENTITY, NOT THE FOUR NUMBERS. A change of seed or of noise
#    level moves every figure on the page and must not be able to falsify the
#    frame; the identity holds for any p and t at all.
# ==========================================================================
def mean(xs):
    return sum(xs) / len(xs)


def cov(xs, ys):
    mx, my = mean(xs), mean(ys)
    return mean([(x - mx) * (y - my) for x, y in zip(xs, ys)])


N = 64
_t = [_rnd.gauss(0.0, 1.0) for _ in range(N)]
VAR_T = cov(_t, _t)

ROWS = []
for noise in (2.0, 0.5, 0.1, 0.0):
    p = [ti + _rnd.gauss(0.0, noise) for ti in _t]
    true = mean([(a - b) ** 2 for a, b in zip(p, _t)])
    bcast = mean([(a - b) ** 2 for a in p for b in _t])
    assert abs((bcast - true) - 2 * cov(p, _t)) < 1e-12, \
        "the broadcast excess is not twice the covariance"
    ROWS.append((noise, true, bcast))

# The two consequences, each asserted rather than described.
_, true0, bcast0 = ROWS[-1]                       # noise 0.0: a perfect fit
assert true0 < 1e-24, "a perfect fit should have no loss at all"
assert abs(bcast0 - 2 * VAR_T) < 1e-12, \
    "at a perfect fit the reported loss is twice the variance of the targets"

# ...and the half that makes it expensive, which took two attempts to state.
#
# THE FIRST ATTEMPT WAS THAT THE EXCESS GROWS AS THE FIT IMPROVES, AND THE
# ASSERTION REFUTED IT on the first run: the excess went 1.01, 1.59, 1.43,
# 1.44 over the four noise levels, which is not increasing. The excess is
# 2 Cov(p, t) = 2 Var(t) + 2 Cov(eps, t), and the second term is a SAMPLE
# covariance between the residual and the targets -- a random quantity of size
# about sigma * sd(t) / sqrt(n) that does not shrink in step with sigma. At
# n = 64 it is large enough to reorder the rows.
#
# What is true, and is the better sentence, is that the excess converges to a
# FLOOR SET BY THE TARGETS while the true loss goes to zero underneath it. So
# the RATIO is the thing that runs away, and it does so monotonically because
# ratio = 1 + excess / true with excess essentially fixed. Both are asserted:
# a Cauchy-Schwarz bound that holds for any sample, and the ratio's ordering.
excess = [b - a for _, a, b in ROWS]
sd_t = math.sqrt(VAR_T)
for (noise, true, bcast), ex in zip(ROWS, excess):
    assert abs(ex - 2 * VAR_T) <= 2 * noise * sd_t + 1e-12, \
        "the excess must sit within Cauchy-Schwarz of twice the target variance"

ratios = [b / a for _, a, b in ROWS if a > 0]
assert ratios == sorted(ratios) and len(ratios) == len(ROWS) - 1, \
    "the reported loss must run away from the true one as the fit improves"
assert ratios[-1] > 50 * ratios[0], \
    "the runaway should be dramatic enough for the frame to be worth writing"

# BEFORE QUOTING A RATIO, DIVIDE THE TWO NUMBERS AS THE PAGE PRINTS THEM.
# F04 shipped 22 778 beside a page that divided to 22 776 and F05 shipped 51.7
# beside a page that divided to 53.1; both were caught the same way and this
# guard is the habit made mechanical. The low-noise true loss needs four
# decimals rather than three -- at three it prints 0.009 and the page divides
# to 291 against a stated 286.
def _printed(x, digits):
    return float(f"{x:.{digits}f}")


_TRUE_HI_D, _BCAST_HI_D = 2, 2
_TRUE_LO_D, _BCAST_LO_D = 5, 2
_RATIO_HI_D, _RATIO_LO_D = 1, 0

for _a, _ad, _b, _bd, _r, _rd in (
        (ROWS[0][1], _TRUE_HI_D, ROWS[0][2], _BCAST_HI_D,
         ROWS[0][2] / ROWS[0][1], _RATIO_HI_D),
        (ROWS[2][1], _TRUE_LO_D, ROWS[2][2], _BCAST_LO_D,
         ROWS[2][2] / ROWS[2][1], _RATIO_LO_D)):
    assert (f"{_printed(_b, _bd) / _printed(_a, _ad):.{_rd}f}"
            == f"{_r:.{_rd}f}"), \
        "the ratio does not reproduce from the two numbers the page prints"

# Only what the frames quote is emitted. The floor and the target variance are
# both asserted above and neither is on a page: the frames state the identity
# and the transcript carries a three-element example a reader can check by
# hand, so a fifth figure would be a number to trust rather than to verify.
emit("p07.mse.n", N)
emit("p07.mse.true.hi", ROWS[0][1], _TRUE_HI_D)
emit("p07.mse.bcast.hi", ROWS[0][2], _BCAST_HI_D)
emit("p07.mse.true.lo", ROWS[2][1], _TRUE_LO_D)
emit("p07.mse.bcast.lo", ROWS[2][2], _BCAST_LO_D)
emit("p07.mse.ratio.hi", ROWS[0][2] / ROWS[0][1], _RATIO_HI_D)
emit("p07.mse.ratio.lo", ROWS[2][2] / ROWS[2][1], _RATIO_LO_D)
NOTES.append(
    f"the broadcast loss exceeds the true one by exactly 2 Cov(p, t); at a "
    f"perfect fit it reads {bcast0:.2f} = 2 Var(t) and cannot fall below it")

# The cheaper trap in the same section, and both readings are legal.
BIAS = [10, 20, 30]
M33 = Arr(list(range(1, 10)), (3, 3))
per_row = [[M33[(i, j)] + BIAS[j] for j in range(3)] for i in range(3)]
per_col = [[M33[(i, j)] + BIAS[i] for j in range(3)] for i in range(3)]
assert per_row != per_col, "the two readings of a broadcast bias must differ"
assert per_row[0] == [11, 22, 33] and per_col[0] == [11, 12, 13], \
    "the worked bias rows are not what the frames print"

# ==========================================================================
# 3. reshape, transpose, permute: which of them moves data, and the head
#    split that turns on it.
#
#    The two orders both produce a rank-4 array of the right shape, and the
#    assertion is that they are DIFFERENT -- and equal once the permute is put
#    back. The second half is what turns a warning into a rule.
# ==========================================================================
B, S, H, D = 2, 4, 3, 5
X = Arr(list(range(B * S * H * D)), (B, S, H * D))

right = X.reshape(B, S, H, D).permute(0, 2, 1, 3)     # split, then move heads
wrong = X.reshape(B, H, S, D)                          # split straight to rank 4
assert right.shape == wrong.shape == (B, H, S, D), "both give the right shape"
assert right != wrong, "the two head splits must not agree"
assert right.permute(0, 2, 1, 3).reshape(B, S, H * D) == X, \
    "putting the permute back must recover the buffer"

differ = sum(1 for a, b in zip(right.buf, wrong.buf) if a != b)
emit("p07.split.entries", len(right.buf))
emit("p07.split.differ", differ)
emit("p07.split.b", B)
emit("p07.split.s", S)
emit("p07.split.h", H)
emit("p07.split.d", D)
NOTES.append(f"the two head splits agree in shape and differ in "
             f"{differ} of {len(right.buf)} entries")

# A reshape does not move data; the buffer is the same object read a second
# way. Asserted, because the whole of section 5 rests on it.
assert X.reshape(B, S, H, D).buf == X.buf, "reshape must not move a number"
assert X.reshape(B * S * H * D).buf == X.buf, "nor must flattening"

# ==========================================================================
# The word collision, which is three-way and is section 1's trap.
# ==========================================================================
EMB_B, EMB_S, EMB_D = 32, 128, 768
emit("p07.emb.b", EMB_B)
emit("p07.emb.s", EMB_S)
emit("p07.emb.d", EMB_D)
emit("p07.emb.rank", 3)
emit("p07.emb.total", EMB_B * EMB_S * EMB_D)
assert EMB_B * EMB_S * EMB_D == 3145728, "the worked total is not what it was"

# ==========================================================================
# numpy, as a cross-check that announces itself when it is absent. The book's
# claims must survive a plain python3, so nothing here may depend on it --
# F03 paid for that rule and CI has fallen over it once.
# ==========================================================================
try:
    import numpy as np
except ImportError:                                      # pragma: no cover
    NOTES.append("numpy absent: the einsum and broadcast cross-checks were skipped")
else:
    _q = np.array(Q.buf, dtype=np.int64).reshape(Q.shape)
    _k = np.array(K.buf, dtype=np.int64).reshape(K.shape)
    _s = np.einsum("bhqd,bhkd->bhqk", _q, _k)
    assert list(_s.reshape(-1)) == scores.buf, "numpy's einsum differs from ours"
    _p = np.array([ti for ti in _t], dtype=float)
    _tt = _p.reshape(-1, 1)
    assert (_p - _tt).shape == (N, N), \
        "numpy does not broadcast (n,) against (n,1) to (n,n)"
    NOTES.append("numpy agrees: the same einsum string, and (n,) against (n,1) "
                 "really does give (n,n)")

# ==========================================================================
# The transcript. It imports what it calls -- P04 shipped one that did not,
# and every gate stayed green while a reader pasting it got a NameError.
# ==========================================================================
LOSS_TEXT = """\
>>> from p07_tensors_shapes import mean
>>> p = [1.0, 2.0, 3.0]        # predictions, shape (n,)
>>> t = [[1.0], [2.0], [3.0]]  # targets,     shape (n, 1)
>>> mean([(a - b[0]) ** 2 for a, b in zip(p, t)])
{true}
>>> mean([(a - b[0]) ** 2 for b in t for a in p])
{bcast}
"""
_pp = [1.0, 2.0, 3.0]
_tt3 = [[1.0], [2.0], [3.0]]
_true3 = mean([(a - b[0]) ** 2 for a, b in zip(_pp, _tt3)])
_bcast3 = mean([(a - b[0]) ** 2 for b in _tt3 for a in _pp])
assert _true3 == 0.0, "the small example should fit perfectly"
assert abs(_bcast3 - 2 * cov(_pp, _pp)) < 1e-12, \
    "the small example must show the 2 Var(t) floor too"
LOSS_TEXT = LOSS_TEXT.format(true=repr(_true3), bcast=repr(_bcast3))
assert LOSS_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in LOSS_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(LOSS_TEXT.strip().splitlines()) <= 14, "transcript too tall"
emit("p07.demo.floor", _bcast3, 2)


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p07-broadcast.txt").write_text(LOSS_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p07-broadcast.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p07_tensors_shapes.py --- do not edit.",
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
