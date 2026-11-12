"""Find embedded images (figure crops from scans) that are probably clipped: ink touching an edge of the image.
For each image placed on a page: the share of dark pixels in the outermost 3-pixel band of each side; a band with
noticeably more ink than a clean margin has means the crop cut through the figure on that side.
usage: python -X utf8 -B clipped_images.py PDF [threshold=0.02]"""
import sys

import fitz

path = sys.argv[1]
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02
d = fitz.open(path)
seen, hits, total = set(), [], 0
for i in range(d.page_count):
    for img in d[i].get_images(full=True):
        xref = img[0]
        if xref in seen:
            continue
        seen.add(xref)
        pix = fitz.Pixmap(d, xref)
        if pix.n - pix.alpha > 1:
            pix = fitz.Pixmap(fitz.csGRAY, pix)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        w, h = pix.width, pix.height
        if w < 40 or h < 40:
            continue
        total += 1
        s = pix.samples
        stride = pix.stride

        def dark(x0, y0, x1, y1):
            n = k = 0
            for y in range(y0, y1):
                row = s[y * stride:(y + 1) * stride]
                for x in range(x0, x1):
                    n += 1
                    k += row[x] < 110
            return k / max(n, 1)

        b = 3
        sides = {"top": dark(0, 0, w, b), "bottom": dark(0, h - b, w, h), "left": dark(0, 0, b, h),
                 "right": dark(w - b, 0, w, h)}
        bad = {k: round(v, 3) for k, v in sides.items() if v > thr}
        if bad:
            hits.append((i + 1, xref, w, h, bad))
print("%s: %d images, %d with ink at an edge" % (path.split("/")[-1], total, len(hits)))
for h in hits:
    print("  page %d  xref %d  %dx%d  %s" % h)
