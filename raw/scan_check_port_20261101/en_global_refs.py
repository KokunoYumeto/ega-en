"""English EGA: set references the way EGA prints them (and the checked French edition now has them), in one pass.

EGA prints the chapter number of a reference in bold, (0, 2.1.1) and (I, 1.3.9) with bold 0 and I, the subscript of
0_I in ordinary weight, and sets references upright inside the italic statements. The French scan check corrected
these one by one (about 2,300 bold numerals and 2,600 upright parentheses); in the English they are made by rule:

  R1  ega-preamble.tex: \\sref prints its volume argument in bold and the whole reference upright; \\eref upright.
  R2  \\sref optional arguments with a subscript: 0\\textsubscript{I} -> 0\\textsubscript{\\mdseries I} (the subscript stays
      in ordinary weight inside the bold), $0_{\\mathrm{I}}$ -> $\\mathbf{0}_{\\mathrm{I}}$.
  R3  \\hyperref display texts that start with a chapter number: {0, ...} -> {\\textbf{0}, ...} (also I, II, III, IV,
      0\\textsubscript{..}, $0_{..}$, $\\mathbf{0_I}$).
  R4  plain-text references (0, 1.2.3) / (I, 1.2.3) outside commands and comments: the number in bold.
  R5  inside the italic statements (proposition, theorem, corollary, lemma, namedtheorem, namedlemma): a parenthesis
      that holds only references, e.g. (\\hyperref[..]{\\textbf{0}, 2.1.1}) or (\\textbf{I}, 2.3.1 and 2.3.2), is wrapped
      in \\textup{...}.

usage: python -I en_global_refs.py [--apply]   (log: EN_GLOBAL_REFS_LOG.jsonl)
"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BS = chr(92)
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
EN = E / "ega-en" / "tex"
apply = "--apply" in sys.argv
NUM = r"(?:0|I|II|III|IV)"
log = []
stats = collections.Counter()


def note(f, rule, old, new, pos, t):
    log.append(dict(file=str(f.relative_to(EN)).replace(BS, "/"), rule=rule, line=t.count("\n", 0, pos) + 1,
                    old=old, new=new))
    stats[rule] += 1


def protect_comments(t):
    """Spans of TeX comments (from an unescaped % to the end of the line)."""
    spans = []
    for m in re.finditer(r"(?<!\\)%[^\n]*", t):
        spans.append((m.start(), m.end()))
    return spans


def in_spans(k, spans):
    return any(a <= k < b for a, b in spans)


MATHENV = re.compile(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|displaymath|math|xy|tikzcd|"
                     r"array|CD)\}.*?\\end\{\1\}", re.S)


def math_spans(t):
    """Spans of inline and display mathematics: $...$, $$...$$, \\(...\\), \\[...\\] and the math environments."""
    spans = [(m.start(), m.end()) for m in MATHENV.finditer(t)]
    spans += [(m.start(), m.end()) for m in re.finditer(r"\\\[.*?\\\]", t, re.S)]
    spans += [(m.start(), m.end()) for m in re.finditer(r"\\\(.*?\\\)", t, re.S)]
    i, n, start, mode = 0, len(t), None, 0
    while i < n:
        ch = t[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "%":
            j = t.find("\n", i)
            i = n if j < 0 else j
            continue
        if ch == "$":
            dbl = t.startswith("$$", i)
            if mode == 0:
                mode, start = (2 if dbl else 1), i
            elif (mode == 2 and dbl) or (mode == 1 and not dbl):
                spans.append((start, i + (2 if dbl else 1)))
                mode = 0
            i += 2 if dbl else 1
            continue
        i += 1
    return spans


# --- R1 preamble ------------------------------------------------------------------------------------------------
PRE = EN / "ega-preamble.tex"
pre = PRE.read_text(encoding="utf-8")
old_sref = (BS + r"newcommand{" + BS + r"sref}[2][]{" + BS + r"hyperref[#2]{(" + BS + r"if" + BS + r"relax" + BS +
            r"detokenize{#1}" + BS + r"relax" + BS + r"else#1,~" + BS + r"fi" + BS + r"ref*{#2})}}")
new_sref = (BS + r"newcommand{" + BS + r"sref}[2][]{" + BS + r"hyperref[#2]{" + BS + r"textup{(" + BS + r"if" + BS +
            r"relax" + BS + r"detokenize{#1}" + BS + r"relax" + BS + r"else" + BS + r"textbf{#1},~" + BS + r"fi" + BS +
            r"ref*{#2})}}}")
old_eref = BS + r"newcommand{" + BS + r"eref}[1]{" + BS + r"hyperref[#1]{(" + BS + r"ref*{#1})}}"
new_eref = BS + r"newcommand{" + BS + r"eref}[1]{" + BS + r"hyperref[#1]{" + BS + r"textup{(" + BS + r"ref*{#1})}}}"
old_comment = ("% when the target is in another chapter, e.g. " + BS + "sref[0]{0.6.7.4} gives (0, 6.7.4).")
new_comment = ("% when the target is in another chapter, e.g. " + BS + "sref[0]{0.6.7.4} gives (0, 6.7.4). As in EGA, the\n"
               "% volume number is bold (a subscript in ordinary weight: " + BS + "sref[0" + BS + "textsubscript{" + BS +
               "mdseries I}]{...})\n% and the reference is upright, also inside the italic statements.")
if old_sref in pre:
    for o, n in ((old_sref, new_sref), (old_eref, new_eref), (old_comment, new_comment)):
        assert pre.count(o) == 1, o
        note(PRE, "R1", o, n, pre.find(o), pre)
        pre = pre.replace(o, n)
else:
    assert new_sref in pre, "unexpected \\sref definition"

files = [f for f in sorted(EN.rglob("*.tex")) if f.name != "ega-preamble.tex"]
texts = {f: f.read_text(encoding="utf-8") for f in files}

# --- R2 \sref optional arguments -----------------------------------------------------------------------------------
R2 = re.compile(re.escape(BS) + r"sref\[([^\]]*)\]")


def r2_new(arg):
    m = re.fullmatch(r"0" + re.escape(BS) + r"textsubscript\{([IVX]+)\}", arg)
    if m:
        return "0" + BS + "textsubscript{" + BS + "mdseries " + m.group(1) + "}"
    m = re.fullmatch(r"\$0_\{" + re.escape(BS) + r"mathrm\{?([IVX]+)\}?\}\$", arg)
    if m:
        return "$" + BS + "mathbf{0}_{" + BS + "mathrm{" + m.group(1) + "}}$"
    if arg == "0I":
        return "0" + BS + "textsubscript{" + BS + "mdseries I}"
    return None


# --- R3 hyperref display heads -------------------------------------------------------------------------------------
R3 = re.compile(re.escape(BS) + r"hyperref\[[^\]]*\]\{(" + NUM + r"|0" + re.escape(BS) + r"textsubscript\{[IVX]+\}|\$0_\{"
                + re.escape(BS) + r"mathrm\{?\s?[IVX]+\}?\}\$|\$0_\{?[IVX]+\}?\$|\$" + re.escape(BS) +
                r"mathbf\{0_\{?[IVX]+\}?\}\$)(,)")


def r3_new(head):
    if re.fullmatch(NUM, head):
        return BS + "textbf{" + head + "}"
    m = re.fullmatch(r"0" + re.escape(BS) + r"textsubscript\{([IVX]+)\}", head)
    if m:
        return BS + "textbf{0}" + BS + "textsubscript{" + m.group(1) + "}"
    m = re.search(r"([IVX]+)", head[2:] if head.startswith("$0") else head)
    return "$" + BS + "mathbf{0}_{" + BS + "mathrm{" + m.group(1) + "}}$"


# --- R4 plain-text references ---------------------------------------------------------------------------------------
R4 = re.compile(r"\((" + NUM + r")(, ?\d+(?:\.\d+)*)")

for f in files:
    t = texts[f]
    out, pos = [], 0
    edits = []
    for m in R2.finditer(t):
        n = r2_new(m.group(1))
        if n:
            edits.append((m.start(1), m.end(1), m.group(1), n, "R2"))
    for m in R3.finditer(t):
        edits.append((m.start(1), m.end(1), m.group(1), r3_new(m.group(1)), "R3"))
    com = protect_comments(t)
    mth = math_spans(t)
    for m in R4.finditer(t):
        if in_spans(m.start(), com) or in_spans(m.start(), mth):
            continue
        # not inside a command argument such as \label{..} or \hyperref[..]
        before = t[max(0, m.start() - 40):m.start()]
        if re.search(r"\\(?:label|ref|hyperref|sref|egalabel)\[?[^\]}\s]*$", before):
            continue
        edits.append((m.start(1), m.end(1), m.group(1), BS + "textbf{" + m.group(1) + "}", "R4"))
    edits.sort()
    for a, b, o, n, rule in edits:
        assert a >= pos
        out.append(t[pos:a])
        out.append(n)
        pos = b
        note(f, rule, o, n, a, t)
    out.append(t[pos:])
    texts[f] = "".join(out)

# --- R5 upright parenthesised references inside the italic statements ------------------------------------------------
ITAL = ("proposition", "theorem", "corollary", "lemma", "namedtheorem", "namedlemma")
ENV = re.compile(re.escape(BS) + r"(begin|end)\{(" + "|".join(ITAL) + r")\}")
HREF = re.escape(BS) + r"hyperref\[[^\]]*\]\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}"
BOLDNUM = re.escape(BS) + r"textbf\{" + NUM + r"\}|\$" + re.escape(BS) + r"mathbf\{0\}_\{" + re.escape(BS) + r"mathrm\{[IVX]+\}\}\$"
REFTOK = r"(?:" + HREF + r"|" + BOLDNUM + r"|\d+(?:\.\d+)*|[,;~ \n]|and|or|resp\.)"
PAREN = re.compile(r"(?<![\w{}\\])\((" + REFTOK + r"+)\)")


def italic_spans(t):
    spans, stack = [], []
    for m in ENV.finditer(t):
        if m.group(1) == "begin":
            stack.append(m.end())
        elif stack:
            spans.append((stack.pop(), m.start()))
    return spans


for f in files:
    t = texts[f]
    spans = italic_spans(t)
    if not spans:
        continue
    com = protect_comments(t)
    mth = math_spans(t)
    edits = []
    for m in PAREN.finditer(t):
        inner = m.group(1)
        if not (re.search(HREF, inner) or re.search(BOLDNUM, inner)) or not re.search(r"\d", inner):
            continue
        if not in_spans(m.start(), spans) or in_spans(m.start(), com) or in_spans(m.start(), mth):
            continue
        if t[max(0, m.start() - 8):m.start()].endswith(BS + "textup{"):
            continue
        edits.append((m.start(), m.end(), m.group(0), BS + "textup{" + m.group(0) + "}"))
    out, pos = [], 0
    for a, b, o, n in edits:
        out.append(t[pos:a])
        out.append(n)
        pos = b
        note(f, "R5", o, n, a, t)
    out.append(t[pos:])
    texts[f] = "".join(out)

print(("applied" if apply else "dry run"), dict(stats))
ex = collections.defaultdict(list)
for x in log:
    if len(ex[x["rule"]]) < 4:
        ex[x["rule"]].append((x["file"], x["line"], x["old"][:70], x["new"][:80]))
for k, v in ex.items():
    print(k)
    for e in v:
        print("   ", e)
if apply:
    PRE.write_text(pre, encoding="utf-8", newline="")
    for f in files:
        if texts[f] != f.read_text(encoding="utf-8"):
            f.write_text(texts[f], encoding="utf-8", newline="")
    with open(E / "EN_GLOBAL_REFS_LOG.jsonl", "a", encoding="utf-8") as fh:
        for x in log:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
