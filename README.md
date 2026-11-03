# EGA in English: Grothendieck's *Éléments de géométrie algébrique*, Chapters 0–IV

An English translation of Alexander Grothendieck's *Éléments de géométrie algébrique* (EGA, *Elements of Algebraic
Geometry*), written with the collaboration of Jean Dieudonné: the Introduction and Chapters 0–IV, first published in
the *Publications mathématiques de l'IHÉS* 4, 8, 11, 17, 20, 24, 28 and 32 (1960–1967).

## How it was made

The text is AI-translated from the French transcription in [ega-fr](https://github.com/KokunoYumeto/ega-fr):

- by Claude Opus 5.5 (Anthropic): the Introduction; Chapter 0, §§1–11 and 14; Chapter I; Chapter II with its
  errata; Chapter III, §§1 and 3; Chapter IV: its introduction, §§1, 16, 17 and 20, and the bibliography and
  indexes that close its first part;
- by OpenAI Codex models (GPT-6 Astra, GPT-5.6 Sol): the other sections.

The mathematics, the numbering and the cross-references follow the French transcription. The French transcription
is being checked page by page against the printed volumes, and the corrections from that check are carried into this
translation.

## Status

The translation is complete. Errors may remain; corrections from the check of the French transcription continue to
be carried into this translation.

## Other editions of EGA

- French: [ega-fr](https://github.com/KokunoYumeto/ega-fr): complete transcription of the original printing, in a
  diplomatic and a corrected edition.
- Spanish: [ega-fga-es](https://github.com/KokunoYumeto/ega-fga-es): EGA II, EGA III and EGA IV parts 3–4; of EGA IV
  part 1, Chapter 0 only; EGA I and EGA IV part 2 are not included.
- Brazilian Portuguese: [ega-fga-sga-pt-br](https://github.com/KokunoYumeto/ega-fga-sga-pt-br): EGA II, EGA III part 1,
  EGA IV part 3 and Chapter I of EGA I; other parts in single sections only.
- Vietnamese: [ega-fga-sga-vi](https://github.com/KokunoYumeto/ega-fga-sga-vi): EGA II, EGA III part 1 and Chapter I
  of EGA I; other parts in single sections only.
- Korean: [ega-ko](https://github.com/KokunoYumeto/ega-ko): EGA I–III; of EGA IV part 1, Chapter 0, §§14–23 and
  Chapter IV, §1.
- Chinese (Simplified): [ega-zh-hans-cn](https://github.com/KokunoYumeto/ega-zh-hans-cn): EGA I–III; of EGA IV part 1,
  Chapter 0, §§14–23 and Chapter IV, §1.

All editions of EGA, FGA and SGA made in this project are listed in
[ega-fga-sga](https://github.com/KokunoYumeto/ega-fga-sga).

## Contents

[pdf/EGA_EN.pdf](pdf/EGA_EN.pdf) is the whole translation in one PDF: the Introduction; Chapter 0, §§1–23;
Chapters I–IV; and the bibliographies, indexes, errata and addenda of the original volumes, each after the chapter it
belongs to.

- Every numbered paragraph keeps its original number, and cross-references such as (IV, 17.5.1) are links.
- The page numbers of the original printing are in the margin: [IV-2 | 19] is page 19 of the second part of
  Chapter IV.

[tex/](tex) holds the LaTeX sources of the PDF: the main file `EGA_EN.tex`, the shared preamble `ega-preamble.tex`,
and one folder per chapter (`ega0` to `ega4`, with `components` and `source_aligned` for Chapter IV). To build the
PDF, run `pdflatex EGA_EN.tex` in `tex/` until LaTeX no longer asks for a rerun.

## Sources

- The original: Alexander Grothendieck, with the collaboration of Jean Dieudonné, *Éléments de géométrie algébrique*,
  Publications mathématiques de l'IHÉS 4, 8, 11, 17, 20, 24, 28 and 32 (1960–1967), freely readable on
  [Numdam](https://www.numdam.org/journals/PMIHES/).
- The French transcription translated here: [ega-fr](https://github.com/KokunoYumeto/ega-fr).

## Rights

To the extent that the publisher holds any rights in the AI-produced translation, corrections and typesetting, they
are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). This does not
affect the rights in the original work and grants no permission to use it. Full notice: [LICENSE](LICENSE); purpose
of this edition: [PURPOSE.md](PURPOSE.md).

---

[Sponsor this work](https://github.com/sponsors/KokunoYumeto)
