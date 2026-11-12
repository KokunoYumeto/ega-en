"""Undefined and multiply defined labels of the last build (build/src/EGA_EN.log and .aux), grouped by key shape,
with the defined labels that a missing key most likely meant (same key with or without a volume prefix, -fr suffix).
usage: python -I -X utf8 -B label_report.py [N examples]"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
B = pathlib.Path(__file__).resolve().parent.parent / "build" / "src"
log = (B / "EGA_EN.log").read_text(encoding="utf-8", errors="replace")
aux = (B / "EGA_EN.aux").read_text(encoding="utf-8", errors="replace")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
defined = set(re.findall(r"\\newlabel\{([^}]*)\}", aux))
undef = collections.Counter(re.findall(r"Reference `([^']*)' on page \S+ undefined", log))
multi = collections.Counter(re.findall(r"Label `([^']*)' multiply defined", log))


def shape(k):
    return re.sub(r"\d+", "N", k)


print("defined labels:", len(defined), "| undefined keys:", len(undef), "(", sum(undef.values()), "uses ) | multiply defined:", len(multi))
by_shape = collections.Counter()
for k, c in undef.items():
    by_shape[shape(k)] += c
print("\nundefined, by key shape:")
for s, c in by_shape.most_common(25):
    ex = [k for k in undef if shape(k) == s][:4]
    print("%5d  %-28s e.g. %s" % (c, s, ", ".join(ex)))


def guess(k):
    cands = [k + "-fr", re.sub(r"-fr$", "", k)]
    m = re.match(r"^(0|I|II|III|IV)\.(.*)$", k)
    if m:
        cands += [m.group(2)]
    for v in ("0", "I", "II", "III", "IV"):
        cands.append(v + "." + k)
    return [c for c in cands if c in defined and c != k]


print("\nundefined keys with a defined near-miss:")
hits = [(k, guess(k)) for k in undef if guess(k)]
print(len(hits), "keys;", ", ".join("%s->%s" % (k, g[0]) for k, g in hits[:n]))
print("\nmultiply defined, by key shape:")
ms = collections.Counter(shape(k) for k in multi)
for s, c in ms.most_common(12):
    print("%5d  %-28s e.g. %s" % (c, s, ", ".join([k for k in multi if shape(k) == s][:4])))
