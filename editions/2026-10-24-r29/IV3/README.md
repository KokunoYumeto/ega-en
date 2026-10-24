# EGA IV, Part Three — English edition

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

Source editing and assembly: OpenAI Codex, GPT-6 Astra, Ultra. These credits concern the recorded
source work; they do not assign all inherited translation to the named model.

Original rights and inherited licence notices remain applicable. This package
grants no additional rights over the original work.

[English editions](https://github.com/KokunoYumeto/ega-en) ·
[French editions](https://github.com/KokunoYumeto/ega-fr)


## Translation sources and contributors

The EGA English edition series incorporates the human community translation [ryankeleti/ega](https://github.com/ryankeleti/ega). Its named contributors are Mateo Carmona, Tim Holzschuh, Tim Hosgood, Ryan Keleti, Thiago Solovera & Nery, and Wayne Yang. See [the contribution scope, exact source version and rights information](ATTRIBUTION.md). Subsequent additions are AI-translated; subsequent corrections, editing, typesetting and assembly are AI-produced. The publisher did not translate the text.

## Rights and availability

Rights in the original works and in any protected contributions to these derivative translations and transcriptions remain with their respective rights holders. This project does not dedicate those works or contributions to the public domain or grant a licence over them. Existing third-party notices and any permissions already granted remain applicable.

These editions are made available free of charge for non-commercial, purely educational purposes, on the presumption that the respective rights holders would not object to these translations and transcriptions being freely available alongside the French originals on [NUMDAM](https://www.numdam.org/journals/PMIHES/). This presumption is not a statement that permission has been obtained; free access to the originals does not itself grant permission to translate, adapt or republish them.

If you hold rights in any material presented here and object to its availability, please [open a GitHub issue](https://github.com/KokunoYumeto/ega-en/issues). The publisher will take down the affected material at the rights holder's request.
