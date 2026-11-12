"""Progress of the EGA retranslation: per task group, which chunks are written and whether each passes check_chunk.py.
Also records launched task numbers given on the command line in LAUNCHED.json.
usage: python -I -X utf8 -B progress.py [--launched 8 9 ...]"""
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parent.parent
groups = json.loads((R / "GROUPS.json").read_text(encoding="utf-8"))
lf = R / "LAUNCHED.json"
launched = set(json.loads(lf.read_text(encoding="utf-8"))) if lf.exists() else set()
if "--launched" in sys.argv:
    launched |= {int(a) for a in sys.argv[sys.argv.index("--launched") + 1:]}
    lf.write_text(json.dumps(sorted(launched)), encoding="utf-8")
done_tasks, total_ok = [], 0
for k, g in enumerate(groups):
    states = []
    for ch in g:
        f = R / "en" / (ch + ".en.tex")
        if not f.exists():
            states.append("-")
            continue
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(R / "tools" / "check_chunk.py"), ch],
                           capture_output=True, text=True, encoding="utf-8")
        ok = r.stdout.startswith("OK")
        total_ok += ok
        states.append("ok" if ok else "PROBLEM")
    if all(s == "ok" for s in states):
        done_tasks.append(k)
    flag = "launched" if k in launched else ""
    if any(s != "-" for s in states) or flag:
        print("%2d %-9s %s" % (k, flag, " ".join(states)))
print("tasks complete: %d of %d | chunks passing check: %d of %d | launched: %s" % (
    len(done_tasks), len(groups), total_ok, sum(len(g) for g in groups), sorted(launched)))
