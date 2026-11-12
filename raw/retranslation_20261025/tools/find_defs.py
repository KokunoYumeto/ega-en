"""Find definitions (\\newcommand, \\renewcommand, \\providecommand, \\def, \\DeclareMathOperator, \\let) of the given
macros under the given directories, and with --uses also a few example uses.
usage: python -I -X utf8 -B find_defs.py DIR [DIR ...] -- NAME [NAME ...] [--uses]"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
args = sys.argv[1:]
uses = "--uses" in args
args = [a for a in args if a != "--uses"]
k = args.index("--")
dirs, names = args[:k], args[k + 1:]
for name in names:
    pat_def = re.compile(r"\\(?:(?:re|provide|new)command\*?|DeclareMathOperator\*?|DeclareRobustCommand\*?)\s*\{?\\%s(?![A-Za-z])|\\(?:def|let|gdef)\s*\\%s(?![A-Za-z])" % (name, name))
    pat_use = re.compile(r"\\%s(?![A-Za-z])" % name)
    found, shown = 0, 0
    for d in dirs:
        for f in sorted(pathlib.Path(d).rglob("*.tex")) + sorted(pathlib.Path(d).rglob("*.sty")):
            t = f.read_text(encoding="utf-8", errors="replace")
            for m in pat_def.finditer(t):
                line = t[t.rfind("\n", 0, m.start()) + 1:t.find("\n", m.end())]
                print("DEF  %-8s %s: %s" % (name, f.name, line.strip()[:160]))
                found += 1
            if uses and shown < 3:
                for m in pat_use.finditer(t):
                    print("USE  %-8s %s: %s" % (name, f.name, t[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")))
                    shown += 1
                    if shown >= 3:
                        break
    if not found:
        print("DEF  %-8s (none found)" % name)
