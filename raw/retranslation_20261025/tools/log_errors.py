"""Show the first N occurrences (with context) of a TeX error message in build/src/EGA_EN.log.
usage: python -I -X utf8 -B log_errors.py "Missing \\endcsname" [N]"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
log = (pathlib.Path(__file__).resolve().parent.parent / "build" / "src" / "EGA_EN.log").read_text(encoding="utf-8", errors="replace")
needle = "! " + sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
pos, shown = 0, 0
while shown < n:
    k = log.find(needle, pos)
    if k < 0:
        break
    print(log[k:k + 500].replace("\n", " | "))
    print("-" * 60)
    pos, shown = k + 1, shown + 1
