"""Structural check of one translated chunk against its French source: same labels, same references, same
environments, same \\oldpage markers and footnote count, the same mathematics (inline and display, with \\text{...}
contents ignored), and a plausible length ratio. usage: python -I -X utf8 -B check_chunk.py CHUNK  (name without .fr.tex)"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
name = sys.argv[1]
fr = (ROOT / "fr" / (name + ".fr.tex")).read_text(encoding="utf-8")
en = (ROOT / "en" / (name + ".en.tex")).read_text(encoding="utf-8")


def strip_comments(t):
    return re.sub(r"(?m)(?<!\\)%.*$", "", t)


def labels(t):
    return collections.Counter(re.findall(r"\\label\{([^}]*)\}", t))


def refs(t):
    # keys only: \hyperref[key]{shown text} is compared by its key, since the shown text is translated
    keys = re.findall(r"\\(?:sref|ref|eqref)(?:\[[^\]]*\])?\{([^}]*)\}", t)
    keys += re.findall(r"\\hyperref\[([^\]]*)\]", t)
    return collections.Counter(keys)


def envs(t):
    return collections.Counter(re.findall(r"\\(begin|end)\{([^}]*)\}", t))


def oldpages(t):
    return re.findall(r"\\oldpage(?:\[[^\]]*\])?\{([^}]*)\}", t)


def math(t):
    t = strip_comments(t)
    t = re.sub(r"\\text(?:rm|it|bf)?\{(?:[^{}]|\{[^{}]*\})*\}", "", t)
    t = re.sub(r"\\(?:mbox|hbox)\{(?:[^{}]|\{[^{}]*\})*\}", "", t)
    segs = re.findall(r"(?<!\\)\$(.+?)(?<!\\)\$", t, re.S)
    segs += re.findall(r"\\\[(.+?)\\\]", t, re.S)
    for env in ("equation", "align", "gather", "multline", "eqnarray", "displaymath"):
        segs += re.findall(r"\\begin\{%s\*?\}(.+?)\\end\{%s\*?\}" % (env, env), t, re.S)
    return collections.Counter(re.sub(r"\s+", "", s) for s in segs)


def letters(t):
    t = strip_comments(t)
    t = re.sub(r"(?<!\\)\$.+?(?<!\\)\$", " ", t, flags=re.S)
    t = re.sub(r"\\[A-Za-z]+\*?", " ", t)
    return len(re.findall(r"[^\W\d_]", t))


problems = []
for what, f in (("labels", labels), ("references", refs), ("environments", envs), ("math", math)):
    a, b = f(fr), f(en)
    if a != b:
        only_fr = list((a - b).elements())[:6]
        only_en = list((b - a).elements())[:6]
        problems.append("%s differ: only in French %s | only in English %s" % (what, only_fr, only_en))
if oldpages(fr) != oldpages(en):
    problems.append("oldpage markers differ: %s vs %s" % (oldpages(fr)[:8], oldpages(en)[:8]))
nf, ne = len(re.findall(r"\\footnote", fr)), len(re.findall(r"\\footnote", en))
if nf != ne:
    problems.append("footnotes: French %d, English %d" % (nf, ne))
lf, le = letters(fr), letters(en)
ratio = le / lf if lf else 1.0
if not 0.75 <= ratio <= 1.30:
    problems.append("length ratio English/French letters %.2f (expected 0.75-1.30)" % ratio)
print("OK" if not problems else "PROBLEMS:\n- " + "\n- ".join(problems), "| ratio %.2f" % ratio)
