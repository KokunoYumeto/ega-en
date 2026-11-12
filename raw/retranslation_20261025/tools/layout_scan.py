"""Layout scan of a typeset PDF: pages whose text runs past the paper or far into the margins, nearly empty pages
(not the last page of a section or chapter), raw TeX visible in the output (\\begin, \\frac, $, ^{, _{ ...),
unresolved references (??), replacement characters, and pages with lines much wider than the text block.
Writes nothing; prints flagged pages with reasons. usage: python -X utf8 -B layout_scan.py PDF [max listed]"""
import collections
import re
import statistics
import sys

import fitz

path = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 40
d = fitz.open(path)
W = d[min(5, d.page_count - 1)].rect.width
H = d[min(5, d.page_count - 1)].rect.height
RAW = re.compile(r"\\(begin|end|frac|mathcal|mathscr|mathfrak|textbf|emph|sref|label|item|section|cite)\b|\$|\^\{|_\{|\\\\")
flags = collections.defaultdict(list)
fills = []
lefts, rights = [], []
for i in range(d.page_count):
    p = d[i]
    words = p.get_text("words")
    if words:
        xs0 = [w[0] for w in words]
        xs1 = [w[2] for w in words]
        lefts.append(statistics.median(xs0))
        rights.append(max(xs1))
L = statistics.median(lefts) if lefts else 0
R = statistics.quantiles(rights, n=20)[17] if len(rights) > 20 else max(rights or [W])  # 90th percentile
for i in range(d.page_count):
    p = d[i]
    text = p.get_text()
    words = p.get_text("words")
    if not words:
        flags[i + 1].append("no text")
        continue
    x1 = max(w[2] for w in words)
    x0 = min(w[0] for w in words)
    if x1 > W - 4 or x0 < 4:
        flags[i + 1].append("text at the paper edge (x %.0f-%.0f of %.0f)" % (x0, x1, W))
    elif x1 > R + 25:
        flags[i + 1].append("line %.0fpt past the usual right edge" % (x1 - R))
    ys = [w[3] for w in words]
    fill = (max(ys) - min(w[1] for w in words)) / H
    fills.append(fill)
    if fill < 0.30 and i + 1 < d.page_count:
        flags[i + 1].append("only %.0f%% of the page used" % (100 * fill))
    m = RAW.search(text)
    if m:
        k = m.start()
        flags[i + 1].append("raw TeX? %r" % text[max(0, k - 25):k + 25].replace("\n", " "))
    if "??" in text:
        flags[i + 1].append("?? in text")
    if "\ufffd" in text:
        flags[i + 1].append("replacement character")
print("%s: %d pages, paper %.0fx%.0f, usual text %.0f-%.0f, median fill %.0f%%" % (
    path.split("/")[-1], d.page_count, W, H, L, R, 100 * statistics.median(fills)))
kinds = collections.Counter(r.split(" (")[0].split(" %")[0].split("?")[0] for v in flags.values() for r in v)
print("flag kinds:", dict(kinds))
for pg in sorted(flags)[:limit]:
    print("  p%-5d %s" % (pg, "; ".join(flags[pg])))
print("flagged pages:", len(flags))
