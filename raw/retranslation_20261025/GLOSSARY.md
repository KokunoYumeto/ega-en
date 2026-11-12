# EGA: French → English glossary

For translating the chunks in `fr/` (see `SPEC.md`). **English** = our AI-translated EGA English in `ours/` (prose, plus the index and contents pages of I, II, III part 1 and IV); where `ours/` is inconsistent, the majority form is given and the variant noted. Counts *(a:b)* are occurrences in `ours/` of the chosen form : the variant. **(std)** = standard English term (Stacks Project, Vakil, nLab, Wikipedia) not found in `ours/`. **(lit.)** = literal rendering found in neither; record a better choice in the chunk notes if one turns up.

## 1. Conventions

- **Sheaves of modules: lowercase.** French $\mathcal O_X$-Module, $\mathcal A$-Algèbre, Idéal → **$\mathcal O_X$-module, $\mathcal A$-algebra, ideal (of $\mathcal O_X$), sub-$\mathcal O_X$-module** (sheaf contexts in `ours/`: module 814 : Module 604; algebra 120:46; "ideal of $\mathcal O_X$" 39:19). Capital "Module" survives as a variant in IV §§2, 6–9, 21, III §7 and in places in 0 §§12, 15. Bare "Module(s)" → "module(s)"; "faisceau d'idéaux" → "sheaf of ideals" (III §2 prose also writes "quasi-coherent ideal of $\mathcal O_X$"). Modules over a ring or stalk ($A$-module, $\mathcal O_{X,x}$-module) are lowercase in both languages.
- **EGA's own terms stay.** préschéma → prescheme; schéma → scheme (= separated prescheme); $S$-préschéma → $S$-prescheme; préschéma au-dessus de $S$ → prescheme over $S$; schéma affine → affine scheme. Never turn "prescheme" into "scheme".
- **sub-.** sous-préschéma → **sub-prescheme** (318:116; "subprescheme" is the variant in III and the I index); sous-faisceau → sub-sheaf (15:3); sous-$\mathcal O_X$-Module → sub-$\mathcal O_X$-module. Every other sub- word is closed: subscheme (29:3), submodule, subring, subalgebra, subset, subobject, subcategory, subgroup, subfield.
- **Spelling: British with -ize.** fibre (404:1), neighbourhood (656:14), behaviour (7:0); generization, localization, normalization, specialization (-ization overall 233:98). Ours writes "factorisation" 36:12 (mostly IV); use "factorization", as III does (Stein factorization).
- **Hyphens.** Always quasi-coherent, quasi-compact, quasi-separated, quasi-finite, quasi-affine, quasi-projective, quasi-regular; semi-local (101:28); non-empty (87:58), but nonzero (94:20) and nonnegative. Closed: preadic, preadmissible, retrocompact, unibranch. "of finite type" (1154:124 "finite-type"); "of finite presentation" (535:32 "finitely presented").
- **Capitals.** Noetherian (1619:4), Artinian (103:0); Algebraic Geometry for the discipline (French "Géométrie algébrique"; 22:11); Treatise (Traité). Chapter, Proposition, Theorem, Corollary, Lemma, Remark only before a number ("Chapter IV"; otherwise "this chapter", "the proposition"). Eponyms are possessive: Nakayama's lemma (29:5), Serre's criterion, Chow's lemma, Zariski's connectedness theorem, Zariski's ``main theorem'', Stein factorization. Two people: en dash (Euler--Poincaré 14:3, Cartan--Eilenberg 36:0); one person: hyphen (Mittag-Leffler). $n$-ème → $n$-th (21:2 "$n$th").
- **Typography.** « … » and \og … \fg{} → ``…'' (drop the inner ~). "~;" and "~:" → ";" and ":" with no space before (`ours/` has none). Latin keeps its \emph{}: \emph{a fortiori} (110:9), \emph{loc. cit.} (57:24), \emph{ipso facto}, \emph{a priori}. "resp." stays "resp."; "cf." stays lowercase (85:0 "Cf."). C.Q.F.D. → Q.E.D.; (A suivre.) → (To be continued.); Reçu le 28 juin 1961 → Received June 28, 1961. Remarque(s) → Remark(s); Démonstration → Proof; Énoncé → Statement; Exemples → Examples; (suite) → (continued); Préliminaires → Preliminaries. Titles: Compléments sur → Supplement on (9:5 "Complements on"); Rappels sur → Review of (4:2 "Reminders on"); Généralités sur → Generalities on. A defined term keeps its \emph{} in English ("… est dit \emph{plat}" → "… is said to be \emph{flat}").
- **Mathematics and references.** Copy all mathematics and reference text exactly as in the French (SPEC rule 2): $\mathcal O_X$, \operatorname{Spec}, (0\textsubscript{I}, 5.4.6), (I, 9.3.1), (G, II, 7.2.1), \S, n\textsuperscript{o}, 1\textsuperscript{o}. Do not introduce the macros of `ours/` (\sh, \HH, \sref) and do not add "Proposition" before a bare reference such as (2.1.3). Wording around references: d'après / en vertu de (…) → "by (…)" / "by virtue of (…)" (525:58 "in view of"); compte tenu de (…) → "taking into account (…)"; il résulte de (…) que → "it follows from (…) that"; cf. (…) → "cf. (…)". Bourbaki citations keep the French abbreviations and title; only connecting words are translated: (Bourbaki, \emph{Alg. comm.}, chap. II, \S~3, n\textsuperscript{o}~2, cor. 1 de la prop. 4) → (Bourbaki, \emph{Alg. comm.}, chap. II, \S~3, n\textsuperscript{o}~2, cor. 1 of prop. 4) (chap. 393:20 "ch."; n\textsuperscript{o} 202:115 "no.").
- **Voice and tense.** Present tense as in the French. "on" → "we" by default (we may/can 713:592 "one may/can"; we have 737:506 "one has"), "one" where "we" is awkward. on dit que → we say that (117:17 "one says that"); nous dirons que → we will say that (19:3 "we shall say"); on appelle → we call; nous désignerons par → we denote by; Soient … → Let … be …; posons → set; supposons → suppose (878:34 "assume"); il suffit de → it suffices to (415:124 "it is enough"); En effet → Indeed (427:2 "In fact"); pour tout → for every (1637:232 "for all"); évidemment → evidently (108:12 "obviously"); autrement dit → in other words; c'est-à-dire → that is (85:48 "i.e."); par exemple → for example; en outre → moreover; par suite → consequently; il résulte aussitôt de → it follows immediately from; on est ramené au cas où → we are reduced to the case where; on peut se borner au cas où → we may restrict to the case where; la question étant locale sur $X$ → the question being local on $X$; assez grand → sufficiently large (65:15); deux à deux → pairwise; un nombre fini de → finitely many (77:35); cas particulier → particular case (57:53 "special case"); ce qui achève la démonstration → which completes the proof; nous laissons au lecteur le soin de → we leave it to the reader to; par abus de langage → by abuse of language.
- **Words that split or mislead** (details in the table): fibre of a sheaf → stalk, of a morphism → fibre; intègre and entier → both "integral"; positif means ≥ 0 (nonnegative integer; graded in positive degrees); séparé, also topologically → separated, never "Hausdorff"; rare → rare (= nowhere dense); racine d'un idéal → radical; partie → subset; couple → pair; application → map; quelconque → arbitrary; majoré par → dominated by; ouvert, fermé (nouns) → open subset, closed subset.

## 2. Glossary

| French | English (ours) | note |
|---|---|---|
| à ... près (à un isomorphisme canonique près) | up to (canonical) isomorphism | |
| a fortiori | \emph{a fortiori} | italic (110:9 plain) |
| à valeurs dans (point ~) | (point) with values in | |
| aboutissement (d'une suite spectrale) | abutment | |
| abus de langage (par) | by (a slight) abuse of language | |
| adhérence (d'un sous-préschéma) | closure (of a sub-prescheme) | |
| adique (anneau, morphisme, préschéma formel, système inductif) | adic (ring, morphism, formal prescheme, inductive system) | EGA's adic ring is separated and complete (I index note) |
| admissible; préadmissible (anneau) | admissible; preadmissible (ring) | no hyphen |
| affine (morphisme; préschéma ~ au-dessus de $S$) | affine (morphism; prescheme affine over $S$) | |
| Algèbre ($\mathcal O_X$-Algèbre, $\mathcal A$-Algèbre) | $\mathcal O_X$-algebra, $\mathcal A$-algebra | lowercase (120:46); variant "-Algebra" (IV §§8, 14, 18–19) |
| algèbre de type fini; algèbre finie; algèbre entière (finie) | algebra of finite type; finite algebra; (finite) integral algebra | |
| algèbre extérieure (complexe de l'~) | exterior algebra complex | III index/TOC; variant "complex of the exterior algebra" |
| algèbre symétrique | symmetric algebra | |
| algébrisable | algebraizable | (25:0 "algebraisable") |
| ample; très ample; relativement ample | ample; very ample; relatively ample | "ample relativement à $f$" = "ample relative to $f$", "$f$-ample" |
| amplitude (critère d'~; critère d'~ de Grauert) | ampleness (criterion); Grauert's ampleness criterion | never "amplitude" (11:1) |
| analytiquement intègre | analytically integral | |
| anneau de fractions (complet) | (complete) ring of fractions | |
| anneau de valuation (discrète) | (discrete) valuation ring | |
| anneau intègre | integral ring | 111:37; variant "integral domain" |
| anneau local (de $X$ en $x$; de $X$ le long de $Y$) | local ring (of $X$ at $x$; of $X$ along $Y$) | |
| anneau topologique (linéairement topologisé) | (linearly topologized) topological ring | |
| anneaux locaux apparentés | related local rings | |
| annuler (s'~ en $x$) | vanish at $x$ | sense $f(x)=0$ (0, 5.5.1), not $f_x=0$ |
| application | map | (380:4 "mapping") |
| application linéaire tangente; espace tangent; faisceau tangent; fibré tangent | tangent linear map; tangent space; tangent sheaf; tangent bundle | "relatif" = "relative" |
| application rationnelle ($S$-~); domaine de définition | rational map (rational $S$-map); domain of definition | |
| artinien | Artinian | capital A |
| au-dessus de | over (object over a base); above (points, fibres) | "$S$-préschéma, préschéma au-dessus de $S$" = "$S$-prescheme, prescheme over $S$"; "point above $s$" |
| augmentation (d'une résolution); idéal d'augmentation | augmentation; augmentation ideal | (8:6 "ideal of augmentation") |
| autrement dit | in other words | |
| base d'ouverts | basis of open subsets | I index; "base of the topology" also occurs |
| bi-alternée (cochaîne) | bi-alternating (cochain) | |
| bicomplexe | bicomplex | never "double complex" (62:0) |
| biéquidimensionnel; équidimensionnel; équicodimensionnel | biequidimensional; equidimensional; equicodimensional | |
| borne inférieure (supérieure) | infimum (supremum) | |
| canonique (application, homomorphisme, morphisme, injection, projection, rétraction, symétrie) | canonical (map, homomorphism, morphism, injection, projection, retraction, symmetry) | |
| caractéristique (de ~ $p$; ~ nulle) | (of) characteristic $p$; characteristic zero | |
| caractéristique d'Euler-Poincaré | Euler--Poincaré characteristic | en dash between two names (14:3) |
| caténaire | catenary | |
| chaîne (saturée, maximale); condition des chaînes | (saturated, maximal) chain; chain condition | |
| changement d'anneau(x); ~ de partie multiplicative | change of ring(s); change of multiplicative subset (std) | 0 §§1.4, 1.5, 6.2 titles |
| changement de base (morphisme de ~) | base change (base-change morphism) | (98:23 "change of base") |
| changement de préschéma de base; extension du préschéma de base | change of the base prescheme; extension of the base prescheme | II TOC; I index |
| Chevalley (schémas de ~) | Chevalley schemes (lit.) | I §8 |
| codimension (de $Y$ dans $X$, au point $x$) | codimension (of $Y$ in $X$, at the point $x$) | |
| cohomologie de Čech (d'un recouvrement ouvert) | Čech cohomology (of an open covering) | III TOC has "open cover" |
| complété (n.); séparé complété | completion; separated completion | |
| complété formel (d'un préschéma le long d'une partie fermée) | (formal) completion (of a prescheme along a closed subset) | I index |
| complexe (de chaînes, de cochaînes; filtré; simplicial; de type fini) | complex (of chains, of cochains; filtered; simplicial; of finite type) | |
| composante irréductible / connexe | irreducible / connected component | |
| composé | composite | |
| composé direct (d'anneaux, de corps) | direct product (of rings, of fields) | IV §18 |
| compte tenu de | taking into account | |
| condition (ML); condition de Mittag-Leffler | condition (ML); Mittag-Leffler condition | hyphen: one person |
| condition (TF), (TN); (TN)-isomorphisme | condition (TF), (TN); (TN)-isomorphism | |
| condition de recollement | gluing condition | |
| condition de séparation | separation condition (lit.) | I §5 title; the property itself is "separatedness" |
| conditions de finitude (relatives) | (relative) finiteness conditions | II TOC; IV §1 title |
| cône (affine, projectif; épointé) | (affine, projective; punctured) cone | |
| cône projetant (affine, projectif) | (affine, projective) projecting cone | |
| constructible (ensemble, partie, fonction); localement constructible | constructible (set, subset, function); locally constructible | |
| corps de base | base field | |
| corps de fonctions (de dimension 1; algébriques d'une variable) | function field (of dimension one); algebraic function field in one variable (std) | first form: II TOC |
| corps des fractions | field of fractions | (199:29 "fraction field") |
| corps des valeurs (d'un point géométrique) | field of values | I, 3.4.5 |
| corps résiduel | residue field | |
| correspondance biunivoque | bijective correspondence | (14:1 "one-to-one correspondence") |
| couple | pair | |
| courbe algébrique (complète) | (complete) algebraic curve | |
| critère de Serre | Serre's criterion | possessive eponyms (Nakayama's lemma 29:5) |
| critère jacobien | Jacobian criterion | |
| critère valuatif (de séparation, de propreté) | valuative criterion (for separatedness, for properness) | |
| critères locaux de platitude | local flatness criteria | |
| cup-produit | cup product | no hyphen |
| cycle; cocycle; bord; cobord (objet des ~s) | cycle; cocycle; boundary; coboundary (object of ~s) | |
| de carré nul | of square zero | (16:7 "square-zero") |
| dégénérée (suite spectrale) | degenerate | |
| dense; partout dense; rare | dense; everywhere dense; rare | "rare" = nowhere dense; ours keeps "rare" (30:11) |
| dérivation ($S$-~, $(X/S)$-~, $f$-~) | derivation ($S$-~, $(X/S)$-~, $f$-~) | |
| détermination locale (d'un morphisme) | local determination (of a morphism) (lit.) | I §6.5 title |
| dévissage (lemme de ~) | dévissage lemma | keep the French word |
| di-homomorphisme | di-homomorphism | hyphenated (32:0), also for "dihomomorphisme" |
| diagonale; morphisme diagonal | diagonal; diagonal morphism | |
| différentielle (extérieure); $\mathcal O_X$-Module des 1-différentielles; $p$-différentielles | (exterior) differential; $\mathcal O_X$-module of first differentials; $p$-differentials | "first differentials" from IV index (1×); "1-differentials" would parallel "$p$-differentials" |
| différentiellement lisse (jusqu'à l'ordre $r$) | differentially smooth (up to order $r$) | |
| dimension combinatoire (de $X$ en $x$) | combinatorial dimension (of $X$ at $x$) | |
| dominant (morphisme); dominer | dominant (morphism); dominate | |
| éclaté (préschéma, schéma ~) | blow-up prescheme (scheme) | II index/TOC (5:4); variant "blown-up prescheme" (IV) |
| éclatement; faire éclater | blowing-up; blow up | "obtained by blowing up $Y'$"; II TOC "Blow-up of projecting cones" |
| élément homogène (de degré $d$); graduation; gradué (anneau, module, algèbre) | homogeneous element (of degree $d$); grading; graded (ring, module, algebra) | |
| en vertu de | by virtue of | (525:58 "in view of") |
| entier (élément, algèbre, morphisme; ~ sur) | integral (over) | ≠ intègre, though both are "integral" |
| espace annelé (en anneaux locaux); morphisme d'espaces annelés | ringed space (in local rings); morphism of ringed spaces | "in local rings" in prose (8:3); variant "locally ringed space" (I index) |
| espace de Kolmogoroff | Kolmogorov space | |
| espace homogène principal | principal homogeneous space | |
| espace irréductible; espace noethérien | irreducible space; Noetherian space | |
| espace sous-jacent | underlying space | |
| espace topologiquement annelé | topologically ringed space | |
| essentiellement constant (système projectif) | essentially constant | |
| essentiellement intègre / réduit | essentially integral / reduced | |
| évidemment | evidently | (108:12 "obviously") |
| exact (à gauche, à droite; sous-ensemble ~ d'une catégorie abélienne) | (left, right) exact; exact (subset of an abelian category) | |
| extension radicielle | radicial extension | not "purely inseparable" (65:0) |
| facteur direct | direct factor | tie with "direct summand" (14:14) |
| faisceau (à valeurs dans une catégorie) | sheaf (with values in a category) | |
| faisceau (formellement) principal homogène; torseur; pseudo-torseur | (formally) principal homogeneous sheaf; torsor; pseudo-torsor | |
| faisceau (localement) simple | (locally) simple sheaf | |
| faisceau algébrique | algebraic sheaf | "$\mathcal A$-Modules ou faisceaux algébriques" (0, 4.1.3) |
| faisceau associé (à un préfaisceau, à un module) | sheaf associated to (a presheaf, a module) | "associated to" (102:65 "with") |
| faisceau conormal | conormal sheaf | |
| faisceau constant; préfaisceau constant | constant sheaf; constant presheaf | |
| faisceau d'anneaux, d'ensembles, de groupes (abéliens) | sheaf of rings, of sets, of (abelian) groups | |
| faisceau d'idéaux (de définition) | sheaf of ideals (of definition) | prose often "ideal of $\mathcal O_X$" (III §2) |
| faisceau de torsion; sans torsion | torsion sheaf; torsion-free | |
| faisceau des germes de $S$-sections | sheaf of germs of $S$-sections | |
| faisceau des parties principales (d'ordre $n$) | sheaf of principal parts (of order $n$) | |
| faisceau fondamental (d'un fibré projectif) | tautological sheaf | II index (1×); literal "fundamental sheaf" |
| faisceau inversible | invertible sheaf | |
| faisceau pseudo-discret (d'espaces, d'anneaux topologiques) | pseudo-discrete sheaf (of spaces, of topological rings) | |
| faisceau structural | structural sheaf | (3:2 "structure sheaf", I index); cf. structural morphism |
| fermeture intégrale | integral closure | |
| fermeture projective | projective closure | |
| fibre (d'un faisceau, $\mathcal F_x$) | stalk | I index; 0 §15 |
| fibre (d'un morphisme); fibre géométrique (rationnelle) | fibre; (rational) geometric fibre | British spelling (404:1) |
| fibré projectif | projective bundle | |
| fibré vectoriel | vector bundle | |
| fidèlement plat | faithfully flat | |
| filtrant (à droite; famille ~e décroissante) | filtered (to the right; decreasing filtered family) | |
| filtration (co-discrète, co-séparée, exhaustive, séparée) | filtration (co-discrete, co-separated, exhaustive, separated) | |
| fini (morphisme; préschéma ~ sur $S$) | finite (morphism; prescheme finite over $S$) | |
| foncteur cohomologique (universel); $\delta$-foncteur | (universal) cohomological functor; $\delta$-functor | |
| foncteur covariant / contravariant; bifoncteur | covariant / contravariant functor; bifunctor | |
| foncteur dérivé | derived functor | |
| foncteur pleinement fidèle; sous-catégorie pleine | fully faithful functor; full subcategory | |
| foncteur représentable | representable functor | |
| fonction méromorphe; pseudo-morphisme | meromorphic function; pseudo-morphism | IV §20 |
| fonction rationnelle; faisceau des fonctions rationnelles | rational function; sheaf of rational functions | |
| fonctions symétriques élémentaires | elementary symmetric functions | |
| fonctoriel (comportement ~) | functorial (behaviour) | British "behaviour" |
| générisation | generization | (95:16 "generisation") |
| genre arithmétique | arithmetic genus | |
| géométriquement connexe / irréductible / réduit | geometrically connected / irreducible / reduced | |
| germe (d'une section, d'un morphisme) | germ | |
| graphe (d'un morphisme); morphisme graphe | graph; graph morphism | |
| homogénéisé (n.); variable d'homogénéisation | homogenization; homogenization variable | |
| homomorphisme local | local homomorphism | |
| hypercohomologie; hyperhomologie | hypercohomology; hyperhomology | |
| Idéal (de $\mathcal O_X$); $\mathcal A$-Idéal | ideal (of $\mathcal O_X$); $\mathcal A$-ideal | lowercase (39:19; "coherent ideal" 34:22) |
| idéal de définition (système fondamental d'~s) | ideal of definition (fundamental system of ~s) | also for capital "Idéal de définition" |
| idéal premier (gradué, minimal) | (graded, minimal) prime ideal | |
| idéal régulier / quasi-régulier | regular / quasi-regular ideal | |
| idéalement séparé | ideally separated | Bourbaki term |
| il suffit de | it suffices to | (415:124 "it is enough") |
| image directe (supérieure) | (higher) direct image | |
| image fermée | closed image | |
| image réciproque | inverse image | |
| images universelles (objet des ~) | universal images (object of ~) | |
| immersion (ouverte, fermée, locale; ~ canonique) | (open, closed, local; canonical) immersion | |
| immersion régulière / quasi-régulière | regular / quasi-regular immersion | |
| induit (faisceau, préschéma ~ sur un ouvert, espace annelé) | induced (sheaf; prescheme induced on an open subset; ringed space) | |
| intégralement clos | integrally closed | |
| intègre (anneau, préschéma); localement intègre | integral; locally integral | = domain; cf. entier |
| invariant normal (d'ordre $n$, d'ordre infini) | normal invariant (of order $n$, of infinite order) | |
| invariants différentiels (fondamentaux) | (fundamental) differential invariants | IV TOC |
| isomorphisme local | local isomorphism | |
| le long de | along | |
| lemme de Chow | Chow's lemma | |
| lieu à l'infini | locus at infinity | |
| limite inductive (filtrante) | (filtered) inductive limit | (134:20 "direct limit") |
| limite projective | projective limit | (89:2 "inverse limit") |
| lisse; formellement lisse / non ramifié / étale | smooth; formally smooth / unramified / étale | |
| localement de type fini / de présentation finie | locally of finite type / of finite presentation | |
| localement fermé | locally closed | |
| localement libre (de rang $n$, de rang fini) | locally free (of rank $n$, of finite rank) | |
| localement noethérien | locally Noetherian | |
| localisation (de la platitude) | localization (of flatness) | (31:12 "localisation") |
| localisé en $x$ (point géométrique) | localized at $x$ | |
| localité | locality | |
| loi de composition (interne, externe) | (internal, external) composition law | |
| longueur (finie) | (finite) length | "of finite length" (43:6 "finite-length") |
| «main theorem» de Zariski | Zariski's ``main theorem'' | |
| majoré par | dominated by | (10:4 "majorized by") |
| Module ($\mathcal O_X$-Module, sous-$\mathcal O_X$-Module) | $\mathcal O_X$-module, sub-$\mathcal O_X$-module | lowercase (814:604); variant "Module" (IV §§2, 6–9, 21; III §7) |
| module de fractions | module of fractions | |
| Module inversible | invertible module | lowercase rule; ours has 1:2 "invertible Module" (IV) |
| module plat; $A$-plat; $f$-plat | flat module; $A$-flat; $f$-flat | |
| module quasi-fini | quasi-finite module | |
| monogène (module, algèbre) | monogenic | |
| morphisme d'immersion | immersion morphism | IV index (1×); I §4 title |
| morphisme d'injection (canonique) | (canonical) injection morphism (lit.) | I, 4.1.8–4.1.9; "majoré par un ~" = "dominated by an ~" |
| morphisme de Segre | Segre morphism | |
| morphisme quasi-compact; application quasi-compacte | quasi-compact morphism; quasi-compact map | |
| morphisme radiciel | radicial morphism | "radiciel" left untranslated 10× in 0 §§19–22 |
| morphisme structural | structural morphism | (74:10 "structure morphism") |
| morphisme universellement fermé / ouvert | universally closed / open morphism | |
| multiplication intérieure | interior multiplication (std) | III §1 |
| net (morphisme ~) | net (= unramified) | IV index |
| noethérien | Noetherian | capital N (1619:4) |
| nombre fini de | finitely many; a finite number of | (77:35) |
| nombre géométrique (de points, de composantes connexes) | geometric number (of points, of connected components) | |
| non ramifié | unramified | |
| non vide | non-empty | (87:58 "nonempty") |
| objet en groupes ($C$-~); $C$-groupe, $C$-anneau, $C$-module | group object (in $C$); $C$-group, $C$-ring, $C$-module | III index |
| objet final | final object | |
| objet gradué (limité inférieurement, supérieurement) | graded object (bounded below, above) | |
| opérateur différentiel (d'ordre $\leq n$) | differential operator (of order $\leq n$) | |
| ouvert (n.), fermé (n.); partie ouverte, partie fermée | open subset, closed subset | (282:42 "open set"; 172:12 "closed set") |
| ouvert affine | affine open subset | (139:29 "open affine") |
| ouvert formel affine (adique, noethérien) | affine formal open subset (adic, Noetherian) | |
| partie | subset | |
| partie multiplicative (saturée) | (saturated) multiplicative subset | |
| partie principale (d'ordre $n$) | principal part (of order $n$) | |
| partie propre (sur $\mathfrak Y$) | proper subset (over $\mathfrak Y$) | |
| partout défini | everywhere defined | |
| plat; platitude | flat; flatness | |
| point fermé / générique / maximal | closed / generic / maximal point | |
| point géométrique (au-dessus de $s$) | geometric point (above $s$) | |
| point rationnel sur $K$ | point rational over $K$; $K$-rational point | |
| polynôme de Hilbert | Hilbert polynomial | |
| positif (entier ~; à degrés ~s) | nonnegative (integer); graded in positive degrees | EGA "positif" = ≥ 0; ours: "nonnegative integers" (3:2), "positive degrees" (14:1) |
| préadique | preadic | no hyphen |
| préfaisceau (sur une base d'ouverts) | presheaf (on a basis of open subsets) | |
| préschéma ($S$-~; ~ au-dessus de $S$) | prescheme ($S$-prescheme; prescheme over $S$) | |
| préschéma algébrique | algebraic prescheme | |
| préschéma des sommets; section sommet | apex prescheme; apex section | |
| préschéma formel | formal prescheme | |
| présentation finie (de); module de type fini | of finite presentation; module of finite type | (535:32 "finitely presented"; 1154:57 "finitely generated") |
| principe de récurrence noethérienne | principle of Noetherian induction | |
| problème universel; propriété universelle | universal problem; universal property | |
| produit fibré | fibre product | |
| produit tensoriel complété | completed tensor product | |
| prolongement (d'une section, d'un faisceau; aux complétés); prolongement canonique | extension (to completions); canonical extension | |
| propre (morphisme); propreté | proper (morphism); properness | |
| puissance extérieure ($p$-ème) | ($p$-th) exterior power | |
| quasi-cohérent (et les autres quasi-) | quasi-coherent; quasi-compact, quasi-separated, quasi-finite, quasi-affine, quasi-projective, quasi-regular | always hyphenated |
| quelconque | arbitrary; any | |
| racine (d'un idéal); radical (d'un anneau); nilradical | radical (of an ideal); radical (of a ring); nilradical | "racine" ≠ root |
| rang (séparable) | (separable) rank | |
| rappels sur | review of | (4:2 "reminders on") |
| recollement; recoller | gluing; glue | "gluing" (24:2 "glueing") |
| recouvrement (ouvert, fini) | (open, finite) covering | (129:6 "cover") |
| récurrence (par ~) | (by) induction | |
| réduction (mod $\mathfrak J$) | reduction (modulo $\mathfrak J$) | |
| réduit (préschéma ~; préschéma réduit associé) | reduced (prescheme; associated reduced prescheme) | |
| relativement à | relative to | |
| résolution (injective, projective, plate, libre; de Cartan-Eilenberg) | resolution (injective, projective, flat, free; Cartan--Eilenberg) | en dash |
| restriction (d'un espace annelé, d'un morphisme); restriction des scalaires | restriction; restriction of scalars | |
| rétrocompact | retrocompact | |
| schéma | scheme | = separated prescheme (I, 5.4.1) |
| schéma affine | affine scheme | |
| schéma formel (affine) | (affine) formal scheme | |
| schéma local | local scheme | |
| schémas usuels | ordinary (pre)schemes | (5:3 "usual") |
| scindé (suite exacte ~e) | split (exact sequence) | |
| section ($S$-~; ~ au-dessus de $U$) | section ($S$-section; section over $U$) | |
| section nulle | zero section | |
| séparation (critère de ~) | separatedness (criterion for ~) | |
| séparé (morphisme, préschéma; anneau ~ et complet) | separated (morphism, prescheme; separated and complete ring) | never "Hausdorff" |
| séries formelles restreintes | restricted formal power series | |
| somme (de préschémas) | sum (of preschemes) | |
| sous-faisceau | sub-sheaf | (15:3 "subsheaf") |
| sous-objet | subobject | |
| sous-préschéma (ouvert, fermé) | (open, closed) sub-prescheme | (318:116); variant "subprescheme" (III; I index) |
| sous-schéma | subscheme | (29:3 "sub-scheme") |
| spécialisation | specialization | (31:14 "specialisation") |
| spectre (d'une $\mathcal O_S$-Algèbre); spectre formel | spectrum (of an $\mathcal O_S$-algebra); formal spectrum | |
| spectre premier (homogène); spectre homogène | (homogeneous) prime spectrum; homogeneous spectrum | |
| suite régulière / quasi-régulière | regular / quasi-regular sequence | |
| suite spectrale (faiblement convergente, régulière, corégulière, birégulière) | spectral sequence (weakly convergent, regular, coregular, biregular) | |
| système de coefficients | coefficient system | |
| système fondamental (de voisinages, d'idéaux de définition) | fundamental system (of neighbourhoods, of ideals of definition) | |
| système inductif (adique) | (adic) inductive system | |
| système projectif (strict) | (strict) projective system | |
| théorème de connexion de Zariski | Zariski's connectedness theorem | |
| théorème de finitude; théorème fondamental; théorème d'existence | finiteness theorem; fundamental theorem; existence theorem | |
| topologie $\mathfrak J$-adique / $\mathfrak J$-préadique | $\mathfrak J$-adic / $\mathfrak J$-preadic topology | |
| topologie spectrale | spectral topology | |
| topologiquement nilpotent | topologically nilpotent | |
| Traité | Treatise | capital T |
| type fini (de); morphisme de type fini | of finite type; morphism of finite type | (1154:124 "finite-type") |
| unibranche | unibranch | |
| unité (élément ~; section ~) | unit element; unit section | variant "identity element" (2:2) |
| universellement injectif | universally injective | |
| valeur (d'une section en un point) | value (of a section at a point) | |
| voisinage (ouvert); voisinage infinitésimal ($n$-ème); voisinage formel | (open) neighbourhood; ($n$-th) infinitesimal neighbourhood; formal neighbourhood | British (656:14 "neighborhood") |
