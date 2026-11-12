# Suspected errors in the French text (transcription or original), noted while translating

196 entries, in the order of the edition.


## ega0-1-7__0.1-fr

- 0.1.2.4 — "(pour la structure de $B$-module sur $N$ définie par $u:A\to B$)": the structure on $N$ defined by $u$ is an $A$-module structure, so "$B$-module" looks like an error for "$A$-module". Translated as written.

## ega0-1-7__0.3-fr.part01

- 0.3.5.3 — the closing parenthesis of the prose aside "(autrement dit un homomorphisme …)" sits inside the math: `$\mathcal{G}\to\psi_*(\mathcal{G}'))$`. Copied as is.
- subsection 3.5 "Images réciproques de préfaisceaux" has no \label (the other subsections have subsection:0.3.x-fr). Kept unlabelled.
- 0.3.5.4 — French spacing `~;` inside the display ending in $\psi_*(\psi^*(\mathcal{G}_2))$. Kept, since mathematics is copied verbatim.

## ega0-1-7__0.3-fr.part02

- 3.7.1 — `v^b`, `(u^\sharp)^b`, `(v^b)^\sharp` use the letter b where EGA's notation is presumably ♭ (this transcription writes `v^\flat` in 4.4.3); copied as is.

## ega0-1-7__0.4-fr

- 4.1.2 — `(j,\omega^b)`: letter b where ♭ is presumably meant (cf. `v^\flat` in 4.4.3); copied as is.
- 4.1.5, 4.1.7, 4.2.2 — a blank line before `\oldpage` (pp. 38, 39, 40) starts a new paragraph in mid-sentence; kept as in the French.
- 4.1.7 — the glued space is referred to as $X$ ("la partie ouverte $X'_\lambda$ correspondante dans $X$") without having been named; "$X$" may be missing after "l'espace topologique".
- 4.4.3 — "homomorphisme de $\psi^*(\mathcal{B})$-modules" (lowercase) where the same structure is called "$\psi^*(\mathcal{B})$-Modules" a few lines later; lowercase kept.
- 4.4.8 — $v$ in $v''=v\circ v'$ is not introduced in the paragraph (presumably a homomorphism from $\mathcal{G}$ to $\mathcal{F}$ as in 4.4.1); translated as is.
- 4.3.2, 4.3.5, (4.4.3.2), (4.4.3.3), 4.4.6, 4.4.8 — French `~;` inside display math; kept, since mathematics is copied verbatim.

## ega0-1-7__0.5-fr.part01

- 5.2.4 — "$f^*(\mathcal{G})$ est un $\mathcal{O}_X$-module de type fini" (lowercase, elsewhere "Module" for sheaves); lowercase kept.
- 5.2.7, 5.4.1, 5.4.4, 5.4.7 — blank lines around `\oldpage` (pp. 47, 49, 50, 52) split a sentence into separate paragraphs; kept as in the French.
- 5.4.6 — `\tag{4.3.3.1}` prints the justifying reference (4.3.3.1) beside the display as if it were an equation number (same number as the tag in 4.3.3); kept.
- 5.4.8 — `\omega^\#` where `\omega^\sharp` is presumably meant; copied as is.

## ega0-1-7__0.6-fr

- numbering — env numbers jump from 6.7.6 to 6.7.8 (no 6.7.7); check the scan for an omitted item or an original numbering gap.
- 0.6.6.2-fr — "$\varphi^{-1}(\mathfrak n)\cap A$": the "$\cap A$" is redundant for a preimage in $A$, and $\varphi$ is not introduced in 6.6.2 (only "$A\to B$"); possibly "$\mathfrak n\cap A$" or "$\varphi^{-1}(\mathfrak n)$" in the original.

## ega0-1-7__0.7-fr.part01

- 0.7.3.5-fr proof — "Enfin, a) entraîne b)", but the argument shows that every module of finite type is separated, i.e. c); harmless since b)⟺c) was shown just before, but possibly "c)" in the original.
- 0.7.4.2-fr proof — references written "(I.7.4)", "(I.7.2)", "(I.7.5)", a form used nowhere else in these chunks; check the intended target (e.g. "(1.7.4)" or a [I] reference).

## ega0-1-7__0.7-fr.part02

- 0.7.6.16-fr — the statement assumes only "anneau noethérien", but the proof uses (7.6.14), whose hypotheses (7.6.13) require $A$ to be a Noetherian adic ring; "adique" may be missing.

## ega1-3__I.3-fr.part02

- after Def. 3.5.4 (I.3.5.4-fr): "(T, 1.1)", whereas the chunk elsewhere cites "(T, I, 1.1)"; kept as is.
- 3.6.4 (I.3.6.4-fr): optional argument "3.6.4) («~transitivité des fibres~»" has unbalanced parentheses (heading workaround); structure kept, only the quoted words translated.

## ega1-4__I.4-fr

- 4.4.3 (I.4.4.3-fr): "canoniquement isomorphée" is a garbled "isomorphe"; translated "canonically isomorphic".
- 4.1.7, 4.1.9 (I.4.1.7-fr, I.4.1.9-fr): $\omega^b$ presumably renders $\omega^\flat$ (same convention in 0, 4); math copied unchanged.

## ega1-5__I.5-fr.part01

- 5.1.2 proof: "du sous-préschéma fermé défini $Y$ par $\mathscr{N}_X$", word-order slip; rendered "the closed sub-prescheme $Y$ defined by $\mathscr{N}_X$".
- 5.1.5: "$(\psi,\omega^b)$", where "^b" presumably stands for $\flat$ (the same form occurs in 0 §§3–4); math kept.
- 5.1.5: "l'homomor-" / "phisme" is split across \oldpage[I]{129}; kept as "homomor-" / "phism" at the same place (renders "homomor- phism", as the French does).
- numbering: Proposition 5.3.2 is followed directly by Corollary 5.3.4; there is no 5.3.3 (omitted statement or numbering slip; not checked against the original).
- 5.3.9 proof opens with errata wording ("Pour avoir une démonstration correcte, il suffit d'utiliser (4.2.4, $a$) : …", with French spacing unlike the rest); apparently the published correction inserted in place of the proof. Translated as it stands ("To obtain a correct proof, …").
- blank lines (paragraph breaks) inside a sentence before \oldpage[I]{131} and \oldpage[I]{135}; kept.

## ega1-5__I.5-fr.part02

- 5.5.1, proof of (ii): the composite of the closed immersions $\Delta_{X|Y}$ and $j$ is justified by (4.2.4); the statement on composites is (4.2.5), while (4.2.4) is the local criterion.
- remark after 5.5.5 ("La prop. (5.5.4) permet, en prenant un recouvrement de $Y$ par des ouverts affines, …") and proof of 5.5.9 (both necessity and sufficiency): (5.5.4) is cited where the argument uses the open-covering criterion (5.5.5).
- 5.5.11, second example: "$\mathfrak{j}_y\neq(0)$ … pour $\mathfrak{j}_y=(0)$, $f^{-1}(y)$ se compose de deux points". The doubled point is the origin, $\mathfrak{j}_y=(s)$; over the generic point $(0)$ the fibre is one point. Probably $(s)$ in both places; math kept.
- blank lines (paragraph breaks) inside a sentence before \oldpage[I]{137} and \oldpage[I]{139}; kept.

## ega1-6__I.6-fr.part01

- blank line (paragraph break) inside a sentence, splitting "\emph{Tout sous-$\mathscr{O}_X$-}" / "\emph{Module …}" before \oldpage[I]{141}, and another before \oldpage[I]{146}; kept.

## ega1-7__I.7-fr

- 7.4.5 proof — the display `\[ ... =(R(X))^{(I)}~; \]` contains the French `~;` inside the mathematics; kept verbatim (math is copied), so the English output has a space before that semicolon.

## ega1-8__I.8-fr

- 8.1.3 proof — "comme $A-\mathfrak p\subset M$, on a $A_\mathfrak p\subset M$": the inference needs the elements of $A-\mathfrak p$ to be invertible in $M$, i.e. $A-\mathfrak p\subset M-\mathfrak m(M)$; "$-\mathfrak m(M)$" may have been dropped. Translated as written.
- 8.2.2 proof — "$x\in V(\mathfrak a)=W\cap F$ pour $x\in U$": since $F=W\cap V(\mathfrak a)$, the equality $V(\mathfrak a)=W\cap F$ does not hold as written (expected something like $W\cap V(\mathfrak a)=F$ for $x\in W$). Translated as written.
- 8.2.8 proof and 8.3.2 — a blank line before `\oldpage[I]{168}` and before `\oldpage[I]{169}` splits a sentence into two paragraphs; kept as in the French.

## ega1-9__I.9-fr.part01

- (9.1.13.1) — `\operatorname{Supp}(p^{-1}(\mathscr{F}))`: the reduction is to $\mathscr{F}\otimes_S\mathscr{O}_Y=p^*(\mathscr{F})$, and the stalk argument that follows ($\mathscr{O}_z/\mathfrak{m}_x\mathscr{O}_z\neq0$) is needed only for $p^*$; expected `p^*(\mathscr{F})`. Kept as in the French.
- proof after (9.1.1) — "si $\mathscr{F}$ est cohérent, on peut supposer qu'il est le conoyau…": the quasi-coherent $\mathscr{H}om$ assertion needs this reduction for $\mathscr{F}$ of finite presentation; the original may read "admet une présentation finie". Translated as written.

## ega1-9__I.9-fr.part02

- proof of (9.5.2) — the closed sub-prescheme called $Y'$ in (9.5.1)/(9.5.2) is written $X'$ throughout the proof (the competitor is $X''$); notation mismatch, possibly already in the original. Kept as in the French.
- (9.5.10) — the statement names the injection $i:Y\to X$, but the proof applies (9.5.1) "à l'injection $j$"; possibly original. Kept.

## ega1-10__I.10-fr.part01

- (10.3.6) proof display — `\Gamma\bigl(\mathfrak{D}(f^n),(\mathfrak{J}^n)^\Delta\bigr)`: the chain concerns $\mathfrak{D}(f)$; expected `\mathfrak{D}(f)` (harmless, since $\mathfrak{D}(f^n)=\mathfrak{D}(f)$). Kept.
- proof of (10.5.4), affine case — cites (10.3.4) (restriction to $\mathfrak{D}(f)$), but the argument rests on the description of all ideals of definition of $\operatorname{Spf}(A)$ in (10.3.5); possibly (10.3.5) intended. Kept.
- proof of (10.5.6)(i) — `(\psi,\omega^b)`: EGA writes the adjoint as $\omega^\flat$ (cf. $\theta^\sharp$); `^b` is probably a rendering of `^\flat`. Kept.

## ega1-10__I.10-fr.part02

- (10.6.2) proof — `$g=(\psi,\omega^b)$`: the map $\mathscr{O}_{\mathfrak{Y}}\to\psi_*(\mathscr{O}_{\mathfrak{X}})$ deduced from $\omega$ is EGA's $\omega^\flat$ (counterpart of the $\theta_\lambda^\sharp$ used just before); "^b" looks like a transcription of the flat sign. Kept.
- (10.6.3) b) — "pour tout $x\in X$": no $X$ is defined in 10.6.3 (the space is $\mathfrak{X}$); presumably $x\in\mathfrak{X}$. Kept.
- (10.6.4) statement — $\mathscr{J}$ in "$\mathscr{J}^{(n)}=\mathscr{J}^{n+1}$" and "$\mathscr{J}/\mathscr{J}^2$" is never defined; the conclusion $\mathscr{J}/\mathscr{J}^2\cong\mathscr{J}_1$ requires $\mathscr{J}=\mathscr{J}^{(0)}$; a defining clause may be missing. Translated as written.
- (10.6.4) proof — "$\mathscr{J}_{ij}=\widetilde{\mathfrak{J}_{ji}}$": 10.6.3 defines no $\mathscr{J}_{ij}$ (it shows that the kernel of $u_{ji}$ is $\widetilde{\mathfrak{J}_{ji}}$); possibly $\mathscr{J}_{ji}$, or the original's shorthand for that kernel. Kept.

## ega1-10__I.10-fr.part03

- (10.8.8, (i)) third display — ends with the French punctuation `~;` inside the math (`\widehat{M''}~;`); kept verbatim because mathematics is copied unchanged (English typography would be `;`).

## ega1-10__I.10-fr.part04

- proof of (10.12.3.1) — no punctuation after the display $\mathfrak{K}/\mathfrak{K}^{n+1}=(B/\mathfrak{K}^{n+1})\rho_n(\ldots)$; the following "comme l'homomorphisme $\rho$ … est égal à $\varprojlim\rho_n$" begins a new statement (a ";" is probably lost). Translated as written ("since …", lowercase).

## ega1-10__I.10-fr.part05

- (10.15.5) — "$\mathfrak{X}$ un $\mathfrak{S}$-préschéma de type fini": elsewhere "$\mathfrak{S}$-préschéma formel" (10.13.3, 10.15.4); "formel" may be missing. Translated as written ("an $\mathfrak{S}$-prescheme of finite type").

## ega2-1-8__II.1-fr.part01

- proof of (1.2.7) — "$U=D(\lambda)$, avec $\lambda\in S$": $D(\lambda)$ needs an element of the ring $A$ of $S$; $\lambda\in A$ expected. Translated as written.
- proof of (1.3.7) — "comme $\Gamma(U,\widetilde{B})=B$": no $U$ is introduced in this proof; $\Gamma(S,\widetilde{B})=B$ expected. Translated as written.
- proof of (1.4.5) — "où $B$ est une $A$-algèbre de type fini (I, 9.6.2)": (1.4.5) does not assume $\mathcal{B}$ of finite type; possibly already in the original. Translated as written.

## ega2-1-8__II.2-fr.part01

- 2.2.2 (proof) — reference text "0, I.4.6" for label key 0.1.4.6; the "I" looks like a misread "1" (0, 1.4.6). Kept as in the French.
- 2.2.3 — same: reference text "0, I.4.1" for label key 0.1.4.1. Kept.
- 2.2.7 — "formé des éléments d'ordre $0$": elsewhere the text says "de degré $0$"; possibly "de degré" in the original. Translated literally "of order $0$".

## ega2-1-8__II.2-fr.part02

- 2.6.4 — "un $\mathcal{O}_X$ module" lacks the hyphen (and capital M) of "$\mathcal{O}_X$-Module"; rendered "$\mathcal{O}_X$-module".
- 2.6.2 — the word "canoni-/quement" is split across \oldpage[II]{37} (with blank lines around the marker); the English keeps "canonically" whole before the marker, blank lines unchanged.

## ega2-1-8__II.3-fr.part02

- 3.4.7 (Remarks), affine case: "$t_i$ soit la restriction à $p^{-1}(U)$ de $s_ig^n$" does not fit the following "$b_i=a_i(g|W)^{-n}$", which needs $g^nt_i=s_i|p^{-1}(U)$. Translated as written.
- 3.6.2, proof of (i): "on a $G(\varphi)=X$". Here $\varphi:\mathcal S\to\mathcal S'$, so by 3.5.1 $G(\varphi)$ is an open subset of $\operatorname{Proj}(\mathcal S')$, and one expects $G(\varphi)=\operatorname{Proj}(\mathcal S')$ (possibly already in the original). Translated as written.
- 3.6.4, proof: reference "(3.6.1, (i))". 3.6.1 has no item (i); the closed-immersion statement used is 3.6.2, (i). Reference kept.

## ega2-1-8__II.3-fr.part03

- 3.8.2, proof: "la restriction de $r$ à $U_\alpha$ soit une immersion fermée de $V_\alpha$ dans $D_+(s_\alpha)$". $U_\alpha$ is not defined; $V_\alpha=r^{-1}(D_+(s_\alpha))$ is meant. Translated as written.
- 3.8.5, proof: "Comme $q^{-1}(U_i)$ est compact". In EGA's terminology this should be "quasi-compact" ($q$ of finite type). Translated as "compact".
- 3.8.5, proof: "une puissance $s_{ij}^\rho$ telle que $\rho m_{ijk}n_{ij}=n$". For $s_{ij}^\rho\in S_n$ and $t_{ijk}s_{ij}^{\rho-m_{ijk}}\in S_n$ one needs $\rho n_{ij}=n$. Translated as written.
- 3.8.5, proof: "un sous-$\mathcal O_Y$-Module cohérent de type fini $\mathcal E_i$". (I, 9.4.7) and the statement concern quasi-coherent submodules of finite type; "quasi-cohérent" expected. Translated as "coherent".
- 3.8.5, proof, last line: "tel que $f|V$ soit une base". $f$ is not defined here; $f_{ij}|V$ is meant. Translated as written.

## ega2-1-8__II.4-fr.part01

- 4.3.2, before Lemma 4.3.2.4: "(en revenant au cas affine, à l'aide de (I, 3.2.7 et (3.2.3))". One closing parenthesis is missing, and the second reference (label I.3.2.3) is displayed as "3.2.3" without "I,"; probably "(I, 3.2.7 et 3.2.3)". Kept as in the French.
- 4.2.1: "un faisceau inversible $\mathcal L_r$ sur $\mathcal O_X$"; "sur $X$" (or "$\mathcal O_X$-Module inversible") expected. Translated literally.

## ega2-1-8__II.4-fr.part03

- 4.5.4 (proof) — "idéaux premiers gradués $\mathfrak{p}_i$ de $S_+$": the points of $\operatorname{Proj}(S)$ are graded prime ideals of $S$ not containing $S_+$ (2.3.1); "de $S$" expected. Translated as written ("of $S_+$").
- 4.5.10.1 — "la conclusion résulte de (4.5.5, d'))": the step needs $\mathcal{E}(n)$ generated by its sections for every large $n$, which is d) of (4.5.5); d') gives only one $n$. Possibly "d)" in the original. Reference kept as "4.5.5, d')".
- proof of (4.5.13.3) — "(resp. $\Gamma(U_\alpha,\mathcal{O}_Z(q))$ soit": the closing parenthesis of the "resp." clause is missing; kept unbalanced as in the French.

## ega2-1-8__II.4-fr.part04

- 4.6.13, proof of (ii) — plain-text reference "(4.6.1.13, (i))" after $X_{s'_i}=f^{-1}(Y_{s_i})$: evidently Lemma (4.6.13.1, (i)) with digits transposed (and not linked). Kept as written.
- 4.6.13, proof of (ii) — "$t_{ij}\in\Gamma(X,\mathcal{L}^{\otimes n_{ij}})$": the $t_{ij}$ come from the ampleness of $\mathcal{L}|X_{s'_i}$ and $t_{ij}\otimes s_i'^{\otimes m}$ is then extended from $X_{s'_i}$ to $X$ by (I, 9.3.1), so sections over $X_{s'_i}$ ($\Gamma(X_{s'_i},\dots)$) are expected. Math copied unchanged.
- 4.6.13, proof of (ii) — "par définition des images réciproques ((0, 3.7.1) et (4.4.1))": the second reference is linked to II.4.4.1 (immersions into projective bundles), which does not concern inverse images; a Chapter 0 number (e.g. 0, 4.4.1) may be meant. Kept as written.

## ega2-1-8__II.5-fr.part01

- 5.2.1 proof (c') implies b)) — "$x\in X_f\subset X-U$": $U$ is an open neighbourhood of $x$, and $f$ vanishes on $X-U$ with $f(x)=1_x$, so the argument gives $X_f\subset U$. Copied as is.
- 5.4.2 proof — "(I, 4.3.2 et 3.3.3)" links 3.3.3 to key II.3.3.3-fr (about $X_f$ in Proj); the fact used, $Y\times_YY'=Y'$, is I, 3.3.3 ($X\times_SS=X$). Key kept.
- 5.4.2 proof display — French `~;` inside \[…\] after $X\times_YZ$; kept, since mathematics is copied verbatim.
- after 5.3.1 — "Nagata [26]" is plain text, whereas 5.5.4 (iv) (part02) writes \cite{II-26}; kept.
- proof of 5.1.6, proof of 5.2.1, 5.4.9 — blank lines around \oldpage (pp. 96, 98, 103) split a sentence into two paragraphs; kept as in the French.

## ega2-1-8__II.5-fr.part02

- 5.5.4 (iii) — "$\mathcal{S}_y=\mathbf{S}_{k(y)}((k(y))^{r+1})$ (1.7.3)": (1.7.3) (symmetric algebra and localization) gives the stalk $\mathbf{S}_{\mathcal{O}_y}(\mathcal{O}_y^{r+1})$; the form over $k(y)$ is the fibre $\mathcal{S}_y\otimes k(y)$ used in 5.5.3. Possibly in the original; copied as is.
- 5.6.1 B) — the quasi-compact immersion $S_i\to S$ is justified by "(5.3.4, (ii))" and the composite $T_{ij}\to S$ by "(5.3.4, (iii))"; by the statement of 5.3.4 these are (i) (quasi-compact immersion) and (ii) (composition), (iii) being base change. Kept.
- 5.6.1 A), C), D) and 5.6.3 — blank lines around \oldpage (pp. 107–110) split a sentence into two paragraphs; kept as in the French.

## ega2-1-8__II.6-fr.part01

- 6.1.10, proof: "(6.1.5, (vii))" is cited for the reduction to reduced $X$, $Y$; Proposition 6.1.5 has only (i)–(vi), and the statement on $f_{\mathrm{red}}$ is (vi). Kept "(vii)".
- remark after 6.2.3: "tout morphisme fini est quasi-fini (6.1.8)"; finite discrete fibres of a finite morphism are (6.1.7), while (6.1.8) concerns function fields. Kept "6.1.8".
- 6.2.4 (iv): the display reads $f\times_S g:X\times_S Y\to X'\times_S Y'$ for $f:X\to Y$, $g:X'\to Y'$; it should be $X\times_S X'\to Y\times_S Y'$ (as in 6.1.5 (iv)). Math kept.
- 6.3.9: "$X'$ (resp. $Y'$) est un préschéma intègre et normal (6.3.6)"; integrality, normality and the function field are stated in Proposition (6.3.7), so (6.3.7) may be intended. Kept.
- blank lines (paragraph breaks) inside sentences at \oldpage[II]{113}, {114}, {116}, {118}, {120}; kept.

## ega2-1-8__II.6-fr.part02

- 6.5.1, display (6.5.1.2) `...=1_{\mathcal{A}}~;` has the French `~;` inside the mathematics; kept verbatim (math is copied), so a space precedes that semicolon in the English.
- 6.4.9: "endomorphisme" is split "endo-" / "morphisme" across \oldpage[II]{125} with blank lines; kept as "endo-" / "morphism".
- blank lines (paragraph breaks) inside sentences at \oldpage[II]{123} and {127}; kept.
- 6.4.7, last paragraph: "les formules (6.4.1.3) et (6.4.1.5) ont un sens et sont valables"; extending the proof of 6.4.5 also needs (6.4.1.4), so "(6.4.1.3) à (6.4.1.5)" (as in 6.4.2) may be intended. Kept "and".

## ega2-1-8__II.8-fr.part01

- remark after (8.1.3), "Lorsqu'on remplace $\mathcal{I}$ par $\mathcal{I}^d$ ... canoniquement isomorphe $X'$ (8.1.1)": (8.1.1) only treats the twist by an invertible $\mathcal{J}$; replacing $\mathcal{I}$ by $\mathcal{I}^d$ replaces $\mathcal{S}$ by $\mathcal{S}^{(d)}$, for which (3.1.8) would be expected. Possibly already in the original; translated as written.

## ega2-1-8__II.8-fr.part02

- (8.4.3) "les immersions canoniques $E\to\widehat{E}$ et $\widehat{E}\to\widehat{C}$": the justification just given (the underlying spaces of $E$ and $\widehat{E}$ are non-closed open subsets of $\widehat{C}$) points to $E\to\widehat{C}$ for the first immersion. Possibly already in the original; translated as written.

## ega2-1-8__II.8-fr.part03

- 8.8.3, second paragraph: "la \emph{section nulle} de $\mathbf{V}(\mathcal{L})$ (identifiée à $Y$)". The zero section of $\mathbf{V}(\mathcal{L})$ is $j(X)\cong X$ (8.8.2), so "identifiée à $X$" is expected. Translated as written ("identified with $Y$").

## ega2-1-8__II.8-fr.part04

- 8.10.6: the page marker \oldpage[II]{188} falls inside "quasi-cohérent" ("un faisceau quasi-", blank line, \oldpage, "cohérent"), so the paragraph breaks in mid-word. Mirrored in the English ("quasi-" / "coherent").
- 8.11.6, statement: "supposons outre que"; "en" is missing ("supposons en outre que"). Translated "suppose moreover that".

## ega2-1-8__II.8-fr.part05

- 8.12.1: "un $\mathcal{O}_{\widehat{C}}$-Module gradué quasi-cohérent $\operatorname{Proj}_0(\widehat{\mathcal{M}})$". $\operatorname{Proj}_0$ of a graded $\widehat{\mathcal{S}}$-module is an ungraded $\mathcal{O}_{\widehat{C}}$-module, so "gradué" looks misplaced (possibly already in the printed text). Translated as written.
- 8.12.5, second paragraph: "et $\mathcal{S}_X$ par $(\mathcal{S}_X^{\geq})^{\wedge}$". (8.12.5.1) contains $\mathcal{S}_X^{\geq}$, not $\mathcal{S}_X$; "$\mathcal{S}_X^{\geq}$ par …" seems meant. Translated as written.
- 8.12.8, proof: "des isomorphismes (8.12.5.4) et (8.12.6.1)". (8.12.5.4) is only an $r$-morphism (its restriction (8.12.6.1) is the isomorphism); the $u$-isomorphism (8.12.5.3) seems intended. Translated as written.

## ega2-errata__ega2-errata

- (0, 2.1.6) erratum display — `Z_i\cap C\left(\bigcup_{j\ne i}Z_j\right)`: the plain `C` is presumably the complement sign (the text of 0, 2.1.6 writes `\complement\Bigl(\bigcup_{j\neq i}Z_j\Bigr)`). Copied as is.

## ega3-1-file__0.8-fr

- 8.2.6 — "En vertu de (8.1.3), on a $\alpha_X=h_{a_X}$": (8.1.3) only constructs $\alpha$, $\beta$; the bijectivity used is (8.1.4)/(8.1.6), and the parallel step in 8.2.4 cites (8.1.6). Possibly (8.1.6) intended. Kept as written.

## ega3-1-file__0.10-fr

- 10.3.1.1 (0.10.3.1.1-fr) — "dont l'idéal maximal $\mathfrak L=\mathfrak J B$" has no verb (presumably "dont l'idéal maximal est …"); rendered "with maximal ideal $\mathfrak L=\mathfrak J B$", nothing added.

## ega3-1-file__0.11-fr.part01

- 11.3.3, proof 4° (0.11.3.3-fr) — the display ends with "." although the sentence continues ("dès que $p-r+1+j_0<n$, …"); the parallel display in 3° has no period. Math copied unchanged.

## ega3-1-file__0.11-fr.part02

- 11.4.4 (0.11.4.4-fr) — no env heading: the number exists only as a \phantomsection label inside env 11.4.3 ("Sauf mention expresse du contraire…"), so "(11.4.4)", cited in the proof of 11.4.5, is never displayed. Structure kept as is.
- 11.5.2.1 (ii) (0.11.5.2.1-fr) — with $Q^0=Q'^1$ and $f'^i=0$ for $i\leq0$, $f^0=f'^1\circ d^0$ need not be injective (e.g. $A^\bullet$ concentrated in degree 0), against "$f^i$ est injectif pour tout $i$"; 2° for $i=0$ forces $\mathrm Z^0(Q^\bullet)=0$. Check "$i\geq1$", "$Q^0=Q'^1$", "$i\leq0$" and 2° "$i\geq0$" against the scan (possibly a slip of the original). Translated as written.
- 11.6.2 (0.11.6.2-fr) — "les critères de (11.3.4)": the regularity criteria for bicomplexes with differentials of degree −1 are (11.3.6); (11.3.4) is the edge homomorphism. Reference kept.

## ega3-1-file__0.11-fr.part03

- proof of 11.7.2 — "D'autre part, pour tout $r$, $M_{\bullet,r,\bullet}$ est une résolution de Cartan-Eilenberg du complexe simple $K_{\bullet,r}$, le calcul fait dans (M, XV, 2) montre que": two main clauses joined only by a comma; a conjunction (probably "comme") seems missing. Translated as written.

## ega3-1-file__III.1-fr.part01

- 1.1.5, after (1.1.5.2) — "les deux membres sont des antidérivations de $\bigwedge F$, et il suffit de vérifier qu'ils coïncident dans $F$": both sides are maps $\bigwedge E\to\bigwedge F$, determined by their values on $E$, so one expects "dans $E$" (and "de $\bigwedge E$ dans $\bigwedge F$"). Translated as written.

## ega3-1-file__III.1-fr.part02

- proof of 1.4.16 — "il résulte de (1.4.15)" is the only internal reference in this chunk written as plain text, without \hyperref[III.1.4.15-fr]{...}; kept as plain text.

## ega0-14__ega0-14

- introductory paragraph (before \S 14) — "La presque totalité des paragraphes précédents": the sections meant (\S\S 14–23) follow this paragraph and are only listed in the summary above it; "précédents" may stand for "suivants". Translated literally ("the preceding sections").

## ega4-16__IV.16.part01

- paragraph after (16.1.2) — "par la puissance $(\mathscr{I}_f/\mathscr{I}_f^{n+1})^m$ de l'Idéal d'augmentation de $\mathcal{O}_{Y^{(n)}}$": for $\mathcal{O}_{Y^{(n)}}$ to be the quotient of $\mathcal{O}_{Y^{(m)}}$ the power should be $(\mathscr{I}_f/\mathscr{I}_f^{m+1})^{n+1}$ of the augmentation ideal of $\mathcal{O}_{Y^{(m)}}$. Translated as is.
- 16.2.3 (ii) — cites (16.1.6) for the $\mathcal{O}_Y$-algebra structure defined by $g$; that structure is constructed in (16.1.7) (cited correctly in 16.3.2). Translated as is.
- proof of 16.2.3 (i) — "le morphisme $g$ étant une immersion": $g:X\to Y$ is not an immersion; (16.2.2, (ii)) needs the section $f$ to be one. Translated as is.
- 16.2.5 (ii) — "Par exemple (avec les notations de la démonstration de (16.2.2, (ii)), il": the opening parenthesis is never closed. Kept as is.

## ega4-16__IV.16.part02

- 16.4.2 — first arrow of the composite is `\rho'^*(\nu_n^\#)`, but (16.4.1.3) defines $\nu_n:\rho^*(\mathscr P^n_{X/S})\to\mathscr P^n_{X'/S'}$ with no $^\#$; $\rho'^*(\nu_n)$ seems meant. Copied as is.
- proof of 16.4.23 — the injective $p_{Z/X/S}:p^*(\mathscr P^n_{X/S})\to\mathscr P^n_{Z/S}$ is of type (16.4.18.2) and the surjection $\mathscr P^n_{Z/S}\to\mathscr P^n_{Z/Y}$ of type (16.4.18.1); the two references look swapped (perhaps already in the original).
- 16.4.24 (i) — "(16.4.21.2)" does not exist; 16.4.21 has only (16.4.21.1) (its left-hand map seems meant).

## ega4-16__IV.16.part03

- proof of 16.5.3 — "$u:\mathcal{O}_X\to\mathscr{F}$": the $u_V$ are defined on $\Omega^1_{B/A}$, so $u:\Omega^1_{X/S}\to\mathscr{F}$ seems meant.
- 16.5.12 — "$\Gamma(T_{X/S}/S)$" and "germes de $S$-sections": (II, 1.7.9) concerns sections of $T_{X/S}$ over $X$, so $X$ seems meant (possibly already in the original).
- before 16.5.17 — "le problème considéré en (16.5.13)": the problem is posed in (16.5.14).
- 16.5.18 — "Avec les notations de (16.5.16)": the notation is that of (16.5.17).
- 16.6.2 — "endomorphisme de $\psi^*(\mathcal{O}_X)$-Modules gradués": $\psi^*(\mathcal{O}_S)$ seems meant (cf. 16.5.9); $\psi$ is not introduced in 16.6.1.
- proof of 16.6.2 — "(en vertu de (i)) combinaison linéaire …": writing sections as combinations of $g\,df_1\wedge\cdots\wedge df_p$ uses (ii), not (i).
- proof of 16.6.2 — "quels que soient $f$, $g$ dans $A$" after (16.6.2.3): $f$, $g$ range over $B$.
- 16.6.4 — "déduit de l'isomorphisme (16.5.9.1)": (16.5.9.1) is the bracket; the isomorphism is (16.5.10.1).
- 16.6.5 — "les dérivations $D_i$ définies dans (16.5.7)": they are defined in (16.5.8).

## ega4-16__IV.16.part04

- 16.7.1 display, (16.7.4.1), 16.7.7 second display — `X,qquad`, `t,qquad`, `(\mathscr{F})qquad(n\leq m)`: `qquad` lacks the backslash of `\qquad`; copied as is.
- 16.8.1 (paragraph after the definition) — "Pour $n\geq0$, un opérateur différentiel n'est pas en général un homomorphisme de $\mathcal{O}_X$-Modules": the preceding sentence says order-0 operators are exactly the $\mathcal{O}_X$-homomorphisms, so presumably $n>0$.
- (16.8.3.1) — left side written $\mathscr{H}\!om_{\mathcal{O}_U}$ (sheaf Hom), but the map is an isomorphism of additive groups onto the group $\operatorname{Diff}_{U/S}^n(\ldots)$; presumably $\operatorname{Hom}_{\mathcal{O}_U}$.
- 16.8.7 — "les flèches horizontales sont les isomorphismes (16.8.4.2)": there is no (16.8.4.2); the isomorphism is (16.8.4.1).
- proof of 16.8.8 — the displayed expansion $\sum_{H}(\prod_{i\in H}a_i)\otimes((\prod_{i\notin H}a_i)t)$ carries no sign; expanding $\prod(a_i\otimes1-1\otimes a_i)$ gives the factor $(-1)^{n+1-\operatorname{Card}(H)}$, which matches (16.8.8.2) only up to a global sign (possibly so in the original).
- (16.7.8.2) — the citation "(Bourbaki, Alg., 3e éd., §5, no 3)" lacks the "chap. II" of the citation just before (possibly so in the original).

## ega4-16__IV.16.part05

- 16.9.3 — the statement indexes the sequence as $(f_i)_{1\leq i\leq m}$, but the last assertion ("$(f'_i)_{1\leq i\leq n}$ de $n$ sections") and the proof ("une base de $n$ éléments") use $n$; $m$ is presumably $n$.
- 16.11.3 (i) — "ne permutant aux produits par les sections de $\mathcal{O}_U$ que si $n=0$": no $n$ occurs in this context; presumably $\mathbf{p}=0$.

## ega4-1__IV.1-fr.part01

- 1.4.3 proof of (ii) — "d'aute part": misspelling of "d'autre part"; translated "on the other hand".
- 1.4.5 — "le sous-préschéma fermé de $Y$ associé à $j$": this sub-prescheme is closed in $U$ (its ideal $\mathcal J$ is an ideal of $\mathcal O_U$), so "de $U$" may be meant. Translated as written.
- 1.4.7 proof — "$w=v\circ u:B''\to B$": with $v:B''\to B'$ and $u:B'\to B$ the composite is $u\circ v$. Math kept as written.
- 1.4.7 proof — "Inversement, si $B'$ est un $A$-module de présentation finie": the converse needs this hypothesis on $B$ ($B'$ is free of finite rank anyway), so "$B$" is presumably meant. Kept $B'$.

## ega4-1__IV.1-fr.part02

- 1.8.3 proof — "ramené à prouver le lemme lorsque $X_i$ est \emph{affine} d'anneau $A$": the rest of the proof works with $X$ affine of ring $A$ ($X_{f_i}$, $Z'$ closed in $X$), so "$X$" may be meant. Translated as written.
- 1.8.5 proof — "(compte tenu de (1.5.4, (iii)) qu'on est ramené": the first opening parenthesis is never closed. Kept as written.
- 1.8.5.1 — the statement has neither "$g\neq0$" nor "$B$ containing $A$"; with $g=0$ it is vacuous, and its uses in 1.8.5 and 1.8.6 need $g\neq0$ and $A\to B$ injective. A word may be missing. Translated as written.

## ega4-1__IV.1-fr.part03

- 1.9.3 proof, a') ⇒ a'') — "$X'_\alpha$ est réunion d'ouverts affines $X''_{\alpha\lambda}$ ($\lambda\in L$)", whose sum is then called affine: this needs $L$ finite ($X'_\alpha$ is quasi-compact), so "finie" may be missing. Translated as written.
- after 1.9.3.1 — "théorème de Chevalley (1.8.5)": Chevalley's theorem is (1.8.4); (1.8.5) assumes a Noetherian base, and the proof of 1.9.5 (viii) cites (1.8.4). Reference kept.
- 1.9.5 (iv) — "(rep. ind-constructible)": typo for "resp."; rendered "resp.".
- 1.9.5 proof of (vii) — "puisque $g\circ f$ est quasi-compact": with $g:X''\to X'$, $f:X'\to X$ the composite is $f\circ g$. Math kept.
- 1.9.12 proof — "on est ramené au cas où $X$ est affine, en vertu de (1.9.5, (iv))": (1.9.5, (iv)) localizes on $Y$, where $E$ lies, so "$Y$" may be meant. Translated as written.
- 1.9.14 proof — "traduisent respectivement (1.9.5), (vi), (vii) et (viii)": presumably "(1.9.5, (vi), (vii) et (viii))". Parenthesization kept.
- 1.9.15 proof of (ii) — "voisinage ouvert affine $U$ de $X$ ne contenant pas $y$": a neighbourhood of the point $x$ is meant. Kept $X$.

## ega4-17__ega4-17.part01

- \section short title — "(ou nets) morphismes étales" has no comma before "morphismes étales" (the long title has a line break there); the English keeps the same punctuation.
- 17.1.2 (ii) display — "qquad" lacks its backslash, so it prints the letters "qquad"; copied unchanged.
- 17.3.5 proof — "(17.3.3, (iii))": the step needs the composition statement (17.3.3, (ii)); (iii) is base change (cf. 17.1.5, which cites (ii) and (v)). Translated as written.
- 17.4.1 proof of b) ⇔ b'') — "$s'=(1_{Y'},h)_X$": $X'=Y'\times_Y X$ is a product over $Y$, so the subscript would be $Y$; copied unchanged.
- 17.4.6 — "un morphisme non ramifiée": gender agreement slip; no effect on the English.

## ega4-17__ega4-17.part02

- 17.5.1 proof, b) ⇒ a) — "$B_{\mathfrak q}/\mathfrak rB_{\mathfrak q}$ est une $A_{\mathfrak r}$-algèbre formellement lisse": this ring is killed by $\mathfrak r$ and is formally smooth over $k(y)$, not in general over $A_{\mathfrak r}$; likewise the quotient written "$C_{\mathfrak p}=(B_{\mathfrak q}/\mathfrak rB_{\mathfrak q})/(\mathfrak J_{\mathfrak q}/\mathfrak r\mathfrak J_{\mathfrak q})$" is $C_{\mathfrak p}/\mathfrak rC_{\mathfrak p}$. Possibly in the original; translated as written.
- 17.6.1 proof — "l'équivalence de a) et d) dans (17.5.1)": (17.5.1) has no condition d); the equivalence used is a) ⇔ c). Translated as written.
- 17.7.1 (ii) proof — "un morphisme plat au point $X'$": the point is $x'$; math copied unchanged.
- 17.7.2 (ii) — "l'ensemble des points de $X$ où $f$ (resp. $f'$)" lacks "(resp. $X'$)", present in (i). Translated as written.
- 17.7.3 proof — "$f'$ est localement de présentation finie par (2.7.1, (iv))": the descent conclusion concerns $f$ ($f'$ is already locally of finite presentation); math copied unchanged.
- 17.7.7 proof — "$f^{-1}(s)$ est lisse (resp. étale) sur $k(s)$ au point $x$": the relevant point of $f^{-1}(s)$ is $y$. Translated as written.

## ega4-17__ega4-17.part03

- 17.9.3 proof — "(1, 5.4.6)": presumably "(I, 5.4.6)" (a section of a separated morphism is a closed immersion); copied as is.
- 17.11.1 proof — "est un $C_{\mathfrak m}$-module libre: en effet (16.10.6) il existe des éléments $t_i$": "en effet" reads oddly, since the existence of the $t_i$ does not justify the freeness; possibly "en outre" in the original; translated "indeed".
- 17.12.1 proof (c implies a) — "en posant $s=h(x)$": here $h:Y\to S$ and $x\in X$; presumably $s=f(x)$ ($=h(y)$); copied as is.
- 17.12.2 proof — "à l'aide de (17.9.6)": the fibrewise criterion for open immersions used here is (17.9.5); (17.9.6) concerns monomorphic endomorphisms; copied as is.
- 17.12.3 — "lisse en un point $x\in X$ ... dans un voisinage de $s=f(x)$": the criterion only makes sense for $x$ in $u(S)$ (presumably $x=u(s)$); words may be missing; translated as is.
- 17.12.5 proof — "$v=(g',g')_Y$": commutativity of the square requires $p_2\circ v=h\circ f'=g'\circ s'\circ f'$, i.e. presumably $v=(g',h\circ f')_Y$; copied as is.
- 17.12.7 — "$f$ est lisse aux points de $s(S)$": $f$ is not introduced (presumably the structural morphism $G\to S$); copied as is.
- 17.12.8 — "différentiellement lisse sur $S$ (17.12.6)": the criterion applied is the group-prescheme criterion (17.12.7); copied as is.

## ega4-17__ega4-17.part04

- 17.13.4 (iv) — "(II, 9.18)": EGA II has no §9; the intended reference is unclear; copied as is.
- 17.13.6 c) — "Le morphisme $T=Y\times_SZ\to X\times_SX$": $T$ was defined as $Y\times_XZ$; the morphism meant is presumably $u:Y\times_SZ\to X\times_SX$ of (17.13.5.1); copied as is.
- 17.13.8 proof — "$\gamma$ et $\delta$ ceux figurant au second membre de (17.13.5.2)": the two homomorphisms $p_{T/Y/S}$, $q_{T/Z/S}$ are on the right-hand side of (17.13.5.3); copied as is.
- 17.13.9 — the tag (17.13.9.1) is used twice (the diagram, label IV.17.13.9.1, and the exact sequence, label IV.17.13.9.1-seq); the final "situation de (17.13.9.1)" presumably means the diagram; copied as is.
- 17.13.10 b') — "$\mathrm{T}_{Y_i/X}(y_i)$": presumably $\mathrm{T}_{Y_i/S}(y_i)$ (tangent spaces relative to $S$, as in 17.13.6 b')); copied as is.
- 17.13.10, last paragraph — "La remarque (17.13.4, (iii))": the openness statement for proper $T$ is (17.13.4, (ii)); copied as is.
- 17.14.2 proof (i) and 17.14.3 — "$\mathfrak m'^{,j}$", "$\mathfrak m'^{,j+1}$": a comma in the exponent, presumably a garbled thin space (\mathfrak m'^{\,j}); copied as is (mathematics).

## ega4-17__ega4-17.part05

- proof of (17.15.5), b) ⇒ a) — "le fait que $f$ soit lisse en $x$": no $f$ is defined in (17.15.5); presumably the structural morphism $X\to\operatorname{Spec}(k)$. Kept.
- proof of (17.15.9) — "la suite (17.15.7.2)": there is no (17.15.7.2); the exact sequence meant is (17.15.8.2), cited earlier in the same proof. Kept.
- proof of (17.16.1) — "locale sur $X$ et $Y$": the statement has base $S$, not $Y$. Kept.
- proofs of (17.16.2), (17.16.4), (17.16.5) — "(I, 2.7)", "(I, 6.2)", "(I, 8.4)", "(I, 9.9)": two-number references that fit IV §1, i.e. (1.2.7), (1.6.2), (1.8.4), (1.9.9); the constructibility of $f(W_\alpha)$ is Chevalley's theorem, cited as "(1.8.4)" in ega4-17.part02. Kept.
- end of proof of (17.16.6) — $K'_j$ "isomorphe canoniquement au corps résiduel de $A_j$" and $K'_j\to A_j\to k(A_j)$ "dont le composé est un isomorphisme": when $k(A_j)$ is not separable over $k$ such a $K'_j$ need not exist, and $\operatorname{Spec}(K'_j)\to\operatorname{Spec}(k)$ would not be étale; the argument needs the largest separable subextension of $k(A_j)/k$ (with $u_i$ radicial). Words may be missing, or the slip may be original. Translated as written.

## ega4-20__sec0.part01

- (20.1.8) — "une section $s$ de $\sh{L}$ au-dessus de $X$ sera appelée une section méromorphe régulière de $\sh{L}$": the context (regular meromorphic sections over $U$) suggests a section of $\sh{M}_X(\sh{L})$. Translated as written.
- (20.1.13) — `\sref{IV.20.2.13}[(i)]` for $M(Y)=R(Y)$: that identification is stated in (20.2.13, (ii)), not (i). Kept.
- (20.1.13) — "$Y^\mathrm{an}$ ayant même espace topologique sous-jacent": the points of $Y^{\mathrm{an}}$ are the closed points of $Y$, with the classical topology; possibly missing words or an imprecision of the original. Translated as written.

## ega4-20__sec0.part02

- (20.2.8) — `\Hom(V,\bb{Z}[T])`: the correspondence of (I, 3.3.15) is with morphisms $V\to\Spec(\bb{Z}[T])$; presumably `\Hom(V,\Spec(\bb{Z}[T]))` (or an abuse of notation in the original). Copied as is.
- (20.2.12) — "l'ensemble des éléments réguliers de $X$": presumably "de $A$". Translated as written.

## ega4-20__sec0.part03

- 20.3.1 — "On a $\operatorname{dom}(f\circ\omega)=\operatorname{dom}(\omega)$": in general only $\operatorname{dom}(f\circ\omega)\supset\operatorname{dom}(\omega)$ holds (if $Z$ is a point, $f\circ\omega$ is everywhere defined while $\omega$ need not be, e.g. $(x:y)$ from the affine plane to $\mathbf{P}^1$). 20.3.3 cites it as an equality but only needs the inclusion. Kept.
- 20.3.2 — the open subset is named $V'=f^{-1}(\operatorname{dom}_S(\omega))$, but the next clause writes $u\circ(f|U')$; $V'$ is presumably meant. Kept.
- 20.3.8.4 — the statement names the open set $V_\alpha$ (inverse images $V_\lambda$, $V$), then speaks of $U_\alpha$, $U_\lambda$, $U$, as does the proof; the same set is presumably meant. Kept.
- 20.3.8.6 — "appartiennent au même pseudo-homomorphisme": a pseudo-($S_\lambda$-)morphism is meant; translated literally as "pseudo-homomorphism".

## ega4-20__sec0.part04

- 20.4.6, condition (P) — the square has no left vertical arrow $\Spec(k(a))\to\Spec(k(x))$; copied as is.
- 20.4.6, proof — "$h(x')$ est une spécialisation de $h'_x(x)=y$" (and again "$h(x')$ est une spécialisation de $y$"): since $y=h'_1(a)$ with $a$ the closed point and $h(x')=h'_1(b)$, it is $y$ that is a specialization of $h(x')$ (i.e. $h(x')$ is a generization of $y$), which is what the next steps ($h(U)\subset Y'$, $y\in p^{-1}(x)$) use. Translated literally.
- 20.4.11, proof — "$B$ étant une $A$-algèbre de type fini": the hypotheses only make $Y$ affine over $S$, and the next sentence uses an arbitrary family $(T_\lambda)_{\lambda\in L}$; "de type fini" looks spurious. Kept.

## ega4-20__sec0.part05

- 20.6.2 — "$M(X/S,F)$": presumably $M(X/S,\sh{F})$ (script letter lost). Kept.
- 20.6.5 (i) — "$\varphi=\pi/T$ est une fonction méromorphe sur $S$ relative à $S$": $\varphi$ lives on $X=S[T]$, so "sur $X$" is presumably meant. Translated literally.
