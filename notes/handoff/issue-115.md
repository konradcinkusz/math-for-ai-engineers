# Issue #115 --- Quiz and "Can you?" headings stranded at page feet

Reviewed against `main` at `c9b8bb6`. The issue is the layout item CLAUDE.md
has carried as *recorded rather than taken* for eight consecutive batches,
with the standing note that **the instrument is owed before the sweep**.

**What is fixed here is not the layout.** It is the four comments that told
each of those eight batches the Quiz was already guarded --- three in
`preamble.tex`, one in `tools/checkpdf.py`. Every one of them is a claim
about a mechanism, none had been checked against the mechanism, and two of
them are false. That is why the defect was walked past rather than measured,
and it is the whole reason this issue has an eight-batch history.

**Nothing typeset changed.** Proved mechanically rather than asserted: the
non-comment content of `preamble.tex` is byte-identical to `HEAD`, and
`tools/checkpdf.py`'s AST is identical to `HEAD`'s. Both instruments were
watched producing a known answer first --- a one-character change to
`\mfasectionreserve` makes the first report a diff, and a one-character
change to `FILL_FLOOR` makes the second report `False`. **No frame changed
length, no value was emitted or retired, and no page can move: there is no
cue walk owed to the sync session from this branch.**

## The environment, which decided the shape of the pass

**There is no TeX in this container.** `pdflatex`, `latexmk`, `xelatex`,
`lualatex`, `tex` and `kpsewhich` are all missing and there is no
`texlive` tree. So the page-level findings could not be re-measured, a
standalone probe could not be built, and --- decisively --- a new
`checkpdf.py` check could not be watched firing. That last is why the
instrument is still owed; see below.

## Two of the issue's premises are wrong, and the second one is the finding

> "The two unnumbered headings every program carries --- Quiz on the opener
> and Can you? near the end --- are `\section*` and get no such test."

**Can you? is not a `\section*`.** `\canyou` calls `\mfa@endhead`
(`preamble.tex:1261`), which is `\large\bfseries` plus a ToC line. Both
`preamble.tex`'s `\mfa@sectionroom` note and `tools/checkpdf.py`'s
`RE_SECNO` note listed it among the `\section*` headings, so a reader
following either would look in the wrong place. Corrected in both.

**The Quiz does carry a room test** --- `8\baselineskip`, added deliberately,
with its own paragraph of justification. The issue's premise is wrong and
the defect is worse than the issue describes, because the guard is not
missing: **it is sized below what the box it guards demands, so in a window
it produces the stranding rather than failing to prevent it.**

## The arithmetic, which needs no build

Both constants live in the same comment block in `preamble.tex`, twenty-odd
lines apart, and they contradict each other:

| | |
|---|---|
| the `quiz` room test reserves | `8\baselineskip` |
| the box's `lines before break` demands | `12` lines |

`lines before break=N` means the box will not *begin* on a page that cannot
hold N lines of its content; below that it is not broken, it is moved whole.
That semantics is not taken from tcolorbox's manual --- it is the book's own
recorded measurement, in the same comment: at the default (2) F01's quiz
broke 3 + 9 in both A4 builds, and 12 keeps it whole in all four.

So `8 < 12` **before** the heading and its three-line instruction are counted
at all. On every page whose remaining room falls between the guard's
threshold and the box's demand, the guard passes, `\section*{Quiz}` and
`\lblQuizIntro` are set, and the box then moves whole. The heading and the
instruction are left at the foot with `\flushbottom` spending the page's
stretch as the hole the issue describes.

The reserve was sized as *"heading plus instruction plus the first
question"* --- that is, on the assumption the box would break after one
question, which the `lines before break` twelve lines above it forbids. The
comment contains its own refutation and has since the guard was written.

## "Can you?" --- a different mechanism, and the recorded reasoning misses it

`\canyou`'s note argues that the heading is safe because *"what follows this
heading is an ordinary paragraph, which `\nobreak` does hold"*, and then
spends the rest of its length on a club-penalty widow.

That is true about the paragraph and silent about the `tabularx` under it,
which is **one unbreakable box**: when it does not fit it moves whole.
`\nobreak` holds the intro to the heading and has nothing to say about the
table, so the two go over the leaf *together* --- which is exactly the shape
the issue reports (heading, instruction, five-to-eight blank lines, no
items).

Of `\mfa@endhead`'s three callers this is the only one exposed: a named frame
carries `\mfa@namedframe`'s own room test (`preamble.tex:~1495`), and Further
problems is followed by a list, which breaks.

## Retired --- a remedy that was already built and rejected

The issue's fix 2 asks to *"repeat the Frames column header on continuation
pieces of the quiz box (tcolorbox `title after break`)"*. **That variant was
built and rejected**, and `preamble.tex` says so in as many words: the
heading does repeat on the continuation, and the FIRST part of the box then
has no top rule at all.

This is the P01/P02 rule in its strongest form, and the third time in recent
batches: not a finding that no longer reproduces, but a *remedy* that has
already been evaluated. It cost one read of the comment above the macro.

## Recorded rather than taken --- three layout changes, with their mechanisms

All three move pages, and the task's own classification names "a room test"
and "a preamble constant" as the class to record. What follows is written so
the next session does one build and a sweep of one number rather than a
re-diagnosis.

**1. The Quiz reserve.** It must become heading + instruction +
`lines before break` + the box's rule and top padding. That is a
*derivation*, not a sweep --- but raising it turns a page at the top of a
program and every break in the book after it moves, so what it costs is a
measurement across four builds. `\mfasectionreserve`'s own sweep table is
what one looks like, including its non-monotonicity. **Give the two numbers
one macro** so they cannot drift apart again; today they are independent
literals in one comment block.

**2. The "Can you?" guard needs no constant and no sweep.** Because the
table is unbreakable its height is knowable: `\sbox` it, compare
`\ht`+`\dp` against `\pagegoal-\pagetotal`, `\newpage` when it will not fit,
guarding `\pagegoal=\maxdimen` (a fresh page means *unlimited*, not *no
room*) and a table taller than `\textheight` (or it loops). This is the
measure-your-own-box idiom the frame badge, the Summary icon and
`\mfaheadmark` already use, and it is exact where a reserve in
`\baselineskip` is a guess. It still turns pages.

> **`longtable` is NOT the alternative, and it is the trap waiting here.**
> It is loaded in `preamble.tex:165` and has no call site anywhere in the
> book, so it looks exactly like the answer to a table that will not break.
> It has no `X` column, and this table has one (`{@{}Xcccccc@{}}`).
> Combining it with `tabularx` needs `xltabular` or `ltablex`, neither
> loaded, and adding a package one of this project's two TeX installations
> may lack is P09's recorded trap. CLAUDE.md's Appendix E pass records this
> already; it is repeated here because the next person will reach for it.

**3. Breaks inside a Quiz item, and row separation in "Can you?".** Both are
ordinary (b): an unbreakable-item penalty inside `quizlist`, and
`\addlinespace`/`\extrarowheight` between the rating rows. Each changes
where breaks fall or how tall rows are, so each moves pages.

## The instrument, still owed --- and now with a specification

`tools/checkpdf.py`'s stranded-heading check **cannot see either of these
headings, structurally**: `is_heading` requires `RE_SECNO` to match the
line's first word, i.e. a section *number*, and neither `Quiz` nor
`Can you?` has one. That is why the issue's instances were found by eye, one
page image at a time, and why it says "19 of 55 units judged; more will be
added".

Closing it needs two things:

- **the heading STRING rather than a number** --- `\lblQuiz` and
  `\lblCanYou` read out of `lang/*.tex` exactly the way `cue_strings()`
  already reads `\lblNextFrame`, and for the same reason it gives;
- **a second size calibration**, because `\mfa@endhead` sets `\large` where
  a numbered section sets `\Large`, so the height `heading_metrics()` learns
  from numbered headings will not match "Can you?" within its 0.3 pt
  tolerance.

**It is not written here**, and that is a decision rather than an omission:
with no TeX in the container there is no way to watch it fire, and this
repository's own rule is that a check nobody has watched fire is worth less
than none. Written blind it would most likely have reported a confident
zero --- which is the failure mode the P32--P34 batches recorded five times
over, and which the Part III elicitation pass met head-on when `detect.py`
printed `flagged 0` from a loop that never ran.

Whoever has a TeX installation should write it first. It turns the sweep
from a page-by-page reading of four builds into one build, and it is the
only part of this issue that is blocked on nothing but an environment.

## Nothing found in a neighbouring program

This issue is entirely `preamble.tex` machinery and one tool; it touches no
prose in `programs/en` or `programs/pl`, so "both editions" is satisfied by
construction --- all four builds read the one preamble.

## Gates

`parity.py` 56 file pairs / 1866 frames / 0 failures, 0 warnings.
`check_structure.py --frames --answers --outcomes --values --elicit
--scripts --terms --parts` green, exit 0. `gen_stubs.py --check` current.
`make numbers` reproduced every committed value with no drift in
`figures/values/`. `make verify` is **fully green** --- *"All computed output
is current: values and transcripts"*, exit 0 --- including
`figures/values/appf.tex`, which a comment-only change cannot move, so this
branch leaves the sync session no ledger to regenerate. Elicitation unmoved
at 1030/1866 (55%), because nothing was converted and no frame added.
