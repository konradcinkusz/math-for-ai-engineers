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
| Programs | **F1 written, both editions.** F2–F13 and P1–P34 are stubs carrying their briefs | 46 of 47 |
| Appendices | A (answers, generated) and B (notation) drafted; C–F are stubs | C, D, E, F |

**Two languages times two paper formats, four PDFs, all clean.** A4 at 12pt is
the format the book is read in; 17 x 24 cm is the trade format shared with the
companion volumes.

| | Pages | Errors | Unresolved | Overfull hbox | Overfull vbox |
|---|---|---|---|---|---|
| `main-en` (17x24) | 175 | 0 | 0 | 4, worst 4.1 pt | 0 |
| `main-pl` (17x24) | 175 | 0 | 0 | 4, worst 4.1 pt | 0 |
| `main-en-a4` | 167 | 0 | 0 | 5, worst 6.3 pt | 0 |
| `main-pl-a4` | 167 | 0 | 0 | 4, worst 4.4 pt | 0 |

The 6.3 pt box is `$7\,000\,000\,000$` in F1, which cannot break; it exists in
one format and one language because that is where the line falls. Well under
the 15 pt budget. Parity reports **0 failures and 0 warnings** across 56 file
pairs; `reflist.py` confirms 66 labels resolve to the same numbers in both
editions.

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

- **46 of 47 programs are stubs**, in each language. This is the whole of the
  remaining work and it dwarfs everything else.
- 0 exercises without an answer · 0 programs outside the 30–70 frame band ·
  0 programs without declared learning outcomes
- 28 computed values, all referenced, all present
- 0 `verifybox` blocks · 6 Mermaid sources, all rendering
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
| `check_structure.py --frames` | A cue that is not the **last thing** in its frame. C16 counts cues and cannot see position, so a cue misplaced identically in both editions is invisible to C4, C14 and C16 alike. It is a *line* test on purpose: a cue hoisted above a frame's closing prose tokenises to nothing after it and reads as correctly placed |
| `reflist.py` | `\label{prog:F08}` resolving to F8 in one edition and F9 in the other. Both builds stay internally consistent and neither warns |
| **`checkpdf.py`** | A frame's rule and margin badge stranded at the foot of a page with the frame's body overleaf. It reads the finished PDF, because that defect produces no error, no warning and no overfull box — no log can see it, and the badge it strands is the book's navigation device |

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

**The trap catalogue** — 38 misconceptions AI engineers actually hold, each
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
3. `python3 tools/parity.py` — zero failures before you commit
4. `make debt` — confirm the ledgers moved the way you expected
5. Update the Status table and the ledgers at the top of this file

Note on tagging: `git push --tags` returns HTTP 403 through the sandbox's git
proxy, so tags created in a web session exist locally only. Tag from a local
clone instead.

---

## What is left

1. **Forty-six programs.** This is the work. F2–F13 first, because the
   Foundation part is what makes the book's claim — *it assumes nothing* — true
   or false, and because F3 (logarithms) and F12 (the chain rule) are the two
   the rest of the book leans on hardest.
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
