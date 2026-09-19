#!/usr/bin/env node
// Every maths span in a content bundle, through KaTeX. Issue #239 §1:
//
//   "Render test in the book's CI: every one of the ~13 900 maths spans
//    through katex on Node. How many render unchanged is the open
//    measurement of note §4; turn it into a number."
//
// This is that number. It is a MEASUREMENT of the compiler's own claim:
// content_compile.py expands 31 book macros and passes the rest through on
// the strength of a list called KATEX_OK, and a list is an assertion until
// something runs it. A span that KaTeX refuses is a page with a red error
// on it, so the failure has to happen here rather than in a reader's
// browser -- which is what "the compiler REFUSES rather than degrades"
// means once the maths has left the book.
//
//   node lab/tools/content_katex.js build/content/bundle.json
//
// strict:true is deliberate. KaTeX's default quietly accepts several things
// it renders differently from LaTeX, and a renderer that accepts what it
// cannot reproduce is the degradation this pipeline exists to refuse.
'use strict';
const fs = require('fs');
const katex = require('katex');

const path = process.argv[2];
if (!path) { console.error('usage: content_katex.js <bundle.json>'); process.exit(2); }
const bundle = JSON.parse(fs.readFileSync(path, 'utf8'));

const spans = [];
const TEXT_KEYS = new Set(['body', 'answer', 'titles', 'labels']);
(function walk(node, where) {
  if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${where}/${i}`));
  if (node && typeof node === 'object') {
    for (const [k, v] of Object.entries(node)) {
      if (TEXT_KEYS.has(k) && v && typeof v === 'object') {
        for (const [lang, s] of Object.entries(v)) {
          if (typeof s === 'string') collect(s, `${where}/${k}/${lang}`);
        }
      } else walk(v, `${where}/${k}`);
    }
  }
})(bundle, '');

function collect(text, where) {
  const re = /\$\$([\s\S]*?)\$\$|\$([^$]*)\$/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const display = m[1] !== undefined;
    spans.push({ tex: (display ? m[1] : m[2]).trim(), display, where });
  }
}

let ok = 0;
const failures = new Map();
for (const s of spans) {
  try {
    katex.renderToString(s.tex, { displayMode: s.display, strict: true,
                                  throwOnError: true, trust: false });
    ok++;
  } catch (e) {
    const msg = String(e.message).replace(/ at position \d+.*$/, '').slice(0, 110);
    if (!failures.has(msg)) failures.set(msg, []);
    failures.get(msg).push(s);
  }
}

const bad = spans.length - ok;
console.log(`${spans.length} maths spans, ${ok} render, ${bad} do not ` +
            `(katex ${require('katex/package.json').version}, strict)`);
if (bad) {
  const sorted = [...failures.entries()].sort((a, b) => b[1].length - a[1].length);
  for (const [msg, hits] of sorted) {
    console.log(`\n  ${hits.length}  ${msg}`);
    for (const h of hits.slice(0, 3)) {
      console.log(`       ${h.where}`);
      console.log(`       ${h.tex.slice(0, 120).replace(/\n/g, ' ')}`);
    }
  }
  process.exit(1);
}
