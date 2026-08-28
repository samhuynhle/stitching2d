from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel
from ..models.pattern import ProjectPattern, PatternPiece, Edge, SeamType
from .geometry import distance, build_edges_from_vertices


class SeamValidationResult(BaseModel):
    source_piece_id: str
    source_piece_name: str
    source_edge_id: str
    target_piece_id: str
    target_piece_name: str
    target_edge_id: str
    source_length: float
    target_length: float
    length_delta: float
    ease_ratio_percent: float
    status: str  # "MATCH", "EASED", "MISMATCH"
    message: str
    seam_allowance_compatible: bool


class SeamTopologyReport(BaseModel):
    total_seams_checked: int
    matched_seams: int
    eased_seams: int
    mismatches: int
    results: List[SeamValidationResult]
    unpaired_edges: List[str]


def calculate_edge_length(edge: Edge) -> float:
    """Calculates the physical length of an edge."""
    if edge.edge_type == "bezier" and edge.control_points:
        from .geometry import evaluate_bezier_cubic
        if len(edge.control_points) >= 2:
            pts = evaluate_bezier_cubic(edge.start, edge.control_points[0], edge.control_points[1], edge.end)
            return sum(distance(pts[i], pts[i+1]) for i in range(len(pts)-1))
    return distance(edge.start, edge.end)


def validate_project_seams(project: ProjectPattern, tolerance: float = 0.05) -> SeamTopologyReport:
    """
    Validates all paired seams across all pattern pieces in the project.
    Combines explicit paired_to definitions with intelligent geometric seam matching.
    """
    piece_map: Dict[str, PatternPiece] = {p.id: p for p in project.pieces}
    edge_map: Dict[str, Dict[str, Edge]] = {}

    for piece in project.pieces:
        edges = build_edges_from_vertices(piece)
        edge_map[piece.id] = {e.id: e for e in edges}

    results: List[SeamValidationResult] = []
    processed_pairs = set()
    paired_edge_keys = set()

    # 1. Process explicit pairings
    for piece_id, edges in edge_map.items():
        for edge_id, edge in edges.items():
            if not edge.paired_to:
                continue

            pair_key = tuple(sorted([f"{piece_id}:{edge_id}", edge.paired_to]))
            if pair_key in processed_pairs:
                continue
            processed_pairs.add(pair_key)
            paired_edge_keys.add(f"{piece_id}:{edge_id}")
            paired_edge_keys.add(edge.paired_to)

            try:
                target_piece_id, target_edge_id = edge.paired_to.split(":")
            except ValueError:
                continue

            target_piece = piece_map.get(target_piece_id)
            target_edge = edge_map.get(target_piece_id, {}).get(target_edge_id)
            if not target_piece or not target_edge:
                continue

            l_src = calculate_edge_length(edge)
            l_tgt = calculate_edge_length(target_edge)
            delta = abs(l_src - l_tgt)
            ease_pct = ((l_src - l_tgt) / l_tgt) * 100.0 if l_tgt > 0 else 0.0

            sa_src = edge.seam_allowance if edge.seam_allowance is not None else piece_map[piece_id].default_seam_allowance
            sa_tgt = target_edge.seam_allowance if target_edge.seam_allowance is not None else target_piece.default_seam_allowance
            sa_compat = abs(sa_src - sa_tgt) < 1e-4 or edge.seam_type in (SeamType.FLAT_FELLED, SeamType.FRENCH)

            if delta <= tolerance:
                status = "MATCH"
                msg = f"Clean match (Δ = {delta:.3f}\")"
            elif abs(ease_pct) <= 8.0:
                status = "EASED"
                msg = f"Intentional ease ({ease_pct:+.1f}%)"
            else:
                status = "MISMATCH"
                msg = f"Discrepancy (Δ = {delta:.3f}\", {ease_pct:+.1f}% ease)"

            results.append(
                SeamValidationResult(
                    source_piece_id=piece_id,
                    source_piece_name=piece_map[piece_id].name,
                    source_edge_id=edge_id,
                    target_piece_id=target_piece_id,
                    target_piece_name=target_piece.name,
                    target_edge_id=target_edge_id,
                    source_length=round(l_src, 3),
                    target_length=round(l_tgt, 3),
                    length_delta=round(delta, 3),
                    ease_ratio_percent=round(ease_pct, 1),
                    status=status,
                    message=msg,
                    seam_allowance_compatible=sa_compat
                )
            )

    # 2. Intelligent Auto-Detection for Unpaired Mating Edges within Same Fabric/Assembly
    unpaired_list = []
    for piece_id, edges in edge_map.items():
        for edge_id, edge in edges.items():
            key = f"{piece_id}:{edge_id}"
            if key not in paired_edge_keys:
                unpaired_list.append((piece_id, edge_id, edge))

    # Auto-match compatible edges across different pieces
    used_in_auto = set()
    for i in range(len(unpaired_list)):
        p1_id, e1_id, edge1 = unpaired_list[i]
        key1 = f"{p1_id}:{e1_id}"
        if key1 in used_in_auto:
            continue

        l1 = calculate_edge_length(edge1)
        best_match = None
        min_delta = float('inf')

        for j in range(len(unpaired_list)):
            if i == j:
                continue
            p2_id, e2_id, edge2 = unpaired_list[j]
            key2 = f"{p2_id}:{e2_id}"
            if key2 in used_in_auto or p1_id == p2_id:
                continue

            # Must share layer or compatible category
            p1 = piece_map[p1_id]
            p2 = piece_map[p2_id]
            if p1.fabric_id != p2.fabric_id and p1.category != "trim" and p2.category != "trim":
                continue

            l2 = calculate_edge_length(edge2)
            delta = abs(l1 - l2)

            if delta <= 0.15 and delta < min_delta:
                min_delta = delta
                best_match = (p2_id, e2_id, edge2, l2)

        if best_match:
            p2_id, e2_id, edge2, l2 = best_match
            key2 = f"{p2_id}:{e2_id}"
            used_in_auto.add(key1)
            used_in_auto.add(key2)

            delta = abs(l1 - l2)
            ease_pct = ((l1 - l2) / l2) * 100.0 if l2 > 0 else 0.0

            sa_src = edge1.seam_allowance if edge1.seam_allowance is not None else piece_map[p1_id].default_seam_allowance
            sa_tgt = edge2.seam_allowance if edge2.seam_allowance is not None else piece_map[p2_id].default_seam_allowance
            sa_compat = abs(sa_src - sa_tgt) < 1e-4

            status = "MATCH" if delta <= tolerance else ("EASED" if abs(ease_pct) <= 8.0 else "MISMATCH")
            msg = f"Auto-detected seam join (Δ = {delta:.3f}\")"

            results.append(
                SeamValidationResult(
                    source_piece_id=p1_id,
                    source_piece_name=piece_map[p1_id].name,
                    source_edge_id=e1_id,
                    target_piece_id=p2_id,
                    target_piece_name=piece_map[p2_id].name,
                    target_edge_id=e2_id,
                    source_length=round(l1, 3),
                    target_length=round(l2, 3),
                    length_delta=round(delta, 3),
                    ease_ratio_percent=round(ease_pct, 1),
                    status=status,
                    message=msg,
                    seam_allowance_compatible=sa_compat
                )
            )

    unpaired_final = [
        f"{p_id}:{e_id}"
        for p_id, e_id, _ in unpaired_list
        if f"{p_id}:{e_id}" not in used_in_auto and f"{p_id}:{e_id}" not in paired_edge_keys
    ]

    matched = sum(1 for r in results if r.status == "MATCH")
    eased = sum(1 for r in results if r.status == "EASED")
    mismatched = sum(1 for r in results if r.status == "MISMATCH")

    return SeamTopologyReport(
        total_seams_checked=len(results),
        matched_seams=matched,
        eased_seams=eased,
        mismatches=mismatched,
        results=results,
        unpaired_edges=unpaired_final
    )
