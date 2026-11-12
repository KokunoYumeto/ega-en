"""Small follow-ups of the slips pass (5 Nov), and the blank lines around page markers that break a sentence into two
paragraphs (\\oldpage between blank lines, the text before not ending a sentence, the text after starting in lower case).
usage: python -I en_final_fixes.py [--apply]"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
E = pathlib.Path(__file__).parent
T = E / "ega-en" / "tex"
BS = chr(92)
apply = "--apply" in sys.argv
log = []


def edit(rel, old, new, count=1):
    p = T / rel
    t = p.read_text(encoding="utf-8")
    n = t.count(old)
    log.append({"file": rel, "old": old, "new": new, "found": n})
    if apply and n == count:
        p.write_text(t.replace(old, new), encoding="utf-8", newline="")


# 1. ega4-19, p. IV-4 188: (0_III, 10.1.3) as in the French
edit("source_aligned/ega4-19.tex", BS + "sref[0]{0.10.1.3}", BS + "sref[0" + BS + "textsubscript{" + BS + "mdseries III}]{0.10.1.3}")
# 2. ega4-12: the second \oldpage[IV-3]{179} (before 12.2.1) duplicates the first
p = T / "source_aligned" / "ega4-12.tex"
t = p.read_text(encoding="utf-8")
mk = BS + "oldpage[IV-3]{179}"
first = t.find(mk)
second = t.find(mk, first + 1)
log.append({"file": "source_aligned/ega4-12.tex", "old": "second " + mk, "new": "", "found": 2 if second > 0 else 1})
if apply and second > 0:
    end = second + len(mk)
    if t[end:end + 1] == "\n":
        end += 1
    t = t[:second] + t[end:]
    p.write_text(t, encoding="utf-8", newline="")
# 3. ega4-18: SGA 1 cited by its number in the IV bibliography, as the French "[43, exp. XII]"
edit("source_aligned/ega4-18.tex", BS + "cite[exp.~XII]{SGA1}", BS + "cite[exp.~XII]{IV-43}")

# 4. page markers wrapped in blank lines in the middle of a sentence
MK = re.compile(r"\n[ \t]*\n([ \t]*\\oldpage\[[^\]]*\]\{[^}]*\}[ \t]*)\n[ \t]*\n(?=[ \t]*[a-zà-ÿ(])")
joins = {}
for f in sorted(T.rglob("*.tex")):
    t = f.read_text(encoding="utf-8")
    out, last, n = [], 0, 0
    for m in MK.finditer(t):
        before = t[:m.start()].rstrip()
        if not before or before[-1] in ".:;}!?" or before.endswith(BS + "]") or before.endswith("$$"):
            continue
        out.append(t[last:m.start()])
        out.append("\n" + m.group(1) + "\n")
        last = m.end()
        n += 1
    if n:
        joins[str(f.relative_to(T))] = n
        if apply:
            out.append(t[last:])
            f.write_text("".join(out), encoding="utf-8", newline="")
for x in log:
    print(x)
print("markers joined into their sentence:", sum(joins.values()), joins)
