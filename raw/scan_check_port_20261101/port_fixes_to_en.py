"""Carry the French scan-check fixes (corrected edition, FIXLOG_CURRENT.jsonl) into the English EGA (ega-en clone).

Both editions carry the same printed-page markers \\oldpage[PART]{N}. For each French fix the script looks for a window
of the French "old" text that contains the whole change, occurs exactly once in the English text of the same printed
page (or the page before or after, together), and no longer occurs on the French page. That window is replaced by the
matching window of "new". Formulas, references and notation transfer this way; French wording does not match the
English and goes to the hand list.

Outcomes per entry (PORT_EN_LOG.jsonl, keyed by the entry's line number in FIXLOG_CURRENT.jsonl):
  applied   the window was replaced in the English
  already   the English already has the new reading
  marker    the fix moves a French page marker or blank lines (layout of the French text; not carried over)
  hand      no safe window: listed in PORT_EN_HAND.json for an agent (wording, ambiguous or missing passages)
Entries already in the log are skipped, so the script can be rerun after more French fixes.

usage: python -I port_fixes_to_en.py [--apply] [--parts=IV-2,IV-3] [--max-lines=N]
Without --apply nothing is written except the summary on stdout.
"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
EN = E / "ega-en" / "tex"
LOG = E / "PORT_EN_LOG.jsonl"
HAND = E / "PORT_EN_HAND.json"
apply = "--apply" in sys.argv
parts_arg = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--parts=")]
only_parts = set(parts_arg[0].split(",")) if parts_arg else None
max_lines = [int(a.split("=", 1)[1]) for a in sys.argv[1:] if a.startswith("--max-lines=")]
MARK = re.compile(r"\\oldpage\[([^\]]+)\]\{(\d+)\}")
MIN_WINDOW = 6


def segments(text):
    """(part, page) -> list of (start, end) spans; the text before the first marker continues the previous page."""
    out = collections.defaultdict(list)
    ms = list(MARK.finditer(text))
    if ms:
        out[(ms[0].group(1), int(ms[0].group(2)) - 1)].append((0, ms[0].start()))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out[(m.group(1), int(m.group(2)))].append((m.start(), end))
    return out


en_files = sorted(EN.rglob("*.tex"))
en_text = {f: f.read_text(encoding="utf-8") for f in en_files}
en_segs = {f: segments(t) for f, t in en_text.items()}
fr_cache = {}


def en_regions(part, page):
    regs = []
    for p in (page - 1, page, page + 1):
        for f in en_files:
            for s, e in en_segs[f].get((part, p), []):
                regs.append((f, s, e))
    return regs


FR_ROOT = E / "ega-fr" / "editions" / "2026-10-24-r20" / "current" / "packages"
fr_files = sorted(FR_ROOT.glob("*/native/**/*.tex"))  # not the assembled readers in */direct, which lag behind


def fr_near_text(part, page):
    """Corrected French text of pages page-1 .. page+1 of the part, from every file of the corrected edition."""
    out = []
    for f in fr_files:
        if f not in fr_cache:
            t = f.read_text(encoding="utf-8")
            fr_cache[f] = (t, segments(t))
        t, segs = fr_cache[f]
        for p in (page - 1, page, page + 1):
            out.extend(t[s:e] for s, e in segs.get((part, p), []))
    return "\n".join(out)


BREAK = set(" \n\t{}$()[],.;:=+-^_~'\\")


def boundaries(s):
    """Positions where a window may start or end: next to a space, brace, dollar or punctuation sign, and not inside
    a control word."""
    inside = set()
    for m in re.finditer(r"\\(?:[A-Za-z]+|.)", s, re.S):  # control words and control symbols such as \, or \\
        inside.update(range(m.start() + 1, m.end()))
    for m in re.finditer(r"\\(?:begin|end|label|ref|eqref|hyperref|SGARefLink|egalabel)(?:\[[^\]]*\])?\{[^}]*\}", s):
        inside.update(range(m.start() + 1, m.end()))  # never split an environment name or a label
    return [k for k in range(len(s) + 1) if k not in inside
            and (k == 0 or k == len(s) or s[k - 1] in BREAK or s[k] in BREAK)]


def texy(w):
    return "\\" in w or "$" in w or any(c.isdigit() for c in w)


STRUCT = re.compile(r"\\begin\{[^}]*\}|\\end\{[^}]*\}|\\\[|\\\]|\\\(|\\\)|(?<!\\)\$|\\item\b|&|\\\\|\\oldpage")


def structure_kept(w_old, w_new):
    """True if the edit keeps environments, math delimiters, items, alignment marks and brace balance: such edits
    can be transferred to the English without knowing how the translation is laid out."""
    if STRUCT.findall(w_old) != STRUCT.findall(w_new):
        return False
    depth_old = w_old.count("{") - w_old.count("}") - (w_old.count("\\{") - w_old.count("\\}"))
    depth_new = w_new.count("{") - w_new.count("}") - (w_new.count("\\{") - w_new.count("\\}"))
    return depth_old == depth_new


def same_change(w_old, w_new, near_entries):
    """How many occurrences of w_old the French fixes of these pages turned into w_new; None if some fix turned
    w_old into something else (then the English occurrences cannot be matched to the French ones)."""
    n = 0
    for o, nw in near_entries:
        if w_old not in o:
            continue
        if o.replace(w_old, w_new) == nw or (w_new in nw and nw.count(w_new) - o.count(w_new) >= o.count(w_old)):
            n += o.count(w_old)
        else:
            return None
    return n


def find_window(old, new, regs, fr_near=None, near_entries=(), budget=300, multi_ok=False):
    """Smallest-first search for a window of old that contains the whole change and occurs in the English regions,
    while the corrected French text of the same pages (fr_near) no longer contains it. A window made of TeX, formulas
    or numbers may occur several times (the French changed every occurrence on these pages, so the English follows);
    a plain-text window must occur exactly once. Returns (w_old, w_new, hits) or None. Without fr_near (the reverse
    check for "already"), exactly one occurrence is required. A window that does not occur in the English is not
    grown further: no larger window can occur either."""
    p = 0
    while p < min(len(old), len(new)) and old[p] == new[p]:
        p += 1
    q = 0
    while q < min(len(old), len(new)) - p and old[-1 - q] == new[-1 - q]:
        q += 1
    lo, hi = p, len(old) - q
    bnd = boundaries(old)
    left = [k for k in bnd if k <= lo][::-1]
    right = [k for k in bnd if k >= hi]
    frontier, seen = [(0, 0)], set()
    while frontier and budget > 0:
        i, j = frontier.pop(0)
        if (i, j) in seen or i >= len(left) or j >= len(right):
            continue
        seen.add((i, j))
        a, b = left[i], right[j]
        w_old = old[a:b]
        w_new = new[a:len(new) - (len(old) - b)]
        if b - a < MIN_WINDOW or not w_old.strip() or not structure_kept(w_old, w_new):
            frontier += [(i + 1, j), (i, j + 1)]
            continue
        budget -= 1
        hits = count_in(regs, w_old)
        if not hits:
            continue
        if fr_near is None:
            if len(hits) == 1 or (multi_ok and texy(w_old)):
                return w_old, w_new, hits
        elif w_old not in w_new and w_old not in fr_near and (len(hits) == 1 or texy(w_old)):
            done_fr = same_change(w_old, w_new, near_entries)
            if done_fr is not None and len(hits) <= done_fr:
                return w_old, w_new, hits
        frontier += [(i + 1, j), (i, j + 1)]
    return None


def clean_cut(t, k, w):
    """The occurrence of w at position k of t neither starts nor ends inside a TeX control word or symbol."""
    before, after = t[:k], t[k + len(w):]
    if len(before) - len(before.rstrip("\\")) % 2 == 1 or before.endswith("\\"):
        return False
    if w[:1].isalpha() and re.search(r"\\[A-Za-z]+$", before):
        return False
    if re.search(r"\\[A-Za-z]+$", w) and after[:1].isalpha():
        return False
    return True


KEYS = re.compile(r"\\(?:sref|ref\*?|eqref|label|egalabel|EGAReaderTarget|cite|egabib|href|url)(?:\[[^\]]*\])?"
                  r"(?:\{[^{}]*\}){1,2}|\\hyperref\[[^\]]*\]")
en_prot = {}


def protected(f):
    """Spans of the English file whose text is a link key or label (\\sref uses its argument as a key)."""
    if f not in en_prot:
        en_prot[f] = [(m.start(), m.end()) for m in KEYS.finditer(en_text[f])]
    return en_prot[f]


def count_in(regs, w):
    hits = []
    for f, s, e in regs:
        t = en_text[f]
        seg = t[s:e]
        prot = protected(f)
        start = 0
        while True:
            k = seg.find(w, start)
            if k < 0:
                break
            a, b = s + k, s + k + len(w)
            if clean_cut(t, a, w) and not any(ps < b and a < pe for ps, pe in prot):
                hits.append((f, a))
            start = k + 1
    return hits


done = set()
if LOG.exists():
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.strip():
            done.add(json.loads(line)["entry"])
entries = []
for n, line in enumerate(open(E / "FIXLOG_CURRENT.jsonl", encoding="utf-8"), 1):
    if line.strip():
        entries.append((n, json.loads(line)))
if max_lines:
    entries = [(n, x) for n, x in entries if n <= max_lines[0]]
fr_entries = collections.defaultdict(list)  # (part, page) -> [(old, new)] of all corrected-edition fixes
for n, x in entries:
    fr_entries[(x.get("part") or "I", int(x["page"]))].append((x["old"], x["new"]))

stats = collections.Counter()
by_part = collections.defaultdict(collections.Counter)
hand = json.loads(HAND.read_text(encoding="utf-8")) if HAND.exists() else []
log_out = open(LOG, "a", encoding="utf-8") if apply else None
changed_files = set()
dry_recs = []
for n, x in entries:
    if n in done:
        continue
    part, page, old, new = x.get("part") or "I", int(x["page"]), x["old"], x["new"]
    if only_parts and part not in only_parts:
        continue
    rec = dict(entry=n, part=part, page=page, file=pathlib.Path(x["file"].replace("\\", "/")).name)
    if "\\oldpage" in old or "\\oldpage" in new or re.sub(r"\s+", "", old) == re.sub(r"\s+", "", new):
        outcome = "marker"
    else:
        regs = en_regions(part, page)
        fr_near = fr_near_text(part, page)
        near_entries = [e for p in (page - 1, page, page + 1) for e in fr_entries.get((part, p), [])]
        outcome = "hand"
        if regs:
            found = find_window(old, new, regs, fr_near, near_entries)
            if found:
                w_old, w_new, hits = found
                f, k = hits[0]
                rec.update(en_file=f.name, en_line=en_text[f].count("\n", 0, k) + 1, window_old=w_old,
                           window_new=w_new, occurrences=len(hits))
                if apply:
                    for f, k in sorted(hits, key=lambda h: (str(h[0]), h[1]), reverse=True):
                        t = en_text[f]
                        rep = w_new
                        # keep a control word before or after the edit from running into a letter (\noindent I)
                        if rep[:1].isalpha() and re.search(r"\\[A-Za-z]+$", t[:k]):
                            rep = " " + rep
                        if re.search(r"\\[A-Za-z]+$", rep) and t[k + len(w_old):k + len(w_old) + 1].isalpha():
                            rep = rep + " "
                        en_text[f] = t[:k] + rep + t[k + len(w_old):]
                        changed_files.add(f)
                    for f in {h[0] for h in hits}:
                        en_segs[f] = segments(en_text[f])
                        en_prot.pop(f, None)
                outcome = "applied"
            else:
                back = find_window(new, old, regs, multi_ok=True)
                if back and not count_in(regs, back[1]):
                    outcome = "already"
        else:
            rec["note"] = "no English text for this page"
    rec["outcome"] = outcome
    dry_recs.append(dict(rec, old=old, new=new))
    stats[outcome] += 1
    by_part[part][outcome] += 1
    if outcome == "hand":
        hand.append(dict(rec, old=old, new=new, kind=x.get("kind"), why=x.get("why"), fr_file=x["file"]))
    if log_out:
        log_out.write(json.dumps(rec, ensure_ascii=False) + "\n")

if apply:
    for f in changed_files:
        f.write_text(en_text[f], encoding="utf-8", newline="")
    HAND.write_text(json.dumps(hand, ensure_ascii=False, indent=1), encoding="utf-8")
else:
    (E / "PORT_EN_DRYRUN.json").write_text(json.dumps(dry_recs, ensure_ascii=False, indent=1), encoding="utf-8")
print(("applied" if apply else "dry run"), dict(stats))
for part, c in sorted(by_part.items()):
    print(f"  {part:24s} {dict(c)}")
