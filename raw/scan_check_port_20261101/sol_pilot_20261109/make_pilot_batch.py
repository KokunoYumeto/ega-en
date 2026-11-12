"""Pick about 55 of the English port items still to do (typography items of PORT_EN_HAND3_typography.json not yet in
PORT_EN_LOG3.jsonl) on pages spread over the whole EGA, and write them as one batch from the current English with
make_port_batches.py. usage: python -I make_pilot_batch.py"""
import collections
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
E = HERE.parent
BS = chr(92)
done = {json.loads(l)["entry"] for l in open(E / "PORT_EN_LOG3.jsonl", encoding="utf-8") if l.strip()}
items = [x for x in json.loads((E / "PORT_EN_HAND3_typography.json").read_text(encoding="utf-8")) if x["entry"] not in done]
PARTS = ["0" + BS + "textsubscript{I}", "I", "II", "0" + BS + "textsubscript{III}", "III", "IV",
         "0" + BS + "textsubscript{IV-1}", "IV-1", "IV-2", "IV-3", "IV-4"]
bypage = collections.defaultdict(list)
for x in items:
    bypage[(x["part"], int(x["page"]))].append(x)
keys = sorted(bypage, key=lambda k: (PARTS.index(k[0]) if k[0] in PARTS else 99, k[1]))
print(len(items), "items to do on", len(keys), "pages;", collections.Counter(k[0] for k in keys))
chosen, n, step = [], 0, max(1, len(keys) // 22)
for k in keys[step // 2::step]:
    if n >= 55:
        break
    if len(bypage[k]) > 8:
        continue
    chosen.append(k)
    n += len(bypage[k])
sel = [x for k in chosen for x in bypage[k]]
(HERE / "pilot_items.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(sel), "items on", len(chosen), "pages:", ", ".join(f"{p} {g}" for p, g in chosen))
subprocess.run([sys.executable, "-I", str(E / "make_port_batches.py"), str(HERE / "batch"), "1000",
                "--items=sol_pilot_20261109/pilot_items.json", "--prefix=pilot"], check=True)
