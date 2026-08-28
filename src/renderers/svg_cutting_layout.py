from typing import Optional
from ..core.nesting import FabricNestingLayout


def render_nesting_layout_to_svg(
    layout: FabricNestingLayout,
    scale: float = 12.0,
    margin_px: float = 40.0
) -> str:
    """Renders a FabricNestingLayout into a high-visibility cutting marker SVG."""
    bolt_w_px = layout.bolt_width * scale
    cut_len_px = max(layout.total_cut_length, 10.0) * scale

    total_w = bolt_w_px + (margin_px * 2)
    total_h = cut_len_px + (margin_px * 2)

    def tx(x: float) -> float:
        return x * scale + margin_px

    def ty(y: float) -> float:
        return y * scale + margin_px

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}" class="nesting-svg">',
        '<defs>',
        '  <pattern id="selvage" width="8" height="8" patternUnits="userSpaceOnUse">',
        '    <path d="M0 0 L8 8 M8 0 L0 8" stroke="#cbd5e1" stroke-width="1"/>',
        '  </pattern>',
        '</defs>',
        # Background canvas
        f'<rect width="100%" height="100%" fill="#f1f5f9" />',
        # Fabric Bolt Roll (White fabric base)
        f'<rect x="{margin_px}" y="{margin_px}" width="{bolt_w_px}" height="{cut_len_px}" fill="#ffffff" stroke="#94a3b8" stroke-width="2" rx="4" />',
        # Selvage edges (Left and Right)
        f'<rect x="{margin_px}" y="{margin_px}" width="10" height="{cut_len_px}" fill="url(#selvage)" />',
        f'<rect x="{margin_px + bolt_w_px - 10}" y="{margin_px}" width="10" height="{cut_len_px}" fill="url(#selvage)" />',
        # Header text
        f'<text x="{margin_px}" y="25" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a">'
        f'Fabric: {layout.fabric_name} ({layout.bolt_width:.0f}" Bolt Width) — Total Yardage: {layout.total_cut_length_yards:.2f} yds ({layout.total_cut_length:.1f}") — Utilization: {layout.utilization_rate_percent:.1f}%'
        f'</text>',
    ]

    # Yardage tick marks on the left
    yard_interval_in = 18.0  # every 0.5 yard
    cur_y = yard_interval_in
    while cur_y <= layout.total_cut_length:
        y_pos = ty(cur_y)
        yds = cur_y / 36.0
        svg_parts.append(f'<line x1="{margin_px - 8}" y1="{y_pos}" x2="{margin_px + bolt_w_px}" y2="{y_pos}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" />')
        svg_parts.append(
            f'<text x="{margin_px - 12}" y="{y_pos + 4}" font-family="sans-serif" font-size="10" font-weight="600" fill="#64748b" text-anchor="end">{yds:.1f} yd ({cur_y:.0f}")</text>'
        )
        cur_y += yard_interval_in

    # Render each nested piece
    colors = ["#dbeafe", "#fef3c7", "#dcfce7", "#f3e8ff", "#ffedd5", "#e0e7ff", "#ccfbf1"]
    border_colors = ["#2563eb", "#d97706", "#16a34a", "#9333ea", "#ea580c", "#4f46e5", "#0d9488"]

    for idx, p in enumerate(layout.placements):
        c_idx = idx % len(colors)
        bg = colors[c_idx]
        border = border_colors[c_idx]

        pts_str = " ".join([f"{tx(pt.x):.1f},{ty(pt.y):.1f}" for pt in p.cut_vertices])
        svg_parts.append(
            f'<polygon points="{pts_str}" fill="{bg}" stroke="{border}" stroke-width="1.5" />'
        )

        # Center label
        cx = tx(p.placed_x + p.width / 2.0)
        cy = ty(p.placed_y + p.height / 2.0)

        svg_parts.append(
            f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle" dy="-2">'
            f'{p.piece_name} #{p.instance_index}'
            f'</text>'
        )
        svg_parts.append(
            f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="sans-serif" font-size="9" fill="#475569" text-anchor="middle" dy="12">'
            f'{p.width:.1f}" × {p.height:.1f}" ({p.rotation_deg:.0f}°)'
            f'</text>'
        )

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)
