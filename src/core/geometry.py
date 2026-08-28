import math
from typing import List, Tuple, Optional, Dict
import numpy as np
from shapely.geometry import Polygon, LineString, Point
from shapely import affinity

from ..models.pattern import Point2D, Edge, EdgeType, PatternPiece


def distance(p1: Point2D, p2: Point2D) -> float:
    return math.hypot(p2.x - p1.x, p2.y - p1.y)


def evaluate_bezier_cubic(p0: Point2D, p1: Point2D, p2: Point2D, p3: Point2D, num_samples: int = 20) -> List[Point2D]:
    """Evaluates cubic Bezier curve points for t in [0, 1]."""
    points: List[Point2D] = []
    for t in np.linspace(0.0, 1.0, num_samples):
        x = (1 - t)**3 * p0.x + 3 * (1 - t)**2 * t * p1.x + 3 * (1 - t) * t**2 * p2.x + t**3 * p3.x
        y = (1 - t)**3 * p0.y + 3 * (1 - t)**2 * t * p1.y + 3 * (1 - t) * t**2 * p2.y + t**3 * p3.y
        points.append(Point2D(x=float(x), y=float(y)))
    return points


def polygon_area(vertices: List[Point2D]) -> float:
    """Calculates polygon area using the Shoelace formula."""
    if len(vertices) < 3:
        return 0.0
    poly = Polygon([(p.x, p.y) for p in vertices])
    return abs(poly.area)


def polygon_perimeter(vertices: List[Point2D]) -> float:
    """Calculates the total perimeter length of a closed polygon."""
    if len(vertices) < 2:
        return 0.0
    total = 0.0
    for i in range(len(vertices)):
        total += distance(vertices[i], vertices[(i + 1) % len(vertices)])
    return total


def polygon_bounds(vertices: List[Point2D]) -> Tuple[float, float, float, float]:
    """Returns (min_x, min_y, max_x, max_y)."""
    xs = [p.x for p in vertices]
    ys = [p.y for p in vertices]
    return (min(xs), min(ys), max(xs), max(ys))


def polygon_centroid(vertices: List[Point2D]) -> Point2D:
    """Calculates the centroid (center of mass) of a polygon."""
    poly = Polygon([(p.x, p.y) for p in vertices])
    c = poly.centroid
    return Point2D(x=float(c.x), y=float(c.y))


def is_clockwise(vertices: List[Point2D]) -> bool:
    """Determines if the vertices are oriented clockwise."""
    s = 0.0
    n = len(vertices)
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        s += (p2.x - p1.x) * (p2.y + p1.y)
    return s > 0


def ensure_counter_clockwise(vertices: List[Point2D]) -> List[Point2D]:
    """Standardizes polygon vertices to CCW orientation for reliable outward normal calculation."""
    if is_clockwise(vertices):
        return list(reversed(vertices))
    return list(vertices)


def compute_outward_offset(
    vertices: List[Point2D],
    edge_allowances: Optional[List[float]] = None,
    default_allowance: float = 0.5,
    mitre_limit: float = 2.5
) -> List[Point2D]:
    """
    Computes outward offset polygon (Cut Line) from the base sew line.
    Supports variable per-edge seam allowances or uniform expansion.
    """
    if len(vertices) < 3:
        return vertices

    # Standardize to CCW
    ccw_verts = ensure_counter_clockwise(vertices)
    n = len(ccw_verts)

    if edge_allowances is None or len(edge_allowances) != n:
        allowances = [default_allowance] * n
    else:
        allowances = edge_allowances

    # If all allowances are equal, use Shapely's robust buffer
    if all(abs(a - allowances[0]) < 1e-5 for a in allowances):
        dist = allowances[0]
        if dist <= 0:
            return ccw_verts
        poly = Polygon([(p.x, p.y) for p in ccw_verts])
        buffered = poly.buffer(dist, join_style=2, mitre_limit=mitre_limit)  # 2 = MITRE
        if buffered.geom_type == 'Polygon':
            coords = list(buffered.exterior.coords)[:-1]
            return [Point2D(x=float(x), y=float(y)) for x, y in coords]

    # Variable edge offset calculation
    offset_lines = []
    for i in range(n):
        p1 = ccw_verts[i]
        p2 = ccw_verts[(i + 1) % n]
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.hypot(dx, dy)
        if length < 1e-6:
            continue

        # In CCW, outward normal is (dy / L, -dx / L)
        nx = dy / length
        ny = -dx / length
        sa = allowances[i]

        o1 = (p1.x + nx * sa, p1.y + ny * sa)
        o2 = (p2.x + nx * sa, p2.y + ny * sa)
        offset_lines.append((o1, o2))

    # Intersect adjacent offset lines
    new_vertices: List[Point2D] = []
    num_lines = len(offset_lines)
    for i in range(num_lines):
        line1 = offset_lines[(i - 1) % num_lines]
        line2 = offset_lines[i]

        pt = intersect_infinite_lines(line1[0], line1[1], line2[0], line2[1])
        if pt is not None:
            # Check miter limit
            orig_p = ccw_verts[i]
            dist_to_orig = math.hypot(pt[0] - orig_p.x, pt[1] - orig_p.y)
            max_allowed_dist = (allowances[(i - 1) % num_lines] + allowances[i]) * mitre_limit
            if dist_to_orig > max_allowed_dist:
                # Clamp / bevel
                dir_x = (pt[0] - orig_p.x) / dist_to_orig
                dir_y = (pt[1] - orig_p.y) / dist_to_orig
                pt = (orig_p.x + dir_x * max_allowed_dist, orig_p.y + dir_y * max_allowed_dist)
            new_vertices.append(Point2D(x=float(pt[0]), y=float(pt[1])))
        else:
            new_vertices.append(Point2D(x=float(line2[0][0]), y=float(line2[0][1])))

    return new_vertices


def intersect_infinite_lines(
    p1: Tuple[float, float], p2: Tuple[float, float],
    p3: Tuple[float, float], p4: Tuple[float, float]
) -> Optional[Tuple[float, float]]:
    """Calculates intersection point between two infinite 2D lines."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    ix = x1 + t * (x2 - x1)
    iy = y1 + t * (y2 - y1)
    return (ix, iy)


def build_edges_from_vertices(piece: PatternPiece) -> List[Edge]:
    """Constructs default Edge objects from pattern piece vertices if not explicitly provided."""
    if piece.edges and len(piece.edges) == len(piece.vertices):
        return piece.edges

    edges: List[Edge] = []
    n = len(piece.vertices)
    for i in range(n):
        start = piece.vertices[i]
        end = piece.vertices[(i + 1) % n]
        edges.append(
            Edge(
                id=f"{piece.id}_edge_{i+1}",
                edge_type=EdgeType.LINE,
                start=start,
                end=end,
                seam_allowance=piece.default_seam_allowance
            )
        )
    return edges
