# P07 — *Tensors, shapes and index notation*: the frame-by-frame plan

P07 was added by the August 2026 curriculum review rather than designed, so its
manifest entry is a **contract** and this is the plan the contract did not come
with. `CLAUDE.md` names writing it as a prerequisite for writing the program.

Read this beside `tools/programs.json`'s P7 entry, which is the authority on
scope, and beside the written P06, which is the authority on what the reader
already has.

---

## 1. What the neighbours have already spent

Read out of the written files, not remembered. This is the step that has changed
the shape of five programs running, and it changes this one too.

**P06 §4 is the whole of the rank-2 story and it hands this program four things
by name.** It establishes that a shape is the domain and the codomain written
down, that $(m \times n)(n \times p) \to (m \times p)$, that a shape error is
therefore a *type* error, that a vector is an $n \times 1$ matrix so $Ax$ needs
no second rule, and that a batch of $k$ inputs is $n \times k$ — one column
each — because linearity never had anything to say about the other columns.

Its note then says, in as many words, that **real frameworks stack the batch
along the *first* axis instead**, so a layer computes $XW^{\mathsf T}$ with $X$
of shape $k \times n$, and that P07 is where the axes get named properly, along
with reshape, transpose and the rank-4 arrays two indices cannot describe. Its
closing frame hands over the four-index question by name.

**So P07 opens exactly there.** The convention flip is the first thing a
reader's rank-2 model meets in a real framework, P06 has already flagged it, and
resolving it in frame 1 or 2 buys the rest of the program its motivation.

What the others leave:

- **P04** owns dimension as *the number of independent directions*, which is the
  word this program collides with. P07 must name the collision rather than
  quietly reuse the word.
- **P03** owns the memory bill and the arithmetic intensity, so any claim here
  about what a copy costs points there rather than measuring again.
- **P08** owns rank in the linear-algebra sense. **The word `rank` therefore
  means two different things three programs apart**, and this program is the one
  that has to say so.
- **P32** assembles multi-head attention. Its brief cites P6 for *multi-head as
  a reshape and a block-diagonal map*; the block-diagonal map is P06's, and the
  reshape is this program's, because P06 has two indices and the object has
  four. Say so here so P32 does not have to relitigate it.

**The frame estimate of 55 is a planning figure from before P06 existed**, and
the pattern of the last six programs says the written length will be well under
it. Do not pad to reach it. Thirty-five to forty is the realistic band, and the
band check reads the manifest, so **if the plan lands below 30 the manifest's
`frames` must be lowered first** — that is a curriculum decision made
deliberately, exactly as F13's was, not a waiver.

## 2. The argument, in one sentence

*An operation on arrays is a statement about which axes line up, and index
notation says it exactly where a picture cannot.*

The reason the program exists is the mismatch the review found: **the audience
manipulates rank-4 arrays daily and has only ever been taught rank-2 notation**,
so the mental model in use is a picture, the picture stops at three axes, and
every shape bug lives in the gap.

## 3. The five sections

### §1 An array is a shape and a rule for reading it (frames 1–7)

Opens on P06's unfinished business: the same layer, two conventions, and both
are the same map.

- Frame 1: P06's $n \times k$ batch against a framework's $k \times n$. Elicit:
  which one is the layer? Answer: both, and $XW^{\mathsf T}$ is the transpose of
  $W X$ — one identity, no new mathematics.
- **An axis is a name for a position in the index tuple**, not a direction in
  space. That is the sentence the whole program rests on and it costs one frame.
- **The word collision, and it is three-way.** `ndim` (how many axes),
  `shape[i]` (how long one axis is), and P04's *dimension of a space* (how many
  independent directions). A rank-3 array does not live in three dimensions;
  a batch of 32 sentences of 128 tokens of 768 numbers is rank 3 and its vectors
  live in 768. **Trap frame**, elicited: ask for the dimension of the space the
  embeddings of a `(32, 128, 768)` array live in, and let the reader say three.
- **`rank` means something else in P08**, said once, plainly, with the pointer.
  Two programs apart is close enough to collide and far enough to forget.
- The buffer: an array is a flat run of numbers plus a shape plus a rule for
  turning an index tuple into an offset. The rule earns its place because §5's
  reshape/transpose distinction is unstateable without it.

### §2 Index notation says what a picture cannot (frames 8–14)

- Write P06's product in indices: $C_{ij} = \sum_k A_{ik} B_{kj}$. P06 *derived*
  this as composition; this program *writes* it, which is a different act.
- **The whole rule, in one line: an index that appears twice is summed over and
  an index that appears once survives.** Everything in §3 is this rule with the
  sigma left out.
- Read one back. $\sum_k A_{ik} B_{jk}$ — elicit, and the answer is
  $AB^{\mathsf T}$, which is exactly the framework convention from §1 and closes
  that loop.
- Four axes, on a real object: $S_{bhqk} = \sum_d Q_{bhqd} K_{bhkd}$. Elicit
  which indices survive and which is summed, **before** any of the words
  *attention*, *head* or *einsum* are used. The reader can do it from the rule
  alone, which is the point.
- Note: $b$ and $h$ appear twice and are *not* summed, because they appear on
  the left as well. That is the exception the convention needs and §3's arrow
  makes it explicit rather than conventional.

### §3 `einsum` is that sentence with the sigma left out (frames 15–21)

- `'ik,kj->ij'` **is** $\sum_k A_{ik}B_{kj}$, character for character. The arrow
  names the survivors; anything not on the right is summed.
- Read four strings cold, elicited one at a time: `'ij->ji'`, `'ii->'`,
  `'ij,j->i'`, `'bhqd,bhkd->bhqk'`.
- Write two. Given a sentence, produce the string.
- **The trap, and it is the one people actually get wrong:** a repeated index
  that *also* appears on the right is a **batch** index, not a contraction. Ask
  for `'bij,bjk->bik'` in words and the common wrong answer is *sum over $b$
  too*. Elicit it.
- Transcript: a hand-rolled `einsum` for the two-operand case, twenty lines of
  pure Python, checked against explicit loops. The point is that the string is
  not magic — it is a parser and a nest of loops, and writing the loops is the
  proof.

### §4 Broadcasting is a rule, not a courtesy (frames 22–29) — the headline

- **State the rule exactly**, once, and then never paraphrase it: align the
  shapes from the **right**; a pair of axes is compatible when they are equal or
  one of them is 1; a missing axis counts as 1.
- Why right-aligned rather than left: the last axes are the ones an operation
  usually means, and the leading ones are the ones that get added.
- **THE MEASUREMENT. `(n,)` against `(n,1)` gives `(n,n)`, and the loss it
  produces is wrong by an exactly derivable amount.**

  With predictions $p$ of shape `(n,)` and targets $t$ of shape `(n,1)`, the
  difference broadcasts to every *pair*, and

  \[ \operatorname{mean}_{i,j}(p_i - t_j)^2
     \;=\; \operatorname{mean}_i (p_i - t_i)^2 \;+\; 2\operatorname{Cov}(p, t). \]

  Verified numerically to the digit before this plan was written; the script
  must assert the identity rather than the two numbers.

  Two consequences, and they are why this is the headline rather than a warning
  box:

  1. **The error grows as the model improves**, because $\operatorname{Cov}(p,t)$
     is precisely the thing training increases.
  2. **At a perfect fit the reported loss is $2\operatorname{Var}(t)$ and cannot
     go below it.** The true loss is zero. What the engineer sees is a loss that
     falls, plateaus at a number nobody can explain, and stays there — which is
     read as the model having stopped learning, and is in fact a missing
     `keepdims`.

  Measured on one run at four noise levels the true loss goes
  $4.25 \to 0.29 \to 0.012 \to 0$ while the reported one goes
  $5.26 \to 1.87 \to 1.44 \to 1.44$ and sticks. **No error, no warning, and the
  training loop is fine.**
- `keepdims` stated as what it is: it keeps the axis, so the alignment is
  unambiguous rather than guessed. Not a formatting flag.
- A second, cheaper trap worth one frame: a `(3,)` bias added to a `(3, 3)`
  matrix adds it **per row**, and adding it per column needs `(3, 1)`. Both are
  legal, both run, and only one is what was meant.

### §5 reshape, transpose, permute: which of them moves data (frames 30–37)

- Elicit first: which of the three moves numbers in memory? The common answer is
  *transpose does and reshape does not*. **Both are usually wrong**: reshape
  reinterprets the buffer and transpose changes the *strides*, so neither moves
  anything. What moves data is asking for the result contiguous, which is a
  third thing with its own name.
- **The trap, at the exact line where it costs people days.** Splitting heads:
  `x.reshape(b, s, h, d).transpose(1, 2)` against
  `x.reshape(b, h, s, d)`. Both give a rank-4 array of the right shape and
  **they are different arrays**. Show both, elicited, with the numbers.
- The rule that makes it decidable rather than remembered: **reshape is safe
  exactly where the axes being split or merged are adjacent and already in the
  order the buffer has them.** Everything else needs a permute first.
- Payoff frame: multi-head attention with all four axes named — batch, head,
  query, key — and what the product actually contracts, which is the last axis
  and only the last axis. Then hand P32 the assembly by name.

## 4. Diagrams (three, ASCII source, both editions)

Keep to the width budget recorded in `CLAUDE.md`: three ranks, 650–660 pt wide,
which sets node text at 6.71 pt in the trade format and 7.62 pt on A4.

1. `p07-axes-not-directions` — an index tuple against a direction in space; the
   three-way word collision. Must **not** contain the answer to §1's elicited
   dimension question, so it goes *after* that answer.
2. `p07-broadcast-alignment` — shapes aligned from the right, one compatible
   pair and one that is not. Goes after §4's rule is stated, never before the
   `(n,)`/`(n,1)` elicitation.
3. `p07-reshape-or-permute` — the same buffer read two ways. Goes below §5's
   answer, because it *is* §5's answer.

## 5. The script, `code/p07_tensors_shapes.py`

Pure Python, no dependencies; numpy only as a cross-check that announces itself
when it is absent, on the F03 precedent. Assertions written **at** each
computation, before the prose they support.

1. A two-operand `einsum` written from the rule, checked against explicit loops
   on `'ik,kj->ij'`, `'ij,j->i'`, `'ij->ji'` and `'bhqd,bhkd->bhqk'`.
2. The broadcasting identity above, asserted as the **identity** and not as the
   four numbers, plus the perfect-fit floor asserted equal to $2\operatorname{Var}(t)$.
3. The two head-splitting orders, asserted **different** — and asserted equal
   once the permute is put back, which is the half that makes it a rule rather
   than a warning.
4. A cross-programme drift gate on P06's collapse or shape numbers **only if the
   two programs genuinely quote one computation**. P04's pass established that a
   gate wired to a coincidence is worse than no gate; do not invent one.

Transcript: one, generated, committed, importing whatever it calls, and
extracted from the finished PDF and run before the frame around it is written.

## 6. Traps this program owes `notes/02`

None of these is in the catalogue yet, which is itself worth noting for a
program the review called the largest gap in the field.

- an array's rank read as the dimension of a space
- `rank` in P07's sense against `rank` in P08's
- `(n,) + (n,1)` — the loss that plateaus at $2\operatorname{Var}(t)$
- a bias added per row where per column was meant
- a repeated `einsum` index that is a batch axis, read as a contraction
- reshape and transpose treated as interchangeable when splitting heads
- "reshape copies, transpose does not" — both halves wrong

## 7. What this program does not do

- **Rank, the four subspaces, least squares, LoRA** — P08.
- **The determinant, the inverse, change of basis** — P09.
- **The transformer assembled** — P32. This program names the axes and stops.
- **What a copy costs in bytes or in time** — P03 owns the memory bill and the
  arithmetic intensity; quote it, do not re-measure it.
- **Autodiff through a reshape** — P16/P18.
