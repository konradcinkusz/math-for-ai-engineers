# CLAUDE.md — working on this book

Context for continuing *Matematyka od zera dla inżyniera AI* /
*Mathematics from Zero for the AI Engineer*.
Read this before touching a program.

---

## Status

| | Done | Remaining |
|---|---|---|
| Structure | Four mains over one `body.tex`, shared preamble, `structure.tex`, Makefile, CI, parity tooling, Mermaid pipeline | — |
| Front matter | Title page, *How to use this book*, Introduction — **both editions** | — |
| Programs | **F1–F5 written, both editions.** F6–F13 and P1–P34 are stubs carrying their briefs | 42 of 47 |
| Appendices | A (answers, generated) and B (notation) drafted; C–F are stubs | C, D, E, F |

**Two languages times two paper formats, four PDFs, all clean.** A4 at 12pt is
the format the book is read in; 17 x 24 cm is the trade format shared with the
companion volumes.

| | Pages | Errors | Unresolved | Overfull hbox | Overfull vbox |
|---|---|---|---|---|---|
| `main-en` (17x24) | 318 | 0 | 0 | 4, worst 4.1 pt | 0 |
| `main-pl` (17x24) | 326 | 0 | 0 | 4, worst 4.1 pt | 0 |
| `main-en-a4` | 292 | 0 | 0 | 5, worst 6.3 pt | 0 |
| `main-pl-a4` | 294 | 0 | 0 | 4, worst 4.4 pt | 0 |

The 6.3 pt box is `$7\,000\,000\,000$` in F1, which cannot break; it exists in
one format and one language because that is where the line falls. Well under
the 15 pt budget. **F2 added no overfull box to any of the four formats** —
the multiset came back identical to the pre-F2 baseline, which took two fixes
recorded under *Program F2 pass* below, and **the F2 review pass did not move it
either**, in any of the four. **F3, and both of its review passes, did not move
it either**: the four multisets above are element-for-element what the pre-F3
table recorded, which is now three programs and 33 to 39 pages of new material
without a new overfull box — and the second F3 review pass moved a figure, cut
lines out of three frames in both editions and loaded a new package without
changing one of the twenty numbers. **F4 did not move it either, but not for
free**: its first build added an 11.2 pt box to `main-en-a4` alone, from a
32-character `\code{}` in a test exercise, and the fix was to set the loop as a
displayed three-line block instead of running it into the sentence. Parity
reports **0 failures and 0 warnings** across 56 file pairs; `reflist.py`
confirms 97 labels resolve to the same numbers in both editions.

**The only page count that moved in the second F3 review pass was `main-pl-a4`,
231 to 229**, and both of those pages were defects rather than content: a page
carrying a running head, two italic words and nothing else. See *the orphaned
cue* below.

**All four counts moved again in the F4 review pass**, from 286/294/262/262:
the editorial cuts account for most of it and the new section room test for
the rest. Measured separately, the section guard alone took `main-pl` and
`main-en-a4` down two and put two back on `main-pl-a4` — which is what a guard
that turns pages does, and why its constant was swept rather than chosen.

`main-pl` is six pages longer than `main-en` in the trade format, down from
eight, and four pages longer on A4, where the two editions were briefly level
at 262. That levelness was coincidence and not convergence: A4 spends the extra
width on margin, so the same text sets in fewer, longer-lived lines and the two
editions' page counts drift independently of the trade format's. The editions
have never been required to paginate alike — nothing that matters navigates by
page — but the gap is written down rather than left to look like a defect.

**Four pages per format came from the Stroud layout pass**, from two causes.
Two are the next-frame cue: 33 cues in a 45-frame program, measured with and
without them. Two are the page-turn guards that stop a frame opener or the Quiz
heading being stranded at the foot of a page. The frame
badge, the outcomes checkboxes, the quiz route boxes, the named end-of-program
frames and the opener's frame range together cost **zero** — the overfull-hbox
multiset came back byte-identical to the pre-pass baseline in all four formats.
At F01's 73% cue rate the cost over 2,415 planned frames is of the order of a
hundred pages, which belongs in the one-volume/two-volume question in
`notes/01-curriculum.md` §20.

**Compare the hbox multiset only against a baseline built on the same
machine.** CI has newtx and inconsolata; a bare container has neither, and the
two measure different line widths. The numbers above are from a container
build that reproduced the pre-pass table exactly, so they are comparable to
what was there before.

**Debt ledgers, reported by CI on every build** (`make debt`):

- **42 of 47 programs are stubs**, in each language. This is the whole of the
  remaining work and it dwarfs everything else.
- 0 exercises without an answer · 0 programs outside the 30–70 frame band ·
  0 programs without declared learning outcomes
- 168 computed values, all referenced, all present, plus the committed console
  transcripts, which are inside the same drift gate as of the F3 pass
- 0 `verifybox` blocks · 30 Mermaid sources, all rendering
- **0 stranded frame openers and 0 stranded section headings**, in all four
  builds. Both are structural and both are hard gates in `tools/checkpdf.py`.
- **26 orphan-tail pages: 3 · 9 · 7 · 7** across `main-en`, `main-pl`,
  `main-en-a4`, `main-pl-a4`, up from 15 before F5 and the largest single jump
  the ledger has taken. Eleven of the eleven added are F5's, which is what 47
  frames of new material costs at this cue rate; the count is the signal and
  it is going the wrong way. `checkpdf.py` prints every one of them on
  every run and **does not fail the build for them**; the reasoning is in the
  note above its `main()` and is summarised under *Program F4 review pass*.
  This is the second ledger that is reported rather than gated, and like the
  first it must not quietly go away. **When the count goes up, that is the
  signal.**
- **80/80 validation: NOT ESTABLISHED**, and printed as outstanding on every
  build. See *The evidence, honestly* below — this is the one ledger that is a
  claim rather than a count, and it must not quietly go away.

---

## Non-negotiable conventions

**Every number is computed, not remembered.** A numeric value goes in a script
under `code/`, is written to `figures/values/<program>.tex` as
`\mfaval{key}{value}`, and reaches the page as `\val{key}`. The book contains
references, not digits. `figures/values/` is **committed** so a changed number
shows up in review as a diff, and CI fails the build when a script no longer
produces what the book prints.

**And a console transcript is a computed number that happens to be verbatim.**
`figures/transcripts/` is written by the same scripts, pulled in with
`\transcript{}`, committed for the same reason — and for its first program it
sat outside every drift gate in the repository, because the Makefile target,
all three workflows and the values artefact were scoped to `figures/values`
alone. Both directories are now in `$(COMPUTED)` and in all three workflows.
Anything a script under `code/` emits belongs in that variable: the promise is
exactly as wide as the gate, and no wider.

The one exception, and it is a real one: **arithmetic the program is teaching is
written inline.** `2^5 = 32` is the thing the reader is meant to do; putting it
behind `\val{}` would be theatre. The rule is *anything the reader cannot do in
their head is computed*.

**Prefer measurements to assertions**, as in both companion volumes, with the
interpretation a mathematics book needs: a theorem is proved or attributed, not
measured; the measurements are for the claims that sit *between* the mathematics
and the practice, which is exactly where folklore lives. Ten experiments are
specified in `notes/01-curriculum.md`; **none has been run**, and until one is,
the claim it would support is labelled as judgement and its table stays empty.
Nine of the ten are free and finish on a laptop in under a minute.

**A gate on PAGINATION cannot be hard on two machines that paginate
differently.** This repository builds on two TeX installations: the container
that writes the published PDF has neither newtx nor inconsolata, CI has both,
and the same source gives an overfull multiset of `[4.1 x 4]` here against
`[1.2 x 4]` there. Every line breaks somewhere else.

`checkpdf.py`'s four checks do not survive that equally. The **stranded frame
opener** and the **stranded section heading** do, because the reservations
behind them are measured in `\baselineskip` and hold under either metric: each
is a statement about a frame or a heading and the room in front of it, not
about where a particular line falls. Both stay hard gates everywhere. The
**orphaned cue** and the **orphan tail** do not: each is one frame's tail
landing a line past a page boundary, so its location is a property of the
installation. Trimming the line CI names fixes CI and moves the defect here;
trimming the line this container names does the reverse. That is an unwinnable
loop, and it was entered once before it was recognised.

So the cue check is **hard where a person can act on it** (`make check`, on the
author's own build) and **reported, not fatal, in CI** (`--cues=warn`), and the
orphan tail is **reported and never fatal** while its pre-existing ledger
stands. The count is printed either way and neither defect is dismissed. The
real fix for both is structural — the tail of a frame should be incapable of
standing alone — and it is open; three attempts are recorded in `preamble.tex`
with their measurements, and a fourth, `\widowpenalty` and `\clubpenalty` at
10000, was measured in the F4 review pass: **30 orphan tails against 26 and six
pages added**, and it was reverted.

**And a claim about a LIBRARY can be true here and false on the build server.**
F03's note box said `np.logspace(-5, -2, 4)[0]` is one unit in the last place
below `1e-5`, and `code/f03_logarithms.py` asserted it. Both were right on this
container and **CI failed on the assertion**, because there the first element is
exactly `1e-5`. Same numpy version string; different answer.

That is the same defect as a claim nobody ran, wearing a disguise: it *was*
run, on one machine, and one machine is not the population. The fix is not to
pick the other value — it is to notice that the printed form is `1.e-05` either
way, so **the repr is the thing that cannot be trusted**, and to say that
instead. The script now asserts only what is universal (the value lies within
one ulp of `1e-5`) and *reports* which it got, with its `.hex()`.

Two rules fall out of it. Assert the invariant, never the observation. And when
a build-dependent fact is interesting, make the dependence the teaching point
rather than picking a branch — the reader who checks on their machine is the
reader the book is for, and they must not find it wrong.

**A claim the book makes about the book is still a claim, and it is the one
class nothing can check.** There is no external source to check it against, and
it is the easiest thing in the repository to open and confirm — which is
exactly why it does not get opened. F03 asserted that a bare logarithm produces
no PDF (it does; `nonstopmode` writes one over the error, as this file's own
*Build traps* section says), that its one bare logarithm was the only one in
the book (there were five in that file), and that F1's ladder of magnitudes
climbs a decade per rung (it climbs 3, 2, 4, 3 and 10). **Never state a count of
occurrences**: name the rule and the places it is lifted, because a tally
decays silently and no lint can see it. And before writing a sentence about
another program, open that program.

**A bare `\log` is a build error.** In Polish textbooks it means base ten; in
machine-learning writing it means base *e*. The same three characters carry
opposite meanings to the two readerships this book serves, and they collide
hardest where it matters most — entropy in bits and cross-entropy in nats are
two programs apart. Write `\ln` or `\logb{2}`. The preamble redefines `\log` to
raise an error, and `tools/parity.py` C10 catches it before the build does.

**ASCII inside listings, and inside `.mmd` files.** `listings` cannot handle a
multi-byte character it has no `literate` mapping for, and the unrendered-diagram
fallback typesets Mermaid source through `listings`. The preamble maps the
Polish diacritics and the common dashes; nothing else is safe.

**Underscores** inside `\code{}`, `\api{}` and `\pkg{}` must be written `\_`.

**Voice.** British English and idiomatic Polish, second person, senior audience.
The book is allowed to say a technique is folklore, that a popular claim is a
ratio quoted without its two quantities, and that the author has not verified
something. No marketing register. No *simply*, no *just*, no *powerful*.

**Two to four figures per program**, each teaching something. Mermaid, ASCII
source, per language, committed; rendered PDFs are build output.

**A figure must not answer the frame that follows it.** The rule recorded after
the F2 pass — *a figure sits only where the next frame does not open with an
answer* — is about the answer box, and it is too narrow. F2's expansion grid
obeyed it and still printed `(a + b)^2 = a^2 + 2ab + b^2`, in a node and again
in its caption, on the same page as and four inches above the frame that says
*cover the rest of the page and write down the expansion of (a+b)^2 as fast as
you can*. The elicitation the whole program was built around was inert, because
the spoiler was above the covering hand. So the rule is the wider one: **a
figure may not contain the answer to any question put to the reader in the
frames on either side of it, whether or not those frames open with `\ans`.** A
figure that teaches a correction goes *after* the correction, where it explains,
and a figure that would preview a trap does not go in at all. Read the figure
and the two frames around it as a page, not as a source file.

**And read the figure's content first, because position does not settle it.**
Two verifiers disagreed over F03 on exactly this and both were describing
something real: two of its three figures do sit above the elicitation that
follows them, in all four builds, and neither contains an answer to it, so
neither is a defect. The one figure that does carry an answer, F3.3, is below that
answer's frame in all four builds. So the test is *does this figure say the
thing the reader is about to be asked for* — and only then *where did it land,
in all four builds*. The measured pages for F03 are under *Program F3, second
review pass*.

**No instruction may depend on where the page happens to break.** *Before you
turn over* was false in F2 in three places, and differently false in each
edition, because the four PDFs paginate differently by construction — the same
sentence was true in English and false in Polish. Nothing can gate it: C4, C8,
C12 and C14 all read the source, where pagination does not exist. The answer box
is a thing you put your hand over (`notes/07-stroud-original-layout.md` §3), so
write *before you read on* / *zanim pójdziesz dalej*, which is true under every
pagination. *Cover the rest of the page* is fine; it names the hand, not the
leaf.

**No inline `\dfrac`, and watch the leading as well as the margin.** `\dfrac`
in running prose sets a display-size fraction inside a text line, and the line's
box then exceeds the leading: the denominator prints into the line beneath.
TeX never says so, because the box is too **tall** and TeX only reports boxes
that are too **wide**. F2 shipped a draft with 78 inline `\dfrac` against F1's
17. Write `\frac` inline — in inline maths it is textstyle already — or move
the fraction into a display. `\dfrac` is right inside `\ans`, which is a
centred box with no line under it.

**The overlap counts once recorded here did not survive re-measurement, and
they are gone.** An independent pass with three instruments — `pdftotext
-bbox` boxes, PyMuPDF word boxes and PyMuPDF per-character boxes — put F1 at
**0** overlapping pairs in every build, not 8–12, and could not find any
tolerance that reproduces the original figure. What it did confirm is the
direction: the F2 draft had a handful of real overlaps, the worst 6.1–7.3 pt,
and converting the fractions took them to zero. So the rule stands and the
numbers behind it do not. If you need a metric, use `pdftotext -bbox` boxes at
a 0.05 pt tolerance — it gives 0 for both programs in all four builds and is
one command to re-run. Do not quote a number here that you have not
re-measured.

**Watch the margin.** 17 cm page in the trade format, 21 cm on A4 — but both
are set to about the same measure, so a line that overflows in one usually
overflows in the other. Anything over ~15 pt is a defect; the current worst is
6.3 pt. Count vboxes as well as hboxes — an overfull **vbox** means a
boxed block grew past a page and could not break, and the fix is to split the
table, not to shrink the text.

---

## Two editions, two formats, one source

Four main files: two languages times two paper formats. They differ in five
lines each — the class's point size, `\booklang`, `\bookpaper` and the PDF
title — and share everything else, **including the document body**:

```
main-{en,pl}.tex      17 x 24 cm at 11pt, the trade format
main-{en,pl}-a4.tex   A4 at 12pt, the format the book is read in
body.tex              THE document body. One copy, read by all four.
preamble.tex          all machinery, every format
lang/en.tex           every user-visible string + the notation contract
lang/pl.tex           the same macro set, or CI fails
structure.tex         THE part and program sequence. One list, both editions.
figures/values/       computed numbers, committed, shared
code/                 the scripts that produce them
programs/{en,pl}/     the only place prose is duplicated
```

**`body.tex` is not tidiness, it is C15 made structural.** `main-en.tex` was
once rewritten with the introduction dropped and every other check passed,
because nothing that compares *programs* can see a difference that lives in the
*wiring*. Adding a second format would have made that four copies of the wiring
and four chances to make the same mistake. There is one copy, parameterised by
`\booklang` exactly as `structure.tex` already parameterises the program
sequence, so the defect is now impossible rather than merely detected. C15 was
rewritten to guard the structure that makes it impossible: every main file
reads the body, and the body still wires up a whole book.

**Why A4 at all.** The trade format is right for a printed book and wrong for
both things a reader actually does with this one — read it in a PDF viewer, or
print it on an office printer, where a 17 x 24 cm page lands in the middle of an
A4 sheet surrounded by white. Both formats are set to **about the same measure**:
A4 spends its extra width on margin, not on a longer line. A 15.5 cm block at
12pt would be some eighty-five characters, past the point where the eye loses
the line return, and "it reads badly" would have been fixed into the wrong
shape.

A format change moves every page boundary, so **CI compiles all four**. A table
that fits on one page in the trade format can overflow its vbox on A4 without
the trade build noticing, and that is exactly the class of defect a
single-format build ships.

**There is exactly one list of programs**, so the two editions cannot contain
different ones. Part titles live in `lang/*.tex`, not in `structure.tex`: the
rule is that *nothing outside a language file hard-codes a word the other
edition also sets*, and `structure.tex` broke it once with `\ifpl` and produced
a build failure in exactly one of the two editions.

### The parity checks, and why each exists

`tools/parity.py` is the single parity tool. Run it before every commit; CI
gates on it.

| Check | Catches |
|---|---|
| C1 files, C2 include order | A program in one edition and not the other |
| C3 lang catalogue | A label defined in one language only — an undefined control sequence in exactly one build. The regex reads `\newcommand*`, `\newcommand\foo`, `\providecommand` and `\DeclareRobustCommand` as well as the plain form: it used to see only `\newcommand{\foo}`, so a one-edition macro written any other way passed |
| **C4 ordered structural signature** | `\yourturn` moved from frame 2 to frame 3. A histogram cannot see reordering; every Summary back-reference and Quiz route navigates by frame number |
| C5 labels, C6 answer keys | `T3` must be the *same question* in both, not merely the third one |
| C7 values | A `\val{}` with no script behind it, and a computed value nothing uses |
| **C8 per-frame maths digest** | A sign fixed in one edition only. Changes no count and no histogram |
| C10 notation lint | The contract below, enforced with a file and a line |
| **C12 numeric literals, in order, strictly** | A translated number silently changing |
| C13 verbatim ASCII | The `listings` UTF-8 trap |
| C14 macro histogram | A `\trapbox` or an `\index` dropped in translation |
| **C15 main-file wiring** | A main file rewritten with a chapter of front matter dropped |
| **C16 next-frame cues** | A `\nextframe` where the next frame answers nothing, or missing where the next frame answers. C4 and C14 are both blind to a cue dropped in *both* editions at once |
| `check_structure.py --frames` (payloads) | A Quiz route, outcome range or Summary bracket naming a frame the program does not have, or a range that runs backwards. `\teachesat`, `\teachesatone`, `\outcome` and `\sumitem` are the whole of the book's return index, and they were compared *between the editions* and never against the program: a probe routing a Quiz question to frames 91--93 of a 48-frame program was green on `parity.py`, `check_structure.py`, `gen_stubs.py --check` and `make verify` alike, and stays green on parity even now, because the Polish edition says 91--93 too. **It closes the existence half only.** Whether frame 20 answers the question routed to it is a reading job, and the tool says so in its own comment rather than letting a green ledger imply otherwise |
| `check_structure.py --frames` | A cue that is not the **last thing** in its frame. C16 counts cues and cannot see position, so a cue misplaced identically in both editions is invisible to C4, C14 and C16 alike. It is a *line* test on purpose: a cue hoisted above a frame's closing prose tokenises to nothing after it and reads as correctly placed |
| `reflist.py` | `\label{prog:F08}` resolving to F8 in one edition and F9 in the other. Both builds stay internally consistent and neither warns |
| **`checkpdf.py`** (openers) | A frame's rule and margin badge stranded at the foot of a page with the frame's body overleaf. It reads the finished PDF, because that defect produces no error, no warning and no overfull box — no log can see it, and the badge it strands is the book's navigation device |
| **`checkpdf.py`** (headings) | The same one element earlier: a numbered section heading as the last thing on a page, with its section beginning overleaf, because `\begin{fr}` turned the page after the heading had been set. It was pervasive — 42 instances across the four builds when the check was written, in every program from F1 to F4 — and every other gate was green. The heading's size is learnt from the document rather than assumed: `\Large` bold measures *smaller* than the body here, because `pdftotext` reports the font's own box |
| **`checkpdf.py`** (cues) | The mirror image at the other end of the frame: a page whose only text-block content is the next-frame cue, so the reader turns over expecting an answer and gets a running head, two italic words and white paper. A row of dots counts as nothing, because dots-plus-cue is the same defect one breakpoint earlier. The cue is read out of `\lblNextFrame` in `lang/*.tex` rather than hard-coded, so rewording the cue cannot silently switch the check off |
| **`checkpdf.py`** (tails) | The cue's defect one line less extreme, which the cue test cannot see because the page is not *the cue and nothing else*: a body page whose ink stops in its top quarter. Reported, never fatal — see the ledger at the top of this file and the note above the tool's `main()` |

`tools/gen_stubs.py` regenerates every stub and `structure.tex` from
`tools/programs.json`, which is the single source of the part and program
sequence. **It will not overwrite a program that has been written** — a file
with no `\programstub{}` left in it is finished prose — and it refuses outright
if a written program has been renumbered under it, because moving written work
is a decision and not a side effect. `--check` fails when anything is stale.

Use it. Inserting P7 by hand would have been forty-seven file renames and a
renumbering done by eye, and the one-off patch that escaped the briefs' LaTeX
the first time was silently undone by the next regeneration — which is exactly
why the escaping now lives in the generator.

C12 compares **strictly** — the Polish decimal comma is *not* normalised away.
That was tried and it hid the defect it was meant to catch: a `$0.1$` / `$0{,}1$`
pair authored by hand rather than by `\num{}`, which is a number written twice
and therefore a number only one of which will ever be corrected.

**Consequence for the translator:** a digit stays a digit. *Dwubajtowym* for
`2-byte` breaks C12 and is a real editorial divergence, not a false alarm.

### The notation contract

Governed by the **keyboard test**: *if the reader will type the token into a
computer, both editions use the code spelling; if they will only ever read or
write it, the Polish edition uses the Polish form.* So `tg` for the tangent and
`tanh` — not `tgh` — for the hyperbolic tangent, and that apparent
inconsistency is the rule working.

Implemented as macros in `lang/*.tex`, so the *source* is identical and only the
output differs:

| | English sets | Polish sets |
|---|---|---|
| `\tg` `\ctg` `\arctg` | `tan` `cot` `arctan` | `tg` `ctg` `arc tg` |
| `\gcdop` `\lcmop` | `gcd` `lcm` | `NWD` `NWW` |
| `\num{}` / `\val{}` | `0.5`, `10 000` | `0,5`, `10 000` |
| `\dash` | spaced em dash | spaced półpauza |
| `\enquote{}` | British single quotes | Polish quotation marks |
| `\intcc{a}{b}` | `[a,b]` | `[a,b]` — *not* `⟨a,b⟩`; flagged to the reader at the first interval |
| `\Var` `\Ex` | `Var` `E` | `Var` `E` — with a **mandatory** notation box for `D²(X)` in P23 |

Three rows are genuine splits rather than clean divergences, and are settled in
`notes/03-bilingual-and-notation.md` §2.8 so nobody re-litigates them from a
search result: the interval brackets, `tanh` against `tgh`, and `Var` against
`D²`. `D²(X)` is **current** Polish teaching usage, not a historical curiosity —
do not skip its box.

**Rules the lint cannot check**, and the translator brief must carry:
listing comments stay English (the reader is being trained to read English
code); never translate the spelling of a constant (`e`, `π`, `i`); and where an
English ML term has no Polish form in real use, keep the English word and
inflect it Polish. *Embedding*, *transformer*, *token*, *softmax*, *batch* are
what Polish engineers say; *zanurzenie* is a calque nobody will search for.

---

## The Stroud machinery, in LaTeX

Implemented in `preamble.tex`. The interesting decisions:

**`\begin{fr}` is the frame**, not `\begin{frame}`. LaTeX2e already defines
`\frame` (it draws a box in a `picture`), and an environment of that name
silently redefines it. `fr` is also short, which matters when it is typed
seventy times in a program.

**`\ans{}` opens a frame with the previous frame's answer**, set apart and
centred so the eye can find the edge to cover. `\begin{ansblock}` for a worked
answer. `\blank` is the row of dots; it carries a `\penalty0` so a long question
has a break opportunity before the dots — without it the Polish edition ran into
the margin.

**`\canyou` is generated from the declared outcomes.** `\outcome{frames}{text}`
both prints the entry list and accumulates a table row, and `\canyou` replays
the rows. The 1:1 property Stroud's checklist depends on is therefore
structural: the two cannot drift, and the ledger that would have policed it is
reduced to *did this program declare any outcomes at all*.

Note the mechanism: the rows are **accumulated at declaration time**, not looped
over inside the table. A `\loop` inside a `tabularx` body does not survive
alignment scanning — TeX needs to see the `&` and the row break while it reads
the cell, and a conditional hides them. The symptom is an empty table and no
error.

**Answers are authored at the point of use and printed at the back**, carried
there by a global macro store (`\csgdef` + etoolbox lists), not by an auxiliary
file. The companion volumes collect their manifests with `\@starttoc` and a
custom extension, which works because those entries are one line of text. It is
the wrong mechanism for an answer: an answer contains displayed maths, and
material written to an `.aux`-style file is expanded at shipout, where fragile
commands break with errors that name neither the answer nor the program.
`\include` is sequential within a run, so a macro defined globally while
typesetting F1 is still defined when the back matter is typeset. That is all
this needs.

**Program numbering** is `F1..F13` then `1..33`. `\foundationnumbering` and
`\mainnumbering` switch it. Both also set `\theHchapter`, which is hyperref's
*destination* name: resetting the chapter counter without it produces duplicate
PDF destinations and bookmarks that jump to the wrong program. `\appendix` is
patched for the same reason.

**Admonitions**, a deliberately small fixed vocabulary: `note`, `warning`,
`trapbox` (the misconception, after the reader has walked into it), `aibox`
(*where this shows up in AI* — if it cannot name a specific line of a specific
system it should not be written), `rigourbox` (*what we are not proving*, and
where the proof lives), `notationbox`, `verifybox`, `exercisebox`.

**Two box treatments, and that is the whole visual grammar.** `mfa tinted` is a
block the reader may read in passing: a tint and a thick left bar, no outline.
`mfa outlined` is a block the reader must stop at: a full rule on white. Both
styles live in one `\tcbset` so the eight boxes share one set of spacing
numbers rather than eight copies that drift. A third treatment would mean the
first two are not carrying their meaning.

The numbers that matter are `before skip` and `after skip`, at 13 pt. tcolorbox
defaults to a couple of points, which is not enough air to read as a separate
block — and every box carrying its own value is how a page ends up looking
arbitrary.

**The frame boundary is a hairline across the measure, with the frame's number
in the OUTER margin beside it** — right on a recto, left on a verso, following
the spread, so a reader thumbing for frame 37 runs a finger down the edge of
the block and never crosses the text. That is the original
(`notes/07-stroud-original-layout.md` §3) and the reason is navigational.

The badge is a `\marginnote`, never a `\marginpar`: `\marginpar` floats, takes
one note per line and defers the rest with *Marginpar on page N moved*, and at
four to six frames a page that is the normal case. A badge that has moved down
the page no longer names the rule it belongs to, which is the one thing the
element exists to do. Loaded `[quiet,noadjust]`, and `noadjust` is load-bearing:
under the default the note emits a `\strut` into the rule's line, which is
invisible until the next item is tall enough to clamp the interline glue — and
about a third of frames open a tcolorbox immediately after the rule. Nothing in
the preamble may set `\reversemarginpar`; marginnote honours it and would move
every badge to the *inner* margin silently.

`\marginparwidth` and `\marginparsep` are declared per format in the geometry
options and asserted at `\begin{document}` against the narrower of the two
outer margins. Left to the class the margin box is 116 pt wide inside a 51.2 pt
margin and the badge survives by accident. Do **not** reach for geometry's own
*the marginal notes overrun the paper* warning as the guard: `\Gm@checkmp` is
called only under `\ifGm@verbose`, this preamble does not pass `verbose`, and a
deliberately over-wide setting warns about nothing. The assertion is a hard
error instead.

`\mfaframeabove` (17 pt) and `\mfaframebelow` (12 pt) are the gutter, and they
are the most load-bearing numbers in the layout: the frame is the unit the
reader covers with a hand, and two frames a hairline apart are one block of
text to the eye no matter what the rule says. Generous above, tighter below, so
the white space reads as belonging to the frame that follows it. `below` went
from 10 pt to 12 pt when the badge left the flow: the old badge hung off the
rule's left end and filled that gap, and a bare hairline does not.

**A named frame is a frame with a heading.** `summarybox` and `testexercises`
call `\mfa@namedframe`, so the Summary and the Test exercises are numbered
frames and take the two numbers after the last teaching frame — 46 and 47 in
F1. The Summary's badge is joined by a drawn three-row list icon sitting on the
rule where the number used to be, and a broken Summary panel carries a
triangular continuation mark on every piece but the last. `Can you?` and
`Further problems` are deliberately *not* frames; the reasons are in notes/07.

**The debt ledgers count teaching frames, not printed frames.**
`check_structure.py`'s `RE_FRAME` and `parity.py`'s frame counter both match
`\begin{fr}` only, so F1 reports 45 while the reader sees 47. That is correct —
the 30–70 band is a statement about teaching load and the two closing frames
are fixed overhead every program pays — but it is a quiet disagreement, so it
is written down in both tools. Do not "fix" one counter without the other, or
every program's band shifts by two.

**The next-frame cue is placed by rule, not by taste.** A frame carries
`\nextframe` **if and only if the next frame opens with `\ans` or
`\begin{ansblock}`**, ignoring a leading `\label`, which marks a position and
typesets nothing. That is a mechanical property of the file, so it is inserted
mechanically and checked mechanically: parity's **C16** fails when a cue sits
where nothing answers it or is missing where something does, and
`check_structure.py`'s `RE_DEMANDS` treats the cue as the demand it announces.
C4 and C14 are both blind to a cue dropped in *both* editions at once, which is
exactly the failure this repository has been bitten by before.

**The opener's frame range is a two-pass value carried in the `.aux`.** Each
program writes `\mfaframetotal{key}{n}` at the start of the *next* program and
at `\end{document}`; the next run reads them all back before anything is
typeset. A total of `0` is a written measurement, not an absence — it is what
tells a stub from a program whose total this run has not computed yet. Neither
the key nor the count may be recomputed at the flush: `\mainnumbering` resets
the chapter counter between Part I and Part II, and an appendix's `\chapter`
resets `frameno`. A program with no recorded total prints **nothing** and
reserves nothing, and raises a rerun warning; it must never print `??`, because
46 of the 47 programs are stubs and a marker on 46 openers trains the reader to
ignore it.

**The running head no longer carries the frame number.** It is mirrored as the
original is: page number **outer**, running title **inner** — the program on
the verso, its title in italic on the recto — and the foot is empty. Chapter
openers keep the class's `plain` style, number at the foot and no head, which
is why the frame-range box is the first thing on the page. The old recto head
named the last frame *begun* on the page, so it could read `Frame 10` over
badges 7, 8 and 9; the margin badge names the frame the reader is looking at.

**A program opens between two rules** — a hairline above the PROGRAM Fn line, a
heavy one under the title — and a part page gets the same treatment one level
up. Programs are what the reader navigates by: every Summary back-reference,
every Quiz route and every cross-reference in the book names a program and a
frame. A coloured title alone does not survive being thumbed past.

---

## Build traps already hit and fixed

Each cost time; none is obvious from its error message.

- **A `#1` inside an `\IfFileExists` branch.** `\IfFileExists` stores its
  branches in `\reserved@a`, so `#1` is read as a parameter of *that* macro and
  the run raises `Illegal parameter number in definition of \reserved@a`. The
  branches need `##1`. The consequence here was that **siunitx never loaded**,
  so the decimal comma — the single most visible feature of a Polish
  mathematics book — silently did not work.

- **`amssymb` alongside `newtxmath` is a fatal clash**, and it is invisible on a
  machine without newtx. `newtxmath` supplies the AMS symbols itself, so loading
  `amssymb` too gives
  `amssymb.sty:261: LaTeX Error: Command \Bbbk already defined` and no PDF.
  This is the one to remember, because of *how* it was found: every local build
  was green for hours, because this container has no newtx and the preamble
  degrades past it. **CI, on a fuller TeX Live, failed on the first line of the
  first program.** A preamble that probes for optional packages is only tested
  by a machine that has them.

  The preamble loads `amsmath` first, then `newtxmath` if present and `amssymb`
  only if it is not.

- **`grep '^!' main.log` cannot see that error.** With `-file-line-error` an
  error line begins with a *path*, and `-interaction=nonstopmode` writes a PDF
  over the top of it, so the exit code and the PDF both say fine. This is the
  habit inherited from both companion volumes and it is not sufficient here.
  **Use `tools/checklog.py`**, which matches both formats and also fails on an
  overfull vbox and on an hbox over the 15 pt budget.

- **A non-converged build exits 0 with a stale number on the page.** Two things
  in this book ride through the `.aux` on `\@newl@bel` and are keyed on layout:
  marginnote's record of which margin each frame badge belongs in, and each
  program's frame total for the range on its opener. Both can oscillate, and
  both fail *silently* — the failure is a wrong number, not a missing one,
  which is the same shape as a console block nobody ran. `Label(s) may have
  changed` used to be in `checklog.py`'s `WARN_IGNORE`, and `report()` never
  failed on a warning anyway. It is now in `HARD_WARN` alongside `Rerun to
  get`, `Marginpar on page` and marginnote's `Consecutive odd/even pages`, and
  a final log carrying any of them fails the build.

- **`\ifpl` was fragile.** A plain `\newcommand` in a `\part` title lands
  *unexpanded* in the `.toc`, and on read-back the English build died with
  `Extra }, or forgotten \endgroup` while the Polish one survived — a
  one-edition-only build failure. `\DeclareRobustCommand` fixes it;
  `\pdfstringdefDisableCommands` is then needed as well, because a robust macro
  cannot go into a PDF bookmark string either. The better fix, which is what is
  in the tree, is that part titles do not use `\ifpl` at all.

- **A `listings` body sets `'` as a RIGHT SINGLE QUOTATION MARK, and the code
  on the page is then not code.** In T1 the input character `'` is
  `quoteright`, so `struct.unpack('<f', ...)` prints as
  `struct.unpack(’<f’, ...)`; typed back in that is
  `SyntaxError: invalid character (U+2019)`. It is **font-dependent**, which is
  why it shipped: `inconsolata` is loaded with `varqu`, whose whole purpose is
  an upright quote, so on a full TeX Live the page looks right. This container
  has neither inconsolata nor newtx, and it is the container the published PDF
  is built in — the `amssymb`/`newtxmath` trap from the other end, where a bare
  installation ships a defect a full one hides. The preamble loads `upquote`,
  which makes `'` the ASCII apostrophe whatever the typewriter font is. Check
  it the only way that means anything: extract the listing from the finished
  PDF and run what comes out.

- **`\val{}` does not expand inside a listing.** `listings` reads verbatim and
  the style sets no `escapechar`, so it prints the macro name. **Every console
  transcript must be a file written by `code/` and pulled in with
  `\lstinputlisting`. No transcript is typed.** The companion volume's
  consistency pass found that its only outright factual error survived a whole
  draft inside a fabricated `console` block, because a transcript nobody ran is
  indistinguishable from one that was.

- **`\mermaidfig` used to float its unrendered fallback.** A Mermaid source
  typeset verbatim is often taller than a page and a float cannot break, so
  every unrendered diagram produced an overfull box. The fallback no longer
  floats.

- **`fancyhdr` needs its head height set through `geometry`** (`head=23pt`), not
  by `\setlength{\headheight}` afterwards, or the text block moves. And any
  `\chaptermark` redefinition must come *after* `\pagestyle{fancy}`, which
  installs its own and silently discards anything defined earlier.

- **Never add a `literate` mapping for U+00A0.** Fatal, no PDF, and the message
  names neither the character nor the line. Hit in two of the three books in
  this series; latent in the third.

- **`babel` with a missing language is fatal, not a warning.** The preamble
  probes for `polish.ldf` and `british.ldf` before requesting either. Do not
  simplify this back to a bare `\usepackage`.

- **A rule drawn after a mark draws straight through it.** The frame number is
  in the margin now, but the Summary's list icon still sits *on* the separating
  rule and the trap is unchanged for it. Doing it the obvious way round — mark
  first in an `\rlap`, then the rule — paints a hairline across the glyph,
  which at that size reads as struck out rather than as a tab on a line. The
  rule goes down first, inside the `\rlap`; the mark is painted over it second,
  on a white ground so the hairline is masked either side. Nothing warns; it
  just looks wrong.

- **Do not guess the vertical shift of anything that sits on the frame rule.**
  The badge and the Summary icon are each centred by measuring their own box —
  `\dimexpr0.3pt-0.5\ht<box>+0.5\dp<box>` — never by a fixed offset, because
  the two formats set 11pt and 12pt from the same source and a hard-coded shift
  is right in exactly one of them. The badge's own tikz box is 11.94 pt tall at
  11 pt, so the shift is −5.67 pt there: it is nowhere near zero and it is not
  guessable. Measure the marginnote's baseline **outside** its `\raisebox` if
  you ever check this; inside it you measure the raise and get a constant
  −5.67 pt that looks like a defect and is not.

- **A breakable tcolorbox splits itself, in its own code, and will contribute
  an empty first piece.** So `\nobreak` before one does not keep a heading with
  its panel: the rule, the badge, the icon and the word *Summary* end up alone
  at the foot of a page with the panel overleaf. This is the one service
  `\section*` was performing for free, through `\@startsection`'s penalty, and
  it stopped being free the moment the heading stopped being a `\section`.
  needspace does not fix it either — its trick relies on TeX finding the page
  overfull and preferring an earlier breakpoint, and on a rigid page every
  candidate is equally awful, so TeX keeps the material and lets tcolorbox
  split anyway (measured: 95 pt reserved against 54 pt left, still stranded).
  Measure `\pagegoal-\pagetotal` and turn the page explicitly — and remember
  `\pagegoal` is `\maxdimen` on a fresh page, which means *unlimited*, not *no
  room*; testing it the obvious way turns a page at the top of every program.

- **An over-long `fancyhdr` field does not overfull. It prints on top of the
  field next to it.** With the page number and a running title sharing one
  measure, fancyhdr sets an over-wide field at its natural width and overprints:
  measured at 15 pt of overlap with P25's 82-character title, with zero overfull
  boxes, zero warnings and exit code 0 from both latexmk and `checklog.py`. The
  15 pt hbox budget is structurally blind to it. Anything placed in a running
  head must be width-capped; `\mfaheadmark` measures the box and scales only if
  it is too wide, reserving 4 em at `\small` so the reserve tracks the point
  size. This is latent today only because no long-titled program is written.

- **`\usebox0` followed by a space typesets that space.** `\usebox` takes an
  undelimited argument, so `\usebox0 #1` consumes the `0` and sets the space —
  3.33 pt of it, measured — through which a hairline shows as a short grey stub
  that looks like dirt on the page. Write `\usebox{0}#1`, or use a named box.

- **`\marginnote` must be called in horizontal mode**, or it attaches to the
  wrong baseline. `\framerule` issues it after `\noindent` and the rule's
  `\rlap`, from the rule's own line, which is what makes the note and the rule
  share a baseline.

- **`\parfillskip=0pt` leaks unless the `\par` is inside the same group.** The
  flush-right idiom used by the outcomes' frame range and the Quiz's route boxes
  sets it; `\teachesat` happened to hide the leak because xstring forces it into
  a `\begingroup`, and `\teachesatone` had no group, so every later paragraph
  in the same quiz was set fully justified on its last line with an underfull
  hbox in the log. Brace the parameter and the `\par` together.

---

## Resolved questions

### Scaffolding pass, August 2026

**Four checker bugs, each of which had let a real defect through.** Recorded
because the pattern is the point: *a check that is wrong in the same way in both
editions stays green and only the ledger lies*.

1. The notation lint peeked a fixed distance behind each decimal looking for a
   `\num`, so `\frac{\num{1e5}}{0.75}` passed — the `\num` belonged to the
   numerator and the bare decimal was in the denominator. Wrapper spans are now
   removed before the scan.
2. The per-frame maths digest included the words inside `\text{}`, so
   *and also* against *oraz* read as a mathematical divergence. Prose inside a
   display is normalised out.
3. `\val{}` inside maths never reached the value ledger, because a maths span is
   consumed and digested whole. Both editions were wrong identically, so parity
   stayed green while the ledger reported values as unused that the book was
   printing.
4. There was no check on the two main files at all, and one of them was
   rewritten with the introduction dropped. Every other check passed. C15 exists
   because of that.

**Two parity tools became one.** They disagreed, and both were right about
different things. `parity.py` kept the ordered signature and the maths digests;
it absorbed strict numeric comparison, the verbatim-ASCII guard and the macro
histogram from the tool it replaced.

### Program F1 pass, August 2026

**F1 is *Numbers, powers and roots*, not floating point.** The first draft brief
proposed opening with machine arithmetic, on the argument that the AI engineer's
equivalent of arithmetic is the number system their hardware implements. It is a
good argument and it is wrong for *F1*: the Foundation part must assume nothing,
and a reader who genuinely needs it is not ready for a mantissa on page three.
The floating-point material became **P1**, placed before the linear algebra
rather than after it, and `notes/05-floating-point-plan.md` is its plan.

What F1 keeps from that argument is the *payoff*: it ends on sizing a model's
weights, and it points forward to P1 at the exact moment a reader asks why
`0.1` is awkward.

**Frame numbers must be corrected after writing, not before.** The outcomes, the
Quiz's `\teachesat` routes and the Summary's brackets all name frames, and the
draft plan's numbers were wrong by ten by the end. Write the program, then map
the frames (`\begin{fr}` occurrences, in order), then fix every reference. It is
mechanical and it is not optional: those numbers *are* the return index.

**Four traps, and the strongest is the compounding one.** `2^10 ≈ 10^3` is
2.40% wrong, which is nothing; `2^80` against `10^24` is 20.89% wrong, which is
not. It generalises to the per-layer error bound in P2 and to the GB/GiB ladder
in the same program, so it earns its place three times.

### Program F2 pass, August 2026

**Fifty teaching frames, both editions, and the plan was right about the
mathematics and wrong about three placements.** All three failures were the
same failure: the plan put a diagram at a frame that ends by asking a question,
and F01's practice — never stated, only observed — is that a figure sits only
where the *next* frame does not open with an answer. A figure between a
question and its answer box puts the reader's own answer overleaf from the
question. So three frames were rewritten to close a teaching beat instead of
asking:

- **Frame 21** works `(x+2)(x+3)` through in full and points at the grid;
  the elicitation of `(a+b)^2` is wholly frame 22.
- **Frame 39** works the whole of `y = wx + b -> x = (y-b)/w`; the plan's
  second question, *make b the subject*, is gone and frame 40 carries the
  acquired condition instead.
- **Frame 45** states the four-step method and applies steps one to three
  without asking; frame 46 does step four. Everything in section 8 therefore
  sits one frame later than the plan, and trap 39's route is **45--48**.

The cost is the cue rate: **39 of 50, 78%**, against the plan's projected 82%.
That is the right trade — the alternative was three figures printed between a
question and its answer.

> **Superseded in part by the F2 review pass below.** Frame 21 obeyed the rule
> above and the trap still did not fire, because the rule is about the *answer
> box* and the defect was the *figure's own content*. Figure F2.1 now sits after
> frame 23, which does end by asking, and its answer box is frame 24 — the only
> deliberate exception in the program, taken because the figure explains a
> correction and previewed a trap where it was. It was checked on the page: in
> all four builds the question, the figure and the answer are on one page, so
> nothing the reader writes is overleaf from what they wrote it about. The rule
> to write against now is the wider one in *Non-negotiable conventions*.

**Five traps, each elicited before it is named**, and the two the brief owns are
the load-bearing pair. `(a+b)^2` is elicited at 22 under a *speed* instruction,
immediately after frame 21 has made the reader fluent with the grid; the
correction names `a^2 + b^2` on the page first, falsifies it at 3 and 4, and
then explains the reasoning — an index does distribute over a product, and the
reader generalised a true rule past its hypothesis. Trap 39 (the convolution
floor) is elicited in two steps across 46 and 47: the first case has the stride
dividing exactly, so the floor is decoration and the reader stops typing it, and
then one digit changes. Both wrong answers, `3.5` and `4`, are predicted by name
in frame 48.

**Two corrections to the plan's own text, both small and both worth recording.**

- The plan's frame 48 says *the mismatch surfaces `f02.conv.gap.3` layers
  downstream*. That misreads the key: `gap.3` is the **shape shortfall** (1),
  not a distance in layers. The frame says *you are one short* and leaves the
  downstream distance qualitative, which is also the honest claim.
- Quiz Q10 is `\teachesat{33--34}`, not `\teachesatone{33}`: frame 33 asks it
  and frame 34 answers it.

**Two overfull hboxes, and the second is a new class this book had not met.**
Both were fixed and the multiset came back to the pre-F2 baseline exactly.

- **32 pt: a word-formula set inline.**
  `$\text{bytes} = \text{parameters} \times \text{bytes per parameter}$` has no
  break opportunity anywhere in it — three `\text{}` spans and two operators —
  so it cannot be broken and it cannot be hyphenated. A word-formula goes in a
  display, always.
- **12.6 pt in the *diagram manifest*, Polish only, in both formats.**
  `\mermaidfig` writes `\texttt{<key>.mmd} --- <third argument>` into a
  narrow, indented contents line. At 24 characters `f02-equation-to-code.mmd`
  plus a 139-character Polish description overflowed; the 22- and 23-character
  keys beside it did not. **The third argument is manifest copy, not a caption:
  keep it short, and shorter again in Polish, where the words are longer.**
  The sibling volume records the same failure from the other end — a long
  `\code{}` inside screenshot instructions landing in the same column.

**Also worth keeping:** `f02.conv.dropped` is `1`, and quoting it first in a
sentence starts that sentence with a digit in both editions. Reworded rather
than left. A value that is a small integer needs its sentence built round it.

**The numbers behaved as `code/f02_algebra.py`'s comments said they would.** The
layer-norm misreading gives 297.03 against 90.45, 228.4% above the printed
value, and the frame says in the same breath that the variance was chosen small
on purpose and that the ratio is not typical while the failure mode is. The Adam
comparison lands at 0.00050000 against 0.00100001 — a factor of 2.00002, not
2 — and the frame quotes the five decimals rather than rounding a number the
reader would then check and find inexact.

### Program F2 review pass, August 2026

Two independent reviewers read the program **and the rendered pages**, and
between them found four blocking defects. Every one of the four was invisible to
every gate in the repository, and three of them were invisible because they live
on the finished page rather than in the source. That is the generalisable
finding: **this book now has a class of defect that only a reader of the PDF can
see**, and `checkpdf.py` was written for exactly one member of that class.

**1. The headline trap did not fire.** Figure F2.1 printed
`(a + b)^2 = a^2 + 2ab + b^2` in a node, and it sat on the same page as, and
four inches above, the frame that says *cover the rest of the page and write
down the expansion of (a+b)^2 as fast as you can*. Covering the page does
nothing when the spoiler is above the covering hand. The figure moved to after
frame 23 — the correction — and the identity came out of the node and out of the
caption; it teaches as corners-versus-edges and states no result. The rule that
was in this file was too narrow (*a figure sits only where the next frame does
not open with an answer*) and is now the wider one, in *Non-negotiable
conventions*: **a figure must not answer the frame that follows it.**

Verified on the page, not in the source: in all four builds the elicitation
frame ends on one page and the figure is on the next, below the correction, with
frame 23's closing question and frame 24's answer on the same page as the figure
so nothing the reader writes is overleaf from what they wrote it about.
`\mermaidfig` renders into `figure[htbp]`, so this **cannot be settled by source
order alone** — a float can be hoisted to the top of the page it is declared on.
It cannot rise above the page where its declaration point falls, which is what
makes the fix sound; but re-check it on the page after any edit that moves the
break.

**2. *Before you turn over* was false, and differently false in each edition.**
Three of them: the page carried both frames in English, and the Polish build
broke elsewhere again, so the same sentence was true in one edition and false in
the other. Nothing can gate this — C4, C8, C12 and C14 all read the source, and
the four PDFs paginate differently by construction. Now *before you read on* /
*zanim pójdziesz dalej*. The rule is in *Non-negotiable conventions*.

**3. A trapbox asserted a remembered fact about C.** *In Python `-3**2` is −9,
and the same expression in C behaves the same way.* **C has no exponentiation
operator**; `-3^2` in C is a bitwise XOR. The claim was written from memory into
a printed box, in a book whose first rule is verify before writing. Both halves
of the replacement were run before being written:

- `python3 -c "print(-3**2)"` → `-9`
- `node -e "console.log(-3 ** 2)"` → `SyntaxError: Unary operator used
  immediately before exponentiation expression. Parenthesis must be used to
  disambiguate operator precedence` (Node 22)

JavaScript's refusal is a better example than C's agreement would have been,
because the box's point is that the line is ambiguous — and one real parser says
so in as many words.

**4. The same box gave a negative variance the wrong cause.**
`notes/02-grounding-and-traps.md` item 3, owned by P01, attributes it to
catastrophic cancellation in the one-pass formula. Two programs would have given
one symptom two causes. The squared-error clause stays; the variance clause is
now a cross-reference to P1.

**The trap catalogue is a source of authority over the chapters, not a
by-product of them.** Check a trap claim against `notes/02` before writing it,
the same way an API claim is checked against the installed package in the
sibling volumes.

#### The seven smaller findings

- **The trap was announced.** *The next frame is going to catch you holding it*
  removes the confidence, and the errorful-generation benefit is largest exactly
  when the learner was confident. Cut. Frame 22's *no working, as fast as you
  can do it* suppresses deliberation without warning.
- **Two Quiz routes named the asking frame**, against F01's convention of
  routing to the frame that answers: Q2 `4` → `4--5`, Q8 `24` → `24--25`. All
  thirteen routes and all fifteen Summary brackets were then re-read against the
  frames; `\sumitem{7--9}` → `7--10`, because the *which an array library will
  not tell you* clause is frame 10's warning box. **There is now no
  `\teachesatone` in F02** — every route is a range, which is what a route to an
  answered question looks like.
- **Frame 29 overstated the factorisation saving.** Horner's `x(x + 5) + 6` is
  one multiplication and two additions *without* factorising, so the saving is
  against the naive expanded form and not the best one. The frame says so now,
  and keeps the transferable habit: count the operations rather than trust the
  shape.
- **Two aiboxes named no system.** Frame 50's was a four-program roadmap and is
  now prose. Frame 12's named a shape and then talked about compilers, which is
  not AI; it now collects the like terms of the original transformer's
  feed-forward block, `4d^2 + 4d^2 = 8d^2`, which is the program's own move done
  on a real model's numbers. The aibox rule holds: **if it cannot name a
  specific line of a specific system it is prose.**
- **F02 used `\blank` zero times in fifty frames** where F01 uses it five times.
  It is a distinct retrieval mode — a gap inside a worked line rather than a
  question with an answer overleaf — and skipping it costs the program a rung of
  the scaffolding gradient. Added to frames 20 and 46; 46's three-stage floor
  evaluation was a gapped worked example in everything but the macro.
- **Polish `krok` was carrying both *step* and *stride***, in one frame and then
  two frames apart. Both readings are standard, which is why the collision is
  invisible to the translator and visible to the reader. The stride is now
  `przesunięcie`, introduced once as *przesunięcie, czyli krok splotu*, so every
  remaining `krok` in the program means *step*. **No digit changed**, so C12
  stayed green.

#### What was measured

Three measurements, all made against the finished PDFs, because the log has
nothing to say about any of them. The scripts are disposable; the methods and
the numbers are not.

**Diagram type size.** A `\mermaidfig` is an `\includegraphics` scaled to the
measure, so its node text lands at whatever size the scaling leaves it. Method:
take the document-wide modal word-box height as the body reference, then take
the modal box height of the words above each caption that are shorter than the
body. F1's three diagrams set the floor.

| | en 17x24 | pl 17x24 | en A4 | pl A4 |
|---|---|---|---|---|
| F1.1 / F1.2 / F1.3 | 4.32 / 4.35 / 4.47 | 4.32 / 4.24 / 4.47 | 5.37 / 5.41 / 5.09 | 5.37 / 5.27 / 5.09 |
| F2.1 before | 2.89 | — | — | — |
| **F2.1 after** | **6.61** | **5.75** | **7.52** | **6.55** |
| F2.3 before | 3.58 | 3.57 | 4.08 | 4.06 |
| **F2.3 after** | **5.69** | **5.58** | **6.48** | **6.36** |
| F2.2 | 4.57 → 4.69 | 4.55 → 4.63 | 5.20 → 5.34 | 5.18 → 5.27 |

**The "before" column cannot be re-derived.** The six `f02-*.mmd` files were
untracked when they were first measured, so git holds no earlier revision to
re-render and those figures rest on one pass's word. The "after" column was
reproduced independently to the hundredth. Commit a diagram before you measure
it, and the next comparison will be checkable.

**The cause is always the graph's width, never the font.** `\mermaidfig` scales
to `0.95\linewidth` or `0.42\textheight`, whichever binds, so on-page type size
is `12.57 pt x min(350.9/W, 229.2/H)` in the trade format and
`12.57 pt x min(398.4/W, 284.9/H)` on A4, where `W` and `H` are the rendered
`.mmd`'s own page in points — `pdfinfo` prints them. Re-measured over all nine
figures now in the book, in all four builds, that formula reproduces the
measured type size **to a hundredth of a point every time**. F2.1 was eight
nodes across; it is now four ranks of at most two. F2.3 was a six-rank chain;
the four reading steps are paired into two nodes and it is four ranks.

**The aspect ratio is a FLOOR, not a band, and the recorded band was wrong at
the top.** *Aim for 2.2–2.8* was written from one program's redesign and the
book's own shipped practice contradicts it: F3's three diagrams are **3.59,
3.24 and 2.59** and they measure the largest node text in the book. What the
number actually governs is one thing only.

- **Stay above about 1.5.** Below that the height cap binds — the crossover is
  `350.9/229.2 = 1.53` in the trade format and `398.4/284.9 = 1.40` on A4 — and
  the figure is set to its full allowed height whatever its width. It then
  cannot share a page with the frames it belongs to and floats away with a
  quarter of its own page blank. That is what happened to the first square
  redesign of F2.1, at 7.07 pt.
- **There is no ceiling.** Above the crossover the *width* cap always binds, so
  the aspect ratio drops out of the type size entirely and only `W` is left:
  `12.57 x 350.9/W`. F1.3 is 5.50 and F2.2 is 4.35, and both are small for the
  same reason F3's are large — they are 985 and 939 points wide.

So the working rule is a **width budget**, which is the quantity the type size
actually depends on: under about 700 pt keeps node text above 6.3 pt, and under
about 520 pt reaches 8.5 pt, which is where F3 sits. Measured, in the trade
format:

| | W x H (en) | ratio | binds | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|---|
| F3.1 log-mirror | 517 x 144 | 3.59 | width | 8.51 | 8.63 | 9.69 | 9.82 |
| F3.2 underflow | 645 x 199 | 3.24 | width | 6.82 | 7.02 | 7.76 | 7.99 |
| F3.3 log-axis | 516 x 199 | 2.59 | width | 8.53 | 8.23 | 9.71 | 9.36 |
| F1.1 magnitudes | 210 x 667 | 0.31 | **height** | 4.32 | 4.32 | 5.37 | 5.37 |

`W` is the English render; the Polish one differs, because Polish labels are
longer, and that is why the two editions' figures do not measure alike — pl
log-mirror is 510 wide and sets larger, pl log-axis is 535 and sets smaller.
Predicted and measured agree to a hundredth in all sixteen cells.

The last row is the hazard, kept in the table because it is the only figure in
the book on the wrong side of the crossover.

**Glyph overlap from inline `\dfrac`.** Method: word pairs on adjacent lines
whose boxes overlap by more than 2.5 pt, body-sized words only — diagram text is
packed tightly inside its nodes and would bury the signal. Measured with the
same build either side of the change, so only the fractions differ.

| | F1 (control) | F2 before | F2 after |
|---|---|---|---|
| en 17x24 | 8 | 25 | **0** |
| pl 17x24 | 8 | 21 | **0** |
| en A4 | 12 | 22 | **3** |
| pl A4 | 10 | 22 | **2** |

Worst single overlap in F2 went from 6.32 / 6.12 / 7.30 / 7.30 pt to
0 / 0 / 2.58 / 2.58. **F02 now overlaps less than F01 does**, over more pages,
and F01 is the next thing to fix by the same method.

**A trap worth knowing before you measure anything from an `.aux`.** All four
builds write to the same `programs/<lang>/*.aux`, so after `make all-formats`
those files describe **whichever format ran last**. A page range computed from
them for the trade build is silently a few pages short, and the measurement
then quietly omits the end of the program. Read the ranges out of the PDF's own
running heads instead — the verso head names the program.

### Program F3 review pass, August 2026

Two independent reviewers read *Logarithms and logarithmic scales* **and
rendered every page**, as they did for F2, and between them found nine factual
errors on the page, one false claim the book made about itself in four places,
five pedagogical defects and two holes in the tooling. Every one of them was
invisible to every gate in the repository. The generalisable finding is
narrower and sharper than F2's:

**A book can be wrong about a book. It is the class of claim nothing checks,
because there is no external source to check it against.** Four of the errors
were F3 describing the rest of this repository — its build behaviour, its own
notation ban, another program's figure — and each was written from memory about
material the author could have opened in the next tab.

#### The one that matters most: the notation box was false about the build

The box said a bare logarithm **"raises an error and no PDF is produced"**. It
does not. `-interaction=nonstopmode` writes a PDF over the top of the error,
which is the first entry in this file's own *Build traps* section and the
reason `tools/checklog.py` exists at all. Appendix B had it right the whole
time — *the build refuses a bare logarithm* — so the book contradicted itself
between a chapter and an appendix, in the direction of the stronger claim.
§F03-base now matches Appendix B word for word in substance.

The same box then said the frame above it was **"the one deliberate exception
in the whole book"**. There are five typeset `\mfalogplain` in F03 alone — the
entry Quiz, frame 8, frame 9 twice, frame 13's aibox — plus Appendix B. The
claim appeared in **four places**: the box, both file headers (as *once*), and
`preamble.tex`'s own comment on the macro. All four are fixed, and the fix is
not a corrected count:

> **Record the restriction as a rule, never as a tally.** `preamble.tex` now
> names the places the ban is lifted — Appendix B, F03's Quiz and §2 — and says
> in as many words that the count is deliberately not stated, because it was
> stated, it was wrong by five, and **nothing can check it**: C10's regex
> cannot see inside the macro name. A tally nobody maintains is a claim that
> decays silently.

#### The other eight factual errors

- **A wrong answer was printed.** Further problem 17 said `log_b x` and
  `log_c x` differ by `1/log_b c`. They differ by `log_b c = 1/log_c b` — the
  printed factor was its reciprocal. `log2(100)/log10(100) = 3.3219 = log2(10)`,
  and `1/log2(10) = 0.301`. The irony is worth keeping: this is the inversion
  §2 of the same program warns about by name.
- **`np.logspace(-5, -2, 4)` does not "return exactly those four".** Element 0
  is `9.999999999999999e-06`, one ulp below `1e-5`. numpy's repr prints
  `1.e-05` and hides it, and the script's own guard rounded `log10` to nine
  decimals and hid it too — a comparison nothing within a few hundred ulp can
  fail, which is a guard that has already stopped working. The prose now says
  *prints*, a note box states the ulp, and **the script's assertion is now a
  bitwise comparison of `struct.pack` bytes**. A second assertion checks the
  numpy claim wherever numpy exists and **announces itself when it is skipped**,
  because `make numbers` must run on a plain `python3`.
- **F3 was false about F1's own figure.** §7 opened by saying F1's ladder of
  magnitudes *climbs by a factor of ten per rung and prints the rungs evenly
  spaced*. `f01-magnitudes.mmd` climbs `10^0 -> 10^3 -> 10^5 -> 10^9 -> 10^12
  -> 10^22` — 3, 2, 4, 3 and 10 decades. Neither predicate was true, and the
  section's whole argument leant on it. The payoff is kept and the predicates
  are gone: the ladder *labels every rung with a power of ten and measures the
  climb in exponents*, which is true and is the same point.
- **A table contradicted the sentence above it.** *Four values of x a
  thousand-fold apart* headed a table of 10, 1000, 10^6, 10^9 — the first gap
  is a hundred-fold. Now *spread over eight decades*, which leaves the payoff
  sentence (*a hundred-million-fold increase moves the logarithm by eight*)
  exactly right.
- **"A ratio with four zeros in it."** The ratio is `50000/7 = 7143` and has no
  zeros; the four zeros are in `50000`.
- **"Three of the four runs tested the same order of magnitude as each other."**
  The linspace points are `1e-5, 3.34e-3, 6.67e-3, 1e-2`; F01 defines an order
  of magnitude as the exponent alone, so only two share one. Now *within a
  factor of three of one another*, which is measured: `1e-2/3.34e-3 = 2.99`.
- **Frame 31's arithmetic was not reproducible from what was printed.** The
  page said *2000 copies of log10(0.0907) added together*, which gives
  −2084.79, and then printed −2084.61 — the figure from the **unrounded**
  `e^-2.4`. The script said so in a comment; the page did not. The step is now
  written as `2000 x (-2.4)/ln 10`, which is what was computed, reproduces
  −2084.61 to the digit, and is the better teaching move: it shows the loss
  becoming a base-ten exponent.
- **One quantity at two precisions, two inches apart.** `f03-log-axis.mmd` node
  B3 said 31.6 and the frames print `\val{f03.axis.mid}` = 31.62; on `main-en`
  p96 both were on the page. The diagram says 31.62.
- **The diagram's axis marks belonged to a different axis than the question it
  set up.** Node A1 listed the linear marks as 0, 25, 50, 75, 100 and node A3
  then asked about 10 -> 100. A1 now states that the marks step by a fixed
  amount, which is the property being contrasted, and A3 is unchanged.

#### Pedagogy: the entry Quiz was spoiling the program's headline trap

Quiz question 4 read *`math.log(1000)` prints 6.907755 and your schooling says
log 1000 = 3. Which of the two is wrong?* That is not a question about the
trap, **it is the trap's reveal, printed before frame 1**. Frame 8 then asks
the reader to write down `log 1000` from memory and could not fire for anybody
who took the triage Quiz — which is every reader the Quiz is for. F02's
precedent is the opposite: its Q7 asks *Expand (a+b)^2* and discloses nothing.
The question is now *What does `math.log(1000)` return?* and the back-matter
answer carries both conventions.

Four smaller ones:

- **A `\blank` whose answer was four lines above it.** Frame 45 stated *that
  distance is log10(2) of a decade* and then asked the reader to fill in *a
  doubling covers \blank of a decade*. Same frame, same page, nothing to cover.
  The stating clause is cut; frame 46's `ansblock` delivers it, as it already
  did. The other four `\blank` sites were checked and are sound.
- **"Reread the previous frame" pointed at the question.** In frame 25's
  answer: the previous frame is 24, the `\yourturn` that asked it. The
  correction is frames 20–21, and the pointer now names the section and the
  frames.
- **Two outcomes leant on their traps.** O2's *name the base every time you
  write a logarithm* is the frame-8/9 trap's moral, and O6 telegraphed the
  model-card frames. An outcome is read before the program; it may not carry a
  conclusion the program means to elicit.
- **A Polish calque.** *float32 poddaje się 44 tokenów w sekwencję 2000
  tokenów* is *gives up 44 tokens into a 2000-token sequence* carried word for
  word, and is not Polish. Now *poddaje się po 44 tokenach sekwencji liczącej
  2000 tokenów* — both digits stay in order, so C12 stayed green. *Na średnią
  długość nie wpływa*, which parses two ways, is now *Średnia nie zależy od
  długości*.

#### The two tooling holes, which outlast the program

**1. `figures/transcripts/` was outside every drift gate.** The `\transcript`
mechanism arrived with F3 and did not carry the guarantee the book makes for
computed numbers: the Makefile's `verify` target, `build.yml`, `pages.yml`,
`release.yml` and the `values` artefact were all scoped to `figures/values`
alone. Change `LOSS_NATS` in `code/f03_logarithms.py` and the transcript on the
page could disagree with every `\val{}` around it with nothing failing. It is
the sibling volume's fabricated-console-block defect with a build step in front
of it, **which is worse, because the file now looks generated**.

Fixed in all five places, behind a `$(COMPUTED)` variable so the next directory
a script writes has one place to be added. Proved both ways: a script change
that moves only the transcript is now reported STALE and names the file, and
the old scoping demonstrably saw nothing; an untracked transcript is reported
too. One latent instance was found while doing it — the transcript's own
comment carried `0.0907` as a literal, which is `P_TOKEN` written twice — and
is now interpolated, byte-identical output.

`\transcript` also had **no `\IfFileExists` guard**, where `\mermaidfig` has had
one since the diagrams pipeline was written. A clean checkout that has not run
`make numbers` died on `File not found`. Verified by deleting the transcript
and building: unguarded, `pdflatex` exits 1 on a Listings error; guarded, it
exits 0 and prints a marker where the transcript belongs.

**2. Frame-number payloads were compared between the editions and never
validated against the program.** `\teachesat`, `\teachesatone`, `\outcome` and
`\sumitem` are the whole of the book's return index — every Quiz route, every
outcome range, every Summary bracket — and F2 lost a review round to three of
them. A probe that routed a Quiz question to **frames 91–93 in a 48-frame
program** passed every gate in the repository, and *still* passes parity when
both editions carry it, because nothing diverges.

`check_structure.py --frames` now parses those payloads per program and fails
on an endpoint past the last teaching frame, a range that does not ascend, a
range starting before frame 1, and a payload that is not a frame range at all.
Proved by mutation, five faults, each introduced and restored: the 91–93 probe,
a backwards `\sumitem{45--43}`, an `\outcome{43--49}` one past the end, a
degenerate `{20--20}`, an en-dash typo `{10-11}` — and the same bad payload in
**both** editions, where the new check fails and `parity.py` exits 0.

This closes the *existence* half mechanically. **Whether frame 20 actually
answers the question routed to it stays a reading job**, and the tool says so
in its own comment rather than letting a green ledger imply otherwise.

#### The layout constant had drifted from its own evidence

`\begin{fr}`'s page-turn reservation was raised from five `\baselineskip` to
seven while F3 was written, and **the comment above it still carried the sweep
table that chose five**. A sweep table naming a constant the code no longer
uses is worse than no table: it reads as evidence. Re-swept over three programs
and all four builds:

| reserve | en | pl | en A4 | pl A4 | stranded openers |
|---|---|---|---|---|---|
| 4 | 250 | 256 | 231 | 231 | 2 |
| 5 | 252 | 256 | 229 | 231 | 1 |
| 6 | 250 | 254 | 229 | 231 | 1 |
| **7** | **248** | **256** | **229** | **231** | **0** |
| 8 | 250 | 256 | 231 | 231 | 1 |

This also explains a discrepancy worth not re-chasing: the review reported the
page table as 250/254/229/227, which is the reserve-6 row, not the shipped
one. **Page counts are a function of this constant**, so re-measure them from
the build in front of you rather than carrying a figure across a layout change
— which is the rule this file already states for the overfull multiset.

**Five was right for a one-program book and is wrong for a three-program one**,
which is the honest reading: the constant is tuned to what is written and has
now failed once. Seven is the only value in the range that clears all four
builds. Note that **eight strands a frame seven does not** — the guard turns
pages, so it reshuffles every later break, and neither page count nor stranding
count is monotonic in the reservation.

#### One residue, recorded rather than fixed

`\val{f03.seq.prod}` is `2.43e-2085` and the frame prints `10^{-2084.61}`
beside it; `10^-2084.61` is `2.45e-2085`, because the mantissa comes from the
unrounded logarithm and the exponent on the page is rounded to two decimals.
Both statements are true and the answer box says *About*, so this is rounding
display and not the reproducibility defect above — but it is the same shape,
and a reader who checks will find it. The choice is between quoting the
mantissa to fewer figures and not printing the rounded exponent beside it.
**Left as it is, deliberately, and written down so the next pass decides rather
than rediscovers.**

### Program F3, second review pass, August 2026

A third round of verifiers read F03 and disagreed with each other about one
thing. Most of what they reported had already been fixed by the first review
pass and was re-checked rather than re-fixed; what was left was two claims
nobody had run, one navigation error, one outcome that gave away its trap, a
disputed figure question that was settled by measuring, and a page-level defect
class the repository had no check for.

#### The book's only listing printed invalid Python

`figures/transcripts/f03-underflow.txt` is generated, committed, gated for
drift, and reproduces exactly in a real REPL. It still printed as
`struct.unpack(’<f’, struct.pack(’<f’, x))[0]` on page 101 of `main-en` --
U+2019 at both ends of a string literal, which is
`SyntaxError: invalid character (U+2019)`. The full trap is in *Build traps*;
the part worth repeating here is **how it hid**. `inconsolata` is loaded with
`varqu` precisely so that quotes come out upright, so any machine with
inconsolata renders it correctly. This container has neither inconsolata nor
newtx and is the container that builds the published PDF, so the defect existed
only in the artefact readers get.

That is the `amssymb`/`newtxmath` trap running backwards. There, a full TeX
Live failed where a bare one passed. Here, a bare one shipped a defect a full
one hides. **A preamble that probes for optional packages has two failure
directions and CI only exercises one of them.**

Fixed with `\usepackage{upquote}`, and verified the only way that means
anything: `pdftotext` the finished page, strip the `>>>` and `...` prompts, and
run what comes out. It prints 311 and 44, which are the two `\val{}`s beside it.

#### Two more claims about the toolchain, one of them false

`preamble.tex` said a bare `\log` is caught by `tools/check_notation.py`.
**There is no such file and there never was.** What exists is `parity.py`'s C10,
which names a file and a line before the build runs, and the `\PackageError`,
which fails the run. All of it was measured rather than reasoned about, by
putting a bare `\log` into F03 frame 1:

- `pdflatex` exits 1 **and writes a 244-page PDF over the top of the error**;
- `grep '^!' main.log` finds nothing, because `-file-line-error` puts a path
  first;
- `tools/checklog.py` reports `ERRORS: 1  Package mfabook Error: A bare \log`;
- `parity.py` reports
  `FAIL [C10-notation] programs/en/F03-logarithms.tex:100 a bare \log`.

So §F03-base's *the build refuses a bare mark* is true and matches Appendix B,
and the comment naming a non-existent checker is the thing that was wrong. The
five typeset `\mfalogplain` in F03 are the entry Quiz plus §2 (frames 8, 9 twice
and frame 13's aibox), which is what the file header, the notation box and
`preamble.tex` all now say -- as a rule, with no tally.

#### Every library claim in F03, re-run

Against Python 3.11.15 and numpy 2.4.6. All of them reproduce, so nothing here
needed changing; it is recorded so the next pass does not re-run them.

| Claim | What it printed |
|---|---|
| `math.log(1000)` | `6.907755278982137` |
| `math.log(0)`, `math.log(-8)` | `ValueError: math domain error` |
| `np.log(0.0)` | `-inf` + `RuntimeWarning: divide by zero encountered in log` |
| `np.log(-8.0)` | `nan` + `RuntimeWarning: invalid value encountered in log` |
| `math.exp(1000)` | `OverflowError: math range error` |
| `np.exp(1000.)` | `inf` + `RuntimeWarning: overflow encountered in exp` |
| `np.logaddexp(1000., 1001.)` | `1001.3132616875182` |
| `np.logspace(-5, -2, 4)` | prints `[1.e-05 1.e-04 1.e-03 1.e-02]`; element 0 is `9.999999999999999e-06` |
| `np.linspace(1e-5, 1e-2, 4)` | `[1e-05, 0.00334, 0.00667, 0.01]`, ratio of the top three `2.994` |

The last row is the one the first review pass rewrote: *within a factor of three
of one another* is `1e-2 / 3.34e-3 = 2.994`, so it is measured and it holds.

#### Navigation: one route and one bracket

- **Quiz Q14 routed to `47--48`.** Frame 47 states *a power law is a straight
  line on log-log axes and the gradient of the line is the exponent*, which is
  the whole answer; frame 48 is the learning-rate sweep and has nothing to do
  with it. Now `\teachesatone{47}` -- **the only `\teachesatone` in F03**, and
  it is right for the same reason F02 has none: F02's routes all point at a
  question answered in the next frame, and this one points at a frame that
  states its own answer.
- **`\sumitem{43--45}`** claims *a doubling is `log10 2` of a decade*, and the
  number arrives in frame 46's answer block; 45 only asks for it. Now `43--46`,
  which overlaps `46--48`. Overlap is established practice -- F01 has `34--36`
  followed by `36`.

All fourteen routes and all nineteen brackets were then re-read against the
frames. Nothing else misdirects.

**Outcome 7** promised *including where the midpoint between two ticks falls*,
which is the frame 43/44 trap named on the opener, forty pages before the
elicitation. The first review pass fixed exactly this shape in outcomes 2 and 6
and left this one. Now *including what a distance along one measures*, which
promises the skill and gives away no answer.

#### The disputed one, settled by measuring

Two verifiers disagreed about rule 2 -- *a figure must not answer the frame that
follows it*. One reported all three F03 figures clear in all four builds; the
other reported a figure sitting above the elicitation it shades in three of
four. **Both are describing something real, and the disagreement is that page
position is not the test.** Measured, page and vertical position, from
`pdftotext -bbox`:

| build | figure | fig | elicitation | answer |
|---|---|---|---|---|
| `main-en` | F3.1 log-mirror | p97 y169 | p97 y340 | p97 y544 |
| | F3.2 underflow | p103 y357 | p103 y503 | p104 y96 |
| | F3.3 log-axis | p110 y206 | p108 y186 | p108 y280 |
| `main-pl` | F3.1 | p102 y238 | p102 y400 | p103 y145 |
| | F3.2 | p109 y546 | p110 y135 | p110 y273 |
| | F3.3 | p116 y360 | p114 y370 | p114 y481 |
| `main-en-a4` | F3.1 | p84 y570 | p85 y168 | p85 y377 |
| | F3.2 | p90 y308 | p90 y454 | p90 y602 |
| | F3.3 | p95 y458 | p93 y705 | p94 y108 |
| `main-pl-a4` | F3.1 | p84 y639 | p85 y168 | p85 y377 |
| | F3.2 | p90 y310 | p90 y454 | p90 y600 |
| | F3.3 | p95 y529 | p93 y734 | p94 y158 |

So the second verifier's observation is right: **F3.1 and F3.2 both sit above
the elicitation that follows them, in all four builds.** And the first
verifier's conclusion is also right, because neither figure contains an answer
to the question below it:

- **F3.1** carries the product law and the index mirror. Frame 24 asks the
  reader to expand `ln(x^2 y / z)`, collapse `2 ln a + ln b - 3 ln c`, and
  simplify `ln(x+y)`. The figure gives none of the three, and it never writes a
  sum inside a logarithm, which is the trap.
- **F3.2** carries 44 and 311 tokens at `p = 0.0907`, both already printed in
  frames 32 and 33. Frame 35 asks for `p = 0.5`, whose answers are 150 and 1075.
- **F3.3** is the only one of the three that *does* contain an answer to a
  question put to the reader -- *halfway from 10 to 100 is 31.62, the geometric
  mean*, which is frame 43's elicitation -- and it is below frame 44's answer in
  all four builds: two pages later in the trade format, one page later on A4.

**The generalisable finding: page position does not settle rule 2, and neither
does source order.** A figure above an elicitation is fine when it answers
nothing; a figure below one is fatal when it answers it. Read what the figure
says, then check where it landed -- both, in that order, and in all four builds.
Nothing changed in F03 as a result of this; the measurement is the deliverable.

#### The orphaned cue: a defect class, and a new check

`main-en-a4` p94, `main-en-a4` p31 and `main-pl-a4` p45 each shipped as a
running head, the words *Next frame.* / *Kolejna ramka.*, and nothing else. The
question, its `\dotline` and everything else were on the page before. This is
`checkpdf.py`'s stranded opener seen in a mirror -- that check looks for a badge
with no body **below** it; this is a cue with no frame **above** it -- and the
tool now fails on both. A page of dots-plus-cue counts too, because it is the
same defect one breakpoint earlier.

**Four things were tried. Three did not work, and each is worth not repeating.**

1. **`\removelastskip` in `\nextframe`.** The obvious fix, and a no-op twice
   over. Plain `\vspace` in vertical mode is `\vskip#1 \vskip\z@skip`, so
   `\lastskip` reads the *zero* skip and the 2 pt one behind it is untouched;
   and `\removelastskip` is `\vskip-\lastskip`, which on the main vertical list
   cancels the space and leaves the breakpoint exactly where it was. Measured:
   page counts and the overfull multiset came back identical in all four builds
   and all three orphans survived.
2. **`\nobreak` on `\dotline`'s trailing `\vspace`.** Measured, and it makes it
   **worse: three orphaned cues became seven** -- `main-en` gained two,
   `main-en-a4` and `main-pl-a4` one each -- and `main-en` grew six pages. This
   independently reproduces the earlier pass's verdict on that experiment, with
   a number attached. Do not try it again.
3. **The `\begin{fr}` reservation.** Swept 4 to 10 against both checks; the
   table is in `preamble.tex` and is now two columns wide. Seven, eight and nine
   all clear both, and seven is the cheapest in pages. But the sweep clears the
   cue column by reshuffling breaks, not by fixing anything: **this guard
   reserves room for a frame OPENER and has nothing to say about a frame's
   tail.** Ten orphans two cues that nine does not.
4. **`\widowpenalty` and `\clubpenalty` at 10000**, added and measured in the
   F4 review pass because the defect looks like a widow and is not quite one.
   **Worse: 30 orphan tails against 26, and six pages added** across the four
   builds. Reverted. TeX is being asked to refuse a break it has no better
   alternative to, and it pays for the refusal somewhere else on the page.
5. **What worked: shorten the frames whose tails sat on the page boundary, and
   move one figure.** F01's `f01-magnitudes` -- the one figure in the book on the
   wrong side of the aspect-ratio crossover, height-bound at `0.42\textheight`
   and therefore unable to share a page with the frames around it -- moved from
   between frames 31 and 32 to the end of §F1.5, after frame 33. It no longer
   crowds frame 32's tail, it summarises the section instead of pre-empting it,
   and it answers nothing in frame 34 (which asks for bytes; the ladder has
   none). Three frames then lost a line each in both editions: F01 frame 32, F02
   frame 5 and F03 frame 43.

**The cost of getting it wrong is that trimming is a random walk.** One source,
four paginations: a cut that pulls the cue back onto the page in `main-en-a4`
pushes a different frame over the edge in `main-pl-a4`. Measured twice, in both
directions -- round one went three orphans to three orphans in different places
and cost `main-pl-a4` two pages. **Fix them in document order, F01 before F02
before F03, and rebuild all four after every edit**; a trim in F03 cannot move
F01, but the reverse is not true.

The class will recur. The three written programs carry 102 cue sites, so across
four builds there are 408 chances for a frame tail to land within a line of the
page bottom; a handful of orphans is the expected steady state, and every future
program re-rolls every one of them.
`checkpdf.py` is what makes that survivable; the fix is always editorial.

#### Also done in this pass

- The `f01-magnitudes` move is the first time a figure has been relocated for
  layout rather than for rule 2. It carries no `\ref{}` anywhere, and it is
  still F1.2 because it stayed between `f01-number-sets` and `f01-prefixes`.
- Verified rather than re-fixed, because the first review pass had already
  corrected them: the notation box's claim about the build, the *within a factor
  of three* sentence, *a ratio in the thousands*, `f03-log-axis.mmd`'s A1 node,
  and frame 25's pointer at *the trap at the end of §F3.3, frames 20 and 21*.
  Each was re-read against the source it describes.

### Program F4 pass, August 2026

**Forty-two teaching frames, forty-four printed, both editions**, against a
plan that projected forty-two and a manifest estimate of forty. The plan was
right about the mathematics and about the section list; what it got wrong was
three placements, and all three were forced by the same tool.

**`check_structure.py`'s `RE_DEMANDS` is a design constraint, not a lint.** It
treats `\blank`, `\dotline`, `\yourturn` and `\nextframe` alike: *any* frame
containing one of them must be followed by a frame that opens with an answer.
The plan put a `\blank` in three frames that then closed a teaching beat, which
is unbuildable. Each was restructured to end by asking, and the section
boundaries did not move. **Read that regex before planning where the gaps go**;
it is cheaper than rewriting three frames.

**The debt F3 left is paid, and it is narrower than both the brief and the
first draft of this note said.** F03 prints `ln p(sequence) = sum_i ln p(token
i | ...)` and then divides by the token count, having never defined that
sigma. **The subscript is not part of the debt.** F02 introduces it in as many
words — *a subscript is nearly always an index: x_i is the i-th input* — uses
it twice more, and hands the sigma itself forward by name. What stood here
instead was that *no subscripted variable is introduced anywhere in F01, F02
or F03*: a statement of non-occurrence, which is the class the rule above
forbids outright because nothing can check it, and it was false in the one
file it would have taken one grep to open. It had reached both F04 file
headers as well. §F4.4 opens by naming F03's sentence, writes
it as `L = -(1/n) sum ln p_i`, and quotes `\val{f03.seq.tokens}` and
`\val{f02.loss.nats}` rather than new keys, so the three programs are provably
quoting one computation. F03 does the same thing back at F01 and F02; naming
the instances is the point, and counting them is the thing this file keeps
telling itself not to do.

**Two firsts, both deliberate.** F4 is the first program to use
`\begin{python}` — four three-line loops, because "a sigma is a loop" is the
whole argument and a picture of the loop is not the same as the loop. It
renders correctly inside `fr`, and the listing extracted from the finished PDF
runs. And §F4.6 carries the book's **first `rigourbox`**, for the convergence
of the geometric series: the limit is stated, attributed to a first analysis
course and not proved. Both were open questions in the plan and both are now
settled by having been done.

**One manifest amendment, on the F03 precedent.** Frame 28's aibox wanted to
say that a cross-entropy averaged per micro-batch and then averaged again is
not the mean over the accumulated batch — item 25 of the trap catalogue, and a
real production defect. **No brief undertook it**: P20's covers AdamW and
schedules, P21's covers minibatch noise and clipping, and neither mentioned the
denominator. A clause was added to **P21**'s brief in `tools/programs.json` and
the stubs regenerated, so the forward pointer now names a program that has
promised to deliver it.

**And some of the trap catalogue's program numbers are one low.**
`notes/02-grounding-and-traps.md` §3 was written before P7 was inserted, so its
optimisation section heads "(P18–P21)" where the manifest says P19–P22 and its
probability section "(P22–P27)" where the manifest says P23–P28. It now carries
a warning to that effect at the top of §3. **Never copy an owner out of that
file**; re-derive it from `tools/programs.json`. Five entries were added there
for F4's traps, and item 41's own tally — "the third instance in three
programs" — was replaced by the rule, because F4 made it four.

**Two things the script found that the frames may not say**, both recorded in
`code/f04_sums.py` at their computation:

- **Bias correction is exact in the algebra and not to the bit.** On a constant
  sequence the corrected EMA is 1 in exact arithmetic; measured, the worst
  `|mhat - 1|` over t = 1..5 at both betas is 1.4e-14, and at beta = 0.999,
  t = 2 it prints `1.0000000000000142`. The script asserts a tolerance and
  prints the worst error on every run; frame 40 says *exactly right in the
  algebra* and then says what binary64 does. This is F03's `np.logspace` defect
  caught before it shipped.
- **`np.array([]).mean()` emits two RuntimeWarnings, not one** — `Mean of empty
  slice` and `invalid value encountered in scalar divide`. A frame quoting "the
  RuntimeWarning" would already have been wrong. The warning frame states only
  the invariant (one library stops, the other returns `nan` and carries on) and
  says in as many words that the wording is a property of the installed
  version.

**A `\blank` inside an `ansblock` is not established practice, and the one draft
instance was a defect.** Frame 26 opened with `\frac{\blank}{\blank} =
\frac{91}{110} = 0.8273`, so the gap was answered on its own line. The gap
belongs in a frame that then gets answered, never in the block that answers it.
Removed. **Two more were removed in the review pass for the wider version of
the same rule** — a gap whose answer is printed in the same frame, above it —
so do not carry a tally of them here; grep for `\blank` and read each one
against its own frame.

**Two page-level defects, both found only on the finished page.**

- **An 11.2 pt overfull hbox in `main-en-a4` alone**, from
  `\code{for c, p in zip(counts, prices): total = total + c * p}` run into a
  test-exercise sentence. `\code{}` does not hyphenate and TeX preferred the
  overfull line to a very loose one. Set as a displayed three-line block, and
  the multiset came back to the pre-F4 baseline in all four builds.
- **An orphaned cue on `main-en` p139**, and it took two trims of frame 26 to
  clear it: the first merged a paragraph and moved the cue but did not pull it
  back, the second tightened the throughput sentences. As CLAUDE.md already
  says, trimming is a random walk across four paginations — but F4 is the last
  program *written*, so a trim inside it cannot move F01 to F03, which made it
  a cheap walk. It is not the last program in the book, and a note that says
  so will stop being true the day F05 is drafted.

**The three diagrams, measured on the page** against the width formula, in the
trade format:

| | W (en / pl) | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|
| F4.1 sigma-as-loop | 507 / 524 | 8.68 | 8.40 | 9.88 | 9.56 |
| F4.2 two-averages | 558 / 579 | 7.89 | 7.60 | 8.98 | 8.65 |
| F4.3 ema-weights | 510 / 565 | 8.63 | 7.79 | 9.82 | 8.87 |

Predicted and measured agree to a hundredth in all twelve cells. The first cut
of F4.2 was 447 pt wide and set its node text at **9.87 pt in the trade format
and 11.21 on A4**, which would have been the largest in the book by a margin —
so the fix was to make the nodes *wordier*, which is the opposite of the
instinct. Width is the only quantity that matters above the aspect-ratio
crossover.

**Rule 2 was checked by reading the figures first and then finding them in all
four builds**, as the F03 second review pass prescribes. F4.1 shares a page
with frame 12's question in `main-pl-a4`, F4.2 with frame 29's in both A4
builds, and F4.3 with frame 39's in three of the four. F4.1 carries no product and F4.2 carries no sequence.

> **F4.3 was wrong and the reasoning above it was wrong**, and the review pass
> caught it. The node read *newest value 0.10*, which is frame 39's answer at
> beta = 0.9 by a different route, and it was left on the argument that frame
> 38 prints that weight in its own answer box **directly above the figure**.
> That is true in three builds and **false in `main-pl`**, where frame 38's
> answer is on the previous page and the figure is the only place on the page
> the number appears. A justification that depends on where a page happens to
> break is not a justification — the same rule this file already states for
> *before you turn over*. The ladder now starts at 0.09 and node B keeps the
> newest weight derivable. Re-checked on the page in all four builds.

### Program F4 review pass, August 2026

Three verifiers read the program and the rendered pages. Between them they
found six false claims, seven places where an answer was printed before its
question, one layout defect that turned out to be pervasive across the whole
book, and four smaller things. As in the F3 pass, **every one of them was
invisible to every gate in the repository**, and the most expensive class was
again the book being wrong about the book.

#### The book was wrong about the book, and it had reached this file

Both F04 file headers and this document asserted that F03's sigma used notation
the reader had not been given, because **no subscripted variable is introduced
anywhere in F01, F02 or F03**. F02 introduces it in as many words at its
notation box, uses it again for the constant-factor rule and again for the
softmax. The claim was a **statement of non-occurrence**, which is exactly the
class this file's *Non-negotiable conventions* forbid — nothing can check it,
and a tally decays silently — and it had propagated into the binding document
the next author reads first. Deleted from all three places.

The debt F03 leaves is real and narrower: it wrote the sum **with a sigma it
never defined**, and F02 hands that sigma forward by name (*Program F4 reads a
sum as a loop*). Frame 17 said F03 *ended a section with a sentence it did not
have the notation to write*; F03 line 846 writes it, with a `\sum`. It now says
what is true. Frame 1 no longer presents the subscript as new either — it names
F02 as where the reader met it.

**The generalisable rule, and it is the third pass running that has paid for
it: before writing a sentence about another program, open that program.** A
statement about what a file does not contain is one grep away from being
checked and one draft away from being folklore.

#### The other five false claims

- **A bolded claim about how a real optimiser is implemented.** The frame said
  momentum *is this recurrence* — the `(1 - beta)` form. Common implementations
  drop the `(1 - beta)` and fold it into the learning rate. Verified against a
  real optimiser's own documentation rather than from memory: `optax` ships
  **both** transforms and its docstrings for `trace` and `ema` say so in one
  sentence — *`trace = decay * trace + t`, while `ema = decay * ema +
  (1-decay) * t`. Both are frequently found in the optimization literature* —
  and `optax.sgd`'s momentum is the first of the two. **No library is named on
  the page**, deliberately and for the reason this program already gives about
  numpy's warning text: a library's internals are a fact about a version. What
  the page carries is the mathematics, which is checkable by the reader — the
  two forms differ by exactly `1/(1-beta)`, so they give the same direction and
  a different length, and a constant factor on a step is indistinguishable from
  a change of step size. The consequence a reader can act on (a step size does
  not travel between the two forms) is handed to **P20**, and a clause was
  added to P20's brief in `tools/programs.json` so the forward pointer names a
  program that has promised to deliver it. The matching further-problem answer
  was fixed too.
- **A forward pointer to a worked example nobody had promised.** *Program P3
  prices this in FLOPs rather than in pairs* pointed at the causal mask; P03's
  brief never mentions attention, and the transformer count was deliberately
  moved out of P03 to P32 by the curriculum review. Softened to *prices work in
  FLOPs rather than counting pairs*, which is what P03 does undertake. Adding
  the clause to P03's brief was the other option and was rejected: it would
  have re-inflated a brief that a review had just trimmed for exactly this
  reason.
- **A ratio that did not reproduce from the two numbers printed beside it.**
  The frame prints `(0.9)^50 = 0.005154` and `(1.1)^50 = 117.39` and then said
  the two were about **22 778** apart. Divide what is on the page and you get
  22 776. The exact ratio is 22 777.6, so five figures was a precision the page
  could not support — the same shape as F03's mantissa taken from an unrounded
  logarithm. `f04.decay.ratio` is now emitted at **three significant figures**,
  22 800, and `code/f04_sums.py` asserts that dividing the two rounded products
  gives the same figure, so the page cannot stop reproducing quietly.
- **An arithmetic nit that had been read twice and never worked.** *With
  `c = 5` the second gives `5 + 10 = 15` whichever way round you do it* — the
  right-hand route is `5 x 3`. Both routes are now written out.
- **`\lblCanYouFooter`, which prints at the end of every program in the book,**
  told the reader to take the Quiz a second time and called the difference *the
  only honest measure of what this program did for you*. This file records that
  the Quiz cannot serve as entry and exit test, because the same items serve
  both, and that the instrument is the scored Test exercises. The footer now
  says so, in both languages. It was out of F4's scope and it was printing 47
  times.

#### Seven spoilers: an answer printed before its question

The pattern is one rule with seven instances, and two of them were in generated
files, which is the part worth remembering: **a figure and a transcript are
under the same rule as a frame, and neither is reviewed as prose.**

1. **The transcript answered a question in the frame it sits in.** It ended
   `>>> math.factorial(0)` / `1`, and the frame closes by asking *So what is
   0!?* — four lines below the answer, on the same page, where no pagination
   could separate them. The script's own comment already stated the rule and
   kept `0.0/0.0` out for it. Removed; `ZERO_FACTORIAL` is still computed and
   still asserted, and the further problem still asks for `0!` by two routes.
2. **Figure F4.3 printed `0.10`** — see the correction under *Program F4 pass*
   above.
3. **Frame 8's `\blank` was answered by frame 8's own `\ans` box**, which opens
   the frame with `n + 1`. The third row now prints `n + 1`; the middle row is
   the only gap.
4. **Frame 19's `\blank` was answered three lines above it**, by the answer
   block at the top of the same frame. The cell is filled; the frame's numeric
   question already carries the retrieval.
5. **Two outcomes carried the conclusion their traps elicit**, printed on the
   opener some twenty pages early: *and when it is not* gives away the
   average-of-averages trap, and *correct the bias its initialisation
   introduces* gives away section 7's. **F3's review pass fixed the same shape
   twice and it came back.** An outcome promises a skill; it may not carry a
   finding.
6. **Quiz Q14 asked *and what is the one-line fix?***, which tells the reader
   before frame 1 that the reading is wrong. The clause is gone, and so is the
   fix from its back-matter answer: the Quiz is a triage instrument, not a
   teaching one, and F03's review pass had already had to make this cut once.
7. **Outcome 1--6 promised a skill no frame taught** — *read a sigma aloud*.
   `\canyou` replays the outcomes, so the reader was being asked to rate
   themselves on something the program never showed. Frame 1 now gives the
   spoken form in one clause.

#### The layout defect was pervasive, and nothing had ever looked for it

`\begin{fr}` measures the room left and turns the page when a frame will not
fit. A `\section` immediately before it has already been typeset by then, so
**the heading stays behind and its whole section begins overleaf**. §F4.7 was
alone on a page in three of the four builds — and when a check was written for
it, it found **10, 14, 9 and 9** headings left behind, in every program from F1
to F4. No error, no warning, no overfull box; forty-two instances of a defect
in a book that had been through five review passes.

- `\section` now carries the same room test `\begin{fr}` has, sized for the
  heading and its spacing as well (`\mfa@sectionroom`, `\mfasectionreserve`).
  Only numbered sections: `\section*` is the Quiz, *Can you?*, the manifests
  and the front matter, none of which is followed by a frame.
- The constant was **swept against the check over all four builds**, and the
  table is in `preamble.tex` beside it. Nine leaves three headings stranded and
  ten leaves one; eleven, twelve and thirteen leave none; **sixteen strands
  none and puts an orphan tail back in two builds while taking one out of a
  third**, which is the non-monotonicity this file already records for the
  frame reservation. Twelve is the choice.
- `tools/checkpdf.py` gained the check, and it was **verified to fire on F02's
  own instances before the guard was written** — F2.7 in `main-pl` and
  `main-pl-a4`, F2.8 in `main-en-a4` — which is the only way to know a new
  check is looking at anything.

Two mechanics worth keeping. The heading is **not** simply taller than the
body: `\Large` bold measures 12.6 pt against the body's 14.2 pt in the trade
format, because `pdftotext` reports the font's own box and the two fonts have
different depths. So the tool **learns** the heading size from the document
instead of assuming it, the way it already learns the cue string and the text
block. And the text block had to be measured **per page parity**: the margins
are mirrored, so one mode over the whole document describes the recto and is
11 pt wrong about the verso.

#### The orphan tail: a check that reports and does not gate

`checkpdf` also gained the fill-fraction check the second half of the layout
work asked for: a body page whose ink stops in its top quarter, which is the
orphaned cue's defect one line less extreme and therefore invisible to the cue
test. Part pages, chapter openers, blank versos and the last page of a chapter
are excluded — on that last one there is nothing below to pull back, and the
index's and the manifests' final pages are short by construction.

The floor was swept and **the interesting result is that it is a plateau**:
every page the check names carries between 7 and 10 per cent of a block, and
the next page up the distribution is at 50. Anywhere between a tenth and a half
names the same set. A quarter is the middle of the gap and is about ten lines.

**It reports and it does not fail the build, and that is a deliberate
divergence from what was asked.** Two of its own cues cleared editorially and
one of F4's tail pages with them; of the fifteen that remain, thirteen are in
F1, F2 and F3. Clearing those means cutting a sentence of reviewed prose out of
three programs in two languages to move one line on one of four paginations,
with every later break in that language reshuffled by each cut — and a line is
about 180 characters on A4 against the fifty of genuine slack those frames
turned out to hold. A gate that is red on something nobody can responsibly
clear teaches the next person to stop reading the output, so the count is
printed in full on every run and carried as a ledger at the top of this file
instead. **That is the same treatment the 80/80 standard gets, for the same
reason.** If a later pass finds the structural fix — the tail of a frame should
be incapable of standing alone — it retires both this ledger and the cue's.

#### Three smaller things

- **An aibox that named no system.** Frame 34's was a generic depth mechanism
  plus a forward pointer to F12. Demoted to prose, which is what the aibox rule
  says to do and which also returned the lines the section guard needed.
- **Polish.** *Zestaw* was doing three jobs and collided with *zbiór* two lines
  apart, both reading as *evaluation set*; the harness is now *harness*,
  inflected Polish, on this file's own rule about English ML terms. And
  *przeżywa więcej starej wartości* is a calque — transitive *przeżywać* is *to
  live through* — now *zostaje więcej starej wartości*.
- **This file said F4 was the last program in the book.** It is the last one
  *written*. The reasoning that rested on it (a trim inside F4 cannot move F01)
  holds; the sentence stops being true the day F05 is drafted — **and F05 is
  now drafted, so it is F5 that a trim cannot propagate out of.** The rule is
  the general one: a trim can only move breaks *after* itself, so fix orphans
  in document order and rebuild all four after every edit.

#### One thing found and deliberately not fixed

**A blank verso carries a running head.** `main-en-a4` p102 has *88 · Program
F3* at the top and nothing else on it: the page `\cleardoublepage` inserts is
blank in the body only. It is a real typographic defect and it is one line of
preamble to fix, and it was left alone because it is nothing to do with F4 and
because it moves no page. `checkpdf`'s chapter-final test had to be written
around it — a page with nothing but a head is what has to be skipped, not a
page with nothing at all — so the next person will meet it there.

### Program F5 pass, August 2026

**Forty-seven teaching frames, forty-nine printed, both editions**, against a
brief that projected forty-five. Seven sections: what a function is, the graph,
the four moves, weight and bias, composition, inverses, and the order a
strictly increasing function keeps. The payoff is the last section's and it is
why the program sits in the Foundation part: **a strictly increasing function
keeps the order of a list, so it cannot move the argmax**, and therefore
temperature cannot change which token is most likely -- only how often the
others get drawn instead.

**The script's own assertion caught a fabricated number before the prose was
written, and that is the finding worth keeping.** `code/f05_functions.py`'s
module docstring said the top probability ran "from 0.1749 to 0.7112 over the
range used here", written from expectation rather than from output; the
assertion two hundred lines below it (`TOP_HI / TOP_LO > 3.0`) failed on the
first run. The real range is 0.7042 down to 0.4042, a factor of 1.74.

This is the first time a guard in this repository has caught a plausible
number *in the same commit that invented it*, and the reason it worked is
ordering: **write the assertion at the computation, before writing the
sentence the computation is for.** The docstring is now the corrected figure
and the assertion is an invariant rather than a threshold -- the maximum of a
softmax falls monotonically in T and the minimum rises, which survives a
change of logits, where `> 3.0` would not have.

#### The tail did not reproduce from the page, which is F4's defect in new digits

The striking figure here is not the top of the distribution but the bottom:
over T from 0.5 to 2.0 the most likely token falls by a factor of 1.74 while
the least likely rises by 51.7. The page printed 51.7 beside a table whose tail
entries are 0.0017 and 0.0902 -- **and those divide to 53.1**, because the
smaller of them carries two significant figures at four decimal places.

That is exactly F4's `22 778` against a page that divides to `22 776`, and it
had to be caught the same way: by dividing what is actually printed. The fix is
not more decimals in one row of an otherwise uniform table. The page now states
a **bound** -- *more than fiftyfold* -- and `code/f05_functions.py` asserts
that the exact ratio and the ratio of the rounded printed values both clear it.
The top ratio is left as a figure, with an assertion that it *does* reproduce
from the rounded table, because that is the property the tail turned out not to
have.

**The rule: before quoting a ratio, divide the two numbers as the page prints
them.** If the answer differs, the page cannot support that precision.

#### Two tables that could not fit, and the fix is transposition

The first build added an overfull hbox of **195.8 pt** and another of
**79.5 pt** -- by a wide margin the largest this book has produced, against a
15 pt budget. Measured with `\sbox`, the logistic table was **565.7 pt** wide
and the softmax table **449.4 pt**, against a 350.9 pt measure.

**A `\val{}` numeric column costs about 70 pt**, so eight of them do not fit
and no amount of rewording will make them. Both tables were transposed, and
the softmax one reads better transposed than it did before: with the
temperatures across the top, the reader scans *down* each column and finds the
top row largest every time, which is the invariance the section is about. The
multiset came back to the pre-F5 baseline in all four builds.

#### Five claims a reader could have falsified

Found by re-reading against the sources rather than by any gate, and two of
them are the book being wrong about the book:

- **"$x > 0$, which Program F03 spent a section on."** F03 has seven sections
  and none of them is about the domain. It is settled in two frames inside
  *What a logarithm is*. Now *and Program F03 says why*. Third pass running
  that this file's rule has been paid for: **open the program before writing a
  sentence about it.**
- **"At $w = 5$ the curve does all its work in a window under one unit wide,
  and outside that window it is flat to three decimal places."** The first
  clause is measured; the second is false, and not marginally. Outside the
  0.1-to-0.9 band the curve still has a tenth of its range to cover at each
  end, and at $w = 5$ it needs nearly another whole unit of $x$ to come within
  0.001 of its limit. The false clause is gone and the measured one stands
  alone.
- **"The best such line has slope 2.4286."** *Best* is not defined until the
  criterion is named, and least squares and minimax give different answers.
  Now *the least-squares line of that form*.
- **"It appears in every binary cross-entropy."** A universal claim about a
  composition that holds when the input is a logit, which is the usual case and
  not all of them. Narrowed to what is true.
- **The trap catalogue routed the threshold trap to P19**, which is *Convexity
  and Jensen's inequality*. No program in the manifest undertakes parametrising
  a unit by its threshold, and the entry now says so rather than naming one.

#### CLAUDE.md's own tally of the trap catalogue had drifted by five

This file said the catalogue held **41** misconceptions. The catalogue's own
heading said **46**. Neither is now stated anywhere: the heading names the list
and the Foundation section names *which program produced which entry* -- item
41 out of F3, 42 to 46 out of F4, 47 and 48 out of F5 -- which is checkable and
does not decay.

The rule this file already carried is *never state a count of occurrences*, and
the document stating it was carrying two counts that had come apart. **A rule
written in a file does not audit that file.**

#### Exact in the algebra, and not to the bit

The argmax result is stated as exact, and it is: dividing by a positive $T$ and
exponentiating are both strictly increasing, and the final division is by one
positive total. A random search over **200,000 vectors** of two to eight
entries at seven temperatures found no counterexample.

But push $T$ high enough and every entry becomes the same float -- measured, at
$T = 10^{6}$ on a vector spanning 3.0 -- and the comparison has nothing left to
compare. The frame says so, in one clause, exactly as F4 says the bias
correction is exact in the algebra and 1.4e-14 in binary64. **A result that is
exact mathematically still owes the reader a sentence about the arithmetic.**

#### The diagrams, and the crossover caught in the act

`f05-four-moves` first rendered at 515 x 344, an aspect ratio of **1.50**,
against a crossover of 1.53 in the trade format. That is the hazard this file
records for `f01-magnitudes` and it was caught before it shipped: below the
crossover the height cap binds and the figure cannot share a page with the
frames it belongs to. Flattening the tree from three ranks into two rows of
three took it to 2.65. And `f05-one-output` first came out 492 pt wide, which
would have set **10.18 pt** on A4 -- the largest node text in the book -- so its
nodes were made wordier, which is again the opposite of the instinct.

| | W (en / pl) | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|
| F5.1 one-output | 492 / 538 | 8.97 | 8.20 | 10.18 | 9.31 |
| F5.2 four-moves | 527 / 508 | 8.37 | 8.68 | 9.50 | 9.86 |
| F5.3 order-kept | 555 / 544 | 7.95 | 8.11 | 9.02 | 9.20 |

**Rule 2 was checked by reading each figure first and then finding it in all
four builds**, as the F03 second review pass prescribes. All three figures
contain an answer to something the program asks -- F5.1 the non-function, F5.2
the shift direction, F5.3 the argmax -- and all three sit **after** the frame
that delivers it, by two to five pages in every build:

| | F5.1 / its answer | F5.2 / its answer | F5.3 / its answer |
|---|---|---|---|
| `main-en` | 159 / 156 | 167 / 164 | 181 / 178 |
| `main-pl` | 165 / — | 175 / 170 | 187 / 185 |
| `main-en-a4` | 140 / 137 | 149 / 145 | 160 / 158 |
| `main-pl-a4` | 142 / — | 150 / 147 | 161 / 159 |

That is sound by construction as well as by measurement: a float cannot rise
above the page its declaration point falls on, and every one of these is
declared at the end of the section that corrects the thing it draws.

#### The orphan-tail ledger took its largest jump, and one cue was a hard gate

`main-pl-a4` shipped a page carrying the words *Kolejna ramka.* and nothing
else -- the tail of frame 42, the temperature elicitation, one line past the
boundary. That is the **hard** half of `checkpdf` locally and it was cleared
editorially: frame 42 lost a clause in both editions (the instruction was
tightened in English too, so the two editions still say the same thing), and
`main-pl-a4` lost two pages with it. No digit changed, so C12 stayed green.

The orphan tails went **15 to 26**. All eleven added are F5's, and none is
clearable without the random walk this file already describes. It is the
reported ledger and it is going the wrong way; the structural fix -- a frame's
tail should be incapable of standing alone -- is still open, and the two
candidates measured so far (a penalty on `\dotline`, and widow/club penalties
at 10000) both made it worse.

### Stroud layout pass, August 2026

The seven structural elements of the original's page, applied from photographed
reference (`notes/07-stroud-original-layout.md`) rather than from memory: the
margin frame badge, the answer box and its next-frame cue, the outcomes panel's
checkboxes, the Quiz's route boxes, the Summary and Test exercises as named
frames, the opener's frame range and the mirrored running heads, and the
tooling that gates all of it.

**Everything but the cue is free.** The badge, the checkboxes, the route boxes,
the named frames and the frame range together moved no page and added no
overfull box in any of the four formats. The 33 next-frame cues cost two pages
per format. That is worth knowing before the remaining 46 programs are written,
because it is the one element whose cost scales.

**Four things the layout could not have been got right by reading about them.**

1. *A margin badge "would overflow a 17 cm page".* It does not — the whole
   claim rested on `\marginparwidth` being left at the class default of 116 pt
   inside a 51.2 pt margin. Declared per format and asserted at
   `\begin{document}`, a two-digit badge leaves 24.6 pt of clear paper in the
   trade format and 51.2 pt on A4.
2. *`halign=center` on the answer box was stretching the maths by 16%* —
   237.68 pt against 204.20 pt on one measured line, in the shipped PDF, not in
   a scratch file. `flush center` cannot stretch, so an over-wide answer now
   overflows visibly and `checklog.py` catches it.
3. *The checkbox derived on paper sat 0.7 pt low*, because `\fbox` leaves the
   finished box a depth of exactly `\fboxrule`. A constant 0.7 pt inside an
   ex-based design is a different fraction of the x-height in each of the two
   formats. Measured with `\sbox`, as the frame badge already was.
4. *The Quiz box broke 3 + 9 across a page in BOTH A4 builds*, leaving nine
   questions and a column of boxed numbers under nothing that said they were
   frames. `lines before break=12` was measured, not guessed: 8 fixes one A4
   edition and not the other.

**And one the tooling could not see.** `\nextframe` was invisible to C4 *until
it was added to `parity.py`'s `BARE` table* — before that the ordered signature
compared byte-identical with 33 cues inserted. The `BARE` entry is what makes a
one-edition move visible, and it was verified by mutation: moving a cue between
frames in one edition, or deleting one from the Polish file alone, now fails on
two or three checks at once and names the token index. Do not trim it.

A cue dropped from **both** editions at once stays invisible to C4 and to C14
alike, because nothing diverges. C16 exists for that, and it is written against the *mechanical* rule — a frame carries the cue
if and only if the next frame opens with an answer — so the cues were inserted
by script in both editions from the same derivation rather than by hand twice.

**The frame range counts 47, not 45.** The Summary and the Test exercises are
printed frames, so an opener reading `Frames 1 to 45` would contradict two
frames the reader can see. The ledgers still count 45 because they count
teaching frames; that divergence is deliberate and is now written into both
tools rather than left to be rediscovered.

**Dead code removed:** `\framelabelfix`, defined and never called. The theory it
rested on — that `\theHframeno` is undefined so frame anchors restart in every
program — is false: `\newcounter{frameno}[chapter]` gives hyperref a parent and
the `.aux` is byte-identical with and without it. It was deleted rather than
wired in, which is what the reviewer who measured it recommended.

### The evidence, honestly

Stroud's programs were validated **above 80/80** before publication. This book
has not been read by anybody and may not borrow that.

**And the general evidence for programmed instruction is adverse.** Kulik, Cohen
and Ebeling's 1982 meta-analysis found the format did not typically raise
achievement in secondary education, and that small steps, linear sequencing and
immediate reinforcement were not what mattered. Both editions' front matter says
so, in a warning box, rather than leaving it out.

The defence this book actually makes is narrower and better supported:
**retrieval practice** (with study time held constant, being made to recall beats
rereading, and the advantage appears at two days and a week rather than
immediately) and **errorful generation** (eliciting a wrong answer and then
correcting it beats studying without the error, with the benefit largest exactly
when the learner was confident). The frame and the trap are for those two
findings, and for nothing else.

The consequence for the reader is stated in the front matter and should not be
softened: **the method feels worse than reading while you are doing it.** Readers
rate the method they retain less from as the more effective one. A reader who
abandons the book for feeling inefficient is abandoning it for the reason it
works.

---

## Structure

Nine parts, thirteen Foundation programs and thirty-four main programs.
The full reasoning, with each program's argument, its AI payoff, its frame
estimate and the dependency graph, is `notes/01-curriculum.md`.

| Part | Programs |
|---|---|
| I — Foundation / Podstawy | F1–F13 · assumes nothing, triaged by Quiz |
| II — Number, precision and cost | P1–P3 · before the linear algebra, deliberately |
| III — Linear algebra | P4–P11 · the largest part |
| IV — Discrete structures and argument | P12–P14 |
| V — Calculus and automatic differentiation | P15–P18 |
| VI — Optimisation | P19–P22 |
| VII — Probability and statistics | P23–P28 · past the normal distribution, to inference and Bayes |
| VIII — Information theory | P29–P31 |
| IX — Assembling it | P32–P34 · no new mathematics |

**Each program's brief lives in its own file**, inside the `\programstub{}`
block: what it must argue and what it must buy the reader. That is deliberate —
the brief sits next to the work, prints in the draft PDF so nobody mistakes a
stub for a program, and disappears the moment the program is written. Writing a
program means deleting the stub. If the brief turns out to be wrong once the
mathematics has been worked, change it and record the contradiction here.

**Forward prerequisites, all declared rather than discovered.** An adversarial
review of the curriculum found four and a later pass found a fifth, and the rule
is now that each is stated in the owning program's Learning outcomes with a
pointer:

- **P21** (stochastic optimisation) needs random variables and variance from
  **P24–P25**, two parts later. P25 revisits minibatch noise once the machinery
  exists.
- **P10** and **P11** use the covariance matrix, defined in **P24**. They need
  two facts from it — symmetric, positive semi-definite — and say so.
- **P18** (matrix calculus) carries the book's most reused derivation, the
  softmax–cross-entropy gradient, and cross-entropy is not defined until
  **P30**. P18 gives it a definitional frame; P26 and P30 each return to it.
- **P22** (constrained optimisation) states its whole payoff in terms of a
  **KL-penalised objective** — the multiplier as the price of a constraint, and
  the equivalence of a hard KL constraint with a KL penalty — and KL is not
  defined until **P30**. This one the review missed; it was found by building the
  dependency graph in `tools/programs.json` and checking every edge against the
  declared list. Either declare the one fact it needs, as P18 does, or carry the
  payoff with a plain quadratic penalty and have P30 return to it. **The author's
  call, but it may not be left undeclared** — the brief now says so.

Anything else is a dependency error, not a forward reference. **The graph is now
machine-checkable:** every program in `tools/programs.json` carries `deps`, so a
forward edge that is not on this list is findable in one pass rather than by
reading forty-seven briefs. That is how the fifth was found, and it is worth
re-running after any curriculum change.

### Changes the curriculum review forced, August 2026

An adversarial pass over `notes/01-curriculum.md` rejected it as it stood, and
five of its findings are now in the manifest:

1. **A program on tensors, shapes and index notation was missing** — the
   largest content gap in the book, and in every book in its own competitive
   survey. The audience manipulates rank-4 arrays daily and has only ever been
   taught rank-2 notation, which is where the shape errors come from. It is now
   **P7**, between *Matrices as linear maps* and *Rank*, and everything after it
   moved up one.
2. **F13 was curriculum inertia.** Forty-five frames on the integral, in a book
   whose own scope statement excludes every integration technique. Cut to
   twenty and retitled *Accumulation, area and expectation* — it exists to make
   an expectation an integral and a density integrate to one, and for nothing
   else.
3. **P3 asked the reader to count the parameters of a transformer block** three
   parts before any program had said what a matrix is. The count moved to P32;
   P3 keeps magnitude and cost, which need only arithmetic and sigma notation.
4. **Nothing explained why a training run diverges at initialisation.** No
   variance propagation, no fan-in argument, no He or Xavier. Added to P25,
   where it belongs, because it is a variance argument.
5. **Part I's contract was false.** *Assumes genuinely nothing* is contradicted
   by every Foundation payoff sentence, F1's included: it has the reader compute
   what a seven-billion-parameter model weighs and does not stop to say what a
   parameter is. Both introductions now separate the two floors — no mathematics
   beyond school arithmetic, but the vocabulary of the job assumed throughout —
   and say plainly that a reader who has never trained or served a model will
   find the mathematics correct and the reasons for caring about it absent.

**And the 80/80 standard was unmeasurable as defined.** The Quiz runs on the
thirteen Foundation programs only, so a standard defined against it could not be
measured on thirty-four of the forty-seven — and was contaminated on the other
thirteen, because the same items serve as entry and exit test. The instrument is
now the **scored Test exercises**, which every program has, with entry and exit
items drawn from the same pool but not identical.

**The trap catalogue** — the misconceptions AI engineers actually hold, each
phrased in the reader's own voice with its correction and its owning program —
is `notes/02-grounding-and-traps.md` §3. A trap frame must *elicit* the error,
not warn against it, and the correction must explain the reasoning that produced
it; the pretesting literature is clear that a box saying "wrong" does nothing.

---

## Build

```bash
make            # numbers, diagrams, both editions at 17 x 24 cm, then the gates
make a4         # both editions on A4
make all-formats  # all four PDFs
make en         # English only, and check its log properly
make pl         # Polish only
make en-a4      # the same, on A4
make numbers    # regenerate figures/values from code/
make verify     # fail if any committed number has drifted from its script
make debt       # every outstanding-work ledger
make check      # checklog + parity + reflist, without rebuilding
make site       # assemble locally exactly what CI publishes to Pages
```

**The PDF has an address.** Before, the only way to get one was a 14-day CI
artefact or a tagged release, so the book was not readable without a TeX
installation. `pages.yml` now builds both editions on every push to `main` and
publishes them:

- `.../book-en-a4.pdf` · `.../book-pl-a4.pdf` — A4, and what the site links to
- `.../book-en.pdf` · `.../book-pl.pdf` — 17 x 24 cm

It duplicates the compile steps from `build.yml` on purpose, and runs
`checklog.py` against its own logs rather than trusting another workflow's:
Pages must never publish a PDF that did not build.

CI runs the numbers job first and gates everything on it, then parity as a hard
gate, then **all four PDFs in a matrix** (two languages times two formats), then
a cross-reference comparison out of the two `.aux` files. Only the trade format
uploads its aux tree: labels resolve to program and frame numbers, which the
paper format cannot change, so a second copy would give `reflist.py` two
identical things to compare and collide on the artefact name. The ledgers are advisory and are published to the step
summary on every build.

**After each pass:**

1. `make all-formats` — zero errors, zero warnings, zero unresolved references.
   All four, not two: a format change moves every page boundary, and a table
   that fits on one page in the trade format can overflow its vbox on A4.
2. `python3 tools/checklog.py main-*.log` — **not** `grep '^!'`
3. `python3 tools/checkpdf.py main-*.pdf` — the two defects that live on the
   finished page and in no log: a stranded frame opener, and an orphaned cue.
   All four PDFs, for the same reason as step 1 — every orphaned cue found so
   far was in an A4 build only.
4. `python3 tools/parity.py` — zero failures before you commit
5. `python3 tools/check_structure.py --frames` — every frame number the program
   quotes exists, and every cue is the last thing in its frame
6. `make debt` and `make verify` — confirm the ledgers moved the way you
   expected, and that no computed value or transcript has drifted from its
   script
7. Update the Status table, the page table and the ledgers at the top of this
   file. **Re-measure the page counts and the overfull multiset from the build
   in front of you**: both are functions of the layout constants, and neither
   survives being carried across a change.

Note on tagging: `git push --tags` returns HTTP 403 through the sandbox's git
proxy, so tags created in a web session exist locally only. Tag from a local
clone instead.

---

## What is left

1. **Forty-two programs.** This is the work. F6–F13 first, because the
   Foundation part is what makes the book's claim — *it assumes nothing* — true
   or false. **F12 (the chain rule) is still the one outstanding program the
   rest of the book leans on hardest** — and it is now owed two things by name:
   F4's sigma and product, for stating a chain of layers as one, and F5's
   composition, which frame 34 hands it explicitly. F6 is the natural next one:
   its brief is *solving is undoing*, which F5 has already had the reader doing
   informally at every inverse and every rearranged bracket.
2. **The ten measurements.** All specified, nine free. E9 — logit variance and
   softmax entropy with and without the `1/√d_k` scaling — is the one to run
   first: it costs nothing and it converts the book's central derivation from an
   argument into a demonstration.
3. **Appendices C–F.** C (formula reference) is the one that fixes Stroud's
   fair criticism that a book of frames is a useless reference.
4. **Program P7 has no plan.** It was added by review rather than designed, so
   its brief is a contract and not yet a frame-by-frame plan. Write that before
   writing the program.
5. **`odzera`, the companion library.** One stage per part, every gradient
   checked against finite differences in CI, no GPU, the whole suite under a
   minute. Specified in `notes/01-curriculum.md` §18; nothing built.
6. **Reader validation.** Nobody has read this. Until somebody has, the 80/80
   ledger stays open and the book may not claim it.

Two decisions still open, both recorded in `notes/01-curriculum.md` §20: whether
this is one volume or two (≈2,415 frames is 470–550 pages), and whether P12
(combinatorics) should move next to the probability that consumes it.
