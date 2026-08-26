# Program F1 — frame-by-frame plan

**Title (en):** Numbers, powers and roots · **(pl):** Liczby, potęgi i pierwiastki
**Files:** `programs/{en,pl}/F01-numbers-powers-roots.tex` · **Values:** `code/f01_numbers.py`
**Frame count:** 55 (band enforced by `tools/check_structure.py` is 30–70)

> **This plan is reconciled with work already in the repository.** F01 is being
> drafted: 15 of 55 frames, 8 outcomes and a 12-item Quiz are written. This
> document keeps every commitment already made in that file, specifies frames
> 16–55, and supplies the four sections that are wholly absent. Where it
> disagrees with the draft it says so explicitly (§3.3 — one defect found).

---

## 1. The subject decision

### 1.1 The proposal, and the verdict

The proposed subject was **"Numbers and machine arithmetic"** — number sets and place
value opening onto IEEE-754, fp16 overflow in attention logits, log-sum-exp,
catastrophic cancellation in a variance computation, epsilon in layer norm, and bf16's
exponent-for-mantissa trade.

**Verdict: reject the scope, keep the instinct.** F1 stays *Numbers, powers and roots*.
Machine arithmetic is not F1's subject; it is P1's and P2's.

Four arguments land in the same place, and one is fatal on its own.

**(a) It cannibalises two programs that already exist.** `structure.tex` allocates
P1 *Floating point: what the machine actually computes* (45 frames) and P2 *Numerical
error, stability and computing in log-space* (50 frames). Read their stubs against the
proposal and the overlap is close to total:

| Proposed F1 topic | Already owned by |
|---|---|
| bf16 vs fp16, exponent budget, overflow threshold | P1 (named in its stub) |
| machine epsilon | P1 (named in its stub) |
| non-associativity of a gradient sum | P1 (named in its stub) |
| fp16 overflow in attention logits | P2 (named in its stub) |
| log-sum-exp, max-subtraction | P2 (named in its stub) |
| catastrophic cancellation in variance, Welford | P2 (named in its stub) |

Adopting the proposal does not add a program; it empties two, and makes the reader meet
IEEE-754 twice, three hundred pages apart, with P1 demoted to revision. If the proposal
were right the honest move would be to delete P1 and P2 and renumber Part II — and
nobody is proposing that, because Part II is the structural departure the introduction
singles out and defends.

**(b) It breaks the triage contract. This is the fatal one.** Part I is triaged by Quiz.
`frontmatter/*/how-to-use.tex` tells a reader with a degree to work the thirteen
Foundation quizzes and *nothing else*, entering a program only where its Quiz goes badly
and entering it at the frames the failed question names. That mechanism assumes each
Foundation Quiz is a fair proxy for its whole program.

Put machine arithmetic inside F1 and the mechanism inverts. A senior engineer sits the
F1 Quiz, answers the index-law and scientific-notation questions cold, scores well, and
is told to skip — skipping precisely the fp16/bf16 material the book most wants them to
have. Meanwhile the beginner, who fails and enters at frame 1, reaches bit layouts by
frame 30 of a program advertised as assuming nothing. **One program cannot serve both
populations through one diagnostic.** The F1/P1 split is what lets the book serve both,
and it is the method's own mechanism, not a housekeeping preference.

**(c) It forward-references.** A real treatment of machine arithmetic needs logarithms:
bf16's exponent budget is a log-scale statement, log-sum-exp is a logarithm identity,
and "orders of magnitude" is base-10 logs with the name filed off. Logarithms are F3.
Stroud does not forward-reference inside Part I, and he is right not to — a Foundation
program that leans on a later one cannot be entered from its own Quiz.

**(d) It does not fit.** Number sets, place value, bases, indices, roots, scientific
notation, orders of magnitude, IEEE-754, fp16/bf16, log-sum-exp and cancellation is
comfortably 120 frames. `check_structure.py` enforces 30–70 and would fail the build.
The band is not arbitrary: it is the size at which a program can be worked in one
sitting, which is what the retake-the-Quiz loop assumes.

### 1.2 What the proposal was right about

Its instinct is sound and must be honoured: **F1 must land somewhere a senior engineer
still learns something.** A Foundation program that stops at surds has failed this
audience. F1 earns its keep three ways, and the drafted frames already do the first:

1. **It answers 0.1 completely, at its own level.** The reason 0.1 has no exact binary
   form is place value in a base — in base 2, $\tfrac1{10}$ behaves exactly as
   $\tfrac13$ behaves in base 10. That needs no mantissa, no exponent field, no rounding
   rule. F1 gives the **reason**; P1 gives the **machinery**. This matters: the method's
   claim is that an elicited misconception is *corrected*, and a trap deferred three
   hundred pages is elicited without being corrected — the worst of both. The drafted
   frame 5 gets this right.
2. **It plants the sentence P1 cashes** (frame 32): a float is normalised scientific
   notation in base 2 on a fixed digit budget. Two consequences follow with no bit
   layout at all — relative precision is constant, absolute spacing grows with
   magnitude.
3. **It ends on the payoff arithmetic**: model memory, 6ND, device-days, GB against GiB,
   and how to quote a ratio without lying.

### 1.3 Consequences to action

- **Keep** the title and the argument. The draft already reflects the decision.
- **Amend the stub comment** to name the two deliberate hand-offs, so a later pass does
  not read F1 as having under-delivered: *0.1 is answered at place-value level here, the
  bit-level machinery is P1's; frame 32 plants the scientific-notation-in-base-2
  sentence that P1 cashes.*
- **Fix a stale comment.** `preamble.tex` line 896 reads
  `\newcommand{\Fset}{\mathbb{F}}   % the floating-point numbers, F1's subject`.
  Floating point is **P1's** subject. This is a leftover from an earlier scoping —
  corroborating that the question was once live — and it will mislead the next person to
  open the preamble. Change to `P1's subject`.
- **Record in CLAUDE.md** under *Resolved questions* that the F1/P1 boundary was
  challenged and re-affirmed, with argument (b) as the reason, so it is not
  re-litigated.

---

## 2. Status of the draft

| Part of the skeleton | State |
|---|---|
| `\program`, `\label`, `\index` | done |
| Learning outcomes | **8 declared**, frames 1–55 (§3) |
| Quiz | **12 items**, every one with `\answerto{}` and `\teachesat{}` |
| Frames | **15 of 55** written (through the indices section) |
| Summary | **absent** |
| Can you? | **absent** (generated, but `\canyou` is not called) |
| Test exercises | **absent** |
| Further problems | **absent** |
| Figures | 1 of 4 (`f01-number-sets`) |
| Polish edition | **0 frames** — the whole program is parity debt |

`make debt` will currently report F01 as written in neither language (the `\programstub`
is gone from `en`, so `make stubs` counts it as written while four of its seven skeleton
sections are missing — worth noting that the stub ledger cannot see a half-written
program; `make frames` catches it via the 30–70 band).

---

## 3. Learning outcomes and the frame contract

### 3.1 The eight outcomes, as committed

These are already in the file. They generate *Can you?*, so they are the load-bearing
version; §7 restates them rather than re-deciding them.

| # | Outcome | Frames |
|---|---|---|
| O1 | say which set a number belongs to, and why the answer changes what a program can do with it | 1–7 |
| O2 | use the laws of indices, including the zero and negative exponents, without stopping to think | 8–17 |
| O3 | read a fractional index as a root, and move between the two forms in either direction | 18–24 |
| O4 | write any quantity in scientific notation, and multiply, divide and compare quantities while they stay in it | 25–33 |
| O5 | estimate an order of magnitude in your head, and say how far the estimate can be trusted | 34–40 |
| O6 | compute the memory a model's weights need from its parameter count and its precision | 41–46 |
| O7 | tell a gigabyte from a gibibyte, and say which one a piece of tooling is reporting | 47–51 |
| O8 | state a speed-up unambiguously, and spot the two readings of "fifty per cent faster" | 52–55 |

They partition 1–55 with no gap and no overlap, which is what makes the generated
checklist a complete route back.

### 3.2 The frame contract the Quiz has already fixed

Each `\teachesat{}` is a promise to route a reader to specific frames. The unwritten
frames must therefore teach what the Quiz says they teach. This is the binding
specification for frames 16–55:

| Q | Asks | `\teachesat` |
|---|---|---|
| Q1 | which of $-4,\ \tfrac72,\ \sqrt9,\ \sqrt7$ are rational | 1–7 |
| Q2 | simplify $2^6\times2^{-2}$ | 9–15 |
| Q3 | what is $5^0$, and why | **14** ← wrong, see §3.3 |
| Q4 | write $81^{3/4}$ without an index | 18–23 |
| Q5 | is $\sqrt{9+16}=\sqrt9+\sqrt{16}$ | **24** |
| Q6 | write $0.00042$ in scientific notation | 25–27 |
| Q7 | compute $(3{\times}10^8)(2{\times}10^{-3})$ | 28–29 |
| Q8 | by what percentage is "$2^{10}\approx$ a thousand" wrong | **35–36** |
| Q9 | bytes for a 7B model at 2 bytes/parameter | 41–45 |
| Q10 | 14 GB against 13.04 GiB — which is wrong | 47–49 |
| Q11 | 200 ms and now "fifty per cent faster" | **52–53** |
| Q12 | FLOPs to train 7B on 2T tokens at 6 FLOPs/parameter/token | 37–40 |

The bolded rows place three of the five traps before a single one of those frames has
been written. §4 honours all of them.

### 3.3 One defect found in the drafted Quiz

**Q3 carries `\teachesat{14}`. $5^0$ is asked at frame 11 and derived at frame 12.**
Frame 14 is the worked-with-gaps answer block for negative indices. The route sends a
reader who fails Q3 two frames past the derivation they needed.

Fix: `\teachesat{11--12}`.

This is worth more than the one-line correction. The Summary's back-references and every
Quiz route navigate by frame number, and `tools/parity.py` compares an *ordered*
structural signature precisely because a histogram cannot see a frame move. A drift of
two frames appeared in a program that is 27% written, before any renumbering pressure
has been applied. **Frame references should be inserted last, against the finished
frame numbering, or written as `\label`/`\ref` pairs rather than literals** — the
preamble's `\framelabelfix` exists to make `\label` inside `\begin{fr}` capture the
frame number, and it is currently unused in F01.

---

## 4. The frames

**Frames 1–15 are written.** For the record, and because the traps and the scaffolding
audit depend on them:

| # | What it does |
|---|---|
| 1–3 | $\N$ (with $0\in\N$ stated as this book's convention), $\Z$ forced by subtraction, $\Q$ forced by division — each elicited by a situation, not asserted |
| 4 | $\tfrac13 = 0.333\dots$; a rational's expansion stops or repeats, and *that it repeats is a fact about base ten, not about $\tfrac13$* — in base 3 it is exactly $0.1$ |
| 5 | **Trap 1.** "Is $0.1$ simple or awkward?" → *Simple* → "the right answer in base ten and the wrong answer about your computer". `trapbox`. Then irrationals and $\R$ |
| 6–7 | Classify $7,\,-17,\,\tfrac{22}7,\,\sqrt2,\,\sqrt9$ — with $\sqrt9$ as the sting: a form is not a set |
| 8–10 | $a^n$; the product law derived by counting; the quotient and power-of-a-power laws |
| 11 | **Trap 2.** "Is $2^3\times3^2=6^5$?" → No. `trapbox`: **every index law requires a common base** |
| 12–13 | $a^0=1$ and $a^{-n}=1/a^n$, both *derived* from the quotient law; a negative index is a reciprocal, not a negative number |
| 14–15 | Worked with gaps (three expressions), then `\yourturn` on $(x^2)^3x^{-4}/x^{-1}$; `aibox` on $n^2d$ attention cost |

**Frames 16–55 are specified below.** **R** = the response the frame demands, **A** = the
answer opening the next frame. ▸ marks `\yourturn`; ⚠ marks a trap.

`check_structure.py` requires that any frame containing `\blank`, `\dotline` or
`\yourturn` is followed by one opening with `\ans{}` or `\ansblock`. Frame 55 is last and
demands nothing, which the checker permits.

### O2 completed — indices (16–17)

| # | Teaches | R | A |
|---|---|---|---|
| 16 | All three laws in one expression, worked with gaps. | $(10^6)^2/10^{-3}$ and $2^{10}\times2^{10}$ | $10^{15}$; $2^{20}$ |
| 17 | The four facts as one table (product, quotient, power, zero/negative) — the reference the rest of the book uses. ▸ | Simplify $(2^{-2}\times2^{5})^2/2^{4}$ | $2^2 = 4$ |

### O3 — fractional indices and roots (18–24)

| # | Teaches | R | A |
|---|---|---|---|
| 18 | Roots as the inverse of powers; $\sqrt{\ }$ and $\sqrt[n]{\ }$. Worked: $\sqrt[3]{27}=3$. | $\sqrt{64}$ and $\sqrt[3]{8}$ | 8; 2 |
| 19 | $a^{1/2}=\sqrt a$ **derived**, not asserted: $(a^{1/2})^2 = a^1$ by the power-of-a-power law. | $16^{1/2}$ | 4 |
| 20 | Generalise: $a^{1/n}=\sqrt[n]{a}$. Worked: $32^{1/5}=2$. | $81^{1/4}$ | 3 |
| 21 | $a^{m/n} = (\sqrt[n]{a})^m$, and the practical rule — **take the root first**, because the numbers stay small. Both orders shown for $8^{2/3}$: $(\sqrt[3]8)^2=4$ against $\sqrt[3]{64}=4$. | $27^{2/3}$ | 9 |
| 22 | Worked with gaps, three at once. | $4^{3/2}$, $9^{-1/2}$, $125^{2/3}$ | 8; $\tfrac13$; 25 |
| 23 | ▸ Negative and fractional together — the form that stops people. | $16^{-3/4}$ | $\tfrac18$ |
| 24 ⚠ | **Trap 3** (Quiz Q5 routes here). Ask straight: is $\sqrt{9+16} = \sqrt9+\sqrt{16}$? Elicit the commitment, then state flatly that it is wrong: $\sqrt{25}=5$, not 7. `trapbox`: roots and powers distribute over a **product**, never over a **sum** — and the same kills $(a+b)^2 = a^2+b^2$. `aibox`: this *is* the L2 norm. $\lVert(3,4)\rVert_2 = 5$; a reader who adds component magnitudes has computed the L1 norm, 7, and called it Euclidean distance. | Compute $\lVert(3,4)\rVert_2$ and $\lVert(3,4)\rVert_1$ | 5; 7 |

### O4 — scientific notation (25–33)

| # | Teaches | R | A |
|---|---|---|---|
| 25 | Normalised form $a\times10^n$, $1\le|a|<10$. Worked both ways: $14\,000\,000\,000 \to 1.4\times10^{10}$, $0.00025 \to 2.5\times10^{-4}$. | Write $93\,000\,000$ in normalised form | $9.3\times10^7$ |
| 26 | The exponent counts places moved and its sign says which way. Worked with gaps. | $0.00042$ and $6\,400\,000$ | $4.2\times10^{-4}$; $6.4\times10^6$ |
| 27 | ▸ Both directions, one small and one that is a plant for frame 35. | $0.0000000072$ and $1024$ | $7.2\times10^{-9}$; $1.024\times10^3$ |
| 28 | Multiplication: multiply mantissas, **add exponents** — index law 1 doing the work. Worked, including renormalising when the mantissa leaves $[1,10)$: $(5{\times}10^4)(4{\times}10^3) = 20{\times}10^7 = 2{\times}10^8$. | $(4\times10^6)(2\times10^5)$ | $8\times10^{11}$ |
| 29 | Division: divide mantissas, subtract exponents. Worked with gaps, then ▸. | $(8{\times}10^9)/(2{\times}10^4)$; then $(6{\times}10^{-3})/(3{\times}10^{-7})$ | $4\times10^5$; $2\times10^4$ |
| 30 | Comparing: compare exponents first, mantissas only on a tie. | Which is larger, $9.9\times10^{11}$ or $1.1\times10^{12}$? | $1.1\times10^{12}$ |
| 31 | Significant figures. The mantissa says **what**, the exponent says **where**. | How many s.f. in $6.022\times10^{23}$ and in $1.4\times10^{10}$? | Four; two |
| 32 | **The bridge to Part II.** A float is normalised scientific notation *in base 2*, with a fixed budget of significant bits and a fixed exponent range. Demonstrated on a toy 3-significant-decimal-digit format. **Figure 2** here. | Gap between representable numbers near 1000? And near 1? | 10; 0.01 |
| 33 | So the gap **scales with the magnitude** — a thousand times the number, a thousand times the gap. Constant *relative* precision, growing *absolute* spacing, from scientific notation alone with no bit layout. `rigourbox`: P1 supplies the binary widths and machine epsilon. | Gap-fill: the mantissa fixes the $\blank$; the exponent fixes the $\blank$ | relative error; range |

### O5 — orders of magnitude (34–40)

| # | Teaches | R | A |
|---|---|---|---|
| 34 | An order of magnitude is a factor of ten; estimating by keeping only the exponent. | How many orders of magnitude between $10^3$ and $10^9$? | Six |
| 35 ⚠ | **Trap 4, set** (Quiz Q8 routes here). $2^{10}=1024$, "about a thousand". So is $2^{80}$ about $10^{24}$ — within a few percent? Demand a yes/no **and** a percentage. | Commit to both | No — it exceeds $10^{24}$ by 20.89% |
| 36 ⚠ | **Trap 4, sprung.** State flatly. The mechanism: $2^{10}/10^3 = 1.024$, an error of 2.4%; used eight times the error **multiplies**, $1.024^8 = 1.2089$. Print the 25 digits of $2^{80}$ in a display. `trapbox`. | By what factor is the estimate out after eight applications? | $1.024^8 = 1.2089$ |
| 37 | Estimating a real quantity: the $6ND$ rule, about 6 FLOPs per parameter per token (two forward, four backward). Labelled in the running text as a **standard estimate, not a measurement**. Worked: $6\times7{\times}10^9\times2{\times}10^{12} = 8.4\times10^{22}$. | $6ND$ for $N=7\times10^9$, $D=1\times10^{12}$ | $4.2\times10^{22}$ |
| 38 | FLOPs into time. A device at $4\times10^{14}$ FLOP/s at 40% utilisation gives $1.6\times10^{14}$ effective; $8.4{\times}10^{22}/1.6{\times}10^{14} = 5.25\times10^8$ s. | Convert to days | 6076 days |
| 39 | And into a fleet: 16.6 years on one device, or 203 devices for 30 days. ▸ | How many devices for 10 days? | 608 |
| 40 | **False precision.** The inputs carry one significant figure, so "6076 days" is a lie told in four — quote $6\times10^3$. Ties back to frame 31. | How many s.f. should the answer carry? | One |

### O6 — model memory (41–46)

| # | Teaches | R | A |
|---|---|---|---|
| 41 | Bytes per parameter by format: fp32 4, fp16 and bf16 2, int8 1. Note fp16 and bf16 are the *same width* and differ in how they split it — P1's subject, named here only. | Bytes per parameter in fp16? | 2 |
| 42 | **The payoff, worked in full.** $7\times10^9$ parameters $\times$ 2 bytes $= 1.4\times10^{10}$ bytes $= 14$ GB. **Figure 3** here. | The same model in fp32? | 28 GB |
| 43 | Worked with gaps, a different model. | A 13B model in bf16: bytes and GB? | $2.6\times10^{10}$ bytes; 26 GB |
| 44 | Weights are not the whole bill. Under **stated** assumptions — fp16 weights (2 B), fp16 gradients (2 B), fp32 Adam $m$ and $v$ (4 B each) — training holds 12 bytes per parameter, so 7B needs 84 GB. The assumptions are stated so the number is arithmetic, not folklore. | The same 12 bytes/parameter for 13B? | 156 GB |
| 45 | Inference is a different sum: about 2 FLOPs per parameter per generated token, plus a KV cache that grows with sequence length (named, not costed — P3's job). | Inference FLOPs per token for 7B? | $1.4\times10^{10}$ |
| 46 | ▸ Everything in one. | A 70B model in bf16: bytes, GB, GiB? | $1.4\times10^{11}$ B; 140 GB; 130.4 GiB |

### O7 — gigabytes against gibibytes (47–51)

| # | Teaches | R | A |
|---|---|---|---|
| 47 | Two prefix systems, not one. SI: k $=10^3$, M $=10^6$, G $=10^9$. Binary: Ki $=2^{10}$, Mi $=2^{20}$, Gi $=2^{30}$. Table generated from the computed values, not typed. | How many bytes in a GiB? | $1\,073\,741\,824$ |
| 48 | **The two directions of one gap, which is where people go wrong.** A GiB is 7.4% *more bytes* than a GB; the same byte count *expressed in GiB* is a 6.9% *smaller number*. Both worked on 14 GB $\to$ 13.04 GiB. | Express 14 GB in GiB | 13.04 GiB |
| 49 | So your arithmetic and your tooling are both right (Quiz Q10). `aibox`: which tools report which. | Your sum says 140 GB, a tool reports 130.4 GiB. Which is wrong? | Neither |
| 50 | The gap **widens with the prefix**: 2.4% at Ki, 4.9% at Mi, 7.4% at Gi, 10.0% at Ti. Generated table. **Figure 4** here. | At which prefix does it first exceed 5%? | Gi, at 7.4% |
| 51 | ▸ Reading a real device report. | A device reports 79.15 GiB. How many decimal GB? | 84.99 GB |

### O8 — stating a speed-up (52–55)

| # | Teaches | R | A |
|---|---|---|---|
| 52 ⚠ | **Trap 5, set** (Quiz Q11 routes here). A request took 200 ms and is now "fifty per cent faster". Ask for the new time as a single number. | Commit to a number | Ambiguous — 100 ms **or** 133.3 ms |
| 53 ⚠ | **Trap 5, sprung.** Two defensible readings: half the time (100 ms), or one and a half times the rate ($200/1.5 = 133.3$ ms). They differ by 33.3 ms, a sixth of the original. `trapbox`. | Which reading gives 133.3 ms? | The rate reading |
| 54 | The fix: quote both absolute numbers, or a ratio with its direction and its base. "200 ms → 133 ms" cannot be misread. Speed-up factor against percentage reduction, worked on $200\to100$: 2×, 50%. ▸ | Throughput rises 30 → 45 tokens/s. Speed-up factor, % throughput increase, % latency reduction? | 1.5×; 50%; 33.3% |
| 55 | Close. What the program bought: classify a number, use the index laws, move between roots and fractional indices, work in scientific notation, estimate an order of magnitude, size a model, tell a GB from a GiB, and state a speed-up. Forward pointers: P1 for the bits and machine epsilon, P2 for stability and log-space, P3 for orders of magnitude at scale, F3 for logarithms. *Last frame — no response demanded.* | — | — |

### Scaffolding gradient audit

Every outcome block runs fully-worked → worked-with-gaps → *now one for you* before the
reader is left unaided in the exercises.

| Outcome | Fully worked | With gaps | ▸ *One for you* |
|---|---|---|---|
| O1 (1–7) | 1–5 | — | 6 |
| O2 (8–17) | 8–12 | 13, 16 | 14, 17 |
| O3 (18–24) | 18–21, 24 | 22 | 23 |
| O4 (25–33) | 25, 28, 32 | 26, 29, 33 | 27, 29 |
| O5 (34–40) | 34, 36–38 | — | 39 |
| O6 (41–46) | 41, 42, 44, 45 | 43 | 46 |
| O7 (47–51) | 47–49 | 50 | 51 |
| O8 (52–55) | 52–54 | — | 54 |

O1 and O5 have no gap-fill rung. That is acceptable — O1 is definitional and O5's
estimation frames are each a full worked calculation — but if either block later feels
thin, frame 6 and frame 34 are where a `\dotline` belongs.

---

## 5. The traps

Five, against a required three. Two are written; three are already placed by the Quiz's
`\teachesat{}`. Each follows Stroud's three beats: **elicit a commitment → state flatly
that it is wrong → demonstrate.** Each is closed inside F1.

| # | Frames | The wrong answer elicited | Why it is wrong | Demonstration | State |
|---|---|---|---|---|---|
| 1 | 5 | "$0.1$ is simple — one digit, exact" | True in base ten, false about the machine. In base 2, $\tfrac1{10}$ behaves as $\tfrac13$ does in base 10 | The $\tfrac13$/base-3 parallel set up one frame earlier, so the reader has already accepted the principle before it is turned on them | **written** |
| 2 | 11 | "$2^3\times3^2 = 6^5$ — add the exponents" | Every index law requires a **common base**; there is no rule combining $a^m$ and $b^n$ | $8\times9 = 72$ against $6^5 = 7776$ | **written** |
| 3 | 24 | "$\sqrt{9+16} = \sqrt9+\sqrt{16} = 7$" | Roots and powers distribute over a **product**, never over a **sum** | $\sqrt{25} = 5 \ne 7$. Cashed as L2 against L1: $\lVert(3,4)\rVert_2 = 5$, $\lVert(3,4)\rVert_1 = 7$ | to write |
| 4 | 35–36 | "$2^{80}$ is about $10^{24}$, near enough" | The 2.4% error is applied eight times and **multiplies**, not adds | $1.024^8 = 1.2089$; $2^{80} = 1208925819614629174706176$, 20.89% high. Lands on GB/GiB at 47–50 | to write |
| 5 | 52–53 | "50% faster means 100 ms" (or "133 ms"), stated with confidence | Both readings are defensible; the phrase does not determine which | $200\times0.5 = 100$ ms against $200/1.5 = 133.3$ ms — a 33.3 ms spread | to write |

Trap 1 is placed early, before the reader has any reason to distrust the machine.
Trap 5 is last because it is the one they will use in a stand-up the same week.

---

## 6. Summary

Absent from the draft. Fourteen items, each tagged with its source frame —
`\sumitem{35--36}{...}` — so the Summary doubles as the return index that *Can you?*
points at.

| Item | Frames |
|---|---|
| $\N\subset\Z\subset\Q\subset\R$; subtraction forces $\Z$, division forces $\Q$, $\sqrt2$ forces $\R$. A form is not a set — $\sqrt9\in\N$ | [1–7] |
| A rational's expansion stops or repeats; **that it repeats is a fact about the base**, not the number. $\tfrac13$ is exactly $0.1$ in base 3, and $\tfrac1{10}$ repeats in base 2 | [4–5] |
| $a^ma^n=a^{m+n}$, $a^m/a^n=a^{m-n}$, $(a^m)^n=a^{mn}$ — **all three require a common base** | [8–11] |
| $a^0=1$ and $a^{-n}=1/a^n$, both forced by the quotient law. A negative index is a reciprocal, not a negative number | [12–13] |
| $a^{m/n}=(\sqrt[n]{a})^m$; take the root first and the numbers stay small | [19–21] |
| Roots and powers distribute over a **product**, never a **sum**: $\sqrt{a+b}\ne\sqrt a+\sqrt b$, $(a+b)^2\ne a^2+b^2$ | [24] |
| Normalised form $a\times10^n$ with $1\le|a|<10$; multiply mantissas and add exponents, divide and subtract | [25–29] |
| Compare exponents first; the mantissa says **what**, the exponent says **where** | [30–31] |
| A float is normalised scientific notation in base 2 on a fixed budget, so **relative** precision is constant and **absolute** spacing grows with magnitude | [32–33] |
| $2^{10}=1024$ is 2.4% above $10^3$, and the error **multiplies** when compounded: 20.89% by $2^{80}$ | [35–36] |
| Training FLOPs $\approx 6ND$; do not quote more significant figures than the estimate carries | [37–40] |
| Memory $=$ parameters $\times$ bytes per parameter; training holds roughly 12 bytes per parameter under the stated fp16/Adam assumptions | [41–44] |
| A GiB is 7.4% more bytes than a GB; the same bytes in GiB is a 6.9% smaller number. The gap widens with the prefix | [47–50] |
| Quote a ratio with its direction and its base, or quote both absolute numbers; "fifty per cent faster" names two different times | [52–54] |

---

## 7. "Can you?"

Absent from the draft — `\canyou` must be called. It is **generated** from the stored
`\outcome{}` declarations, so it cannot drift from §3.1; nothing is authored here beyond
placing the macro. It prints the eight outcomes with their frame ranges and a 1–5
self-rating row, under the standing instruction that anything below 4 sends the reader
back to the named frames, followed by the Quiz retake.

| # | On entry this program promised you would be able to | Frames |
|---|---|---|
| 1 | say which set a number belongs to, and why it changes what a program can do with it | 1–7 |
| 2 | use the laws of indices, including zero and negative exponents, without stopping to think | 8–17 |
| 3 | read a fractional index as a root, and move between the forms in either direction | 18–24 |
| 4 | write any quantity in scientific notation, and multiply, divide and compare within it | 25–33 |
| 5 | estimate an order of magnitude, and say how far the estimate can be trusted | 34–40 |
| 6 | compute the memory a model's weights need from parameter count and precision | 41–46 |
| 7 | tell a gigabyte from a gibibyte, and say which one a tool is reporting | 47–51 |
| 8 | state a speed-up unambiguously, and spot the two readings of "fifty per cent faster" | 52–55 |

---

## 8. Test exercises

Absent from the draft. Twelve, in the order the program taught them, no traps, nothing
needing an idea not met. Each takes `\answerto{}`; answers print in Appendix A.

| T | Question | Answer | O |
|---|---|---|---|
| T1 | Classify $\sqrt{25}$, $\tfrac73$, $-11$, $\sqrt3$ by the smallest set containing each | $5\in\N$; $\tfrac73\in\Q$; $-11\in\Z$; $\sqrt3\in\R$ and nothing smaller | O1 |
| T2 | Simplify $(2^6\times2^{-2})/2^3$ | $2^1 = 2$ | O2 |
| T3 | Evaluate $5^0$, $3^{-2}$, $(4^2)^3$ | 1; $\tfrac19$; $4^6 = 4096$ | O2 |
| T4 | Evaluate $64^{1/2}$, $64^{1/3}$, $64^{2/3}$, $64^{-1/2}$ | 8; 4; 16; $\tfrac18$ | O3 |
| T5 | Write $81^{3/4}$ and $32^{-2/5}$ without an index | 27; $\tfrac14$ | O3 |
| T6 | Write $93\,000\,000$ and $0.0000061$ in scientific notation, with their significant figures | $9.3\times10^7$ (2 s.f.); $6.1\times10^{-6}$ (2 s.f.) | O4 |
| T7 | Compute $(2.4\times10^5)(5\times10^{-9})$ and $(9\times10^7)/(3\times10^{-2})$ | $1.2\times10^{-3}$; $3\times10^9$ | O4 |
| T8 | $2^{20}$ is often called "a million". By what percentage does it exceed $10^6$? | $2^{20} = 1\,048\,576$; 4.86% | O5 |
| T9 | Estimate the FLOPs to train a 3B model on 1T tokens at 6 FLOPs per parameter per token, and give the answer to the precision the estimate justifies | $1.8\times10^{22}$; one significant figure | O5 |
| T10 | A 3B model in fp16: bytes, decimal GB, binary GiB | $6\times10^9$ B; 6 GB; 5.59 GiB | O6 |
| T11 | A tool reports 23.28 GiB. How many decimal GB? | 25.0 GB | O7 |
| T12 | A step falls from 250 ms to 200 ms. Give the speed-up factor and the percentage reduction | 1.25×; 20% | O8 |

## 9. Further problems

Absent from the draft. Twenty, for consolidation. Each takes `\answerto{}`.

| P | Question | Answer |
|---|---|---|
| P1 | Classify $-4$, $0$, $\tfrac28$, $\sqrt{49}$, $\sqrt{50}$, $0.333\dots$ by the smallest set containing each | $\Z$; $\N$; $\Q$ $(=\tfrac14)$; $\N$ $(=7)$; $\R$; $\Q$ $(=\tfrac13)$ |
| P2 | $\tfrac17$ repeats with period six in base ten. Give a base in which it terminates, and say why | Base 7 (or any multiple of 7) — the denominator's only prime factor must divide the base |
| P3 | Simplify $(3^5\times3^{-7})/3^{-3}$ | $3^1 = 3$ |
| P4 | Simplify $(x^3y^{-2})^2\times(x^{-1}y^3)$ | $x^5y^{-1} = x^5/y$ |
| P5 | Is $2^4\times4^2$ equal to $8^3$? Show your working | No: $16\times16 = 256$; $8^3 = 512$. Rewrite to a common base — $2^4\times2^4 = 2^8 = 256$ |
| P6 | Evaluate $81^{3/4}$, $125^{-2/3}$, $(16/81)^{1/4}$ | 27; $\tfrac1{25}$; $\tfrac23$ |
| P7 | Give a counterexample to $(a+b)^2 = a^2+b^2$ and state the correct expansion | $a=b=1$: 4 against 2. $(a+b)^2 = a^2+2ab+b^2$ |
| P8 | Compute $\lVert(5,12)\rVert_2$ and $\lVert(5,12)\rVert_1$ | 13; 17 |
| P9 | Write $0.00000000072$, $4\,500\,000$ and $1024$ in normalised scientific notation | $7.2\times10^{-10}$; $4.5\times10^6$; $1.024\times10^3$ |
| P10 | Compute $(6\times10^{-4})^2$ and $\sqrt{9\times10^{-8}}$ | $3.6\times10^{-7}$; $3\times10^{-4}$ |
| P11 | Order these without a calculator: $9.9\times10^{11}$, $1.1\times10^{12}$, $8.5\times10^{11}$ | $8.5{\times}10^{11} < 9.9{\times}10^{11} < 1.1{\times}10^{12}$ |
| P12 | A toy format keeps 4 significant decimal digits. What is the gap between consecutive representable numbers near 1, and near $10^6$? | 0.001; 1000 |
| P13 | $2^{40}$ is often quoted as $10^{12}$. By what percentage is that wrong, and why is it worse than the error at $2^{10}$? | $2^{40} = 1\,099\,511\,627\,776$, 9.95% high; the 2.4% error is applied four times and multiplies |
| P14 | A 405B model in bf16: how many GB, and how many 80 GB devices for the weights alone? | 810 GB; $810/80 = 10.125$, so 11 — and this ignores activations and the KV cache |
| P15 | Training memory for a 13B model on frame 44's 12 bytes-per-parameter assumption | 156 GB |
| P16 | Estimate the FLOPs to train a 405B model on 15T tokens; then the days on 16384 devices at $4\times10^{14}$ FLOP/s and 40% utilisation | $3.645\times10^{25}$ FLOPs; $1.39\times10^7$ s $=$ 160.9 days, which to the precision justified is about 160 days |
| P17 | A device reports 79.15 GiB. Give the figure in decimal GB, and say which number a purchase order would quote | 84.99 GB; the marketing figure is the decimal one |
| P18 | By what percentage does a TiB exceed a TB, and how does that compare with the GiB/GB gap? | 10.0% against 7.4% — the gap widens with every prefix |
| P19 | Throughput rises from 120 to 180 tokens/s. Give the speed-up factor, the percentage increase in throughput, and the percentage reduction in per-token latency | 1.5×; 50%; 33.3% |
| P20 | A colleague reports a change as "30% faster". Write the two sentences that would each make it unambiguous | Either "latency fell from 200 ms to 140 ms" (0.7× the time) or "throughput rose from 100 to 130 req/s" (1.3× the rate) |

---

## 10. Figures

Four. One exists. Sources at `figures/mermaid/{en,pl}/<key>.mmd`, rendered PDFs
gitignored; CI checks that both languages carry the same key set.

**Deliberately excluded**, because §1 assigns them elsewhere: the IEEE-754 bit layout and
the spacing of representable numbers on the real line belong to **P1**; log-sum-exp
belongs to **P2**. Figure 2 below is the F1-legal version of the bit-layout figure — the
*shape* of a number in normalised form, with no bit fields.

### 10.1 `f01-number-sets` — frame 5/6 — **exists**

Nested $\N\subset\Z\subset\Q\subset\R$ with $\pi$ and $\sqrt2$ outside $\Q$, and the
machine's set drawn as a finite subset *inside* $\Q$. Its caption already makes the
claim the frames make in words.

### 10.2 `f01-scientific-anatomy` — frame 32 — **to draw**

**Teaches:** the three parts of a number in normalised form, and that a float is the same
shape in base 2 on a fixed budget. This is the bridge figure to Part II, and the reason
frame 32 can make P1's central claim without a single bit.

A `flowchart` splitting $-1.4\times10^{10}$ into three labelled parts: **sign**;
**mantissa** — "*what* — a fixed count of significant digits, so **relative** precision
is constant"; **exponent** — "*where* — a fixed range, so **reach** is capped". Beneath,
the same three parts again for base 2 with both budgets left as `?`, and a terminal node
reading **"P1 fills in the numbers"**. The unfilled budgets are the point: F1 establishes
the shape, P1 supplies the widths.

### 10.3 `f01-magnitude-ladder` — frame 42 — **to draw**

**Teaches:** the payoff is one chain of multiplications, and every rung is arithmetic the
reader has just done.

A vertical `flowchart TD`, each edge labelled with its operator: parameters
$7\times10^9$ → ($\times$ 2 bytes) → $1.4\times10^{10}$ bytes → ($\div10^9$) → 14 GB,
with a branch → ($\div2^{30}$) → 13.04 GiB styled in the trap colour and carrying the
gap. A second branch from the parameter node → ($\times6D$) → $8.4\times10^{22}$ FLOPs →
($\div$ effective FLOP/s) → $5.25\times10^8$ s → 6076 device-days. One picture holds O6,
O7 and half of O5.

### 10.4 `f01-si-vs-binary` — frame 50 — **to draw**

**Teaches:** the two prefix ladders are not the same ladder, and they diverge — which is
why the confusion gets worse as the numbers get bigger.

Two parallel `flowchart LR` ladders, SI $10^3\to10^6\to10^9\to10^{12}$ above and binary
$2^{10}\to2^{20}\to2^{30}\to2^{40}$ below, with a labelled connector at each rung
carrying the gap: 2.4%, 4.9%, 7.4%, 10.0%. The visual claim is the widening, which no
table makes as immediate.

---

## 11. Numeric claims and the verifying script

House rule: the book contains no digits, only `\val{}` references. Every value is
produced by `code/f01_numbers.py` into `figures/values/f01.tex`; `make verify` fails if
the committed file and the script disagree.

**Every number in this plan has been executed**, including all twelve Test exercises and
all twenty Further problems. The tables in §4, §5, §8 and §9 are script output.

### 11.1 A hazard in the existing values — two numbers for one fact

The script emits **both** of these, and they are reciprocal readings of the same gap:

| Key | Value | Means |
|---|---|---|
| `f01.gib.over.si.pct` | **7.4** | $2^{30}/10^9 - 1$ — a GiB is 7.4% **more bytes** than a GB |
| `f01.gib.gap.pct` | **6.9** | $1 - 10^9/2^{30}$ — the same bytes in GiB is a 6.9% **smaller number** |

Both are correct and they are trivially swappable. The drafted Quiz Q10 uses
`f01.gib.over.si.pct` correctly ("a gibibyte is 7.4% more bytes"); frame 48 needs *both*,
and is the only place that should use them together.

**Recommendation:** rename to make the direction unswappable —
`f01.gib.over.gb.pct` (7.4) and `f01.gb.under.gib.pct` (6.9) — and add an assertion that
the two are not equal, so a future edit cannot silently collapse them into one. This is
exactly the class of error the computed-values machinery exists to prevent, and the
current names do not prevent it.

### 11.2 Values already emitted (reuse unchanged)

`f01.params`, `f01.weights.bytes`, `f01.weights.gb`, `f01.weights.gib`,
`f01.weights.fp32.gb`, `f01.gib.per.gb`, `f01.gib.gap.pct`, `f01.two.ten`,
`f01.two.ten.err.pct`, `f01.two.eighty`, `f01.two.eighty.err.pct`, `f01.tokens`,
`f01.train.flops`, `f01.train.flops.exp`, `f01.device.flops`, `f01.device.util.pct`,
`f01.device.days`, `f01.device.years`, `f01.devices.for.30.days`,
`f01.infer.flops.per.token`, `f01.big.params`, `f01.big.gb`, `f01.big.gib`,
`f01.kib.bytes`, `f01.mib.bytes`, `f01.gib.bytes`, `f01.tib.bytes`,
`f01.{kib,mib,gib,tib}.over.si.pct`, `f01.novel.words`, `f01.novel.tokens`,
`f01.base.ms`, `f01.fifty.pct.less.ms`, `f01.fifty.pct.more.rate.ms`,
`f01.speedup.discrepancy.ms`.

### 11.3 Values the script must gain

| Key | Value | Used at |
|---|---|---|
| `f01.two.ten.err.compounded` | 1.2089 | 36 |
| `f01.flops.1t` | `4.20e22` | 37 |
| `f01.devices.for.10.days` | 608 | 39 |
| `f01.sig3.gap.near1000` / `.near1` | 10 / 0.01 | 32 |
| `f01.sig4.gap.near1` / `.near1e6` | 0.001 / 1000 | P12 |
| `f01.norm2.34` / `f01.norm1.34` | 5 / 7 | 24 |
| `f01.norm2.512` / `f01.norm1.512` | 13 / 17 | P8 |
| `f01.model13.gb` | 26 | 43 |
| `f01.model3.gb` / `.gib` | 6 / 5.59 | T10 |
| `f01.model405.gb` / `.devices80` | 810 / 11 | P14 |
| `f01.train.bytes.per.param` | 12 | 44 |
| `f01.train.mem.gb` / `.13b.gb` | 84 / 156 | 44, P15 |
| `f01.gib7915.gb` | 84.99 | 51, P17 |
| `f01.gib2328.gb` | 25.0 | T11 |
| `f01.two.twenty.err.pct` | 4.86 | T8 |
| `f01.two.forty.err.pct` | 9.95 | P13 |
| `f01.flops.3b.1t` | `1.80e22` | T9 |
| `f01.flops.405b` / `f01.days.16384` | `3.645e25` / 160.9 | P16 |
| `f01.tok.speedup` / `.throughput.pct` / `.latency.red.pct` | 1.5 / 50 / 33.3 | 54 |
| `f01.tok2.speedup` / `.throughput.pct` / `.latency.red.pct` | 1.5 / 50 / 33.3 | P19 |

### 11.4 Script sketch

Extends the existing file; same `emit()` and `VALUES` mechanism, same output path.

```python
import math

# ---- The GiB/GB gap, in both directions, named so they cannot be swapped ---
GIB, GB = 2**30, 10**9
emit("f01.gib.over.gb.pct", (GIB / GB - 1) * 100, 1)   # 7.4 -- a GiB is MORE BYTES
emit("f01.gb.under.gib.pct", (1 - GB / GIB) * 100, 1)  # 6.9 -- the NUMBER is smaller
assert round(GIB / GB - 1, 4) != round(1 - GB / GIB, 4), \
    "the two readings of the GiB gap must stay distinct"

# ---- Compounded approximation error -------------------------------------
emit("f01.two.ten.err.compounded", 1.024**8, 4)        # 1.2089
for k, n in (("twenty", 20), ("forty", 40)):
    emit(f"f01.two.{k}.err.pct", (2**n / 10**(3 * n // 10) - 1) * 100, 2)
assert 2**80 // 10**24 == 1 and round((2**80 / 10**24 - 1) * 100, 2) == 20.89

# ---- Norms: what does not distribute over a sum --------------------------
for a, b in ((3, 4), (5, 12)):
    emit(f"f01.norm2.{a}{b}", math.hypot(a, b), 0)     # 5, 13
    emit(f"f01.norm1.{a}{b}", a + b)                   # 7, 17

# ---- Representable spacing, from significant digits alone ----------------
def gap(sig_digits: int, near: float) -> float:
    """Gap between consecutive numbers held to `sig_digits` decimal digits."""
    return 10 ** (math.floor(math.log10(near)) - (sig_digits - 1))
emit("f01.sig3.gap.near1000", gap(3, 1e3), 0)          # 10
emit("f01.sig3.gap.near1",    gap(3, 1.0), 2)          # 0.01
emit("f01.sig4.gap.near1",    gap(4, 1.0), 3)          # 0.001
emit("f01.sig4.gap.near1e6",  gap(4, 1e6), 0)          # 1000

# ---- Sizing --------------------------------------------------------------
BYTES = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1}
def weight_gb(params, fmt="fp16"): return params * BYTES[fmt] / 1e9
for tag, n in (("3", 3e9), ("13", 13e9), ("405", 405e9)):
    emit(f"f01.model{tag}.gb", weight_gb(n), 0)
emit("f01.model3.gib", 3e9 * 2 / GIB, 2)               # 5.59
emit("f01.model405.devices80", math.ceil(weight_gb(405e9) / 80))   # 11

# Training memory, under ASSUMPTIONS THE FRAME STATES: fp16 weights and
# gradients, fp32 Adam m and v. The frame prints the four terms, not just 12.
TRAIN_BYTES = 2 + 2 + 4 + 4
emit("f01.train.bytes.per.param", TRAIN_BYTES)
emit("f01.train.mem.gb",     7e9 * TRAIN_BYTES / 1e9, 0)   # 84
emit("f01.train.mem.13b.gb", 13e9 * TRAIN_BYTES / 1e9, 0)  # 156

# ---- Cost, to an order of magnitude --------------------------------------
def flops_6nd(n, d): return 6 * n * d
def days(flops, devices, peak=4e14, util=0.4):
    return flops / (devices * peak * util) / 86400
emit("f01.flops.1t",    f"{flops_6nd(7e9, 1e12):.2e}".replace("e+", "e"))
emit("f01.flops.3b.1t", f"{flops_6nd(3e9, 1e12):.2e}".replace("e+", "e"))
emit("f01.devices.for.10.days", f"{days(flops_6nd(7e9, 2e12), 1) / 10:.0f}")
emit("f01.flops.405b",  f"{flops_6nd(405e9, 15e12):.3e}".replace("e+", "e"))
emit("f01.days.16384",  days(flops_6nd(405e9, 15e12), 16384), 1)   # 160.9

# ---- Reading a device report --------------------------------------------
for gib in (79.15, 23.28):
    emit(f"f01.gib{str(gib).replace('.', '')}.gb", gib * GIB / 1e9, 2)

# ---- Ratios --------------------------------------------------------------
def ratio_report(before, after):
    """Throughput before/after -> (speed-up, % rise, % latency reduction)."""
    return after / before, (after / before - 1) * 100, (1 - before / after) * 100
for tag, (b, a) in (("", (30, 45)), ("2", (120, 180))):
    s, up, red = ratio_report(b, a)
    emit(f"f01.tok{tag}.speedup", s, 1)
    emit(f"f01.tok{tag}.throughput.pct", up, 0)
    emit(f"f01.tok{tag}.latency.red.pct", red, 1)
```

### 11.5 Typesetting notes

- **Never hard-code a digit.** $2^{80}$ is 25 digits and belongs in a display via
  `\rawval{f01.two.eighty}`, never inline — it would run into the 17 cm margin.
- **`\rawval`, not `\val`, wherever the digits themselves are the point** and `siunitx`
  grouping would obscure the pattern.
- **The Polish edition needs no separate values.** `\val` applies
  `\mfadecimalmarker`, so `13.04` sets as `13,04` automatically. Values emitted as
  pre-formatted strings bypass that, so keep those free of decimal points.
- **Frames 37, 44 and 45 must carry their assumptions in the running prose**, not a
  footnote. $6ND$ and 12 bytes/parameter are estimates; the house rule is that a claim
  carries a method or an explicit label as judgement. The draft's Quiz Q12 already says
  "given roughly 6 FLOPs per parameter per token", which is the right register.

---

## 12. Build and parity checklist

- 55 `\begin{fr}`; every response-demanding frame followed by `\ans{}` or `\ansblock`
  (`make frames` enforces both, plus the 30–70 band).
- Add `\begin{summarybox}`, `\canyou`, `\begin{testexercises}`,
  `\begin{furtherproblems}` — **all four are currently missing**, and only the last two
  are visible to a ledger (`make answers` compares item and `\answerto` counts per
  environment). A missing Summary and a missing *Can you?* are invisible to every check
  in `check_structure.py`; **consider adding a fifth ledger for the seven skeleton
  sections**, since the format's whole claim rests on them being present.
- Fix `\teachesat{14}` → `\teachesat{11--12}` on Quiz Q3 (§3.3), and prefer
  `\label`/`\ref` over literal frame numbers from here on — `\framelabelfix` exists for
  this and is unused.
- 12 quiz + 12 test + 20 further items, each with exactly one `\answerto{}`.
- Every `\val{}` backed by an emitted value (`make values` catches both directions).
- **Both editions in the same commit.** `programs/pl/F01` is at **0 of 55 frames** while
  `en` is at 15 — `make translate` / `tools/parity.py` compares an ordered structural
  signature and will report the whole program as outstanding.
- Polish conventions: `\dash{}` rather than a typed dash; `\enquote{}` for quotation
  marks; decimal comma free through `\val`.
- Underscores inside `\code{}`/`\api{}`/`\pkg{}` written `\_`. Never add a `listings`
  literate mapping for U+00A0.
- After the pass: `make` (both editions), `make check`, `make debt`, and compare the
  overfull hbox **and vbox** multiset against a reverted build.
