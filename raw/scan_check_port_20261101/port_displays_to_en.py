"""Carry the French corrections that set a displayed formula inline (as the print has it) into the English EGA.

For each FIXLOG_CURRENT entry whose old text has a display \\[ ... \\] and whose new text sets it inline ($ ... $),
the English display with the same formula (compared without spaces and without trailing punctuation) is looked for
on the same printed page or the page before or after. If exactly one such display exists, it is replaced by the
inline formula(s) of the French correction, followed by the English display's own trailing punctuation. Skipped:
corrections whose new text has words between the formulas, displays carrying \\tag or \\label, and anything not
found exactly once. Log: PORT_EN_DISPLAY_LOG.jsonl (keyed by the entry's line number, so reruns skip done entries).

usage: python -I port_displays_to_en.py [--apply]
"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
EN = E / "ega-en" / "tex"
LOG = E / "PORT_EN_DISPLAY_LOG.jsonl"
apply = "--apply" in sys.argv
MARK = re.compile(r"\\oldpage\[([^\]]+)\]\{(\d+)\}")
DISPLAY = re.compile(r"[ \t]*\n?[ \t]*\\\[(.*?)\\\]", re.S)
INLINE = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$", re.S)
TRAIL = re.compile(r"(?:\s|\\[,;:!]|\\q?quad)*([.,;:])?(?:\s|\\[,;:!]|\\q?quad)*$")


def norm(m):
    """Formula without spaces, thin spaces, quads and trailing punctuation, for comparison."""
    m = re.sub(r"\\(?:[,;:!]|q?quad|nonumber)", "", m)
    m = re.sub(r"\s+", "", m)
    return m.rstrip(".,;:")


SKEL_DROP = re.compile(r"\\(?:mathcal|mathscr|sh|mathrm|mathbf|boldsymbol|bm|mathit|operatorname|textup|text|mathsf|"
                       r"mathbb|left|right|bigl|bigr|Bigl|Bigr|big|Big|displaystyle|[,;:!]|q?quad)(?![A-Za-z])")
SKEL_MAP = [(r"\\(?:longrightarrow|rightarrow)(?![A-Za-z])", r"\\to"), (r"\\RR(?![A-Za-z])", "R"),
            (r"\\HH(?![A-Za-z])", "H"), (r"\\kres(?![A-Za-z])", "k"), (r"\\setmin(?![A-Za-z])", "-"),
            (r"\\(?:isoto|simto)(?![A-Za-z])", r"\\to"), (r"\\red(?![A-Za-z])", "red")]


def skel(m):
    """Formula with fonts, sizes, spacing, braces and the English edition's own macro names removed: the same
    formula in the French and English sources has the same skeleton."""
    for a, b in SKEL_MAP:
        m = re.sub(a, b, m)
    m = SKEL_DROP.sub("", m)
    m = re.sub(r"[{}\s]", "", m)
    return m.rstrip(".,;:")


def segments(text):
    out = collections.defaultdict(list)
    ms = list(MARK.finditer(text))
    if ms:
        out[(ms[0].group(1), int(ms[0].group(2)) - 1)].append((0, ms[0].start()))
    for i, m in enumerate(ms):
        out[(m.group(1), int(m.group(2)))].append((m.start(), ms[i + 1].start() if i + 1 < len(ms) else len(text)))
    return out


en_files = sorted(EN.rglob("*.tex"))
en_text = {f: f.read_text(encoding="utf-8") for f in en_files}
en_segs = {f: segments(t) for f, t in en_text.items()}
done = set()
if LOG.exists():
    done = {json.loads(l)["entry"] for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()}
log = open(LOG, "a", encoding="utf-8") if apply else None
stats = collections.Counter()
changed = set()
for n, line in enumerate(open(E / "FIXLOG_CURRENT.jsonl", encoding="utf-8"), 1):
    if not line.strip() or n in done:
        continue
    x = json.loads(line)
    old, new = x["old"], x["new"]
    if "\\[" not in old or "\\[" in new or "$" not in new:
        continue
    part, page = x.get("part") or "I", int(x["page"])
    rec = dict(entry=n, part=part, page=page)
    fr_disp = re.findall(r"\\\[(.*?)\\\]", old, re.S)
    inl = list(INLINE.finditer(new))
    between = new[inl[0].start():inl[-1].end()] if inl else ""
    words_between = re.sub(r"(?<!\\)\$.+?(?<!\\)\$", " ", between, flags=re.S)
    if len(fr_disp) != 1 or not inl or re.search(r"[A-Za-zÀ-ÿ]{2,}", re.sub(r"\\[A-Za-z]+", "", words_between)):
        rec["outcome"] = "skip: several displays or words between formulas"
    else:
        target = {norm(fr_disp[0]), norm("".join(m.group(1) for m in inl))}
        inline_math = between.rstrip()
        inline_math = re.sub(r"[.,;:]\s*$", "", inline_math)  # the English keeps its own trailing punctuation
        hits = []
        for p in (page - 1, page, page + 1):
            for f in en_files:
                for s, e in en_segs[f].get((part, p), []):
                    for m in DISPLAY.finditer(en_text[f], s, e):
                        body = m.group(1)
                        if "\\tag" in body or "\\label" in body:
                            continue
                        if norm(body) in target:
                            hits.append((f, m.start(), m.end(), body))
        if not hits and len(inl) == 1:
            # second pass: same formula in the English edition's own notation; set the English formula inline
            tskel = {skel(fr_disp[0]), skel(inl[0].group(1))}
            cand = []
            for p in (page - 1, page, page + 1):
                for f in en_files:
                    for s, e in en_segs[f].get((part, p), []):
                        for m in DISPLAY.finditer(en_text[f], s, e):
                            body = m.group(1)
                            if re.search(r"\\tag|\\label|\\\\|&|\\begin|\\q?quad", body):
                                continue
                            if skel(body) in tskel:
                                cand.append((f, m.start(), m.end(), body))
            if len(cand) == 1:
                f, a, b, body = cand[0]
                punct = TRAIL.search(body).group(1) or ""
                core = TRAIL.sub("", body).strip()
                core = re.sub(r"\s*\n\s*", "\n", core)
                hits = [(f, a, b, body)]
                inline_math = "$" + core + "$"
        if len(hits) != 1:
            rec["outcome"] = f"skip: {len(hits)} matching English displays"
        else:
            f, a, b, body = hits[0]
            punct = TRAIL.search(body).group(1) or ""
            rep = " " + inline_math + punct
            rec.update(outcome="applied", en_file=f.name, en_line=en_text[f].count("\n", 0, a) + 1,
                       en_old=en_text[f][a:b], en_new=rep)
            if apply:
                en_text[f] = en_text[f][:a] + rep + en_text[f][b:]
                en_segs[f] = segments(en_text[f])
                changed.add(f)
    stats[rec["outcome"].split(":")[0] if rec["outcome"].startswith("skip") else rec["outcome"]] += 1
    if rec["outcome"].startswith("skip"):
        stats[rec["outcome"]] += 1
    if log:
        log.write(json.dumps(rec, ensure_ascii=False) + "\n")
    elif rec["outcome"] == "applied" and stats["applied"] <= 6:
        print(f"  {part} p{page} {rec['en_file']}:{rec['en_line']}\n    {rec['en_old'][:140]!r}\n -> {rec['en_new'][:140]!r}")
if apply:
    for f in changed:
        f.write_text(en_text[f], encoding="utf-8", newline="")
print(("applied" if apply else "dry run"), {k: v for k, v in stats.items() if v})
