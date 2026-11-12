"""English EGA: residue fields written \\kappa(...) or \\mathbf{k}(...) where the print has the bold italic k (\\kres)
(ENGLISH_SLIPS.md: content_012, content_015/016, content_018, misprint_en_003). Lists every \\kappa and \\mathbf{k}
use with its argument, so that only residue fields are changed.
usage: python -I en_kres.py [--apply]   (log EN_KRES_LOG.jsonl)"""
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
E = ROOT / "ega-en" / "tex"
BS = chr(92)
PAT = re.compile(r"\\kappa(?![A-Za-z])|\\mathbf\{k\}|\\mathbf k(?![A-Za-z])")
apply = "--apply" in sys.argv
kinds = collections.Counter()
samples = collections.defaultdict(list)
log = []
for f in sorted(E.rglob("*.tex")):
    t = f.read_text(encoding="utf-8")
    out, last = [], 0
    for m in PAT.finditer(t):
        after = t[m.end():m.end() + 1]
        nxt = t[m.end():m.end() + 25]
        if after == "(":
            kind = "residue"  # \kappa(x), \mathbf{k}(y): residue field
        elif after == "_" or after == "^":
            kind = "sub/sup"
        else:
            kind = "other"
        kinds[(m.group(0)[:7], kind)] += 1
        if len(samples[(m.group(0)[:7], kind)]) < 4:
            samples[(m.group(0)[:7], kind)].append(f.name + ": " + t[max(0, m.start() - 35):m.end() + 25].replace("\n", " "))
        if kind == "residue":
            out.append(t[last:m.start()])
            out.append(BS + "kres")
            last = m.end()
            log.append({"file": str(f.relative_to(E)), "old": m.group(0) + nxt[:12], "new": BS + "kres" + nxt[:12]})
    out.append(t[last:])
    new = "".join(out)
    if apply and new != t:
        f.write_text(new, encoding="utf-8", newline="")
for k, v in sorted(kinds.items()):
    print(k, v)
    for s in samples[k]:
        print("    ", s)
if apply:
    with open(ROOT / "EN_KRES_LOG.jsonl", "a", encoding="utf-8") as fh:
        for x in log:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
print(len(log), "residue-field uses", "replaced" if apply else "(dry run)")
