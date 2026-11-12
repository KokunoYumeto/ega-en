"""Audit of the automatic English port (ENGLISH_SLIPS.md, content_023 warning): French corrections that the first or
second automatic round logged as "already" (the English has the corrected reading) or "applied" at several places,
but whose OLD reading still occurs on the English pages p-1..p+1 (normalized as in port_hand_auto.py). Such an entry
may be a false "already" (e.g. a letter R -> K where the English writes the R differently) or a partial application.

Reuses the normalization and search functions of port_hand_auto.py (its code before the main loop).
usage: python -I audit_already_en.py OUT.json"""
import json
import pathlib
import sys

E = pathlib.Path(__file__).parent
out_path = pathlib.Path(sys.argv[1])
sys.argv = [sys.argv[0]]  # never --apply
src = (E / "port_hand_auto.py").read_text(encoding="utf-8")
cut = src.index('hand = json.loads((E / "PORT_EN_HAND.json")')
ns = {"__name__": "port_hand_auto_lib", "__file__": str(E / "port_hand_auto.py")}
exec(compile(src[:cut], "port_hand_auto.py", "exec"), ns)
norm_fr, en_regions, count_in, boundaries, norm_of = (ns["norm_fr"], ns["en_regions"], ns["count_in"],
                                                      ns["boundaries"], ns["norm_of"])

fixlog = {}
for n, line in enumerate(open(E / "FIXLOG_CURRENT.jsonl", encoding="utf-8"), 1):
    fixlog[n] = json.loads(line)
outcome = {}
for fn in ("PORT_EN_LOG.jsonl", "PORT_EN_LOG2.jsonl"):
    for line in open(E / fn, encoding="utf-8"):
        r = json.loads(line)
        k = r.get("entry")
        if k is None:
            continue
        if r.get("outcome") == "already" or (r.get("outcome") == "applied" and (r.get("occurrences") or 1) > 1):
            outcome[k] = (fn, r.get("outcome"), r.get("occurrences"))


def windows(o, nw):
    p = 0
    while p < min(len(o), len(nw)) and o[p] == nw[p]:
        p += 1
    q = 0
    while q < min(len(o), len(nw)) - p and o[-1 - q] == nw[-1 - q]:
        q += 1
    lo, hi = p, len(o) - q
    bnd = boundaries(o)
    left = [k for k in bnd if k <= lo][::-1][:5]
    right = [k for k in bnd if k >= hi][:5]
    cands = sorted({(a, b) for a in left for b in right if b > a}, key=lambda ab: ab[1] - ab[0])
    for a, b in cands:
        w = o[a:b]
        if len(w.strip()) >= 5 and w not in nw:
            yield w


flags = []
for k, (fn, oc, occ) in sorted(outcome.items()):
    x = fixlog.get(k)
    if not x or x.get("part") is None or x.get("page") is None:
        continue
    o, nw = norm_fr(x["old"]), norm_fr(x["new"])
    if o == nw:
        continue
    regs = en_regions(x["part"], x["page"])
    if not regs:
        continue
    for w in windows(o, nw):
        hits = count_in(regs, w)
        if hits:
            f, (s, e) = hits[0]
            t = ns["en_text"][f]
            flags.append({"entry": k, "round": fn, "outcome": oc, "occurrences": occ, "part": x["part"],
                          "page": x["page"], "fr_old": x["old"][:300], "fr_new": x["new"][:300], "window_old": w,
                          "en_file": str(pathlib.Path(f).relative_to(E / "ega-en" / "tex")) if pathlib.Path(f).is_absolute() else str(f),
                          "en_hits": len(hits), "en_context": t[max(0, s - 80):e + 80]})
            break
out_path.write_text(json.dumps(flags, ensure_ascii=False, indent=1), encoding="utf-8")
print("checked", len(outcome), "entries; flagged", len(flags))
by = {}
for fl in flags:
    by[(fl["round"], fl["outcome"])] = by.get((fl["round"], fl["outcome"]), 0) + 1
print(by)
