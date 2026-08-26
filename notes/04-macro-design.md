# `macros.tex` — design note

Programmed-learning machinery for *Matematyka od zera dla inżyniera AI* /
*Mathematics from Zero for the AI Engineer*, implementing K. A. Stroud's format
as an extension of the house preamble in `/home/user/llm-book/preamble.tex`.

Everything below was compiled. Nothing here is proposed and untested; where
something is untested it says so, under **Residual risks**.

---

## Status: what was actually built and run

pdflatex only, TeX Live 2023, five separate builds, three passes each, all under
`-halt-on-error` — the flag the house CI uses, which turns a warning-shaped
problem into no PDF at all.

| Build | What it proves | Pages | Errors | Overfull hbox | Overfull vbox | Duplicate hyperref anchors | Unresolved refs |
|---|---|---|---|---|---|---|---|
| `test/` | drop-in on the **unmodified** llm-book `preamble.tex` | 21 | 0 | 0 | 0 | 0 | 0 |
| `test/pl/` | Polish edition from the same source | 21 | 0 | 0 | 0 | 0 | 0 |
| `test/degraded/` | `siunitx` **and** `mathtools` absent | 21 | 0 | 0 | 0 | 0 | 0 |
| `test/standalone/` | **no house preamble at all** | 5 | 0 | 0 | 0 | 0 | 0 |
| `test/stress/` | 13 Foundation Programs, **580 frames**, F1–F13 then 1 | 175 | 0 | 0 | 0 | 0 | 0 |

The stress build is the one that matters. Thirteen Programs of forty frames
(F13 has sixty), each with outcomes, a quiz, a summary, a "Can you?", test
exercises and further problems, plus 91 answers collected to the back and
grouped by Program. **Zero overfull boxes of either kind.** Every `mfa` audit
warning it emits is one I planted.

The remaining test builds emit exactly the defects deliberately planted in them:
an exercise without a solution, a `\val` key with no computed value, Programs
below the frame floor.

---

## 1. A Program is a `\chapter`

Reusing `\chapter` rather than inventing `\program` from nothing is the decision
everything else rests on. `titlesec`, `fancyhdr`, `\include`, the ToC, `\label`,
`\ref`, `\autoref` and the PDF bookmarks all keep working, because nothing about
the sectioning machinery changes. Only the **printed representation of the
counter** does.

```latex
\part{Foundation}
\foundationprograms          % F1, F2, ... F13
\program[Series]{Series, Convergence and Divergence}

\part{Main Programs}
\mainprograms                % 1, 2, ... n
```

`\program[short]{long}` wraps `\chapter[short]{long}`, records the title for the
answers section, resets the audit flags, and closes the previous Program's audit.

### The trap this creates, and it is invisible

Resetting `\c@chapter` at the Part boundary makes F1 and Program 1 **both chapter
number 1**. `\thechapter` distinguishes them; hyperref does not use
`\thechapter`. It builds anchor names from `\theH<counter>`, so both claim
`chapter.1`, and so do `figure.1.1`, `equation.1.3` and every other counter that
numbers within the chapter.

The symptoms are a pile of `destination with the same identifier has been used`
warnings, PDF bookmarks that open the wrong Program, and `\autoref` links that
land a hundred pages away. **Nothing fails the build.** You find out from a
reader.

The fix is an anchor prefix that is never empty and always distinct:

```latex
\def\theHchapter{\mfa@Hprefix\arabic{chapter}}   % F1.. / M1.. / A1..
\def\theHsection{\theHchapter.\arabic{section}}
\def\theHfigure{\theHchapter.\arabic{figure}}
...
```

`\mfa@prefix` is what the reader sees (`F`, or nothing); `\mfa@Hprefix` is what
hyperref sees (`F`, `M`, `A`) and is never empty. `\appendix` is patched with
`\apptocmd` rather than redefined, because book.cls owns `\thechapter` there and
only the `\theH` half needs adding.

Measured: **0 duplicate destinations** across a document containing F1–F13,
Program 1 and Appendix A.

### Three more numbering traps, all fixed

- **The ToC number column.** `book.cls` sets `\l@chapter`'s number box to
  `1.5em`, which fits `12` and not `F13`. Section numbers become `F13.10`, which
  needs about `3.4em` against the stock `2.3em`. Left alone, the number runs into
  the title in the contents and in the list of figures — and the log says nothing,
  because nothing overflows a *line*, it just collides. Patched with
  `\patchcmd` on the literal `1.5em`, and `\l@section` / `\l@subsection` /
  `\l@figure` redefined with wider columns. Verified in the stress build's ToC,
  where F13's title wraps cleanly around a number that fits.
- **`\chaptername` and babel.** babel installs its own `\chaptername` when the
  language is selected, which happens at `\begin{document}` — *after* the
  preamble. Setting it in the preamble works right up until somebody installs
  `texlive-lang-polish`, at which point it silently reverts to "Chapter". Set
  inside `\AtBeginDocument`, which runs after babel's own hook.
- **`\chaptermark` and fancyhdr.** The house `CLAUDE.md` already records that
  `\ps@fancy` installs its own `\chaptermark`, so a redefinition before
  `\pagestyle{fancy}` is silently discarded. Rather than depend on `macros.tex`
  being input after `preamble.tex`, this file **re-issues `\pagestyle{fancy}`
  immediately before its own redefinition**. `\pagestyle` is idempotent, so this
  is free, and it removes an ordering dependency between two files instead of
  documenting one.

`\mfaprefixsep` is empty by default; set it to `{.}` for Stroud's own `F.1`.

---

## 2. The frame

```latex
\begin{fr}
Body.
\end{fr}

\begin{fr}[$\dfrac{1}{1-r}$]     % the previous frame's answer
Body.
\end{fr}
```

Two letters. This is typed forty to seventy times per Program — roughly fifteen
hundred times in the book — and any longer name is a tax on every page. `fr`
rather than `frame` is forced as well as chosen: the LaTeX kernel already defines
`\frame`, so `\newenvironment{frame}` is an error.

### Not a tcolorbox

A breakable `tcolorbox` per frame would be slow at fifteen hundred instances,
would fight page breaking, and would draw a container around something that is
not a container. A frame is a numbered position in a stream. Stroud sets frames
as a stream separated by a rule with the number in the margin, and so does this —
which also means a frame breaks across a page for free, with no code at all.

### Not a `\marginpar`

The frame number is set in a **zero-width box overlapping into the left margin**,
not a margin note. `\marginpar` was the obvious alternative and is the wrong
tool: margin notes are floats, they migrate when they land near a page break, and
they are silently dropped inside boxes and lists. Losing one frame number in a
stream of fifty is a defect a proofreader will not catch. A zero-width overlap
cannot migrate, cannot be dropped, and cannot produce an overfull box warning.

The cost is that the number alternates between the inner (2.2 cm) and outer
(1.8 cm) margin on facing pages. Stroud does that anyway. A two-digit bold number
plus a 0.9 em gap is about 20 pt against 51 pt of outer margin, so there is
plenty of room.

`\framenumbersinline` switches to a lead-in number instead, for anyone who
disagrees; `\framenumbersinmargin` switches back. Both are tested.

Inside a frame, `\clubpenalty` and `\widowpenalty` are set to 9999. Two lines of
a frame stranded at the foot of a page is worse than a slightly loose page, and
this is the cheapest possible fix.

`\refstepcounter{progframe}` means `\label` inside a frame yields the bare frame
number, which is exactly what the summary's square brackets want.

---

## 3. The answer at the head of the next frame

`\ans{...}`, or equivalently the optional argument of `fr`.

```latex
\begin{fr}[No. It diverges.]
If you said yes, you are in good company and you are wrong.
```

It sets the answer in a distinct weight and colour, then draws a **short rule
under it**. The rule is the "cover above this line" cue — the physical card the
reader is told to use has to land somewhere, and a full-width rule would be
confusable with the frame separator above it.

Deliberately **not a box of any kind**. Display mathematics is a common answer
and has to be allowed to break out of the paragraph; a `minipage` or a `tcolorbox`
would forbid that and would also forbid the answer breaking across a page.
`\leavevmode` rather than `\noindent` so that `\ans` works both as the first
thing in a frame (already in horizontal mode, just after the frame number) and
free-standing.

The optional-argument form is canonical because it guarantees the answer is at
the very top and cannot drift down the frame in a later edit. `\ans` remains
available as the escape hatch — see **Residual risks** for when you need it.

---

## 4. The row of dots

```latex
so the derivative is \blank
so the derivative is \blank[3cm]
\[ y = \blank[2.5cm] \]
\dispblank                          % centred, on its own line
```

A fixed-width run of dot leaders in an `\hbox`. Fixed width rather than
`\dotfill`, for two reasons: `\dotfill` eats the whole line and gives the reader
no clue how long the answer is, and a dotted run that stretches differently on
every line reads as a typesetting fault rather than a device.

`\ifmmode` makes it work inside display maths, which is where most of the blanks
in this book will live.

---

## 5. Outcomes and "Can you?" are the same list

The brief requires the "Can you?" checklist to be 1:1 with the entry outcomes.
Rather than make that a rule somebody has to keep, **they are one list**:

```latex
\learningoutcomes{
  \outcome[1--9]{state the ratio test and apply it}
  \outcome[10--18]{say why the harmonic series diverges}
}
...
\canyou
```

`\outcome` appends to a store; `\learningoutcomes` renders the store as the entry
list; `\canyou` re-renders **the same store** as the exit grid. They cannot drift,
because there is only one of them. This is the same argument as `\pyregion` in
the house preamble: if the book and the thing it describes must agree, do not
typeset them twice.

The optional argument is the frame range. The entry list ignores it — the reader
has not read the frames yet and a range would be noise. The exit checklist prints
it, because a 4 or a 5 needs somewhere to go back to.

### The rating grid is a list, not a table

The house `CLAUDE.md` says to count overfull **vboxes** as well as hboxes, and
the reason is precisely this construct: a centred `tabularx` inside an admonition
cannot break across a page, so a checklist of eight two-line outcomes overflows by
hundreds of points and the only fix is to split the table.

So the grid is not a table. Each outcome is a list item; the five rating boxes are
inline, each carrying its own digit. It breaks wherever it likes, and it needs no
alignment between a header row and the rows beneath it. The same reasoning governs
`summary`. **The stress build has zero overfull vboxes**, with thirteen of these.

---

## 6. Quiz, summary, exercises

**`quiz`** — Foundation only, enforced. A quiz in Part II is a sign the Program
has been written as revision. It is a warning rather than an error, because a
draft has to be allowed to compile. The frame range against each item is the whole
point: the quiz is diagnostic on entry and the exit test on the way out, so a
reader who gets item three wrong must be told which frames to work. The hint is
set flush right *on its own line*, so a long question and a long hint cannot fight
for the same line and produce an overfull hbox.

**`summary`** — `\sitem[7]{...}` prints the frame number flush right in square
brackets, so the summary doubles as a return index. Both forms work:

```latex
\sitem[7]{A geometric series converges iff $|r|<1$.}
\sitem[\ref{fr:harmonic}]{The harmonic series diverges.}
```

The `\ref` form is the one that survives inserting a frame later, and it works
because the frame environment does `\refstepcounter`. The bracket uses the
standard end-of-proof idiom, so it moves onto a line of its own only when it will
not fit.

**`testexercises` / `furtherproblems`** — ordinary `enumerate` lists that count
their own items and their own solutions and complain if the two disagree:

```
Package mfa Warning: Program F1 Further problems: 2 exercises but 1 solutions
```

Counting this in LaTeX rather than in the Makefile is worth the code: a grep
cannot tell which `\item` a `\solution` belongs to, and this can. Items are counted
by wrapping `\item` — `\stepcounter` expands to nothing, so `\@ifnextchar`'s
lookahead for `\item`'s optional argument still sees the right token.

---

## 7. Answers at the back — and why `\addcontentsline` cannot be used

Same `\@starttoc` trick as the house `.dgm` and `.shots` manifests, with a new
extension `.ans`. `\listofanswers` in the back matter prints them, grouped by
Program.

**The `.ans` file contains digits and nothing else:**

```
\mfa@ansgroupline {F1}
\mfa@ansline {1}{6}
\mfa@ansline {2}{6}
```

The answer *body* is stored in a global macro keyed by a serial number, at the
point of use. Only the key and the page are written to the file. That split is the
whole design, and there are two independent reasons for it.

**Reason one: catcodes.** The obvious implementation writes the answer text
itself through `\addcontentsline` into the `.aux`. Do that and every answer goes
through `\protected@write`, where a bare `%` comments out the rest of the line, a
`#` has to be doubled, and anything with unusual catcodes cannot survive at all.
In a book whose answers are almost entirely mathematics, that is a class of defect
nobody would find until it was in print. Storing the body in a macro avoids all of
it: the body is never written to a file, never re-read, never re-tokenised. It is
also always current, because it comes from *this* run rather than the last one —
only the ordering and the paging come from the previous run.

**Reason two, subtler: hyperref.** `hyperref` wraps the **text** argument of
`\contentsline` in a link before handing it to `\l@<type>`, so a handler that
expects a lookup key receives
`\hyper@linkstart{link}{anchor}{key}\hyper@linkend` instead, and the lookup
silently fails. The house preamble's `.dgm` and `.shots` ledgers are safe from
this only because they reuse `\l@subsection`, whose text argument is *meant* to be
a link. **A key-lookup ledger cannot use `\addcontentsline`.** It has to go one
level down, to `\addtocontents`, which writes `\@writefile{ans}{...}` directly and
never involves `\contentsline` at all.

Grouping by Program is emitted once per Program, guarded by comparing an `\edef`
of `\thechapter` against a global "last Program written" macro.

### Two bugs this design flushed out, both caught by compiling

Both were *silently wrong output*, not errors, and both are the same mistake:
**capturing something at print time that should have been frozen at capture
time.**

1. The group heading was stored with `\gdef` as
   `{\mfastrProgram\ \thechapter\ \ \mfa@progtitle}`. Both `\thechapter` and
   `\mfa@progtitle` have moved on by the time the back matter is typeset, so
   *every* group heading in the book read **"Program A — Vectors and Vector
   Spaces"** — the last chapter of the appendix, and the last Program's title.
   Fixed with `\protected@xdef`.
2. The answer label was stored as `\noexpand\mfa@setabbrev~\arabic{mfaex}`, and
   `\mfa@setabbrev` is defined *inside* `testexercises`, so by the answers section
   it was undefined. That one at least announced itself — as **"Undefined control
   sequence" reported against `main.ans`, a generated file, with no line in any
   source to look at**. Fixed by expanding it with `\protected@edef` at capture
   and `\global\let`-ing the result.

Both now render correctly in English (`TE 1`, `FP 1`) and in Polish (`Ćw. 1`,
`Zad. 1` — note the `\protected@edef` carries UTF-8 through inputenc's `\IeC`
correctly), across 91 answers in thirteen groups in the stress build.

### The write-stream budget

pdfTeX has sixteen `\write` streams. This book already spends them on `.aux`, the
`\include` part-aux, `.toc`, `.lof`, hyperref's `.out`, imakeidx's index, and (if
inherited) `.dgm` and `.shots`. Adding `.ans` makes about nine. There is room, but
not unlimited room: **count before adding a tenth and an eleventh**, because
running out produces `No room for a new \write` and nothing that points at the
cause. This is one reason the computed-value ledger below reads a file instead of
opening a stream.

---

## 8. `\programstub{}`

Mirrors the house `\chapterstub{}` exactly — a red dashed box reading NOT YET
WRITTEN, so an unfinished Program cannot be mistaken for a finished one and the
page count never flatters the draft. It additionally sets a flag that switches off
the frame-count audit, because a stub with no frames is expected rather than
defective.

---

## 9. Admonitions

`dotnetbox` goes: there is no .NET reader here. Four replace it. The rest of the
house vocabulary is kept unchanged, because a stable vocabulary across the
author's books is worth more than a locally optimal one.

| Box | Title | Why it exists |
|---|---|---|
| `trapbox` | The usual mistake | **The load-bearing one.** Stroud's method depends on eliciting a wrong answer and correcting it before it sets. It is visually distinct from `warning` — framed, not barred — because they feel the same and mean different things: a `warning` is about a hazard you should avoid, a `trapbox` is about an error you have probably just made. Always placed **after** the question, never before it, or the device does not work. |
| `notationbox` | Notation: Polish and English | Polish and English mathematical notation genuinely differ: `tg`/`ctg` against `tan`/`cot`, a decimal comma against a point, `NWD`/`NWW` against `gcd`/`lcm`, half-open intervals written with an angle bracket. A bilingual book that ignores this teaches one audience to write things its own tooling will reject. It doubles as the translator's checklist. |
| `aibox` | Why this matters for AI | The reason this book exists rather than Stroud. Every technique earns its place by being used: log-sum-exp for softmax overflow, the chain rule for backpropagation, eigenvalues for PCA. A reader who skips every one still gets a complete mathematics course; a reader who reads only these gets the motivation and none of the method. Both are legitimate, which is why it is a box and not a paragraph. |
| `rigourbox` | What is being skipped | Stroud's own stated limitation is that he proves nothing. This book keeps the method and refuses to pretend the gap is not there: what is asserted without proof, why that is the right trade for this reader, and which book to open when it stops being. |
| `verifybox` | This number has not been computed | Retitled, not redefined. Marks a numeric claim no script has produced. See §10. |

**`rigourbox` is not debt.** It is a permanent, deliberate statement. It must
never be counted in a ledger or "cleared" — the one thing that would ruin it is
somebody treating it as a to-do. This is worth writing into `CLAUDE.md` before the
first `make debt` runs, because every other box in the house style *is* debt.

**Considered and rejected:** a `recallbox` ("you met this in F3"). Programmed
learning is heavily cross-referential and the temptation is real, but a box for
every backward reference would be one per page. `\xfref{fr:key}` (below) does the
job inline and costs nothing.

The six inherited boxes are defined **only if absent**, so this file is a drop-in
on the unmodified house preamble *and* works standalone. `\ifcsname` rather than
`\@ifundefined`, because the bodies contain `#1` — see the trap in §11.

---

## 10. The verification convention: every number comes from a script

The maths analogue of the house's "run the listing, or mark it".

> **Every number in this book is either an exact value the reader can check by
> hand in one line, or a value produced by a script in `code/` and imported. There
> is no third category.** A number typed into a Program because it looked right is
> the maths equivalent of a listing nobody ran.

```
code/f03/harmonic.py     prints  \definevalue{f03-harmonic-1000}{7.485470860550343}
make values              collects every script's output into generated/values.tex
\val{f03-harmonic-1000}  pulls it into the book
CI                       make values && git diff --exit-code generated/values.tex
```

**The last line is what makes it a guarantee rather than a habit.** If a script's
output no longer matches what is committed, the build fails and names the key. The
book and the script cannot drift, in the same way `\pyregion` means a listing and
the repository cannot drift.

`generated/values.tex` is **committed**, unlike the rendered diagrams, for two
reasons: the book must build for somebody who has not got Python, and a changed
number is exactly the sort of thing that should appear in a diff.

### What this buys the bilingual edition, for free

Values are stored in machine form and rendered through `siunitx`:

| Source | English build | Polish build |
|---|---|---|
| `\definevalue{f03-harmonic-1000}{7.485470860550343}` | `7.4855` | `7,4855` |

One source, both decimal markers, `\valplaces{2}` to change precision at the point
of use. All four cells above are from the compiled PDFs.

`\valtext{key}` bypasses `siunitx` for anything it would choke on — a verdict, an
interval, an exact fraction.

A missing key is **loud and non-fatal**: it prints `[?? key-name]` in red, emits a
package warning naming the key, and increments a counter reported at the end of
the run. A draft must build; a missing number must be impossible to miss.

Keys use **hyphens**. An underscore in `\val{a_b}` is a subscript in text mode and
produces "Missing $ inserted", a confusing error a long way from its cause. The
generator should reject a key containing one.

### `siunitx` detail worth keeping

`group-digits=integer` is not optional. `siunitx` groups digits on **both** sides
of the decimal marker by default, so `7.4855` sets as `7.485 5` — which looks like
a typesetting fault and is wrong in both languages. Found by reading the compiled
output, not by reading the manual.

---

## 11. The trap that cost a build, and the general rule behind it

This one is worth its own section because the house's own graceful-degradation
convention leads you straight into it.

```latex
\IfFileExists{siunitx.sty}{\newcommand{\x}[1]{\num{#1}}}{\newcommand{\x}[1]{#1}}
```

> `! Illegal parameter number in definition of \reserved@a.`

A real error. Under `-halt-on-error` — which the house CI uses — that is **no
PDF**, and the message names `\reserved@a`, which appears nowhere in anything you
wrote. Minimally reproduced; a single-line `\IfFileExists{f}{\renewcommand{\aaa}[1]{A#1}}{}`
is enough.

The rule, established by testing each case rather than by reading the kernel:

| Construct | `#1` in a branch | Why |
|---|---|---|
| `\IfFileExists{f}{...#1...}{...}` | **fatal** | the branch reaches a `\def\reserved@a{...}`, and a `#` in a macro body must be `##` |
| `\@ifpackageloaded{p}{...#1...}{...}` | safe | branches go through `\@firstoftwo`, which only *reads* them as arguments |
| `\ifcsname x\endcsname\else ...#1... \fi` | safe | conditional text is never an argument to anything |
| `\newcommand{\m}[3]{\IfFileExists{fig/#1.pdf}{...#1...}{...}}` | safe | `#1` is substituted **before** `\IfFileExists` reads the branch |

The last row is why the house preamble's `\mermaidfig` has never tripped over
this, and why the trap looks like it does not exist until the day a *fallback*
needs to define a macro with an argument — which is exactly what a fallback for
`\num` or `\shortintertext` requires.

**The fix, used in both places in `macros.tex`:** set a flag inside the branch,
and do the defining outside it.

```latex
\newcommand{\mfa@fmtnum}[1]{#1}                       % the fallback IS the definition
\newif\ifmfa@siunitx
\@ifpackageloaded{siunitx}{\mfa@siunitxtrue}{\IfFileExists{siunitx.sty}{\mfa@siunitxtrue}{}}
\ifmfa@siunitx
  \renewcommand{\mfa@fmtnum}[1]{\num{#1}}             % siunitx upgrades it
\fi
```

This belongs in the new book's `CLAUDE.md` next to the U+00A0 entry. It is the
same shape of problem: an obvious thing to write, fatal, and the error names
neither the cause nor the line.

### Every other house trap, respected

- **No `literate` mapping for U+00A0.** `macros.tex` adds no `literate` entries at
  all; it inherits the house `lccode` style untouched.
- **babel is not loaded here.** `preamble.tex` already probes for `polish.ldf` and
  `british.ldf` before requesting either, because babel with a missing language
  file is fatal rather than a warning. Loading it twice, or simplifying that probe
  away, is how you lose an afternoon. The language switch in `macros.tex`
  (`\mfabooklang`) is independent of babel and drives only the strings the
  machinery emits and the `siunitx` decimal marker.
- **`\chaptermark` after `\pagestyle{fancy}`** — handled by re-issuing
  `\pagestyle{fancy}`, as above.
- **Underscores in `\code{}`/`\api{}`/`\pkg{}` written `\_`** — unchanged, and
  `\val` keys are barred from containing one at all.
- **Overfull vboxes counted, not just hboxes** — and designed against, by using
  lists rather than `tabularx` for the two constructs that would otherwise grow
  past a page.

---

## 12. Bilingual machinery

One line in `main.tex`:

```latex
\def\mfabooklang{pl}
\input{macros}
```

Every fixed string the *machinery* emits goes through one table of `\ifmfapl`
one-liners: Program, Learning outcomes, Quiz, Frames, Summary, Can you?, Test
exercises, Further problems, Answers, the four new box titles, and the
`TE`/`FP` answer abbreviations. Prose is selected by separate Program trees;
this table only covers the words nobody would otherwise own. Keeping them in one
place is what stops an English "Test exercises" heading appearing in the Polish
edition six months after nobody remembers where it came from.

A plain `\newif`, not an `etoolbox` toggle, so the switch costs nothing and works
if `etoolbox` is somehow absent.

Polish also gets `\appendixname`, `\contentsname`, `\indexname`, `\figurename`,
`\tablename` and `\partname`, all inside `\AtBeginDocument` for the babel reason
above.

---

## 13. Cross-Program frame references

Frame numbers restart at 1 in every Program, so "Frame 12" is ambiguous the moment
it is written in a different Program from the frame it names — and this book will
cross-reference constantly. `\ref` cannot help; it stores the frame number and
nothing else. This surfaced in testing as `\frefrange` cheerfully rendering
**"Frames 2–2"** for two frames in different Parts.

```latex
\begin{fr}[...]
\framelabel{fr:harmonic}      % instead of \label
...
\xfref{fr:harmonic}           % -> "Program F1, frame 3"
```

`\framelabel` labels the frame and additionally records which Program it was in, by
writing a line into the `.aux`. That line is executed when the `.aux` is read at
`\begin{document}`, so the information is available from the second run onwards,
exactly like `\ref` itself. Note that `\@writefile` is gobbled during that read and
ordinary macros are not, which is why this is a bare `\protected@write` rather than
an `\addtocontents`.

`\fref` remains for same-Program references, which is most of them.

---

## 14. Ledgers: what LaTeX counts and what the Makefile greps

Debt is counted, not remembered. The split is deliberate: **a grep gets what a grep
can see; everything else is counted by LaTeX and emitted as a package warning.**

LaTeX counts, per Program:

- frames outside the 30–70 range (`\mfaminframes` / `\mfamaxframes`)
- outcomes declared but `\canyou` never called
- a Foundation Program with no quiz
- a Program with no summary
- exercises whose count does not match their solutions
- `\val` keys with no computed value
- solutions recorded when `\listofanswers` was never called

CI reads them out of the log with one line:

```bash
grep 'Package mfa Warning' main.log
```

### Makefile

```make
PROGRAMS := $(wildcard programs/*.tex)

values:
	@mkdir -p generated
	@python3 tools/collect_values.py > generated/values.tex

stubs:
	@grep -rln '\\programstub{' programs appendices 2>/dev/null | sed 's/^/STUB: /' || true

frames:
	@for f in $(PROGRAMS); do \
	   n=$$(grep -c '\\begin{fr}' "$$f"); \
	   printf '%-44s %3d' "$$f" "$$n"; \
	   [ "$$n" -lt 30 ] && printf '   <- under the floor'; \
	   [ "$$n" -gt 70 ] && printf '   <- over the ceiling'; \
	   echo; \
	 done

vals:
	@grep -rhoE '\\val(text)?\{[^}]*\}' programs appendices \
	  | sed -E 's/.*\{(.*)\}/\1/' | sort -u > .used-keys
	@grep -oE '\\definevalue\{[^}]*\}' generated/values.tex \
	  | sed -E 's/.*\{(.*)\}/\1/' | sort -u > .have-keys
	@comm -23 .used-keys .have-keys | sed 's/^/MISSING VALUE: /'
	@comm -13 .used-keys .have-keys | sed 's/^/UNUSED VALUE:  /'
	@rm -f .used-keys .have-keys

debt: stubs frames vals
	@printf "== verifybox blocks: "
	@grep -rc 'begin{verifybox}' programs appendices 2>/dev/null \
	  | awk -F: '{s+=$$2} END {print s+0}'
	@echo "== audit warnings from the last build =="
	@grep 'Package mfa Warning' main.log 2>/dev/null || echo "  none"

clean:
	latexmk -C
	rm -f *.ans *.dgm *.shots *.ilg *.ind *.idx
```

Add `*.ans` to `.gitignore`. Do **not** gitignore `generated/values.tex`.

### CI

Two additions to the house workflow. The first is the guarantee that makes §10
real:

```yaml
  values:
    name: Recompute every number in the book
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v5
        with: { python-version: '3.13' }
      - run: make values
      - name: The book and the scripts must agree
        run: |
          if ! git diff --exit-code generated/values.tex; then
            echo "::error::A computed value changed. Commit generated/values.tex,"
            echo "::error::or fix the script. The book may not disagree with code/."
            exit 1
          fi
```

The second publishes the audit to the step summary, alongside the house's existing
stub and verifybox ledgers:

```yaml
      - name: Programmed-learning audit
        if: always()
        run: |
          {
            echo "### Programmed-learning audit"; echo ""
            if grep -q 'Package mfa Warning' main.log; then
              echo '```'; grep -A1 'Package mfa Warning' main.log; echo '```'
            else
              echo "_Clean._"
            fi
            echo ""; echo "### Frames per Program"; echo ""
            echo '```'; make -s frames; echo '```'
          } >> "$GITHUB_STEP_SUMMARY"
```

---

## 15. On the 80/80 standard

Stroud's validation claim is that at least 80% of students score at least 80%.
That is a **measurement**, and by the house rule it needs a method and a number or
an explicit label as judgement. Until a cohort has actually been tested, the book
may say Stroud's method was validated to 80/80 and **may not say this book was**.
The machinery supports collecting the data — the quiz is one environment reused on
entry and exit, and the "Can you?" is 1:1 by construction — but the machinery
cannot supply the number, and an empty table stays empty.

---

## 16. Residual risks I could not eliminate

Ordered by how likely you are to meet them.

1. **`\begin{fr}[...]` breaks on an unbraced `]`.** `\begin{fr}[$[0,1]$]`
   terminates the optional argument early. This is the standard LaTeX
   optional-argument limitation and cannot be fixed without a different syntax.
   Mitigation: brace it — `\begin{fr}[{$[0,1]$}]` — or use free-standing `\ans{}`,
   which takes a mandatory argument and has no such problem. Interval notation in
   an answer is not a rare case in a maths book, so **this will happen**; it is
   worth a line in `CLAUDE.md`.
2. **Answers cannot contain verbatim.** `\solution{...}` captures its body with
   `\gdef`, so catcodes are fixed at capture. Mathematics is entirely fine; a
   listing or a `\verb` is not. If a worked answer ever needs code, it has to be
   `\input` at the point of use or referenced rather than reproduced.
3. **Two runs before answers appear.** Identical to the table of contents, and
   `latexmk` handles it, but somebody running `pdflatex` once on a fresh checkout
   will see an empty Answers chapter and think it is broken.
4. **`\l@chapter` is patched by matching the literal `1.5em`.** If a future
   `book.cls` changes that literal the patch fails; it warns (greppable, as
   `Package mfa Warning`), but the ToC then silently reverts to a number column too
   narrow for `F13`. Low probability, silent consequence.
5. **The `\val` guarantee assumes deterministic scripts.** A Monte Carlo estimate
   must be seeded or `git diff --exit-code` fails on every run and the team
   disables the job — which is worse than not having it. That is a discipline
   requirement on `code/`, and LaTeX cannot enforce it. Write it into `CLAUDE.md`
   as a rule about scripts, not about the book.
6. **A third numbering scheme would need a fourth anchor prefix.** `F`, `M` and `A`
   are hard-coded in `\foundationprograms`, `\mainprograms` and the `\appendix`
   patch. Adding, say, a second appendix series without choosing a new prefix
   reintroduces the silent duplicate-anchor bug of §1. The prefixes are all set in
   one place, which is the best mitigation available.
7. **`\outcome` outside `\learningoutcomes` accumulates silently** into the next
   Program's list. `\program` clears the store, which limits the blast radius to
   one Program, but nothing detects it.
8. **`\protected@xdef` of the answers group heading expands the Program title.** A
   title containing a genuinely fragile command that is not `\protect`-aware would
   fail there rather than in the chapter head. Titles are plain text in practice;
   the risk is real but small.
9. **A frame beginning with a display equation** puts the margin number on a line
   of its own. Cosmetic, but it will look like a mistake. Start frames with text,
   or use `\framenumbersinline` for that Program.
10. **The Polish edition's babel main language is not solved here.** The house
    preamble hard-codes `[polish,main=british]`. A real Polish edition needs
    `main=polish`, which is a `preamble.tex` change and interacts with the
    fatal-babel probe. `macros.tex` deliberately does not touch babel.
11. **Not tested: `\include`, `imakeidx` with shell-escape, and `mermaid` figures
    inside a frame.** All three are inherited house machinery and none of them
    interacts with anything new here, but "should be fine" is not "was run", and
    this book's own rule is that the difference matters.

---

## 17. File layout this assumes

```
main.tex                 \input{preamble} then \input{macros}
preamble.tex             the house preamble, minus dotnetbox,
                         with verifybox retitled
macros.tex               this file
generated/values.tex     COMMITTED. written by `make values`
code/f03/harmonic.py     prints \definevalue lines
programs/f01-....tex     one Program per file
appendices/
figures/mermaid/*.mmd    committed; figures/diagrams/*.pdf gitignored
tools/collect_values.py
```

`tools/collect_values.py` runs every script under `code/`, asserts that keys are
unique and contain no underscore, and writes the `\definevalue` lines in sorted
order so the CI diff is stable.
