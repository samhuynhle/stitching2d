from typing import Optional, List
from ..core.nesting import FabricNestingLayout


def wrap_text(text: str, max_chars: int = 34) -> List[str]:
    """Splits a string into lines that don't exceed max_chars, breaking on spaces."""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    for w in words:
        if current_len + len(w) + (1 if current_line else 0) <= max_chars:
            current_line.append(w)
            current_len += len(w) + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)
    if current_line:
        lines.append(" ".join(current_line))
    return lines or [text]


def render_nesting_layout_to_svg(
    layout: FabricNestingLayout,
    scale: float = 12.0,
    margin_px: float = 35.0
) -> str:
    """
    Renders a FabricNestingLayout into a professional CAD cutting marker SVG
    with numbered callout badges on each nested piece and an engineering legend card.
    """
    bolt_w_px = layout.bolt_width * scale
    cut_len_px = max(layout.total_cut_length, 12.0) * scale

    legend_w = 320.0
    gap_px = 30.0

    # Calculate legend card dimensions
    legend_items_count = len(layout.placements)
    # Estimate height per item based on text wrapping
    item_row_heights = []
    for p in layout.placements:
        name_lines = wrap_text(p.piece_name, max_chars=28)
        row_h = 32 + (len(name_lines) - 1) * 14 + (16 if p.is_optional else 0)
        item_row_heights.append(row_h)

    header_box_h = 95.0
    total_legend_h = header_box_h + sum(item_row_heights) + 30.0

    canvas_h = max(cut_len_px, total_legend_h)
    total_w = bolt_w_px + legend_w + gap_px + (margin_px * 2)
    total_h = canvas_h + (margin_px * 2)

    def tx(x: float) -> float:
        return x * scale + margin_px

    def ty(y: float) -> float:
        return y * scale + margin_px

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.1f} {total_h:.1f}" width="{total_w:.1f}" height="{total_h:.1f}" class="nesting-svg">',
        '<defs>',
        '  <pattern id="selvage" width="8" height="8" patternUnits="userSpaceOnUse">',
        '    <path d="M0 0 L8 8 M8 0 L0 8" stroke="#cbd5e1" stroke-width="1"/>',
        '  </pattern>',
        '</defs>',
        # Background canvas
        f'<rect width="100%" height="100%" fill="#f8fafc" />',
        # Fabric Bolt Roll (White fabric base)
        f'<rect x="{margin_px}" y="{margin_px}" width="{bolt_w_px:.1f}" height="{cut_len_px:.1f}" fill="#ffffff" stroke="#94a3b8" stroke-width="2" rx="4" />',
        # Selvage edges (Left and Right)
        f'<rect x="{margin_px}" y="{margin_px}" width="10" height="{cut_len_px:.1f}" fill="url(#selvage)" />',
        f'<rect x="{margin_px + bolt_w_px - 10:.1f}" y="{margin_px}" width="10" height="{cut_len_px:.1f}" fill="url(#selvage)" />',
    ]

    # Yardage tick marks on the left
    yard_interval_in = 18.0  # every 0.5 yard
    cur_y = yard_interval_in
    while cur_y <= layout.total_cut_length:
        y_pos = ty(cur_y)
        yds = cur_y / 36.0
        svg_parts.append(f'<line x1="{margin_px - 8}" y1="{y_pos:.1f}" x2="{margin_px + bolt_w_px:.1f}" y2="{y_pos:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4,4" />')
        svg_parts.append(
            f'<text x="{margin_px - 12}" y="{y_pos + 4:.1f}" font-family="sans-serif" font-size="10" font-weight="600" fill="#64748b" text-anchor="end">{yds:.1f} yd ({cur_y:.0f}")</text>'
        )
        cur_y += yard_interval_in

    # Render each nested piece with clean polygon & Numbered Badge
    colors = ["#eff6ff", "#fefce8", "#f0fdf4", "#faf5ff", "#fff7ed", "#eef2ff", "#f0fdfa"]
    border_colors = ["#3b82f6", "#eab308", "#22c55e", "#a855f7", "#f97316", "#6366f1", "#14b8a6"]

    for idx, p in enumerate(layout.placements):
        callout_num = idx + 1
        if p.is_optional:
            bg = "#fef3c7"
            border = "#d97706"
            dash_attr = 'stroke-dasharray="5,3" stroke-width="2"'
        else:
            c_idx = idx % len(colors)
            bg = colors[c_idx]
            border = border_colors[c_idx]
            dash_attr = 'stroke-width="1.75"'

        pts_str = " ".join([f"{tx(pt.x):.1f},{ty(pt.y):.1f}" for pt in p.cut_vertices])
        svg_parts.append(
            f'<polygon points="{pts_str}" fill="{bg}" stroke="{border}" {dash_attr} />'
        )

        # Center point
        cx = tx(p.placed_x + p.width / 2.0)
        cy = ty(p.placed_y + p.height / 2.0)

        # Single Clean Numbered Badge (Circle) centered on piece — No floating text labels!
        badge_bg = "#d97706" if p.is_optional else "#2563eb"
        svg_parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="{badge_bg}" stroke="#ffffff" stroke-width="2" />'
        )
        svg_parts.append(
            f'<text x="{cx:.1f}" y="{cy + 4:.1f}" font-size="11" font-family="sans-serif" font-weight="800" fill="#ffffff" text-anchor="middle">{callout_num}</text>'
        )

    # ----------------------------------------------------
    # 3. CAD Cutting Legend & Takeoff Card (Right Sidebar)
    # ----------------------------------------------------
    legend_x = margin_px + bolt_w_px + gap_px
    legend_y = margin_px

    svg_parts.append(f'<g transform="translate({legend_x:.1f}, {legend_y:.1f})">')
    
    # Outer Card Background
    svg_parts.append(
        f'  <rect width="{legend_w}" height="{total_legend_h:.1f}" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />'
    )
    
    # Header Title Box
    svg_parts.append(
        f'  <rect width="{legend_w}" height="{header_box_h}" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" />'
    )
    
    # Fabric Header Text
    fab_lines = wrap_text(layout.fabric_name, max_chars=26)
    cur_header_y = 20
    for fl in fab_lines:
        svg_parts.append(
            f'  <text x="14" y="{cur_header_y}" font-size="12.5" font-family="sans-serif" font-weight="700" fill="#0f172a">{fl}</text>'
        )
        cur_header_y += 16

    # Metrics Summary Row
    svg_parts.append(
        f'  <text x="14" y="{cur_header_y + 4}" font-size="10" font-family="sans-serif" font-weight="600" fill="#475569">'
        f'    Bolt Width: <tspan fill="#0f172a" font-weight="700">{layout.bolt_width:.0f}"</tspan>  |  Cut Length: <tspan fill="#0f172a" font-weight="700">{layout.total_cut_length_yards:.2f} yds</tspan>'
        f'  </text>'
    )
    cur_header_y += 18
    svg_parts.append(
        f'  <text x="14" y="{cur_header_y + 2}" font-size="10" font-family="sans-serif" font-weight="600" fill="#475569">'
        f'    Utilization: <tspan fill="#16a34a" font-weight="700">{layout.utilization_rate_percent:.1f}%</tspan>  |  Waste: <tspan fill="#dc2626">{layout.waste_percent:.1f}%</tspan>'
        f'  </text>'
    )

    # Divider line
    cur_row_y = header_box_h + 14
    svg_parts.append(
        f'  <text x="14" y="{cur_row_y}" font-size="10.5" font-family="sans-serif" font-weight="700" fill="#334155" letter-spacing="0.5">CUTTING MARKER KEY ({legend_items_count} PANELS)</text>'
    )
    cur_row_y += 8
    svg_parts.append(
        f'  <line x1="14" y1="{cur_row_y}" x2="{legend_w - 14}" y2="{cur_row_y}" stroke="#e2e8f0" stroke-width="1" />'
    )
    cur_row_y += 14

    # Render each piece in the legend table
    for idx, p in enumerate(layout.placements):
        callout_num = idx + 1
        name_lines = wrap_text(p.piece_name, max_chars=26)
        row_h = item_row_heights[idx]

        # Alternating subtle row background
        if idx % 2 == 1:
            svg_parts.append(
                f'  <rect x="8" y="{cur_row_y - 10:.1f}" width="{legend_w - 16}" height="{row_h:.1f}" rx="4" fill="#f8fafc" />'
            )

        # Number Badge Circle
        badge_bg = "#d97706" if p.is_optional else "#2563eb"
        svg_parts.append(
            f'  <circle cx="24" cy="{cur_row_y + 4:.1f}" r="9.5" fill="{badge_bg}" stroke="#ffffff" stroke-width="1.5" />'
        )
        svg_parts.append(
            f'  <text x="24" y="{cur_row_y + 7.5:.1f}" font-size="10" font-family="sans-serif" font-weight="800" fill="#ffffff" text-anchor="middle">{callout_num}</text>'
        )

        # Piece Name
        p_name_y = cur_row_y
        for nl_idx, nl in enumerate(name_lines):
            svg_parts.append(
                f'  <text x="42" y="{p_name_y + (nl_idx * 14):.1f}" font-size="10" font-family="sans-serif" font-weight="600" fill="#0f172a">{nl}</text>'
            )
        
        detail_y = p_name_y + (len(name_lines) * 14)

        # Optional tag if applicable
        if p.is_optional:
            svg_parts.append(
                f'  <rect x="42" y="{detail_y - 10:.1f}" width="60" height="12" rx="2.5" fill="#d97706" />'
            )
            svg_parts.append(
                f'  <text x="72" y="{detail_y - 1:.1f}" font-size="7.5" font-family="sans-serif" font-weight="800" fill="#ffffff" text-anchor="middle">OPTIONAL</text>'
            )
            detail_y += 14

        # Details: Instance, Dimensions, Rotation
        mirror_str = " (Mirrored)" if p.is_mirrored else ""
        rot_info = f", {p.rotation_deg:.0f}° rot" if p.rotation_deg != 0 else ""
        svg_parts.append(
            f'  <text x="42" y="{detail_y:.1f}" font-size="9" font-family="sans-serif" fill="#64748b">'
            f'    #{p.instance_index}{mirror_str} — <tspan font-weight="600" fill="#475569">{p.width:.2f}" × {p.height:.2f}"</tspan>{rot_info}'
            f'  </text>'
        )

        cur_row_y += row_h

    svg_parts.append('</g>')
    svg_parts.append('</svg>')
    return "\n".join(svg_parts)
