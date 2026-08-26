# Bilingual architecture and the Polish notation contract

*Matematyka od zera dla inżyniera AI* / *Mathematics from Zero for the AI Engineer*

Design note, August 2026. Written against the repository as it stood at
`b4320e0` plus the scaffolding in progress, with every claim about the build
executed rather than assumed.

> **Concurrency note.** A sibling session was writing to
> `/home/user/math-for-ai-engineers` while this was being written. `structure.tex`,
> the program stubs, `frontmatter/*/introduction.tex` and a `Makefile` appeared
> mid-pass. Where that changed a recommendation, it is marked. One naming
> collision is outstanding and is flagged in §1.9.

---

## Part 0 — What is already true, and what turned out not to be

Three things were verified by running them, not by reading them. Two were
defects in a scaffold that reported itself as clean.

### 0.1 The smoke build was green and broken

`_smoke.pdf` existed at 12 pages and `grep -c '^!' _smoke.log` returned `0`.
The build was not clean. `preamble.tex` line 702 raised

```
./preamble.tex:702: Illegal parameter number in definition of \reserved@a.
```

because `#1` appeared inside an `\IfFileExists` branch:

```latex
\IfFileExists{siunitx.sty}{%
  \usepackage{siunitx}%
  \sisetup{ output-decimal-marker = {\mfadecimalmarker} }%
  \newcommand{\mfanum}[1]{\num{#1}}%     % <- illegal here
}{%
  \newcommand{\mfanum}[1]{#1}%           % <- and here
}
```

`\IfFileExists` stores its branches in `\reserved@a`, so `#1` is read as a
parameter of *that* macro. The branches need `##1`. **Fixed** and verified: with
`##1`, `\val{f01.eps64}` sets `2,220446049250313 · 10⁻¹⁶` in the Polish edition
and `2.220446049250313 × 10⁻¹⁶` in the English one.

The consequence is worth stating plainly, because it is the argument for the
whole of §1.7: **siunitx never loaded, so the decimal comma — the single most
visible thing about a Polish mathematics book — silently did not work, in a
build everybody believed was green.**

Two things hid it, and both are general:

- `-interaction=nonstopmode` recovers from errors and still writes a PDF.
- With file-line-error formatting an error line begins with a *path*, not with
  `!`. The sibling books' habit of `grep '^!' main.log` cannot see it.

`tools/checklog.py` exists because of this and matches both formats.

### 0.2 `\ifpl` is fragile and broke the English edition

`structure.tex` writes part titles as `\part{\ifpl{Teoria informacji}{Information theory}}`.
`\ifpl` is a plain `\newcommand`, so it is fragile: it lands **unexpanded** in
the `.toc`/`.aux`,

```
\@writefile{toc}{\contentsline {part}{VIII\hspace {1em}\ifpl {Teoria informacji}{Information theory}}...}
```

and on read-back the English build died with `! Extra }, or forgotten \endgroup.`
The Polish build survived, so this was a **one-edition-only build failure** —
exactly the class of bug a bilingual repository exists to make visible.

Two fixes, and the second is the one to take:

1. `\DeclareRobustCommand{\ifpl}[2]{...}` — verified; both editions then build.
2. **Better: part titles should not use `\ifpl` at all.** They are user-visible
   strings, and `lang/en.tex`/`lang/pl.tex` already carry the rule that *nothing
   outside the language files may hard-code a word the other edition also sets*.
   `structure.tex` breaks its own house rule. Moving the nine part titles to
   `\lblPartI`…`\lblPartIX` fixes the build, restores the rule, and brings the
   part titles under check **C3**, which compares the two catalogues' macro sets.

Fix 1 is applied and the concurrent session has since adopted and documented it
independently, including the follow-on that a robust macro cannot go into a PDF
bookmark string and needs `\pdfstringdefDisableCommands`. Fix 2 is still the
recommendation: it removes the class of bug rather than the instance.

`\ifpl` should survive only for genuinely structural asymmetries (an extra
Polish-only notation frame), never for a string.

### 0.3 `\val` does not expand inside a listing

Verified: inside `\begin{console}` the macro prints its own name,
`\rawval{f01.eps64}`, because `listings` reads verbatim and the `mfacode` style
sets no `escapechar`. So a console transcript cannot pull a computed number.

This matters more here than it looks. The sibling book's consistency pass found
that its only outright factual error survived a whole draft inside a
**fabricated `console` block**, because a transcript nobody ran is
indistinguishable from one that was. In a mathematics book that failure mode is
worse: a wrong digit is not a broken example, it is a falsehood the reader
carries away.

The rule that follows is in the contract at §2.7 and enforced by check **C10**:
*every console transcript is a file written by `code/`, pulled in with
`\lstinputlisting`. No transcript is typed.*

### 0.4 The decimal that was localised by hand

The clearest single illustration of what the contract is for, found by running
the checks against the introduction the scaffolding session had just written:

```latex
en:  ... cannot represent $0.1$ ...
pl:  ... nie potrafi przedstawić liczby $0{,}1$ ...
```

Both PDFs are correct today. The design is still wrong, in three ways:

- the number is **authored twice**, so a correction to one will not reach the other;
- the frame's mathematics can never again be compared between editions, because
  the source deliberately differs;
- it establishes the habit that a translator localises numbers by hand, which is
  the habit that eventually changes a digit.

The correct form is `$\num{0.1}$` in **both** files — identical source, and
siunitx sets `0.1` or `0,1` from `\mfadecimalmarker`. This is what §2.2's
"never a literal decimal in maths" row means, and C10 enforces it.

It also settles a design disagreement between the two parity tools now in the
repository; see §1.9.

### 0.5 Current state, measured

Both editions build. `latexmk -pdf main-en.tex` and `main-pl.tex` each return 0:

| | en | pl |
|---|---|---|
| Pages | 142 | 142 |
| Errors | 0 | 0 |
| Overfull hbox | 4 (max 4.09 pt) | 4 (max 4.09 pt) |
| Overfull vbox | 0 | 0 |
| Labels resolved | 52 | 52 |

The page equality is an artefact of every program still being a stub; expect
Polish to run roughly 10–15% longer once there is prose. **Page-count parity is
not a check and must never become one.**

---

# HALF ONE — Repository architecture

## 1.1 What the book actually is, structurally

This is not a book with a translation. It is one book with two surfaces, and
that distinction drives everything below.

A Stroud program is a **stream of numbered frames**, and the numbers are load-
bearing in four places at once:

- the Summary tags every item with the frame it came from — `[12]` — so the
  summary is a return index;
- the Quiz names the frames that teach each question, so a wrong answer routes
  the reader to a specific place;
- "Can you?" is generated from the entry outcomes, each carrying frame numbers;
- programs cross-reference each other by frame.

So the failure that matters is not "the Polish is a worse translation". It is
**frame 12 of the Polish edition teaching something other than frame 12 of the
English one**, at which point every one of those four navigation aids points
somewhere different in the two books, and *neither build emits a warning*,
because each is internally consistent.

Everything in Half One is aimed at that single failure.

## 1.2 The options, judged

| | (a) inline `\iflanguage` | (b) parallel trees | (c) po4a / PO | (d) shared skeleton, per-frame files |
|---|---|---|---|---|
| **Diff reviewability** | Bad. Every frame is a two-branch conditional; a Polish reviewer reads English to find their sentence, and the maths is buried between branches. | Good. A Polish reviewer opens a Polish file and reads a book. Two-file diffs on a PR, side by side. | Poor *as a book*. The Polish reviewer reviews a `.po` file, never a program. | Good per frame, unreadable per program — no file contains a whole lesson. |
| **Drift risk** | Near zero — structurally impossible to add a frame to one edition only. | **The whole risk.** Nothing in LaTeX stops the editions diverging. Must be imported from CI. | Low for content; fuzzy-matching flags a changed source string automatically — the only option that does this for free. | Near zero for structure; unchanged for content. |
| **Cost of adding a program** | High per frame. Constant context-switching; the author writes both languages in one buffer, at one sitting, badly. | Low. Write English, then translate, or write Polish first — the tree does not care which. | Low to add, high to set up. po4a's LaTeX module segments on paragraphs and needs per-macro configuration to know which arguments are translatable; this book has `\ans{}`, `\outcome{}{}`, `\sumitem{}{}`, `\answerto{}`, `\teachesat{}`. | High. 50 frames × 46 programs × 2 languages ≈ 4600 files. |
| **Can CI prove parity?** | Trivially — parity is a tautology. | **Yes, and this is the design work.** See §1.6. | Yes; `msgfmt --statistics` gives coverage directly. | Yes, and more cheaply than (b). |

Three further considerations decide it.

**Polish is not the translation.** The working title is Polish-first. A
mechanism that makes one edition generated output makes it second-class
permanently, which rules out (c) on editorial grounds before the tooling
arguments start.

**The editions must be allowed to diverge deliberately.** The Polish edition
needs frames the English one does not: a notation box on `D²(X)`, a frame on why
this book writes `[a,b]` where the reader's schooling wrote `⟨a,b⟩`, and a
terminology appendix for English AI vocabulary that has no settled Polish form.
Option (c) cannot express that at all; (a) expresses it badly.

**Prose in two languages in one buffer is a false economy.** Option (a)'s
zero-drift guarantee is real, and it is bought by making both editions
unpleasant to write and impossible to review. Stroud's method needs an author
with the reader's ear; nobody has that ear in two languages in alternate lines.

## 1.3 Recommendation

> **Adopt (b) — parallel trees — hardened by three mechanisms that convert
> option (a)'s structural guarantee into CI checks, without paying option (a)'s
> authoring cost.**
>
> 1. **A shared spine.** There is exactly one list of parts and programs,
>    `structure.tex`, read by both main files. A program cannot exist in one
>    edition only. *(This is the sibling session's design and it is right —
>    keep it. It makes an entire check unnecessary rather than automating it.)*
> 2. **An executed notation contract.** Every user-visible string and every
>    symbol that differs between editions is a macro resolved from
>    `lang/<lang>.tex`. A translator never types `tg`; they type `\tg` in both
>    editions. This is what makes §1.6's maths-digest check possible at all.
> 3. **A structural signature, compared in CI.** Each program file is reduced to
>    an ordered token stream — frames, answers, exercises, boxes, back-references
>    and a hash of every mathematical expression — and the twins must match
>    token for token.

The slogan: **structure is shared, prose is duplicated, and the boundary between
them is machine-checked.**

Mechanism 3 is the load-bearing one. Option (b)'s only real weakness is drift,
and drift is only dangerous when it is invisible. A structural signature makes
it loud.

## 1.4 Shared versus duplicated

| Artefact | Status | Why |
|---|---|---|
| `preamble.tex` | **Shared, one file** | Both mains `\input` it after setting `\booklang`. Style cannot diverge. |
| `structure.tex` | **Shared, one file** | The single list of parts and programs. Makes program-set drift impossible by construction. |
| `lang/en.tex`, `lang/pl.tex` | **Twinned, checked** | Every user-visible string, plus the symbols that genuinely differ. C3 asserts identical macro *sets*. |
| Part titles | **Move into `lang/`** | Currently inline `\ifpl` in `structure.tex`; see §0.2. |
| `programs/<lang>/*.tex` | **Duplicated** | The prose. This is the point of the design. |
| Frame *sequence* inside a program | **Duplicated, checked (C4)** | Cannot be shared without option (d)'s file explosion; checked instead. |
| Mathematics inside frames | **Duplicated, checked (C8)** | Byte-identical source because the contract is macro-executed; a hash comparison catches a sign fixed in one edition only. |
| Label names | **Duplicated, checked (C5, C11)** | Same names in both. Separate PDFs, so no clash. |
| Exercise & answer keys (`Q1`, `T3`, `P7`) | **Derived from position, checked (C6)** | Never authored. A reader looking up `T3` must get the same question in both. |
| Learning outcomes → "Can you?" | **Generated in the preamble** | Already generated from the stored outcomes, so those two cannot drift *within* an edition. C4 compares the frame ranges across editions. |
| Computed numbers | **Shared, one source** | `code/*.py` → `figures/values/*.tex` → `\val{}`. Both editions read the same digits; only the decimal marker differs. |
| Console transcripts | **Shared, generated** | See §0.3. Written by `code/`, `\lstinputlisting`-ed. |
| Code listings | **Shared** | Python is not translated. Comments in listings stay English (see §2.7). |
| Mermaid diagrams | **Per language today; recommend splitting** | See §1.5. |
| `figures/screenshots/` | **Shared** | Should be near-zero in this book. |
| Answers appendix | **Generated** | Collected from `\answerto{}` at the point of use. Ordering follows the shared spine, so it cannot diverge independently. |
| The index | **Duplicated** | Genuinely different: Polish sorts differently and indexes different head terms. Not checked for parity, deliberately. |

## 1.5 One refinement to the diagram pipeline

The preamble currently expects `figures/mermaid/<lang>/<key>.mmd` — a full
duplicate of each diagram per language. A diagram's *labels* are prose and must
be translated; its *topology* is structure and must not diverge. Duplicating the
whole file puts topology on the wrong side of the line.

Recommend the same split used everywhere else: one source with placeholders,
plus a label catalogue per language.

```
figures/mermaid/<key>.mmd          # topology, with @L.node1@ placeholders
figures/mermaid/labels.en.json     # {"node1": "Forward pass", ...}
figures/mermaid/labels.pl.json     # {"node1": "Przebieg w przód", ...}
```

`tools/render_diagrams.py` substitutes and renders to
`figures/diagrams/<lang>/<key>.pdf`. Cost: about forty lines. Benefit: a node
added in English cannot fail to appear in Polish, and a missing translation is a
missing JSON key — a hard error rather than a silently English node in a Polish
book.

Until that exists, **C9** checks that both languages carry the same key set and
that every referenced `.mmd` is present in both trees.

## 1.6 The CI parity checks

Eleven checks in three runnable scripts. All are in the repository, all were
run, and §1.7 shows them catching injected faults.

| # | Check | Catches | Where |
|---|---|---|---|
| C1 | File-set parity across `programs/`, `appendices/`, `frontmatter/` | A file written in one edition only | `parity.py` |
| C2 | Shared spine present; include order identical | Program-set drift *(mostly obsolete now `structure.tex` exists — keep as a regression guard against reintroducing two include lists)* | `parity.py` |
| C3 | `lang/en.tex` and `lang/pl.tex` define the same macro set | A label added to one catalogue only | `parity.py` |
| C4 | **Structural signature**, token for token | Frame count, exercise count, outcome count, box placement, `\yourturn`, `\blank`, summary back-references — all at once | `parity.py` |
| C5 | Label-name set parity | A `\label` in one edition only | `parity.py` |
| C6 | Answer-key parity (`Q*`, `T*`, `P*`) | `T3` meaning different questions in the two editions | `parity.py` |
| C7 | `\val{}` keys used ⊆ keys produced by `code/`; unused values warned | A number the scripts no longer produce | `parity.py` |
| C8 | **Maths digest per frame** | A sign or exponent fixed in one edition only | `parity.py` |
| C9 | Diagram-key parity; `.mmd` present in both | A figure that exists only in English | `parity.py` |
| C10 | **Notation contract lint** | `\tan` hard-coded, bare `\log`, bare decimals in maths, `\val` inside a listing, straight quotes in Polish | `parity.py` |
| C11 | Every `\ref` resolves in **both**, and resolves to the **same number** | `prog:F08` numbering as F8 in English and F9 in Polish | `reflist.py` |

Plus the build-integrity check that is not about parity but is what made the
rest trustworthy:

| — | Real errors (both log formats), undefined/multiply-defined refs, overfull h/vbox budget, **and a run that wrote no PDF at all** | A green build that errored, or produced nothing | `checklog.py` |

### Why C4 is stricter than counting

Counting frames catches a dropped frame. It does not catch a translator who
turns "now one for you to do" into another worked example — the third rung of
Stroud's scaffolding gradient quietly becoming the second. C4 compares the
ordered stream, so `YOURTURN` missing at position 13 is a failure with a line
number in both files.

Tokens compared: `PROGRAM`, `LABEL(name)`, `FRAME(n)`, `ANS`, `BEGIN/END(box)`,
`YOURTURN`, `BLANK`, `DOTLINE`, `OUTCOME(frames)`, `SUMITEM(frame)`,
`EXITEM(key)`, `ANSWERTO`, `TEACHESAT(frames)`, `VAL(key)`, `FIG(key)`,
`REF(name)`, `MATH(hash)`, `CANYOU`, `STUB`.

Payloads are compared where they are a number, a key or a cross-reference.
Prose payloads (`\sumitem`'s second argument, `\outcome`'s second argument) are
not compared — they are the translation.

### Why C8 works at all

A hash comparison of mathematics only works if the two editions' maths *source*
is byte-identical. It is, and only because of mechanism 2: both editions write
`\tg\theta`, `\Var(X)`, `\gcdop(12,18)`, `\intcc{0}{1}`, and the language files
decide what those set. Hard-code `\tan` in the English edition and C8 fires — as
does C10, naming the rule.

This is the closed loop that makes the whole architecture hang together: **the
notation contract is not a document the translator remembers, it is the
mechanism that makes divergence detectable.**

### The escape hatch, and why it is debt

Some divergence is legitimate — a Polish-only notation frame. Declared by
putting, in **both** files at the corresponding point:

```latex
% parity: allow-divergence  Polish-only note on the D^2(X) convention
```

The marker emits a token of its own, so the streams still align, and the next
token is dropped from both signatures. `make debt` counts these. An
allow-divergence that appears in one file only is itself a divergence and fails.

## 1.7 Proof that the checks bite

A faithful translation of a three-frame program passes:

```
ok  [C4-structure] ZZ-test.tex: 36 tokens, 3 frames
ok  [C8-math]      ZZ-test.tex: maths identical across 3 frames
```

Five faults were then injected, one at a time. Every one was caught, with a
location in both files:

| Injected fault | Reported |
|---|---|
| Translator drops `\yourturn` | `[C4] diverge at token 13 -- en:11 YOURTURN != pl:12 MATH(ccce857498)` |
| Sign lost from a summary item (`-∑` → `∑`) | `[C4] token 24 -- en:23 MATH(cb703657f9) != pl:23 MATH(d10b782be9)` + `[C8] frame 3 maths differs` |
| An extra test exercise in English only | `[C4] token 36 -- en:29 EXITEM(T3) != pl:29 END(testexercises)` + `[C6] answer key 'T3' in en only` |
| Summary back-reference retargeted | `[C4] token 23 -- en:23 SUMITEM(1) != pl:23 SUMITEM(2)` |
| `\tan` hard-coded and a bare decimal | `[C4]`/`[C8]` maths differs, plus `[C10] \tan -- use \tg` and `[C10] bare decimal '0.5' in maths` |

C11 was proved against synthetic `.aux` files, because it must ignore page
differences and catch number differences:

```
FAIL  label 'fr:sine-rule' numbers differently: en='F8.12' pl='F8.13'
  3 labels in en, 3 in pl, 1 mismatches
```

On the live tree the checks immediately found real defects that had been
committed minutes earlier by the scaffolding session: a `\tan` hard-coded in
*both* introductions, a bare `0.1` inside maths, an English-only frontmatter
file, and a Polish appendix stub that had lost the six expressions its English
twin carried.

## 1.8 The scripts

Three files, all runnable from the repository root with no dependencies beyond
the standard library.

- **`tools/parity.py`** — C1–C10. Tokenises both trees, compares signatures,
  label/answer/value/diagram sets and per-frame maths digests, then lints the
  notation contract. Exit 1 on any failure.
- **`tools/reflist.py`** — C11. Reads both `main-*.aux` trees after a build and
  compares resolved label *numbers*, ignoring pages.
- **`tools/checklog.py`** — build integrity. Matches errors in **both**
  pdflatex formats, undefined and multiply-defined references, and the
  15 pt/0 pt overfull budget inherited from the sibling books.

CI wiring lives in `.github/workflows/build.yml`, which the concurrent session
has since rewritten and improved. Its shape is right: `numbers` gates everything
and fails if a committed value differs from what `code/` now produces; `parity`
is a hard gate; `diagrams` renders and checks that both languages carry the same
keys; `build` is a two-way matrix over `{en, pl}` with `fail-fast: false`, so a
Polish-only break is never masked by a green English job; `ledgers` is advisory
and prints `make debt` to the step summary.

Two additions it still needs:

- **`tools/reflist.py` after both builds (C11).** No single-edition job can see
  a label that numbers differently in the two books.
- **The overfull budget as a gate, not a report.** The workflow currently prints
  the hbox/vbox lists to the summary. `checklog.py` fails above 15 pt and on any
  overfull vbox, which is the inherited house rule. A vbox in particular is
  never cosmetic — it means a boxed table grew past a page and could not break.

It correctly passes `-halt-on-error -file-line-error`, which closes the §0.1
hole from the other direction: the build now stops rather than writing a PDF
through an error. Keep both defences — `checklog.py` also catches undefined
references and the box budget, which `-halt-on-error` does not.

`texlive-lang-polish` must be installed explicitly. babel with a missing `.ldf`
is fatal, not a warning, and names neither babel nor the language.

## 1.9 Two parity tools, and how to merge them

The concurrent session wrote `tools/check_parity.py` alongside this note's
`tools/parity.py`. Both are good; they check different things, and right now
they disagree:

```
$ python3 tools/check_parity.py
  The two editions are in step.

$ python3 tools/parity.py
  FAIL [C4] appB-notation.tex: diverge at token 3 -- en:10 MATH(782cb89fbe) != pl:EOF
  FAIL [C8] appB-notation.tex: frame 0 maths differs (en 6 expr, pl 0 expr)
  FAIL [C4] introduction.tex: diverge at token 2 -- en:75 MATH(180505679c) != pl:77 MATH(da24e04cb6)
  ... 8 failures, 16 warnings
```

Both divergences are real: `appendices/pl/appB-notation.tex` dropped the entire
paragraph in which the English stub records its notation decisions, and the two
introductions carry the hand-localised decimal of §0.4.

**Merge, keeping the strictly better half of each.** Neither tool is a superset.

| Keep from `check_parity.py` | Why |
|---|---|
| Numeric literals compared in order | Catches a translated number silently changing — the strongest single check either tool has |
| Non-ASCII inside `python`/`console`/`shellcmd` | Guards the `listings` UTF-8 trap directly |
| Macro-usage histogram | Cheap breadth; catches a macro dropped in translation |
| `lang/*.tex` macro-set comparison | Same as C3; either implementation is fine |

| Keep from `parity.py` | Why |
|---|---|
| **Ordered** structural signature (C4) | A histogram cannot see reordering. `\yourturn` moved from frame 2 to frame 3 leaves every count identical. |
| Per-frame maths digest (C8) | A sign fixed in one edition only changes no count and no histogram |
| Answer-key identity `Q1`/`T3`/`P7` (C6) | Counts are not enough; `T3` must be the *same question* |
| Notation-contract lint (C10) | The rules of Half Two, enforced |
| `reflist.py` (C11), `checklog.py` | Neither has an equivalent |

**One design disagreement to settle explicitly.** `check_parity.py` normalises
the Polish decimal comma to a full stop before comparing numbers. That is what
lets `$0.1$` / `$0{,}1$` pass. It is the wrong default: it hides the fact that
the number was localised **by hand instead of by macro**, which is precisely the
defect. Forbid hand-localised decimals (C10), and the normalisation becomes
unnecessary — after which numbers can be compared strictly, which is stronger
than comparing them loosely.

`check_structure.py` should stay as it is. It checks *within*-edition
invariants — exercises with no answer, the 30–70 frame band, outcomes declared —
which are a different job and a genuinely useful ledger.

---

# HALF TWO — Polish mathematical notation and typography

## 2.1 The governing principle: the keyboard test

Polish mathematical convention and Polish AI writing pull in opposite
directions, and a rule is needed that is not "pick the Polish one" or "pick the
English one", because both produce a book that reads wrong.

> **The keyboard test.** If the reader will *type* the token into code, both
> editions use the code spelling. If the reader will only ever *read* or
> *write* it, the Polish edition uses the Polish form.

`tg θ` is never typed into a computer; `tanh` is `torch.tanh`. So the Polish
edition sets `tg` for the tangent and `tanh` for the hyperbolic tangent, and
that apparent inconsistency is the rule working, not failing. It is stated to
the reader in the notation appendix, once.

Two secondary rules:

- **Where usage is genuinely split, pick the form that survives contact with the
  literature the reader is being trained to read** — which for this book is
  English-language papers and library documentation.
- **Where the Polish reader's schooling supplied a different symbol, say so in a
  `notationbox` at first use.** Not in the appendix only. A Polish reader who
  meets `[0,1]` where they learned `⟨0,1⟩` and is not told will conclude the
  book is a careless translation, and they will be reasonable to.

## 2.2 The notation contract

Every row is implemented as a macro in `lang/en.tex` and `lang/pl.tex`, so the
*source* is identical in both editions and only the output differs. C10 rejects
the raw forms.

### Functions

| Item | English sets | Polish sets | Macro | Decision and reason |
|---|---|---|---|---|
| tangent | `tan` | `tg` | `\tg` | Polish universally writes `tg`; `tan` reads as a calque. Confirmed across Polish teaching sources. |
| cotangent | `cot` | `ctg` | `\ctg` | Same. Polish also sees `ctn`; `ctg` dominates. |
| arctangent | `arctan` | `arc tg` | `\arctg` | Polish sets `arc tg` (thin space) or `arctg`. Thin space chosen to match `arc ctg`. |
| arccotangent | `arccot` | `arc ctg` | `\arcctg` | Same. |
| **hyperbolic tangent** | `tanh` | **`tanh`** | `\tanh` | **Split, and deliberately resolved against Polish tradition.** PWN's encyclopedia and Polish university notes write `tgh`. Keyboard test: this is the activation function, it is `torch.tanh`, and a Polish reader who learns `tgh` will not find it in any library. `notationbox` records `tgh` at first use. |
| sine, cosine | `sin`, `cos` | `sin`, `cos` | built-in | Identical. No action. |
| natural log | `ln` | `ln` | `\ln` | Identical, and see the next row. |
| **base-10 / bare `log`** | — | — | **forbidden** | **The most consequential row in this table.** In Polish textbooks a bare `log` means base 10; in AI writing it means base *e*. The same three characters carry opposite meanings to the two audiences. **The book never writes a bare `\log`.** Always `\ln` (nats) or `\log_2` (bits). C10 fails on `\log` not followed by `_`. |
| `lg` | — | — | **not used** | Polish `lg` also means base 10 but is rare in practice; introducing it buys nothing and adds a third spelling. |

> **This overrides a decision already written into `appendices/en/appB-notation.tex`,**
> which currently promises "that `\log` means the natural logarithm throughout".
> That convention is common in ML papers and is wrong for *this* book: it fights
> the Polish reader's entire schooling, and it is at its most dangerous in
> exactly the programs where it matters most. Entropy in bits and cross-entropy
> in nats appear within two programs of each other (P28, P29); a reader who has
> to remember a global convention to know the base of a logarithm in an entropy
> formula has been set up to fail. Write the base. It costs two characters.

### Numbers, sets and arithmetic

| Item | English | Polish | Macro | Decision and reason |
|---|---|---|---|---|
| Decimal separator | `0.5` | `0,5` | `\num{}` / `\val{}` | siunitx `output-decimal-marker` from `\mfadecimalmarker`. **Never a literal decimal in maths** — C10 fails it, because a literal prints a full stop in a book that owes a comma. |
| Thousands grouping | `10 000` | `10 000` | `\num{}` | Thin space (`\,`) in **both**. Polish never uses a comma; English-language technical writing accepts the thin space and SI prefers it. Grouping starts at five digits, so `1000` stays ungrouped. |
| Decimals in code | `0.1` | `0.1` | — | **Unchanged.** A comma is a syntax error in Python. Listings are ASCII and never localised. |
| Machine output | as printed | as printed | `\rawval{}` | A transcript is evidence. It keeps the machine's own point. |
| Closed interval | `[a, b]` | `[a, b]` | `\intcc` | **Split, resolved against Polish tradition.** Polish schooling writes `⟨a, b⟩`; ISO 80000-2 and every paper the reader will open write `[a, b]`. `notationbox` at first use, and a row in appendix B. |
| Open interval | `(a, b)` | `(a, b)` | `\intoo` | Consistent with the above. Note the genuine ambiguity with an ordered pair — where context does not settle it, write the set-builder form instead. |
| ℕ, ℤ, ℚ, ℝ, ℂ | same | same | `\N` … | Identical glyphs. **But state explicitly that 0 ∈ ℕ** in the frame that introduces it; Polish and English usage are both split and the book should not rely on convention. |
| gcd | `gcd` | `NWD` | `\gcdop` | *Największy wspólny dzielnik.* Standard, unambiguous, no code collision. |
| lcm | `lcm` | `NWW` | `\lcmop` | *Najmniejsza wspólna wielokrotność.* Same. |
| Binomial coefficient | `\binom{n}{k}`, "n choose k" | `\binom{n}{k}`, *symbol Newtona*, "n po k" | `\binom` | **Same symbol, different name.** Polish calls it *symbol Newtona* and reads it *n po k*. A frame that says "n choose k" in Polish is a translation failure even though the maths is right. Vocabulary row, not a notation row. |

### Linear algebra

| Item | Both editions | Decision and reason |
|---|---|---|
| Vector | `\vect{x}` → upright bold lowercase | Bold is international. Polish also uses an arrow (`x⃗`) at school level; bold is what papers and this book's own AI material use. `notationbox` at first use. |
| Matrix | `\mat{A}` → upright bold capital | Same reasoning. |
| Transpose | `A\T` → `Aᵀ` | Identical in both; `\mathsf{T}` so it is not mistaken for an index. Polish sometimes uses `A'`; not adopted — the prime is needed for derivatives. |
| Vectors are **columns** | — | Declare once, in P04, and never rely on it implicitly. |
| Matrix-calculus layout | **numerator (Jacobian) layout**, declared | Not a Polish/English split — a discipline split, and the source of half the transpose confusion in backpropagation. Declare it, and put the alternative in a `notationbox`. |
| Norm, inner product | `\norm{}`, `\inner{}{}` | Identical. |

### Probability and statistics

| Item | English | Polish | Macro | Decision and reason |
|---|---|---|---|---|
| Probability | `P(A)` | `P(A)` | `\Prob` | Identical. Not `Pr` — `\Pr` is banned by C10 for consistency. |
| Expectation | `E(X)` | **`E(X)`** | `\Ex` | **Checked, and the scaffold's comment overstates the divergence.** Current Polish university materials use `E(X)` (often with `m = E(X)`). `M(X)` is the older, Russian-tradition form and is now rare. A one-line mention, not a `notationbox`. |
| **Variance** | `Var(X)` | **`Var(X)`**, with `D²(X)` noted | `\Var` | **The genuine live divergence, and the one to handle carefully.** Polish teaching materials still write `D²(X)` *alongside* `Var(X)` today — this is current usage, not a historical curiosity. The book sets `Var` because that is what NumPy, papers and the English literature use, and carries a `notationbox` in P23 stating the equivalence explicitly. Do not skip that box: a Polish reader who learned `D²` and meets an unexplained `Var` loses confidence in the book. |
| Std deviation | `σ`, `sd` | `σ` | — | Greek is international. Avoid `D(X)`. |
| Covariance, correlation | `Cov`, `Corr` | same | `\Cov`, `\Corr` | Identical. |

## 2.3 Typography

| Item | English edition | Polish edition | Decision and reason |
|---|---|---|---|
| **Quotation marks** | `'…'` (British single) | **`„…"`** | Both from `\enquote{}` with `csquotes` `autostyle=true`, which follows babel's active language. **Verified**: the identical source `\enquote{x}` sets `'x'` under `main=british` and `„x"` under `main=polish`. Identical source is essential — it keeps C4/C8 clean. |
| **Dash as punctuation** | `---` (em, closed up) | **`--` (półpauza, spaced)** | A real divergence. Polish typography sets the *myślnik* as a **półpauza with spaces on both sides**; the em dash closed up is an English/American habit that reads as foreign in Polish. Implement as `\dash` in the language files, not by asking translators to remember. |
| Hyphen | `-` | `-` | Identical (*dywiz*). |
| **Hyphenation** | `british` | `polish` main | `babel` with `main=polish` for the Polish edition. **Non-negotiable**: Polish without its patterns hyphenates as English and produces both wrong breaks and overfull boxes. CI installs `texlive-lang-polish`; the preamble probes with `\IfFileExists` because a missing `.ldf` is fatal. |
| `"` shorthand | n/a | **off** | babel-polish makes `"` active. The preamble already does `\shorthandoff{"}` for `pl` — correct, and it must stay: an active character near a `listings` body is a category-code accident waiting to happen. This is *why* quotes must go through `\enquote{}`. |
| Non-breaking space in listings | — | — | **Never add a U+00A0 `literate` mapping.** Fatal, no PDF, and the message names neither the character nor the line. Hit in two of the three books in this series. |
| Polish diacritics in listings | mapped | mapped | The existing `literate` list is correct. ASCII inside listings remains the rule regardless. |
| Ordinals / dates | `17 October 2025` | `17 października 2025` | Polish uses a genitive month name. From the language files. |
| Units | siunitx | siunitx | `\qty{14}{\giga\byte}` in both; siunitx handles the spacing. |

## 2.4 siunitx configuration

Already in the preamble and correct once the `##1` bug of §0.1 is fixed:

```latex
\sisetup{
  group-digits         = integer,
  group-minimum-digits = 5,
  group-separator      = {\,},
  exponent-product     = \cdot,
  output-decimal-marker = {\mfadecimalmarker}   % "." in en, "{,}" in pl
}
```

Two notes. `exponent-product = \cdot` is right for both — Polish writes
`2,22 · 10⁻¹⁶` and it is acceptable English usage. And `\mfadecimalmarker` is
`{,}` rather than `,` in Polish deliberately: braced, the comma is set as an
ordinary symbol rather than a maths punctuation mark, so `0,5` gets no spurious
space after the comma.

## 2.5 AI/ML terms with no settled Polish form

The precedent is the sibling book's Appendix E: an English-headed table with a
Polish rendering and a short gloss, *because the documentation is in English and
a good many of the conversations about it are not.*

**House rule, in three parts:**

1. **The English term is the head.** It is what the reader will search for, read
   in a paper and see in an API. The Polish edition indexes both.
2. **Give a Polish rendering where one is in real use.** Not a coined one.
   *Uczenie maszynowe*, *uczenie głębokie*, *sieć neuronowa*, *spadek gradientu*,
   *funkcja straty*, *warstwa*, *waga* are all live Polish.
3. **Where no Polish form is in real use, keep the English word, inflect it
   Polish, and say so once.** Polish practitioners write *embedding*,
   *transformer*, *token*, *softmax*, *attention*, *dropout*, *batch*. Rendering
   *embedding* as *zanurzenie* or *przedstawienie wektorowe* in running prose
   produces something no Polish engineer says and no Polish engineer will search
   for. A calque invented by a translator is worse than a borrowing everyone
   already uses.

Rule 3 is the one that keeps the Polish edition from reading as machine
translation, and it is the opposite of what a translation service will do
unprompted. It belongs in the translator brief in those words.

Appendix D (*Terminology*) carries the table. Suggested treatment of the hard
cases:

| English | Polish edition uses | Note |
|---|---|---|
| embedding | **embedding** (n. *embeddingu*, pl. *embeddingi*) | *Zanurzenie* exists in mathematical Polish and means something else here; *przedstawienie wektorowe* is a description, not a term. |
| gradient descent | **spadek gradientu** | Established. |
| loss function | **funkcja straty** | Established. |
| learning rate | **współczynnik uczenia** | Established. |
| attention | **attention** / *uwaga* | *Mechanizm uwagi* is used and readable; the bare term stays English. |
| transformer | **transformer** | Never *transformator* — that is an electrical device. |
| token, tokenizer | **token**, **tokenizator** | Established borrowings. |
| overfitting | **przeuczenie** | Established. |
| feature | **cecha** | Established. |
| batch / mini-batch | **batch** / *partia* | *Partia* is understood; *batch* is what is said. |
| logit | **logit** | Also a statistics term in Polish; same word. |
| ground truth | *dane referencyjne* | No settled Polish term; gloss it. |

## 2.6 What the Polish edition must carry that the English one need not

Three `notationbox` frames and one appendix section, each declared with a
`% parity: allow-divergence` marker so C4 stays green and `make debt` counts
them:

1. **Intervals** — `[a,b]` here, `⟨a,b⟩` in your schooling (first interval, F06).
2. **Variance** — `Var(X)` here, `D²(X)` in your schooling (P23).
3. **Hyperbolic tangent** — `tanh` here, `tgh` in Polish mathematical writing
   (F08 or P31, whichever comes first).
4. **Appendix D** — the English-term glossary and the borrowing rule of §2.5.

Everything else in the contract is handled by macros and needs no reader-facing
note.

## 2.7 Rules the lint enforces

C10 fails the build on each of these, with a file and line:

- `\tan`, `\cot`, `\arctan`, `\arccot`, `\gcd`, `\Pr` — use the contract macro.
- A bare `\log` not followed by `_`.
- A literal decimal inside maths not wrapped in `\num{}`, `\val{}` or `\rawval{}`.
- `\val{}` or `\rawval{}` inside a verbatim listing (it does not expand — §0.3).
- Warns on a straight `"` in a Polish source file.

Two further rules are conventions the lint cannot check and the translator brief
must carry:

- **Listing comments stay English.** The reader is being trained to read English
  code. A Polish comment in a Python listing is the one place where localisation
  actively harms.
- **Never translate a mathematical constant's spelling.** `e`, `π`, `i`.

## 2.8 Where Polish usage is split, restated

Four rows are genuine splits rather than clean divergences. Recorded here so
nobody re-litigates them from a search result:

| Item | The split | Chosen | Because |
|---|---|---|---|
| Interval brackets | `⟨a,b⟩` (Polish schooling) vs `[a,b]` (ISO 80000-2, all papers, modern Polish teaching) | `[a,b]` | The reader is being trained to read papers. Flagged to the reader at first use. |
| `tanh` vs `tgh` | PWN and Polish academic writing say `tgh`; code and ML literature say `tanh` | `tanh` | Keyboard test. |
| `Var` vs `D²` | Both current in Polish teaching materials | `Var` | NumPy, papers, and the English literature. Flagged. |
| `E` vs `M` for expectation | Mostly settled on `E`; `M` is residual | `E` | Barely a split any more. One-line mention only. |

---

## Appendix — the checks, verbatim

`tools/parity.py`, `tools/reflist.py` and `tools/checklog.py` are committed to
the repository and were executed against it. Reproduce with:

```bash
cd /home/user/math-for-ai-engineers
python3 tools/parity.py                       # C1-C10, no TeX needed
latexmk -pdf -interaction=nonstopmode -f main-en.tex
latexmk -pdf -interaction=nonstopmode -f main-pl.tex
python3 tools/checklog.py main-en.log main-pl.log
python3 tools/reflist.py                      # C11
```

Current output on the live tree: both editions build at 142 pages with zero
errors, zero overfull vboxes and four overfull hboxes of at most 4.09 pt; 52
labels resolve identically in both. `parity.py` reports eight failures, all
genuine and all introduced by the scaffolding session while this note was being
written:

- `\tan` hard-coded in **both** introductions instead of `\tg`;
- a bare `0.1` inside maths in the English introduction, and its hand-localised
  Polish twin `0{,}1` (§0.4);
- a bare `\log` in `appB-notation.tex`, attached to a convention this note
  recommends reversing (§2.2);
- `appendices/pl/appB-notation.tex` missing the six expressions its English twin
  carries.

That is the argument for the architecture in one paragraph: none of these was
noticed by the people who wrote them, none breaks either build, and all eight
were found in under a second by a script with no TeX installed.

## Immediate actions

1. Move the nine part titles out of `structure.tex` into `lang/*.tex` (§0.2).
2. Reverse the bare-`\log` convention in `appB-notation.tex` (§2.2).
3. Fix the two introductions: `\tg`, `\num{0.1}` in both editions (§0.4).
4. Translate the `appB-notation.tex` Polish stub, or mark it with
   `% parity: allow-divergence` so the debt is counted rather than silent.
5. Merge the two parity tools on the split in §1.9.
6. Add `reflist.py` to CI and make the overfull budget a gate (§1.8).
7. Keep the two preamble fixes of §0.1 and §0.2 — both are applied and verified,
   and both are the kind of bug that reappears when a file is rewritten.
