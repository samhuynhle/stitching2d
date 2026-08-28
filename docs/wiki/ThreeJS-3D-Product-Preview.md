# 🧊 Three.js Interactive 3D WebGL Studio

The **Stitching2D 3D Preview Engine** (`static/viewer3d.js`) generates real-time, interactive 3D WebGL representations of the assembled physical product directly from the 2D CAD pattern data.

---

## 🎮 Key Capabilities

### 1. 🧲 Live "Mouth Snap" Kinematic Folding
The toolbar features a continuous **Mouth Snap Slider** that simulates magnetic closure kinematics in real time:
$$D_{\text{top}}(t) = 0.2'' + (5.8'' \times t) \quad \text{where } t \in [0.0, 1.0]$$
* **$1.0$ (Open):** Expands the mouth into the full $8.5'' \times 6.0''$ two-hand dipping opening.
* **$0.0$ (Snapped):** Simulates the 4 pairs of N52 magnets clamping the Ultrasuede rim flat into a $0.2''$ dust seal, folding the side gussets inward.

---

### 2. ✨ Cross-Linked 2D ⇄ 3D Glowing Selection
When you click any pattern piece in the 2D CAD sidebar:
* **Vivid Cyan Pulse:** The corresponding 3D mesh lights up with a radiant pulsating cyan neon glow (`#06b6d4`).
* **Auto-Ghosting:** If you select an interior piece (like the **`anti_puff_baffle_flap`** or **`fleece_lining_u_panel`**), the outer 1000D Cordura shell automatically drops to $25\%$ opacity so the internal component is clearly visible through the walls.

---

### 3. 🔍 Layer Isolation & View Modes
* **`Full Assembly`:** Outer 1000D Cordura shell + Teal Ultrasuede rim + Amber Anti-Puff Baffle flaps + Cream plush fleece lining.
* **`Exterior Shell`:** Strips away all interior layers to focus solely on external construction.
* **`Internal Anti-Puff Baffles`:** Renders only the 70D ripstop baffle flaps.
* **`Interior Fleece Lining`:** Renders only the soft fleece interior.
* **🔍 X-Ray Mode:** Semi-transparent shell showing the full internal stack.
* **🕸️ Wireframe Mode:** Shows the underlying polygon geometry and seam tessellation.

---

## 🕹️ Controls

* **Orbit Rotate:** Left Click + Drag
* **Pan Viewport:** Right Click + Drag (or Shift + Left Click)
* **Zoom:** Scroll Wheel / Pinch
