"""Apply the English hand-pass agents' decisions (one JSON list per batch) to the English EGA.

An "apply" decision is applied when en_old occurs exactly once in the English text of pages PAGE-1..PAGE+1 of the
item's part, in en_file (or, if en_file is wrong, in exactly one file); otherwise it goes to PORT_EN_LEFT3.json.
Every decision is logged in PORT_EN_LOG3.jsonl (entry = FIXLOG_CURRENT line number of the French fix).

usage: python -I apply_port_decisions.py DECISIONS.json [DECISIONS.json ...] [--dry]
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
dry = "--dry" in sys.argv
paths = [pathlib.Path(a) for a in sys.argv[1:] if not a.startswith("--")]
MARK = re.compile(re.escape(BS) + r"oldpage\[([^\]]+)\]\{(\d+)\}")
meta = {}
for name in ("PORT_EN_HAND2.json", "PORT_EN_HAND3_content.json", "PORT_EN_HAND3_typography.json", "PORT_EN_HAND_MISPRINTS.json"):
    if (E / name).exists():
        meta.update({x["entry"]: x for x in json.loads((E / name).read_text(encoding="utf-8"))})
done = set()
LOG = E / "PORT_EN_LOG3.jsonl"
if LOG.exists():
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            if d.get("outcome") == "left":   # an edit that did not place may be decided again (9 Nov: second look)
                done.discard(d["entry"])
            else:
                done.add(d["entry"])
files = sorted(EN.rglob("*.tex"))
text = {f: f.read_text(encoding="utf-8") for f in files}


def bal(s):
    """Brace balance, ignoring \\{ \\} and \\\\: an edit must not change it (9 Nov: Sol once wrote \\textup{(resp.\\})."""
    s = s.replace(BS * 2, "").replace(BS + "{", "").replace(BS + "}", "")
    return s.count("{") - s.count("}")


def spans(f, part, page):
    t = text[f]
    ms = list(MARK.finditer(t))
    out = []
    for p in (page - 1, page, page + 1):
        if ms and (part, p) == (ms[0].group(1), int(ms[0].group(2)) - 1):
            out.append((0, ms[0].start()))
        for i, m in enumerate(ms):
            if (m.group(1), int(m.group(2))) == (part, p):
                out.append((m.start(), ms[i + 1].start() if i + 1 < len(ms) else len(t)))
    return out


def occurrences(f, part, page, s):
    t = text[f]
    hits = []
    for a, b in spans(f, part, page):
        k = t.find(s, a)
        while k >= 0 and k + len(s) <= b:
            hits.append(k)
            k = t.find(s, k + 1)
    return sorted(set(hits))


stats = collections.Counter()
left = json.loads((E / "PORT_EN_LEFT3.json").read_text(encoding="utf-8")) if (E / "PORT_EN_LEFT3.json").exists() else []
changed = set()
logrecs = []
for path in paths:
    for d in json.loads(path.read_text(encoding="utf-8")):
        entry = int(d["id"])
        if entry in done or entry not in meta:
            stats["skipped"] += 1
            continue
        x = meta[entry]
        part, page = x["part"], int(x["page"])
        rec = dict(entry=entry, part=part, page=page, decision=d.get("decision"), note=d.get("note"), batch=path.stem)
        if d.get("decision") == "apply":
            old = (d.get("en_old") or "").replace("\r\n", "\n")
            new = (d.get("en_new") or "").replace("\r\n", "\n")
            cands = [f for f in files if f.name == pathlib.Path(d.get("en_file") or "").name or
                     str(f.relative_to(EN)).replace(BS, "/") == (d.get("en_file") or "")]
            hit = None
            for f in cands:
                occ = occurrences(f, part, page, old) if old else []
                if len(occ) == 1:
                    hit = (f, occ[0])
            if hit is None and old:
                allhits = [(f, k) for f in files for k in occurrences(f, part, page, old)]
                if len(allhits) == 1:
                    hit = allhits[0]
            if hit is None or MARK.search(old) or MARK.search(new) or old == new or bal(old) != bal(new):
                rec["outcome"] = "left"
                left.append(dict(d, part=part, page=page, why="en_old not found exactly once on pages p-1..p+1"))
            else:
                f, k = hit
                if not dry:
                    text[f] = text[f][:k] + new + text[f][k + len(old):]
                    changed.add(f)
                rec.update(outcome="applied", en_file=str(f.relative_to(EN)).replace(BS, "/"), en_old=old, en_new=new)
        else:
            rec["outcome"] = d.get("decision")
        stats[rec["outcome"]] += 1
        logrecs.append(rec)
if not dry:
    for f in changed:
        f.write_text(text[f], encoding="utf-8", newline="")
    with open(LOG, "a", encoding="utf-8") as fh:
        for r in logrecs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (E / "PORT_EN_LEFT3.json").write_text(json.dumps(left, ensure_ascii=False, indent=1), encoding="utf-8")
print(("dry run " if dry else "") + ", ".join(f"{k} {v}" for k, v in sorted(stats.items())),
      "| files changed", len(changed))
rejected = [r["entry"] for r in logrecs if r["outcome"] == "left"]
if rejected:
    print("rejected ids (en_old not found exactly once on pages p-1..p+1, or an edit of a marker):", rejected)
