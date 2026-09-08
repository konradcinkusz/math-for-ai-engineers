# Hand-off: issue #180, the whole-book index and the twelve blockers

Issue #180 is the index and verdict for the full read of the English A4
edition. It is not a unit of prose: its own content is the **twelve blockers**
it says it re-verified itself, plus a UX picture and an index of sixty-eight
per-unit issues. So this pass is a verification pass on those twelve, and the
result is that **eleven of them no longer reproduce and one does.**

## The twelve, one at a time

Every one was read against current source before anything was touched, which
is the standing rule that a review is a claim about the build it was made on:
#180 was filed against `main` at 9402620, and the Foundation batch, the
blocker batch and the two Part VII batches have all landed since.

| # | blocker | verdict |
|---|---|---|
| 1 | *Which is larger, 1 TiB or 1.1 TB?* answered `1 TiB` | **retired** — F01 line 928 now answers `1.1 TB`, with both byte counts |
| 2 | *Fewer. About 4* for near-orthogonal capacity in `R^64` | **retired** — P05's frame now says the relaxation "cannot cost you anything", that the answer is "at least 64 whatever else is true", and that "the relaxation is not harder to satisfy"; the 4 is explicitly what random drawing buys |
| 3 | *the spread falls like `sqrt(B)`* | **retired** — P24 line 459 reads `1/\sqrt{B}` |
| 4 | P32 Summary item 8: the 40-layer bound "below what a `float32` can hold" | **retired** — both the frame and the Summary item now say the product is *representable* and name `float32`'s smallest normal; the `\result{}` replay into Appendix C carries the corrected version |
| 5 | P33 plateau arithmetic: the final-vs-first reading presented as the running minimum | **retired** — the frame now asks the two-reading question it computes, and a note box carries the running-minimum reading as `p33.p.flat.min` against `p33.p.flat` with the ratio |
| 6 | Appendix A Quiz Q5 gives the `beta = 0.9` value where the Quiz asked `beta = 0.98` | **retired** — the Quiz asks at `p33.beta.dash` = 0.98 and is answered with `p33.smooth.dash` = 0.101; the 22.9% figure for `beta = 0.9` is named as P21's and labelled |
| 7 | **F1 further problem 18's inequality is false, and the answer asserts it** | **FIXED — see below. The only live one.** |
| 8 | P12 further problem 2: beam width `2e82` printed as `10^84` | **retired** — emitted as `p12.beam.pct.width` = 1.98e+82 |
| 9 | P30 further problem 3: a Jensen–Shannon value given as the `ln 2` bound | **retired** — emitted as `p30.js.overlap` = 0.2158, with the frame explaining that the bound is attained on point masses, which this pair is not |
| 10 | P33 further problem 2: pooled mean 2.525 printed as 2.475 | **retired** — emitted as `p33.accum.pooled` = 2.525 |
| 11 | Appendix B still prints its `\programstub{}` | **retired** — `grep -rn programstub appendices/` returns nothing; the appendix opens by saying it is deliberately not a symbol table and why |
| 12 | GitHub Pages has never deployed (#110) | **recorded, not fixable in the tree — mechanism below** |

## The one that was live: F1 further problem 18

`Show that $10^{-3} < 2^{-10} < 10^{-2}$` — and `2^{-10} = 1/1024 =
0.0009765625`, which is **below** `10^{-3}`, not above it. So the exercise
asked the reader to show something false, and its answer asserted it: *"which
lies between `1e-3` and `1e-2`"*. Identical in both editions.

Fixed to `10^{-4} < 2^{-10} < 10^{-3}`, which is true, and the answer now
gives the step the wrong version fluffed: **`2^{10} = 1024` exceeds `10^{3}`,
so taking reciprocals reverses the comparison.** That is not an invented
justification — it is F01's own established fact, printed in three places in
the same program (the entry Quiz's own question, frames 30–31, and the
`\result{}`-wrapped Summary item, all quoting `f01.kib.over.si.pct` = 2.40),
so the corrected exercise now *uses* the program's headline instead of
contradicting it, and the reciprocal reversal is a real trap in its own right.

**No value was emitted, deliberately.** Every number in the corrected answer is
derivable from figures already on the page: `1024` is printed at F01 lines 492
and 497, and `1/1024 = 9.77e-4` to three significant figures is one division.
Emitting it would be a second copy of arithmetic the page already carries.

**The class is the one the review names as its own headline** — the wrong
numbers are in the places the gates do not reach. C7 asks whether every
`\val{}` has a script behind it and whether every emitted value is used; a
literal in an `\answerto{}` is neither, so it sits outside the mechanism the
whole book is built around, in the one part a reader opens *because they
already suspect they are wrong*. Note that **this one survived two passes that
covered it**: it is filed under both #124 (F01, closed by the F01–F06 batch)
and #123 (Appendix A, closed by the blocker batch), and neither caught it.

**The same list was then swept for a second instance**, because a class that
has been missed twice should not be fixed one at a time. Every `\answerto{}`
in F01 carrying a comparison was extracted and checked: `2^{10} = 1024` is
2.40% above `10^{3}`; `(2/3)^3 = 8/27`; `sqrt(a^2+b^2) < a+b` for positive
`a`, `b` via the `2ab` argument; and `10^6 < 2^20 < 3^13` with `2^20 ~ 1.05e6`
and `3^13 ~ 1.59e6`. All four are correct. There is no second instance.

## Frame lengths, and what the sync session needs to know

**No frame changed length.** The edit is entirely inside a `furtherproblems`
item and its `\answerto{}`, neither of which is a `\begin{fr}`, so no cue can
have moved for that reason.

Two things about it are still the sync session's to measure, and I am **not**
claiming either way:

- The body item changed from `10^{-3} < 2^{-10} < 10^{-2}` to
  `10^{-4} < 2^{-10} < 10^{-3}` — **the same character count, differing only
  in two superscript digits.** Whether that is width-neutral I could not
  measure: **this container has no TeX installation at all** (no `pdflatex`,
  `latexmk`, `tex`, `luatex` or `xelatex`, and no `/usr/local/texlive`), so
  the `\sbox` probe that would have settled it in seconds could not run. Its
  silence was instrument failure, not a measurement, and it is not recorded as
  one. The Appendix E pass measured the analogous text-digit substitution as
  width-neutral to the hundred-thousandth of a point because those digits are
  tabular; these are in maths mode and that reading is untested here.
- **The Appendix A answer grew from two source lines to four**, so the answers
  appendix is a little longer. That moves back-matter pagination rather than
  body pagination.

No page counts, no overfull-box multiset, no orphan-tail ledger and no
orphaned-cue walk are in this note, per the parallel arrangement — and they
could not have been taken here in any case, for the reason above.

**CI then answered part of the width question, and it is worth being exact
about which part.** Build run 212 came back green on all four formats, and
`build.yml` runs `checklog.py` as a hard gate and `checkpdf.py --cues=warn`
after it. So on CI's metrics — the fuller ones, with newtx and inconsolata
— this branch has **no error, no unresolved reference, no rerun or
label-drift warning, no overfull vbox, no overfull hbox over the 15 pt budget,
no stranded frame opener and no stranded section heading**, in every format.
That is as far as it goes: a box under 15 pt still passes, the cue check is
`--cues=warn` there by design, and the orphan tail is never fatal. **So the
page counts, the exact multiset and both of those ledgers are still the sync
session's, and the cue walk in particular is untouched by a green CI run.**

## Values

None emitted, none retired. `make verify` reports every computed value and
transcript current, `figures/values/appf.tex` included, so **no ledger moved
and there is nothing for the sync session to regenerate on this branch.**

## Recorded rather than taken

**#110, GitHub Pages, and the mechanism is worth writing down because the
obvious diagnosis is wrong.** The failure is at `actions/configure-pages` with
*Resource not accessible by integration*, which reads as a missing workflow
permission — and `.github/workflows/pages.yml` already declares exactly the
right ones (`contents: read`, `pages: write`, `id-token: write`) and names the
`github-pages` environment. So the token is not the problem: **Pages is not
enabled for the repository**, and enabling it is Settings → Pages → Source:
GitHub Actions, which nobody working in the tree can flip. There is no tree
change that fixes this, and adding one would be compensating for a switch
nobody has thrown — which is the shape the index/multicol chase already cost
this repository five CI cycles. Leave the workflow alone.

**The UX cluster is each its own open issue and each is a book-wide layout
change nobody has measured.** #180 lists them under *the four layout issues*
as though they were one `\section*` room test, one `breakable` policy and one
merged answer-box macro; the standing practice is to record them with the
mechanism, and the mechanisms are already known:

- **#115** (Quiz and *Can you?* headings stranded over a hole). The Part V
  batch established the diagnosis and it is now in its eighth consecutive
  batch: `quiz` *does* carry a room test, of `8\baselineskip`, and its box
  separately carries `lines before break=12` — the two disagree, so there is a
  window in which the reserve passes and the box then moves whole. And
  `checkpdf.py`'s heading check learns the **numbered** heading's size from the
  document, so a `\section*` left behind is invisible to it. **The instrument
  is owed before the sweep**, and the `\section` guard's own constant needed a
  sweep across four builds when it was chosen.
- **#116** (headless box fragments). Half of this shipped: the Part V batch
  gave every admonition the continuation mark `summarybox` had, measured at the
  mechanism as exactly one extra filled path on a broken box's first piece and
  none on its last, so it adds no height. *Marking* the break and *stopping* it
  are two different jobs whose costs differ by a whole build — stopping it is
  the room test above.
- **#117** (two answer-box treatments), **#118** (figures), **#119**
  (transcript type size), **#120** (blank versos — found and deliberately left
  in the F04 review pass), **#121** (orphan tails and orphaned cues — the
  reported-never-gated ledger, whose fix is a random walk across four
  paginations).
- **#157** (114 elicitations with the answer on the facing recto) is decided by
  **page parity**, so it is a property of the build and of the installation,
  and it is the one class in this list that no source-level gate can see.
- **#174** (48 elicitations spent in advance) has already been measured and
  deliberately not shipped: the second review batch prototyped the `\val{}`-key
  check #180 suggests and recorded the numbers — 103 hits naive, 14 when routed
  through `\teachesat` of which sampling found one genuine, and 0 / 1 / 3 / 14
  for 7- / 6- / 5- / 4-word phrase overlap once Quiz `\answerto{}` bodies are
  excluded. So **there are no verbatim seven-word leaks in the book and the
  real ones are paraphrases**, and choosing four words because it catches the
  case you already knew about is the threshold-chosen-so-a-claim-passes trap.
  The prose half is a reading job and the issue's own table of 48 is the
  evidence. Do not re-run it.

## Nothing found in a neighbouring program

The sweep above stayed inside F01. Nothing was touched in any other unit's
files, and no defect was found in one in passing.

## One thing about #180 itself, for whoever closes it

Its verdict quotes the book's own ledgers, and they have moved since it was
filed: 1863 teaching frames against 1864 now, 1626 computed values against
1673, and elicitation at 52% against 55% after the two part-wide elicitation
passes. Those are figures in an issue rather than in the book, so nothing was
edited for them — but they are the plainest evidence for the rule the
verification half of this pass rests on.
