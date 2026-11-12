"""Contact sheets of selected embedded images of a PDF, to look at figure crops: each cell shows one image scaled to
fit, with a 1-pixel red frame drawn just outside the image so a cut at its edge is visible, and a label.
usage: python -X utf8 -B image_sheets.py PDF OUTDIR PAGE:XREF [PAGE:XREF ...]"""
import io
import pathlib
import sys

import fitz
from PIL import Image, ImageDraw

pdf, out = fitz.open(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
items = [tuple(int(x) for x in a.split(":")) for a in sys.argv[3:]]
CW, CH, COLS, ROWS = 560, 300, 2, 3
for s in range(0, len(items), COLS * ROWS):
    sheet = Image.new("RGB", (COLS * CW, ROWS * CH), "white")
    draw = ImageDraw.Draw(sheet)
    for k, (page, xref) in enumerate(items[s:s + COLS * ROWS]):
        pix = fitz.Pixmap(pdf, xref)
        if pix.n - pix.alpha > 3 or pix.colorspace and pix.colorspace.n > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        im.thumbnail((CW - 24, CH - 34))
        cx, cy = (k % COLS) * CW, (k // COLS) * CH
        x0, y0 = cx + 12, cy + 24
        sheet.paste(im, (x0, y0))
        draw.rectangle([x0 - 1, y0 - 1, x0 + im.width, y0 + im.height], outline="red")
        draw.text((cx + 12, cy + 6), "page %d  xref %d" % (page, xref), fill="black")
    sheet.save(out / ("sheet_%02d.png" % (s // (COLS * ROWS) + 1)))
print("sheets:", (len(items) + COLS * ROWS - 1) // (COLS * ROWS))
