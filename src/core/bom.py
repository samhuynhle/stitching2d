from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ..models.pattern import ProjectPattern, AttachmentType
from .geometry import polygon_perimeter, polygon_area
from .nesting import nest_project


class FabricTakeoff(BaseModel):
    fabric_id: str
    fabric_name: str
    bolt_width: float
    cut_length_inches: float
    yardage_exact: float
    yardage_recommended_10pct_waste: float
    estimated_cost: Optional[float] = None


class LinearMaterialTakeoff(BaseModel):
    name: str
    type: str  # webbing, zipper, velcro, elastic, bias_tape
    width: Optional[float]
    total_length_inches: float
    total_length_feet: float
    pieces_count: int


class HardwareTakeoff(BaseModel):
    name: str
    type: str
    quantity: int
    notes: Optional[str] = None


class BillOfMaterials(BaseModel):
    project_id: str
    project_name: str
    units: str
    fabrics: List[FabricTakeoff]
    linear_materials: List[LinearMaterialTakeoff]
    hardware: List[HardwareTakeoff]
    estimated_thread_consumption_yards: float
    total_seam_length_inches: float
    total_pieces_to_cut: int


def generate_bom(project: ProjectPattern) -> BillOfMaterials:
    """Calculates full Bill of Materials (BOM) takeoff for the project."""
    # 1. Fabrics takeoff via nesting engine
    nesting_layouts = nest_project(project)
    fabric_takeoffs: List[FabricTakeoff] = []
    fabric_map = {f.id: f for f in project.fabrics}

    for fab_id, layout in nesting_layouts.items():
        fab = fabric_map.get(fab_id)
        cut_len = layout.total_cut_length
        yds = layout.total_cut_length_yards
        yds_buffered = round(yds * 1.10, 2)  # +10% standard buffer
        cost = round(yds_buffered * fab.cost_per_yard, 2) if fab and fab.cost_per_yard else None

        fabric_takeoffs.append(
            FabricTakeoff(
                fabric_id=fab_id,
                fabric_name=layout.fabric_name,
                bolt_width=layout.bolt_width,
                cut_length_inches=round(cut_len, 2),
                yardage_exact=round(yds, 2),
                yardage_recommended_10pct_waste=yds_buffered,
                estimated_cost=cost
            )
        )

    # 2. Linear attachments (webbing, zipper, velcro, elastic)
    linear_map: Dict[str, Dict[str, Any]] = {}
    for piece in project.pieces:
        for att in piece.attachments:
            if att.type in (
                AttachmentType.WEBBING,
                AttachmentType.ZIPPER,
                AttachmentType.VELCRO,
                AttachmentType.ELASTIC,
            ) and att.length:
                key = f"{att.type.value}_{att.name}_{att.width or 0}"
                if key not in linear_map:
                    linear_map[key] = {
                        "name": att.name,
                        "type": att.type.value,
                        "width": att.width,
                        "total_len": 0.0,
                        "count": 0,
                    }
                qty = piece.quantity
                linear_map[key]["total_len"] += att.length * qty
                linear_map[key]["count"] += qty

    linear_takeoffs = [
        LinearMaterialTakeoff(
            name=v["name"],
            type=v["type"],
            width=v["width"],
            total_length_inches=round(v["total_len"], 2),
            total_length_feet=round(v["total_len"] / 12.0, 2),
            pieces_count=v["count"]
        )
        for v in linear_map.values()
    ]

    # 3. Hardware items
    hardware_takeoffs = [
        HardwareTakeoff(
            name=hw.name,
            type=hw.type,
            quantity=hw.quantity,
            notes=hw.notes
        )
        for hw in project.hardware
    ]

    # 4. Total seam lengths & Thread consumption (Lockstitch ISO 301 ratio approx 2.5x to 2.8x)
    total_seam_len = 0.0
    total_cut_pieces = 0
    for piece in project.pieces:
        perim = polygon_perimeter(piece.vertices)
        total_seam_len += perim * piece.quantity
        total_cut_pieces += piece.quantity

    # Standard thread ratio: 2.7x seam length + 15% bobbin & tail waste
    thread_yards = (total_seam_len * 2.7 * 1.15) / 36.0

    return BillOfMaterials(
        project_id=project.id,
        project_name=project.name,
        units=project.units.value,
        fabrics=fabric_takeoffs,
        linear_materials=linear_takeoffs,
        hardware=hardware_takeoffs,
        estimated_thread_consumption_yards=round(thread_yards, 1),
        total_seam_length_inches=round(total_seam_len, 2),
        total_pieces_to_cut=total_cut_pieces
    )
