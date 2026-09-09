# Hand-off — issue #110, GitHub Pages has never deployed

Unit: infrastructure, not a program. Branch `claude/pages`. Nothing under
`programs/`, `appendices/` or `frontmatter/` was touched, so **no frame changed
length and there is no cue walk owed.**

## The one finding that is not mine to fix

**Pages is still not enabled, and no file in this repository can enable it.**
Creating a repository's first Pages site is an administrative action;
`administration` is not a scope a workflow can grant its own `GITHUB_TOKEN`,
so no value of `enablement:` and no `permissions:` block reaches that call.
The fix is one click by a repository admin: **Settings → Pages → Build and
deployment → Source → GitHub Actions.** Every push after it deploys with
nothing further needed in the tree.

That is why the issue should stay open until somebody clicks, whatever else
this branch fixes. Until then the README's four download links and the badge's
own href resolve to nothing.

## What I retired, and on what evidence

- **"`enablement: true` cannot create the site; the workflow does not say
  so."** Already fixed, by `b1862d3`, two commits before I started. The
  comment now states the mechanism and a guarded step writes the Settings fix
  to the job summary. **Confirmed live rather than by reading**: in run
  34331393420 that step ran and succeeded at 09:08:37, one second after
  `configure-pages` failed. The mechanism fires.
- **"README line 5 shows a Pages deployment badge for a site that has never
  deployed."** Retired deliberately. That badge is a *live* shields.io query
  against the `github-pages` environment — it reports "no deployments" because
  there are none, and it will report a deployment the moment there is one. It
  is the only element of the four the issue names that cannot go stale, and
  removing it would remove the one honest indicator on the page. Its *href*
  404s today, but so do the download links, and both are fixed by the same
  click.
- **"README … still says … forty-six of forty-seven programs are stubs."**
  No longer reproduces: the README's status paragraph was rewritten at
  `9402620` (the Appendix F pass) and now reads "Complete draft. All
  forty-seven programs and all six appendices are written". The issue was
  filed against that same commit, so this half of the finding was stale on
  the day it was written. **`docs/index.html` was not** — its last commit is
  `7fc402b` and it still carried the F1-only banner.

## What I fixed

### The workflow: a one-second gate that ran after seventeen minutes

`configure-pages` ran **last**, after the diagram render, four LaTeX compiles
and every gate. Measured on the two most recent runs, which are the shape all
89 failures share:

| run | green steps | then | upload / deploy |
|---|---|---|---|
| 34328269747 | 17 min 14 s | 1 s to fail here | skipped |
| 34331393420 | 17 min 33 s | 1 s to fail here | skipped |

Moved to immediately after `checkout`. Safe because nothing downstream reads
its outputs — the site is assembled from `docs/` and the four PDFs, and
`upload-pages-artifact` takes a path — and it is where GitHub's own starter
workflows put it, ahead of the build rather than behind it. On a repository
with no Pages site the job now fails in seconds with the Settings fix in the
summary; on one where it exists the step costs a second wherever it sits.

**Moving it falsified two things in the same edit**, and both are corrected in
the same commit rather than left:

- the step's own comment said the failure came "with the book itself compiling
  clean and every gate above passing" — no longer true when it runs first;
- the summary it writes said "Every PDF compiled and every gate above this step
  passed", which would have sent a reader to four logs that do not exist. It
  now says nothing was built and why that is deliberate.

**And a third, which the reorder exposed rather than caused.** `Report what was
published` carries `if: always()`, so it fired at 09:08:36 in run 34331393420
and headed the job summary "## Published to Pages" — on a run that published
nothing. With the gate now upstream it would have fired before a single PDF
existed. It is `Report what was built`, guarded on
`hashFiles('main-en.log') != ''`, which keeps the original intent (leave a log
summary behind even when a later step fails) and stops it reporting a
publication that did not happen.

### The landing page, which was stale in eight places

`docs/index.html` had not been touched since `7fc402b`. Every one of these was
checked against the thing it describes before it was changed:

1. **The banner** — "Early draft … Program F1 in both languages are done — 163
   pages on A4 … Forty-six of forty-seven programs are stubs." Now the true
   status, with **no page count and no count of what is written** beyond the
   structural 47 the manifest gates: a page count moves on every build, which
   is how this one got to be out by a factor of seven. Banner accent red →
   amber, because red is the colour of an error and "complete draft" is not one.
2. **"Ten experiments … none has been run."** False since the P20 pass.
   `notes/01` §17's Status column shows E3, E6, E7, E8, E9 and E10 run and E1
   half run. Replaced by the rule, with **no total**, because a total is the
   claim CLAUDE.md records as having decayed unread in two documents already.
3. **"Thirty-eight of them are catalogued."** A count of occurrences; the
   catalogue is at 328. Replaced by the practice.
4. **"Nearly every frame ends by asking … over one program that happens forty
   to seventy times."** That is the *frame band* read as the *elicitation
   count*. The measured rate is 55% book-wide and 45–55% across P01–P34, so
   the second sentence is out by about a factor of two — and "thirty to
   seventy" is false of F13 anyway, which is 22 frames by design.
5. **"Same source, same page for page."** The two formats paginate differently
   by construction. Replaced with that, and with why it does not matter:
   nothing in the book navigates by page.
6. **"The book contains no digits of its own."** A universal the book states an
   exception to — arithmetic the program is teaching is written inline.
7. **"CLT and Monte Carlo"** in the contents. P25's title is "…the central
   limit theorem, concentration and initialisation"; no section of it touches
   Monte Carlo, which the P23/P25/P26 batch established.
8. **The floors.** The page claimed only the mathematical one. The
   introduction (`frontmatter/en/introduction.tex:23–30`) states two, and the
   second is the one a reader can be caught by.

### The README carried three of the same defects

Items 3, 4 and 7 above are in `README.md` too, word for word in two cases —
one defect in two artefacts, which is this repository's own recurring finding
that fixing an instance is not fixing the class. All three fixed there as well.
Its "none has been run" was the same false claim as the landing page's.

Also added, under the download links: **the same four PDFs are attached to
every run of the build workflow as artefacts, kept for fourteen days.** That is
a route that works today for a reader whose link 404s, and it is phrased so it
stays true once Pages is live rather than needing removal. It does **not** say
"attached to every release": `release.yml` attaches `*.pdf`, but no release has
ever been published, and a promise about a workflow nobody has run is the exact
claim this issue is about.

### And the five figures both pages print are now gated

`README.md` and `docs/index.html` each argued that every number in this book is
computed rather than remembered, and each made that argument with the same five
Program F1 figures **typed in by hand**. All five re-derive from
`figures/values/f01.tex` — I checked before changing anything, and none was
wrong. They were the only digits in this repository with no script behind them,
in the two artefacts a reader meets before the book.

`tools/check_structure.py --site` reads a `data-val="key"` attribute off each
figure and compares the rendered text with what the script now produces. It
fires in the direction that actually breaks them — a value moving under a page
nobody edited — which `make verify` is structurally blind to, because it
compares a values file with the script that wrote it and those two stay in
perfect agreement while a page quoting them goes stale.

Proved by mutation, four ways, before it was believed: untagged pages (fires),
a figure changed to `13.0` (fires, names the key and both values), a key
misspelled (fires, says it names no computed value), `--soft` (reports, exits
0). Restored and green at 18 figures across the two pages.

Wired into `make check`, `make site` (which should not assemble a site whose
figures have drifted), `make debt` via a `frontpage` target — **not** `site`,
which is taken by the existing local-assembly target — and both workflows.

## One of my own corrections was the defect it replaced

The first draft of item 4 read "More than half of them end by asking you for
something" after a clause that had just localised to "a program". The book-wide
rate is 55%; the lowest program is **45%**. So as a per-program claim it is
false of at least one member while true of the ensemble — which is the
quantifier class this batch catalogued three instances of, committed in the fix
for it. Caught by re-reading my own replacements against the ledger rather than
against the feel of the fix, before the push. Both pages now say "over half the
frames in the book", which is the quantity that is measured.

The experiments sentence went the same way one notch smaller: "names the pass
that ran each" is true of the rows that have run and not of the four that have
not. It records what became of each now.

## Recorded rather than taken

- **`build.yml` carries `paths-ignore: ['docs/**', '**.md']`,** so a docs-only
  or README-only pull request runs no CI at all and the new `--site` gate does
  not run on it. Widening that means a full four-format LaTeX build on every
  landing-page typo, which is the wrong trade. The hole is covered where it
  matters: `pages.yml` has no `paths-ignore`, so the edit-the-page direction is
  caught there before anything is served, and the values-change direction —
  the one that breaks a page nobody touched — is caught in `build.yml`, because
  `code/` and `figures/` are not path-ignored. The asymmetry is written into
  the check's own comment.
- **No page-level measurement was taken and none is owed.** I ran no build, so
  no page counts, no overfull-box multiset, no orphan-tail ledger and no cue
  walk. Nothing I touched is typeset.

## Found in a neighbour, not fixed

- **`notes/02-grounding-and-traps.md:338`** — experiment row E4's specification
  still reads "for each of the **41** items". The catalogue is at 328, and
  CLAUDE.md records that this tally was retired from the file's heading and
  from CLAUDE.md itself precisely because it had come apart. It survived in the
  experiments table. One number, one line; left because `notes/02` is shared
  and a parallel session may be in it.

- **`tools/check_structure.py:247`** — `check_elicitation`'s docstring is not
  a raw string and contains `\blank` and `\yourturn`, so **every invocation of
  this tool in every job prints `SyntaxWarning: invalid escape sequence '\y'`**
  before its own output. Visible in the CI log of run 34333946874. One
  character to fix (an `r` prefix on that docstring), and left alone because
  that function belongs to another unit and a parallel session may be in it.

## Values

None emitted, none retired. `figures/values/` is untouched, so `make verify`
reports only `appf.tex`, which is the sync session's.

## Gates

Every source gate, run before anything else and again at the end:

```
parity.py                56 file pairs | 1866 frames | 0 failures, 0 warnings
check_structure --frames --answers --outcomes --values --elicit
                --scripts --terms --parts     green
                --results --rigour --index    green
                --site                        18 figures across 2 pages
gen_stubs.py --check     47 programs, 2418 planned frames; current
```
