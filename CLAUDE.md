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
| Programs | **F1–F13 and P1–P33 written, both editions \dash{} Parts I to VIII entire, and Part IX all but its last program.** P34 is a stub carrying its brief | 1 of 47 |
| Appendices | A (answers, generated) and B (notation) drafted; C–F are stubs | C, D, E, F |

**Two languages times two paper formats, four PDFs, all clean.** A4 at 12pt is
the format the book is read in; 17 x 24 cm is the trade format shared with the
companion volumes.

| | Pages | Errors | Unresolved | Overfull hbox | Overfull vbox |
|---|---|---|---|---|---|
| `main-en` (17x24) | 1295 | 0 | 0 | **0** | 0 |
| `main-pl` (17x24) | 1313 | 0 | 0 | **0** | 0 |
| `main-en-a4` | 1080 | 0 | 0 | 1, the 6.3 pt below | 0 |
| `main-pl-a4` | 1094 | 0 | 0 | **0** | 0 |

**Three of the four builds now carry no overfull box at all, and the fourth
carries one.** That box is `$7\,000\,000\,000$` in F1, which cannot break; it
exists in one format and one language because that is where the line falls,
and it is well under the 15 pt budget.

The four boxes each build used to carry were `F10`, `F11`, `F12` and `F13` in
the table of contents, and they were **not** anybody's prose: `book.cls` sizes
a chapter's number box at 1.5em and a section's at 2.3em, which fit arabic
numerals and do not fit `F10` or `F10.1`. They had been in the baseline since
F10 was given a number, which is to say they were there before F10 was
written and were attributed to nothing. Widened in `preamble.tex`, measured
rather than guessed, with the reasoning beside them. **Compare any future
multiset against this table, not against the older one**, and note that
Part II onward numbers programs 1 to 34, whose labels are narrower, so F13 is
the binding case for the whole book. **F2 added no overfull box to any of the four formats** —
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
At F01's 73% cue rate the cost over the manifest's 2,418 planned frames is of
the order of a hundred pages, which belongs in the one-volume/two-volume
question in `notes/01-curriculum.md` §20 \dash{} where the page estimate that
question rested on is now measured and was wrong by a factor of about three.

**Compare the hbox multiset only against a baseline built on the same
machine.** CI has newtx and inconsolata; a bare container has neither, and the
two measure different line widths. The numbers above are from a container
build that reproduced the pre-pass table exactly, so they are comparable to
what was there before.

**Debt ledgers, reported by CI on every build** (`make debt`):

- **1 of 47 programs is a stub**, in each language. This is the whole of the
  remaining work and it dwarfs everything else.
- 0 exercises without an answer · 0 programs outside their frame band ·
  0 programs without declared learning outcomes
- 1570 computed values, all referenced, all present, plus the committed console
  transcripts, which are inside the same drift gate as of the F3 pass
- 0 `verifybox` blocks · 292 Mermaid sources, all rendering
- 80 `\transcript{}` references, every one backed by a committed file and
  every one now actually on the page \dash{} see *The transcripts were not
  printing* below
- **0 stranded frame openers and 0 stranded section headings**, in all four
  builds. Both are structural and both are hard gates in `tools/checkpdf.py`.
- **101 orphan-tail pages: 29 · 29 · 22 · 21** across `main-en`, `main-pl`,
  `main-en-a4`, `main-pl-a4` \dash{} P12 moved none, P13 two, P14 two,
  **P15 none**, P16 one, **P17 none**, P18 one, **P19 none**, P20 three, P21 three, P22 one,
  **P23 none**, P24 one, P25 two, P26 two, P27 two, **P28 none**, P29 one, **P30 one**, **P31 none**, **P32 none** and P33 one
  \dash{} from 15 before F5, 26 before F6, 33 before F7,
  41 before F8, 43 before F9, 45 before F10, 49 before F11, 51 before F12,
  55 before P1, 57 before P2, 59 before P3, 60 before P4, 65 before P5 and 68
  before P6. **P6 added two and the ten transcripts it turned on added three**,
  all of the latter in `main-pl` \dash{} a listing appearing where a marker box
  used to be moves every break after it. **P7 added none, and P9 added none
  either**, which has now happened three times (F13, P07, P09) and every time
  for the same reason: the recorded rules were applied while drafting rather
  than after a build named the defect. **P8 added
  three, over three rounds of lengthening** \dash{} see its pass note for the
  clearest instance yet of the random walk
  \dash{} and one of P04's five is the price of the three cues its pass added
  back, which is the Stroud layout pass's measurement arriving from the other
  direction.
  The count is the signal and it is going the wrong way, at roughly one to
  eleven per program written; **F8 added one, F9 two, F10 four, F11 two and
  F12 four, against F5's eleven**, and the reason is worth having — all five
  were written with the two-sided rule from F6 in hand, so a frame whose tail
  lands badly is lengthened rather than trimmed. **P12 added none either**,
  which is the fourth time; **P23 made it the eighth, P28 the ninth and P32
  the eleventh** \dash{} though P32's cost seven rounds of lengthening rather
  than coming free from the recorded rules. **A fourth structural fix was measured in the F6 pass and
  reverted**, because it clears the orphaned *cue* by converting it into more
  orphan *tails* — see *Program F6 pass* and the sweep table in
  `preamble.tex`. `checkpdf.py` prints every one of them on
  every run and **does not fail the build for them**; the reasoning is in the
  note above its `main()` and is summarised under *Program F4 review pass*.
  This is the second ledger that is reported rather than gated, and like the
  first it must not quietly go away. **When the count goes up, that is the
  signal.**
- **Elicitation rate: 51% of the book's frames put a question to the reader**,
  and the trend is the ledger rather than the number: **73--78% through
  F01--F06, 50--66% through F08--F13, 29--31% across the whole of Part II,
  35% in P04, 36% in P05, 38% in P06, 40% in P07, 35% in P08, 40% in P09,
  39% in P10, 39% in P11, **46% in P12**, **50% in P13**, **48% in P14** and
  **50% in P15**, **47% in P16**, **50% in P17**, **48% in P18** and
  **47% in P19**, **47% in P20**, **48% in P21**, **45% in P22**,
  **53% in P23**, **46% in P24**, **48% in P25**, **52% in P26** and
  **53% in P27**, **54% in P28**, **55% in P29**, **52% in P30**, **50% in
  P31**, **51% in P32** and **51% in P33** \dash{} P29 is the highest outside
  Part I, with P28 next and then P23 and P27; P26 and P30 follow, and P13,
  P15, P17, P31, P32 and P33 reach or pass the book's own rate.**
  **P24 is the first program whose rate is visible in its frame count**: nine
  of its sixty-four frames exist because the draft was raised from 36%, which
  is the elicitation ledger's cost measured in frames rather than in pages.
  Part III is climbing because the rate is now designed in rather than measured
  afterwards. The book's own figure falls as Part III grows, because every
  Part III program sits below Part I's rate \dash{} which is why the per-program
  column is the ledger and the single number is not. A frame carries `\nextframe` if and only if the
  next frame opens
  with an answer, so the cue rate *is* the elicitation rate. It halved over
  seventeen programs with every gate green, because `RE_DEMANDS` treats
  `\nextframe`, `\blank`, `\dotline` and `\yourturn` alike and C16 compares
  the editions rather than the ratio \dash{} **nothing in the repository looked
  at it.** `make debt` reports it now, per program and for the book, **reported
  and never fatal**, on the orphan tail's reasoning. The last `\yourturn` in
  the book is in F04 and the last `\blank` is in F07. **When the rate falls,
  that is the signal.**
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
specified in `notes/01-curriculum.md`, nine of them free and finishing on a
laptop in under a minute; until one runs, the claim it would support is
labelled as judgement and its table stays empty.

**This paragraph used to say none had been run, and it had been false since the
P20 pass** \dash{} which has its own heading in this file, *Experiment E6*,
reporting measured step counts against predicted ones. E9 has been run too, in
the P25 pass. So the ledger is now a **Status column** in
`notes/01-curriculum.md` §17, filled in by the pass that runs the experiment,
and neither that file nor this one states a total: a count of how many have run
is exactly the class of claim the paragraphs below forbid, and it decayed in
the two documents the next author reads first.

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
| **`check_structure.py --scripts`** | A `\transcript{}` naming a file that is not there, or written as a path rather than a stem. The macro's own fallback prints a grey marker and builds, which is what let ten of the book's twelve transcripts go nine programs without reaching a page. Hard gate in `make check`, because on a tree where `make numbers` has run it is always a typo |
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
| `\Var` `\Ex` | `Var` `E` | `Var` `E` — the mandatory notation box for `D²(X)` and `M(X)` is P24 §3, and Appendix B points at it |

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

**And the rule the lint DOES check, which the translator keeps breaking: order
is part of the translation.** C4, C8 and C12 compare the two editions'
structural tokens, maths spans and numeric literals **in order**, so a sentence
must carry the same spans and numbers in the same sequence, not merely contain
the same ones. Polish word order fights this in two specific ways, and between
them they cost F06 three parity rounds and F07 six:

- **A number spelled as a word.** *zerem* for `$0$`, *dwukrotnie* for `$2$`,
  *ujemne* where the English repeats `$k$`. Each drops a maths span and a
  digit, and C8 and C12 both fail. Write `$0$`, `$2$-krotnie`, `ujemne $k$`.
- **A reference behind its maths.** `$2^{10} \approx 10^{3}$ z Programu F01`
  against `Program F01's $2^{10} \approx 10^{3}$` — same content, swapped
  order, C4 fails. Rebuild the Polish sentence so the reference leads:
  *Program F01 podaje $2^{10} \approx 10^{3}$*.
- **An English compound whose Polish form needs the symbol.** English writes
  *p-value* as prose and Polish writes *wartość $p$*, which carries a maths
  span English does not have — C4 and C8 both fail, in every frame the term
  appears in. Neither edition is wrong; the fix is the **English's**, because
  `$p$-value` is standard typography and it makes the two streams identical.
  Found in P28, seven times in one program.

Neither is a mathematical divergence and both are real editorial ones, which is
why the checks are right to fail. The fix is always to rebuild the Polish
sentence, never to loosen the check.

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

- **A PDF page number does not transfer between two installations that
  paginate differently, and anchoring on one costs cycles.** CI failed
  `en` A4 on two overfull vboxes, 12.29 pt and 4.99 pt, reported on page 639
  of 660. The page was chased into the ANSWERS appendix, because 639 of 660
  is 21 from the end and 21 from the end of the local 670-page build is the
  answers. It is the **index**, and TeX said so all along:

  ```
  (./main-en-a4.ind [637
  ] [638]
  Overfull \vbox (12.28888pt too high) has occurred while \output is active
  Overfull \vbox (4.98888pt too high) has occurred while \output is active
  ```

  Two complaints, one page, a two-column region: the index's third page
  overflowing in both columns, which is the shape recorded below for the same
  file. The arithmetic failed because the answers appendix is *much* shorter
  under CI's metrics, so the two builds differ by thirty pages at that point
  and by ten overall. **Anchor on what TeX says it had open, never on distance
  from either end.**

  Three glue changes were made to the answers appendix before the raw log was
  read, and **not one moved the reported size by a tenth of a point** \dash{}
  which was the evidence, ignored twice, that the box was somewhere those
  changes could not reach. `theindex` carries its own `\raggedbottom` and
  `\parskip` shrink, so it was immune to all of them by construction.

  **The rule: read the log before the third fix, not after.** `checklog.py`
  now names the page or the file and line of every vbox and distinguishes a
  page that came out too tall from a fixed box that did not fit, and the
  workflow prints TeX's own words around each complaint. Both were written
  during this chase and both would have ended it at the first cycle.

- **A page of REFERENCE MATTER has no glue, and `\flushbottom` requires every
  page to be exactly `\textheight` tall.** The index is the standing example
  (see below). The **answers appendix** is a second one, found while looking
  for the index box and fixed on its own merits rather than because it was
  this failure: its `list` set `\topsep`, `\itemsep` and `\parsep` with
  `\setlength`, so all three were rigid, and the tail of the appendix is
  twenty-two `\subsection*` headings in a row \dash{} one per unwritten
  program, each with a single line under it, eleven on a page \dash{} which
  is a concertina of rigid three-line blocks with nothing to give at any of
  its breakpoints. It now carries `\raggedbottom`, shrink on the three list
  lengths, and a pure-shrink `\vspace{0pt plus 0pt minus 3pt}` before each
  heading. Nothing moves; all four page counts and the whole overfull multiset
  were unchanged by the last of those.

  **The generalisable rule: anywhere this book sets vertical glue with
  `\setlength`, ask what gives on that page.** And *shrink has to be where
  the material is* \dash{} on those heading pages there is no list at all,
  so the shrink added to the list lengths could not have helped even if the
  box had been there.

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

- **`float()` accepts `inf`, `-inf` and `nan`, so a value ledger that tests
  numerichood with a bare `try: float(...)` will route them to `\val{}`** —
  and siunitx answers `Invalid number '-inf'` and **writes a PDF over the top**,
  which the exit code and the PDF both call fine. Guard with `math.isfinite`.
  And an infinity is a *name* rather than a computed number: it belongs on the
  page as `\code{-inf}`, not behind `\val{}`.

- **The four-significant-figure rounding of the largest double is not a
  double.** `f"{1.7976931348623157e308:.4g}"` gives `1.798e+308`, which is
  above the ceiling and parses back to `inf`. Anything printing a format's
  ceiling must truncate towards zero and assert that the printed form is a
  value the format can hold. Found in P01 *after* P01 had shipped, by the
  `isfinite` guard above.

- **A background command written `make ... > log 2>&1; echo "EXIT $?"` reports
  exit 0 whatever make did**, because the notification carries the compound
  command's status. A build that died with `Error 12` was reported complete and
  three of the four page counts had silently not moved. Read the log's own exit
  line, and treat an unchanged page count as a failed build — which is F12's
  tell arriving through a different door.

- **A Test exercise is set in a narrower measure than the frame its numbers
  came from.** F06 recorded this for `\answerto` and F08 for a long `\code{}`
  inside one; a `testexercises` item is the third place it bites. Two
  coordinate pairs, `$(3, 4)$` and `$(4.5981, 1.9641)$`, sit comfortably inside
  the frame that introduces them and gave **25.8 pt** in `main-en-a4` alone
  when run into an exercise. The recorded fix works without a detour: **put it
  in a display.** A display gets its own line, so an unbreakable run cannot
  overflow under any metrics.

- **The index is where the two TeX installations diverge worst, and the cure
  is not the one prose uses.** CI failed on two OVERFULL VBOXES in
  `main-en.ind` \dash{} 3.8 pt and 17.4 pt \dash{} on source this container
  built with zero. Prose has paragraph glue to give and the recorded fix is to
  put the unbreakable run in a display; an index has almost none. Index lines
  carry no stretch, `\parskip` there is `0pt plus 0.3pt` with **no shrink**,
  and `\indexspace` gives back 3 pt, while `book` in twoside mode holds every
  column to the full text height. **The cure is two lengths and it took two
  rounds against CI**, which is worth having because the second round is the
  instructive one:

  1. **`\raggedbottom` inside `theindex`** lets a column end short, which is
     what every index in print does. CI went from `[17.4, 3.8]` to `[3.8, 3.8]`.
  2. The pair that remained were **the same size**, and that is the tell:
     `\output` fires once per column in a `\twocolumn` region, so it is one
     page overflowing identically in *both* columns \dash{} the index's first,
     where `\@makeschapterhead` leaves a residual that is not a whole number
     of lines. `\raggedbottom` cannot touch it, because it adds **stretch**
     and the page is too **tall**. What an index lacks is **shrink**:
     `theindex` sets `\parskip` to `0pt plus 0.3pt` with none. A fifth of a
     point per entry is eight points a column, absorbs the residual under any
     metrics, and is invisible between two index lines.

  `\vfuzz` was the other candidate and was rejected: raising it hides real
  overfull vboxes everywhere else, which is how a gate goes quiet. Trimming an
  index entry is the unwinnable loop this file names, and it is *especially*
  unwinnable here because the entry that would have to go is chosen by
  whichever machine is complaining.

  And the patch block sits **outside** the preamble's `\makeatletter` group,
  so the length is written in plain units; `\z@` and `\@plus` there are an
  undefined control sequence in every build.

  **AND ALL OF THAT WAS MEASURED AGAINST THE WRONG MECHANISM, which the P23
  pass established and which retires every constant above.** The index in this
  book is **not** a `\twocolumn` region. `imakeidx` is loaded without its
  `original` option and in that mode it replaces `theindex` with
  **`multicols`**. So `\raggedbottom` \dash{} which sets `\@textbottom`, read
  by `\@makecol` \dash{} had been **inert since the day it was added**, because
  multicol installs its own output routine and never calls `\@makecol`; and
  `\vfuzz` is inert too, because multicol sets `\vfuzz\z@` itself immediately
  before the `\vbox to` that balances the final page. The switch that is
  actually read is **`\raggedcolumns`**, and multicol's default,
  `\flushcolumns`, is exactly the rigid setting the paragraphs above diagnose.
  **Retired outright in the P24 pass**: the index's last page is no longer
  balanced at all, which is what `multicols*` does and what an index does in
  print, so the `\vbox to` that emitted every one of these complaints does not
  run. See that pass note; the constants above are history.
  It also explains the one detail nobody could account for: the complaint was
  always on the index's **last** page, because that is the only page multicol
  *balances* rather than splits, and a balanced column under `\flushcolumns`
  must come out exact.

  **The generalisable rule: a remedy that is correct for the environment you
  think you are in is INERT in the one you are actually in, and an inert remedy
  is indistinguishable from one that did not go far enough.** Five passes read
  the surviving residual as evidence that the constant needed raising. Before
  sweeping a constant a second time, confirm that the macro you are setting is
  read by the code that emits the complaint \dash{} here that was one `grep` of
  `imakeidx.sty` and one of `multicol.sty`. And when the question is about
  TeX's own semantics rather than about this book, **ask TeX**: the whole
  mechanism was settled by a ten-line standalone file in seconds, against four
  CI cycles spent on the constant.

- **`\apptocmd{\tableofcontents}{...}` runs AFTER the contents has been
  typeset, and the assignment then stands for the rest of the book.**
  `\tableofcontents` is `\chapter*{\contentsname}` followed by
  `\@starttoc{toc}`, and it is not inside a group. So anything appended to it
  reaches nothing in the contents and leaks into every paragraph that follows.
  An `\emergencystretch` added this way to rescue one over-wide contents line
  did exactly that \dash{} **and it was invisible because it made the ledger
  look better**: the 6.3 pt box this file records in `main-en-a4` disappeared,
  which is a real overfull line silently loosened rather than fixed. `\pretocmd`
  sets it before the contents is read and `\apptocmd` restores it after, which
  is the scoping the comment had claimed all along.

  **The generalisable rule, and it cost two diagnoses in one pass: when a fix
  does not move the number, check WHERE it runs before you check how large it
  is.** The index's `\raggedbottom` and `\vfuzz` above are the same shape from
  the other direction, and both looked like fixes that had not gone far enough.

- **You cannot reproduce CI's metrics in this container, and trying breaks
  something worth more.** `texlive-fonts-extra` and `texlive-plain-generic`
  install newtx, inconsolata and `binhex.tex`, and the build then dies on
  `Font TS1/ntxtlf/m/n/10.95=ts1-qtmr ... invalid font` because the TS1 map is
  incomplete \dash{} and even complete, this is TeX Live 2023 against CI's
  2026, so the metrics would still differ. Worse, a container that *has* newtx
  is no longer the bare installation whose absence of inconsolata found the
  `upquote` defect, and every page count in this file was measured on the bare
  one. They were installed, tried and purged. **CI is the reproduction; treat
  it as the second machine it is, and fix the class rather than the instance.**

- **A generated, committed, drift-gated transcript can still be un-runnable.**
  `make verify` proves a transcript matches the script that wrote it. It says
  nothing about whether the listing on the page executes: P04's called a
  function it never imported, so a reader pasting it got `NameError` while
  every gate stayed green. The test is the one F03 established for the
  `upquote` defect \dash{} extract it from the finished PDF and run what comes
  out \dash{} and it has to be applied to generated transcripts too, precisely
  because they look as though somebody must have.

- **A measured floating-point residual is a property of the machine, so it
  must be committed as a BOUND and never as a figure.** CI rejected P06 over
  two values: `p06.assoc.err` was `4.4e-16` here and `2.2e-16` there, and
  `p06.bend.affine` `2.7e-16` against `2.6e-16`. Neither number was wrong.
  They are the rounding noise left after summing a few dozen doubles, and the
  order those additions happen in is a property of the interpreter and the
  build rather than of the mathematics \dash{} so the drift gate was right and
  the committed value was the defect.

  It is F03's `np.logspace` finding wearing different clothes: an
  **observation** committed where an **invariant** was meant. The invariant is
  *the disagreement is rounding rather than a difference*, and the honest way
  to write that is a ceiling the measurement clears on any machine.
  `code/p06_matrices_as_maps.py` has a `bound()` helper that rounds up to the
  next power of ten and asserts the measurement clears it; the page then reads
  *better than $10^{-15}$* rather than a figure nobody can reproduce.

  **Fourteen more are latent**, in F05, F07, F08, F09, F12 and P05 \dash{}
  every committed value whose name ends `.err` and every residual quoted
  beside one. They have survived CI so far, which is not the same as being
  reproducible. Sweeping them is a pass of its own: each is quoted in prose in
  two editions, and rewriting six merged programs inside a PR about a seventh
  is how a measurement stops being trusted. Note that the IEEE-754 constants
  \dash{} `p01.gap.one`, `p01.fp64.eps`, `f11.fd.vanishes` and the rest
  \dash{} are **not** in this class: they are exact everywhere and must stay
  as figures.

- **A background `sleep` is not a wait, and reading repeated identical poll
  results as elapsed time is how you invent a failure that never happened.**
  During P14's CI run five successive polls of the diagrams job returned
  `in_progress`, and each poll was preceded by a `sleep` started **in the
  background** \dash{} which returns immediately. Almost no wall time passed.
  The five identical answers were read as thirty minutes, a hang was diagnosed
  against a job whose comparable runs finish in seven, and a workflow change
  was written and pushed on that basis. `date -u` said 5.7 minutes.

  It is this repository's own recurring defect wearing new clothes: **a
  measurement taken from a misread instrument**, exactly like the CI vbox
  chased into the answers appendix because a page number was read as a
  distance from the end. The rule is the same one, and it is cheap: **before
  concluding anything from elapsed time, ask the clock.** A status that has
  not changed is not evidence that time has passed.

- **A timeout belongs at the granularity you want the failure reported at.**
  This one is worth keeping on its own reasoning, separately from the false
  alarm above that produced it. The diagrams job renders every Mermaid source
  in one step behind a single 25-minute `timeout-minutes`; one wedged headless
  Chromium would spend the whole budget and report only *the diagrams job
  timed out*, naming neither the diagram nor the reason. Each render now
  carries `timeout 180` and reports the file it was rendering. That is the
  argument that put `timeout-minutes` on every job, applied one level down.

  In the same place: the loop called `npx -y @mermaid-js/mermaid-cli@11`
  **once per diagram**, paying package resolution over a hundred and sixty
  times and growing by six per program. It installs once now. All three
  workflows carry the same loop and all three were changed, on the
  `$(COMPUTED)` principle already recorded here. The Makefile's per-target
  `npx` is deliberately untouched \dash{} a local build is watched by a person
  who can see it hang.

- **A CI job with no `timeout-minutes` reports nothing when it hangs, for six
  hours.** The numbers job sat \enquote{in progress} for most of an afternoon
  on a step that takes half a minute on a laptop, with every other job green
  and no signal to act on; the token this session runs under cannot cancel or
  re-run a workflow, so there was not even a way to clear it. GitHub's default
  is six hours, which is not a ceiling anybody chose. Every job in all three
  workflows now carries one, sized generously against its own measured cost.
  **A hung job with a timeout is a failure somebody can read; without one it is
  indistinguishable from a slow queue.**

- **A fallback that keeps a build alive also keeps a typo alive, and this one
  hid ten of the book's twelve listings.** `\transcript` used to take a whole
  path; nine of the twelve call sites passed a bare stem, so `\IfFileExists`
  looked for `p06-order.tex`, failed, and printed the macro's
  file-is-absent marker instead. **Ten transcripts went nine programs without
  ever reaching a page**, with every gate green, because the marker prints in
  grey with its own label and reads exactly like somebody's decision. `make
  verify` compares each file against the script that wrote it and never asks
  whether a page includes it; `checklog` reads the log, `checkpdf` reads the
  layout, and parity compares the two editions, which agreed because both were
  wrong.

  The macro now takes the **stem** and builds the path itself, which makes the
  wrong call impossible rather than detectable \dash{} the move `\mermaidfig`
  and `\pyregion` already make. `check_structure.py --scripts` is the second
  half and is a hard gate in `make check`: on a tree where `make numbers` has
  run, a `\transcript` naming a file that is not there is a typo and nothing
  else, and it is worth failing on before the build rather than after it. It
  refuses a path as well, because a path is the old form and would now resolve
  to `figures/transcripts/figures/transcripts/...`. Both faults were introduced
  and reverted to prove the check fires.

  **The generalisable shape: every graceful degradation in this preamble is a
  place where a defect can look intentional.** `\mermaidfig` has the same
  exposure and `\val{}` does not, because a missing value is a `??` nobody
  reads as a choice.

- **A macro from a CONDITIONALLY LOADED package is invisible to both of this
  project's machines.** A P09 draft used `\begin{psmallmatrix}`, which comes
  from **mathtools**, and `preamble.tex` loads mathtools inside an
  `\IfFileExists`. On a TeX installation without it the build dies on an
  undefined control sequence \dash{} and **neither machine here would have
  caught it**, because this container has mathtools and CI has a fuller TeX
  Live than this container. The `amssymb`/`newtxmath` trap is a full
  installation failing where a bare one passes; the `upquote` trap is a bare
  one shipping what a full one hides; this is the third direction, latent on
  every machine that exists here and waiting for a reader's.

  `preamble.tex` carries eleven `\IfFileExists` probes and **mathtools is the
  only one that supplies macros the prose can use** \dash{} the rest are fonts,
  `babel`, `upquote`, and `csquotes`, which has a fallback branch. So the rule
  is narrow: **before using a maths macro you have not used before, grep the
  preamble for the package that defines it.** No gate was added, because this
  has never shipped; the rule is here so that the first time it does, somebody
  knows where to look.

- **A gate that measures a ratio is a different animal from one that measures a
  property, and this repository had none of the first kind.** `RE_DEMANDS`,
  parity's C16, C4 and C14 all check that each cue is *correct*; none of them
  looks at how many there are. The elicitation rate accordingly halved over
  seventeen programs with every gate green throughout. When a design property
  is a rate rather than a predicate, the check has to count both sides.

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
rather than after it. **`notes/05-floating-point-plan.md` is F1's own
frame-by-frame plan, not P1's** — its §1 is the F1/P1 boundary argument, which
is where the filename comes from. The P01 pass below records what else in that
file the written F01 does not bear out.

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

### Program F6 pass, August 2026

**Forty-two teaching frames, forty-four printed, both editions**, against a
brief that projected forty-five. Six sections: solving as undoing, making a
letter the subject, the straight line, two equations in two unknowns,
inequalities, and clipping. All three of the brief's payoffs are delivered
where it said they would be \dash{} `y = wx + b` is the entire linear model
(frame 17), a decision threshold is an inequality (frames 34--35), and a
clipped value is two inequalities (frame 36).

**Two new operators**, `\logit` and `\clip`, beside `\relu` and `\softmax` in
`preamble.tex`. Both spell the same in Polish, so neither needs a language
file entry \dash{} which is the notation contract's keyboard test coming out
the simple way for once.

#### The orphaned cue: the fix is sometimes to make the frame LONGER

This is the pass's most transferable finding and it contradicts what this file
has said since F3.

Two orphaned cues arrived with F06, and **shortening the frames did not move
them**. Two rounds of trimming on the English frame 12 left the cue on exactly
the same page both times: the page kept ending precisely at the `\dotline`,
because every line taken out of frame 12 pulled a line of frame 11 up behind
it. The tail stayed where it was and the page stayed full.

**Lengthening cleared it in one round.** A paragraph added to the frame pushes
the question, the dots and the cue over the boundary *together*, which is what
was wanted; trimming can only ever pull more material up to fill the gap. So
the rule is now two-sided: when a frame's tail sits one line past a page
boundary, ask which side of the boundary you want it on, and note that adding
is the move that carries the whole tail and cutting is the move that carries
none of it.

Both edits were made in **both** editions, so the two say the same thing: the
English gained a paragraph on why a confident unit is hard to make more
confident, and both gained a sentence on why adding two equations is the
balance rule.

#### A fourth structural attempt on the cue, measured and reverted

`preamble.tex` records three failed attempts (`\removelastskip`, a penalty on
`\dotline`, widow and club penalties). The comment above `\nextframe` said the
only thing that would close it is "a penalty before that glue, which means
inside `\dotline`, and that is out of bounds here". That was worth testing, so
it was tested: give `\dotline` the same room test `\begin{fr}` has, sized for
the dots plus the cue, and turn the page before the dots when there is not
enough.

| reserve | pages (en / pl / en-a4 / pl-a4) | orphaned cues | orphan tails |
|---|---|---|---|
| none | 352 / 358 / 318 / 320 | 2 | 35 |
| 2 bl | 354 / 360 / 320 / 322 | 1 | 44 |
| 4 bl | 354 / 360 / 320 / 320 | **0** | 43 |

The sweep was run mid-pass, so its `none` row is the tree as it stood then and
not the final page table at the top of this file \dash{} which is the rule
this file already states about carrying page counts across a change.

**It works, and it is a relabelling.** Every page the guard turns early is a
page whose ink stops in its top quarter, which is precisely the orphan-tail
defect: two cues become eight more tails and six more pages, and the reader
still turns over onto white paper. The cue check goes quiet because the cue
has company, not because the page got better. Reverted, and the table is in
`preamble.tex` beside the other three so the fifth person does not re-run it.

#### An answer that overflowed on ONE TeX installation, and the fix that cannot

The Q14 answer carries `$\max(-1, \min(1, x))$`, which is one unbreakable
maths span, and in Polish it sits behind a longer clause than in English. It
produced a **17.4 pt** overfull hbox in `main-pl` \dash{} the first box over
the 15 pt budget this book has shipped into a build \dash{} and the first
reword took it to **34.4 pt** on A4, because *w pozostałych przypadkach* is
longer than *w przeciwnym razie*.

The generalisable part is where it happened: **a back-matter answer is set in
a narrower measure than the frame it came from**, so a formula that sits
comfortably inside a frame can overflow inside its own answer, and only the
answers appendix will show it.

**And shortening the clause did not settle it, because the two TeX
installations disagree.** With the clause trimmed the container built clean and
**CI came back with a 22.9 pt box on the same answer**, because newtx is wider
than Latin Modern and the break the container found is not available there.
That is the `amssymb`/`newtxmath` trap in its third direction: not a full
installation failing where a bare one passes, nor a bare one shipping a defect
a full one hides, but **the same source overflowing on one and not the other
with no error either way**.

Chasing it with prose is unwinnable, because the metrics that decide it are
not on this machine. **The fix is to remove the unbreakable run: the formula
now sits in a display inside the answer.** A display gets its own line, so a
110 pt formula in a 320 pt column cannot overflow under any metrics, and the
prose around it wraps freely. `\answerto` takes a display without complaint
— which is the mechanism CLAUDE.md already says the answer store was chosen
for.

**The rule: an inline formula of any length inside an `\answerto` is a
latent overfull box on somebody else's TeX. Put it in a display.**

#### Word order is part of the translation

Three parity failures were the same failure: Polish naturally puts a maths
span or a number where English puts a word, and **C4, C8 and C12 all compare
in order**.

- `section 1's $2x = x + x$` against `$2x = x + x$ z sekcji 1` \dash{} the
  digits arrive as `1, 2` in one edition and `2, 1` in the other.
- `frame $21$'s gap in $y = mx + c$` against `luka w $y = mx + c$ z ramki $21$`.
- `\textbf{The $-1$ in $f^{-1}$}` against `Minus jedynka w $f^{-1}$`, where the
  Polish spelled the number as a word and lost both a maths span and a digit.

None is a mathematical divergence and all three are real editorial ones. The
rule for the translator: **a sentence containing two maths spans, or a number
and a maths span, has to keep them in the same order**, not merely contain the
same ones.

#### Four claims a reader could have falsified

- **A contradictory vector.** A further problem said *a gradient is
  $(1, 0, 0, \ldots, 0)$ with a single non-zero component equal to $10$*. It
  is `(10, 0, …, 0)`; the answer beneath it was right and the statement was
  not.
- **The English file header named the wrong frames** for its own headline
  trap \dash{} 33 and 34, where the trap is at 29 and 30 \dash{} because the
  header was written before the frame-number remap and only the Polish twin
  was updated. **A file header is a claim about the file and nothing checks
  it.**
- **A division with no condition, in the program that insists on conditions.**
  Frame 27 reads the gradient off $ax + by = c$ as $-\frac{a}{b}$ without
  saying $b \ne 0$, six frames after section 2 made *state the condition every
  time you divide by a letter* a rule. It now says it, and names the excluded
  case as frame 21's vertical line, which closes the loop the program had
  already opened.
- **The trap catalogue's owner for gradient clipping was stale** (P19, written
  before P7 was inserted; P19 is *Convexity and Jensen's inequality*). Item 26
  now points at F06 for the operations and the measurement and at **P21** for
  the noise model, and says in as many words why it used to say P19.

#### The measurement

Item 26 of the catalogue, and the one place in F06 where the reader's
intuition is actively wrong. On $g = (6, \num{0.5}, -\num{0.25})$, of length
$\num{6.0260}$, with a threshold of $\num{1.0}$:

| | length after | turned by |
|---|---|---|
| clipped **by value** | $\num{1.1456}$ \dash{} still above the threshold | $\num{23.9}$° |
| clipped **by norm** | $\num{1.0000}$ exactly | $0$° |

What `code/f06_equations.py` asserts is not those figures but the two
properties \dash{} that clipping by norm turns the vector through zero and
lands its length on the threshold, and that clipping by value does neither
\dash{} so a change of gradient moves the numbers and cannot quietly falsify
the frame. Both results are cross-checked against numpy, which announces
itself when absent.

The script also substitutes every solution it prints back into the equation it
came from and fails the build if the residual exceeds one part in $10^{12}$.
That is section 1's own instruction to the reader, executed by the build.

### Program F7 pass, August 2026

**Thirty-one teaching frames, thirty-three printed, both editions**, against a
brief that projected forty \dash{} the shortest Foundation program so far, and
the reason is worth recording rather than treating as a shortfall.

**A brief written before its neighbours over-estimates what is left to do.**
F07's brief was drafted when F05 and F06 were stubs. By the time it came to be
written, F05 had already given the logistic, its table of values, its symmetry
about $(0, \frac{1}{2})$, its crossing at $-b/w$ and the logit, and F06 had
already inverted it and turned its threshold into an inequality. What was
actually left was narrower and better: **where the shape comes from**. Section
3 derives it from the odds \dash{} if the odds are $e^{x}$ to one then the
probability is $\frac{e^{x}}{1+e^{x}}$ \dash{} and the flat ends stop being a
feature somebody added and become what a bounded quantity has to do. Check the
neighbours before estimating a length.

#### Two identities, asserted over a range rather than checked at a point

They are the program's spine, and each turns a second function into a
restatement of one the reader already has:

| Identity | Worst error | Over |
|---|---|---|
| $\tanh x = 2\sigma(2x) - 1$ | $\num{3.3e-16}$ | 401 points, and 4001 under numpy |
| $\softmax$ on two scores $= \sigma(a-b)$ | $\num{2.2e-16}$ | the whole $121 \times 121$ grid |

*These are the same curve* is a claim one agreeing value would not establish,
which is why both are swept rather than spot-checked. The consequence is that
$\tanh$ is not a second function to learn and softmax is not a new one to
meet \dash{} and the second settles the recurring question of whether a binary
classifier should use one logistic output or a two-way softmax. It is the same
model, because the two-score softmax depends only on $a - b$.

#### The restraint that matters: this program may not say the gradient vanishes

The measurement is there \dash{} the logistic is about
\val{f07.slope.ratio6} times less steep six units out than at its centre
\dash{} and the sentence everybody reaches for is not.

**One factor of a hundredth is survivable; the product of forty is not, and
the multiplying is the part that needs the chain rule.** F07 owns the shape and
hands the compounding to F12, in a `rigourbox` that says so. A program that
delivered the punchline here would leave F12 with nothing to prove and would
have taught the reader to say a sentence they could not derive.

#### The elicited trap: tanh saturates HARDER

Everyone knows $\tanh$ was preferred to the logistic in hidden layers. Almost
everyone attributes it to gentler saturation, and that is backwards.

| | at $x = 0$ | at $x = 2$ | ratio |
|---|---|---|---|
| logistic | \val{f07.slope.0} | \val{f07.slope.2} | about 2 |
| $\tanh$ | \val{f07.tanh.slope0} | \val{f07.tanh.slope2} | about 14 |

And it **follows from the identity** rather than being a separate fact:
squashing horizontally by two doubles the steepness and stretching vertically
by two doubles it again, so $\tanh$ is four times the logistic's steepness at
the centre \dash{} four quarters, which is 1 \dash{} and its flat region sits
four times closer in. The case for $\tanh$ was always that it is centred on
zero, which is a claim about where its outputs sit and not about how it bends.

The section closes on the mirror-image error, because it is as easy to acquire:
saturation is no argument against a logistic at an **output**, where the
flatness is what keeps a probability inside its range. Two arguments about the
same function in two places, and the second is not evidence for the first.

#### The section 1 trap, and one claim that was written from memory

*Exponential growth means fast growth* is wrong: it means growth proportional
to the current size. At $x = 5$ the polynomial $x^{5}$ is
\val{f07.poly.at5.ratio} times larger than $e^{x}$, and the exponential does
not overtake until $x = \val{f07.poly.crossover}$ \dash{} found by bisection,
so that changing the power changes the number on the page.

And one claim in section 3 was written from memory and then checked, which is
the wrong order: that $\sigma$ rounds to exactly $\num{1.0}$ *somewhere around
$x = 37$*. It does, and the hedge was hiding that nobody had run it. The
threshold is now computed and asserted from both sides \dash{}
$x = \val{f07.sig.saturates}$ \dash{} and the page quotes it. **A hedge is not
a substitute for a measurement; it is a confession that there is not one.**

#### Six parity failures, all one class, now generalised into the rules

Every one was Polish word order against checks that compare **in order**: a
number spelled as a word (*zerem* for `$0$`, *dwukrotnie* for `$2$`, a dropped
repeat of `$k$` or `$x$`), or a cross-reference sitting behind its maths
(`$2^{10} \approx 10^{3}$ z Programu F01` against `Program F01's $2^{10}
\approx 10^{3}$`).

F06 lost three rounds to the same thing and the note went into that pass's
write-up, where the next author would not look for it. It is now in
*Non-negotiable conventions*, beside the notation contract, as part of what the
translator brief must carry. **A lesson recorded only in a pass note is
recorded in the wrong place.**

#### What went right, and is worth not re-learning

F07 is the first program since F02 to need no orphaned-cue chase at all: all
four builds came back with zero cues on the first attempt. The six diagrams
also landed between 6.8 and 8.0 pt on the first render, all above the
aspect-ratio crossover, because the width budget was checked before the prose
was written rather than after.

### Program F8 pass, August 2026

**Thirty teaching frames, thirty-two printed, both editions**, against a brief
that projected forty-five. It is the shortest program written so far and
deliberately: the brief is *sine and cosine are the coordinates of a point
going round a circle*, and everything trigonometry usually carries with it —
the sine rule, the cosine rule, solving triangles, the identity list — is
excluded by the book's own scope statement. What is left is one picture and the
two things it buys, and padding it back to forty-five would have meant putting
the excluded material in.

**The two payoffs are identities swept in the script, not shown at a point.**
Cosine similarity *is* the cosine of the angle, checked against the angle
computed independently over 3481 pairs; and $R(\alpha)a \cdot R(\beta)b$
depends only on $\beta - \alpha$, over 1600 pairs. The second is the sentence
the brief asks for, and it makes "rotate the query and the key" a claim a
reader can check rather than an incantation.

#### Four claims a reader could have falsified, and two are the recurring class

- **The book was wrong about the book, for the fourth pass running.** Frame 13
  credited **F06** with putting the logistic's threshold at $-\frac{b}{w}$
  rather than at $b$. F06 line 302 says in as many words that it is *the
  crossing point Program F05 derived* — F06 uses it and attributes it. The
  fix strengthens the paragraph, because the paragraph is about F05's four
  moves throughout. **Open the program before writing a sentence about it**;
  this is the fourth time that rule has been paid for and the first where the
  file being described states the correct attribution on the line that was
  misread.
- **A forward pointer to something nobody had promised.** Frame 21 said
  *Program P05 takes both of these seriously* about embedding anisotropy and
  about similarity driven by shared style or length. P05's brief undertakes
  neither: it is the inner product, norms and projection, and what it does
  undertake is that **in high dimension two unrelated vectors are almost always
  nearly orthogonal**. That is the *baseline* both failure modes are deviations
  from, so the pointer is now to what P05 actually promises, and the frame says
  plainly that neither failure mode is measured in this book. Same shape as
  F04's P03 pointer, and resolved the same way — by softening rather than by
  re-inflating another program's brief.
- **Two counts that were one over.** The page said the identities were checked
  *at fourteen hundred angles* and *over six hundred angles*; the sweeps were
  `range(-700, 701)` and `range(-300, 301)`, which are 1401 and 601. The fix is
  the sweep, not the wording: both now run exactly as many angles as the page
  says. It is F05's tail-ratio defect in a smaller denomination — **a number on
  the page that does not reproduce from the thing that produced it.**
- **A threshold that did not match its own figure.** Frame 18 printed a
  retrieval score of `0.9899` (from a vector pair) and the trapbox one line
  below compared cutoffs of `0.99` and `0.98`, quoting *about eleven and a
  half* degrees from arithmetic nobody had run. Two numbers an inch apart that
  look like one and are not. Both cutoffs and both angles are now computed —
  `f08.cos.hi/lo`, `f08.ang.hi/lo` — and the vector pair that produced `0.9899`
  is gone. The script asserts the **invariant** rather than the two figures:
  the same drop in similarity buys more than three times as much angle near $1$
  as it does in the middle of the range, which is what "cosine is flat near
  zero" means and survives a change of cutoff.

#### Two overfull boxes, and the second is the F6 rule paying off

- **22.0 pt in `main-en`**, from frame 29's run of short unbreakable spans —
  `$\val{}$ when they sit at positions $1$ and $2$, and $\val{}$` has almost no
  break opportunity in it. Split into two clauses with a semicolon and it went
  to zero. Polish had the same sentence and the same fix.
- **21.0 pt in `main-pl` and 12.6 pt in `main-en-a4`, both in the answers
  appendix**, from `\code{math.cos(math.radians(180))}` inside an `\answerto`.
  This is exactly F6's finding — *a back-matter answer is set in a narrower
  measure than the frame it came from, so an unbreakable run that is
  comfortable in a frame overflows in its own answer* — and it was chased
  through three rewordings that each moved the box to a different build before
  the recorded fix was applied: **put it in a display.** One `\begin{center}`
  and it is zero in all four. The rule generalises from formulas to any
  unbreakable run, `\code{}` included, and the rewording detour cost more than
  the fix.

Also worth not repeating: `$\cos 20°$` is a `\textdegree` **in math mode** and
warns rather than errors, so `checklog.py` catches it but a `grep` for errors
does not. Write `^{\circ}` inside maths and keep the bare `°` for the table
cells, where it sits outside the maths.

**One box was chased into a worse one.** Moving `\code{code/f08_trigonometry.py}`
into the middle of a Polish sentence to shift the line breaks put a
24-character `\code{}` at a line end and took a 6.8 pt box to **36.9**. A long
`\code{}` belongs at the start of a sentence, where it starts a line reliably,
or in a display — never in the middle of a long paragraph in the edition with
the longer words.

**The final multiset is element-for-element the pre-F8 baseline** in all four
builds: `[4.1 x 4]`, `[4.1 x 4]`, `[6.3, 4.4 x 4]`, `[4.4 x 4]`.

#### The diagrams

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| F8.1 unit-circle | 630 / 657 | 5.73 | 7.00 | 6.71 | 7.95 | 7.62 |
| F8.2 cosine-angle | 599 / 589 | 6.43 | 7.36 | 7.48 | 8.36 | 8.49 |
| F8.3 rotate-both | 615 / 549 | 5.60 | 7.17 | 8.03 | 8.14 | 9.12 |

`f08-rotate-both` was first drawn at 434 pt, which sets **11.54 pt on A4** and
would have been by some way the largest node text in the book. Widened by
making the nodes wordier, which is the same counter-intuitive fix F4 and F5
both needed and is now three for three: above the aspect-ratio crossover only
the width matters, so the way to make a diagram's type *smaller* is to give it
more to say.

**Rule 2 checked by reading the figures first and then finding them in all four
builds.** Only F8.3 contains an answer to anything the program asks — frame
27's *what can their dot product depend on* — and it is a page later than both
that elicitation and frame 28's answer in every build (fig 261/226/269/229
against elicitation 260/224/267/228). F8.1 and F8.2 carry nothing that is asked
either side of them.

#### Parity: three word-order failures, all the recorded class

C4 diverged three times and each was Polish putting a maths span or a number
where English puts a word — the rule already in *Two editions*, now with three
more instances. `Program~\ref{prog:F04}'s $\sum_i a_i b_i$` against
`$\sum_i a_i b_i$ z Programu~\ref{prog:F04}` is the clearest: same reference,
same sum, opposite order, and C4 reads order. And *tak blisko dokładnej
jedynki* spelled a number as a word, which C12 counts as a missing literal.

One defect the gates caught that a reader would have: rewriting Quiz Q4 from
*Why is $\cos^2\theta + \sin^2\theta = 1$?* — which prints the identity before
frame 1 and disarms frame 5's elicitation — left the **answer** still answering
the old question. C8 failed on it, because the Polish answer stated the
identity and the English one did not.

#### Also done

- The section title *Rotation, and why it encodes a difference* stated frame
  27's finding at the head of the section, three frames early, and is now
  *Rotation, and what it is for*. Two outcomes were reworded on the same rule:
  one printed the Pythagorean identity on the opener, the other promised
  *encode a difference*. **Third pass running that an outcome has had to be
  stripped of its own conclusion** — it is the easiest place in the skeleton to
  leak an answer, because an outcome reads like a promise and writes like a
  summary.
- Frame numbers were remapped after writing, as they must be: the plan's five
  sections were `1--7 / 8--13 / 14--19 / 20--27 / 28--35` and the program's are
  `1--6 / 7--10 / 11--15 / 16--23 / 24--30`. Fifteen quiz routes moved with
  them.

### Program F9 pass, August 2026

**Thirty-two teaching frames, thirty-four printed, both editions**, against a
brief that projected forty. Five sections: what a vector is, length, the dot
product, distance against similarity, and where the picture runs out.

**It is the cheapest program so far by every layout measure**: zero new
overfull boxes in any of the four builds, no stranded openers or headings, no
orphaned cues, and two orphan tails. Parity came back clean on its first run,
which has not happened before. The reason is not luck — it is that F6's
two-sided rule and F8's `\code{}`-placement rule were both applied while
drafting rather than after a build named the box.

#### The payoff is a bridge, and the manifest decided its scope

F9 sits after F8, which had already used $a \cdot b$, $\lVert a \rVert$ and
cosine similarity without defining any of them. So F9's honest job is to
define what F8 borrowed and then pay it back with an identity:

\[ \lVert a - b \rVert^{2} = \lVert a \rVert^{2} + \lVert b \rVert^{2} - 2(a \cdot b) \]

which is F8's $a \cdot b = \lVert a \rVert \lVert b \rVert \cos\theta$
rearranged. On the unit sphere it collapses to $2 - 2\cos\theta$, so **distance
and cosine similarity rank identically and cannot disagree** — confirmed on
13,026 comparisons. Off it they can, and the frames work one triple where the
nearest neighbour is not the most similar.

**That split was decided by reading three briefs, not by taste.** P04 owns
vector spaces, span, independence and basis; P05 owns inner products in
general, projection, L1 against L2, the disagreement case worked out, what
normalising costs, and near-orthogonality in high dimension; P07 owns
broadcasting. What is left for F9 is the arithmetic and **the identity that
says exactly when the two measures cannot differ** — which is a better
possession than the general comparison, because it is provable rather than
empirical. F8's pass had just been burnt by pointing at a P05 that had not
promised what was claimed; checking first is now cheap and it changed the
program's shape.

#### One false claim, caught by reading rather than by any gate

The triangle-inequality trapbox said *for numbers on a line the two sides are
equal, always*. That is false for signed numbers: $3$ and $-4$ give
$\lvert a + b \rvert = 1$ against $\lvert a \rvert + \lvert b \rvert = 7$.
What is true, and is the actual source of the habit, is that **two lengths
laid end to end on a line do measure their sum**, because a length is
positive. Rewritten to say that.

The shape is worth naming because it is the fourth instance: a sentence
justifying a trap by appeal to a simpler setting, written from the feel of the
simpler setting rather than from its arithmetic. F02's `-3**2` box and F04's
momentum claim were the same, and both were also about a claim the author
believed and had not evaluated.

#### Two cross-program claims, both checked and both improved by checking

- **F04 works the identical sum.** F09's dot-product example is
  $1 \times 3 + 2 \times 4 = 3 + 8 = 11$, and F04 line 231 prints exactly that
  while asking whether a sigma distributes over a product. The frame now says
  so, so the two programs are provably quoting one computation rather than
  coincidentally agreeing.
- **F08 named the length and did not define it**, which is narrower than the
  draft's *without saying where it came from* and is what the file actually
  does. Corrected to *named it the length without saying how to compute one*.

Also caught while drafting: frame 2 pointed at *section 6* in a program with
five sections.

#### The diagrams, and the crossover a third time

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| F9.1 list-or-arrow | 648 / 612 | 5.90 | 6.81 | 7.21 | 7.73 | 8.18 |
| F9.2 length-twice | 618 / 621 | 5.62 | 7.14 | 7.10 | 8.10 | 8.06 |
| F9.3 two-questions | 618 / 633 | 3.11 | 7.14 | 6.97 | 8.10 | 7.91 |

`f09-two-questions` was first drawn as a diamond — two nodes converging on one
— and came out **433 pt wide, setting 11.54 pt on A4**, the same hazard F8's
`rotate-both` had. Here the F4/F5/F8 fix did **not** work: making the nodes
wordier changed nothing, because mermaid wraps node text at its own width and
the graph's width was already at that cap. What fixed it was **adding a rank**:
splitting the diamond into a source node plus the two branches plus the join
took it from two columns to three, 433 pt to 618.

So the rule generalises: above the crossover the width is what matters, and
the width is set by the number of *columns* as much as by the text. Wordier
nodes widen a chain; only more ranks widen a graph that is already wrapping.

**Rule 2 checked by content first and then on the page in all four builds.**
Only F9.3 contains an answer to something the program asks — frame 22's *which
has the higher cosine similarity* — and it sits below frame 23's answer
everywhere: en p279 y445 against y227, en-a4 p240 y583 against y346, pl p286
y530 against y241, pl-a4 p245 y409 against y107. F9.1 and F9.2 each restate
the frame they are declared in and answer nothing put to the reader.

#### Also

- Three traps added to `notes/02` (55 to 57): adding a scalar to a vector,
  lengths adding, and *nearest* against *most similar*.
- Frame numbers remapped after writing: plan `1--6 / 7--12 / 13--18 / 19--27 /
  28--33`, program `1--6 / 7--13 / 14--18 / 19--27 / 28--32`. Two outcomes were
  reworded on the now-familiar rule — one named the zero vector, which frame 12
  elicits, and one carried frame 23's finding.
- The `tabularx` two-column table in frame 31 is the program's own summary of
  what transfers and what does not, and it is the honest form of the payoff:
  the brief's *every intuition built in 2-D will have to be tested against high
  dimension in P5* is a hand-over, and the book says so rather than
  manufacturing a measurement it does not own.

### Program F10 pass, August 2026

**Thirty-seven teaching frames, thirty-nine printed, both editions**, against a
brief that projected forty. Five sections: what a set throws away, union and
intersection and the mask, and/or/not, counting without listing, and when a
count becomes a bill.

**The layout result is the pass's headline and it is not F10's doing.** Three
of the four builds now carry **zero** overfull boxes and the fourth carries
one — see the table at the top, and the note under it about where the four
that had been there all along came from.

#### Scope: five programs declare F10 as a dependency

More than any other Foundation program, so the reading-first discipline that
F9 established was the whole of the planning. P12 owns the four counting rules
formally, the pigeonhole principle and the birthday calculation; P14 owns
implication, quantifiers and proof; P03 owns O-notation; P13 owns graphs; P23
owns probability. What is left is genuinely F10's and it is the elementary
layer all five are built on:

- **three counting rules, deliberately three and not four** — product, the
  two-set union rule, and $2^{n}$ subsets. The two-set union rule is in
  because a union is not countable without it; the general inclusion--exclusion
  is P12's.
- **and/or/not as operations**, which is what a mask does, leaving implication
  and quantifiers to P14.
- **the numerator and the denominator**, and the observation that choosing the
  denominator was a decision — leaving what a probability *is* to P23.

That split lets §5 say *the notation for this growth is P03's; the count is
yours now, and it is the more useful half in a design review*, which is a
better sentence than either program could write alone.

#### An assertion caught the author again, and in the direction nobody checks

`code/f10_sets.py` asserted that doubling an all-pairs input multiplies the
work by **just under four**, written before the prose it was for. It failed on
the first run. The ratio is
\[ \frac{\text{pairs}(2n)}{\text{pairs}(n)} = \frac{4n-2}{n-1} \]
which is 4.020 at a hundred and 4.002 at a thousand, and falls towards four
**from above**. A frame quoting "four times" flatly would have been wrong, and
the trapbox now says so and says the assertion failed, because the failure is
the persuasive part.

This is the second time (after F5's softmax range) that writing the assertion
*at the computation, before the sentence it supports* has caught a plausible
number in the same commit that invented it. It is worth treating as the
method rather than as luck.

#### Three claims a reader could have falsified

- **"There is no single word for it"**, of exclusive or. There is: it is
  called exclusive or and most languages have an operator. What is true, and
  is what the frame needs, is that the *three words this section gives you* do
  not include it, so from those it has to be built. Corrected in the frame and
  in the further-problem answer.
- **A borrowed rule, attributed too widely.** The product-rule frame said
  stating the independence condition was *the habit Program F06 made a rule
  of*. F06's rule names division: *state the condition every time you divide
  by a letter*. This is the same move on a different operation, and the frame
  now says that rather than borrowing the rule whole.
- **"about thirty years"** for $2^{30}$ seconds, which is 34. Now *over thirty
  years*, which is what the reader's own arithmetic will support.

#### Rule 2 caught two figures, both by reading rather than by measuring

- `f10-set-and-mask` sat in frame 12 and **frame 13 asks the reader to tell a
  set from a mask** — which is what the figure says. Moved below the answer,
  to frame 14.
- `f10-three-growths`'s third node said *twice as many items gives four times
  as many pairs*, and **frame 31 asks exactly that**. The node now states
  frame 30's rule (a pair is one thing named twice, so the product halves)
  instead of frame 31's answer.

Neither needed a page measurement to condemn: reading the figure against the
frames on either side of it was enough, which is the order the F03 second
review pass prescribes and is much cheaper than the alternative.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| F10.1 set-and-mask | 624 / 599 | 5.68 | 7.07 | 7.36 | 8.03 | 8.36 |
| F10.2 overlap | 570 / 588 | 6.12 | 7.74 | 7.50 | 8.79 | 8.52 |
| F10.3 three-growths | 639 / 657 | 5.03 | 6.90 | 6.71 | 7.84 | 7.62 |

#### The orphaned cue: trimming measured as a no-op, lengthening cleared it

Three orphaned cues arrived — one in `main-en-a4` and two in `main-pl-a4` —
and this pass ran the experiment F6 could only do once. **Both editions' three
frames were trimmed first**, by a clause each, and all four builds were
rebuilt: the three cues came back on the *same three pages*. Then the same
three frames were **lengthened** by a paragraph each, and all three cleared.

That is a second confirmation of F6's finding with the failed half measured
rather than argued: trimming a frame whose tail hangs over a page boundary
pulls the previous frame's material up to fill the gap, so the page stays full
and the tail stays where it was. Lengthening pushes the question, the dots and
the cue over **together**, which is what was wanted.

The paragraphs added were made to earn their place rather than pad: that set
operations compose because each returns a set; that an English requirement
containing *or* has to be read twice; and that a grid's constraint is usually
enforced somewhere further in, so the count is wrong from the start and the
discovery arrives runs later.

#### Also

- Five traps added to `notes/02` (58 to 62): corpus against vocabulary, two set
  sizes adding, De Morgan on a filter, $2^{n}$, and twice the data being four
  times the work.
- Two long `\code{}` runs went into displays, one of them in an `\answerto` —
  the F6 rule, now applied on sight rather than after a build named the box.
- `\val{f10.fault.frac}` was emitted and then removed: the frame's point is
  that a naive probability is **two counts and a division**, so the page builds
  $\frac{\val{f10.faults}}{\val{f10.docs}}$ from the two counts it already has
  rather than being handed a third number to trust. C7 found it, because a
  non-numeric value is written with `\mfavaltext` and the value ledger scans
  for `\mfaval` — worth knowing before emitting another text value.
- Frame numbers remapped after writing: plan `1--7 / 8--14 / 15--21 / 22--29 /
  30--35`, program `1--7 / 8--15 / 16--22 / 23--30 / 31--37`.

### Program F11 pass, August 2026

**Thirty-five teaching frames, thirty-seven printed, both editions**, against a
brief that projected forty-five. Five sections: a change divided by a change,
shrinking the chord, what a machine does when you shrink $h$, reading a
derivative, and walking downhill.

The brief's payoff is *gradient descent has a mechanism, and the reader has
seen it before meeting the word*, and §5 delivers it as a consequence rather
than as an announcement: downhill is against the sign of the derivative, so
$x \leftarrow x - \eta f'(x)$ is what the definition says to do, and there is
nothing else in it.

#### Scope, again decided by reading

F12 owns the four rules and the chain rule; P15 the gradient; P17 curvature and
the step-size bound; P19 convexity; P20 the optimisers; P01 floating point. So
F11 derives **two** derivatives from the definition, gets a constant and a
line for free, lays the four results in a table, and then says explicitly:
*there is a pattern in there and you may well have spotted it; do not go
looking for the general rule yet.* Noticing it is what makes F12's statement
of it land, and stating it here would spend F12's opening.

#### An assertion caught a fudge before the prose existed

`code/f11_derivative.py` first checked whether the gradient-descent walk had
*converged* in sixty steps and compared that against $\lvert 1-2\eta \rvert <
0.85$. It failed at $\eta = 0.08$ and deserved to: it conflated **converges**
with **converges fast enough to notice**, and 0.85 was a threshold picked to
make the two agree. What is actually true is the recurrence
\[ x - 3 \;\longleftarrow\; (1 - 2\eta)(x - 3) \]
so that is what is asserted now — one step at a time, then compounded over
sixty, at three hundred values of $\eta$. Third pass running that writing the
assertion *at the computation, before the sentence it supports* has caught
something, and the first time it caught a **fudge factor** rather than a wrong
number. Worth naming as its own failure mode: a threshold chosen so an
assertion passes is not an assertion.

The corrected recurrence then produced the best thing in the program, which
was not planned. At $\eta = 0.1$ and $\eta = 0.9$ the factor is $+0.8$ and
$-0.8$, so one walk crawls down one side and the other jumps the minimum every
single step — and **after eight steps they are at the same number to the
digit**. That is a consequence of the algebra, not a coincidence, and it makes
$\eta = 1.1$'s divergence obvious before it is computed.

#### The U-curve is the program's best measurement

The whole seventeen-row sweep is a committed transcript rather than a table,
because the shape is the argument and five rows would let a reader think the
middle was interpolated. The error falls as the mathematics says (it is $h$
itself), bottoms out at **3.6e-08 at $h = 10^{-8}$**, and climbs back to
**6.0** at $h = 10^{-16}$ — where $3 + h$ *is* $3$ and the quotient is exactly
zero.

The frame that follows it claimed the turning point moves with the size of the
numbers being subtracted. That was a mechanism argument, so it was **measured**
rather than left as one: the same sweep at $x = 3000$ puts the best $h$ at
$10^{-5}$, a thousandfold move. F11 hands the *reason* for the right-hand
branch to P01, whose subject it is.

#### Three claims a reader could have falsified

All three were pointers, and all three were checked against the manifest:

- *Program F12 \dots proves that they compose.* F12's brief undertakes four
  rules and one composition rule; proving they compose is not in it. Now
  *adds the one rule for differentiating a function of a function.*
- *Which kind of stationary point it is \dash{} Program P17 supplies it.*
  Neither F12 nor P17 undertakes the one-dimensional classification by name.
  The frame now says what is true: it takes the derivative of the derivative,
  which F12 gives the rules for and P17 turns into a statement about
  curvature.
- The crossover claim above, now a measurement.

#### The orphaned cue, and lengthening confirmed a third time

Two arrived, both in `main-en`, and both were cleared by **lengthening** —
which is now the first thing to reach for rather than the second. The first
addition earns its place particularly well: frame 3 now shows that the chord
from $3$ to $6$ has slope $9$ where the chord from $3$ to $5$ has slope $8$,
so the number was never a property of the curve *at* a point, which is what
forces the question the program exists to answer. (The numbers were chosen to
avoid $7$ and $6$, which frames 7 to 10 elicit.)

Note the random walk in action: the first lengthening cleared the cue at
frame 3 and moved a different one to frame 32, which the second cleared.
Fix them in document order and rebuild all four after every edit.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| F11.1 chord-to-tangent | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| F11.2 two-errors | 609 / 623 | 3.33 | 7.24 | 7.08 | 8.22 | 8.04 |
| F11.3 sign-and-size | 627 / 637 | 6.73 | 7.03 | 6.91 | 7.99 | 7.85 |

`f11-two-errors` was first drawn as a diamond at 408 pt, setting **12.25 pt on
A4**. The F10 fix applied unchanged: add a rank, 408 pt to 609. That is now
twice, so the rule is settled — **wordier nodes widen a chain; only more ranks
widen a graph that is already wrapping.**

#### Also

- Four traps added to `notes/02` (63 to 66): the derivative not being a chord
  slope, smaller $h$ not being better, a zero gradient not being a minimum,
  and a large gradient not meaning a long way to go.
- **Three C4 word-order divergences, all the same shape**, and all three were
  `Program~\ref{...}'s <maths>` against `<maths> z Programu~\ref{...}`. That
  is now so reliable it is worth checking for while translating rather than
  after: any English possessive attached to a reference will invert in Polish.
- A 24-character `\code{}` mid-paragraph gave **67.2 pt** in `main-pl` and
  49.8 in `main-pl-a4` while English was clean — the F6 latency rule. Moved to
  the start of its sentence in both editions.
- Six emitted values went unused because the transcript already carries every
  row; C7 reported them and they were removed rather than referenced. A
  transcript makes per-row values redundant by construction.
- Frame numbers remapped: plan `1--7 / 8--15 / 16--22 / 23--30 / 31--38`,
  program `1--6 / 7--15 / 16--20 / 21--26 / 27--35`. Two outcomes were reworded
  on the usual rule.

### Program F12 pass, August 2026

**Thirty-one teaching frames, thirty-three printed, both editions**, against a
brief that projected fifty-five and called this the longest Foundation program
for a reason. It is not the longest, and the reason it is not is worth
recording: the brief was written before F05, F07 and F11 existed, and each of
them has since taken a piece of what F12 would otherwise have had to do. F05
established that a network is a composition; F07 measured the saturation; F11
supplied the limit definition and four worked derivatives and then said
explicitly that the pattern in them is F12's to state. **A brief's frame
estimate is a planning figure from before its neighbours were written**, and
this is now the fourth program where the written length came in well under it.

#### The hinge, and what it took to reach it

The chapter reaches
\[ \frac{\mathrm{d}y}{\mathrm{d}x} = \prod_{k=1}^{n} w_k\,\sigma'(z_k) \]
in five frames from the chain rule, and then says the sentence: **backpropagation
is the chain rule applied to a composition of layers, with the intermediate
values kept rather than recomputed, and there is nothing else in it.** Both of
the consequences people learn the hard way fall straight out of the same
expression — activations must be stored, and a deep weight's gradient contains
every factor between it and the loss.

#### A cross-programme drift gate, and it is new machinery

F07 measured that a saturated logistic answers with about a hundredth of its
centre response and committed `f07.slope.ratio6` = 101. F12 needed the same
figure to turn one flat layer into a product of forty, and rather than quoting
it, **`code/f12_chain_rule.py` computes it from scratch and asserts the two
agree**, reading F07's committed value out of `figures/values/f07.tex`.

That makes *the same computation quoted twice* a gate rather than a claim:
break either program's arithmetic and `make numbers` fails and names both.
The repository had no such check before — `make verify` compares a script
against its own output, and nothing compared two programs against each other.
**It is three lines and it should be used wherever one program quotes
another's number.**

#### Every rule checked against a derivative obtained without it

The four rules and the chain rule are each compared with a central difference
at $h = 10^{-5}$ — near the bottom of the U-curve F11 measured — over two
hundred points. Worst disagreements: $\val{}$ of order 1e-9 to 1e-11.

That is F11's measurement paying for itself one program later. F11 showed a
finite difference makes a bad *definition*; this program uses it as an
excellent independent *check*, with the step chosen where the U-curve is low
rather than as small as possible.

#### The two bounds, and their asymmetry

- **Vanishing.** $\sigma' \le \frac14$ everywhere, exactly, because
  $\sigma(1-\sigma)$ is a product of two numbers adding to one. So forty
  layers at unit weight give at most $0.25^{40} = 8.3 \times 10^{-25}$ — *at
  their very best*, which no trained network is. At F07's saturated point the
  product is $4.8 \times 10^{-105}$, which underflows to exactly zero long
  before layer forty.
- **Exploding, with a sharp threshold.** The factor is $w\sigma' \le w/4$, so
  **a logistic chain cannot amplify at all unless $\lvert w \rvert > 4$.** The
  two failure modes are not symmetric: vanishing needs nothing but depth,
  exploding needs a specific weight. That is a checkable statement and the
  frames make it the section's second result rather than a footnote.

#### One claim that overreached, and one filename

- The draft said *deep networks have vanishing gradients* was **already false
  when this argument was first published**. It was not: the analysis was made
  about networks that were deep sigmoid chains. What is true is that each of
  the three changes the frame lists — $\relu$, residual paths, normalisation —
  was adopted partly because it stops being true. Corrected in both editions
  and in the summary.
- **F12 was written to the wrong filename** and the build did not notice:
  `structure.tex` includes `F12-chain-rule`, and thirty-one frames went into
  `F12-differentiation-rules.tex`, which nothing reads. Every gate passed —
  parity compares the pair, `check_structure` reads the files it is given —
  and the tell was the **page count not moving**. Renamed to the manifest's
  name, which is the single source. Check the manifest's `file` field before
  writing, and treat an unchanged page count as a failed build.

#### Layout

Three of the four builds carry no overfull box; the fourth carries the known
F1 one. Three boxes were cleared, all recorded classes: a long unbreakable
maths span inside a further-problem answer (into a display, the F6 rule), and
**two diagram-manifest lines in Polish** — `\mermaidfig`'s third argument is
manifest copy set in a narrow indented column and is longer in Polish, which
is F02's finding and its third recurrence. Shorten the Polish third argument,
always.

One orphaned cue, cleared by lengthening, and the added paragraph earns its
place: it says why the frame asks for the *best* case rather than a realistic
one — a best case is a bound, so a hopeless one settles the question without
needing to know where any unit sits.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| F12.1 product-not-product | 627 / 615 | 4.94 | 7.03 | 7.17 | 7.99 | 8.14 |
| F12.2 composition-chain | 615 / 643 | 6.61 | 7.17 | 6.85 | 8.14 | 7.78 |
| F12.3 factors-multiply | 635 / 657 | 6.82 | 6.95 | 6.71 | 7.89 | 7.62 |

`f12-product-not-product` was first drawn with **four** ranks and came out
860 pt wide, setting 5.12 pt — below the book's band and near F1.1's 4.32.
That is the opposite failure from F9's and F11's diamonds, and it completes
the rule: **three ranks is the sweet spot at this measure.** Two is too narrow
and four is too wide.

#### Parity: six word-order divergences in one program

Four of the recorded `Program~\ref{...}'s <maths>` class, and **two of a
second class worth naming: a number spelled as a word.** *dwójki się skracają*
for *the $2$s cancel* and *z samych jedynek* for *a path of $1$s* both drop a
maths span and a numeric literal, so C8 and C12 both fire. Polish reaches for
the word far more readily than English does, and the rule is the one already
in this file: **a digit stays a digit.**

#### Also

- Four traps added to `notes/02` (67 to 70).
- Frame numbers remapped: plan `1--8 / 9--16 / 17--26 / 27--34 / 35--42`,
  program `1--6 / 7--13 / 14--20 / 21--25 / 26--31`. Two outcomes were
  reworded on the usual rule, and two editing slips were caught while
  remapping — an `\ans{}` that quoted an unrelated value, and a fragment of a
  deleted sentence left in a frame.

### Program F13 pass, August 2026 — the Foundation part is complete

**Twenty-two teaching frames, twenty-four printed, both editions**, against a
brief that planned twenty and said so as a design decision rather than an
estimate. Five sections: adding up many small pieces, the notation, the two
directions, a density, and a weighted average.

**The layout cost was nothing.** Zero new overfull boxes in any of the four
builds on the first attempt, no stranded openers or headings, no orphaned
cues, and the orphan-tail count did not move. That has not happened before,
and the reason is that the four recorded rules — lengthen rather than trim, a
long `\code{}` at a sentence start, a long span inside an `\answerto` into a
display, Polish manifest copy kept short — were applied while drafting.

#### The frame band had to learn about a deliberately short program

`check_structure.py` held every program to 30–70 frames, and F13 is planned at
twenty **on purpose**: the curriculum review cut it from forty-five and its
brief says *substitution, parts and partial fractions are excluded
deliberately and by name... twenty frames rather than forty-five, and the
difference is the point.* Padding it into the band would mean writing the
material the scope excludes.

So the band is now **taken from the manifest** when a program plans fewer
frames than the band's floor: such a program must land within a quarter of its
own plan. That is a real check rather than a waiver — F13 at 22 passes its
15–26 band, and at 40 or at 12 it would still fail, which was verified by
running the function on both. Read from `tools/programs.json`, so a curriculum
change moves the check with it.

**The general lesson: when a gate and a deliberate decision disagree, the gate
should learn the decision's own criterion, not be switched off.** A hard-coded
exception for F13 would have been one line and would have stopped being true
the next time a program is planned short.

#### The measurement is a convergence rate, not a convergence

Right-hand rectangles under $x^{2}$ over $\intcc{0}{1}$ give
$\val{}$ 0.385, 0.33835, 0.333834, 0.333383 — heading for $\frac13$. Four rows
suggesting a limit is weaker than what is actually available: the sum of the
first $n$ squares has a closed form, so the total is **exactly**
\[ \frac{1}{3} + \frac{1}{2n} + \frac{1}{6n^{2}} \]
and the script asserts that identity at four sizes rather than asserting that
the numbers look like they are going somewhere. The frames can then say *how
fast* — the error halves each time $n$ doubles — which is a claim a reader can
check on the table in front of them.

#### The trap is a category error, not an approximation

A density's **height** is not bounded by one; its **area** is. The uniform
density on an interval of width $0.1$ has height $10$, and narrowing the
interval raises the height without limit while the area stays $1$. So $p(x)$
is probability *per unit of $x$* — a rate, as a speed is not a distance — and
a likelihood a library prints above one is not a bug.

That is Program F10's count-against-denominator point in its continuous form,
and the two frames say so.

#### One claim a reader could have falsified

The notation frame said $\sum_{i=1}^{n} f(x_i)\,\Delta x$ was
**Program F04's**. F04 has the sigma and does *not* have the $\Delta x$ — it
writes $\sum_{i=1}^{n} x_i$ and $\sum_{i=1}^{n} a_i b_i$, and a Riemann sum's
width is new here. The frame now says which half is F04's, which is both
accurate and more useful. Fifth pass running that a claim about another
program was the thing that needed fixing.

#### What F13 deliberately does not say

It never says what a probability is. Three programs declare F13 as a
dependency — P23 (probability as a measure, Bayes), P24 (random variables,
expectation and variance) and P19 (convexity and Jensen) — so F13 supplies the
accumulation, the area, the density and the **shape** of a weighted average,
and hands over every object those shapes turn out to be about. Its last frame
writes $\int x\,p(x)\,\mathrm{d}x$, says it has a name, and declines to use
it, because naming it would need three words the book has not defined.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| F13.1 sum-to-integral | 652 / 600 | 7.00 | 6.76 | 7.35 | 7.68 | 8.35 |
| F13.2 height-not-area | 645 / 657 | 5.87 | 6.84 | 6.71 | 7.76 | 7.62 |
| F13.3 weighted-average | 657 / 621 | 7.06 | 6.71 | 7.10 | 7.62 | 8.06 |

#### Also

- Three traps added to `notes/02` (71 to 73): a density's height read as a
  probability, `dx` treated as notation, and an integral confused with an
  antiderivative.
- Two parity divergences, both the recorded classes: a number spelled as a
  word (*dziesięciokrotnie* for `$10$`), and one `\mfavaltext` value that C7
  reported unused — `1/3` is arithmetic the reader does, so the page writes it
  rather than referencing it. The F10 finding, applied on sight.
- Frame numbers remapped: plan `1--5 / 6--9 / 10--12 / 13--17 / 18--20`,
  program `1--5 / 6--9 / 10--12 / 13--17 / 18--22`.

### Program P1 pass, August 2026 --- Part II begins

**Thirty-five teaching frames, thirty-seven printed, both editions**, against a
brief that projected forty-five. Five sections: scientific notation in base
two, the gap growing with magnitude, order changing the answer, one width and
two splits, and two floors rather than one.

The layout came back to the pre-P01 baseline exactly \dash{} `[]`, `[]`,
`[6.3]`, `[]` \dash{} with no stranded openers, no stranded headings and no
orphaned cues. Two orphan tails were added.

#### Reading the neighbour's brief cut the program's best demonstration, correctly

The draft's centrepiece was a million small contributions summed into a running
total in both orders, with the loss printed. It demonstrates well and **it is
not P01's**: P02's brief undertakes *why summing a million small gradients in
the wrong order loses them*, along with cancellation, Welford and the catalogue
of fixes. Writing it here would have spent P02's payoff and left P02 repeating.

What *is* P01's is the **threshold underneath that loss**, because it is a fact
about the encoding and follows from the gap table the program has already
built: under round-to-nearest, a contribution below **half the gap** at the
running total moves nothing at all. Not *loses precision* \dash{} moves
nothing. `1.0 + 1e-17 == 1.0` is `True`, and the threshold is half an epsilon
of the total, so it is a fixed *fraction*: $\num{6.0e-08}$ in `fp32`,
$\num{3.9e-03}$ in `bf16`.

That is the F07/F12 split applied one part later \dash{} F07 owned the shape of
saturation and F12 owned the compounding \dash{} and it makes the section
better rather than shorter, because a threshold is provable where an
accumulated loss is a demonstration.

**No manifest amendment was needed, and that is the point.** The manifest was
right and the draft was wrong; checking cost one file read.

#### An assertion that passed on a difference the page could not show

The cut demonstration failed before it was cut. With `TINY = 1e-10` the two
summation orders printed **the same ten decimal places**, because the gap at
$1$ is $\num{2.22e-16}$ and $10^{-10}$ sits comfortably inside it, so nothing
was lost. `assert forward != backward` passed on a difference invisible to a
reader.

**An assertion on the underlying floats is not an assertion about what the
reader will read.** Where a frame's argument is that two printed numbers
differ, assert on the printed strings. The rule is now in
`code/p01_floating_point.py` at the computation it came from.

#### The cross-programme drift gate caught a live disagreement, first time out

F12 introduced the mechanism \dash{} a script reading another program's
committed value and asserting agreement. P01 has four such gates, and one of
them fired on P01 itself.

**P01 made the `fp64` coin-flip cliff 1074 where F03 had committed 1075**, and
`fp32` 149 against 150. Both statements are true and they count from opposite
sides of the same boundary: the largest $n$ with $\num{0.5}^{n}$ still
representable, against the first $n$ at which the product is zero. Printing
them two hundred pages apart would have put two numbers in the book that look
like one and are not \dash{} F08's defect, at a distance no reader could
reconcile. F03 asks *after how many tokens is the product exactly zero*, so
that is the definition P01 adopted, and the script now checks it against F03's
value rather than merely resembling it. The other three gates cover F03's four
format thresholds, F03's sequence probability and F12's underflowing product.

**Use this wherever one program quotes another's number.** It is three lines
and it is the only thing in the repository that compares two programs against
each other; `make verify` compares a script against its own output and would
not have seen any of it.

#### A vacuous assertion, and the program's best demonstration hiding inside it

The F03 gate was written as `_f03 < smallest_subnormal(...)` and passed for
every format \dash{} **vacuously**, because `float("2.43e-2085")` returns
`0.0` in Python, and zero is below every floor.

The failure to parse *is* the finding. F03's committed number **cannot be read
back into a double at all**, which makes it the one computed value in this book
that a reader cannot paste into a prompt and inspect \dash{} and it is exactly
why F03 computed it as a logarithm and never as a product. The gate now
compares the decimal exponent parsed out of the string, never the float, and
asserts `float(...) == 0.0` so the day that changes the build says so.

**A comparison against a value that silently became zero is not a comparison.**
It is the same shape as F03's rounded-`log10` guard, which could not fail
within a few hundred ulp.

#### Six wrong numbers in the draft, all found by dividing what was printed

None was caught by any gate. Every one was caught by re-reading the draft
against arithmetic, and every one is now computed and asserted rather than
written from expectation.

- **The `aibox` argued the opposite of what it printed.** Two validation losses
  differing by $\num{1.7e-6}$ were called *smaller than epsilon at that
  magnitude*, which is $\num{2.7e-7}$. They differ by six gaps. The pair is now
  emitted with the gap beside it and an assertion that the difference is
  smaller.
- **"About a million times larger"** for the gap at a billion against the gap
  at $1$. The ratio is $\num{5.4e8}$.
- **"Each row is about a million times the one above it."** The first step is
  $512$; only the second is a million. The frame now defers the quantitative
  claim to the next frame, which states it correctly with the factor-of-two
  binade caveat.
- **The decimal-digit counts were one too high in two rows.** An epsilon of
  $\num{7.81e-3}$ is about **two** decimal digits, not three. Now
  `round(-log10(eps))`, emitted per format.
- **"About one epsilon"** for the error in `0.1 + 0.2`. It is *exactly one gap
  at $\num{0.3}$*, which is a quarter of the gap at $1$ \dash{} and quoting a
  gap without the magnitude it sits at is the precise mistake the same section
  warns against. Asserted equal to `math.ulp(0.3)`.
- **"A fortieth of a per cent"** for `bf16`'s swamping threshold, which is
  $\num{0.39}$ per cent, sixteen times larger. Now emitted as a percentage.

And one notation error of the same family: `\intcc{2^{29}}{2^{30}}` for the
range over which a coincidence holds, where $2^{30}$ is precisely the point at
which the binade changes and the gap doubles. `\intco` exists and is what was
meant.

**The rule this pass earned: a claim of the form *X is about N times Y* is a
division, so do the division.** Four of the six were that shape.

#### The coincidence worth keeping, and the assertion that stops it generalising

Half a double's gap at a billion is **exactly** half an `fp32` epsilon, to the
bit. A billion falls in the binade starting at $2^{29}$, and $29$ is precisely
the difference between the two significand budgets, $52 - 23$.

It is a property of that magnitude and not a law, so the script asserts both
halves: that the two are equal at $10^{9}$, **and that they are not equal at
$10^{10}$**. The second assertion is what stops a true sentence becoming
folklore, and it is worth copying wherever the book prints a coincidence.

The sentence it buys is the whole subject in one line: *a double counting near
a billion is as coarse as a float counting near one.* Precision is a property
of a format and a magnitude together, never of a format alone.

#### Three transcripts, and one of them exists because a console line was typed

The draft carried *ask Python for `float("2.43e-2085")` and it returns 0.0* as
prose. That is the fabricated-console-block shape with a claim standing in for
a run, in the program whose stated method is that a claim about what the
machine stores is settled by asking it. It is now `p01-underflow.txt`,
generated, committed, gated, and it does a second job \dash{} the two lines
under it bracket the floor by multiplying rather than by parsing.

Replacing it also cleared the only remaining parity warning, because the Python
string literal took a straight double quote into Polish prose, where C10 wants
`\enquote{}`. **A `"` inside `\code{}` in the Polish edition is a warning with
no correct silencing**; the fix is to move the code into a transcript, where it
belonged.

All three transcripts were extracted from the finished files and executed, and
all three reproduce exactly. The width guard is 64 characters, taken from the
widest listing line already in the book, and **it fired on two of its first
three runs** \dash{} which is the only way to know a new check is looking at
anything.

#### The one new overfull box was a Polish table HEADER

$\num{9.9}$ pt in `main-pl` alone, from a header cell reading *odległość do
następnej liczby podwójnej precyzji powyżej* \dash{} 51 characters where the
English is 33.

F05 recorded that a `\val{}` numeric column costs about 70 pt and that some
tables simply cannot fit. This is the same finding one cell over: **the header
is as capable of overflowing a `tabular` as the data is, and it is longer in
Polish by a wider margin than the prose is.** Shortened, and the multiset came
back to the baseline in all four builds.

#### `notes/05-floating-point-plan.md` is F1's plan, and this file said it was P01's

It is F01's frame-by-frame plan; its §1 is the F1/P1 *boundary* decision, which
is why the filename mentions floating point. Corrected below.

**And its §1.3 records a commitment the written F01 does not contain.** The
plan says F01 frame 32 plants *a float is normalised scientific notation in
base 2 on a fixed digit budget* for P01 to cash. Nothing of the sort is in the
written F01: what F01 has is its `Scientific notation` section, plus the
base-two trapbox on $\num{0.1}$ and the `aibox` handing `bf16`/`fp16` to P01.

So P01 builds the bridge itself, and it is better for it \dash{} F01's
section is written, rich and quotable ($m$ carries the precision, $e$ carries
the size), so P01's opening move is to change the ten to a two and cap the
mantissa's digits, and everything else follows. **The written program is the
authority and a plan document is not**, which is the same rule this file states
for briefs.

#### The trap catalogue's item 1 was stale in the direction nobody checks

It routed the *whole* of the summation story to P01, including the accumulated
loss that P02's brief undertakes by name. Corrected to name the split, with the
reason. Items **74 to 79** were added out of writing P01, under a new heading
of their own, on the Foundation section's pattern.

#### The diagrams

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P1.1 three-fields | 657 / 657 | 7.06 | 6.71 | 6.71 | 7.62 | 7.62 |
| P1.2 same-width | 657 / 657 | 2.82 | 6.71 | 6.71 | 7.62 | 7.62 |
| P1.3 two-floors | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six hit mermaid's own wrap cap at 657 pt on the first render, which is
where a third of the book's figures already sit, so no redesign was needed.

**Rule 2 checked by content first and then on the page.** Only `p01-two-floors`
contains an answer to something the program asks \dash{} frame 27's *what is
below the smallest normal* \dash{} and it sits below frame 28's answer in all
four builds, measured: elicitation at y197/219/238/205, answer at
y291/317/331/303, figure caption at y522/570/560/556, all on one page.

#### Also

- Frame numbers remapped after writing, as always: sections landed at
  `1--6 / 7--12 / 13--19 / 20--26 / 27--35` against a plan of
  `1--7 / 8--14 / 15--21 / 22--30 / 31--38`. Nine quiz routes, six outcomes and
  fourteen summary brackets moved with them, and **two quiz routes were
  swapped** by a careless ordered replace \dash{} caught by reading the printed
  list, which is worth doing after any bulk remap.
- Four parity divergences, all recorded classes: two numbers spelled as words
  (*jedynką* for `$1$`, *zerem* for `$0$`) and two references sitting behind
  their maths. The `Program~\ref{...}'s <maths>` inversion is now so reliable
  that it is worth fixing while translating.
- `p01.fp16.max` is $\num{6.55e4}$ and `p01.fp16.max.exact` is $65504$, under
  two names on purpose: the quiz asks *roughly how large* and the frame asks
  for the number, and printing a rounding beside the thing it rounds is F08's
  defect.
- Four emitted values went unreferenced and were cut rather than forced into
  the prose; one more, `p01.fp64.max`, earned a sentence instead \dash{} a
  double spans over six hundred orders of magnitude, which is why it rarely
  makes you think about either end.

### Program P2 pass, August 2026

**Thirty-seven teaching frames, thirty-nine printed, both editions**, against a
brief that projected fifty. Five sections: an algorithm correct in exact
arithmetic, what a subtraction costs and compounds to, the exponential's two
cliffs, never forming a probability, and adding a great many numbers.

Seventh program under its brief's estimate, and the reason is a new one.
**F03 and F07 had already spent the derivations.** F03 derives the two-term
log-sum-exp identity in full and F07 states in a warning box that subtracting
the maximum is an *identity and not a trick*. A P02 that re-derived either
would have been repeating. What was left is the better half and it is what the
two of them explicitly deferred: **which** pivot, and what the wrong one costs.

#### An assertion caught a false claim, and the failure is the frame

`code/p02_numerical_stability.py` asserted that only the maximum keeps every
term of a log-sum-exp inside `fp16`. It failed on the first run: **three of the
five pivots survive** on an ordinary row, because `fp16` tolerates a shortfall
of up to $\num{11.09}$ between the largest score and the pivot.

The failed claim is a worse frame than the true one. A pivot $c$ is safe
exactly when $\max z - c \le \ln(\text{ceiling})$, so whether a non-maximal
pivot works is **a property of the data**. The maximum is the only choice that
is safe for every row, every spread and every format, because it makes the
shortfall zero. Everything else runs through a test suite, through a review and
into production, and then meets the batch that does not.

That is what \enquote{numerically stable} means as a technical term, and the
measurement is what makes the sentence land: not *more accurate*, but *safe for
inputs you have not tried*. Sixth pass running that writing the assertion at
the computation, before the prose it supports, has caught something.

#### Two data choices that had to be searched for rather than reasoned to

- **The negative variance needed the right offset.** The first draft used
  readings near $10^{9}$, on the reasoning that a bigger offset cancels harder.
  It cancels so hard that every reading rounds to the same `fp32` value \dash{}
  the gap there is $64$ \dash{} and the formula returns exactly $0.0$, which
  demonstrates nothing. The offset has to be large enough for the squares to
  cancel and small enough for the readings to stay distinct. A sweep found
  $30\,000$: five readings a microsecond apart, and the one-pass formula
  reports $-64$.
- **And $-64$ is exactly one `fp32` gap** at the magnitude of the quantities
  being subtracted, which is the smallest non-zero answer the subtraction could
  have given. The draft said *a multiple of the gap*; it is one, and saying so
  is both checkable and a better sentence.

#### A tolerance that was wrong about the method rather than the data

The summation section asserted that every fix lands within $10^{-5}$ of the
exact total, and **sorted failed it**: smallest-first recovers
$\num{99.6733}\%$ of a million $10^{-8}$ values, not all of them, because a
million roundings into a growing total drift in a shared direction.

Scoring the fixes pass/fail would have hidden the interesting half. The
assertion is now the **recovered fraction** plus an ordering \dash{} Kahan and
pairwise must beat sorting \dash{} and the frames can say the honest thing:
sorting fixes the catastrophe and leaves the drift, it is the cheapest fix and
the weakest, and it is the one most often called sufficient.

#### A fabricated console line, and a cross-check that was too narrow

The draft's cliff transcript printed `162754.796875` for
`float(np.exp(np.float32(12)))`. A direct run gives **`162754.78125`**: the
draft had interpolated `f32(math.exp(12))`, which is the *fp64* exponential
rounded to `fp32`, where numpy computes the exponential *in* `fp32`. Two
different computations under one label, in the program about not trusting what
a number looks like.

The script already carried a numpy cross-check. **It did not cover that line.**
A cross-check is only as wide as what it checks, and the tell was noticing that
the committed transcript and a direct run disagreed. The line is now plain
`math.exp`, which needs no numpy and is exactly reproducible, and every
remaining numpy claim in both transcripts is asserted.

**Every transcript line is also wrapped in `float()` on purpose.** numpy 2
reprs a scalar as `np.float32(-64.0)` where numpy 1 printed `-64.0`, so a
transcript quoting either is a claim about a numpy version rather than about
the arithmetic \dash{} F03's `np.logspace` defect in a new coat. `float()`
returns a plain Python float whose repr is stable, and it is what anybody
comparing two of these would type.

#### Three build traps, and two of them are new to this repository

- **`float()` accepts `inf`, `-inf` and `nan`.** Both scripts classified an
  emitted value as numeric by a bare `try: float(body)`, so `-inf` was written
  as `\mfaval` and `\val{}` handed it to siunitx, which answers
  `Package siunitx Error: Invalid number '-inf'` **and writes a PDF over the
  top**. Eight errors, no PDF anybody should ship. The guard is
  `math.isfinite`, and it is now in both scripts. Latent in P01 and fatal in
  P02, which is the same shape as the `amssymb` trap.

  The follow-up is better than the fix: `-inf` is a **name**, not a computed
  number, so it does not belong behind `\val{}` at all. The page writes
  `\code{-inf}`.

- **The four-figure rounding of the largest double is not a double.**
  `f"{1.7976931348623157e308:.4g}"` is `1.798e+308`, which is *larger* than the
  largest double and parses straight back to `inf` \dash{} which is how the
  `isfinite` guard found it, in P01, after P01 had shipped. A ceiling printed
  above the ceiling is wrong in precisely the way that program is about.
  `printed_ceiling()` truncates towards zero instead, and asserts
  $0 < \text{float(printed)} \le \text{true max}$ for every format.

- **`make ... > log 2>&1; echo "EXIT $?"` in a background task reports exit
  0.** The task notification carries the *compound* command's status, which is
  the echo's. A build that failed with `make: *** Error 12` was reported as
  complete, and the page counts for three of the four formats had silently not
  moved \dash{} which is F12's tell arriving through a different door. **Read
  the log's own exit line, and treat an unchanged page count as a failed
  build.**

#### P01 shipped a claim this pass falsified

Correcting P01's ceilings turned up a sentence that was already wrong:
\code{bf16}'s ceiling and \code{fp32}'s were said to be *the same, to three
figures*. They are $\num{3.39}$ and $\num{3.40}$ \dash{} the same to **two**.
The largest value of a format is $(2 - 2^{-m}) \times 2^{127}$, so
\code{bf16}'s shorter significand makes its ceiling $\num{0.39}$ per cent
lower. Both editions now say that, which is more accurate and more
instructive; the shared exponent budget was always the point.

Same rule as ever, and the fifth time it has paid: **divide the two numbers as
the page prints them.**

#### Six more claims a reader could have falsified

- **The `aibox`'s two validation losses argued the opposite of their own
  figures**: a difference of $\num{1.7e-6}$ was called smaller than the gap at
  that magnitude, which is $\num{2.7e-7}$. It is six gaps. The pair is now
  emitted with the gap beside it and an assertion that the difference is the
  smaller.
- **The signed underflow value was used as a magnitude**, twice \dash{} *once
  the gap exceeds $-16.6$* is not a statement. `p02.drop.fp16` is the positive
  number, under its own name.
- *Less than one part in $10^{5}$* for a term that survives max-subtraction; it
  is under $6 \times 10^{-8}$ of the largest.
- *A million values pass through about twenty additions* conflated **depth**
  with count: the count is unchanged at a million, the depth is twenty, and it
  is the depth that bounds the drift.
- *Pairwise summation is the default in most array libraries* is a claim about
  releases. Narrowed, with the reason stated \dash{} the same reason F04 gives
  for not naming an optimiser.
- *An attention logit of twelve is an ordinary afternoon* now names the program
  that owns the reason: keeping those scores small is the whole job of the
  $1/\sqrt{d_k}$ factor, which is **P25**'s derivation, checked against the
  manifest rather than assumed.

#### Layout

Back to the baseline in all four builds. One new box arrived and was cleared:
$\num{11.3}$ pt in `main-en`, from a **diagram-manifest line** \dash{}
`p02-cancellation.mmd` plus a 33-character description in the narrow indented
column. That is F02's finding and its fourth recurrence, and the first time it
has been the **English** that overflowed rather than the Polish. All three
third arguments were cut to under 25 characters.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P2.1 cancellation | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P2.2 two-cliffs | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P2.3 pivot | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

**Rule 2 moved a figure, and reading alone was not enough to settle it.**
`p02-cancellation` was declared after frame 4, where nothing it says is an
answer \dash{} but frame 5 asks *how many significant figures survive*, and the
figure's middle node says *every digit they agree on cancels to nothing*, which
is one step from \enquote{none} for a reader who has just been told the
operands share nine figures and the format holds seven. On the page it landed
beside that question in all four builds. Moved below frame 6's answer, and
re-measured: question, then answer, then figure, in every build.

The generalisable part: **a figure that supplies the last step of an answer is
as much a spoiler as one that states it.** F02's rule says *contains the
answer*; this is the milder case and it needed the same fix.

#### Also

- Traps 80 to 86 added to `notes/02`, and item 1's owner split \dash{} which
  the P01 pass corrected from a promise \dash{} is now marked delivered with
  the numbers.
- **Parity came back clean on its first run**, on a program of this size, which
  has not happened before. The accumulated translator rules did it: no number
  spelled as a word, and every `Program~\ref{...}'s <maths>` built the other
  way round while drafting rather than after a failure.
- Frame numbers remapped after writing: sections landed at
  `1--8 / 9--13 / 14--21 / 22--28 / 29--37` against a plan of
  `1--9 / 10--15 / 16--24 / 25--33 / 34--43`. Two markdown asterisk pairs had
  to be turned into `\emph{}` \dash{} they set as literal asterisks and nothing
  warns.

### Program P3 pass, August 2026 --- Part II is complete

**Thirty-four teaching frames, thirty-six printed, both editions**, against a
brief that projected forty-five. Five sections: what the notation says, what it
does not say, counting operations, counting bytes, and operations against bytes.

**It is the cheapest program in the book by every layout measure.** Zero new
overfull boxes in any of the four builds on the first attempt, no stranded
openers or headings, no orphaned cues, and one orphan tail. Parity needed four
rounds, all of them recorded classes.

#### The bare-logarithm ban met the one case where the omission is a theorem

`O(n \log n)` is the standard written form, and this book makes a bare
logarithm a **build error** \dash{} for good reason, since its two readerships
read it as two different functions and entropy in bits is two programs from
cross-entropy in nats. C10 fired seventeen times on the first parity run.

The resolution is not an exception, it is a **notation box**, because inside an
$O$ the missing base is provable rather than conventional:
\[ \logb{a} n = \frac{\logb{b} n}{\logb{b} a} \]
so changing the base multiplies by a constant, and a constant is exactly what
the notation discards. $O(n \log n)$ therefore names **one** class of growth for
every base at once, and writing a base inside it would suggest a distinction
that does not exist. Two sections later the same program writes
$\val{p03.cross.c2}\,n\logb{2}n$ *with* its base, because there it is outside an
$O$ and the base is back.

`preamble.tex`'s comment on `\mfalogplain` now names two kinds of legitimate
place rather than one \dash{} where the ban itself is the subject (Appendix B,
F03), and inside an $O$, $\Theta$ or $\Omega$ (P03) \dash{} and it still states
no tally, for the reason that comment already gives.

**The generalisable part: when a house rule and a real convention collide, ask
whether the convention has a reason.** Here it did, the reason is two lines of
algebra, and the collision produced a frame rather than a workaround.

#### The measurement F10 asked for by name

F10 said $O$-notation needs *its own definition, its own warnings about what it
does not say, and a worked account of why the faster of two implementations
today can be the slower one at scale.* The third is the one that needed a
number.

Two implementations of one job: $\val{p03.cross.c1}n^{2}$ with a tight inner
loop, against $\val{p03.cross.c2}\,n\logb{2}n$ with an expensive one. They trade
places at $n = \val{p03.cross.n}$, found by bisection because
$n^{2} = c\,n\logb{2}n$ has no elementary solution. At $n = 100$ **the
asymptotically better algorithm costs $\val{p03.cross.ratio.100}$ times as
much**; at $n = 100\,000$ the other one costs
$\val{p03.cross.ratio.100000}$ times as much.

That is the whole argument in two rows, and it is why every sorting library
ships an $O(n^{2})$ insertion sort inside its $O(n\log n)$ one.

#### F01's largest debt, paid, and the number that explains a common question

F01 said twice that the weights are a **floor**. The rest of the bill:

| | GB |
|---|---|
| weights, two bytes | $\val{p03.mem.weights}$ |
| gradients, two bytes | $\val{p03.mem.grads}$ |
| master copy, four bytes | $\val{p03.mem.master}$ |
| two moments, four bytes each | $\val{p03.mem.moment1}$ + $\val{p03.mem.moment2}$ |
| **total** | **$\val{p03.mem.total}$** |

**The weights are $\val{p03.mem.weights.pct}\%$ of the training bill and the
whole is $\val{p03.mem.multiple}$ times the model card's number.** That factor
is the answer to *why will a model that serves on this card not fine-tune on
it*, and the useful form is that each remedy removes a **row** rather than
shrinking all of them.

The assertion is the invariant rather than the figure: the weights must be a
small minority, because a recipe that made them the majority would need the
frames rewritten and not the number updated.

#### The exponent trap, which is the best thing in the program

**Attention's compute is quadratic in the sequence and its cache is linear**,
and almost everybody expects both to be quadratic \dash{} the expectation comes
from somewhere real, because F04 counted exactly those $n^{2}$ pairs.

The cache holds one key and one value per *position*, not per pair; the pairs
are formed and consumed inside the computation and never stored. Measured:
$\val{p03.kv.gib}$ GiB at $\val{p03.kv.seq}$ tokens, exactly double at twice the
length, $\val{p03.kv.per.token.mib}$ MiB per token in flight. It is usually larger
than the weights and it is the term that decides how many users a card serves.

Two quantities, two exponents, one layer. The script asserts the doubling
rather than the size.

#### Three claims quantified where the folklore is qualitative

- **A matrix multiply is compute-bound only above $n \approx
  \val{p03.ai.smalln}$.** Its intensity is $\frac{n}{3}$, which *grows*;
  \enquote{matmuls are compute-bound} is a statement about the large ones,
  repeated as though it were about the operation. A batch of small ones \dash{}
  narrow heads, low-rank adapters, a mixture of narrow experts \dash{} is on the
  wrong side of the line.
- **An elementwise operation is short of the device by
  $\val{p03.ai.short}$**, and $n$ does not appear in its intensity at all, so
  the shortfall is the same however large the arrays are.
- **Fusion helps and does not rescue.** Fusing $\val{p03.fuse.chain}$
  elementwise operations divides the bytes by $\val{p03.fuse.factor}$ for
  exactly the same operations, taking the intensity to
  $\val{p03.fuse.after}$ \dash{} against a device ratio of
  $\val{p03.dev.ratio}$. The bytes have a floor: the input must be read once and
  the output written once whatever happens between. The script asserts that the
  fused chain is *still* memory-bound, so the frame's point cannot quietly
  become false.

#### Two smaller things the drafting caught

- **A ratio printed as `0.0`.** The crossover table emitted
  $\text{linlog}/\text{quad}$ throughout, which is $0.033$ above the crossover
  and rounds to nothing \dash{} hiding that the quadratic is now thirty times
  worse. It now always reports the slower against the faster, so the number is
  above one and reads the same way in both directions.
- **Two numbers written twice**, once as a word and once as a value:
  \emph{thirteen times faster} beside a table computing $13$, and \emph{one part
  in twelve hundred} beside a value of $1200$. Both are now the value. It is
  F02's rule about small integers, running the other way.

#### A text value cannot be referenced

`p03.cross.loser.*` named which algorithm is slower at each size, and C7
reported all three as \enquote{used but no script produces it}: the ledger's
produced set scans for `\mfaval`, and a non-numeric value is written with
`\mfavaltext`. F10 met the same wall from the other side.

The right reading is not that the check is wrong. **A word is not a computed
value**, and these words differ between the editions anyway \dash{} so they
belong in the frames, per edition, and what the script asserts instead is that
the frames name the right one at each size.

#### Layout and figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P3.1 crossover | 654 / 657 | 5.95 | 6.74 | 6.71 | 7.66 | 7.62 |
| P3.2 memory-bill | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P3.3 roofline | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

**Rule 2 checked by content and then measured.** `p03-memory-bill` contains
frame 18's answer \dash{} what else is resident while a model trains \dash{} and
is declared after frame 19, which delivers it. On the page all three land
together in every build, in the order question, answer, figure, with the caption
227 to 372 points below the question. The other two figures answer nothing asked
either side of them.

#### Also

- Traps 87 to 92 added to `notes/02`.
- Four parity rounds, all recorded classes: a reference behind its maths in a
  summary item, and three cases of Polish splitting one English maths span into
  two (`tablic $n$ na $n$` for `$n$-square`). The second is a *new* instance of
  the ordered-span rule and worth naming: **Polish often needs two spans where
  English needs one**, and the fix is to find a Polish phrase that keeps it to
  one (`tablic o boku $n$`), not to add a span to the English.
- Frame numbers remapped: sections landed at
  `1--7 / 8--12 / 13--17 / 18--24 / 25--34` against a plan of
  `1--6 / 7--13 / 14--20 / 21--29 / 30--38`.
- One markdown `**bold**` pair had to become `\textbf{}`; it sets as literal
  asterisks and nothing warns. Second program running.

### Program P4 pass, August 2026 --- Part III begins

**Thirty-four teaching frames, thirty-six printed, both editions**, against a
brief that projected fifty-five. Five sections: what a space is, span,
independence, basis and dimension, and what the counting forces.

It is the first program in the book that needs a new **object** rather than a
new question, which is what P03's closing frame says and was verified rather
than remembered.

#### The scope was decided by reading four briefs, and it changed the program

P05 owns inner products, norms, projection and near-orthogonality in high
dimension; P06 owns matrices as linear maps; P08 owns rank and LoRA; F09 had
already defined vector arithmetic and then deferred, in a warning box, *how
vectors are arranged* to P05, saying in as many words that measuring it needs
the vocabulary P04 supplies.

So P04 never measures an angle, because it has not been given one. **Section 5
goes as far as a counting theorem and stops.** That is the better possession:
20,000 tokens in 4,096 dimensions leaves at least 15,904 of the embeddings ---
80% --- as combinations of the others, it follows from two integers, and no
amount of training changes it. What it does *not* say is that the model cannot
distinguish that many things, and the gap between the two is where the
linear-representation and superposition accounts live. Both are stated as
hypotheses, with what would falsify each, which is the issue's contract and the
place a book of this kind slides into folklore.

#### Exact rank over rationals, because P01 established why

`code/p04_vector_spaces.py` computes rank by Gaussian elimination over
`Fraction`, with **no epsilon anywhere**. That is deliberate and it is P01
paying off two programs later: a float comparison is not yes-or-no, so a rank
computed with a tolerance would have made the program's central theorem depend
on a threshold nobody could defend. Over the rationals the answer is exact and
the assertion is the theorem: `rank(n random vectors in d dimensions) ==
min(n, d)`, and separately, over 300 draws at random `n` and `d`, that no set
ever exceeds rank `d`.

The frames say what those draws are for, because it is not what it looks like:
**the draws are testing the code.** A search that succeeded would have refuted
a proof.

#### A cross-programme gate that was fabricated, and caught by writing it out

The first version asserted that F09's `f09.len3d` matched this program's
`(3, 4)`-vector length. F09's value is **7** and the length here is **5**, and
they are different computations that happened to sit near each other --- so the
gate would have failed for the right reason and been "fixed" by loosening it.

It was replaced with a gate on `f09.dim`, which the two programs genuinely
share: P04 quotes F09's dimension count to give the counting bound a second
case, so the assertion is that `f09.dim < VOCAB` and the dependent count is
derived from F09's own committed number rather than from a copy of it.

**A cross-programme gate is only worth having when the two programs are quoting
one computation.** Two numbers that merely appear together are the defect the
mechanism exists to catch, not the thing to wire it to.

#### Rule 2, and the pointer that named the wrong program

- **A forward pointer nobody had promised.** *Rotating a model's
  representations and asking whether it still works --- one that Program P08 is
  equipped to think about properly.* P08's brief is rank, the four subspaces,
  least squares and LoRA; it undertakes no such thing. Softened on the F04/F08
  precedent rather than by re-inflating P08's brief: the rotation is itself a
  matrix, which is **P06**'s subject, and the book does not run the test.
  Sixth pass running that a claim about another program was the thing that
  needed fixing.
- All three figures were read against the frames either side of them before
  being measured. Only `p04-basis-not-unique` contains an answer to something
  the reader is asked, and it is declared after the frame that delivers it.

#### The elicitation rate had halved over seventeen programs, and nothing saw it

The finding is not P04's and it is the most valuable thing this pass produced.
A frame carries `\nextframe` **if and only if** the next frame opens with an
answer, so the cue rate *is* the elicitation rate. Measured across the book:

| | F01--F06 | F08--F13 | Part II and P04 |
|---|---|---|---|
| frames that elicit | 73--78% | 50--66% | 26--31% |

**The last `\yourturn` in the book is in F04 and the last `\blank` is in F07.**
Ten and thirteen programs ago respectively. Both are distinct retrieval modes
rather than decoration --- a gap inside a worked line, and a question with its
answer overleaf --- and skipping them costs a program a rung of the scaffolding
gradient, which the F02 review pass had already recorded once.

Every gate stayed green throughout, and the reason is precise:
`check_structure.py`'s `RE_DEMANDS` treats `\nextframe`, `\blank`, `\dotline`
and `\yourturn` alike, so a program that elicits rarely satisfies it perfectly.
Parity's C16 counts cues per frame and compares the editions, so a rate that
falls identically in both is invisible to it, and to C4 and C14 as well.
**Nothing in the repository looked at the ratio.**

`make debt` now reports it, per program and for the book, **reported and never
fatal** --- the orphan tail's treatment, for the orphan tail's reason: there is
no defensible threshold and a permanently red gate teaches the next person to
stop reading the output. The book stands at 60%.

P04 was written at 26% and is now at **35%**, the highest in Part II, by three
conversions that added no frames and therefore needed no renumbering: each took
a frame that *stated* something the reader could produce, moved the statement
into the next frame's answer, and ended the first frame by asking. The best of
the three is *must two bases for the same space contain the same number of
vectors* --- most readers answer yes without hesitating, which is the right
answer arrived at the wrong way, and the frame says so before calling it a
theorem.

**Raising Part I's rate back across P01--P03 is a pass of its own and is not
this one.** Rewriting three merged programs to chase a ledger introduced in the
same commit is how a measurement stops being trusted.

#### The front matter was wrong about the book, in two places, and it prints once

Found while checking P04 against its issue, which says *no Quiz (Foundation-only)*.

- *How to use this book* said **Quiz --- Foundation programs only.** Every
  written program has one, P01 to P04 included, all three of the others merged.
- The same page told the reader to **retake the Quiz** and called the
  difference between the two scores *the only honest measure of what a program
  did for you*. That is the exact claim the F04 review pass removed from
  `\lblCanYouFooter` --- the same items serve entry and exit, so the difference
  measures memory --- and the front matter had been contradicting the corrected
  footer ever since.

Both fixed in both editions, and the loop diagram now runs *Can you?* straight
into the Test exercises, which is what the book actually scores itself against.
It was out of P04's scope on the F04 `\lblCanYouFooter` precedent, and taken for
the same reason: it printed on page one and it was false.

#### The transcript did not run as printed, and it is generated

`figures/transcripts/p04-rank.txt` calls `rank(...)` and never defines it, so a
reader pasting the listing out of the finished PDF gets `NameError` on the last
line. The file is **generated by `code/`, committed, and inside `make verify`'s
drift gate** \dash{} and none of that makes it runnable. It is the sibling
volume's fabricated-console-block defect wearing a generated file's clothes,
which is worse, because the file looks like it must have run.

Fixed by importing `rank` from the script that produced it, and verified the
only way that means anything: extracted, run from `code/`, prints
`[2, 4, 8, 8, 8, 8]`, which is what the page prints.

**All ten transcripts in the book were then swept** by parsing each one and
listing the names it uses but never binds. P04's was the only one; the other
nine are self-contained. The sweep is one short script and is worth re-running
whenever a transcript is added \dash{} the F03 pass earned the same habit for
console blocks nobody ran, and this is that habit one build step further on.

#### Layout

A 25.8 pt overfull hbox in `main-en-a4` alone --- by a wide margin the largest
since F05's tables --- from the two coordinate pairs `$(3, 4)$` and
`$(4.5981, 1.9641)$` run inline in a **test exercise**. That is F06's finding
and F08's, one measure further out: a test-exercise item is set narrower than
the frame its numbers came from, so a pair of unbreakable spans that is
comfortable in the frame overflows there. The recorded fix applied without a
detour --- **put it in a display** --- and the multiset came back to the
pre-P04 baseline in all four builds.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P4.1 span | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P4.2 saturation | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P4.3 basis-not-unique | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's own wrap cap on the first render, so no redesign.

**The three added cues cost `main-en-a4` two pages and put one orphan tail back
in `main-pl-a4`.** That is the Stroud layout pass's measurement arriving from
the other direction \dash{} it priced 33 cues at two pages per format \dash{}
and it is the honest cost of the elicitation rate. It is worth paying and it is
worth knowing before Part II's rate is raised.

Measured on the page in all four builds, which is the second half of the check:

| build | P4.1 fig / elicit / answer | P4.2 fig / answer | P4.3 fig / answer |
|---|---|---|---|
| `main-en` | 462 y130 / y204 / y283 | 465 y380 / y196 | 469 y130 / 468 y416 |
| `main-pl` | 466 y130 / y204 / y283 | 469 y389 / y196 | 473 y130 / 472 y443 |
| `main-en-a4` | 392 y149 / y212 / y294 | 395 y121 / 394 y614 | 398 y149 / 397 y532 |
| `main-pl-a4` | 395 y361 / y449 / y530 | 397 y630 / y443 | 401 y477 / y270 |

**P4.1 sits above its elicitation in all four builds and that is not a defect**,
which is precisely the F03 second review pass's finding restated: it carries the
definition of a span, which the frame above it states in full, and the question
below it is *what do two vectors span* whose answer \dash{} a plane, usually
\dash{} appears nowhere in the figure. The question, the figure and the answer
are on one page in every build, so nothing the reader writes is overleaf from
what they wrote it about. P4.2 and P4.3 both sit below their answers everywhere.

#### Also

- Traps 93 to 98 added to `notes/02`.
- `\spanof` added to both language files beside `\gcdop` and `\lcmop`; it sets
  `span` in English and `lin` in Polish, which is current Polish usage.
- Two parity failures, both recorded classes: a reference behind its maths in a
  summary item, and `2,317` in an English aibox against `2317` in Polish ---
  the thousands comma splits the English literal into `2` and `317`, and a
  neuron index is an identifier rather than a quantity, so it takes no
  separator in either edition.
- Frame numbers were mapped after writing rather than before: sections landed
  at `1--8 / 9--14 / 15--20 / 21--27 / 28--34`.

### Program P5 pass, August 2026

**Forty-six teaching frames, forty-eight printed, both editions**, against a
brief that projected sixty. Five sections: what one more operation buys, norms,
projection, which measure and what normalising decides, and what high dimension
actually does.

The layout came back to the pre-P05 baseline exactly \dash{} `[]`, `[]`,
`[6.3]`, `[]` \dash{} with no stranded openers and no stranded headings. Three
orphan tails were added, and **one orphaned cue arrived from the figure reword
below and was cleared by lengthening the frame**, which is the fourth
confirmation of F06's two-sided rule: the paragraph added says that nothing
requires a norm to come from an inner product, which is the sentence §2 needed
anyway.

#### Two predictions refuted by their own assertions, and both are better frames

Eighth pass running that writing the assertion at the computation, before the
sentence it supports, has caught something. This time it caught two, and the
second is the section the program is built on.

**One: greedy packing is the wrong construction.** The draft asked P04's
question \dash{} *what does relaxing exactly-orthogonal to nearly-orthogonal
buy?* \dash{} by drawing random directions and keeping each one whose cosine
against every kept direction stayed under a tolerance, asserting that more than
$d$ would fit. At $d = 64$, tolerance $0.2$, it kept **forty-five**, fewer than
the sixty-four that are *exactly* orthogonal. Acceptance decays like $p^{k}$ as
the kept set grows, so the search stalls long before the geometry does: **it
measures the search, not the space.** No tuning would have rescued it.

Replaced with the **union bound** over the exact cosine density
$(1-c^{2})^{(d-3)/2}$, integrated numerically and cross-checked against the
sampled fractions at $d = 10$, $100$ and $768$ \dash{} which is what makes the
integral trustworthy rather than merely plausible.

**Two: the capacity is not monotone in $d$**, which the redraft asserted:

| $d$ | $P(\lvert\cos\rvert > 0.2)$ | capacity | vs $d$ |
|---|---|---|---|
| 3 | 8.0e-1 | 2 | 0.5x |
| 64 | 1.1e-1 | 4 | 0.07x |
| 768 | 2.2e-8 | 9 487 | 12x |
| 4096 | 3.1e-38 | 8.0e18 | 2e15x |

**There is a threshold, at $d = 488$, and it is where the tolerance meets the
typical spread** \dash{} $0.2$ is $4.4$ spreads out there. Below it, high
dimension buys nothing over exact orthogonality; above it the capacity runs
away. Everybody quotes the second half without the qualifier, and that is the
trap the section is built on. The failed assertion is a better frame than the
claim it replaced, and §5 says so.

#### The headline, and what four written neighbours were owed

F09's closing table names three claims that "do not transfer" to high dimension
and defers all three here by name. All three now have numbers.

| $d$ | cosine spread | within 5 deg of a right angle |
|---|---|---|
| 2 | 0.715 | 5% |
| 10 | 0.320 | 21% |
| 100 | 0.100 | 61% |
| 768 | 0.035 | **99%** |

The assertion is the **invariant** \dash{} the measured spread tracks
$1/\sqrt{d}$ to within $2.0\%$ over three decades \dash{} and not any single
cosine, which is a random variable that would move with the seed. F11 paid for
the lesson that a threshold chosen so an assertion passes is not an assertion.

The consequence worth carrying out of the program: **a cosine similarity of
$0.3$ at 768 dimensions is about eight spreads out, and enormous.** Read on
two-dimensional intuition it looks like a weak signal.

#### The brief promised a worked example that F09 had already spent

P05's brief undertakes "the case where they rank differently worked out". F09
works it in full \dash{} query $(1,0)$, $A = (0.30, 0.06)$, $B = (0.95,
0.45)$, $A$ more similar and $B$ nearer, with a table of both measures. Writing
it again would have been repetition.

What F09's trapbox actually hands forward is narrower and better: **which**
measure to prefer, and **what normalising costs**. So §4 is a decision rather
than a demonstration, and it lands on a sentence the worked example could not
reach: normalising does not make the dot product behave like the cosine, it
makes the two queries the same query, so it is not a preprocessing step but
**the decision to throw the lengths away, taken silently**.

That is the fifth program running whose brief over-estimated what was left,
and the reason is always the same: the brief was written before its neighbours.

#### A percentage that rounded to 100, caught by a guard that is now general

The first draft printed **"100.0 per cent"** of a ball's volume in the outer
tenth of its radius, twice. At $d = 100$ it is $99.99735\%$. A quantity that
rounds to a hundred per cent must be reported as its **complement**, where
every figure is significant: the inner nine tenths hold $2.7\times10^{-5}$ of
the ball at $d = 100$ and $7.2\times10^{-36}$ at $d = 768$. The script now
refuses to emit any percentage that rounds to $100$, which is a guard worth
copying into every script that emits one.

Those figures are computed rather than sampled, and the note in §5 says why:
the inner half of the radius holds $6.4\times10^{-232}$ of a 768-dimensional
ball, so a sampled estimate would report zero, and **finding nothing is not
measuring nothing** \dash{} which is the shape of an assertion that cannot
fail.

#### The cross-programme gate, wired to a shared computation rather than a coincidence

P04's pass established what one of these is worth and what it is not: its own
first attempt gated this program's $(3,4)$ length of $5$ against F09's
`f09.len3d`, which is $7$ and a different vector entirely. Not repeated. What
P05 and F09 genuinely share is the **dimension**: F09 reasons at `f09.dim`
throughout and defers the arrangement question here, so the gate asserts that
the near-orthogonality table measures at exactly that dimension. If F09's
number ever moves, the table is quietly about a different model and the build
says so.

#### The transcript imports what it calls, on sight

P04 shipped one that named a function it never imported. P05's imports `unit`
and `dot` from the script that produced it and was verified by extraction and
execution before the frame around it was written, printing
`[0.715, 0.315, 0.099, 0.036]` \dash{} which is $1/\sqrt{d}$ at
$d = 2, 10, 100, 768$, and is the concentration in one line.

#### Rule 2 moved one figure and reworded another

Both by reading the figure against the frames either side of it first, and then
measuring, which is the order the F03 second review pass prescribes.

- **`p05-spread-shrinks`** was declared after the $1/\sqrt{d}$ answer, and the
  next frame asks *how many of a hundred pairs at 768 dimensions are within
  five degrees of a right angle*. Its third node said *a typical pair is nearly
  at right angles*, which is one step from "nearly all of them". That is P02's
  finding \dash{} a figure supplying the last step of an answer is as much a
  spoiler as one stating it \dash{} so it moved below the answer.
- **`p05-what-it-buys`** sits above an elicitation in all four builds, which is
  not by itself a defect. But its third node said *lengths, angles and
  perpendicular all follow from that one definition*, and the frame below asks
  the reader to make $\cos\theta$ the subject and say that the equation now
  **defines** the angle. Node C now states frames 6--7's content instead \dash{}
  perpendicular stops being a picture and becomes a sum that is zero \dash{}
  which the frames above it have already delivered.

`p05-closest-point` sits below both its elicitation and its answer in every
build, measured at y438/443/446/458 against answers at y236/240/241/241.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P5.1 what-it-buys | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P5.2 closest-point | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P5.3 spread-shrinks | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's own wrap cap on the first render, so no redesign.

#### Also

- Traps 99 to 105 added to `notes/02`.
- **The elicitation rate was designed in rather than retrofitted**, which is
  the first program written since the ledger existed. P05 is at **36%**, above
  Part II's 29--31% and P04's 35%, and three of its cues came from converting
  frames that stated something the reader could produce. It is still far below
  Part I's 73--78%, and the honest reason is that a derivation-heavy section
  \dash{} §3 is one \dash{} has fewer places to stop and ask than a section
  built on numbers.
- Parity took two rounds. Twenty-two bare decimals inside maths had to be
  wrapped in `\num{}` (C10, in both editions, because the Polish edition owes a
  comma), and one C4 divergence was the recorded word-order class with `$A$`
  rather than a reference: English had `$B$ ... len.b ... $A$'s ... len.a` and
  Polish had the two values adjacent with `$A$` behind them.
- Sixteen emitted values went unreferenced and the **emission** was narrowed
  rather than the prose padded \dash{} the assertions still sweep every
  dimension, and only the rows the frames quote are written out. F11's finding,
  applied on sight.

### Program P6 pass, August 2026

**Thirty-six teaching frames, thirty-eight printed, both editions**, against a
brief that projected sixty. Five sections: what makes a function linear,
multiplication is composition, why the order matters, shape is a type
signature, and the collapse in more than one dimension.

**It is the cheapest program in Part III by every layout measure.** Zero new
overfull boxes in any of the four builds on the first attempt, no stranded
openers, no stranded headings, no orphaned cues, and two orphan tails. Parity
needed two rounds and both were the recorded word-order class.

#### Two of the brief's four payoffs were already spent, and it was one file read

The brief promises the collapse derived, multi-head attention as a reshape, and
a batch as one extra index. **F05 already derives the collapse in full**, in one
dimension, including the $\relu$ argument \dash{} two hundred layers of
$wx + b$ collapse to one and the activation exists because without it the
composition is provably a waste. And **P07 owns index notation, einsum,
broadcasting, reshape against transpose against permute, and the axes of a
rank-4 attention tensor**, so both the reshape and the batch index are its.

What F06 names is the job that is actually left, and it says so in as many
words: *P06 makes the weights a matrix and shows that matrix multiplication is
composition, which is F05's collapse argument done in more than one dimension.*
Sixth program running whose brief over-estimated what was left, and the reason
is always the same \dash{} the brief was written before its neighbours.

#### The collapse needed a new argument, and the new one is better

Restating F05's *no amount of stretching and sliding produces a corner* would
have been repetition. In more than one dimension there is a cleaner test and it
needs no picture: **an affine map cannot bend a straight line.** Three collinear
inputs come out collinear through the collapsed matrix ($\val{p06.bend.affine}$
of the spacing, which is rounding) and bent through the $\relu$-separated pair
($\val{p06.bend}$).

That rules out **every** affine map at once rather than failing to find one,
which is a stronger form of the same argument, and it is why the requirement on
an activation is only \enquote{not affine} \dash{} the field could swap the
logistic for $\relu$ for GELU without rewriting the theory.

#### Two measurements, and the second is the one the reader gets wrong

- **The waste is the depth.** Eight linear layers of width
  $\val{p06.stack.width}$ hold $\val{p06.stack.params}$ parameters and express
  what $\val{p06.stack.collapsed}$ express, so
  $\val{p06.stack.wasted.pct}\%$ bought nothing. The script asserts
  $(k-1)/k$ **at every width**, because the fraction not depending on $d$ is
  the point and the single figure is not.
- **Of $\val{p06.commute.trials}$ random $3 \times 3$ pairs,
  $\val{p06.commute.found}$ commute.** Not \enquote{few} \dash{} none, and none
  could: commuting is a condition on a set of measure zero. This is the frame
  the reader answers wrongly, so it is elicited before it is stated.

And one that is free and worth having: **the same triple product costs
$\val{p06.cost.left}$ multiplications one way and $\val{p06.cost.right}$ the
other**, a factor of $\val{p06.cost.ratio}$, with an identical answer.
Associativity is free and bracketing is not, which is the mechanical half of
why a low-rank update is cheap \dash{} P08 owns the other half.

#### The elicitation ledger was designed against, and it moved

P06 is at **38%**, above P05's 36%, P04's 35% and Part II's 29--31%, and it is
the highest in Part III. Two of the fourteen cues came from converting frames
that stated something the reader could produce, and **neither conversion added a
frame**, so no renumbering followed:

- Frame 11 stated why the row of $A$ meets the column of $B$. It now asks, and
  frame 12 opens with the answer **and then asks the associativity question**
  \dash{} a frame may open with `\ans` and end with `\dotline`, which is the
  original's own alternating pattern and satisfies `RE_DEMANDS` and C16 alike.
- Frame 17's trapbox stated that none of the random pairs commute. The count is
  now elicited and the trapbox keeps the reasoning that produces the wrong
  answer, which is where the errorful-generation benefit lives.

**The second conversion moved a figure**, and that is worth recording as a cost
of raising the rate: `p06-order-matters` had been declared between the new
question and its answer, which is F02's rule from the other side. Moved below
the answer frame and re-measured in all four builds.

#### Rule 2, read first and then measured

Only `p06-shape-is-a-type` contains an answer to something the reader is asked
\dash{} its middle node is frame 20's *which of $AB$ and $BA$ is even defined*
\dash{} and it is declared after frame 21, which delivers it. Measured:
question, answer, figure, in that order, on one page in every build.

`p06-order-matters` sits a page after both its elicitation and its answer in
three builds and below both on one page in `main-en-a4`.
**`p06-matrix-is-a-function` sits above the elicitation that follows it in all
four builds and that is not a defect**, which is P04's finding restated: it
carries the two properties, which the frame above states in full, and the
question below is *is $f(x) = x + 3$ linear?*, whose answer turns on $f(0)$ and
appears nowhere in the figure.

| build | fig1 / q / a | fig2 / q / a | fig3 / q / a |
|---|---|---|---|
| `main-en` | 504 y530 / 505 y533 / 506 y121 | 512 y250 / 511 y380 / 511 y504 | 513 / 513 y197 / 513 y318 |
| `main-pl` | 507 y454 / 507 y551 / 508 y121 | 513 y252 / 512 y365 / 512 y502 | 514 / 514 y197 / 514 y318 |
| `main-en-a4` | 426 y361 / 427 y241 / 427 y349 | 431 y586 / 431 y173 / 431 y299 | 432 / 432 y217 / 432 y342 |
| `main-pl-a4` | 431 y324 / 431 y427 / 431 y536 | 436 y149 / 435 y372 / 435 y512 | 437 / 436 y512 / 436 y637 |

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P6.1 matrix-is-a-function | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P6.2 order-matters | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P6.3 shape-is-a-type | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's own wrap cap on the first render, so no redesign.

#### The transcripts were not printing, and had not been for nine programs

Found by applying F03's own discipline to P06's transcript \dash{} extract it
from the finished PDF and run what comes out \dash{} and discovering there was
nothing on the page to extract. **Ten of the book's twelve transcripts had
never reached a reader**, from F11 through P05, every gate green throughout.
The mechanism and the fix are in *Build traps*; what belongs here is what it
cost and what it changed.

**What it makes false.** Three pass notes in this file describe transcripts as
though they were on the page: F11's *the whole seventeen-row sweep is a
committed transcript rather than a table, because the shape is the argument*,
P04's *verified the only way that means anything: extracted, run from
`code/`*, and P05's *verified by extraction and execution before the frame
around it was written*. Each verified the **file**. None of them verified the
**page**, and the difference is the whole defect. The sentences are left
standing above with this correction under them, because rewriting them would
hide that the distinction is easy to miss.

**All twelve were then swept**, extracted from `main-en.pdf` and executed from
`code/`. All twelve run. The four that do not match their committed file
character for character differ only in runs of spaces, which is
`pdftotext -layout` re-columning, and one is a page break inside a listing.
Quotes come out as ASCII apostrophes, so the `upquote` fix holds for the ten
listings that had never been checked on a page because they had never been on
one.

**One was a spoiler, and it was created by making them print.** F11 frame 17
carries the seventeen-row sweep and then asks *what is the value at
$h = \val{f11.fd.vanishes}$, and why?* \dash{} whose numeric half is the last
row of the table, four inches above. The question now points at that row and
asks only for the reason, which is what frame 18's answer was always about.
That is P04's rule (**a transcript is under the same rule as a frame**) biting
a program that had been merged for weeks, and it is the predictable cost of
switching ten listings on at once: ten frames whose relationship to their own
listing had never been reviewed on a page. The other eleven were read against
their frames in the same pass; the four that ask a question after the listing
\dash{} F04's *what is $0!$*, P01's *what has the exponent done*, P05's *say
what rule they follow* and P06's *how many pairs commute* \dash{} each ask for
something the listing does not contain.

**The pages moved and the overfull multiset did not.** A listing is often
shorter than the marker box it replaced: `main-en` 656 to 654, `main-pl` 658 to
664, `main-en-a4` unchanged, `main-pl-a4` 567 to 565. Three orphan tails
arrived, all in `main-pl`.

#### Also

- Traps 106 to 111 added to `notes/02`.
- **Two parity rounds, both the recorded word-order class**, and both were an
  English possessive attached to something that inverts in Polish:
  `Program~\ref{prog:F06}'s $y = wx + b$` in a summary item, and
  `against $A(BC)$'s $d r d + d^{3} = \dots$` in a further-problem answer. The
  second is worth naming because the possessive was attached to a **maths
  span** rather than to a reference, which is the same inversion one step
  further out.
- Frame numbers were mapped after writing: sections landed at
  `1--8 / 9--14 / 15--19 / 20--25 / 26--36`, and every outcome, quiz route and
  summary bracket moved with them.
- One garbled clause was caught by reading the draft aloud rather than by any
  gate \dash{} *it passes through the scalar nothing*, which is not a sentence.
  It is now *it carries a scalar straight through*, which is the second
  linearity property said in words.

### Program P7 pass, August 2026

**Thirty-seven teaching frames, thirty-nine printed, both editions**, against a
brief that projected fifty-five. Five sections: an array is a shape and a rule
for reading it, index notation says what a picture cannot, an `einsum` string is
that sentence with the sigma left out, broadcasting is a rule rather than a
courtesy, and which of reshape, transpose and permute moves data.

**It cost nothing on any layout ledger.** Zero new overfull boxes in any of the
four builds, no stranded openers, no stranded headings, no orphaned cues after
one round, and **the orphan-tail count did not move at all** \dash{} which has
happened once before, at F13, and both times because the recorded rules were
applied while drafting rather than after a build named the defect.

#### The program had no plan, and writing one first changed its shape

P07 was inserted by the August 2026 curriculum review rather than designed, so
its manifest entry is a contract and this file has carried *write the plan
before the program* as an open item ever since. The plan is
`notes/08-tensors-plan.md` and it was written before a line of the program.

Two things came out of it that would not have come out of drafting:

- **P06 §4 hands this program four things by name**, including the note that
  real frameworks stack the batch along the *first* axis and compute
  $XW\T$. That is the first place a reader's rank-2 model meets a framework, so
  it is frame 1 \dash{} and the answer is *both, because $XW\T$ is the
  transpose of $WX$*, which is the last question in the program answerable with
  a matrix identity. Opening there buys the rest of the program its motivation.
- **The word *dimension* does three jobs and the word *rank* does two.** P04
  owns dimension as the number of independent directions and P08 owns rank as
  what a matrix does. Neither collision is avoidable and both are invisible
  while drafting; the plan caught them and §1 names them.

#### The headline is an identity, not a demonstration

Predictions of shape $(n)$ minus targets of shape $(n, 1)$ broadcast to
$(n, n)$, so a loss is averaged over every *pair*. The excess is exactly

\[ \operatorname{mean}_{ij}(p_i - t_j)^2 - \operatorname{mean}_i(p_i - t_i)^2
   = 2\operatorname{Cov}(p, t) \]

and the two consequences are what make it worth a section rather than a warning
box. **The error grows as the model improves**, because a covariance is
precisely what training increases; and **at a perfect fit the reported loss is
$2\operatorname{Var}(t)$ and cannot fall below it.** Measured, the reported
number is $\val{p07.mse.ratio.hi}$ times the true one at a poor fit and
$\val{p07.mse.ratio.lo}$ times at a good one. What an engineer sees is a loss
that falls, flattens at a number nobody can account for, and stays there, which
is read as a model that has stopped learning.

No error, no warning, and the training loop is fine. It is the best trap the
book has found so far, and it is exactly derivable.

#### An assertion refuted the frame it was written for, for the ninth pass running

The first version asserted that **the excess grows monotonically as the fit
improves**. It failed on the first run: the excess went $1.01$, $1.59$, $1.43$,
$1.44$ over four noise levels. The excess is
$2\operatorname{Var}(t) + 2\operatorname{Cov}(\varepsilon, t)$, and the second
term is a *sample* covariance between the residual and the targets \dash{} a
random quantity of size about $\sigma\,\mathrm{sd}(t)/\sqrt{n}$ that does not
shrink in step with $\sigma$. At $n = 64$ it is large enough to reorder the
rows.

What is true is better: the excess converges to a floor set by the targets while
the true loss goes to zero underneath it, so **the ratio** is what runs away,
and it does so monotonically because it is $1 + \text{excess}/\text{true}$ with
the excess essentially fixed. Both are asserted now \dash{} a Cauchy--Schwarz
bound that holds for any sample, and the ratio's ordering.

**And the ratio did not reproduce from the page.** At three decimals the good
fit prints $0.009$ and $2.62/0.009 = 291$ against a stated $286$. That is F04's
`22 778` and F05's `51.7` for the third time, so the script now carries the
check as code: it formats both operands and the ratio exactly as the page will,
divides, and fails if the answer differs. Four decimals fixes it.

#### Also

- Traps 112 to 118 added to `notes/02`, which had **nothing** on shapes before
  this pass \dash{} the review's \enquote{largest content gap} arriving from a
  second direction.
- **Elicitation 40%, the highest in Parts II and III**, from two conversions
  that added no frame: the column-wise bias shape and the reshape-safety rule
  are now elicited rather than stated. The second moved a `trapbox` up one frame
  so the answer block could open the next one, which is the P06 pattern.
  The two cues cost `main-en` two pages, which is the measured price.
- **Three Polish parity failures, all one class and all the same word.**
  *jedynkami*, *jedynką* and a third for `$1$` \dash{} Polish reaches for the
  spelled-out numeral far more readily than English, and *pad with $1$s*
  invites it three times in one program. Write *wartościami $1$*.
- A 6.0 pt box in `main-pl` from two coordinate tuples run into one sentence,
  and one orphaned cue in `main-en-a4`. The first was fixed by splitting the
  sentence in both editions; the second by **lengthening** the frame, which is
  now the fifth confirmation of F06's two-sided rule. The paragraph added earns
  its place: it says what each of the three axes runs over, which makes the
  shape concrete without touching the question below it.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P7.1 axes-not-directions | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P7.2 broadcast-alignment | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P7.3 reshape-or-permute | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's own wrap cap on the first render, so no redesign.

**Rule 2, read first and then measured.** P7.1 sits after the answer it
explains in all four builds and P7.3 sits below both its question and its answer
on one page in all four. **P7.2 sits above its elicitation in all four and that
is not a defect**, for the reason F03's second review pass established and P04
restated: it carries the alignment rule, which the frame above states in full,
and the question below asks for the resulting *shape*, which appears nowhere in
the figure. A figure the reader is meant to *apply* belongs above the question,
not below it.

### Program P8 pass, August 2026

**Thirty-four teaching frames, thirty-six printed, both editions**, against a
brief that projected sixty. Five sections: what a matrix reaches and what it
discards, one number rather than two, solving what has no solution, a rank
imposed on purpose, and a rank lost by accident.

Eighth program running under its brief's estimate, and the reason is the
familiar one plus a new instance of it. **P04 already has rank as a computed
quantity** \dash{} of a *set of vectors* \dash{} and its trapbox already says
that the random draws are testing the code rather than hunting a
counterexample. So the saturation demonstration was spent, and what was left
is the better half: rank as a property of a **matrix**, which brings the four
subspaces and the row-rank/column-rank theorem with it.

And **P05 hands least squares over twice and by name**: *the same formula
projects onto a line in any number of dimensions, and onto a subspace, and
\dash{} once Program P08 arrives \dash{} onto the column space of a matrix,
which is what least squares is.* So §3 is one object swapped into a derivation
the reader already had, and it says so: nothing new is defined to get the
orthogonality characterisation, and the answer comes with the swap.

#### The worked example is exact and hand-checkable, which was the point of choosing it

Three points, $(1,1)$, $(2,3)$ and $(3,2)$, fitted by
$y = \val{p08.ls.slope}x + \val{p08.ls.intercept}$. The residuals are
$-\frac{1}{2}$, $1$, $-\frac{1}{2}$; both orthogonality conditions are
**exactly zero**; the sum of squares is $\val{p08.ls.sse}$. A reader can check
the whole thing on the page without a calculator, and the frame asks them to.

The script asserts the **defining property** rather than the answer \dash{} the
residual is orthogonal to every column \dash{} and then perturbs the fit in
eight directions and requires every one to be worse, so \enquote{closest} is
measured rather than asserted. The points were searched for, not chosen: they
had to give small rationals in the fit, the residuals and both dot products at
once.

#### Three measurements, all exact over the rationals

No epsilon anywhere, and the elimination is P04's reused unchanged, on purpose:
two programs that both talk about rank must not be able to disagree about what
one is.

- **Row rank equals column rank** on $\val{p08.rank.trials}$ matrices of
  assorted shapes, half of them deliberately built rank-deficient with a thin
  middle. P04's framing carries: a search that succeeded would have refuted a
  proof, so the draws are testing the code.
- **A rank-$\val{p08.chain.r}$ bottleneck survives $\val{p08.chain.len}$
  full-rank $\val{p08.chain.d} \times \val{p08.chain.d}$ factors** stacked on
  top with its rank unchanged. That is the exact mechanism under what the
  literature calls rank collapse \dash{} and the program is careful that they
  are not the same claim.
- **The low-rank update priced**: $\val{p08.lora.lowrank}$ against
  $\val{p08.lora.dense}$, a factor of $\val{p08.lora.factor}$ and
  $\val{p08.lora.pct}\%$. The ratio is $2r/d$ and depends on nothing about the
  model.

**The crossover is the part nobody quotes**: $2dr = d^{2}$ exactly at
$r = d/2$, so an adapter with an inner dimension above half the width
\emph{costs more} than the dense update while still constraining it. Nobody
sets $r$ that high, which is why the threshold is worth knowing \dash{} it says
the saving comes from $r$ being small relative to $d$ and from nothing else.

#### The claim the program refuses to make

The brief asks for rank collapse in deep attention stacks \enquote{described as
the phenomenon it is}. §5 proves the bottleneck theorem exactly and then puts
the phenomenon in a `warning` box saying **this book has not measured it and it
is not the same statement**: the theorem is about a narrow map in the chain,
the phenomenon is about a stack with no narrow layer in which the rank falls
anyway, which is a claim about training and the softmax rather than about what
shapes force. What would settle it is the singular-value spectrum at each
depth, which needs P11 and a real model.

That split is worth more than a paragraph of hedged prose, and it is the same
move P05 made with its capacity threshold.

#### The orphaned-cue random walk, in its clearest instance yet

Three rounds, and each one moved the defect rather than clearing it:

| round | edit | result |
|---|---|---|
| 1 | lengthened `main-en`'s frame 19 | en cleared, **two** appeared in `main-pl` |
| 2 | lengthened frames 23 and 27 | pl cleared, **one** appeared in `main-en-a4` |
| 3 | lengthened frame 27 again | all four clean |

This is what CLAUDE.md means by a random walk across four paginations, and it
is the first time it has taken three rounds. Every edit was made in **both**
editions, so the two still say the same thing, and every added paragraph earns
its place \dash{} that checking the two dot products is checking optimality
rather than arithmetic; that the two thin factors are the whole of what is
stored and trained; and that a constraint costing nothing would buy nothing.

Note that the fix was **lengthening** every time. That is now the sixth
confirmation of F06's two-sided rule and it has not failed yet.

#### Also

- Traps 119 to 125 added to `notes/02`.
- **Parity came back clean on its first run**, on a program of this size, which
  has now happened twice (P02 was the first). The accumulated translator rules
  did it: no number spelled as a word, and every possessive attached to a
  reference built the other way round while drafting.
- Elicitation 35%, from five conversions that between them added one frame. The
  best of the five is frame 3's: after naming the four subspaces, ask which two
  live in the space $A$ reads from \dash{} because the null space is the one
  people put in the wrong room, and sorting them once is what makes §1's
  rank--nullity frame land.
- A cross-programme gate on P04's `p04.embed`, wired to a shared computation
  rather than a coincidence: this program quotes the same integer to bound an
  embedding matrix's rank, so if P04's dimension moves the bound is quietly
  about a different model and the build says so.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P8.1 one-number | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P8.2 closest-in-the-space | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P8.3 thin-middle | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's own wrap cap on the first render, so no redesign.

**Rule 2 read first and then measured.** All three figures carry an answer to
something the reader is asked \dash{} the shared dimension, what the residual is
perpendicular to, and what the rank constraint assumes \dash{} and all three are
declared after the frame that delivers it, which a float cannot rise above.
Measured on the page: question, answer, figure, in that order, in all four
builds.

### Program P9 pass, August 2026

**Thirty-seven teaching frames, thirty-nine printed, both editions**, against a
brief that projected forty-five. Five sections: what one number can say about a
whole map, zero and what it destroys, scale factors multiply, the inverse and
why the code does not form it, and change of basis.

Ninth program running under its brief's estimate, and this time three
neighbours had each taken a piece. **P04 already does change of basis as a
worked example** \dash{} the point $(3, 4)$ against axes turned by $30$
degrees, coordinates changing and length not \dash{} so the idea was spent and
what was left is better: the change is itself a **matrix**, and it is
invertible exactly because nothing was destroyed. **F08 has rotation matrices
and rotary position embedding in full**, so P09 adds one frame rather than a
section: the reading F08 could not give, that a rotation is an orthogonal
change of basis and therefore costs the model nothing. And **P08 hands the
program over by name**, which makes the $\det = 0$ frame a gate rather than a
finding.

#### The brief pointed at the wrong neighbour, and it was the program's own brief

P09's manifest entry says the cost of \code{inv()} is \enquote{stated here,
measured in P10}. It is wrong twice. **P10 undertakes no such measurement**
\dash{} it is eigenvalues, the spectral theorem and quadratic forms \dash{}
while **P11 undertakes \enquote{why the normal equations square the condition
number and a QR solve does not, which is the concrete form of do not
invert}**. And the operation count is not merely stated here, it is
**measured** here.

Seven passes have now found a claim about another program that needed fixing,
and this is the first where it was **the program's own brief** rather than a
frame's forward pointer. The manifest is amended: the operation count measured
here, the accuracy argument owned by P11. Checking cost two file reads.

The split is the F07/F12 one again and it makes the section better rather than
shorter, because it lets §4 close on a sentence neither program could write
alone: the operation count is measured here, the accuracy is P11's, **and the
accuracy is the half that decides the argument**.

#### The cost is a measurement of the code beside it

Both routines count their own arithmetic as they do it \dash{} every multiply
and every divide increments a counter \dash{} so nothing on the page is quoted
from a textbook's $n^{3}/3$. At $n = \val{p09.cost.n}$, elimination costs
$\val{p09.cost.solve}$ multiplications and divisions against
$\val{p09.cost.invert}$ for forming the inverse and multiplying, a factor of
$\val{p09.cost.ratio}$ \dash{} and the script asserts that the two routes agree
**exactly** over the rationals first, because a difference between them would
have made the comparison about something else.

The reason is then one sentence: elimination builds $n$ numbers and the inverse
builds $n^{2}$, of which you use $n$.

#### A third kind of cross-programme gate: a shared PREDICATE

The gates this book has built so far read another program's committed
**value** and assert agreement. P09 has one of those \dash{} the
change-of-basis matrix applied to P04's point at P04's angle must return P04's
own two committed coordinates \dash{} wired to a shared computation rather than
a coincidence, on P04's own rule.

But the $\det = 0$ frame needed something else. P08 defines singular by rank
and P09 defines it by volume, and **the two programs must not be able to
disagree about which matrices are singular**. So the script computes both, from
the same elimination P04 wrote and P08 reused unchanged, and asserts they name
the same set: on $\val{p09.sing.trials}$ matrices, $143$ of them singular,
$\det A = 0$ and $\operatorname{rank} A < n$ agreed every time.

That is not a value gate and it is not a discovery. It is two definitions
checked against each other, and it costs three lines. **Use it wherever two
programs define the same predicate two ways.**

#### The diamond hazard, a fourth time, and the fix is settled

`p09-solve-or-invert` was first drawn as a fan-out \dash{} one node branching
into two \dash{} and came out **433.92 pt wide**, which is 10.17 pt in the
trade format and **11.54 pt on A4**, by some way the largest node text in the
book. That is exactly F08's `rotate-both` figure to the hundredth of a point,
which is worth knowing: **a two-column LR graph at this node width lands at
433.92 pt every time.**

The recorded fix applied unchanged and on sight: **add a rank.** Converging the
two branches on a fourth node took it from two columns to three and from
433.92 pt to the wrap cap. Wordier nodes would have done nothing, because
mermaid was already wrapping. That is now three uses of the add-a-rank fix
(F09, F11, P09) and none of the wordier-nodes fix on a wrapping graph.

#### A macro from a conditionally-loaded package is invisible to both machines

The draft used `\begin{psmallmatrix}` in a summary item and two exercises.
`psmallmatrix` comes from **mathtools**, and `preamble.tex` loads mathtools
inside an `\IfFileExists`. So on a TeX installation without it the build dies
on an undefined control sequence.

The part worth recording is that **neither of this project's two machines would
have caught it.** This container has mathtools and CI has a fuller TeX Live
than this container, so both compile it. The `amssymb`/`newtxmath` trap is a
full installation failing where a bare one passes; the `upquote` trap is a bare
one shipping what a full one hides; this is the third direction, where the
defect is latent on every machine that exists here and waits for a reader's.

`preamble.tex` has eleven `\IfFileExists` probes and **mathtools is the only
one of them that supplies macros the prose can use** \dash{} the rest are fonts,
`babel`, `upquote`, and `csquotes`, which has a fallback branch. So the rule is
narrow and checkable: **before using a maths macro you have not used before,
grep the preamble for the package that defines it.** No gate was added, because
this has never shipped; the rule is recorded so that the first time it does,
somebody knows where to look.

#### Layout

The multiset came back **element for element** to the pre-P09 baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with no stranded openers,
no stranded headings, and **no orphan tails added at all**, which has now
happened three times (F13, P07, P09).

Two things had to be cleared to get there, both recorded classes and both
applied on sight once the build named them:

- **A 3.5 pt box in `main-en` alone**, from `$\det(A^{-1})\det(A) =
  \det(A^{-1}A) = \det I = 1$` run inline \dash{} a chain of four unbreakable
  maths spans with almost no break opportunity in it. Into a display, which is
  F06's rule, and it went to zero.
- **One orphaned cue in `main-pl`**, the tail of frame 20. Cleared by
  **lengthening**, sixth confirmation of F06's two-sided rule, and the
  paragraph added earns its place: it says why the question is only put to a
  square matrix, which is Program~\ref{prog:P08}'s two shape facts doing a
  third job. `main-pl` lost two pages with it.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P9.1 one-number | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P9.2 zero-means-flat | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P9.3 solve-or-invert | 657 / 657 | 2.82 | 6.71 | 6.71 | 7.62 | 7.62 |

**Rule 2 read first and then measured.** Only `p09-zero-means-flat` states an
answer outright \dash{} its first node *is* frame 9's answer \dash{} but all
three were placed after the frame that delivers what they carry, and all three
land in the order question, answer, figure in every build:

| build | fig1 / fr1 / fr2 | fig2 / fr8 / fr9 | fig3 / fr24 / fr25 |
|---|---|---|---|
| `main-en` | 565 y586 / 564 / 565 y96 | 569 y493 / 568 / 568 y194 | 575 y321 / 574 / 575 y96 |
| `main-pl` | 576 y130 / 574 / 575 y96 | 579 y493 / 578 / 578 y194 | 585 y310 / 584 / 585 y96 |
| `main-en-a4` | 475 y437 / 474 / 474 y514 | 478 y372 / 477 / 477 y203 | 483 y224 / 482 / 482 y380 |
| `main-pl-a4` | 479 y437 / 478 / 478 y513 | 482 y395 / 481 / 481 y213 | 487 y224 / 486 / 486 y517 |


#### Also

- Traps 126 to 131 added to `notes/02`.
- **Elicitation 40%**, the joint highest in Parts II and III with P07, from two
  conversions that added no frame: the $2 \times 2$ formula is now applied to
  the swap and answered overleaf rather than checked in passing, and the
  condition a change of basis puts on its determinant is asked rather than
  stated. The second produced the P06 pattern again \dash{} a frame that opens
  with `\ans` and ends with `\dotline`.
- **Parity came back clean on its first run**, which has now happened three
  times (P02, P08, P09). The translator rules are doing it: no number spelled
  as a word, and every possessive attached to a reference built the other way
  round while drafting rather than after a failure.
- The trapbox claiming a shear has determinant $1$ and stretches is **gated
  rather than argued**: the script asserts $\det S = 1$, that $S$ sends
  $(0,1)$ to $(1,1)$, and that the squared length becomes $2$. It emits
  nothing, because those are numbers the reader does in their head \dash{} but
  an assertion costs nothing and a claim in a printed box should not rest on
  the author having done the arithmetic in their head either.
- Frame numbers were mapped after writing: sections landed at
  `1--7 / 8--14 / 15--19 / 20--27 / 28--37`.

### The manifest's own pointers were one low, August 2026

Found while reading P10's brief before writing it, which is the discipline five
passes have now paid for \dash{} and this time the thing that was wrong was not
a frame's forward pointer but **`tools/programs.json` itself**, the file this
document tells everybody to re-derive owners from.

**The mechanism, and it is entirely explicable.** The curriculum review inserted
**P7** and moved everything after it up one. It renumbered the *sequence*, and
it re-derived the *declared forward-reference list* \dash{} which is why P18's
and P22's briefs name P26, P30 and P18 correctly. **It never swept the ordinary
payoff prose.** So twenty pointers inside nine briefs still named the program
that used to hold the material.

The clearest case is the one that would have shipped: P10's payoff says the
Hessian's eigenvalues are \enquote{collected here and spent in P16 and P19}.
P16 is *autodiff* and P19 is *convexity and Jensen*. The programs that spend
them are **P17**, whose own brief says *why the largest stable learning rate is
bounded by the inverse of the curvature*, and **P20**, the optimiser program.
Issue \#24 says P17 and P20, and F11 and F12 both point their curvature
material at P17 \dash{} so the manifest disagreed with the issue derived from
it, with two written programs, and with the destination briefs.

**Every one of the twenty was confirmed against the destination program's own
brief, which undertakes the named thing in as many words.** None was inferred
from the off-by-one alone, and the pointers that were already right were left
alone: P17's *joining P9 and P10 to the optimiser*, P18's and P22's declared
references, P03's P32, and every reference to P1 to P6, which the insertion
could not move. The full list, with the destination's own words as the
justification for each, is in the commit that made the change.

**The generalisable finding is about where a rule lives.** This file already
says *never copy an owner out of `notes/02`; re-derive it from
`tools/programs.json`* \dash{} a rule written after the same defect was found in
the trap catalogue. The rule was right and its destination was not audited, so
the defect simply moved into the file the rule points at. **A rule that names a
source of truth has to be accompanied by a check on that source**, and there
still is not one: nothing compares a brief's prose pointers against what the
named program undertakes, because doing it mechanically needs the briefs to be
machine-readable in a way they are not.

What *is* mechanical and worth re-running after any curriculum change is the
listing that found this: print every `P<n>` in every brief with its surrounding
clause and the title of the program named, and read the column. It took one
pass over 47 entries.

#### And a sixth undeclared forward reference, found the same way

Checking the declared list against the graph is how the review found the fifth
(P22's KL). The same check finds a sixth, and it is in a **merged** program:
**P07 prints $\operatorname{Cov}(p, t)$ and $\operatorname{Var}(t)$ in its
headline identity and declares neither.** Both are defined in P24, seventeen
programs later.

It is milder than P18's and P22's, because P07 never asks the reader to *know*
what a covariance is \dash{} the sentence it needs (*a covariance is exactly
what training increases*) is delivered in the frame. But the identity is
*stated in terms of* the two, so a reader who has not met them cannot check the
line the whole section rests on, which is the bar P18 and P22 are held to.

**Recorded rather than fixed**, on this file's own rule about rewriting merged
programs inside a pass about something else. The fix is one clause in P07's
Learning outcomes, on the P21 pattern. Whoever takes it should also decide
whether the rule is *declare anything not yet defined* or *declare anything a
payoff depends on*, because P07 is the first case where those two answers
differ.

### Program P10 pass, August 2026

**Forty-three teaching frames, forty-five printed, both editions**, against a
brief that projected sixty-five \dash{} the largest estimate in the manifest.
Five sections: a direction the matrix only stretches, three ways the promise
fails, the spectral theorem, a bowl a saddle or a ridge, and the shape of
something.

**The under-estimate has a different cause this time, and it is worth
separating from the previous nine.** Those came in short because a neighbour
had already spent the material. Here nothing had: a grep for \emph{eigenvalue},
\emph{eigenvector}, \emph{spectral norm}, \emph{Hessian}, \emph{PCA} and
\emph{positive definite} across every written program found the words only in
file headers saying \enquote{-> P10}. P10 is the first program in Part III with
genuinely unspent ground. What made it shorter than sixty-five is that its
neighbours supplied the \emph{machinery} rather than the content \dash{} the
null space, the determinant, the dot product and the basis are all borrowed, so
the derivations are short even though the ideas are new.

#### The spectral theorem, demonstrated with no rounding anywhere

The construction is Program~\ref{prog:P09}'s rational $3$--$4$--$5$ rotation.
$A = QDQ\T$ with rational $Q$ and $D$ is a rational \emph{symmetric} matrix
whose eigenvalues \emph{are} $D$'s entries and whose eigenvectors \emph{are}
$Q$'s columns \dash{} known by construction rather than found by a solver. So
$\val{p10.spectral.trials}$ trials check every eigenvalue, every eigenvector
and every right angle over fractions.

**Why that is worth the lines, and it is not the obvious reason.** Going the
usual way round \dash{} pick a symmetric matrix, solve for its eigenvalues
\dash{} the discriminant is almost never a perfect square, so the answers are
irrational and there is nothing exact left to compare. This is the only place
in the book where a claim containing the word \emph{exactly} is checked with
arithmetic that is itself exact; a float test would have needed a tolerance,
which is what that word refuses.

#### The gate P09 asked for

P09's closing frame promised that the determinant is the product of the amounts
the surviving directions are stretched by. That is now arithmetic rather than a
sentence: the script computes the determinant with **P09's own `det()`** and
asserts it equals the product of the eigenvalues, and the trace their sum.

#### An assertion refuted its own frame, for the tenth pass running

The ridge case \dash{} eigenvalues $5$ and $0$ \dash{} was asserted to have a
sampled minimum of zero over $\val{p10.form.dirs}$ directions. It failed
immediately and deserved to: **the flat direction is one direction out of
infinitely many and sampling will never land on it.** That is P05's
\enquote{finding nothing is not measuring nothing} from the other side.

The replacement is two assertions rather than one \dash{} sample for
non-negativity, and evaluate \textbf{exactly} at the eigenvector the
construction already knows \dash{} and it produced the section's best sentence:
*you cannot find a flat direction by looking for it*, which is the argument for
computing eigenvectors at all.

#### The measurement people get wrong

Eigenvalues $\val{p10.basin.hi}$ and $\val{p10.basin.lo}$, a ratio of
$\val{p10.basin.eigratio}$ \dash{} and the level ellipse is
$\val{p10.basin.axisratio}$ times longer than it is wide. **The square root**,
because the form carries the coordinate squared. Most readers answer
$\val{p10.basin.eigratio}$. Guarded, on the recorded rule, so that the printed
axis ratio reproduces from the printed eigenvalue ratio.

That ratio is where \enquote{ravine}, \enquote{sharp minimum} and \enquote{the
learning rate is too high} become three numbers read off one matrix. **The
shape is collected here and deliberately not spent**: the inequality is
Program~\ref{prog:P17}'s and the optimisers are Program~\ref{prog:P20}'s, which
is what the manifest says now that the sweep before this program corrected it
from P16 and P19.

#### The declared forward reference, discharged rather than owed

The manifest requires the covariance matrix's two facts to be declared, since
P24 defines it. They are declared \dash{} and both are **proved here** from
$C = \frac{1}{n}X\T X$, symmetric by construction and positive semi-definite
because $v\T Cv = \frac{1}{n}\lVert Xv\rVert^{2}$ is a sum of squares. So
nothing waits on P24 but the meaning of the word, and the note says the pointer
is an attribution rather than a debt. Worth copying: a forward reference whose
facts can be proved locally should be.

#### The orphaned-cue random walk, two rounds

| round | edit | result |
|---|---|---|
| 1 | lengthened frames 20 and 33 | `main-pl-a4` cleared, `main-en` gained one and `main-en-a4` went 1 to 2 |
| 2 | lengthened frames 26 and 33 again | all four clean |

Seventh confirmation of F06's two-sided rule, and the second time one frame
needed lengthening twice. Every paragraph added earns its place: why the
construction runs backwards from the answer; that a worst-case bound is the one
that \emph{composes} where average behaviour does not; and that writing $x$ in
the eigenvector basis is the step silently carrying the spectral theorem.

#### `\blank` returns after thirteen programs

CLAUDE.md recorded that the last `\blank` in the book was in F07. P10 has two,
both in the classification table, where the reader fills in \emph{saddle} and
\emph{ridge} from the sign patterns above them. It is a distinct retrieval mode
and the F02 review pass called skipping it a lost rung of the scaffolding
gradient; it is available in a `tabularx` cell, which F04 and F05 already use.

#### Layout

The multiset came back element for element to the pre-P10 baseline in all four
builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with **no overfull box added at
any point in the pass**, no stranded openers and no stranded headings. One
orphan tail added, in `main-pl-a4`.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P10.1 only-stretched | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P10.2 bowl-or-saddle | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P10.3 ellipse-axes | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, so no redesign.

**Rule 2 read first and then measured.** `p10-only-stretched` carries frame 1's
answer in its second node and `p10-bowl-or-saddle` carries frame 29's in its
third; `p10-ellipse-axes` states that one ratio describes the elongation and
stops short of the square root, so it does not answer frame 36. All three are
declared after the frame that delivers what they carry.

| build | fig1 / its answer | fig2 / its answer | fig3 / its answer |
|---|---|---|---|
| `main-en` | 587 y479 / 587 y146 | 599 y130 / 598 y144 | 601 y569 / 601 y303 |
| `main-en-a4` | 495 y315 / 494 y650 | 504 y334 / 503 y494 | 506 y612 / 506 y327 |
| `main-pl` | 598 y130 / 597 y337 | \dash{} | 611 y541 / 611 y303 |
| `main-pl-a4` | 500 y288 / \dash{} | \dash{} | 511 y641 / 511 y402 |

**The Polish dashes are extraction failures, not defects, and saying so is the
honest form.** `pdftotext` hyphenates the Polish anchors and the phrase search
could not find three of them. The structural argument covers those cases and is
the one this file already records as making the fix sound: a float cannot rise
above the page its declaration point falls on, and all three declaration points
are after the frame that delivers the content. The English columns measure the
same source in both formats.

#### The transcript splits across a page break

Extracted from the finished PDF and executed, it reproduces
`[Fraction(0, 1), Fraction(1, 1)]` exactly \dash{} zero for the symmetric
matrix, one for the non-symmetric. But the seven lines land 3 on one page and 4
on the next, so the extraction had to join two pages.

Not a defect \dash{} the P06 sweep already found one listing broken this way,
and this one sits after the answer it evidences rather than before a question.
Recorded because **an extraction script that assumes a listing is on one page
will silently read a fragment**, which is how the first attempt here reported a
one-line transcript and a `None` output.

#### Also

- Traps 132 to 137 added to `notes/02`, and **items 13, 14 and 15 corrected**:
  13 pointed at P08 and belongs to P09 (where it is now items 129 and 130), 14
  pointed at P09 and is P10's own trap, 15 pointed at P10 and is P11's. Item 16
  is marked delivered. Each was settled against the destination program rather
  than by assuming the off-by-one. **The rest of §3 is not swept** \dash{} items
  74 onward are correct, items 1--73 are a mix because several were corrected by
  hand as their program was written, so a blanket renumber would break the ones
  that are right. It is a pass of its own.
- **Parity clean on its first run**, on the longest program written so far.
  Fourth time (P02, P08, P09, P10).
- Elicitation 39%, from six conversions that between them added no net frame.
  Two produced the P06 pattern \dash{} a frame opening with `\ans` and ending
  with `\dotline`.
- Frame numbers mapped after writing: sections landed at
  `1--10 / 11--17 / 18--23 / 24--32 / 33--43`.

### Program P11 pass, August 2026 --- Part III is complete

**Thirty-three teaching frames, thirty-five printed, both editions**, against a
brief that projected sixty. Five sections: what survives when the theorem does
not, not eigenvalues, keeping the largest pieces, error in and error out, and
why the code does not form $A\T A$.

Part III is now written end to end, and its shape came out as one argument:
Program~\ref{prog:P04} asked what a space is, \ref{prog:P06} made a matrix a
function, \ref{prog:P08} counted how much survives it, \ref{prog:P09} measured
how much, \ref{prog:P10} found the directions that survive unturned, and this
program says every matrix has all of it in one factorisation.

#### The construction extends P10's by exactly one degree of freedom

P10 built $A = QDQ\T$ with the **same** $Q$ on both sides, because a symmetric
matrix's two sets of directions are the same set. Here they need not be, so two
different rational rotations \dash{} $3$--$4$--$5$ and $5$--$12$--$13$ \dash{}
give $A = U\Sigma V\T$ rational and **not** symmetric, with singular values
$\val{p11.sig.hi}$ and $\val{p11.sig.lo}$ exactly because they were put there.
$Av_i = \sigma_i u_i$ is then checked over fractions.

**And that example makes the trap hard rather than easy.** The same matrix's own
eigenvalues are $\val{p11.lam.hi}$ and $\val{p11.lam.lo}$ \dash{} a $5\%$
difference no plot would show. A wildly different pair would have been a weaker
example, because the question is why the confusion survives.

#### The headline measurement, and the cell was chosen by measuring

The debt Program~\ref{prog:P09} handed over by name \dash{} \emph{the accuracy
is P11's, and it is the half that decides the argument} \dash{} is paid with a
number: a degree-$\val{p11.ls.deg}$ fit through $\val{p11.ls.points}$ points,
solved twice in float64, the factorisation clearing $\val{p11.ls.qr.bound}$ and
the normal equations failing $\val{p11.ls.ne.floor}$.

**The first assertion failed**, because degree $6$ is not ill-conditioned
enough, and the fix was to sweep degrees $6$ to $14$ and read the table rather
than guess again. Degree $12$ was rejected on *pedagogy* rather than on
arithmetic: it gives an answer $395\%$ wrong, which reads as a broken program.
Degree $8$ gives one that looks plausible and is wrong from the sixth
significant figure, which is the failure people actually ship.

**Every number in that section is a bound or a count**, and the four digits are
derived from the two committed bounds rather than from the measurement, so they
cannot drift between machines even by one. That is the P06 residual rule applied
before CI could apply it.

#### Rule 2 caught a figure twice, and the second catch is the recorded one

`p11-keep-the-largest`'s third node said *throwing away the smallest pieces
costs exactly what those pieces were contributing* \dash{} which is frame 15's
answer, sitting before frame 14's question. Reworded to say that the pieces can
be judged one at a time, which is what the frames above it deliver.

**Then the caption still said it.** \enquote{Why dropping the smallest pieces
costs exactly what they were worth} is the same spoiler one line lower, and it
survived the node fix because a caption does not read like part of the figure.
That is exactly F02's finding \dash{} the identity was \enquote{in a node and
again in its caption} \dash{} and it is the second time this book has fixed a
node and left the caption. **Read the caption as a node.**

#### Also

- Traps 138 to 143 added to `notes/02`, and item 15 marked delivered.
- **Parity took four rounds**, all recorded classes: a number and a reference in
  the wrong order in a quiz item, a `Program~\ref{...}'s <maths>` inversion, one
  Polish sentence repeating `$\sigma_2$` where the English used a pronoun, and a
  `\mermaidfig` I forgot to place in the Polish at all. The last is worth
  naming: **C9 catches a diagram present in one edition only**, and nothing else
  would have.
- Two bare decimals inside maths (`0.8`, `1.6`) needed `\num{}`; C10 caught them
  in the English, which is the edition that does not obviously owe a comma.
- Elicitation 39%, from five conversions that added no frame. Two produced the
  P06 pattern.
- The orphaned cue took one round of lengthening in each A4 build, and both
  added paragraphs earn their place: that a condition number is closer to a
  weather forecast than to a diagnosis, and that all three steps of the
  pseudoinverse are things the program has already named.
- Layout: multiset element for element the pre-P11 baseline in all four builds,
  no stranded openers or headings, one orphan tail added.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P11.1 three-moves | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P11.2 keep-the-largest | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P11.3 error-in-error-out | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

#### What P11 does NOT claim, and the brief asked for it

The brief asks for \enquote{the singular-value spectrum of a real embedding
matrix, plotted, showing how few directions carry the energy \dash{} the
empirical case for LoRA and for embedding compression, **measured**}.

That needs a real model. This book does not have one and does not download one,
and constructing a spectrum with a plausible decay and reporting it as a
measurement is precisely the fabrication this book's rules forbid. So the
spectrum in §3 is **constructed and labelled as such**, it demonstrates the
mechanism, and a warning box states the empirical claim, says the book has not
measured it, and says what would settle it.

That is Program~\ref{prog:P08}'s precedent for rank collapse, and P08 had
already anticipated it: its own warning box says the phenomenon \enquote{needs
Program P11's machinery **and a real model**}. The machinery is now here. The
model is not, and both programs say so.

**The manifest brief is left as written**, because it describes what the program
should contain when the book can afford it, and softening it would hide an
outstanding piece of work. It belongs on the *What is left* list instead.

### Program P12 pass, August 2026 --- Part IV begins

**Forty-three teaching frames, forty-five printed, both editions**, against a
brief that projected forty-five. Five sections: two questions before any
formula, arrangements and choices, the rules that are not products, how many
bits a hash needs, and two counts that decide a design.

**It is the cheapest program in the book by every layout measure and the
richest by the elicitation one.** Zero new overfull boxes in any of the four
builds on the first attempt, no stranded openers, no stranded headings, no
orphaned cues, and **the orphan-tail count did not move at all** \dash{} the
fourth time (F13, P07, P09, P12) and every time for the same reason: the
recorded rules were applied while drafting rather than after a build named the
defect. Parity needed one round.

#### The open curriculum question was decided, and one of its two arguments was dead

`notes/01-curriculum.md` §20 item 4 asks whether this program stays in Part IV
or opens Part VII, ten programs nearer the probability that consumes it, and
the issue says to decide before writing. **Decided: it stays**, and the entry
now records both the decision and the fact that **one of the two arguments it
gave for staying is falsified by the written book.**

\enquote{P12 also feeds P3} is not true. `P03` is written and merged and needed
nothing from combinatorics, because `F10` supplied every count it used; and
`P13`'s declared dependencies are `F10, P6, P10`, not this program. So nothing
in Part IV depends on P12 at all, and the case cannot rest on the graph.

What it rests on instead is better: **P12's own three payoffs are counting
payoffs rather than probability ones** \dash{} sizing a hash, the size of a
beam search's space, the cost of an exact Shapley value \dash{} and only the
birthday calculation touches probability, needing nothing beyond F10's
two-counts-and-a-division. The gap is paid inside the program instead, by
restating the pair count where §4 uses it.

**And the same off-by-one that PR-swept the manifest was still in the notes.**
`notes/01-curriculum.md` §19 carried the whole dependency graph written out,
and every edge from `P7` onward named the program that used to hold the
material \dash{} `P11 <- F10, F4` for combinatorics, and 33 main programs where
there are 34. That is the *third* file to carry it, after the trap catalogue
and the manifest, and it is in the file this document tells everybody to
re-derive owners from.

**The fix was to delete the duplicate rather than correct it.** A corrected
copy is the next thing to go stale at the next insertion, and the live graph
is already machine-readable in each program's `deps` field. §19 now says where
the graph lives, why it is not repeated, and prints the one-line command that
reads it. **A rule that names a source of truth is worth less than deleting
the copies that compete with it.**

#### The regime table, which an assertion produced by failing

The first draft asserted that the closed form tracks the exact product to
$10^{-6}$ at hash scale. It failed \dash{} and the failure named the wrong
suspect, because the degraded expression is the one labelled *exact*.

Measured against a reference that is neither of them (the product summed in
log space, which subtracts nothing from one):

| | the product | the exponential |
|---|---|---|
| 23 people, 365 days | **exact to the last bit** | 1.4e-2 |
| 100 000 hashes, 64 bits | 1.3e-5 | 1.7e-15 |
| 1 000 000 hashes, 128 bits | **1.0** \dash{} it returns zero | 0.0 |

**Each is right exactly where the other fails, and they fail for opposite
reasons.** The product is destroyed by cancellation when the answer is near
zero; the exponential drops a second-order term that matters only when the
terms are large, which is when the answer is near a half. Neither is the safe
default, and a book that had picked one would have been wrong in one of the two
places its own examples live.

The middle row is the one worth keeping. **At 64 bits with only 100 000 items
the textbook expression has already lost five significant figures**, long
before it fails outright: a formula does not stop working at a threshold, it
degrades, and the degradation is invisible until somebody computes the same
thing another way.

#### Program P02's finding, in a hash, and it returns a plausible answer

`1 - prod(1 - i/N)` in float64 at 128 bits returns **exactly `0.0`**. Every
factor is within one part in $10^{33}$ of one and rounds to `1.0`, so the
product is `1.0` and the subtraction has nothing left to say. No exception, no
warning, no `nan` \dash{} a float, and a completely reasonable-looking one.

It is worse than the loss P02 measured, on two counts: there the loss was
digits and here it is all of them, and **the wrong answer is the one that ends
the conversation.** A collision probability of zero reads as a proof of safety.

Written up as a committed transcript, extracted from the finished PDF and run:
both printed values reproduce exactly.

#### The headline, and the ratio that had to be divided as printed

$10^{9}$ documents in a 64-bit hash collide with probability **2.67 per
cent**, against the $\num{5.42e-11}$ that the documents-over-values reading
gives \dash{} a factor of $\num{4.93e8}$, and the difference is entirely that
the quantity is the number of **pairs**. The coin flip is at
$\num{5.06e9}$ documents, which is a corpus that exists.

The ratio is emitted by dividing the two numbers **as the page prints them**,
with an assertion that this agrees with the unrounded ratio \dash{} the rule
F04, F05 and P07 each paid for, applied on sight this time.

And the rule that survives the arithmetic: **a hash's safe capacity is about
the square root of its number of values**, so doubling the bits squares the
corpus rather than doubling it.

#### Three cross-programme gates, all to one program, and one of them is a continuation

F10 is the elementary layer under P12 and says so, so all three gates point at
it. Two are the established kind \dash{} $\binom{n}{2}$ must reproduce F10's
committed pair count, and $\sum_k \binom{n}{k}$ must reproduce its committed
subset count, so \enquote{choices} here and \enquote{pairs} and
\enquote{subsets} there cannot come apart.

**The third is new in kind: the same worked example, continued.** §3's three
evaluation sets are F10's two with a third added, and the gate asserts that the
first two sets have F10's own committed sizes and overlap. That is stronger
than a resemblance and cheaper than a re-derivation, and it is the form to
reach for whenever a program extends an example rather than inventing one.

#### The brief's \enquote{simple recurrences}, read narrowly

Two recurrences, and neither was invented to discharge the brief: **Pascal's
rule**, which is also why `math.comb` never forms a factorial it must divide
away, and **the birthday product**, since $P(m) = P(m-1)(1 - (m-1)/N)$ is how
the number is actually computed. A counting program's recurrence should count
something; a generic worked example of a recurrence would have been padding.

#### Rule 2, and the fourth confirmation that four ranks is too wide

All three figures were first drawn with four ranks and came out **881.04 pt**,
setting 5.01 pt \dash{} below the book's band. Cutting to three ranks took all
six to mermaid's wrap cap. That is F12's rule confirmed from the wide side:
**three ranks is the sweet spot; two is too narrow and four is too wide.**

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P12.1 two-questions | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P12.2 pairs-not-items | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |
| P12.3 orderings-or-subsets | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |

Read by content first and then measured, with the captions read as nodes on
P11's precedent. P12.2 and P12.3 each carry an answer \dash{} that the pairs
are what is counted, and that the orderings collapse \dash{} and both sit after
the frame that delivers it in all four builds. **P12.1 sits above the
elicitation that follows it in all four and that is not a defect**, which is
now the fourth instance of the P04/P07 case: it carries the decision procedure,
which the frame above states in full, and the question below asks for
$\val{p12.four.n}!$, which appears nowhere in it.

#### CI failed on the index, and it took five cycles because the page number lied

The first CI run failed `en` A4 alone on **two overfull vboxes, 12.29 pt and
4.99 pt**, on source that built with zero vboxes here. That is the recorded
two-installations divergence. What made it expensive was not the divergence.

**Two of the five cycles were tooling and were worth it.** `checklog.py`
reported the sizes and not the pages, so the report said a page was 12.3 pt
too tall and not which page; it now prints the page, or the file and line for
a fixed box, and the two are distinguished because they need different fixes.
The workflow threw the log away, so after a log-only failure the one artefact
anybody wants was the one not kept; it is uploaded now, and a step prints
TeX's own words around each complaint.

**Three of the five were wrong, in the same way twice.** The page number said
639 of 660; 21 from the end of a 670-page local build is the answers
appendix; so the answers appendix was fixed, three times, and **not one of the
three moved the reported size by a tenth of a point.** That invariance was the
evidence and it was read as something else twice \dash{} once as proof the
list needed shrink, once as proof the box was not a page at all.

It is the **index**, and the raw log says so in one line: `(./main-en-a4.ind
[637 ] [638]` and then both complaints. Two complaints on one page in a
two-column region is one page overflowing in both columns, which is the shape
this file already records for the same file. The cure is the one already
recorded for it too: `theindex`'s `\parskip` shrink, from 0.2 pt to 0.5 pt,
because a fifth of a point over forty entries is eight and eight does not
absorb twelve.

**The lesson is not about vboxes.** A PDF page number is not a location when
two installations paginate differently \dash{} the two builds differ by ten
pages overall and by thirty at the index, because the answers appendix sets
much shorter under newtx. Anchor on what TeX says it had open. And read the
raw log before the third fix, not after: the tooling that ended this in one
look was written in cycle four and would have ended it in cycle one.

The answers-appendix changes are kept. Its rigid `\setlength` glue and its
run of twenty-two headings are a real latent fragility of the same class, they
are scoped so that no frame, no cue, no orphan tail and no body page moves,
and they are right for reference matter whatever this failure turned out to
be. They are recorded above as what they are: a second defect found while
looking for the first, not the fix for it.

#### Also

- Traps 144 to 151 added to `notes/02`; items 59 and 61 marked delivered, with
  the note that P12 *refines* F10's independence condition rather than
  repeating it \dash{} what must be fixed is the **number** of options at each
  step, not the options, which is why a shrinking pool multiplies anyway.
- **Elicitation 46%**, the highest outside Part I and the first program in
  Parts II--IV to reach the book's own rate. It was designed in: the two
  questions, the product-rule refinement, the symmetry and the pigeonhole
  guarantee are all elicited before they are stated, and five of the twenty
  cues sit in section 1 alone, which is where a reader's wrong answer is
  cheapest.
- One parity round, two classes, both recorded: the
  `Program~\ref{...}'s <maths>` inversion, and `$0.0$` written as maths where
  it is a **repr** \dash{} a name, like P01's `-inf`, so it belongs in
  `\code{}`. C10 caught it in both editions at once.
- `p12.trap.right` was emitted and removed: the transcript prints it, and a
  value a listing already carries is a second copy nothing would correct. F11's
  finding, applied on sight.
- One value was deliberately *not* emitted twice: $\binom{20}{3}$ is the
  symmetry frame's number and the triples in the ablation count, and the script
  asserts they are equal rather than giving one number two names.
- Frame numbers mapped after writing: sections landed at
  `1--8 / 9--16 / 17--26 / 27--35 / 36--43` against a plan of
  `1--9 / 10--19 / 20--29 / 30--39 / 40--46`.

### Program P13 pass, August 2026

**Thirty-four teaching frames, thirty-six printed, both editions**, against a
brief that projected fifty. Five sections: a set and a relation, two encodings
and two costs, walks are matrix powers, a DAG and the order that makes
evaluation well defined, and where a random walk settles.

**Elicitation 50%** \dash{} the highest outside Part I, and the first program
anywhere in Parts II to IV to pass the book's own rate. It was designed in from
the frame plan rather than retrofitted: every section opens by asking, and the
two questions the reader is most likely to get wrong (what $(A^{2})_{ii}$ is,
and whether different topological orders compute different things) are both put
before they are answered.

#### The ground was unspent, and the neighbours supplied the machinery instead

Unlike P12, this program leans hard on Part III \dash{} and unlike P10, whose
ground was also unspent, the under-run has an easy explanation. A grep for
\emph{adjacency}, \emph{topological}, \emph{PageRank}, \emph{random walk},
\emph{DAG} and \emph{computation graph} across every written program returns
nothing but F10's own file header deferring \enquote{a graph as a set plus a
relation} here by name. So no content was spent \dash{} but three of the four
sections turn out to be one theorem each from a program that is already
written, and a theorem you already have is short to state:

- **§3 is P06.** \enquote{A matrix product is a composition} read backwards
  gives \enquote{$(A^{k})_{ij}$ counts walks of length $k$} in two sentences.
- **§5 is P10.** A stationary distribution is an eigenvector for eigenvalue 1,
  so everything that program said about power iteration applies unchanged.
- **§1's handshake lemma is P12's double counting**, and the complete graph's
  edge count is F10's pair count gated in code.

#### The payoff is an assertion over every order, not an example

Six services, eight calls, $\val{p13.topo.total}$ orderings and
$\val{p13.topo.count}$ topological orders. The script evaluates the graph
under **all four** and requires the results to be identical, which is what
makes the sentence in §4 a fact rather than a demonstration: *a build system,
an agent workflow, a query plan and a forward pass are one object, and all four
are deterministic for the same reason.* Adding one edge to close a cycle makes
the list of orders empty, which is asserted too \dash{} a cycle does not make
evaluation hard, it makes it undefined.

#### Exact over the rationals, twice, and both times deliberately

The walk-counting theorem is checked against walks that are **enumerated**
rather than against a second formula \dash{} $\val{p13.walk.checks}$
comparisons \dash{} because an enumeration cannot be wrong about what a walk
is. And the stationary distribution is solved exactly with P04's Gaussian
elimination and then asserted as $P\T p = p$ with **no tolerance at all**:
\enquote{stationary} is a claim about equality, and a float comparison would
have made it a claim about a threshold.

The dangling-node measurement is the same discipline from the other side. The
mass left after each step is $\frac23$, then $\frac16$, then **exactly zero**
\dash{} so it is reported as a step number rather than as a figure, because
\enquote{0.0000} reads as rounding and this is not rounding. The convergence
residual went the same way: committed as a **bound** rather than a figure,
because P06 had two of exactly those rejected by CI for being machine
properties.

#### Two things caught by checks rather than by reading

- **The file was written to the wrong name.** The manifest says
  `P13-graphs-dags` and thirty-four frames went into `P13-graphs.tex`. That is
  F12's trap exactly, and F12 recorded that the tell is the page count not
  moving \dash{} but here `gen_stubs.py --check` refused before the build
  finished, naming the file and saying to rename it deliberately. **The check
  that F12's failure earned is the check that caught its recurrence.**
- **The transcript named four things it never imported**, which is P04's
  defect. Fixed with two import lines, and verified the only way that means
  anything: extracted from the finished PDF and run, printing the four values
  the page prints.

#### One self-inflicted build failure worth recording

A build was killed with `pkill -f latexmk` to free the tree for a rename, and
the next run died with a hundred copies of `Text line contains an invalid
character` on `main-pl.out` line 26. **A killed latexmk can leave a NUL-filled
auxiliary file**, and hyperref's `.out` is read back on the next run, so the
failure looks like a source error in a file nobody edited. Deleting the aux
tree fixes it. The tell is that the error names an `.out`, `.aux` or `.toc`
rather than a `.tex`.

#### The orphaned cue took two rounds, and both additions earn their place

`main-en-a4` and `main-pl-a4` both orphaned the cue of frame 21; lengthening it
cleared English and moved the Polish one to frame 31. Eighth confirmation of
F06's two-sided rule, and the second time the walk has taken two rounds. What
was added: why the clause \emph{without retracing an edge} is what makes
\enquote{acyclic} a usable word at all, and why PageRank's apparent circularity
is a **condition** rather than a definition \dash{} which is the honest content
of a sentence the frame had been asserting in passing.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P13.1 set-plus-relation | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P13.2 walks-are-powers | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P13.3 order-not-answer | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

**Rule 2 read by content first, captions read as nodes, then measured in all
four builds.** Only P13.3 carries an answer to something the reader is asked
\dash{} whether different orders compute different things \dash{} and it is
declared after the frame that delivers it: question, answer, figure, in that
order everywhere. P13.1 and P13.2 both sit **above** the elicitation that
follows them and neither is a defect, which is now the fifth instance of the
P04/P07 case: each carries what the frames above it state in full, and neither
mentions the quantity the question below asks for (a degree sum, and a reach in
hops).

#### Also

- Traps 152 to 161 added to `notes/02`.
- Layout cost nothing: the overfull multiset is element for element the
  pre-P13 baseline in all four builds, no stranded openers, no stranded
  headings. Two orphan tails added, both in `main-pl`.
- One parity round, one failure, the recorded word-order class:
  `Program~\ref{prog:P12}'s $n!$` against `$n!$ z~Programu~\ref{prog:P12}`.
  Four unused values were cut rather than forced into the prose, on F11's
  finding.
- Frame numbers mapped after writing: sections landed at
  `1--8 / 9--13 / 14--20 / 21--26 / 27--34`.

### Program P14 pass, August 2026 --- Part IV is complete

**Thirty-one teaching frames, thirty-three printed, both editions**, against a
brief that projected forty-five. Five sections: what a theorem is made of,
implication is not equivalence, quantifiers and the order that changes the
claim, three proof shapes and what each would take to break, and three results
this field misquotes.

Tenth program under its brief's estimate, and the reason is a **third** kind.
Nine of the previous ones came in short because a neighbour had spent the
material (the F07/P06 case) or because the neighbours supplied the machinery
(P10/P13). Here neither: **the subject is genuinely small.** Reading a theorem
is three parts, one four-row table, quantifier order, three proof shapes and
three worked misquotations, and there is nothing else in it. Padding it to
forty-five would have meant teaching proof-writing, which the program
explicitly refuses in its own `rigourbox`. A brief's estimate is a planning
figure; a scope statement is a decision.

#### The headline: a tally about the book, in four places, replaced by a universal that was also false

The draft said **fourteen** rigour boxes \dash{} in the file header, frame 1,
the closing frame and further problem 5. There are fifteen counting P14's own,
so the number was right under exactly one reading and would be wrong the day
P15 is written. That is F03's `\mfalogplain` defect repeating: a count in four
places, wrong by five. CLAUDE.md's own rule says **never state a count of
occurrences**, and this pass paid for it again.

**And the fix was itself a defect, which is the better half of the finding.**
Replacing the tally with *every rigour box says: here is the statement, it is
not proved here, and here is where the proof lives* looks safe, because a
universal is checkable where a tally is not. So it was checked, by opening all
fifteen \dash{} and it is **false**. Four point at a **later program** rather
than at a proof (P01 twice, P02, P03), and P04's second points at a
**measurement nobody has made**. What is true of every one of them:

> each names something the program is not doing, and says where it is done
> instead \dash{} usually a first course, sometimes a later program here, and
> once a measurement that has not been made.

**The rule this earns: replacing a tally with a universal is not automatically
safe.** A universal is the stronger claim, so it needs the same treatment the
tally needed \dash{} open every instance. Both drafts of that sentence were
written from the feel of the boxes rather than from the boxes, which is the
same failure twice in one pass. It is the eleventh pass running where a claim
about another part of the book was the thing that needed fixing, and the first
where the fix for such a claim was one too.

The wider reading is better teaching, incidentally: it makes the box a
**pointer** rather than an apology, which is the sentence the closing frame
wanted all along.

#### Every claim in the program is settled by exhaustive enumeration

Four truth-table rows; all 512 relations on a three-element set; 36
pairs on a six-element domain. Each is a **proof** rather than a demonstration,
because the domain is finite and none of it was left out \dash{} and the
program says so, in the same trapbox as $n^{2}+n+41$, which is prime for every
$n$ below 40 and composite at 40.

That contrast is the section's whole argument, so the book's own method is the
teaching example: **checking every case is a proof; checking many cases is
evidence, and the difference is not how many but whether any were left.**

`code/p14_logic_proof.py` carries a thousand confirmations of a *true* claim
three lines above the forty confirmations of the false one, asserted and
deliberately **not emitted**: the number of checks is not a measurement, it is
the rhetorical *a thousand tests* the trapbox names, and a value nothing
references is a second copy nobody would correct. F11's finding, applied on
sight; `p14.delta` went the same way, because $100 - 95$ is head arithmetic.

#### One contradiction, caught by extracting the page rather than reading the source

The trapbox printed *prime for every $n$ from $0$ to $40$, and composite at
$40$* \dash{} which cannot both be true. The Quiz's own answer said *to $40$
exclusive* and was right; the trapbox, four hundred lines away, was not, and
the two now say the same thing.

It was found by `pdftotext`-ing the finished PDF for the transcript check and
reading what came out, which is the F03 discipline finding something it was not
looking for. **Extracting a listing puts the prose around it in front of you in
a form you have not read before**, and that is worth as much as the listing
test itself.

The listing test also passed: extracted from `main-en.pdf` p693 and run from
`code/`, it prints `True`, `False`, `0`, which is what the page prints.

#### The diagram manifest, fifth recurrence, and the first time it was the KEY

A **20.5 pt** box in `main-en` \dash{} the first over the 15 pt budget since
F06 \dash{} from `p14-converse-or-contrapositive.mmd`, **34 characters against
a book whose next longest key is 28**. Six characters clear of anything that
has ever fitted, and F02's recorded fix (shorten the third argument) could not
have reached it. Renamed `p14-two-rewritings` (22).

Then a **13.8 pt** box in `main-en-a4` **alone**, from a 26-character key plus
a 35-character description. Two things worth having:

- **The manifest column constrains the key as well as the copy.** Keep a
  diagram key under about 28 characters and the manifest line \dash{} key plus
  four for `.mmd` plus the third argument \dash{} under about 48.

  > **The second half of that is falsified; see the P32 pass.** Measured with
  > a brace-matching parser, 153 of the book's 284 manifest lines are at or
  > over 48 and none of them overflows: the column is set with
  > `\@dottedtocline` and **wraps**, so an entry's total length is not what
  > overflows it. The key half stands \dash{} a long key is an unbreakable
  > `\texttt{}` run and that is what P14's own instance was. Keep the key
  > short and stop counting the copy.
- **A4 at 12pt is the binding case for that column, not the trade format.**
  Every previous instance was found in the trade build or in Polish; this one
  exists in one format and one language, and the trade build was clean.

After both fixes the multiset is element for element the pre-P14 baseline in
all four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with no stranded
openers, no stranded headings and **no orphaned cues at any point in the
pass**. Two orphan tails added, one in each A4 build.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P14.1 parts-of-a-theorem | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P14.2 two-rewritings | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P14.3 exists-is-not-found | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

**Rule 2 read by content first, captions read as nodes, then measured.** None
of the three carries an answer to a question put beside it: P14.1 states the
three parts, which the frame above delivers in full, and the question below
asks for the topological-order theorem's hypotheses, which appear nowhere in
it; P14.2 restates frame 9's own bolded sentence four frames above it, and the
question below asks what would *refute* an implication; P14.3 restates frame
18's own list of silences, and the frame after it asks nothing.

| build | fig1 / q3 / a4 | fig2 / q13 / a14 | fig3 / a18 |
|---|---|---|---|
| `main-en` | 683 / 683 / 684 | 688 / 688 / 688 | 691 / 690 |
| `main-pl` | 695 / 695 / 696 | 700 / 700 / 700 | 703 / 702 |
| `main-en-a4` | 575 / 575 / 575 | 579 / 579 / 579 | 582 / 582 |
| `main-pl-a4` | 581 / 581 / 581 | 585 / 585 / 585 | 588 / 588 |

**P14.1 sits above the elicitation that follows it in all four builds and that
is not a defect**, which is now the sixth instance of the P04/P07 case: a
figure the reader is meant to *apply* belongs above the question.

#### The open curriculum decision, settled

`notes/01-curriculum.md` §21 carried three judgement calls the review left to
the author. The third \dash{} *is P14 enough of a fix for Stroud's rigour gap,
or does the book want a later program on writing a proof?* \dash{} is now
**decided: it is enough, and no second program is wanted**, on the P12
precedent that an open question is settled in the pass that writes the program.

Two things settled it and neither was available when the question was posed.
Reading a theorem turned out to be a complete subject rather than a reduced
one, so a second program would not be finishing this one; and the position is
now **on the page in two places rather than implicit in neither**. The
introduction said only what the reader would *not* get \dash{} *you will not be
able to prove things* \dash{} and now says what they get instead. That is the
P04 precedent: the front matter prints on page one and was half-silent about
the book.

#### Also

- Traps 162 to 169 added to `notes/02`.
- **Parity clean on its first run**, fifth time (P02, P08, P09, P10, P14). The
  accumulated translator rules did it \dash{} no number spelled as a word, and
  every possessive attached to a reference built the other way round while
  drafting.
- A cross-programme gate rebuilds Program~F10's filter population from the
  truth table and asserts both of its committed counts, so the logic here and
  the measurement there cannot come apart.
- **`MAKE_EXIT 2` while the harness reported exit 0.** The recorded trap fired
  again and the recorded habit caught it: read the log's own exit line, never
  the notification.
- The issue's *No Quiz (Foundation-only)* checkbox is stale in exactly the way
  the P04 pass found the front matter stale \dash{} every written program has
  one. P14 has one; consistency with twenty-six merged programs beats a
  checkbox already known to be false.
- Frame numbers mapped after writing: sections landed at
  `1--7 / 8--14 / 15--19 / 20--25 / 26--31`.

### Program P15 pass, August 2026 --- Part V begins

**Thirty-eight teaching frames, forty printed, both editions**, against a brief
that projected fifty-five. Five sections: one input at a time, collecting them
into one object, the rate of change along any direction, steepest and across
the contour, and what that does to the walk.

**Elicitation 50%**, equal with P13 for the highest outside Part I. Designed in
rather than measured afterwards: every section opens by asking, and the three
questions a reader is most likely to get wrong \dash{} why write the partials
as a vector, does the steepest direction point at the minimum, and how far does
the walk actually travel \dash{} are all put before they are answered.

#### The payoff is a derivation, and the whole of it is one dot product

The brief asks for gradient descent's direction to be *derived rather than
asserted*, and the derivation is three lines once Program~\ref{prog:P05} is in
the room. The rate of change along a unit direction is $\nabla f \cdot u$;
P05 writes a dot product as $\lVert a\rVert\lVert b\rVert\cos\theta$; so
$D_u f = \lVert\nabla f\rVert\cos\theta$ and **the whole question of which
direction is steepest collapses into which cosine is biggest.**

The two payoffs then fall out of the same equation read at its two ends:
$\cos\theta = 1$ gives steepest ascent, and $\cos\theta = 0$ gives
perpendicular-to-the-contour. Those are not two facts about the gradient. They
are one fact read twice, and saying so is worth more than either.

#### Four assertions refuted their own drafts, in one script

The most in any pass so far, and each failure improved the measurement rather
than merely correcting it.

1. **A tolerance chosen so a check would pass.** The sweep over
   3600 directions asserted that the sampled maximum *equals*
   $\lVert\nabla f\rVert$, to $10^{-9}$, and failed by $3.2 \times 10^{-7}$. A
   maximum over a sample cannot equal a maximum over everything. What is
   asserted now is a pair \dash{} no direction beats the gradient, which is
   exact and is P05's inequality, and the sampled best falls short by no more
   than the grid spacing can account for. That turns the shortfall from an
   embarrassment into an explanation, and the frame says so. F11 paid for this
   lesson once; this is its second instance.
2. **A check that was wrong about its own geometry.** The perpendicular
   directions were tested against $90$ degrees only, so the one at $270$
   reported a gap of $180$ and looked like a defect. The mathematics was right
   and the test was not.
3. **Exact in the algebra and not to the bit, again.** On a circular bowl
   $-\nabla f$ is *exactly* parallel to the direction home, and the cross
   product says so exactly in floats. Asking `acos` reports about a millionth
   of a degree instead, because the cosine comes back as one minus a rounding
   and the arccosine of a number that close to $1$ is where P02's cancellation
   lives. **The arccosine is the wrong instrument for measuring a zero**, and
   the note box in §5 says that rather than quoting either number as the angle.
4. **The wrong ratio entirely.** \enquote{Path length over distance to the
   minimum} reported $\num{0.85}$ for a walk that is a dead straight line,
   because after twenty steps it has not arrived. That is a fact about the step
   size and not about the direction. **Path length over displacement** is $1$
   for any straight path however far it gets, which is the property the section
   is about, and it gives $\val{p15.zig.ratio}$ on the elongated bowl.

#### The measurement, on Program P10's own bowl rather than a new one

P10 committed eigenvalues $\val{p15.lam.hi}$ and $\val{p15.lam.lo}$ and a level
ellipse $\val{p10.basin.axisratio}$ times longer than wide, and said in as many
words that the shape was collected there and deliberately not spent. This is
where it is spent, so the script reads P10's committed numbers and fails the
build if they move. **A cross-programme gate is worth having when the two
programs are quoting one computation**, which is P04's rule, and this is one
bowl rather than two that resemble each other.

| | |
|---|---|
| angle between $-\nabla f$ and the way home | $\val{p15.zig.angle}$ degrees |
| crossings in $\val{p15.zig.steps}$ steps | $\val{p15.zig.crossings}$ |
| distance travelled against distance moved | $\val{p15.zig.ratio}$ |
| factor per step, steep direction | $\val{p15.fac.hi}$ |
| factor per step, shallow direction | $\val{p15.fac.lo}$ |

The mechanism is F11's own recurrence one eigendirection at a time: each
coordinate is multiplied by $1 - \eta\lambda$, so the steep one's factor is
negative and it changes side every step while the shallow one creeps. **One
step size has to serve both**, which is the sentence P20's momentum answers.

**Nothing is emitted from the F11 gate, deliberately.** F11's factor at its own
curvature has the same magnitude as this program's steep-direction factor, and
printing both would put two numbers that look like one on the page two sections
apart, which is F08's defect. The gate lives in the script; the frame names the
shared formula in words.

#### The word collides, and reading the neighbours found it

F06 uses \enquote{gradient} 68 times and F11 20 times for the **slope of a
line** \dash{} standard British usage, and right in both. Here it is a vector.
That is P07's \emph{dimension}-does-three-jobs collision in a new place, it is
invisible while drafting, and §2 carries a notation box naming it. It was found
by grepping the written programs before writing a line, which is the discipline
twelve passes have now paid for.

#### The index shrink came back, exactly as its own comment predicted

`main-pl` failed on a **5.5 pt overfull vbox**, and the recorded rule
\dash{} anchor on what TeX says it had open, never on distance from either end
\dash{} put it in `main-pl.ind` in one look rather than in five cycles. P12's
comment above that patch says the number \enquote{scales with the index and the
index only grows, so expect to raise it again}. It was right, and the raise was
half a point to nine tenths.

**The useful part is the prediction rather than the constant.** That shrink is
not a constant, it is a function of how long the index is, and the index only
grows. The comment now says so in as many words: raise it when a build says so
and do not go looking for a cleverer fix.

#### The orphaned-cue walk, two rounds

Round one cleared `main-pl` and put the cue into `main-pl-a4`; round two
cleared both. Ninth confirmation of F06's two-sided rule and it has still never
failed. Both added paragraphs earn their place: that the first factor is the
same whatever direction you pick, so the choice controls only the cosine; and
that the update is componentwise, so a framework applies it to a billion
parameters with nothing coordinated.

A 4.6 pt box in `main-pl-a4` alone came from two invented hyphen chains
\dash{} \emph{najbardziej-stromo-pod-górę} \dash{} which have no break
opportunity in them. Set as `\emph{}` phrases in both editions, and gone.

#### Rule 2 caught two figure nodes, both by reading rather than by measuring

`p15-any-direction`'s third node said \enquote{so the whole question is the
cosine}, which is one step from frame 21's answer; and
`p15-across-the-valley`'s said \enquote{so the walk crosses and crosses
again}, which is frame 34's. Both were reworded to state what the frames above
them deliver. That is P02's finding \dash{} a figure supplying the last step of
an answer is as much a spoiler as one stating it \dash{} and neither needed a
page measurement to condemn.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P15.1 hold-the-rest-still | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P15.2 any-direction | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |
| P15.3 across-the-valley | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

#### Also

- Traps 170 to 176 added to `notes/02`.
- **The orphan-tail count did not move at all**, which has now happened five
  times (F13, P07, P09, P12, P15) and every time for the same reason: the
  recorded rules were applied while drafting rather than after a build named
  the defect.
- Parity took three rounds, all recorded classes: one Polish sentence inverting
  two maths spans (\emph{stałą mnożącą $y$ jest $x^{2}$} against
  \emph{$x^{2}$ is the constant multiplying $y$}), and two summary items I had
  appended at the end of the English rather than in their natural position.
- Three emitted values went unreferenced and were cut rather than forced into
  the prose. F11's finding, applied on sight.
- Frame numbers mapped after writing: sections landed at
  `1--7 / 8--13 / 14--19 / 20--28 / 29--38`.

### Program P16 pass, August 2026

**Thirty-eight teaching frames, forty printed, both editions**, against a brief
that projected sixty-five \dash{} the largest estimate left in the manifest.
Five sections: what shape a derivative has, the chain rule multiplies them and
nobody forms one, which end and why the shape decides, what it has to keep, and
three times it answers a different question.

#### The whole argument was already measured, one program early

P06 bracketed one triple product two ways for identical answers and a factor of
$\val{p06.cost.ratio}$ in cost. **That is forward mode against reverse mode**,
measured before either had a name, and P16's job was to notice it rather than
to derive it again. The ratio here is gated against P06's committed values.

So the decision procedure comes out as two integers and nothing else: forward
costs one pass per input, reverse one per output. A scalar loss with many
parameters makes reverse cheaper by **a factor of the parameter count**, and
nothing about deep learning enters the argument at any point.

Measured exactly over the rationals: $\val{p16.fwd.muls}$ multiplications
forward against $\val{p16.rev.muls}$ reverse for a gradient asserted
*identical*, with the ratio swept over four widths and equal to the input count
every time. The single figure would have been a fact about one stack.

#### The arithmetic P03 named and left

P03 says checkpointing trades operations for bytes and stops. Here it is: keep
every $k$th activation and you hold $\frac{L}{k} + k$ at once, whose derivative
vanishes at $k = \sqrt{L}$. **The $\sqrt{L}$ everyone quotes is a stationary
point, not a rule of thumb** \dash{} F11's own machinery used on a cost rather
than on a loss. At $\val{p16.ckpt.layers}$ layers that is
$\val{p16.ckpt.peak}$ held instead of $\val{p16.ckpt.layers}$, a factor of
$\val{p16.ckpt.saving}$, for exactly $\val{p16.ckpt.passes}$ forward passes.

#### The extract-and-run test caught a defect nothing else could

The transcript printed $-0.4$ for a gradient whose own listing produces
$\val{p16.inplace.used}$. The script had computed the in-place demonstration on
one example and written the listing from another, so **the values in the frames
and the numbers in the listing described two different computations.**

`make verify` cannot see this: the script wrote exactly what it computed, so
the transcript and its generator agree perfectly. What it does not check is
whether the listing's own code produces the numbers the *frames* quote. The
only instrument that catches it is F03's \dash{} extract the listing from the
finished PDF and run what comes out \dash{} and it did, on the first try.

**So a generated, committed, drift-gated transcript can still disagree with the
prose beside it**, which is one step beyond P04's finding that such a
transcript can be un-runnable. The fix was to make the demonstration and the
listing one computation, which is the only arrangement in which they cannot
come apart.

#### Rule 2 caught three figure nodes, all by reading

`p16-jacobian-shape`'s third node answered the frame two later that asks it;
and **both** of `p16-two-brackets`'s later nodes gave the pass counts that the
frame after them elicits \dash{} and that figure lands a page *before* the
question in three of the four builds. All three were reworded to state what the
frames above them deliver.

That is the second pass running in which reading the figures against their
neighbouring frames caught more than measuring them did. **Read the nodes as
prose first; the page positions only settle where a genuine answer landed.**

#### The contents is the book's third narrow column

`main-pl` failed on a **2.2 pt overfull hbox in the table of contents**: the
Polish title is fifty-six characters and the contents line is narrow.
`preamble.tex`'s note on `\mfaheadmark` already said this class was \enquote{latent
today only because no long-titled program is written}. One now is.

The fix is LaTeX's own `\chapter[short]{long}`, passed through a new optional
argument on `\program`, rather than anything invented \dash{} and it discharges
the same latent defect for the running head that note names. **Use it in both
editions or in neither**: parity compares structural tokens, so a short title in
one file and not the other diverges.

#### The index shrink, twice in two programs

P15 raised it from half a point to nine tenths and wrote down that the number is
a function of index length rather than a constant. P16's entries took the Polish
index past that too \dash{} $18.8$ pt and $3.4$ pt \dash{} and it went to
$1.5$ pt. Two raises in two programs is the prediction being right twice; the
comment above the patch is the thing to read before reaching for a cleverer fix.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P16.1 jacobian-shape | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P16.2 two-brackets | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |
| P16.3 keep-or-recompute | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |

#### Also

- Traps 177 to 184 added to `notes/02`.
- **No framework is named anywhere in the program**, on F04's rule that a
  library's internals are a fact about a version. What carries the three silent
  failures instead is a reverse-mode differentiator of about forty lines written
  for the program, which exhibits all three rather than asserting them \dash{}
  and which is itself checked against a central difference, at the step F11
  measured, to better than $\val{p16.check.bound}$.
- A bare `\log` in a further-problem answer fired C10 four times. The resolution
  is P03's: the base is provably immaterial *inside* an $O$, so the claim is
  written $O(\mfalogplain L)$ rather than given a base it does not need.
- Elicitation 47%. One orphan tail added, in `main-en`; no orphaned cues and no
  stranded openers or headings at any point in the pass.
- Frame numbers mapped after writing: sections landed at
  `1--8 / 9--15 / 16--22 / 23--29 / 30--38`.

### Program P17 pass, August 2026

**Thirty-eight teaching frames, forty printed, both editions**, against a brief
that projected fifty. Five sections: the best local model, the matrix of second
derivatives, why the step size has a ceiling, using the curvature and what it
costs, and sharp and flat honestly.

Eleventh program under its brief's estimate, and the cause is the P10/P13 kind
rather than the F07/P06 one: nothing had spent the material, and the neighbours
supplied the *machinery* instead. **P15 put the reader one line from the
payoff** and its own rigour box said so \dash{} *this program can say that the
factor goes negative and that the walk crosses; it may not tell you where the
boundary is.* **P10** built the bowl and said the inequality was P17's.
**F04** owns the geometric sequence the derivation actually is. **P16** priced
a Jacobian, so a Hessian is one dimension worse and the count is gated against
P16's own parameter figure. What was genuinely left is the second-order model
and the inequality, and both are short once you already have the pieces.

#### The payoff is a debt another program recorded, and it is paid with a gate

$\lvert 1 - \eta\lambda\rvert < 1$, so $\eta < 2/\lambda$, so with several
directions $\eta < 2/\lambda_{\max}$: **a statement about a geometric sequence
with nothing about networks, losses or training in it.** That turns *the
learning rate was too high* from a judgement into an inequality whose right-hand
side is a property of the surface rather than of the optimiser.

Derived, and then **measured**: the script sweeps $\eta$ and finds the value at
which the walk first stops converging, at $\num{0.1000}$ against a derived
$\num{0.10}$. And it reads P15's committed $\eta = \num{0.09}$ out of
`figures/values/p15.tex` and asserts it lies strictly under the boundary, so
two programs describing one walk cannot come apart about it.

**One gate is asserted and deliberately not emitted.** F11's factor at its own
curvature has the same magnitude as this program's steep-direction factor, and
printing both would put two numbers that look like one on the page two sections
apart, which is F08's defect. The gate lives in the script and the frame names
the shared formula in words.

#### The issue named a trap the draft did not carry, and the fix raised the rate

Issue \#31's *Done when* list names one trap in the reader's own voice \dash{}
*my loss surface has local minima, and that is what training gets stuck in*
\dash{} and the draft carried the counting argument as an `aibox` that
**stated** it. Two of this book's rules point the same way: a trap frame must
*elicit* the error rather than warn against it, and a box that cannot name a
specific line of a specific system is prose. So the aibox became a question
(*what has to be true of $\val{p17.params}$ eigenvalue signs for the point to be
a minimum, and in how many ways can that be missed by a single sign?*) and a
trapbox. It cost one frame, took the elicitation rate from 47% to **50%**, and
shifted every payload from frame 15 onward by one.

**The rule: read the issue's own checklist before the frame remap, not after.**
The trap it names is a contract exactly like the diagram count, it was the only
one of nine items the draft had missed, and finding it after the renumber would
have meant doing the renumber twice.

#### Rule 2 caught two figures, and there is a pattern in where it bit

Both were the **third node of a three-rank figure** stating the next frame's
answer. `p17-three-models` ended on *an order better, not a size*, which is
frame 4's answer, in a figure declared in frame 2. `p17-why-the-step-caps` ended
on *the steepest direction sets the cap for all of them*, which is frame 19's,
in a figure declared in frame 17.

That is worth naming as a shape rather than as two incidents: **three ranks is
the sweet spot for width and the third rank is where the spoiler lives**,
because a three-node chain naturally ends on the conclusion and the conclusion
is usually what the next frame elicits. Both were reworded to state what the
frames above them deliver. `three-models`'s caption had to change with its node
\dash{} P11's *read the caption as a node*, second instance.

Measured afterwards in all four builds, and the result is the P04/P07 case
again: `p17-why-the-step-caps` sits **above** frame 18's question in all four
and is not a defect, because the question is *which of several directions
decides* and the figure never mentions more than one. Answer, figure, question:
`main-en` 756 y578 / 757 y169 / 757 y293; `main-en-a4` 635 y561 / 635 y719 /
636 y160; `main-pl` 769 y141 / y308 / y434; `main-pl-a4` 643 y623 / 644 y159 /
644 y280. `p17-sharp-is-not-a-fact` is below its answer in all four.

#### A wrong exponent that two coincidences were hiding

The draft asserted the error orders as *the linear error divides by about
$\val{p17.order.lin}^{2}$ each time*. The committed value **is the exponent**,
so the expression should be $2^{\val{p17.order.lin}}$ \dash{} and both forms
evaluate to $4$, so the page was right and the formula was not. It would have
gone wrong silently the day an order changed. Both halves are now written
$2^{\val{}}$, which is symmetric and is what the script asserts.

**A `\val{}` used as a base where it is an exponent is invisible when the two
readings agree numerically.** Read a formula containing a `\val{}` as the script
computes it, not as it prints.

#### The index shrink came back a third time, and the last page is why

CI's recorded lesson \dash{} anchor on what TeX says it had open, never on
distance from either end \dash{} put $\num{10.8}$ pt and $\num{4.8}$ pt inside
`main-pl.ind` in one look. The `theindex` `\parskip` shrink went $\num{1.5}$ to
$\num{2.5}$ pt and all four builds came back clean, which is the third raise in
three programs and exactly what the comment above the patch predicts.

**What is new is which page.** Both complaints were on the index's **last**
page, and that is the page where the shrink has to do the work: an interior
column that will not fit pushes an entry to the next page, and the final one has
nowhere to push. `\raggedbottom` then makes it reliably the *fullest* of the
four, because every page before it is allowed to end short. Recorded beside the
constant.

Also worth not repeating: `checklog.py` reports the location as *PDF page N*
and the number it prints is TeX's own `\thepage`, which in this book is the
**printed** folio and lands some twenty sheets earlier in the file. Chasing PDF
page 884 found the answers appendix; printed page 884 is the index.

#### Two emitted values cut, and one of them is a class

`p17.taylor.x0` is a parameter of a demonstration the page never quotes.
`p17.rescale.outputs.same` was the integer $1$, standing for *the outputs
agreed* \dash{} which is **a gate, not a quantity**, and a gate belongs in the
script's assertion rather than in the value ledger. F11's finding with a name
attached.

The symmetry check went the other way for the same reason: the two mixed
partials agree to *exactly zero* here, which is luck of this function, so the
committed number is a ceiling of $\num{1e-06}$ rather than the measurement.
P06's rule, applied before CI could apply it.

#### The transcript, extracted from the page and run

Printed listing, extracted from `main-en.pdf` p758 and executed from `code/`:
it prints `(0.1, 2.0)` and `1469.7715679690943`, which are
`\val{p17.eta.star}`, `\val{p17.eta.shallow}` and the figure the frame points
at. That is the P16 test as well as the F03 one \dash{} the listing runs *and*
it agrees with the prose beside it.

#### Also

- Traps 185 to 192 added to `notes/02`, including the one the issue names.
- **A new parity class, and it reads as a style choice: the English's own
  abbreviation is part of the token stream.** Where English writes a bare
  \enquote{P15} rather than `Program~\ref{}`, the Polish must too, because C4
  and C14 both count references. Two of the pass's five parity failures were
  that; the other three were the recorded classes \dash{} a reference behind
  its maths, a reference behind its noun, and a summary item inverting
  `\val{p17.steps.99}` and $99$. Noted in the Polish file's own header.
- Layout cost nothing: the overfull multiset is element for element the
  pre-P17 baseline in all four builds, no stranded openers, no stranded
  headings, **no orphaned cues at any point in the pass**, and **the orphan-tail
  count did not move** \dash{} the sixth time (F13, P07, P09, P12, P15, P17).
- Three diagrams, all six renders at mermaid's wrap cap of $657$ pt on the
  first attempt, at three ranks.
- Frame numbers mapped after writing and then again after the trap frame:
  sections landed at `1--8 / 9--15 / 16--23 / 24--30 / 31--38`.

### Program P18 pass, August 2026

**Thirty-nine teaching frames, forty-one printed, both editions**, against a
brief that projected sixty. Five sections: the layout convention,
differentiating by a matrix, the $\softmax$ Jacobian, cross-entropy and the
gradient everybody uses, and why the two are fused.

Twelfth program under its brief's estimate, and the cause is the P10/P13 kind:
the neighbours supplied the machinery. **P16** owns the shape rule, the
finite-difference method and \enquote{nobody forms a Jacobian}; **F07** owns
$\softmax$ and the two-score identity; **P06** owns the matrix as a function;
**P15** and **P17** own both derivative objects. What was genuinely left is a
\emph{layout} and five identities, and this program defines no new object at
all.

#### The headline has two reasons and they are different in kind

$\vect{p} - \vect{y}$ against the honest two-step route:

- **Cost.** $\val{p18.fuse.ratio}$ times fewer operations at a vocabulary of
  $\val{p18.vocab}$, and the Jacobian nobody forms would be
  $\val{p18.fuse.gib}$ GiB.
- **Definedness.** The two-step route forms $-1/p_c$, and once a logit falls
  about $\val{p18.cliff}$ below the largest, $p_c$ underflows to exactly zero
  and it divides by zero. $\vect{p} - \vect{y}$ never forms the reciprocal and
  returns an ordinary $(\num{0.5}, \num{0.5}, -\num{1.0})$.

**Separating them is worth more than either**, because the cost argument alone
leaves \enquote{keep the clear route and pay for it} open, and the second
closes it: the two are not the same function, and the rows where they differ
are the rows a run meets early, when the model is worst. That is
Program~\ref{prog:P01}'s floor and Program~\ref{prog:P02}'s sense of
\enquote{numerically stable} arriving in the field's most reused derivation.

#### An assertion refused a threshold chosen to make it pass

The layer-norm gradient agrees with a central difference to $\num{1.7e-08}$
and the draft asserted $10^{-8}$. That is a threshold picked so a check would
pass rather than derived, which is the failure mode Program~\ref{prog:F11}
paid for and Program~\ref{prog:P15} paid for again. The ceiling is now the
method's \dash{} one shared $\val{p18.check.ceiling}$ across all five
identities, an order above every measured gap and orders below any real error,
because a dropped term disagrees by something of order one rather than by a
decimal place \dash{} with the per-identity bounds committed separately.

#### Appendix B is wrong about the book, in four of its five pointers

It says numerator layout is \enquote{declared in Program~P17}. P17 is the
Hessian program and declares nothing of the sort: it is the P7-insertion
off-by-one surviving in the appendix, and it is **this program's own
declaration misattributed**. Corrected in both editions, and section 1 is the
declaration the appendix names, so the pointer now closes rather than merely
renumbering.

**That is the fourth file to carry that off-by-one**, after the trap
catalogue, the manifest and the curriculum notes. And checking the one pointer
found three more false claims in the same appendix, none of them this
program's and none of them the off-by-one:

- `Program~P23` for the $D^{2}(X)$ notation box. P23 is *Probability and
  Bayes*; **P24** is *Random variables and distributions*, whose brief names
  variance in its first sentence. Correcting it needs a clause in P24's brief,
  which is the F04-to-P20 remedy.
- \enquote{Program~F6 says so at the first interval a reader meets}: the first
  interval in the book is F03's, and **F06 carries no notation box at all**.
- \enquote{Program~F8 records that where the function appears}, of *tgh*: F08
  mentions $\tanh$ once in passing and records nothing, and F07, which owns
  $\tanh$, records nothing either.

**Recorded rather than fixed**, on the P07-covariance precedent: each needs a
merged-program edit or a manifest clause, and doing that inside a pass about
something else is how a measurement stops being trusted. The generalisable
part is the finding itself: **Appendix B has never been audited against the
programs it names, and it is five greps.**

#### Rule 2, and one figure carried two answers at once

`p18-one-transpose` gave frame 4's \enquote{$W$ itself} in its **middle** node
and frame 6's \enquote{one transpose} in its last, **and its manifest copy
gave the second one again}. `p18-two-routes`'s last node reached one step past
frame 33 towards frame 35's answer. Both reworked to state what the frames
above them deliver.

So Program~\ref{prog:P17}'s finding generalises rather than being about the
third node: the spoiler is anywhere the chain reaches past the frame it sits
in, and **the manifest copy is a fourth place to read, after the node and the
caption**. Measured afterwards in all four builds: all three figures sit after
the frame that delivers what they carry, and the two that sit above a
following question do not answer it, which is the P04/P07 case for the seventh
time.

#### Two gates were right and the emissions were the defect

- **C10 fired on `log-softmax`**, written $\log$-$\softmax$. That is a
  \emph{name} rather than a logarithm whose base is in question, so it goes in
  `\code{}` \dash{} Program~\ref{prog:P01}'s `-inf` and P12's `0.0`
  resolution, not Program~\ref{prog:P03}'s notation box.
- **C7 reported two shape values as unproduced**, because they were text and
  the ledger scans for `\mfaval`. The right fix is F10's and P03's: a shape is
  arithmetic the reader does from two counts already on the page, so the page
  builds $\val{p18.n.out} \times \val{p18.n.in}$ from what is there and the
  emission was the defect.

#### Layout

A **24.7 pt** hbox in `main-en`, from four unbreakable maths spans run into
one sentence \dash{} the score derivative, the summation index and a product
of two partials, with almost no break opportunity anywhere in it. That is
Program~\ref{prog:F06}'s rule applied after the build named the box rather
than while drafting, and the recorded fix worked without a detour: **put it in
a display.** The frame reads better for it.

**The index shrink came back a fourth time in four programs**, $\num{2.5}$ to
$\num{3.5}$ pt, and four data points are enough to see the shape: $\num{0.5}$,
$\num{0.9}$, $\num{1.5}$, $\num{2.5}$, $\num{3.5}$. The requirement grows with
the index, the index grows with the programs, and twenty-nine programs remain.
Extrapolated it reaches ten points or so by the end of the book, and ten points
of shrink between two index lines is no longer invisible. **So the recorded
advice has a horizon**, and that is now written beside the constant: somewhere
before Part IX this needs a structural answer instead of another raise.

After both, the multiset is element for element the pre-P18 baseline in all
four builds, with no stranded openers, no stranded headings and **no orphaned
cues at any point in the pass**. One orphan tail added, in `main-en`.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P18.1 one-transpose | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P18.2 shape-is-the-check | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P18.3 two-routes | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

#### Also

- Traps 193 to 200 added to `notes/02`, including the one the issue names.
- **The declared forward reference is discharged as declared**: cross-entropy
  gets a definitional frame in section 4 and the Learning outcomes say so,
  with the justification handed to Program~\ref{prog:P26} and the meaning to
  Program~\ref{prog:P30}. The review found this as an undeclared dependency
  once; it has not reverted.
- **Parity came back clean on its ordered checks first time** \dash{} the two
  failures were C10 and C7, which are not word-order divergences. That is the
  sixth program with no C4, C8 or C12 round.
- The listing was extracted from `main-en.pdf` p783 and executed from `code/`:
  it prints `0.0`, `[0.5, 0.5, -1.0]` and the `ZeroDivisionError`, which is
  what the page prints and what the frames beside it claim.
- Frame numbers mapped after writing: sections landed at
  `1--7 / 8--14 / 15--21 / 22--31 / 32--39`.

### Program P19 pass, August 2026 --- Part VI begins

**Thirty-eight teaching frames, forty printed, both editions**, against a brief
that projected forty-five. Six sections: a definition you can check, what
convexity promises, Jensen's inequality, why you cannot average perplexities,
the same inequality once more, and when the promise is broken.

Thirteenth program under its brief's estimate, and this one is the F07/P06 kind
in its purest form: **Program~\ref{prog:F04} had already worked the headline
demonstration in full** \dash{} the two ways of averaging a perplexity, with
both numbers computed \dash{} and hands the general statement here by name. So
what P19 owes is not the demonstration but **the inequality that says the
demonstration could not have come out the other way**, and the difference makes
the section better rather than shorter.

#### The headline is the size of the error, and it is a property of the corpus

The ratio of the wrong average to the right one is $\exp(\Var/2)$, so it is
governed by the **spread** of the per-token losses and by nothing else. Measured
over $\val{p19.ppl.tokens}$ tokens at a mean loss of $\val{p19.ppl.meanloss}$:

| spread | correct | averaged wrongly | ratio |
|---|---|---|---|
| $0$ | $\val{p19.ppl.right.00}$ | $\val{p19.ppl.wrong.00}$ | $\val{p19.ppl.ratio.00}$ |
| $\num{0.5}$ | $\val{p19.ppl.right.05}$ | $\val{p19.ppl.wrong.05}$ | $\val{p19.ppl.ratio.05}$ |
| $1$ | $\val{p19.ppl.right.10}$ | $\val{p19.ppl.wrong.10}$ | $\val{p19.ppl.ratio.10}$ |
| $2$ | $\val{p19.ppl.right.20}$ | $\val{p19.ppl.wrong.20}$ | $\val{p19.ppl.ratio.20}$ |

**The correct number does not move at all across that table**, which is what
makes the failure mode worth a section: a harness with the bug agrees to four
figures on a homogeneous fixture and is wrong by a factor of
$\val{p19.ppl.ratio.20}$ on a diverse corpus. That is
Program~\ref{prog:P02}'s sense of \enquote{numerically stable} \dash{} safe for
inputs you have not tried \dash{} arriving in published evaluation code rather
than in a library, and the test suite that would have caught it is the one
nobody writes.

The prediction is asserted rather than the four figures: the measured ratio must
track $\exp(\Var/2)$, at every spread, so a change of seed or of token count
cannot quietly falsify the section.

#### The index shrink was not a dial, and the sweep that showed it was wrong too

Both halves belong here, because the second is this repository's own recurring
defect and it was committed before it was caught.

P15, P16, P17 and P18 each raised `theindex`'s `\parskip` shrink by a step
\dash{} $\num{0.5}$, $\num{0.9}$, $\num{1.5}$, $\num{2.5}$, $\num{3.5}$ \dash{}
and the note above the patch drew the obvious line through those five points:
the requirement grows with the index, the index only grows, **so raise it when
a build says so and do not look for a cleverer fix.** The P18 note in this file
extrapolated that to ten points by the end of the book.

P19's index overflowed at $\num{3.5}$, the number was raised, and a sweep
reported that $2$ and $6$ both failed builds that $\num{4.5}$ cleared \dash{}
so the advice was retired and replaced with *sweep against all four builds*.
**That sweep was taken while the program was still being written, and it was
quoted here as though it described the shipped tree.** Re-measured against the
finished one, every value from $3$ to $\num{5.5}$ clears all four and the
cliff is at $6$:

| shrink | `main-en` | `main-pl` | `main-en-a4` | `main-pl-a4` |
|---|---|---|---|---|
| $3$ to $\num{5.5}$ | clean | clean | clean | clean |
| $6$ | \dash{} | \dash{} | clean | $\num{26.3}$ pt |
| $7$ | \dash{} | \dash{} | clean | $\num{26.3}$ pt, twice |
| $10$ | \dash{} | \dash{} | \dash{} | $\num{616.8} + \num{90.8}$ pt |

Ten points is catastrophic rather than merely insufficient: more shrink lets
TeX believe it can cram another column's worth onto a page, and it then
overflows by a whole column. So the conclusion survives \dash{} the constant
**reshuffles breaks, non-monotonically**, exactly as `preamble.tex` already
records for the `\begin{fr}` reservation \dash{} and the table that carried it
did not.

**The generalisable half is the one this file already states about page counts
and the overfull multiset, and it applies to every pagination measurement:
re-measure from the build in front of you.** A sweep over a layout constant is
a pagination measurement, so it does not survive a change to the material
being paginated, and a sweep taken mid-pass describes a tree that no longer
exists. Both instances of the wrong table are corrected rather than deleted,
because the correction is the finding.

#### And then CI disagreed about where the window is

At $\num{4.5}$ \dash{} clean in all four builds here \dash{} **CI failed
`en (a4)` on an $\num{18.29}$ pt overfull vbox in the index.** That is the
recorded two-installations divergence at its worst point: CI sets the same
entries in three pages where this container needs four, so its columns are
fuller and demand more shrink than any local sweep will ever ask for.

So the rule gains its second half. A sweep on one machine cannot choose a
value for the other, and **CI is the second measurement rather than a
formality**. When a value clears here and fails there, move within the locally
clean range *towards* more shrink \dash{} the complaint is that a column could
not be compressed enough \dash{} and stop short of the cliff. The value is
$\num{5.5}$, which is the top of the locally clean range and a full point
below the first local failure.

**The raise worked, partly, and that settled the mechanism.** At $\num{5.5}$
CI's box went from $\num{18.29}$ pt to $\num{9.29}$ pt \dash{} exactly nine
points for one more point of shrink per entry \dash{} so the shrink does reach
it and the direction was right. What it also showed is that **no single value
can serve both machines**: CI wants more than $\num{5.5}$ and this container's
`main-pl-a4` breaks at $6$, by $\num{26.3}$ pt.

**So the remedy is a second source of shrink, and the point of it is that it
does not scale with the page's contents.** A column holds some forty-five
entries, so one more point on each is forty-five points of extra capacity and
TeX packs more \dash{} which is exactly why the constant is non-monotonic.
`\indexspace` appears three or four times a page whatever the entries are, so
six more points of shrink on each is about twenty points, bounded, and it
absorbs a residual without changing how much TeX is willing to cram.

That is the generalisable half: **there is a difference between giving a page
slack and giving it appetite**, and a knob that scales with the content gives
both. When a rigid region needs a few points, find a source of shrink whose
total is fixed.

**And one process error, recorded because it will happen again.** The raise to
$\num{5.5}$ was made, and a background sweep script still running in the tree
restored $\num{4.5}$ on its way out, so the commit carried the old value and
CI reported $\num{18.28874}$ pt a second time \dash{} to the ten-thousandth of
a point. This file already records that an identical measurement after a change
is the signal that the change did not reach what was measured; the CI vbox
chased into the answers appendix is the same shape. Here it was simpler still:
the change had not reached the *file*. **Re-read a constant out of the file
immediately before committing it**, and do not leave a script that rewrites the
working tree running behind you.

#### The transcript was about to be a fabricated console block

The listing prints two pairs of perplexities, and the draft's file carried
`(12.18, 12.18)` where the functions return `12.182493960703473`. The file was
generated by `code/`, committed and inside `make verify`'s drift gate \dash{}
and it was **still a fabrication**, because the rounding had been applied to the
script's *output* rather than written into the listing's own code, so the page
showed Python printing something Python does not print.

Fixed by putting `round(..., 2)` inside the listing, which is the only
arrangement in which the printed line and the printed result cannot come apart,
and verified by extraction: pulled out of `main-en.pdf` p801, run from `code/`,
and it prints `(12.18, 12.18)` and `(12.18, 46.47)`.

That is one step beyond P04's finding that a generated transcript can be
un-runnable and P16's that it can disagree with the prose beside it. **A
transcript is a claim about what a session prints, so every transformation
applied to a value has to be visible in the listing.**

#### An accidental quadratic, found by the script timing out

`make numbers` hit the two-minute mark on a script that does no heavy
arithmetic. The variance of the per-token losses was written as a generator over
$\val{p19.ppl.tokens}$ elements with `sum(losses) / len(losses)` **inside** it,
so the mean was recomputed two hundred thousand times per spread. Hoisting it to
a local took the whole script to $\num{1.07}$ s.

Worth recording because of what it nearly cost rather than what it was: the
obvious remedy for a slow measurement is to shrink the sample, and shrinking it
would have made the Jensen gap noisier and the section weaker for a defect that
had nothing to do with the sample size.

#### Rule 2 caught two figures, both in the third node again

`p19-chord-above`'s node C said the test is arithmetic rather than a picture and
works in any dimension, which is frame 4's answer; `p19-one-basin`'s said where
you end up depends on where the walk began, which is frame 12's. Both were
reworded to state what the frames above them deliver, re-rendered and rebuilt.

That is now three passes running (P17, P18, P19) in which the spoiler was the
**last node of a three-rank figure**, and the reason is structural rather than
accidental: a three-node chain naturally ends on its conclusion, and the
conclusion is usually what the next frame elicits. **Read the last node against
the next frame before rendering anything.**

Measured afterwards in all four builds, and the result is the P04/P07 case for
the eighth time: `p19-chord-above` sits above frame 3's question in `main-en`
(answer p792 y516, figure p793 y130, question p793 y218, answer p793 y297) and
answers nothing in it, with question, figure and answer on one page. The other
two sit below the frame that delivers what they carry.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P19.1 chord-above | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P19.2 one-basin | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P19.3 order-of-two | 657 / 657 | 5.18 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

#### What the program refuses to say

The brief asks for the honest statement that non-convex does not mean hopeless,
and §6 gives it as a measurement rather than as reassurance: on the wiggle
function the curvature is negative at $\val{p19.curv.negative}$ of
$\val{p19.curv.tested}$ sampled points and the two basins end
$\val{p19.wiggle.gap}$ apart, so a walk's answer depends on where it started
\dash{} and the book says in as many words that it has **not** measured whether
that matters at the scale people train at, because it would need a real model.
That is Program~\ref{prog:P08}'s and Program~\ref{prog:P11}'s treatment of rank
collapse, applied to the claim everybody repeats about loss landscapes.

#### Also

- Traps 201 to 208 added to `notes/02`.
- **A cross-programme gate on F04's two perplexities**: this program's
  inequality must order them the way F04's committed values already do, so the
  demonstration there and the theorem here cannot come apart.
- Elicitation 47%. Two parity rounds, both recorded classes: a dropped `$f$`
  span where the Polish attached the adjective to the noun instead
  (`Dla funkcji \textbf{wklęsłej}` against `Dla \textbf{wklęsłej} $f$`), and the
  `<maths> z Programu~\ref{...}` inversion.
- Layout cost nothing: the overfull multiset is element for element the pre-P19
  baseline in all four builds, no stranded openers, no stranded headings, **no
  orphaned cues at any point in the pass**, and **the orphan-tail count did not
  move** \dash{} the seventh time (F13, P07, P09, P12, P15, P17, P19).
- Frame numbers mapped after writing: sections landed at
  `1--8 / 9--14 / 15--18 / 19--26 / 27--30 / 31--38`.

### Program P20 pass, August 2026

**Forty-two teaching frames, forty-four printed, both editions**, against a
brief that projected sixty-five \dash{} the largest estimate that was left in
the manifest. Seven sections: one update and what has to be estimated,
averaging the direction, the convention that changes the step, scaling each
coordinate, correcting an average that starts at zero, where the penalty
enters, and what a schedule does to the step.

Fourteenth program under its brief's estimate, and the reason is the F07/P06
kind at its strongest: **four written programs had each already delivered one
of P20's ingredients**, so nothing here had to be derived from scratch.
Program~\ref{prog:F04} owns the exponential moving average outright, including
the bias correction and the $(1-\beta)$ convention, and says in as many words
that P20 supplies the gradient and not the average. Program~\ref{prog:P15}
owns the zig-zag and hands the fix here by name. Program~\ref{prog:P17} owns
$\eta < 2/\lambda_{\max}$, the bowl's optimal step size, its rate and its step
count \dash{} all gated rather than recomputed \dash{} **and, unexpectedly,
the argument that turns out to be the sharpest thing this program can say
about Adam**. Program~\ref{prog:P11} owns the condition number.

So the shape of the program is not \emph{what does Adam do} but \emph{what was
wrong with the thing before it}, which is what its own brief asks for and what
the reading made possible.

#### Experiment E6, and the asymmetry that made it worth running

The issue names E6 by name: SGD, momentum and Adam on a quadratic of known
condition number, iterations to tolerance against the predicted count. It is
free, and it makes Program~\ref{prog:P11}'s condition number pay off as a
prediction rather than as a definition.

The result is better than a table of three numbers, because **the two
predictions do not behave alike**:

| | plain descent | momentum |
|---|---|---|
| rate | $(\kappa-1)/(\kappa+1)$ | $(\sqrt{\kappa}-1)/(\sqrt{\kappa}+1)$ |
| predicted count at $\kappa = 20$ | $\val{p20.pred.sgd}$ | $\val{p20.pred.mom}$ |
| measured | $\val{p20.steps.sgd}$ | $\val{p20.steps.mom}$ |
| across six $\kappa$ from $4$ to $1000$ | **exact every time** | a floor it approaches |

**Plain descent's prediction is exact at every condition number tried**, and
momentum's is not, and the second half is the section. The draft asserted the
two would agree within two steps and it failed at $17$ against $11$ \dash{}
the eleventh pass running in which writing the assertion at the computation,
before the prose it supports, caught something.

Two reasons, and both are checkable rather than excuses. A rate describes the
tail and not the start, and this walk **overshoots**: the distance rises to
$\val{p20.overshoot}$ times its starting value before it falls. And at the
optimal coefficients the two roots of the iteration coincide in both
eigendirections at once \dash{} the discriminant is exactly $0$, which the
script checks \dash{} so the decay carries a factor of $k$ and the rate is
approached from above rather than attained. Measured over fifty steps of the
tail the ratio is $\val{p20.tail.rate}$ against a predicted
$\val{p20.rate.mom}$.

The sentence worth keeping: **a rate is a limit and a step count is not**, and
quoting one as the other is how $\sqrt{\kappa}$ becomes folklore. The measured
advantage is $\val{p20.sweep.ratio.hi}$ at $\kappa = \val{p20.sweep.k.hi}$
against a $\sqrt{\kappa}$ of $\val{p20.sweep.sqrt.hi}$ \dash{} less than half
of it.

#### Three more assertions refuted their own drafts, all in the same script

Unusually many for one pass, and each replacement is a better frame than the
claim it replaced.

- **A threshold chosen so a claim would pass.** The $(1-\beta)$ demonstration
  asserted that carrying a step size across the convention \enquote{takes more
  than three times as long}. False at Polyak's $\beta$, where the factor is
  only $\num{1.67}$. Rewritten at Program~\ref{prog:F04}'s own $\beta =
  \num{0.9}$, where the factor is ten and the claim needs no tolerance at all:
  rescaling reproduces a $\val{p20.conv.same}$-step walk **exactly**, and not
  rescaling **diverges**. Not slower \dash{} gone.
- **Adam's step is not $\eta$.** The unit-step check asserted $\eta$ to
  $10^{-6}$ for every gradient and failed at $\lvert g\rvert = 10^{-6}$, where
  the step is $\num{0.09967}$. The failure is the frame: the first step is
  exactly $\eta/(1 + \varepsilon/\lvert g\rvert)$, so **the epsilon is where
  the unit-step property stops**, and it is an identity rather than an
  approximation.
- **And that identity produced the epsilon section.** A draft asserted the
  outside form was scale-free to $10^{-9}$; it is short by
  $\varepsilon/\lvert g\rvert$. Measuring both shortfalls instead of asserting
  one away gives the argument: at $\lvert g\rvert = \val{p20.eps.g}$ the
  epsilon costs $\val{p20.eps.short.out}$ per cent of the step outside the
  root and $\val{p20.eps.short.in}$ per cent inside it. A later draft then
  asserted the *ratio* grows as the gradient falls, which is also false \dash{}
  the inside shortfall saturates below $100$ per cent while the outside one
  keeps climbing, so the ratio peaks. The ratio was never the claim.

#### CI rejected a value on a rounding boundary, and `bound()` itself was unsafe

`p20.cos.area` printed $\num{0.501}$ here and $\num{0.500}$ on CI, and the
recompute job caught it. The two schedules' budgets were averaged over
$t = 0 \ldots \text{TOTAL}-1$, which misses the last point and puts the answer
at $\num{0.5005}$ \dash{} **exactly on a rounding boundary at three decimals**,
so the printed form depends on the last bit, and `libm`'s cosine is not
bit-identical across platforms.

That is Program~\ref{prog:P06}'s residual defect in a new place: an
*observation* committed where an *invariant* was meant. The invariant is that
both schedules spend half the peak, exactly, by symmetry about the midpoint.
The sum is now a trapezoid with its endpoints halved, the assertion is a
ceiling both machines clear, and **the page prints the exact value the
symmetry gives rather than the sum's**.

**And the same pass found that `bound()` has the defect built in.** The helper
this book uses to commit a residual returns the *tightest* power of ten above
it \dash{} which is itself a property of the machine when the residual can be
exactly zero, because one machine measures $0$ and another $10^{-16}$. It now
takes the ceiling as an argument and merely checks it, so what is committed is
a decision rather than an observation. The other scripts' copies are untouched:
their residuals are genuine and nowhere near zero, and sweeping them is the
pass this file already lists.

#### And one measurement that was arithmetic dressed as a measurement

The weight-decay section first \enquote{measured} the effective strength by
computing $\lambda/(\lambda/100)$ and reporting $100$. That cannot fail, which
is Program~\ref{prog:P05}'s rule about finding nothing, and it was caught by
reading the script rather than by any gate.

It is now an equilibrium: two coordinates differing only in curvature, by a
factor of $\val{p20.wd.curvratio}$, run to where the penalty balances the data
gradient. Under $L_2$ they settle at $\val{p20.wd.l2.steep}$ and
$\val{p20.wd.l2.flat}$ \dash{} the same $\lambda$ pulling
$\val{p20.wd.l2.spread}$ times harder on the coordinate with the *smaller*
gradient \dash{} and under decoupled decay both settle in the same place, to
better than $\val{p20.wd.gap}$. The $L_2$ equilibrium has a closed form,
$w = at/(a+\lambda)$, so it is checked rather than reported.

**And the other half of the AdamW argument is measured too**: for plain
descent the two forms settle identically to better than
$\val{p20.wd.sgd.gap}$, which is what makes the distinction a fact about
adaptive methods rather than about penalties.

#### Program P17's rescaling turned out to be the best thing to say about Adam

This was not planned and it cost nothing, because P17 had already done the
work. That program showed that writing a parameter as $w = c\,u$ leaves the
function a network computes completely unchanged while multiplying that
direction's curvature by $c^{2}$ \dash{} one model, two sharpnesses.

It is exactly the transformation a per-coordinate method is invariant to. At
$c = \val{p20.rescale.c}$ plain descent at its own optimal step size
**diverges**, $\val{p20.sgd.overshoot}$ times past P17's bound, while Adam
takes $\val{p20.adam.plain}$ steps in both coordinate systems. That is a
stronger claim than any speed comparison, because it does not depend on the
problem \dash{} and the program says in its closing frame that it is *not*
claiming Adam is better, because that is an empirical question about a class
of surface nobody has characterised.

#### Rule 2 caught the last node of a three-rank figure, for the fourth pass running

All three figures were read against the frames on either side of them before
being rendered, and all three needed work \dash{} `p20-one-update`'s middle
node previewed §4's mechanism, `p20-each-fixes-one`'s last node stated §4's
answer thirteen frames early, and `p20-penalty-enters`'s last node stated the
answer to the question the frame it sits in ends with.

That is P17, P18, P19 and now P20, and the reason is structural rather than
accidental: **a three-node chain naturally ends on its conclusion, and the
conclusion is usually what the next frame elicits.** Read the last node
against the next frame before rendering anything.

Measured afterwards in all four builds. `p20-one-update` sits above frame 3's
question and answers nothing in it, which is the P04/P07 case for the ninth
time; the other two sit on the page that delivers what they carry, in the order
question, answer, figure.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P20.1 one-update | 657 / 654 | 5.98 | 6.71 | 6.74 | 7.62 | 7.66 |
| P20.2 each-fixes-one | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P20.3 penalty-enters | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

#### Layout

Two overfull boxes arrived and both are recorded classes, applied after the
build named them rather than while drafting:

- **$\num{12.1}$ pt in `main-pl`**, from the comparison table's row labels
  \dash{} *zysk przy $\kappa = \ldots$* against English's *advantage at* \dash{}
  which is Program~\ref{prog:F05}'s finding that a `\val{}` numeric column
  leaves almost no room for a long label. The labels are now the bare
  $\kappa$ values in both editions.
- **$\num{3.9}$ pt in `main-en-a4` alone**, from a run of four unbreakable
  maths spans inside a further-problem `\answerto`. Program~\ref{prog:F06}'s
  rule exactly, and the recorded fix worked without a detour: **put it in a
  display.**

After both, the multiset is element for element the pre-P20 baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with no stranded
openers, no stranded headings and **no orphaned cues at any point in the
pass**. Three orphan tails added, one each in `main-en`, `main-pl` and
`main-pl-a4`.

#### The trap catalogue's Optimisation cluster was stale, and it is now the fifth file

Reading the issue's own trap list before writing \dash{} the discipline
Program~\ref{prog:P17}'s pass earned \dash{} turned up the P7-insertion
off-by-one again, this time in five places in `notes/02` §3: the section
heading said `(P18–P21)` where Part VI is P19--P22, item 21 pointed at P16 and
P18 where P17 delivers it, item 23 pointed at P19 where P20 owns schedules,
item 24 pointed at P20 where P21's brief undertakes the linear scaling rule by
name, and item 25 pointed at P19 and P24 where F04 elicits it and P21
undertakes it.

**Every one was settled against the destination program's own brief rather
than by assuming the off-by-one**, which is the rule Program~\ref{prog:P10}'s
pass established and the reason item 24 moved *forward* rather than back. The
rest of §3 is still not swept, for the reason already recorded: items 74
onward are correct and items 1--73 are a mix, so a blanket renumber would
break the ones that are right.

#### Also

- Traps 209 to 215 added, and items 21 to 25 corrected.
- **Elicitation 47%**, from three conversions that added no frame. The best of
  them is the one that names Adam: the reader writes the update out of the two
  averages and is then asked what they have written, so the algorithm arrives
  as something they assembled rather than as a recipe.
- Parity took two rounds. One was the recorded `Program~\ref{...}'s <maths>`
  inversion in a summary item; the other was a genuine editorial slip \dash{}
  the English said *section 6* and the Polish *sekcja 7* for the same
  forward pointer, and with seven sections the Polish was right.
- The listing was extracted from `main-en.pdf` p823 and executed from `code/`:
  it prints `[0.0997, 0.0999]` and `[0.1, 0.1]`, which is what the page prints
  and what the frame beside it claims. Note the first row \dash{} the epsilon
  biting at a tiny gradient \dash{} is the section's own measurement visible in
  the listing, which is why the listing uses two coordinates rather than one.
- Frame numbers mapped after writing: sections landed at
  `1--7 / 8--16 / 17--20 / 21--29 / 30--33 / 34--37 / 38--42`.

### Program P21 pass, August 2026

**Thirty-nine teaching frames, forty-one printed, both editions**, against a
brief that projected fifty. Seven sections: a gradient you did not ask for, how
noisy exactly, why the occasional enormous step, two rules that hold different
things fixed, what a smoothed curve hides, one denominator two answers, and two
ways through a coin flip.

Fifteenth program under its brief's estimate, and the cause is the F07/P06 kind
once more: **three written programs had already delivered the pieces this one
would otherwise have had to build.** Program~\ref{prog:P20} hands over the
batch by name and leaves the optimiser entirely settled.
Program~\ref{prog:F06} owns clipping outright \dash{} both operations and the
measurement \dash{} and says in as many words that P21 owes *why the enormous
step happens*, never the two operations. Program~\ref{prog:F04} owns the
average-of-averages error and works it three times, and owns the exponential
moving average.

So P21's own job is narrower and better: it is the program in which every
complaint about training turns out to be a statement about a **variance**.

#### The headline is a fork, and it is free

Two estimators of one gradient through a sampling step, both unbiased, measured
at $\val{p21.grad.samples}$ samples:

| dimension | score function | reparameterised |
|---|---|---|
| $\val{p21.grad.d.lo}$ | $\val{p21.grad.score.lo}$ | $\val{p21.grad.repar}$ |
| $\val{p21.grad.d.hi}$ | $\val{p21.grad.score.hi}$ | $\val{p21.grad.repar}$ |

**The reparameterised variance does not move at all**, and not by luck: the
estimator for one component is a function of that component's own draw, so the
other ninety-nine dimensions never enter it, and the script asserts it at every
dimension. The score function's grows by three orders of magnitude, because it
multiplies by the value of the *whole* function.

The consequence is the sentence the section exists for. After forty thousand
samples the reparameterised estimate is $\val{p21.grad.off.repar}$ per cent
from the truth and **the score-function estimate is still
$\val{p21.grad.off.score}$ per cent out** \dash{} from an estimator that is
exactly right on average. *Unbiased is not the same as usable*, and that is why
the policy-gradient literature is largely a literature about variance reduction
and the variational one is not.

#### The scaling rules, stated as two exact invariants rather than adjudicated

The brief asks for the linear scaling rule *as folklore, not as a law*, and the
honest way to do that turned out to be arithmetic rather than hedging. The
update is $\eta\hat g$, so its variance is $\eta^{2}\sigma^{2}/B$, and:

- scaling $\eta$ by $\sqrt{k}$ leaves that **exactly** unchanged;
- scaling $\eta$ by $k$ multiplies it by $\val{p21.scale.linear}$, and holds
  the ground covered per example fixed instead.

Both are one line and both are checked. So the program can state precisely what
each rule preserves, say that the empirical question of which matters more is
not settled here, and leave the reader able to ask what a recommendation rests
on. That is worth more than either picking a side or refusing to discuss it,
and it turns trap item 24 from a caution into two invariants.

The third choice \dash{} change $B$ and leave $\eta$ \dash{} holds neither
fixed, which is why it is the one nobody argues for, and it is elicited rather
than warned about.

#### An assertion refused a threshold, for the twelfth pass running

The unbiasedness section first asserted that the worst batch mean is *more than
four times the population mean away from it*. It failed at $6$ against $8$
\dash{} a threshold chosen so a claim would pass, which Programs
\ref{prog:F11}, \ref{prog:P15} and \ref{prog:P20} have each paid for.

The replacement needs no threshold at all and is a better frame: the
$\val{p21.pop.subsets}$ batch means average to $\val{p21.pop.mean}$ **exactly**,
over fractions, and they **straddle** it \dash{} from $\val{p21.pop.lo}$ to
$\val{p21.pop.hi}$, with one of them pointing the opposite way. Unbiasedness is
a statement about the ensemble; straddling is what says it is not a statement
about a draw.

And because every batch is drawn, it is a **proof** for that population rather
than evidence about it, which is Program~\ref{prog:P14}'s distinction doing a
second job.

#### A percentage that rounds to zero, which is P05's defect in a mirror

The clipping section reported that a threshold at four times the typical
gradient size clips $\num{0.0}$ per cent of steps. That reads as *exactly
none* and it is not \dash{} it is one step in $\val{p21.clip.trials}$.
Program~\ref{prog:P05} recorded the same failure from the other end, where a
quantity rounding to $100$ per cent had to be reported as its complement; the
rule generalises to **any percentage that rounds to a boundary**, and the fix
is the same: report the count, where every figure means something.

The measurement is then the section's best sentence: **$\val{p21.clip.half}$
per cent of steps against $\val{p21.clip.four.n}$ in $\val{p21.clip.trials}$**,
for the same operation with the threshold moved. The first is not a safety net
but a different algorithm \dash{} the direction of the gradient with a length
fixed by hand \dash{} and nothing reports the difference.

#### Rule 2 caught the last node of all three figures, for the fifth pass running

`p21-one-draw`'s middle node said the average over every batch is exact, which
is frame 4's answer, and its last node gave frame 6's trapbox.
`p21-noise-and-batch`'s last node gave frame 12's answer to a question frame 11
ends with. `p21-two-estimators`'s last node gave frame 34's.

That is P17, P18, P19, P20 and now P21. The finding is no longer a coincidence
and is worth stating as a rule in its own right: **write the figure's last node
against the frame that follows it, before rendering anything.** A three-node
chain ends on its conclusion, and the conclusion is what the next frame elicits;
the shape of the diagram and the shape of a frame pair are in conflict by
construction.

Measured afterwards in all four builds. `p21-one-draw` sits on the same page as
frame 3's question in every build and answers nothing in it, which is the
P04/P07 case for the tenth time; `p21-two-estimators` sits a page before frame
33's question and carries only what frames 32--33 state; `p21-noise-and-batch`
sits with frame 11's question and frame 12's answer.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P21.1 one-draw | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P21.2 noise-and-batch | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P21.3 two-estimators | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

#### The forward prerequisite, discharged as declared

This is the book's one deliberate forward dependency and it has not reverted:
variance itself is Program~\ref{prog:P24}'s and concentration is
Program~\ref{prog:P25}'s, two parts later. Section 1 carries a `rigourbox`
naming both with pointers, giving the one sentence the reader needs, and saying
that P25 returns to minibatch noise once the machinery exists. The Learning
outcomes say so too.

**And the issue's own trap list carries the P7-insertion off-by-one, in a fifth
file.** Issue \#35 names \enquote{Adam with \code{weight\_decay} is $L_2$
regularisation} as one of P21's three traps; that is item 22, its owner in the
catalogue is P20, and Program~\ref{prog:P20} delivered it in the previous pass.
The other two \dash{} the batch-size rule and the accumulation denominator
\dash{} are P21's and are both delivered here. Recorded rather than edited,
because the issues are generated from the manifest and the manifest is right.

#### Also

- Traps 216 to 222 added, and items 24 and 25 marked delivered with their
  numbers.
- Layout cost nothing: the overfull multiset is element for element the
  pre-P21 baseline in all four builds \dash{} `[]`, `[]`, `[6.3]`, `[]`
  \dash{} with no stranded openers, no stranded headings and **no orphaned
  cues at any point in the pass**. Three orphan tails added.
- **Parity found one genuine divergence and it was in the English**: an
  `$\eta/1$` written for \enquote{$\eta$ per example}, which is not a
  meaningful expression and which the Polish had sensibly not translated. C4,
  C8, C12 and C14 all fired on it at once. The English now says what it means
  in words.
- Elicitation 48%, from four conversions that added no frame. The best of them
  is the third scaling choice: the reader is asked which quantity keeping
  $\eta$ holds fixed, and the answer is \enquote{neither}.
- The listing was extracted from `main-en.pdf` p840 and executed from `code/`:
  it prints `True` and `(-4.0, 7.333333333333333)`, which is what the page
  prints and what the frames beside it claim.
- Frame numbers mapped after writing: sections landed at
  `1--7 / 8--12 / 13--17 / 18--22 / 23--25 / 26--30 / 31--39`.

### Program P22 pass, August 2026 --- Part VI is complete

**Thirty-five teaching frames, thirty-seven printed, both editions.** Six
sections: a best point that is not available, where the two curves touch, the
multiplier is a price, the other way to enforce a constraint, a price you have
already been setting, and when the constraint is an inequality.

Sixteenth program under its brief's estimate, and again because the neighbours
had spent the machinery rather than the content. Program~\ref{prog:P15} owns
the gradient **and** the fact that it is perpendicular to a contour, derived
from Program~\ref{prog:P05}'s cosine rather than drawn \dash{} which is the
entire geometric content of \enquote{the two gradients are parallel}, said
about two functions instead of one. Program~\ref{prog:P05} owns projection in
full, including that the answer is the closest point rather than merely a
point. Program~\ref{prog:P19} owns convexity, so the honest hedge about
sufficiency is written there.

#### The price is an identity, not an analogy, and it is exact

Every book says a multiplier can be interpreted as a rate of change of the
optimal value. This program **checks it as an equality**, over fractions, with
no tolerance anywhere:

\[ \lambda \;=\; \frac{\mathrm{d}f^{*}}{\mathrm{d}c} \]

at $\val{p22.price.levels}$ constraint levels. A central difference is exact
for a quadratic \dash{} its error term carries a third derivative and a
quadratic has none \dash{} so the two lists come out identical term for term as
`Fraction`s, and the committed transcript prints them side by side.

That is worth more than the interpretation stated in prose, because it converts
\enquote{can be interpreted as} into \enquote{is}, and the whole of the rest of
the program is then a reading rather than a claim.

**And the caveat is measured too.** Relaxing the constraint from
$\val{p22.relax.from}$ to $\val{p22.relax.to}$ gains $\val{p22.relax.gain}$
against a multiplier of $\val{p22.relax.lam}$: a multiplier prices the
\emph{first} unit, and using it for a whole one is the same error as using a
gradient for a whole step.

#### The payoff, in the setting people actually meet it

$\beta$ in a KL-penalised objective is a multiplier, so it is a price with
units \dash{} reward per nat. Measured along the family of solutions
$p \propto q e^{r/\beta}$, the slope of expected reward against divergence is
$\beta$ itself, to better than $\val{p22.kl.slope.bound}$ at every $\beta$
tried.

Two consequences fall straight out and both are the kind of thing this book is
for. A $\beta$ tuned against one reward model does not transfer to a reward
model on a different scale, because the two rewards are in different units
\dash{} which is Program~\ref{prog:P21}'s point about hyperparameters one part
later and one level up. And **each $\beta$ names exactly one divergence level**,
so a hard constraint and a penalty are the same problem parameterised
differently: methods presented as rivals on that axis are arguing about
parameterisation rather than about objectives.

#### The declared forward reference, taken by P18's route

The manifest left the choice open \dash{} state the one fact KL needs with a
pointer, or carry the payoff with a quadratic penalty \dash{} and said it may
not be left undeclared. This program takes the first route, on
Program~\ref{prog:P18}'s precedent and Program~\ref{prog:P21}'s: a `rigourbox`
in section 5 states that KL is a non-negative measure of how far one
distribution sits from another, zero only when they agree, names
Program~\ref{prog:P30} as where it is defined, and uses nothing else about it.
The Learning outcomes say so too.

That is now three declared forward references discharged the same way (P18's
cross-entropy, P21's variance, P22's KL), which makes it a settled house
pattern rather than three separate decisions.

#### Rule 2 caught two figures, and one of them gave away two frames at once

`p22-two-gradients` was declared in frame 6 and its middle node said *where
they cross at an angle you can slide along the constraint and improve* \dash{}
frame 8's answer \dash{} while its last node said *at the best feasible point
they touch, and touching is a statement about gradients*, which is frame 9's.
**One figure answering the next two elicitations** is the worst instance this
book has had, and it happened because the figure was written as a summary of
the section rather than of the frames above it.

`p22-two-enforcements`'s last node reached frame 21's answer, which is the
familiar case. Both were reworked to state only what the frames above them
deliver, and the third figure needed nothing.

So the rule stated at P21 holds and gains a clause: **write a figure against
the frames above it, never against the section it sits in.** A section's
summary is by construction the answer to the section's questions.

#### Two assets shared a stem, which nothing checks

The transcript and one of the figures were both called `p22-price`, so
`figures/transcripts/p22-price.txt` and `figures/diagrams/*/p22-price.pdf`
existed side by side. Nothing in the repository objects: `\transcript{}` and
`\mermaidfig{}` build their own paths from the stem and neither knows about the
other, so the collision is silent and would only ever surface as a confusing
`make` dependency or a wrong file in a manifest.

Renamed to `p22-lambda-is-slope`, which is a better name anyway. **No check was
added**, because this has never shipped and the fix is to notice it while
naming; but it is worth knowing that the two namespaces are separate and
unpoliced.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P22.1 two-gradients | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P22.2 price | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P22.3 two-enforcements | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks.

#### Also

- Traps 223 to 229 added.
- **Layout cost nothing.** The overfull multiset is element for element the
  pre-P22 baseline in all four builds \dash{} `[]`, `[]`, `[6.3]`, `[]`
  \dash{} with no stranded openers, no stranded headings and **no orphaned
  cues at any point in the pass**. One orphan tail added, in `main-pl`.
- **Parity came back clean on its ordered checks first time** \dash{} C4, C8,
  C12 and C16 all passed on the first run, which is the seventh program to
  manage it. The only failure was C7 on a *text* value, `p22.price.h`, which
  is the F10/P03/P18 situation: a step size of a thousandth is a parameter of
  a check rather than a computed quantity, so both editions now write
  $\frac{1}{1000}$ and the emission is gone.
- The listing was extracted from `main-en.pdf` p865 and executed from `code/`:
  it prints the two identical lists of `Fraction`s that the page prints.
- `main-pl` passed a thousand pages.
- Frame numbers mapped after writing: sections landed at
  `1--6 / 7--11 / 12--17 / 18--21 / 22--28 / 29--35`.

### Program P23 pass, August 2026 --- Part VII begins

**Forty-seven teaching frames, forty-nine printed, both editions**, against a
brief that projected fifty-five. Six sections: a weight on a list of outcomes,
conditioning is changing the denominator, Bayes in one line, what fraction of
the alarms are real, independence and what it does not survive, and
conditional independence and a second signal.

Seventeenth program under its brief's estimate, and the smallest shortfall in a
long while, because the cause is a fourth kind. The ground was genuinely
unspent \dash{} a grep for \emph{Bayes}, \emph{conditional}, \emph{prior},
\emph{independence} and \emph{base rate} across every written program returns
only file headers deferring here \dash{} and the neighbours supplied
\emph{objects} rather than machinery or content. Program~\ref{prog:F10} hands
over the numerator, the denominator and the observation that choosing the
denominator was a decision; Program~\ref{prog:F13} hands over the density and
the fact that its height is a rate. So nothing had to be built and nothing had
been spent, which is why the estimate nearly held.

#### The elicitation rate was measured on the draft and then designed up

**53%, the highest outside Part I and above the book's own rate**, and the
route there is the finding rather than the number. The finished draft measured
**33%**. Ten frames that \emph{stated} something the reader could produce were
converted \dash{} the statement moved into the next frame's answer, the frame
ended by asking \dash{} and that took it to 53% while adding two frames.

The P04 pass did three of those conversions and reported the move as cheap.
Doing ten says something stronger: **measure the rate on the draft before the
frame remap, because a conversion is nearly free and the remap is not.** Nine
of the ten needed no new frame at all; five produced the P06 pattern, a frame
opening with `\ans` and ending with `\dotline`.

#### A bare caret in a manifest brief is a fatal build error, and it was mine

Appendix~B's variance pointer had to move to Program~\ref{prog:P24}, so a
clause was added to P24's brief naming the notation \dash{} written as prose,
with `D^2(X)` in it. `gen_stubs.py`'s `escape()` turns an exponent into maths
**only inside backticks**; outside them the caret reaches LaTeX raw, opens
maths mode and swallows the rest of the paragraph.

Two `Missing $ inserted` errors and a **192.5 pt overfull hbox** \dash{} the
largest this book has produced since F05's tables \dash{} from one character,
in a stub file nobody had edited by hand, and `make` died with `Error 12`
before three of the four formats had run. **One cause, three symptoms**: the
errors, the box, and three page counts that had not moved.

The recorded habit caught it: `MAKE_EXIT 2` while the harness reported exit 0,
and an unchanged page count is a failed build. What the generator now does is
**refuse** such a brief before writing anything, naming the program and saying
to write backticks instead. Refusing beats escaping it to
`\textasciicircum{}`, because a caret in a brief always means an exponent, so
silently producing an unreadable glyph would hide the author's actual mistake.
Proved by mutation: a probe caret in F1's brief fails `--check` with exit 1 and
names F1.

**The generalisable half is about where a mechanism's documentation stops.**
`escape()`'s own docstring describes the backticked case exactly and correctly.
Nothing said what happens outside it, and nothing checked. That is the third
time in this repository a graceful mechanism has hidden an authoring error
\dash{} after `\transcript`'s file-is-absent marker and `\mermaidfig`'s
fallback \dash{} and the fix has been the same each time: make the wrong form
impossible or fail on it, rather than degrade.

#### The index's overfull vbox: five cycles against a mechanism that was never running

This is the pass's most valuable finding and it retires an entry this file has
been extending since Program~\ref{prog:P12}.

`theindex` here is not book.cls's two-column index. **`imakeidx` is loaded
without its `original` option, and in that mode it replaces the environment
with `multicols`.** So none of the machinery five passes reasoned about was in
the room:

- **`\raggedbottom` sets `\@textbottom`, which `\@makecol` reads.** multicol
  installs its own output routine and never calls `\@makecol`, so the
  `\raggedbottom` added after the first CI failure had been **inert from the
  day it was added**. Its analogue inside `multicols` is **`\raggedcolumns`**.
- **`\vfuzz` is inert too, and provably so**: multicol sets `\vfuzz\z@` itself
  immediately before the `\vbox to` that balances the final page. A value set
  in the environment's body cannot survive that assignment \dash{} which is
  exactly why CI answered `8.28874` pt a second time, to the ten-thousandth of
  a point, after `\vfuzz` was added.
- **`\flushcolumns` is multicol's default**, and it is precisely the rigid
  setting every one of those comments diagnoses: each column held to
  `\@colroom` with nothing to give.

And it explains the one detail Program~\ref{prog:P17}'s pass recorded and could
not account for: **the complaint was always on the index's last page**, because
that is the only page multicol *balances* rather than splits, and a balanced
column under `\flushcolumns` has to come out exact.

So the `\parskip` shrink swept five times, the `\textheight` reduction that
replaced it and the `\vfuzz` that replaced that were all compensating for a
switch nobody had thrown. `\raggedcolumns` is one word, it is multicol's
documented answer, and it is what every index in print does.

**The generalisable finding, and it is worth more than the fix: a remedy that
is correct for the environment you think you are in is INERT in the one you are
actually in, and an inert remedy looks exactly like one that did not go far
enough.** Every cycle read the surviving residual as evidence that the constant
needed raising. The check that would have ended it at the first cycle is one
line: **before sweeping a constant a second time, confirm that the macro you
are setting is read by the code that emits the complaint.** Here it took one
`grep` of `imakeidx.sty` and one of `multicol.sty`.

Two smaller things fall out of it. The repository's own rule \dash{} *an
identical measurement after a change is the signal that the change did not
reach what was measured* \dash{} fired correctly and was read as
\enquote{the value is too small} rather than \enquote{the assignment is not
reaching}; it is the second reading that is nearly always right. And the
mechanism was settled in seconds by a ten-line standalone file rather than by
another book build: a `\vbox` overfull inside a group with `\vfuzz` raised,
shipped inside the group and again outside it. **When a question is about TeX's
own semantics rather than about this book, ask TeX, not the book.**

#### The contents column, a four-digit page number, and a fix in the wrong place

`main-pl` crossed a thousand pages in the P22 pass and acquired four-digit
contents entries in this one. book.cls reserves `\@pnumwidth` = 1.55em for the
page number, which fits three digits and not four: `1001` and `1009` each
overflowed by $\num{4.93}$ pt. It is the contents column's third defect of this
shape after P16's long Polish title and the running-head guard, and it is the
first that **cannot be fixed by shortening anything**, because the token that
overflows is a page number. Widened once, to 2.05em, rather than watched.

**And the first attempt at the second half of that fix was worse than the
defect it addressed.** `\l@part` and `\l@chapter` take their title's
`\rightskip` from `\@pnumwidth` as well, so widening it narrows those two lines
and tipped the Polish Part V title over on A4. `\emergencystretch` is the right
instrument \dash{} TeX spends it only on a line it cannot otherwise set. It was
added with `\apptocmd{\tableofcontents}`, **which runs after `\@starttoc{toc}`
has already typeset the whole contents.** So it reached nothing it was written
for, and because `\tableofcontents` is not inside a group it stood for every
paragraph of the book from the contents page onward.

**It was invisible because it made the ledger look better.** The $\num{6.3}$ pt
box this file records in `main-en-a4` \dash{} F1's
$7\,000\,000\,000$, which cannot break \dash{} simply disappeared: a genuine
overfull line silently loosened rather than fixed, which is precisely the
objection this book makes to `\vfuzz`. `\pretocmd` sets the stretch before the
contents is read and `\apptocmd` restores it after, and the 6.3 pt box comes
back, where it belongs.

**And removing the leak exposed a second line it had been masking**, which is
the diagram manifest's **sixth** recurrence and the first caused by something
other than long copy: `\@pnumwidth` is also the right margin `\@dottedtocline`
wraps against, so widening it for a four-digit page number narrowed the
manifest column by half an em for every entry in the book. `main-pl-a4`'s
`p10-bowl-or-saddle.mmd` line went 2.57 pt over. Fixed the recorded way
\dash{} shorten the Polish copy, from 33 characters to 25 \dash{} rather than
by widening the stretch, because manifest copy is the one thing in that column
that *can* be shortened. The Part V contents line cannot, which is why the
stretch stays there and only there.

**Two remedies in one pass applied where the code that produces the complaint
could not read them**, and both looked like remedies that had not gone far
enough. It is worth stating as one rule: **when a fix does not move the number,
check where it runs before you check how large it is.** The two diagnoses cost
five CI cycles between them and one `grep` each to settle.

#### The transcript spoiled a frame fourteen frames later

One listing carried the base-rate sweep and the evidence accumulation
together, and the accumulation prints `Fraction(363, 400)` \dash{} section 6's
elicited answer \dash{} inside section 4.

That is Program~\ref{prog:P04}'s rule (**a transcript is under the same rule as
a frame**) biting at a new distance. Every previous instance was a listing
answering the frame it sits in, which is visible while writing that frame; this
one answered a question two sections away, which is only visible if you read
the listing against the whole program. Split into `p23-base-rate` and
`p23-accumulate`, each placed where its content has just been delivered, and
both extracted from the finished PDF and run.

**So the rule needs its scope stated: a transcript may not answer any question
put to the reader anywhere later in the program**, which is the same widening
rule~2 went through after the F02 review pass.

#### Appendix B's three stale pointers, and P18's estimate was right

Program~\ref{prog:P18}'s pass found four false pointers in Appendix~B, fixed
the one that was its own, recorded the other three and said the audit was
\enquote{five greps}. It was five greps.

- **The variance box pointed at P23.** Variance is Program~\ref{prog:P24}'s,
  whose brief names it in its first sentence, and P23 defines no random
  variable at all. Corrected \dash{} and the clause was added to P24's brief so
  the pointer names a program that has promised the thing, which is the
  F04-to-P21 remedy.
- **The interval box said Program~F6 says so at the first interval a reader
  meets.** The first interval in the book is F03's, and neither program carries
  an interval notation box. Corrected to what is true: the first interval is in
  Program~F3 and the appendix is where the convention is recorded.
- **The `tgh` note said Program~F8 records it.** F08 mentions $\tanh$ once in
  passing and records nothing; F07, which owns it, records nothing either. Same
  correction.

Fixing them was in scope precisely because P23 is the program one of them
names, and the other two are a line each in a file already open. The
P07-covariance precedent (record rather than fix) is for edits that would need
a merged program rewritten; these needed no program touched.

#### The cross-programme gate is P12's third kind

Not a value gate and not a shared predicate but **the same worked example
continued**. Program~\ref{prog:F10} counts two overlapping evaluation sets and
then says a fraction of counts is a naive probability; divide its four
committed counts by their union and the union rule \emph{is} the addition rule:
$\frac{1}{2} + \frac{3}{5} - \frac{1}{10} = 1$. The script asserts F10's own
numbers and emits nothing, because every fraction in that frame is head
arithmetic from figures F10 already prints.

That is the form to reach for whenever a program extends an example rather than
inventing one, and it is stronger than a resemblance and cheaper than a
re-derivation.

#### Rule 2: written against the frames above, before rendering

The P22 rule was applied while designing rather than after a build, and all
three figures still needed work \dash{} which is the sixth pass running that
the last node of a three-rank chain has been the spoiler.

**And figure 1 had to move**, which is the milder P02 case. Its third node said
an event's probability is \emph{the weight of that set}, and the frame it was
declared in ends by asking which of the three rules does not apply to a
density's height \dash{} whose answer is \enquote{the second, because it bounds
the measure of a set}. The node did not state the answer; it supplied its last
step. Moved to the end of frame 3, where its content is exactly what frames 1
to 3 deliver and where the following question (the complement rule) is
untouched by it.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P23.1 space-and-measure | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P23.2 two-denominators | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P23.3 two-populations | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks. Measured on
the page afterwards, each figure sits at the end of the frame that delivers
what it carries, with the following question and its answer immediately after
it \dash{} `main-en` 883/884/884, 888/889/889, 893/893; `main-en-a4`
741/741/742, 745/746/746, 749/749. Three Polish anchors could not be extracted
because `pdftotext` hyphenates them, which is Program~\ref{prog:P10}'s recorded
extraction limit rather than a defect; the ones that did extract agree
(`main-pl` 898/898, 903/903/903; `main-pl-a4` 751/751, 756/756/756), and the
structural argument covers the rest: a float cannot rise above the page its
declaration point falls on.

#### An aibox that named no specific quantity

The draft's said that an anomaly detector fires constantly and every alert is
noise, which names a class of complaint rather than a line of a system. Third
pass in the book to have to fix this, and the replacement is better than a
demotion to prose: **precision is $\Prob(\text{real} \mid \text{flagged})$ and
recall is $\Prob(\text{flagged} \mid \text{real})$**, both printed on every
classification report, and recall conditions on the true class alone so it
travels with the model while precision conditions on what was flagged so it
does not. Two adjacent lines of one report behaving completely differently,
with nothing on the card to say so \dash{} which is specific, checkable and is
the section's own theorem read on an artefact the reader has in front of them.

#### The trap catalogue's unswept range bit again, exactly as predicted

Item 28 \dash{} the base-rate calculation, which is this program's headline
\dash{} pointed at \enquote{P22, P26}. P22 is \emph{Constrained optimisation}.
It is the P7-insertion off-by-one in the range Program~\ref{prog:P10}'s pass
deliberately left unswept, saying items 1--73 are a mix and a blanket renumber
would break the ones already corrected. Corrected against the destination
briefs: P23 delivers it and **P28** returns to it with a prior on the parameter
rather than a point estimate.

Traps 230 to 236 added.

#### Also

- **Parity came back clean on its ordered checks first time** \dash{} C4, C8,
  C12 and C16 all passed on the first run, the eighth program to manage it. The
  two failures were C9 (a diagram renamed under a key too long for the manifest
  column, on P14's finding) and C7 on two values the frames do not quote.
- The two transcripts were extracted from the finished PDF and executed: they
  print the same fractions the page prints, including the exact
  $\frac{1}{2}$ at one fault in a hundred, which is why the listing prints
  fractions rather than decimals.
- **A number that did not reproduce from the page, caught before it shipped.**
  Two alarms give exactly $\frac{363}{400}$, and at one decimal the page would
  have said $\num{90.8}$ per cent beside a transcript printing $\num{0.9075}$.
  The value is emitted at two decimals instead. That is F04's, F05's and P07's
  defect, avoided by dividing what the page prints before writing the sentence.
- **A figure that rounds to another figure two sections away.** Three alarms
  leave a $\num{99.9}$ per cent posterior, which is also the accuracy paradox's
  number \dash{} F08's defect of two quantities printing as one. Reported as
  its complement instead, where every digit means something, which is P05's
  rule for a quantity near a boundary.
- **Layout cost one line of manifest copy and nothing else.** The overfull
  multiset came back element for element to the baseline in all four builds
  \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with **zero overfull vboxes
  anywhere**, no stranded openers, no stranded headings, **no orphaned cues at
  any point in the pass**, and **the orphan-tail count did not move**: 23, 27,
  20, 21, exactly the pre-P23 figures. That is the eighth time (F13, P07, P09,
  P12, P15, P17, P19, P23), and every time for the same reason \dash{} the
  recorded rules were applied while drafting rather than after a build named
  the defect.
- Pages 1027 / 1043 / 864 / 875, from 997 / 1016 / 840 / 853.
- Frame numbers mapped after writing and again after the ten conversions:
  sections landed at `1--8 / 9--15 / 16--21 / 22--30 / 31--37 / 38--47`.

### Program P24 pass, August 2026

**Sixty-four teaching frames, sixty-six printed, both editions**, against a
brief that projected sixty. **It is the first program in eighteen to come in
over its estimate, and the reason is measurable rather than mysterious**: the
finished draft was fifty-five frames, in line with the seventeen before it, and
raising the elicitation rate from 36% to **46%** added nine.

That is the first time the elicitation ledger's cost has been visible in the
frame count. Program~\ref{prog:P04}'s pass priced three cues at two pages;
this one prices ten percentage points at nine frames, on a program whose
sections 2 to 4 are derivations and therefore have fewer places to stop and
ask. Both halves are worth carrying: **the brief's estimate is a planning
figure for content, and the rate is paid in frames on top of it.**

#### The issue asked this program to repay a debt that is not its to repay

Issue \#38's \enquote{Done when} list says \emph{minibatch noise revisited,
repaying P21's forward reference}. Four sources say otherwise and they agree
with each other: Program~\ref{prog:P21}'s own rigour box names
Program~\ref{prog:P25}, this file names P25, P25's brief owns
\enquote{variances of independent quantities add; averages concentrate} in as
many words \dash{} and **P21 has already measured the $1/B$ law and the
$\sqrt{B}$ spread itself**, over twenty thousand values and four thousand
trials per batch size.

So what P21 borrowed was never the rate. It was a **definition**, given in its
rigour box as one sentence and pointed here. That is what is returned: the
definition, computed on P21's own ten-number population, by both of its routes,
exactly over fractions, and gated against P21's committed mean. The rate stays
Program~\ref{prog:P25}'s, and section 3 says so.

Ninth pass to find a claim about another program that needed fixing, and the
second \dash{} after Program~\ref{prog:P09}'s own brief \dash{} where the
wrong claim was in a **contract document** rather than in a frame. The
manifest brief is right and the issue's checklist is the stale copy, which is
the same shape as the \emph{No Quiz (Foundation-only)} box that P04 and P14
each found false.

#### Four claims about other programs, and three of them were wrong

The recurring class, three times in one pass, all caught by opening the files
rather than by any gate.

- **The book does not state the Cauchy--Schwarz inequality anywhere.** A rigour
  box said Program~\ref{prog:P05} states it for the dot product. It does not,
  and neither does anything else. What the book *does* have is
  Program~\ref{prog:F09}'s $a \cdot b = \lVert a\rVert \lVert b\rVert
  \cos\theta$, and a cosine is never outside $\intcc{-1}{1}$ \dash{} so the
  bound on a correlation is F09's geometry read on a different space, which is
  both true and a better sentence.
- **Program~\ref{prog:P19} could not have written $\Ex[f(X)] \ge f(\Ex[X])$**,
  because the expectation was not defined until this program. It states Jensen
  for \emph{means} \dash{} the mean of the squares is at least the square of
  the mean. The correction improves the frame rather than merely fixing it: the
  expectation defined here is the same object, so P19's sentence now reads in
  the new notation, which is what defining the object bought.
- **The exponential moving average is Program~\ref{prog:F04}'s, not
  Program~\ref{prog:P20}'s**, and F04 does no probability at all, so
  \enquote{its expectation is read term by term} was wrong twice over. Replaced
  with an example from this program's own section 5.
- And one **statement of first occurrence** removed \dash{} *this book has
  been calling it the spread since Program~P05* \dash{} which is the class this
  file forbids outright, because nothing can check it and it decays silently.
  It now names P05 and P21 as places the word is used, which is checkable.

#### The transcript was about to be a fabricated console block, again

`[round(v, 4) for v in top_k(PROBS[2.0], 2)]` was written into the file as
`0.0000` for the two truncated tokens, because the rounding had been applied to
the script's \emph{output} with a format string rather than written into the
listing's own code. A session prints `0.0`.

That is Program~\ref{prog:P19}'s finding exactly, one program later, and the
fix is the same: `repr()` of the rounded list, so the printed line and the
printed result cannot come apart. Extracted from the finished PDF and run, it
reproduces to the character.

#### The headline: what each of the three knobs destroys

Program~\ref{prog:F05} settled temperature \dash{} a strictly increasing
function keeps the order of a list, so it cannot move the $\argmax$ \dash{} and
committed the same four-token distribution at three temperatures. This program
continues that worked example rather than inventing one, gated against all
twelve of F05's committed probabilities, and asks the question F05 could not:
what does each knob \emph{destroy}?

- **Temperature reweights.** Every token stays possible and the edit is
  reversible.
- **Top-$k$ removes.** At $T = 2$ with $k = 2$ it deletes
  $\val{p24.topk.del.t20}$ per cent of the weight, after which
  \enquote{unlikely} and \enquote{impossible} are the same thing.
- **And the two fight, measurably.** The same $k$ deletes
  $\val{p24.topk.del.t05}$ per cent at $T = \num{0.5}$ and
  $\val{p24.topk.del.t20}$ at $T = 2$ \dash{} a factor of
  $\val{p24.topk.del.ratio}$, from a knob nobody touched, because temperature
  moves weight into the tail and the tail is what $k$ cuts. **Raising the
  temperature for variety and then truncating at a small $k$ spends most of
  what the temperature bought**, and nothing in a sampling configuration
  records that the two are coupled.
- **Top-$p$ keeps a count that is an outcome rather than a setting.** The same
  $p$ keeps $\val{p24.topp.kept.t05}$ tokens at $T = \num{0.5}$ and
  $\val{p24.topp.kept.t20}$ at $T = 2$, and between
  $\val{p24.topp.sweep.lo}$ and $\val{p24.topp.sweep.hi}$ of the four over a
  $\val{p24.topp.sweep.n}$-point sweep.

#### The Gumbel-max trick, and why it is integrated rather than sampled

$\argmax(\ln p + G)$ with $G$ standard Gumbel has \emph{exactly} the
distribution $p$. **The two-token case is already in the book**: the difference
of two Gumbels is logistic, so the first wins with probability
$\sigma(\ln p_1 - \ln p_2)$, and Program~\ref{prog:F07} proved that $\softmax$
on two scores \emph{is} $\sigma$ of their difference. The trick's simplest case
is F07's frame read backwards, and the script recomputes that identity over an
$81 \times 81$ grid rather than remembering it.

The four-token case is **integrated, not sampled**, and the frame says why: a
sampled check produces an estimate with an error bar, and \enquote{it agreed
within the error bar} demonstrates that the trick is approximately right, which
is the reading the section exists to refuse. Integration reproduces all four
probabilities at all three temperatures to $\num{1.1e-13}$, against a committed
ceiling of $10^{-11}$.

**Two things about that integral are worth keeping.** The range was chosen
rather than guessed \dash{} the Gumbel tail beyond $g$ is under $e^{-g}$, so a
first draft's $22$ left $\num{3e-10}$ outside and the four answers summed to
$\num{0.9999999989}$. And **more steps made it worse**: $\num{2.1e-13}$ at
200,000 against $\num{1.1e-13}$ at 100,000, because past a point the rounding
accumulated over the sum grows faster than Simpson's error falls. That is
Program~\ref{prog:P02}'s subject arriving in a quadrature.

#### The two halves meet on one number, and it is emitted once

At $T = 2$ top-$k$ deletes $\val{p24.topk.del.t20}$ per cent of the weight, and
those same two tokens win the noisy $\argmax$ $\val{p24.topk.del.t20}$ per cent
of the time. **The same figure, and the equality is the theorem** rather than a
coincidence: Gumbel-max reproduces $p$ exactly, so a token's win rate is its
probability and its probability is what truncation deletes.

So the script asserts the two are equal and the page quotes one value. Printing
it twice under two names would have been Program~\ref{prog:F08}'s defect
\dash{} two numbers that look like one \dash{} in the one place where being the
same number is the point.

#### An assertion refuted its own draft, for the thirteenth pass running

The draft asserted that top-$k$ deletes about the same fraction at every
temperature. It failed, and the failure is the section: what is asserted now is
the **ordering**, which is structural, rather than the three figures, which
move with the logits.

#### P07's undeclared forward reference is closed, and the rule is settled

This file has carried it as outstanding since the P10 pass: P07 prints
$\operatorname{Cov}(p, t)$ and $\operatorname{Var}(t)$ in its headline identity
and declares neither, and whoever wrote P24 was nominated to fix it and to
settle whether the rule is \emph{declare anything not yet defined} or
\emph{declare anything a payoff depends on}.

**It is neither, quite. The rule is: declare anything the reader must be able
to check.** P07's identity is *stated in terms of* the two, so a reader who has
not met them cannot verify the line the whole section rests on \dash{} which is
the bar Programs \ref{prog:P18} and \ref{prog:P22} were held to, and it is why
P07 needed the declaration while a merely-unnamed object would not. One clause
in P07's Learning outcomes, in both editions, on the P21 pattern.

Programs \ref{prog:P10} and \ref{prog:P11} needed the opposite treatment and
had already taken it: they declared the covariance matrix and then proved its
two facts where they stood. **A forward reference whose facts can be proved
locally should be**, and section 4 says so as a rule rather than as an
anecdote.

#### Also

- Traps 237 to 244 added, and **items 29 and 30 corrected**: both pointed at
  P23 and both are this program's, which is the P7-insertion off-by-one in the
  range Program~\ref{prog:P10}'s pass deliberately left unswept. Item 29's
  second owner was also wrong \dash{} mutual information is
  Program~\ref{prog:P31}'s, not P30's. Each was settled against the destination
  brief rather than by assuming the off-by-one.
- **The mandatory notation box is in section 3**: $\Var(X)$ against $D^{2}(X)$
  and $\Ex[X]$ against $M(X)$. Appendix~B's pointer was moved here by the P23
  pass on the strength of this program's brief, so the pointer now closes.
- Three cross-programme gates, all of Program~\ref{prog:P12}'s third kind
  \dash{} the same worked example continued: P21's population and its mean,
  P23's alarm rate and its positive predictive value, and F05's twelve
  committed probabilities.
- One value deliberately not emitted twice, and two emitted values cut because
  the frames quote the two ends of a sweep rather than its middle.

#### An overfull box, and clearing it made the cue ledger worse

Frame~1 quotes Program~\ref{prog:F13}'s unfinished sentence, so it carries
$\int x\,p(x)\,\mathrm{d}x$ inline \dash{} one unbreakable maths span with a
dash-bracketed clause either side of it. In Polish that gave a
$\num{12.0}$ pt hbox and in English nothing, which is
Program~\ref{prog:F06}'s finding exactly: an inline formula of any length is a
latent overfull box on a measure or an installation you are not looking at.
The recorded fix worked without a detour \dash{} **put it in a display** \dash{}
and it reads better, because the integral is the thing the frame is about.

**And the fix moved the cue ledger against itself.** The display lengthens
frame~1, so every break in the program after it shifts: the build came back
with the box gone, `main-pl` two pages longer, and its orphaned cues gone from
one to **three**. That is this file's random walk with a new cause \dash{}
previous instances were a trim or a lengthening aimed *at* a cue, and this was
a fix for an unrelated defect three hundred lines upstream. **Any edit near the
top of a program re-rolls every cue in it.**

Round two lengthened all four offending frames \dash{} 6, 24, 28 and 58, in
both editions \dash{} and all four builds came back clean. **Round three came
later and from the same cause**: the two displays that fixed CI's hbox added
two pages to `main-en` and put a cue back at frame 37, cleared by lengthening
that frame. Eleventh confirmation of Program~\ref{prog:F06}'s two-sided rule,
and it has still never failed \dash{} and the third time in one pass that an
edit made for something else re-rolled the cue ledger.
Every added paragraph earns its place: that the expectation's sum runs over the
sample space rather than over the distinct values, so an outcome repeating a
value counts twice; that the book keeps the variance as well as its root
because the variance is the one that **adds**, which is
Program~\ref{prog:P25}'s subject; that dividing a covariance by both spreads
cancels the units, so two correlations from unrelated pairs sit on one scale;
and that the Gumbel noise goes onto the $\ln p_i$ and never onto the $p_i$,
which is the half people misremember.

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P24.1 space-to-number | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P24.2 two-summaries | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P24.3 three-knobs | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All six at mermaid's wrap cap on the first render, at three ranks. Written
against the frames **above** them before rendering, which is
Program~\ref{prog:P22}'s rule, and this is the first pass in seven where the
last node of a three-rank chain needed no correction afterwards \dash{} because
the rule was applied while drawing rather than after a build.

Measured on the page in all four builds. Figures 1 and 2 both sit above the
question that follows them and neither answers it, which is the P04/P07 case
for the eleventh time: figure 1 carries what frames 1 to 10 state in full and
the question below asks whether linearity needs independence, which appears
nowhere in it; figure 2 carries the units-squared reading that frames 18 to 24
deliver and the question below asks for a Bernoulli's two summaries. Figure 3
sits in the closing frame with nothing after it.

| build | fig 1 / next question | fig 2 / next question | fig 3 |
|---|---|---|---|
| `main-en` | 914 / 915 | 925 / 925 | 935 |
| `main-pl` | 928 / 929 | 940 / 940 | 950 |
| `main-en-a4` | 769 / 769 | 777 / 778 | 786 |
| `main-pl-a4` | 777 / 777 | 786 / 786 | 794 |

#### CI could not say WHERE, an inference filled the gap, and the inference was wrong

This is the pass's most useful finding and it cost a cycle to get.

Both A4 builds failed on CI and neither trade build did: an over-budget hbox
of $\num{25.4}$ pt in `main-en-a4` and $\num{37.7}$ pt in `main-pl-a4`, on
source this container sets with zero. `checklog.py` reported **the sizes and
nothing else**, because Program~\ref{prog:P12}'s pass had taught it to name
the page or the file and line of every overfull **vbox** \dash{} for a reason
it stated plainly, that the two installations paginate differently so the
machine that must fix a box is usually not the one that saw it \dash{} and had
left the **hbox** half printing sizes alone. That is the reporting CI uses.

**So the gap was filled by inference, and the inference was good and wrong.**
Two A4 builds over budget and two trade builds clean says a line that is
unbreakable in *both* editions and only bites at 12 pt, which narrows it to
something the two files share character for character. That is
`\code{code/p24\_distributions.py}` run into the middle of a paragraph
\dash{} 26 characters, the longest script name in the book, and exactly
Program~\ref{prog:F08}'s and Program~\ref{prog:F11}'s recorded class. It was
moved to the start of its sentence, which is the recorded fix, and pushed.

**CI came back with $\num{37.7}$ pt again, to the tenth of a point** \dash{}
which is this file's own signal, arriving for the fourth time in this
repository, that a change did not reach what was measured. What was different
is that the same push had closed the reporting gap, so the tool named it:

> `37.7 pt too wide, source lines 345--347, in or after ./programs/pl/P24-distributions.tex`
> `[Policz ja dla dziesieciu liczb. Ich srednia to $20$, wiec]`

It is `$1, 3, 2, 1, 7, 7, 0, 8, 3, 6$` \dash{} **ten numbers inside one inline
maths span**. TeX does not break at a comma in maths mode, so that is a
thirty-character unbreakable run, and it is Program~\ref{prog:F05}'s and
Program~\ref{prog:P04}'s class rather than F08's. The recorded fix applied
without a detour: **put it in a display.** Both occurrences of the list went
into one, in both editions, which is also the form the same ten numbers
already use where the population is first printed \dash{} so the fix makes
the program internally consistent as well as buildable.

The `\code{}` move is kept. It is a real latent box by the recorded rule and
it cost nothing; it simply was not this one.

**Three things worth carrying, and the third is the general one.**

- **A diagnostic that is only ever read on the other machine has to be as
  complete as the one you read on your own.** The vbox half was completed the
  moment it cost a cycle. The hbox half was not, because on this container the
  location is a `grep` away and the gap never showed.
- **An identical measurement after a change means the change missed**, and the
  second reading of that signal is nearly always the right one: not *the fix
  was too small* but *the fix did not reach*. Here it was neither the constant
  nor the scope \dash{} it was the wrong line.
- **Inference from the shape of the evidence is not measurement, and it reads
  exactly like it.** The argument from two-failing-two-clean was sound, it
  named a real defect of the right class in the right file, and it was still
  not the cause. What settled it was one line of tool output. **Close the
  reporting gap before spending a cycle on the inference it invites** \dash{}
  in this pass both happened to go in the same push, which is the only reason
  it cost one cycle rather than three.

#### The index's overfull vbox, retired at the mechanism rather than tuned

`main-en-a4` also carried a $\num{1.0}$ pt overfull vbox in the index, and it
survived every fix above \dash{} **reported as $\num{0.98073}$ pt on three
consecutive heads**, to the ten-thousandth of a point, across edits that added
and then removed two pages of body text. That invariance is the first useful
half: the index starts on a fresh page and its entries did not change, so its
residual does not move when the body does. It was the one pagination number in
this book that could be swept as a single variable, and every earlier pass
that tried had been fighting body-text noise as well.

**Swept once, it failed in the recorded direction.** Raising `theindex`'s
`\parskip` shrink from $1$ to $\num{1.5}$ pt \dash{} the knob five passes had
used \dash{} took this container from **no complaint at all to
$\num{2.28874}$ pt**, because the extra shrink let the balancer target a
smaller height, fit the index into one page fewer, and hand the last page
more. That is Program~\ref{prog:P19}'s non-monotonicity arriving from the
other machine, and it is the fifth demonstration that **no single value of
that constant serves both installations.**

**And the knob recorded for it one commit earlier does not exist.** The note
called `\multicolovershoot` \enquote{the bounded knob P19's pass went looking
for}. Asked properly \dash{} which is what that same note said to do \dash{}
it is a compensating pair: multicol adds it to `\splittopskip` while
*splitting* and subtracts exactly the same amount while *balancing*, so its
net effect on the balanced last page is zero. Its sign is the opposite of its
name, too. pdftex, asked in five lines: a `\vbox to 20pt` round a 25 pt rule
is $\num{5.0}$ pt overfull with no shrink, $\num{2.0}$ pt with `minus 3pt`,
and $\num{8.0}$ pt with `minus -3pt`. Negative shrink makes an overfull box
worse.

**So the fix is structural, it is three tokens, and it retires the whole
class.** Reading multicol's own `\@namedef{multicols*}`, the starred form is
the unstarred one with `\balance@columns@out` redefined to ship the final page
through the **ordinary** column output routine. The balancing `\vbox to` never
happens, so the complaint has no mechanism left rather than a wider tolerance
\dash{} which matters, because that box is the one multicol pins `\vfuzz\z@`
for, and `\maxbalancingoverflow` runs afterwards and only decides whether to
log \enquote{Balanced column too large}. `imakeidx` opens the environment
itself and offers no hook, but `\balance@columns@out` is read at
`\end{multicols}`, so setting it in the body is enough and it is local.

It is also what an index looks like in print: the last page's first column
runs to the foot and the second ends where the entries end. `\raggedcolumns`
stays, because `\ifshr@nking` is read by `\multi@column@out` as well as by the
balancer, so it still governs the page that is now doing the work. Locally the
change costs nothing \dash{} same page counts, same multiset, same ledgers.

**The rule this earns is one this file already had, paid for twice in one
pass.** The `\code{}` inference was written from the shape of the evidence and
was wrong; the `\multicolovershoot` note was written from the shape of the
source and was wrong. Both were corrected by an instrument costing
seconds \dash{} one line of tool output, and a five-line file put to TeX.
**A reading of a mechanism is a hypothesis, and this book's own rule is that a
hypothesis stays labelled as judgement until it is run.** That applies to the
comments in `preamble.tex` exactly as it applies to the frames \dash{} and it
is worth noticing that both wrong readings were confident, specific, and of
the right general class.

#### Layout, and the ledgers

The multiset came back element for element to the baseline in all four builds
\dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull vboxes, no
stranded openers, no stranded headings and **no orphaned cues** after the two
rounds above. **One orphan tail added, in `main-pl`**: 23, 28, 20, 21 against
the pre-P24 23, 27, 20, 21.

Pages 1059 / 1076 / 893 / 901, from 1027 / 1043 / 864 / 875 \dash{} thirty-two
and thirty-three in the trade format, which is what a sixty-four-frame program
costs.

Frame numbers mapped after writing and again after the elicitation
conversions: sections landed at
`1--10 / 11--17 / 18--25 / 26--36 / 37--48 / 49--64`.

### Program P25 pass, August 2026

**Fifty-four teaching frames, fifty-six printed, both editions**, against a
brief that projected fifty-five. Six sections: two things added, the average of
many, the shape and where the theorem is silent, what an evaluation run costs,
why attention divides by a square root, and why a run can diverge before it
starts.

**It is the first estimate in nineteen programs to hold.** Seventeen came in
under and Program~\ref{prog:P24} came in over. Worth one hypothesis, labelled
as one because $n = 1$: P25's brief is among the five the curriculum review
amended \dash{} it added the initialisation section by name \dash{} so it is
the only brief in the manifest written after somebody had looked at what its
neighbours would spend. Every other estimate predates its own neighbours,
which is the reason this file already gives for the seventeen.

#### The ledger that said no experiment had been run had been false for five programs

This is the pass's most valuable finding and it is not about P25.

`notes/01-curriculum.md` §17 said \enquote{Ten candidate experiments.
\textbf{None has been run.}} and this file repeated it in *Non-negotiable
conventions*. **Experiment E6 was run in the P20 pass**, which has its own
heading a few sections above \dash{} *Experiment E6, and the asymmetry that
made it worth running* \dash{} reporting measured step counts against predicted
ones. So the sentence had been false for five programs, in the two documents
the next author reads first.

It is the recorded class exactly: **a claim about the book that nothing derives
from anything.** This file forbids stating a count of occurrences because a
tally decays silently, and the experiment ledger was a tally in prose sitting
two paragraphs from the rule. The table now carries a **Status column** naming
the pass that ran each experiment, with the instruction to fill it in that pass
and never to restate a total.

**Three more rows say \enquote{see the note below} rather than an answer**, and
that is the honest form. Program~\ref{prog:P02} measured the overflow cliff per
format and what a non-maximal pivot costs (E1); Program~\ref{prog:P05} swept
the cosine spread over $d = 2, 3, 10, 100, 768, 4096$ and the concentration
towards orthogonality (E3, whose specification is that sweep almost word for
word); Program~\ref{prog:P16} counted forward against reverse multiplications
exactly and derived the checkpointing peak (E5). Each looks like the experiment
beside it and **no pass claimed one**, so whether the specification is met is a
reading job on three merged programs and not an inference to make from a table.
E5 is the clearest case for \enquote{no}: it asks for time and peak memory
measured on a machine, and P16 deliberately counted operations instead.

**And E9's owner had moved without the table.** The review put the derivation of
the scaling in P25 and the table still said P32. E9 as specified \dash{} random
vectors, head sizes, spread and entropy \dash{} is P25's and was run here; what
is left for P32 is the same measurement on an assembled architecture, which is
what this program's own closing frames say. Corrected in the table and in the
manifest brief, which had said the reader \enquote{derives it here and measures
it in P32}.

#### E9, run: the headline

Without the division, at $d_k = \val{p25.e9.d.hi}$: spread
$\val{p25.e9.raw.sd.512}$, softmax entropy $\val{p25.e9.raw.ent.512}$ nats
against a maximum of $\val{p25.e9.maxent}$, and one key of
$\val{p25.e9.keys}$ taking $\val{p25.e9.raw.top.512}$ per cent of the weight.
With it: spread $\val{p25.e9.scaled.sd.512}$ at every head size and the entropy
between $\val{p25.e9.scaled.ent.8}$ and $\val{p25.e9.scaled.ent.512}$ across a
sixty-fourfold change in $d_k$.

**Nothing moves** is the whole claim, and it is now measured rather than
argued. Program~\ref{prog:P18}'s Jacobian diagonal then turns it into a
gradient: $\val{p25.e9.resp.raw}$ raw against $\val{p25.e9.resp.scaled}$
scaled, a factor of $\val{p25.e9.resp.ratio}$. \enquote{The gradient dies} is
$p(1-p)$ evaluated at a $p$ the architecture drove to one.

The derivation costs four lines and no limit theorem: the script enumerates
every sign vector at $d = 1$ to $5$ and gets $\Var(q \cdot k) = d_k$ exactly.
And it is **gated against Program~\ref{prog:P05}'s four committed cosine
spreads**, which measured the same theorem at the normalised scaling three
parts earlier and reproduces to within $\val{p25.p05.worst.pct}$ per cent
\dash{} so the attention scaling is a Part III measurement read at the other
scaling rather than a new claim.

#### Three assertions refuted their own drafts, for the fourteenth pass running

1. `RATIO_3 > 1.5` for how far the Gaussian overstates the tail at three
   spreads. It is $\val{p25.tail.ratio3}$.
2. **\enquote{The ratio is above one everywhere}** \dash{} false at one spread,
   where it is $\val{p25.tail.ratio1}$: the Gaussian slightly *understates*
   there. **The failure is the section.** The Gaussian is not uniformly wrong in
   one direction; it is excellent in the middle, crosses, and runs away outside
   \dash{} $\val{p25.tail.ratio1}$, $\val{p25.tail.ratio3}$ and
   $\val{p25.tail.ratio5}$ at one, three and five spreads, and at six the truth
   is exactly zero while the Gaussian still says $\val{p25.tail.gauss6}$.
3. An eight-decimal format printed the five-spread tail as `0.00000000`, so the
   reproduce-from-the-page check divided by zero. Three significant figures
   instead \dash{} which is the recorded rule (divide the two numbers as the
   page prints them) failing inside the guard written to enforce it.

And `p25.tail.ratio3` was first emitted at zero decimals, printing `1` for a
value of $\val{p25.tail.ratio3}$. **A ratio table needs its precision chosen
per row**: these rows span three orders of magnitude and no single format
serves them, so the script carries a per-$z$ digit map.

#### The translator rule is symmetric, and this is the first time it broke the other way

Every recorded instance of the ordered-token class has been Polish spelling a
digit as a word. Here it was the reverse, twice: the English quiz answer says
*a factor of two costs a factor of four* in words and the Polish had `$2$` and
`$4$`; the English trapbox says *differ by a factor of two here* and the Polish
had `$2$`. C4, C8 and C12 all fired.

So the rule in *Two editions* is not only \enquote{a digit stays a digit} but
its mirror: **a word stays a word.** The instinct to reach for the numeral is
as real as the instinct to reach for the word, and the ordered checks catch
both.

#### Also

- C10 fired on `0.9` and `0.1` inside a `\sqrt{}` in a test exercise, **in both
  editions** \dash{} the English owed the wrapping as much as the Polish did,
  which is the half of C10 that is easy to forget.
- Seventeen values went unreferenced. Sixteen were cut on
  Program~\ref{prog:F11}'s finding \dash{} the E9 assertions still sweep all
  five head sizes and only the three the tables print are emitted \dash{} and
  **one earned a sentence**: the trial count, because a book's first experiment
  should be reproducible from its own page.
- Traps 245 to 252 added, including the one the issue names.
- The listing was extracted from `main-en.pdf` p957 and run as a REPL would: it
  prints `(22.7, 22.6)` and `1.0`, which is what the page prints and what the
  frames beside it claim.
- The issue's *No Quiz (Foundation-only)* checkbox is stale in the way P04, P14
  and P24 each found it stale. P25 has one, like all twenty-eight before it.

#### Layout, and one round of lengthening cleared five cues

The first build came back with **five orphaned cues** \dash{} one in `main-en`,
three in `main-pl`, one in `main-en-a4` \dash{} across four frames. All four
were lengthened in both editions in **one round**, and all four builds came
back clean. Twelfth confirmation of Program~\ref{prog:F06}'s two-sided rule,
and it has still never failed.

Every added paragraph earns its place, and one of them is the best sentence in
its section: $p(1-p)$ is largest at a half and falls away towards both ends, so
**a model scoring near chance carries the widest interval it can have and one
scoring near the ceiling carries a narrow one** \dash{} the same item count
buys more precision at the top of a benchmark than in the middle of it. The
other three say why the Jacobian's *diagonal* is the entry to reason about
(the off-diagonal terms move weight between keys, and a row that has given
everything to one key has none to move); that the fan-in belongs to the
architecture while the two variances belong to the initialiser, which is why
the design question has one answer rather than a family; and that the
per-layer factor is one number with the depth as its exponent, so the tolerance
on it tightens as a network gets deeper without anybody changing it.

The overfull multiset came back element for element to the baseline in all four
builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull vboxes, no
stranded openers and no stranded headings. **Two orphan tails added, both in
`main-en`**: 25, 28, 20, 21 against the pre-P25 23, 28, 20, 21.

Pages 1090 / 1104 / 913 / 925, from 1059 / 1076 / 893 / 901.

#### Rule 2, written against the frames above and then measured

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P25.1 one-rate | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P25.2 signal-depth | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P25.3 tail-is-silent | 657 / 645 | 5.98 | 6.71 | 6.84 | 7.62 | 7.76 |

All six at mermaid's wrap cap or within twelve points of it on the first
render, at three ranks. Written against the frames **above** them before
rendering, which is Program~\ref{prog:P22}'s rule, and for the second pass
running the last node of a three-rank chain needed no correction afterwards.

Measured on the page: all three sit on the same page as the question that
follows them, in all four builds \dash{} `main-en` 961, 963, 965; `main-pl`
976, 978, 980; `main-en-a4` 806, 808, 809; `main-pl-a4` 814, 816, 818 \dash{}
and none answers it. P25.1 carries the identity three sections have delivered
and the question below asks what a $\relu$ passes on, which appears nowhere in
it; P25.2 carries the geometric sequence its own frame states and the question
below asks for a number at four per layer, which needs the squaring the figure
never mentions; P25.3 is in the closing frame with nothing after it.

### Program P26 pass, August 2026

**Forty-six teaching frames, forty-eight printed, both editions**, against a
brief that projected fifty-five. Six sections: two ways of being wrong, the
$n-1$ and what it does not fix, the parameter that makes the data least
surprising, training a language model is maximum likelihood, a penalty is the
logarithm of a prior, and the score.

Nineteenth program under its brief's estimate and the largest shortfall since
Program~\ref{prog:P18}, for the F07/P06 reason at its strongest: **five
written programs each deliver one of this program's ingredients and each says
so.** Program~\ref{prog:P21} owns unbiasedness outright \dash{} the
definition, the exact proof over every subset, the trapbox \dash{} so P26 may
not re-teach it and owes the *second* axis instead. Program~\ref{prog:P18}
gives cross-entropy a definitional frame and says in as many words that the
justification is here. Program~\ref{prog:P20} owns weight decay and measured
what its $\lambda$ does. Program~\ref{prog:P19} owns Jensen including the
concave case. Programs~\ref{prog:F02} and \ref{prog:F03} own the loss and the
sequence probability. So this program derives where its predecessors
demonstrated, which is a better possession and a shorter one.

#### Program P21 deferred two things here and only one was known about

The manifest brief names one debt: Program~\ref{prog:P18}'s cross-entropy.
Reading Program~\ref{prog:P21} before writing turned up a **second**, in its
section 8: the score-function and reparameterised estimators are \enquote{a
line of algebra that Programs P24 and P26 are better placed to give}.
**Program~\ref{prog:P24} did not give it**, and nothing in this repository
recorded that it had not.

It costs four lines here rather than a section, because it is the same object
maximum likelihood sets to zero: define the score, show its expectation is
exactly zero, and $\nabla\Ex[f] = \Ex[f\,s]$ follows from
$\nabla p = p\nabla\ln p$. Both halves are checked exactly over fractions at
nine rates and three functions. So §6 closes the deferral P21 wrote down and
the one nobody had.

**The generalisable half: a program's forward debts are not all in the
manifest.** The manifest carries the *declared* ones; a deferral written into
a frame's prose is invisible to `deps` and to every gate. Reading the
neighbour is what found it, and it is the fifteenth pass that discipline has
paid for.

#### Two findings that are the program's own

**The unbiased estimator is not the best one, and it is exact.** On a
four-number population with samples of $\val{p26.draw.n}$, the mean squared
error splits as $\text{bias}^{2} + \Var$ at all twenty-one shrinkages tried,
over fractions \dash{} and shrinking the sample mean by
$\val{p26.shrink.c}$ beats it by $\val{p26.shrink.gain.pct}$ per cent,
$\val{p26.mse.shrunk}$ against $\val{p26.mse.unbiased}$. The honest caveat is
in the frame: the optimal shrinkage depends on the unknown mean, so it is a
finding rather than a recipe \dash{} and it is why every regulariser in the
book is a bias taken on purpose, which §5 then prices.

**The $n-1$ corrects the variance and leaves the standard deviation short.**
Enumerated at $n = 2$ to $5$, the $n$-denominator sample variance averages
exactly $\frac{n-1}{n}$ of the population's and the $(n-1)$ one averages it
exactly. Then the half nobody says: a square root is concave, so
Program~\ref{prog:P19}'s Jensen makes the corrected $s$ **still biased**,
short by $\val{p26.sd.short.2}$ per cent at $n = 2$ and
$\val{p26.sd.short.5}$ per cent at $n = 5$ \dash{} which is the sample size
people actually report a spread over, and the bias runs in the direction that
makes results look more reproducible than they are.

#### The payoff, and a gate three programs long

Product of token probabilities, logarithm, negate, divide by the count: that
is Program~\ref{prog:P18}'s cross-entropy character for character, so
training a language model is maximum likelihood and was never anything else.

The gate is Program~\ref{prog:P12}'s third kind \dash{} the same worked
example continued \dash{} run in **both directions**.
Program~\ref{prog:F02}'s $\val{p26.f02.loss}$ nats and
Program~\ref{prog:F03}'s $\val{p26.f03.tokens}$-token sequence reproduce each
other: forwards to F03's committed exponent to the printed digit, backwards
to $\val{p26.back.loss}$ nats. **The backward tolerance is derived rather
than chosen** \dash{} it is exactly what rounding that exponent to two
decimals can account for, and nothing wider, which is the rule
Programs~\ref{prog:F11}, \ref{prog:P15}, \ref{prog:P20} and \ref{prog:P21}
each paid for.

And $\lambda = 1/\tau^{2}$ is matched **on the gradients
Program~\ref{prog:P20} actually adds** rather than on a formula, at five
values of $w$, because the correspondence turns on whether the penalty
carries a half \dash{} which is exactly the trap Program~\ref{prog:F04}
recorded about momentum. Its $\lambda = \val{p26.p20.lambda}$ is the claim
that every weight is Gaussian of width $\val{p26.prior.tau}$, and that is
checkable against the trained weights rather than a knob to turn.

#### The build named the line, and the recorded habit read it right

The first build exited $2$ with `main-pl` and `main-pl-a4` at **exactly** the
page counts they had before P26 existed. That is this file's own tell
\dash{} an unchanged page count is a failed build \dash{} and it was right:
`make` stopped at the English target, so the Polish ones never ran.

What ended it in one look rather than three was the hbox reporting the P24
pass added. It named the file, the source lines and the offending text: a
$\num{22.7}$ pt box from `\ln\bigl(\frac{\ldots}{\ldots}\bigr)` set inline in
a further-problem answer, which is Program~\ref{prog:F06}'s rule exactly. The
recorded fix applied without a detour \dash{} **put it in a display** \dash{}
and the multiset came back to the baseline.

**That is the reporting gap closing and paying for itself one program
later.** The P24 pass closed it after an inference filled it and was wrong;
here there was no inference to make.

#### Layout, and one round of lengthening cleared three cues

Three orphaned cues \dash{} two in `main-pl`, one in `main-pl-a4`, across
frames 5, 11 and 26 \dash{} cleared in **one round** by lengthening, in both
editions. Thirteenth confirmation of Program~\ref{prog:F06}'s two-sided rule
and it has still never failed.

Every added paragraph earns its place: that the *squared* distance is what
makes the two axes add rather than interact, since an absolute error has no
decomposition at all; that the $n-1$ argument depends on how the estimator
was built and not on which numbers were drawn, which is why the fix can be a
fixed factor; and that of the three steps turning a likelihood into a loss
only the negation is convention, because every optimiser in
Program~\ref{prog:P20} was written to go downhill.

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, no stranded openers and no stranded headings. **Two orphan tails
added**, one in `main-en` and one in `main-pl`: 26, 29, 20, 21 against the
pre-P26 25, 28, 20, 21.

Pages 1116 / 1132 / 935 / 945, from 1090 / 1104 / 913 / 925.

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P26.1 two-axes | 657 / 646 | 5.98 | 6.71 | 6.83 | 7.62 | 7.75 |
| P26.2 one-quantity | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P26.3 prior-is-penalty | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P26.4 set-it-to-zero | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All eight at or within eleven points of mermaid's wrap cap on the first
render, at three ranks. Written against the frames **above** them before
rendering, which is Program~\ref{prog:P22}'s rule, and for the third pass
running the last node of a three-rank chain needed no correction afterwards.

Measured on the page in all four builds. P26.1 sits on the same page as the
question that follows it and answers nothing in it, which is the P04/P07 case
for the twelfth time: it carries the two axes and the decomposition that
frames 1--5 state in full, and the question below asks what goes wrong when
you divide by $n$. P26.2 and P26.3 are the same case one section on; P26.4 is
in the closing frame with nothing after it.

#### Also

- Traps 253 to 260 added to `notes/02`.
- **Elicitation 52%**, the second highest outside Part I after
  Program~\ref{prog:P23}'s 53%, and designed in from the frame plan rather
  than retrofitted \dash{} which is Program~\ref{prog:P23}'s lesson applied
  before the remap rather than after it, so it cost no renumbering.
- Parity took four rounds and every failure was a recorded class: a Polish
  word inside `\mathrm{}` where `\text{}` is what C8 normalises (**use
  `\text{}` for a translated word in maths, never `\mathrm{}`**, which names
  an operator and must not be translated); `$n-1$` against `$(n-1)$` in a
  table label and again in a summary item; and one
  `Program~\ref{...}'s <value>` inversion in a summary item.
- Two emitted values were cut on Program~\ref{prog:F11}'s finding: the frame
  writes \emph{twenty trials give seven successes} in words, and quoting them
  as values would start a clause with a digit, which is
  Program~\ref{prog:F02}'s rule.
- The listing was extracted from `main-en.pdf` p979 and run as a REPL would:
  it prints `(False, True)` and `(1.4142, 1.8708)`, which is what the page
  prints and what the frames beside it claim.
- The issue's *No Quiz (Foundation-only)* checkbox is stale in the way P04,
  P14, P24 and P25 each found it stale.

### Program P27 pass, August 2026

**Thirty-nine teaching frames, forty-one printed, both editions**, against a
brief that projected sixty. Six sections: what one point is, an interval with
no formula, they saw the same prompts, what a p-value says, forty models on
one leaderboard, and what you can now check.

Twentieth program under its brief's estimate, and the shortfall has a cause
this file has not recorded before. The nineteen previous ones came in short
because a neighbour had spent the *material*, or supplied the *machinery*, or
because the subject was small. Here **two of the brief's seven itemised
deliverables were already on the page, by name**:

- \enquote{the standard error of a proportion} is Program~\ref{prog:P25} §4,
  with the interval, the four-times rule and $p(1-p)$ widest at a half;
- \enquote{a power calculation answering how many evaluation items are needed
  to detect a one-point difference} is the same section's
  $\val{p27.n.rho00}$ items per model.

So the reading before drafting was not \enquote{what is left of the subject}
but **\enquote{which lines of the brief have been delivered}**, which is a
cheaper question and a sharper one. It is worth doing that way for every
remaining program whose brief lists its contents.

#### The headline is Program P25's own number, done right

P25's $\val{p27.n.rho00}$ assumes the two evaluations are independent. They
are not: A and B ran on the same prompts. P25's *own* section 1 carries the
term that fixes it \dash{} $\Var(X-Y) = \Var X + \Var Y - 2\Cov(X,Y)$ \dash{}
and it used only the plus half. Using the minus half, the item count carries a
factor of exactly $1-\rho$:

| $\rho$ | items per model |
|---|---|
| $0$ | $\val{p27.n.rho00}$ |
| $\num{0.5}$ | $\val{p27.n.rho50}$ |
| $\num{0.8}$ | $\val{p27.n.rho80}$ |
| $\num{0.9}$ | $\val{p27.n.rho90}$ |

**The gate is that at $\rho = 0$ the paired formula must return P25's own
committed figure**, so the two programs cannot come apart about a comparison
they jointly describe. The script asserts the factor at four accuracies and
three gap sizes rather than the four numbers, because the factor is the result.

And the exact form needs no variance at all. Only the **discordant** items
\dash{} where exactly one model is right \dash{} carry the difference;
$\val{p27.concord}$ concordant ones cancel exactly. Under \enquote{equally
good} those items are fair coin flips, so the test is
Program~\ref{prog:P12}'s binomial coefficient over integers: exact,
machine-independent, and it lets **the p-value arrive as a coin count two
sections before it arrives as a word.**

The worked answer is the program's reason for existing. A published gap of
$\val{p27.gap.pts}$ points on $\val{p27.items}$ items is
$\val{p27.gap.items}$ item; the exact test gives $\val{p27.p.exact}$; and the
gap would have to reach $\val{p27.net.needed.pts}$ points \dash{} twelve times
what was published \dash{} before this evaluation set could distinguish the
two models at all.

> **Corrected after merge, by the next program's assertion.** The first
> version of this section used $30$ discordant items with a lead of $1$, which
> **cannot happen**: the lead is a difference of two counts adding to the
> discordant total, so the two have the same parity. It is the same parity
> fact this program's own script documents as a formula trap two hundred lines
> above, applied to the formula and not to the data. Program~\ref{prog:P28}
> asserted it while continuing the example and the build stopped.
>
> **The corrected section is better rather than merely legal.** On an odd
> count a tie is impossible, so somebody must be ahead, the smallest available
> lead is one, and that is what was observed \dash{} so the p-value is
> \textbf{exactly 1}, and the published difference is the least informative
> outcome the arithmetic permits. The threshold moved from $\num{5.5}$ to
> $\val{p27.net.needed.pts}$ points.
>
> The generalisable half is narrow and worth having: **a parity constraint on
> a formula is usually also a constraint on the data**, and recording it in
> one place does not enforce it in the other.

#### Every assertion passed on the first run, and that was the warning

This is the pass's most useful finding and it is new. Fourteen passes have
recorded that **a failing assertion is the finding**. None had recorded what
to do when none fails, and the answer is: **read the formulas against the
numbers anyway, because a script whose assertions all pass has told you only
that it is self-consistent.** Three defects were sitting in it.

- **A parity trap hid a wrong argument.** The exact test was called with
  $2 \times \text{net}$ where the net is the statistic itself. It gives the
  same number, because $2c - m$ has the parity of $m$ so the answers for
  `net` and `net + 1` coincide at even $m$ \dash{} and it would be wrong at
  odd $m$. That is Program~\ref{prog:P17}'s shape exactly: a formula whose two
  readings agree numerically is invisible until the day they do not.
- **The threshold search inherited the doubling**, and reported
  $6$ items / $\num{3.0}$ points where the answer is
  $\val{p27.net.needed}$ items / $\val{p27.net.needed.pts}$ points. Neither
  number was right, and the corrected one is a far better sentence.
- **Two ratios did not reproduce from the page**, which is the class F04, F05,
  P07, P12 and P23 have each paid for.

So the pass added a `reproduces()` helper: it formats the operands exactly as
the page will, applies the operation to *those*, and compares the printed
forms. **It fired on its first run** \dash{} the only way to know a new check
is looking at anything \dash{} and the answer it gave was that no single
decimal is both true and reproducible for the interval-to-gap ratio: the exact
value is $\num{12.53}$ and the page's own two numbers divide to $\num{12.6}$.
Program~\ref{prog:F05}'s recorded fix applied: **state a bound**, and assert
that both the exact and the printed ratio clear it. The Bonferroni cost needed
the other half of the same rule \dash{} $z$ is emitted at three decimals
rather than two, because at two the page prints $\num{3.23}$ and
$(\num{3.23}/\num{1.96})^{2}$ is $\num{2.72}$ against a true
$\val{p27.bonf.cost}$.

#### The transcript carried the wrong argument after the script was fixed

`net = 2` survived in the listing, printing the right number for the wrong
reason, and a reader comparing it against frames that say one item would have
found the contradiction. Nothing catches this: `make verify` proves the file
matches the script that wrote it, and the script wrote exactly what it
computed. It is Program~\ref{prog:P16}'s finding \dash{} a generated,
committed, drift-gated transcript can still disagree with the prose beside it
\dash{} and the only instrument is reading the listing against the frames.

The listing was then extracted from `main-en.pdf` p1014 and run: it prints
`0.8555` and `0.1445`, which is what the page prints.

#### The diagram manifest, seventh recurrence, and a new cause

A $\num{16.5}$ pt box in `main-en`, and it was mine: `\mermaidfig` writes
`\texttt{<key>.mmd} --- <third argument>` itself, and **all eight calls put
the key and `.mmd` into the third argument as well**, so the manifest line
carried the key twice. Every previous instance of this column overflowing was
long copy; this one was a duplicated key, and the fix is a rule rather than a
trim:

> **The third argument is manifest copy only.** The macro supplies the key,
> the extension and the dashes. Keep the copy short \dash{} shorter in Polish
> \dash{} and check `len(key) + 9 + len(copy) < 48`, which is
> Program~\ref{prog:P14}'s budget. P27's eight calls were measured against it
> by hand and land between 33 and 43.

**A book-wide check was attempted and is NOT in the tree**, which is worth
recording rather than quietly dropping. `\mermaidfig`'s caption argument spans
lines and contains braces, so a regex that looks like it parses the three
arguments silently captures the caption as the copy and reports most of the
book over budget. The measurement it produced was wrong and was discarded.
A real check needs a brace-matching parser for the macro's arguments \dash{}
which `check_structure.py` could carry \dash{} and it is a job of its own; a
check nobody has watched fire is exactly what this file says not to add.

`MAKE_EXIT 2` while the harness reported exit 0, with three page counts
unmoved: the recorded tell fired for the fourth time and the recorded habit
caught it.

#### `notes/02` §4 carried three stale pointers, and a sweep is only as wide as its section

The P7-insertion off-by-one again, in the file this document tells everybody
to re-derive owners from \dash{} but in **§4, the exclusions table**, where
every previous sweep looked at §3, the trap list. Each was settled against the
destination brief rather than by assuming the off-by-one:

- \enquote{P26 teaches bootstrap and permutation first} \dash{} P26 is
  estimation; **P27** owns the bootstrap, and its exact test on discordant
  pairs is a permutation argument on the one design that matters.
- \enquote{P25 does maximum likelihood as an objective} \dash{} that is
  **P26**; P25 is the CLT.
- \enquote{Inference and Bayes (P26--P27)} \dash{} the block is
  **P27--P28**.

And one clause pointed at something **nobody has promised**: \enquote{the
classical tests get a table showing which resampling procedure replaces
which}. No brief undertakes it. Softened on the F04/F08/P04 precedent, and the
entry now says in as many words that the table was promised there and nowhere
else \dash{} rather than naming a program that has not agreed to it.

**The generalisable half: a sweep is as wide as the section somebody thought
to look at.** Five passes have corrected owners in `notes/02` §3 and not one
opened §4.

#### Layout, and one round of lengthening cleared five cues

The first clean build came back with **five orphaned cues** \dash{} two in
`main-en`, two in `main-en-a4`, one in `main-pl-a4` \dash{} across four
frames. All four were lengthened in both editions in **one round**, and all
four builds came back clean. Fourteenth confirmation of
Program~\ref{prog:F06}'s two-sided rule, and it has still never failed.

Every added paragraph earns its place. The best of them says what
\enquote{equally good} is being taken to mean, because the exactness of the
test rests on it: not that the two models are the same model, but that on an
item where they disagree either could have been the one to get it \dash{}
which is what makes each discordant item a coin flip. The others say that the
threshold question is the same sum run upwards rather than once, so asking
where the bar is costs nothing; that the prior in the false-discovery
calculation is a count somebody could go and make (how many of last year's
proposed changes helped) rather than a philosophical position; and that of the
three design routes out of an unresolvable comparison, pairing is free, items
cost quadratically in precision, and a better measurement is the only one with
no ceiling and the only one nobody budgets for.

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, no stranded openers and no stranded headings. **Two orphan tails
added, both in `main-en`**: 28, 29, 20, 21 against the pre-P27 26, 29, 20, 21.

Pages 1146 / 1158 / 955 / 967, from 1116 / 1132 / 935 / 945.

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P27.1 one-item | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P27.2 what-to-resample | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P27.3 same-prompts | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |
| P27.4 winner-is-noise | 657 / 657 | 5.98 | 6.71 | 6.71 | 7.62 | 7.62 |

All eight at mermaid's wrap cap on the first render, at three ranks. Written
against the frames **above** them before rendering, which is
Program~\ref{prog:P22}'s rule, and for the fourth pass running the last node
of a three-rank chain needed no correction afterwards.

The one that needed care is P27.3, which sits in the frame that ends by asking
which of three groups of items carries the difference. Its nodes carry the
covariance, the shared prompts and the factor of $1-\rho$, and mention neither
concordant nor discordant items \dash{} so it is the P04/P07 case for the
thirteenth time: a figure the reader is meant to *apply* belongs above the
question.

#### Also

- Traps 261 to 272 added to `notes/02`.
- **Elicitation 53%**, joint highest outside Part I with
  Program~\ref{prog:P23} and designed in from the frame plan, so it cost no
  renumbering \dash{} which is the second pass running that P23's lesson has
  been applied before the remap rather than after it.
- Parity took three rounds and every failure was the recorded word-order
  class: `Program~\ref{...}'s <maths>` against `<maths> z Programu~\ref{...}`,
  twice in a summary item and once in a further-problem answer. That is where
  P13, P15, P19 and P26 each hit it too, and it is worth checking summary
  items first.
- The one C7 warning was five values the frames do not quote. Four emissions
  were cut on Program~\ref{prog:F11}'s finding; **one earned a sentence**
  \dash{} the leaderboard's accuracy, because naming it makes the standard
  error beside it reproducible from the page.
- The issue's *No Quiz (Foundation-only)* checkbox is stale in the way P04,
  P14, P24, P25 and P26 each found it stale.
- Frame numbers mapped after writing: sections landed at
  `1--6 / 7--14 / 15--22 / 23--30 / 31--36 / 37--39`.

### Program P28 pass, August 2026 --- Part VII is complete

**Thirty-seven teaching frames, thirty-nine printed, both editions**, against a
brief that projected fifty. Six sections: a distribution on the parameter, the
update is adding counts, a credible interval, the probability that B is better,
routing under uncertainty, and a judge model's stated probability.

Twenty-first program under its brief's estimate, and this one is the P10/P13
kind: the ground was unspent and the neighbours supplied the *machinery*.
Program~\ref{prog:P23} owns Bayes and, crucially, the **odds form** \dash{}
§1 puts the same theorem on a continuum and §6 uses the odds form again
unchanged. Program~\ref{prog:P26} owns the MAP and says in as many words that
it throws the posterior away, so this program owes the **distribution**, never
the arithmetic that finds its mode. Program~\ref{prog:P27} hands
\enquote{the probability that B is better} over by name and had already built
one side of the credible/confidence contrast. So nothing had to be motivated
and nothing had to be re-derived, and what is left is short: no new object is
defined anywhere in the program.

**All five of the brief's payoffs are delivered**, which is the first time
since P25 that a brief's checklist ticked off complete \dash{} and it was read
as a checklist before drafting, which is Program~\ref{prog:P27}'s lesson
applied rather than restated.

#### The elicitation rate is 54%, the highest outside Part I, and it cost nothing

Above Program~\ref{prog:P23}'s and Program~\ref{prog:P27}'s 53%, with **no
conversions at all**: the frame plan was written that way, so there was no
retrofit and therefore no renumbering. That is now three passes running
(P26, P27, P28) demonstrating the same thing, and it is worth stating as a
finding rather than a run of luck: **designing the rate in is free, and
raising it afterwards is not.** Program~\ref{prog:P24} paid nine frames for ten
points and Program~\ref{prog:P23} paid two frames for twenty.

#### P27's threshold was a value its own data cannot take, and the parity fix did not reach it

Program~\ref{prog:P27}'s pass note already records one parity defect, caught by
this program's assertion while continuing the worked example: thirty discordant
items with a lead of one is impossible, because the lead is a difference of two
counts adding to the total and so carries its parity. That was fixed in the
**data**. It was not fixed in the **threshold search**, which stepped by one:

```python
NEED = 1
while two_sided_exact(DISCORDANT, NEED) >= ALPHA_LATER:
    NEED += 1
```

On thirty-one discordant items that answers $12$ \dash{} and a net of twelve
cannot occur, because $\lvert 2c - 31\rvert$ is odd for every integer $c$. The
smallest **achievable** net clearing the bar is thirteen, so the threshold is
$\num{6.5}$ points rather than $\num{6.0}$, and the published gap is thirteen
times under it rather than twelve. The search now steps by two from the
observed net and asserts the parity it inherits.

**The finding is that fixing an instance is not fixing the class, and the
evidence was twenty lines above the defect.** The same script's
most-likely-outcome check already iterates `range(3, DISCORDANT + 1, 2)`,
which is the parity written down correctly; the loop below it ignored it. A
constraint recorded at one use is not enforced at the next, and neither
Program~\ref{prog:P27}'s own pass nor the parity correction that followed it
swept for a second site. **When a constraint bites once, grep for every place
the quantity is computed** \dash{} it took one search of the file.

The stale comment above that loop said \enquote{these same 30 discordant
items} after the data had moved to thirty-one, which is the same failure one
level down and is the reason the loop was read at all.

#### A new parity class: an English term that Polish naturally writes as maths

C4 and C8 diverged in five frames, and every one was the same word. English
wrote \enquote{p-value} as prose; Polish wrote \emph{wartość $p$}, which
carries a maths span English did not have. Neither edition was wrong and both
are idiomatic.

The fix is the English's, not the Polish's: `$p$-value` is standard typography
and it makes the two token streams identical. **So the rule in *Two editions*
gains a third instance beside the digit and the word: an English compound
whose Polish form needs the symbol has to carry the symbol in both.** It is
worth checking for while drafting, because it fires on every frame the term
appears in and there were seven of them.

#### The claim was true and did not reproduce from the page, and it was an inequality

The credible and confidence intervals differ by at most $\num{0.4978}$ points,
strictly under Program~\ref{prog:P27}'s $\val{p27.grid.pts}$-point grid, and
the script asserted exactly that. **The page prints $\val{p28.cred.hi}$ and
$\val{p28.conf.hi}$, which subtract to $\num{0.5}$** \dash{} equal to the
grid, not under it \dash{} so a frame saying \enquote{both gaps are under it}
is contradicted by its own two numbers.

Programs~\ref{prog:F04}, \ref{prog:F05}, \ref{prog:P07}, \ref{prog:P12},
\ref{prog:P23} and \ref{prog:P27} each paid for the general rule, and every
previous instance was a **ratio**. This is the first time it has bitten an
**inequality**, which is why it survived a `reproduces()`-style habit: that
helper checks an arithmetic result against its printed operands and has nothing
to say about a comparison. The script now carries a second assertion on the
printed forms, and both editions say \emph{no larger than} rather than
\emph{under}.

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P28.1 point-or-shape | 588 / 636 | 7.73 | 7.50 | 6.93 | 8.51 | 7.88 |
| P28.2 prior-in-items | 550 / 518 | 7.23 | 8.02 | 8.52 | 9.10 | 9.67 |
| P28.3 two-sentences | 635 / 657 | 6.82 | 6.95 | 6.71 | 7.89 | 7.62 |
| P28.4 route-by-belief | 600 / 657 | 5.46 | 7.35 | 6.71 | 8.35 | 7.62 |

All eight at or under mermaid's wrap cap on the first render, at three ranks,
and **for the fifth pass running the last node of a three-rank chain needed no
correction afterwards**, because Program~\ref{prog:P22}'s rule was applied
while drawing.

Three of the four sit between a question and its answer and none answers it,
which is the P04/P07 case for the fourteenth time. Measured in `main-en`:
figure 1 and frame 3's question on p1031 with the answer on p1032; figure 2 on
p1033 a page before frame 9's question; figure 4 with frame 29's question on
p1043 and the answer on p1044. In `main-en-a4` figures 1 and 4 each share a
page with their question **and** its answer (861 and 871), which is the
strongest form of the check. The Polish anchors hyphenate under `pdftotext`,
which is Program~\ref{prog:P10}'s recorded extraction limit rather than a
defect; the structural argument covers them, since a float cannot rise above
the page its declaration point falls on.

#### Layout, and one round of lengthening cleared both cues

Two orphaned cues in `main-pl-a4`, at frames 20 and 29, cleared in **one
round** by lengthening in both editions. Fifteenth confirmation of
Program~\ref{prog:F06}'s two-sided rule and it has still never failed.

Both added paragraphs earn their place. Frame 20's says what the parameter is
conditioned on \dash{} it is defined *given* that the two models disagreed, so
two evaluations of very different sizes with the same discordant counts give
the same posterior, which is Program~\ref{prog:P27}'s statement about the
concordant items reached from the definition rather than from the arithmetic.
Frame 29's says that the $\varepsilon$-greedy rule needs a second decision
nobody states \dash{} who counts as the leader \dash{} and that near a half
the label flips on one observation, so the traffic split is discontinuous
exactly where the evidence is weakest.

One overfull box before that, and it was plain Polish prose: $\num{2.2}$ pt in
`main-pl-a4` from a line of long words with no maths in it at all. Reworded,
and the multiset came back element for element to the baseline in all four
builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull vboxes, no
stranded openers and no stranded headings. **The orphan-tail count did not
move at all**: 28, 29, 20, 21, exactly the pre-P28 figures, which is the ninth
time (F13, P07, P09, P12, P15, P17, P19, P23, P28).

Pages 1168 / 1182 / 975 / 987, from 1146 / 1158 / 955 / 967.

#### Also

- Traps 274 to 281 added to `notes/02`.
- **Parity came back clean on its ordered checks after one correction round**,
  and that round was the new `$p$-value` class rather than a word-order
  divergence. The four values C7 reported unused were cut on
  Program~\ref{prog:F11}'s finding: two are a **gate** on
  Program~\ref{prog:P23}'s odds form, which belongs in the assertion and never
  in the ledger (Program~\ref{prog:P17}'s rule), and two are $1 + 143$ and
  $1 + 57$, which the reader does in their head.
- The listing was extracted from `main-en.pdf` p1039--1040 and run: it prints
  `0.57`, which is what the page prints and what the frame's display claims.
  Note the rounding is **inside** the listing, which is
  Program~\ref{prog:P19}'s rule applied while writing rather than after.
- The issue's *No Quiz (Foundation-only)* checkbox is stale in the way P04,
  P14, P24, P25, P26 and P27 each found it stale.
- Frame numbers mapped after writing: sections landed at
  `1--5 / 6--11 / 12--18 / 19--26 / 27--30 / 31--37`.

### Program P29 pass, August 2026 --- Part VIII begins

**Thirty-four teaching frames, thirty-six printed, both editions**, against a
brief that projected forty-five. Six sections: how surprised should you be,
entropy is average surprise, what a bit is, the effective number of choices,
entropy at run time, and what a bits-per-token figure is missing.

Twenty-second program under its brief's estimate, and the cause is the one
Program~\ref{prog:P27} named rather than any of the three before it: **the
brief was read as a checklist and two of its three payoffs turned out to be
handed here by name**, by passes that had already written down what they were
leaving. Program~\ref{prog:P19} §5 works \enquote{why you cannot average
perplexities} in full, with the measurement, and its own header says what is
left \dash{} *what a perplexity MEANS (the effective number of choices) ->
P29*. Program~\ref{prog:P25} measures an attention row's entropy at three head
sizes and its header says *entropy as a quantity in its own right -> P29*. So
§4 owes the **reading** of a number the book already has and §5 owes the
meaning of six committed ones, and neither may re-teach its neighbour.

**What was genuinely left is one section.** §3 \dash{} entropy is the shortest
average code length, and that is what makes a bit a thing somebody sends
rather than a scale somebody picked. Program~\ref{prog:F03} owns the unit
*conversion*; nothing in the book had said what a bit **is**.

#### Every assertion passed on the first run, and Program P27's warning was right

That pass recorded the finding and this one is its first test: **a script whose
assertions all pass has told you only that it is self-consistent**, so read the
formulas against the numbers anyway. Four defects were sitting in a script that
ran green, and none of them is a kind any assertion would have caught.

- **A number under two names, two hundred pages apart.** `p29.bpt` was
  Program~\ref{prog:F03}'s committed `f03.nats.to.bits` \dash{} that exact
  conversion of that exact loss \dash{} recomputed and emitted again. It is
  Program~\ref{prog:F08}'s defect at the widest separation the book has
  produced. It is now **gated and not emitted**, and the frames quote F03's
  value directly.
- **Two searches under one number.** `p29.code.assignments` was enumerated at
  a codeword-length cap of six while the theorem check ran at seven, so the
  page would have quoted a count about a different search from the one the
  claim rests on. One cap throughout, and the count is
  $\val{p29.code.assignments}$.
- **An assertion weaker than its frame.** The maximum-entropy sweep asserted
  that no distribution beats the uniform, where §2 says the maximum is
  *attained*. That is Program~\ref{prog:P10}'s ridge finding from the other
  side: a sweep that never lands on the point cannot establish attainment. The
  grid now provably contains the uniform point (`GRID % 3 == 0` is asserted)
  and the comparison is an equality.
- **Two values duplicating a listing.** Program~\ref{prog:F11}'s finding, and
  at a *different precision* than the transcript prints, which would have put
  `4.0` and `4.00` on facing pages.

**And a fifth, found by re-reading the same script in this pass**, which is
Program~\ref{prog:P28}'s finding one program later: the `reproduces()` helper
checked each bits-per-character figure against *its own* operands and said
nothing about the sum a reader actually does \dash{} dividing the two figures
printed side by side. **A helper is only as wide as the comparison it was
pointed at.** The page's own row is now divided as the page prints it, and
asserted.

#### The one thing the book did not have: what a bit is

Program~\ref{prog:F03} owns the conversion between nats and bits and the base
warning. Nothing had said what a bit **is**, and §3 says it in the only way
that is checkable: a prefix-free code exists with lengths $l_i$ exactly when
$\sum_i 2^{-l_i} \le 1$, and **entropy is the shortest average code length
those lengths can reach**.

It is enumerated rather than argued. Every Kraft-admissible assignment is
generated \dash{} $\val{p29.code.assignments}$ of them at a cap of
$\val{p29.code.cap}$ \dash{} and the best is compared with the entropy over
`Fraction`, with no tolerance anywhere:

| alphabet | best average code | entropy | gap |
|---|---|---|---|
| dyadic, $(\frac12, \frac14, \frac18, \frac18)$ | $\val{p29.code.best}$ | $\val{p29.code.h}$ | **exactly zero** |
| $(\frac25, \frac15, \frac15, \frac15)$ | $\val{p29.nondy.best}$ | $\val{p29.nondy.h}$ | $\val{p29.nondy.gap}$ |

The first row is a **proof for that alphabet** rather than evidence about it,
because nothing was left out \dash{} which is Program~\ref{prog:P14}'s
distinction doing a second job, in the section that most invites a
demonstration instead. The second row is why the bound is a bound: a length is
a whole number of digits and $\logb{2} \frac{5}{2}$ is not.

#### The payoff makes six numbers the book already had readable, and all six are gated

$e^{H}$ is the number of equally likely choices with that entropy, so it
returns $n$ exactly on a uniform distribution over $n$ \dash{} checked at
$\val{p29.eff.checked}$ sizes over `Fraction` where the logarithm allows it.
That one reading is the whole of §4 and §5, and it is worth having because it
turns numbers three earlier programs committed into sentences:

| what it was | what it says |
|---|---|
| F03's seven-way uniform, $\val{p29.seven.nats}$ nats | $\val{p29.seven.n}$ choices, exactly |
| F02's $\val{p29.f02.loss}$ nats $\rightarrow$ F03's $\val{p29.f03.ppl}$ | $\val{p29.ppl.frac}$ per cent of a $\val{p29.vocab}$-token vocabulary |
| P25's attention entropy without the division | $\val{p29.att.raw.eff}$ effective keys of $\val{p29.att.keys}$ |
| P25's, with it | $\val{p29.att.scaled.eff}$ of $\val{p29.att.keys}$ |
| F05's four tokens at $T = \num{0.5}, 1, 2$ | $\val{p29.tok.t05.eff}$, $\val{p29.tok.t10.eff}$, $\val{p29.tok.t20.eff}$ choices |

**Every one of them is a cross-programme gate rather than a quotation**, which
is Program~\ref{prog:P12}'s third kind \dash{} the same worked example
continued. The F02-to-F03 chain is gated in **both** directions on
Program~\ref{prog:P26}'s precedent. So this program cannot come apart from its
four neighbours, and none of them can be corrected without it noticing.

The best sentence the reading buys is P25's: an attention row that P25
measured as giving $\val{p25.e9.raw.top.512}$ per cent of its weight to one key is
\enquote{attending to $\val{p29.att.raw.eff}$ keys}, and the scaling buys back
$\val{p29.att.scaled.eff}$ of $\val{p29.att.keys}$ \dash{} the same
measurement P25 reported in nats, in the unit a design review can argue about.

#### What §5 may conclude, and what it may not

Entropy at run time is a real signal and it is cheap: it needs the
distribution the model already computed and no second forward pass. What a low
entropy licenses is exactly one sentence \dash{} *this model would give nearly
the same answer if you asked again* \dash{} and that is repeatability, not
accuracy. A confidently wrong model has an entropy of
$\val{p29.wrong.ent}$ nats against an honestly uncertain one's
$\val{p29.spread.ent}$.

So the frame says **use it as a filter and never as a warrant**, and names the
cost of getting it backwards: a dashboard built on an entropy threshold is
green through exactly the incident it was bought for.

#### §6: a ratio quoted without one of its two quantities

Bits per character is bits per **token** times tokens per **character**, and
the second factor belongs to the tokeniser and appears nowhere in a loss. The
same model on the same text at $\val{p29.tpc.a}$ and $\val{p29.tpc.b}$ tokens
per character reports $\val{p29.bpc.a}$ and $\val{p29.bpc.b}$ bits per
character \dash{} a factor of $\val{p29.bpc.ratio}$ in which **the model's
contribution cancels exactly**, which the script asserts because it is the
section's whole claim.

Three consequences, each checkable rather than a caution: a model can lower
its loss by changing its tokeniser with the weights untouched; two losses are
comparable only under one tokeniser, and stating that condition costs a
sentence; and a compression claim is a file size somebody can produce where a
loss is not, which is why converting to it is worth the multiplication.

That is this book's recurring complaint \dash{} a ratio quoted without one of
its two quantities \dash{} arriving in the place it does the most damage,
because two models are routinely compared on loss alone.

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P29.1 surprise-adds | 634 / 657 | 5.77 | 6.96 | 6.71 | 7.90 | 7.62 |
| P29.2 code-budget | 595 / 628 | 6.39 | 7.41 | 7.02 | 8.42 | 7.97 |
| P29.3 nats-to-count | 522 / 561 | 5.61 | 8.45 | 7.86 | 9.59 | 8.92 |
| P29.4 two-tokenisers | 645 / 597 | 6.93 | 6.84 | 7.39 | 7.76 | 8.39 |

All eight at three ranks and all above the aspect-ratio crossover on the first
render, so no redesign. `p29-nats-to-count` at $522$ pt is the narrowest of
the four and sets its node text at $\num{9.59}$ pt on A4, which is inside the
band F03, F04 and F05 already occupy \dash{} checked against the recorded
table rather than asserted, and the width budget was read before the nodes
were written rather than after.

Written against the frames **above** them, which is
Program~\ref{prog:P22}'s rule, and **for the sixth pass running the last node
of a three-rank chain needed no correction afterwards.** That is now long
enough to say the rule works rather than that six passes were lucky.

#### Parity: three rounds, every failure a recorded class

- **A reference behind its maths, twice.** `Program~\ref{prog:F01} podaje
  $2^{10} \approx 10^{3}$` had to be rebuilt so the reference leads, and
  `dokładnie tak, jak Program~\ref{prog:P25} pokazuje dla $p(1-p)$` the same.
  It is the class F06 lost three rounds to and F07 six, and it is still the
  one to check for while translating.
- **A summary item with two of them at once**, which is where P13, P15, P19,
  P26 and P27 each hit it. Summary items are worth reading first.
- **A bare decimal inside maths in both editions.** C10 caught `1.32`, which
  the English owed as much as the Polish did \dash{} the half of that check
  that is easy to forget.

C7 reported four values the frames do not quote; all four emissions were cut
on Program~\ref{prog:F11}'s finding rather than forced into the prose.

#### Layout, and one round of lengthening cleared both cues

Two orphaned cues \dash{} frame 7 in `main-en-a4` and frame 23 in
`main-pl-a4` \dash{} cleared in **one round** by lengthening in both editions.
Sixteenth confirmation of Program~\ref{prog:F06}'s two-sided rule and it has
still never failed.

Both added paragraphs earn their place. Frame 7's says that the unit is a
choice of logarithm base and nothing more \dash{} the same fair coin is
$\val{p29.coin.bits}$ bit or $\ln 2$ nats and neither is the more fundamental
\dash{} and then says why the bit wins the rest of the program: §3 sends
binary digits down a wire, and a digit is a two-way choice. Frame 23's says
why the reading generalises at all: an attention row is a distribution,
because the $\softmax$ is what makes it sum to one, so §2's definition applies
to it unchanged. Nothing in this program was built for language models.

**A Polish manifest line measured 48 characters against
Program~\ref{prog:P14}'s budget of \enquote{under about 48}, and it was left
alone deliberately.** The build is the instrument for that column, it reported
no box, and this file's own rule is to be led by the measurement rather than by
the guideline that summarises earlier ones. Recorded so that the next person
meets the boundary case with the reasoning rather than the number.

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, no stranded openers, no stranded headings and no orphaned cues.
**One orphan tail added, in `main-en-a4`**: 28, 29, 21, 21 against the pre-P29
28, 29, 20, 21.

Pages 1188 / 1207 / 993 / 1008, from 1168 / 1182 / 975 / 987.

#### Also

- Traps 282 to 289 added to `notes/02`.
- **Elicitation 55%, the highest outside Part I**, above
  Program~\ref{prog:P28}'s 54% and Programs~\ref{prog:P23} and
  \ref{prog:P27}'s 53%, and again with **no conversions at all** because the
  frame plan was written that way. That is four consecutive programs
  (P26, P27, P28, P29) demonstrating the same thing, so the finding is
  settled: **designing the rate in is free and raising it afterwards is
  not.** Program~\ref{prog:P24} paid nine frames for ten points.
- The listing was extracted from the finished PDF and run as a REPL would: it
  prints `(4.0, 1.18)`, which is what the page prints, and the rounding is
  **inside** the listing, which is Program~\ref{prog:P19}'s rule applied
  while writing rather than after.
- The issue's *No Quiz (Foundation-only)* checkbox is stale in the way P04,
  P14, P24, P25, P26, P27 and P28 each found it stale.
- Frame numbers mapped after writing: sections landed at
  `1--4 / 5--10 / 11--18 / 19--25 / 26--30 / 31--34`.

### Program P30 pass, August 2026

**Forty-six teaching frames, forty-eight printed, both editions**, against a
brief that projected fifty-five. Eight sections: what it costs to use the
wrong code, the excess cannot be negative, it is not symmetric, what a zero
costs each way round, mode-covering and mode-seeking, it is not a distance,
why not simply symmetrise it, and the direction you are already minimising.

Twenty-third program under its brief's estimate, and the cause is
Program~\ref{prog:P27}'s: **the brief was read as a checklist and its
machinery turned out to be spent while its content was not.**
Program~\ref{prog:P29} §3 supplies the whole of the coding argument
exhaustively enumerated; Program~\ref{prog:P26} supplies cross-entropy as a
negative log-likelihood; Program~\ref{prog:P18} supplies its derivative;
Program~\ref{prog:P19} supplies Jensen in both directions, so
$\KL{p}{q} \ge 0$ is two lines from a theorem the reader already has rather
than a new proof; and Programs~\ref{prog:F09} and \ref{prog:P05} supply the
triangle inequality **with its equality condition**, which is what makes §6's
contrast land as a misnomer rather than as pedantry.

**What no written program mentions at all** is the asymmetry's cost:
mode-covering, mode-seeking, Jensen--Shannon, and the fact that minimising a
training loss picks one of the two directions for you. That is P30's own, and
it is four of the eight sections.

#### Every debt was written down in the program that owed it

Eight programs point here by name and a ninth points from a file header, and
this file's own instruction was to read them rather than count them. That is
the cheapest starting position any program in the book has had, and it is
worth recording what it bought: **the arrival needed no new computation at
all.**

Program~\ref{prog:P29} §3 reports that on the non-dyadic alphabet
$(\frac25, \frac15, \frac15, \frac15)$ the best code averages
$\val{p29.nondy.best}$ bits against an entropy of $\val{p29.nondy.h}$, and
calls the $\val{p29.nondy.gap}$ gap *the rounding of a length to a whole
number*. The winning lengths are $(1, 2, 3, 3)$ with a Kraft sum of exactly
one, so the code implies the distribution $q_i = 2^{-l_i}$ \dash{} which is
**P29's own dyadic alphabet, the other row of the same table**. So

\[ H(p) + \KL{p}{q} \;=\; \val{p29.nondy.h} + \val{p30.src.kl}
   \;=\; \val{p30.src.ce} \]

exactly, and P30's opening move is to say what a number already on the page
**is**. The two alphabets P29 chose in order to contrast a dyadic case with a
non-dyadic one turn out to be the source and the code of one divergence.

That is Program~\ref{prog:P12}'s third kind of gate \dash{} the same worked
example continued \dash{} and it is the cleanest instance available anywhere
in the book, because the number was already committed and already meant
something.

#### The measurement was probed before drafting, and two designs failed first

The brief says the mode behaviour must be **measured on a bimodal target, not
asserted**, and Program~\ref{prog:P05}'s greedy-packing failure is the
standing warning: a demonstration whose answer depends on where an optimiser
stopped **measures the search rather than the geometry**. So the design was
run as a probe before a line of prose existed, and two versions of it were
wrong.

- **A target with zeros in it destroys the asymmetry.** Reverse KL came back
  infinite for $77$ of $81$ candidates, because a zero in the *target* is a
  zero in reverse KL's second argument. The target has to be **strictly
  positive everywhere** for the mechanism to be visible at all.
- **A target whose modes are not sharp enough leaves $-H(q)$ dominating**, so
  reverse KL still preferred a wide candidate and the finding disappeared.

Both were found by running the design rather than by reasoning about it,
which is this file's recorded rule arriving one step earlier than usual
\dash{} before there was any prose for an assertion to contradict.

**The mechanism that survived needs no optimiser at all**, which is what makes
it exact. Forward KL contains $p_i \ln(p_i/q_i)$, so a $q$ that puts zero
where $p$ is positive costs $+\infty$; reverse KL contains $q_i \ln(q_i/p_i)$,
so the same omission costs it **nothing**, because the sum never visits that
outcome. Every candidate in a $\val{p30.fam.n}$-member family is then
enumerated and the minimiser of each direction reported \dash{} a proof over
that family rather than a search, which is Program~\ref{prog:P14}'s
distinction doing exactly the job P05 warns about.

| | forward | reverse |
|---|---|---|
| candidate chosen | the widest, full support | the narrowest, a point mass |
| its width | $\val{p30.fwd.width}$ bins | $\val{p30.rev.width}$ bin |
| mass left on the second mode | $\val{p30.fwd.mode2}$ per cent | **exactly zero** |
| candidates with a finite value | $\val{p30.fin.fwd}$ of $\val{p30.fam.n}$ | $\val{p30.fin.rev}$ of $\val{p30.fam.n}$ |

Asserted over **all $\val{p30.targets.n}$ targets tried**, including one whose
second mode carries $\val{p30.head.mode2}$ per cent of the distribution and
which the reverse direction throws away entirely. So the finding is a property
of **which distribution sits in the numerator of the ratio** rather than of
the target, and the script says so over the whole set rather than reporting
one cell.

#### The triangle inequality does not merely fail, it fails as the common case

On an exact grid of distributions on three points with denominator
$\val{p30.tri.den}$, **$\val{p30.tri.bad}$ of $\val{p30.tri.total}$ ordered
triples violate it** \dash{} $\val{p30.tri.pct}$ per cent, over `Fraction`
with no tolerance anywhere. The worst on that grid is a detour
$\val{p30.tri.gap}$ nats **shorter** than going direct:
$\val{p30.tri.direct}$ against $\val{p30.tri.via}$.

\enquote{Sometimes fails} would have been a hedge covering a quarter of all
cases. And the contrast is against a property the reader can check, because
Program~\ref{prog:F09} gave them the inequality *with* its equality
condition \dash{} which is why the misnomer lands rather than reading as
pedantry.

#### And Jensen--Shannon's cost is one line

Two point masses $\val{p30.js.seps}$ bins apart and one bin apart are at
**exactly the same** Jensen--Shannon distance, $\ln 2 = \val{p30.js.cap}$,
where KL is infinite for both. So the symmetric bounded alternative reports
the same number however far apart the distributions are: it saturates, and it
saturates in precisely the regime a training run starts in.

That is the honest answer to *why not simply symmetrise it*, and it needs no
hedging \dash{} KL's unboundedness is a gradient signal where JS has none, and
the asymmetry is the thing §5 showed you were choosing on purpose.

#### The payoff closes Program P26's loop from the other side

Minimising cross-entropy against a fixed dataset **is** minimising the forward
divergence to the empirical distribution, because the identity's other term is
$H(\hat p)$, a property of the file, and no gradient reaches it. Checked at
three models, exactly, and against a uniform model the page prints the
identity with three numbers in it:
$\val{p30.emp.ce.uniform} = \val{p30.emp.h} + \val{p30.emp.kl.uniform}$.

So §5's choice was made for the reader by the shape of the objective long
before anybody discussed it, and the consequence is checkable rather than
rhetorical: **every run launched against a fixed dataset minimised the
mode-covering direction**, which is why a model asked for something ambiguous
hedges across the possibilities rather than committing to one. It was trained
by an objective that pays an unbounded price for putting no mass where the
data had some, and nothing at all for spreading.

Program~\ref{prog:P26} said the excess *has a name and is P30's*; this is the
same identity read from the training end rather than the estimation one.

#### The two gates the pass earned, and both are the recorded classes

**One fired on its first run and named a real defect.** The arrival gate
asserted this program's cross-entropy against `p29.code.best`, which is the
**dyadic** row of P29's table; the non-dyadic one is `p29.nondy.best`. Two
committed values that look like one, in the very table P29 wrote in order to
contrast them \dash{} which is Program~\ref{prog:F08}'s defect appearing
inside the mechanism built to prevent it. It failed loudly rather than
quietly, which is the whole argument for writing the gate before the prose.

**The second was written for this pass and is P28's finding applied.** §8
prints all three terms of the identity on one page, so a reader will *add* the
two on the right. The existing assertion was on the underlying floats and had
nothing to say about that \dash{} which is exactly the gap
Program~\ref{prog:P28} found on an inequality and Program~\ref{prog:P29} found
again on a row of a table. The sum is now checked **in the form the page
prints it**, because that is the only form anybody will check.

#### Two things caught by reading rather than by any gate

- **A transcript that demonstrated symmetry in the section about asymmetry.**
  The first version used $(\num{0.9}, \num{0.1})$ against
  $(\num{0.1}, \num{0.9})$, whose two divergences are equal **by
  construction** \dash{} a listing illustrating the asymmetry with a pair that
  does not have one. It is $(\num{0.9}, \num{0.1})$ against
  $(\num{0.5}, \num{0.5})$ now, which gives $\num{0.3681}$ and $\num{0.5108}$.
- **A tail ratio dropped on Program~\ref{prog:F05}'s precedent.** F05's exact
  ratio is $\num{51.7}$ and its own printed table divides to $\num{53.1}$,
  which is why that program states a bound; quoting the $\num{53.1}$ here
  would have imported a figure the source page cannot support. Asserted in the
  script and not emitted.

#### The elicitation rate broke a run of four, and the cost was measured

**52%**, equal with Program~\ref{prog:P26} and below Programs
\ref{prog:P27}, \ref{prog:P28} and \ref{prog:P29}. Those four were designed in
from the frame plan and cost nothing. **This one was not**: the finished draft
measured 41%, and six conversions took it to 52% for **two frames**.

So the run of four is broken and the finding it established is unharmed,
because the price is now measured at a third point: Program~\ref{prog:P23}
paid two frames for twenty points, Program~\ref{prog:P24} paid nine for ten,
and this pass paid two for eleven. **Designing it in is free; retrofitting it
is cheap when the frames are short and dear when they are long.**

The honest reason the plan came in at 41% is the one
Program~\ref{prog:P05} recorded: §1 to §4 are derivations, and a derivation
has fewer places to stop and ask than a section built on numbers. Five of the
six conversions are in §5 to §8, where the material is measurements. Four of
them produced the P06 pattern \dash{} a frame opening with `\ans` and ending
with `\dotline`.

#### Parity: two rounds, and neither was a word-order divergence

**C4, C8, C12 and C16 all passed on the first run** \dash{} the ninth program
to manage it, and the second running (after Program~\ref{prog:P28}) where the
correction rounds were something other than the ordered-token classes.

- **C10 fired on three bare decimals per edition**, all of them the subscript
  in $p_{\num{0.5}}$ naming a distribution by its temperature. The fix was not
  to wrap them: a distribution named by a **shape** reads better and carries
  no decimal at all, so they are $p_{\text{peaked}}$ and $p_{\text{broad}}$ in
  English and $p_{\text{szpiczasty}}$ and $p_{\text{szeroki}}$ in Polish.
  Note the `\text{}`, which is Program~\ref{prog:P26}'s rule \dash{} `\mathrm{}`
  names an operator and must not be translated.
- **C7 reported two values the frames did not quote**, and here the fix was
  the other way round from Program~\ref{prog:F11}'s usual one: they were
  **worth quoting**, because printing all three terms makes the identity
  concrete where stating it leaves it abstract. That is what earned the
  printed-form assertion above.

#### An over-correction to a lint became three overfull boxes

C10 fired on three bare decimals per edition \dash{} the subscript in
$p_{\num{0.5}}$, naming Program~\ref{prog:F05}'s distribution by its
temperature. The check was right: a bare decimal in a Polish edition owes a
comma. **The fix it asks for is `\num{}` around the decimal, and what was
written instead was a long word.** $p_{\text{peaked}}$ is seventeen
characters set as text where $p_{\num{0.5}}$ is eight, and the clause
carried two of them inside two `\KL{}{}` spans.

The next build came back with a **$\num{62.7}$ pt** hbox, the largest this
book has produced from ordinary prose. It went into a display, on the
recorded rule \dash{} and the build after **that** produced a
$\num{46.9}$ pt box at a *third* site, inline, in **Polish only**, because
the same sentence in English is short enough to break.

**Fixing the instance was not fixing the class**, which is
Program~\ref{prog:P28}'s finding arriving two programs later and in a
different medium. And the class was never the width of a span: it was the
name. The two distributions **are** §1's $p$ and $q$ with a particular pair
in them, so they are called $p$ and $q$, declared in one clause where the
prose already says *peaked* and *broad* in words. Every downstream formula is
then two characters wide, C10 has nothing to complain about because there is
no decimal left, and the notation connects §3 to §1 instead of inventing a
private pair of names for one section.

**So the generalisable half is not \enquote{a lint fix can cost you a
box}** \dash{} though it can, and no gate connects a source-level check to a
page-level one. It is narrower and more useful: **when a check names a token,
fix the token it names.** C10 objected to a decimal and the decimal was
replaced with something else entirely, which satisfied the check by
removing the thing it was looking at rather than by correcting it. The width
was the symptom; the over-correction was the defect; and the right answer
turned out to be shorter *and* better notation than what was there before the
lint fired.

**And one box was a class this book has not recorded: a display can overflow
too.** The Jensen chain is five relations on one line, and a display gets its
own line but not an unlimited one. Broken after the inequality with `align*`,
which Programs~\ref{prog:F06} and \ref{prog:P02} already use. So the
recorded advice \dash{} *put it in a display* \dash{} has a limit worth
knowing: a display rescues an unbreakable run **inside a paragraph**, and a
display that is itself one long chain still has to be broken by hand.

#### And the build's own exit line caught it, for the fifth time

`MAKE_EXIT 2` while the harness reported the command complete, with
`main-pl`, `main-en-a4` and `main-pl-a4` at **exactly** their pre-P30 page
counts because `make` stopped after the English target. Both halves of the
recorded habit fired together and either alone would have been enough.

**And the hbox reporting Program~\ref{prog:P24}'s pass added paid for itself
a third time.** It named the file, the source lines *and* the offending text
\dash{} `Before computing anything: do you expect $D[...]$ and $D[...]$`
\dash{} so there was no inference to make and no cycle to spend on one. That
is now P24 (which paid a cycle to learn it), P26 and this pass.

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P30.1 two-pieces | 539 / 533 | 5.79 | 8.18 | 8.27 | 9.29 | 9.39 |
| P30.2 which-is-first | 651 / 657 | 5.92 | 6.77 | 6.71 | 7.69 | 7.62 |
| P30.3 two-fits | 546 / 582 | 5.86 | 8.08 | 7.58 | 9.17 | 8.60 |
| P30.4 three-promises | 598 / 547 | 6.42 | 7.37 | 8.06 | 8.37 | 9.16 |

All eight at three ranks and all above the aspect-ratio crossover on the
first render, so no redesign. `p30-two-pieces` at $539$ pt is the narrowest
and sets $\num{9.29}$ pt on A4, inside the band Programs~\ref{prog:F03},
\ref{prog:F04} and \ref{prog:F05} already occupy \dash{} checked against the
recorded table rather than asserted.

Written against the frames **above** them, which is
Program~\ref{prog:P22}'s rule, and **for the seventh pass running the last
node of a three-rank chain needed no correction afterwards.**

Measured on the page afterwards, in all four builds: `main-en` 1079, 1086,
1091, 1093; `main-en-a4` 902, 907, 912, 914; `main-pl` 1095, 1102, 1107,
1110; `main-pl-a4` 914, 919, 924, 926. Figures 1 and 2 each sit above the
question that follows them and neither answers it \dash{} the P04/P07 case
for the fifteenth time: F1 carries the split, which the frames above state in
full, and the question below asks for the divergence **written out**, which
appears nowhere in it; F2 carries what a zero costs each way round, and the
question below asks whether adding a floor fixes it. Figures 3 and 4 each
close a section with the next section's heading below them.

#### Layout, and two rounds of lengthening

The first build stopped at the English target with `MAKE_EXIT 2` and three
page counts unmoved. After the boxes were cleared, two orphaned cues arrived
in the **A4** builds \dash{} both the same frame, P30's 25 \dash{} and
clearing them moved one into `main-pl`, at frame 13, which is the frame the
box fix had just edited. Two rounds, both cleared by **lengthening**:
seventeenth and eighteenth confirmations of Program~\ref{prog:F06}'s
two-sided rule, which has still never failed.

Both added paragraphs earn their place, and the first is load-bearing rather
than filler. Frame 25's says precisely what would be wrong with fitting a
candidate: the answer would depend on where the search started, when it
stopped and how the candidate was parameterised, so a difference between the
two answers could have come from any of four things and nothing on the page
would say which. Frame 13's says that the two distributions have the **same
support**, so nothing in §3 can be blamed on a missing outcome \dash{} which
rules out §4's mechanism as a confound before §4 introduces it.

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, no stranded openers, no stranded headings and no orphaned cues.
**One orphan tail added, in `main-en`**: 29, 29, 21, 21 against the pre-P30
28, 29, 21, 21.

Pages 1216 / 1233 / 1015 / 1028, from 1188 / 1207 / 993 / 1008.

#### Also

- Traps 290 to 296 added to `notes/02`.
- The listing was extracted from the finished PDF and run as a REPL would: it
  prints `(0.3681, 0.5108)` and `(inf, 0.6931)`, which is what the page
  prints. The rounding is **inside** the function, which is
  Program~\ref{prog:P19}'s rule applied while writing rather than after, and
  the `inf` is what Python prints rather than a value behind `\val{}`, which
  is Program~\ref{prog:P01}'s rule.
- Frame numbers mapped after writing and again after the six conversions:
  sections landed at `1--6 / 7--12 / 13--18 / 19--23 / 24--33 / 34--38 /
  39--42 / 43--46`.

### Program P31 pass, August 2026 --- Part VIII is complete

**Thirty-eight teaching frames, forty printed, both editions**, against a
brief that projected fifty. Six sections: what two margins do not say, why it
cannot be negative, symmetric out of asymmetric pieces, what a finite sample
does to it, post-processing cannot create it, and what would settle it.

Twenty-fourth program under its brief's estimate, and the cause is the one
Program~\ref{prog:P27} named and Program~\ref{prog:P30} split in two: the
machinery was entirely spent and the content was not. **Program~\ref{prog:P30}
built every tool this program uses** \dash{} the divergence, its
non-negativity through Program~\ref{prog:P19}'s Jensen, zero exactly on
agreement \dash{} because mutual information **is** that divergence applied to
one particular pair of arguments. So this program defines exactly one new
object in six sections, and sections 1 to 3 are short by construction.

**And P30 said where the length goes, in its own closing frame**: *P31 defines
it, and spends most of its length on why the claims people make with it are
usually not supported.* Sections 4 and 5 are two thirds of the program, which
is what that sentence asked for.

#### The arrival needs no new example, for the second pass running

Program~\ref{prog:P24} built the smallest space that shows a zero correlation
proving nothing \dash{} $Z$ uniform on $\{-1, 0, 1\}$ and $W = Z^{2}$
\dash{} proved $\Cov(Z, W) = 0$ exactly over fractions, and wrote the pointer:
*Program P31 builds the quantity that does see it.*

So the new quantity is computed on that same pair and the two numbers sit
side by side: the correlation is $0$ and $I(Z; W) = \val{p31.zw.mi}$ nats,
which is $H(W)$ **identically**, because $W$ is a function of $Z$. The script
asserts the identity rather than the figure, and gates on
Program~\ref{prog:P24}'s own committed `p24.tri.n` so that a change to its
construction stops this arrival rather than quietly re-aiming it.

That is Program~\ref{prog:P12}'s third kind of gate \dash{} the same worked
example continued \dash{} and P30 had exactly the same thing from P29's two
alphabets. **Two passes running, the opening move has been to take a number
already on the page and say what the new quantity makes of it**, and both
times the neighbour had written the pointer.

#### An assertion failed and the failure is the better frame

The draft asserted $H(Z \mid W) = 0$ alongside $H(W \mid Z) = 0$. Only the
second is true: $W$ is a function of $Z$, so being told $Z$ leaves nothing of
$W$ undetermined, while being told $W$ leaves $Z$ ambiguous between $-1$ and
$1$. $H(Z \mid W) = \val{p31.zw.hzw}$ nats.

**So the conditional entropies are asymmetric while the mutual information
they both give is not** \dash{} one number reached from two sets of pieces
that have almost nothing in common. That is section 3, and it is exactly what
a reader who has just spent Program~\ref{prog:P30} on an asymmetric quantity
should be made to notice. Sixteenth pass running that writing the assertion at
the computation, before the prose it supports, caught something.

#### The headline is an exact expectation, and P27's warning caught it quoting itself out of regime

For a two-by-two table with total $N$ the outcomes are the ways of splitting
$N$ counts into four cells, so the expected plug-in mutual information under
independence is **summed exactly**: every table enumerated, the multinomial
weights asserted to sum to exactly $1$ as a `Fraction`, no seed and no error
bar. That is Program~\ref{prog:P14}'s distinction doing the job
Program~\ref{prog:P05}'s greedy-packing failure warns about, which is how
Program~\ref{prog:P30} handled its own family.

| $N$ | tables | $\Ex[\text{plug-in}]$, truth is $0$ | vs $\frac{1}{2N}$ |
|---|---|---|---|
| $10$ | $\val{p31.bias.tables10}$ | $\val{p31.bias.n10}$ | $\val{p31.bias.ratio10}$ |
| $20$ | $\val{p31.bias.tables20}$ | $\val{p31.bias.n20}$ | $\val{p31.bias.ratio20}$ |
| $50$ | $\val{p31.bias.tables50}$ | $\val{p31.bias.n50}$ | $\val{p31.bias.ratio50}$ |
| $100$ | $\val{p31.bias.tables100}$ | $\val{p31.bias.n100}$ | $\val{p31.bias.ratio100}$ |

**Two findings, both exact.** The estimator returns a positive number on data
with no dependence at all, in expectation, at every $N$. And the textbook
correction $(a-1)(b-1)/2N$ **understates it worst exactly where the bias is
largest**, converging from $\val{p31.bias.ratio10}$ to
$\val{p31.bias.ratio100}$ \dash{} so the standard remedy fails hardest in the
regime that reaches for it.

**And then Program~\ref{prog:P27}'s warning paid off, for the second time
after Program~\ref{prog:P29}.** Every remaining assertion passed on the first
run, so the formulas were read against the numbers anyway \dash{} and the
scale-up was quoting its own formula outside its regime. The correction is
asymptotic in items against **cells**, and sixteen categories each way is
$\val{p31.big.cells}$ of them: at fifty items that is a fifth of an item per
cell, where a probe of this file measured $\num{0.64}$ times what the formula
predicts. \enquote{$\num{2.25}$ nats of bias, eighty-one per cent of the
maximum} is a striking sentence and it is a number the formula cannot
support.

**Restated the way round that is in regime and is exact arithmetic**: the bias
falls under one per cent of the maximum $\val{p31.big.max}$ nats only at
$N = \val{p31.big.need}$, about $\val{p31.big.per}$ items per cell. That
converts an abstract bias into a sample-size requirement a reader can check
against their own experiment \dash{} and it is a better number, because
nobody reports it. **The warning box in §4 says all of this on the page**,
because a program whose subject is quoting numbers out of their range owes
the reader its own instance of the error.

#### The inequality reads from both ends, and that is the section

Post-processing cannot create information: if $X \to Y \to Z$ then
$I(X; Z) \le I(X; Y)$, checked against every channel on a rational grid
\dash{} $\val{p31.dpi.channels}$ of them \dash{} with none exceeding it.

The number worth keeping is not the inequality but **the gap**. The best
channel in the family reaches $\val{p31.dpi.best}$ nats against
$\val{p31.dpi.ixy}$, leaving **more than a quarter** behind. So one inequality
says two things and both are routinely got wrong, in opposite directions, by
the same people:

- **A better probe cannot mean more information.** Its score was bounded by
  what the layer carried before anyone trained it, so an improvement is
  movement towards a ceiling and never movement of the ceiling.
- **A weak probe does not mean little information.** The bound is a lower
  bound and it is loose by an amount nobody measures.

That is Program~\ref{prog:P15}'s shape \dash{} one fact read twice at its two
ends \dash{} and it is what makes the section an argument rather than a
caution. The consequence for depth follows and goes the way people do not
expect: a layer is computed from the one before it, so **information about the
input can only fall with depth**; what a deeper layer can be is easier to
read, which is a statement about the probe.

#### The `reproduces` guard fired before it shipped

The DPI percentage would have printed $\num{74.1}$ beside two values that
divide to $\num{74.2}$ \dash{} the class Programs~\ref{prog:F04},
\ref{prog:F05}, \ref{prog:P07}, \ref{prog:P12}, \ref{prog:P23} and
\ref{prog:P27} each paid for, caught here by the helper written to enforce it.
Program~\ref{prog:F05}'s recorded fix applied: the exact percentage is not
load-bearing, so the section **states a bound** \dash{} more than a quarter
\dash{} asserted on both the exact and the printed forms.

Six emissions were cut before parity could report them, on
Programs~\ref{prog:F08}, \ref{prog:F11} and \ref{prog:P03}'s rules: a fraction
Program~\ref{prog:P24} already prints, two duplicating `p31.big.*` under other
names, two the transcript carries, and one text value that is a word rather
than a computed number.

#### The diagram manifest, eighth recurrence, and the budget is not enforced by anything

Program~\ref{prog:P27} measured its eight manifest lines against
`len(key) + 9 + len(copy) < 48` **by hand** and recorded the budget. This pass
wrote the copy without checking it, and **six of the eight came out between 52
and 64** \dash{} while **only one produced a box**, which is
Program~\ref{prog:F06}'s latency rule: the other five land where the line
happens to break and would have shipped latent.

So the budget is not something a build enforces. The build catches whichever
line is unlucky on whichever installation ran. The check is three lines of
Python over a regex tolerating one level of brace nesting, it ran correctly
over all eight here, and it belongs at the point of authoring \dash{} which is
also why Program~\ref{prog:P27}'s attempt at a book-wide version failed: a
looser regex captured the caption instead of the copy and reported most of the
book over budget.

#### The converging-diamond width hazard, fourth instance

`p31-two-routes-one-number` was drawn as two routes meeting at one node
\dash{} two columns \dash{} and rendered at **348 pt**, the narrowest diagram
in the book, setting **$\num{14.39}$ pt on A4** against a band of $\num{6.71}$
to $\num{10.18}$. Wordier nodes do nothing on a graph that is already
wrapping. **Add a rank**: a source node in front of the two routes took it to
$549$ pt and $\num{9.12}$ pt.

That is Programs~\ref{prog:F09}, \ref{prog:F11}, \ref{prog:P09} and now this
one, and the fix has never failed.

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P31.1 what-a-margin-drops | 581 / 577 | 6.24 | 7.59 | 7.64 | 8.62 | 8.68 |
| P31.2 two-routes-one-number | 549 / 574 | 3.33 | 8.03 | 7.68 | 9.12 | 8.72 |
| P31.3 bias-is-not-signal | 578 / 537 | 6.21 | 7.63 | 8.21 | 8.67 | 9.32 |
| P31.4 probe-is-a-floor | 586 / 560 | 6.29 | 7.53 | 7.88 | 8.54 | 8.94 |

**Rule 2 read by content first** \dash{} node, caption and manifest copy, which
is Program~\ref{prog:P18}'s four places \dash{} against the frames on either
side, and **for the eighth pass running the last node of a three-rank chain
needed no correction afterwards**, because Program~\ref{prog:P22}'s rule was
applied while drawing. Measured on the page afterwards: `main-en` 1107, 1111,
1116, 1120 and `main-en-a4` 924, 928, 932, 935, each on the same page as or
one before the frame that follows it, and none answering it. Two Polish
anchors hyphenate under `pdftotext`, which is Program~\ref{prog:P10}'s
recorded extraction limit rather than a defect; the structural argument covers
them, since a float cannot rise above the page its declaration point falls on.

#### Layout, and one round of lengthening

One orphaned cue in `main-en-a4`, at frame 2, cleared in **one round** by
lengthening in both editions. Nineteenth confirmation of
Program~\ref{prog:F06}'s two-sided rule, which has still never failed.

The added paragraph earns its place by guarding against the over-correction a
reader is most likely to make: the correlation is **not** useless and not
broken \dash{} on a pair whose relationship really is a straight line it
measures exactly the right thing, cheaply. What it cannot do is answer a
question it was never asked.

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, no stranded openers, no stranded headings and no orphaned cues.
**The orphan-tail count did not move at all**: 29, 29, 21, 21, exactly the
pre-P31 figures, which is the tenth time (F13, P07, P09, P12, P15, P17, P19,
P23, P28, P31).

Pages 1237 / 1257 / 1034 / 1048, from 1216 / 1233 / 1015 / 1028.

#### Also

- Traps 297 to 304 added to `notes/02`.
- **Parity came back clean on its first run** \dash{} C4, C8, C12, C16, C10
  and C7 all passed, which is the tenth program to manage it and the first
  since Program~\ref{prog:P29}. The accumulated translator rules did it: no
  number spelled as a word, no word spelled as a number, and every reference
  built to lead its maths while drafting.
- One translation decision recorded in the Polish file's own header:
  \enquote{sonda} for *probe*. It is an ordinary Polish word with real use in
  this sense rather than a calque, so this file's rule about keeping English
  ML terms does not reach it.
- **Elicitation 50%**, from three P06-pattern conversions applied to the draft
  before the frame remap \dash{} which is Program~\ref{prog:P23}'s lesson, and
  the conversions cost two frames where doing them after would have cost a
  second renumbering.
- The listing was extracted from the finished PDF and run: it prints `0.0` and
  `0.0201`, which is what the page prints, with the rounding **inside** the
  function on Program~\ref{prog:P19}'s rule.
- Frame numbers mapped after writing and again after the conversions: sections
  landed at `1--6 / 7--10 / 11--15 / 16--25 / 26--34 / 35--38`.

### Program P32 pass, August 2026 --- Part IX begins

**Thirty-nine teaching frames, forty-one printed, both editions**, against a
brief that projected seventy \dash{} the largest estimate left in the
manifest. Eight sections: one position through one block, the score and
whether the derivation survives assembly, from scores to weights, heads, the
residual stream, normalisation and where a position enters, what it costs, and
what this book has not checked.

Twenty-fifth program under its brief's estimate, and Part IX's contract is why:
it introduces **no new mathematics**, so the shortfall is not a shortfall. The
question was never \enquote{what is left of the subject} but \enquote{which
lines of the brief have already been delivered}, and eight of the eleven
bracketed handovers turned out to be spent.

#### Exactly three things were this program's own

`grep -rn 'prog:P32' programs/en/*.tex` was the first thing run, and seven
programs defer here by name.

- **The block parameter count.** Programs~P03 and P06 both hand it over in as
  many words \dash{} \enquote{the count itself is Program P32's, where every
  piece exists} \dash{} and F02 supplies the feed-forward half already.
- **The residual stream.** F12: \enquote{the architecture's own answer... is
  the residual connection, which Program P32 derives.} It names the mechanism
  and does not derive it; greps confirm nothing does.
- **The score measured through the assembly**, which P25 handed over.

Everything else is assembly and none of it is re-taught. That is the part's
contract working as designed rather than a thin program.

#### THE ASSEMBLY PAYOFF: F01's headline number, derived

Program~F01 opens the book by having the reader work out what a
seven-billion-parameter model weighs, and never says where the seven billion
comes from \dash{} on page three there is no vocabulary for it. P03 commits
the shape of the same model.

    attention per block     4 d^2  =  67,108,864
    feed-forward per block  8 d^2  = 134,217,728   (F02 collects this already)
    per block              12 d^2  = 201,326,592
    x 32 layers                    = 6,442,450,944 = 92.0% of F01's 7e9

**The blocks are 92 per cent of the headline number and the embedding is about
two.** It is a cross-programme gate of P12's third kind at the widest span the
book has \dash{} Program F01 to Program P32 \dash{} and it is the sentence
Part IX exists to be able to write.

And the elicitation is counter-intuitive and free, because F02 already handed
the reader the 8d^2: **attention is 4d^2 and the feed-forward block is 8d^2**,
so the half nobody discusses holds twice the half everybody does.

#### The measurement: two probe designs failed, and dropping the sampling was the finding

P25 measured the score spread on vectors it drew directly and handed over
\enquote{check it survives contact}.

- **Probe 1 redrew W_Q and W_K inside every trial.** That is not a
  transformer: a block has FIXED weights and varying inputs, so averaging over
  weight draws answers an easier question than the one asked. It also did not
  finish \dash{} 250M pure-Python operations.
- **Probe 2 fixed the weights and was still too slow** at d_k = 256.
- **Probe 3: the sampling was unnecessary.** q.k = (W_Q^T x).(W_K^T y) =
  x^T M y with M = W_Q W_K^T, and for independent standard-normal x, y that
  bilinear form has variance EXACTLY ||M||_F^2. One weight draw gives the
  score variance in closed form, and
  E||M||_F^2 = d^2 * d_k * (1/d)^2 = d_k, exactly.

**So the assembly preserves P25's d_k, provably, and it needs no trained
model.** Measured at d_model = 64: 2.86, 3.96, 5.63, 8.02 against sqrt(d_k),
and the script gates the d_k = 8 and 64 rows against P25's own committed 2.83
and 7.99.

The half P25's method cannot see is the second column: **a trained model has
one weight draw, not an average**, so its own scores are a few per cent off
before training starts. Reported as indicative (30 draws estimate a spread to
about a seventh) and the ordering is the structural part \dash{} M has rank at
most d_k, so a narrow head has fewer independent directions to average over,
which is P08 doing a job nobody wrote it for.

#### The residual stream, derived and gated on F12's own chain

F12 commits depth 40, sigma' <= 1/4 and the 8.3e-25 bound. The derivation:
with y = x + f(x) the Jacobian is prod(1 + f'_k), and expanding gives a SUM
OVER 2^n PATHS, one per subset of layers. **The empty subset -- around every
layer -- contributes exactly 1.**

    a plain chain's gradient is one product, which n small factors kill;
    a residual stack's is a sum, and one term of that sum is 1.

Checked over Fractions, and gated: this program recomputes (1/4)^40 and
asserts it reproduces F12's committed figure to the printed digit. Same chain,
same depth, and **the contrast IS the derivation** rather than a separate
demonstration.

**And a vacuous assertion was caught before it shipped.** The first version
checked the identity path with `assert Fraction(1) == Fraction(1)`, which
cannot fail \dash{} the defect P01 and P05 both recorded. Replaced by the
consequence, which is the claim: turn every layer off and a plain chain's
gradient is exactly 0 while a residual stack's is exactly 1.

The trapbox states the other half honestly: **one term being 1 does not make
the sum at least 1.** Set every f' to -1 and the other 2^n - 1 paths cancel it
exactly. The identity path guarantees arrival, not size.

#### FOUND WHILE GATING: a defect in a merged program

P03 computes the per-token cache as `kv_bytes(1) / 2**20` \dash{} MEBIbytes
\dash{} under a key named `.mb`, and prints it as \enquote{MB} two lines below
printing the cache itself in GiB. **P32's own gate fired on it.**

It escaped a whole draft because 0.5 MiB is 0.524 MB and **both round to 0.5
at one decimal**: P17's shape exactly, two readings of a formula that agree
numerically and stay invisible until they do not. And P03's own summary warns
about this confusion by name \dash{} \enquote{GB is 10^9 and GiB is 2^30,
about seven per cent larger. A capacity plan that is seven per cent out is
nearly always this.}

Corrected: key to `p03.kv.per.token.mib`, printed unit to MiB, four call sites
across two editions. **No printed digit changed**, so the page and parity were
untouched. In scope because P32's gate surfaced it and P32 is the program that
derives the cache from the block's shapes.

**And it had spread further than P03.** The same figure with the same wrong
unit is in `notes/02` item 90, and in this file's own P03 pass note. Both are
corrected \dash{} and the habit that found them is worth more than the fix:
**when a wrong figure is corrected, grep for the figure, not for the file**,
which is Program~\ref{prog:P28}'s finding about fixing an instance rather than
a class, arriving in a unit rather than in a parity constraint. And the new
catalogue entry written for it originally said
\enquote{item 24 is the general form}: item 24 is the batch-size and
learning-rate rule, and **there is no general entry for the binary prefixes at
all**. That sentence was written from the feel of the catalogue rather than
from the catalogue, which is the class this file keeps recording, inside the
entry warning about exactly that kind of unchecked reading. The entry now says
what is true \dash{} that it *is* the general form, because nothing else was.

#### Parity: three rounds, and the third is the lesson

Every failure was a recorded class, and the useful part is that fixing them one
at a time was the wrong method.

- **A duplicated paragraph.** English frame 3 carried a paragraph the Polish
  had put in frame 4, and it duplicated the sentence after it. Aligned to the
  Polish, which read better.
- **The reference-before-maths inversion, THREE TIMES** \dash{} in a frame, in
  a summary item, and in a second summary item. After the second, the file was
  swept for every `Programu~\ref` rather than waiting for the next failure,
  which is P28's finding applied.
- **A number spelled as a word**: \emph{suma z jedynką} for the English's
  `a sum with a $1$ in it`.
- **And hand-authored decimals in a table**, `$2.83$` against `$2,83$`, which
  is precisely what C12's refusal to normalise the decimal comma exists to
  catch. Both editions now write `\num{2.83}`.

Five emissions were cut on F11's finding rather than the prose padded: the
four `.var` values are the squares of the `.sd` values the table prints, and
`with.embed` is arithmetic the reader does from two figures already on the
page.

#### Also

- Traps 305 to 312 added to `notes/02`.
- **Elicitation 51%**, designed in from the frame plan. The draft came in at
  45% and 33 frames; six frames were added in the thin sections with their
  elicitations written in rather than retrofitted, which is P23's lesson
  applied before the frame remap rather than after it.
- Four diagrams, and **the authoring-time check was aimed at the wrong
  quantity**, which is the pass's sharpest small lesson. P31's finding was
  applied faithfully: all eight manifest lines were measured against
  Program~\ref{prog:P14}'s budget before rendering, and all eight passed. The
  budget turns out not to govern anything (see below), and **the quantity that
  does \dash{} the rendered width \dash{} was not measured until the figures
  were on the page.** Two of the four were the recorded two-column hazard:

  | | before | after |
  |---|---|---|
  | `paths-not-product` en / pl | 315 / 348 pt | 508 / 518 pt |
  | `where-parameters-are` en / pl | 294 / 314 pt | 567 / 498 pt |

  At 294 pt `where-parameters-are` set its node text at **17.03 pt on A4**,
  against a book whose largest is 10.18 and whose typical is under 8. It would
  have been half again the biggest type in the book. Worse, its aspect ratio
  was **1.48**, *below* the trade format's 1.53 crossover \dash{} the
  `f01-magnitudes` hazard \dash{} so in that format the height cap would have
  bound and the figure could not have shared a page with its own frames.

  The recorded fix applied without a detour and for the fifth time: **add a
  rank.** A source node in front of the two routes, and a join node after the
  two halves. Then two chains were widened by making their nodes wordier,
  which is the other recorded fix, and all eight now land between 7.78 and
  10.09 pt with every ratio above 2.39.

  **The generalisable half: a check you ran is not the check you needed.**
  Measuring the manifest line felt like diligence and was aimed at a budget
  that predicts nothing, while the one number the book has a formula for went
  unmeasured. Render and measure the width before writing the prose around a
  figure; it is one `pdfinfo` per file.
- The transcript is the identity path made concrete: with every layer off,
  `(0.0, 1.0)`. Nothing is rounded, so there is no transformation for the
  listing to hide.
- **And the extract-and-run test needed a better instrument.** Every previous
  pass ran the extracted listing as a *script*, which works while the listing
  ends in explicit `print()` calls. This one relies on the REPL echoing an
  expression's value, so run as a script it prints nothing \dash{} and the
  first wrapper written for it put each call's trailing comment *inside* a
  `print(...)`, so the parenthesis closed after the comment and the whole
  block silently produced empty output. That is a defect in the harness
  reading exactly like a defect in the listing. Feeding the extracted lines to
  `code.InteractiveInterpreter` echoes them as a session does, and both
  printed values then reproduce to the character. **What comes out of a
  transcript is REPL input, so run it in a REPL.**

#### The orphaned-cue walk took seven rounds, more than twice the previous record

| round | edit | result |
|---|---|---|
| 1 | \dash{} | 5 cues: `main-pl` 1, `main-en-a4` 3, `main-pl-a4` 1, over four frames |
| 2 | lengthened all four, both editions | 3 cues, and **two of them were the frame round 1 had just lengthened**, now in both trade builds |
| 3 | lengthened that frame again, alone | 1 cue: the residual-Jacobian frame in `main-en-a4` |
| 4 | lengthened that one | measurement void \dash{} two diagrams had to be widened, so the build was stopped rather than spent |
| 5 | the two diagrams widened | 1 cue: the empty-subset frame in `main-pl` |
| 6 | lengthened that one | 1 cue: the parameter-halves frame in `main-pl-a4`, which round 1 had already cleared once |
| 7 | lengthened that one again | clean |

Program~\ref{prog:P08}'s three rounds were the previous record. Two things
are worth carrying.

**Round 2 is the clearest instance of the walk this book has.** Lengthening a
frame moved its own cue *out of* the A4 build and *into both trade builds*
\dash{} one source, four paginations, and a fix aimed at one of them is a
re-roll of the other three.

**And a frame cleared in round 1 came back in round 6**, which is the part
that makes the count seven rather than four. Nothing about that frame changed
between the two; four hundred pages of other people's line breaks moved
underneath it. It is the plainest statement available of what this file means
by a random walk: **a frame is not fixed, only a pagination is**, and the
pagination is re-rolled by every later edit in the same program.

**And round 4 was abandoned deliberately, which is the cheaper move.** A
diagram's size moves every break after it, so that build would have measured a
tree about to stop existing. Ten minutes producing a number to be discarded is
worse than a kill and a clean restart \dash{} provided the aux tree is then
cleared properly, which is what the next entry is about. **When an edit is
queued that will move pagination, stop the build rather than finish it.**

Every edit was made in **both** editions and every added paragraph earns its
place. What went in: that Program~\ref{prog:P25}'s argument needs the entries
to be independent and here they are two images of one stream, so
\enquote{drawn independently} is exactly what the assembly might have
destroyed; that if the hypothesis fails the divisor is right about P25's model
and wrong about every trained block, so the question is not a formality; that
squaring or exponentiating would both give positive weights and neither sums
to one, so the question is what the *normalisation* buys; that both halves of
the parameter count are per block, so multiplying by depth leaves their ratio
where it was; that one number is a model card's figure and the other is what
the shapes force, so any gap has to be accounted for; and that
 = x + f(x)$ constrains $ and (x)$ to one shape and introduces no
operation the book has not got, so a change needing no new rule is exactly the
kind that reads as cosmetic.

**And round 2's edit had introduced a repetition that the layout work found.**
The paragraph added in round 1 opened with \emph{That is a different
computation}, which was already the frame's closing sentence four lines below
\dash{} so the frame said it twice. Removing the duplicate *shortened* the
frame, which is the wrong direction for the cue, so the round-3 edit had to
replace it with something that earns its length rather than merely fill it.
Worth knowing: **a lengthening pass is an editing pass, and it can introduce
the defect it is not looking for.**

#### A killed latexmk truncates the INDEX file, and `makeindex` then segfaults

Program~\ref{prog:P13} records that a killed `latexmk` can leave a NUL-filled
auxiliary file, and that the tell is an error naming an `.out`, `.aux` or
`.toc` rather than a `.tex`. This pass met the same trap in a second form, and
the recorded fix was **not wide enough**: the aux tree was cleared of `.aux`
files and the index files were left, so the next run began

```
No existing .aux file, so I'll make a simple one, and require run of *latex.
Latexmk: applying rule 'makeindex main-pl.idx'...
Scanning input file main-pl.idx....done (380 entries accepted, 0 rejected).
Segmentation fault
```

**`latexmk` runs `makeindex` before the first `pdflatex`** when a stale `.idx`
is newer than its `.ind`, so the leftover file is consumed before anything can
rewrite it. And the leftover was truncated rather than NUL-filled: `main-pl.idx`
stopped at exactly $20\,480$ bytes \dash{} a page boundary \dash{} in the middle
of the token `\index`, which is a half-flushed write buffer. `main-en-a4.idx`
ended at $8192$ bytes the same way. A partial `\indexentry` is what makeindex
died on.

So the rule is one clause wider than P13 recorded: **clear the whole aux tree,
`.idx`, `.ind` and `.ilg` included**, and note that the corruption is a *short*
file as often as a NUL-filled one.

**And the first measurement of it was wrong, by exactly the instrument defect
this file already records.** `grep -c $'\x00' main-pl.idx` reported that every
one of its 380 lines carried a NUL. Bash strings cannot hold a NUL, so
`$'\x00'` is the **empty string** and the command counts every line in the
file; re-measured in Python the four `.idx` files carry **zero** NUL bytes
between them. It is Program~\ref{prog:P14}'s misread-instrument class in a new
place: a shell quoting rule silently turned a specific test into a vacuous one,
which is Program~\ref{prog:P01}'s vacuous assertion arriving from the command
line. **A grep for a byte the shell cannot represent is not a grep for that
byte.**

#### The issue's own brief carries the P7 off-by-one, and the manifest does not

Reading issue \#46 as a checklist \dash{} Program~\ref{prog:P17}'s discipline
\dash{} turned up five stale pointers in its contract paragraph: the scaling
attributed to `[P24]` where the manifest says `[P25]`, the convex combination
to `[P18]` where the manifest says `[P19]`, the residual stream to `[P15]`
against `[P16]`, layer normalisation to `[P17]` against `[P18]`, and rotation
to `[F8, P8]` against `[F8, P9]`.

**The manifest is right in all five**, because the sweep before
Program~\ref{prog:P10} corrected it and the issues were generated on
26 August, before that. So this is the P7 insertion surviving in a **sixth**
file \dash{} after the trap catalogue, the manifest, the curriculum notes,
Appendix~B and the issues' trap lists \dash{} and for once it is demonstrably
*downstream* of a fix rather than beside one.

**Recorded rather than edited**, on Program~\ref{prog:P21}'s precedent: the
issues are generated from the manifest and the manifest is the source of
truth. The generalisable half is the one Program~\ref{prog:P27} stated about
`notes/02` §4 \dash{} **a sweep is as wide as the artefact somebody thought to
open** \dash{} with a clause added: **it is also as wide as the artefacts that
existed when it ran.** Anything generated from a source of truth before the
source was corrected still carries the defect, and nothing regenerates it.

And the checkbox saying *No Quiz (Foundation-only)* is stale in exactly the way
Programs~\ref{prog:P04}, \ref{prog:P14} and \ref{prog:P24} to \ref{prog:P29}
each found it stale. P32 has one, like all thirty-one before it.

#### The diagram-manifest budget is falsified, and the evidence was already in the book

Program~\ref{prog:P14} recorded a budget for the manifest column \dash{} keep
`len(key) + 9 + len(copy)` under about $48$ \dash{} and two passes have worked
against it. Program~\ref{prog:P27} measured its eight lines against it by hand.
Program~\ref{prog:P31} measured six of its eight at $52$ to $64$, found that
only one produced a box, and read the other five as latent defects that
\enquote{would have shipped}.

This pass wrote the brace-matching parser Program~\ref{prog:P27} said the job
needed, checked it against the macro's own definition \dash{}
`\mermaidfig` is `[3]` and the manifest line is `\texttt{#1.mmd} --- #3`, so
the third argument is the copy \dash{} and ran it over the book.
**153 of 284 manifest lines are at or over $48$, in a book with zero overfull
boxes.** F01's and F02's copy runs to $106$ and $130$ characters.

Program~\ref{prog:P27}'s note says a loose regex \enquote{silently captures
the caption as the copy and reports most of the book over budget}, and
discarded that measurement as wrong. **A correct parser reports the same
thing.** What is wrong is not the parser but the budget.

And the reason is one look at the finished page. The manifest is set with
`\@dottedtocline`, so an entry **wraps**: `f01-number-sets.mmd` occupies three
lines in Appendix~F and is perfectly well set. Ordinary prose in that column
has break opportunities and takes as many lines as it needs, so its total
length cannot be what overflows it.

**So the rule is retired rather than restated, and no check was added.** A
gate enforcing a figure that mispredicts more than half the book is worse than
no gate \dash{} it is the permanently-red ledger this file already refuses.
What actually overflows that column is an **unbreakable run**, which is why
Program~\ref{prog:P14}'s own instance was a 34-character *key* inside a
`\texttt{}` that cannot hyphenate; the recorded remedy, *rename the key*, was
right, and the character budget bolted onto it afterwards was a generalisation
nobody measured. Isolating the exact break-opportunity condition is open, and
is labelled judgement here rather than guessed at.

The immediate consequence for a drafting pass is smaller and better than the
rule it replaces: **keep the key short, and stop counting the copy.** P32's
eight lines were written against the old budget and happen to sit between $36$
and $47$, which is a fact about them and not evidence for anything.

#### One more instrument defect, and it is the same shape as the other two

Three times in this pass a measurement or an edit was made with a tool that
was quietly not doing what it looked like it was doing, and the third is the
plainest: a pass note written through a Python `"""..."""` string containing
`Program~\ref{...}`. **`\r` inside a non-raw Python string is a carriage
return**, so every one of those references was written as `Program~` + CR +
`ef{...}`. It survived because a later edit read the file with universal
newlines and wrote it back, silently turning the CR into a line break, so the
damage read as odd line wrapping rather than as a corrupted macro.

With the `grep -c $'\x00'` empty-pattern and the extract-and-run wrapper that
swallowed a comment, that is three in one pass, and they share a shape worth
naming: **each tool accepted the input and returned a plausible answer.**
None errored. The rule that catches all three is the one this book already
applies to its own frames \dash{} do not trust an instrument you have not
watched produce a *known* answer \dash{} and the cheap version of it here is
to write LaTeX through raw strings, `r"""..."""`, always.

Nothing reached the repository: the four programs, `CLAUDE.md` and both notes
files carry zero carriage returns, because those edits happened to use escaped
backslashes. That is luck rather than method, which is why it is written down.

#### Rule 2, and the placement that made it easy

Read by content first \dash{} node, caption and manifest copy, which is
Program~\ref{prog:P18}'s four places \dash{} and **all four figures close
their section, with the next section's heading below them.** So there is no
following frame for any of them to answer, and the P04/P07 case does not
arise in this program at all.

That is worth naming as a placement rather than as luck. A figure that
summarises a section is by construction the answer to that section's
questions, which is Program~\ref{prog:P22}'s finding; putting it *after* the
last of those questions has been answered makes the summary safe, where
putting it mid-section makes it a spoiler. In a program that assembles rather
than derives, every section ends on a result, so the summary placement is
available throughout \dash{} which is a property of Part IX and worth
expecting again in P33 and P34.

For the ninth pass running the last node of a three-rank chain needed no
correction afterwards, because Program~\ref{prog:P22}'s rule was applied while
drawing.

#### Layout

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, zero errors, zero unresolved references, no stranded openers, no
stranded headings and, after the seven rounds above, no orphaned cues.

**And the orphan-tail count did not move at all**: 29, 29, 21, 21, exactly the
pre-P32 figures. That is the eleventh time (F13, P07, P09, P12, P15, P17, P19,
P23, P28, P31, P32), and it is worth saying that here it was not free \dash{}
the seven rounds of lengthening are what bought it, against five programs
where the recorded rules applied while drafting were enough on their own.

Pages 1267 / 1287 / 1058 / 1070, from 1237 / 1257 / 1034 / 1048 \dash{} thirty
and thirty in the trade format, which is what a thirty-nine-frame program with
four figures costs.

### The notes sweep, August 2026 --- and a wrong fix of my own

Run before P33 rather than inside it, because the P32 pass found the P7
insertion's off-by-one surviving in a sixth file and the standing instruction
was to settle the notes against the destination briefs first. What it found is
larger than the item it was opened for, and one of its own corrections was
wrong.

#### The duplicate curriculum was deleted rather than corrected

`notes/01-curriculum.md` §§4--11 carried a **second copy of every program's
brief**, one per part, written before `tools/programs.json` existed. Thirty-three
of them, and from P7 onward **every title belonged to the next program**
\dash{} fourteen were verbatim the manifest's brief one number up.

Deleted, all 489 lines, on Program~\ref{prog:P12}'s precedent for the same
file's §19 dependency graph: **a corrected copy is the next thing to go stale at
the next insertion.** Each part keeps its framing prose and the sequence is read
from the manifest, which is where the rest of this repository already reads it.

Then the arithmetic that survives a deletion: the part ranges in every §§5--11
heading and in the §4 summary table, \enquote{Seven programs} where there are
eight, \enquote{(P1--P33)} where the book has thirty-four, and 2,370 frames
where the manifest sums to 2,418.

#### A sweep is as wide as the SECTION somebody opened, and then as wide as the ROWS

Program~\ref{prog:P27}'s pass found three stale pointers in `notes/02` §4 and
named the finding: **a sweep is as wide as the section somebody thought to
open**, because five passes had corrected owners in §3 and not one had opened
§4. This sweep is that finding one level down. §4 had **eight more** stale
pointers in rows P27's pass did not read, and §§1--2 and §5 had six between
them \dash{} a summary table naming four part ranges, all four wrong; the
verdict on Strang crediting the SVD to the eigenvalue program; the verdict on
Boyd sending convexity to the matrix-calculus program.

Every one was settled against the destination program's own brief, and **one of
them the shift would have got wrong**: §5 credits the $1/\sqrt{d_k}$ variance
argument to the program after the one it named, and the manifest gives it to
P25 \dash{} two further on. That is Program~\ref{prog:P10}'s rule earning its
keep for the second time, after item 24.

**The §3 headings are corrected and the §3 items are not**, and the distinction
is worth stating because the file's own warning did not have it: a part range is
settled against the manifest by arithmetic and cannot break anything, where an
item owner is a mix of hand-corrected and stale entries and a blanket renumber
would break the ones already right. The warning box said so as of this pass, and
it had itself gone stale \dash{} it named the optimisation heading as an example
of what to distrust, and Program~\ref{prog:P20}'s pass had corrected that heading
a month earlier.

#### And the biggest claim in both files was wrong by a factor of three

The sweep's own arithmetic turned it up. `notes/01-curriculum.md` opened by
estimating the book at **460--540 pages** for its 2,418 planned frames, and this
file repeated it as 470--550. Neither number had been looked at since
scaffolding.

**Measured: 1,811 teaching frames are written and they set 1,295 pages in the
trade format.** That is $\num{0.72}$ pages a frame against the estimate's
$\num{0.21}$, with one program and four appendices still to come. (The
measurement was 1,757 frames in 1,267 pages when it was first taken, before
P33; the ratio has not moved.)

And the reason is knowable rather than mysterious, which is what makes it worth
recording rather than merely correcting. **The estimate predates the Stroud
layout pass**, so a *frame* in it was a paragraph. A frame as built is a rule
across the measure, a margin badge, 17 pt above and 12 pt below, usually an
answer box, often a row of dots and a cue \dash{} and every program also carries
a Quiz, an outcomes panel, two to four figures, a Summary, Test exercises and
Further problems, with an answers appendix and a six-page index behind them.
The layout pass measured its own cost honestly, at two pages a format for
F01's cues; nobody went back and re-multiplied.

It matters because it is the premise of **the one decision this book still
records as open**. §20 item 1 now carries the measurement and the per-part page
ranges read out of the trade build's own running heads \dash{} front matter and
Part I at 388 pages, Parts II--VI at 494, Parts VII--IX as written at 413
\dash{} so the proposed Parts I--VI cut gives an **882-page first volume**,
which does not settle it either. At this geometry the book is nearer three
volumes than two, or the geometry has to change. The decision stays the
author's; what changed is that it now has numbers in front of it.

**The class is this file's oldest: a claim about the book that nothing derives
from anything.** It survived thirty-two program passes in the two documents the
next author reads first, and every one of those passes re-measured its page
counts and its overfull multiset from the build in front of it \dash{} because
those have a ledger and this did not. **When a number in one of these files is
derived from another number in the same file, derive it again.**

#### The one that matters: my own fix was the defect

The exclusions table said **P23** gives a diffusion model's forward process as a
Markov chain of Gaussians. P23 is *Probability and Bayes* and defines no random
variable, so this sweep moved it to **P24** on the shift.

**Neither program delivers it, and nothing in the book does.** A grep of all
forty-seven briefs finds no *Markov*, no *diffusion* and no *forward process*,
and a grep of the written programs finds none either. The corrected pointer was
as false as the one it replaced and it read better, which is worse.

That is Program~\ref{prog:P14}'s finding generalised: **replacing a wrong claim
with a plausible one is not automatically safe.** There it was a tally replaced
by a universal that was also false; here it is a pointer replaced by a pointer
that is also false. Both drafts were written from the feel of the destination
rather than from the destination, and the check is the same one either way
\dash{} open it.

The entry now says what is true on the F04/F08/P04 precedent: the book gives the
Gaussian and the fact that variances of independent quantities add, which is the
whole of a discrete-time chain of Gaussians, and **never applies them to one**.
The row's reason for excluding SDEs was always sound; only its pointer was
invented.

The same precedent settled the PAC-learning row, in the other direction. It owed
\enquote{one frame in P33} \dash{} and neither Part IX brief undertakes it,
while **P14 already delivers it**, eliciting what happens to a bound holding
\enquote{with probability at least 95 per cent} when a paper applies it once per
experiment. So the entry records a debt discharged rather than one owed, which
is the better sentence and was one `grep` away the whole time.

### Program P33 pass, August 2026

**Fifty-four teaching frames, fifty-six printed, both editions**, against a
brief that projected sixty. Eight sections: one step and six programs, which
of the six fail silently, a plateau, a spike, a suspiciously smooth descent,
the one shape that is diagnostic, the other curve, and what this program has
not checked.

Twenty-sixth program under its brief's estimate, and Part IX's contract is
again the reason rather than a shortfall \dash{} the program introduces no new
mathematics, so everything is spent by construction and the pass's whole job
was to find what was not.

#### The cleanest handover position any program in this book has had

`grep -rn 'prog:P33' programs/en/*.tex` was the first thing run, and it
returns **F03 and nothing else, twice** \dash{} and both deferrals are word
for word the two halves the brief calls this program's own:

- *\enquote{Program P33 reads a loss curve as evidence \dash{} what a plateau,
  a spike and a suspiciously smooth descent each imply, and which of them are
  distinguishable from noise.}*
- *\enquote{Program P33 treats such a fit as an empirical fit with a stated
  extrapolation error rather than as a law of nature.}*

Program~\ref{prog:P30} had eight programs pointing at it and had to sort the
machinery from the content; here there was nothing to sort. F03 owns the log
axis and the fact that a power law is a straight line on log-log axes with the
exponent as its gradient, and it never fits one \dash{} which is exactly the
P30 split, arriving pre-sorted because the deferring program wrote down both
halves when it made them.

**The six bracketed items are spent by construction**, each by a program whose
own header says so: P26 the loss as maximum likelihood, P18 its gradient as
$\vect{p} - \vect{y}$, P20 the optimiser with F04's average inside it, P01 the
arithmetic, P17 the boundary, F06 clipping outright with P21's noise model
behind it. None is re-taught.

#### So the assembly's own question is the one no owner could ask

Put the six in the order they execute and ask **which of them, got wrong,
raises nothing**. Two raise \dash{} P18's two-step route divides by zero, and
a step size above P17's boundary leaves \dash{} and four do not:

| piece | what being wrong costs | owner |
|---|---|---|
| the loss | $\val{p33.fail.ppl}$ times the true perplexity | P19 |
| the average | $\val{p33.conv.fold}$ times as long, or divergence | F04, P20 |
| the arithmetic | a gradient under $\val{p33.fail.swamp}$ per cent of the total moves nothing | P01 |
| the sample | a gradient of a different objective, by $\val{p33.fail.acc}$ | F04, P21 |

**Every one of the four is a correct computation of the wrong quantity**: a
mean of means is a mean, a rounded sum is a sum, a rescaled step is a step.
There is no invalid operation anywhere in them for anything to catch \dash{}
which is why the four silent ones are exactly the four that have to be
detected from outside, and there is one instrument for that. That sentence is
the bridge from §2 to §3 and it is the program's spine.

#### An assertion caught a self-comparison, inside the gate written to prevent one

The first draft of the step-size gate read
`assert ETA_STAR < 2 / LAM_HI`. **`p17.eta.star` IS $2/\lambda_{\max}$**
\dash{} the boundary, not the optimum \dash{} so that is a quantity compared
with itself, and it failed on the first run with `(0.1, 0.1)`.

Nothing else would have said so. The two print identically at two decimals,
which is Program~\ref{prog:P17}'s own recorded defect \dash{} a formula whose
two readings agree numerically stays invisible until the day they do not
\dash{} appearing inside a cross-programme gate written in that program's
honour. The gate now recomputes the boundary and asserts it reproduces P17's
committed figure, which is what a gate is for.

And the corrected reading produced §1's number: the optimum on that bowl is
$\val{p33.eta.best}$ and the boundary is $\val{p33.eta.bound}$, so
**a schedule spends its whole life inside a band $\val{p33.eta.margin}$ per
cent wide.** Reported at zero decimals because that is the only precision at
which the exact margin and the margin a reader computes from the two printed
figures agree \dash{} $\num{4.76}$ against $\num{5.00}$ at two \dash{} and
the `reproduces` guard was proved to fire on it by mutation.

#### A threshold chosen so a claim would pass, refuted for the fifth time

§7 first asserted `OUT_ERR > 20 * RESID`: the fit's error three decades out
against its residual inside the span. It failed at $\num{13.6}$, and the
failure is the better statement, because **what is true has no constant in
it.** The error outside the span grows with distance, monotonically, and is
unbounded; the error inside is bounded by the residual. Both are asserted now
and neither carries a number somebody chose.

The same correction went through the fit's own uncertainty. The claim is not
that its band is small \dash{} it is that **the truth lies outside it**, which
is checkable without a threshold and is what \enquote{an empirical fit with a
stated extrapolation error} turns out to be worth.

Programs~\ref{prog:F11}, \ref{prog:P15}, \ref{prog:P20} and \ref{prog:P21}
each paid for this rule. It has now been paid for five times, and the pattern
in all five is identical: the threshold is written to make a sentence the
author has already drafted come out true.

#### The plateau, which is the program's headline

Nothing is sampled anywhere in this program. Every answer in §§3--6 is a
statement about a normal distribution evaluated with `math.erf`, and the
noise model is not invented: a minibatch loss is a mean over $B$ examples of a
per-example loss whose spread Program~\ref{prog:P19} committed, so its spread
is Program~\ref{prog:P25}'s $\sigma/\sqrt{B}$ and nothing else.

| | |
|---|---|
| spread of one step's reported loss | $\val{p33.sigma.step}$ |
| chance a healthy run looks flat for $\val{p33.watch}$ steps | $\val{p33.p.flat}$ per cent |
| steps of flatness before it is evidence at $\val{p33.alpha}$ | about $\val{p33.plateau.k}$ |

**The run in the scenario is $\val{p33.drop.steps}$ steps long, so the flat
stretch would have to be three times the whole run before it meant anything.**
The frames say which half of that is measured and which is chosen \dash{} the
spread is Program~\ref{prog:P19}'s, the fall is a choice made to have
something to divide by \dash{} and then say that what the arithmetic delivers
is a *ratio*, so everything follows from the progress per step being far
smaller than the noise per step.

The figure is reported to two significant figures because five do not survive
the page: a reader multiplying the three printed operands gets $29\,080$ where
the exact answer is $29\,078$, and the script asserts both that the rounding
agrees and that the unrounded forms disagree \dash{} so the guard cannot go
quiet by accident.

#### The spike, gated to P27's own arithmetic

A long run contains large single-step deviations by construction:
$\val{p33.spike.expected}$ four-spread steps are expected in a
$\val{p33.steps}$-step run, and correcting for the run length puts the
surprising size at $\val{p33.spike.z}$ spreads.

That is Program~\ref{prog:P27}'s multiple-comparison arithmetic with steps in
place of models, so it is **gated rather than resembled**: the same routine
with forty in place of $\val{p33.steps}$ must return P27's committed
Bonferroni figure to the digit. Two programs that describe one correction
cannot come apart about it.

#### The smoother: P21 owns the lag and its own trapbox names the split

Program~\ref{prog:P21} §5 measures what smoothing does to *when* \dash{} it
moves every event later by exactly the half-life \dash{} and its trapbox ends
\enquote{read the raw curve when the question is \emph{when}, and the smoothed
one when the question is \emph{whether}}.

So this program owes the *whether*, and the answer is exact: an exponential
moving average of independent noise has variance $\frac{1-\beta}{1+\beta}$
times the raw variance, which is Program~\ref{prog:F04}'s geometric series, so
the picture shows $\val{p33.smooth.pct}$ per cent of the real spread at P21's
own $\beta$ and understates it by a factor of
$\val{p33.smooth.dash.times}$ at a dashboard's $\val{p33.beta.dash}$.

**The handover was written down in the program that owed it, for the fourth
pass running** (P29, P30, P31, P33), and the closed form is checked against
the series itself rather than against the same formula twice.

#### E10, run, and split the way Program P32 split E9

The ledger specifies E10 on \enquote{published numbers}. P32's question asked
of it: does the claim need external data, or is it a statement about the fit?

**The half that carries the argument needs nothing external.** How far a
power-law fit can be trusted past its last point is a property of the fit and
of the span, and it is exactly computable when the truth is known because the
script chose it. What a paper would add is one specific exponent, and the
frames say so rather than pretending the general claim needs it.

The truth is the form the literature itself uses \dash{} an irreducible loss
plus a power law \dash{} and a *pure* power law is fitted to it, which is what
everybody fits:

| | |
|---|---|
| largest miss over the fitted $\val{p33.fit.decades}$ decades | $\val{p33.fit.resid}$ per cent |
| true exponent against fitted exponent | $\val{p33.fit.alpha}$ against $\val{p33.fit.b}$ |
| prediction $\val{p33.fit.decades}$ decades out, truth $\val{p33.out.truth}$ | $\val{p33.out.fitted}$ |
| the fit's own two-standard-error band there | $\val{p33.fit.band.lo}$ to $\val{p33.fit.band.hi}$ |
| where the fit predicts a loss below the floor | $10^{\val{p33.absurd.dec}}$ |

Four findings, and the last two are the ones worth carrying. **The fit is
confident precisely because it is wrong**: a least-squares standard error is
built from the residuals, the data lie on a smooth curve, so the reported
uncertainty is tiny and the truth is outside the band it gives. And
**$\val{p33.absurd.past}$ decades past the last measured point the fitted line
predicts a loss below the irreducible floor** \dash{} not merely inaccurate
but impossible, from a fit whose residual is half of one per cent.

The least-squares routine is gated of Program~\ref{prog:P09}'s third kind:
two programs must not be able to disagree about what a least-squares line is,
so it has to return Program~\ref{prog:P08}'s committed slope, intercept and
sum of squares on P08's own three hand-checkable points.

#### The extract-and-run harness was the defect again

The transcript is a REPL session defining `phi` on one line, so it carries a
`...` continuation. The first replay harness fed only the `>>> ` lines, so
`phi` was never defined and it reported `NameError` \dash{} **against a
listing that runs perfectly**.

That is Program~\ref{prog:P32}'s finding recurring one program later, and in
the same medium: an instrument that accepts the input and returns a plausible
answer. The rule it earned there is the one that settles it here \dash{} what
comes out of a transcript is REPL input, so run it in a REPL, and feed the
continuation lines too. Replayed correctly it prints $\num{0.489}$ and
$\num{0.05}$, which is what the page prints.

**And the listing moved for Program~\ref{prog:P23}'s rule.** It was first
placed after the frame that answers the $\val{p33.watch}$-step question
\dash{} and its second line prints $\num{0.05}$ at $29\,000$, which is the
answer to a question two frames later. A transcript may not answer a question
put to the reader anywhere later in the program. Moved below that answer,
where it is the reader's own check rather than the reveal.

#### A markdown-only pull request runs no CI, and \enquote{pending} reads as a queue

Recorded because it cost twelve minutes of the wrong kind of waiting, and
because it is this file's own instrument-misread class arriving through a new
door.

The notes sweep that preceded this pass touched three `.md` files and nothing
else. `build.yml` carries `paths-ignore: ['docs/**', '**.md']`, so **no
workflow was triggered at all** \dash{} and the API's answer to \enquote{what
is the status} is `state: pending, total_count: 0`, which is exactly what it
answers while a check is queued.

The two states are indistinguishable from that call. What distinguishes them
is one look at the workflow's own `on:` block, and the rule is the one
Program~\ref{prog:P23} stated about `\raggedbottom`: **before waiting for a
mechanism, confirm the mechanism is running.** An unchanged reading is
evidence that nothing is happening, not that something is happening slowly.

> **And the first draft of this very note got the mechanism wrong, which is
> why it is worth reading twice.** It said a markdown-only *push* runs
> nothing. It does not: on a `pull_request` event GitHub evaluates
> `paths-ignore` against **the PR's whole diff**, base to head, not against
> the newest commit. So a markdown-only *PR* runs nothing \dash{} which is
> what the notes sweep was, three `.md` files and no others \dash{} while a
> markdown-only *push to a PR that already touches code* runs the full
> matrix. This pass's own last push was two `.md` files onto a PR full of
> `.tex`, and all four jobs queued immediately, which is how the error was
> caught.
>
> It is the pass's own theme arriving one level up: the claim was written
> from the feel of the mechanism rather than from the mechanism, and what
> settled it was reading `build.yml` \dash{} eight lines, four seconds. The
> corrected rule is more useful than the wrong one, because it tells you
> *which* PRs are exposed: **check the shape of the whole diff, not of the
> push.**

#### Rule 2, and the figures

| | W (en / pl) | ratio | en | pl | en A4 | pl A4 |
|---|---|---|---|---|---|---|
| P33.1 six-pieces | 592 / 642 | 2.98 | 7.45 | 6.87 | 8.46 | 7.80 |
| P33.2 flat-or-stuck | 592 / 571 | 3.23 | 7.45 | 7.73 | 8.46 | 8.77 |
| P33.3 smooth-hides | 609 / 606 | 3.06 | 7.24 | 7.28 | 8.22 | 8.26 |
| P33.4 inside-outside | 624 / 636 | 2.89 | 7.07 | 6.94 | 8.03 | 7.87 |

All eight at three ranks and all well above the aspect-ratio crossover on the
first render, because the width was measured before the prose was written
\dash{} which is Program~\ref{prog:P32}'s explicit lesson and cost one
`pdfinfo` per file.

**And the fourth figure had to be reworded twice, in two of the four places
Program~\ref{prog:P18} says to read.** Its middle node ended
\enquote{\dots and nothing in the fit bounds it}, which is a claim about the
*fit's own uncertainty* \dash{} and the frame two later asks what that
uncertainty is about. Its **caption** then said \enquote{only the first is
supported by the residual}, which hands the reader the answer's noun outright.
Neither is the last node of a three-rank chain, which is where the previous
five passes found the spoiler; both are one rank and one line away from it.

So the node now says what frames 44 to 46 deliver \dash{} the miss grows with
every decade until the line predicts a loss below the floor \dash{} and the
caption says *inside the span it is measured; outside it, guessed*, which is
the section's thesis without its evidence. The generalisable half is
Program~\ref{prog:P11}'s, restated: **the caption is a node, and it is the one
you have already stopped reading as one.**

The other three needed nothing. All four close by restating what the frames
above them deliver, and each sits above a question it does not answer: the
step-size margin, the probability of a flat stretch, which program owns
divergence, and what the reported uncertainty is about. That is the P04/P07
case for the sixteenth time \dash{} a figure the reader is meant to *apply*
belongs above the question.

#### Half of a two-edition edit did not land, and the build found it forty minutes later

Round 3 of the cue walk lengthened frame 52 \dash{} in both editions, as every
recorded lengthening must be. **Only the English reached the file.** Round 4
then rebuilt all four formats, and `main-pl-a4` reported the cue on
**exactly the page it had reported in round 3**, because the Polish file had
not changed and the Polish A4 build was therefore the same book.

An identical measurement after a change is this file's own signal that the
change did not reach what was measured, and its second reading \dash{} *the
fix did not reach* rather than *the fix was too small* \dash{} is again the
right one. But nothing needed inferring, because **the gate had already named
it**: `FAIL [C14-macros] P33-training-run.tex: \S: en=2 pl=1; \ref: en=51
pl=50`. One `\S\ref{}` in one edition and not the other is a paragraph in one
edition and not the other, stated in six characters.

**The finding is where that line was.** `make all-formats` runs the gates
*after* it has built four PDFs, so a parity failure introduced by the very
edit that triggered the build is not reported until the build ends. The whole
of round 4 \dash{} four formats, four thousand pages \dash{} was spent on a
tree with a known-failing gate in it, and the gate's own output was sitting
inside the log the build was still writing.

The remedy is the *order* this file's own \enquote{After each pass} list
already gives: **the source-level gates before the build, not inside it.**
They run in seconds against a build that runs in tens of minutes, and they
read the source rather than the artefact \dash{} so they are the only ones
that can be run before there is an artefact. Every previous pass happened to
do it that way and none had recorded why it matters.

**And the same shape cost a CI cycle in the same pass, which is what makes it
a finding rather than an anecdote.** `make debt` failed on the pushed head
with `quiz has 6 items and 0 answers`, in both editions: P33's six Quiz items
carried their `\teachesat{}` routes and no `\answerto{}`, so a reader taking
the entry Quiz had nothing to check against. It is a real defect, it is
mechanically detectable, `check\_structure.py --answers` detects it in under a
second \dash{} and it was found by a CI job rather than by the author,
because `make debt` had not been run since the Quiz was written.

So the two instances are one instance: **a check that reads the source was
run at artefact time.** One sat inside a forty-minute local build; the other
sat in CI, on a job this file's own Build section describes as
\enquote{advisory}, which is exactly the word that stops somebody running it.
Neither needed a PDF. The habit worth keeping is narrower than
\enquote{run the gates}: **before launching a build, run every gate that
would not need the build**, which here is `parity.py`, both halves of
`check\_structure.py`, and `make debt`.

#### Layout, and a cue walk whose fourth round measured nothing

| round | edit | result |
|---|---|---|
| 1 | lengthened frame 52, both editions | `main-pl` cleared |
| 2 | lengthened frame 31, both editions | `main-en-a4` cleared |
| 3 | lengthened frame 52 again \dash{} **English only, unnoticed** | \dash{} |
| 4 | none that reached a file | `main-pl-a4` reported its cue on **the same page as round 3** |
| 5 | the Polish half of round 3, plus the two rule-2 rewords | all four clean |

**Round 4 is the one worth keeping, and it is not the random walk this file
keeps recording.** Every previous wasted round moved the defect somewhere
else; this one moved nothing, because the edit it was measuring did not
exist. The two are distinguishable in one look \dash{} a defect that has
moved is on a different page, and a defect that was never touched is on the
same one to the digit.

Every edit that landed was a **lengthening**, in both editions: twentieth and
twenty-first confirmations of Program~\ref{prog:F06}'s two-sided rule, which
has still never failed. The paragraph frame 52 gained says the thing the
section most needs and had not said: **a run's own logged losses \emph{are}
the sample.** Fit the trend, take the residuals, and ask how often they exceed
three and four spreads against what a normal distribution predicts. Nobody
does it, the data is already on disk, and the answer would turn every number
in \S3 from a model into a measurement.

The overfull multiset came back element for element to the baseline in all
four builds \dash{} `[]`, `[]`, `[6.3]`, `[]` \dash{} with zero overfull
vboxes, zero errors, zero unresolved references, no stranded openers, no
stranded headings and no orphaned cues. **One orphan tail added, in
`main-en-a4`**: 29, 29, 22, 21 against the pre-P33 29, 29, 21, 21.

Pages 1295 / 1313 / 1080 / 1094, from 1267 / 1287 / 1058 / 1070 \dash{}
twenty-eight and twenty-six in the trade format, which is what a fifty-four
frame program with four figures and six new back-matter answers costs.

#### Also

- Traps 313 to 320 added to `notes/02`, under one shape: every one is a
  question asked of the loss curve that the loss curve cannot answer.
- **Elicitation 51%**, level with the book's own rate, from **ten**
  P06-pattern conversions that added **no
  frames at all** \dash{} the draft measured 33%. Every conversion took a
  frame that stated something the reader could produce, moved the statement
  into the next frame's answer, and ended the first frame by asking. That
  makes the retrofit free here where Program~\ref{prog:P24} paid nine frames
  for ten points, and the difference is that these were conversions of
  *statements* rather than additions of *questions*.
- **Diagram widths measured before the prose**, which is P32's explicit
  lesson, and all eight renders landed in the band on the first attempt
  \dash{} 571 to 642 pt, ratios 2.98 to 3.23, node text 6.87 to 8.77 pt. No
  redesign, and the rule cost one `pdfinfo` per file.
- **Five parity divergences and every one was the same recorded class**: an
  English possessive attached to a reference, which inverts in Polish. Four
  were in prose and one in a table cell. It is still the single most reliable
  thing to check for while translating.
- The four Polish shape names are **taken from F03's own Polish twin**, which
  defers here by name \dash{} `plateau`, `skok`, `podejrzanie gładki spadek`
  \dash{} so the cross-reference lands in the reader's own vocabulary.
- The listing was extracted from the finished `main-en.pdf` and replayed
  through `code.InteractiveInterpreter`: it prints $\num{0.489}$ and
  $\num{0.05}$, which is what the page prints.
- Frame numbers mapped after writing: sections landed at
  `1--8 / 9--14 / 15--21 / 22--27 / 28--33 / 34--37 / 38--50 / 51--54`.
- **The Quiz's six back-matter answers were missing** and CI's ledger job
  found them, which is written up above. They add nothing to the body
  \dash{} `\answerto` typesets at the back \dash{} so no frame, no cue and
  no body page moved, and CI compiled all four formats green with them in.
- C7 reported five unused values and all five emissions were cut on
  Program~\ref{prog:F11}'s finding: two were gate inputs, two were superseded
  by figures the page expresses another way, and one was a count the page
  writes in words.

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
  **P24–P25**, two parts later. **Discharged, in two halves, exactly as
  declared**: P24 returned the definition, on P21's own population and gated
  against its committed mean, and said in as many words that the $1/B$ rate is
  P25's; P25 derived the rate in two steps from its own section 1 and gated it
  against P21's committed population spread, so neither program can now be
  corrected without the other noticing. It is the book's oldest declared
  forward reference and it is closed.
- **P10** and **P11** use the covariance matrix, defined in **P24**. They need
  two facts from it — symmetric, positive semi-definite — and say so, **and
  both prove them where they stand**, so the pointer was always an attribution
  rather than a debt. P24 records that as the rule: a forward reference whose
  facts can be proved locally should be.
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

- **P07** (tensors and shapes) prints $\operatorname{Cov}(p, t)$ and
  $\operatorname{Var}(t)$ in its headline broadcasting identity and declared
  neither; both are defined in **P24**. Found by the same check that found the
  fifth, carried as outstanding because it is in a merged program, and
  **closed in the P24 pass** \dash{} one clause in P07's Learning outcomes, in
  both editions, on the P21 pattern. It also settled the rule the entry was
  left open on, and the answer is neither of the two that were offered:
  **declare anything the reader must be able to check.** P07's identity is
  *stated in terms of* the two, so a reader who has not met them cannot verify
  the line the section rests on, which is the bar P18 and P22 were held to; an
  object merely used and not named would not need it.

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
   quotes exists, and every cue is the last thing in its frame. And
   `--scripts`, which `make check` runs: every `\transcript{}` names a file
   that is there
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

1. **One program.** F1 to F13 and P1 to P33, both editions. What remains is
   P34 and the appendices.

   **P34 is next** \dash{} *Measuring a model honestly* \dash{} and Part IX's
   contract still holds: it introduces **no new mathematics**. Read
   `tools/programs.json` for its brief and then do what the last seven passes
   did: **read the brief as a checklist and read the neighbours' file headers
   with it.** That question has been cheaper than \enquote{what is left of
   the subject} eight times running, and P33 is the cleanest case yet
   \dash{} the only program that defers to it is F03, which wrote down both
   halves of what it was leaving when it left them, so there was nothing to
   sort.

   **P34's brief brackets six handovers and at least four are visibly
   spent**, which is worth knowing before estimating it: the bootstrap, the
   paired comparison and the power calculation are Program~\ref{prog:P27} in
   full, the judge model's stated probability is Program~\ref{prog:P28}'s
   §6, cost per token is Program~\ref{prog:P03}'s, and the limits of the
   information-theoretic measures are Programs~\ref{prog:P29} to
   \ref{prog:P31}'s. What is left is the **design** \dash{} an evaluation
   read as an estimation problem rather than as a score \dash{} and the
   closing discipline both companion volumes are built on. Its estimate is
   fifty-five and Part IX's two written programs came in at thirty-nine and
   fifty-four against seventy and sixty.

   **Part IX is a different job from the eight parts before it**, and the
   estimates should not be read the same way. Every program so far came in
   under its brief because a neighbour had spent the machinery or the
   content; a program that assembles what the book already has is made
   entirely of that, so the question is not what is left but **what order the
   pieces go in**. P32 bears that out: it came in at thirty-nine against
   seventy, and the shortfall is the contract working rather than a thin
   program.

   **P32 settled the real-architecture question, and the answer generalises to
   P33 and P34.** Three programs had pointed here asking for a hypothesis
   checked on a trained model. What P32 found is that the question splits:
   the **assembly** half of Program~\ref{prog:P25}'s scaling needs no model
   at all \dash{} $q \cdot k = x\T M y$ has variance exactly
   $\lVert M\rVert_F^{2}$, so one weight draw settles it in closed form
   \dash{} while the **training** half does. So the assembly half was
   derived and the training half is stated as outstanding, on
   Programs~\ref{prog:P08}, \ref{prog:P11}, \ref{prog:P19},
   \ref{prog:P20}, \ref{prog:P25} and \ref{prog:P31}'s precedent.
   **Ask that split of every claim P33 and P34 inherit**: a surprising
   amount of what looks as though it needs a model turns out to be a
   statement about shapes, and the part of it that genuinely needs one is
   then worth stating plainly rather than hedging the whole claim.


   **Part III still leaves one measurement outstanding, deliberately.** P11's
   brief asks for the singular-value spectrum of a real embedding matrix,
   measured; the program constructs one, labels it, and says the empirical
   claim is not settled. With P08's rank-collapse warning that is **one debt
   with two entries**, and both need a trained model's real matrices. It is
   the first item in this book that cannot be done from a sandbox at all.
   **P19 added a third entry of the same kind** \dash{} whether the basin a
   walk lands in matters at the scale people train at \dash{} and **P20 a
   fourth**, since it declines to say whether Adam reaches a better answer
   than momentum on a real surface. **P25 added a fifth**: E9 is measured on
   random vectors, and whether the derivation's independence hypothesis
   survives training was P32's to check on an assembled architecture.

   **P32 halved that fifth entry rather than adding to it**, and the way it
   did so is the thing to carry into P33 and P34. The question split: the
   *assembly* half needed no model, because through a block the score is a
   bilinear form whose variance is exactly $\lVert M\rVert_F^{2}$ and one
   weight draw settles it in closed form; only the *training* half \dash{}
   whether the independence assumption survives a run \dash{} still needs
   one. **Ask that split of every remaining claim before accepting that it
   needs a model.** So the debt is one trained model away from being five
   answers rather than one, and one of the five is now half answered.

   **And there is still a Part II-shaped job that is nobody's program.** The
   elicitation ledger puts P01, P02 and P03 at 29--31% against Part I's
   73--78%, and raising them is a pass of its own: it means finding, in three
   merged programs, the frames that state something the reader could produce,
   and moving the statement into the next frame's answer. P04 did three of
   those and went 26% to 35% without adding a frame; P23 did ten and went 33%
   to 53% for two frames, which is the measurement to plan against.
   **P26, P27, P28 and P29 were four consecutive demonstrations that the rate
   is free when it is designed in**: 52%, 53%, 54% and **55%** with no
   conversions at all, because all four frame plans were written that way
   \dash{} and P29 is the highest outside Part I. **P30 broke the run and
   priced the alternative a third time**: its plan came in at 41%, and six
   conversions took it to 52% for two frames. So the three data points now
   read P23 two frames for twenty points, P24 nine for ten, P30 two for
   eleven \dash{} retrofitting is cheap when the frames are short and dear
   when they are long, and designing it in is still free. **P31 paid two
   frames for six points**, applying the conversions to the draft before the
   frame remap, which is P23's lesson and is why it cost one renumbering
   rather than two. **This is the largest genuinely
   parallelisable job in the repository**, because it touches three merged
   program files and nothing else; the programs themselves are not
   parallelisable, for the reason the frame estimates below record.

   Before estimating any remaining program's length, read its written
   neighbours. F7's brief projected forty frames and thirty-one were needed;
   **F8's forty-five against thirty**; **F9's forty against thirty-two**;
   **F12's fifty-five against thirty-one**; **P14's forty-five against
   thirty-one**, because the subject is genuinely small; **P15's fifty-five
   against thirty-eight**; **P16's sixty-five against thirty-eight**,
   because P06 had already measured its central result under another name;
   **P17's fifty against thirty-eight**, because P15 and P10 between
   them had left only the model and the inequality; **P18's sixty
   against thirty-nine**, because it defines no new object at all;
   **P19's forty-five against thirty-eight**, because F04 had already worked
   its headline demonstration; **P20's sixty-five against forty-two**,
   because four written programs had each already delivered one of its
   ingredients; **P21's fifty against thirty-nine**, because F06, F04 and
   P20 between them had left it only the noise model; and **P22's against
   thirty-five**, because P15 and P05 had left it only the multiplier; and
   **P23's fifty-five against forty-seven**, the smallest shortfall in a long
   while, because its ground was genuinely unspent and its neighbours supplied
   *objects* rather than machinery or content. **P24 broke the run: sixty
   against sixty-four**, and for a reason that is not about content at all
   \dash{} its draft came in at fifty-five, in line with the seventeen before
   it, and nine frames were added raising the elicitation rate from 36% to 46%.
   **And P25 landed on its estimate**, fifty-four against fifty-five, which is
   the first time in nineteen \dash{} and the hypothesis for why is that its
   brief is one of the five the curriculum review amended, so it is the only
   one written after somebody had looked at what its neighbours would spend.
   **P26 went back under, fifty-five against forty-six**, which is consistent
   with that: its brief was not amended, and five written programs had each
   delivered one of its ingredients. **P27 is the largest shortfall in Part VII,
   sixty against thirty-nine**, and it is the first with a cause that is not
   about the subject at all: two of the seven things its brief itemised were
   already on the page, by name, in Program~\ref{prog:P25} §4. **P28 came in
   at thirty-seven against fifty** with every one of its brief's five payoffs
   still owed \dash{} the neighbours had supplied only the machinery, and the
   program defines no new object at all. **P29 came in at thirty-four against
   forty-five**, for P27's reason rather than any of the other three: read as
   a checklist, two of its three payoffs turned out to be handed here **by
   name**, in the headers of Programs~\ref{prog:P19} and \ref{prog:P25},
   which had written down what they were leaving. **P30 came in at forty-six
   against fifty-five**, for the same reason once more \dash{} but with its
   two halves separated, which is worth having: its *machinery* was entirely
   spent (P29's coding argument, P26's likelihood, P18's derivative, P19's
   Jensen, F09's triangle inequality with its equality condition) while its
   *content* was untouched, since no written program mentions mode-covering,
   mode-seeking or Jensen--Shannon at all. So four of its eight sections were
   short because the tools were already there and four were full length
   because nobody had been there. **P31 came in at thirty-eight against
   fifty**, the same shape once more and at its most extreme: mutual
   information IS Program~\ref{prog:P30}'s divergence applied to one pair of
   arguments, so the program defines exactly one new object in six sections
   and its first three are short by construction. P30's own closing frame had
   already said where the length goes, and two thirds of the program is where
   it said. **P32 came in at thirty-nine against seventy**, the largest
   shortfall in the book, and it is the only one that is not a shortfall at
   all: Part IX's contract is that it introduces no new mathematics, so
   \emph{everything} was spent by construction and the pass's whole job was
   to find the three things that were not. A Part IX estimate measures the
   assembly rather than the subject, and should not be read against the
   twenty-four before it. **P33 came in at fifty-four against sixty**, which
   is the smallest shortfall Part IX will produce and is the same contract
   read from the other end: its brief bracketed six pieces and all six were
   spent, so what remained was the *order* they go in and the one question
   no owner could ask \dash{} which of the six, got wrong, raises nothing.
   That question is the program, and it is long because the answer is four.
   **A brief's frame estimate is otherwise a planning figure from before its
   neighbours were written**, and the elicitation rate is paid in frames on top
   of it. It is not a target \dash{} and the record above is also the reason
   the programs cannot be written in parallel: each one is shaped by what the
   ones before it turned out to spend.
2. **The measurements.** Ten are specified, nine of them free. **E6 was run in
   the P20 pass and E9 in the P25 pass**, and the ledger in
   `notes/01-curriculum.md` §17 now carries a Status column naming the pass
   rather than a total in prose \dash{} it said "none has been run" for five
   programs after E6 had. Fill the column in the pass that runs one.

   **E4 needs a trained model** and is the same debt as item 1's. Three rows
   \dash{} E1, E3 and E5 \dash{} say "see the note below" because P02, P05
   and P16 each measured something that closely resembles the specification
   beside them and no pass claimed it; deciding those is a reading job on three
   merged programs and is not an inference to make from the table. The rest are
   unclaimed and free: E2, E7, E8 and E10.

   Also outstanding: raise the frame estimates' credibility by writing down,
   in the pass, which neighbour spent what. Nineteen programs now have that
   record and it is the reason each estimate missed.
3. **Appendices C–F.** C (formula reference) is the one that fixes Stroud's
   fair criticism that a book of frames is a useless reference.
4. **The residual sweep.** Fourteen committed values are measured
   floating-point residuals rather than invariants — every key ending `.err`
   across F05, F07, F08, F09, F12 and P05, plus the figures quoted beside them.
   CI rejected two of P06's for exactly this and they are now emitted as
   bounds; the rest have survived so far, which is not the same as being
   reproducible. See the build trap. It is a pass of its own, because each is
   quoted in prose in two editions.
5. **`odzera`, the companion library.** One stage per part, every gradient
   checked against finite differences in CI, no GPU, the whole suite under a
   minute. Specified in `notes/01-curriculum.md` §18; nothing built.
6. **Reader validation.** Nobody has read this. Until somebody has, the 80/80
   ledger stays open and the book may not claim it.

**One decision still open**, recorded in `notes/01-curriculum.md` §20: whether
this is one volume or two. **Its stated premise is falsified**: 470–550 pages
for ≈2,418 frames is 0.21 pages a frame, and the written book measures **0.72**
\dash{} 1,811 teaching frames in 1,295 trade pages, with one program and four
appendices still to come. §20 item 1 now carries the measurement and the
per-part page ranges, so the decision has a number rather than an estimate. The
other two that
stood beside it are now settled in the passes that wrote their programs
\dash{} P12's placement, and whether P14 is enough of a fix for the rigour gap
\dash{} and each entry records the argument the written book falsified rather
than only the answer.
