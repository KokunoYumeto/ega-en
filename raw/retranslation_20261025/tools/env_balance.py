"""Environment and brace balance of a TeX file, and the text around a given needle.
usage: python -I -X utf8 -B env_balance.py FILE [NEEDLE]"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
t = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
body = re.sub(r"(?m)(?<!\\)%.*$", "", t)
b = collections.Counter(re.findall(r"\\begin\{([^}]*)\}", body))
e = collections.Counter(re.findall(r"\\end\{([^}]*)\}", body))
print("begin:", dict(b))
print("end:  ", dict(e))
print("unbalanced:", {k: b[k] - e[k] for k in set(b) | set(e) if b[k] != e[k]})
opens = len(re.findall(r"(?<!\\)\{", body))
closes = len(re.findall(r"(?<!\\)\}", body))
print("braces { %d } %d" % (opens, closes))
for cmd in ("begingroup", "endgroup", "bgroup", "egroup"):
    print(cmd, len(re.findall(r"\\%s\b" % cmd, body)))
if len(sys.argv) > 2:
    k = t.find(sys.argv[2])
    print("----\n" + t[max(0, k - 700):k + 700])
