# Issue #174 --- 48 elicitations spent before the reader reaches them

The synthesis issue for the spoiler class. Reviewed against `main` at
`9402620`; `git merge-base --is-ancestor 9402620 HEAD` confirms six review
batches have landed since it was filed, so every finding was read against
current source before anything was touched. **Thirteen of the twenty majors
no longer reproduce.** Seven survive and are fixed here, in both editions.

## The mechanical half was already worked, and is not re-opened

The issue proposes a check: *a `\val{}` key appearing both in a program's
opener and in one of its answer boxes is nearly always a spoiler*. **The
second review batch (`e581f33`) prototyped it, measured it and recorded why
it was not shipped** --- naive 103 hits, routed 14 with one genuine in a
sample of four, phrase overlap 0 at seven words. Its conclusion stands and
is not re-litigated: the discriminator is semantic (a value can be
*scenario* in the opener and *payload* in the answer, and nothing syntactic
separates them), and choosing a four-word shingle because it catches the
case you already knew about is the threshold-chosen-so-a-claim-passes trap.

So this pass is the **prose half**, which the issue itself says is a reading
job. That reading confirmed the prototype's own sampling twice over: of the
five `\val{}` cases it named (P32, P10, P17, P25, P33), **two were still
live** --- P32 and P33 --- and both are of exactly the STATE kind the
sampling isolated.

## Retired --- verified against current source, not against the notes

| finding | evidence it no longer reproduces |
|---|---|
| F1, fig F1.1 gives three of frame 6's five answers | `f01-number-sets.mmd` now draws 4, -3, 1/3, 0.1, e, pi. None of the frame's five. F01--F06 batch |
| F5, entry Quiz asks both elicited traps | Both items **ask**; answers are in Appendix A, not on the opener. The second review batch adjudicated this exact item as triage on the recorded STATE-vs-ASK criterion. No new evidence, so not re-opened |
| F11, fig F11.3's last node states frame 27's answer | Node C now restates frame 26's own trapbox, which sits above it *in the same frame*. F08--F11 batch |
| P8, transcript in frame 16 answers frame 17 | Split into `p08-least-squares` + `p08-orthogonality`. Part III batch |
| P10, opener Note prints frame 40's answer | Note now withholds which two properties: "which two, and why each follows, is section 5's to elicit". Second review batch |
| P15, transcript pre-answers frame 18 | Split; `p15-directional` now sits after frame 19. Part V batch |
| P16, listing prints frame 34's answer | Split into `p16-relu` + `p16-inplace`. Part V batch |
| P17, Quiz Q4 prints frame 24's answer | `c3e3b8b` removed "and lands on the minimum of a quadratic in one step". Part V batch |
| P18, opener states **p** - **y** | grep for the span in the opener returns nothing. Part V batch |
| P23, frame 13 gives away section 4 | The "hold on to" / "section 4 is entirely about" clauses are gone. Part VII A |
| P25, two Quiz items hand over frames 33 and 52 | Both now **ask**; answers in Appendix A. Part VII A |
| P28, frame 5 trap prints frames 9--10's answers | The two measured clauses are cut. Part VII B |
| P32, Summary item 8 contradicts frame 22 | Now says the number *is* representable and names underflow as the realistic case. Blocker batch. (Its `\result{}` replay into Appendix C was corrected with it --- one fix, two places.) |

## Fixed --- seven, both editions

1. **P32 Quiz Q3** printed `\val{p32.plain.bound}` in its stem, which is
   exactly what frame 21 asks the reader to derive and frame 22 answers.
   The Quiz *question* had been reworded by an earlier batch; the spoiler
   had not. The stem now gives frame 21's own **given** --- a product of one
   factor per layer, each at most 1/4, which frame 21 states outright before
   asking --- so the scenario survives and the payload does not. Route,
   answer and difficulty unchanged.
2. **P10 Quiz Q1** stated "$A$ sends $(1,1)$ to $(3,3)$", and frame 1 asks
   "apply $A$ to $(1,1)$ --- what comes out?" with frame 2 answering
   $(3,3)$. Changed to $(2,5) \mapsto (8,20)$, eigenvalue 4: the triage
   question (do you know the words?) is untouched and frame 1's arithmetic
   is no longer spent.
3. **P20 frames 23, 25, 26.** Two spoilers for one question. Frame 23's
   display wrote the denominator $\sqrt{v} + \varepsilon$ --- the epsilon
   **outside** --- and frame 25 then printed $\eta/(1+\varepsilon/|g|)$,
   which is the outside form's own consequence, immediately above the dots
   asking *where should the epsilon go, inside or outside?* Frame 23's
   display now reads $g/\sqrt{v}$, which is precisely the units argument the
   frame makes and nothing more; frame 25 introduces the epsilon as a guard
   **without placing it**; and the exact-first-step display moves down into
   frame 26, where it is the consequence of the answer. The transcript in
   frame 24 prints only numbers, so it does not place the epsilon either ---
   the shortfall it shows is now a puzzle frame 25 resolves rather than a
   restatement.
4. **P31 frame 24's aibox** ended "...and it would have come out positive on
   **shuffled labels**", two lines above "There is a check that costs one
   extra run" / "What is it?" --- whose answer is *shuffle the labels*. Now
   "...and nothing in the number itself would say so", which sets the
   question up instead of answering it.
5. **P33 Quiz Q6** printed `\val{p33.fit.resid}` in its stem; frame 42 asks
   for it and frame 43 answers it. The stem now says the points lie on the
   line "closely enough that no plot would show the difference", which is
   what the triage question needs and is frame 43's own wording for the
   consequence rather than its figure.
6. **P34 outcome 4** promised "and why its agreement figure does not tell
   you" --- which is frame 25's yes/no answer, printed on the opener. Now
   "and what would have to be known about the judge to correct for it": the
   skill without the finding, which is the remedy the F03, F04 and F08
   passes each applied to an outcome.
7. **P34 frame 35** stated, in bold, "**the model's contribution cancels**",
   one frame before frame 36 asks "what cancels out of that comparison?" and
   frame 37 answers "The model." The numbers under it (same model, two
   tokenisers, two bits-per-character figures) supply the last step even
   without the bolded clause, so both went. The numeric illustration is
   **moved into frame 37's answer**, where it confirms rather than reveals;
   all five `p29.*` keys stay referenced there and in P29.

## Frames whose length changed --- the sync session's signal to walk the cues

No frame was added or removed anywhere, and no cue was added or removed, so
`\nextframe` placement and every `\teachesat`, `\outcome` and `\sumitem`
payload are untouched. Lengths moved in six places:

- **P20 frame 23** shorter by one maths token (the epsilon).
- **P20 frame 25** shorter by one display, longer by roughly one line of
  prose --- net about two lines shorter.
- **P20 frame 26** longer by one display plus two lines.
- **P32 Quiz Q3**, **P33 Quiz Q6**, **P10 Quiz Q1**: each within a line of
  its previous length; these are opener items rather than frames, so they
  move the opener's own pagination and everything after it in that program.
- **P34 frame 35** shorter by about six lines (a paragraph and five `\val{}`
  spans removed).
- **P34 frame 37** longer by about six lines (the same material, relocated).

**P20 and P34 are the two to watch.** P34's pair very nearly cancels, but
frames 35 and 37 are three frames apart, so the intervening break can move.
P20's three edits are consecutive and net roughly one line longer.

## Values, and the ledger this pass ended up owning

None emitted and none retired by this pass, and elicitation is unchanged at
1028/1864 (55%), because it converted nothing and added no frame.

**It did regenerate `figures/values/appf.tex`, 1674 -> 1677**, which the
parallel arrangement had reserved for a synchronising pass. The reason is
that this branch was later asked to merge itself: the P34 review (#178)
added three values and left the ledger at HEAD by the same rule, so `main`
was carrying `appf.values = 1674` against a real count of 1677, and CI's
"Recompute every number" job gates hard on `$(COMPUTED)` drift. The P20
session hit exactly this one merge earlier and regenerated it for the same
reason. **A branch that merges itself cannot hand the ledger on.**

## A collision with another live session, test-merged

**PR #201 (`claude/issue-34-resolution-u6ucib`) is editing P20 at the same
time**, and it touches the same section. Its change is confined to **frame
24**: it splits the single shortfall figure into two, emitting
`p20.adam.shortfall.lo`, so the frame now reads "not by the same amount in
both". Mine are frames 23, 25 and 26.

**It merged first, and it composed exactly as the test merge predicted.**
A `git merge --no-commit` had auto-merged both editions with no conflict
before either landed, and the real merge did the same. More usefully, the
two compose rather than merely coexisting, and the composed reading is better
than either alone:

- frame 24 (theirs) now shows **two different** shortfalls;
- frame 25 (mine) explains why they differ --- the departure is the
  epsilon's, and it is largest where the gradient is smallest;
- frame 26 (mine) gives the formula as the consequence of the answer.

Observation, then mechanism in words, then the question, then the formula.

**One thing to check on the real merge.** That branch's commit message says
the two shortfalls differing "is exactly what the next frame explains with
eta/(1 + eps/|g|)". After this pass the *next* frame explains it in words and
the **formula** sits one frame further on, in frame 26, because printing it
in frame 25 was one of the two spoilers fixed here. The section still
delivers it; only its position moved, and moving it is the fix. No edit is
needed --- but whoever merges should read frames 24 to 26 once as a run,
because neither session saw the other's text.

Nothing else was found in a neighbouring program. Every edit is inside the
seven units named above.

## One instrument defect, recorded because it is the standing class

The prose detector I wrote for this pass reported `flagged 0` on a deliberate
`carries a` -> `carriesa` mutation. Its split loop was `range(2, len(w)-1)`,
which cannot reach a split whose second half is one letter, so `carries|a`
was unreachable --- and `flagged 0` is the answer you expect, so there was
nothing to be surprised by. Caught only by mutation, which is
Program P34's rule (watch the instrument produce an answer you already
know). Fixed to `range(1, len(w))`, re-proved on the mutation, and the six
candidates it then reported on the real files are all ordinary
single-letter inflections (`factor|s`, `know|n`, `czynnik|a`, `czynnik|i`)
with the line-length instrument reporting zero for each --- the recorded
two-instrument false-positive pattern. The detector also refuses to run with
no file arguments, per the Part III elicitation pass's finding.

## Recorded rather than taken

**The class cannot be closed by this pass, and the issue says so.** Three
widenings of rule 2 and four recorded Quiz cuts are the evidence that
reading does not scale to 1864 frames; the mechanical check that would scale
was measured and rejected, with numbers, in `e581f33`. What is left is the
**28 minor and cosmetic instances** the issue routes to the per-program
issues, and the two related issues it names:

- **#157**, 114 elicitations whose answer sits on the facing recto. That is
  pagination rather than authorship, it is a property of the installation as
  much as of the source, and it needs a different fix --- the same reasoning
  that makes the orphaned cue a hard gate locally and a warning in CI.
- **#118**, the figures.

The one structural option nobody has costed: the six sources differ in
whether they print **before frame 1** (Quiz, outcomes) or beside the frame
(figure, transcript, admonition, own prose). Only the first two spoil the
whole program, and only the first two are written last, when the author
knows every answer. A check restricted to those two regions is a smaller
problem than the one the prototype measured --- but it is the same semantic
discriminator, so it would need the author to adjudicate its hits, and a
gate nobody can clear is the permanently-red ledger this repository refuses.


## A second collision, which did NOT compose: P34, and the resolution

**PR #210 (the P34 review, #178) merged while this branch was open, and it
fixes two of the same findings** --- outcome 4 and frame 35. Both conflicts
were that overlap. Neither resolution loses behaviour, so it was resolved
here rather than escalated, and it is a composite:

- **outcome 4 -> theirs.** "what its published agreement figure is a
  statement about" removes the spoiler as cleanly as this pass's wording,
  and P34 is that pass's unit.
- **frame 35 -> this pass's, and the reason is a finding.** Their fix
  replaced "the model's contribution cancels" with "**one of the two factors
  belongs to the tokeniser**", in bold --- which is frame 37's own opening
  sentence, one frame before frame 36 asks the question. It also kept the
  numbers under it, and "the same model reports two different figures" is one
  step from "the model cancelled": Program P02's rule that supplying the last
  step of an answer is as much a spoiler as stating it. This pass moves the
  illustration into frame 37, where it confirms rather than reveals, and that
  hunk merged cleanly, so the two compose.

**The generalisable half, and it is new.** Two sessions reading the same
issue found the same two defects and fixed them differently, and one of the
two fixes was incomplete in a way only visible from the *other* pass's
reading. A duplicated fix is not wasted work: it is a second reading, and
where the two disagree the disagreement is the signal. What it costs is a
conflict, and the conflict is where somebody has to know both readings ---
which is an argument for the per-program issue and the synthesis issue not
being worked in parallel on the same unit.

**One thing left un-reconciled, deliberately.** The detector reports 18
candidates on the merged P34 and every one is pre-existing: `origin/main`'s
Polish P34 carries 111 lines over the wrap width and so does this tree, so
they came in with #210 and are not this pass's to sweep.


## A third collision, and it is the one worth keeping: P31

**PR #211 (a P31 review, issue #45) merged while this branch was open and
rewrote the same aibox.** Its rewrite is *better on the substance* --- it
replaces "the estimate is dominated by its own bias" with the regime
argument, that a few hundred items over that many cells is far below the
items per cell the bias formula needed, so the formula does not apply and
whatever the bias is, it is of the order of the quantity itself. That is
section 4's own point and it belongs there.

**And its last sentence reintroduced the defect this issue files for P31**:

> A run on labels with no relationship to the input at all would have come
> back positive too.

Two lines below it the frame asks *What is it?*, and the answer block reads
*Shuffle the labels and re-run the whole pipeline --- the labels keep the
distribution they had and lose every relationship to the input.* So the
sentence is the answer, in the answer's own words, above the question. It is
the same spoiler this pass had just removed, rewritten from scratch by
somebody fixing something else in the same box.

Resolved as a composite in both editions: their regime argument in full,
their final sentence replaced by "nothing in the number itself would say so".

**This is the strongest evidence in the run for what the issue argues.**
\#174's thesis is that the class cannot be closed by a rule, because reading
for it does not scale. Here a careful pass, working the same box, with the
rule written down in CLAUDE.md, reintroduced the spoiler within hours of its
removal --- not by ignoring the rule but by rewriting the sentence for an
unrelated reason and not re-reading it against the question two lines below.
**A spoiler is not a defect you fix once; it is a defect the next edit to
that paragraph can recreate**, and nothing in the repository can see it.

That is an argument for the narrow mechanical check this pass declined to
ship, but only in the two regions that print *before frame 1*. It is not an
argument for one over the whole book: the prototype's numbers still stand.
