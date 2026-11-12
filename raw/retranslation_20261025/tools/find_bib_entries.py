"""List EGA bibliography entries found in a source tree: \\bibitem[n]{key} items and plain-text entries "[n] A. Author"
at the start of a line, with file and the first words. usage: python -I -X utf8 -B find_bib_entries.py DIR [DIR ...]"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ITEM = re.compile(r"\\bibitem(?:\[([^\]]*)\])?\{([^}]*)\}\s*([^\n]{0,70})")
PLAIN = re.compile(r"(?m)^\s*\[(\d{1,2})\]\s+([A-Z][^\n]{0,70})")
for d in sys.argv[1:]:
    for f in sorted(pathlib.Path(d).rglob("*.tex")):
        if any(s in f.name for s in ("EGA_English", "EGA4_reference", "_EN.tex", "Standalone", "Reader")):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        rows = [("bibitem", m.group(1) or "", m.group(2), m.group(3)) for m in ITEM.finditer(t)]
        rows += [("plain", m.group(1), "", m.group(2)) for m in PLAIN.finditer(t)]
        if rows:
            print("== %s (%d)" % (f.relative_to(d).as_posix(), len(rows)))
            for r in rows[:60]:
                print("   %-7s [%s] {%s} %s" % r)
