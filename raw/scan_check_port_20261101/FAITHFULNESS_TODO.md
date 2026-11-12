# English EGA: stretches that need a sentence-by-sentence faithfulness check against the French

Reported by the slips agents (5 Nov) as condensed or paraphrased beyond the items they fixed. Each needs a reading of
the English against the corrected French, paragraph by paragraph, with a faithful retranslation where it departs.
- IV 9.9.2 proof, parts (i)-(v), and probably 9.9.3 onward (slips_IV_8_11).
- 0_IV §§19-20: fixed in full by the slips agent (66 fixes incl. condensed proofs 19.3.5, 19.3.10.1, 19.3.12,
  19.5.6.4-19.5.6.7, 20.4.13 (iv), 20.5.12-20.5.13); no further check needed unless new reports.
- IV §19: 19.7.1.5 retranslated; other unlisted slips fixed (slips_IV_19).
- IV §§6-7: fixed by the slips agent (46 listed + 60 extra; retranslated 6.11.9 (i), lemma 6.14.1.2 and step III of
  6.14.1, the proof of 6.15.5, the proof of 7.5.2; repaired the proof nesting 6.11.6.1-6.14.1).
- Page markers off by a sentence or paragraph (to align with the French before the next port): ega4-6 154, 160, 161,
  162, 169-172, 175; ega4-7 184, 188, 192, 214, 217, 221; ega4-8 [IV-3]{13} (inside 8.3.2 b), French before b));
  ega4-11 [IV-3]{146} (11.4.4). [IV-2]{182} was missing in ega4-6: added.
- Typography, whole edition (GLOBAL_ISSUES 17): the print sets capitals in formulas upright; the French TeX italic;
  the English mixed (ega4-6/7/11/18/19/21 upright, ega4-9/10/12/13/14 italic).
- 0_IV §§14-18: done (28 fixes; ega0-16 upright letters made italic as the French; 15.1.6 marker moved). More lost
  emphases probably in ega0-17 §17.2 beyond 17.2.2.
- 0_IV §§21-23: done (77 fixes; retranslated proofs of 21.1.6, 21.2.1, 22.7.2 and its continuation; two missing
  paragraphs at p. 157 translated; six missing markers added). To check: ega0-23 around p. 221 ("it will thus suffice
  to prove that A'_m is the intersection ..."), possibly a paraphrase. Upright letters in ega0-21/22 where the French is
  italic (typography pass).
- Markers off (move into the French position): ega0-21 pp. 156, 162, 163, 172, 176; ega0-22 pp. 183, 184, 188, 191;
  ega0-23 p. 216.
- EGA III §§2-6: done (78 fixes; retranslated 2.6.2 pp. 112-114, 5.3.5, 5.4.1, 5.4.4-5.4.5, 5.5.1-5.5.2, 6.1.1-6.1.4,
  6.2.1-6.2.4, 6.3.6, 6.4.4-6.4.5, 6.5.2, 6.6.2-6.6.4, 6.7.3-6.7.6, 6.9.4). Left: ega3-6 has 28 displays wrapped in
  \begin{env}[6.x.y.z] (a bold number above the equation tag; the French has only the tag); \mathcal H for the
  French \mathscr H in §6.2; ~9 emphases in 2.6.2 pp. 114-115. Chapter-0 references converted by script (55).
- EGA IV §§20-21, end matter, errata: done (75 fixes; retranslated Err 17, 19, 30, 31, 33, 44, 21.4.9 and parts of
  21.9.11-21.14.3). Left: the rest of the proofs of 21.14.1 (pp. 324-326) and 21.14.3 are loose paraphrase; upright
  letters in ega4-21 from §21.5 on; markers ega4-21 pp. 289, 290, 315; the Err 53 text is inserted into the body of
  §21.4 (the French has it only in the errata): decide; bibliography: ega4-18 l. 933 \cite[exp.~XII]{SGA1} ->
  {IV-43}, and \egabib{IV-34}{34}, \egabib{IV-37}{37} in ega4-7, then drop the hidden \bibcite lines.
- EGA IV §§2-5: done (91 fixes, 49 extra; retranslated 2.4.3 (v), 2.5.5.2, 2.5.8, 4.7.3, 4.8.5, 5.6.11.1, 5.7.1-5.7.7,
  5.9.12, 5.10.17 (iv), 5.11.2 (i), 5.11.4-5.11.7; a real error fixed: Ass(G) ⊂ Ass(F) -> Ass(F) ⊂ Ass(G) in 5.11.4).
  Left: ⊗_{O_Y} for the French ⊗_Y in §§2.1-2.2 (~57); upright letters ega4-2 §§2.3-2.6 and (S_k)/(R_k) in 5.8-5.13;
  enumeration labels "(a)" for "a)" in 4.6.12-4.6.13; markers IV-2 27, 65, 77, 126. Item references
  \sref{IV.x.y.z.a} rewritten by en_item_refs.py (27).
- Chapter 0 §§9-13: done (31 fixes; hypercohomology \mathcal{H} vs sheaf \sh{H} distinction restored in 12.4.1-12.4.8,
  as in III 6.2.1).
