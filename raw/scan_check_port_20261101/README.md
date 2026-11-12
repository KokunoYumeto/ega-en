# Carrying the corrections of the French EGA into the English (3–9 November 2026): records

From 1 to 5 November 2026 the French transcription of EGA ([ega-fr](https://github.com/KokunoYumeto/ega-fr)) was
checked page by page against the Numdam scans of the printed volumes; its records are in ega-fr,
`raw/scan_check_20261101/`. This folder holds the records of carrying those corrections into this English edition.
`METHODOLOGY.md` (§ 3) describes the method in full.

## How

Both editions carry the same printed-page markers (`\oldpage`), so each French correction can be located on the same
printed page of the English.

1. **Automatic port** (`port_fixes_to_en.py`, log `PORT_EN_LOG.jsonl`): the smallest window of the French change that
   occurs exactly once on the English pages p−1..p+1 is replaced by the matching window of the corrected French.
   Formulas, references and notation transfer this way; French wording does not.
2. **Layout and reference typography by rule** (`port_displays_to_en.py`, `match_inline_layout_en.py`,
   `en_global_refs.py`, `en_ref_syntax.py`, `en_kres.py`, `en_ch0_subscripts.py`, `en_item_refs.py`,
   `en_final_fixes.py`, with their logs `EN_*.jsonl`, `PORT_EN_DISPLAY_LOG.jsonl`, `PORT_EN_INLINE_LAYOUT.jsonl`).
3. **Second automatic round** on normalized text (`port_hand_auto.py`, `PORT_EN_LOG2.jsonl`).
4. **Agent hand pass**: Claude Opus 5.5 subagents in Claude Code, prompt `PORT_EN_AGENT_PROMPT.txt`, batches in
   `port_en_batches/`, decisions applied by `apply_port_decisions.py` (`PORT_EN_LOG3.jsonl`; items left:
   `PORT_EN_LEFT3.json`). An audit of the "already right" outcomes: `audit_already_en.py`, `AUDIT_ALREADY_EN*.json`.
5. **Translation slips** found on the way (`ENGLISH_SLIPS.md`): fixed by Claude Opus 5.5 subagents with
   `SLIPS_AGENT_PROMPT.txt`, logs in `slips/`. `FAITHFULNESS_TODO.md` records why the whole English needs a
   paragraph-by-paragraph faithfulness reading.
6. **Typographic corrections, 9 November** (`sol_pilot_20261109/`, `sol_bulk_20261109/`): GPT-6.1 Sol (OpenAI, API,
   effort max, flex tier) decided the remaining italic/upright items in batches; its answers were audited by script
   (`sol_bulk_20261109/AUDIT.md`) before they were applied.

## Where the corrections went

Commits 6a6aa10 (3 Nov), 10e1119 and b83bfde (5 Nov), 9e13cf2 (5 Nov, misprints of the print) and 6aaedc5
(9 Nov, 3,557 typographic corrections).

## Not included

Page images and PDFs; runs marked `*_reverted` and `*.discarded_*` are kept as the record of what was undone. 43
record files that quote long passages of the English text (27 batch files of `port_en_batches/`, 15 files of the
9 November runs and `ega_en_port_diff.txt`) are not published here. Local paths are rewritten (`user`).

## Rights

The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights,
in the AI-produced translation, corrections, records and typesetting, they are dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). This edition is published for educational,
non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its
publication here, please open a GitHub issue and we will take it down.
