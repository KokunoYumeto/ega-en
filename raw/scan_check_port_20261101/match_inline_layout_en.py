"""Set inline in the English EGA the displayed formulas that the French edition (corrected text, which follows the
print) has inside the sentence.

For each English display \\[ ... \\] without \\tag, \\label, alignment or line breaks, on printed page p (by the
\\oldpage markers), the formula's skeleton (fonts, sizes, spacing, braces and the English macro names removed) is
compared with the French formulas of pages p-1 .. p+1: if the French has it inline ($ ... $) and nowhere as a
display, the English display becomes an inline formula followed by its own trailing punctuation. Log:
PORT_EN_INLINE_LAYOUT.jsonl. usage: python -I match_inline_layout_en.py [--apply]
"""
import collections
import json
import pathlib
import re
import runpy
import sys

sys.stdout.reconfigure(encoding="utf-8")
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
sys_argv, sys.argv = sys.argv, ["port_displays_to_en.py"]
g = runpy.run_path(str(E / "port_displays_to_en.py"), run_name="helpers")  # dry run there: only its helpers are used
sys.argv = sys_argv
skel, segments, TRAIL = g["skel"], g["segments"], g["TRAIL"]
apply = "--apply" in sys.argv
FUZZY = "--fuzzy" in sys.argv  # also near matches: >= 90 % similar to a French inline formula, unlike any display
import difflib
EN = E / "ega-en" / "tex"
FR = E / "ega-fr" / "editions" / "2026-10-24-r20" / "current" / "packages"
DISPLAY = re.compile(r"[ \t]*\n?[ \t]*\\\[(.*?)\\\]", re.S)
FR_DISPLAY = re.compile(r"\\\[(.*?)\\\]|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)\}(.*?)\\end\{\2\}"
                        r"|\$\$(.*?)\$\$", re.S)
INLINE = re.compile(r"(?<!\\)(?<!\$)\$(?!\$)(.+?)(?<!\\)\$", re.S)

fr_inline = collections.defaultdict(set)   # (part, page) -> skeletons of inline formulas
fr_display = collections.defaultdict(set)  # (part, page) -> skeletons of displayed formulas
for f in sorted(FR.glob("*/native/**/*.tex")):
    t = f.read_text(encoding="utf-8")
    for key, spans in segments(t).items():
        for s, e in spans:
            seg = t[s:e]
            for m in FR_DISPLAY.finditer(seg):
                body = m.group(1) or m.group(3) or m.group(4) or ""
                fr_display[key].add(skel(body))
            no_disp = FR_DISPLAY.sub(" ", seg)
            for m in INLINE.finditer(no_disp):
                fr_inline[key].add(skel(m.group(1)))

stats = collections.Counter()
log = open(E / "PORT_EN_INLINE_LAYOUT.jsonl", "a", encoding="utf-8") if apply else None
for f in sorted(EN.rglob("*.tex")):
    t = f.read_text(encoding="utf-8")
    segs = segments(t)
    edits = []
    for (part, page), spans in segs.items():
        near_inline = set().union(*(fr_inline.get((part, p), set()) for p in (page - 1, page, page + 1)))
        near_display = set().union(*(fr_display.get((part, p), set()) for p in (page - 1, page, page + 1)))
        for s, e in spans:
            for m in DISPLAY.finditer(t, s, e):
                body = m.group(1)
                if re.search(r"\\tag|\\label|\\\\|&|\\begin|\\q?quad|\\xymatrix|\\EGAReaderTarget", body):
                    stats["kept: numbered, aligned or diagram"] += 1
                    continue
                k = skel(body)
                if len(k) < 3:
                    continue
                fuzzy_inline = False
                if FUZZY and k not in near_inline and k not in near_display and len(k) >= 8:
                    best_in = max((difflib.SequenceMatcher(None, k, c).ratio() for c in near_inline
                                   if abs(len(c) - len(k)) <= 0.2 * len(k)), default=0)
                    best_disp = max((difflib.SequenceMatcher(None, k, c).ratio() for c in near_display
                                     if abs(len(c) - len(k)) <= 0.3 * len(k)), default=0)
                    fuzzy_inline = best_in >= 0.9 and best_disp < 0.8
                    if fuzzy_inline and not apply and "--show" in sys.argv and stats["shown"] < 10:
                        stats["shown"] += 1
                        c = max((c for c in near_inline), key=lambda c: difflib.SequenceMatcher(None, k, c).ratio())
                        print(f"  {part} p{page} {f.name}\n    EN display: {k[:120]}\n    FR inline:  {c[:120]}")
                if (k in near_inline and k not in near_display) or fuzzy_inline:
                    punct = TRAIL.search(body).group(1) or ""
                    core = re.sub(r"\s*\n\s*", "\n", TRAIL.sub("", body).strip())
                    edits.append((m.start(), m.end(), " $" + core + "$" + punct, part, page))
                elif k in near_display:
                    stats["kept: displayed in the French too"] += 1
                else:
                    stats["kept: no French counterpart found"] += 1
    if edits:
        stats["set inline"] += len(edits)
        if apply:
            for a, b, rep, part, page in sorted(edits, reverse=True):
                log.write(json.dumps(dict(file=f.name, part=part, page=page, old=t[a:b], new=rep), ensure_ascii=False) + "\n")
                t = t[:a] + rep + t[b:]
            f.write_text(t, encoding="utf-8", newline="")
print(("applied" if apply else "dry run"), dict(stats))
