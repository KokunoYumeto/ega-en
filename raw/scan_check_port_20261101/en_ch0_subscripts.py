"""English EGA IV: references to chapter 0 written \\sref[0]{0.N...} print "(0, n)" where the print has 0_I (N <= 7) or
0_III (8 <= N <= 13). Convert them to \\sref[0\\textsubscript{\\mdseries I}]{...} / ...{III}, but only when the French
of the same part writes that number with the same subscript (generalizes the IV 8-11 slips agent's script).
usage: python -I en_ch0_subscripts.py [--apply] ENFILE...   (paths relative to ega-en/tex, without .tex)"""
import json
import pathlib
import re
import sys

E = pathlib.Path(__file__).parent
EN = E / "ega-en" / "tex"
FRP = E / "ega-fr" / "editions" / "2026-10-24-r20" / "current" / "packages"
BS = chr(92)
apply = "--apply" in sys.argv
files = [a for a in sys.argv[1:] if not a.startswith("--")]
sub_I = re.compile(r"(_\{\\mathrm ?\{?I\}?\}|_\\mathrm\{I\}|\\textsubscript\{I\}|_\{\\rm I\}|_\{I\}|_I)(?![I])")
sub_III = re.compile(r"(_\{\\mathrm ?\{?III\}?\}|_\\mathrm\{III\}|\\textsubscript\{III\}|_\{\\rm III\}|_\{III\})")
pat = re.compile(r"\\sref\[0\]\{0\.(\d+)\.([0-9.]+)\}")
french = {}
for part in ("IV1", "IV2", "IV3", "IV4"):
    french[part] = "\n".join(p.read_text(encoding="utf-8") for p in sorted((FRP / part / "native").rglob("*.tex")))


# EGA III only (in EGA I the chapter-0 references carry no subscript)
french["III"] = "\n".join(p.read_text(encoding="utf-8") for p in sorted((FRP / "BASE" / "native" / "ega3").glob("*.tex")))


def part_of(name):
    if name.startswith("ega3-"):
        return "III"
    n = int(re.search(r"ega4-(\d+)", name).group(1))
    return "IV2" if n <= 7 else ("IV3" if n <= 15 else "IV4")


log = []
for rel in files:
    p = EN / (rel + ".tex")
    fr = french[part_of(p.name)]
    s = p.read_text(encoding="utf-8")
    out = []
    for m in pat.finditer(s):
        n = int(m.group(1))
        if n > 13:
            continue
        num = m.group(1) + "." + m.group(2).rstrip(".")
        want = "I" if n <= 7 else "III"
        hits = []
        for fm in re.finditer(r"(?<![0-9.])" + re.escape(num) + r"(?![0-9])", fr):
            before = fr[max(0, fm.start() - 45):fm.start()]
            if "0" not in before:
                continue
            tail = before[before.rfind("0"):]
            if sub_III.search(tail):
                hits.append("III")
            elif sub_I.search(tail):
                hits.append("I")
            elif re.search(r"\\mathbf ?\{?0\}?|\\textbf\{0\}", before):
                hits.append("none")
        ok = bool(hits) and all(h == want for h in hits)
        log.append({"file": rel, "line": s.count("\n", 0, m.start()) + 1, "ref": num, "want": want, "french": hits,
                    "ok": ok})
        if ok:
            out.append((m.start(), m.end(), BS + "sref[0" + BS + "textsubscript{" + BS + "mdseries " + want + "}]{0."
                        + num + "}"))
    if apply and out:
        for a, b, rep in reversed(out):
            s = s[:a] + rep + s[b:]
        p.write_text(s, encoding="utf-8", newline="")
for r in log:
    if not r["ok"]:
        print("left:", json.dumps(r, ensure_ascii=False))
print("converted" if apply else "would convert", sum(1 for r in log if r["ok"]), "of", len(log))
if apply:
    with open(E / "EN_CH0_SUBSCRIPTS_LOG.jsonl", "a", encoding="utf-8") as fh:
        for r in log:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
