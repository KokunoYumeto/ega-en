"""Final decisions for the 57 pilot items: Sol max's answers, with the two items it missed fixed by hand (graded by
Claude against the French fixes) and item 18083 taken from Sol high so that both c) labels of IV 14.4.2-14.4.3 get the
same markup. Writes decisions_pilot_final.json. usage: python -I finalize_pilot.py"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
mx = json.loads((HERE / "decisions_max.json").read_text(encoding="utf-8"))
hi = {x["id"]: x for x in json.loads((HERE / "decisions_high.json").read_text(encoding="utf-8"))}
by = {x["id"]: x for x in mx}
f9344 = by[9344]["en_file"]
fixes = {
    18079: {"id": 18079, "decision": "apply", "en_file": "source_aligned/ega4-14.tex",
            "en_old": "(or, what amounts to the same, at the maximal points of $X_y$ "
                      "{\\hyperref[IV.14.3.3.1]{(14.3.3.1, (ii))}}).\n\\end{enumerate}",
            "en_new": "\\textup{(or, what amounts to the same, at the maximal points of $X_y$ "
                      "{\\hyperref[IV.14.3.3.1]{(14.3.3.1, (ii))}})}.\n\\end{enumerate}",
            "note": "fixed by Claude: the parenthesis is inside Corollary 14.4.2 (italic)"},
    9345: {"id": 9345, "decision": "apply", "en_file": f9344,
           "en_old": "in the conclusion of \\sref{0.19.8.8}, (ii), one can replace",
           "en_new": "in the conclusion of \\sref{0.19.8.8}, \\textup{(ii)}, one can replace",
           "note": "fixed by Claude: (ii) stood italic inside Corollary 19.8.9"},
    18083: hi[18083],
}
out = [fixes.get(x["id"], x) for x in mx]
(HERE / "decisions_pilot_final.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "decisions;", sum(1 for x in out if x["decision"] == "apply"), "apply")
