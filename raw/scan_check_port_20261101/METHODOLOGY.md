# EGA: checking the French transcription against the printed pages, and carrying the corrections into the translations

Working log of the method, kept for a later write-up (GitHub provenance, a methodology section, a post). It records
what was done, how, with which tools and prompts, what it found, what it cost, and what went wrong. Numbers are
measured unless marked as estimates. Dates are 2026.

## 1. Material

- **Print:** *Éléments de géométrie algébrique* (Grothendieck, with Dieudonné), Publ. Math. IHÉS 4, 8, 11, 17, 20, 24,
  28, 32 (1960–1967): chapters 0, I–IV, about 1,800 printed pages. Scans: the Numdam PDFs of the PMIHÉS issues.
- **Transcription:** the French LaTeX of the user's repository `ega-fr` (AI-transcribed earlier in 2026), in two
  editions: a *diplomatic* edition that reproduces the print, its misprints included, and a *corrected* edition that
  gives the correct reading. Every printed page is marked in the source by `\oldpage[PART]{N}`.
- **Translations:** English (`ega-en`, AI-translated, complete), Spanish (`ega-fga-es`, AI-translated: II, III, IV-1
  ch. 0, IV-3, IV-4), and partial Brazilian Portuguese, Vietnamese, Japanese, Korean and Chinese editions.

## 2. The scan check (1–5 November)

**Unit of work:** a batch of five printed pages, checked by one Claude subagent (Claude Opus, Claude Code subagents),
up to 20 at a time on the larger subscription and about 3–4 on the smaller one.

**Preparation** (`prep_batch.py`): for each page, the TeX of that page (from its `\oldpage` marker to the next) and the
scan rendered at 300 dpi, cropped to the printed area and cut into four overlapping horizontal strips (one Read each:
sharp enough for subscripts, tildes and primes, without the model's own downscaling of a full page).

**Checker prompt** (`CHECKER_PROMPT.txt`): compare word by word and symbol by symbol; ignore line breaks, spacing,
old-style figures and layout commands; report every difference as JSON with an exact edit `{old, new}` of the page's
TeX, unique on the page; classify it (word, formula, symbol, font, italics, punctuation, missing, extra, number,
marker, convention, misprint of the print); for a misprint of the print, keep the printed reading in the diplomatic
edition and record the correct reading. Ten numbered **systematic conventions** were added to the prompt during the
pilot, because the same difference recurred on almost every page (bold italic **k** of residue fields, bold chapter
numbers in references, the isomorphism arrow with a tilde, the tilde written after a parenthesis, upright words
inside italic statements, the long dash for set difference, …). Document-wide questions (statement-number fonts, the
proof heading, remark fonts) were taken out of the per-page work and decided once (`GLOBAL_ISSUES.md`).

**Applying** (`process_batch.py` → `apply_fixes.py`, `apply_manual.py`, `replay_to_current.py`):
- a fix is applied only when its `old` occurs exactly once on the page; everything else goes to a manual list,
  resolved by hand;
- every change is logged (`FIXLOG.jsonl`: file, page, old, new, kind, source batch);
- the transcription fixes are replayed on the corrected edition (`FIXLOG_CURRENT.jsonl`), the reversions to a printed
  misprint are not;
- misprints of the print go to `MISPRINTS.json` (page, where, printed reading, correct reading, what the TeX did);
- page markers are checked after every batch (`check_markers.py`), and each part is compiled before a push.

**The checker prompt was revised in a loop**, like the transcription prompts: run on a few batches, read the findings,
name what recurs, change the prompt, run the next batches.
- After the pilot (pp. 80–89): eight numbered conventions, so that the same typographic difference is reported the same
  way on every page; two more (9, 10) were added when they turned up in EGA I and II.
- Document-wide differences (statement-number fonts, the proof heading, remark fonts) were taken out of the per-page
  work after they filled the first findings files.
- After the corrected edition was found to skip misprint fixes that also carried a layout change: the prompt forbids
  combining a misprint fix with any other change in one edit.
- After two edits glued a macro to the next word: a check for glued macros and unbalanced environments after each
  batch (outside the prompt).

**Pilot:** pp. 80–89 of EGA I. About 55–60 thousand subagent tokens per page; the fixed cost of the injected project
instructions is a large share. Findings were mostly typographic conventions, some formula slips, and misprints of
the print; no wrong words.

**Result (5 November):** all 327 batches checked and applied (EGA 0–IV, front and end matter).
- 25,385 logged edits of the diplomatic edition, on 1,697 of the printed pages: conventions 10,154, italics 4,260,
  symbols 2,024, fonts 1,871, punctuation 1,457, formulas 1,045, misprint reversions 859, page markers 661, words 309,
  extra text 245, missing text 192, numbers 113, other 1,852.
- 24,623 edits replayed or made on the corrected edition.
- 1,217 misprints of the print recorded.

**What went wrong, and the fixes:**
- Two checker edits glued a macro to the next word (`\setminZ`); scripts now scan for glued macros and unbalanced
  environments after each batch.
- Agents stopped on usage limits several times (session, then weekly); each was resumed with "continue where you
  stopped".
- The corrected edition kept the *old transcription* wherever the diplomatic edition was reverted to a printed
  misprint, sometimes a third reading (print u^♭, correct v^♭, old TeX v^b). Found on 5 November; a separate pass
  (`MISPRINT_PROMPT.txt`, `apply_misprint_decisions.py`) gives each of the 1,217 misprints its correct reading in the
  corrected edition, checked against the mathematics of the passage ("keep" when the correction is not certain).
- A misprint the checkers did not flag (EGA II 5.2.1: the print's X_f ⊂ X − U for X_f ⊂ U) was found by the English
  pass, checked, and corrected in both editions.
- **Result of the misprint pass (5 November):** of the 1,217 misprints, 245 needed a correction in the corrected
  edition (made, and logged in `FIXLOG_CURRENT.jsonl` as `misprint_pass`), about 950 already had the correct reading
  there, and 21 were left as printed because the correction is not certain (`MISPRINT_KEEP.md`, e.g. a reference
  number printed twice, or a letter whose intended replacement the context does not settle). The corrections then went
  into the translations like every other fix: English 50 automatically, 22 already right, 136 by the agent pass;
  Spanish 46 automatically, 29 already right, 98 by hand.

## 3. Carrying the corrections into the English (3–5 November)

Both editions carry the same `\oldpage` markers, so a French correction can be located on the same printed page.

1. **Automatic port** (`port_fixes_to_en.py`): find the smallest window of the French `old` text that contains the
   whole change, occurs exactly once in the English pages p−1..p+1, and no longer occurs in the corrected French;
   replace it by the matching window of `new`. Formulas, references and notation transfer this way; French wording
   does not. Result: 3,254 applied, 1,106 already right, 1,210 French-only layout, 13,040 left.
2. **Layout:** the English used a different page layout (11 pt, two-sided, blank pages: 1,764 pages against the
   French 1,250); it was given the French layout and about 1,050 displays were set inline as the print has them
   (1,302 pages).
3. **Reference typography by rule** (`en_global_refs.py`): bold chapter numbers in references and upright references
   inside italic statements, as printed, made once through the English `\sref` macro and five rules (3,681 of the
   items).
4. **Second automatic round** (`port_hand_auto.py`): the same window search on normalized text (French label keys
   without `-fr`, English macros expanded, one-letter arguments without braces): 112 applied, 1,232 found already right.
5. **Agent hand pass** (`PORT_EN_AGENT_PROMPT.txt`, batches of 150–220 items; `apply_port_decisions.py`): per item
   "apply" (an exact English edit, unique on the pages), "already", "not_applicable" or "unclear". Priority: changes of
   formulas, words, numbers and references first, italic/upright typography later. Cost about 3–3.5 thousand subagent
   tokens per item. The agents also report English translation errors that no French fix covers; those are checked
   and fixed by hand.

**What went wrong, and the fixes:**
- A window could end with a font command that took the next token (`\boldsymbol` before an already bold k) or
  cut into a link key; windows may no longer end in such commands or cut keys, and a brace-less `\boldsymbol k`
  is one unit.
- A plain-text French window matched the beginning of a longer English word ("(i)] Si" matched "(i)] Since") and put
  an upright label on the wrong item; all automatic edits were scanned for this (`check_partial_words.py`): three
  cases, one reverted.
- An environment renamed in the French (remark → remarks) must change `\begin` and `\end` together; these items are
  handled separately.
- A rule-based classification counted `\textup{(i)}` as a reference; 347 such items were sent back to the hand pass.
- Decisions that depend on the English edition's own layout are fixed by the coordinator (the English sets
  Definitions upright, so French removals of `\emph` inside Definitions are not carried over).
- The automatic rounds logged a correction as "already" when the old French window did not occur on the English
  pages; where the English wrote the same formula differently (`\mathfrak{R}` with braces), a letter correction R → K
  passed as done. An audit (`audit_already_en.py`, `audit_already_filter.py`) re-searched the 4,195 "already" and
  multi-place outcomes on normalized text: 431 old windows still occur on their pages, mostly fonts and symbols that
  recur legitimately elsewhere on the page; of the 30 letter and digit corrections among them, 22 were real misses, all
  in two passages (0_IV 19.4.7, p. 89; IV 19.7.1, pp. 214-216), and went to the agents of those files.
- Two reference forms printed wrongly in the English (parentheses doubled around `\sref`, sub-items in brackets
  `\sref{..}[(i)]`) and two forms of the residue field (`\kappa(x)`, `\mathbf{k}(x)` for the print's bold italic k)
  were fixed by script (`en_ref_syntax.py`, 332 places; `en_kres.py`, 118 places).

**Translation slips (5 November on).** The agents of the hand pass also reported places where the English is wrong
for reasons of its own: omitted sentences and clauses, garbled or misplaced passages, a few proofs replaced by a
different argument, wrong letters, indices and references, French words left untranslated (`ENGLISH_SLIPS.md`, about
210 entries). They are fixed by a second set of agents (`SLIPS_AGENT_PROMPT.txt`), one per group of English files,
each with the corrected French at hand; passages that are not translations of the French are translated anew from the
French. Logs in `slips/`.
Result (5 November, 12 agents, about 6.5 million subagent tokens): 861 log entries, 802 fixed (about 400 of them slips
the agents met in the passages they read, beyond the reported ones), 42 already right, 12 not slips, 5 unclear. About
70 paragraphs and proofs were translated anew, among them proofs the English had replaced by a different argument
(III 7.4.2, 0_IV 19.6.6) and passages it had condensed to a sentence. One real mathematical error of the English was
found this way (IV 5.11.4: the inclusion of the sets of associated primes reversed). The reports also showed that the
whole English needs a paragraph-by-paragraph faithfulness reading: every group found as many unreported slips as
reported ones (`FAITHFULNESS_TODO.md`). Scripts after the pass: chapter-0 references with subscripts as printed
(`en_ch0_subscripts.py`, checked against the French), references to items (`en_item_refs.py`), page markers that
broke sentences into paragraphs (`en_final_fixes.py`, 120). Pushed: ega-en b83bfde (1,298 pp.).

**French places the English pass sent back (`FRENCH_RECHECK.md`).** Four places where the English had the reading the
mathematics needs and the French did not: all four are misprints of the print. Two were already corrected in the
corrected edition; two were new: in 0_IV (15.1.15) the flatness hypothesis needs 1 ≤ i ≤ n+1 (printed n; with i ≤ n,
A = M = k[T], f₁ = T, A' = k is a counterexample), and in the proof of (17.3.4) the citation is (16.4.6, (ii)) (printed
(i)). Corrected in the corrected French and Spanish editions.

## 4. Carrying the corrections into the Spanish (5 November)

The Spanish has the same markers and keeps the French macros, so the window method works well there
(`port_fixes_to_lang.py`): corrected editions 3,528 applied and 2,105 already right; diplomatic editions (from the
diplomatic French fixes) 1,229 applied and 792 already right. Every edition was compiled; the port had introduced two
kinds of error, both fixed (`\setmin` not defined in three masters; superscript hats without braces). The published
readers (flattened TeX, PDF, sources ZIP) are rebuilt from the sources (`rebuild_es_readers.py`).

## 5. Costs and compute

- Claude subscriptions (Max, then Ultra), Claude Code subagents. Scan check: about 50–60 thousand tokens per printed
  page. Translation hand pass: about 3 thousand tokens per correction.
- Week of 3–10 November (Ultra): the user set a ceiling of 80 % of the weekly limit, with about 10 % for the Longue
  Marche transcription.
