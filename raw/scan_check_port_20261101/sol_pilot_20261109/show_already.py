"""Show the English of the pilot batch around the places Sol called "already" (plain substring search)."""
import re
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")
import ega_sol_pilot as S  # noqa: E402

txt = S.BATCH.read_text(encoding="utf-8")
en = re.sub(r"(?ms)^----- French corrections on page.*?(?=^=================== PAGE|\Z)", "", txt)
keys = {6626: ["widehat{\\mathcal M}^{", "widehat{\\mathcal{M}}^{"], 7214: ["-functor"], 7217: ["iregular"],
        7233: ["ohomology module", "module of \\emph{cohomology", "\\emph{cohomology"],
        8604: ["delete", "Delete", "suppress"], 8686: ["is \\emph{zero}", "is \\emph{null}", "is zero at", "is null at"],
        9345: ["19.8.8"], 12302: ["deg.tr"], 12311: ["rare", "nowhere dense"], 16823: ["(Z_i)_\\eta"],
        17135: ["widehat{A"], 18079: ["14.3.3.1"]}
for i, ks in keys.items():
    print(f"## {i}")
    n = 0
    for k in ks:
        p = en.find(k)
        while p >= 0 and n < 5:
            print("   ", repr(en[max(0, p - 150):p + len(k) + 100]))
            n += 1
            p = en.find(k, p + 1)
