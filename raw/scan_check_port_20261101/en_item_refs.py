"""English EGA IV: references to item labels (\\sref{IV.4.9.1.a}, \\sref{IV.5.1.10.ii}) print the paragraph number
without the item, or "((i))" (slips agent of IV 2-5). Rewrite them in the edition's form \\sref{KEY},~a) /
\\sref{KEY},~(ii) when the paragraph key KEY exists as a label; "bprime" -> b').
usage: python -I en_item_refs.py [--apply]   (log EN_ITEM_REFS_LOG.jsonl)"""
import json
import pathlib
import re
import sys

E = pathlib.Path(__file__).parent
T = E / "ega-en" / "tex"
BS = chr(92)
apply = "--apply" in sys.argv
labels = set()
for f in T.rglob("*.tex"):
    labels.update(re.findall(r"\\label\{([^}]*)\}", f.read_text(encoding="utf-8")))
PAT = re.compile(r"\\sref(\[[^\]]*\])?\{(IV\.[0-9.]+?)\.([a-z]+(?:prime)?)\}")
ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}
log = []
for f in sorted(T.rglob("*.tex")):
    t = f.read_text(encoding="utf-8")
    out, last = [], 0
    for m in PAT.finditer(t):
        opt, key, item = m.group(1) or "", m.group(2), m.group(3)
        if key not in labels:
            log.append({"file": str(f.relative_to(T)), "old": m.group(0), "new": None, "note": "no label " + key})
            continue
        if item in ROMAN:
            sub = "(" + item + ")"
        else:
            letter = item.replace("prime", "")
            if len(letter) != 1:
                log.append({"file": str(f.relative_to(T)), "old": m.group(0), "new": None, "note": "unknown item"})
                continue
            sub = "$" + letter + ("'" if item.endswith("prime") else "") + ")$" if False else letter + ("'" if item.endswith("prime") else "") + ")"
        # inside the paragraph (or its proof) the item is cited bare, as in the print: "a)", "(ii)"
        heads = [h for h in re.finditer(r"\\label\{(IV\.[0-9.]+?)\}", t[:m.start()]) if not re.search(r"\.[a-z]+$", h.group(1))]
        if heads and heads[-1].group(1) == key and not opt:
            new = BS + "textup{" + sub + "}"
        else:
            new = BS + "sref" + opt + "{" + key + "},~" + sub
        out.append(t[last:m.start()])
        out.append(new)
        last = m.end()
        log.append({"file": str(f.relative_to(T)), "old": m.group(0), "new": new})
    out.append(t[last:])
    if apply and len(out) > 1:
        f.write_text("".join(out), encoding="utf-8", newline="")
for x in log:
    print(x["file"], "|", x["old"], "->", x["new"], x.get("note", ""))
if apply:
    with open(E / "EN_ITEM_REFS_LOG.jsonl", "a", encoding="utf-8") as fh:
        for x in log:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
print(sum(1 for x in log if x["new"]), "rewritten" if apply else "to rewrite")
