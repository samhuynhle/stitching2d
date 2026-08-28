# Spec: Stitching2D Application Initialization & Core Geometry Engine
**Date:** 2026-08-27
**Status:** Complete

### 1. Objective
Establish the `Stitching2D` application—a dedicated 2D vector CAD, pattern drafting, seam logic, fabric cutting nesting, and attachment planning engine for technical sewing, gear design, and garment construction.

---

### 2. Research & Context
- **Affected Files:**
  - `Stitching2D/GEMINI.md` — Domain knowledge base.
  - `Stitching2D/README.md` — Project documentation and setup guide.
  - `Stitching2D/requirements.txt` — Dependencies.
  - `Stitching2D/src/models/pattern.py` — Pydantic data schemas.
  - `Stitching2D/src/core/geometry.py` — Geometry offset and curve engine.
  - `Stitching2D/src/core/seam_logic.py` — Seam matching and topology engine.
  - `Stitching2D/src/core/nesting.py` — Bolt cutting layout and nesting engine.
  - `Stitching2D/src/core/bom.py` — Bill of Materials takeoff generator.
  - `Stitching2D/src/renderers/svg_pattern.py` — SVG pattern piece renderer.
  - `Stitching2D/src/renderers/svg_cutting_layout.py` — SVG bolt cutting layout renderer.
  - `Stitching2D/src/server.py` — FastAPI local web server (:5050).
  - `Stitching2D/main.py` — Launcher CLI.
  - `Stitching2D/data/projects/chalk_bag.json` & `zippered_pouch.json` — Built-in project templates.

---

### 3. Verification Plan
- Verify Pydantic schema validation on project templates.
- Verify variable seam allowance offsets and geometry calculations.
- Verify seam edge perimeter matching and ease calculation.
- Verify 2D nesting efficiency metrics and SVG rendering.
- Verify web dashboard on port `5050`.
