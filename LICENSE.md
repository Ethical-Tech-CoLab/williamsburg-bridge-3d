# License

This repository contains two kinds of material, licensed separately.

## Research content and data — CC BY 4.0

The governance documents, control data, source register, test definitions and generated model
artifacts are licensed under the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

This covers:

```text
README.md, AGENT-INSTRUCTIONS.md, GEOMETRY-CONTROL.md, SOURCE-REGISTER.md,
CONFIDENCE-MODEL.md, SCALE-HO.md, HOW-TO-DESIGN.md
tests/*.json
viewer/metadata/*.json
mesh/glb/*
```

You are free to share and adapt this material for any purpose, including commercially, provided you
give appropriate credit and indicate if changes were made.

Cite as:

> *Williamsburg Bridge Digital Twin: a source-governed control skeleton.* Ethical Tech CoLab, 2026.

## Code — MIT

The build pipeline and the browser viewer are licensed under the MIT License.

This covers:

```text
scripts/*.py
viewer/src/*, viewer/components/*, viewer/*.ts, viewer/*.json, viewer/index.html
```

```text
MIT License

Copyright (c) 2026 Ethical Tech CoLab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Incorporated material

**Ported code.** `scripts/control_model.py`, `scripts/normalize_units.py` and
`scripts/export_gltf.py` were ported from
[manhattan-bridge-3d](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-3d) (Ethical Tech
CoLab, MIT). `HOW-TO-DESIGN.md` is copied from the same repository under CC BY 4.0.

**Archival sources.** HAER No. NY-128 data pages and photograph captions are U.S. Government works
in the public domain and are retained in `sources/drawings/`.

**Quoted material.** Short passages are quoted for scholarly commentary and citation from the
New York City Department of Transportation's published bridge facts (© City of New York) and from
the Wikipedia article *Williamsburg Bridge* (CC BY-SA 4.0). Those passages remain the property of
their respective authors. No copyrighted source document is redistributed in this repository.
Individual sources, their licences and their verification state are recorded in
[SOURCE-REGISTER.md](SOURCE-REGISTER.md).
