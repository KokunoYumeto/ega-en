# EGA 0–IV — English edition

Original work by Alexandre Grothendieck and Jean Dieudonné.

This source project contains the editable mathematical text, formulas, diagrams,
references, styles and bibliography for the accompanying English reader. The
modular source is in `native/`; the assembled LaTeX source is in `direct/`.

To compile with an installed pdfLaTeX and BibTeX distribution, run in PowerShell:

```powershell
./BUILD.ps1 -PdfLatex <path-to-pdflatex> -BibTeX <path-to-bibtex> -SourceForm native -OutputDirectory <new-directory-inside-this-package>
```

Use `-SourceForm direct` for the assembled source. The build requires the standard
TeX packages and fonts named by the source preamble. The supplied script serializes
compilation and limits process memory; it does not install packages automatically.

Source editing and assembly: OpenAI Codex, GPT-6 Astra, Ultra. The retained EGA III-1
source also records work by GPT-5.6 Sol, Ultra. These credits concern the recorded
source work; they do not assign all inherited translation to either model.

Original rights and inherited licence notices remain applicable. This package
grants no additional rights over the original work.

[English editions](https://github.com/KokunoYumeto/ega-en) ·
[French editions](https://github.com/KokunoYumeto/ega-fr)
