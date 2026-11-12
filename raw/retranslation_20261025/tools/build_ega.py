"""Assemble the English EGA from the new translations (en/*.en.tex) and our own earlier English (ours/), in the
cumulative order Introduction, Chapter 0 §§1-23, Chapters I-IV, and compile it.
New chunks are joined into section files under build/src/ (labels lose the "-fr" suffix of the French sources);
ours/ is copied there unchanged. Missing new sections are reported and replaced by a placeholder line.
usage: python -I -X utf8 -B build_ega.py [--nocompile]"""
import collections
import json
import pathlib
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parent.parent
EN, OURS, B = R / "en", R / "ours", R / "build"
SRC = B / "src"


def chunk_target(chunk):
    """New-translation chunk name -> section file (relative to src) it belongs to."""
    m = re.match(r"ega0-1-7__0\.(\d+)-fr", chunk)
    if m:
        return "ega0/ega0-%s.tex" % m.group(1)
    m = re.match(r"ega3-1-file__0\.(\d+)-fr", chunk)
    if m:
        return "ega0/ega0-%s.tex" % m.group(1)
    m = re.match(r"ega3-1-file__III\.(\d+)-fr", chunk)
    if m:
        return "ega3/ega3-%s.tex" % m.group(1)
    m = re.match(r"ega1-(\d+)__I\.\d+-fr", chunk)
    if m:
        return "ega1/ega1-%s.tex" % m.group(1)
    m = re.match(r"ega2-1-8__II\.(\d+)-fr", chunk)
    if m:
        return "ega2/ega2-%s.tex" % m.group(1)
    fixed = {"ega1-intro__ega1-intro": "ega1/ega1-intro.tex", "ega2-errata__ega2-errata": "ega2/ega2-errata.tex",
             "ega0-14__ega0-14": "ega0/ega0-14.tex"}
    if chunk in fixed:
        return fixed[chunk]
    if chunk.startswith("ega4-16__"):
        return "ega4/ega4-16.tex"
    if chunk.startswith("ega4-17__"):
        return "ega4/ega4-17.tex"
    if chunk.startswith("ega4-20__"):
        return "ega4/ega4-20.tex"
    if chunk.startswith("ega4-1__sec"):
        return "ega4/ega4-1-backmatter.tex"
    if chunk.startswith("ega4-1__"):
        return "ega4/ega4-1.tex"
    return None


def normalize(t):
    t = re.sub(r"(\\(?:label|ref|sref|eqref|pageref|autoref)(?:\[[^\]]*\])?\{[^}]*?)-fr\}", r"\1}", t)
    t = re.sub(r"(\\hyperref\[[^\]]*?)-fr\]", r"\1]", t)
    return t


NAMED = re.compile(r"(\\begin\{(?:proposition|theorem|corollary|lemma|definition|remarks?|examples?|notation|scholium)\})"
                   r"\[(\d+(?:\.\d+)*)\)?\s+\(([^\]]*?)\)?\]")


def split_names():
    """A statement number followed by a name, [19.6.1 (Cohen)], becomes [19.6.1][Cohen]."""
    n = 0
    for f in SRC.rglob("*.tex"):
        t = f.read_text(encoding="utf-8", errors="replace")
        t2, k = NAMED.subn(r"\1[\2][\3]", t)
        if k:
            f.write_text(t2, encoding="utf-8", newline="\n")
            n += k
    return n


EXTRA = R / "ours_extra"  # our own English files written for this edition (EGA I and II bibliographies)
# (file, plain entries "[n]" in it that get a citation key with this prefix)
PLAIN_BIB = [("ega3/ega3-5.tex", "III"), ("ega4/ega4-1-backmatter.tex", "IV"),
             ("source_aligned/ega4-15-backmatter.tex", "IV")]
FIXUPS = [  # (file, old, new): bibliographic titles stay in their original language
    ("source_aligned/ega4-15-backmatter.tex", r"\emph{Local Fields}", r"\emph{Corps locaux}"),
    ("source_aligned/ega4-15-backmatter.tex", r"\emph{Proalgebraic Groups}", r"\emph{Groupes proalgébriques}"),
]


def bibliography_keys():
    """Citation keys for every EGA bibliography entry: plain entries get \\egabib, the IV-4 list gets the keys the
    text cites (IV-41 ...), without the two entries that EGA I and IV-1 already define."""
    n = 0
    for rel, vol in PLAIN_BIB:
        f = SRC / rel
        t = f.read_text(encoding="utf-8", errors="replace")
        t2, k = re.subn(r"(?m)^(\s*)\[(\d{1,2})\](\s+[A-Z])", lambda m: "%s\\egabib{%s-%s}{%s}[%s]%s" % (
            m.group(1), vol, m.group(2), m.group(2), m.group(2), m.group(3)), t)
        f.write_text(t2, encoding="utf-8", newline="\n")
        n += k
    f = SRC / "source_aligned" / "ega4-backmatter-bibliography.tex"
    t = f.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"\\bibitem\[(?:32|I-4)\]\{[^}]*\}.*?(?=\\bibitem|\\end\{thebibliography\})", "", t, flags=re.S)
    t = t.replace("{IV4-print-SGA1}", "{SGA1}")
    t = re.sub(r"\{IV4-print-(IV-\d+)\}", r"{\1}", t)
    t = re.sub(r"\\begin\{quote\}\\footnotesize\s*Entries \[32\].*?\\end\{quote\}\s*", "", t, flags=re.S)
    f.write_text(t, encoding="utf-8", newline="\n")
    # Chapter IV opens with its own title page; the running head is the edition's
    f = SRC / "ega4" / "ega4-1.tex"
    t = f.read_text(encoding="utf-8", errors="replace")
    f.write_text(t.replace("\\markboth{CHAPTER IV}{CHAPTER IV}", "", 1), encoding="utf-8", newline="\n")
    for rel, old, new in FIXUPS:
        f = SRC / rel
        t = f.read_text(encoding="utf-8", errors="replace")
        if old in t:
            f.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
            n += 1
    return n


DISPLAY = re.compile(r"(?<!\\)\\\[(.*?)(?<!\\)\\\]", re.S)  # \[ ... \], not the line break \\[2pt]


def tag_display_labels():
    """A labelled display without a tag, \\[ ... \\label{I.10.9.2.1} ... \\], prints no number although the label
    names one: give it \\tag{10.9.2.1}, the number the key names."""
    n = 0
    for f in SRC.rglob("*.tex"):
        t = f.read_text(encoding="utf-8", errors="replace")

        def fix(m):
            nonlocal n
            body = m.group(1)
            lab = re.search(r"\\label\{((?:0|I|II|III|IV)\.(\d+(?:\.\d+)+))\}", body)
            if not lab or "\\tag" in body or "\\notag" in body:
                return m.group(0)
            n += 1
            # tag and label go at the top level of the display (a tag inside aligned or xymatrix is not allowed);
            # no blank line may remain inside the display
            rest = re.sub(r"\s*" + re.escape(lab.group(0)) + r"\s*", " ", body, count=1)
            rest = re.sub(r"\n\s*\n", "\n", rest).rstrip()
            return "\\[" + rest + "\n\\tag{%s}%s\n\\]" % (lab.group(2), lab.group(0))

        t2 = DISPLAY.sub(fix, t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8", newline="\n")
    return n


def fix_label_numbers():
    """After a pass: every label whose recorded number differs from the EGA number its key names is rewritten to
    record that number (\\egalabel), so that references to it print the right number."""
    aux = (SRC / "EGA_EN.aux").read_text(encoding="utf-8", errors="replace")
    want = {}
    for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{\{?([^{}]*)\}?\}", aux):
        key, got = m.group(1), m.group(2)
        k = re.match(r"^(0|I|II|III|IV)\.(\d+(?:\.\d+)*)(\.eq)?$", key)
        if k and re.sub(r"[()\s]", "", got) != k.group(2):
            want[key] = k.group(2)
    if not want:
        return 0
    n = 0
    for f in SRC.rglob("*.tex"):
        t = f.read_text(encoding="utf-8", errors="replace")
        t2 = re.sub(r"\\label\{([^}]*)\}", lambda m: ("\\egalabel{%s}{%s}" % (m.group(1), want[m.group(1)])
                                                      if m.group(1) in want else m.group(0)), t)
        if t2 != t:
            n += sum(1 for k in want if "\\label{%s}" % k in t)
            f.write_text(t2, encoding="utf-8", newline="\n")
    return n


ORDER = (["ega1/ega1-intro.tex"] + ["ega0/ega0-%d.tex" % n for n in range(1, 24)] +
         ["ega1/ega1-%d.tex" % n for n in range(1, 11)] + ["ega1/ega1-bibliography.tex"] +
         ["ega2/ega2-%d.tex" % n for n in range(1, 9)] + ["ega2/ega2-bibliography-en.tex"] +
         ["ega2/ega2-errata.tex"] + ["ega3/ega3-%d.tex" % n for n in range(1, 7)] +
         ["ega3/ega3-7.tex"] +  # inputs ega3-7-2 ... ega3-7-9 itself (and ega3-7-7 inputs ega3-7-7-rest)
         ["ega4/ega4-1.tex", "ega4/ega4-1-backmatter.tex", "ega4-2.source_aligned_r1.tex", "ega4-3.source_aligned_r1.tex",
          "ega4-4.source_aligned_r1.tex", "ega4-5.source_aligned_r1.tex"] +
         ["source_aligned/ega4-%d.tex" % n for n in range(6, 16)] +
         ["ega4/ega4-16.tex", "ega4/ega4-17.tex", "source_aligned/ega4-18.tex", "source_aligned/ega4-19.tex",
          "ega4/ega4-20.tex", "source_aligned/ega4-21.tex"] +
         ["source_aligned/ega4-backmatter-%s.tex" % s for s in ("bibliography", "notation", "terminology", "contents")] +
         ["source_aligned/ega4-errata-addenda-list3.tex"])
CHAPTERS = {"ega0/ega0-1.tex": ("0", "Preliminaries"), "ega1/ega1-1.tex": ("I", "The language of schemes"),
            "ega2/ega2-1.tex": ("II", "Elementary global study of some classes of morphisms"),
            "ega3/ega3-1.tex": ("III", "Cohomological study of coherent sheaves"),
            "ega4/ega4-1.tex": ("IV", "Local study of schemes and morphisms of schemes")}
EDITION = r"""\begin{titlepage}\centering
{\Large Alexandre Grothendieck}\par\smallskip
{\large with the collaboration of Jean Dieudonné}\par\vspace{2em}
{\Huge Elements of Algebraic Geometry}\par\smallskip
{\large (\'El\'ements de g\'eom\'etrie alg\'ebrique)}\par\vspace{1.5em}
{\large Chapters 0--IV}\par\vfill
{\normalsize English translation}\par
\end{titlepage}
\noindent Translated from the French transcription of the original publication in the \emph{Publications
math\'ematiques de l'IH\'ES} 4, 8, 11, 17, 20, 24, 28 and 32 (1960--1967),
\url{https://github.com/KokunoYumeto/ega-fr}. The translation is AI-translated: by Claude Opus 5.5 (Anthropic) for
the Introduction, Chapter~0, \S\S1--11 and 14, Chapter~I, Chapter~II with its errata, Chapter~III, \S\S1 and 3,
and Chapter~IV: its introduction, \S\S1, 16, 17 and 20, and the bibliography and indexes that close its first part;
by OpenAI Codex models (GPT-6 Astra, GPT-5.6 Sol) for the other sections.

The rights in the original work remain with its rights holders. Anything in this edition that the publisher holds
rights to is dedicated to the public domain under CC0~1.0. Rights holders who object to the availability of this
material can open an issue at \url{https://github.com/KokunoYumeto/ega-en/issues}; the material will be taken down.
\clearpage
"""


LINK = re.compile(r"\\hyperlink\{ega4\.c04\.([a-z]+)\.([0-9A-Za-z-]+)\}")


def relink():
    """Our earlier EGA IV sources link with \\hyperlink{ega4.c04.<kind>.<n-n-n>}; point those links at the labels
    (IV.n.n.n) instead, and print the shown text unlinked where no label matches."""
    labels = set()
    files = sorted(SRC.rglob("*.tex"))
    for f in files:
        labels.update(re.findall(r"\\label\{([^}]*)\}", f.read_text(encoding="utf-8", errors="replace")))

    def target(m):
        kind, parts = m.group(1), m.group(2).split("-")
        while parts:
            key = "IV." + ".".join(parts)
            for cand in ([key + ".eq"] if kind == "eq" else []) + [key, "subsection:" + key, "section:" + key]:
                if cand in labels:
                    return "\\hyperref[%s]" % cand
            parts = parts[:-1]
        return "\\unlinked"

    changed = 0
    for f in files:
        t = f.read_text(encoding="utf-8", errors="replace")
        if "\\hyperlink{ega4.c04." in t:
            t2 = LINK.sub(target, t)
            f.write_text(t2, encoding="utf-8", newline="\n")
            changed += 1
    return changed


STMT = re.compile(r"\\begin\{(?:env|proposition|theorem|corollary|lemma|definition|remarks?|examples?|notation|scholium)\}"
                  r"\[(\d+(?:\.\d+)+)\]")
TAG = re.compile(r"\\tag\{(\d+(?:\.\d+)+)\}")
REFCMD = re.compile(r"\\(sref|eref|eqref|ref\*?)(\[[^\]]*\])?\{([^}]*)\}")


def volume(rel):
    """Volume prefix of the label keys in a source file (relative path under src)."""
    for prefix, vol in (("ega0/", "0"), ("ega1/", "I"), ("ega2/", "II"), ("ega3/", "III")):
        if rel.startswith(prefix):
            return vol
    if rel.startswith(("ega4", "source_aligned/", "components/")):
        return "IV"
    return None


def all_labels(files):
    labels = set()
    for f in files:
        labels.update(re.findall(r"\\label\{([^}]*)\}", f.read_text(encoding="utf-8", errors="replace")))
    return labels


def autolabel():
    """Some numbered paragraphs and formulas of the French transcription carry a number but no \\label; give them
    the label their number implies (e.g. (4.3.3) in Chapter 0 gets 0.4.3.3) when no label of that name exists."""
    files = [f for f in sorted(SRC.rglob("*.tex")) if "errata" not in f.name and "backmatter" not in f.name]
    labels = all_labels(SRC.rglob("*.tex"))
    added = 0
    for f in files:
        rel = f.relative_to(SRC).as_posix()
        vol = volume(rel)
        if vol is None:
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        out, pos = [], 0
        marks = sorted([(m.end(), m.group(1)) for m in STMT.finditer(t)] + [(m.end(), m.group(1)) for m in TAG.finditer(t)])
        for end, num in marks:
            # the paragraph's own label comes before its first display or tag; a formula's label does not count
            follow = re.split(r"\n\s*\n|\\begin\{|\\end\{|\\item\b|\\\[|\\tag\{|\$\$", t[end:end + 600], maxsplit=1)[0]
            key = "%s.%s" % (vol, num)
            if "\\label{" in follow or key in labels:
                continue
            out.append(t[pos:end])
            out.append("\\label{%s}" % key)
            pos = end
            labels.add(key)
            added += 1
        if out:
            out.append(t[pos:])
            f.write_text("".join(out), encoding="utf-8", newline="\n")
    return added


def display(key):
    """Printed form of a reference whose label is not in this edition: the number its key gives."""
    k = re.sub(r"^(?:sub)?section:", "", key)
    m = re.match(r"^(0|I|II|III|IV)\.Err\.(.+)$", k)
    if m:
        return "Err\\textsubscript{%s}, %s" % (m.group(1), m.group(2)), True
    k = re.sub(r"^(?:0|I|II|III|IV|[A-Z])\.", "", k)
    parts = k.split(".")
    i = 0
    while i < len(parts) and not parts[i].isdigit():
        i += 1
    head, num = parts[:i], ".".join(parts[i:])
    return ", ".join(head + ([num] if num else [])), False


def resolve_refs():
    """References to keys no label defines: use the section or subsection label of that number when there is one,
    and otherwise print the number given by the key, unlinked."""
    files = sorted(SRC.rglob("*.tex"))
    labels = all_labels(files)
    stats, unresolved = collections.Counter(), collections.Counter()

    def fix(m):
        cmd, opt, key = m.group(1), m.group(2) or "", m.group(3)
        if key in labels or "#" in key:
            return m.group(0)
        for alt in ("subsection:" + key, "section:" + key):
            if alt in labels:
                stats["to section label"] += 1
                return "\\%s%s{%s}" % (cmd, opt, alt)
        text, is_err = display(key)
        stats["printed unlinked"] += 1
        unresolved[key] += 1
        if cmd == "sref":
            o = opt[1:-1] if opt and not is_err else ""
            return "(%s%s)" % (o + ",~" if o else "", text)
        if cmd in ("eref", "eqref"):
            return "(%s)" % text
        return text

    def fix_link(m):
        key = m.group(1)
        if key in labels or "#" in key:
            return m.group(0)
        for alt in ("subsection:" + key, "section:" + key):
            if alt in labels:
                return "\\hyperref[%s]" % alt
        stats["link printed unlinked"] += 1
        unresolved[key] += 1
        return "\\unlinked"

    for f in files:
        if f.name in ("ega-preamble.tex",) or f.name.startswith("EGA4_reference_v2"):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        t2 = REFCMD.sub(fix, t)
        t2 = re.sub(r"\\hyperref\[([^\]]*)\]", fix_link, t2)
        if t2 != t:
            f.write_text(t2, encoding="utf-8", newline="\n")
    (B / "unresolved_refs.txt").write_text("\n".join("%d %s" % (c, k) for k, c in unresolved.most_common()),
                                           encoding="utf-8", newline="\n")
    return dict(stats)


def section_number(rel):
    m = re.search(r"ega[0-4]-(\d+)(?:\.source_aligned_r1)?\.tex$", rel)
    return int(m.group(1)) if m else None


def build():
    if SRC.exists():
        shutil.rmtree(SRC)
    shutil.copytree(OURS, SRC)
    shutil.copytree(EXTRA, SRC, dirs_exist_ok=True)
    shutil.copy2(B / "ega-preamble.tex", SRC / "ega-preamble.tex")
    manifest = [m["chunk"] for m in json.loads((R / "MANIFEST.json").read_text(encoding="utf-8")) if m["bytes"] > 200]
    parts, missing_chunks = {}, []
    for chunk in manifest:
        tgt = chunk_target(chunk)
        f = EN / (chunk + ".en.tex")
        if tgt is None:
            print("no target for", chunk)
            continue
        if not f.exists():
            missing_chunks.append(chunk)
            parts.setdefault(tgt, []).append("\n%% [not yet translated: %s]\n" % chunk)
            continue
        parts.setdefault(tgt, []).append(normalize(f.read_text(encoding="utf-8")))
    for tgt, texts in parts.items():
        (SRC / tgt).parent.mkdir(parents=True, exist_ok=True)
        (SRC / tgt).write_text("\n".join(texts), encoding="utf-8", newline="\n")
    relink()
    print("named statements split:", split_names(), "| displays given their number:", tag_display_labels(),
          "| bibliography keys and fixes:", bibliography_keys())
    print("labels added:", autolabel(), "| references:", resolve_refs())
    body, absent = [], []
    for rel in ORDER:
        if not (SRC / rel).exists():
            absent.append(rel)
            continue
        if rel == "ega1/ega1-intro.tex":
            body.append("\\cleardoublepage\\phantomsection\\addcontentsline{toc}{chapter}{Introduction}"
                        "\\markboth{Introduction}{Introduction}")
        if rel in CHAPTERS:
            num, title = CHAPTERS[rel]
            head = "Chapter %s. %s" % (num, title)
            if "\\begin{center}" in (SRC / rel).read_text(encoding="utf-8", errors="replace")[:600]:
                # the chapter's own title page (Chapter IV, with its summary) stands for the heading
                body.append("\\cleardoublepage\\phantomsection\\addcontentsline{toc}{chapter}{%s}\\markboth{%s}{}"
                            % (head, head))
            else:
                body.append("\\chapter*{%s}\\addcontentsline{toc}{chapter}{%s}\\markboth{%s}{}" % (head, head, head))
        if "backmatter" in rel or "errata" in rel or "bibliography" in rel:
            head = re.search(r"\\section\*\{((?:[^{}]|\{[^{}]*\})*)\}", (SRC / rel).read_text(encoding="utf-8", errors="replace"))
            if head:
                mark = re.sub(r"\\[A-Za-z]+\*?|[{}]", "", head.group(1)).strip()
                body.append("\\clearpage\\markboth{%s}{%s}" % (mark, mark))
        n = section_number(rel)
        if n is not None:
            body.append("\\setcounter{section}{%d}" % (n - 1))
        body.append("\\input{%s}" % rel[:-4])
    numbering = ("\\renewcommand{\\thesection}{\\S\\arabic{section}}\n"
                 "\\renewcommand{\\thesubsection}{\\arabic{section}.\\arabic{subsection}}\n")
    master = ("\\documentclass[11pt]{book}\n\\input{ega-preamble.tex}\n" + numbering + "\\begin{document}\n" + EDITION +
              "\\tableofcontents\n" + "\n".join(body) + "\n\\end{document}\n")
    (SRC / "EGA_EN.tex").write_text(master, encoding="utf-8", newline="\n")
    print("chunks translated: %d of %d | section files missing: %s" % (len(manifest) - len(missing_chunks), len(manifest), absent))
    return SRC / "EGA_EN.tex"


def compile_master(path):
    # marginnote places each note from the position recorded in the .aux on the previous run, so the passes go on
    # until the log no longer asks for a rerun (at most five)
    for run in range(1, 7):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", path.name], cwd=path.parent, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
        log = path.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
        if run == 1:
            print("labels given their key's number:", fix_label_numbers())
        if run >= 4 and not re.search(r"Rerun|may have changed", log):
            break
    print("passes:", run)
    log = path.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
    errs = re.findall(r"^! (.*)", log, re.M)
    pages = re.search(r"Output written on .*?\((\d+) pages", log)
    print("errors:", len(errs), errs[:5], "| pages:", pages.group(1) if pages else None)


if __name__ == "__main__":
    master = build()
    if "--nocompile" not in sys.argv:
        compile_master(master)
