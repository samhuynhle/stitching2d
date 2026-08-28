# 🔗 Seam Topology & Ease Validation Engine

The **Seam Topology Engine** (`src/core/seam_logic.py`) performs automated topological inspection across all mating pattern edges in a project to guarantee that panels join together without puckering, tension tears, or accidental bunching.

---

## 1. Automated Geometric Edge Matching

Stitching2D analyzes the geometric boundary of every pattern piece and checks:
1. **Explicit `paired_to` Tags:** Validates direct designer-specified edge pairings (e.g. `ext_u_panel:edge_2 <-> ext_side_gusset_left:edge_2`).
2. **Intelligent Geometric Auto-Discovery:** Automatically pairs matching perimeter segments across adjacent panels by comparing physical path lengths, shared layer categories, and edge orientations.

---

## 2. Validation Statuses & Tolerance Thresholds

| Status | Delta Threshold ($\Delta L$) | Ease Ratio ($\%$) | Physical Meaning |
| :--- | :--- | :--- | :--- |
| **`MATCH`** | $\Delta L \le 0.05\text{ in}$ | $0.0\%$ | Exact mathematical match. Pins smoothly with zero fabric distortion. |
| **`EASED`** | $0.05'' < \Delta L \le 0.50''$ | $+1.0\% \text{ to } +8.0\%$ | Intentional structural fullness (e.g., easing a curved sleeve cap into an armhole or stretching elastic trim). |
| **`MISMATCH`** | $\Delta L > 0.50''$ | $> +8.0\%$ or $< -8.0\%$ | Drafting defect! Flagged in red to alert the designer before cutting fabric. |

### Ease Ratio Formula:
$$\text{Ease \%} = \left( \frac{L_{\text{source}} - L_{\text{target}}}{L_{\text{target}}} \right) \times 100$$

---

## 3. Seam Allowance Compatibility Rules

* **Plain Join Seams (ISO 301):** Source $SA$ and Target $SA$ must match within $0.001''$.
* **French / Flat-Felled Seams:** Compatible even if $SA$ differs, provided the folding allowance ($2\times$) is accounted for.
* **Trim / Collar / Hem Joins:** Noted as `⚠️ Trim/Enclosed` if a $0.375''$ collar band joins a $0.5''$ main panel.

---

## 4. Example Validation Matrix (BoulderPro Chalk Bucket)

```
=======================================================
🔗 Seam Topology Validation: BoulderPro Magnetic Chalk Bucket
=======================================================
Checked: 19 | Matched: 18 | Eased: 1 | Discrepancies: 0

✅ [MATCH] ext_u_panel (Edge 2) <-> ext_side_gusset_left (Edge 2) | Len: 11.543" vs 11.543" (ΔL = 0.000")
✅ [MATCH] ext_u_panel (Edge 3) <-> ext_side_gusset_left (Edge 1) | Len: 8.000" vs 8.000" (ΔL = 0.000")
✅ [MATCH] ext_u_panel (Edge 4) <-> ext_side_gusset_left (Edge 4) | Len: 11.543" vs 11.543" (ΔL = 0.000")
⚠️ [EASED] rear_mesh_pocket <-> anti_puff_baffle_flap | Len: 8.600" vs 8.500" (Ease: +1.2%)
```
