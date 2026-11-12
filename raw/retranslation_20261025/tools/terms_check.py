"""Terminology and spelling conventions of GLOSSARY.md applied to the new English chunks: report, and with --fix
apply, the unambiguous ones. Only prose is touched: mathematics ($...$, \\[...\\], display environments), \\label,
\\ref/\\sref/\\hyperref keys and comments are left exactly as they are.
usage: python -I -X utf8 -B terms_check.py [--fix]"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parent.parent
RULES = [  # (pattern, replacement); replacement None = report only
    (r"\b([Ff])iber(s|ed|ing)?\b", lambda m: m.group(1) + "ibre" + {"s": "s", "ed": "d", "ing": "ing"}.get(m.group(2) or "", "")),
    (r"\b([Nn])eighborhood", r"\1eighbourhood"),
    (r"\b([Bb])ehavior", r"\1ehaviour"),
    (r"\b([Ff])actorisation", r"\1actorization"),
    (r"\bnoetherian\b", "Noetherian"),
    (r"\bartinian\b", "Artinian"),
    (r"\bquasi ?(compact|coherent|separated|finite|affine|projective|regular)\b", r"quasi-\1"),
    (r"\bsubprescheme", "sub-prescheme"),
    (r"\bsub-scheme", "subscheme"),
    (r"\bsubsheaf", "sub-sheaf"),
    (r"(\$-)Module(s?)\b", r"\1module\2"),
    (r"(\$-)Algebra(s?)\b", r"\1algebra\2"),
    (r"\bnonempty\b", "non-empty"),
    (r"\bnon-zero\b", "nonzero"),
    (r"\bCf\.", "cf."),
    (r"\bHausdorff\b", None),
    (r"\bfinite-type\b", None),
    (r"\bfinitely presented\b", None),
]
PROTECT = re.compile(r"(?s)(?<!\\)\$\$.+?(?<!\\)\$\$|(?<!\\)\$.+?(?<!\\)\$|\\\[.+?\\\]|\\begin\{(equation|align|gather|multline|displaymath|eqnarray)\*?\}.+?\\end\{\1\*?\}"
                     r"|\\(?:label|ref|sref|eqref|pageref)(?:\[[^\]]*\])?\{[^}]*\}|\\hyperref\[[^\]]*\]|(?m:(?<!\\)%.*$)")


def apply(text, fix):
    # split into protected and free segments; apply rules to free ones only
    out, pos, counts = [], 0, collections.Counter()
    for m in PROTECT.finditer(text):
        free = text[pos:m.start()]
        out.append(rules(free, counts, fix))
        out.append(m.group(0))
        pos = m.end()
    out.append(rules(text[pos:], counts, fix))
    return "".join(out), counts


def rules(seg, counts, fix):
    # "$-Module" needs the preceding "$", so the segment boundary is handled by checking the joined text below
    for pat, rep in RULES:
        n = len(re.findall(pat, seg))
        if n:
            counts[pat] += n
            if fix and rep is not None:
                seg = re.sub(pat, rep, seg)
    return seg


def fix_module_after_math(text, fix):
    # "$\mathcal{O}_X$-Module": the "$" belongs to the protected math, so treat "-Module" right after a math segment
    pat = re.compile(r"(?<=\$)-(Module|Algebra)(s?)\b")
    n = len(pat.findall(text))
    if fix:
        text = pat.sub(lambda m: "-" + m.group(1).lower() + m.group(2), text)
    return text, n


total = collections.Counter()
for f in sorted((R / "en").glob("*.en.tex")):
    t = f.read_text(encoding="utf-8")
    t2, counts = apply(t, "--fix" in sys.argv)
    t2, nmod = fix_module_after_math(t2, "--fix" in sys.argv)
    if nmod:
        counts["$-Module/Algebra (after math)"] += nmod
    total.update(counts)
    if counts:
        print("%-46s %s" % (f.name[:-7], dict(counts)))
    if "--fix" in sys.argv and t2 != t:
        f.write_text(t2, encoding="utf-8", newline="\n")
print("TOTAL:", dict(total))
