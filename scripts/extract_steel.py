"""Extract the fabricated (steel/sheet) parts from Mekanika STEP assemblies.

Every unique part in the assembly tree is measured and sorted:
  - flat   : plate of constant thickness  -> DXF of the cut profile + STEP
  - bent   : sheet metal with folds       -> STEP (sheet-metal shops unfold it, or
             use FreeCAD SheetMetal / Fusion "Flat pattern")
  - solid  : machined or thick part       -> STEP

Purchased parts (profiles, rails, motors, screws...) are skipped by name.
Identical geometries are merged and their quantities summed.

Usage:
    .venv/bin/python scripts/extract_steel.py "cad/source/FAB V1.0.stp" cad/steel/fab
"""

from __future__ import annotations

import csv
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import ezdxf
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepGProp import BRepGProp
from OCP.collections import Sequence_TDF_Label as TDF_LabelSequence  # OCP >= 8
from OCP.GCPnts import GCPnts_QuasiUniformDeflection
from OCP.GeomAbs import GeomAbs_Circle, GeomAbs_Line, GeomAbs_Plane
from OCP.GProp import GProp_GProps
from OCP.gp import gp_Ax3, gp_Dir, gp_Pln, gp_Pnt, gp_Trsf, gp_Vec
from OCP.IFSelect import IFSelect_RetDone
from OCP.Message import Message, Message_Gravity
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_REVERSED, TopAbs_VERTEX
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Shape
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ShapeTool

# Bought-in parts, matched on the part's display name.
PURCHASED = re.compile(
    r"profile|rail|block|slide|rack|nema|motor|stepper|spindle(?! plate)|bearing|ring|"
    r"ball|screw|nut(?! offset)|washer|rondelle|spacer|din9|iso ?7|m\d+x\d+|bump|"
    r"rubber|foot(?! plate)|coupler|pulley|pinion(?! drive)|spring|bague|bronze|sensor|"
    r"chain|tray|cable|sfu|sfs|angle bracket|_br_|hgh20|hgw20|9\d{4}a\d{3}|22004|"
    r"canti|insert|raspberry|rpi4|planetcnc|smps|driver|pcb|fan|connector|plug|"
    r"switch|relay|inverter|breaker|terminal|klemme|header|optocoupler|photocoupler|"
    r"gx12|speakon|c14|usb|hdmi|sd card|wire|klein|mstb|tb5|dg301|rj21|dip_|"
    r"electronic|fastener|adapter|converter|pwm",
    re.IGNORECASE,
)
# Fabricated parts whose names would otherwise trip PURCHASED ("Rack & Pinion drive
# plate", "Limit switches support", "Bearing Support Offset Plate"...). Wins over it.
FABRICATED = re.compile(
    r"plate|gantry|gusset|triangulation|limit switches support|cable chain support|"
    r"nut offset|x_motor|x_bearing|enclosure (base|cover)|control unit (base|cover)",
    re.IGNORECASE,
)
# Assembly groups that only hold bought-in parts (the control-unit STEPs use them).
BOUGHT_GROUP = re.compile(r"electronic components|electronics|fasteners( \(\d+\))?", re.IGNORECASE)
# Leaf names that say nothing: fall back to the parent assembly's name.
GENERIC = re.compile(
    r"\d+|compound|d[ée]faut|body\d*|solid\d*|component\d*( \(\d+\))?|base(_\d+)?|"
    r"cover|top|unnamed|mettalic part.*",
    re.IGNORECASE,
)
FLAT_TOL = 0.2  # mm: a plate is flat if its extent along the normal == its thickness
MAX_SHEET = 6.0  # mm: thicker than this and not flat -> machined "solid" part


@dataclass
class Part:
    name: str
    path: list[str]
    shape: TopoDS_Shape
    qty: int = 0
    kind: str = ""
    thickness: float = 0.0
    size: tuple[float, float] = (0.0, 0.0)
    files: list[str] = field(default_factory=list)
    aliases: set[str] = field(default_factory=set)


def quiet_occt() -> None:
    printers = Message.DefaultMessenger_s().Printers()
    for i in range(1, printers.Length() + 1):
        printers.Value(i).SetTraceLevel(Message_Gravity.Message_Fail)


def label_name(label: TDF_Label) -> str:
    attr = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), attr):
        return attr.Get().ToExtString()
    return "unnamed"


def display_name(path: list[str]) -> str:
    leaf = path[-1]
    if GENERIC.fullmatch(leaf.strip()) and len(path) > 1:
        return f"{path[-2]} - {leaf}"
    return leaf


def read_assembly(path: Path) -> list[Part]:
    """Walk the XCAF tree and count the instances of every leaf part."""
    doc = TDocStd_Document(TCollection_ExtendedString("doc"))
    reader = STEPCAFControl_Reader()
    reader.SetNameMode(True)
    if reader.ReadFile(str(path)) != IFSelect_RetDone:
        sys.exit(f"cannot read {path}")
    reader.Transfer(doc)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())

    parts: dict[tuple[str, int], Part] = {}

    def walk(label: TDF_Label, trail: list[str]) -> None:
        trail = trail + [label_name(label)]
        if XCAFDoc_ShapeTool.IsAssembly_s(label):
            comps = TDF_LabelSequence()
            XCAFDoc_ShapeTool.GetComponents_s(label, comps, False)
            for i in range(1, comps.Length() + 1):
                ref = TDF_Label()
                XCAFDoc_ShapeTool.GetReferredShape_s(comps.Value(i), ref)
                walk(ref, trail)
            return
        key = (trail[-1], label.Tag())
        if key not in parts:
            shape = XCAFDoc_ShapeTool.GetShape_s(label)
            parts[key] = Part(display_name(trail), trail, shape)
        parts[key].qty += 1

    roots = TDF_LabelSequence()
    tool.GetFreeShapes(roots)
    for i in range(1, roots.Length() + 1):
        walk(roots.Value(i), [])
    return list(parts.values())


def planar_faces(shape: TopoDS_Shape):
    """Yield (area, outward normal, point on plane, face) for each planar face."""
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face(exp.Current())
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == GeomAbs_Plane:
            ax = surf.Plane().Axis()
            n = gp_Vec(ax.Direction())
            if face.Orientation() == TopAbs_REVERSED:
                n.Reverse()
            props = GProp_GProps()
            BRepGProp.SurfaceProperties_s(face, props)
            yield props.Mass(), n, ax.Location(), face
        exp.Next()


def extent_along(shape: TopoDS_Shape, origin: gp_Pnt, n: gp_Vec) -> tuple[float, float]:
    lo, hi = math.inf, -math.inf
    exp = TopExp_Explorer(shape, TopAbs_VERTEX)
    while exp.More():
        p = BRep_Tool.Pnt_s(TopoDS.Vertex(exp.Current()))
        d = gp_Vec(origin, p).Dot(n)
        lo, hi = min(lo, d), max(hi, d)
        exp.Next()
    return lo, hi


def geometry_key(part: Part) -> tuple:
    """Fingerprint used to merge identical parts (mirrors of flat plates included)."""
    vol, area = GProp_GProps(), GProp_GProps()
    BRepGProp.VolumeProperties_s(part.shape, vol)
    BRepGProp.SurfaceProperties_s(part.shape, area)
    key = (part.kind, part.thickness, round(vol.Mass(), -1), round(area.Mass(), -1))
    if part.kind != "flat":  # a bent mirror part is a different part
        key += (re.sub(r"\s*\(\d+\)", "", part.name),)
    return key


def longest_line_dir(face) -> gp_Dir | None:
    best, best_len = None, 0.0
    exp = TopExp_Explorer(face, TopAbs_EDGE)
    while exp.More():
        c = BRepAdaptor_Curve(TopoDS.Edge(exp.Current()))
        if c.GetType() == GeomAbs_Line:
            length = c.Value(c.FirstParameter()).Distance(c.Value(c.LastParameter()))
            if length > best_len:
                best, best_len = c.Line().Direction(), length
        exp.Next()
    return best


def classify(part: Part):
    faces = sorted(planar_faces(part.shape), key=lambda f: -f[0])
    if not faces:
        part.kind = "solid"
        return None
    _, n, origin, main_face = faces[0]
    lo, hi = extent_along(part.shape, origin, n)
    extent = hi - lo
    # Thickness = distance to the largest face pointing the opposite way.
    backs = [f for f in faces[1:] if f[1].Dot(n) < -0.999]
    thickness = abs(gp_Vec(origin, backs[0][2]).Dot(n)) if backs else extent
    if abs(extent - thickness) <= FLAT_TOL:
        part.kind = "flat"
    elif thickness <= MAX_SHEET:
        part.kind = "bent"
    else:
        part.kind = "solid"
    part.thickness = round(thickness, 2)
    return n, origin, main_face, lo, hi


def plate_frame(n: gp_Vec, origin: gp_Pnt, main_face, lo: float, hi: float) -> gp_Trsf:
    """Transform taking the plate's mid-plane to global XY, long edge along X."""
    mid = origin.Translated(n.Multiplied((lo + hi) / 2))
    xdir = longest_line_dir(main_face)
    nd = gp_Dir(n)
    ax = gp_Ax3(mid, nd, xdir) if xdir else gp_Ax3(mid, nd)
    t = gp_Trsf()
    t.SetTransformation(ax)
    return t


def write_dxf(part: Part, frame: gp_Trsf, n: gp_Vec, out: Path) -> None:
    # Cut the solid at mid-thickness: gives the through-profile, ignoring chamfers.
    plane_origin = gp_Pnt(0, 0, 0).Transformed(frame.Inverted())
    section = BRepAlgoAPI_Section(part.shape, gp_Pln(plane_origin, gp_Dir(n)))
    section.Build()
    flat = BRepBuilderAPI_Transform(section.Shape(), frame, True).Shape()

    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    xs, ys = [], []
    exp = TopExp_Explorer(flat, TopAbs_EDGE)
    while exp.More():
        c = BRepAdaptor_Curve(TopoDS.Edge(exp.Current()))
        u0, u1 = c.FirstParameter(), c.LastParameter()
        p0, p1 = c.Value(u0), c.Value(u1)
        if c.GetType() == GeomAbs_Line:
            msp.add_line((p0.X(), p0.Y()), (p1.X(), p1.Y()))
            pts = [p0, p1]
        elif c.GetType() == GeomAbs_Circle:
            circ = c.Circle()
            ctr, r = circ.Location(), circ.Radius()
            if abs((u1 - u0) - 2 * math.pi) < 1e-6:
                msp.add_circle((ctr.X(), ctr.Y()), r)
                pts = [gp_Pnt(ctr.X() - r, ctr.Y() - r, 0), gp_Pnt(ctr.X() + r, ctr.Y() + r, 0)]
            else:
                a0 = math.degrees(math.atan2(p0.Y() - ctr.Y(), p0.X() - ctr.X()))
                a1 = math.degrees(math.atan2(p1.Y() - ctr.Y(), p1.X() - ctr.X()))
                if circ.Axis().Direction().Z() < 0:
                    a0, a1 = a1, a0
                msp.add_arc((ctr.X(), ctr.Y()), r, a0, a1)
                pts = [p0, p1]
        else:
            disc = GCPnts_QuasiUniformDeflection(c, 0.01)
            pts = [disc.Value(i) for i in range(1, disc.NbPoints() + 1)]
            msp.add_lwpolyline([(p.X(), p.Y()) for p in pts])
        xs += [p.X() for p in pts]
        ys += [p.Y() for p in pts]
        exp.Next()
    if xs:
        part.size = (round(max(xs) - min(xs), 1), round(max(ys) - min(ys), 1))
    doc.saveas(out)


def write_step(shape: TopoDS_Shape, out: Path) -> None:
    w = STEPControl_Writer()
    w.Transfer(shape, STEPControl_AsIs)
    w.Write(str(out))


def slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")


def main(src: Path, out_dir: Path) -> None:
    quiet_occt()
    # Match the display name only: a parent like "Motor & Pinion Assembly" also
    # holds fabricated plates, so parent names must not exclude their children.
    candidates = [
        p for p in read_assembly(src)
        if (FABRICATED.search(p.name) or not PURCHASED.search(p.name))
        and not any(BOUGHT_GROUP.fullmatch(n) for n in p.path[1:-1])
    ]

    merged: dict[tuple, Part] = {}
    for part in candidates:
        part.geo = classify(part)
        key = geometry_key(part)
        if key in merged:
            merged[key].qty += part.qty
            merged[key].aliases.add(part.name)
        else:
            part.aliases.add(part.name)
            merged[key] = part

    for d in ("dxf", "step"):
        (out_dir / d).mkdir(parents=True, exist_ok=True)
    rows = sorted(merged.values(), key=lambda p: (p.kind, p.name.lower()))
    for part in rows:
        part.name = re.sub(r"\s*\(\d+\)", "", min(part.aliases, key=len))
        stem = f"{slug(part.name)}_t{part.thickness:g}mm_x{part.qty}"
        if part.kind == "flat" and part.geo:
            n, origin, face, lo, hi = part.geo
            write_dxf(part, plate_frame(n, origin, face, lo, hi), n, out_dir / "dxf" / f"{stem}.dxf")
            part.files.append(f"dxf/{stem}.dxf")
        write_step(part.shape, out_dir / "step" / f"{stem}.step")
        part.files.append(f"step/{stem}.step")
        size = f"{part.size[0]:>7} x {part.size[1]:<7}" if part.kind == "flat" else " " * 17
        print(f"{part.kind:5} t={part.thickness:5.2f} x{part.qty:<3} {size} {part.name}")

    with open(out_dir / "parts.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "qty", "kind", "thickness_mm", "flat_size_mm", "assembly_path", "files"])
        for p in rows:
            size = f"{p.size[0]} x {p.size[1]}" if p.kind == "flat" else ""
            w.writerow([p.name, p.qty, p.kind, p.thickness, size, " > ".join(p.path[1:-1]), " ".join(p.files)])
    print(dict(Counter(p.kind for p in rows)), f"-> {out_dir}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
