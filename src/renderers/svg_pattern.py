import math
from typing import List, Optional
from ..models.pattern import PatternPiece, ProjectPattern, AttachmentType, Point2D
from ..core.geometry import (
    compute_outward_offset,
    polygon_bounds,
    polygon_centroid,
    polygon_area,
    distance,
    build_edges_from_vertices
)


def wrap_text(text: str, max_chars: int = 34) -> List[str]:
    """Wraps text cleanly into multiple lines with word boundary protection."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    current_line = []
    current_len = 0
    for word in words:
        added_len = len(word) + (1 if current_line else 0)
        if current_len + added_len <= max_chars:
            current_line.append(word)
            current_len += added_len
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def render_piece_to_svg(
    piece: PatternPiece,
    scale: float = 22.0,
    padding: float = 36.0,
    show_cut_line: bool = True,
    show_attachments: bool = True,
    show_grainline: bool = True,
    show_dimensions: bool = True
) -> str:
    """Renders a single PatternPiece into a calibrated 2D SVG with multi-line wrapped text and an engineering legend."""
    # 1. Compute cut lines and bounding box
    edges = build_edges_from_vertices(piece)
    edge_sas = [e.seam_allowance if e.seam_allowance is not None else piece.default_seam_allowance for e in edges]
    cut_verts = compute_outward_offset(piece.vertices, edge_sas, piece.default_seam_allowance)

    all_verts = piece.vertices + cut_verts
    min_x, min_y, max_x, max_y = polygon_bounds(all_verts)

    width_in = max_x - min_x
    height_in = max_y - min_y
    area_sq_in = polygon_area(piece.vertices)

    # 2. Wrap Title and Subtitle Text
    legend_w = 320
    title_lines = wrap_text(piece.name, max_chars=34)
    subtitle_lines = wrap_text(
        f'Cut {piece.quantity} {"(1+1 Mirror)" if piece.mirror else ""} • SA: {piece.default_seam_allowance}" • {piece.fabric_id}',
        max_chars=40
    )

    header_box_h = 16 + (len(title_lines) * 16) + (len(subtitle_lines) * 14) + 6

    # 3. Process Attachment Legend Items
    legend_items = []
    total_legend_items_h = 0

    if show_attachments and piece.attachments:
        for idx, att in enumerate(piece.attachments):
            callout_num = idx + 1
            name_lines = wrap_text(att.name, max_chars=30)
            dim_str = f'{att.type.value.upper()} ({att.width or 0:.2f}" × {att.length or 0:.2f}")' if (att.width or att.length) else att.type.value.upper()
            row_h = max(34, (len(name_lines) * 14) + 18)
            total_legend_items_h += row_h

            legend_items.append({
                "num": callout_num,
                "name_lines": name_lines,
                "dims": dim_str,
                "row_h": row_h,
                "att": att
            })
    else:
        total_legend_items_h = 30

    total_legend_h = header_box_h + 38 + total_legend_items_h + 20

    content_w = width_in * scale
    content_h = height_in * scale

    svg_w = int(content_w + (padding * 2) + legend_w + 30)
    svg_h = int(max(content_h + (padding * 2), total_legend_h + (padding * 2)))

    pattern_offset_x = padding + legend_w + 30

    def tx(x: float) -> float:
        return (x - min_x) * scale + pattern_offset_x

    def ty(y: float) -> float:
        return (max_y - y) * scale + padding

    # 4. Build SVG elements
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" class="pattern-svg">',
        '<defs>',
        '  <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '    <path d="M 0 0 L 10 5 L 0 10 z" fill="#0284c7" />',
        '  </marker>',
        '  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">',
        '    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" stroke-width="1"/>',
        '  </pattern>',
        '</defs>',
        f'<rect width="100%" height="100%" fill="url(#grid)" />',
    ]

    # Background panel fill
    cut_pts_str = " ".join([f"{tx(p.x):.1f},{ty(p.y):.1f}" for p in cut_verts])
    sew_pts_str = " ".join([f"{tx(p.x):.1f},{ty(p.y):.1f}" for p in piece.vertices])

    if show_cut_line:
        svg_parts.append(
            f'<polygon points="{cut_pts_str}" fill="#f8fafc" stroke="#0f172a" stroke-width="2.0" stroke-linejoin="miter" />'
        )

    # Stitch line (Dashed blue line)
    svg_parts.append(
        f'<polygon points="{sew_pts_str}" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="6,4" />'
    )

    # Vertex dots
    for p in piece.vertices:
        svg_parts.append(f'<circle cx="{tx(p.x):.1f}" cy="{ty(p.y):.1f}" r="3.5" fill="#2563eb" />')

    # Edge length labels with backdrop pills
    if show_dimensions:
        for i, edge in enumerate(edges):
            mid_x = (edge.start.x + edge.end.x) / 2.0
            mid_y = (edge.start.y + edge.end.y) / 2.0
            l = distance(edge.start, edge.end)
            sa = edge.seam_allowance if edge.seam_allowance is not None else piece.default_seam_allowance
            lbl = f'{l:.2f}" (SA {sa:.2f}")'
            px = tx(mid_x)
            py = ty(mid_y)
            svg_parts.append(
                f'<rect x="{px - 44:.1f}" y="{py - 12:.1f}" width="88" height="15" rx="3" fill="#ffffff" fill-opacity="0.9" stroke="#cbd5e1" stroke-width="0.5"/>'
            )
            svg_parts.append(
                f'<text x="{px:.1f}" y="{py - 1:.1f}" font-size="9.5" font-family="sans-serif" font-weight="600" fill="#475569" text-anchor="middle">'
                f'{lbl}'
                f'</text>'
            )

    # Grainline arrow
    if show_grainline:
        c = polygon_centroid(piece.vertices)
        g_len = min(width_in, height_in) * 0.45
        if piece.grainline:
            angle_rad = math.radians(piece.grainline.angle_deg)
            gx1 = c.x - (g_len / 2.0) * math.cos(angle_rad)
            gy1 = c.y - (g_len / 2.0) * math.sin(angle_rad)
            gx2 = c.x + (g_len / 2.0) * math.cos(angle_rad)
            gy2 = c.y + (g_len / 2.0) * math.sin(angle_rad)
        else:
            gx1, gy1 = c.x, c.y - g_len / 2.0
            gx2, gy2 = c.x, c.y + g_len / 2.0

        svg_parts.append(
            f'<line x1="{tx(gx1):.1f}" y1="{ty(gy1):.1f}" x2="{tx(gx2):.1f}" y2="{ty(gy2):.1f}" stroke="#0284c7" stroke-width="1.75" marker-end="url(#arrow)" marker-start="url(#arrow)" />'
        )
        svg_parts.append(
            f'<rect x="{tx(c.x) - 34:.1f}" y="{ty(c.y) - 8:.1f}" width="68" height="16" rx="3" fill="#ffffff" fill-opacity="0.9" stroke="#bae6fd" stroke-width="0.75"/>'
        )
        svg_parts.append(
            f'<text x="{tx(c.x):.1f}" y="{ty(c.y) + 4:.1f}" font-size="9" font-family="sans-serif" fill="#0284c7" text-anchor="middle" font-weight="700" letter-spacing="0.5">GRAINLINE</text>'
        )

    # Render Attachment Markers & Numbered Badges on the Pattern Piece
    if show_attachments:
        for idx, item in enumerate(legend_items):
            att = item["att"]
            ax = tx(att.position.x)
            ay = ty(att.position.y)
            ang = att.angle_deg or 0.0

            l_px = (att.length or 2.0) * scale
            w_px = (att.width or 1.0) * scale

            svg_parts.append(f'<g transform="translate({ax:.1f}, {ay:.1f}) rotate({ang:.1f})">')

            if att.type == AttachmentType.WEBBING:
                # Length spans along primary axis, width along perpendicular
                svg_parts.append(
                    f'<rect x="{-l_px/2:.1f}" y="{-w_px/2:.1f}" width="{l_px:.1f}" height="{w_px:.1f}" fill="#f59e0b" fill-opacity="0.35" stroke="#d97706" stroke-width="1.5" rx="3" />'
                )
                # Stitch reinforcement ticks on ends
                svg_parts.append(f'<line x1="{-l_px/2 + 4:.1f}" y1="{-w_px/2:.1f}" x2="{-l_px/2 + 4:.1f}" y2="{w_px/2:.1f}" stroke="#d97706" stroke-width="1.5" stroke-dasharray="2,2"/>')
                svg_parts.append(f'<line x1="{l_px/2 - 4:.1f}" y1="{-w_px/2:.1f}" x2="{l_px/2 - 4:.1f}" y2="{w_px/2:.1f}" stroke="#d97706" stroke-width="1.5" stroke-dasharray="2,2"/>')
            elif att.type == AttachmentType.ZIPPER:
                svg_parts.append(
                    f'<line x1="{-l_px/2:.1f}" y1="0" x2="{l_px/2:.1f}" y2="0" stroke="#dc2626" stroke-width="4" stroke-dasharray="3,3" />'
                )
            elif att.type in (AttachmentType.GROMMET, AttachmentType.SNAP_BUTTON):
                if att.length and att.length > 2.0:
                    # Multi-magnet channel band
                    svg_parts.append(
                        f'<rect x="{-l_px/2:.1f}" y="{-w_px/2:.1f}" width="{l_px:.1f}" height="{w_px:.1f}" fill="#e2e8f0" fill-opacity="0.5" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4,2" rx="4" />'
                    )
                    # Discrete magnet indicators
                    for mx in [-l_px/3, 0.0, l_px/3]:
                        svg_parts.append(f'<circle cx="{mx:.1f}" cy="0" r="6.5" fill="#e2e8f0" stroke="#475569" stroke-width="1.5" />')
                        svg_parts.append(f'<circle cx="{mx:.1f}" cy="0" r="2" fill="#475569" />')
                else:
                    svg_parts.append(f'<circle cx="0" cy="0" r="7" fill="#e2e8f0" stroke="#475569" stroke-width="2" />')
                    svg_parts.append(f'<circle cx="0" cy="0" r="2.5" fill="#475569" />')
            elif att.type == AttachmentType.BOX_X:
                sz = w_px
                svg_parts.append(f'<rect x="{-sz/2:.1f}" y="{-sz/2:.1f}" width="{sz:.1f}" height="{sz:.1f}" fill="none" stroke="#ef4444" stroke-width="1.5" />')
                svg_parts.append(f'<line x1="{-sz/2:.1f}" y1="{-sz/2:.1f}" x2="{sz/2:.1f}" y2="{sz/2:.1f}" stroke="#ef4444" stroke-width="1.5" />')
                svg_parts.append(f'<line x1="{-sz/2:.1f}" y1="{sz/2:.1f}" x2="{sz/2:.1f}" y2="{-sz/2:.1f}" stroke="#ef4444" stroke-width="1.5" />')
            elif att.type == AttachmentType.ELASTIC:
                svg_parts.append(
                    f'<rect x="{-l_px/2:.1f}" y="{-w_px/2:.1f}" width="{l_px:.1f}" height="{w_px:.1f}" fill="#38bdf8" fill-opacity="0.3" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="2,2" rx="2" />'
                )
            else:
                svg_parts.append(f'<circle cx="0" cy="0" r="5" fill="#8b5cf6" />')

            svg_parts.append('</g>')

            # Numbered Badge Circle (render unrotated at anchor position for readability)
            badge_offset_x = (l_px / 2.0 + 12) if ang == 0.0 else 0
            badge_offset_y = (w_px / 2.0 + 12) if ang == 90.0 else 0
            svg_parts.append(
                f'<circle cx="{ax + badge_offset_x:.1f}" cy="{ay + badge_offset_y:.1f}" r="9.5" fill="#2563eb" stroke="#ffffff" stroke-width="1.5" />'
            )
            svg_parts.append(
                f'<text x="{ax + badge_offset_x:.1f}" y="{ay + badge_offset_y + 3.5:.1f}" font-size="10" font-family="sans-serif" font-weight="800" fill="#ffffff" text-anchor="middle">{item["num"]}</text>'
            )

    # 5. CAD Engineering Title Block & Attachment Legend Card (Sidebar)
    svg_parts.append(f'<g transform="translate({padding:.1f}, {padding:.1f})">')
    
    # Outer Legend Card Background
    svg_parts.append(
        f'  <rect width="{legend_w}" height="{total_legend_h}" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />'
    )
    
    # Title Block Header Box
    svg_parts.append(
        f'  <rect width="{legend_w}" height="{header_box_h}" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" />'
    )
    
    # Render Wrapped Title Lines
    cur_title_y = 18
    for t_line in title_lines:
        svg_parts.append(
            f'  <text x="14" y="{cur_title_y}" font-size="12" font-family="sans-serif" font-weight="700" fill="#0f172a">{t_line}</text>'
        )
        cur_title_y += 16

    # Render Wrapped Subtitle Lines
    cur_title_y += 2
    for s_line in subtitle_lines:
        svg_parts.append(
            f'  <text x="14" y="{cur_title_y}" font-size="9.5" font-family="sans-serif" fill="#64748b">{s_line}</text>'
        )
        cur_title_y += 13

    # Spec Dimensions Row
    spec_y = header_box_h + 16
    svg_parts.append(
        f'  <text x="14" y="{spec_y}" font-size="10" font-family="sans-serif" font-weight="600" fill="#475569">'
        f'    Dimensions: <tspan fill="#0f172a">{width_in:.2f}" × {height_in:.2f}"</tspan> ({area_sq_in:.1f} sq in)'
        f'  </text>'
    )
    svg_parts.append(
        f'  <line x1="14" y1="{spec_y + 10}" x2="{legend_w - 14}" y2="{spec_y + 10}" stroke="#f1f5f9" stroke-width="1" />'
    )

    # Legend Items Table
    cur_item_y = spec_y + 26
    if legend_items:
        svg_parts.append(
            f'  <text x="14" y="{cur_item_y}" font-size="9.5" font-family="sans-serif" font-weight="700" fill="#94a3b8" letter-spacing="0.5">ATTACHMENTS LEGEND</text>'
        )
        cur_item_y += 18

        for item in legend_items:
            # Badge Circle
            svg_parts.append(
                f'  <circle cx="22" cy="{cur_item_y + 2}" r="8" fill="#2563eb" />'
            )
            svg_parts.append(
                f'  <text x="22" y="{cur_item_y + 5.5}" font-size="9" font-family="sans-serif" font-weight="800" fill="#ffffff" text-anchor="middle">{item["num"]}</text>'
            )

            # Name Lines
            name_y = cur_item_y
            for n_idx, n_line in enumerate(item["name_lines"]):
                svg_parts.append(
                    f'  <text x="36" y="{name_y}" font-size="10" font-family="sans-serif" font-weight="700" fill="#0f172a">{n_line}</text>'
                )
                name_y += 13

            # Dims / Type
            svg_parts.append(
                f'  <text x="36" y="{name_y}" font-size="8.5" font-family="sans-serif" fill="#64748b">{item["dims"]}</text>'
            )

            cur_item_y += item["row_h"]
    else:
        svg_parts.append(
            f'  <text x="14" y="{cur_item_y + 10}" font-size="10" font-family="sans-serif" fill="#94a3b8">No attachments on this piece.</text>'
        )

    svg_parts.append('</g>')

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)
