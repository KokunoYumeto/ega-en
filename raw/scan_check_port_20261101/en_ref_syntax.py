"""English EGA: two scriptable reference-syntax slips (ENGLISH_SLIPS.md, content_015/016, 022, 023):
1. "(\\sref{KEY})": the macro prints its own parentheses, so the outer pair doubles them -> "\\sref{KEY}".
2. "\\sref{KEY}[(i)]", "\\sref{KEY}[i]": the bracket prints literally -> "\\sref{KEY},~(i)" (the edition's form).
usage: python -I en_ref_syntax.py [--apply]   (dry run by default; log EN_REF_SYNTAX_LOG.jsonl)"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
E = ROOT / "ega-en" / "tex"
SREF = r"\\sref(?:\[[^\]]*\])?\{[^}]*\}"
PAT_DBL = re.compile(r"\((" + SREF + r")\)")
PAT_BR = re.compile(r"(" + SREF + r")\[\(?([ivx]+|[a-z]'*)\)?\]")
apply = "--apply" in sys.argv
log = []
for f in sorted(E.rglob("*.tex")):
    t = f.read_text(encoding="utf-8")
    new = t
    for pat, repl, kind in ((PAT_DBL, lambda m: m.group(1), "doubled"),
                            (PAT_BR, lambda m: m.group(1) + ",~(" + m.group(2) + ")", "bracket")):
        out, last = [], 0
        for m in pat.finditer(new):
            r = repl(m)
            log.append({"file": str(f.relative_to(E)), "kind": kind, "old": m.group(0), "new": r,
                        "context": new[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")})
            out.append(new[last:m.start()])
            out.append(r)
            last = m.end()
        out.append(new[last:])
        new = "".join(out)
    if apply and new != t:
        f.write_text(new, encoding="utf-8", newline="")
by = {}
for x in log:
    by.setdefault((x["file"], x["kind"]), 0)
    by[(x["file"], x["kind"])] += 1
for k, v in sorted(by.items()):
    print(k, v)
for x in log[:8]:
    print(x["kind"], "|", x["context"])
if apply:
    with open(ROOT / "EN_REF_SYNTAX_LOG.jsonl", "a", encoding="utf-8") as fh:
        for x in log:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
print("total", len(log), "applied" if apply else "(dry run)")
