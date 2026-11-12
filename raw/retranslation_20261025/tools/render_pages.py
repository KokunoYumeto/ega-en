"""Render selected PDF pages (1-based) to PNG for a visual check.
usage: python -X utf8 -B render_pages.py PDF OUTDIR PAGE [PAGE ...]   (needs PyMuPDF, so no -I)"""
import pathlib
import sys

import fitz

pdf, out = fitz.open(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for p in sys.argv[3:]:
    page = pdf[int(p) - 1]
    page.get_pixmap(dpi=80).save(str(out / ("p%04d.png" % int(p))))
print("pages:", pdf.page_count)
