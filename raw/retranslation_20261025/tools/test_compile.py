"""Compile a test document in build/test and summarize errors and undefined macros.
usage: python -I -X utf8 -B test_compile.py [name]   (default t)"""
import collections
import pathlib
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
D = pathlib.Path(__file__).resolve().parent.parent / "build" / "test"
name = sys.argv[1] if len(sys.argv) > 1 else "t"
r = subprocess.run(["pdflatex", "-interaction=nonstopmode", name + ".tex"], cwd=D, capture_output=True, text=True,
                   encoding="utf-8", errors="replace")
log = (D / (name + ".log")).read_text(encoding="utf-8", errors="replace")
errs = re.findall(r"^! (.*)", log, re.M)
print("rc", r.returncode, "| errors", len(errs))
for k, v in collections.Counter(errs).most_common(10):
    print("  ", v, k)
undef = re.findall(r"! Undefined control sequence\.\s*\n(?:<[^\n]*\n)*l\.\d+ [^\n]*?(\\[A-Za-z@]+)\s*\n", log)
print("undefined macros:", collections.Counter(undef).most_common(15))
envs = re.findall(r"Environment (\S+) undefined", log)
print("undefined environments:", collections.Counter(envs).most_common(10))
m = re.search(r"Output written on .*?\((\d+) pages", log)
print("pages", m.group(1) if m else None)
