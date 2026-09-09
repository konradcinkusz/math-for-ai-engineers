# Hand-off: the front matter (issue #111)

Six findings and two smaller ones, against `main` at `c9b8bb6`. **Four are
fixed, three are retired because they no longer reproduce, one is recorded
with its mechanism** — and the recorded one comes with a correction to the
diagnosis already in CLAUDE.md.

Only `frontmatter/{en,pl}/{titlepage,how-to-use,introduction}.tex` were
touched. No ledger was moved: `make verify` reports all computed output
current, and `figures/values/appf.tex` is untouched.

## Retired — verified against current source, no longer reproduces

- **Finding 3, "the seven parts of every program" is false for four
  programs.** The issue reports P05–P08 shipping with no `Can you?` panel.
  All four carry `\canyou` now — the panel was added by the \#114 pass in the
  second review batch, and `check_structure.py --outcomes` has gated its
  presence and its position ever since. One `grep -c canyou` retired it.
- **Smaller finding A, P31–P34 print Test exercises before Can you?** The
  same pass moved them; `\canyou` now precedes `\begin{testexercises}` by two
  lines in all four, and `--outcomes` fails the build otherwise.
- **Finding 4, the Quiz header says take it twice.** `\lblQuizIntro`
  (`lang/en.tex:52`, `lang/pl.tex:52`) now reads *Take this before you read
  the program*, with no second sitting. Corrected in the F01–F06 review
  batch. The how-to page's own paragraph on this (p18) agrees with it and
  with `\lblCanYouFooter`, so all three now say one thing.

That is the P01/P02 rule paying off for another batch: **a review is a claim
about the build it was made on.** Three findings, three greps, no cycle spent.

## Fixed

### 1. The program count, and it is computed now rather than corrected

The cover and the introduction said **forty-six** in both editions; the book
has forty-seven. Rather than write the right word, all four sites now read
`\val{appf.programs}` — the value `code/appf_ledgers.py` already emits and
`make verify` already gates, printed in Appendix~F's own ledger table.

That retires the class instead of the instance. The cover promises, twelve
lines below the strapline, that *every number in this book is produced by a
script*; a spelled-out wrong number above that promise was the exact irony
the issue closes on, and the P7 insertion is precisely the event that would
do it again.

- `frontmatter/en/titlepage.tex:8`, `frontmatter/pl/titlepage.tex:8`
- `frontmatter/en/introduction.tex:80`, `frontmatter/pl/introduction.tex:80`

**Note the asymmetry that let this survive and the neighbouring "Nine parts"
does not have.** `check_structure.py --parts` reads the introduction's part
ranges and compares them against the manifest positionally, so a change in
the part count fails a gate that names the introduction by file. **Nothing at
all gated the program count.** "Nine parts" is therefore left as words; the
program count is not.

### 5. "The chain rule gets the longest program in the part"

F12 has **31** teaching frames. Part~I's longest is F02 at 50, then F03 48,
F05 47, F01 45, F04 42, F06 42. Only F08 (30) and F13 (23) are shorter, and
F07 is level at 31. True of the plan, false of the book.

**The same sentence's other clause was also false and the issue does not name
it**, which is why fixing only the flagged half would have been a
half-correction: *logarithms get a whole program because log-space arithmetic
is load-bearing __three parts later__*. Three parts on from Part~I is
Part~IV, discrete structures. Log space is Part~II's — `P02` is titled
*Numerical error, stability and computing in log-space*, one part later — and
Part~VIII's, seven later. False under every reading.

Both clauses now name a program rather than counting parts or frames: *a
question that needs no positional claim should not carry one*, and a
part-distance decays the moment the curriculum moves. `Program~P2` matches
the file's own bare style at line 26 (`Program~F1 has you compute…`).

- `frontmatter/en/introduction.tex:82-86`, `frontmatter/pl/introduction.tex:82-86`

### 6. "Nearly every one demands a response … forty to seventy times"

Measured with `check_structure.py --elicit`, which counts `\nextframe`
exactly — the macro that *is* "the answer is at the top of the next frame":

| | |
|---|---|
| book-wide rate | 1030 of 1866 frames, 55 per cent |
| per program, lowest | 12 (F13) |
| per program, highest | 39 (F02) |

So **no program reaches forty**, and "nearly every one" is 55 per cent. The
issue names the second; the first is the premise that generated it, and a
third clause in the same paragraph — *it is the only way the pages can be
turned* — is the same claim at full strength and is false for the 45 per cent
that ask nothing. All three were one error and all three are fixed.

**The range is gone rather than corrected**, on this book's own rule against
stating a count of occurrences: a per-program band decays silently and
nothing gates the introduction against the elicitation ledger. What replaced
it is `$\val{appf.elicit.pct}$ per cent` — the same computed value Appendix~F
prints — with a pointer saying where the figure lives.

The claim has a second site the issue does not name, on the how-to page
(*Nearly every frame ends by asking you for something*), and it is fixed too.

- `frontmatter/en/introduction.tex:63-68`, `frontmatter/pl/introduction.tex:62-67`
- `frontmatter/en/how-to-use.tex:13-15`, `frontmatter/pl/how-to-use.tex:13-16`

### 2. "The dependency list in the introduction" does not exist

Confirmed: the introduction carries the part-by-part map and nothing else.

**The issue's own suggested reword is also false, and checking it is the
finding.** It offers *each program's Learning outcomes name what it assumes*.
They do not — an `\outcome{}` states what the reader will be able to do, and
the only assumptions any outcome names are the four declared *forward*
references. Writing it would have replaced a wrong pointer with a plausible
one.

What is true was measured before it was written: **every program except F01
cites at least one earlier program by `\ref{prog:…}`**, F01 being the first
and having nothing behind it. The minimum over the rest is four distinct
predecessors (P04, P14); the typical program cites eight to fourteen. So the
pointer now says that where one program leans on an earlier one it names it
on the spot, which is checkable and needs no list that does not exist.

Generating the dependency table from the manifest's `deps` — the issue's
first option — is a new front-matter section of 47 rows, so it is a
pagination change nobody has measured. Not taken here.

- `frontmatter/en/how-to-use.tex:99-104`, `frontmatter/pl/how-to-use.tex:100-105`

## Recorded rather than taken — and CLAUDE.md's diagnosis of it is wrong

**Smaller finding B: the contents runs to fourteen pages.**

CLAUDE.md's metadata pass records the cause as *nothing sets `tocdepth` or
`secnumdepth` anywhere, so book.cls's default of 2 puts every numbered
section of forty-seven programs into it*, and files it under this issue.
That is half the mechanism and it is the wrong half for what the issue
complains about.

Measured:

| source | entries | governed by |
|---|---|---|
| numbered `\section{` in the programs | 275 | `tocdepth`, default 2 |
| **starred back-matter sections, 5 × 47** | **235** | **explicit `\addcontentsline`** |

The ~200 repeated identical entries the issue names — Quiz / Summary / Can
you? / Test exercises / Further problems, one set per program — are
`\section*`, and a starred section does not reach the contents through
`tocdepth` at all. They are written by two explicit calls:

- `preamble.tex:1377` — `\phantomsection\addcontentsline{toc}{section}{\lblQuiz}` inside the `quiz` environment;
- `preamble.tex:1460` — the same line inside `\mfa@endhead`, which sets the Summary, *Can you?*, Test exercises and Further problems heads.

**So `\setcounter{tocdepth}{0}` would do the opposite of what the issue
asks**: it would drop the 275 numbered section lines, which are the useful
half, and leave all 235 repeated ones. The fix the issue actually wants is to
gate or drop those two `\addcontentsline` calls.

Not taken because removing 235 contents lines shortens the front matter by
five or six pages and therefore moves every page boundary in the book, in
four formats — and this container has no TeX at all (see below), so it could
not be measured here even if the pass were allowed to build. It is one
counter and two lines whenever somebody can run the sweep.

## For the sync session

- **No frame in any program was lengthened or shortened.** Every edit is in
  the front matter, which contains no frames, so there is no cue to walk on
  my account. The front matter does move by a line here and there, which
  shifts the whole book by at most a line before the first program.
- **This container has no TeX** — no `pdflatex`, no `latexmk`, no
  `/usr/local/texlive`. So the six `\val{}` additions are unexercised until
  your build or CI. The evidence for them is that `\val{}` is already used
  bare in text mode 524 times in `programs/en` and `appendices/en`, and that
  `figures/values/all.tex` — which inputs `appf` — is loaded at
  `preamble.tex:2412`, in the preamble, so the keys resolve on the title page
  as they do anywhere else. `appf.programs` and `appf.elicit.pct` are both
  already referenced by Appendix~F, so C7's ledger does not move.
- Values emitted: none. Values retired: none. `figures/values/appf.tex`
  untouched, `make verify` current.

## Found in a neighbouring artefact and not fixed

**`docs/index.html:88-96` — the published landing page still describes an
early draft.** The banner reads *Early draft. The structure, the build, the
bilingual tooling and __Program F1 in both languages__ are done — 163 pages
on A4 in each language … __Forty-six of forty-seven programs are stubs__
carrying the brief they must satisfy.*

That is four stale claims, and the last of them is verbatim the sentence the
Appendix~D pass corrected in `README.md` on the P04 precedent — in the
sibling file that pass did not open. It is CLAUDE.md's own recorded class,
*a sweep is as wide as the artefact somebody thought to open*, in a third
place after `notes/02` §4 and the generated issues.

Not fixed here because the file is outside this unit and because correcting
only the count would leave a banner that is still wrong in three other ways,
which reads as maintained and is worse than one that reads as stale. The
README already carries the corrected text to mirror; it is a five-minute job
for whoever owns the site page. `docs/index.html` is hand-maintained — the
Makefile's `site` target only assembles `_site/`.

**`lang/en.tex:80` — a stale figure in a comment**, *a translator cannot be
expected to carry a typographic convention in their head forty-six programs
deep.* It is a comment, it prints nothing, and it reads as a figure of speech
about depth rather than a count. Left alone deliberately: `lang/*.tex` is
shared by every unit and a gratuitous edit there risks a conflict for no
reader-visible gain.

## Gates

Run before the edits and again after. `make` was not run; nothing here
produces a page count, an overfull-box table or an orphan-tail figure.

```
parity.py                                   56 file pairs | 1866 frames
                                            0 failures, 0 warnings          exit 0
check_structure.py --frames --answers --outcomes --values
                   --elicit --scripts --terms --parts                       exit 0
gen_stubs.py --check   47 programs, 2418 planned frames; current            exit 0
make numbers                                                                exit 0
make verify            All computed output is current: values and transcripts
make debt              0 of 47 programs are stubs, 0 of 6 appendices;
                       1718 computed values, all referenced, all present;
                       9 part ranges in each introduction, all matching
```

The prose detector (word joins against `HEAD`, new over-long lines, lost
paragraph breaks, doubled short words) flagged one JOIN candidate in the
Polish introduction, `podaje` — an ordinary inflected verb in the new
sentence, with the line-length instrument reporting zero for it. That is the
recorded two-instrument false-positive pattern.
