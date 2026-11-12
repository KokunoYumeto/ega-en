"""Keep the audit flags (AUDIT_ALREADY_EN.json) whose French correction changes letters or digits (a formula slip such
as R -> K, Y -> S, i -> j), not fonts or macros, and whose old window is long enough to be specific.
usage: python -I audit_already_filter.py IN.json OUT.json"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(sys.argv[1], encoding="utf-8"))
keep = []
for x in d:
    o, n = x["fr_old"], x["fr_new"]
    p = 0
    while p < min(len(o), len(n)) and o[p] == n[p]:
        p += 1
    q = 0
    while q < min(len(o), len(n)) - p and o[-1 - q] == n[-1 - q]:
        q += 1
    co, cn = o[p:len(o) - q], n[p:len(n) - q]
    # extend the cores to whole alphanumeric runs, so that "R" vs "K" inside \mathfrak{R} is seen as a letter change
    if re.fullmatch(r"[A-Za-z0-9']{1,3}", co or "x") and re.fullmatch(r"[A-Za-z0-9']{1,3}", cn or "x"):
        before = o[max(0, p - 12):p]
        if re.search(r"\\[A-Za-z]*$", before) and not before.endswith("{"):  # inside a control word: a macro change
            continue
        if len(x["window_old"]) < 8:
            continue
        x["core"] = f"{co} -> {cn}"
        keep.append(x)
json.dump(keep, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(keep), "kept of", len(d))
for x in keep[:60]:
    print(x["entry"], x["part"], x["page"], x["core"], "|", repr(x["window_old"][:50]), "|",
          x["en_context"][60:200].replace("\n", " "))
