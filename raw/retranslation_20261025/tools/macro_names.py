"""Names (only) of the macros and environments a TeX setup file defines, and how often each is used in a source tree.
usage: python -I -X utf8 -B macro_names.py SETUP_FILE [SETUP_FILE ...] -- TREE [TREE ...]"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
args = sys.argv[1:]
k = args.index("--")
setup_files, trees = args[:k], args[k + 1:]
DEF = re.compile(r"\\(?:(?:re)?newcommand|providecommand|DeclareMathOperator|DeclareRobustCommand)\*?\s*\{?\\([A-Za-z@]+)"
                 r"|\\(?:def|gdef|edef|let)\s*\\([A-Za-z@]+)"
                 r"|\\(?:newtheorem|newenvironment|renewenvironment)\*?\s*\{([A-Za-z*]+)\}")
names = collections.OrderedDict()
for s in setup_files:
    t = pathlib.Path(s).read_text(encoding="utf-8", errors="replace")
    for m in DEF.finditer(t):
        n = m.group(1) or m.group(2) or m.group(3)
        names.setdefault(n, "env" if m.group(3) else "cs")
uses = collections.Counter()
for tree in trees:
    for f in pathlib.Path(tree).rglob("*.tex"):
        if ".git" in f.parts or f.name in ("preamble-base.tex", "preamble.tex"):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        for n, kind in names.items():
            if kind == "env":
                uses[n] += t.count("\\begin{%s}" % n)
            else:
                uses[n] += len(re.findall(r"\\%s(?![A-Za-z@])" % re.escape(n), t))
for n, kind in names.items():
    print("%-6s %-24s %d" % (kind, n, uses[n]))
