# Translating EGA from the French — instructions for each chunk

You translate chunks of Grothendieck–Dieudonné, *Éléments de géométrie algébrique*, from the French LaTeX
transcription into English LaTeX. Workspace: `user/Documents/ega_en_retranslation_20261025/`.

## Input and output

- Input: `fr/<chunk>.fr.tex` (French LaTeX). Read it completely (use offset/limit for long files).
- Output: `en/<chunk>.en.tex` — the same LaTeX, with the French prose translated into English. Write it with the
  Write tool; for a long chunk, build it in a few consecutive parts (write the first part, then use Edit or a second
  Write of the full text — never leave a truncated file).
- Notes: `notes/<chunk>.md` — only if there is something to note (see below). No other files.

## Rules

1. **Translate everything, faithfully.** Every sentence, in order; nothing summarized, nothing added, no
   translator's remarks in the TeX. Section and subsection titles are translated.
2. **Mathematics is copied, never retyped.** Everything inside `$…$`, `\[…\]` and display environments stays
   exactly as in the French, except French words inside `\text{…}`, which are translated.
3. **Structure is kept exactly.** Same macros (`\sh`, `\sref`, `\oldpage`, `env`, …), the same `\label` and
   reference commands with the same keys, the same environments, line breaks of displays, footnotes (their text
   translated), `\oldpage[...]{…}` markers in the same places. Do not rename labels or macros.
4. **Terminology** follows `GLOSSARY.md` (our own English EGA usage). For a term not in it, use the standard English
   term of algebraic geometry (Stacks Project, Vakil, nLab usage) and list it in your notes. Keep EGA's historical
   terms (prescheme, scheme = separated prescheme, etc.).
5. **Never consult or reuse any existing English translation of EGA**, in particular github.com/ryankeleti/ega. Translate from the French yourself.
6. **Style**: clear mathematical English, as in the EGA English we already have in `ours/` (e.g.
   `ours/ega3/ega3-2.tex`). French typography becomes English typography: « » → ``…''; `~;` and `~:` → `;` and `:`
   (no space before); "cf." stays "cf.".
7. **Do not correct the French silently.** If the French transcription looks wrong (a garbled formula, a wrong
   reference number, a missing word), translate what is there and record it in the notes.

## Notes file (only when needed)

`notes/<chunk>.md`, short lines:
- `TRANSCRIPTION?` location (env number or label) — what looks wrong in the French and why.
- `TERM` French → English — for terms not in the glossary.

## Check before you finish

Run `python -I -X utf8 -B user/Documents/ega_en_retranslation_20261025/tools/check_chunk.py <chunk>`.
It compares labels, references, environments, mathematics, `\oldpage` markers, footnotes and the length ratio.
Fix every problem it reports (unless it is a genuine French-word-in-math case, which you then mention in the
notes). Report back in at most 60 words: chunk names, OK/problems, number of notes.
