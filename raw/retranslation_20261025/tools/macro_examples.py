"""Print a few usage examples of selected macros/environments in the French chunks and our English sources.
usage: python -I -X utf8 -B macro_examples.py NAME [NAME ...]"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parent.parent
files = list((R / "fr").glob("*.tex")) + list((R / "ours").rglob("*.tex"))
texts = [p.read_text(encoding="utf-8", errors="replace") for p in files]
for name in sys.argv[1:]:
    if name.startswith("env:"):
        pat = re.compile(r"\\begin\{%s\}(\[[^\]]*\]|\{[^}]*\})?" % re.escape(name[4:]))
    else:
        pat = re.compile(r"\\%s(?![A-Za-z])(\[[^\]]*\])?(\{(?:[^{}]|\{[^{}]*\})*\})?(\{(?:[^{}]|\{[^{}]*\})*\})?" % re.escape(name))
    c = collections.Counter()
    for t in texts:
        c.update(m.group(0) for m in pat.finditer(t))
    print("%-12s %5d uses | %s" % (name, sum(c.values()), " ; ".join(k for k, _ in c.most_common(6))))
