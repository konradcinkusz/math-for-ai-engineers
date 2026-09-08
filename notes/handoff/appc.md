# Hand-off — Appendix C (issue #49)

## What the issue asked for, and what was already on the page

**Issue #49 was substantively delivered before this pass ran**, by the work
CLAUDE.md records under *Appendix C pass, September 2026*. Checked item by
item against the tree rather than against that note:

| Done when | State |
|---|---|
| A tagging mechanism in `preamble.tex`, F1 tagged as the worked example | present — `\result{}` / `\resultsbody`, and F01 carries 14 marks in each edition |
| `appendices/en/appC-formulae.tex` written, stub deleted | done, `\programstub{}` count 0 |
| `appendices/pl/…` written, entry-for-entry identical | done — 722 marks each edition, and the per-program counts match in all 47 |
| Every entry resolves to a real program and frame, no hard-coded numbers | true, and **now checked** — see below |
| Grouped so it can be scanned | grouped, by program; the part level was considered and not taken — see below |
| Notation matches Appendix B exactly | true of the contract's *banned spellings*; **four marked spans bypass a contract macro** — see below |
| No bare `\log` | C10, green |
| Gates green | green, see the PR body |

So the pass's job was verification, and what it delivered is the half the
issue asked for that had not been built: **the checking**. The issue's own
wording is that the 1:1 property should be *structural rather than policed*,
and *checked by CI*. The mechanism was structural; nothing checked it.

## The finding: the coordinate could be wrong, and nothing would have said so

Appendix C's whole design is that no line in it is transcribed, so the
program key and frame range it prints cannot be wrong. **The range does not
come from the mark.** It comes from `\sumitem`, which stashes it in
`\mfa@sumfr` for a `\result` inside its body to pick up. A `\result` written
anywhere else silently inherits whichever Summary item was read last — or, in
a program whose Summary has not been reached, the `\providecommand` fallback,
and prints `[?]`.

**Measured rather than assumed.** A probe `\result` placed outside every
Summary item, in *both* editions, left `parity.py`, `--frames`, `--answers`,
`--outcomes`, `--values`, `--scripts` and `gen_stubs --check` all green. It
has to be both editions to be interesting: C14 counts macros generically, so a
mark added to one edition alone already fails — and a fault identical in both
is the recorded shape, *a check that is wrong in the same way in both editions
stays green and only the ledger lies*.

`check_structure.py --results` closes it, and is a hard gate in `make check`
and in CI beside `--scripts`, `--terms` and `--parts`. It also catches two
faults that ride along on the same parse and are invisible everywhere else: a
mark nested inside another mark (Appendix C prints its text twice), and an
empty mark (a bullet and a coordinate with no formula between them).

**Every branch was watched producing a known answer before any of it was
believed**, which is the house rule after the run of misread instruments in
the P32–P34 passes:

| probe | reported |
|---|---|
| `\result` outside every `\sumitem`, both editions | names file and line, exit 1 |
| `\result` nested inside another | *would print its text twice*, exit 1 |
| `\result{}` empty | *a bullet and a coordinate with no formula*, exit 1 |
| clean tree | 722 marked in each edition, exit 0 |

The brace matcher was separately checked against `\{` and `\}` inside a mark,
and the comment blanking against offset drift, because the check reports line
numbers and a shifted offset names the wrong line.

## A claim I had to correct in a neighbour — and did NOT fix

**`programs/{en,pl}/P07-tensors-shapes.tex` hard-codes `\operatorname{Var}`
(10 sites) and `\operatorname{Cov}` (12 sites) where the book uses the
contract macros `\Var` and `\Cov` 158 and 44 times.** Two of those spans are
`\result{}`-marked (en:801, pl:804) and therefore replay verbatim into
Appendix C — the one place in the book where the notation contract has to hold
exactly, because the reader arrives there with none of the section around it.

`\Var` and `\Cov` are declared in `lang/en.tex:128–129` and
`lang/pl.tex:130–131`, so the *source* is meant to be identical and only the
output may differ. Today both language files set them to `Var` and `Cov`, so
the bypass is byte-identical output and that is exactly why it shipped: no
glyph differs, no gate fires. It is a **latent** one-edition divergence — the
day anyone acts on P24's `D²(X)` / `M(X)` notation box, the 202 macro sites
move together and P07's 22 do not.

C10 forbids exactly one of these spellings, `\operatorname{lcm}`. The contract
owns ten operators.

**Not fixed here, deliberately**: P07 is another program's file and the
parallel arrangement puts it out of bounds for this session. The fix is a
mechanical substitution that changes no glyph today, so it costs nothing and
can be taken by whoever owns P07 or by the sync session.

Instead, `--results` reports it — non-fatal, on the treatment this book gives
every ledger nobody can responsibly clear in the pass that finds it. **The
list of raw spellings is read out of `lang/en.tex`** rather than typed, so an
operator added to the contract is covered the day it is added; it currently
derives 30 spellings over all ten macros, and it was proved live by planting
an `\operatorname{gcd}` it had never seen fire on.

## Grouping: considered, and not taken

The checklist asks for grouping *by part, or by subject, but not by order of
appearance*. The appendix is grouped — 47 subsections, each naming a program
and its title, which is a subject — but the sequence of those groups is the
book's own, and there is no part level above them. `\lblResultsIntro` says
"in program order" in as many words.

Part headings would satisfy the item literally and are cheap in principle:
patch `\part` to record a pending part title and have `\program` consume it
into `mfa@part@<key>`, then let `\mfa@resultprogram` emit a heading when that
key is non-empty. Derived from `structure.tex`, so it could not go stale.

**Not taken, for one reason that is not about taste**: it is a change to
`preamble.tex`, which every parallel session compiles, and this session is
forbidden to build — so it would ship a macro change to shared machinery that
nobody has watched compile. The recorded trap it would be most exposed to is
the `\makeatletter` one this preamble already carries three instances of, and
whose tell is that the error names neither the macro nor the block. A
verified improvement is worth more than an unverified one; the mechanism is
written down here so the next person meets it with the reasoning rather than
rediscovering it.

## Values, figures, frames

None. This pass emitted no value, retired none, added no frame, wrote no
figure and moved no prose in either edition — the book's text is untouched.
`--elicit` is unmoved at 1028/1864 (55%) for the same reason.

## For the sync session

- `figures/values/appf.tex` is **not** touched here, and `code/appf_ledgers.py`
  was not run. No ledger count moved: 722 marks is the tree as it stands, and
  CLAUDE.md's header says 721 — that figure was already one behind before this
  pass, and is the sync session's to reconcile.
- CLAUDE.md is untouched. A pass note for this belongs under *Resolved
  questions*, and the entry above *Appendix C pass* should gain the sentence
  that its coordinate claim is now enforced rather than merely true.
- The four P07 sites above are the one outstanding item, and they are one
  substitution.
