# 🧵 Welcome to the Stitching2D Wiki

**Stitching2D** is a precision 2D pattern drafting CAD, seam topology validation engine, fabric roll nesting optimizer, and interactive Three.js 3D product preview studio built for technical outdoor gear makers, apparel designers, and MYOG (Make Your Own Gear) builders.

---

## 📚 Wiki Sitemap

* **[📐 2D Pattern Drafting & Sewing Math](Pattern-Drafting-and-Math)** — Parallel polygon offsetting, variable seam allowances, Bézier curves, corner mitering, and grainlines.
* **[🔗 Seam Topology & Ease Validation](Seam-Topology-and-Validation)** — Automated edge matching, ease ratios, tolerance thresholds ($\Delta L \le 0.05\text{ in}$), and ISO seam classifications.
* **[✂️ Fabric Nesting & Automated BOM](Fabric-Nesting-and-BOM)** — 2D guillotine shelf-nesting on bolt rolls ($45'', 54'', 60'', 72''$), ISO 301 thread consumption formulas, and hardware takeoffs.
* **[🧊 Three.js 3D WebGL Studio](ThreeJS-3D-Product-Preview)** — Real-time parametric 3D assembly, interactive "🧲 Mouth Snap" kinematic folding, and 2D $\leftrightarrow$ 3D cross-linked glowing piece synchronization.
* **[🧗 Project Spotlight: BoulderPro Magnetic Chalk Bucket](BoulderPro-Magnetic-Chalk-Bucket)** — Monolithic continuous U-panel cradle, 100% zipper-free N52 magnetic closures, 70D aerodynamic anti-puff baffles, and 1in bottom stash slot.

---

## ⚡ Quickstart Guide

### 1. Installation
```bash
git clone https://github.com/samhuynhle/stitching2d.git
cd stitching2d
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Launch Local CAD Dashboard
Double-click `run_server.bat` or run:
```bash
python -m uvicorn src.server:app --host 0.0.0.0 --port 5050 --reload
```
Open **[http://localhost:5050](http://localhost:5050)** in your browser.

### 3. CLI Power Tools
* **Inspect Project:** `python main.py --inspect data/projects/bouldering_chalk_bucket.json`
* **Validate Seams:** `python main.py --validate-seams data/projects/bouldering_chalk_bucket.json`
* **Bill of Materials:** `python main.py --bom data/projects/bouldering_chalk_bucket.json`
* **Optimize Nesting:** `python main.py --nest data/projects/bouldering_chalk_bucket.json`

---

## 🏛️ System Architecture

```
Stitching2D/
├── src/
│   ├── core/
│   │   ├── geometry.py        # Offsets, Bézier splines, mitering, Shoelace area
│   │   ├── seam_logic.py      # Automated topological seam & ease validator
│   │   ├── nesting.py         # 2D guillotine fabric roll nesting engine
│   │   └── bom.py             # ISO 301 thread math, hardware & fabric takeoff
│   ├── models/
│   │   └── pattern.py         # Typed Pydantic data schemas
│   ├── renderers/
│   │   ├── svg_pattern.py     # Numbered callouts & auto-wrapping CAD legends
│   │   └── svg_cutting_layout.py # Fabric roll cut layout renderer
│   └── server.py              # FastAPI REST endpoints
├── static/
│   ├── index.html             # CAD Dashboard with Tabbed Viewports
│   ├── style.css              # Technical Design System
│   ├── app.js                 # UI State & Pan/Zoom SVG canvas
│   └── viewer3d.js            # Three.js WebGL 3D Studio & Glowing Selection
├── data/projects/             # JSON Project Blueprints
└── docs/                      # Technical Spec Sheets & Wiki Source
```
