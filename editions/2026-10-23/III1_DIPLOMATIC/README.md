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
