"""More English context for the pilot's doubtful "already" decisions (plain substring search)."""
import re
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")
import ega_sol_pilot as S  # noqa: E402

txt = S.BATCH.read_text(encoding="utf-8")
en = re.sub(r"(?ms)^----- French corrections on page.*?(?=^=================== PAGE|\Z)", "", txt)
for label, k, before, after in (("12302/12304", "transcendence", 200, 200), ("12302b", "deg", 60, 60),
                                ("17135", "mathfrak m_\\alpha'", 250, 150), ("17135b", "A'}", 120, 60),
                                ("18079", "universally open at all points of $X_y$ (or", 900, 50),
                                ("8604-8610", "p+q=n+1", 500, 300)):
    p = en.find(k)
    n = 0
    print(f"## {label}: {k}")
    while p >= 0 and n < 3:
        print("   ", repr(en[max(0, p - before):p + len(k) + after]))
        n += 1
        p = en.find(k, p + 1)
