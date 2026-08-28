from typing import List, Dict, Tuple, Optional
import math
from pydantic import BaseModel
from shapely.geometry import Polygon
from shapely import affinity

from ..models.pattern import ProjectPattern, PatternPiece, FabricMaterial, Point2D
from .geometry import (
    compute_outward_offset,
    polygon_area,
    polygon_bounds,
    ensure_counter_clockwise
)


class NestedPiecePlacement(BaseModel):
    piece_id: str
    piece_name: str
    instance_index: int
    is_mirrored: bool
    is_optional: bool = False
    placed_x: float
    placed_y: float
    rotation_deg: float
    width: float
    height: float
    cut_vertices: List[Point2D]


class FabricNestingLayout(BaseModel):
    fabric_id: str
    fabric_name: str
    bolt_width: float
    total_cut_length: float
    total_cut_length_yards: float
    net_pattern_area_sq_in: float
    gross_fabric_area_sq_in: float
    utilization_rate_percent: float
    waste_percent: float
    placements: List[NestedPiecePlacement]


def get_cut_polygon_vertices(piece: PatternPiece) -> List[Point2D]:
    """Generates the cut perimeter with seam allowance for nesting."""
    edge_sas = [e.seam_allowance if e.seam_allowance is not None else piece.default_seam_allowance for e in (piece.edges or [])]
    if len(edge_sas) != len(piece.vertices):
        edge_sas = [piece.default_seam_allowance] * len(piece.vertices)
    return compute_outward_offset(piece.vertices, edge_sas, piece.default_seam_allowance)


def nest_pieces_for_fabric(
    fabric: FabricMaterial,
    pieces: List[PatternPiece],
    margin: float = 0.5
) -> FabricNestingLayout:
    """
    Nests pattern pieces onto a fabric roll of given bolt_width using a guillotine shelf-packing algorithm.
    Enforces grainline and directional nap rotation rules.
    """
    # Expand all piece instances (quantity + mirror)
    expanded_items: List[Dict] = []
    for piece in pieces:
        if piece.fabric_id != fabric.id:
            continue

        base_cut_verts = get_cut_polygon_vertices(piece)

        for q in range(piece.quantity):
            is_mirror = piece.mirror and (q % 2 == 1)
            verts = base_cut_verts
            if is_mirror:
                # Mirror across X axis
                verts = [Point2D(x=-p.x, y=p.y) for p in verts]

            # Allowed rotations based on grainline & directional nap
            allowed_rotations = [0.0]
            if not fabric.directional_nap:
                if piece.grainline and piece.grainline.directional:
                    allowed_rotations = [0.0]
                else:
                    # 180 flip allowed on straight grain
                    allowed_rotations = [0.0, 180.0]

            expanded_items.append({
                "piece_id": piece.id,
                "piece_name": piece.name,
                "instance_index": q + 1,
                "is_mirrored": is_mirror,
                "is_optional": piece.optional,
                "base_verts": verts,
                "allowed_rotations": allowed_rotations,
            })

    # Calculate bounding boxes and sort by descending height/area (First-Fit Decreasing)
    prepared_items = []
    total_net_area = 0.0

    for item in expanded_items:
        verts = item["base_verts"]
        area = polygon_area(verts)
        total_net_area += area

        # Find optimal rotation bounding box
        best_rot = 0.0
        best_w, best_h = 0.0, 0.0
        min_bbox_area = float('inf')

        for rot in item["allowed_rotations"]:
            poly = Polygon([(p.x, p.y) for p in verts])
            if rot != 0.0:
                poly = affinity.rotate(poly, rot, origin='center')
            minx, miny, maxx, maxy = poly.bounds
            w = maxx - minx
            h = maxy - miny
            if (w * h) < min_bbox_area:
                min_bbox_area = w * h
                best_rot = rot
                best_w = w
                best_h = h

        prepared_items.append({
            **item,
            "best_rot": best_rot,
            "width": best_w,
            "height": best_h,
            "net_area": area,
        })

    # Sort descending by height
    prepared_items.sort(key=lambda x: x["height"], reverse=True)

    # Shelf packing
    usable_width = fabric.bolt_width - (2 * margin)
    shelves: List[Dict] = []  # List of shelves: {y, height, current_x, items}
    placements: List[NestedPiecePlacement] = []

    current_shelf_y = margin

    for item in prepared_items:
        placed = False
        item_w = item["width"] + margin
        item_h = item["height"] + margin

        for shelf in shelves:
            if shelf["current_x"] + item_w <= usable_width and item_h <= shelf["height"] * 1.3:
                # Place in this shelf
                px = shelf["current_x"] + margin
                py = shelf["y"]
                shelf["current_x"] += item_w
                shelf["height"] = max(shelf["height"], item_h)

                # Transform vertices
                poly = Polygon([(p.x, p.y) for p in item["base_verts"]])
                if item["best_rot"] != 0.0:
                    poly = affinity.rotate(poly, item["best_rot"], origin='center')
                minx, miny, _, _ = poly.bounds
                poly = affinity.translate(poly, xoff=px - minx, yoff=py - miny)
                cut_pts = [Point2D(x=float(x), y=float(y)) for x, y in poly.exterior.coords[:-1]]

                placements.append(NestedPiecePlacement(
                    piece_id=item["piece_id"],
                    piece_name=item["piece_name"],
                    instance_index=item["instance_index"],
                    is_mirrored=item["is_mirrored"],
                    is_optional=item["is_optional"],
                    placed_x=round(px, 3),
                    placed_y=round(py, 3),
                    rotation_deg=item["best_rot"],
                    width=round(item["width"], 3),
                    height=round(item["height"], 3),
                    cut_vertices=cut_pts
                ))
                placed = True
                break

        if not placed:
            # Start new shelf
            new_shelf_y = current_shelf_y if not shelves else (shelves[-1]["y"] + shelves[-1]["height"])
            px = margin
            py = new_shelf_y

            shelves.append({
                "y": new_shelf_y,
                "height": item_h,
                "current_x": margin + item_w
            })

            poly = Polygon([(p.x, p.y) for p in item["base_verts"]])
            if item["best_rot"] != 0.0:
                poly = affinity.rotate(poly, item["best_rot"], origin='center')
            minx, miny, _, _ = poly.bounds
            poly = affinity.translate(poly, xoff=px - minx, yoff=py - miny)
            cut_pts = [Point2D(x=float(x), y=float(y)) for x, y in poly.exterior.coords[:-1]]

            placements.append(NestedPiecePlacement(
                piece_id=item["piece_id"],
                piece_name=item["piece_name"],
                instance_index=item["instance_index"],
                is_mirrored=item["is_mirrored"],
                is_optional=item["is_optional"],
                placed_x=round(px, 3),
                placed_y=round(py, 3),
                rotation_deg=item["best_rot"],
                width=round(item["width"], 3),
                height=round(item["height"], 3),
                cut_vertices=cut_pts
            ))

    total_cut_len = (shelves[-1]["y"] + shelves[-1]["height"] + margin) if shelves else 0.0
    total_cut_yards = total_cut_len / 36.0
    gross_area = fabric.bolt_width * total_cut_len
    utilization = (total_net_area / gross_area * 100.0) if gross_area > 0 else 0.0
    waste = max(0.0, 100.0 - utilization)

    return FabricNestingLayout(
        fabric_id=fabric.id,
        fabric_name=fabric.name,
        bolt_width=fabric.bolt_width,
        total_cut_length=round(total_cut_len, 2),
        total_cut_length_yards=round(total_cut_yards, 2),
        net_pattern_area_sq_in=round(total_net_area, 2),
        gross_fabric_area_sq_in=round(gross_area, 2),
        utilization_rate_percent=round(utilization, 1),
        waste_percent=round(waste, 1),
        placements=placements
    )


def nest_project(project: ProjectPattern, margin: float = 0.5) -> Dict[str, FabricNestingLayout]:
    """Generates nesting cutting layouts for all fabrics in the project."""
    layouts: Dict[str, FabricNestingLayout] = {}
    for fabric in project.fabrics:
        layout = nest_pieces_for_fabric(fabric, project.pieces, margin=margin)
        layouts[fabric.id] = layout
    return layouts
