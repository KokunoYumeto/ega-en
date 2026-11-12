"""EGA English port, bulk run by OpenAI GPT-6.1 Sol (effort high, Flex tier) after the 9 Nov pilot (sol_pilot_20261109:
55 of 57 right at both max and high; the two misses were upright parentheses inside italic statements, so the prompt
gets one added rule on that). Items: the typography items of PORT_EN_HAND3_typography.json not yet in PORT_EN_LOG3.jsonl.

usage:
  python -I run_bulk.py build              write items_remaining.json and the batches (make_port_batches.py, current English)
  python -I run_bulk.py run [CONCURRENCY]  submit every batch without an answer, at most CONCURRENCY at a time (default 4);
                                           save answer_<batch>.md and decisions_<batch>.json, dry-run each; print cost
  python -I run_bulk.py summary
The API key is read from the user's note at run time by enr_pilot.key() and never printed or stored."""
import collections
import json
import pathlib
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"user\Documents\enriques_api_pilot_20261106")
import enr_pilot as P  # noqa: E402

HERE = pathlib.Path(__file__).parent
E = HERE.parent
BATCHES = HERE / "batches"
STATE = HERE / "state.json"
MODEL, EFFORT = "gpt-6.1-sol", "high"
EXTRA_RULE = ("- Italic statements: everything inside a proposition, theorem, corollary or lemma environment is italic, "
              "including its enumerate items and the parentheses that contain references; \\sref and \\hyperref make only "
              "the reference itself upright, not the text around it. When the French fix sets a parenthesis or label "
              "upright there, the English needs \\textup{...} on the same parenthesis or label, unless the English "
              "already prints it upright (\\textup, \\rm, \\upshape, or \\emph inside the italic statement).\n")


def prompt(batch_text):
    p0 = (E / "PORT_EN_AGENT_PROMPT.txt").read_text(encoding="utf-8")
    head, rest = p0.split("For each id decide:", 1)
    old = "Your batch file: {BATCH} (plain text; read it in parts with offset/limit). It has one block per printed page:"
    assert old in head
    head = head.replace(old, "Your batch is below, between BEGIN BATCH and END BATCH. It has one block per printed page:")
    decide, rules_out = rest.split("Rules:", 1)
    rules = rules_out.split("{OUTFILE}: one JSON list", 1)[0]
    assert "- Do not edit any file. Write only {OUTFILE}.\n" in rules
    rules = rules.replace("- Do not edit any file. Write only {OUTFILE}.\n", "")
    marker = "- Use LF line breaks"
    assert marker in rules
    rules = rules.replace(marker, EXTRA_RULE + marker, 1)
    out = ("Answer with one fenced block ```json containing one JSON list, one object per id, in the batch's order:\n"
           '  {"id": N, "decision": "apply"|"already"|"not_applicable"|"unclear", "en_file": ..., "en_old": ..., '
           '"en_new": ...,\n   "note": "..."}\n'
           '("en_file" and "en_old" for "apply" and "already", "en_new" only for "apply"; "note" short, and only where '
           "useful). Every id of the batch gets exactly one object.\n"
           'For "already", "en_old" is the exact English text (occurring once in the English pages of the block) that '
           "already says what the corrected French says, so that the decision can be checked.\n"
           "After the block, one line each: any place where the English translation itself is wrong in a way the French "
           "fix does not cover (do not fix those). Nothing else.\n")
    return head + "For each id decide:" + decide + "Rules:" + rules + out + "\nBEGIN BATCH\n" + batch_text + "\nEND BATCH\n"


def build():
    done = {json.loads(l)["entry"] for l in open(E / "PORT_EN_LOG3.jsonl", encoding="utf-8") if l.strip()}
    items = [x for x in json.loads((E / "PORT_EN_HAND3_typography.json").read_text(encoding="utf-8"))
             if x["entry"] not in done]
    (HERE / "items_remaining.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(items), "items remaining")
    subprocess.run([sys.executable, "-I", str(E / "make_port_batches.py"), str(BATCHES), "150",
                    "--items=sol_bulk_20261109/items_remaining.json", "--prefix=bulk"], check=True)


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=1), encoding="utf-8")


def submit(name):
    text = (BATCHES / f"{name}.txt").read_text(encoding="utf-8")
    body = {"model": MODEL, "input": prompt(text), "reasoning": {"effort": EFFORT}, "max_output_tokens": 128000,
            "background": True, "service_tier": "flex"}
    code, r = P.call("POST", P.API, body)
    return code, r.get("id"), r.get("error")


def finish(name, r):
    text = "".join(c.get("text", "") for o in r.get("output", []) if o.get("type") == "message"
                   for c in o.get("content", []))
    (HERE / f"answer_{name}.md").write_text(text, encoding="utf-8")
    m = re.search(r"```json\s*\n(.*?)```", text, re.S)
    ok = False
    if m:
        try:
            lst = json.loads(m.group(1))
            (HERE / f"decisions_{name}.json").write_text(json.dumps(lst, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")
            ok = True
        except ValueError as e:
            print(name, "JSON error", e)
    u = r.get("usage") or {}
    usd = (u.get("input_tokens", 0) * 2 + u.get("output_tokens", 0) * 10) / 1e6 / 2
    dry = ""
    if ok:
        res = subprocess.run([sys.executable, "-I", str(E / "apply_port_decisions.py"),
                              str(HERE / f"decisions_{name}.json"), "--dry"], capture_output=True, text=True,
                             encoding="utf-8")
        dry = res.stdout.strip().splitlines()[0] if res.stdout.strip() else res.stderr.strip()[-300:]
    return ok, round(usd, 4), u.get("input_tokens"), u.get("output_tokens"), dry


def run(conc=4):
    index = json.loads((BATCHES / "BATCHES_bulk.json").read_text(encoding="utf-8"))
    todo = [b["batch"] for b in index if not (HERE / f"decisions_{b['batch']}.json").exists()]
    st = load_state()
    flying = {n: v["id"] for n, v in st.items() if v.get("status") == "submitted" and n in todo}
    queue = [n for n in todo if n not in flying]
    while queue or flying:
        while queue and len(flying) < conc:
            n = queue.pop(0)
            code, rid, err = submit(n)
            if code >= 300 or not rid:
                print(n, "submit failed", code, json.dumps(err)[:200], flush=True)
                st[n] = {"status": "submit_failed", "http": code}
                save_state(st)
                continue
            flying[n] = rid
            st[n] = {"status": "submitted", "id": rid, "t": time.time(), "tries": st.get(n, {}).get("tries", 0) + 1}
            save_state(st)
        time.sleep(45)
        for n, rid in list(flying.items()):
            code, r = P.call("GET", f"{P.API}/{rid}")
            s = r.get("status")
            if s in ("queued", "in_progress"):
                continue
            del flying[n]
            if s == "completed":
                ok, usd, ti, to, dry = finish(n, r)
                st[n].update(status="done" if ok else "bad_answer", usd=usd, input_tokens=ti, output_tokens=to,
                             dry=dry, minutes=round((time.time() - st[n]["t"]) / 60, 1))
                print(n, st[n]["status"], f"${usd}", st[n]["minutes"], "min |", dry, flush=True)
            else:
                st[n].update(status=s, detail=r.get("incomplete_details") or r.get("error"))
                print(n, s, json.dumps(st[n].get("detail"))[:200], flush=True)
                if st[n]["tries"] < 3:
                    queue.append(n)
            save_state(st)
    summary()


def summary():
    st = load_state()
    c = collections.Counter(v.get("status") for v in st.values())
    usd = sum(v.get("usd") or 0 for v in st.values())
    dec = collections.Counter()
    for f in HERE.glob("decisions_bulk_*.json"):
        dec.update(x.get("decision") for x in json.loads(f.read_text(encoding="utf-8")))
    print("batches:", dict(c), f"| cost ${usd:.2f} | decisions:", dict(dec))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "run":
        run(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    else:
        summary()
