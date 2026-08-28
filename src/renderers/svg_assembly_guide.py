"""
Stitching2D — IKEA / LEGO Style Step-by-Step Illustrated Assembly Manual Generator
Generates clean vector SVG technical schematics and structured steps for technical gear assembly.
"""

from typing import List, Dict, Any


def generate_step_1_svg() -> str:
    """Step 1: Basement Floor & 2in Upward Self-Closing Flap Sub-Assembly"""
    return """
    <svg viewBox="0 0 520 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid1" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#f1f5f9" stroke-width="0.5"/>
        </pattern>
        <marker id="arrow1" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb" />
        </marker>
        <marker id="foldarrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626" />
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect width="100%" height="100%" fill="url(#grid1)" rx="8"/>

      <!-- BASEMENT FLOOR PANEL OUTLINE -->
      <!-- Base (y=0 to 8.0) + Flap (y=8.0 to 10.25) -->
      <rect x="50" y="40" width="260" height="150" fill="#eff6ff" stroke="#2563eb" stroke-width="2" rx="3" />
      <text x="58" y="58" font-family="sans-serif" font-size="10" font-weight="700" fill="#1e40af">① BASEMENT FLOOR (10.5" × 8.0")</text>

      <!-- FOLD LINE (y = 8.0) -->
      <line x1="50" y1="130" x2="310" y2="130" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="5,4" />
      <text x="315" y="133" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#dc2626">FOLD LINE (y=8.0")</text>

      <!-- 1" ELASTIC HINGE (Stitched under 15% tension) -->
      <rect x="70" y="122" width="220" height="16" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5" stroke-dasharray="2,2" rx="2" />
      <text x="180" y="133" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#854d0e" text-anchor="middle">1" ELASTIC HINGE (15% STRETCH) ────►</text>
      <!-- Stitch Lines -->
      <line x1="72" y1="124" x2="288" y2="124" stroke="#ca8a04" stroke-width="1" stroke-dasharray="3,2"/>
      <line x1="72" y1="136" x2="288" y2="136" stroke="#ca8a04" stroke-width="1" stroke-dasharray="3,2"/>

      <!-- 2.0" UPWARD FLAP ZONE -->
      <rect x="50" y="130" width="260" height="60" fill="#dbeafe" fill-opacity="0.6" />
      <text x="58" y="148" font-family="sans-serif" font-size="9" font-weight="700" fill="#2563eb">2.0" UPWARD FLAP</text>

      <!-- 3x N52 MAGNETS -->
      <circle cx="90" cy="165" r="10" fill="#dc2626" stroke="#991b1b" stroke-width="1.5"/>
      <text x="90" y="169" font-family="sans-serif" font-size="9" font-weight="800" fill="#ffffff" text-anchor="middle">🧲</text>

      <circle cx="180" cy="165" r="10" fill="#dc2626" stroke="#991b1b" stroke-width="1.5"/>
      <text x="180" y="169" font-family="sans-serif" font-size="9" font-weight="800" fill="#ffffff" text-anchor="middle">🧲</text>

      <circle cx="270" cy="165" r="10" fill="#dc2626" stroke="#991b1b" stroke-width="1.5"/>
      <text x="270" y="169" font-family="sans-serif" font-size="9" font-weight="800" fill="#ffffff" text-anchor="middle">🧲</text>

      <!-- Center Snap Button Stud -->
      <circle cx="180" cy="165" r="5" fill="#1e293b" stroke="#ffffff" stroke-width="1.5"/>

      <!-- Pull Tab -->
      <rect x="170" y="185" width="20" height="20" fill="#334155" stroke="#0f172a" stroke-width="1" rx="2"/>
      <text x="180" y="198" font-family="sans-serif" font-size="8" font-weight="700" fill="#ffffff" text-anchor="middle">TAB</text>

      <!-- CALLOUT / FOLD UP ARROW -->
      <path d="M 340 175 Q 385 150 365 100" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-dasharray="4,3" marker-end="url(#arrow1)"/>
      <text x="390" y="130" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#2563eb">Folds UP &amp; Snaps</text>
      <text x="390" y="142" font-family="sans-serif" font-size="8.5" fill="#64748b">against lower front wall</text>

      <!-- LEGEND BADGE -->
      <rect x="360" y="45" width="140" height="42" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" rx="4"/>
      <text x="370" y="60" font-family="sans-serif" font-size="9" font-weight="800" fill="#0f172a">SEAM TOLERANCE</text>
      <text x="370" y="74" font-family="sans-serif" font-size="8.5" fill="#475569">Seam Allowance: 0.50"</text>
      <text x="370" y="84" font-family="sans-serif" font-size="8.5" fill="#16a34a">Hem Topstitch: 1/8" Edge</text>
    </svg>
    """


def generate_step_2_svg() -> str:
    """Step 2: Front U-Panel Hardware, Elevated 3D Pocket & Receiver Docks"""
    return """
    <svg viewBox="0 0 520 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid2" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#f1f5f9" stroke-width="0.5"/>
        </pattern>
        <marker id="arrow2" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb" />
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect width="100%" height="100%" fill="url(#grid2)" rx="8"/>

      <!-- LONG CONTINUOUS U-PANEL SECTION (FRONT WALL REGION) -->
      <rect x="40" y="30" width="220" height="180" fill="#eff6ff" stroke="#2563eb" stroke-width="2" rx="3" />
      <text x="48" y="46" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#1e40af">EXTERIOR CONTINUOUS U-PANEL</text>

      <!-- 1" Grab Handle (y=2.5) -->
      <rect x="75" y="55" width="150" height="12" fill="#1e293b" rx="2"/>
      <text x="150" y="64" font-family="sans-serif" font-size="8" font-weight="700" fill="#ffffff" text-anchor="middle">1" FRONT GRAB HANDLE (6.0")</text>

      <!-- Roll-Top Buckle Anchor (y=4.5) -->
      <rect x="140" y="75" width="20" height="18" fill="#475569" rx="2"/>
      <text x="150" y="88" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#ffffff" text-anchor="middle">♀ BUCKLE</text>

      <!-- ELEVATED 3D X-PAC POCKET BODY (y=5.0 to 8.5) -->
      <rect x="60" y="100" width="180" height="55" fill="#fdf4ff" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="3,2" rx="3"/>
      <text x="68" y="114" font-family="sans-serif" font-size="8.5" font-weight="700" fill="#9333ea">ELEVATED 3D X-PAC POCKET MOUNT</text>
      <!-- Pleats indicator -->
      <line x1="75" y1="100" x2="75" y2="155" stroke="#d8b4fe" stroke-width="1"/>
      <line x1="225" y1="100" x2="225" y2="155" stroke="#d8b4fe" stroke-width="1"/>
      <text x="150" y="132" font-family="sans-serif" font-size="8" fill="#7e22ce" text-anchor="middle">Box Pleated Volume (+1.0" Depth)</text>

      <!-- RECEIVER MAGNETS & SNAP SOCKET (y=10.0) -->
      <rect x="55" y="168" width="190" height="24" fill="#fee2e2" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="3,2" rx="2"/>
      <circle cx="85" cy="180" r="7" fill="#dc2626"/>
      <circle cx="150" cy="180" r="7" fill="#dc2626"/>
      <circle cx="215" cy="180" r="7" fill="#dc2626"/>
      <circle cx="150" cy="180" r="3.5" fill="#1e293b" stroke="#ffffff" stroke-width="1"/>
      <text x="150" y="176" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#b91c1c" text-anchor="middle">3x N52 RECEIVER MAGNETS + TRAVEL SNAP SOCKET</text>

      <!-- EXPLODED 3D POCKET PANEL COMING IN -->
      <path d="M 370 125 L 255 125" stroke="#9333ea" stroke-width="2" marker-end="url(#arrow2)"/>
      <rect x="375" y="95" width="115" height="60" fill="#faf5ff" stroke="#9333ea" stroke-width="1.8" rx="4"/>
      <text x="432" y="115" font-family="sans-serif" font-size="9" font-weight="800" fill="#6b21a8" text-anchor="middle">X-PAC POCKET</text>
      <text x="432" y="130" font-family="sans-serif" font-size="8" fill="#7e22ce" text-anchor="middle">VX21 Diamond Face</text>
      <text x="432" y="145" font-family="sans-serif" font-size="8" font-weight="700" fill="#16a34a" text-anchor="middle">RST 3/8" Seams</text>
    </svg>
    """


def generate_step_3_svg() -> str:
    """Step 3: Side Gussets (Inverted Brushes, Magnetic Docks & Carabiner Loop)"""
    return """
    <svg viewBox="0 0 520 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid3" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#f1f5f9" stroke-width="0.5"/>
        </pattern>
        <marker id="arrow3" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#16a34a" />
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect width="100%" height="100%" fill="url(#grid3)" rx="8"/>

      <!-- LEFT GUSSET (TRAPEZOID + 2" RISER) -->
      <polygon points="60,195 200,195 200,165 185,45 75,45 60,165" fill="#fefce8" stroke="#ca8a04" stroke-width="2" />
      <text x="130" y="38" font-family="sans-serif" font-size="9.5" font-weight="700" fill="#854d0e" text-anchor="middle">LEFT GUSSET (BRUSH CARRIER)</text>

      <!-- Top Carabiner Anchor Loop (y=9.0) -->
      <rect x="120" y="60" width="20" height="14" fill="#334155" stroke="#0f172a" stroke-width="1" rx="2"/>
      <circle cx="130" cy="67" r="3" fill="#ffffff"/>
      <text x="130" y="55" font-family="sans-serif" font-size="8" font-weight="700" fill="#0284c7" text-anchor="middle">CARABINER LOOP</text>

      <!-- Silicone-Grip Elastic Loops (y=6.0) -->
      <rect x="80" y="105" width="35" height="15" fill="#1e293b" rx="2"/>
      <rect x="145" y="105" width="45" height="15" fill="#1e293b" rx="2"/>
      <text x="97" y="116" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#f8fafc" text-anchor="middle">0.75" ELASTIC</text>
      <text x="167" y="116" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#f8fafc" text-anchor="middle">1.0" ELASTIC</text>

      <!-- Lower Magnetic Docks (y=3.0) -->
      <circle cx="97" cy="155" r="8" fill="#dc2626"/>
      <text x="97" y="159" font-family="sans-serif" font-size="8" font-weight="800" fill="#ffffff" text-anchor="middle">🧲</text>

      <circle cx="167" cy="155" r="8" fill="#dc2626"/>
      <text x="167" y="159" font-family="sans-serif" font-size="8" font-weight="800" fill="#ffffff" text-anchor="middle">🧲</text>
      <text x="130" y="180" font-family="sans-serif" font-size="8" font-weight="700" fill="#dc2626" text-anchor="middle">LOWER MAGNETIC DOCKS</text>

      <!-- INVERTED BRUSH SCHEMATIC (TAIL UP, BRISTLES DOWN) -->
      <!-- Detailing Brush -->
      <rect x="320" y="50" width="10" height="120" fill="#b45309" rx="2"/>
      <circle cx="325" cy="58" r="3" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5"/>
      <text x="325" y="44" font-family="sans-serif" font-size="8" font-weight="700" fill="#0284c7" text-anchor="middle">TAIL RING</text>
      <rect x="317" y="150" width="16" height="25" fill="#334155" rx="1"/>
      <text x="325" y="190" font-family="sans-serif" font-size="8" font-weight="700" fill="#334155" text-anchor="middle">BRISTLES DOWN</text>

      <path d="M 310 110 L 210 110" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow3)"/>

      <!-- RIGHT GUSSET MINI PREVIEW -->
      <polygon points="390,175 470,175 470,155 460,75 400,75 390,155" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" />
      <circle cx="430" cy="100" r="6" fill="#334155"/>
      <text x="430" y="65" font-family="sans-serif" font-size="8" font-weight="700" fill="#15803d" text-anchor="middle">RIGHT GUSSET</text>
      <text x="430" y="115" font-family="sans-serif" font-size="7.5" font-weight="600" fill="#475569" text-anchor="middle">0.75" D-RING</text>
    </svg>
    """


def generate_step_4_svg() -> str:
    """Step 4: Interior Anti-Puff Baffles & Microfleece Chamber"""
    return """
    <svg viewBox="0 0 520 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid4" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#f1f5f9" stroke-width="0.5"/>
        </pattern>
        <marker id="arrow4" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#f59e0b" />
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect width="100%" height="100%" fill="url(#grid4)" rx="8"/>

      <!-- MICROFLEECE CRADLE (GREY/DARK) -->
      <rect x="60" y="40" width="220" height="150" fill="#f1f5f9" stroke="#475569" stroke-width="2" rx="4"/>
      <text x="170" y="120" font-family="sans-serif" font-size="10" font-weight="800" fill="#334155" text-anchor="middle">HIGH-LOFT MICROFLEECE CHAMBER</text>
      <text x="170" y="135" font-family="sans-serif" font-size="8.5" fill="#64748b" text-anchor="middle">Traps Chalk Dust (280 GSM)</text>

      <!-- 70D DIAMOND RIPSTOP ANTI-PUFF BAFFLE FLAPS -->
      <rect x="75" y="45" width="190" height="32" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5" rx="3"/>
      <text x="170" y="64" font-family="sans-serif" font-size="9" font-weight="800" fill="#b45309" text-anchor="middle">70D RIPSTOP ANTI-PUFF BAFFLE FLAP</text>
      <line x1="75" y1="46" x2="265" y2="46" stroke="#d97706" stroke-width="2" stroke-dasharray="4,2"/>
      <text x="170" y="74" font-family="sans-serif" font-size="7.5" fill="#92400e" text-anchor="middle">Stitched to Top Rim with 3/8" Seam</text>

      <!-- INCOMING BAFFLE DIAGRAM -->
      <path d="M 350 60 L 275 60" stroke="#f59e0b" stroke-width="2" marker-end="url(#arrow4)"/>
      <rect x="355" y="42" width="130" height="50" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.5" rx="4"/>
      <text x="420" y="60" font-family="sans-serif" font-size="8.5" font-weight="800" fill="#b45309" text-anchor="middle">AERODYNAMIC BAFFLE</text>
      <text x="420" y="74" font-family="sans-serif" font-size="7.5" fill="#78350f" text-anchor="middle">Deflects Air Upwards</text>
      <text x="420" y="85" font-family="sans-serif" font-size="7.5" fill="#16a34a" text-anchor="middle">Zero Plume on Drop</text>

      <!-- ASSEMBLY NOTES PILL -->
      <rect x="310" y="125" width="180" height="60" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" rx="4"/>
      <text x="320" y="142" font-family="sans-serif" font-size="8.5" font-weight="800" fill="#0f172a">SEWING DIRECTIVE</text>
      <text x="320" y="156" font-family="sans-serif" font-size="8" fill="#475569">• Right sides together (RST)</text>
      <text x="320" y="168" font-family="sans-serif" font-size="8" fill="#475569">• 3/8" seam allowance</text>
      <text x="320" y="180" font-family="sans-serif" font-size="8" fill="#16a34a">• Leave top rim open for drop-in</text>
    </svg>
    """


def generate_step_5_svg() -> str:
    """Step 5: Ultrasuede Magnetic Collar & 3D Outer Shell Assembly"""
    return """
    <svg viewBox="0 0 520 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid5" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#f1f5f9" stroke-width="0.5"/>
        </pattern>
        <marker id="arrow5" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb" />
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect width="100%" height="100%" fill="url(#grid5)" rx="8"/>

      <!-- 3D EXPLODED UNION SCHEMATIC -->
      <!-- Center: Continuous U-Panel Folding Around Base & Gussets -->
      <!-- Left Gusset -->
      <polygon points="50,150 110,150 110,130 100,70 60,70 50,130" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
      <text x="80" y="115" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#854d0e" text-anchor="middle">LEFT GUSSET</text>

      <!-- Main U-Panel Center Cradle -->
      <path d="M 150 50 L 150 160 Q 210 190 270 160 L 270 50" fill="none" stroke="#2563eb" stroke-width="2.5"/>
      <text x="210" y="110" font-family="sans-serif" font-size="9" font-weight="800" fill="#1d4ed8" text-anchor="middle">CONTINUOUS U-PANEL</text>
      <text x="210" y="125" font-family="sans-serif" font-size="8" fill="#3b82f6" text-anchor="middle">Front - Base - Back</text>

      <!-- Right Gusset -->
      <polygon points="310,150 370,150 370,130 360,70 320,70 310,130" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
      <text x="340" y="115" font-family="sans-serif" font-size="7.5" font-weight="700" fill="#15803d" text-anchor="middle">RIGHT GUSSET</text>

      <!-- Join Arrows -->
      <path d="M 115 110 L 145 110" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow5)"/>
      <path d="M 305 110 L 275 110" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow5)"/>

      <!-- ULTRASUEDE TOP COLLAR WITH 8x N52 MAGNETS -->
      <rect x="140" y="30" width="140" height="18" fill="#10b981" rx="3"/>
      <circle cx="160" cy="39" r="4" fill="#ffffff"/>
      <circle cx="190" cy="39" r="4" fill="#ffffff"/>
      <circle cx="230" cy="39" r="4" fill="#ffffff"/>
      <circle cx="260" cy="39" r="4" fill="#ffffff"/>
      <text x="210" y="24" font-family="sans-serif" font-size="8" font-weight="800" fill="#065f46" text-anchor="middle">ULTRASUEDE COLLAR (4 PAIRS N52)</text>

      <!-- BASEMENT FLOOR PANEL -->
      <rect x="160" y="185" width="100" height="28" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5" rx="2"/>
      <text x="210" y="202" font-family="sans-serif" font-size="8" font-weight="800" fill="#1e40af" text-anchor="middle">BASEMENT FLOOR</text>

      <!-- SPECS CALLOUT -->
      <rect x="390" y="45" width="115" height="70" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1" rx="4"/>
      <text x="400" y="62" font-family="sans-serif" font-size="8.5" font-weight="800" fill="#0f172a">UNION SPECS</text>
      <text x="400" y="76" font-family="sans-serif" font-size="7.5" fill="#475569">• 1/2" Main Seam</text>
      <text x="400" y="88" font-family="sans-serif" font-size="7.5" fill="#475569">• Tex 90 / V-69 Thread</text>
      <text x="400" y="100" font-family="sans-serif" font-size="7.5" fill="#16a34a">• Notch Match Check</text>
    </svg>
    """


def generate_step_6_svg() -> str:
    """Step 6: Drop-In Lining Integration & Grosgrain Rim Binding"""
    return """
    <svg viewBox="0 0 520 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid6" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#f1f5f9" stroke-width="0.5"/>
        </pattern>
        <marker id="arrow6" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#16a34a" />
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect width="100%" height="100%" fill="url(#grid6)" rx="8"/>

      <!-- COMPLETED PRODUCT OUTLINE -->
      <!-- Outer Cordura Bucket -->
      <polygon points="120,200 280,200 295,70 105,70" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
      
      <!-- Inner Fleece Lining Dropping In -->
      <polygon points="135,185 265,185 275,85 125,85" fill="#f8fafc" stroke="#475569" stroke-width="1.5" stroke-dasharray="4,2"/>
      <path d="M 200 25 L 200 65" stroke="#16a34a" stroke-width="3" marker-end="url(#arrow6)"/>
      <text x="200" y="18" font-family="sans-serif" font-size="8.5" font-weight="800" fill="#15803d" text-anchor="middle">DROP IN LINING (WST)</text>

      <!-- GROSGRAIN BINDING TAPE WRAPPING TOP RIM -->
      <rect x="95" y="65" width="210" height="12" fill="#0f172a" stroke="#ffffff" stroke-width="1" rx="2"/>
      <text x="200" y="74" font-family="sans-serif" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">GROSGRAIN RIM BINDING TAPE (36.0")</text>

      <!-- 2" Basement Flap Visual -->
      <rect x="120" y="170" width="160" height="30" fill="#dbeafe" stroke="#1d4ed8" stroke-width="1.5"/>
      <circle cx="200" cy="180" r="3.5" fill="#1e293b"/>
      <text x="200" y="195" font-family="sans-serif" font-size="8" font-weight="800" fill="#1e40af" text-anchor="middle">2.0" BASEMENT FLAP (LOCKED)</text>

      <!-- FINAL QC CHECKLIST -->
      <rect x="335" y="45" width="165" height="135" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" rx="6"/>
      <text x="345" y="65" font-family="sans-serif" font-size="9.5" font-weight="800" fill="#166534">FINAL QC CHECKLIST</text>
      <text x="345" y="85" font-family="sans-serif" font-size="8" fill="#15803d">✅ Magnetic rim auto-snap test</text>
      <text x="345" y="100" font-family="sans-serif" font-size="8" fill="#15803d">✅ Elastic hinge snap-back test</text>
      <text x="345" y="115" font-family="sans-serif" font-size="8" fill="#15803d">✅ Travel snap button lock test</text>
      <text x="345" y="130" font-family="sans-serif" font-size="8" fill="#15803d">✅ Dual brush magnetic docking</text>
      <text x="345" y="145" font-family="sans-serif" font-size="8" fill="#15803d">✅ Zero chalk spill test</text>
      <text x="345" y="165" font-family="sans-serif" font-size="8.5" font-weight="800" fill="#2563eb">Ready for the Crag! 🧗</text>
    </svg>
    """


def get_illustrated_assembly_steps() -> List[Dict[str, Any]]:
    """Returns the full structured data with SVG diagrams for the illustrated assembly manual."""
    return [
        {
            "step_number": 1,
            "title": "Basement Floor & 2in Upward Self-Closing Flap Sub-Assembly",
            "phase": "Phase 1: Sub-Assemblies & Hardware Prep",
            "parts_needed": [
                {"name": "Basement Floor Panel", "badge": "①", "qty": 1, "type": "fabric"},
                {"name": "N52 Disc Magnets (15mm)", "badge": "🧲", "qty": 3, "type": "hardware"},
                {"name": "1in Elastic Hinge Webbing (8.0in)", "badge": "🧵", "qty": 1, "type": "linear"},
                {"name": "Center Travel Snap Button Stud", "badge": "🔘", "qty": 1, "type": "hardware"},
                {"name": "0.8mm HDPE Stiffener Blade (8.0in × 1.5in)", "badge": "🛡️", "qty": 1, "type": "insert"},
                {"name": "Hypalon Pull Tab", "badge": "🏷️", "qty": 1, "type": "webbing"}
            ],
            "instructions": [
                "Place <strong>Basement Floor Panel</strong> flat on cutting table right-side-up.",
                "Align the <strong>1in Elastic Hinge Strip</strong> along the interior fold line at <code>y = 8.0in</code>. Stitch with heavy polyester thread (Tex 70/90) under <strong>~15% stretch/tension</strong> so it actively springs upward when relaxed.",
                "Center and bartack the <strong>Hypalon Quick-Pull Tab</strong> at the top edge of the flap (<code>y = 10.0in</code>).",
                "Insert the <strong>0.8mm HDPE Stiffener Blade</strong>, <strong>3x N52 Neodymium Magnets</strong>, and install the <strong>Center Snap Button Stud</strong> inside the 2.0in upward hem channel.",
                "Fold hem edge over and double-row topstitch at <code>1/8in</code> from edge to securely encapsulate all hardware without needle strikes."
            ],
            "pro_tip": "Always check magnet polarity with the matching receiver magnets before final hem topstitching! Keep sewing machine needle at least 1/4in away from magnet edges.",
            "svg": generate_step_1_svg()
        },
        {
            "step_number": 2,
            "title": "Front Continuous U-Panel, Elevated 3D Pocket & Receiver Docks",
            "phase": "Phase 1: Sub-Assemblies & Hardware Prep",
            "parts_needed": [
                {"name": "Exterior Continuous U-Panel", "badge": "②", "qty": 1, "type": "fabric"},
                {"name": "Front 3D Bellows Pocket Body (X-Pac)", "badge": "➂", "qty": 1, "type": "fabric"},
                {"name": "Front Pocket Storm Flap", "badge": "➃", "qty": 1, "type": "fabric"},
                {"name": "N52 Receiver Magnets (15mm)", "badge": "🧲", "qty": 3, "type": "hardware"},
                {"name": "Center Travel Snap Socket", "badge": "🔘", "qty": 1, "type": "hardware"},
                {"name": "1in Roll-Top Female Buckle Anchor Webbing", "badge": "🧵", "qty": 1, "type": "webbing"},
                {"name": "1in Front Carry Grab Handle (6.0in)", "badge": "🧵", "qty": 1, "type": "webbing"}
            ],
            "instructions": [
                "Lay <strong>Exterior Continuous U-Panel</strong> flat. Box-stitch the <strong>Front 1in Grab Handle</strong> horizontally at <code>y = 2.5in</code>.",
                "Bartack the <strong>1in Female Buckle Anchor Webbing</strong> vertically at <code>y = 4.5in</code>.",
                "Fold the box-pleated bottom and side darts on the <strong>Front 3D X-Pac Pocket Body</strong> (+1.0in depth). Topstitch perimeter to the elevated placement guide at <code>y = 5.0in to 8.5in</code>.",
                "Encapsulate the <strong>3x N52 Receiver Magnets</strong> and <strong>Center Travel Snap Socket</strong> in a reinforcing patch on the lower front wall at <code>y = 10.0in</code> (exactly 2.0in above the front bottom fold line)."
            ],
            "pro_tip": "Elevating the 3D pocket gives generous visual and physical clearance above the 2.0in bottom flap so large phones and bulky tape rolls slide in with zero interference.",
            "svg": generate_step_2_svg()
        },
        {
            "step_number": 3,
            "title": "Side Gusset Sub-Assemblies (Brush Retention & D-Ring)",
            "phase": "Phase 1: Sub-Assemblies & Hardware Prep",
            "parts_needed": [
                {"name": "Exterior Left Side Gusset", "badge": "➄", "qty": 1, "type": "fabric"},
                {"name": "Exterior Right Side Gusset", "badge": "➅", "qty": 1, "type": "fabric"},
                {"name": "0.75in & 1.0in Silicone-Grip Elastic Loops", "badge": "🧵", "qty": 2, "type": "elastic"},
                {"name": "N52 Lower Brush Dock Magnets (15mm)", "badge": "🧲", "qty": 2, "type": "hardware"},
                {"name": "0.75in Top Micro-Carabiner Loop", "badge": "🏷️", "qty": 1, "type": "webbing"},
                {"name": "0.75in Aluminum D-Ring & Webbing Loop", "badge": "🪝", "qty": 1, "type": "hardware"}
            ],
            "instructions": [
                "<strong>Left Gusset:</strong> Box-stitch the <strong>0.75in Top Carabiner Clip Loop</strong> at <code>y = 9.0in</code>.",
                "Bartack the <strong>0.75in Detailing</strong> and <strong>1.0in Boulder Crimp Silicone Elastic Loops</strong> at <code>y = 6.0in</code>.",
                "Sew internal patch pockets to encapsulate the <strong>2x N52 Lower Magnetic Docks</strong> at <code>y = 3.0in</code> (aligned with inverted brush heads).",
                "<strong>Right Gusset:</strong> Thread <strong>0.75in D-Ring</strong> onto webbing loop, fold, and box-X stitch at <code>y = 9.5in</code>."
            ],
            "pro_tip": "With the top carabiner loop, brushes dock inverted (tail up, bristles down). This protects delicate boar's hair bristles from getting crushed in your pack!",
            "svg": generate_step_3_svg()
        },
        {
            "step_number": 4,
            "title": "Interior Anti-Puff Baffles & Microfleece Chamber Construction",
            "phase": "Phase 2: Interior Lining & Baffle System",
            "parts_needed": [
                {"name": "Interior Microfleece Cradle", "badge": "⑦", "qty": 1, "type": "fabric"},
                {"name": "Interior Fleece Side Gussets", "badge": "⑧", "qty": 2, "type": "fabric"},
                {"name": "70D Diamond Ripstop Anti-Puff Baffles", "badge": "⑨", "qty": 2, "type": "fabric"}
            ],
            "instructions": [
                "Hem the bottom edges of the <strong>70D Diamond Ripstop Anti-Puff Baffle Flaps</strong>.",
                "Baste baffle flaps along the upper mouth perimeter of the <strong>Interior Microfleece Cradle</strong>.",
                "Pin <strong>Fleece Side Gussets</strong> to the fleece main cradle, Right Sides Together (RST), aligning perimeter alignment notches.",
                "Sew around side seams with <code>3/8in</code> seam allowance using a walking foot or serger. Leave top mouth rim unsewn."
            ],
            "pro_tip": "Microfleece can stretch under standard presser feet. Reduce presser foot tension or use a Teflon/walking foot to prevent wavy seams.",
            "svg": generate_step_4_svg()
        },
        {
            "step_number": 5,
            "title": "Ultrasuede Magnetic Collar & Outer Shell Union",
            "phase": "Phase 3: 3D Shell Integration",
            "parts_needed": [
                {"name": "Ultrasuede Rim Gaskets", "badge": "⑩", "qty": 2, "type": "fabric"},
                {"name": "N52 Waterproof Disc Magnets (18mm × 2mm)", "badge": "🧲", "qty": 8, "type": "hardware"},
                {"name": "Prepared Continuous U-Panel Shell", "badge": "②", "qty": 1, "type": "subassembly"},
                {"name": "Prepared Side Gussets", "badge": "➄➅", "qty": 2, "type": "subassembly"},
                {"name": "Prepared Basement Floor Panel", "badge": "①", "qty": 1, "type": "subassembly"}
            ],
            "instructions": [
                "Sandwich <strong>4 pairs of 18mm N52 Magnets</strong> inside the <strong>Ultrasuede Rim Gasket</strong> channels and stitch divider pockets between each magnet.",
                "Pin the <strong>Exterior Left & Right Gussets</strong> to the <strong>Continuous U-Panel</strong>, Right Sides Together (RST), starting from the bottom corners and working upwards.",
                "Sew main structural perimeter seams with <code>1/2in</code> seam allowance using heavy bonded polyester Tex 90 thread.",
                "Stitch the <strong>Basement Floor Panel</strong> along the rear and side base seams, leaving the front 2.0in upward flap free to hinge."
            ],
            "pro_tip": "Clip curved corners at bottom transitions before turning right-side-out to produce crisp 90-degree box corners on the base.",
            "svg": generate_step_5_svg()
        },
        {
            "step_number": 6,
            "title": "Drop-In Lining Integration, Rim Binding & Final QC Inspection",
            "phase": "Phase 4: Final Finishing & Quality Assurance",
            "parts_needed": [
                {"name": "Outer Cordura Shell Assembly", "badge": "📦", "qty": 1, "type": "subassembly"},
                {"name": "Inner Microfleece Baffle Lining", "badge": "📦", "qty": 1, "type": "subassembly"},
                {"name": "Heavy-Duty Grosgrain Binding Tape (36.0in)", "badge": "🧵", "qty": 1, "type": "linear"}
            ],
            "instructions": [
                "Insert the <strong>Microfleece Baffle Lining</strong> into the <strong>Outer Cordura Shell</strong>, Wrong Sides Together (WST). Smooth out all corners.",
                "Align the <strong>Ultrasuede Magnetic Rim Gasket</strong> along the upper mouth perimeter and perimeter baste at <code>1/4in</code>.",
                "Wrap the entire top mouth circumference with <strong>1in Heavy-Duty Grosgrain Binding Tape</strong> using a binder attachment or twin-needle topstitch.",
                "Perform the 5-point Quality Control Inspection: Magnetic Snap Test, Elastic Hinge Spring-Back Test, Travel Snap Button Lock Test, Dual Brush Magnetic Docking, and Zero-Chalk-Plume Drop Test."
            ],
            "pro_tip": "Join grosgrain binding tape ends with a clean 45-degree bias fold at the rear center seam for a sleek factory finish!",
            "svg": generate_step_6_svg()
        }
    ]
