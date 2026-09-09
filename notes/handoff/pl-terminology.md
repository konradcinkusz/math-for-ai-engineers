# Hand-off: issue #195 — three unsettled Polish renderings, and a pointer that renamed its own referent

Unit: the Polish edition's terminology, book-wide. Branch `claude/pl-terminology`.
Verified against `origin/main` at `c9b8bb6`; the issue was written against
`f0a5660`, and the book moved in between.

**No build was run.** No page counts, no overfull-box table, no orphan-tail
ledger, no orphaned-cue walk — the sync session owns those. The frames whose
length changed are listed under *What moves a line* below.

---

## The decision, which is what the issue asked for

The issue asks for a decision on three terms and then either the sweep or a
recorded refusal. **The refusal is recorded, and the fixes that do not need the
decision are taken.** The line I drew, and it is the whole of the reasoning:

> Settling `partia`/`wsad`/`batch`, `zanurzenie`/`embedding` and `krok
> uczenia`/`współczynnik uczenia` is a **new editorial call about a whole
> edition**. Bringing strays inside a call the book has **already made** is
> not, and neither is repairing a pointer that lands on a different noun from
> the one it cites.

Everything below sorts into those two boxes.

---

## Fixed

### 1. The cross-reference the issue names — `programs/pl/P18-matrix-calculus.tex:157`

Reproduces exactly as reported. P18 attributed a sentence to P06 using `wsad`
where P06:476 writes `partię`:

- P18:157 `…biblioteki układają **wsad** wzdłuż pierwszej osi` → `…układają **partię** wzdłuż`
- P06:476 `Prawdziwe frameworki układają **partię** wzdłuż \emph{pierwszej} osi`

The two now agree word for word. This is the one the issue calls "the instance
a reader actually trips over", and it is a navigation defect rather than a
terminology preference: the citing sentence quotes a statement and renamed it.

### 2. `paczka` — a **fourth** rendering of *batch*, named by neither the issue nor Appendix D

Not in the issue's table, not in Appendix D, and undocumented anywhere. Six
occurrences across three programs, every one meaning *batch*, and **five of the
six sit in passages citing P21, which writes `partia` 55 times**:

| file:line | was | now | cites |
|---|---|---|---|
| `programs/pl/P25-clt-monte-carlo.tex:256` | `rozmiarze paczki` | `rozmiarze partii` | P21 |
| `programs/pl/P25-clt-monte-carlo.tex:264` | `paczki cztery razy większe` | `partie …` | P21 |
| `programs/pl/P25-clt-monte-carlo.tex:265` | `paczka cztery razy większa` | `partia …` | P21 |
| `programs/pl/P26-maximum-likelihood.tex:83` | `gradient z paczki` | `gradient z partii` | P21 |
| `programs/pl/P26-maximum-likelihood.tex:84` | `po każdej paczce` | `po każdej partii` | P21 |
| `programs/pl/P26-maximum-likelihood.tex:988` | `o gradiencie z paczki` | `o gradiencie z partii` | P21 |
| `programs/pl/F05-functions-graphs.tex:746` | `od paczki, na którą` | `od partii, na którą` | — |

`grep -ri paczk programs/ appendices/ frontmatter/` now returns **zero**.

Why this is inside the line rather than the sweep: `partia`, `wsad` and `batch`
are all catalogued in Appendix D with a reason each, and all three are in real
Polish ML use. `paczka` is none of those things — it is a stray outside the
decision the author has already recorded, and retiring it makes the book
consistent with Appendix D rather than making a new call.

**`paczka` and `partia` are both feminine**, so every agreeing adjective and
relative pronoun in those seven sentences is unchanged. Each was read back in
full; the Polish is correct.

**P26:988 sits OUTSIDE its `\result{}`** — it is the attribution clause the
Appendix C pass deliberately leaves outside the mark — so nothing replayed into
Appendix C and no Appendix C edit was needed. That split did its job.

### 3. Appendix D — its note was made false by fix 1, and its `batch` row stated a count that had already gone stale

Appendix D has **moved since the issue was filed**: it now lists four terms, not
three, and it already carried a note about the P18/P06 cross-reference. So "if
not swept, say so in Appendix D" was already done by a later pass. What was left
undone was the one-line fix — and once that landed, the note describing it was
false.

- **The note** (both editions) now describes the one live instance that a
  pointer fix *cannot* repair: `P32-transformer-derived.tex:1056`'s
  outstanding-work row sends the reader to P08 and P11 for the spectrum of a
  real embedding matrix, writing `macierz zanurzeń` — which P11:453 also writes
  and **P08:627,899 does not** (`macierz embeddingów`). The row names two
  programs that disagree with each other, so there is no word to change at the
  pointer. The note says so, and says it is the argument for settling
  `embedding` first — which is the issue's own view.
- **The `batch` row** said *"All three, for one object … Expect all three."*
  That is a count of occurrences, the class CLAUDE.md forbids, and it had
  already decayed by exactly the predicted mechanism: `paczka` was underneath
  it. The row now names the rule instead — `partia` is the base and the only
  one that compounds (`mikropartia` is built on it); `wsad` survives for the
  adjective `wsadowy`, which `partia` cannot form; `batch` is the borrowing —
  and says the number is deliberately not counted, because it was once and a
  fourth had appeared under it.

**Appendix D's `wsadowy` justification was checked and is true and
load-bearing**: `wsadowy` occurs 8 times, all in P07, all as `wskaźnik
wsadowy` / `wsadowy wielogłowicowy wynik uwagi`, and `partia` has no adjective.
Those 8 are **not** part of any sweep — they are forced.

### 4. Appendix F — the universal over four items omitted this debt

`\section{What this book does not claim}` prints *"That is the whole of what is
outstanding, as far as anybody knows."* over the 80/80 warning and three named
debts. The unsettled Polish renderings are recorded in Appendix D two
appendices earlier and were not among them, so the English edition contradicted
itself. A fourth debt is now named, in both editions, and "Three other things
are owed" → "Four".

---

## Recorded rather than taken, with the mechanism

### The sweep itself

~150 noun replacements across ~20 Polish files (measured: `partia` 153 in 15
programs, `wsad` noun 27 in 7, `batch` 31 in 5; `zanurzenie` 55 in 9 against
`embedding` 8 in 5; `krok uczenia` 18 in 8 against `współczynnik uczenia` 13 in
5).

**Mechanism, and why not here:** every one of those is Polish prose, so the
sweep re-rolls Polish pagination in twenty programs at once — the largest
single pagination change this book has recorded. P32's pass priced one
program's worth of that at seven rounds of the orphaned-cue chase. This session
is explicitly barred from running a build, so it cannot walk the cues, and a
sweep taken here would hand the sync session an unmeasured book-wide layout
change on top of several other parallel units. That is the standing treatment
for a book-wide layout change nobody has measured.

**And the substantive reason, which is the issue's own:** overruling a native
speaker's word choice across a whole edition is the author's decision. The
issue asked for a decision; it did not delegate the word.

### THE THING THAT SHOULD DECIDE IT — the book disagrees with its own stated rule

This is not in the issue and it is the most useful thing this pass found.

**Both of the book's own rule documents prescribe the borrowings**, and the
Polish edition does the opposite:

- `notes/03-bilingual-and-notation.md:609–611` — *"Polish practitioners write
  embedding, transformer, token, softmax, attention, dropout, batch. Rendering
  embedding as zanurzenie … "*; line 625 gives `embedding` as the recommended
  rendering and line 634 gives **`batch` / *partia*** with the gloss *"Partia is
  understood; batch is what is said."*
- CLAUDE.md's *Non-negotiable conventions* says the same thing and names
  `zanurzenie` as **the** example of the calque not to use.

Measured, the Polish edition runs `zanurzenie` 55 : `embedding` 8, and `partia`
153 : `batch` 31. **The book went against its own brief, roughly seven to one,
in both terms.**

So this is not a tie to be broken on taste. Either the sweep goes toward the
borrowings and the book comes into line with a rule it already publishes, or the
rule is wrong and `notes/03` and CLAUDE.md have to be corrected. **They cannot
both stand.** Nothing in the repository compares a translator rule against the
prose it governs, which is why this survived.

`notes/03` was **not** edited: it is the same editorial decision, and if the
author sweeps toward the borrowings it is already right.

### `P32-transformer-derived.tex:1056` — a pointer that cannot be repaired at the pointer

Described under fix 3. It needs the word settling; there is nothing to change
locally, because the row cites P11 (which agrees with it) and P08 (which does
not). The compound *embedding matrix* runs `macierz zanurzeń` in P11, P29 and
P32 against `macierz embeddingów` in P08 alone — 3:1, with P08 the outlier.

### `F01-numbers-powers-roots.tex:393`, `F02:672`, `P07:137,140`, `P09:703`

The `embedding` borrowing where it is the reader's search term or a countable
noun. Part of the same open question. `P09:703`'s *Rotary position embedding*
is **not** a divergence — it is the proper name of a technique, correctly kept
in English by the book's own rule.

### Observed and deliberately left

`appendices/{en,pl}/appD-terminology.tex` §D.4 opens *"Four terms in this book
are rendered more than one way in the Polish edition."* That is a count, and it
is an unverified universal about the body: making it true means auditing every
term in the book for double rendering, which nobody has done. It is milder than
the row's count was, because the evidence is the table directly beneath it
rather than the body of the book — so it cannot decay silently in the same way.
Left, and named here so the next pass meets it rather than rediscovering it.

`\dash` count in Appendix D is en=10 pl=11 and was so at `HEAD`. Not a defect:
`dash` and `emph` are both in parity's `PROSE_MACROS`, which C14 excludes by
design, because a translator may need a different number of them.

---

## Retired — checked and not fixed

- **The issue's counts do not reproduce.** It reports *partia* 220 in 13
  programs, *wsad* 35 in 8, *batch* 42 in 6, *mikropartia* 10 in 1. Measured on
  cleaned prose at `c9b8bb6`: 153 in 15, 35 in 8 (of which **8 are the forced
  adjective `wsadowy`** and 27 the noun), 31 in 5. The **shape** reproduces —
  every one of the three divergences is real — and the numbers are a claim
  about `f0a5660`. Nothing was fixed on the strength of a number from the
  issue.
- **`mikropartia` is not a fourth rendering of *batch*.** It is *micro-batch*,
  a different object, and it is a compound **of** `partia` — which is positive
  evidence that `partia` is the settled base noun. 16 occurrences, P21 and P33,
  consistent throughout.
- **"If not swept, say so in Appendix D" was already done.** A later pass added
  the record and the P18/P06 note. Retired as no-longer-outstanding; what was
  left was the fix, which is taken above.
- **A hypothesis of my own, refuted.** I tested whether `wsad` and `partia`
  split by collocation — `wsad` for batch-as-configuration, `partia` for
  batch-as-collection. They do not: *batch size* is written both ways,
  `rozmiar wsadu` in F12 and P12 against `rozmiar/wielkość partii` in P21, P33
  and P24. There is no rule being observed. Recorded so nobody re-runs it.
- **Three of my own sweep's candidates were instrument artefacts**, each
  retired by reading the file:
  - `P15-gradient.tex:185` — every `parti` hit in P15 is `\partial`
    (`\index{derivative!partial}`, `\partial f/\partial x`). My script did not
    strip maths or `\index` arguments, which is **exactly** the trap
    `check_structure.py`'s own comment on `--terms` warns about. The documented
    instrument defect, reproduced.
  - `F04-sums-products-sequences.tex:1267` — a two-line window straddling two
    `\sumitem`s; the `\ref`s belong to the previous item. F04 writes `batch`
    uniformly, 21 times, and is internally consistent.
  - `P26-maximum-likelihood.tex:373` — my `prób[kc]` stem matched
    `wypróbowałeś`; P19 has no `próbka` in the ML sense, and the citation is
    about Jensen's equality case. `wariancja z próby` is the collocation
    Appendix D says is correct.

**Instrument discipline.** The cross-reference sweep was checked against a known
answer before its silence was believed: it had to find `P18:157` citing
`prog:P06` with `wsad`, and it did. The prose detector refuses to run with no
arguments (`no files given -- refusing to report a clean tree`, verified by
running it bare), because `flagged 0` from an empty loop is byte-identical to
`flagged 0` from a clean tree.

---

## What moves a line — the sync session's signal to walk the cues

**Eight one-word swaps in Polish prose**, seven of them length-neutral:

- `paczki`→`partii`, `paczka`→`partia`, `paczce`→`partii`, `paczki`→`partie`
  are all **six characters to six**. `F05:746`, `P25:256,264,265`,
  `P26:83,84,988`.
- **`P18-matrix-calculus.tex:157` is the only length change**: `wsad` (4) →
  `partię` (6), **+2 characters**. The line is now 79 characters and it is
  inside a `\begin{note}` inside a frame. This is the one place a Polish line
  could re-flow, and it is in P18.

**Appendix D and Appendix F each gained prose** — the D note is four lines
longer in each edition, the D `batch` row three, and F gains a paragraph of
nine lines in each edition. Both are **back matter**, which CLAUDE.md records as
moving no page boundary in the body: the only defect class available to an
appendix is one of its own lines overflowing, and no line I wrote exceeds 78
characters.

**No frame was lengthened or shortened**, so I do not expect a cue walk from
this unit — but P18:157 is the one line that could have re-flowed and it is
worth a look.

---

## Values

**None emitted and none retired.** `make verify` reports *All computed output is
current*; `figures/values/appf.tex` was **not** touched and did not go stale,
because this unit emits nothing.

## Gates — all green, run before the build that was not run

```
parity.py                56 file pairs | 1866 frames | 0 declared divergences
                         | 0 failures, 0 warnings                      exit 0
check_structure.py --frames --answers --outcomes --values --elicit
                   --scripts --terms --parts                           exit 0
  84 Polish renderings named in Appendix D, every one used in the prose.
  88 transcript references, every one backed by a committed file.
  9 part ranges in each introduction, every one matching the manifest.
  BOOK 1030/1866 frames elicit (55%) — unmoved; nothing converted, no frame added
gen_stubs.py --check     47 programs, 2418 planned frames; current      exit 0
make numbers / make verify   All computed output is current             exit 0
make debt                    all ledgers as before                      exit 0
prose detector           1 false positive ('cannot' — `can`+`not`, and the
                         line-length instrument reports nothing for it); 1
                         pre-existing 128-character line at
                         P26-maximum-likelihood.tex:988, which was 128 at HEAD
                         and is one of 121 such lines in that file — left, on
                         the Part II pass's finding that rewrapping them is
                         churn.
```
