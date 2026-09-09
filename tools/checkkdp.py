#!/usr/bin/env python3
r"""Is this PDF acceptable to Amazon KDP as a paperback interior?

One implementation, called by `make check-kdp` and by the KDP workflow, exactly
as tools/checklog.py is shared -- because a gate that exists twice is a gate
that disagrees with itself.

WHAT IT CHECKS, and why each is here rather than assumed:

  trim        every page exactly 6 x 9 in. A single stray page size is rejected
              at upload, and it is invisible in a viewer.
  pages       24 <= n <= 828 (black ink, white paper, regular trim), and EVEN:
              KDP accepts an odd count and then prints the last leaf as a stray
              recto.
  colour      no page carrying a non-gray mark. Amazon prices a colour interior
              several times higher, and one tinted box decides it. The test
              RECURSES INTO FORM XOBJECTS: every diagram in this book is one,
              and a scanner that reads only the page stream reported a
              1524-page colour interior as clean.
  fonts       every font embedded.
  margins     inner >= the bracket minimum for that page count, outer, top and
              bottom >= 0.25 in.
  bleed       no crop marks, registration marks or colour bars: the interior is
              no-bleed, so MediaBox must BE the trim.

Needs poppler (pdftotext, pdffonts) and pikepdf.

Run:  python3 tools/checkkdp.py kdp-v3-en.pdf
      python3 tools/checkkdp.py --json build/kdp kdp-v*.pdf
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PT_PER_MM = 72.0 / 25.4
PT_PER_IN = 72.0
TRIM_W_PT = 152.4 * PT_PER_MM          # 432.0
TRIM_H_PT = 228.6 * PT_PER_MM          # 648.0
TRIM_TOL_PT = 0.1 * PT_PER_MM          # SS8: within 0.1 mm

MIN_SIDE_MARGIN_IN = 0.25              # KDP no-bleed floor, all four sides

RE_WORD = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">'
    r'(.*?)</word>', re.S)
RE_PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)


def load_limits() -> dict:
    return json.loads((ROOT / "tools" / "volumes.json").read_text("utf8"))


def gutter_min_in(pages: int, table) -> float | None:
    for lim, g in table:
        if pages <= lim:
            return g
    return None


GUTTER_TABLE = [(150, 0.375), (300, 0.500), (500, 0.625),
                (700, 0.750), (828, 0.875)]


# ------------------------------------------------------------------ colour ---
def nongray_pages(path: Path) -> tuple[list[int], list]:
    """Pages carrying a non-gray mark, and samples of what the marks are.

    Operands are tested, not operators: `0.5 0.5 0.5 rg' is DeviceRGB and is
    visually gray, so the question is whether the components are equal.
    """
    import pikepdf
    from pikepdf import Name

    def scan(owner, resources, seen, out, depth=0):
        if depth > 8:
            return
        try:
            instrs = pikepdf.parse_content_stream(owner)
        except Exception as exc:                       # a stream we cannot read
            out.append(("unparsable-stream", str(exc)[:40]))
            return
        for operands, op in instrs:
            o = str(op)
            if o == "Do":
                xo = (resources or {}).get("/XObject", {})
                ob = xo.get(str(operands[0])) if xo else None
                if ob is None:
                    continue
                if ob.get("/Subtype") == Name("/Form"):
                    if ob.objgen in seen:
                        continue
                    seen.add(ob.objgen)
                    scan(ob, ob.get("/Resources", {}), seen, out, depth + 1)
                elif ob.get("/Subtype") == Name("/Image"):
                    cs = ob.get("/ColorSpace")
                    s = str(cs) if cs is not None else "?"
                    if "Gray" not in s:
                        out.append(("image-colourspace", s[:40]))
                continue
            try:
                v = [float(x) for x in operands]
            except Exception:
                continue
            if o in ("rg", "RG") and len(v) == 3 and max(v) - min(v) > 1e-6:
                out.append(("rgb", tuple(round(x, 4) for x in v)))
            elif o in ("k", "K") and len(v) == 4 and max(v[:3]) > 1e-6:
                out.append(("cmyk", tuple(round(x, 4) for x in v)))
            elif o in ("sc", "scn", "SC", "SCN") and len(v) == 3 \
                    and max(v) - min(v) > 1e-6:
                out.append(("scn", tuple(round(x, 4) for x in v)))

    pdf = pikepdf.open(str(path))
    bad, samples = [], []
    for i, page in enumerate(pdf.pages, 1):
        out: list = []
        scan(page, page.get("/Resources", {}), set(), out)
        if out:
            bad.append(i)
            samples.extend(out[:2])
    return bad, samples[:6]


# ------------------------------------------------------------- page boxes ---
def page_boxes(path: Path):
    import pikepdf
    pdf = pikepdf.open(str(path))
    out = []
    for i, page in enumerate(pdf.pages, 1):
        mb = [float(x) for x in page.mediabox]
        extra = {k: [float(x) for x in page[k]]
                 for k in ("/CropBox", "/TrimBox", "/BleedBox", "/ArtBox")
                 if k in page}
        out.append((i, mb, extra))
    return out


def unembedded_fonts(path: Path) -> list[str]:
    r = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True)
    bad = []
    for line in r.stdout.splitlines()[2:]:
        f = line.split()
        if len(f) >= 4 and f[-5:][0] == "no":
            bad.append(f[0])
    # pdffonts columns: name type encoding emb sub uni object ID -- 'emb' is the
    # 4th from the left of the trailing fixed block. Parse by header position
    # instead, which survives a name containing a space.
    return bad


def unembedded_fonts_strict(path: Path) -> list[str]:
    r = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True)
    lines = r.stdout.splitlines()
    if len(lines) < 2:
        return []
    hdr = lines[0]
    col = hdr.index("emb")
    return [ln[:col].split()[0] if ln[:col].split() else "?"
            for ln in lines[2:] if ln[col:col + 3].strip() == "no"]


# --------------------------------------------------------------- margins ----
def ink_margins(path: Path):
    """Smallest text margin on each side, and on the inner side per parity.

    Measured from the ARTEFACT with pdftotext -bbox, as tools/checkpdf.py does,
    rather than from the geometry options -- so it keeps working when the
    geometry changes, and so it measures what was actually printed.

    It measures TEXT ink. Rules are not words and do not appear here; the frame
    hairline spans the measure and so cannot be outside it, and the margin badge
    is a word in the OUTER margin, which is why outer is reported separately and
    judged against the KDP floor rather than against the text block.
    """
    xml = subprocess.run(["pdftotext", "-bbox", str(path), "-"],
                         capture_output=True, text=True).stdout
    inner = []      # (page, margin) on the binding side
    outer, top, bottom = [], [], []
    for n, (w, h, body) in enumerate(RE_PAGE.findall(xml), start=1):
        w, h = float(w), float(h)
        xs0, xs1, ys0, ys1 = [], [], [], []
        for a, b, c, d, t in RE_WORD.findall(body):
            if not t.strip():
                continue
            xs0.append(float(a)); ys0.append(float(b))
            xs1.append(float(c)); ys1.append(float(d))
        if not xs0:
            continue                     # a genuinely blank page has no margins
        left, right = min(xs0), w - max(xs1)
        # recto = odd page number in a twoside book opening on a recto
        if n % 2 == 1:
            inner.append((n, left)); outer.append((n, right))
        else:
            inner.append((n, right)); outer.append((n, left))
        top.append((n, min(ys0))); bottom.append((n, h - max(ys1)))
    return inner, outer, top, bottom


# ----------------------------------------------------------------- report ----
def check(path: Path, cfg: dict) -> tuple[dict, list[str]]:
    fails: list[str] = []
    rep: dict = {"file": path.name}

    boxes = page_boxes(path)
    n = len(boxes)
    rep["pages"] = n

    bad_size = [i for i, mb, _ in boxes
                if abs((mb[2] - mb[0]) - TRIM_W_PT) > TRIM_TOL_PT
                or abs((mb[3] - mb[1]) - TRIM_H_PT) > TRIM_TOL_PT]
    rep["trim_ok"] = not bad_size
    if bad_size:
        i, mb, _ = boxes[bad_size[0] - 1]
        fails.append(f"{len(bad_size)} page(s) are not {TRIM_W_PT:.0f} x "
                     f"{TRIM_H_PT:.0f} pt; page {i} is "
                     f"{mb[2] - mb[0]:.2f} x {mb[3] - mb[1]:.2f} pt")

    # A no-bleed interior must have no box larger than the trim, and no crop or
    # registration furniture -- which can only live outside the trim.
    bleedy = [i for i, mb, extra in boxes
              for k, b in extra.items()
              if abs(b[2] - b[0] - (mb[2] - mb[0])) > TRIM_TOL_PT
              or abs(b[3] - b[1] - (mb[3] - mb[1])) > TRIM_TOL_PT]
    rep["bleed_artefacts"] = sorted(set(bleedy))
    if bleedy:
        fails.append(f"{len(set(bleedy))} page(s) carry a box that differs from "
                     f"the trim -- crop marks or bleed furniture")

    lim = cfg["limits"]
    rep["page_floor_ok"] = n >= lim["min_pages"]
    rep["page_ceiling_ok"] = n <= lim["max_pages_black_regular"]
    if n < lim["min_pages"]:
        fails.append(f"{n} pages is below KDP's minimum of {lim['min_pages']}")
    if n > lim["max_pages_black_regular"]:
        fails.append(f"{n} pages is above the black-ink ceiling of "
                     f"{lim['max_pages_black_regular']}")
    rep["even_ok"] = n % 2 == 0
    if n % 2:
        fails.append(f"{n} pages is odd; the last leaf prints as a stray recto")

    bad_pages, samples = nongray_pages(path)
    rep["nongray_pages"] = bad_pages[:40]
    rep["nongray_count"] = len(bad_pages)
    rep["nongray_samples"] = [[a, list(b) if isinstance(b, tuple) else b]
                              for a, b in samples]
    if bad_pages:
        fails.append(f"{len(bad_pages)} page(s) carry a non-gray mark "
                     f"(first: {bad_pages[:6]}) -- Amazon prices this as a "
                     f"colour interior")

    nofont = unembedded_fonts_strict(path)
    rep["unembedded_fonts"] = nofont
    if nofont:
        fails.append(f"{len(nofont)} font(s) not embedded: {nofont[:4]}")

    inner, outer, top, bottom = ink_margins(path)
    need_in = gutter_min_in(n, GUTTER_TABLE)
    rep["gutter_required_in"] = need_in
    if inner:
        pi, mi = min(inner, key=lambda t: t[1])
        rep["inner_margin_pt"] = round(mi, 2)
        rep["inner_margin_in"] = round(mi / PT_PER_IN, 4)
        if need_in is None:
            fails.append(f"{n} pages has no gutter bracket -- above the ceiling")
        elif mi < need_in * PT_PER_IN - 0.5:
            fails.append(f"inner margin {mi / PT_PER_IN:.3f} in on page {pi} is "
                         f"below the {need_in} in KDP requires at {n} pages")
    for name, seq in (("outer", outer), ("top", top), ("bottom", bottom)):
        if not seq:
            continue
        p, m = min(seq, key=lambda t: t[1])
        rep[f"{name}_margin_in"] = round(m / PT_PER_IN, 4)
        if m < MIN_SIDE_MARGIN_IN * PT_PER_IN - 0.5:
            fails.append(f"{name} margin {m / PT_PER_IN:.3f} in on page {p} is "
                         f"below KDP's {MIN_SIDE_MARGIN_IN} in floor")

    # Spine and cover, so the report carries what the cover job needs.
    t = cfg["paper"]["thickness_in_per_page"]
    rep["spine_in"] = round(n * t, 4)
    pr = cfg["pricing"]
    cost = pr["fixed_cost"] + pr["per_page_cost"] * n
    rep["printing_cost"] = round(cost, 2)
    rep["min_list_price"] = round(cost / pr["royalty_rate"] * (1 + pr["vat_rate"]), 2)
    rep["currency"] = pr["currency"]

    rep["ok"] = not fails
    rep["failures"] = fails
    return rep, fails


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--json", metavar="DIR",
                    help="also write <DIR>/<stem>/kdp-report.json")
    ap.add_argument("--summary", metavar="FILE",
                    help="append a markdown table (for $GITHUB_STEP_SUMMARY)")
    a = ap.parse_args()

    cfg = load_limits()
    rc = 0
    rows = []
    for p in a.pdfs:
        path = Path(p)
        if not path.exists():
            print(f"== {p} ==\n  MISSING")
            rc = 1
            continue
        rep, fails = check(path, cfg)
        print(f"== {path.name} ==")
        print(f"  pages           : {rep['pages']}"
              f"  ({'even' if rep['even_ok'] else 'ODD'})")
        print(f"  trim            : "
              f"{'6 x 9 in on every page' if rep['trim_ok'] else 'WRONG'}")
        print(f"  colour          : {rep['nongray_count']} non-gray page(s)")
        print(f"  fonts           : "
              f"{len(rep['unembedded_fonts'])} not embedded")
        print(f"  inner margin    : {rep.get('inner_margin_in', '?')} in "
              f"(needs {rep['gutter_required_in']})")
        print(f"  outer/top/bottom: {rep.get('outer_margin_in','?')} / "
              f"{rep.get('top_margin_in','?')} / {rep.get('bottom_margin_in','?')} in")
        print(f"  spine           : {rep['spine_in']} in")
        print(f"  printing cost   : {rep['printing_cost']} {rep['currency']}"
              f"   min list {rep['min_list_price']}")
        for f in fails:
            print(f"  FAIL  {f}")
        if not fails:
            print("  OK")
        rows.append(rep)
        rc |= 1 if fails else 0
        if a.json:
            d = Path(a.json) / path.stem
            d.mkdir(parents=True, exist_ok=True)
            (d / "kdp-report.json").write_text(json.dumps(rep, indent=1), "utf8")

    if a.summary and rows:
        with open(a.summary, "a", encoding="utf8") as fh:
            fh.write("\n| volume | pages | trim | colour | fonts | gutter | "
                     "spine | cost | min list |\n|---|---|---|---|---|---|---|"
                     "---|---|\n")
            for r in rows:
                fh.write(f"| {r['file']} | {r['pages']} | "
                         f"{'ok' if r['trim_ok'] else 'BAD'} | "
                         f"{r['nongray_count']} | "
                         f"{len(r['unembedded_fonts'])} | "
                         f"{r.get('inner_margin_in','?')} in | "
                         f"{r['spine_in']} in | "
                         f"{r['printing_cost']} {r['currency']} | "
                         f"{r['min_list_price']} |\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
