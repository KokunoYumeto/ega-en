"""Find page-marker margin notes ([vol | page]) that overlap the text block in the built PDF, and notes that run
off the page. usage: python -X utf8 -B note_overlaps.py PDF   (needs PyMuPDF, so no -I)"""
import re
import sys

import fitz

doc = fitz.open(sys.argv[1])
NOTE = re.compile(r"^\[[^\]]*\|[^\]]*\]$")
inside, offpage, total = [], [], 0
for pno in range(doc.page_count):
    page = doc[pno]
    W = page.rect.width
    spans, body = [], []
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            for s in line["spans"]:
                txt = s["text"].strip()
                if not txt:
                    continue
                if s["size"] < 9.5 and NOTE.match(txt.replace(" ", "")):
                    spans.append(fitz.Rect(s["bbox"]))
                elif s["size"] >= 10 and s["bbox"][1] > 75:  # below the running head
                    body.append(fitz.Rect(s["bbox"]))
    if not body:
        continue
    left = min(r.x0 for r in body)
    right = max(r.x1 for r in body)
    for r in spans:
        total += 1
        if r.x1 > W or r.x0 < 0:
            offpage.append(pno + 1)
        elif r.x0 > left + 2 and r.x1 < right - 2:
            inside.append(pno + 1)
print("notes:", total, "| inside the text block on pages:", inside[:30], len(inside), "| off the page:", offpage[:30], len(offpage))
