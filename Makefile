.PHONY: all a4 all-formats check check-a4 site stubs-check en pl en-a4 pl-a4 scripts terms parts \
        text-only watch-en watch-pl clean diagrams diagrams-clean \
        numbers verify stubs answers frames elicit outcomes values translate shots debt

# Two paper formats from one source. `standard` is the 17 x 24 cm trade format
# shared with the companion volumes; `a4` is A4 at 12pt, which is what the book
# is actually read in -- on a screen, or off an office printer. The format is
# chosen by the main file, and the four main files differ in five lines.
LANGS   := en pl
FORMATS := standard a4

MMD_SRC := $(wildcard figures/mermaid/en/*.mmd) $(wildcard figures/mermaid/pl/*.mmd)
MMD_PDF := $(patsubst figures/mermaid/%.mmd,figures/diagrams/%.pdf,$(MMD_SRC))
VAL_SRC := $(wildcard code/*.py)

# Everything a script under code/ writes and git tracks. The book's central
# promise -- that the page cannot disagree with the script that computed it --
# is exactly as wide as this variable and no wider, so anything a script emits
# belongs in it. It was figures/values alone for two programs, and the day a
# transcript was added the promise quietly stopped covering the whole book.
COMPUTED := figures/values figures/transcripts

# mermaid-cli drives a headless Chromium. The config below is written on first
# use and points at whatever browser is available; override BROWSER on the
# command line if yours lives somewhere else.
BROWSER ?= $(shell command -v chromium 2>/dev/null || command -v chromium-browser 2>/dev/null || command -v google-chrome 2>/dev/null || echo /opt/pw-browsers/chromium)

all: numbers diagrams en pl check

# Both editions on A4. Use `make all-formats` for all four PDFs.
a4: numbers diagrams en-a4 pl-a4 check-a4

all-formats: numbers diagrams en pl en-a4 pl-a4 check check-a4

# The three gates. A build that only *looked* like it succeeded is the failure
# mode this book cannot afford: -interaction=nonstopmode writes a PDF over the
# top of an error, and with -file-line-error the error line does not begin with
# a `!`, so the inherited `grep '^!' main.log` habit cannot see it.
check:
	@python3 tools/gen_stubs.py --check
	@python3 tools/check_structure.py --scripts
	@python3 tools/check_structure.py --terms
	@python3 tools/check_structure.py --parts
	@python3 tools/checklog.py main-en.log main-pl.log
	@python3 tools/checkpdf.py main-en.pdf main-pl.pdf
	@python3 tools/parity.py | tail -n 3
	@python3 tools/reflist.py 2>/dev/null || true

# The A4 build is the same source, so parity and the stub manifest are already
# covered by `check`. What is NOT covered is the log: a format change can push
# a table past a page boundary and produce an overfull vbox in one format only,
# which is exactly the class of defect the trade format's own log cannot see.
check-a4:
	@python3 tools/checklog.py main-en-a4.log main-pl-a4.log
	@python3 tools/checkpdf.py main-en-a4.pdf main-pl-a4.pdf

en: numbers
	latexmk -pdf -interaction=nonstopmode -file-line-error main-en.tex
	@python3 tools/checklog.py main-en.log

pl: numbers
	latexmk -pdf -interaction=nonstopmode -file-line-error main-pl.tex
	@python3 tools/checklog.py main-pl.log

en-a4: numbers
	latexmk -pdf -interaction=nonstopmode -file-line-error main-en-a4.tex
	@python3 tools/checklog.py main-en-a4.log

pl-a4: numbers
	latexmk -pdf -interaction=nonstopmode -file-line-error main-pl-a4.tex
	@python3 tools/checklog.py main-pl-a4.log

# Skip diagram rendering and value regeneration -- useful when iterating on
# prose. Unrendered diagrams print their Mermaid source, so the build is still
# readable, and a stale value still prints; it is the CI job that catches drift.
text-only:
	latexmk -pdf -interaction=nonstopmode main-en.tex
	latexmk -pdf -interaction=nonstopmode main-pl.tex

# Assemble locally exactly what CI publishes to Pages, so a link or a layout
# change can be checked before it is deployed rather than after.
site: en pl en-a4 pl-a4
	@rm -rf _site && mkdir -p _site
	@cp -r docs/. _site/
	@cp main-en.pdf "_site/Mathematics-from-Zero-for-the-AI-Engineer.pdf"
	@cp main-pl.pdf "_site/Matematyka-od-zera-dla-inzyniera-AI.pdf"
	@cp main-en.pdf _site/book-en.pdf
	@cp main-pl.pdf _site/book-pl.pdf
	@cp main-en-a4.pdf _site/book-en-a4.pdf
	@cp main-pl-a4.pdf _site/book-pl-a4.pdf
	@echo "  _site/ assembled. Open _site/index.html."

watch-en:
	latexmk -pvc -pdf -interaction=nonstopmode main-en.tex
watch-pl:
	latexmk -pvc -pdf -interaction=nonstopmode main-pl.tex

clean:
	for j in main-en main-pl main-en-a4 main-pl-a4; do latexmk -C $$j.tex; done
	rm -rf _site
	rm -f *.dgm *.ilg *.ind *.idx programs/*/*.aux appendices/*/*.aux

# ---------------------------------------------------------------------------
# Numbers. Every numeric value in the book is produced here and pulled into the
# text with \val{}. The book does not contain the digits, it contains a
# reference to them, so the book and the scripts cannot disagree.
# ---------------------------------------------------------------------------
numbers:
	@mkdir -p $(COMPUTED)
	@for f in $(VAL_SRC); do \
	  echo "  values: $$f"; \
	  python3 "$$f" || exit 1; \
	done
	@# One file the preamble can \input, because TeX cannot glob a directory.
	@{ echo '% Generated by `make numbers` --- do not edit.'; \
	   for v in figures/values/*.tex; do \
	     case "$$v" in */all.tex) continue;; esac; \
	     echo "\\input{$${v%.tex}}"; \
	   done; } > figures/values/all.tex
	@echo "  index:  figures/values/all.tex"

# Re-runs the scripts and fails if any committed value would change. This is
# the check that makes the previous rule mean something.
# TWO failures, not one, and `git diff` alone can only see the first.
#
#   drift     -- a tracked file no longer matches its script
#   untracked -- a file git has never seen, so it was never compared to
#                anything. Every program's FIRST values file is in this state,
#                which means every program's first values file used to pass
#                this gate by being invisible to it. Found when F02 added 32
#                values and the gate went green on all of them.
#
# TWO DIRECTORIES, not one. figures/transcripts holds console transcripts
# written by the same scripts and pulled into the page with \transcript{}, and
# for its first program it sat outside this gate entirely: the drift check, all
# three workflows and the values artefact were scoped to figures/values alone.
# A transcript is a printed number that happens to be inside a verbatim block,
# so it is exactly the thing the book promises cannot disagree with its script
# -- change LOSS_NATS in code/f03_logarithms.py and the transcript on the page
# was free to contradict every \val{} around it with nothing failing. It is
# the sibling volume's fabricated-console-block defect with a build step in
# front of it, which is worse, because the file now LOOKS generated.
#
# Staged-but-not-committed is NOT a failure: the content matches the script,
# which is the whole question this gate asks. Testing `git status --porcelain`
# instead would fail on a staged file and make the gate unusable mid-commit.
verify: numbers
	@drift=$$(git diff --name-only -- $(COMPUTED)); \
	 new=$$(git ls-files --others --exclude-standard -- $(COMPUTED)); \
	 if [ -n "$$drift" ] || [ -n "$$new" ]; then \
	   [ -n "$$drift" ] && { echo "STALE: these no longer match their script:"; \
	                         echo "$$drift"; git diff --stat -- $(COMPUTED); }; \
	   [ -n "$$new" ] && { echo "UNTRACKED: git has never seen these, so they have"; \
	                       echo "never been compared to anything. git add them:"; \
	                       echo "$$new"; }; \
	   exit 1; \
	 else echo "All computed output is current: values and transcripts."; fi

# ---------------------------------------------------------------------------
# Diagrams. Source of truth is figures/mermaid/<lang>/*.mmd, committed. The
# rendered PDFs are build output and are gitignored, so a diagram change shows
# up in review as a readable text diff.
# ---------------------------------------------------------------------------
diagrams: $(MMD_PDF)

figures/diagrams/%.pdf: figures/mermaid/%.mmd figures/mermaid/.puppeteer.json figures/mermaid/config.json
	@mkdir -p $(dir $@)
	npx -y @mermaid-js/mermaid-cli@11 \
	  -i $< -o $@ \
	  -p figures/mermaid/.puppeteer.json \
	  -c figures/mermaid/config.json \
	  -b transparent --pdfFit

figures/mermaid/.puppeteer.json:
	@mkdir -p figures/mermaid
	@printf '{"executablePath":"%s","args":["--no-sandbox","--disable-dev-shm-usage"]}\n' "$(BROWSER)" > $@
	@echo "Wrote $@ pointing at $(BROWSER)"

diagrams-clean:
	rm -rf figures/diagrams

# ---------------------------------------------------------------------------
# Debt ledgers. Each is a promise made to a reader that has not yet been kept,
# so it is counted rather than remembered. Four of these are new to this book;
# the other three are inherited from the companion volumes.
# ---------------------------------------------------------------------------

# 0. The manifest and the tree agree. tools/programs.json is the single source
#    of the part and program sequence; this fails when a stub or structure.tex
#    is stale against it.
stubs-check:
	@python3 tools/gen_stubs.py --check

# 1. Programs not yet written.
stubs:
	@for L in $(LANGS); do \
	  n=$$(grep -rl '\\programstub{' programs/$$L 2>/dev/null | wc -l); \
	  echo "  $$L: $$n of $$(ls programs/$$L/*.tex 2>/dev/null | wc -l) programs are stubs"; \
	done

# 2. Exercises with no answer. A mathematics book's most common defect, and
#    mechanically detectable.
answers:
	@python3 tools/check_structure.py --answers

# 3. Frame counts against the 30--70 band, frames that ask a question nobody
#    answers, and every frame NUMBER the program quotes -- Quiz routes,
#    outcome ranges, Summary brackets -- checked against the frames that
#    exist. Those payloads used to be compared between the editions and never
#    against the program, so a route to frames 91--93 in a 48-frame program
#    passed every gate here.
frames:
	@python3 tools/check_structure.py --frames

# 3b. What fraction of each program's frames actually asks the reader
#     something. REPORTED, NEVER FATAL, like the orphan-tail ledger, and for
#     the same reason -- there is no defensible threshold and a permanently red
#     gate teaches people to stop reading the output. It exists because the
#     number decayed from 78% to 26% over seventeen programs with every other
#     gate green throughout: RE_DEMANDS treats \nextframe, \blank and
#     \yourturn alike, so a program that elicits rarely is invisible to
#     check_frames, to parity's C16, and to C4 and C14.
elicit:
	@python3 tools/check_structure.py --elicit

# 4. Programs that declare no learning outcomes. The "Can you?" checklist is
#    GENERATED from the outcomes, so it can no longer drift from them -- which
#    means the only failure left is a program that declared none at all.
outcomes:
	@python3 tools/check_structure.py --outcomes

# 5. \val{} references with no value behind them, and values nothing uses.
values:
	@python3 tools/check_structure.py --values

# 5b. \transcript{} references naming a file that is not there. Not a ledger
#     of outstanding work -- a hard gate, because it is always a typo on a tree
#     where `make numbers` has run, and because the macro's own fallback prints
#     a grey marker and BUILDS. That fallback is what let ten of the book's
#     twelve transcripts go nine programs without reaching a page with every
#     other gate green. See the note above check_scripts().
scripts:
	@python3 tools/check_structure.py --scripts

# 5b. Appendix D is a claim about the body on every line, and a glossary row
#     naming a word the book does not use is the failure that matters. It is
#     not hypothetical: the suggested table in notes/03 carries rows for
#     `dropout` and `ground truth`, and neither appears anywhere in either
#     edition. Reads the PROSE of programs/pl, because a substring count over
#     raw LaTeX counts a \label and a \val key as usage -- which is how an
#     audit of this appendix twice licensed a row for a word the prose never
#     writes. See the note above check_terms().
terms:
	@python3 tools/check_structure.py --terms

# 5b. The introduction's own map of the book, against the manifest.
#     This is the one class the parity checks are structurally blind to:
#     C4, C8, C12 and C14 all compare the two EDITIONS, so a part range
#     that is stale in both stays green. Seven of the nine ranges were
#     wrong in both introductions for the whole of the book -- the P7
#     insertion, never swept out of the prose -- on page one, with every
#     gate passing. Compare against tools/programs.json, never between
#     the editions.
parts:
	@python3 tools/check_structure.py --parts

# 6. The two editions out of step. tools/parity.py is the single parity tool;
#    it compares an ORDERED structural signature rather than counts, because a
#    histogram cannot see \yourturn moving from frame 2 to frame 3, and every
#    Summary back-reference and Quiz route navigates by frame number.
translate:
	@python3 tools/parity.py | tail -n 3
	@python3 tools/reflist.py 2>/dev/null || \
	  echo "  (cross-reference comparison needs a completed build of both editions)"

# 7. Numeric claims not produced by a script, and diagrams not drawn.
shots:
	@printf "  verifybox blocks: "
	@grep -rc 'begin{verifybox}' programs appendices 2>/dev/null \
	  | awk -F: '{s+=$$2} END {print s+0}'
	@printf "  mermaid sources:  "
	@ls figures/mermaid/*/*.mmd 2>/dev/null | wc -l

debt:
	@echo "== Manifest and tree =="              ; $(MAKE) -s stubs-check || true
	@echo; echo "== Programs not yet written ==" ; $(MAKE) -s stubs
	@echo; echo "== Exercises with no answer =="  ; $(MAKE) -s answers
	@echo; echo "== Frames =="                    ; $(MAKE) -s frames
	@echo; echo "== Learning outcomes =="         ; $(MAKE) -s outcomes
	@echo; echo "== Elicitation rate =="          ; $(MAKE) -s elicit
	@echo; echo "== Computed values =="           ; $(MAKE) -s values
	@echo; echo "== Transcripts on the page =="   ; $(MAKE) -s scripts
	@echo; echo "== Appendix D terminology =="   ; $(MAKE) -s terms
	@echo; echo "== The introduction's map =="    ; $(MAKE) -s parts
	@echo; echo "== Polish/English parity =="     ; $(MAKE) -s translate
	@echo; echo "== Unverified claims, diagrams ="; $(MAKE) -s shots
	@echo
	@echo "== Reader validation =="
	@echo "  80/80: NOT ESTABLISHED. The method is validated; this book is not."
	@echo "  It may not claim 80/80 until it has been trialled on readers."
	@echo
	@echo "  The instrument is the scored Test exercises, NOT the Quiz. The Quiz"
	@echo "  runs on the thirteen Foundation programs only, so a standard defined"
	@echo "  against it would be unmeasurable on thirty-four of the forty-seven --"
	@echo "  and contaminated on the other thirteen, because the same items are"
	@echo "  used on entry and on exit. Every program has Test exercises."
