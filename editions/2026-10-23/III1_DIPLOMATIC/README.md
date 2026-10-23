# EGA III, Part One — diplomatic English translation

Original work by Alexandre Grothendieck and Jean Dieudonné.

The modular LaTeX project is in `native/`; the assembled document is in `direct/`.
These sources contain the mathematical text, formulas, diagrams, references and
bibliography of the accompanying reader.

Compile with an installed pdfLaTeX and BibTeX distribution:

```powershell
./BUILD.ps1 -PdfLatex <pdflatex> -BibTeX <bibtex> -SourceForm native -OutputDirectory <new-directory-inside-this-package>
```

Use `-SourceForm direct` for the assembled document. Install the standard TeX
packages and fonts named in the preambles before compiling.

Source preparation and assembly: OpenAI Codex, GPT-6 Astra, Ultra.
The III-1 sources also include recorded work by GPT-5.6 Sol, Ultra.
These credits concern the recorded source work and do not attribute all inherited
translation to a single model. Original rights and licence notices remain applicable;
this package grants no additional rights over the original work.

[English editions](https://github.com/KokunoYumeto/ega-en) ·
[French editions](https://github.com/KokunoYumeto/ega-fr)

The modular build uses the supplied bibliography file; BibTeX is not run for this edition.


## Translation sources and contributors

The EGA English edition series incorporates the human community translation [ryankeleti/ega](https://github.com/ryankeleti/ega). Its named contributors are Mateo Carmona, Tim Holzschuh, Tim Hosgood, Ryan Keleti, Thiago Solovera & Nery, and Wayne Yang. See [the contribution scope, exact source version and rights information](ATTRIBUTION.md). Subsequent additions are AI-translated; subsequent corrections, editing, typesetting and assembly are AI-produced. The publisher did not translate the text.

## Rights and availability

Rights in the original works and in any protected contributions to these derivative translations and transcriptions remain with their respective rights holders. This project does not dedicate those works or contributions to the public domain or grant a licence over them. Existing third-party notices and any permissions already granted remain applicable.

These editions are made available free of charge for non-commercial, purely educational purposes, on the presumption that the respective rights holders would not object to these translations and transcriptions being freely available alongside the French originals on [NUMDAM](https://www.numdam.org/journals/PMIHES/). This presumption is not a statement that permission has been obtained; free access to the originals does not itself grant permission to translate, adapt or republish them.

If you hold rights in any material presented here and object to its availability, please [open a GitHub issue](https://github.com/KokunoYumeto/ega-en/issues). The publisher will take down the affected material at the rights holder's request.
