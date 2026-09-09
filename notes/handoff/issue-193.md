# Issue #193 hand-off — the book cited research and carried no bibliography

Verified against `main` at `c9b8bb6`. The issue was filed against `f0a5660`, so
every finding was re-read against current source before anything was touched.

## What the issue got right, and it is the whole of the complaint

**Zero citations in the book.** No `\cite`, no `thebibliography`, no
`biblatex`, no `natbib`, no `\bibitem` in `programs/`, `appendices/`,
`frontmatter/`, `body.tex` or `preamble.tex`. Confirmed, still true at
`c9b8bb6`. The three claims in *What this book claims, and what it does not*
were three surnames and a year, and two of them had neither.

## THE FINDING THE ISSUE DID NOT MAKE: the one citation the book had was wrong

The box said **Kulik, Cohen and Ebeling's 1982 meta-analysis of the format in
secondary education**. Those three authors wrote a meta-analysis of programmed
instruction in **higher** education, and it is **1980**:

> J. A. Kulik, P. A. Cohen and B. J. Ebeling, "Effectiveness of Programmed
> Instruction in Higher Education: A Meta-analysis of Findings",
> *Educational Evaluation and Policy Analysis*, 2, 51--64, 1980.

The paper the book is actually describing is a different one by different
people:

> C. C. Kulik, B. J. Schwalb and J. A. Kulik, "Programmed Instruction in
> Secondary Education: A Meta-Analysis of Evaluation Findings",
> *Journal of Educational Research*, 75, 133--138, 1982.

Its abstract carries the book's two claims almost word for word --
*programmed instruction did not typically raise student achievement on final
examinations; nor did it make students feel more positively about the subjects
they were studying*. So the substance was right and the attribution merged two
neighbouring papers: the author list of the 1980 higher-education one with the
year and the setting of the 1982 secondary-education one.

**Fixed in both editions.** `frontmatter/en/how-to-use.tex:128`,
`frontmatter/pl/how-to-use.tex:128` (Polish declines it: *Kulik, Schwalba i
Kulika*).

That is this book's own recurring class arriving in the front matter: a claim
about a source written from memory, where two works that sit next to each
other in a literature have been run together. It is worth noting **which
instrument found it** -- not reading, but going to look the paper up. Nothing
in the repository could have caught it, and no amount of re-reading the
sentence would have either.

## What was done: a References section, §E.6, both editions

`\section{Where each attributed claim came from}`,
`\label{sec:E-sources}`, at the end of Appendix E in both editions. Two
tables on §E.5's own pattern -- the evidence for the method, then the results
the programs name -- plus a note on the citation format and a paragraph on the
one claim with no source.

**Every entry was checked against the journal's own record rather than written
from memory.** That was not fastidiousness: writing a bibliography from memory
would have committed the exact defect the issue is about, one level up, and the
misattribution above is what it looks like when somebody does.

> **And the first draft of this note said "ten entries" over a table of
> twelve**, as does the commit message, which is in the history and stays
> there. It is this file's own most-repeated rule -- never state a count of
> occurrences -- broken in the pass whose entire subject is claims nobody
> checked, in the sentence claiming everything had been checked. The fix is the
> one the rule prescribes: name the practice, not the tally, because a tally
> decays the moment somebody adds a row and nothing can see it.

| Source | Carries |
|---|---|
| Stroud, *Engineering Mathematics: Programmes and Problems*, Macmillan, 1970 | the format |
| C. C. Kulik, Schwalb and J. A. Kulik, *J. Educational Research* 75, 133--138, 1982 | the case against it |
| Roediger and Karpicke, *Psychological Science* 17, 249--255, 2006 | retrieval practice |
| Kornell, Hays and Bjork, *JEP:LMC* 35, 989--998, 2009 | errorful generation |
| Butterfield and Metcalfe, *JEP:LMC* 27, 1491--1494, 2001 | the confidence effect |
| Karpicke, Butler and Roediger, *Memory* 17, 471--479, 2009 | why it feels worse |
| Eckart and Young, *Psychometrika* 1, 211--218, 1936 | P11 |
| Efron, *Annals of Statistics* 7, 1--26, 1979 | P27 |
| Kingma and Ba, ICLR, 2015 | F02 |
| Ba, Kiros and Hinton, arXiv:1607.06450, 2016 | F02 |
| Vaswani et al., *NeurIPS* 30, 5998--6008, 2017 | F02, F08 |
| He, Zhang, Ren and Sun, *ICCV*, 1026--1034, 2015 | P25 |

Roediger and Karpicke's delays are 5 minutes, 2 days and 1 week, which is
exactly what the third warning box describes, so that box's claim is cited by
the same entry rather than needing one of its own.

**Format decisions, and each has a reason on the page.** Volume and page range
and no issue numbers -- an issue number is one more place for a transcription
error to hide and it buys nothing. No web addresses, which is the appendix's
own standing rule; where a work exists only as a preprint its identifier is
given, and the note says an identifier is a document number rather than an
address.

### Why §E.6 rather than a new appendix

The issue offered both. A new appendix after F would have displaced the book's
closing line -- *Which is all this book has ever asked you to require of
anybody* -- and inserting one before F would have renumbered F to G and gone
stale in every file that names Appendix F. §E.6 renumbers nothing, needs no
`body.tex` change, no new file and no new package.

And it belongs there on the merits: **§E.5's own closing paragraph already
names the gap this section closes.** It says *Program P27 names the paper the
bootstrap came from* -- i.e. Appendix E already tracked which programs name a
paper without giving its title, and had nowhere to put the title. §E.6 is that
place. The two jobs are kept apart in the section's opening paragraph, which
is what the issue asked for.

## The sweep, and the instrument that had to be replaced twice

The issue asks for "a sweep of the rest of the prose for anything else
attributed by name". **The first sweep was a grep over a list of names I had
thought of, which is the wrong instrument by construction** -- it can only find
what it already knows. Replaced with a pattern sweep for attribution phrasing
next to capitalised name groups, which then failed twice more:

1. **Line-oriented, so it found one hit.** The book wraps at 79 characters, so
   *layer normalisation, from Ba, / Kiros and Hinton* splits across source
   lines. This is the recorded phrase-versus-line class (P25's *before you turn
   over*). Re-run over the whole file with the wrap collapsed.
2. **Surname length threshold too high.** `[A-Z][a-z]{2,}` excludes *Ba*, *He*
   and *Xu*, which are real surnames -- so *Kingma and Ba* was invisible. Set
   the threshold below the shortest name that can exist, which is the lesson
   the Part II elicitation pass recorded about its own join detector.

Only after both fixes did the sweep find F02's two attributions, which are the
strongest case in the book: the aibox says *with the eps as the reference
implementations write it rather than as the paper does*, which is a claim
about what a specific paper prints.

Checking the Polish twins needed the same care: `grep Kingma` on
`programs/pl/F02` returns nothing because Polish declines it to *Kingmy*. All
attributions are present in both editions.

## The one claim left unattributed, deliberately

> Small steps and linear sequencing did not turn out to be essential;
> immediate reinforcement did not turn out to be critical.

**This is not in the 1982 abstract**, and no source was found for it. It is a
claim about the format's mechanism where the meta-analysis is a claim about its
results. §E.6 says so in as many words and names nothing, which is the same
treatment §E.5's *not surveyed* rows get and the same reasoning §E.4 gives for
its own names-without-verdicts. Putting up a paper that might contain it would
be the move the book spends forty-seven programs refusing.

The claims box points the reader at it: it now ends by saying every research
claim above is cited, and that this one is recorded as having no source.

## Findings retired, with the evidence

- **"One four-digit year in the English body text, and it is the 1982 above."**
  False at `c9b8bb6`. `programs/en/P27-inference.tex:336` carries *the original
  is Efron, 1979* inside a rigour box, in both editions;
  `frontmatter/en/introduction.tex:59` carries Stroud's *(1970)*;
  `appendices/en/appE-further-reading.tex` carries 2016 and 2024. The 1982 is
  in the front matter, not the body. It is a count of occurrences, which is the
  class this book forbids, and it decayed the usual way. **The finding it was
  offered as evidence for is sound regardless** -- the citations were missing --
  so nothing turns on it except the number.
- **"the optax `trace`/`ema` docstrings quoted in F04's momentum correction."**
  `grep -rn optax programs/ appendices/ frontmatter/` returns **nothing**. The
  optax quotation is in CLAUDE.md's F04 pass note, which is a repository
  document rather than the book, and F04's own note records that **no library is
  named on the page**, deliberately. Nothing to cite.
- **"the original transformer's feed-forward shapes used in F02's aibox."**
  Not retired -- taken. Vaswani et al. is cited for F02 and F08, and F08's
  *that is the motivation the original transformer's paper gives* is the
  stronger of the two claims.

## The knock-on, and why Appendix F was not edited

Appendix F's *That is the whole of what is outstanding, as far as anybody
knows* stands over four debts, and the issue says this is a fifth. **It is
discharged here rather than added**, so the sentence stays true and F is
untouched. The one residue -- the unattributed small-steps claim -- is recorded
in §E.6 as having no surveyed source, which is exactly where §E.5's *not
surveyed* rows live, and those are not in F's list either. Consistent, but
worth a second opinion when the sibling issues are triaged.

## For the sync session

- **No frame anywhere in the book was touched, so there is no cue to walk.**
  Cues live in frames; `how-to-use.tex` and `appE-further-reading.tex` contain
  none (parity reports 0 frames for both). Nothing I changed can strand a cue.
- **Pagination.** Appendix E grew by about a hundred lines in each edition and
  the front matter by six. `\mainmatter` resets the page counter, so the front
  matter cannot move a body page; an appendix is appended, so it cannot either.
  What can move is Appendix E's own pages, the index after it, and every PDF
  page number. Orphan tails inside Appendix E are the only page-level ledger
  exposed, and that one is reported rather than gated.
- **`figures/values/appf.tex` is NOT stale.** `make verify` returns
  *All computed output is current: values and transcripts*, exit 0. No value was
  emitted or retired, no transcript added, no frame added, so no ledger Appendix
  F prints has moved. Nothing owed on that front.
- **Four index entries added** (two per edition), all topic-shaped rather than
  names, so `--index` is unaffected: it still reports 82 names in 926 entries,
  every one printed in its own program.
- **A file header was falsified by this pass's own edit and is corrected.**
  `appE-further-reading.tex`'s *STILL OUTSTANDING: nothing in the book
  references this appendix* stopped being true the moment the claims box gained
  a `\ref{app:E}`. It now says what is true: there is still no `\ref{app:E}` in
  `programs/`, so a reader at a rigour box still has no route, and the
  front-matter pointer is the only route into the appendix the book has. That
  is the recorded class (Appendix D's pass, F12's) and it took one grep.

## Found in neighbouring files and NOT fixed

- **The book says it has forty-six programs and the manifest says forty-seven.**
  `frontmatter/en/titlepage.tex:8` (*Forty-six programs, worked*),
  `frontmatter/en/introduction.tex:80` (*Nine parts, forty-six programs*), and
  both Polish twins at the same lines (*Czterdzieści sześć programów*).
  `tools/programs.json` holds 47 and `gen_stubs --check` confirms it. This is a
  count of occurrences, on page one, in both editions. It is a different finding
  from #193 and the issue mentions sibling issues filed alongside it, so it is
  left for whoever owns the front matter's own unit rather than edited from
  under them.
- **`programs/{en,pl}/P07-tensors-shapes.tex:801` and `:804`** hard-code
  `\operatorname{Var}` and `\operatorname{Cov}` where the notation contract owns
  `\Var` and `\Cov`. Pre-existing; `check_structure --results` reports it and
  says no parity check can see it because both editions carry the same token,
  and Appendix C replays it verbatim. Reported, never fatal. P07's unit.

## Gates

Run before any edit and again after, all from source, none needing a build:

- `parity.py` -- 56 file pairs, 1866 frames, **0 failures, 0 warnings**, clean
  on the first run after the section was written. `appE` 49 numeric literals
  identical; `how-to-use` 19.
- `check_structure.py --frames --answers --outcomes --values --elicit
  --scripts --results --terms --parts --rigour --index` -- **exit 0**. Note the
  prompt's list omitted `--results`, `--rigour` and `--index`; all three were
  run.
- `gen_stubs.py --check` -- 47 programs, 2418 planned frames, current.
- `make verify` -- **exit 0**, all computed output current, nothing stale.
- `make debt` -- ledgers unmoved; its only FAIL is `reflist` needing
  `main-en.aux`, which is a build this pass is not permitted to run and which
  the tool itself labels as such.
- The three prose instruments against `HEAD` -- **zero over-long lines, zero
  lost paragraph breaks**. Ten JOIN candidates, every one an ordinary word in
  newly added prose that splits into two the file already contains (*Another*,
  *format*, *Everything*, *samego*, *przypominanie*), with the line-length
  instrument reporting zero for each. That is the recorded two-instrument
  false-positive pattern, and neither instrument was trusted alone.
