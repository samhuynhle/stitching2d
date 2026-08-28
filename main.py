import sys
import os
import argparse
import json

# Ensure project root is in Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.models.pattern import ProjectPattern
from src.core.geometry import polygon_area, polygon_perimeter, polygon_bounds
from src.core.seam_logic import validate_project_seams
from src.core.nesting import nest_project
from src.core.bom import generate_bom
from src.server import start_server


def load_project_file(path: str) -> ProjectPattern:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return ProjectPattern(**json.load(f))

    # Check direct candidate paths
    candidates = [
        os.path.join(PROJECT_ROOT, "data", "projects", path),
        os.path.join(PROJECT_ROOT, "data", "projects", f"{path}.json"),
        os.path.join(PROJECT_ROOT, "data", "private_projects", path),
        os.path.join(PROJECT_ROOT, "data", "private_projects", f"{path}.json")
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c, "r", encoding="utf-8") as f:
                return ProjectPattern(**json.load(f))

    # Search all json files across directories by internal ID or partial match
    for d in [os.path.join(PROJECT_ROOT, "data", "projects"), os.path.join(PROJECT_ROOT, "data", "private_projects")]:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".json"):
                full_p = os.path.join(d, f)
                try:
                    with open(full_p, "r", encoding="utf-8") as handle:
                        data = json.load(handle)
                        if data.get("id") == path or os.path.splitext(f)[0] == path:
                            return ProjectPattern(**data)
                except Exception:
                    pass

    print(f"❌ Error: Project file not found for '{path}'")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Stitching2D — Precision 2D Pattern Drafting CAD, Seam Logic & Sewing Planner"
    )
    parser.add_argument("--serve", action="store_true", help="Launch local FastAPI server and interactive web UI")
    parser.add_argument("--port", type=int, default=5050, help="Web server port (default: 5050)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Web server host (default: 0.0.0.0)")
    parser.add_argument("--inspect", type=str, help="Inspect pattern pieces and geometry in a project JSON")
    parser.add_argument("--validate-seams", type=str, help="Run seam topology matching and ease ratio checks")
    parser.add_argument("--bom", type=str, help="Generate Bill of Materials (BOM) material takeoff")
    parser.add_argument("--nest", type=str, help="Calculate fabric roll cutting nesting layouts and yield")

    args = parser.parse_args()

    if args.inspect:
        project = load_project_file(args.inspect)
        print(f"\n=======================================================")
        print(f"🧵 Stitching2D Project Inspector: {project.name}")
        print(f"=======================================================")
        print(f"ID: {project.id} | Units: {project.units.value} | Pieces: {len(project.pieces)} | Fabrics: {len(project.fabrics)}")
        print(f"Description: {project.description}\n")

        for piece in project.pieces:
            area = polygon_area(piece.vertices)
            perim = polygon_perimeter(piece.vertices)
            minx, miny, maxx, maxy = polygon_bounds(piece.vertices)
            w = maxx - minx
            h = maxy - miny
            print(f"• [{piece.category.upper()}] {piece.name} ({piece.id})")
            print(f"  - Dimensions: {w:.2f}\" × {h:.2f}\" (Bounding Box)")
            print(f"  - Area: {area:.2f} sq {project.units.value} | Perimeter: {perim:.2f} {project.units.value}")
            print(f"  - Cut Qty: {piece.quantity} {'(1 + 1 Mirrored)' if piece.mirror else ''} | Fabric: {piece.fabric_id}")
            print(f"  - Default SA: {piece.default_seam_allowance}\" | Attachments: {len(piece.attachments)}")
            for att in piece.attachments:
                print(f"    ↳ Attachment: {att.name} ({att.type.value}) @ ({att.position.x}, {att.position.y})")
            print()
        return

    if args.validate_seams:
        project = load_project_file(args.validate_seams)
        report = validate_project_seams(project)
        print(f"\n=======================================================")
        print(f"🔗 Seam Topology Validation: {project.name}")
        print(f"=======================================================")
        print(f"Checked: {report.total_seams_checked} | Matched: {report.matched_seams} | Eased: {report.eased_seams} | Discrepancies: {report.mismatches}\n")
        for r in report.results:
            icon = "✅" if r.status == "MATCH" else ("⚠️" if r.status == "EASED" else "❌")
            print(f"{icon} [{r.status}] {r.source_piece_id}:{r.source_edge_id} <-> {r.target_piece_id}:{r.target_edge_id}")
            print(f"   Len: {r.source_length}\" vs {r.target_length}\" | ΔL: {r.length_delta}\" | Ease: {r.ease_ratio_percent:+.1f}% | SA Match: {r.seam_allowance_compatible}")
        return

    if args.bom:
        project = load_project_file(args.bom)
        bom = generate_bom(project)
        print(f"\n=======================================================")
        print(f"📊 Bill of Materials Takeoff: {project.name}")
        print(f"=======================================================")
        print("\n[Fabric Requirements]")
        for f in bom.fabrics:
            cost_str = f" (${f.estimated_cost:.2f})" if f.estimated_cost else ""
            print(f"• {f.fabric_name} ({f.bolt_width}\" roll): {f.yardage_recommended_10pct_waste} yds (exact: {f.yardage_exact} yds / {f.cut_length_inches}\"){cost_str}")

        print("\n[Linear Materials & Webbing]")
        for m in bom.linear_materials:
            print(f"• {m.name} ({m.type}): {m.total_length_inches}\" ({m.total_length_feet} ft) across {m.pieces_count} pieces")

        print("\n[Hardware Items]")
        for h in bom.hardware:
            print(f"• {h.name} ({h.type}): Qty {h.quantity} — {h.notes}")

        print("\n[Seam & Thread Estimates]")
        print(f"• Total Seam Perimeter: {bom.total_seam_length_inches}\" ({(bom.total_seam_length_inches/36):.1f} yds)")
        print(f"• Est. Thread Consumption (ISO 301): {bom.estimated_thread_consumption_yards} yds")
        print(f"• Total Pattern Panels to Cut: {bom.total_pieces_to_cut}")
        return

    if args.nest:
        project = load_project_file(args.nest)
        layouts = nest_project(project)
        print(f"\n=======================================================")
        print(f"✂️ Fabric Roll Nesting & Yield: {project.name}")
        print(f"=======================================================")
        for fab_id, l in layouts.items():
            print(f"• Fabric: {l.fabric_name} (Roll Width: {l.bolt_width}\")")
            print(f"  - Cut Length: {l.total_cut_length_yards:.2f} yds ({l.total_cut_length:.1f}\")")
            print(f"  - Net Pattern Area: {l.net_pattern_area_sq_in:.1f} sq in | Gross Fabric Area: {l.gross_fabric_area_sq_in:.1f} sq in")
            print(f"  - Fabric Utilization: {l.utilization_rate_percent:.1f}% | Waste: {l.waste_percent:.1f}%")
            print(f"  - Placements: {len(l.placements)} panels placed")
            for p in l.placements:
                print(f"    ↳ {p.piece_name} #{p.instance_index} @ ({p.placed_x}\", {p.placed_y}\") — Rot: {p.rotation_deg}°")
            print()
        return

    # Default action: start web server
    start_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
