#!/usr/bin/env python3
"""Program F1 --- Numbers, powers and roots.

Every number Program F1 prints is computed here and written to
figures/values/f01.tex, which the book \\input{}s. The book contains no digits
of its own for this program; it contains references. A value that changes here
changes in both editions at once, and a value that stops being produced prints
a visible marker and fails CI.

Run:  python3 code/f01_numbers.py      (or: make numbers)
"""
from __future__ import annotations

from pathlib import Path

VALUES: dict[str, str] = {}


def emit(key: str, value, digits: int | None = None) -> None:
    """Record one value under the name the book will reference it by."""
    if isinstance(value, float) and digits is not None:
        VALUES[key] = f"{value:.{digits}f}"
    elif isinstance(value, float):
        VALUES[key] = repr(value)
    else:
        VALUES[key] = str(value)


# --------------------------------------------------------------------------
# Sizing a model. The worked payoff of the program: parameters times bytes per
# parameter is memory, and the reader computes it rather than repeating it.
# --------------------------------------------------------------------------
PARAMS = 7_000_000_000                 # a "7B" model
BYTES_FP16 = 2
BYTES_FP32 = 4

weights_bytes = PARAMS * BYTES_FP16
emit("f01.params", PARAMS)
emit("f01.weights.bytes", weights_bytes)
emit("f01.weights.gb", weights_bytes / 1e9, 0)            # decimal gigabytes
emit("f01.weights.gib", weights_bytes / 2**30, 2)         # binary gibibytes
emit("f01.weights.fp32.gb", PARAMS * BYTES_FP32 / 1e9, 0)

# The kilo/kibi gap, expressed the way the book states it: a gibibyte is N per
# cent MORE bytes than a gigabyte. The reciprocal form (a gigabyte is 6.9% of a
# gibibyte less) is also true, reads as a different number, and is not used --
# so it is not emitted. A value the book does not reference is a number carried
# without justification, and `make debt` counts it.

# --------------------------------------------------------------------------
# 2^10 against 10^3. The approximation everyone uses, and the error it carries
# when it is compounded -- which is where it stops being harmless.
# --------------------------------------------------------------------------
emit("f01.two.ten.err.pct", (2**10 / 10**3 - 1) * 100, 2)
emit("f01.two.eighty", 2**80)
emit("f01.two.eighty.err.pct", (2**80 / 10**24 - 1) * 100, 2)

# --------------------------------------------------------------------------
# Training cost, to an order of magnitude. The standard estimate is that
# training costs about 6 FLOPs per parameter per token: two for the forward
# multiply-accumulate and four for the backward pass. It is an estimate and the
# book says so; what matters here is that the reader can do the arithmetic.
# --------------------------------------------------------------------------
TOKENS = 2_000_000_000_000              # 2 trillion training tokens
FLOPS_PER_PARAM_TOKEN = 6
train_flops = FLOPS_PER_PARAM_TOKEN * PARAMS * TOKENS
emit("f01.tokens", TOKENS)
emit("f01.train.flops", f"{train_flops:.2e}".replace("e+", "e"))
emit("f01.train.flops.exp", len(str(train_flops)) - 1)

# A device sustaining 4e14 FLOP/s at a realistic utilisation.
DEVICE_FLOPS = 4e14
UTILISATION = 0.4
device_seconds = train_flops / (DEVICE_FLOPS * UTILISATION)
emit("f01.device.flops", f"{DEVICE_FLOPS:.0e}".replace("e+", "e"))
emit("f01.device.util.pct", UTILISATION * 100, 0)
emit("f01.device.days", device_seconds / 86400, 0)
emit("f01.device.years", device_seconds / (86400 * 365), 1)
emit("f01.devices.for.30.days", device_seconds / (86400 * 30), 0)

# A larger model, for the exercise the reader does unaided.
BIG_PARAMS = 70_000_000_000
emit("f01.big.params", BIG_PARAMS)
emit("f01.big.gb", BIG_PARAMS * BYTES_FP16 / 1e9, 0)

# The binary prefixes, so the table in the program is generated rather than
# typed. A table of powers is exactly the kind of thing that acquires a typo.
for name, k in (("kib", 10), ("mib", 20), ("gib", 30), ("tib", 40)):
    if name == "gib":                      # the only one the text spells out
        emit(f"f01.{name}.bytes", 2**k)
    emit(f"f01.{name}.over.si.pct", (2**k / 10 ** (3 * (k // 10)) - 1) * 100, 1)

# Estimating: a novel of 100,000 words, at the rule of thumb that a token is
# about three quarters of an English word.
WORDS = 100_000
emit("f01.novel.words", WORDS)
emit("f01.novel.tokens", round(WORDS / 0.75))

# --------------------------------------------------------------------------
# Ratios and percentages. "50% faster" is ambiguous and the ambiguity is
# expensive; the program makes the reader compute both readings.
# --------------------------------------------------------------------------
BASE_MS = 200.0
emit("f01.base.ms", BASE_MS, 0)
emit("f01.fifty.pct.less.ms", BASE_MS * 0.5, 0)          # half the time
emit("f01.fifty.pct.more.rate.ms", BASE_MS / 1.5, 1)     # 1.5x the throughput
emit("f01.speedup.discrepancy.ms", BASE_MS / 1.5 - BASE_MS * 0.5, 1)

# --------------------------------------------------------------------------
# Write the file the book reads.
# --------------------------------------------------------------------------
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f01.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f01_numbers.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ]
    lines += [f"\\mfaval{{{k}}}{{{v}}}" for k, v in VALUES.items()]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf8")
    width = max(len(k) for k in VALUES)
    for k, v in VALUES.items():
        print(f"  {k:<{width}}  {v}")
    print(f"\n  {len(VALUES)} values -> {OUT.relative_to(OUT.parents[2])}")


if __name__ == "__main__":
    main()
