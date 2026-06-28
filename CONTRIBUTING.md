# Contributing

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
> "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
> "OPTIONAL" in this document are to be interpreted as described in
> [BCP 14](https://www.rfc-editor.org/info/bcp14)
> [[RFC 2119]](https://datatracker.ietf.org/doc/html/rfc2119)
> [[RFC 8174]](https://datatracker.ietf.org/doc/html/rfc8174)
> when, and only when, they appear in all capitals, as shown here.

---

## Contents

- [How to Contribute](#how-to-contribute)
- [Naming Conventions](#naming-conventions)
  - [Directories](#directories)
  - [Files](#files)
  - [Acronyms and Industry Terms](#acronyms-and-industry-terms)
- [Documentation Standards](#documentation-standards)
- [CAD and Technical Files](#cad-and-technical-files)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

---

## How to Contribute

Contributions are welcome in any of the following forms:

- CAD drawings, toleranced prints, or machining notes
- Install photos and real-world fitment data
- Core, adapter, or plumbing product evaluations
- Corrections to specs, part numbers, or recommendations
- Documentation improvements

To contribute:

1. Fork the repository.
2. Create a branch named after the change (e.g., `add-setrab-core-data` or `fix-adapter-thread-spec`).
3. Make your changes following the conventions in this document.
4. Open a pull request against `main` with a clear description.

---

## Naming Conventions

Consistent naming makes the repository navigable without explanation. These rules MUST be followed for all new files and directories. Existing files SHOULD be renamed to match when they are modified.

### Directories

Directories MUST use **CamelCase words separated by underscores** (`_`).

The underscore is the demarcator between logical words in a directory name. Each word MUST be capitalized as it would appear in a title.

```text
CAD_Files/
Filter_Adapters/
Install_Photos/
Oil_Cooler_Cores/
Reference_Docs/
Sandwich_Adapters/
```

- Industry acronyms MUST follow the standards defined in [Acronyms and Industry Terms](#acronyms-and-industry-terms).
- Avoid articles (`A`, `An`, `The`) in directory names.
- Prefer singular names unless the directory inherently contains multiples (e.g., `Cores/`, not `Core/`).

### Files

File naming depends on the file type. The file extension MUST always be lowercase.

#### Code and script files

Files containing executable or interpreted code (`.py`, `.sh`, `.js`, `.c`, `.cpp`, `.rb`,
and similar) MUST use **all lowercase** words separated by hyphens (`-`), unless the
language, runtime, or tool requires a different casing (e.g., `Makefile`, `CMakeLists.txt`).

```text
oil-filter-thread-adapter.py    ✓
setup-freecad-env.sh            ✓
Oil-Filter-Thread-Adapter.py    ✗
Setup_FreeCAD_Env.sh            ✗
```

#### Markdown documentation files

Markdown files (`.md`) MUST use **all UPPERCASE** words separated by hyphens (`-`).
The `.md` extension MUST be lowercase.

```text
README.md                       ✓
CONTRIBUTING.md                 ✓
PROBLEM-STATEMENT.md            ✓
Problem_Statement.md            ✗
install-guide.md                ✗
```

#### Design, drawing, and document files

Non-code, non-markdown files (`.step`, `.dxf`, `.pdf`, `.stl`, `.fcstd`, `.xlsx`, etc.)
MUST use **CamelCase words separated by hyphens** (`-`). Each word MUST be capitalized as
it would appear in a title.

```text
Custom-Adapter-V1.step
LM2-Filter-Boss-Drawing.pdf
LZ0-Oil-Cooler-Mount-Bracket.dxf
Sandwich-Adapter-Drill-Template.dxf
Setrab-6119-Core-Datasheet.pdf
```

- Version identifiers SHOULD follow the word they modify with a capital `V` and a number: `Adapter-V2.step`.
- Do not use spaces, all-lowercase, all-uppercase (except acronyms), or snake_case in design file names.
- The file extension is NOT part of the CamelCase name; it MUST remain lowercase (`.step`, `.dxf`, `.pdf`).

### Acronyms and Industry Terms

Abbreviated words and initialisms MUST follow established industry capitalization. Do not apply CamelCase rules to recognized acronyms.

| Term | Correct | Incorrect |
| ---- | ------- | --------- |
| Computer-Aided Design | CAD | Cad, cad |
| AN fitting standard | AN | An, an |
| Original Equipment Manufacturer | OEM | Oem, oem |
| Drawing Exchange Format | DXF | dxf, Dxf |
| Standard for Exchange of Product Data | STEP | Step (as file format) |
| Portable Document Format | PDF | Pdf, pdf |
| Inner Diameter | ID | Id, id |
| Outer Diameter | OD | Od, od |
| Pounds per Square Inch | PSI | Psi, psi |
| National Pipe Thread | NPT | Npt, npt |
| Gross Combined Weight Rating | GCWR | Gcwr |
| Original Equipment Manufacturer | OEM | Oem |
| Light Machine 2 (engine code) | LM2 | Lm2, lm2 |
| Light Zero (engine code) | LZ0 | Lz0, lz0 |

When an acronym begins a file or directory name, it MUST still appear in its standard capitalization:

```text
CAD_Files/           ✓
OEM-Reference.pdf    ✓
Cad_Files/           ✗
Oem-Reference.pdf    ✗
```

---

## Documentation Standards

All documentation in this repository (`.md` files) MUST adhere to the following:

- Use the RFC 8174 / RFC 2119 boilerplate at the top of any document that uses normative language (MUST, SHOULD, MAY, etc.).
- Write in clear, direct prose. Avoid marketing language or vague qualifiers.
- Tables MUST have a header row and a separator row.
- Headings MUST be surrounded by blank lines.
- Lists MUST be surrounded by blank lines.
- Use HTTPS links only. Do not link to non-authoritative mirrors of spec documents.
- Measurements SHOULD include units. Prefer standard units with the abbreviation after the value (e.g., `0.002"`, `150 PSI`, `180°F`).
- Part numbers and manufacturer model names SHOULD be reproduced exactly as the manufacturer publishes them.

---

## CAD and Technical Files

- STEP (`.step`) files MUST be exported from the native CAD format and SHOULD be tested for import in at least one third-party viewer before committing.
- DXF (`.dxf`) files SHOULD target the AutoCAD 2010 format for broadest compatibility.
- PDF drawings MUST include a title block with: part name, revision, material, thread spec, critical tolerances, and the author's initials.
- All critical dimensions MUST include tolerances on the drawing. A dimension without a tolerance is REQUIRED to include a note referencing a default tolerance standard.
- Revision history SHOULD be tracked in the drawing title block, not only in git history.
- Native format files (e.g., `.f3d`, `.sldprt`, `.ipt`) MAY be included alongside the exported formats.

---

## Pull Request Process

1. PRs MUST target the `main` branch.
2. The PR description MUST include a summary of what changed and why.
3. Technical changes (adapter specs, torque values, thread specs) MUST cite a source.
4. CAD PRs SHOULD include at least one screenshot or render of the model.
5. Install photo PRs SHOULD include vehicle year, model, and engine variant in the PR description.
6. PRs with unresolved review comments MUST NOT be merged.

---

## Issue Reporting

When opening an issue:

- Use a descriptive title (e.g., `Mocal SO7/1 thread spec incorrect for LZ0` not `bug`).
- Include the engine variant (LM2 or LZ0) when the issue is engine-specific.
- Include part numbers, measurements, and sources when reporting incorrect specs.
- Label the issue appropriately (`bug`, `enhancement`, `question`, `cad`).

---

## Code of Conduct

Be direct and specific. Disagreements about specs, clearances, and tolerances are normal — back claims with measurements, datasheets, or install evidence. Personal attacks are not welcome.
