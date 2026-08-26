# CLAUDE.md — working on this book

Context for continuing *Matematyka od zera dla inżyniera AI* /
*Mathematics from Zero for the AI Engineer*.
Read this before touching a program.

---

## Status

| | Done | Remaining |
|---|---|---|
| Structure | Both mains, shared preamble, `structure.tex`, Makefile, CI, parity tooling, Mermaid pipeline | — |
| Front matter | Title page, *How to use this book*, Introduction — **both editions** | — |
| Programs | **F1 written, both editions.** F2–F13 and P1–P34 are stubs carrying their briefs | 46 of 47 |
| Appendices | A (answers, generated) and B (notation) drafted; C–F are stubs | C, D, E, F |

Both editions build clean: `latexmk -pdf main-en.tex` and `main-pl.tex` each
return 0. **English 169 pages, Polish 171 pages, zero errors, zero warnings,
zero overfull vboxes, four overfull hboxes of at most 4.1 pt.** Parity reports
**0 failures and 0 warnings** across 56 file pairs; `reflist.py` confirms 66
labels resolve to the same numbers in both editions.

**Debt ledgers, reported by CI on every build** (`make debt`):

- **46 of 47 programs are stubs**, in each language. This is the whole of the
  remaining work and it dwarfs everything else.
- 0 exercises without an answer · 0 programs outside the 30–70 frame band ·
  0 programs without declared learning outcomes
- 29 computed values, all referenced, all present
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

**Watch the margin.** 17 cm page. Anything over ~15 pt is a defect; the current
worst is 4.1 pt. Count vboxes as well as hboxes — an overfull **vbox** means a
boxed block grew past a page and could not break, and the fix is to split the
table, not to shrink the text.

---

## Two editions, one source

`main-en.tex` and `main-pl.tex` differ in `\booklang` and in which language's
directories they read. Everything structural is shared exactly once:

```
preamble.tex        all machinery, both editions
lang/en.tex         every user-visible string + the notation contract
lang/pl.tex         the same macro set, or CI fails
structure.tex       THE part and program sequence. One list, both editions.
figures/values/     computed numbers, committed, shared
code/               the scripts that produce them
programs/{en,pl}/   the only place prose is duplicated
```

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
| C3 lang catalogue | A label defined in one language only — an undefined control sequence in exactly one build |
| **C4 ordered structural signature** | `\yourturn` moved from frame 2 to frame 3. A histogram cannot see reordering; every Summary back-reference and Quiz route navigates by frame number |
| C5 labels, C6 answer keys | `T3` must be the *same question* in both, not merely the third one |
| C7 values | A `\val{}` with no script behind it, and a computed value nothing uses |
| **C8 per-frame maths digest** | A sign fixed in one edition only. Changes no count and no histogram |
| C10 notation lint | The contract below, enforced with a file and a line |
| **C12 numeric literals, in order, strictly** | A translated number silently changing |
| C13 verbatim ASCII | The `listings` UTF-8 trap |
| C14 macro histogram | A `\trapbox` or an `\index` dropped in translation |
| **C15 main-file wiring** | A main file rewritten with a chapter of front matter dropped |
| `reflist.py` | `\label{prog:F08}` resolving to F8 in one edition and F9 in the other. Both builds stay internally consistent and neither warns |

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
review of the curriculum found four, and the rule is now that each is stated in
the owning program's Learning outcomes with a pointer:

- **P21** (stochastic optimisation) needs random variables and variance from
  **P24–P25**, two parts later. P25 revisits minibatch noise once the machinery
  exists.
- **P10** and **P11** use the covariance matrix, defined in **P24**. They need
  two facts from it — symmetric, positive semi-definite — and say so.
- **P18** (matrix calculus) carries the book's most reused derivation, the
  softmax–cross-entropy gradient, and cross-entropy is not defined until
  **P30**. P18 gives it a definitional frame; P26 and P30 each return to it.

Anything else is a dependency error, not a forward reference.

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
make            # numbers, diagrams, then both editions, then the three gates
make en         # English only, and check its log properly
make pl         # Polish only
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

- `https://konradcinkusz.github.io/math-for-ai-engineers/book-en.pdf`
- `https://konradcinkusz.github.io/math-for-ai-engineers/book-pl.pdf`

It duplicates the compile steps from `build.yml` on purpose, and runs
`checklog.py` against its own logs rather than trusting another workflow's:
Pages must never publish a PDF that did not build.

CI runs the numbers job first and gates everything on it, then parity as a hard
gate, then the two editions in a matrix, then a cross-reference comparison out of
the two `.aux` files. The ledgers are advisory and are published to the step
summary on every build.

**After each pass:**

1. `make` — zero errors, zero warnings, zero unresolved references
2. `python3 tools/checklog.py main-en.log main-pl.log` — **not** `grep '^!'`
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
