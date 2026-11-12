"""Collect the translators' notes (notes/*.md) into two ledgers: TRANSCRIPTION_NOTES.md (suspected errors in the
French transcription or the original, to be checked against the scans) and TERM_NOTES.md (terms not yet in the
glossary). Each entry keeps its chunk name. usage: python -I -X utf8 -B collect_notes.py"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parent.parent
order = [m["chunk"] for m in json.loads((R / "MANIFEST.json").read_text(encoding="utf-8"))]
trans, terms = [], []
for chunk in order:
    f = R / "notes" / (chunk + ".md")
    if not f.exists():
        continue
    for line in f.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if re.match(r"^[-*]\s*TRANSCRIPTION", s):
            trans.append((chunk, re.sub(r"^[-*]\s*TRANSCRIPTION\??\s*", "", s)))
        elif re.match(r"^[-*]\s*TERM", s):
            terms.append((chunk, re.sub(r"^[-*]\s*TERM\s*", "", s)))


def write(name, title, rows):
    out = ["# " + title, "", "%d entries, in the order of the edition." % len(rows), ""]
    last = None
    for chunk, text in rows:
        if chunk != last:
            out += ["", "## " + chunk, ""]
            last = chunk
        out.append("- " + text)
    (R / name).write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


write("TRANSCRIPTION_NOTES.md", "Suspected errors in the French text (transcription or original), noted while translating", trans)
write("TERM_NOTES.md", "Terms chosen while translating that are not in GLOSSARY.md", terms)
print("transcription notes:", len(trans), "| term notes:", len(terms))
