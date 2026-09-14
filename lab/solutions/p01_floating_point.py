"""Lab P1 -- reference solutions.

These exist so the build can prove the exercises are solvable:
lab/tools/labcheck.py --tests runs every check against this file
and requires it to pass, and against lab/exercises/ and requires
it to fail. They are for a reader whose own check already passes,
the way an answer at the back of the book is.

The region markers mirror the exercise file's, and the two files
must export the same names; labcheck --files enforces both.
"""
import math
import struct


# region: gap
def gap(x: float) -> float:
    """The distance from x to the next double above it."""
    bits = struct.unpack("<Q", struct.pack("<d", x))[0]
    above = struct.unpack("<d", struct.pack("<Q", bits + 1))[0]
    return above - x
# endregion: gap


# region: epsilon
def epsilon(mbits: int) -> float:
    """The gap between 1 and the next number up."""
    return 2.0 ** -mbits


def decimal_digits(mbits: int) -> int:
    """Rounded to the nearest digit, as the program counts."""
    return round(-math.log10(epsilon(mbits)))
# endregion: epsilon


# region: tenth
def error_in_gaps() -> float:
    """The error in 0.1 + 0.2, in gaps at 0.3."""
    return ((0.1 + 0.2) - 0.3) / math.ulp(0.3)
# endregion: tenth


# region: orders
def two_orders(a: float, b: float, c: float) -> tuple:
    """((a + b) + c, a + (b + c))."""
    return (a + b) + c, a + (b + c)
# endregion: orders


# region: threshold
def threshold(x: float) -> float:
    """The smallest t with x + t != x, by bisection."""
    lo, hi = 0.0, math.ulp(x)   # x + lo == x, x + hi != x
    while True:
        mid = (lo + hi) / 2
        if mid <= lo or mid >= hi:   # cannot be halved further
            return hi
        if x + mid == x:
            lo = mid
        else:
            hi = mid
# endregion: threshold


# region: flips
_CODES = {"fp64": "<d", "fp32": "<f", "fp16": "<e"}


def store(x: float, fmt: str) -> float:
    """x rounded to fmt and read back."""
    if fmt == "bf16":
        return to_bf16(x)
    code = _CODES[fmt]
    return struct.unpack(code, struct.pack(code, x))[0]


def flips_to_zero(fmt: str) -> int:
    """Halvings of 1.0 until the stored value is exactly 0."""
    x, n = 1.0, 0
    while x != 0.0:
        x = store(x * 0.5, fmt)
        n += 1
    return n
# endregion: flips


# region: bf16
def to_bf16(x: float) -> float:
    """Round to bfloat16: nearest, ties to even."""
    bits = struct.unpack("<I", struct.pack("<f", x))[0]
    lsb = (bits >> 16) & 1
    rounded = (bits + 0x7FFF + lsb) & 0xFFFF0000
    return struct.unpack("<f", struct.pack("<I", rounded))[0]
# endregion: bf16
