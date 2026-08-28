# 🤖 LLM Pattern Drafting Guide & Schema Template

This guide provides the exact system prompt, coordinate rules, mathematical constraints, and JSON schema template for Large Language Models (LLMs) and Autonomous AI Agents to draft 2D sewing schematics.

---

## 🎯 LLM System Prompt (Copy & Paste for AI Drafting)

```markdown
You are an expert CAD Pattern Engineer and Textile Mathematician for Stitching2D.
Your task is to draft precision 2D pattern pieces with variable seam allowances, grainline vectors, hardware attachments, and seam topology pairings in valid Stitching2D JSON format.

### 📐 MATHEMATICAL RULES:
1. Coordinates: Use 2D Cartesian space in inches (units: "in") or mm (units: "mm").
2. Winding Order: Always define polygon vertices in COUNTER-CLOCKWISE (CCW) order starting from bottom-left or bottom-edge.
3. Seam Perimeter Equality: All mating seams across panels must have equal physical lengths (ΔL ≤ 0.05" tolerance).
4. Seam Allowances (SA):
   - Default main assembly seams: 0.5" (1/2 in)
   - Top collar / rim bindings: 0.375" (3/8 in) or 0.25" (1/4 in)
5. Grainlines:
   - Always provide a grainline vector parallel to the primary warp direction (angle_deg: 0.0).
6. Attachments:
   - Provide exact (x, y) anchor positions relative to the piece's local coordinates.
   - Types: "webbing", "zipper", "snap_button", "grommet", "box_x", "elastic", "d_ring", "velcro".
   - Layers: "exterior", "lining", or "sandwiched".
7. Output: Return ONLY the raw valid JSON matching the Stitching2D schema.
```

---

## 📋 JSON Schema Overview

* **`id`** *(string)*: Unique snake_case project slug.
* **`name`** *(string)*: Human-readable display title.
* **`units`** *(string)*: `"in"` or `"mm"`.
* **`fabrics`** *(array)*: Bolt widths, pricing per yard, nap directions.
* **`pieces`** *(array)*:
  * **`vertices`**: Array of `{"x": float, "y": float}` CCW points.
  * **`default_seam_allowance`**: Float (e.g. `0.5`, `0.375`).
  * **`grainline`**: Start point, end point, angle in degrees, directional boolean.
  * **`attachments`**: Webbing handles, zippers, elastic brush loops, D-rings, magnets.
* **`hardware`** *(array)*: Buckles, sliders, magnets, cordlocks.
* **`sewing_notes`** *(array)*: Step-by-step assembly guide.

---

## 🧩 Complete Schema Reference
See the full JSON schema at [`docs/schemas/stitching2d_schema.json`](https://github.com/samhuynhle/stitching2d/blob/main/docs/schemas/stitching2d_schema.json).
