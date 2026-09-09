# Issue #118 — the Mermaid figures. Hand-off.

Filed once for the whole book rather than per program, so this is a figure
pass rather than a unit review. `CLAUDE.md` has been recording one under
*recorded rather than taken* since the F01--F06 batch; this is it.

**The pass wrote an instrument, `tools/checkfigures.py`, and the instrument is
the largest thing in the diff.** Until now the only evidence anybody had about
diagram type size was a handful of hand measurements in this file's own pass
notes, taken with `pdfinfo` on whichever files somebody happened to open.

---

## The mechanism, measured, because it settles four of the five findings

Mermaid lays every flowchart node label out in a `foreignObject` styled
`max-width: 200px; width: 200px; white-space: break-spaces`. **Every node
label in this book is hard-capped at 200 px and the browser wraps inside that
cap.** Read out of the rendered SVG, not reasoned about.

Three things follow, and each of them retires or redirects a finding:

- **The uniform `657.12` pt in this file's own figure tables is the cap**, not
  a coincidence: three ranks at 200 px plus padding and arrows. A third of the
  book's figures sit exactly there.
- **`<br/>` cannot fix a wrap.** The browser wraps at the cap first and a
  source `<br/>` only adds breaks inside it. Measured per node — a label whose
  source asks for 2 lines renders as 3, 4 or 5:

  | figure | node box | source lines | rendered |
  |---|---|---|---|
  | `f08-unit-circle` | 200 px | 2 | 3, 4 |
  | `f10-set-and-mask` | 200 px | 2 | 3, 4 |
  | `p12-pairs-not-items` | 200 px | 2 | 4, 4, 5 |

- **This file's recorded rule is right and now has its mechanism.** "Wordier
  nodes widen a chain; only more ranks widen a graph that is already wrapping"
  — *already wrapping* means *at the 200 px cap*, and that is measurable.

### The issue's two suggested levers, both put to the renderer

| lever | `f08-unit-circle` W x H | trade | a4 |
|---|---|---|---|
| as shipped | 630.00 x 109.92 | 7.00 pt | 7.95 pt |
| `themeVariables.fontSize` 15px -> 24px | 657.12 x 204.00 | **6.71 pt** | **7.62 pt** |
| `flowchart.wrappingWidth` 200 -> 120 | 476.88 x 144.00 | 9.25 pt | 10.50 pt |
| `flowchart.wrappingWidth` 200 -> 90 | 409.92 x 144.00 | 10.76 pt | 12.22 pt |

**The issue's own suggestion — a font size in `figures/mermaid/config.json` —
makes the defect worse**, because `\mermaidfig` scales the graph to the
measure and the graph grows faster than the text does. `wrappingWidth` is the
lever, and it is settable per diagram with a `%%{init}%%` directive rather
than globally. Not taken: see *Recorded* below.

---

## The instrument

`tools/checkfigures.py`, wired into `make check` (hard) and `make debt`
(ledger), and `make figuresize` on its own. It reads `figures/diagrams/`,
which `make diagrams` writes, and is quiet and green on a checkout where they
have not been rendered.

It carries a `pdfinfo` stand-in, because **pdfinfo is installed on neither of
this project's two machines** — the page size comes out of the first MediaBox,
which is the graph itself because mermaid writes with `--pdfFit`.

**Watched producing a known answer before it was believed**: it reports
`f01-magnitudes` at 210.00 x 666.96 and 4.32 pt, against the `210 x 667` and
`4.32` this file's F02 review pass recorded by hand months ago.

**Proved by mutation, three ways**: it fails (exit 1) on the pre-fix
`f01-magnitudes` and names it, passes a known-good figure sitting beside it in
the same directory, and exits 0 with a plain message on a tree with no
rendered diagrams.

**What it gates and what it only reports.** The type size is a ratio with no
defensible floor, so it is a **ledger** — printed in full, never fatal, on the
orphan tail's reasoning; a threshold picked so today's book passes is not an
assertion, and this repository has paid for that five times. What is a **hard
gate** is a predicate: a figure below the aspect-ratio crossover is set to its
full allowed *height* whatever its width, so it cannot share a page with the
frames it belongs to. Both formats' crossovers are computed rather than
quoted.

### The corpus, which is the deliverable

All 300 diagrams, where the evidence was previously six.

|  | before | after |
|---|---|---|
| trade, node text | 4.21 to 9.32 pt, median 6.71 | 4.64 to 9.32 pt, median 6.71 |
| a4, node text | 5.08 to 10.59 pt, median 7.62 | 5.27 to 10.59 pt, median 7.62 |
| below the crossover | **4** | **0** |

**The reviewer's headline is confirmed and is worse than a handful of
figures**: the median diagram sets its node text at about 61 per cent of body
size in the trade format and 64 per cent on A4. The four hard failures were
F1.1 and F1.2 in both editions — two of the figures the issue names.

---

## Fixed

### 1. The four figures below the aspect-ratio crossover, and the book's smallest

Redrawn in both editions. The remedies are this file's own recorded ones: add
a rank, and shorten the node text so the graph comes off the cap.

| figure | before | after | ratio |
|---|---|---|---|
| `en/f01-magnitudes` | 4.32 / 5.37 pt | **7.03 / 7.99** | 0.31 -> 2.06 |
| `pl/f01-magnitudes` | 4.21 / 5.24 pt | **6.87 / 7.80** | 0.31 -> 2.10 |
| `en/f01-number-sets` | 4.29 / 5.33 pt | **6.77 / 7.69** | 0.98 -> 3.00 |
| `pl/f01-number-sets` | 4.29 / 5.33 pt | **6.45 / 7.32** | 0.98 -> 3.15 |
| `en/f01-prefixes` | 4.48 / 5.08 pt | **8.79 / 9.97** | 5.50 -> 4.57 |
| `pl/f01-prefixes` | 4.48 / 5.08 pt | **8.82 / 10.02** | 5.50 -> 4.55 |

`f01-magnitudes` was a seven-rung vertical ladder; it is three short columns
grouped *text / a model / the bill*, which is narrower and says something the
single chain did not. `f01-number-sets` was stacking because **a subgraph
whose members have no edges between them lays them out in a column whatever
`direction` says** — measured; the fix folds one example into each set's own
label instead of hanging it below as a leaf node.

`f01-prefixes` is the reviewer's second claim about it and it holds: the
figure carried the same four prefix rows, at 4.48 pt, that the `tabularx` on
the very next page carries at body size with an extra column. It now shows the
two ends of both ladders and the compounding — **which is the one thing the
table cannot say** — and it hard-codes no percentage, because the caption
already prints both through `\val{}` and a number written twice is a number
only one of which will ever be corrected.

### 2. F1.2 answered the frame above it differently — finding 5

The frame computes a training run at `\num{2e8}` seconds, "about six or seven
years"; the figure's note node said **"10^7 seconds, about a few months"**.
Both arithmetics are right and they are the same question with both operands
rounded to powers of ten, which moves the answer by a factor of 20.

The node now reports the subtraction and stops, and the caption says in both
editions that the ladder rounds, so its `$10^{7}$` and the section's
`$\num{2e8}$` are one question at two precisions. The factor of 20 reproduces
exactly from the two numbers as the page prints them.

### 3. P12.2's last node reached six frames past its own section — finding 4

Node C said "…is why the safe size goes with a square root", which is
§P12.4's conclusion. **The reviewer's justification does not hold** — they say
"frame 35 elicits" it, and frame 35 *states* it while frame 34 derives it, so
nothing is elicited and this is not a rule-2 violation. It is the
last-node-of-a-three-rank-chain class this file records five times over, and
P22's rule settles it: write a figure against the frames above it, never
against the section it sits in. Node C now ends on the pairs growing with the
square, which frames 27--28 deliver in full.

**And the caption said it too** — "what that does to the size of hash you
need". That is P11's *read the caption as a node*, and the P33 pass met the
same shape: node fixed, caption left saying it. Both editions.

### 4. Every caret in the book is now a real superscript — finding 3

24 occurrences across 7 figures per edition, swept as a class rather than the
two the issue names. `10<sup>22</sup>` is pure ASCII, so the `listings`
fallback and parity's C13 are both untouched, and it was **put to the renderer
before it was believed**: `<sup>` survives mermaid's default `securityLevel`
into the painted SVG.

**The assertion in the sweep fired and stopped a half-done job**: my own
lookahead excluded `2^7<br/>`, so four files would have shipped with a caret
each. Worth keeping — the sweep asserted "no caret left in this file" rather
than trusting the regex.

`f02-equation-to-code` is the one deliberate judgement: its `PRINTED` node is
an ASCII-art transcription of a typeset formula and its sibling nodes use
`sigma2` because they are what you *type*. Converting only the printed one
sharpens the contrast the figure is built on.

---

## Retired — verified against current source, no longer reproduces

- **Finding 4, F1.1 printing 7, −17 and √2** into the sets facing the frame
  that asks the reader to classify exactly those. Already fixed by the
  F01--F06 review batch; the figure now carries 4, −3, 1/3, 0.1, e and pi, and
  frame 6 asks for 7, −17, 22/7, √2 and √9. No overlap.
- **Finding 5, F1.1's caption/edge label** calling the machine's set "not
  nested" with Q. Fixed in the same batch; it reads "holds F, but F holds no N
  or Z".
- **Finding 5, Figure 14.3's caption saying "three questions"** where the
  frame counts five. Removed in `eebd6f4`, the Part IV review. The caption
  says "What an existence theorem promises, and what it is silent about" and
  states no number.
- **Finding 3, P13.1's literal `--` for a dash and P13.2's "Program P06"**.
  Both already fixed; P13.2 says "Program 6". Only 3 of 150 EN figures still
  used ` -- ` inside a label, and all three are the `set -- description`
  convention rather than a dash.
- **Finding 3, P30.1's "p_i times l_i"**. `p30-two-pieces` says "each codeword
  length, weighted by how often its symbol turns up".
- **Finding 3's remedy** — "explicit `<br/>` at phrase boundaries in the
  `.mmd` files fixes the wraps". Already shipped in every file named, and
  measured above not to work. This is the second batch running where a
  reviewer specified a remedy that is already in the tree.
- **Finding 1's remedy** — a font size in `config.json`. Measured to make the
  defect worse.

---

## Recorded rather than taken, with the mechanism

- **Finding 2 — figures that restate the paragraph beside them, and the
  drawings the geometric programs want** (F8, F9, P4, P5, P15, P17, P20, P22).
  Confirmed and not fixable inside the pipeline. **The obstacle is convention
  rather than capability**: TikZ is already loaded, so a projection triangle
  or a unit circle is ten lines — but every figure in this book is a committed
  Mermaid source rendered per language, gitignored as build output, and
  counted in Appendix F's manifest through `\mermaidfig`. A drawn figure is a
  **second asset pipeline** outside all of that, and it needs a decision about
  per-language rendering, the manifest, and the unrendered fallback before a
  single figure is drawn. Named in the P05 review pass; unchanged.

- **The wraps themselves.** The mechanism is the 200 px cap and the fix is
  shorter node text across roughly 300 files, or a per-diagram
  `wrappingWidth`. Both change every figure's height, so both re-roll
  pagination across the whole book. A sweep against all four builds, on the
  `\begin{fr}` reservation's precedent — a pass of its own.

- **A figure declared mid-frame, before the frame's own closing question.**
  The issue names P29's (`p29-code-budget`, which pushes the frame's one-line
  question onto the next page alone). **Measured: there are nine, across seven
  programs** — P20, P21, P25, P27, P28 (twice), P29 (twice), P30. Moving one
  is fixing the instance rather than the class, which is P28's finding. Note
  that the content is *not* a rule-2 defect in P29's case: the figure carries
  the budget rule the frame has just delivered and the question asks the
  reader to *apply* it, which is the P04/P07 case this file records fifteen
  times as sound.

- **Finding 4, F1.2 floating between a question and its answer.** A page-level
  claim, and this pass is under instruction not to walk pagination. The
  figure's declaration point is unchanged; its height is not (below).

---

## FOR THE SYNC SESSION — this pass moves pagination

No frame's prose length changed except two captions. **But six figures changed
height, three of them by a lot**, and a figure's height moves page breaks
exactly as a frame's does:

| figure | trade, on the page | a4, on the page |
|---|---|---|
| `en/f01-magnitudes` | 229.2 -> 170.7 pt (−58.5) | 284.9 -> 193.8 (−91.1) |
| `pl/f01-magnitudes` | 229.2 -> 166.7 pt (−62.5) | 284.9 -> 189.3 (−95.6) |
| `en/f01-number-sets` | 229.2 -> 116.9 pt (−112.3) | 284.9 -> 132.8 (−152.1) |
| `pl/f01-number-sets` | 229.2 -> 111.3 pt (−117.9) | 284.9 -> 126.4 (−158.5) |
| `en/f01-prefixes` | 63.8 -> 76.8 pt (+13.0) | 72.4 -> 87.2 (+14.8) |
| `pl/f01-prefixes` | 63.8 -> 77.2 pt (+13.4) | 72.4 -> 87.6 (+15.2) |
| `en/p12-pairs-not-items` | 67.8 -> 76.9 pt (+9.1) | 77.0 -> 87.3 (+10.3) |
| `pl/p12-pairs-not-items` | 58.7 -> 67.8 pt (+9.1) | 66.6 -> 77.0 (+10.3) |

**Net, F01 loses about 158 pt of figure in the trade format and 229 pt on A4,
in each edition** — the two big ones were pinned at exactly `0.42\textheight`
and are not any more. Expect F01's pagination to move and every cue downstream
of it to be re-rolled. **Walk the cues.**

The two captions lengthened (F1.2 by four lines, F1.3 by one) and P12.2's
caption is level.

## Values

None emitted, none retired. `make verify` reports all computed output current,
and `figures/values/appf.tex` is untouched.

## Found in a neighbouring program and not fixed

- `figures/mermaid/{en,pl}/f02-rearrange-moves.mmd` is the book's widest
  figure after this pass at 939--951 pt, setting **4.64--4.70 pt** trade and
  5.27--5.33 on A4 — now the smallest type in the book, and not named in the
  issue. It is above the crossover, so it is a ledger entry rather than a gate
  failure. `make figuresize` prints it first.
- `programs/en/P29-entropy.tex:337` and the eight other mid-frame figure
  declarations listed above.
