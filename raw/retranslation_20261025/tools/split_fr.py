"""Cut the French EGA sources (ega-fr, editions/2026-10-24-r20/current) for the parts to be translated anew into
chunks of at most ~45 KB, at \\section / \\subsection boundaries, and write MANIFEST.json.
Parts: EGA I introduction; EGA 0 §§1-7 (in EGA I), §§8-11 (in EGA III-1), §14 (in EGA IV); EGA I §§1-10;
EGA II §§1-8 and its errata/addenda; EGA III §§1 and 3; EGA IV §16; and the openings of EGA IV §§1, 17, 20 with
their first subsections. usage: python -I -X utf8 -B split_fr.py"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = pathlib.Path("user/Documents/rights_cc0_20261025/ega-fr/editions/2026-10-24-r20/current/packages")
BASE = SRC / "BASE" / "native"
ROOT = pathlib.Path("user/Documents/ega_en_retranslation_20261025")
FR = ROOT / "fr"
FR.mkdir(parents=True, exist_ok=True)
LIMIT = 45000


def read(p):
    return p.read_bytes().decode("utf-8").replace("\r\n", "\n")


def sections(text):
    """Split at \\section{ lines; returns list of (label, text)."""
    idx = [m.start() for m in re.finditer(r"(?m)^\\section\*?\{", text)]
    if not idx:
        return [("all", text)]
    out = [("preamble-part", text[:idx[0]])] if text[:idx[0]].strip() else []
    for a, b in zip(idx, idx[1:] + [len(text)]):
        chunk = text[a:b]
        m = re.search(r"\\label\{section:([^}]+)\}", chunk[:600])
        out.append((m.group(1) if m else "sec%d" % a, chunk))
    return out


def subsplit(label, text):
    """Split a section into pieces <= LIMIT at \\subsection boundaries (greedy)."""
    if len(text.encode("utf-8")) <= LIMIT:
        return [(label, text)]
    cuts = [m.start() for m in re.finditer(r"(?m)^\\subsection\*?\{", text)]
    pieces, start, k = [], 0, 1
    for c in cuts + [len(text)]:
        if c > start and len(text[start:c].encode("utf-8")) > LIMIT and pieces is not None:
            pass
    # greedy accumulation
    bounds = [0] + [c for c in cuts if c > 0] + [len(text)]
    cur = 0
    for i in range(1, len(bounds)):
        if len(text[cur:bounds[i]].encode("utf-8")) > LIMIT and bounds[i - 1] > cur:
            pieces.append(("%s.part%02d" % (label, k), text[cur:bounds[i - 1]]))
            k += 1
            cur = bounds[i - 1]
    pieces.append(("%s.part%02d" % (label, k), text[cur:]))
    return pieces


JOBS = [
    ("ega1-intro", BASE / "ega1" / "intro-fr.tex", None),
    ("ega0-1-7", BASE / "ega1" / "ega0-1-fr.tex", None),
] + [("ega1-%d" % n, BASE / "ega1" / ("ega1-%d-fr.tex" % n), None) for n in range(1, 11)] + [
    ("ega2-1-8", BASE / "ega2" / "ega2-1-fr.tex", None),
    ("ega2-errata", BASE / "ega2" / "ega2-errata-addenda-fr.tex", None),
    ("ega3-1-file", BASE / "ega3" / "ega3-1-fr.tex", {"0.8-fr", "0.9-fr", "0.10-fr", "0.11-fr", "III.1-fr", "III.3-fr"}),
    ("ega0-14", SRC / "IV1" / "native" / "ega4" / "ega0-14-fr.tex", None),
    ("ega4-16", SRC / "IV4" / "native" / "ega4" / "ega4-16-fr.tex", None),
    # §§1, 17, 20 of EGA IV: the earlier English of these sections contains long verbatim runs of the community
    # translation well beyond their openings, so the whole sections are translated anew.
    ("ega4-1", SRC / "IV1" / "native" / "ega4" / "ega4-1-fr.tex", None),
    ("ega4-17", SRC / "IV4" / "native" / "ega4" / "ega4-17-fr.tex", None),
    ("ega4-20", SRC / "IV4" / "native" / "ega4" / "ega4-20-fr.tex", None),
]
manifest = []
for name, path, select in JOBS:
    text = read(path)
    if isinstance(select, set):
        parts = [(lab, t) for lab, t in sections(text) if lab in select]
        missing = select - {lab for lab, _ in parts}
        if missing:
            print("WARNING", name, "sections not found:", sorted(missing), "| found:", [l for l, _ in sections(text)])
    elif select in ("OPENING", "OPENING+FIRST"):
        subs = [m.start() for m in re.finditer(r"(?m)^\\subsection\*?\{", text)]
        end = subs[0] if select == "OPENING" else (subs[1] if len(subs) > 1 else len(text))
        parts = [(name.replace("-file", "") + ("-opening" if select == "OPENING" else "-opening-first"), text[:end])]
    else:
        parts = [(name, text)] if name in ("ega1-intro", "ega2-errata", "ega0-14") else sections(text)
    for lab, t in parts:
        for plab, pt in subsplit(lab if lab != "all" else name, t):
            fn = re.sub(r"[^A-Za-z0-9.+-]", "_", "%s__%s" % (name, plab)) + ".fr.tex"
            (FR / fn).write_text(pt, encoding="utf-8", newline="\n")
            manifest.append({"chunk": fn[:-7], "source": str(path), "bytes": len(pt.encode("utf-8")),
                             "first_line": pt.strip().splitlines()[0][:100] if pt.strip() else ""})
(ROOT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print("chunks:", len(manifest), "| total KB:", round(sum(m["bytes"] for m in manifest) / 1000))
for m in manifest:
    print("%-48s %7d  %s" % (m["chunk"], m["bytes"], m["first_line"][:60]))
