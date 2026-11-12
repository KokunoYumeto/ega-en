"""Check that every label records the number its key names: \\newlabel{IV.9.8.2}{{9.8.2}...} is right,
{{9.8.1}...} is wrong (the label took a neighbouring statement's number, so every reference to it prints the wrong
number). Keys are EGA numbers, so the key is the authority. usage: python -I -X utf8 -B label_numbers.py [N]"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
aux = (pathlib.Path(__file__).resolve().parent.parent / "build" / "src" / "EGA_EN.aux").read_text(encoding="utf-8", errors="replace")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
bad, ok, skipped = [], 0, 0
for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{(\{?)([^{}]*)\}?\}", aux):
    key, num = m.group(1), m.group(3)
    k = re.sub(r"^(?:sub)?section:", "", key)
    k = re.sub(r"\.eq$", "", k)
    mm = re.match(r"^(0|I|II|III|IV)\.(\d+(?:\.\d+)*)$", k)
    if not mm:
        skipped += 1
        continue
    want = mm.group(2)
    got = re.sub(r"\\S\s*|[()\s]|\\textbf|\\relax", "", num)
    if got == want or got == "\\S" + want:
        ok += 1
    else:
        bad.append((key, num))
print("labels checked: %d ok, %d wrong, %d not EGA-numbered" % (ok, len(bad), skipped))
shapes = collections.Counter(re.sub(r"\d+", "N", b[0]) for b in bad)
print("wrong, by key shape:", shapes.most_common(8))
for b in bad[:n]:
    print("  %-26s records %s" % b)
