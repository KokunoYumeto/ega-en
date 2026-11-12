"""Second automatic round for the English hand list (PORT_EN_HAND.json), before the agents.

1. Reference typography: items whose whole change is a bold chapter number in a reference or an upright parenthesis
   around references are covered by en_global_refs.py (outcome "global").
2. The window search of port_fixes_to_en.py, on normalized text: French label keys lose their "-fr" suffix, the English
   macros are expanded (\\kres -> \\boldsymbol{k}, \\sh{F} -> \\mathscr{F}, \\bb{A} -> \\mathbf{A}, ...), and a one-letter
   argument loses its braces on both sides (\\mathscr{F} = \\mathscr F). A window found in the normalized English is
   replaced in the original only if it starts and ends at a whole unit (never inside an expanded macro); the
   replacement is the French corrected text (normalized), which renders the same.
   A replacement may use only control sequences the English edition already uses.

Outcomes (PORT_EN_LOG2.jsonl, keyed by the FIXLOG_CURRENT entry): global, applied, already, hand.
The items left go to PORT_EN_HAND2.json for the agents.

usage: python -I port_hand_auto.py [--apply]
"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BS = chr(92)
E = pathlib.Path(r"user\Documents\ega_scan_check_20261101")
EN = E / "ega-en" / "tex"
apply = "--apply" in sys.argv
MARK = re.compile(re.escape(BS) + r"oldpage\[([^\]]+)\]\{(\d+)\}")
NUM = r"(?:0|I|II|III|IV)"

# ---------------------------------------------------------------- 1. reference typography only
def unwrap_textup_refs(s):
    """Remove \\textup{...} around a parenthesis made of references only."""
    out, i = [], 0
    key = BS + "textup{"
    while True:
        k = s.find(key, i)
        if k < 0:
            out.append(s[i:])
            return "".join(out)
        depth, j = 1, k + len(key)
        while j < len(s) and depth:
            if s[j] == "\\":
                j += 2
                continue
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            j += 1
        inner = s[k + len(key):j - 1]
        bare = re.sub(re.escape(BS) + r"(?:hyperref|sref|ref\*?|eref|eqref)(?:\[[^\]]*\])?(?:\{[^{}]*\})?", "", inner)
        bare = re.sub(re.escape(BS) + r"[A-Za-z]+", "", bare)
        letters = re.sub(r"\b(?:et|and|ou|or|resp|cf|loc|cit|no|n)\b", "", bare)
        if depth == 0 and inner.startswith("(") and inner.rstrip(".,;").endswith(")") and not re.search(r"[A-Za-zÀ-ÿ]{2,}", letters):
            out.append(s[i:k])
            out.append(inner)
            i = j
        else:
            out.append(s[i:k + len(key)])
            i = k + len(key)


def refs_norm(s):
    s = unwrap_textup_refs(s)
    s = re.sub(re.escape(BS) + r"textbf\{(" + NUM + r")\}", r"\1", s)
    s = re.sub(re.escape(BS) + r"mathbf\{0\}_", "0_", s)
    s = re.sub(re.escape(BS) + r"mathbf\{0_", "{0_", s)
    s = s.replace(BS + "mdseries ", "")
    return s


def refs_only(old, new):
    return old != new and refs_norm(old) == refs_norm(new)


# ---------------------------------------------------------------- 2. normalization with a position map
ALIAS = {  # English macro -> expansion
    "kres": BS + "boldsymbol{k}", "vphi": BS + "varphi", "HH": BS + "mathrm{H}", "RR": BS + "mathrm{R}",
    "LL": BS + "mathrm{L}", "red": BS + "mathrm{red}", "emp": BS + "varnothing", "bbGamma": BS + "boldsymbol{" + BS + "Gamma}",
    "shHom": BS + "mathscr{H}" + BS + "!" + BS + "mathit{om}", "shExt": BS + "mathscr{E}" + BS + "!" + BS + "mathit{xt}",
    "shTor": BS + "mathscr{T}" + BS + "!" + BS + "mathit{or}", "CHH": BS + "check{" + BS + "mathrm{H}}",
}
ARGALIAS = {"sh": "mathscr", "bb": "mathbf", "cat": "mathbf"}
ONELETTER = {"mathscr", "mathbf", "mathcal", "mathfrak", "mathrm", "boldsymbol", "mathit", "mathsf", "mathbb",
             "widetilde", "tilde", "overline", "bar", "hat", "widehat", "check", "underline", "textbf", "textit", "emph"}
UNIT = re.compile(re.escape(BS) + r"([A-Za-z]+)(\s*)(\{([A-Za-z0-9])\}|\{((?:[^{}]|\{[^{}]*\})*)\})?|" + re.escape(BS) + r".|.", re.S)


def norm_units(t, english):
    """Split t into units (start, end, normalized text)."""
    units = []
    pos, n = 0, len(t)
    while pos < n:
        m = UNIT.match(t, pos)
        s, e = m.start(), m.end()
        pos = e
        g = m.group(0)
        name = m.group(1)
        if name is None:
            units.append((s, e, g))
            continue
        arg1, argn = m.group(4), m.group(5)
        if english and name in ALIAS and m.group(3) is None:
            units.append((s, e, ALIAS[name]))
            continue
        if english and name in ALIAS and m.group(3) is not None:  # \kres{...}?: keep the argument separate
            units.append((s, m.start(2), ALIAS[name]))
            for k in range(m.start(2), e):
                units.append((k, k + 1, t[k]))
            continue
        cname = ARGALIAS.get(name, name) if english else name
        if m.group(3) is None:
            if cname in ONELETTER and e < n and t[e].isascii() and t[e].isalnum():
                units.append((s, e + 1, BS + cname + " " + t[e]))  # \boldsymbol k: the command takes the letter
                pos = e + 1
                continue
            units.append((s, e, BS + cname + m.group(2)))
            continue
        if arg1 is not None and cname in ONELETTER:
            units.append((s, e, BS + cname + " " + arg1))
            continue
        # a command with a longer argument: the command name is one unit, the argument characters follow
        units.append((s, m.start(3) + 1, BS + cname + "{"))
        inner_start = m.start(3) + 1
        sub = norm_units(t[inner_start:e - 1], english)
        units.extend((inner_start + a, inner_start + b, x) for a, b, x in sub)
        units.append((e - 1, e, "}"))
    return units


def norm_fr(s):
    s = re.sub(r"(" + re.escape(BS) + r"(?:hyperref|label|ref\*?|eqref|sref|egalabel)(?:\[[^\]]*\])?[\[{][^\]}]*?)-fr([\]}])", r"\1\2", s)
    return "".join(x for _, _, x in norm_units(s, english=False))


class NormText:
    def __init__(self, t):
        self.t = t
        self.units = norm_units(t, english=True)
        parts, self.ustart, self.uend = [], {}, {}
        pos = 0
        for i, (s, e, x) in enumerate(self.units):
            self.ustart[pos] = s
            parts.append(x)
            pos += len(x)
            self.uend[pos] = e
        self.n = "".join(parts)

    def to_orig(self, a, b):
        if a in self.ustart and b in self.uend:
            return self.ustart[a], self.uend[b]
        return None


# ---------------------------------------------------------------- English and French texts
def segments(text):
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
en_norm = {}
en_csnames = set()
for f, t in en_text.items():
    en_csnames.update(re.findall(re.escape(BS) + r"([A-Za-z]+)", t))
en_csnames.update(ALIAS)
for v in ALIAS.values():
    en_csnames.update(re.findall(re.escape(BS) + r"([A-Za-z]+)", v))


def norm_of(f):
    if f not in en_norm:
        en_norm[f] = NormText(en_text[f])
    return en_norm[f]


def en_regions(part, page, pages=None):
    """Normalized English regions of pages page-1..page+1 (or the given pages): (file, nstart, nend)."""
    regs = []
    for f in en_files:
        if f not in seg_cache:
            nt = norm_of(f)
            starts = sorted(nt.ustart.items(), key=lambda kv: kv[1])
            seg_cache[f] = (segments(en_text[f]), starts, sorted(nt.uend.items(), key=lambda kv: kv[1]))
        segs, starts, ends = seg_cache[f]
        for p in (pages or (page - 1, page, page + 1)):
            for s, e in segs.get((part, p), []):
                # normalized positions of the original span
                ns = next((k for k, v in starts if v >= s), None)
                ne = None
                for k, v in ends:
                    if v <= e:
                        ne = k
                    else:
                        break
                if ns is not None and ne is not None and ns < ne:
                    regs.append((f, ns, ne))
    return regs


seg_cache = {}


FR_ROOT = E / "ega-fr" / "editions" / "2026-10-24-r20" / "current" / "packages"
fr_files = sorted(FR_ROOT.glob("*/native/**/*.tex"))
fr_cache = {}


def fr_near_text(part, page):
    out = []
    for f in fr_files:
        if f not in fr_cache:
            t = f.read_text(encoding="utf-8")
            fr_cache[f] = (t, segments(t))
        t, segs = fr_cache[f]
        for p in (page - 1, page, page + 1):
            out.extend(t[s:e] for s, e in segs.get((part, p), []))
    return norm_fr("\n".join(out))


BREAK = set(" \n\t{}$()[],.;:=+-^_~'\\")


def boundaries(s):
    inside = set()
    for m in re.finditer(r"\\(?:[A-Za-z]+|.)", s, re.S):
        inside.update(range(m.start() + 1, m.end()))
    for m in re.finditer(r"\\(?:begin|end|label|ref|eqref|hyperref|sref|SGARefLink|egalabel)(?:\[[^\]]*\])?\{[^}]*\}", s):
        inside.update(range(m.start() + 1, m.end()))  # never split an environment name or a label
    for m in re.finditer(r"\\(?:hyperref|sref)\[[^\]]*\]", s):
        inside.update(range(m.start() + 1, m.end()))
    return [k for k in range(len(s) + 1) if k not in inside
            and (k == 0 or k == len(s) or s[k - 1] in BREAK or s[k] in BREAK)]


ENVNAME = re.compile(r"\\(?:begin|end)\{([^}]*)\}")


def renames_environment(old, new):
    """The fix changes the name of an environment (remark -> remarks): its \\begin and \\end must change together."""
    return sorted(ENVNAME.findall(old)) != sorted(ENVNAME.findall(new))


STRUCT = re.compile(r"\\begin\{[^}]*\}|\\end\{[^}]*\}|\\\[|\\\]|\\\(|\\\)|(?<!\\)\$|\\item\b|&|\\\\|\\oldpage")


def structure_kept(w_old, w_new):
    if STRUCT.findall(w_old) != STRUCT.findall(w_new):
        return False
    d = lambda w: w.count("{") - w.count("}") - (w.count("\\{") - w.count("\\}"))
    return d(w_old) == d(w_new)


def texy(w):
    return "\\" in w or "$" in w or any(c.isdigit() for c in w)


KEYS = re.compile(r"\\(?:sref|ref\*?|eqref|label|egalabel|EGAReaderTarget|cite|egabib|href|url|begin|end)"
                  r"(?:\[[^\]]*\])?(?:\{[^{}]*\}){1,2}|\\hyperref\[[^\]]*\]|\\sref\[[^\]]*\]")
prot_cache = {}


def protected(f):
    """Spans of the English file that are link keys, labels or environment names."""
    if f not in prot_cache:
        prot_cache[f] = [(m.start(), m.end()) for m in KEYS.finditer(en_text[f])]
    return prot_cache[f]


def count_in(regs, w):
    hits = []
    for f, s, e in regs:
        nt = norm_of(f)
        seg = nt.n[s:e]
        start = 0
        while True:
            k = seg.find(w, start)
            if k < 0:
                break
            span = nt.to_orig(s + k, s + k + len(w))
            if span and not any(ps < span[1] and span[0] < pe and not (span[0] <= ps and pe <= span[1])
                                for ps, pe in protected(f)):
                hits.append((f, span))  # a hit may contain a whole key, never cut into one
            start = k + 1
    return hits


def same_change(w_old, w_new, near_entries):
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
        if b - a < 6 or not w_old.strip() or not structure_kept(w_old, w_new):
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


def find_already(old, new, regs, budget=300):
    """A window of the corrected French (new) that contains the whole change, occurs in the English, while the
    matching window of the uncorrected French (old) is at least 4 characters long, contains TeX or digits, and
    occurs nowhere in the English regions: the English already has the corrected reading."""
    p = 0
    while p < min(len(old), len(new)) and old[p] == new[p]:
        p += 1
    q = 0
    while q < min(len(old), len(new)) - p and old[-1 - q] == new[-1 - q]:
        q += 1
    lo, hi = p, len(new) - q
    bnd = boundaries(new)
    left = [k for k in bnd if k <= lo][::-1]
    right = [k for k in bnd if k >= hi]
    frontier, seen = [(0, 0)], set()
    while frontier and budget > 0:
        i, j = frontier.pop(0)
        if (i, j) in seen or i >= len(left) or j >= len(right):
            continue
        seen.add((i, j))
        a, b = left[i], right[j]
        w_new = new[a:b]
        w_old = old[a:len(old) - (len(new) - b)]
        budget -= 1
        if len(w_new.strip()) >= 6 and len(w_old.strip()) >= 4 and texy(w_old) and structure_kept(w_new, w_old):
            hits = count_in(regs, w_new)
            if hits:
                if not count_in(regs, w_old):
                    return w_new, w_old, hits
                frontier += [(i + 1, j), (i, j + 1)]
                continue
            continue  # the window does not occur: no larger one can
        frontier += [(i + 1, j), (i, j + 1)]
    return None


# ---------------------------------------------------------------- main
hand = json.loads((E / "PORT_EN_HAND.json").read_text(encoding="utf-8"))
only = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")]
if only:
    want = {int(v) for v in only[0].split(",")}
    hand = [x for x in hand if x["entry"] in want]
    apply = False
fixlog = {}
for n, line in enumerate(open(E / "FIXLOG_CURRENT.jsonl", encoding="utf-8"), 1):
    if line.strip():
        fixlog[n] = json.loads(line)
fr_entries = collections.defaultdict(list)
for n, x in fixlog.items():
    fr_entries[(x.get("part") or "I", int(x["page"]))].append((norm_fr(x["old"]), norm_fr(x["new"])))

stats = collections.Counter()
left, logrecs = [], []
changed = set()
for x in hand:
    part, page = x["part"], int(x["page"])
    rec = dict(entry=x["entry"], part=part, page=page)
    if refs_only(x["old"], x["new"]):
        rec["outcome"] = "global"
    elif renames_environment(x["old"], x["new"]):
        rec["outcome"] = "hand"
        rec["note"] = "environment renamed: \\begin and \\end together"
    else:
        old, new = norm_fr(x["old"]), norm_fr(x["new"])
        regs = en_regions(part, page)
        outcome = "hand"
        if regs and old != new:
            near = [e for p in (page - 1, page, page + 1) for e in fr_entries.get((part, p), [])]
            found = find_window(old, new, regs, fr_near_text(part, page), near)
            if found:
                w_old, w_new, hits = found
                cs = set(re.findall(re.escape(BS) + r"([A-Za-z]+)", w_new))
                if cs <= en_csnames:
                    rec.update(en_file=hits[0][0].name, window_old=w_old, window_new=w_new, occurrences=len(hits))
                    if apply:
                        for f, (a, b) in sorted(hits, key=lambda h: (str(h[0]), h[1][0]), reverse=True):
                            t = en_text[f]
                            rep = w_new
                            if rep[:1].isalpha() and re.search(r"\\[A-Za-z]+$", t[:a]):
                                rep = " " + rep
                            if re.search(r"\\[A-Za-z]+$", rep) and t[b:b + 1].isalpha():
                                rep = rep + " "
                            en_text[f] = t[:a] + rep + t[b:]
                            changed.add(f)
                            en_norm.pop(f, None)
                            seg_cache.pop(f, None)
                            prot_cache.pop(f, None)
                    outcome = "applied"
                else:
                    rec["note"] = "unknown control sequences " + ",".join(sorted(cs - en_csnames))
            else:
                # the English already has the corrected reading: on the page itself, or on the three pages
                for rg in (en_regions(part, page, (page,)), regs):
                    back = find_already(old, new, rg) if rg else None
                    if back:
                        outcome = "already"
                        rec.update(window_new_found=back[0], window_old_absent=back[1])
                        break
        rec["outcome"] = outcome
    stats[rec["outcome"]] += 1
    logrecs.append(rec)
    if only:
        o, nw = norm_fr(x["old"]), norm_fr(x["new"])
        print("ITEM", x["entry"], repr(o), "->", repr(nw), rec)
        rg = en_regions(part, page, (page,))
        for f, s, e in rg:
            seg = norm_of(f).n[s:e]
            for needle in (o, nw):
                core = needle.strip()[:12]
                k = seg.find(core)
                print("   ", f.name, "needle", repr(core), "found at", k, repr(seg[max(0, k - 40):k + 60]) if k >= 0 else "")
    if rec["outcome"] == "hand":
        left.append(x)

print(("applied" if apply else "dry run"), dict(stats), "left", len(left))
ex = collections.defaultdict(list)
for r in logrecs:
    if len(ex[r["outcome"]]) < 5 and r["outcome"] in ("applied", "already"):
        ex[r["outcome"]].append((r["part"], r["page"], r.get("window_old", "")[:60], r.get("window_new", "")[:60]))
for k, v in ex.items():
    print(k)
    for e in v:
        print("   ", e)
if apply:
    for f in changed:
        f.write_text(en_text[f], encoding="utf-8", newline="")
    with open(E / "PORT_EN_LOG2.jsonl", "a", encoding="utf-8") as fh:
        for r in logrecs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (E / "PORT_EN_HAND2.json").write_text(json.dumps(left, ensure_ascii=False, indent=1), encoding="utf-8")
