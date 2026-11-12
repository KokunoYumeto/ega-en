"""Find paragraphs that print their own number by referring to the label placed right after them, e.g.
  \\emph{\\sref{IV.9.8.2}}  then  \\label{IV.9.8.2}
which prints the previous statement's number once the label takes the current counter. Reports per file.
usage: python -I -X utf8 -B self_refs.py SRC_DIR"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
PAT = re.compile(r"(\\noindent\s*)?(\\emph\{|\\textbf\{|\{\\bf\s*)?\\sref(?:\[[^\]]*\])?\{([^}]*)\}\}?\s*(?:\n\s*)?\\label\{\3\}")
per = collections.Counter()
examples = []
for f in sorted(pathlib.Path(sys.argv[1]).rglob("*.tex")):
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in PAT.finditer(t):
        per[f.relative_to(sys.argv[1]).as_posix()] += 1
        if len(examples) < 6:
            examples.append((f.name, t[max(0, m.start() - 60):m.end() + 40].replace("\n", " | ")))
print("total:", sum(per.values()))
for k, v in per.most_common():
    print("%4d %s" % (v, k))
for e in examples:
    print("--", e)
