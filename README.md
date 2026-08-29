# Elements of Algebraic Geometry (EGA) — complete linked English edition

## Related editions

Each link goes directly to a peer edition repository; there is no central hub. Coverage describes public releases and may trail local production.

| Edition | Language | Public scope |
|---|---|---|
| [EGA — French](https://github.com/KokunoYumeto/ega-fr) | French | Complete declared EGA I–IV scope |
| [EGA — English](https://github.com/KokunoYumeto/ega-en) | English | Complete declared EGA 0–IV scope |
| [EGA/FGA — Spanish](https://github.com/KokunoYumeto/ega-fga-es) | Spanish | Validated partial EGA; FGA tranches A and B |
| [SGA — Spanish](https://github.com/KokunoYumeto/sga-es) | Spanish | Complete 13-book linked edition |
| [SGA — English](https://github.com/KokunoYumeto/sga-en) | English | Complete published scope; SGA 6 has mixed source alignment |
| [EGA/FGA/SGA — Brazilian Portuguese](https://github.com/KokunoYumeto/ega-fga-sga-pt-br) | Brazilian Portuguese | Validated partial release, including complete EGA III-1 and SGA 5 readers |
| [EGA/FGA/SGA — Vietnamese](https://github.com/KokunoYumeto/ega-fga-sga-vi) | Vietnamese | Validated partial release; current public readers are EGA |
| [FGA — English (external)](https://github.com/thosgood/fga) | English | Independently maintained external edition |

## Readers

- [Open the complete cumulative EGA 0–IV reader](reader/00_EGA_EN_COMPLETE_LINKED_READER.pdf)
- [Open the standalone EGA III-2 reader](reader/EGA_III2_English_Standalone_Reader.pdf)
- [Open the standalone EGA IV-1 reader](reader/EGA_IV1_English_Standalone_Reader.pdf)
- [Open the standalone EGA IV-3 reader](reader/EGA_IV3_English_Standalone_Reader.pdf)
- [Open the standalone EGA IV-4 reader](reader/EGA_IV4_English_Standalone_Reader.pdf)

The cumulative reader contains EGA 0/I, II, III-1, III-2, and IV-1 through IV-4. The four standalone readers provide direct access to the largest independently rebuilt fascicles. Release r9 binds the reader set and editable-source archive to the same 135-file maintained English source tree through Canon queue R30.

## Persistent identifiers

- Stable concept DOI: <https://doi.org/10.5281/zenodo.21921591>
- Immutable r9 DOI: <https://doi.org/10.5281/zenodo.22147339>
- Predecessor r8 DOI: <https://doi.org/10.5281/zenodo.22145273>

## Source and build

Editable TeX for every reader is in [`source/`](source/). Run [`build/BUILD.ps1`](build/BUILD.ps1) to build all five PDFs with fixed reproducibility settings and place their public filenames in [`reader/`](reader/). Exact file identities are recorded in [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json), [`SOURCE_ARCHIVE_INVENTORY.json`](SOURCE_ARCHIVE_INVENTORY.json), and [`SOURCE_CONTROL_PUBLIC_PROJECTION.json`](SOURCE_CONTROL_PUBLIC_PROJECTION.json).

The English edition is independently maintained and source-rechecked against the French authority. French and English remain independent; no bilingual, parallel, side-by-side, paired, or interleaved reader is produced. No endorsement by the authors, IHÉS, NUMDAM, or an upstream Stacks maintainer is claimed. Project contribution: `AI typesetting & translation`.
