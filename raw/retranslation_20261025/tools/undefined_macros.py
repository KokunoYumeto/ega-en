"""List the undefined control sequences in build/src/EGA_EN.log: the macro name (last token of the context line),
how often, and one example context. usage: python -I -X utf8 -B undefined_macros.py"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
log = (pathlib.Path(__file__).resolve().parent.parent / "build" / "src" / "EGA_EN.log").read_text(encoding="utf-8", errors="replace")
count, example = collections.Counter(), {}
for m in re.finditer(r"! Undefined control sequence\.\n((?:(?!l\.\d).*\n)*?)l\.(\d+) (.*)", log):
    # the undefined macro is the last control sequence on the first context line (an <argument> line, or l.NNN)
    first = m.group(1).split("\n")[0] if m.group(1).strip() else m.group(3)
    names = re.findall(r"\\[A-Za-z@]+", first)
    name = names[-1] if names else "?"
    count[name] += 1
    example.setdefault(name, "l.%s %s" % (m.group(2), m.group(3)[-90:]))
for name, n in count.most_common():
    print("%4d %-20s %s" % (n, name, example[name]))
