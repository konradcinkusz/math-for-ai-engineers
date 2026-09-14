# The `ab-ovo` session prompt

The brief for the Claude Code session that starts the learning application,
`ab-ovo`, in its own empty repository. It is written on the pattern of
`architecture-standards/docs/MASTER-PROMPT.md` — a fixed preamble that says
*read, do not re-derive*, a target block, phases with verification gates, and
ground rules — and for the same reason that document exists: so the session
brief is written once, reviewed once, and not retyped from memory on the day
the repository is created.

**It is the instance, not the procedure.** The procedure for an empty
repository is `docs/scaffold/INIT-GENERIC-TEMPLATE.md`, installed as
`/init-generic-template`; the procedure for every ticket after that is
`docs/delivery/WORKFLOW.md`. Neither is restated below, on the rule
`docs/delivery/GENERATE-MASTER-PROMPT.md` §3 gives every generated prompt: a
prompt that retypes an installed procedure is a fork of it that drifts. What
is below is the half that varies — this product, these decisions, this order.

**Every decision in it is recorded somewhere else first.** The name and the
multi-track requirement are issue #239 §6–§7 on this repository; the five
ADR-shaped decisions are `notes/10-learning-app.md` §6; the plan and its lab
map are §7. If this prompt and those disagree, they win and the disagreement
is a finding to fix here, which is the precedence rule
`GENERATE-MASTER-PROMPT.md` §2 gives a generated prompt in its last block.
Change a decision where it is recorded, then change this file; never the
other way round.

**And it is not a ticket's master prompt.** Those are generated per ticket
from an analysis document by `/generate-master-prompt`, inside the `ab-ovo`
repository, once it exists. This is the brief that gets the session to the
point where that loop can start.

## What to attach to the session

| Repository | Access | Why |
|---|---|---|
| `konradcinkusz/ab-ovo` | write | Empty: nothing tracked beyond `README.md`, `LICENSE` and `.gitignore` (`INIT` §2), or the procedure refuses. The only repository the session writes to. |
| `konradcinkusz/architecture-standards` | read | The constitution, the scaffold procedure, the guides and the delivery workflow. Attach it, or install `architecture-core@architecture-standards` and `ticket-delivery@architecture-standards` from its marketplace; `MARKETPLACE.md` §"Attaching versus installing" is the trade-off. |
| `konradcinkusz/math-for-ai-engineers` | read | The product's source of truth: the proposal, the exercise engine, the committed values, and issue #239. |
| `konradcinkusz/authservice` | read | The estate's identity service, consumed as a published image. `MASTER-PROMPT.md` says why the source is attached anyway: so the integration surface is read rather than guessed. |

## The prompt

Copy this into the new session as its first message, with the four
repositories attached.

```
I maintain one reference architecture across my repositories (.NET Aspire +
Fly.io, container per service, one ServiceDefaults kernel per system,
database per service, JWT/JWKS auth, tag-driven CI/CD to GHCR). It is fully
documented and must NOT be re-derived from scratch. Read these first, in the
attached architecture-standards repository:

  docs/architecture/00-REFERENCE-ARCHITECTURE.md
    - the fifteen principles P1-P15 and the compliance checklist (section 3)
      that every gap and every deviation below is measured against.
  docs/scaffold/INIT-GENERIC-TEMPLATE.md
    - the procedure for an empty repository. Phase 0 below IS this
      procedure; it is installed as /init-generic-template and is not
      restated here.
  docs/delivery/WORKFLOW.md
    - the per-ticket procedure. Every phase after 0 is run as a ticket:
      /ticket-analysis -> /generate-master-prompt -> /implementation-phase
      -> /pr-review.
  docs/guides/
    - load the guide for every domain you touch, by name, before you write
      that layer: REPO-BASELINE, FRONTEND-BFF, SERVICE-API-PATTERNS,
      IDENTITY-AND-ACCOUNTS, FLY-IO-DEPLOYMENT, TESTING-STRATEGY,
      E2E-ACCEPTANCE-TESTING, METRIC-ETHICS, SECURITY-REVIEW,
      STATE-SNAPSHOT-PERSISTENCE, OPEN-SOURCE-RELEASE and
      PRIVATE-CLOUD-DELIVERY. AI-EVALS is named once below, as the reason
      a feature is a non-goal.

Identity across the estate is konradcinkusz/authservice (attached
read-only): product services validate the RS256 tokens it issues against
its JWKS and never keep a user store or mint a token (P5).

The product's own source of truth is the attached book repository,
konradcinkusz/math-for-ai-engineers, read-only in this session:

  notes/10-learning-app.md
    - the proposal this session implements: the book reviewed as a medium
      (section 1), the exercise engine (2), what the application is (3),
      the content compiler and the measurement behind it (4), the
      architecture measured against the constitution (5), the five
      decisions that are ADRs (6), the phased plan and the lab map (7),
      the risks (8).
  notes/11-ab-ovo-session-prompt.md
    - this prompt, and what it must not be read as.
  lab/README.md, lab/check.py, lab/tests/labkit.py, lab/tests/test_p01.py,
  lab/exercises/p01_floating_point.py, lab/solutions/p01_floating_point.py,
  figures/values/p01.tex
    - the exercise engine as it exists: the reader's stubs, the reference
      solution, the checks, the stdlib runner, and the committed values
      every check compares against. The three rules the engine carries
      are in CLAUDE.md, section "And a fourth artefact, the lab".
  GitHub issue #239 on that repository
    - the tracking issue for everything interactive: what the book side
      owes (the content bundle, section 1; the labs, section 5), what
      this repository owes (sections 2-4), the multi-track requirement
      (6) and the decisions (7).

-- Target for this session -----------------------------------------------
Repo:      konradcinkusz/ab-ovo. Empty, and the only repository this
           session writes to.
Slug:      ab-ovo. Latin "ab ovo", from the very beginning: it names the
           method rather than the subject, so it holds for every later
           track. Derived per INIT section 1 and echoed as a table before
           the first file is written: namespace AbOvo; projects
           AbOvo.AppHost, AbOvo.ServiceDefaults, AbOvo.Contracts,
           AbOvo.Api and AbOvo.Api.Tests; workspace web/ with npm scope
           @ab-ovo; Fly apps ab-ovo-postgres, ab-ovo-authservice-<env>,
           ab-ovo-api-<env> and ab-ovo-web-<env>; database apidb; images
           ghcr.io/konradcinkusz/ab-ovo-api and ab-ovo-web; config prefix
           AbOvo__.
Context:   Greenfield. A learning platform that encapsulates the book
           "Mathematics from Zero for the AI Engineer" - forty-seven
           programs in K. A. Stroud's programmed-learning format, English
           and Polish from one source - and its computer exercises. The
           reader works a frame, commits an answer, reveals the next
           frame, and in the lab pane implements a function whose every
           expected value is one the book prints. The book is the first
           track; a Python track will follow, in its own content
           repository. Why now: the book is drafted end to end, the
           exercise engine exists and is gated in the book's own CI, and
           every decision below is already recorded.
Frontend:  Next.js, the estate default (FRONTEND-BFF).
Azure:     no.
--------------------------------------------------------------------------

Decisions already taken. INIT section 1 asks three questions; answer them
with these, record each as an ADR, and never re-open them silently:

  region     waw. The author and the first edition's readers are there
             (notes/10 section 6.3).
  registry   GHCR, with the pull-credential note INIT section 1 asks for
             (the constitution's section 2 disagreement table; notes/10
             section 6.3).
  users      yes: authservice adopted as an external service. AND the
             reader loop - read, answer, reveal, check - must work with no
             account at all; an account adds synchronisation across
             devices and nothing else (notes/10 section 6.2; P8 applied to
             auth).

Deviations and non-goals, recorded as ADRs before the first line of
product code (INIT section 12: a different choice is a recorded decision,
never a silent substitution):

  ADR  The exercise checks are Python and run in the reader's browser
       under Pyodide. No Python runs on any server of this system, and no
       Python source is authored in this repository: exercises, checks and
       values arrive from the book at a pinned revision, first as a fetched
       fixture (phase 1) and then inside the content bundle (phase 2).
       notes/10 section 6.1 carries the reasons and the exit condition.
  ADR  Content is a versioned bundle published by each track's own
       repository. This repository owns the content schema and its
       validator and never parses LaTeX (P11; notes/10 section 4; issue
       #239 section 6). The book's compiler targets the schema; the schema
       does not know that its first track is a book of frames.
  ADR  The instrument measures the book, never the reader. Anti-goals at
       the top of the README, enforced by an absent table: outcomes are
       recorded against a frame, an attempt and a check run, with no reader
       identity in the aggregate store (METRIC-ETHICS sections 1 and 5;
       notes/10 section 6.4). Every rate carries its interval (section 3);
       heuristics about people are not computed (section 4); the
       instrument is opt-in and versioned (IDENTITY-AND-ACCOUNTS section
       9).
  ADR  Non-goal: no language model in the loop. A failed check names the
       frames, and the frames are the explanation; the day one is added,
       AI-EVALS applies in full (notes/10 section 6.5).
  ADR  Dependency automation declared and off: INIT section 4's own
       deviation from REPO-BASELINE section 1, with its trigger for turning
       it on.

The job, in phases. Do not start a phase until the previous one is
verified: builds and tests green, and the phase's own definition of done
met. Phase 0 is the installed procedure; every later phase is a ticket
through WORKFLOW.md, one pull request each.

0. INIT. Run /init-generic-template ab-ovo, exactly as
   INIT-GENERIC-TEMPLATE.md says. Echo the derived-names table; confirm
   the repository is empty (section 2); take the three answers above and
   write the ADRs of section 9 plus the five above; run every gate in
   section 10 and report the table, including P8's zero-credential run
   and the container health check, and report any gate you could not run
   as not run. Definition of done is section 11's: the public URL, or the
   explicit statement that nothing was deployed and the repository stands
   at "builds, tests green, images build".
   The template ships one thin vertical slice and no domain model
   (section 12). Do not invent one here: the application's domain arrives
   in phases 1-3, and the first ticket deletes anything guessed.

1. THE LAB PANE. Lab P1's seven exercises, checked in the browser.
   Inputs, fetched by a script in this repository from the book at a
   pinned commit (0698dca, the merge commit of the book's PR #238, or a
   later one you name) and written under content/, never under src/ and
   never hand-edited: lab/check.py, lab/tests/labkit.py,
   lab/tests/test_p01.py, lab/exercises/p01_floating_point.py,
   lab/solutions/p01_floating_point.py and figures/values/p01.tex.
   Preserve the relative layout: labkit.py takes the directory two levels
   above lab/tests/ as the root and reads figures/values/<program>.tex and
   lab/<exercises|solutions>/<stem>.py from it, and check.py locates
   lab/tests/ relative to its own path, so the virtual file system Pyodide
   mounts must reproduce lab/check.py, lab/tests/, lab/exercises/ and
   figures/values/ under one root.
   The runner is lab/check.py's run(lab, keyword): it imports the test
   module, calls every test_* function, prints one line per check - ok,
   todo, FAIL - and a final "SUMMARY ok=.. fail=.. todo=.." line. Call
   run(), not main(): main() reads argv and exits the interpreter. Before
   each run the editor pane writes the reader's text to
   lab/exercises/<stem>.py in the virtual file system; the pane shows the
   runner's lines verbatim; a FAIL line names frames to re-read and never
   a solution (the lab's three rules).
   Pyodide and the fixture are served from the application's own origin;
   nothing is fetched from a CDN at run time (FRONTEND-BFF section 1).
   Pyodide loads the stdlib alone for Lab P1; numpy is loaded only by a
   lab that names it (notes/10 section 7).
   Definition of done: the Playwright journey of notes/10 section 6.1 -
   open Lab P1, paste the reference solution of one exercise from the
   fetched fixture, press Check, assert the ok line for that check and the
   SUMMARY line - wired in ci.yml in the same commit (E2E-ACCEPTANCE-TESTING
   section 6), and the same journey against ab-ovo-web-dev.fly.dev once
   phase 0 has deployed.

2. THE CONTENT SCHEMA AND THE FRAME VIEW, as two tickets, because the
   second is blocked on work outside this repository.
   2a. The schema: content-schema v1 as JSON Schema in this repository, a
   validator the CI runs, and a synthetic fixture - a three-frame track
   written for the tests and labelled as synthetic, never a transcription
   of the book. A track is a manifest (id, title per language, languages,
   units in order, labs and the runtime each lab needs: stdlib, numpy,
   none) plus units. The Stroud frame - question, answer, next-frame cue,
   boxes, maths for KaTeX, figures as .mmd source, transcripts as text,
   quiz items with routes, outcomes and summary items with frame ranges -
   is ONE unit type, and the minimum unit is title, body and an optional
   check, so a track without frames renders without faking them (issue
   #239 section 6). Progress and the instrument key on (track, tag, unit,
   frame) from this schema, so a second track is data and not a migration.
   Publish the schema's path and version in the README: the book's
   compiler (issue #239 section 1) builds against it.
   2b. The frame view for Program P1 in both languages, from a real
   bundle: content-<tag>.tar attached to a v* release of the book. The
   next frame stays hidden until the reader commits an answer; the cue and
   the covered answer box are the page's own mechanics, rendered rather
   than reinvented; every Quiz route and Summary bracket is a link into
   the frames; figures render from .mmd; transcripts are shown. STOP
   CONDITION: if no bundle exists on the book's releases, this ticket is
   blocked. Say so, and do not parse programs/*.tex in this repository
   (P11). The application pins one (track, tag) pair, and a reader's
   progress records the tag it was made against.
   Definition of done for 2b: every frame of P1 in both editions renders,
   and a check compares the bundle's frame count per program with the
   count the book's tools/check_structure.py reports.

3. PROGRESS AND ACCOUNTS. Local progress in the browser keyed by (track,
   tag, unit, frame), with export to a file and import; a manual test in
   the release checklist for that path (TESTING-STRATEGY section 7,
   client-side-only data); then authservice adopted as MASTER-PROMPT.md
   phase 2 describes, and synchronisation through AbOvo.Api owning apidb -
   DATABASE_PROVIDER with the InMemory fallback, schema by MigrateAsync in
   a hosted service (P4), the ORM-managed schema rather than the snapshot
   pattern (STATE-SNAPSHOT-PERSISTENCE section 6). An account adds
   synchronisation and nothing else; deletion on request
   (IDENTITY-AND-ACCOUNTS section 8).

4. THE INSTRUMENT. The aggregate store beside progress in apidb, keyed by
   (track, tag, unit, frame / exercise / quiz item), with reader identity
   absent by schema; the four measures and their counter-measures from
   notes/10 section 6.4; every rate with its interval, computed the way
   the book's Program P27 computes a proportion's standard error; consent
   opt-in and versioned; analysers as interface plus registration (P10).
   Definition of done: the first sentence the book can print about itself
   - "here is what N readers who agreed to be counted did with frame 8 of
   Program P1" - produced from real data, with its interval.

5. THE OPEN-SOURCE EDITION. MIT (OPEN-SOURCE-RELEASE section 3), images
   public on GHCR (section 5: a package is private by default on first
   push), and a compose file that runs web, API and Postgres without Fly
   (PRIVATE-CLOUD-DELIVERY section 9). Fly stays the deployment; compose
   is the distribution.

Ground rules:
- Work ONLY in ab-ovo. architecture-standards, authservice and the book
  are read-only references in this session: never modified, forked or
  vendored. Anything the book must produce - the bundle, the compiler,
  more labs - is a comment on the book's issue #239, never a change here
  and never a copy of the book's LaTeX here.
- Read the standards; do not re-derive them. Every rule-shaped line you
  write - in an ADR, a README, a review - cites the principle or the guide
  section behind it.
- Every phase lands as an independently shippable, verified change: a
  branch, a pull request, tests green, one PR per phase unless I say
  otherwise. A gate you could not run is reported as not run, never
  implied to have passed.
- Deviations you keep are decisions with reasons, in docs/adr/ and the
  deviation register. Gaps you cannot close are recorded - architecture
  gaps in docs/architecture/, UI/UX gaps in docs/ux/UI-UX.md - and never
  left silent.
- The book's own rule applies to every number this system reports and to
  every instrument that measures it: a measurement is not evidence until
  the instrument has been watched producing an answer you already knew.
  The lab's own gate is the model - the reference solutions pass every
  check and the untouched stubs pass none - and phase 1's Playwright
  journey is that gate seen from the browser.
- English for everything needed to build or deploy (the constitution,
  section 2). The content is bilingual; the repository is not.
- No secret in any file, prompt or pull request. Name the variable, never
  its value (P5).
```

## What a finished first session leaves behind

All of it in `ab-ovo`:

1. The scaffold `INIT` §3 describes, with its gates run and reported
   (§10) and its ADRs written (§9): region, registry, users, dependency
   automation, and the five decisions above.
2. A deployment on Fly.io reached from the first tag, or the explicit
   statement that nothing was deployed (§11).
3. Lab P1 checked in the browser under Pyodide, with the Playwright
   journey wired into CI in the same commit.
4. `docs/ux/UI-UX.md` carrying the ranked backlog the next session picks
   up: phases 2 to 5, each still a ticket through `WORKFLOW.md`.

Phases 2 to 5 are listed in the prompt so the session knows where phase 1
sits; a session that reaches phase 1's definition of done has done its job.

## What it deliberately does not ask for

- **The content compiler.** It lives in the book's repository, on
  `tools/parity.py`'s tokeniser, and is issue #239 §1 there; `ab-ovo`
  never sees LaTeX. The prompt's phase 2b has a stop condition for exactly
  the day somebody is tempted.
- **A second service, an event bus, a mobile application, a language
  model.** The constitution's §4 non-goals, `INIT` §12, and
  `notes/10-learning-app.md` §6.5 and §7.
- **A per-reader score, a ranking, a comparison between readers.** The
  instrument's anti-goals, `METRIC-ETHICS.md` §1, enforced by an absent
  table rather than by a policy.
