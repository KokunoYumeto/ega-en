"""Compare two PDFs of the same work: page count, total words, words per page, typical text-block width and font
size, and the number of numbered statements found (to tell layout growth from duplicated or missing content).
usage: python -X utf8 -B compare_volume.py OLD.pdf NEW.pdf"""
import collections
import re
import statistics
import sys

import fitz


def profile(path):
    d = fitz.open(path)
    words = 0
    widths, sizes = [], collections.Counter()
    nums = set()
    for i in range(d.page_count):
        p = d[i]
        t = p.get_text()
        words += len(t.split())
        nums.update(re.findall(r"\((\d{1,2}\.\d{1,2}\.\d{1,2})\)", t))
        if i % 25 == 0:
            xs = []
            for b in p.get_text("dict")["blocks"]:
                for l in b.get("lines", []):
                    for s in l["spans"]:
                        if s["text"].strip():
                            sizes[round(s["size"], 1)] += len(s["text"])
                            xs.append((s["bbox"][0], s["bbox"][2]))
            if xs:
                widths.append(max(x[1] for x in xs) - min(x[0] for x in xs))
    r = d[min(10, d.page_count - 1)].rect
    return {"pages": d.page_count, "paper": (round(r.width), round(r.height)), "words": words,
            "words/page": round(words / d.page_count), "text width pt": round(statistics.median(widths)) if widths else 0,
            "main font": sizes.most_common(1)[0][0] if sizes else 0, "distinct (a.b.c) numbers": len(nums)}


for path in sys.argv[1:]:
    print(path.split("/")[-1], profile(path))
