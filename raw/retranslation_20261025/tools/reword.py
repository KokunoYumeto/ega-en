"""Find or replace a passage in the translation chunks, matching across line breaks (any run of whitespace in the
pattern matches any run of whitespace in the file).
  python -I -X utf8 -B reword.py find "PATTERN"            print matching file(s) and the passage with context
  python -I -X utf8 -B reword.py apply EDITS.json            apply [{"file": ..., "old": ..., "new": ...}, ...];
                                                              each old must match exactly once in its file"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
EN = pathlib.Path(__file__).resolve().parent.parent / "en"


def rx(s):
    return re.compile(r"\s+".join(re.escape(p) for p in s.split()))


if sys.argv[1] == "find":
    r = rx(sys.argv[2])
    for f in sorted(EN.glob("*.en.tex")):
        t = f.read_text(encoding="utf-8")
        for m in r.finditer(t):
            print("== %s" % f.name)
            print(t[max(0, m.start() - 300):m.end() + 300])
else:
    edits = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    for e in edits:
        f = EN / e["file"]
        t = f.read_text(encoding="utf-8")
        ms = list(rx(e["old"]).finditer(t))
        if len(ms) != 1:
            print("SKIP %s: %d matches for %r" % (e["file"], len(ms), e["old"][:60]))
            continue
        m = ms[0]
        t = t[:m.start()] + e["new"] + t[m.end():]
        f.write_text(t, encoding="utf-8", newline="\n")
        print("ok   %s: %r" % (e["file"], e["old"][:60]))
