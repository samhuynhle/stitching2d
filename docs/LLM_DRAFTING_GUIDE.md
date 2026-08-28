# 🤖 Stitching2D LLM Pattern Drafting Guide & Schema Template

This guide provides the **exact instructions, coordinate rules, mathematical constraints, and JSON schema template** for Large Language Models (LLMs) and Autonomous AI Agents to reliably draft production-ready 2D sewing schematics and 3D product patterns.

---

## 🎯 LLM System Prompt (Copy & Paste for AI Drafting)

```markdown
You are an expert CAD Pattern Engineer and Textile Mathematician for Stitching2D.
Your task is to draft precision 2D pattern pieces with variable seam allowances, grainline vectors, hardware attachments, and seam topology pairings in valid Stitching2D JSON format.

### 📐 MATHEMATICAL RULES:
1. Coordinates: Use 2D Cartesian space in inches (units: "in") or mm (units: "mm").
2. Winding Order: Always define polygon vertices in COUNTER-CLOCKWISE (CCW) order starting from bottom-left or bottom-edge.
3. Seam Perimeter Equality: All mating seams across panels must have equal physical lengths (ΔL ≤ 0.05" tolerance):
   - Example: A continuous side gusset edge must equal the front slope + base edge + back slope of the cradle panel.
4. Seam Allowances (SA):
   - Default main assembly seams: 0.5" (1/2 in)
   - Top collar / rim bindings: 0.375" (3/8 in) or 0.25" (1/4 in)
   - Zipper seams: 0.375" (3/8 in)
5. Grainlines:
   - Always provide a grainline vector parallel to the primary warp direction (angle_deg: 0.0).
   - Set directional: true only for fabrics with directional nap (fleece, corduroy, velvet).
6. Attachments:
   - Provide exact (x, y) anchor positions relative to the piece's local coordinates.
   - Types: "webbing", "zipper", "snap_button", "grommet", "box_x", "elastic", "d_ring", "velcro".
   - Layers: "exterior", "lining", or "sandwiched".
7. Output: Return ONLY the raw valid JSON matching the Stitching2D schema without Markdown fences or conversational filler.
```

---

## 📋 JSON Schema Specification

```json
{
  "id": "unique_project_slug",
  "name": "Human Readable Project Name",
  "version": "1.0.0",
  "description": "Comprehensive design and construction summary.",
  "units": "in",
  "fabrics": [
    {
      "id": "fabric_id",
      "name": "Fabric Display Name",
      "type": "Technical textile classification (e.g. 1000D Cordura, X-Pac VX21, 70D Ripstop)",
      "bolt_width": 60.0,
      "cost_per_yard": 16.50,
      "directional_nap": false
    }
  ],
  "pieces": [
    {
      "id": "piece_id",
      "name": "Panel Display Name",
      "category": "main_body | gusset | pocket | trim | lining | strap",
      "fabric_id": "fabric_id",
      "quantity": 1,
      "mirror": false,
      "default_seam_allowance": 0.5,
      "vertices": [
        {"x": 0.0, "y": 0.0},
        {"x": 8.0, "y": 0.0},
        {"x": 8.0, "y": 10.0},
        {"x": 0.0, "y": 10.0}
      ],
      "grainline": {
        "start_point": {"x": 4.0, "y": 1.0},
        "end_point": {"x": 4.0, "y": 9.0},
        "angle_deg": 0.0,
        "directional": false
      },
      "attachments": [
        {
          "id": "attachment_id",
          "name": "Attachment Display Name",
          "type": "webbing | zipper | snap_button | grommet | box_x | elastic | d_ring | velcro",
          "position": {"x": 4.0, "y": 5.0},
          "length": 4.0,
          "width": 1.0,
          "angle_deg": 0.0,
          "layer": "exterior | lining | sandwiched",
          "notes": "Assembly or stitch specification"
        }
      ]
    }
  ],
  "hardware": [
    {
      "id": "hw_id",
      "name": "Hardware Name & Sizing",
      "type": "Buckle | Zipper Slider | D-Ring | Magnets | Snap Button | Cordlock",
      "quantity": 2,
      "notes": "Placement instructions"
    }
  ],
  "sewing_notes": [
    "Step-by-step ordered assembly instructions."
  ]
}
```

---

## 🧩 Few-Shot Examples for Common Gear Archetypes

### 1. Boxed-Corner Zippered EDC Pouch ($9'' \times 6'' \times 2.5''$)
```json
{
  "id": "boxed_corner_edc_pouch",
  "name": "Boxed Corner Tactical Gear Pouch",
  "version": "1.0.0",
  "description": "Standard 3D boxed-corner EDC utility pouch with #5 weatherproof zipper.",
  "units": "in",
  "fabrics": [
    {"id": "xpac_vx21", "name": "X-Pac VX21", "type": "Laminate", "bolt_width": 54.0, "cost_per_yard": 24.00, "directional_nap": false}
  ],
  "pieces": [
    {
      "id": "main_body_panel",
      "name": "Main Body Panel (Boxed Cutouts)",
      "category": "main_body",
      "fabric_id": "xpac_vx21",
      "quantity": 2,
      "mirror": false,
      "default_seam_allowance": 0.5,
      "vertices": [
        {"x": 1.25, "y": 0.0},
        {"x": 7.75, "y": 0.0},
        {"x": 7.75, "y": 1.25},
        {"x": 9.0, "y": 1.25},
        {"x": 9.0, "y": 6.0},
        {"x": 0.0, "y": 6.0},
        {"x": 0.0, "y": 1.25},
        {"x": 1.25, "y": 1.25}
      ],
      "grainline": {"start_point": {"x": 4.5, "y": 1.5}, "end_point": {"x": 4.5, "y": 5.0}, "angle_deg": 0.0, "directional": false},
      "attachments": [
        {"id": "top_zipper", "name": "YKK #5 Zipper", "type": "zipper", "position": {"x": 4.5, "y": 6.0}, "length": 9.0, "width": 1.0, "angle_deg": 0.0, "layer": "exterior", "notes": "Top entry"}
      ]
    }
  ],
  "hardware": [
    {"id": "hw_zip_slider", "name": "YKK #5 Matte Black Slider", "type": "Zipper Slider", "quantity": 1, "notes": "Main entry slider"}
  ],
  "sewing_notes": [
    "1. Stitch zipper to top edges of both panels with 3/8in SA.",
    "2. Join side and bottom seams with 1/2in SA.",
    "3. Pinch and stitch the 1.25in corner cutouts perpendicular to create 2.5in depth."
  ]
}
```

### 2. Cylindrical Roll-Top Dry Bag ($8'' \text{ Diameter} \times 16'' \text{ Tall}$)
* **Bottom Circular Base:** Approximated as regular 24-gon with radius $R = 4.0''$ ($\text{Perimeter} = 2\pi R = 25.13''$).
* **Rectangular Body Wrap:** Width $= 25.13''$, Height $= 18.0''$ (includes $2.0''$ roll-top collar).
* **Seam Equality:** Cylinder bottom perimeter ($25.13''$) = Body wrap width ($25.13''$) $\rightarrow \Delta L = 0.000''$.

---

## 🛠️ CLI Schema Validation Command
To verify that an LLM-generated JSON file is 100% compliant with Stitching2D:
```bash
python -c "from src.models.pattern import ProjectPattern; p = ProjectPattern.model_validate_json(open('data/projects/my_project.json').read()); print(f'Valid project: {p.name} ({len(p.pieces)} pieces)')"
```
