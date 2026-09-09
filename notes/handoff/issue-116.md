# Issue #116 --- admonition boxes and transcripts breaking into headless fragments

A pure page-level layout issue: nineteen of the fifty-five units judged open a
page with a coloured bar, one to three lines of text, no title and no frame
badge, because the badge was on the page before. Reviewed against `main` at
`9402620`; `git merge-base --is-ancestor 9402620 HEAD` confirms it.

**Nothing in this pass changes a single typeset token.** All 55 added lines
are comments and nothing was removed --- verified, not asserted:
`git diff -U0 preamble.tex | grep '^+' | grep -v '^+++' | grep -vc '^+%'`
answers `0`. So no page, no box, no cue and no tail can have moved, and the
sync session has no cue walk to do from this branch. That is the only reason
it was safe to work the issue without a build: **this container has no TeX
installation at all** (`pdflatex`, `latexmk` and the whole texlive tree are
absent), so I could neither build the book nor put a question to TeX in a
standalone probe, which is what made the one takeable half of this issue
takeable when the Part V batch met it.

## Retired --- two remedies that had already shipped

Both are the P01/P02 rule (*a review is a claim about the build it was made
on*) in its stronger form: not a finding that no longer reproduces, but the
**remedy** the reviewer specifies sitting in the tree, arrived at
independently from the same defect. That is now the third and fourth such
retirement, after the Part V sliver finding and the Part VI `needspace` one.

| suggested fix | shipped in | dated |
|---|---|---|
| 2. give `\transcript` the room test `\begin{fr}` has, sized to the listing | `5dc186c` (F08--F11 batch) | 2026-09-04 |
| 1a. a continuation mark so a fragment is never unmarked | `c3e3b8b` (Part V batch) | 2026-09-05 |

The issue was filed 2026-09-03, so both landed **after** it and both are on
`main`; `git merge-base --is-ancestor 9402620 5dc186c` and the same against
`c3e3b8b` both pass. The transcript guard is `\mfa@transcriptroom`, it boxes
the listing and turns the page when it will not fit, and it carries its own
`\typeout` ledger. The mark is `\mfacontinuationmark` on both shared styles.

**One clause of the issue survives that retirement and is worth carrying**:
the guard's own comment records "ONE split listing reported by the review
issue that prompted it", and #116 independently names two more --- P12's and
P22's --- from a build before the guard. That is a second reviewer confirming
the class was wider than the pages either of them happened to read, and it is
now recorded beside the ledger line in `preamble.tex`.

**And the mark is only half an answer, which the issue is right about.**
`overlay first and middle` marks every piece *before* the break and never the
piece *after* it, so the page the reader lands on still carries nothing. That
is the honest current state and it is now written where the styles are.

## Recorded rather than taken --- everything else, with the mechanism

`lines before break` / `lines after break`, `title after break`,
`breakable=false` under a height threshold, and a room test to keep a frame's
trailing box with its frame. **One reason covers all four: each moves
pagination by construction**, and the property that made the continuation
mark takeable holds for none of them --- an overlay is drawn inside padding
that already exists, so it adds no height and can be settled by counting fill
operators in a standalone file rather than by four book builds.

The full record, with the numbers, is in `preamble.tex` immediately above the
shared `\tcbset`. What is new there and was not available to anyone before:

- **436 admonition boxes in each edition**, 424 inside a frame and twelve in
  the Summary and Quiz regions; **296 (en) and 293 (pl) are the last thing in
  their frame**, and **65 in each are the whole of it**. So a trailing-box
  guard would fire at up to 296 sites per edition.
- Two mechanisms that each cost a cycle to rediscover. **`\needspace` does not
  work** --- already measured on `\mfa@namedframe`, 95pt reserved against 54pt
  left and the heading still stranded, because a breakable tcolorbox splits
  itself in its own code rather than asking the page builder; the working
  mechanism is the explicit `\pagegoal-\pagetotal` test. And **a continuation
  title needs a new string in both `lang/en.tex` and `lang/pl.tex`** --- there
  is none today, and parity's C3 fails a label defined in one language only.
- One figure there is labelled an **estimate and not a measurement**: at the
  issue's own eight-line threshold about 193 English and 197 Polish boxes
  would stop being breakable, dividing each body by 68 characters for a
  typeset line. It prices the option; it does not settle it.

The scale is the argument for not taking it blind. `\transcript`'s guard is
the closest precedent and it fires at single-digit-to-low-teens sites per
build; measured in isolation it cleared a split no editorial fix could reach
**and put three orphaned cues and three orphan tails back doing it**. A guard
an order of magnitude busier is not a change to make and measure in the same
build.

## Not taken as editorial fixes either, and why

The issue notes that individual instances would disappear under the recorded
two-sided rule (lengthen the frame so the box moves whole). They would, and I
did not, for two reasons that are both in `CLAUDE.md`: **fixing an instance is
not fixing the class** (P28), and a lengthening aimed at a page I cannot
render is a random walk taken blind --- the P32 pass needed seven rounds with
a build in front of it.

## Confirmed in source, not fixed

The "related shape" --- a frame's trailing box opening the next page above the
*next* frame's badge, so the reader attaches it to the wrong frame --- is real
and source-visible. `programs/en/P14-logic-proof.tex:199` is an `aibox` closing
frame 6 with `\begin{fr}` for frame 7 at line 211, and `:363` is a `note`
closing frame 16 with frame 17 at line 380. Both are among the 296 counted
above; neither is a defect in the source, and both need the guard.

## Frames whose length changed

**None.** No frame, no answer box, no figure and no listing was touched.

## Values emitted or retired

**None.** `make numbers` and `make verify` are unchanged by this branch, and
`figures/values/` is untouched.

## Gates

Run before anything was edited and again after, both clean:

- `parity.py` --- 56 file pairs, 1866 frames, 0 declared divergences,
  **0 failures and 0 warnings**
- `check_structure.py --frames --answers --outcomes --values --elicit
  --scripts --terms --parts` --- no FAIL or ERROR; 88 transcript references
  all backed, 84 Polish renderings all used, 9 part ranges all matching the
  manifest; elicitation 1030/1866 (55%), **unmoved**, because nothing was
  converted and no frame added
- `gen_stubs.py --check` --- 47 programs, 2418 planned frames, current
- `make numbers` then `make verify` --- **"All computed output is current:
  values and transcripts"**, with nothing stale at all. I had written
  "`appf.tex` STALE, which is expected" into this note before running it,
  from the feel of the expected output rather than from the output; this
  branch emits no value and moves no ledger, so there was nothing for
  `appf.tex` to be behind. Corrected here rather than quietly, because it is
  the class this repository keeps recording and it arrived inside the note
  about it.
- `make debt` --- 0 of 47 programs and 0 of 6 appendices are stubs in each
  edition, 0 verifybox blocks, 88 transcript references all backed, 84 Polish
  renderings all used, 9 part ranges all matching

`make`, `make a4` and `make all-formats` were **not** run, per the parallel
arrangement --- and could not have been, there being no TeX here.
