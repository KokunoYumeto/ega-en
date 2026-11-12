"""Find automatic port edits whose window matched part of a word in the target text: the replaced text now begins or
ends inside a word (e.g. the French window '(i)] Si' matched the English '(i)] Since').
Only windows that begin or end with a letter can do this; each is looked for near the line the log gives
(port_fixes_to_en.py logs en_line), otherwise in the whole file, and reported if it sits inside a longer word.
usage: python -I check_partial_words.py LOG.jsonl [LOG.jsonl ...] --root=DIR"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path([a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--root=")][0])
logs = [a for a in sys.argv[1:] if not a.startswith("--")]
files = {}
for f in root.rglob("*.tex"):
    files.setdefault(f.name, []).append(f)
texts = {}
out = []
for lg in logs:
    for line in open(lg, encoding="utf-8"):
        r = json.loads(line)
        if r.get("outcome") != "applied":
            continue
        wo, wn = r.get("window_old") or "", r.get("window_new") or ""
        if not wn or not (wo[-1:].isalpha() or wo[:1].isalpha()):
            continue
        for f in files.get(r.get("en_file"), []):
            if f not in texts:
                texts[f] = f.read_text(encoding="utf-8")
            t = texts[f]
            lo, hi = 0, len(t)
            if r.get("en_line"):
                ls = t.split("\n")
                L = r["en_line"]
                lo = len("\n".join(ls[:max(0, L - 4)]))
                hi = len("\n".join(ls[:L + 4]))
            for m in re.finditer(re.escape(wn), t[lo:hi]):
                a, b = lo + m.start(), lo + m.end()
                end_in_word = wo[-1:].isalpha() and wn[-1:].isalpha() and t[b:b + 1].isalpha()
                start_in_word = wo[:1].isalpha() and wn[:1].isalpha() and t[a - 1:a].isalpha() and \
                    not re.search(r"\\[A-Za-z]*$", t[max(0, a - 20):a])
                if end_in_word or start_in_word:
                    out.append(dict(entry=r["entry"], part=r.get("part"), page=r.get("page"), file=str(f), pos=a,
                                    window_old=wo, window_new=wn, context=t[max(0, a - 40):b + 25]))
                    print(r["entry"], r.get("part"), r.get("page"), f.name, repr(wo), "->", repr(wn), "|",
                          repr(t[max(0, a - 25):b + 15]))
print("suspicious:", len(out))
(pathlib.Path(logs[0]).parent / "PARTIAL_WORD_SUSPECTS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                                         encoding="utf-8")
