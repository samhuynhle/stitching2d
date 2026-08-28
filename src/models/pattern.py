from enum import Enum
from typing import List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field


class Unit(str, Enum):
    INCHES = "in"
    MILLIMETERS = "mm"
    CENTIMETERS = "cm"


class Point2D(BaseModel):
    x: float
    y: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


class EdgeType(str, Enum):
    LINE = "line"
    BEZIER = "bezier"
    ARC = "arc"


class SeamType(str, Enum):
    STANDARD = "standard"
    FLAT_FELLED = "flat_felled"
    FRENCH = "french"
    HEM_FOLD = "hem_fold"
    ZIPPER = "zipper"
    BIAS_BOUND = "bias_bound"
    RAW_EDGE = "raw_edge"
    OVERLOCK = "overlock"


class Edge(BaseModel):
    id: str
    edge_type: EdgeType = EdgeType.LINE
    start: Point2D
    end: Point2D
    control_points: Optional[List[Point2D]] = None
    seam_allowance: Optional[float] = Field(None, description="Custom SA for this edge. If None, inherits piece default.")
    seam_type: SeamType = SeamType.STANDARD
    hem_depth: Optional[float] = Field(None, description="Additional fold depth if hem_fold")
    paired_to: Optional[str] = Field(None, description="Target piece_id:edge_id to validate join consistency")
    notches: List[float] = Field(default_factory=list, description="Arc distances along edge from start where notches are cut")


class Grainline(BaseModel):
    start_point: Point2D = Field(default_factory=lambda: Point2D(x=0, y=0))
    end_point: Point2D = Field(default_factory=lambda: Point2D(x=0, y=5))
    angle_deg: float = Field(0.0, description="Angle in degrees (0=straight grain, 90=cross, 45=bias)")
    directional: bool = Field(False, description="If True, fabric has directional nap/pile and cannot be rotated 180 deg")


class AttachmentType(str, Enum):
    WEBBING = "webbing"
    ZIPPER = "zipper"
    VELCRO = "velcro"
    SNAP_BUTTON = "snap_button"
    GROMMET = "grommet"
    D_RING = "d_ring"
    BUCKLE = "buckle"
    ELASTIC = "elastic"
    INTERFACING = "interfacing"
    BARTACK = "bartack"
    BOX_X = "box_x"
    LABEL = "label"


class Attachment(BaseModel):
    id: str
    name: str
    type: AttachmentType
    position: Point2D = Field(description="Anchor point on pattern piece")
    length: Optional[float] = Field(None, description="Length in project units (e.g. for webbing/zippers/velcro)")
    width: Optional[float] = Field(None, description="Width in project units (e.g. 1.0 in webbing)")
    angle_deg: float = Field(0.0, description="Orientation angle in degrees")
    layer: str = Field("exterior", description="exterior, interior, or sandwiched")
    notes: Optional[str] = None


class PatternPiece(BaseModel):
    id: str
    name: str
    category: str = Field("main_body", description="main_body, lining, pocket, gusset, trim, reinforcement")
    fabric_id: str
    quantity: int = Field(1, ge=1)
    mirror: bool = Field(False, description="Cut 1 normal + 1 mirrored if quantity > 1")
    default_seam_allowance: float = Field(0.5, ge=0.0, description="Default SA in project units")
    vertices: List[Point2D] = Field(..., min_length=3, description="Ordered closed perimeter vertices")
    edges: Optional[List[Edge]] = Field(None, description="Detailed edge definitions. If omitted, generated from vertices.")
    grainline: Optional[Grainline] = None
    attachments: List[Attachment] = Field(default_factory=list)
    notes: Optional[str] = None


class FabricMaterial(BaseModel):
    id: str
    name: str
    type: str = Field(..., description="e.g. 500D Cordura, X-Pac VX21, 210D Ripstop Nylon, Mesh")
    bolt_width: float = Field(60.0, gt=0.0, description="Usable roll width in project units (e.g. 60.0 in)")
    cost_per_yard: Optional[float] = None
    weight_oz_yd2: Optional[float] = None
    directional_nap: bool = Field(False, description="If True, all pieces must align in the same 0-degree grain direction")


class HardwareItem(BaseModel):
    id: str
    name: str
    type: str = Field(..., description="e.g. Side Release Buckle 1in, YKK #5 Slider, Cordlock")
    quantity: int = Field(1, ge=1)
    notes: Optional[str] = None


class ProjectPattern(BaseModel):
    id: str
    name: str
    version: str = "1.0.0"
    description: Optional[str] = None
    units: Unit = Unit.INCHES
    fabrics: List[FabricMaterial] = Field(default_factory=list)
    pieces: List[PatternPiece] = Field(default_factory=list)
    hardware: List[HardwareItem] = Field(default_factory=list)
    sewing_notes: List[str] = Field(default_factory=list)
