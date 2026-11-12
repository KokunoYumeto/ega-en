"""Check Sol's bulk decisions before they are applied (mechanical checks; the doubtful ones go to a second look).

For every id of decisions_bulk_*.json, with the French fix OLD -> NEW from PORT_EN_HAND3_typography.json:
- apply: en_old must occur exactly once on the English pages p-1..p+1 (as apply_port_decisions.py requires);
- already: en_old (the English that "already says it") must occur there, and must carry the markup the fix adds:
  \\emph for an added emphasis, no \\emph for a removed one, \\textup (or \\rm, \\upshape, or a position outside every
  italic statement environment) for an added upright parenthesis or label;
- not_applicable: doubtful when the fix adds or removes \\emph or \\textup (those normally carry over);
- unclear, and every id without a decision: doubtful.
Writes AUDIT.md (counts and every doubtful id with the French fix and Sol's answer) and doubtful_ids.json.
usage: python -I audit_bulk.py"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
E = HERE.parent
EN = E / "ega-en" / "tex"
BS = chr(92)
MARK = re.compile(re.escape(BS) + r"oldpage\[([^\]]+)\]\{(\d+)\}")
ITALIC = ("theorem", "proposition", "corollary", "lemma", "conjecture", "env", "statement")
meta = {x["entry"]: x for x in json.loads((E / "PORT_EN_HAND3_typography.json").read_text(encoding="utf-8"))}
files = sorted(EN.rglob("*.tex"))
text = {f: f.read_text(encoding="utf-8") for f in files}
marks = {f: list(MARK.finditer(t)) for f, t in text.items()}


def spans(f, part, page):
    ms, out = marks[f], []
    for p in (page - 1, page, page + 1):
        if ms and (part, p) == (ms[0].group(1), int(ms[0].group(2)) - 1):
            out.append((0, ms[0].start()))
        for i, m in enumerate(ms):
            if (m.group(1), int(m.group(2))) == (part, p):
                out.append((m.start(), ms[i + 1].start() if i + 1 < len(ms) else len(text[f])))
    return out


def find(part, page, s):
    hits = []
    for f in files:
        for a, b in spans(f, part, page):
            k = text[f].find(s, a)
            while k >= 0 and k + len(s) <= b:
                hits.append((f, k))
                k = text[f].find(s, k + 1)
    return sorted(set(hits))


def in_italic(f, k):
    """Is position k inside an open theorem-like environment (italic statement)?"""
    t = text[f][:k]
    depth = collections.Counter()
    for m in re.finditer(r"\\(begin|end)\{([A-Za-z*]+)\}", t):
        env = m.group(2).rstrip("*")
        if any(env.startswith(x) for x in ITALIC):
            depth[env] += 1 if m.group(1) == "begin" else -1
    return any(v > 0 for v in depth.values())


def kind(old, new):
    e_old, e_new = old.count(BS + "emph"), new.count(BS + "emph")
    u_old, u_new = old.count(BS + "textup"), new.count(BS + "textup")
    if u_new > u_old:
        return "textup+"
    if e_new > e_old:
        return "emph+"
    if e_new < e_old:
        return "emph-"
    if e_new == e_old and e_new > 0 and old != new:
        return "emph~"
    return "other"


def upright_labels(f, k):
    """Does the enumerate around position k set its labels upright (label=\\rm..., \\textup, \\upshape, \\normalfont)?"""
    t = text[f]
    b = t.rfind("\\begin{enumerate}", 0, k)
    if b < 0 or t.rfind("\\end{enumerate}", b, k) >= 0:
        return False
    opts = re.match(r"\\begin\{enumerate\}\s*(\[[^\n]*\])?", t[b:b + 200])
    return bool(opts and opts.group(1) and re.search(r"\\(rm|textup|upshape|normalfont)", opts.group(1)))


alldec = {}
for path in sorted(HERE.glob("decisions_bulk_*.json")):
    for d in json.loads(path.read_text(encoding="utf-8")):
        alldec[int(d["id"])] = d
rows, doubt, stats = [], [], collections.Counter()
for path in sorted(HERE.glob("decisions_bulk_*.json")):
    for d in json.loads(path.read_text(encoding="utf-8")):
        i = int(d["id"])
        x = meta.get(i)
        if not x:
            stats["unknown id"] += 1
            continue
        part, page = x["part"], int(x["page"])
        k = kind(x["old"], x["new"])
        dec = d.get("decision")
        why = None
        old = (d.get("en_old") or "").replace("\r\n", "\n")
        if dec == "apply":
            if len(find(part, page, old)) != 1:
                why = "apply: en_old not found exactly once on pages p-1..p+1"
        elif dec == "already":
            hits = find(part, page, old) if old else []
            cov = re.search(r"covered by (\d+)", d.get("note") or "")
            if cov and (alldec.get(int(cov.group(1))) or {}).get("decision") == "apply":
                why = None
            elif not hits:
                why = "already: en_old missing or not found"
            elif k == "emph+" and BS + "emph" not in old:
                why = "already: the fix adds an emphasis but the quoted English has none"
            elif k == "emph-" and BS + "emph" in old:
                why = "already: the fix removes an emphasis but the quoted English has one"
            elif k == "textup+" and not re.search(r"\\(textup|rm\b|upshape|emph)", old):
                f0, k0 = hits[0]
                if in_italic(f0, k0) and not upright_labels(f0, k0):
                    why = "already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement"
        elif dec == "not_applicable":
            if k in ("emph+", "emph-", "textup+", "emph~"):
                why = f"not_applicable for a {k} fix"
        else:
            why = f"decision {dec!r}"
        stats[(dec, "doubtful" if why else "ok")] += 1
        if why:
            doubt.append({"id": i, "batch": path.stem, "part": part, "page": page, "kind": k, "fr_old": x["old"],
                          "fr_new": x["new"], "decision": dec, "en_old": d.get("en_old"), "en_new": d.get("en_new"),
                          "note": d.get("note"), "why": why})
(HERE / "doubtful_ids.json").write_text(json.dumps(doubt, ensure_ascii=False, indent=1), encoding="utf-8")
L = ["# Audit of Sol's bulk decisions", "", "| decision | ok | doubtful |", "|---|---:|---:|"]
for dec in ("apply", "already", "not_applicable", "unclear", None):
    L.append(f"| {dec} | {stats[(dec, 'ok')]} | {stats[(dec, 'doubtful')]} |")
L += ["", f"Doubtful by reason: {dict(collections.Counter(d['why'] for d in doubt))}", ""]
for d in doubt:
    L += [f"## {d['id']} ({d['part']} {d['page']}, {d['kind']}, {d['batch']}): {d['why']}",
          f"FR: {d['fr_old']!r} -> {d['fr_new']!r}", f"Sol: {d['decision']} | en_old {d['en_old']!r} | en_new "
          f"{d['en_new']!r} | note {d['note']!r}", ""]
(HERE / "AUDIT.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L[:10]))
