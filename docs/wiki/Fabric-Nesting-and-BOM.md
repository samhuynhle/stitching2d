# ✂️ Fabric Roll Nesting & Automated Bill of Materials (BOM)

Stitching2D includes a 2D guillotine/shelf cutting layout optimizer (`src/core/nesting.py`) and an automated material takeoff engine (`src/core/bom.py`).

---

## 1. 2D Fabric Roll Nesting Algorithm

Pattern pieces are nested across standard commercial bolt roll widths:
* **$45\text{ in}$ ($114\text{ cm}$):** Standard quilting & apparel cottons.
* **$54\text{ in}$ ($137\text{ cm}$):** X-Pac, technical laminates, vinyl, and upholstery.
* **$58\text{ in} - 60\text{ in}$ ($150\text{ cm}$):** Mil-Spec Cordura, Ballistic nylon, Polar Fleece, and Ripstop.
* **$72\text{ in}$ ($183\text{ cm}$):** Tarpaulins and oversized gear textiles.

### Nesting Optimization Rules:
1. **Grainline Alignment:** Pieces can only rotate by $0^\circ$ or $180^\circ$ unless the fabric has `directional_nap = true` (which strictly locks rotation to $0^\circ$).
2. **Buffer Spacing:** A $0.25''$ clearance gap is enforced between cut outlines to prevent rotary blade or laser crossover.
3. **Yield & Waste Calculation:**
   $$\text{Efficiency \%} = \left( \frac{\sum \text{Area of Cut Pieces}}{\text{Roll Width} \times \text{Roll Length Used}} \right) \times 100$$

---

## 2. Automated Bill of Materials (BOM) Takeoff

The BOM Engine (`src/core/bom.py`) generates complete procurement sheets:

### A. Fabric Requirements
* Total physical yardage $+ 10\%$ industry standard waste/kerf buffer.
* Cost estimation based on individual fabric cost per yard.

### B. Linear Hardware & Webbing Takeoff
* Mil-Spec Nylon / Polypropylene Webbing ($0.75'', 1.0'', 1.5'', 2.0''$).
* Zippers (#3, #5, #8, #10 YKK Coil / Aquaguard) with end stop buffers.
* Foldover Elastic Binding (FOE).

### C. Hardware Counts
* Neodymium Disc Magnets (N52).
* Duraflex Side-Release Buckles, Ladderlocks, Cam Buckles.
* D-Rings, Triangle Rings, O-Rings.
* Metal / Plastic Snap Buttons and Grommets.

### D. ISO 301 Lockstitch Thread Consumption Formula
$$\text{Thread Length} = (\text{Total Seam Perimeter}) \times (\text{Seam Plies}) \times 2.75$$

Where $2.75\times$ accounts for needle thread looping, bobbin thread consumption, and stitch penetration into the fabric plies.
