"""Lab P1 -- Floating point: what the machine actually computes.

Open this file on one side of the screen and the lab PDF on the
other. Every function below is one exercise. The PDF names the
frames of Program P1 each one rests on and says what to write
down BEFORE you run anything; the check then compares your code
with the numbers the book prints, and with nothing else.

Check your work (nothing needed beyond Python 3.11):

    python3 lab/check.py p01           # every exercise
    python3 lab/check.py p01 -k gap    # one exercise
    python3 -m pytest lab/tests/test_p01.py   # with pytest

A function that still raises NotImplementedError is one you have
not started. Replace the raise with your code. Keep the names and
the signatures: the check calls them by name.
"""
import math
import struct


# region: gap
def gap(x: float) -> float:
    """The distance from x to the next double above it.

    Read it off the bits, as Program P1 does: pack x as 64
    bits with struct, add one to the integer, unpack the
    result, and subtract x.
    """
    raise NotImplementedError("Lab P1, exercise 1")
# endregion: gap


# region: epsilon
def epsilon(mbits: int) -> float:
    """Machine epsilon for a format that stores `mbits`
    significand bits: the gap between 1 and the next
    representable number above it."""
    raise NotImplementedError("Lab P1, exercise 2")


def decimal_digits(mbits: int) -> int:
    """About how many decimal digits that epsilon buys, to the
    nearest whole digit, which is how Program P1 counts them."""
    raise NotImplementedError("Lab P1, exercise 2")
# endregion: epsilon


# region: tenth
def error_in_gaps() -> float:
    """The error in 0.1 + 0.2, measured in gaps at 0.3.

    Return ((0.1 + 0.2) - 0.3) divided by the gap at 0.3,
    keeping the sign. math.ulp gives the gap.
    """
    raise NotImplementedError("Lab P1, exercise 3")
# endregion: tenth


# region: orders
def two_orders(a: float, b: float, c: float) -> tuple:
    """The same sum bracketed two ways, as a pair:
    ((a + b) + c, a + (b + c))."""
    raise NotImplementedError("Lab P1, exercise 4")
# endregion: orders


# region: threshold
def threshold(x: float) -> float:
    """The smallest positive t with x + t != x, by bisection.

    Start from the interval (0, math.ulp(x)]: adding nothing
    moves x nowhere, and adding a whole gap moves it to its
    neighbour. Halve the interval until it cannot be halved
    any further, keeping the largest t that vanished and the
    smallest that did not, and return the latter.
    """
    raise NotImplementedError("Lab P1, exercise 5")
# endregion: threshold


# region: flips
def store(x: float, fmt: str) -> float:
    """x rounded to a format and read back.

    fmt is 'fp64', 'fp32' or 'fp16'; struct's codes for them
    are '<d', '<f' and '<e'. Packing rounds to nearest, and
    unpacking returns the stored value as a Python float.
    'bf16' has no struct code: exercise 7 builds to_bf16,
    and store should hand 'bf16' to it.
    """
    raise NotImplementedError("Lab P1, exercise 6")


def flips_to_zero(fmt: str) -> int:
    """How many times 1.0 is multiplied by 0.5 before the
    value stored in `fmt` is exactly zero. Round to the
    format after every step, with store()."""
    raise NotImplementedError("Lab P1, exercise 6")
# endregion: flips


# region: bf16
def to_bf16(x: float) -> float:
    """x rounded to bfloat16: an fp32 with the low sixteen
    bits of its pattern rounded away, to nearest, ties to even.

    Take the fp32 bit pattern of x as an integer, round it at
    bit 16, clear the low sixteen bits, and unpack it again.
    """
    raise NotImplementedError("Lab P1, exercise 7")
# endregion: bf16
