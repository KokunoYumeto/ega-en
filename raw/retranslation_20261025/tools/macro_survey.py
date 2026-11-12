"""Survey the macros and environments used in the French chunks and our English sources, to write a new preamble.
usage: python -I -X utf8 -B macro_survey.py"""
import collections
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parent.parent
STD = set("""begin end label ref section subsection subsubsection paragraph item emph textit textbf textrm textsc mathrm
mathcal mathscr mathfrak mathbf mathbb mathsf mathtt operatorname frac dfrac tfrac sum prod coprod lim varinjlim
varprojlim otimes oplus bigoplus bigotimes to mapsto rightarrow leftarrow longrightarrow longleftarrow
longmapsto cdot cdots ldots dots dotsc dotsb vdots ddots alpha beta gamma delta epsilon varepsilon zeta eta theta
vartheta iota kappa lambda mu nu xi pi rho varrho sigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda
Xi Pi Sigma Upsilon Phi Psi Omega in ni notin subset subseteq supset supseteq subsetneq cup cap bigcup bigcap circ
times wedge vee neq ne leq le geq ge left right quad qquad text hbox mbox footnote cite noindent par vspace hspace
smallskip medskip bigskip newline linebreak pagebreak clearpage cleardoublepage setcounter hat bar overline
underline widetilde widehat tilde check prime infty partial nabla exists forall emptyset varnothing not iff implies
colon ast star bullet equiv simeq cong approx sim ll gg mid nmid vert Vert langle rangle lbrace rbrace big Big bigg
Bigg bigl bigr Bigl Bigr biggl biggr Biggl Biggr ell ker dim deg sup inf max min log exp hom det leftrightarrow
Leftarrow Rightarrow Leftrightarrow Longrightarrow Longleftarrow Longleftrightarrow uparrow downarrow hookrightarrow
twoheadrightarrow xrightarrow xleftarrow overset underset stackrel limits nolimits displaystyle textstyle
scriptstyle scriptscriptstyle phantom vphantom hphantom hfill hfil centering enumerate itemize tabular hline
multicolumn array matrix pmatrix bmatrix cases align equation aligned split gathered tag nonumber notag mathop
mathbin mathrel mathord sqrt binom pmod bmod setminus smallsetminus lnot neg backslash leqslant geqslant
operatorname S textup upshape itshape bfseries normalfont small footnotesize large Large huge rm it bf sf tt sc
cdotp colon vdash dashv top perp parallel triangle square diamond flat natural sharp heartsuit spadesuit
dagger ddagger S P copyright pounds textendash textemdash slash ldotp lfloor rfloor lceil rceil quad enspace thinspace
negthinspace hskip vskip kern mkern mskip relax def let newcommand renewcommand providecommand DeclareMathOperator
usepackage documentclass input include maketitle tableofcontents title author date today and the""".split())
macros, envs = collections.Counter(), collections.Counter()
for p in list((R / "fr").glob("*.tex")) + list((R / "ours").rglob("*.tex")):
    t = p.read_text(encoding="utf-8", errors="replace")
    macros.update(re.findall(r"\\([A-Za-z]+)", t))
    envs.update(re.findall(r"\\begin\{([^}]+)\}", t))
print("non-standard macros (count):")
print(", ".join("%s:%d" % (k, v) for k, v in macros.most_common() if k not in STD and v >= 2))
print()
print("environments:", ", ".join("%s:%d" % (k, v) for k, v in envs.most_common(60)))
