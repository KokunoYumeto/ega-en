"""Write the agent batches for the English hand pass from PORT_EN_HAND2.json.

Each batch is one plain-text file (no JSON escaping, so the agent reads the TeX as it is): per printed page, the
English text of the page and its neighbours, then the French corrections of that page with their corrected French
context. Pages are never split across batches. An index BATCHES.json lists the item ids of every batch.

usage: python -I make_port_batches.py OUTDIR [ITEMS_PER_BATCH]
"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BS = chr(92)
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
EN = E / "ega-en" / "tex"
FR_ROOT = E / "ega-fr" / "editions" / "2026-10-24-r20" / "current" / "packages"
out = pathlib.Path(sys.argv[1])
per = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else 120
out.mkdir(parents=True, exist_ok=True)
MARK = re.compile(re.escape(BS) + r"oldpage\[([^\]]+)\]\{(\d+)\}")


def segments(text):
    segs = collections.defaultdict(list)
    ms = list(MARK.finditer(text))
    if ms:
        segs[(ms[0].group(1), int(ms[0].group(2)) - 1)].append((0, ms[0].start()))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        segs[(m.group(1), int(m.group(2)))].append((m.start(), end))
    return segs


en = {}
for f in sorted(EN.rglob("*.tex")):
    t = f.read_text(encoding="utf-8")
    en[f] = (t, segments(t))
fr = {}
for f in sorted(FR_ROOT.glob("*/native/**/*.tex")):
    t = f.read_text(encoding="utf-8")
    fr[f] = (t, segments(t))


def en_page(part, page):
    """[(relative file name, text)] of one printed page of the English."""
    res = []
    for f, (t, segs) in en.items():
        for s, e in segs.get((part, page), []):
            res.append((str(f.relative_to(EN)).replace(BS, "/"), t[s:e]))
    return res


def fr_context(part, page, new, width=260):
    best = None
    for f, (t, segs) in fr.items():
        for p in (page, page - 1, page + 1):
            for s, e in segs.get((part, p), []):
                k = t.find(new, s, e + len(new)) if new.strip() else -1
                if k >= 0:
                    best = t[max(0, k - width):k + len(new) + width]
                    return best
    return best


src = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--items=")]
items = json.loads((E / (src[0] if src else "PORT_EN_HAND2.json")).read_text(encoding="utf-8"))
fixlog = {}
for n, line in enumerate(open(E / "FIXLOG_CURRENT.jsonl", encoding="utf-8"), 1):
    if line.strip():
        fixlog[n] = json.loads(line)
order = {}
PARTS = ["0" + BS + "textsubscript{I}", "I", "II", "0" + BS + "textsubscript{III}", "III", "IV",
         "0" + BS + "textsubscript{IV-1}", "IV-1", "IV-2", "IV-3", "IV-4"]
bypage = collections.defaultdict(list)
for x in items:
    bypage[(x["part"], int(x["page"]))].append(x)
keys = sorted(bypage, key=lambda k: (PARTS.index(k[0]) if k[0] in PARTS else 99, k[1]))
batches, cur, n = [], [], 0
for k in keys:
    if cur and n + len(bypage[k]) > per:
        batches.append(cur)
        cur, n = [], 0
    cur.append(k)
    n += len(bypage[k])
if cur:
    batches.append(cur)

prefix = ([a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--prefix=")] or ["batch"])[0]
index = []
for b, ks in enumerate(batches, 1):
    name = f"{prefix}_{b:03d}"
    lines = [f"# English hand pass, {name}: {sum(len(bypage[k]) for k in ks)} items on {len(ks)} printed pages", ""]
    ids = []
    shown = set()
    for part, page in ks:
        lines.append(f"=================== PAGE {part} {page} ===================")
        for p in (page - 1, page, page + 1):
            if (part, p) in shown:
                lines.append(f"----- (English page {part} {p}: shown above in this file) -----")
                continue
            shown.add((part, p))
            for fname, txt in en_page(part, p):
                lines.append(f"----- English, {fname}, page {part} {p} -----")
                lines.append(txt.rstrip("\n"))
        lines.append(f"----- French corrections on page {part} {page} -----")
        for x in bypage[(part, page)]:
            fx = fixlog.get(x["entry"], {})
            ids.append(x["entry"])
            lines.append(f"[id {x['entry']}]")
            lines.append("OLD: " + x["old"])
            lines.append("NEW: " + x["new"])
            why = fx.get("why") or x.get("why")
            if why:
                lines.append("WHY: " + str(why))
            ctx = fr_context(part, page, x["new"])
            if ctx:
                lines.append("FRENCH CONTEXT (corrected): " + ctx)
            lines.append("")
    (out / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    index.append(dict(batch=name, items=len(ids), pages=[f"{p} {g}" for p, g in ks], ids=ids))
(out / f"BATCHES_{prefix}.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
sizes = [(out / f"{x['batch']}.txt").stat().st_size for x in index]
print(len(index), "batches;", sum(x["items"] for x in index), "items; size KB min/max/mean",
      min(sizes) // 1024, max(sizes) // 1024, sum(sizes) // len(sizes) // 1024)
