import os
import glob
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .models.pattern import ProjectPattern, PatternPiece, Unit
from .core.geometry import compute_outward_offset, polygon_bounds
from .core.seam_logic import validate_project_seams
from .core.nesting import nest_project
from .core.bom import generate_bom
from .renderers.svg_pattern import render_piece_to_svg
from .renderers.svg_cutting_layout import render_nesting_layout_to_svg
from .renderers.svg_assembly_guide import get_illustrated_assembly_steps

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIRS = [
    os.path.join(PROJECT_ROOT, "data", "projects"),
    os.path.join(PROJECT_ROOT, "data", "private_projects")
]
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

app = FastAPI(title="Stitching2D Server", description="Precision 2D Stitching CAD & Pattern Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_project_from_file(project_id: str) -> ProjectPattern:
    for d in DATA_DIRS:
        if not os.path.exists(d):
            continue
        filepath = os.path.join(d, f"{project_id}.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return ProjectPattern(**data)
        
        # Search all json files in case ID differs from filename
        for f in glob.glob(os.path.join(d, "*.json")):
            with open(f, "r", encoding="utf-8") as handle:
                try:
                    data = json.load(handle)
                    if data.get("id") == project_id:
                        return ProjectPattern(**data)
                except Exception:
                    pass
    raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")


@app.get("/api/projects")
def list_projects():
    """Lists all available sewing projects across public and private directories."""
    projects = []
    seen_ids = set()
    for d in DATA_DIRS:
        if not os.path.exists(d):
            continue
        is_private = "private" in d
        for f in glob.glob(os.path.join(d, "*.json")):
            try:
                with open(f, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                    p_id = data.get("id")
                    if p_id and p_id not in seen_ids:
                        seen_ids.add(p_id)
                        name_display = f"[Private] {data.get('name')}" if is_private else data.get("name")
                        projects.append({
                            "id": p_id,
                            "name": name_display,
                            "version": data.get("version", "1.0.0"),
                            "description": data.get("description", ""),
                            "is_private": is_private
                        })
            except Exception as e:
                print(f"Error loading project {f}: {e}")
    return {"projects": projects}


@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    """Retrieves full JSON pattern specification for a project."""
    project = load_project_from_file(project_id)
    return project.model_dump()


@app.get("/api/projects/{project_id}/svg/{piece_id}")
def get_piece_svg(
    project_id: str,
    piece_id: str,
    scale: float = 24.0,
    show_cut_line: bool = True,
    show_attachments: bool = True,
    show_grainline: bool = True,
    show_dimensions: bool = True
):
    """Generates standalone calibrated 2D SVG vector markup for a specific pattern piece."""
    project = load_project_from_file(project_id)
    target_piece = next((p for p in project.pieces if p.id == piece_id), None)
    if not target_piece:
        raise HTTPException(status_code=404, detail=f"Piece '{piece_id}' not found in project '{project_id}'.")

    svg_content = render_piece_to_svg(
        target_piece,
        scale=scale,
        show_cut_line=show_cut_line,
        show_attachments=show_attachments,
        show_grainline=show_grainline,
        show_dimensions=show_dimensions
    )
    return Response(content=svg_content, media_type="image/svg+xml")


@app.get("/api/projects/{project_id}/seams")
def get_seam_validation(project_id: str, tolerance: float = 0.05):
    """Runs topological seam edge-matching and ease ratio analysis across all panels."""
    project = load_project_from_file(project_id)
    report = validate_project_seams(project, tolerance=tolerance)
    return report.model_dump()


@app.get("/api/projects/{project_id}/nesting")
def get_nesting_layouts(project_id: str, margin: float = 0.5):
    """Runs 2D fabric bolt nesting calculation and generates marker SVGs for all fabrics."""
    project = load_project_from_file(project_id)
    layouts = nest_project(project, margin=margin)
    
    result = {}
    for fab_id, layout in layouts.items():
        layout_dict = layout.model_dump()
        layout_dict["svg"] = render_nesting_layout_to_svg(layout, scale=12.0)
        result[fab_id] = layout_dict
    return result


@app.get("/api/projects/{project_id}/bom")
def get_bill_of_materials(project_id: str):
    """Calculates automated Bill of Materials (BOM) material takeoff."""
    project = load_project_from_file(project_id)
    bom = generate_bom(project)
    return bom.model_dump()


@app.get("/api/projects/{project_id}/assembly_guide")
def get_assembly_guide(project_id: str):
    """Generates the IKEA/LEGO-style illustrated step-by-step assembly manual with SVG schematics."""
    project = load_project_from_file(project_id)
    steps = get_illustrated_assembly_steps()
    return {
        "project_name": project.name,
        "total_steps": len(steps),
        "steps": steps
    }


# Mount static assets
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>Stitching2D Server Active</h2><p>Static UI not found.</p>")


@app.get("/favicon.ico")
def serve_favicon():
    return Response(
        content='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🧵</text></svg>',
        media_type="image/svg+xml"
    )


@app.get("/nesting")
def serve_nesting():
    nesting_path = os.path.join(STATIC_DIR, "nesting.html")
    if os.path.exists(nesting_path):
        with open(nesting_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>Stitching2D Nesting View Active</h2>")


def start_server(host: str = "0.0.0.0", port: int = 5050):
    print(f"🧵 Starting Stitching2D Server on http://localhost:{port}")
    uvicorn.run("src.server:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    start_server()
