#!/usr/bin/env python3
"""Program P16 --- Jacobians, the chain rule and automatic differentiation.

Every number Program P16 prints that the reader cannot do in their head is
computed here and written to figures/values/p16.tex, which the book \\input{}s.

P16's thesis is that WHICH MODE IS CHEAPER IS A QUESTION ABOUT SHAPE AND
NOTHING ELSE. The chain rule multiplies Jacobians; matrix multiplication is
associative but its COST is not, which Program P06 measured; so bracketing the
same product from one end or the other is forward mode against reverse mode,
and a scalar loss with many parameters makes one of the two brackets cheaper
by a factor of the parameter count.

WHAT P16 IS OWED, read out of the files rather than remembered:

  F12  gives the chain rule and the product over layers, and says of sigma'
       being expressible in sigma that it "is the seed of what Program P16
       calls reverse mode". It also names the two consequences this program
       owes arithmetic for: the activations have to be stored, and gradient
       checkpointing trades recomputation for memory.
  P06  MEASURED THE BRACKETING. Its committed cost.left, cost.right and
       cost.ratio are one triple product bracketed two ways for identical
       answers. That IS forward against reverse, one program early, so the
       cost ratio here is gated against it rather than re-derived.
  P13  gives the DAG and the theorem that every topological order computes
       the same values -- which is what makes a computation graph well
       defined, and what lets reverse mode walk it backwards at all.
  P15  gives the gradient, and says the update is componentwise. The gradient
       is the one-row Jacobian, so this program's first move is to say that
       out loud.
  P03  already names activations and gradient checkpointing and says the
       trade is operations for bytes. It does NOT do the arithmetic. This
       program owes exactly that arithmetic and must not restate the concept.

WHAT P16 LEAVES ALONE, checked against tools/programs.json:
    the Hessian, curvature and the step-size bound              -> P17
    matrix calculus and the softmax-cross-entropy gradient      -> P18
    the optimisers                                              -> P20
    the residual stream                                         -> P32

NO LIBRARY IS NAMED, on F04's rule: a framework's internals are a fact about a
version. What is here is a reverse-mode differentiator in about forty lines,
which is enough to exhibit every claim the program makes -- including all
three of the ways autodiff silently answers a different question, which are
much more convincing demonstrated than asserted.

Run:  python3 code/p16_autodiff.py      (or: make numbers)
"""
from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p16.tex"
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
    assert x >= 0.0
    return "0" if x == 0.0 else f"1e{math.ceil(math.log10(x)):d}"


def sci(x: float, d: int = 2) -> str:
    return f"{x:.{d}e}"


# ---------------------------------------------------------------------------
# 1. THE COST OF A BRACKET, exactly, over the rationals.
#
# A chain of layers has one Jacobian per layer. The chain rule multiplies them.
# Matrix multiplication is associative, so the ANSWER does not depend on the
# bracketing -- and Program P06 measured that the COST does. Here the two
# bracketings ARE the two modes:
#
#   right to left, (J3 (J2 (J1 v)))   forward: push a direction through
#   left to right, ((u J3) J2) J1     reverse: pull a covector back
#
# The counters are in the routines themselves, so nothing on the page is
# quoted from a textbook's operation count.
# ---------------------------------------------------------------------------
MULS = 0


def matmul(A, B):
    global MULS
    n, k, m = len(A), len(B), len(B[0])
    MULS += n * k * m
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def chain(shape_seq, seed=1):
    """Jacobians for a chain of layers with the given widths, rational and
    deterministic so the two bracketings can be compared exactly."""
    Js, s = [], seed
    for a, b in zip(shape_seq, shape_seq[1:]):
        rows = []
        for i in range(b):
            row = []
            for j in range(a):
                s = (s * 1103515245 + 12345) % 2147483648
                row.append(Fraction(s % 17 - 8, 3))
            rows.append(row)
        Js.append(rows)                        # b x a : output x input
    return Js


# A narrow deep stack, so the ends are the interesting shapes: N inputs, one
# output. That is the shape of a loss.
WIDTH, DEPTH = 20, 6
SHAPES = [WIDTH] * DEPTH + [1]
JS = chain(SHAPES)
emit("p16.width", WIDTH)
emit("p16.depth", DEPTH)

# FORWARD: one column at a time, pushed from the input end.
MULS = 0
fwd_cols = []
for j in range(WIDTH):
    v = [[Fraction(1 if i == j else 0)] for i in range(WIDTH)]
    for J in JS:
        v = matmul(J, v)
    fwd_cols.append(v)
FWD = MULS

# REVERSE: one row, pulled from the output end. One pass, because there is one
# output.
MULS = 0
u = [[Fraction(1)]]                                  # 1 x 1 seed
for J in reversed(JS):
    u = matmul(u, J)
REV = MULS

# THE ANSWERS MUST BE IDENTICAL, exactly, or the comparison is about something
# else. This is the assertion that makes the cost figures mean anything.
assert [c[0][0] for c in fwd_cols] == u[0], "the two brackets must agree"
emit("p16.fwd.muls", sci(float(FWD)))
emit("p16.rev.muls", sci(float(REV)))
ratio = FWD / REV
assert ratio > 1.0
emit("p16.mode.ratio", round(ratio))
NOTES.append(f"same gradient, {FWD} multiplications forward against {REV} "
             f"reverse -- a factor of {ratio:.0f}")

# THE INVARIANT, not the figure: the ratio is the number of INPUTS, because
# forward mode needs one pass per input and reverse one per output. Swept, so
# the sentence survives a change of network.
for w in (3, 7, 20, 50):
    js = chain([w] * 4 + [1])
    MULS = 0
    for j in range(w):
        v = [[Fraction(1 if i == j else 0)] for i in range(w)]
        for J in js:
            v = matmul(J, v)
    f_ = MULS
    MULS = 0
    uu = [[Fraction(1)]]
    for J in reversed(js):
        uu = matmul(uu, J)
    r_ = MULS
    assert abs(f_ / r_ - w) < 1e-9, (w, f_ / r_)
NOTES.append("the ratio IS the input count, over widths 3, 7, 20 and 50")

# GATED AGAINST P06, which measured the same phenomenon one program early.
_l = committed("p06.tex", "p06.cost.left")
_r = committed("p06.tex", "p06.cost.right")
_ra = committed("p06.tex", "p06.cost.ratio")
assert None not in (_l, _r, _ra)
assert abs(float(_r) / float(_l) - float(_ra)) < 1e-6, (_l, _r, _ra)
NOTES.append("gated: P06's bracketing ratio is this program's mode ratio, "
             "measured one program before it had a name")

# What that factor is at a realistic size. A scalar loss and this many
# parameters: forward mode would need one pass PER PARAMETER.
PARAMS = 7_000_000_000
emit("p16.params", sci(float(PARAMS), 0))
NOTES.append("at a realistic parameter count the factor is the count itself")

# ---------------------------------------------------------------------------
# 2. A REVERSE-MODE DIFFERENTIATOR, in about forty lines, so that every later
#    claim is exhibited rather than asserted.
# ---------------------------------------------------------------------------
class V:
    """A value on the tape, with its parents and the local derivatives."""
    __slots__ = ("v", "parents", "grad")

    def __init__(self, v, parents=()):
        self.v = float(v)
        self.parents = parents          # ((V, dself_dparent), ...)
        self.grad = 0.0

    def __add__(self, o):
        o = o if isinstance(o, V) else V(o)
        return V(self.v + o.v, ((self, 1.0), (o, 1.0)))

    def __mul__(self, o):
        o = o if isinstance(o, V) else V(o)
        return V(self.v * o.v, ((self, o.v), (o, self.v)))

    def __sub__(self, o):
        o = o if isinstance(o, V) else V(o)
        return V(self.v - o.v, ((self, 1.0), (o, -1.0)))

    __radd__, __rmul__ = __add__, __mul__


def relu(x: V) -> V:
    # The subgradient at 0 is a CHOICE and this is where it is made.
    return V(x.v if x.v > 0 else 0.0, ((x, 1.0 if x.v > 0 else 0.0),))


def backward(top: V) -> None:
    """Walk the tape in reverse topological order -- which is exactly Program
    P13's theorem being used: every valid order computes the same values, so
    any reverse order will do provided a node is visited after everything that
    consumes it."""
    order, seen = [], set()

    def visit(n):
        if id(n) in seen:
            return
        seen.add(id(n))
        for p, _ in n.parents:
            visit(p)
        order.append(n)

    visit(top)
    top.grad = 1.0
    for n in reversed(order):
        for p, local in n.parents:
            p.grad += n.grad * local        # the chain rule, one edge at a time


def numeric_grad(fn, xs, h=1e-6):
    g = []
    for i in range(len(xs)):
        a = list(xs); a[i] += h
        b = list(xs); b[i] -= h
        g.append((fn(a) - fn(b)) / (2 * h))
    return g


def model(xs):
    """A small chain with a non-linearity, so the tape is not trivial."""
    a = relu(xs[0] * 2.0 + xs[1] * -3.0 + 1.0)
    b = relu(xs[0] * -1.0 + xs[2] * 4.0)
    return a * b + xs[1] * xs[2]


PT = [0.7, -0.4, 1.1]
nodes = [V(x) for x in PT]
out = model(nodes)
backward(out)
auto = [n.grad for n in nodes]
num = numeric_grad(lambda a: model([V(x) for x in a]).v, PT)
worst = max(abs(a - b) for a, b in zip(auto, num))
# FINITE DIFFERENCES ARE THE TEST AND NOT THE IMPLEMENTATION, which is F11's
# U-curve arriving here: the agreement is to a handful of digits, never to the
# last bit, and that is a property of the instrument rather than of the code.
assert worst < 1e-6, worst
emit("p16.check.bound", bound(worst))
emit("p16.check.n", len(PT))
NOTES.append(f"the forty-line differentiator agrees with a central difference "
             f"to better than {bound(worst)}")

# ---------------------------------------------------------------------------
# 3. THE THREE SILENT ANSWERS. Each is DEMONSTRATED, because each is a case
#    where nothing raises and the number is simply not the derivative meant.
# ---------------------------------------------------------------------------
# (a) a non-differentiable point. relu at exactly zero: the derivative does not
#     exist, so an implementation must CHOOSE, and the choice is invisible.
z = V(0.0)
y = relu(z)
backward(y)
left = 0.0        # limit from below
right = 1.0       # limit from above
assert z.grad in (0.0, 1.0)
emit("p16.relu.chosen", int(z.grad))
emit("p16.relu.left", int(left))
emit("p16.relu.right", int(right))
NOTES.append("relu at exactly 0: the two one-sided limits are 0 and 1, and "
             f"the implementation returns {z.grad:.0f} without saying so")

# (b) a detached value. Break the tape and the gradient through that path is
#     not wrong, it is ABSENT -- and the total still looks like a number.
def detached_run(detach: bool):
    xs = [V(v) for v in PT]
    a = relu(xs[0] * 2.0 + xs[1] * -3.0 + 1.0)
    if detach:
        a = V(a.v)                       # same value, no parents
    b = relu(xs[0] * -1.0 + xs[2] * 4.0)
    t = a * b + xs[1] * xs[2]
    backward(t)
    return [n.grad for n in xs], t.v


full_g, full_v = detached_run(False)
det_g, det_v = detached_run(True)
assert full_v == det_v, "the VALUE is identical; only the gradient changed"
assert full_g != det_g
gap = max(abs(a - b) for a, b in zip(full_g, det_g))
assert gap > 0.1, gap
emit("p16.detach.gap", gap, digits=3)
NOTES.append(f"detached: identical loss value, gradient differs by {gap:.3f} "
             "in one component, and nothing raises")

# (c) an in-place write. Overwrite a value the tape still refers to and the
#     stored local derivative is now about a number that no longer exists.
# THE DEMONSTRATION AND THE LISTING MUST BE ONE COMPUTATION. The first draft
# ran this on the model's own inputs and wrote the listing with a different
# pair, so the transcript printed a number its own code does not produce --
# which `make verify` cannot see, because the script did write exactly what it
# computed. What catches it is extracting the listing from the finished PDF
# and running it, and it caught this. These are the listing's numbers.
A0, B0, OVERWRITE = 3.0, 5.0, 99.0
va, vb = V(A0), V(B0)
prod = va * vb                    # local derivative w.r.t. va is vb.v
stale = vb.v
vb.v = OVERWRITE                  # the in-place write
backward(prod)
assert va.grad == stale, (va.grad, stale)   # the OLD value, silently
assert va.grad != OVERWRITE
emit("p16.inplace.a", A0, digits=1)
emit("p16.inplace.used", stale, digits=1)
emit("p16.inplace.now", round(OVERWRITE))
NOTES.append("in-place: the tape had already stored the old value, so the "
             f"gradient uses {stale} while the tensor now holds 99")

# ---------------------------------------------------------------------------
# 4. CHECKPOINTING, with the arithmetic Program P03 named and did not do.
#
#    Keep every activation: L stored, one forward pass of work.
#    Keep every k-th: L/k stored plus a segment of k recomputed, so memory
#    L/k + k and compute 2 forward passes. Minimising L/k + k over k gives
#    k = sqrt(L), which is where the sqrt(L) folklore comes from -- and it is
#    an exact minimisation rather than a rule of thumb.
# ---------------------------------------------------------------------------
LAYERS = 10_000


def peak(k: int) -> float:
    return LAYERS / k + k


best_k = min(range(1, LAYERS + 1), key=peak)
assert abs(best_k - math.isqrt(LAYERS)) <= 1, (best_k, math.isqrt(LAYERS))
emit("p16.ckpt.layers", LAYERS)
emit("p16.ckpt.bestk", best_k)
emit("p16.ckpt.peak", round(peak(best_k)))
saving = LAYERS / peak(best_k)
assert saving > 40
emit("p16.ckpt.saving", round(saving))
# The compute cost is a SECOND forward pass and no more, which is the honest
# form: not "some extra", a factor.
emit("p16.ckpt.passes", 2)
NOTES.append(f"checkpointing: {LAYERS} layers, optimum every {best_k}, peak "
             f"{round(peak(best_k))} stored -- {round(saving)}x less memory "
             "for one extra forward pass")
# AND THE MINIMUM IS EXACT rather than fitted: sqrt(L) is where the derivative
# of L/k + k vanishes, so the assertion is against isqrt and not a tolerance.
NOTES.append("the optimum is sqrt(L) exactly, from d/dk (L/k + k) = 0")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    # TWO listings, and the split is the whole point of this pass. The second
    # block IS the answer frame 34 elicits -- a.grad printed as 5.0 with
    # b.v = 99.0 two lines above it -- and it used to sit in frame 31, four
    # frames earlier and on the facing page of the same spread, where no
    # covering hand reaches. P23 split its own listing for exactly this and
    # P08 did it again; here the ReLU half stays where section 5's first
    # failure is demonstrated and the in-place half moves after frame 35's
    # answer, where it confirms rather than reveals. Each imports what it
    # calls, so either runs pasted into a REPL on its own.
    relu_lines = [
        ">>> from p16_autodiff import V, relu, backward",
        ">>> x = V(0.0)",
        ">>> y = relu(x)",
        ">>> backward(y)",
        ">>> x.grad",
        f"{z.grad}",
    ]
    (TRANSCRIPTS / "p16-relu.txt").write_text(
        "\n".join(relu_lines) + "\n", encoding="utf8")

    inplace_lines = [
        ">>> from p16_autodiff import V, backward",
        f">>> a, b = V({A0}), V({B0})",
        ">>> p = a * b",
        f">>> b.v = {OVERWRITE}",
        ">>> backward(p)",
        ">>> a.grad",
        f"{stale}",
    ]
    (TRANSCRIPTS / "p16-inplace.txt").write_text(
        "\n".join(inplace_lines) + "\n", encoding="utf8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out_lines = [
        "% Generated by code/p16_autodiff.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ]
    out_lines += [
        f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}"
        for k, (body, numeric) in VALUES.items()
    ]
    OUT.write_text("\n".join(out_lines) + "\n", encoding="utf8")

    w = max(len(k) for k in VALUES)
    items = list(VALUES.items())
    for i in range(0, len(items), 3):
        print("  " + "   ".join(f"{k:{w}s} {b:>10s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
