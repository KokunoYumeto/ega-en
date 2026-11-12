"""EGA English port, pilot of OpenAI GPT-6.1 Sol: carry 57 French corrections still to do (typography items, pages
spread over EGA II-IV, batch built from the current English by make_pilot_batch.py) into the English, once at reasoning
effort max and once at high (Flex tier). The task text is PORT_EN_AGENT_PROMPT.txt adapted to one request (the batch
inline, the answer as one JSON block). `compare` checks every apply edit with apply_port_decisions.py --dry and writes
the two answers side by side with the French fix, for grading by hand.

usage:
  python -I ega_sol_pilot.py submit EFFORT        (max | high)
  python -I ega_sol_pilot.py wait EFFORT
  python -I ega_sol_pilot.py compare
The API key is read from the user's note at run time by enr_pilot.key() and never printed or stored."""
import collections
import json
import pathlib
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"user\Documents\enriques_api_pilot_20261106")
import enr_pilot as P  # noqa: E402

HERE = pathlib.Path(__file__).parent
E = HERE.parent
BATCH = HERE / "batch" / "pilot_001.txt"
MODEL = "gpt-6.1-sol"


def prompt():
    p0 = (E / "PORT_EN_AGENT_PROMPT.txt").read_text(encoding="utf-8")
    head, rest = p0.split("For each id decide:", 1)
    old = "Your batch file: {BATCH} (plain text; read it in parts with offset/limit). It has one block per printed page:"
    assert old in head
    head = head.replace(old, "Your batch is below, between BEGIN BATCH and END BATCH. It has one block per printed page:")
    decide, rules_out = rest.split("Rules:", 1)
    rules = rules_out.split("{OUTFILE}: one JSON list", 1)[0]
    assert "- Do not edit any file. Write only {OUTFILE}.\n" in rules
    rules = rules.replace("- Do not edit any file. Write only {OUTFILE}.\n", "")
    out = ("Answer with one fenced block ```json containing one JSON list, one object per id, in the batch's order:\n"
           '  {"id": N, "decision": "apply"|"already"|"not_applicable"|"unclear", "en_file": ..., "en_old": ..., '
           '"en_new": ...,\n   "note": "..."}\n'
           '("en_file", "en_old", "en_new" only for "apply"; "note" short, and only where useful). Every id of the batch '
           "gets exactly one object.\n"
           "After the block, one line each: any place where the English translation itself is wrong in a way the French "
           "fix does not cover (do not fix those). Nothing else.\n")
    text = BATCH.read_text(encoding="utf-8")
    return head + "For each id decide:" + decide + "Rules:" + rules + out + "\nBEGIN BATCH\n" + text + "\nEND BATCH\n"


def submit(effort):
    body = {"model": MODEL, "input": prompt(), "reasoning": {"effort": effort}, "max_output_tokens": 128000,
            "background": True, "service_tier": "flex"}
    st, r = P.call("POST", "https://api.openai.com/v1/responses", body)
    state = {"effort": effort, "http": st, "id": r.get("id"), "submitted": time.time(),
             "error": None if st < 300 else json.dumps(r)[:500]}
    (HERE / f"state_{effort}.json").write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(effort, st, r.get("id"), state["error"] or "")


def wait(effort):
    sp = HERE / f"state_{effort}.json"
    state = json.loads(sp.read_text(encoding="utf-8"))
    while True:
        st, r = P.call("GET", f"https://api.openai.com/v1/responses/{state['id']}")
        if r.get("status") in ("completed", "failed", "cancelled", "incomplete"):
            break
        time.sleep(60)
    text = "".join(c.get("text", "") for o in r.get("output", []) if o.get("type") == "message"
                   for c in o.get("content", []))
    (HERE / f"answer_{effort}.md").write_text(text, encoding="utf-8")
    u = r.get("usage") or {}
    rt = (u.get("output_tokens_details") or {}).get("reasoning_tokens")
    cost = (u.get("input_tokens", 0) * 2 + u.get("output_tokens", 0) * 10) / 1e6 / 2  # Flex: half of $2/$10
    state.update(status=r.get("status"), incomplete=r.get("incomplete_details"), input_tokens=u.get("input_tokens"),
                 output_tokens=u.get("output_tokens"), reasoning_tokens=rt, flex_usd=round(cost, 3),
                 minutes=round((time.time() - state["submitted"]) / 60, 1))
    sp.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(effort, state["status"], "in", state["input_tokens"], "out", state["output_tokens"], "reasoning", rt,
          f"${cost:.3f}", state["minutes"], "min")


def blocks():
    text = BATCH.read_text(encoding="utf-8")
    parts = re.split(r"^=================== PAGE (.+?) ===================$", text, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        page, body = parts[i], parts[i + 1]
        k = body.find("----- French corrections on page")
        en_part, fr_part = body[:k], body[k:]
        subs = re.split(r"^----- English, (.+?), page (.+?) -----$", en_part, flags=re.M)
        en = "\n\u0000\n".join(subs[j + 2] for j in range(1, len(subs), 3))
        fr = {}
        for m in re.finditer(r"^\[id (\d+)\]$(.*?)(?=^\[id \d+\]$|\Z)", fr_part, flags=re.M | re.S):
            fr[int(m.group(1))] = m.group(2).strip()
        out.append({"page": page, "en": en, "fr": fr})
    return out


def parse_answer(effort):
    t = (HERE / f"answer_{effort}.md").read_text(encoding="utf-8")
    m = re.search(r"```json\s*\n(.*?)```", t, re.S)
    return json.loads(m.group(1)), t[m.end():].strip()


def apply_all(en, edits):
    """Apply (en_old, en_new) edits to en; an edit whose en_old does not occur exactly once is not applied."""
    bad = []
    for i, (a, b) in edits:
        if a and en.count(a) == 1:
            en = en.replace(a, b)
        else:
            bad.append((i, "en_old occurs %d times" % (en.count(a) if a else 0)))
    return en, bad


def compare(_=None):
    import subprocess
    fr = {}
    for b in blocks():
        fr.update({i: (b["page"], v) for i, v in b["fr"].items()})
    ans = {}
    for eff in ("max", "high"):
        if not (HERE / f"answer_{eff}.md").exists():
            continue
        lst, extra = parse_answer(eff)
        (HERE / f"decisions_{eff}.json").write_text(json.dumps(lst, ensure_ascii=False, indent=1), encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(E / "apply_port_decisions.py"), str(HERE / f"decisions_{eff}.json"),
                            "--dry"], capture_output=True, text=True, encoding="utf-8")
        print(eff, "dry run:", r.stdout.strip()[-600:])
        ans[eff] = ({int(x["id"]): x for x in lst}, extra)
    NL = chr(10)
    out = []
    for i, (page, frtext) in fr.items():
        out += [f"## id {i} (page {page})", "FRENCH:", frtext, ""]
        for eff, (d, _) in ans.items():
            x = d.get(i) or {}
            dec = x.get("decision", "MISSING")
            if dec == "apply":
                out += [f"SOL {eff}: apply", f"  old: {x.get('en_old')!r}", f"  new: {x.get('en_new')!r}"]
            else:
                out.append(f"SOL {eff}: {dec}  note: {x.get('note')}")
        out.append("")
    for eff, (_, extra) in ans.items():
        out += [f"## Sol {eff}: remarks after the JSON", extra, ""]
    (HERE / "compare.md").write_text(NL.join(out), encoding="utf-8")
    for eff, (d, _) in ans.items():
        print(eff, collections.Counter(x.get("decision") for x in d.values()), "ids answered", len(d), "of", len(fr))


if __name__ == "__main__":
    {"submit": submit, "wait": wait, "compare": compare}[sys.argv[1]](sys.argv[2] if len(sys.argv) > 2 else None)
