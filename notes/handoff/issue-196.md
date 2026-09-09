# Appendix F, the companion library (issue #196) --- hand-off

Unit: the *What this book does not claim* section of Appendix~F,
`\label{sec:F-owed}`. Both editions edited; no other unit's files touched, and
no program file touched at all.

**Written to `issue-196.md` rather than to `appf.md` on purpose.**
`notes/handoff/appf.md` is already occupied by the pending hand-off from the
Appendix~F review pass (issue \#176, commit `7971bb1`), which the sync session
has not yet folded in. Overwriting it would have destroyed another unit's note
before it was read. The `issue-174.md` precedent already in this directory is
the form followed here. **The two passes do not overlap**: \#176 restructured
F.2 and F.3 and the ledger tables, and left both paragraphs this pass edits
exactly as they were.

Gates, all run before any edit and again after, all green: `parity.py` 56 file
pairs / 1866 frames / 0 failures and 0 warnings, with `appF-manifest.tex` at
46 ordered tokens, maths identical, 2 numeric literals identical;
`check_structure.py --frames --answers --outcomes --values --elicit --scripts
--terms --parts`; `gen_stubs.py --check`; `make numbers`; `make verify`
reports every computed output current, **`appf.tex` included --- no value was
emitted and none retired, so `appf.tex` is NOT stale from this pass.**

---

## The finding reproduces, and its three supporting claims reproduce with it

The issue was verified against `main` at `f0a5660`; this pass re-checked every
one of its claims against `c9b8bb6` before touching anything, because a review
is a claim about the build it was made on. All of them hold.

- The paragraph is at `appendices/en/appF-manifest.tex:261` and its Polish
  twin at `:264`, word for word as quoted.
- **The name never appears in the book.** `odzera` occurs in
  `notes/01-curriculum.md:597` and `CLAUDE.md:16599` and **nowhere** in
  `programs/`, `appendices/`, `frontmatter/`, `body.tex` or `structure.tex`.
- **Nothing built.** `code/` holds 48 files: the 47 per-program value scripts
  and `appf_ledgers.py`. No staged library anywhere in the tree.
- **Nothing in the book depends on it.** The one mention above is the only
  one. Note the near-miss: `programs/{en,pl}/P34-measuring-honestly.tex`
  carries three references to the **companion volumes**, which are the two
  sibling books in the series and are real. Two different things sharing a
  word; the P34 references were checked and left alone.
- **`sec:F-owed` is referenced from nowhere**, so the section could be edited
  without chasing pointers.

---

## Fixed, in both editions --- the promise is cut

**The three sentences are gone.** The issue offers two clean options and says
the middle ground is the bad one; this pass takes the cut, and the argument
for it is the one the issue makes and this pass confirmed.

What a reader loses is nothing, and that is checkable rather than a judgement.
The other two debts in that list close a loop the reader has already met: the
trained-model measurements are marked where they appear in the programs, and
the uneven elicitation rate is something the reader has felt for fourteen
hundred pages. The companion library closes no loop, **because no loop was
opened** --- the paragraph was the first and only mention, and it gave no name
and no address. Its whole information content for a reader was *there is a
thing you have never heard of, and it does not exist.* A book that announces a
companion and never names it is worse than one that does not mention it.

Building it was not a live option for a review pass and should not be read as
having been declined lightly: it is eight stages of software, it is
`CLAUDE.md`'s *What is left* item 6, and **its stage 01 wants a real embedding
matrix**, which is the same trained-model dependency as this appendix's own
first debt. The design survives untouched in `notes/01-curriculum.md` \S18 and
in `CLAUDE.md` item 6. Only the book's announcement of it goes.

**The lead-in count moved with it**: *Three other things are owed* is now
*Two*, and *Trzy inne rzeczy* is *Dwie inne rzeczy* (feminine plural, so
*dwie* and not *dwa*). The count is kept rather than dropped because it is not
the class this repository forbids: every recorded instance of a decaying tally
was a claim about material elsewhere in the book, and this one sits directly
above the two bolded paragraphs it counts, where a reader settles it in one
glance.

---

## Fixed, in both editions --- the knock-on, and why the fix is not a longer list

The section closed on **\enquote{That is the whole of what is outstanding, as
far as anybody knows}** over four items. The issue says that sentence is now
false. It is, and this pass confirmed it against the tree rather than against
the issue's word --- three debts a reader filed on the same morning are
outstanding and are not among the four:

| issue | the claim | confirmed by |
|---|---|---|
| \#193 | the book cites research and carries no bibliography | `frontmatter/en/how-to-use.tex:128` and `frontmatter/pl/how-to-use.tex:128` name *Kulik, Cohen and Ebeling's 1982 meta-analysis*; the tree has **zero** `thebibliography`, `biblatex` or `\cite{` |
| \#194 | no copyright page and no ISBN | **zero** matches for `isbn`, `copyright`, `\textcopyright` or *all rights* in any `.tex`; `frontmatter/en/` is three files, none of them a copyright page |
| \#195 | three Polish terms rendered three ways | recorded in `CLAUDE.md`'s Appendix~D pass as deliberately unswept and carried on *What is left* |

**The fix is not to name those three.** A list of four that a reader falsified
in one morning becomes a list of seven that the next reader falsifies, which
is the decaying tally this book spends its length teaching people to distrust
--- and it would put it in the appendix whose subject is exactly that.

So the sentence now says what is durable and true, and it is the stronger
statement rather than the weaker one:

> Those are the debts this book knows about, and whether they are all of them
> is not something this page can establish: what is on the page can be
> counted, and an absence nobody has yet noticed cannot.

That is a fact about what counting can do, so it cannot go stale when an
eighth issue is filed. **And it repairs an argument the section was already
making against itself.** The clause immediately after it says this appendix is
*a claim about the book, of exactly the kind the preceding pages spend their
length teaching you to distrust* --- so the old sentence made the strongest
available claim, a complete inventory, one line before telling the reader to
distrust claims of that kind. The connective is now *So*, which is the logic
the paragraph wanted: because completeness cannot be established, this page is
a claim like any other. The closing line, *Which is all this book has ever
asked you to require of anybody*, is untouched and now follows properly.

The Polish takes the same shape with no `\dash{}` introduced --- the English
paragraph has none, and one added on the Polish side alone would have diverged
C14 for a punctuation mark.

---

## Recorded rather than taken --- mechanism named

**Naming the three new debts in the appendix.** Mechanism: the appendix has no
machine-countable source for *what is missing*, so any enumeration is
hand-maintained prose in the one place the book claims its numbers are
counted rather than remembered. It went stale in under a day the last time it
was written. If a later pass wants those three on the page, the durable form
is to give each its own bolded paragraph beside the two that remain --- a
different kind of debt each, as the lead-in promises --- and to drop the
lead-in's count at that point, not to extend a sentence claiming completeness.

**`CLAUDE.md` *What is left* item 6 and `notes/01-curriculum.md` \S18 are
untouched**, per the do-not list, and both remain true: the library is
specified and unbuilt. The sync session may want one clause on item 6 noting
that the book no longer announces it, so that a future pass does not read the
cut as the design having been abandoned.

---

## For the sync session

- **No frame length changed anywhere.** An appendix has no frames and
  therefore no next-frame cues, and no program file was touched. **There is no
  cue walk owed by this pass** --- the same reasoning the \#176 hand-off gives.
- **Appendix~F got shorter**: about five lines of prose out of each edition,
  against a rewritten closing paragraph of the same length. Appendix~F is the
  last `\include` in `body.tex:45`; **`\printindex` follows it at `:50`**, so
  this shifts the index's page boundaries in both directions of the format
  matrix. That is worth naming rather than assuming harmless: the index's
  balanced last page is where every one of this book's recorded overfull-vbox
  complaints has landed, and it is the one region a back-matter *shortening*
  can reach. Nothing in the body can move.
- **Values: none emitted, none retired.** `appf.tex` is not stale from this
  pass, and `$\val{appf.elicit.pct}$` is still referenced in the paragraph
  above the one rewritten, so C7 stays green --- checked.
- The elicitation ledger is unmoved at 1030/1866: nothing converted, no frame
  added or removed.
- **Issue \#196 is answered by the cut.** Its *Knock-on* section is answered
  too, and the three sibling issues it points at (\#193, \#194, \#195) are
  left open and unaltered --- they are other units' work, and the closing
  sentence no longer depends on their state.
