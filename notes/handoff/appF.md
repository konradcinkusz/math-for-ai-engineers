# Appendix F (issue #52) — hand-off

## What the issue asked for, and what was already spent

**Five of the six "Done when" boxes were already ticked before this pass
started**, by PR #108 (which wrote the appendix) and PR #176 (which reviewed
it). Verified rather than assumed, one at a time:

| Checklist item | State |
|---|---|
| `appendices/en/appF-manifest.tex` written, stub deleted | done — no `\programstub` anywhere in `appendices/` |
| `appendices/pl/appF-manifest.tex`, entry-for-entry identical | done — the two files carry identical `\val` keys, `prog:` references, experiment ids and structural macros, all in the same order |
| Ledgers generated from `tools/`, CI fails on disagreement | done — `code/appf_ledgers.py` writes `figures/values/appf.tex`, `make verify` gates it, and `build.yml`, `pages.yml` and `release.yml` each diff `figures/values` after regenerating |
| The measurement table prints | done, and **the issue's own premise is stale** — see below |
| 80/80 states NOT ESTABLISHED and explains the instrument | done — §F.4's warning box, naming the scored Test exercises and saying why not the Quiz |
| `\listofdiagrams` descriptions one useful line each | **not done — this pass** |

**The measurement table is deliberately not what the issue asked for, and that
is right.** The issue says to print "empty cells for the nine unrun
experiments", written when none had run. Five have since run (E3 in P05, E6 in
P20, E8 in P30, E9 in P25 and P32, E10 in P33), one is half met (E1 in P02) and
four are not run. The appendix prints three tables headed *Run*, *Half run* and
*Not run*, with a paragraph on why E5 is the interesting one. Printing empty
cells against five experiments that have run would be the fabrication the
issue's own warning is about, pointing the other way. **No change made; the
issue's checklist is the stale document, not the appendix.**

## The one thing that was genuinely outstanding

CLAUDE.md's Appendix F pass note says §F.1 "is `\listofdiagrams` and a
paragraph, its coordinates cannot be wrong, and it needed no work at all."
Measured, that is true of the **mechanism** and was not true of the **copy**.

`\mermaidfig{key}{caption}{copy}` writes `\texttt{key.mmd} --- copy` into the
manifest. Parsed with a brace matcher over all 300 calls (a regex captures the
caption instead of the copy — P27's pass recorded that and it is still true):

| | before | after |
|---|---|---|
| entries whose copy contains no content word its own key lacks | **28** | **0** |
| shortest copy | 8 characters | 12 |
| median | 22 | 27 |

Twenty-eight English lines printed the filename and then the filename again:
`p18-two-routes.mmd --- two routes`, `p19-one-basin.mmd --- one basin`,
`p31-two-routes-one-number.mmd --- one number`, `p27-what-to-resample.mmd ---
the unit`. Against the house register, which is a short phrase naming what the
picture shows — `p10-bowl-or-saddle.mmd --- eigenvalues classify a form`,
`p21-noise-and-batch.mmd --- batch size and the spread`.

**34 keys rewritten, in both editions**: the 28 the measurement names, four
more whose English was a thin fragment the metric missed (`p18-one-transpose`,
`p27-what-to-resample`, `p27-winner-is-noise`, `p31-what-a-margin-drops`), and
two whose English was sound while the Polish was a two-word stub
(`p20-each-fixes-one`, `p32-score-assembled`). Every replacement was written
from the diagram's own `.mmd` node text rather than from its key or its
caption, so the line says what the reader would see.

## What was NOT touched, and why it is safe

- **No `.mmd` source changed**, so no diagram was re-rendered, no width moved
  and no figure's position on the page moved. Rendered widths are therefore
  exactly what the programs' own passes measured; nothing to re-measure.
- **No `\val{}`, no script, no transcript, no frame, no payload.** No value was
  emitted or retired. `make verify` reports all computed output current, so
  `figures/values/appf.tex` is **not** stale from this pass.
- **Rule 2.** The manifest copy is the fourth place P18's pass says to read.
  Every new line is a compression of the figure's own nodes, which each
  program's pass already checked against the frames on both sides, so no figure
  is more revealing than it was. None states a conclusion its figure withholds
  — `p17-why-the-step-caps` is the one to watch, and it names the factor its
  own first node states rather than the "steepest direction sets the cap"
  sentence P17's pass removed from its last node.
- **No digits and no maths spans** were added to either edition, so C8 and C12
  have nothing to diverge on; parity came back 0 failures, 0 warnings.

## Source formatting

Replacing the copy joined 31 calls whose argument had been wrapped mid-word
across two source lines, taking them past 79 characters. They were re-wrapped
to `}{%` plus an indented continuation — **the book's own idiom, 64 occurrences
in the tree before this pass**, including `f01-magnitudes`, whose 70-character
manifest copy ships in Appendix F today. Every changed source line is within 79
characters.

## For the sync session

- **No build was run**, per the parallel arrangement: no page counts, no
  overfull-box multiset, no orphaned-cue walk. The manifest column in
  Appendix~F is the one place this change can show. P32's pass retired the
  48-character line budget by measurement — 153 of 284 manifest lines were at
  or over it with none overflowing, because `\@dottedtocline` wraps, and what
  actually overflows is a long unbreakable `\texttt{}` key. **No key changed**,
  and the longest copy added is 45 characters against an existing maximum of
  124. Confirm on the four-format build.
- **Appendix~F is at the back**, so a manifest line that wraps to a second line
  lengthens Appendix~F and moves nothing in the body — the same argument the
  Appendix C, D and F passes each measured.
- **Two ledger figures in CLAUDE.md are stale and were deliberately not
  edited**, being ledger prose the sync session owns: the debt entry says *54
  Polish renderings named in Appendix D* where `make debt` now prints **84**,
  and the Appendix D pass note's own figures were left as written. Neither is
  this pass's doing; both are noted because they are the class that only gets
  read when somebody writes a number down.
- CLAUDE.md's Appendix F pass note's "it needed no work at all" about §F.1 is
  the claim this pass falsified, and is worth correcting there.

## Gates

    parity.py                 56 file pairs | 1866 frames | 0 failures, 0 warnings
    check_structure.py        --frames --answers --outcomes --values --elicit
                              --scripts --terms --parts   all green
    gen_stubs.py --check      47 programs, 2418 planned frames; current
    make verify               all computed output current
    make debt                 80/80 NOT ESTABLISHED, as it must be
