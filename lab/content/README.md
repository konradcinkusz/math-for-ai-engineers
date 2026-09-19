# The content schema, vendored

`content-schema.v1.json` is **a copy**. The source is
[`konradcinkusz/ab-ove`](https://github.com/konradcinkusz/ab-ove), at
`web/app/src/lib/content/content-schema.v1.json`, and that repository owns it
(issue #239 §6: *target that schema, do not invent a second one*).

**Why a copy exists at all, given that this estate's standing objection to one
is that it is a second copy of something that has a source.** Issue #239 §1
requires the compiler to *refuse rather than degrade*, and a refusal has to
happen **before** a bundle is attached to a release — at the producer, offline,
in a CI job that does not reach across a repository boundary. A contract the
producer cannot check is a contract the producer discovers by having a release
rejected, which is ab-ove's ADR-0014's own reasoning for the schema being JSON
Schema rather than a TypeScript type.

**So the copy is deliberately not authoritative.** ab-ove validates every bundle
on the way in, with `validate.ts`, reading the same document. That end is the
authority and this end is an early warning. If the two ever disagree, the far
end is right and this file is stale — refresh it, and read the diff, because a
schema change is a change to what a bundle may contain.

`lab/tools/content_compile.py` validates against this file and additionally
reproduces the structural rules JSON Schema cannot state — the cue invariant in
both directions, contiguous step numbering, every route endpoint and section
anchor naming a step that exists, strictly ascending sections, every declared
language present in every text, every check naming a lab and an exercise the
bundle carries. ADR-0014 says those are *"the compiler's to reproduce or ours to
report"*; this is the compiler reproducing them.
