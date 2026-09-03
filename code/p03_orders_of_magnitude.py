#!/usr/bin/env python3
"""Program P03 --- Orders of magnitude: O-notation, FLOPs and memory.

Every number Program P03 prints that the reader cannot do in their head is
computed here and written to figures/values/p03.tex, which the book \\input{}s.

P03's thesis is that ASYMPTOTIC NOTATION IS A STATEMENT ABOUT GROWTH AND SAYS
NOTHING ABOUT WHICH OF TWO IMPLEMENTATIONS IS FASTER TODAY, and that both
facts matter. P01 asked what the arithmetic is; P02 asked which algorithms
survive it; this program asks what it costs.

WHAT P03 IS OWED, and pays. Five programs promise it by name, and each was
opened before this script was written:

  * F01 -- the weights are a FLOOR, and "optimiser state, activations and the
    key--value cache are counted properly in Program P03". Twice, and it is
    the largest single debt.
  * F02 -- "Program P03 sizes a network this way", of computing the shape at
    every layer before running anything.
  * F04 -- twice: prices work in FLOPs rather than counting pairs, and prices
    a model in sigma notation, "needing nothing more than the arithmetic you
    have".
  * F10 -- the sharpest, and it names three things: O-notation "needs its own
    definition, its own warnings about what it does NOT say, and a worked
    account of why the faster of two implementations today can be the slower
    one at scale. Program P03 does all three."
  * P02 -- "the next question about the same arithmetic: not whether it is
    right, but what it costs."

THE MEASUREMENTS:

  1. THE CROSSOVER, computed rather than asserted. An n^2 algorithm with a
     small constant against an n log n one with a large constant, and the
     exact n at which they trade places. That is F10's "worked account", and
     the number is much larger than people expect.

  2. THE MEMORY BILL, in full. F01 established the weights. This adds the
     optimiser state, the gradients and the activations, and the headline is
     what fraction of the training bill the weights actually are.

  3. THE KEY--VALUE CACHE, and the observation that matters: attention's
     COMPUTE is quadratic in the sequence and its CACHE IS LINEAR. Almost
     everybody expects both to be quadratic.

  4. ARITHMETIC INTENSITY as a ratio, for a matrix multiply and for an
     elementwise operation, against a device's own FLOP-per-byte ratio. That
     ratio is the whole of the compute-bound/memory-bound distinction, and it
     gives the size below which even a matrix multiply is memory-bound.

  5. WHAT FUSION BUYS, as a factor rather than as an argument.

WHAT P03 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    what a matrix IS, and matrix multiplication as composition     -> P06
    the transformer's parameter count, which needs shapes          -> P32
    shape checking as a discipline, broadcasting, einsum           -> P07
P03 counts operations and bytes. It never says what the operations mean, and
where it needs a matrix multiply it describes it as the dot products F09
already gave the reader.

DEVICE FIGURES ARE STATED ASSUMPTIONS, NOT MEASUREMENTS, exactly as F01's
already are. The frames say so. What transfers is the ratio and the method.

Run:  python3 code/p03_orders_of_magnitude.py      (or: make numbers)
"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p03.tex"
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
# SECTION 2 --- the crossover, which is what O-notation does not tell you
#
# Two implementations of one job. A is quadratic with a tight inner loop; B is
# n log n with an expensive one -- an allocation, a comparison through a
# callback, a cache miss per element. The constants are STATED, because the
# point does not depend on their values and every real pair has its own.
# ==========================================================================
C_QUAD, C_LINLOG = 1.0, 200.0


def cost_quad(n: int) -> float:
    return C_QUAD * n * n


def cost_linlog(n: int) -> float:
    return C_LINLOG * n * math.log2(n)


# Bisection rather than a formula: n^2 = c n log2 n has no elementary
# solution, and finding it numerically is what the reader would do.
lo, hi = 2, 1 << 40
while lo + 1 < hi:
    mid = (lo + hi) // 2
    if cost_quad(mid) < cost_linlog(mid):
        lo = mid
    else:
        hi = mid
CROSSOVER = hi
emit("p03.cross.c1", f"{C_QUAD:.0f}")
emit("p03.cross.c2", f"{C_LINLOG:.0f}")
emit("p03.cross.n", CROSSOVER)
assert cost_quad(CROSSOVER - 1) < cost_linlog(CROSSOVER - 1), "below the crossover the quadratic is not faster"
assert cost_quad(CROSSOVER) >= cost_linlog(CROSSOVER), "at the crossover the quadratic is still faster"

# The two things the frames quote either side of it, so the reader can see
# that the ASYMPTOTICALLY WORSE algorithm wins over a range that covers most
# real inputs.
# Always the ratio of the SLOWER to the faster, so the number on the page is
# above one and reads the same way in both directions. The first draft emitted
# linlog/quad throughout and printed 0.0 above the crossover, which is a ratio
# nobody can read and hides that the quadratic is now thirty times worse.
for _n in (100, 1000, 100_000):
    _r = cost_linlog(_n) / cost_quad(_n)
    emit(f"p03.cross.ratio.{_n}", f"{max(_r, 1 / _r):.0f}")
    # WHICH one is slower is a WORD, and the two editions spell it
    # differently, so it cannot be a shared value -- and a \mfavaltext key is
    # not in the ledger's produced set anyway, which is F10's finding. The
    # frames write it. What is asserted here is that they write it correctly.
    assert (_r > 1) == (_n < CROSSOVER), (
        f"at n = {_n} the loser is no longer the one the frames name")
assert cost_linlog(100) / cost_quad(100) > 10, "at n = 100 the n log n form is no longer far slower"
NOTES.append(f"the crossover is at n = {CROSSOVER:,}; at n = 100 the n log n form costs "
             f"{cost_linlog(100)/cost_quad(100):.0f}x as much")


# ==========================================================================
# SECTION 4 --- the memory bill, which is F01's largest debt here
#
# F01 computed the weights and said in as many words that they are a FLOOR.
# The recipe below is the ordinary mixed-precision one: sixteen-bit weights
# and gradients, and an optimiser holding a thirty-two-bit master copy plus
# two moments. NO LIBRARY IS NAMED, for the reason F04 gives about optimiser
# internals -- what transfers is the arithmetic, which the reader can redo
# with whatever their own recipe holds.
# ==========================================================================
PARAMS = 7_000_000_000
BYTES_HALF, BYTES_FULL = 2, 4
GB = 10 ** 9

BILL = {
    "weights": PARAMS * BYTES_HALF,
    "grads": PARAMS * BYTES_HALF,
    "master": PARAMS * BYTES_FULL,
    "moment1": PARAMS * BYTES_FULL,
    "moment2": PARAMS * BYTES_FULL,
}
TOTAL_BILL = sum(BILL.values())
for _k, _v in BILL.items():
    emit(f"p03.mem.{_k}", f"{_v / GB:.0f}")
emit("p03.mem.total", f"{TOTAL_BILL / GB:.0f}")
emit("p03.mem.weights.pct", f"{BILL['weights'] / TOTAL_BILL * 100:.0f}")
emit("p03.mem.multiple", f"{TOTAL_BILL / BILL['weights']:.0f}")
emit("p03.mem.optimiser", f"{(BILL['master'] + BILL['moment1'] + BILL['moment2']) / GB:.0f}")

# The invariant, not the figure: the weights must be a small minority of the
# training bill, because that is the whole point of the section. A recipe that
# made them the majority would need the frames rewritten, not the number
# updated.
assert BILL["weights"] / TOTAL_BILL < 0.2, (
    f"the weights are now {BILL['weights']/TOTAL_BILL:.0%} of the training "
    f"bill; F01's 'this is a floor' no longer has anything behind it")
assert TOTAL_BILL / BILL["weights"] == 8, "the bill is no longer eight times the weights"

# --- the cross-programme gate: these ARE F01's weights ---
_f01 = committed("f01.tex", "f01.weights.gb")
if _f01 is None:                                             # pragma: no cover
    NOTES.append("f01.tex absent: F01's weight figure was NOT checked against P03")
else:
    assert int(_f01) == round(BILL["weights"] / GB), (
        f"P03 makes the weights {BILL['weights']/GB:.0f} GB where F01 committed "
        f"{_f01}: the two programs no longer size the same model")
    NOTES.append(f"F01's {_f01} GB of weights is re-derived here and agrees")


# ==========================================================================
# The key--value cache. THE POINT IS THE EXPONENT, not the size: attention's
# compute is quadratic in the sequence and its cache is LINEAR, and almost
# everybody expects both to be quadratic because they remember the n^2.
# ==========================================================================
LAYERS, D_MODEL = 32, 4096
SEQ, BATCH = 8192, 1


def kv_bytes(seq: int, batch: int = BATCH) -> int:
    """Two tensors, per layer, of width d_model, per position, per sequence."""
    return 2 * LAYERS * D_MODEL * seq * batch * BYTES_HALF


emit("p03.kv.layers", LAYERS)
emit("p03.kv.dmodel", D_MODEL)
emit("p03.kv.seq", SEQ)
emit("p03.kv.gib", f"{kv_bytes(SEQ) / 2 ** 30:.0f}")
emit("p03.kv.per.token.mib", f"{kv_bytes(1) / 2 ** 20:.1f}")
emit("p03.kv.double.gib", f"{kv_bytes(2 * SEQ) / 2 ** 30:.0f}")
assert kv_bytes(SEQ) == 4 * 2 ** 30, "the cache is no longer exactly 4 GiB at these shapes"
assert kv_bytes(2 * SEQ) == 2 * kv_bytes(SEQ), "the cache is no longer linear in the sequence"
NOTES.append(f"the cache is {kv_bytes(SEQ)/2**30:.0f} GiB at {SEQ} tokens and doubles when the sequence does")


# ==========================================================================
# SECTION 5 --- arithmetic intensity
#
# FLOPs per byte moved. The device figures are STATED, as F01's are, and the
# frames say so; what transfers is the ratio and the method.
# ==========================================================================
DEV_FLOPS = 4e14                     # F01's figure, re-used deliberately
DEV_BYTES = 2e12                     # stated, of the same order as HBM
DEV_RATIO = DEV_FLOPS / DEV_BYTES
emit("p03.dev.flops", f"{DEV_FLOPS:.0e}")
emit("p03.dev.bytes", f"{DEV_BYTES:.0e}")
emit("p03.dev.ratio", f"{DEV_RATIO:.0f}")

_dev = committed("f01.tex", "f01.device.flops")
if _dev is None:                                             # pragma: no cover
    NOTES.append("f01.tex absent: the device rate was NOT checked against F01")
else:
    assert float(_dev) == DEV_FLOPS, (
        f"P03 assumes {DEV_FLOPS:.0e} FLOP/s where F01 assumed {_dev}: the two "
        f"programs should size the same device or say why not")
    NOTES.append(f"F01's device rate {_dev} FLOP/s is the one assumed here")

MATMUL_N = 4096


def matmul_intensity(n: int, b: int = BYTES_HALF) -> float:
    """2n^3 multiply-adds against three n-by-n operands read or written."""
    return (2 * n ** 3) / (3 * n * n * b)


def elementwise_intensity(b: int = BYTES_HALF) -> float:
    """One operation per element, two read and one written. n cancels."""
    return 1.0 / (3 * b)


emit("p03.ai.matmul.n", MATMUL_N)
emit("p03.ai.matmul", f"{matmul_intensity(MATMUL_N):.0f}")
emit("p03.ai.elementwise", f"{elementwise_intensity():.2f}")
emit("p03.ai.gap", f"{matmul_intensity(MATMUL_N) / elementwise_intensity():.0f}")
emit("p03.ai.short", f"{DEV_RATIO / elementwise_intensity():.0f}")

# A matrix multiply is compute-bound only above a size, and the size is worth
# computing because it is not small: 2n/(3b) = device ratio.
SMALL_N = math.ceil(DEV_RATIO * 3 * BYTES_HALF / 2)
emit("p03.ai.smalln", SMALL_N)
assert matmul_intensity(SMALL_N) >= DEV_RATIO > matmul_intensity(SMALL_N - 1), (
    "the size at which a matmul becomes compute-bound has moved")
assert elementwise_intensity() < DEV_RATIO, "an elementwise op is no longer memory-bound"
assert matmul_intensity(MATMUL_N) > DEV_RATIO, "a 4096-square matmul is no longer compute-bound"
NOTES.append(f"a matmul is compute-bound above n = {SMALL_N} and an elementwise op never is")

# What fusion buys, as a factor. Three elementwise operations in a row move
# three times as many bytes unfused as fused, for the same FLOPs.
CHAIN = 3
_unfused_bytes = CHAIN * 3 * BYTES_HALF
_fused_bytes = 3 * BYTES_HALF
emit("p03.fuse.chain", CHAIN)
emit("p03.fuse.factor", f"{_unfused_bytes / _fused_bytes:.0f}")
emit("p03.fuse.after", f"{CHAIN / _fused_bytes:.2f}")
assert _unfused_bytes / _fused_bytes == CHAIN, "fusion no longer saves a factor of the chain length"

# How long a fused chain would have to be to reach the device, which is the
# number the frames used to assert away. Bytes are fixed once the chain is
# fused, so intensity is linear in the chain length and unbounded; what makes
# "fusion does not rescue" true is the SIZE of this number, not a ceiling.
FUSE_COMPUTE_CHAIN = round(DEV_RATIO * _fused_bytes)
emit("p03.fuse.compute.chain", FUSE_COMPUTE_CHAIN)
assert FUSE_COMPUTE_CHAIN > 500, FUSE_COMPUTE_CHAIN
# And it has to reproduce from the two figures the page prints beside it,
# which is the recorded rule: divide the numbers AS THE PAGE PRINTS THEM.
_page = float(VALUES["p03.dev.ratio"][0]) / (
    float(VALUES["p03.fuse.after"][0]) / float(VALUES["p03.fuse.chain"][0]))
assert f"{_page:.0f}" == f"{FUSE_COMPUTE_CHAIN}", (_page, FUSE_COMPUTE_CHAIN)
assert CHAIN / _fused_bytes < DEV_RATIO, (
    "a fused chain of three is now compute-bound, which would make the "
    "frame's point that fusion helps and does not rescue")


# ==========================================================================
# SECTION 3 --- FLOPs, and F04's debt
#
# F04 counted attention's PAIRS and said P03 prices the work in FLOPs. The
# translation is the one the reader can check: each pair costs a dot product
# of length d_head, and F09 already said what a dot product costs.
# ==========================================================================
D_HEAD, HEADS = 128, 32
_f04_pairs = committed("f04.tex", "f04.causal.pairs")
if _f04_pairs is None:                                       # pragma: no cover
    NOTES.append("f04.tex absent: the pair count was NOT taken from F04")
    PAIRS = 2_098_176
else:
    PAIRS = int(_f04_pairs)
    NOTES.append(f"F04's {PAIRS:,} causal pairs are priced here rather than recounted")

emit("p03.flop.pairs", PAIRS)
emit("p03.flop.dhead", D_HEAD)
emit("p03.flop.heads", HEADS)
emit("p03.flop.perhead", f"{2 * PAIRS * D_HEAD:.2e}")
emit("p03.flop.allheads", f"{2 * PAIRS * D_HEAD * HEADS:.2e}")
assert 2 * PAIRS * D_HEAD * HEADS > 1e10, "the attention score cost has fallen below 10 GFLOP"

# 6ND, which F01 used and F04 pointed at, re-derived from the same parameters
# so that the two programs are provably quoting one arithmetic.
TOKENS = 2_000_000_000_000
emit("p03.train.flops", f"{6 * PARAMS * TOKENS:.2e}")
_f01_train = committed("f01.tex", "f01.train.flops")
if _f01_train is not None:
    # Compared as a NUMBER, not as a string: F01 emits 8.40e22 and this script
    # formats 8.40e+22, and a gate that fires on the plus sign is checking the
    # formatter rather than the arithmetic.
    assert float(f"{6 * PARAMS * TOKENS:.2e}") == float(_f01_train), (
        f"P03 makes the training cost {6*PARAMS*TOKENS:.2e} where F01 committed "
        f"{_f01_train}")
    NOTES.append(f"F01's training total {_f01_train} FLOPs is re-derived here and agrees")


# ==========================================================================
# The transcript. Nothing typed.
# ==========================================================================
CROSS_TEXT = f""">>> from math import log2
>>> quad = lambda n: {C_QUAD:.0f} * n * n
>>> linlog = lambda n: {C_LINLOG:.0f} * n * log2(n)
>>> [round(linlog(n) / quad(n), 1) for n in (100, 1000, 100000)]
{[round(cost_linlog(n) / cost_quad(n), 1) for n in (100, 1000, 100000)]}
>>> next(n for n in range(2, 10**6) if quad(n) >= linlog(n))
{CROSSOVER}
"""
assert CROSS_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in CROSS_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(CROSS_TEXT.strip().splitlines()) <= 14, "transcript too tall for one frame"
assert next(n for n in range(2, 10 ** 6) if cost_quad(n) >= cost_linlog(n)) == CROSSOVER, (
    "the transcript's one-liner disagrees with the bisection above")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p03-crossover.txt").write_text(CROSS_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p03-crossover.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p03_orders_of_magnitude.py --- do not edit.",
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
    print(f"\n  {len(VALUES)} values -> figures/values/p03.tex")
    for note in NOTES:
        print(f"  {note}")


if __name__ == "__main__":
    main()
