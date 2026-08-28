# 📐 2D Pattern Drafting & Computational Geometry

Stitching2D uses computational geometry principles to generate physical pattern pieces, compute seam allowances, resolve acute corner miters, and render calibrated SVG blueprints.

---

## 1. Multi-Edge Variable Seam Allowance Offsets

In apparel and gear drafting, different edges require different seam allowances ($SA$):
* **Top Collar/Rim Joins:** Typically $0.25''$ or $0.375''$ (enclosed seams or bound hems).
* **Structural Load Seams:** $0.5''$ (standard joining seam).
* **French / Flat-Felled Seams:** $0.625'' - 0.75''$ (double-folded encased seams).

### The Parallel Offset Algorithm (`src/core/geometry.py`):
For a polygon defined by counter-clockwise vertices $V = [p_0, p_1, \dots, p_{n-1}]$, each edge $\vec{e}_i = p_{i+1} - p_i$ is offset outward along its normal vector $\vec{n}_i$:

$$\vec{n}_i = \left(-\frac{\Delta y_i}{\|\vec{e}_i\|},\; \frac{\Delta x_i}{\|\vec{e}_i\|}\right)$$

The offset line $L_i$ is defined by points $p'_i = p_i + SA_i \cdot \vec{n}_i$. Corner vertices are solved by computing the intersection point between consecutive offset lines $L_{i-1}$ and $L_i$.

---

## 2. Acute Corner Mitering

When two edges meet at an acute angle ($\theta < 60^\circ$), simple offset line intersection causes the cut corner to project outward excessively. Stitching2D checks the miter ratio:

$$\text{Miter Distance} = \frac{SA}{\sin(\theta / 2)}$$

If the miter distance exceeds $2.5 \times SA$, the corner is automatically clipped perpendicular to the angle bisector to prevent needle binding during corner turns.

---

## 3. Bézier Curve Approximations

Curved contours (sleeve caps, contoured backpacks, anatomical straps) are evaluated using cubic Bézier splines:

$$B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3 \quad \text{where } t \in [0, 1]$$

The physical arc length is approximated via adaptive chord summation:
$$L = \sum_{k=0}^{N-1} \| B(t_{k+1}) - B(t_k) \|$$

---

## 4. Shoelace Theorem for Pattern Surface Area

The net surface area of any polygon piece is calculated via the Shoelace Formula:

$$\text{Area} = \frac{1}{2} \left| \sum_{i=0}^{n-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$$

---

## 5. Grainline Constraints

Each pattern piece includes a directional grainline vector:
* **$0^\circ$ (Warp / Lengthwise Grain):** Zero stretch, parallel to the fabric selvedge. Carries vertical load.
* **$90^\circ$ (Weft / Crosswise Grain):** Slight elasticity.
* **$45^\circ$ (True Bias):** Maximum drape and fluid stretch.

During nesting, pieces with `directional = true` (like high-loft polar fleece or corduroy) are locked from $180^\circ$ flipping to prevent optical shade mismatches.
