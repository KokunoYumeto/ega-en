"""Second look by GPT-6.1 Sol (effort max, Flex) at the bulk items that the audit questioned (doubtful_ids.json) or
that did not place when applied (PORT_EN_LEFT3.json entries of the clean run). The batch is rebuilt from the current
English; each item comes with the first answer and the reason it was questioned.
usage: python -I second_look.py build | run"""
import json
import pathlib
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
E = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, r"user\Documents\enriques_api_pilot_20261106")
import enr_pilot as P  # noqa: E402
import run_bulk as R  # noqa: E402

LEFT_IDS = [2147, 6793, 6796, 6797, 7081, 6354, 7118, 7137, 15873]


def first_answers():
    out = {}
    for f in sorted(HERE.glob("decisions_bulk_0*.json")):
        for d in json.loads(f.read_text(encoding="utf-8")):
            out[int(d["id"])] = d
    return out


def build():
    doubt = {d["id"]: d["why"] for d in json.loads((HERE / "doubtful_ids.json").read_text(encoding="utf-8"))}
    for i in LEFT_IDS:
        doubt.setdefault(i, "apply: en_old was not found exactly once when the edits were applied")
    meta = {x["entry"]: x for x in json.loads((E / "PORT_EN_HAND3_typography.json").read_text(encoding="utf-8"))}
    items = [meta[i] for i in doubt if i in meta]
    (HERE / "second_items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "second_why.json").write_text(json.dumps(doubt, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(E / "make_port_batches.py"), str(HERE / "second"), "40",
                    "--items=sol_bulk_20261109/second_items.json", "--prefix=second"], check=True)


def run():
    why = {int(k): v for k, v in json.loads((HERE / "second_why.json").read_text(encoding="utf-8")).items()}
    first = first_answers()
    jobs = {}
    for bf in sorted((HERE / "second").glob("second_*.txt")):
        if sys.argv[2:] and bf.stem not in sys.argv[2:]:   # run only the named batches (a retry after a server error)
            continue
        text = bf.read_text(encoding="utf-8")
        ids = [int(m) for m in re.findall(r"^\[id (\d+)\]$", text, re.M)]
        notes = ["", "SECOND LOOK. Every id below was answered once already; a mechanical check questioned that answer.",
                 "For each id: the first answer and why it was questioned. Read the French fix and the English again and",
                 "decide afresh (the first answer may still be right). The English shown is the current English, with the",
                 "other corrections already applied.", ""]
        for i in ids:
            d = first.get(i, {})
            notes.append(f"[id {i}] first answer: {d.get('decision')}; en_old {d.get('en_old')!r}; en_new "
                         f"{d.get('en_new')!r}; note {d.get('note')!r}. Questioned because: {why.get(i)}")
        prompt = R.prompt(text).replace("\nBEGIN BATCH\n", "\n" + "\n".join(notes) + "\n\nBEGIN BATCH\n", 1)
        body = {"model": "gpt-6.1-sol", "input": prompt, "reasoning": {"effort": "max"}, "max_output_tokens": 128000,
                "background": True, "service_tier": "flex"}
        code, r = P.call("POST", P.API, body)
        print(bf.stem, len(ids), "items, submit", code, r.get("id"), flush=True)
        jobs[bf.stem] = r.get("id")
    total = 0.0
    for name, rid in jobs.items():
        while True:
            code, r = P.call("GET", f"{P.API}/{rid}")
            if r.get("status") not in ("queued", "in_progress"):
                break
            time.sleep(45)
        ok, usd, ti, to, dry = R.finish(name, r)
        total += usd
        src = HERE / f"decisions_{name}.json"
        print(name, r.get("status"), f"${usd}", "|", dry, flush=True)
    print(f"total ${total:.3f}")


if __name__ == "__main__":
    {"build": build, "run": run}[sys.argv[1]]()
