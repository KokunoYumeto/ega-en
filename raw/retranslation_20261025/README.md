# The English translation from the French transcription (25 October 2026): records

On 25 October 2026 the parts of this edition that had used text of an earlier English translation (EGA 0 §§1–11 and
14; I §§1–10; II §§1–8; III §§1 and 3; the opening of IV §1; IV §16 and the openings of IV §§17 and 20) were
translated anew from the French transcription in [ega-fr](https://github.com/KokunoYumeto/ega-fr), and published in
commit ac48183. This folder holds the working records of that translation.

- `SPEC.md`: the instructions given to each translating agent (one chunk of the French each).
- `GLOSSARY.md`: the French–English glossary, taken from the usage of the rest of this edition.
- `GROUPS.json`, `LAUNCHED.json`, `MANIFEST.json`: the chunks, their French sources and the order of the work.
- `notes/`: the notes of each chunk; `TERM_NOTES.md` (terms not in the glossary) and `TRANSCRIPTION_NOTES.md`
  (196 places where the French text looked wrong, noted while translating; the page-by-page check of the French
  against the printed volumes, 1–5 November, is recorded in ega-fr, `raw/scan_check_20261101/`).
- `tools/`: the scripts that cut the French into chunks, checked each chunk (labels, environments, macros) and built
  the edition.

Translation: Claude Opus 5.5 subagents in Claude Code. Local paths are rewritten (`user`). Not included: the French
and English chunk texts (the French is in ega-fr, the English in `tex/`), build outputs, a log of rewording edits,
and some administrative scripts.

## Rights

The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights,
in the AI-produced translation, corrections, records and typesetting, they are dedicated to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). This edition is published for educational,
non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its
publication here, please open a GitHub issue and we will take it down.
