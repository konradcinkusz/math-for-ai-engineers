# Hand-off — issue #2, the tracking issue

Issue #2 is not a program. It is the **contract** every program issue pointed
back at, and it is the last issue open in the repository: #3 to #52 and every
`review` issue are closed. So resolving it means one thing — verify the contract
clause by clause against the finished book, correct the repository wherever it
carries the same stale clause the issue does, and close it.

Nothing in `programs/`, `appendices/` or `code/` changed. No frame, no value, no
transcript, no figure. The diff is five documents and one Makefile target.

---

## What the contract promised, and what is actually there

Measured, not remembered. Every figure below is from the tool named beside it.

| Clause | Measured | Instrument |
|---|---|---|
| No `\programstub{}` left | 0 in `programs/`, 0 in `appendices/`, both editions | `make debt` |
| Both editions, or neither | 57 file pairs, 1866 frames, **0 failures, 0 warnings** | `parity.py` |
| Outcomes declared, *Can you?* generated | every program, and the panel precedes the Test exercises | `--outcomes` |
| Frames in the 30–70 band | every program in band | `--frames` |
| Every exercise carries `\answerto{}` | every one | `--answers` |
| 2–4 Mermaid diagrams per edition | min 3, max 4, 150 per edition | counted here |
| At least one trap frame | every program has one | counted here |
| Every number computed | 1718 values, all referenced, all present | `--values` |
| Structure current | 47 programs, 2418 planned frames | `gen_stubs --check` |

`reflist.py` and `checklog.py` are the two clauses that need a build. They are
not run here — the four-format build is the sync session's, and a fresh clone
carries no `.aux` or `.log`. The PR touches `preamble.tex`, so it is not a
markdown-only diff and CI runs the full matrix against both of them.

**F13 sits outside 30–70 at 23 frames and that is correct.** Its brief plans 20
deliberately, and `--frames` takes the band from `programs.json` when a program
plans short, which gives it 15–26. The tool agrees; the clause does not need
relaxing.

---

## The claim the issue got wrong, and the five places it had spread

The contract says **"Quiz on Foundation programs only."** Every one of the
forty-seven carries a Quiz, and has for a long time. CLAUDE.md records this
found stale in the front matter (P04 pass), in `\lblCanYouFooter` (F04 review),
in `\lblQuizIntro` (F01–F06 batch), and in eight consecutive program issues'
checklists — and every one of those passes fixed the site in front of it and
swept no further. This is the sweep-is-as-wide-as-the-artefact finding again,
and the artefacts nobody opened were these:

1. **`README.md:61`** — the skeleton table's Quiz row. The first thing anybody
   reads, and the Appendix D pass rewrote this file *because* it was stale and
   left the row.
2. **`preamble.tex`**, the comment above `\begin{quiz}` — carrying **both**
   corrected claims at once, the scope *and* "the same test on the way out", in
   the file that implements the Quiz. Three places were swept for the retake
   claim; the implementation was not.
3. **`notes/01-curriculum.md` §14** — the skeleton "made mechanical", item 2,
   plus §3's "both the diagnostic on entry and the exit test", plus §21's
   dependent sentence, which reasoned from the scope claim to conclude that
   §16's 80/80 obligation was unmeasurable. Half of that argument survives and
   is now the one it rests on: the standard is contaminated because the same
   items serve entry and exit, not unreachable because thirty-four programs
   lack a Quiz.
4. **`notes/04-macro-design.md` §6** — "`quiz` — **Foundation only, enforced**".
   Both halves wrong. `grep -n quiz tools/*.py Makefile` finds no check and no
   warning, so the "warning rather than an error" it described has never
   existed.
5. **`Makefile`, the `debt` target** — and this is the one that matters most,
   because it is a **ledger**, printed to the CI step summary on every build.
   Its 80/80 entry said the Quiz "runs on the thirteen Foundation programs
   only, so a standard defined against it would be unmeasurable on thirty-four
   of the forty-seven". The instrument whose job is to report the truth about
   the book was reporting a false claim about it, on every build.

All five are corrected in the book's own idiom — the old claim is quoted rather
than silently replaced, because a fix that hides what was there teaches nobody.

---

## Two claims about the tooling, both one grep from settled, both false

Found by testing the assertion rather than reading it, which is the only thing
that has ever caught this class.

**`notes/04` §6 said the quiz rule is *enforced*.** Nothing enforces it. There
is no check and no warning anywhere in `tools/` or the `Makefile`.

**`notes/04` §14 described a `Package mfa Warning` mechanism that does not
exist.** Seven per-program counts, emitted by LaTeX, read out of the log by CI
with one grep. No such warning is emitted anywhere; `\mfaminframes` and
`\mfamaxframes` were never defined; and the section's Makefile snippet globs
`programs/*.tex`, which predates the `programs/{en,pl}/` split.

That matters more than the individual claims, because **the file opens by
promising "Everything below was compiled. Nothing here is proposed and untested;
where something is untested it says so."** Its own §14 falsifies its headline
guarantee. It is the sharpest instance of this class in the repository: a
document that states its reliability and then breaks it, three hundred lines
down.

Four of the seven planned counts do exist — the frames band, outcomes against
`\canyou`, exercises against answers, and `\val` keys against computed values —
but in **Python reading the source**, not LaTeX writing a log. Three were never
built and nothing replaced them: a Program with no quiz, a Program with no
summary, and solutions recorded without `\listofanswers`. None has ever fired as
a defect, which is why nobody noticed. §14 now says which is which.

---

## One number a document disagreed with itself about

`notes/01-curriculum.md` §21 said the book is "47 programs and roughly **2,415**
frames". §1 of the same file says **2,418**, and `gen_stubs.py --check` prints
2,418, and the manifest sums to 2,418. The odd figure was derived from nothing
and sat twenty sections from its own contradiction, in the file this repository
tells everybody to re-derive the sequence from. Corrected, with the old number
named.

---

## Claims I did **not** fix, and why

- **`notes/01-curriculum.md` §3's "Assumes genuinely nothing"** is contradicted
  by the Foundation payoffs, and §22 of the same file already records that the
  curriculum review found it and that the front matter was corrected instead.
  The note is the historical record of a finding, not a live claim. Left.
- **`frontmatter/*/how-to-use.tex`'s "work the thirteen Foundation Quizzes and
  nothing else"** is a *reading strategy*, not a claim about which programs have
  a Quiz. It is correct and it stays. `notes/05` quotes it accurately.
- **`notes/04` §14's Makefile snippet** globs the pre-split path. Named in the
  correction rather than rewritten, because the whole snippet is a design-time
  artefact and rewriting it would make the section look built.

---

## For the sync session

Three things, none of them mine to touch under the parallel-session rules.

**CLAUDE.md's ledgers are stale by the last two merges.** It carries 1673
computed values, 54 Polish renderings, 492 labels, 56 file pairs and
968/1863 frames eliciting at 51%. The tools now print **1718**, **84**, 57 file
pairs and **1030/1866 at 55%**. `reflist.py`'s label figure needs a build. Every
one of these moved under `b71a573` (issue #117) and `602b03e` (pl terminology
#195), and neither pass swept the prose. This is the fourth or fifth time this
file has recorded that the gated copy in `figures/values/appf.tex` is caught by
`make verify` while the ungated sentence is not — `make verify` is green here,
so the appendix is current and only the prose is behind.

**CLAUDE.md's *What is left* item 3 says "E2 and E7 are unclaimed and free".**
`notes/01` §17's Status column now reports **E7 as run, P27 pass**. E2 is the
one free experiment nobody has claimed; E4 needs a trained model and E5 was
deliberately answered another way.

**`notes/handoff/` holds thirty-one notes that were never folded in or
deleted**, this one included. The instruction each pass was given says the sync
session does both.

---

## Gates

Run before any edit and again after every one. All green, all reading source.

```
parity.py            0 failures, 0 warnings   57 pairs | 1866 frames
check_structure.py   --frames --answers --outcomes --values --elicit
                     --scripts --terms --parts        exit 0
                     --results --site --rigour --index exit 0
gen_stubs.py --check 47 programs, 2418 planned frames; current
make numbers         exit 0 — no committed value moved
make verify          exit 0 — values and transcripts current, appf.tex NOT stale
make debt            exit 0
```

`make verify` reports `appf.tex` current rather than stale, which is the
expected result here rather than a lucky one: this pass emitted no value and
retired none, so no ledger the appendix prints has moved.

No build was run, no page count measured, no overfull-box table taken and no
orphaned-cue walk attempted. Pagination is global and belongs to the sync
session.
