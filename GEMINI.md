# Stitching2D (2D Stitching CAD & Planner) Agent Knowledge Base

## Mission
To provide a precision 2D computer-aided pattern drafting, computational geometry, seam logic validation, fabric cutting layout nesting, and attachment planning engine for technical sewing, outdoor gear design (MYOG), and apparel construction.

---

## 🧵 1. Core Domain Fundamentals

### The Coordinate System & Calibrated Units
* **Primary Units:** Imperial inches (`in`) or Metric millimeters (`mm`) / centimeters (`cm`).
* **Calibrated Scale:** All vector outputs (SVG, DXF) encode real-world dimensions:
  $$1\text{ in} = 25.4\text{ mm} = 96\text{ SVG user units (standard CSS px)}$$
* **2D Vector Representation:** Pattern pieces are represented as ordered 2D closed planar polygons or splines defined in local Cartesian coordinates $(x, y)$.

---

## 📐 2. Seam Allowances (SA) & Geometric Offsets

### Seam Allowance Mechanics
* **Cut Line vs. Sew Line (Stitch Line):**
  * **Sew Line:** The inner finished perimeter along which needle penetrations occur.
  * **Cut Line:** The outer perimeter where shears or rotary cutters cut the fabric, offset outward by the Seam Allowance ($SA$):
    $$P_{\text{cut}} = \text{Offset}(P_{\text{sew}}, +SA)$$
* **Variable Seam Allowances:** Different edges of the same pattern piece frequently demand different $SA$ values:
  * **Enclosed / Collar / Trim Seams:** $0.25\text{ in}$ ($6\text{ mm}$) to minimize bulk.
  * **Standard Technical / Apparel Seams:** $0.5\text{ in}$ ($12.7\text{ mm}$) or $0.375\text{ in}$ ($9.5\text{ mm}$).
  * **Flat-Felled & French Seams:** $0.625\text{ in}$ ($16\text{ mm}$) to $0.75\text{ in}$ ($19\text{ mm}$) for fold encapsulation.
  * **Folded Hems / Drawstring Channels:** $1.0\text{ in} - 2.0\text{ in}$ ($25 - 50\text{ mm}$) for multi-fold topstitching.
* **Corner Miter & Bevel Rules:**
  * **Mitered Corners:** Acute angles ($\theta < 90^\circ$) offset to sharp vertices, clipped if the miter length exceeds $2 \times SA$.
  * **Square / Hem Flairs:** Edges leading into folded hems must mirror or flair at the angle of the adjoining seam to prevent hem shorting when folded back.

---

## 🧭 3. Fabric Grainlines & Nesting Mathematics

### Grainline Orientations
1. **Straight Grain (Warp / Lengthwise):** Parallel to the fabric selvage ($0^\circ$). Highest tensile strength, minimal stretch. Crucial for load-bearing straps, body panels, and structural bags.
2. **Cross Grain (Weft / Crosswise):** Perpendicular to selvage ($90^\circ$). Slight mechanical give.
3. **True Bias:** Exactly $45^\circ$ diagonal to the warp/weft. Maximum mechanical stretch, fluidity, and drape. Used for bias binding tape over curved raw edges.

### Nesting & Cutting Layout Math
* **Bolt Constraints:** Standard roll widths:
  * $45\text{ in}$ ($114\text{ cm}$) — Standard cotton / lining
  * $54\text{ in} - 60\text{ in}$ ($137 - 152\text{ cm}$) — Technical Cordura, X-Pac, DCF, Softshell
  * $72\text{ in}$ ($183\text{ cm}$) — Heavy canvas / tarps
* **Nesting Yield & Efficiency Formula:**
  $$\text{Fabric Utilization Rate } (\eta) = \frac{\sum_{i=1}^{N} \text{Area}(\text{Piece}_i)}{\text{Bolt Width} \times \text{Cut Length}} \times 100\%$$
  $$\text{Waste Percentage } (W) = 100\% - \eta$$
* **Rotation Degrees of Freedom:**
  * **2-Way Directional ($0^\circ, 180^\circ$):** For fabrics with directional nap, pile, or camouflage print.
  * **1-Way Fixed ($0^\circ$):** For unidirectional fleece, velvet, or non-reversible prints.
  * **4-Way ($0^\circ, 90^\circ, 180^\circ, 270^\circ$):** For isotropic technical laminates (e.g., non-directional gridstop).

---

## 🔗 4. Seam Joining, Matching & Ease Topology

### Seam Topology Integrity
* **Edge-to-Edge Pairing:** When joining Piece $A$ Edge $k$ to Piece $B$ Edge $m$, the target seam lengths must satisfy:
  $$\Delta L = |L_A - L_B|$$
  * For rigid materials (Cordura, Vinyl): $\Delta L \le 0.05\text{ in}$ ($1.2\text{ mm}$).
  * For eased seams (sleeve cap into armhole): Ease Ratio $E = \frac{L_A - L_B}{L_B} \in [0.03, 0.08]$ ($3-8\%$ ease).
* **Notches & Balance Marks:** Single, double, and triple slit/triangle notches placed along edges at matching arc lengths from anchor vertices to guide assembler alignment during sewing.

---

## 🪡 5. Attachments, Hardware & Reinforcement Planning

### Hardware Library & Clearances
* **Webbing / Straps:** Standard widths: $0.75\text{ in}$ ($20\text{ mm}$), $1.0\text{ in}$ ($25\text{ mm}$), $1.5\text{ in}$ ($38\text{ mm}$), $2.0\text{ in}$ ($50\text{ mm}$).
* **Side-Release Buckles & Ladderlocs:** Insertion depth offset $+0.25\text{ in}$ from seam line for needle clearance.
* **Continuous Coil & Molded Tooth Zippers (#3, #5, #8, #10):**
  * Zipper Tape Width: e.g., #5 Coil = $1.25\text{ in}$ ($32\text{ mm}$) total tape width.
  * Zipper Window Opening: Cut width equals tape width minus $2 \times$ topstitch margin ($0.5\text{ in}$).
* **Grommets, Snaps & Rivets:** Requires circular reinforcement backing patches ($\ge 2 \times$ hardware outer diameter) and edge distance $\ge 1.5 \times \text{diameter}$.
* **Bartack & Box-X Reinforcement:** Load-bearing webbing anchors require high-density box-X stitching ($L \times W$, diagonal cross) or $42\text{ stitch}$ heavy bartacks.

---

## 🧮 6. Standard Stitch Classification (ISO 4915 / ASTM D6193)
* **Class 301 (Lockstitch):** Standard needle + bobbin thread. High tensile strength, zero stretch. Used for structural seams and webbing attachments.
* **Class 401 (Chainstitch):** Needle + looper thread. Good for long continuous seams with moderate flexibility.
* **Class 504 (3-Thread Overlock / Serging):** Edge trimming + overedge encapsulation. Prevents fraying on woven edges.
* **Class 607 (Flatlock):** 4-needle 6-thread joining stitch. Zero seam allowance, flat butt-joint for next-to-skin activewear.

---

## 🚀 7. Stitching2D Architecture & Modules

```text
Stitching2D/
├── data/
│   └── projects/                # Project JSON files (Chalk bag, Zipper pouch, Backpack panel)
├── docs/specs/                  # Spec sheets and feature designs
├── src/
│   ├── models/
│   │   ├── pattern.py           # Pydantic schemas (PatternPiece, Seam, Attachment, Hardware, Project)
│   │   └── schema.json          # Exported JSON Schema
│   ├── core/
│   │   ├── geometry.py          # Parallel polygon offsets, variable SA, Bézier curves, corner mitering
│   │   ├── seam_logic.py        # Edge matching, length validation, ease calculations, notch generation
│   │   ├── nesting.py           # Fabric bolt packing, guillotine/shelf cutting layout, yardage/waste math
│   │   └── bom.py               # Bill of Materials takeoff (fabric sq ft/yd, webbing, zippers, hardware)
│   ├── renderers/
│   │   ├── svg_pattern.py       # 2D SVG pattern piece renderer (cut/sew lines, grainlines, notches)
│   │   └── svg_cutting_layout.py# 2D SVG bolt cutting layout renderer
│   └── server.py                # FastAPI local web server (:5050) & interactive dashboard
├── static/                      # Interactive Web CAD & Nesting UI
│   ├── index.html
│   ├── style.css
│   └── app.js
├── main.py                      # CLI runner & server launcher
├── requirements.txt             # Python requirements
└── README.md                    # Project documentation
```

---
*Maintained by Gemini CLI*
