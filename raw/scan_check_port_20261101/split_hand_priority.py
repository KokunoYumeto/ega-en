"""Split the English hand items not yet sent to an agent into
  content    : changes of formulas, words, numbers, references, structure (first)
  typography : only italic emphasis, upright text, or punctuation and spacing (later)
plus the 'global' items whose upright parenthesis holds no reference (PORT_EN_GLOBAL_RECHECK.json; typography).
Writes PORT_EN_HAND3_content.json and PORT_EN_HAND3_typography.json."""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BS = chr(92)
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
hand = json.loads((E / "PORT_EN_HAND2.json").read_text(encoding="utf-8"))
sent = set()
for b in json.loads((E / "port_en_batches" / "BATCHES.json").read_text(encoding="utf-8")):
    if b["batch"] in ("batch_001", "batch_002", "batch_003", "batch_004"):
        sent.update(b["ids"])
fixlog = {}
for n, line in enumerate(open(E / "FIXLOG_CURRENT.jsonl", encoding="utf-8"), 1):
    if line.strip():
        fixlog[n] = json.loads(line)
WRAP = re.compile(re.escape(BS) + r"(?:emph|textup|textit|textrm|upshape|itshape|em)\b\s*")


def strip_typo(s):
    s = WRAP.sub("", s)
    s = re.sub(r"[{}]", "", s)
    return s


def punct_only(o, n):
    a = re.sub(r"[\s~,;:.!?«»\u00a0\u202f'’`]", "", o)
    b = re.sub(r"[\s~,;:.!?«»\u00a0\u202f'’`]", "", n)
    return a == b


content, typo = [], []
for x in hand:
    if x["entry"] in sent:
        continue
    o, n = x["old"], x["new"]
    if strip_typo(o) == strip_typo(n) or punct_only(o, n):
        typo.append(x)
    else:
        content.append(x)
recheck = set(json.loads((E / "PORT_EN_GLOBAL_RECHECK.json").read_text(encoding="utf-8")))
for n in sorted(recheck):
    x = fixlog[n]
    typo.append(dict(entry=n, part=x.get("part") or "I", page=int(x["page"]), old=x["old"], new=x["new"],
                     kind=x.get("kind"), why=x.get("why"), fr_file=x["file"], file=pathlib.Path(x["file"]).name))
(E / "PORT_EN_HAND3_content.json").write_text(json.dumps(content, ensure_ascii=False, indent=1), encoding="utf-8")
(E / "PORT_EN_HAND3_typography.json").write_text(json.dumps(typo, ensure_ascii=False, indent=1), encoding="utf-8")
print("not yet sent:", len(content) + len(typo) - len(recheck), "| content", len(content), "| typography", len(typo),
      "(incl.", len(recheck), "global rechecks)")
