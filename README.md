# Stitching2D

A precision 2D pattern drafting CAD, computational seam logic validator, fabric bolt cutting nesting engine, and attachment planner for technical sewing, outdoor gear design (MYOG), and apparel construction.

---

## 🧵 Features

- **2D Vector Pattern Drafting:** Precise polygon and curve construction with calibrated units (inches, millimeters, centimeters).
- **Variable Seam Allowance (SA) Engine:** Supports uniform and per-edge custom seam allowances (e.g. $0.25\text{ in}$ collar seams, $0.5\text{ in}$ structural seams, $1.5\text{ in}$ folded hems) with automatic corner mitering.
- **Seam Topology & Ease Validator:** Validates perimeter length matching across paired edges, calculates ease ratios, and detects mismatches before cutting.
- **Fabric Bolt Nesting & Yield Calculator:** Places pattern pieces onto standard fabric roll widths ($45\text{ in}$, $54\text{ in}$, $60\text{ in}$, $72\text{ in}$), enforces grainline rotation constraints, and computes total yardage and waste percentage.
- **Attachments & Hardware Planner:** Defines webbing straps, zippers (#3, #5, #8, #10), velcro, snap buttons, grommets, D-rings, and reinforcement box-X/bartack stitching.
- **Automated Bill of Materials (BOM):** Generates material takeoffs for fabric area, linear webbing, zipper lengths, thread consumption, and hardware counts.
- **Interactive 3D WebGL Product Preview (Three.js):** Real-time 3D rendered assembly with orbit controls, interactive mouth opening/closing magnetic snap slider, X-Ray transparency, seam wireframe mode, and layer inspection (*Cordura shell, Ultrasuede collar, Fleece lining, TPU reservoir*).
- **Interactive Web Dashboard:** Local FastAPI server on `http://localhost:5050` with interactive 2D SVG pattern visualization, 3D WebGL studio viewer, zoom/pan controls, cutting layout viewer, and project manager.

---

## 🚀 Quick Start

1. **Install Dependencies:**
   ```powershell
   cd C:\Users\95sam\Documents\Gemini\Stitching2D
   pip install -r requirements.txt
   ```

2. **Launch the Local Server:**
   ```powershell
   python main.py
   ```
   Or explicitly:
   ```powershell
   python src/server.py
   ```

3. **Open the Interactive Web Dashboard:**
   Navigate to [http://localhost:5050](http://localhost:5050) in your browser.

---

## 📁 Repository Structure

```text
Stitching2D/
├── data/
│   └── projects/                # Sample project JSON templates (Chalk Bag, Zippered Pouch)
├── docs/specs/                  # Project specifications
├── src/
│   ├── models/                  # Pydantic data models (PatternPiece, Seam, Attachment, Hardware)
│   ├── core/                    # Computational geometry, seam logic, nesting & BOM engines
│   ├── renderers/               # 2D SVG vector renderers (Pattern pieces & Bolt cutting layout)
│   └── server.py                # FastAPI dashboard server (:5050)
├── static/                      # Browser UI assets (HTML, CSS, JS)
├── main.py                      # Application launcher & CLI
├── GEMINI.md                    # Domain knowledge base
├── requirements.txt             # Python dependencies
└── README.md
```
