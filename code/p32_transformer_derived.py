"""P32 --- The transformer, derived.

Every number Program P32 prints, and the assertions that keep them honest.

PART IX'S CONTRACT IS THAT IT INTRODUCES NO NEW MATHEMATICS.  So the question
this script had to answer first was not "what is left of the subject" but
"which lines of the brief have already been delivered".  `grep -rn 'prog:P32'
programs/en/*.tex` prints the deferrals with their contexts, and that grep was
the first thing run.  What it names:

  P25  DERIVES the 1/sqrt(d_k) in full -- its section 5 elicits it across
       frames 30-41, states the trap, and measures E9 -- and then says in as
       many words: "E9 is measured here on random vectors rather than on a
       trained model.  Program P32 assembles the architecture and measures it
       there... this program's job was to make the number derivable; that
       one's is to check it survives contact."
  F12  owns the vanishing product and hands over exactly one thing: "the
       architecture's own answer -- a path from the loss to the early layers
       that is not a long product at all -- is the residual connection, which
       Program P32 DERIVES."  It names the mechanism (line 668, "adds a path
       whose factors are 1") and does not derive it.  Greps confirm NO program
       does.
  P03  "What this program does not do is count a transformer block's
       parameters... The count itself is Program P32's, where every piece
       exists."  P06 hands over the same thing.  F02 supplies the
       feed-forward half already, as a collection of like terms: 8 d^2.
  P07  owns the reshape, the four axes and the one contraction, and closes
       "Program P32 assembles the rest."
  P02 softmax stability, P19 the convex combination, P05 the inner product,
  P04 the space, P18 the layer-norm gradient, F08 the rotation.  All SPENT.

SO EXACTLY THREE THINGS ARE THIS PROGRAM'S OWN: the block parameter count,
the residual stream derived, and the score measured through the ASSEMBLY.
Everything else is assembly, which is the part's contract working as designed.

METHOD, and it is the one P30 and P31 established: enumerate or derive in
closed form wherever possible, because a demonstration whose answer depends on
a seed measures the sampler.  Two probe designs failed before this script
existed -- see the note above ASSEMBLED SCORE -- and dropping the sampling
entirely turned out to be the finding.

Run:  python3 code/p32_transformer_derived.py
"""

from __future__ import annotations

import math
import random
import re
from fractions import Fraction
from itertools import combinations
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p32.tex"
TRANSCRIPT = OUT.parent.parent / "transcripts"
VALUES: dict[str, tuple[str, bool]] = {}


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
    """Another program's committed value, read back so the two cannot drift."""
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


def pct(x: float) -> float:
    """Refuse a percentage that rounds to 0 or 100 and so reads as exact."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not.")
    return x


def reproduces(value: float, digits: int, *operands, op) -> float:
    """Refuse a quantity that does not come back out of its own printed page."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


# ======================================================================
# THE COUNT.  Program F01 opens the book by having the reader work out what a
# seven-billion-parameter model weighs, and never says where the seven billion
# comes from -- on page three there is no vocabulary for it.  P03 commits the
# shape of the same model.  Those committed values, from two programs eleven
# parts apart, derive F01's headline number here.  Nothing is invented: d and
# L are read back, and the only new arithmetic is 12 d^2.
# ======================================================================
D_MODEL = int(committed("p03.tex", "p03.kv.dmodel") or 4096)
LAYERS = int(committed("p03.tex", "p03.kv.layers") or 32)
F01_PARAMS = int(committed("f01.tex", "f01.params") or 7_000_000_000)

emit("p32.d", D_MODEL)
emit("p32.layers", LAYERS)

# Attention projects the stream four times -- queries, keys, values, and the
# one that puts the heads back together.  Each is d x d.
ATTN_PER_BLOCK = 4 * D_MODEL * D_MODEL
# The feed-forward block is d -> 4d then 4d -> d.  That is F02's OWN worked
# collection of like terms, 4d^2 + 4d^2, so the reader has already produced it.
FFN_PER_BLOCK = 8 * D_MODEL * D_MODEL
PER_BLOCK = ATTN_PER_BLOCK + FFN_PER_BLOCK

assert PER_BLOCK == 12 * D_MODEL * D_MODEL
assert FFN_PER_BLOCK == 2 * ATTN_PER_BLOCK, (
    "the whole elicitation is that the feed-forward block holds TWICE what "
    "attention does; if that stops being true the frame is wrong, not the "
    "number.")

BLOCKS_TOTAL = PER_BLOCK * LAYERS
emit("p32.attn.block", ATTN_PER_BLOCK)
emit("p32.ffn.block", FFN_PER_BLOCK)
emit("p32.per.block", PER_BLOCK)
emit("p32.blocks.total", BLOCKS_TOTAL)

# How much of F01's headline number the blocks account for.  The remainder is
# the embedding, whose size depends on a vocabulary F01 never fixed -- so the
# honest statement is the FRACTION the blocks explain, not a total that would
# need a number nobody committed.
BLOCKS_PCT = pct(100.0 * BLOCKS_TOTAL / F01_PARAMS)
emit("p32.blocks.pct", BLOCKS_PCT, 1)
emit("p32.f01.params", F01_PARAMS)

# A vocabulary has to come from somewhere to say what the remainder buys, and
# it is a DESIGN CHOICE rather than a measurement, so it is named on the page
# as the assumption it is.
VOCAB = 32000
emit("p32.vocab", VOCAB)
EMBED = VOCAB * D_MODEL
emit("p32.embed", EMBED)
emit("p32.embed.pct", pct(100.0 * EMBED / F01_PARAMS), 1)

# The remainder, and the assertion is the INVARIANT rather than the figure:
# blocks plus one tied embedding must land inside a few per cent of F01's
# number, because if it did not the section would be describing a different
# model and the frames would need rewriting rather than the value updating.
WITH_EMBED = BLOCKS_TOTAL + EMBED
# Asserted and deliberately NOT emitted: the page quotes the blocks and the
# embedding separately, so a third number combining them would be arithmetic
# the reader does from two figures already in front of them.
assert 0.90 * F01_PARAMS < WITH_EMBED < 1.02 * F01_PARAMS, (
    WITH_EMBED, F01_PARAMS)


# ======================================================================
# THE ASSEMBLED SCORE.  P25 measured the spread of q.k on vectors DRAWN
# DIRECTLY and handed over "check it survives contact".  In a block q and k are
# PRODUCED: q = W_Q^T x and k = W_K^T y from a shared stream.
#
# TWO PROBE DESIGNS FAILED BEFORE THIS ONE, and both failures are in the
# frames.  The first redrew W_Q and W_K inside every trial, which is not a
# transformer -- a block has FIXED weights and varying inputs, so averaging
# over weight draws answers an easier question than the one P25 asked.  The
# second fixed the weights and was still 250M pure-Python operations.
#
# THE SAMPLING WAS UNNECESSARY, AND DROPPING IT IS THE FINDING:
#     q.k = (W_Q^T x).(W_K^T y) = x^T M y   with   M = W_Q W_K^T,
# and for independent standard-normal x and y that bilinear form has variance
# EXACTLY ||M||_F^2.  So ONE weight draw gives the score variance in closed
# form, with no sampling over inputs at all.  And in expectation over the
# weights, with entries of variance 1/d_model (which is the fan-in rule P25
# itself derives),
#     E||M||_F^2 = d_model^2 * d_k * (1/d_model)^2 = d_k,
# so THE ASSEMBLY PRESERVES P25'S d_k.  That is a derivation, not a
# measurement, and it needs no trained model.
# ======================================================================
random.seed(20260902)
ASM_DMODEL = 64
emit("p32.asm.dmodel", ASM_DMODEL)


def gram(W):
    """W^T W for W given as d_in rows of d_out."""
    d_out = len(W[0])
    G = [[0.0] * d_out for _ in range(d_out)]
    for row in W:
        for a in range(d_out):
            ra = row[a]
            if ra:
                Ga = G[a]
                for b in range(a, d_out):
                    Ga[b] += ra * row[b]
    for a in range(d_out):
        for b in range(a):
            G[a][b] = G[b][a]
    return G


def frob_sq_product(WQ, WK):
    """||W_Q W_K^T||_F^2 = trace((W_Q^T W_Q)(W_K^T W_K)), which costs
    d_k^2 d_model instead of the d_model^2 d_k of forming M."""
    A, B = gram(WQ), gram(WK)
    n = len(A)
    return sum(A[i][j] * B[i][j] for i in range(n) for j in range(n))


def randmat(rows, cols, sd):
    return [[random.gauss(0.0, sd) for _ in range(cols)] for _ in range(rows)]


ASM_DRAWS = 30
emit("p32.asm.draws", ASM_DRAWS)
SD_W = 1.0 / math.sqrt(ASM_DMODEL)

ASM_ROWS = []
for d_k in (8, 16, 32, 64):
    vals = [frob_sq_product(randmat(ASM_DMODEL, d_k, SD_W),
                            randmat(ASM_DMODEL, d_k, SD_W))
            for _ in range(ASM_DRAWS)]
    mean = sum(vals) / len(vals)
    ASM_ROWS.append((d_k, mean, math.sqrt(mean), vals))

# The claim is the EXPECTATION, which is exact, so that is what is asserted:
# the mean assembled variance tracks d_k.  The tolerance is what 30 draws can
# account for, not a number chosen to make the check pass -- the relative
# error of a mean of 30 draws of a quantity with a few per cent spread is a
# few per cent over root 30, so 8 per cent is generous and still fails on any
# real disagreement, which would be a FACTOR rather than a percentage.
for d_k, mean, sd, _ in ASM_ROWS:
    assert abs(mean - d_k) / d_k < 0.08, (d_k, mean)

# AND THE GATE: the assembled spread must reproduce P25's own committed raw
# spreads, at P25's own head sizes.  If P25's table ever moves, this section
# is quietly about a different measurement and the build says so.
for d_k, key in ((8, "p25.e9.raw.sd.8"), (64, "p25.e9.raw.sd.64")):
    p25 = committed("p25.tex", key)
    if p25 is not None:
        mean = next(m for k, m, _, _ in ASM_ROWS if k == d_k)
        assert abs(math.sqrt(mean) - float(p25)) / float(p25) < 0.05, (
            f"the assembled spread at d_k={d_k} is {math.sqrt(mean):.3f} "
            f"against P25's committed {p25}; the two programs are describing "
            f"different measurements.")

# Only the spread is quoted; the variance is its square and a value the page
# does not print is a second copy nobody would correct (F11's finding).
for d_k, mean, sd, _ in ASM_ROWS:
    emit(f"p32.asm.sd.{d_k}", sd, 2)

# The half P25's method CANNOT see.  A trained model has ONE weight draw, not
# an average over draws, so what its scores actually do is ||M||_F^2 for that
# one M -- which is not d_k.  Reported as a spread across draws, and labelled
# INDICATIVE on the page, because 30 draws estimates a spread to about 13%.
SPREADS = []
for d_k, mean, _, vals in ASM_ROWS:
    var = sum((v - mean) ** 2 for v in vals) / len(vals)
    SPREADS.append((d_k, 100.0 * math.sqrt(var) / mean))
for d_k, rel in SPREADS:
    emit(f"p32.asm.spread.{d_k}", pct(rel), 1)

# It falls as d_k grows, which is the one ordering that is structural: M has
# d_model^2 entries whatever d_k is, but its RANK is at most d_k, so a small
# head has fewer independent pieces to average over.
assert SPREADS[0][1] > SPREADS[-1][1], SPREADS


# ======================================================================
# THE RESIDUAL STREAM.  F12 proves that a plain chain's gradient is ONE
# PRODUCT and bounds it: sigma' <= 1/4, so 40 layers give at most 8.3e-25.  It
# then names the architecture's answer -- "a path from the loss to the early
# layers that is not a long product at all" -- and hands the derivation here.
#
# THE DERIVATION.  With y_k = x_k + f(x_k) the Jacobian of the stack is
# prod(1 + f'_k).  Expand that product and it is a SUM OVER 2^n PATHS, one per
# subset of layers: the subset says which layers you went THROUGH and which
# you went AROUND.  The empty subset -- around every layer, the identity path
# -- contributes exactly 1.
#
# So a plain chain's gradient is one product, which n small factors kill; a
# residual stack's is a sum whose first term is 1 and which no factor can
# kill.  That is F12's sentence turned into arithmetic, and it is exact.
# ======================================================================
DEPTH = int(committed("f12.tex", "f12.depth") or 40)
SIGMA_MAX = Fraction(committed("f12.tex", "f12.sig.max") or "0.25")
emit("p32.depth", DEPTH)

# The gate: F12's own bound, recomputed here on F12's own chain.
PLAIN_BEST = SIGMA_MAX ** DEPTH
f12_bound = committed("f12.tex", "f12.vanish.bound")
if f12_bound is not None:
    assert f"{float(PLAIN_BEST):.1e}" == f"{float(f12_bound):.1e}", (
        f"this program recomputes F12's plain-chain bound as "
        f"{float(PLAIN_BEST):.1e} against its committed {f12_bound}; the two "
        f"are supposed to be the same chain.")
emit("p32.plain.bound", f"{float(PLAIN_BEST):.1e}")

# The path sum, exact over fractions.  Enumerating 2^n subsets is only
# affordable for a small n -- which is enough, because the identity is an
# identity: what it establishes at n = 4 it establishes everywhere.
PATH_N = 4
emit("p32.path.n", PATH_N)
emit("p32.path.count", 2 ** PATH_N)
_a = [Fraction(1, k + 2) for k in range(PATH_N)]
_prod = Fraction(1)
for _x in _a:
    _prod *= (1 + _x)
_paths = Fraction(0)
for _r in range(PATH_N + 1):
    for _sub in combinations(range(PATH_N), _r):
        _t = Fraction(1)
        for _i in _sub:
            _t *= _a[_i]
        _paths += _t
assert _prod == _paths, (_prod, _paths)

# The empty subset is the identity path.  Asserting "it equals 1" against a
# literal 1 is an assertion that cannot fail, which is the defect P01 and P05
# both recorded -- so what is checked is the CONSEQUENCE, and it is the whole
# claim: turn every layer off, and a plain chain's gradient is exactly 0 while
# a residual stack's is exactly 1.  The identity path is the only term left.
_off = [Fraction(0)] * PATH_N
_plain_off = Fraction(1)
_resid_off = Fraction(1)
for _x in _off:
    _plain_off *= _x
    _resid_off *= (1 + _x)
assert _plain_off == 0, _plain_off
assert _resid_off == 1, _resid_off

# And with the layers back on, the residual stack's Jacobian EXCEEDS the sum
# over every path that goes through at least one layer, by exactly 1.
_through = _paths - 1
assert _prod - _through == 1, (_prod, _through)

# What the two stacks do at initialisation, where f' is small and centred on
# zero.  This is an illustration of an exact result rather than the result, so
# what is asserted is the ORDERING and the fact that the residual stack stays
# of order one -- both structural -- and never a figure.
RES_TRIALS = 20000
RES_SD = 0.1
emit("p32.res.trials", RES_TRIALS)
emit("p32.res.sd", RES_SD, 1)
_plain, _resid = [], []
for _ in range(RES_TRIALS):
    fs = [random.gauss(0.0, RES_SD) for _ in range(DEPTH)]
    p = r = 1.0
    for f in fs:
        p *= f
        r *= (1.0 + f)
    _plain.append(abs(p))
    _resid.append(r)
_plain.sort()
_resid.sort()
PLAIN_MED = _plain[len(_plain) // 2]
RESID_MED = _resid[len(_resid) // 2]
WITHIN = 100.0 * sum(1 for r in _resid if 0.5 < r < 2.0) / RES_TRIALS

assert PLAIN_MED < 1e-30, PLAIN_MED
assert 0.5 < RESID_MED < 2.0, RESID_MED
assert WITHIN > 50.0, WITHIN
emit("p32.res.plain.med", f"{PLAIN_MED:.1e}")
emit("p32.res.resid.med", RESID_MED, 2)
emit("p32.res.within", pct(WITHIN), 0)


# ======================================================================
# THE COST.  P03 measured the KV cache and owns the finding that attention's
# compute is quadratic in the sequence while its cache is linear.  It is NOT
# re-taught here.  What the assembly adds is WHY the cache has the size P03
# measured: K and V are two of the block's four projections, so each position
# contributes one d-vector each, per layer -- which is a statement about the
# shapes this program has just counted, and it derives P03's committed number.
# ======================================================================
BYTES = 2                                     # two bytes a number, as F01 sets
SEQ = int(committed("p03.tex", "p03.kv.seq") or 8192)
emit("p32.seq", SEQ)
emit("p32.bytes", BYTES)

# two tensors (K and V), one d-vector per position, per layer
KV_BYTES = 2 * LAYERS * D_MODEL * SEQ * BYTES
KV_GIB = KV_BYTES / 2 ** 30
p03_kv = committed("p03.tex", "p03.kv.gib")
if p03_kv is not None:
    assert abs(KV_GIB - float(p03_kv)) < 0.01, (
        f"the cache derived from the block's own shapes is {KV_GIB:.3f} GiB "
        f"against P03's committed {p03_kv}; the assembly and the measurement "
        f"are supposed to be the same model.")
emit("p32.kv.gib", KV_GIB, 0)

# Per token in flight, which is the number a serving budget is written in.
#
# THIS GATE FIRED, and it found a defect in a merged program.  P03 computed
# this figure as kv_bytes(1) / 2**20 -- MEBIbytes -- under a key named `.mb`
# and printed it as "MB", two lines below printing the cache itself in GiB.
# It escaped because 0.5 MiB is 0.524 MB and both round to 0.5 at one decimal:
# P17's shape exactly, a formula whose two readings agree numerically and stay
# invisible until they do not.  And P03's OWN summary warns about this
# confusion -- "GB is 10^9 and GiB is 2^30, about seven per cent larger".
# The value is mebibytes, so the label is now MiB and the key says so; no
# printed digit changed.
KV_PER_TOKEN_MIB = 2 * LAYERS * D_MODEL * BYTES / 2 ** 20
p03_per = committed("p03.tex", "p03.kv.per.token.mib")
if p03_per is not None:
    assert abs(KV_PER_TOKEN_MIB - float(p03_per)) < 0.01, (
        KV_PER_TOKEN_MIB, p03_per)
emit("p32.kv.per.token.mib", KV_PER_TOKEN_MIB, 1)

# The head count follows from the head width P03 committed, and it is the one
# number multi-head needs that the parameter count does not: h heads of width
# d/h cost exactly what one head of width d costs, which is why the reshape is
# free and why P07 could call it a reshape.
D_HEAD = int(committed("p03.tex", "p03.flop.dhead") or 128)
HEADS = D_MODEL // D_HEAD
assert HEADS * D_HEAD == D_MODEL, (HEADS, D_HEAD, D_MODEL)
emit("p32.d.head", D_HEAD)
emit("p32.heads", HEADS)

# The two exponents, side by side, at the shape this program has been using.
# P03 owns the finding; what is new is that both numbers now come out of one
# block's own arithmetic rather than being asserted about attention in general.
SCORES = HEADS * SEQ * SEQ                    # one score per query-key pair per head
emit("p32.scores", f"{SCORES:.2e}")
CACHE_VECTORS = 2 * LAYERS * SEQ              # one K and one V per position per layer
emit("p32.cache.vectors", f"{CACHE_VECTORS:.2e}")
# double the sequence: the scores go up fourfold and the cache twofold
assert (HEADS * (2 * SEQ) ** 2) == 4 * SCORES
assert (2 * LAYERS * 2 * SEQ) == 2 * CACHE_VECTORS


# ======================================================================
# THE TRANSCRIPT.  The identity path, made concrete.  Nothing is rounded, so
# there is no transformation for the listing to hide -- which is P19's rule,
# applied by having nothing to apply it to.
# ======================================================================
NOTES: list[str] = []
_lines = [
    ">>> def stack(fs):        # (plain chain, residual stack)",
    "...     p = r = 1.0",
    "...     for f in fs:",
    "...         p *= f",
    "...         r *= (1.0 + f)",
    "...     return p, r",
    "...",
    ">>> stack([0.0] * 40)     # every layer contributes nothing",
]


def _stack(fs):
    p = r = 1.0
    for f in fs:
        p *= f
        r *= (1.0 + f)
    return p, r


_off = _stack([0.0] * DEPTH)
_lines.append(repr(_off))
_lines += [
    ">>> stack([0.05] * 40)    # every layer contributes a little",
    repr(_stack([0.05] * DEPTH)),
]

# The listing's own claims, asserted rather than trusted: with every layer off
# the plain chain is exactly zero and the residual stack is exactly one -- the
# identity path and nothing else -- and with the layers on the plain chain has
# vanished while the residual stack has not.
assert _off == (0.0, 1.0), _off
_on = _stack([0.05] * DEPTH)
assert _on[0] < 1e-50 and _on[1] > 1.0, _on
assert max(len(x) for x in _lines) <= 64, max(_lines, key=len)
TRANSCRIPT.mkdir(parents=True, exist_ok=True)
(TRANSCRIPT / "p32-two-stacks.txt").write_text("\n".join(_lines) + "\n",
                                               encoding="utf8")
NOTES.append(
    "  * the identity path is not an approximation: with every layer off the"
    " plain chain is exactly 0 and the residual stack exactly 1")
NOTES.append(
    f"  * the blocks are {BLOCKS_PCT:.1f} per cent of Program F01's committed"
    f" {F01_PARAMS:,} parameters, from P03's own d and L")


# ======================================================================
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf8") as fh:
    fh.write("% Generated by code/p32_transformer_derived.py -- do not edit.\n")
    for k, (body, numeric) in VALUES.items():
        fh.write(f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}\n")

print(f"P32: {len(VALUES)} values -> {OUT}")
for n in NOTES:
    print(n)
