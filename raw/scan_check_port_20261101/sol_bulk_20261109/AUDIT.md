# Audit of Sol's bulk decisions

| decision | ok | doubtful |
|---|---:|---:|
| apply | 3489 | 13 |
| already | 2073 | 79 |
| not_applicable | 556 | 47 |
| unclear | 0 | 4 |
| None | 0 | 0 |

Doubtful by reason: {'apply: en_old not found exactly once on pages p-1..p+1': 13, 'already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement': 63, 'not_applicable for a textup+ fix': 35, 'not_applicable for a emph- fix': 2, 'not_applicable for a emph+ fix': 9, 'already: en_old missing or not found': 4, "decision 'unclear'": 4, 'already: the fix adds an emphasis but the quoted English has none': 4, 'already: the fix removes an emphasis but the quoted English has one': 8, 'not_applicable for a emph~ fix': 1}

## 2735 (II 111, textup+, decisions_bulk_002): apply: en_old not found exactly once on pages p-1..p+1
FR: 'est fini\n(resp. entier).' -> 'est fini\n\\textup{(resp. \\emph{entier})}.'
Sol: apply | en_old 'is finite\n(resp. integral).' | en_new 'is finite\n\\textup{(resp. \\emph{integral})}.' | note None

## 5144 (0\textsubscript{III} 71, textup+, decisions_bulk_006): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\emph{Supposons que le système projectif\n$\\mathbf X^\\bullet=(X_k^\\bullet)_{k\\in\\mathbb Z}$ de complexes filtrés soit\nobtenu comme dans (\\hyperref[0.13.5.2-fr]{13.5.2}). Alors :}' -> 'Supposons que le système projectif\n$\\mathbf X^\\bullet=(X_k^\\bullet)_{k\\in\\mathbb Z}$ de complexes filtrés soit\nobtenu comme dans \\textup{(\\hyperref[0.13.5.2-fr]{13.5.2})}. Alors :'
Sol: already | en_old 'obtained as in \\sref{0.13.5.2}. Then:' | en_new None | note 'The reference macro already renders its parenthesis upright.'

## 5149 (0\textsubscript{III} 72, textup+, decisions_bulk_006): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\emph{Sous les hypothèses de\n(\\hyperref[0.13.5.3-fr]{13.5.3}), on a, pour $s\\geq r>p-p_0$, un\nmonomorphisme canonique}' -> 'Sous les hypothèses de\n\\textup{(\\hyperref[0.13.5.3-fr]{13.5.3})}, on a, pour $s\\geq r>p-p_0$, un\nmonomorphisme canonique'
Sol: already | en_old 'Under the hypotheses of \\sref{0.13.5.3}, for\n$s\\geq r>p-p_0$ there is a canonical monomorphism' | en_new None | note 'The reference macro already renders its parenthesis upright.'

## 5154 (0\textsubscript{III} 72, textup+, decisions_bulk_006): not_applicable for a textup+ fix
FR: '(la flèche verticale de droite provenant du\nmorphisme $X_{p+s-1}^\\bullet\\to X_{p+r-1}^\\bullet$)' -> '\\textup{(la flèche verticale de droite provenant du\nmorphisme $X_{p+s-1}^\\bullet\\to X_{p+r-1}^\\bullet$)}'
Sol: not_applicable | en_old None | en_new None | note 'English translates this as a nonparenthetical “where” clause.'

## 5158 (0\textsubscript{III} 72, textup+, decisions_bulk_006): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: "\\emph{Sous les hypothèses de\n(\\hyperref[0.13.5.3-fr]{13.5.3}), si l'une des limites projectives\n$\\varprojlim_r\\mathrm E_r^{pq}(\\mathbf X^\\bullet)$,\n$\\varprojlim_k\\mathrm E_\\infty^{pq}(X_k^\\bullet)$ existe, il en est de\nmême de l'autre, et on a un isomorphisme canonique}" -> "Sous les hypothèses de\n\\textup{(\\hyperref[0.13.5.3-fr]{13.5.3})}, si l'une des limites projectives\n$\\varprojlim_r\\mathrm E_r^{pq}(\\mathbf X^\\bullet)$,\n$\\varprojlim_k\\mathrm E_\\infty^{pq}(X_k^\\bullet)$ existe, il en est de\nmême de l'autre, et on a un isomorphisme canonique"
Sol: already | en_old 'Under the hypotheses of \\sref{0.13.5.3}, if one of the projective\nlimits' | en_new None | note 'The reference macro already renders its parenthesis upright.'

## 5160 (0\textsubscript{III} 72, textup+, decisions_bulk_006): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\emph{En outre, pour que le système projectif\n$(\\mathrm E_r^{pq}(\\mathbf X^\\bullet))_{r\\in\\mathbb Z}$ soit\nessentiellement constant\n(\\hyperref[0.13.4.2-fr]{13.4.2}), il faut et il suffit que le système\nprojectif $(\\mathrm E_\\infty^{pq}(X_k^\\bullet))_{k\\in\\mathbb Z}$ le soit.}' -> 'En outre, pour que le système projectif\n$(\\mathrm E_r^{pq}(\\mathbf X^\\bullet))_{r\\in\\mathbb Z}$ soit\nessentiellement constant\n\\textup{(\\hyperref[0.13.4.2-fr]{13.4.2})}, il faut et il suffit que le système\nprojectif $(\\mathrm E_\\infty^{pq}(X_k^\\bullet))_{k\\in\\mathbb Z}$ le soit.'
Sol: already | en_old 'constant \\sref{0.13.4.2} if and only if the projective system' | en_new None | note 'The reference macro already renders its parenthesis upright.'

## 5230 (0\textsubscript{III} 76, emph-, decisions_bulk_006): not_applicable for a emph- fix
FR: '\\qquad\\emph{pour tout $p\\in\\mathbb Z$.}\n\\end{equation}\n\\end{proposition}' -> '\\qquad\\textit{pour tout $p\\in\\mathbb Z$.}\n\\end{equation}\n\\end{proposition}'
Sol: not_applicable | en_old None | en_new None | note 'English expresses this condition entirely in mathematics, without the French italic phrase.'

## 5239 (0\textsubscript{III} 76, emph-, decisions_bulk_006): not_applicable for a emph- fix
FR: '\\qquad\\emph{pour tout $p\\in\\mathbb Z$.}\n\\end{equation}\n\\end{corollary}' -> '\\qquad\\textit{pour tout $p\\in\\mathbb Z$.}\n\\end{equation}\n\\end{corollary}'
Sol: not_applicable | en_old None | en_new None | note 'English expresses this condition entirely in mathematics, without the French italic phrase.'

## 5392 (III 99, textup+, decisions_bulk_006): not_applicable for a textup+ fix
FR: '$i=r$ et $n\\leq-(r+1)$.' -> '$i=r$ \\textup{et} $n\\leq-(r+1)$.'
Sol: not_applicable | en_old None | en_new None | note 'English uses a comma between these two conditions, not the French conjunction.'

## 5557 (III 119, emph~, decisions_bulk_007): apply: en_old not found exactly once on pages p-1..p+1
FR: '\\emph{propre sur}' -> '\\emph{propre} sur'
Sol: apply | en_old 'a subset $Z$ of the underlying space of $\\mathfrak X$ is \\emph{proper over}\n$\\mathfrak S$' | en_new 'a subset $Z$ of the underlying space of $\\mathfrak X$ is \\emph{proper} over\n$\\mathfrak S$' | note None

## 6819 (III 137, emph+, decisions_bulk_007): not_applicable for a emph+ fix
FR: 'CHAPITRE III (suite)' -> 'CHAPITRE III \\emph{(suite)}'
Sol: not_applicable | en_old None | en_new None | note 'The French continuation heading is not present in the English file structure.'

## 6832 (III 142, textup+, decisions_bulk_008): not_applicable for a textup+ fix
FR: '(resp. $M_{\\bullet\\bullet}$) un' -> '\\textup{(resp. $M_{\\bullet\\bullet}$)} un'
Sol: not_applicable | en_old None | en_new None | note 'The English coordinates the two bicomplexes without a parenthesis.'

## 6833 (III 142, textup+, decisions_bulk_008): not_applicable for a textup+ fix
FR: '(resp. $M_{i,\\bullet}$)' -> '\\textup{(resp. $M_{i,\\bullet}$)}'
Sol: not_applicable | en_old None | en_new None | note 'The English states the two resolution conditions without a parenthesis.'

## 6834 (III 142, textup+, decisions_bulk_008): not_applicable for a textup+ fix
FR: '(resp. $Q_i$)' -> '\\textup{(resp. $Q_i$)}'
Sol: not_applicable | en_old None | en_new None | note 'The English states the two resolution conditions without a parenthesis.'

## 7154 (III 151, textup+, decisions_bulk_008): not_applicable for a textup+ fix
FR: 'Soit $\\mathscr P_\\bullet$ (resp.\n$\\mathscr Q_\\bullet$) un complexe' -> 'Soit $\\mathscr P_\\bullet$ \\textup{(resp.}\n$\\mathscr Q_\\bullet$\\textup{)} un complexe'
Sol: not_applicable | en_old None | en_new None | note 'The English uses two coordinated complexes, without the French parenthesis.'

## 7155 (III 151, textup+, decisions_bulk_008): not_applicable for a textup+ fix
FR: '-Modules (resp. de\n$\\mathscr O_Y$-Modules) quasi-cohérents; on a' -> '-Modules \\textup{(resp.} de\n$\\mathscr O_Y$-Modules\\textup{)} quasi-cohérents; on a'
Sol: not_applicable | en_old None | en_new None | note 'The English uses two coordinated complexes, without the French parenthesis.'

## 6929 (III 165, textup+, decisions_bulk_009): not_applicable for a textup+ fix
FR: "(dit « foncteur spectral\nd'associativité »)" -> "\\textup{(dit « foncteur spectral\nd'associativité »)}"
Sol: not_applicable | en_old None | en_new None | note 'The English recasts the parenthetical definition without parentheses.'

## 7841 (III 176, textup+, decisions_bulk_009): not_applicable for a textup+ fix
FR: '(resp. exact à droite, exact) pour' -> '\\textup{(resp.} exact à droite, exact) pour'
Sol: not_applicable | en_old None | en_new None | note 'The English recasts this without the parenthesis.'

## 7842 (III 176, textup+, decisions_bulk_009): not_applicable for a textup+ fix
FR: '(resp. exact à droite, exact).' -> '\\textup{(resp.} exact à droite, exact).'
Sol: not_applicable | en_old None | en_new None | note 'The English recasts this without the parenthesis.'

## 7360 (III 187, emph+, decisions_bulk_010): already: en_old missing or not found
FR: '$B_p(P_\\bullet)$ est plat, car' -> '$B_p(P_\\bullet)$ est \\emph{plat}, car'
Sol: already | en_old '$B_p(P_\x08ullet)$ is \\emph{flat}, since there is an exact sequence' | en_new None | note None

## 7372 (III 187, textup+, decisions_bulk_010): not_applicable for a textup+ fix
FR: '(resp. exact à gauche, exact)' -> '\\textup{(resp. \\emph{exact à gauche, exact})}'
Sol: not_applicable | en_old None | en_new None | note 'The English renders the parenthetical as an unparenthesized phrase.'

## 7559 (III 192, textup+, decisions_bulk_010): already: en_old missing or not found
FR: '(resp. exact à gauche, exact) il en' -> '\\textup{(resp.} exact à gauche, exact) il en'
Sol: already | en_old '\\textup{(respectively} left exact, exact), then the same is true of' | en_new None | note 'Passage relocated to the English text shown under page III 196.'

## 7560 (III 192, emph+, decisions_bulk_010): already: en_old missing or not found
FR: '$A$-module plat. On a' -> '$A$-module \\emph{plat}. On a'
Sol: already | en_old '\\emph{flat} $A$-module.  Then, for every $A$-module $M$,' | en_new None | note 'Passage relocated to the English text shown under page III 196.'

## 7565 (III 192, textup+, decisions_bulk_010): apply: en_old not found exactly once on pages p-1..p+1
FR: '(resp. exact à gauche, exact), il faut' -> '\\textup{(resp.} exact à gauche, exact), il faut'
Sol: apply | en_old 'finite-type $A$-modules.  For $T_p$ to be right exact\n(respectively left exact, exact), it is necessary and' | en_new 'finite-type $A$-modules.  For $T_p$ to be right exact\n\\textup{(respectively} left exact, exact), it is necessary and' | note 'Passage relocated to the English text shown under page III 197.'

## 7942 (III 198, emph+, decisions_bulk_010): apply: en_old not found exactly once on pages p-1..p+1
FR: "$Y'$-plats en vertu" -> "$Y'$-\\emph{plats} en vertu"
Sol: apply | en_old "that are $Y'$-flat, by \\sref[I]{I.9.1.12} and" | en_new "that are $Y'$-\\emph{flat}, by \\sref[I]{I.9.1.12} and" | note 'Passage relocated to the English text shown under page III 201.'

## 7995 (III 201, textup+, decisions_bulk_010): not_applicable for a textup+ fix
FR: "(d'où un isomorphisme de foncteurs" -> "\\textup{(d'où un isomorphisme de foncteurs}"
Sol: not_applicable | en_old None | en_new None | note 'The English uses a separate sentence without the French parenthesis.'

## 8089 (III 205, textup+, decisions_bulk_010): not_applicable for a textup+ fix
FR: '(définie dans (7.7.5.1))' -> '\\textup{(définie dans (7.7.5.1))}'
Sol: not_applicable | en_old None | en_new None | note 'The English uses commas, not the French parenthesis.'

## 8099 (III 206, emph+, decisions_bulk_010): not_applicable for a emph+ fix
FR: 'part, a) entraîne' -> 'part, \\emph{a)} entraîne'
Sol: not_applicable | en_old None | en_new None | note 'The English says “It also implies” without repeating the label.'

## 24454 (IV 350, textup+, decisions_bulk_011): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'hypothèses de {\\hyperref[canon-index.ega4.c04.prop.6-2-3]{(6.2.3)}}, soit' -> 'hypothèses de \\textup{\\hyperref[canon-index.ega4.c04.prop.6-2-3]{(6.2.3)}}, soit'
Sol: already | en_old 'Under the hypotheses of {\\hyperref[IV.6.2.3]{(6.2.3)}}, let in addition $M$ be a finite' | en_new None | note 'The reference, including its parentheses, is already upright.'

## 24272 (IV 355, emph+, decisions_bulk_011): apply: en_old not found exactly once on pages p-1..p+1
FR: 'avant « Soient »,' -> 'avant « \\emph{Soient} »,'
Sol: apply | en_old "insert ``(i)'' before ``Let.''" | en_new "insert ``(i)'' before ``\\emph{Let}.''" | note None

## 24273 (IV 355, emph+, decisions_bulk_011): apply: en_old not found exactly once on pages p-1..p+1
FR: '\\textup{(ii)} Inversement, soit $f:X\\to Y$ un morphisme plat. Si $X$\nest unibranche (resp. géométriquement unibranche) en un point $x$, $Y$\nest unibranche (resp. géométriquement unibranche) au point $y=f(x)$.' -> '\\textup{(ii)} \\emph{Inversement, soit $f:X\\to Y$ un morphisme plat. Si $X$\nest unibranche} (resp. \\emph{géométriquement unibranche}) \\emph{en un point $x$, $Y$\nest unibranche} (resp. \\emph{géométriquement unibranche}) \\emph{au point $y=f(x)$.}'
Sol: apply | en_old '\\textup{(ii)} Conversely, let $f:X\\to Y$ be a flat morphism.  If $X$\nis unibranch (respectively geometrically unibranch) at a point $x$, then\n$Y$ is unibranch (respectively geometrically unibranch) at the point\n$y=f(x)$.' | en_new '\\textup{(ii)} \\emph{Conversely, let $f:X\\to Y$ be a flat morphism.  If $X$\nis unibranch} (respectively \\emph{geometrically unibranch}) \\emph{at a point $x$, then\n$Y$ is unibranch} (respectively \\emph{geometrically unibranch}) \\emph{at the point\n$y=f(x)$.}' | note None

## 24274 (IV 355, emph+, decisions_bulk_011): apply: en_old not found exactly once on pages p-1..p+1
FR: 'anneau local réduit, et' -> 'anneau local \\emph{réduit}, et'
Sol: apply | en_old '$Y=\\operatorname{Spec}(A)$, with $A$ a reduced local ring and $y$ the' | en_new '$Y=\\operatorname{Spec}(A)$, with $A$ a \\emph{reduced} local ring and $y$ the' | note None

## 24014 (IV 361, textup+, decisions_bulk_011): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '{\\hyperlink{ega4.c04.cor.21-4-11}{(21.4.11)}}. Pour tout' -> '\\textup{\\hyperlink{ega4.c04.cor.21-4-11}{(21.4.11)}}. Pour tout'
Sol: already | en_old 'Assume the hypotheses of {\\hyperref[IV.21.4.11]{(21.4.11)}}.  For every invertible' | en_new None | note 'The reference, including its parentheses, is already upright.'

## 8816 (0\textsubscript{IV-1} 5, other, decisions_bulk_011): decision 'unclear'
FR: 'CHAPITRE 0 (suite)' -> 'CHAPITRE 0 \\textit{(suite)}'
Sol: unclear | en_old None | en_new None | note 'The chapter heading is not included in the supplied English text.'

## 8842 (0\textsubscript{IV-1} 27, emph+, decisions_bulk_012): not_applicable for a emph+ fix
FR: 'On a $\\dim(M)\\leq d(M)$.' -> '\\emph{On a} $\\dim(M)\\leq d(M)$.'
Sol: not_applicable | en_old None | en_new None | note 'English states only the formula, omitting the introductory words being emphasized.'

## 8851 (0\textsubscript{IV-1} 27, emph+, decisions_bulk_012): not_applicable for a emph+ fix
FR: 'On a $d(M)\\leq s(M)$.' -> '\\emph{On a} $d(M)\\leq s(M)$.'
Sol: not_applicable | en_old None | en_new None | note 'English states only the formula, omitting the introductory words being emphasized.'

## 8859 (0\textsubscript{IV-1} 27, emph+, decisions_bulk_012): not_applicable for a emph+ fix
FR: 'On a $s(M)\\leq\\dim(M)$.' -> '\\emph{On a} $s(M)\\leq\\dim(M)$.'
Sol: not_applicable | en_old None | en_new None | note 'English states only the formula, omitting the introductory words being emphasized.'

## 8865 (0\textsubscript{IV-1} 28, textup+, decisions_bulk_012): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'de sorte (III, 2.5.4) que' -> 'de sorte \\textup{(III, 2.5.4)} que'
Sol: already | en_old 'such that $(\\mathbf{III},~2.5.4)$ for $n$ sufficiently large,' | en_new None | note 'The entire reference, including its parentheses, is in math mode and upright.'

## 9359 (0\textsubscript{IV-1} 114, textup+, decisions_bulk_014): apply: en_old not found exactly once on pages p-1..p+1
FR: 'un $\\Lambda$-homomorphisme' -> 'un \\textup{$\\Lambda$-homomorphisme}'
Sol: apply | en_old 'where $u$ is a continuous $\\Lambda$-homomorphism, also factors' | en_new 'where $u$ is a continuous \\textup{$\\Lambda$-homomorphism}, also factors' | note None

## 10171 (0\textsubscript{IV-1} 130, textup+, decisions_bulk_014): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'canonique \\sref{0.20.5.4.1-fr}' -> 'canonique \\textup{\\sref{0.20.5.4.1-fr}}'
Sol: already | en_old "If $A'$, $B$ are two $A$-algebras and $B'=B\\otimes_A A'$, the canonical homomorphism \\sref{0.20.5.4.1}" | en_new None | note '\\sref already prints the reference upright.'

## 10039 (0\textsubscript{IV-1} 136, emph+, decisions_bulk_014): decision 'unclear'
FR: '$k$-algèbre formellement lisse ou une' -> '$k$-\\emph{algèbre formellement lisse} ou une'
Sol: unclear | en_old None | en_new None | note 'The English omits the equivalence clause containing this occurrence; it instead asserts relative formal smoothness.'

## 10110 (0\textsubscript{IV-1} 148, textup+, decisions_bulk_014): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\sref{0.19.10.2-fr}' -> '\\textup{\\sref{0.19.10.2-fr}}'
Sol: already | en_old 'For $B$ to be formally non-ramified \\sref{0.19.10.2},' | en_new None | note '\\sref already prints the reference upright.'

## 10117 (0\textsubscript{IV-1} 148, textup+, decisions_bulk_014): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'bimorphisme formel \\sref{0.19.1.2-fr}' -> 'bimorphisme formel \\textup{\\sref{0.19.1.2-fr}}'
Sol: already | en_old 'is a formal bimorphism \\sref{0.19.1.2}.' | en_new None | note '\\sref already prints the reference upright.'

## 10221 (0\textsubscript{IV-1} 167, textup+, decisions_bulk_015): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'de (i) sont vérifiées' -> 'de \\textup{(i)} sont vérifiées'
Sol: already | en_old 'The equivalent conditions of \\textnormal{(i)} are satisfied' | en_new None | note None

## 10950 (0\textsubscript{IV-1} 183, emph+, decisions_bulk_015): already: the fix adds an emphasis but the quoted English has none
FR: '  est injectif.\n\\end{enumerate}' -> '  \\emph{est injectif}.\n\\end{enumerate}'
Sol: already | en_old '\\Omega^1_{\\mathrm{B}/\\Lambda}\\otimes_\\mathrm{B}\\mathrm{C}$ is injective.}' | en_new None | note 'The entire assertion is already inside \\emph.'

## 11117 (0\textsubscript{IV-1} 194, textup+, decisions_bulk_016): not_applicable for a textup+ fix
FR: 'mod.~$\\mathfrak m$, on suppose' -> '\\textup{mod.}~$\\mathfrak m$, on suppose'
Sol: not_applicable | en_old None | en_new None | note 'The English spells out “modulo”; the French fix makes the abbreviation “mod.” upright.'

## 11861 (IV-2 12, textup+, decisions_bulk_017): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)]' -> '\\item[\\textup{(ii)}]'
Sol: already | en_old '\\item[\\textnormal{(ii)}] Let $f:X\\to Y$, $g:Y\\to Z$ be two morphisms, $\\sh{F}$' | en_new None | note None

## 11862 (IV-2 12, textup+, decisions_bulk_017): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iii)]' -> '\\item[\\textup{(iii)}]'
Sol: already | en_old '\\item[\\textnormal{(iii)}] Let $f:X\\to Y$, $g:Y\\to Z$ be two morphisms, $\\sh{G}$' | en_new None | note None

## 11863 (IV-2 12, textup+, decisions_bulk_017): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iv)]' -> '\\item[\\textup{(iv)}]'
Sol: already | en_old '\\item[\\textnormal{(iv)}] Let $f:X\\to Y$, $g:Y\\to Z$ be two morphisms, $x$ a point of $X$.' | en_new None | note None

## 11860 (IV-2 12, textup+, decisions_bulk_017): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(i)]' -> '\\item[\\textup{(i)}]'
Sol: already | en_old "\\item[\\textnormal{(i)}] Let $f:X\\to Y$, $g:Y'\\to Y$ be two morphisms, $X'=X\\times_Y Y'$, $\\sh{F}$" | en_new None | note None

## 11871 (IV-2 13, textup+, decisions_bulk_017): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iii)]' -> '\\item[\\textup{(iii)}]'
Sol: already | en_old '\\item[\\textnormal{(iii)}] Let $f:X\\to Y$, $g:Y\\to Z$ be two morphisms such that $f$ is faithfully flat.' | en_new None | note None

## 12107 (IV-2 43, emph+, decisions_bulk_018): already: the fix adds an emphasis but the quoted English has none
FR: 'et les deux membres sont égaux si $Y$ est localement noethérien.' -> '\\emph{et les deux membres sont égaux si $Y$ est localement noethérien.}'
Sol: already | en_old 'and the two sides are equal if $Y$ is locally Noetherian.\n\\end{proposition}' | en_new None | note 'Already italic as part of the proposition.'

## 12807 (IV-2 55, textup+, decisions_bulk_019): not_applicable for a textup+ fix
FR: "(autrement dit l'ensemble des\nidéaux premiers minimaux de $R(X)\\otimes_k R(Y)$)," -> "\\textup{(autrement dit} l'ensemble des\nidéaux premiers minimaux de $R(X)\\otimes_k R(Y)$\\textup{)},"
Sol: not_applicable | en_old None | en_new None | note 'English uses an unparenthesized alternative, so there are no corresponding parentheses to set upright.'

## 12831 (IV-2 57, textup+, decisions_bulk_019): not_applicable for a textup+ fix
FR: '(pour tous les triplets\n$(\\lambda,\\mu,\\nu)$)' -> '\\textup{(}pour tous les triplets\n$(\\lambda,\\mu,\\nu)$\\textup{)}'
Sol: not_applicable | en_old None | en_new None | note 'English uses commas rather than the French parentheses.'

## 12701 (IV-2 70, textup+, decisions_bulk_020): not_applicable for a textup+ fix
FR: '(i.e., $\\mathcal O' -> '\\textup{(i.e.,} $\\mathcal O'
Sol: not_applicable | en_old None | en_new None | note 'The English uses a nonparenthetical “that is” clause.'

## 12703 (IV-2 70, textup+, decisions_bulk_020): not_applicable for a textup+ fix
FR: "(auquel cas on dit aussi que $X\\otimes_k k'$ est ponctuellement intègre)." -> "\\textup{(auquel cas on dit aussi que $X\\otimes_k k'$ est} ponctuellement intègre\\textup{)}."
Sol: not_applicable | en_old None | en_new None | note 'The English renders the remark as a nonparenthetical clause.'

## 14452 (IV-2 75, emph+, decisions_bulk_020): decision 'unclear'
FR: 'soit géométriquement réduit (4.6.11)' -> 'soit \\emph{géométriquement réduit} (4.6.11)'
Sol: unclear | en_old None | en_new None | note 'No matching passage citing 4.6.11 appears here; the similar passage citing 4.6.13 is handled by 14451.'

## 13004 (IV-2 81, textup+, decisions_bulk_020): not_applicable for a textup+ fix
FR: 'resp. un sous-préschéma' -> '\\textup{resp.} un sous-préschéma'
Sol: not_applicable | en_old None | en_new None | note 'The English list omits this repeated “resp.”.'

## 13005 (IV-2 81, textup+, decisions_bulk_020): not_applicable for a textup+ fix
FR: 'resp. un $K$-morphisme' -> '\\textup{resp.} un $K$-morphisme'
Sol: not_applicable | en_old None | en_new None | note 'The English list omits this repeated “resp.”.'

## 13042 (IV-2 83, textup+, decisions_bulk_020): not_applicable for a textup+ fix
FR: 'cohérent, resp. que' -> 'cohérent, \\textup{resp.} que'
Sol: not_applicable | en_old None | en_new None | note 'The English separates these alternatives with a semicolon, without repeating “resp.”.'

## 13043 (IV-2 83, textup+, decisions_bulk_020): not_applicable for a textup+ fix
FR: 'cohérents, resp. que' -> 'cohérents, \\textup{resp.} que'
Sol: not_applicable | en_old None | en_new None | note 'The English uses “or” instead of repeating “resp.”.'

## 13047 (IV-2 83, emph+, decisions_bulk_020): not_applicable for a emph+ fix
FR: 'conditions a), b) ou c)' -> 'conditions \\emph{a)}, \\emph{b)} ou \\emph{c)}'
Sol: not_applicable | en_old None | en_new None | note 'The English refers collectively to the equivalent conditions and does not print their labels.'

## 12902 (IV-2 88, emph+, decisions_bulk_021): not_applicable for a emph+ fix
FR: 'soit fermé dans $U$' -> 'soit fermé \\emph{dans} $U$'
Sol: not_applicable | en_old None | en_new None | note "English omits the intermediate clause about $Z'\\cap U$ to which this emphasis belongs."

## 13300 (IV-2 94, textup+, decisions_bulk_021): not_applicable for a textup+ fix
FR: '(donc fermé)' -> '\\textup{(donc} fermé\\textup{)}'
Sol: not_applicable | en_old None | en_new None | note 'English says “hence a closed morphism” without a parenthesis.'

## 13307 (IV-2 94, emph+, decisions_bulk_021): not_applicable for a emph+ fix
FR: 'préschéma\nsomme de' -> 'préschéma\n\\emph{somme} de'
Sol: not_applicable | en_old None | en_new None | note 'English expresses the sum by $\\amalg$, without a corresponding word to emphasize.'

## 13969 (IV-2 97, emph+, decisions_bulk_021): not_applicable for a emph+ fix
FR: "(sous l'hypothèse b))" -> "(sous l'hypothèse \\emph{b)})"
Sol: not_applicable | en_old None | en_new None | note 'English omits this parenthetical reminder of hypothesis (b).'

## 13993 (IV-2 98, textup+, decisions_bulk_021): not_applicable for a textup+ fix
FR: 'équivalentes a), b), c)' -> 'équivalentes \\textup{a), b), c)}'
Sol: not_applicable | en_old None | en_new None | note 'English refers to the equivalent conditions collectively and omits the individual labels.'

## 14010 (IV-2 99, textup+, decisions_bulk_021): not_applicable for a textup+ fix
FR: '$\\xi$ (resp. $\\eta$)' -> '$\\xi$ \\textup{(resp. $\\eta$)}'
Sol: not_applicable | en_old None | en_new None | note 'English combines the two generic points using “respectively”, without a parenthesis.'

## 14011 (IV-2 99, textup+, decisions_bulk_021): not_applicable for a textup+ fix
FR: 'de $X$ (resp. $Y$)' -> 'de $X$ \\textup{(resp. $Y$)}'
Sol: not_applicable | en_old None | en_new None | note 'English combines the two preschemes using “respectively”, without a parenthesis.'

## 13344 (IV-2 101, textup+, decisions_bulk_021): not_applicable for a textup+ fix
FR: '(resp.\n$\\dim(f^{-1}(y))=n$)' -> '\\textup{(resp.}\n$\\dim(f^{-1}(y))=n$\\textup{)}'
Sol: not_applicable | en_old None | en_new None | note 'English states the alternative hypothesis separately, without the French parenthesis.'

## 13345 (IV-2 101, textup+, decisions_bulk_021): not_applicable for a textup+ fix
FR: '\\end{equation}\n(resp.\n\\begin{equation}' -> '\\end{equation}\n\\textup{(resp.}\n\\begin{equation}'
Sol: not_applicable | en_old None | en_new None | note 'English introduces the alternative conclusion with a separate sentence, not a parenthesis.'

## 13195 (IV-2 107, textup+, decisions_bulk_022): not_applicable for a textup+ fix
FR: '(autrement dit (5.1.3),' -> '\\textup{(autrement dit (5.1.3),}'
Sol: not_applicable | en_old None | en_new None | note 'The English recasts the parenthetical explanation as a separate sentence.'

## 13500 (IV-2 115, textup+, decisions_bulk_022): not_applicable for a textup+ fix
FR: '(avec les notations de (5.9.6)).' -> '\\textup{(}avec les notations de \\textup{(5.9.6))}.'
Sol: not_applicable | en_old None | en_new None | note 'The English has no enclosing prose parenthesis; the reference itself is automatically upright.'

## 13834 (IV-2 129, textup+, decisions_bulk_023): not_applicable for a textup+ fix
FR: "(ce qui aura\nlieu par exemple lorsque $A$ possède l'une des propriétés (i), (ii) de\n(5.11.6))" -> "\\textup{(ce qui aura\nlieu par exemple lorsque $A$ possède l'une des propriétés (i), (ii) de\n(5.11.6))}"
Sol: not_applicable | en_old None | en_new None | note 'The English renders this aside as a separate sentence, not a parenthesis.'

## 15281 (IV-2 149, textup+, decisions_bulk_024): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[b)]' -> '\\item[\\textup{b)}]'
Sol: already | en_old "\\item $\\boldsymbol{Q}(k')$ is true for every finite radicial extension $k'$ of $k$." | en_new None | note 'The enumerate label uses \\emph inside the italic proposition.'

## 15282 (IV-2 149, textup+, decisions_bulk_024): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[c)]' -> '\\item[\\textup{c)}]'
Sol: already | en_old "\\item $\\boldsymbol{Q}(k')$ is true for every extension of finite type $k'$ of $k$." | en_new None | note 'The enumerate label uses \\emph inside the italic proposition.'

## 15284 (IV-2 149, textup+, decisions_bulk_024): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[e)]' -> '\\item[\\textup{e)}]'
Sol: already | en_old "\\item $\\boldsymbol{Q}(k')$ is true for a perfect extension $k'$ of $k$." | en_new None | note 'The enumerate label uses \\emph inside the italic proposition.'

## 15285 (IV-2 149, textup+, decisions_bulk_024): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[f)]' -> '\\item[\\textup{f)}]'
Sol: already | en_old "\\item $\\boldsymbol{Q}(k')$ is true for every extension $k'=k^{p^{-s}}$, where $p$ is the characteristic exponent of $k$, and $s>0$." | en_new None | note 'The enumerate label uses \\emph inside the italic proposition.'

## 14133 (IV-2 152, textup+, decisions_bulk_024): decision 'unclear'
FR: 'propriétés c), d), e) (resp. f)) de (6.6.1). Alors' -> 'propriétés \\textup{c), d), e) (resp. f))} de \\textup{(6.6.1)}. Alors'
Sol: unclear | en_old None | en_new None | note 'The English omits the clause listing c), d), e) (resp. f)); there are no corresponding labels to format.'

## 14145 (IV-2 153, textup+, decisions_bulk_024): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[c)]' -> '\\item[\\textup{c)}]'
Sol: already | en_old '\\item $\\sh{O}_x$ is a formally smooth $\\sh{O}_y$-algebra \\sref[0]{0.19.3.1} for the adic topologies on $\\sh{O}_x$ and $\\sh{O}_y$.' | en_new None | note 'The automatic label uses \\emph inside the italic theorem.'

## 14161 (IV-2 153, emph+, decisions_bulk_024): already: the fix adds an emphasis but the quoted English has none
FR: "l'équivalence de c) et c') résulte" -> "l'équivalence de \\emph{c)} et \\emph{c')} résulte"
Sol: already | en_old 'the equivalence follows from \\sref[0]{0.22.6.4}' | en_new None | note 'The English refers back to the equivalence without repeating its labels.'

## 14352 (IV-2 166, textup+, decisions_bulk_025): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'de caractéristique 0.' -> 'de caractéristique \\textup{0}.'
Sol: already | en_old 'its field of fractions $\\mathrm{K}$ is of characteristic $0$.' | en_new None | note 'The zero is already upright in mathematics.'

## 14844 (IV-2 187, textup+, decisions_bulk_026): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'irréductible de dimension 1,' -> 'irréductible de dimension \\textup{1},'
Sol: already | en_old 'Let $\\mathrm{Y}$ be an irreducible prescheme locally Noetherian of dimension~$1$,' | en_new None | note 'The mathematical numeral is already upright.'

## 14899 (IV-2 189, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[a)]' -> '\\item[\\textup{a)}]'
Sol: already | en_old '\\item For every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$, the ring $\\mathrm{B}^{(1)}$ is a finite B-algebra.' | en_new None | note 'The enumerate label uses \\emph inside the italic proposition, so it is upright.'

## 14900 (IV-2 189, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[b)]' -> '\\item[\\textup{b)}]'
Sol: already | en_old '\\item For every coherent $\\sh{O}_\\mathrm{X}$-Module $\\sh{F}$ and every subset $\\mathrm{Z}$ stable under specialisation,' | en_new None | note 'The enumerate label uses \\emph inside the italic proposition, so it is upright.'

## 14901 (IV-2 189, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[c)]' -> '\\item[\\textup{c)}]'
Sol: already | en_old '\\item For every closed subset $\\mathrm{T}$ of $\\mathrm{X}$ and every coherent $\\sh{O}_\\mathrm{U}$-Module $\\sh{G}$' | en_new None | note 'The enumerate label uses \\emph inside the italic proposition, so it is upright.'

## 14902 (IV-2 189, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[d)]' -> '\\item[\\textup{d)}]'
Sol: already | en_old '\\item For every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$, and every ideal $\\mathfrak{J}$ of height' | en_new None | note 'The enumerate label uses \\emph inside the italic proposition, so it is upright.'

## 14903 (IV-2 189, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[e)]' -> '\\item[\\textup{e)}]'
Sol: already | en_old '\\item For every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$ and every local ring $\\mathrm{C}=\\mathrm{B}_\\mathfrak{q}$ at a prime ideal $\\mathfrak{q}$ of $\\mathrm{B}$, with $\\dim(\\mathrm{C})\\geqslant 2$, the ring $\\mathrm{C}^{(\\omega)}$ is a finite C-algebra' | en_new None | note 'The enumerate label uses \\emph inside the italic proposition, so it is upright.'

## 14904 (IV-2 189, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[f)]' -> '\\item[\\textup{f)}]'
Sol: already | en_old '\\item For every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$, every local ring $\\mathrm{C}=\\mathrm{B}_\\mathfrak{q}$' | en_new None | note 'The enumerate label uses \\emph inside the italic proposition, so it is upright.'

## 14923 (IV-2 190, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[a)]' -> '\\item[\\textup{a)}]'
Sol: already | en_old '\\item For every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$, the completion $\\widehat{\\mathrm{B}}$ is strictly equidimensional' | en_new None | note 'The enumerate label uses \\emph inside the italic theorem, so it is upright.'

## 14925 (IV-2 190, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[b)]' -> '\\item[\\textup{b)}]'
Sol: already | en_old '\\item $\\mathrm{A}$ is formally catenary \\sref{IV.7.1.9}' | en_new None | note 'The enumerate label uses \\emph inside the italic theorem, so it is upright.'

## 14928 (IV-2 190, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[c)]' -> '\\item[\\textup{c)}]'
Sol: already | en_old '\\item $\\mathrm{A}$ is universally catenary \\sref{IV.5.6.2}' | en_new None | note 'The enumerate label uses \\emph inside the italic theorem, so it is upright.'

## 14931 (IV-2 190, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[d)]' -> '\\item[\\textup{d)}]'
Sol: already | en_old '\\item $\\mathrm{A}$ is universally catenary and for every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$ and every local ring $\\mathrm{C}=\\mathrm{B}_\\mathfrak{q}$ at a prime ideal $\\mathfrak{q}$ of $\\mathrm{B}$, with $\\dim(\\mathrm{C})\\geqslant 2$, the ring' | en_new None | note 'The enumerate label uses \\emph inside the italic theorem, so it is upright.'

## 14932 (IV-2 190, textup+, decisions_bulk_027): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[e)]' -> '\\item[\\textup{e)}]'
Sol: already | en_old '\\item $\\mathrm{A}$ is universally catenary and for every integral quotient ring $\\mathrm{B}$ of $\\mathrm{A}$ and every local ring $\\mathrm{C}=\\mathrm{B}_\\mathfrak{q}$ at a prime ideal $\\mathfrak{q}$ of $\\mathrm{B}$, with $\\dim(\\mathrm{C})\\geqslant 2$, the completed ring' | en_new None | note 'The enumerate label uses \\emph inside the italic theorem, so it is upright.'

## 15541 (IV-2 207, textup+, decisions_bulk_028): not_applicable for a textup+ fix
FR: '(la propriété $\\boldsymbol P$ étant définie à\npartir de $\\boldsymbol R$ par (7.5.0))' -> '\\textup{(la propriété $\\boldsymbol P$ étant définie à\npartir de $\\boldsymbol R$ par (7.5.0))}'
Sol: not_applicable | en_old None | en_new None | note 'The English recasts this as a clause without parentheses.'

## 15542 (IV-2 207, textup+, decisions_bulk_028): not_applicable for a textup+ fix
FR: "(ce qui signifie que\npour toute extension finie $k'$ de $k$ et pour chacun des anneaux locaux\ncomplets $B_i$ dont le composé direct est $B\\otimes_k k'$,\n$\\boldsymbol R(B_i)$ est vraie)" -> "\\textup{(ce qui signifie que\npour toute extension finie $k'$ de $k$ et pour chacun des anneaux locaux\ncomplets $B_i$ dont le composé direct est $B\\otimes_k k'$,\n$\\boldsymbol R(B_i)$ est vraie)}"
Sol: not_applicable | en_old None | en_new None | note 'The English recasts this as a separate clause without parentheses.'

## 15560 (IV-2 208, emph+, decisions_bulk_028): already: the fix adds an emphasis but the quoted English has none
FR: '(6.7.7, b))' -> '(6.7.7, \\emph{b)})'
Sol: already | en_old '\\sref{IV.6.7.7},~$b)$' | en_new None | note 'The mathematical letter b is already italic.'

## 15801 (IV-3 13, textup+, decisions_bulk_029): already: en_old missing or not found
FR: '(et alors on a\n$u_\\mu^{-1}(E_\\mu)\\subset u_\\mu^{-1}(F_\\mu)$ pour $\\mu\\geq\\lambda$)' -> '\\textup{(et alors on a\n$u_\\mu^{-1}(E_\\mu)\\subset u_\\mu^{-1}(F_\\mu)$ pour $\\mu\\geq\\lambda$)}'
Sol: already | en_old '\\textup{(and then we also have $u_\\mu^{-1}(\\mathrm{E}_\\mu)\\subset u_\\mu^{-1}(\\mathrm{F}_\\mu)$ for}\n\\oldpage[IV-3]{13}\n\\textup{$\\mu\\geqslant\\lambda$)}' | en_new None | note None

## 15946 (IV-3 29, textup+, decisions_bulk_029): apply: en_old not found exactly once on pages p-1..p+1
FR: '\\end{equation}\nest injectif (resp. bijectif).' -> '\\end{equation}\nest injectif \\textup{(resp.} bijectif\\textup{)}.'
Sol: apply | en_old 'is injective (resp.\\ bijective).\n\\end{lemma}' | en_new 'is injective \\textup{(resp.} bijective\\textup{)}.\n\\end{lemma}' | note None

## 16101 (IV-3 40, textup+, decisions_bulk_029): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '1\\textsuperscript{o} $p$' -> '\\textup{1\\textsuperscript{o}} $p$'
Sol: already | en_old '$1^\\circ$ $p$ is projective;' | en_new None | note 'The English label is already in math mode and upright.'

## 16102 (IV-3 40, textup+, decisions_bulk_029): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '2\\textsuperscript{o} $g$' -> '\\textup{2\\textsuperscript{o}} $g$'
Sol: already | en_old '$2^\\circ$ $g$ is projective and surjective;' | en_new None | note 'The English label is already in math mode and upright.'

## 16103 (IV-3 40, textup+, decisions_bulk_029): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '3\\textsuperscript{o} $j$' -> '\\textup{3\\textsuperscript{o}} $j$'
Sol: already | en_old '$3^\\circ$ $j$ is an open immersion.' | en_new None | note 'The English label is already in math mode and upright.'

## 16688 (IV-3 60, textup+, decisions_bulk_030): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'Y_{\\lambda,s_\\lambda}$). Alors' -> 'Y_{\\lambda,s_\\lambda}$\\textup{)}. Alors'
Sol: already | en_old '$f_{\\lambda,s_\\lambda}=f_\\lambda\\times 1:X_{\\lambda,s_\\lambda}\\to Y_{\\lambda,s_\\lambda}$\\textnormal{)}.' | en_new None | note None

## 16525 (IV-3 97, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: 'on dit que $X_0$ est \\emph{très dense} dans $X$.' -> 'on dit que $X_0$ est très dense dans $X$.'
Sol: already | en_old 'we say that $X_0$ is \\emph{very dense} in $X$.' | en_new None | note 'The English definition style already italicizes the defined term.'

## 16538 (IV-3 98, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: '\\emph{quasi-homéomorphisme} de' -> 'quasi-homéomorphisme de'
Sol: already | en_old 'we say that $f$ is a \\emph{quasi-homeomorphism} of $X_0$ into $X$.' | en_new None | note 'The English definition style already italicizes the defined term.'

## 16737 (IV-3 101, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: 'un \\emph{espace de Jacobson} si' -> 'un espace de Jacobson si'
Sol: already | en_old 'a topological space $X$ is a \\emph{Jacobson space} if' | en_new None | note 'The English definition style already italicizes the defined term.'

## 16740 (IV-3 101, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: '\\emph{préschéma de Jacobson} si' -> 'préschéma de Jacobson si'
Sol: already | en_old 'a prescheme $X$ is a \\emph{Jacobson prescheme} if' | en_new None | note 'The English definition style already italicizes the defined term.'

## 16741 (IV-3 101, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: '\\emph{anneau de Jacobson} si' -> 'anneau de Jacobson si'
Sol: already | en_old 'a ring $A$ is a \\emph{Jacobson ring} if' | en_new None | note 'The English definition style already italicizes the defined term.'

## 16971 (IV-3 110, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: '\\emph{profondeur rectifiée de $\\mathcal F$\nau point $x$}' -> 'profondeur rectifiée de $\\mathcal F$\nau point $x$'
Sol: already | en_old 'we call \\emph{rectified depth} of $\\sh{F}$ at the point $x$' | en_new None | note 'The English definition style already italicizes the defined term.'

## 16972 (IV-3 110, emph-, decisions_bulk_030): already: the fix removes an emphasis but the quoted English has one
FR: '\\emph{profondeur rectifiée de $\\mathcal F$ le long de $Z$}' -> 'profondeur rectifiée de $\\mathcal F$ le long de $Z$'
Sol: already | en_old '\\emph{rectified depth of $\\sh{F}$ along $Z$}' | en_new None | note 'The English definition style already italicizes the defined phrase.'

## 17339 (IV-3 138, textup+, decisions_bulk_031): apply: en_old not found exactly once on pages p-1..p+1
FR: 'conjonction de a) et\nb) implique c), et c) implique a).' -> 'conjonction de \\textup{a)} et\n\\textup{b)} implique \\textup{c)}, et \\textup{c)} implique \\textup{a)}.'
Sol: apply | en_old 'the conjunction of $a)$ and $b)$ implies $c)$, and $c)$ implies $a)$).' | en_new 'the conjunction of \\textup{a)} and \\textup{b)} implies \\textup{c)}, and \\textup{c)} implies \\textup{a)}).' | note None

## 17704 (IV-3 148, emph+, decisions_bulk_032): apply: en_old not found exactly once on pages p-1..p+1
FR: 'sous-anneaux locaux' -> 'sous-anneaux \\emph{locaux}'
Sol: apply | en_old "inductive limit of its local sub-rings $\\mathrm{B}'_\\lambda$" | en_new "inductive limit of its \\emph{local} sub-rings $\\mathrm{B}'_\\lambda$" | note None

## 17612 (IV-3 158, emph+, decisions_bulk_032): apply: en_old not found exactly once on pages p-1..p+1
FR: "qu'il y a un point de" -> "qu'il y a \\emph{un} point de"
Sol: apply | en_old 'we shall see that there is a point of $\\mathrm{X}_1$' | en_new 'we shall see that there is \\emph{a} point of $\\mathrm{X}_1$' | note None

## 18073 (IV-3 211, textup+, decisions_bulk_033): apply: en_old not found exactly once on pages p-1..p+1
FR: '(ou, ce qui\n  revient au même (14.3.3.1, (ii)), aux points maximaux de $X_y$)' -> '\\textup{(ou, ce qui\n  revient au même (14.3.3.1, (ii)), aux points maximaux de $X_y$)}'
Sol: apply | en_old '(or, what amounts to the same, at the maximal points of $X_y$ {\\hyperref[IV.14.3.3.1]{(14.3.3.1, (ii))}})' | en_new '\\textup{(or, what amounts to the same, at the maximal points of $X_y$ {\\hyperref[IV.14.3.3.1]{(14.3.3.1, (ii))}})}' | note None

## 18101 (IV-3 214, textup+, decisions_bulk_033): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '(\\textbf{II}, 6.3.8)' -> '\\textup{(\\textbf{II}, 6.3.8)}'
Sol: already | en_old '$Y_{\\mathrm{red}}$ \\sref[II]{II.6.3.8}.' | en_new None | note None

## 18277 (IV-3 223, textup+, decisions_bulk_034): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '(\\textbf{II}, 5.4.10)' -> '\\textup{(\\textbf{II}, 5.4.10)}'
Sol: already | en_old 'proper over $Y$ \\sref[II]{II.5.4.10}' | en_new None | note '\\sref already prints the reference upright.'

## 18903 (IV-4 22, emph~, decisions_bulk_035): not_applicable for a emph~ fix
FR: "d'une \\emph{section universelle} pour" -> "d'une «\\emph{section universelle}» pour"
Sol: not_applicable | en_old None | en_new None | note 'French guillemets.'

## 20958 (IV-4 131, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[b)] Soient $S=\\Spec(A)$' -> '\\item[\\textup{b)}] Soient $S=\\Spec(A)$'
Sol: already | en_old '\\item Let $S=\\operatorname{Spec}(A)$, $S_0=\\operatorname{Spec}(\\boldsymbol{k})$.' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 20960 (IV-4 131, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[c)] Pour tout morphisme $f:X\\to S$, séparé' -> '\\item[\\textup{c)}] Pour tout morphisme $f:X\\to S$, séparé'
Sol: already | en_old '\\item For every morphism locally of finite type $f:X\\to S$, separated, and every point $x\\in X$ such that $f(x)$ is equal to the closed point $s$ of $S$' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21039 (IV-4 136, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] Il existe une' -> '\\item[\\textup{(ii)}] Il existe une'
Sol: already | en_old "\\item There exists a local $A$-algebra $A_3$ that is strictly essentially \\'{e}tale, and two $A$-homomorphisms $A_1\\to A_3$, $A_2\\to A_3$." | en_new None | note 'The label is upright via \\emph inside the italic lemma.'

## 21049 (IV-4 137, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: "\\item[(ii)] Pour tout anneau local hensélien $B$, l'application canonique" -> "\\item[\\textup{(ii)}] Pour tout anneau local hensélien $B$, l'application canonique"
Sol: already | en_old '\\item For every Henselian local ring $B$, the canonical map' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21050 (IV-4 137, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iii)] ${}^h\\!A$ est un $A$-module fidèlement plat' -> '\\item[\\textup{(iii)}] ${}^h\\!A$ est un $A$-module fidèlement plat'
Sol: already | en_old '\\item ${}^h\\!A$ is a faithfully flat $A$-module, and if $\\mathfrak{m}$ is the maximal ideal of $A$,' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21051 (IV-4 137, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iv)] Si $\\widehat A$ et' -> '\\item[\\textup{(iv)}] Si $\\widehat A$ et'
Sol: already | en_old '\\item If $\\hat{A}$ and $({}^h\\!A)\\hat{\\phantom{x}}$ are the separated completions of the local rings $A$ and ${}^h\\!A$,' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21053 (IV-4 137, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: "\\item[(vi)] Si $A$ est hensélien, l'homomorphisme canonique" -> "\\item[\\textup{(vi)}] Si $A$ est hensélien, l'homomorphisme canonique"
Sol: already | en_old '\\item If $A$ is Henselian, the canonical homomorphism $A\\to{}^h\\!A$ is bijective.' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21052 (IV-4 137, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(v)] Pour que ${}^h\\!A$ soit noethérien' -> '\\item[\\textup{(v)}] Pour que ${}^h\\!A$ soit noethérien'
Sol: already | en_old '\\item For ${}^h\\!A$ to be Noetherian, it is necessary and sufficient that $A$ be so.' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21075 (IV-4 139, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: "\\item[(ii)] Supposons $A$ noethérien. Alors, pour tout idéal premier $\\mathfrak p$ de $A$, l'anneau $({}^h\\!A)" -> "\\item[\\textup{(ii)}] Supposons $A$ noethérien. Alors, pour tout idéal premier $\\mathfrak p$ de $A$, l'anneau $({}^h\\!A)"
Sol: already | en_old '\\item Suppose $A$ Noetherian.\n  Then, for every prime ideal $\\mathfrak{p}$ of $A$, the ring $({}^h\\!A)_{\\mathfrak{p}}/\\mathfrak{p}.({}^h\\!A)_{\\mathfrak{p}}$' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 21103 (IV-4 141, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] Le foncteur' -> '\\item[\\textup{(ii)}] Le foncteur'
Sol: already | en_old '\\item The functor $A\\leadsto{}^h\\!A$ in the category of local rings (where the morphisms are local homomorphisms) commutes with filtered inductive limits.' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21104 (IV-4 141, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iii)] Tout anneau' -> '\\item[\\textup{(iii)}] Tout anneau'
Sol: already | en_old '\\item Every Henselian local ring $A$ is an inductive limit of an inductive filtered system of Henselian and Noetherian local rings $A_\\lambda$' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21159 (IV-4 145, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] Pour tout couple' -> '\\item[\\textup{(ii)}] Pour tout couple'
Sol: already | en_old '\\item For every pair of local $A$-homomorphisms $\\beta_1:A_1\\to K$, $\\beta_2:A_2\\to K$' | en_new None | note 'The label is upright via \\emph inside the italic lemma.'

## 21187 (IV-4 146, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] Pour tout homomorphisme local' -> '\\item[\\textup{(ii)}] Pour tout homomorphisme local'
Sol: already | en_old '\\item For every local homomorphism $u:A\\to B$, where $B$ is a strictly local ring,' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21190 (IV-4 147, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iii)] ${}^{hs}\\!A_{(i)}$' -> '\\item[\\textup{(iii)}] ${}^{hs}\\!A_{(i)}$'
Sol: already | en_old '\\item ${}^{hs}\\!A_{(i)}$ is a faithfully flat $A$-module,' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21192 (IV-4 147, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iv)] Pour que' -> '\\item[\\textup{(iv)}] Pour que'
Sol: already | en_old '\\item For ${}^{hs}\\!A_{(i)}$ to be Noetherian, it is necessary and sufficient that $A$ be so.' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21195 (IV-4 147, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: "\\item[(vi)] Si $i'" -> "\\item[\\textup{(vi)}] Si $i'"
Sol: already | en_old "\\item If $i':k\\to\\Omega'$ is a second homomorphism from $k$ into a separable closure of $k$," | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21193 (IV-4 147, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(v)] Si $A$' -> '\\item[\\textup{(v)}] Si $A$'
Sol: already | en_old '\\item If $A$ is strictly local (hence $\\Omega=k$), one has ${}^{hs}\\!A\\cong A$.' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21221 (IV-4 149, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] Supposons $A$ noethérien' -> '\\item[\\textup{(ii)}] Supposons $A$ noethérien'
Sol: already | en_old '\\item Suppose $A$ Noetherian.\n  Then, for every prime ideal $\\mathfrak{p}$ of $A$, the ring $({}^{hs}\\!A)_{\\mathfrak{p}}/\\mathfrak{p}.({}^{hs}\\!A)_{\\mathfrak{p}}$' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21243 (IV-4 150, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] Le foncteur' -> '\\item[\\textup{(ii)}] Le foncteur'
Sol: already | en_old '\\item The functor $A\\leadsto{}^{hs}\\!A$ in the category of local rings (where the morphisms are local homomorphisms) commutes with filtered inductive limits.' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21244 (IV-4 150, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(iii)] Tout anneau' -> '\\item[\\textup{(iii)}] Tout anneau'
Sol: already | en_old '\\item Every strictly local ring $A$ is an inductive limit of a filtered inductive system of Noetherian strictly local rings (the transition homomorphisms being local).' | en_new None | note 'The label is upright via \\emph inside the italic proposition.'

## 21300 (IV-4 153, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: '\\item[(ii)] $A$ est intègre' -> '\\item[\\textup{(ii)}] $A$ est intègre'
Sol: already | en_old '\\item $A$ is integral, geometrically unibranch and $\\dim(A)\\geq 1$.' | en_new None | note 'The label is upright via \\emph inside the italic lemma.'

## 21358 (IV-4 157, textup+, decisions_bulk_038): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: "\\item[(ii)] l'homomorphisme" -> "\\item[\\textup{(ii)}] l'homomorphisme"
Sol: already | en_old '\\item the homomorphism $\\sh{O}_{Y,y}\\to\\sh{O}_{X,x}$ is injective.\n\\end{enumerate}\n\nMoreover, if this is the case,' | en_new None | note 'The label is upright via \\emph inside the italic theorem.'

## 22088 (IV-4 193, textup+, decisions_bulk_040): not_applicable for a textup+ fix
FR: '(ce qui équivaut à dire, compte tenu de (i), que toutes les fibres $g^{-1}(g(y))$ de $g$ sont des préschémas de Cohen-Macaulay)' -> '\\textup{(ce qui équivaut à dire, compte tenu de (i), que toutes les fibres $g^{-1}(g(y))$ de $g$ sont des préschémas de Cohen-Macaulay)}'
Sol: not_applicable | en_old None | en_new None | note 'The English uses a separate non-parenthetical clause rather than the French parenthesis.'

## 22102 (IV-4 194, textup+, decisions_bulk_040): not_applicable for a textup+ fix
FR: "soit régulier (i.e. (16.9.7) engendré par une suite régulière d'éléments de $B$)." -> "soit régulier \\textup{(i.e. (16.9.7)} engendré par une suite régulière d'éléments de $B$\\textup{)}."
Sol: not_applicable | en_old None | en_new None | note "The English uses non-parenthetical 'that is'; there is no corresponding parenthesis."

## 22288 (IV-4 205, textup+, decisions_bulk_040): already: the fix sets text upright, the quoted English has no upright markup and is inside an italic statement
FR: 'que les $f_i$ ($1\\leq i\\leq n$) appartiennent' -> 'que les $f_i$ \\textup{($1\\leq i\\leq n$)} appartiennent'
Sol: already | en_old 'that the $f_i$ $(1\\leqslant i\\leqslant n)$ belong to the radical of $\\mathrm{A}$' | en_new None | note 'The parentheses are in math mode and already upright.'

## 23879 (IV-4 316, emph-, decisions_bulk_043): already: the fix removes an emphasis but the quoted English has one
FR: 'anneau local $A$ est \\emph{parafactoriel} si,' -> 'anneau local $A$ est parafactoriel si,'
Sol: already | en_old 'We say that a \\emph{local ring} $\\mathrm{A}$ is parafactorial if,' | en_new None | note None
