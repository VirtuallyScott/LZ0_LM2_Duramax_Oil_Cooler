#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FreeCAD Macro — Oil Filter Thread Adapter
==========================================
Chevrolet Duramax 3.0 LM2 / LZ0

Generates a 3-D solid of a billet thread adapter that converts the
1"-16 UNF oil filter boss on the Duramax 3.0 engine block to the
13/16"-16 UNF thread used by most universal sandwich-plate oil cooler
adapters, allowing any standard sandwich plate to be fitted without
custom-machining the block side.

Orientation (Z axis)
--------------------
  Z = 0        Bottom face — 1"-16 UNF male thread entry (screws into block)
  Z = Z1       Top of block thread / bottom face of hex collar (O-ring seating face)
  Z = Z2       Top of hex collar / bottom of sandwich-plate thread
  Z = Z3       Top face — 13/16"-16 UNF male thread exit

Usage
-----
  FreeCAD 0.21+:
    Macro ▸ Macros… ▸ Browse to this file ▸ Execute.
    — or —
    Paste into the FreeCAD Python console.

  Headless / scripted:
    freecadcmd Oil-Filter-Thread-Adapter.py

Output
------
  FreeCAD document "Oil_Filter_Thread_Adapter" containing one solid
  "Adapter_Body" with:
    • 1"-16 UNF male thread  (bottom, block side)
    • 1-1/2" AF hex collar   (wrench grip)
    • O-ring groove          (on hex seating face, Viton -112 c.s.)
    • 13/16"-16 UNF male thread  (top, sandwich-plate side)
    • 0.500" through-bore    (oil passage)
    • 45° lead chamfers on both thread entries

Material (annotated, not enforced by CAD)
-----------------------------------------
  6061-T6 billet aluminum
  Hard anodize or electroless nickel finish recommended

Thread references
-----------------
  ASME B1.1  Unified Inch Screw Threads (UN and UNR Thread Form)
  ASME B1.2  Gages and Gaging for Unified Inch Screw Threads
  Parker O-Ring Handbook ORD 5700 (groove dimension tables)
"""

import math
import FreeCAD
import Part


# ─────────────────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────────────────

def mm(inches: float) -> float:
    """Convert inches to millimetres (FreeCAD internal unit)."""
    return inches * 25.4


def vec(x: float, y: float, z: float) -> FreeCAD.Vector:
    return FreeCAD.Vector(x, y, z)


# ─────────────────────────────────────────────────────────────────────────────
# Specification — edit this section to resize the adapter
# ─────────────────────────────────────────────────────────────────────────────

# ── Block-side thread (bottom, male — screws into engine) ─────────────────────
BLOCK_MAJOR_IN = 1.0000      # 1"-16 UNF nominal major diameter
BLOCK_TPI      = 16          # threads per inch
BLOCK_LEN_IN   = 0.625       # engaged thread length (10 threads)

# ── Sandwich-plate thread (top, male — sandwich plate mounts on this) ─────────
SAND_MAJOR_IN  = 13 / 16     # 0.8125" — 13/16"-16 UNF nominal major diameter
SAND_TPI       = 16
SAND_LEN_IN    = 0.625       # engaged thread length (10 threads)

# ── Hex collar ────────────────────────────────────────────────────────────────
HEX_AF_IN      = 1.500       # across-flats — 1-1/2" socket / open-end wrench
HEX_HEIGHT_IN  = 0.375       # collar height

# ── Oil passage through-bore ──────────────────────────────────────────────────
BORE_DIA_IN    = 0.500       # ID — minimum restriction through the adapter

# ── O-ring groove (cut into bottom face of hex collar / block seating face) ───
# Dimensioned for a Parker / Trelleborg Viton -112 O-ring
#   Cross-section:  0.103" (2.616 mm)
#   ID:             1.049" (26.645 mm)
# Groove follows Parker ORD 5700 Table 3-1 static face-seal recommendations.
ORING_ID_IN    = 1.075       # groove inner diameter
ORING_WIDTH_IN = 0.118       # groove width   (1.14× O-ring c.s. — Parker rec.)
ORING_DEPTH_IN = 0.082       # groove depth   (0.80× O-ring c.s. — Parker rec.)

# ── Lead chamfer ──────────────────────────────────────────────────────────────
CHAMFER_DEG    = 45.0        # chamfer half-angle from thread axis


# ─────────────────────────────────────────────────────────────────────────────
# Thread calculations — ASME B1.1 Class 2A external UNF
# ─────────────────────────────────────────────────────────────────────────────

def unf_minor(major_in: float, tpi: int) -> float:
    """
    External (male) UNF minor diameter per ASME B1.1.

    Formula:  d_minor = d_major - 1.22687 / n
    where n = threads per inch.
    """
    return major_in - 1.22687 / tpi


def unf_pitch_dia(major_in: float, tpi: int) -> float:
    """External UNF pitch diameter per ASME B1.1."""
    return major_in - 0.64952 / tpi


BLOCK_PITCH_IN  = 1.0 / BLOCK_TPI          # 0.0625"
BLOCK_MINOR_IN  = unf_minor(BLOCK_MAJOR_IN, BLOCK_TPI)
BLOCK_PITCH_DIA = unf_pitch_dia(BLOCK_MAJOR_IN, BLOCK_TPI)

SAND_PITCH_IN   = 1.0 / SAND_TPI           # 0.0625"
SAND_MINOR_IN   = unf_minor(SAND_MAJOR_IN, SAND_TPI)
SAND_PITCH_DIA  = unf_pitch_dia(SAND_MAJOR_IN, SAND_TPI)


# ─────────────────────────────────────────────────────────────────────────────
# Z-stack (all in mm, Z=0 at bottom face)
# ─────────────────────────────────────────────────────────────────────────────

Z0 = 0.0
Z1 = mm(BLOCK_LEN_IN)                  # top of block thread / hex seating face
Z2 = Z1 + mm(HEX_HEIGHT_IN)            # top of hex collar
Z3 = Z2 + mm(SAND_LEN_IN)              # top of adapter (sandwich thread tip)
TOTAL_H = Z3


# ─────────────────────────────────────────────────────────────────────────────
# Thread solid — external (male) UNF
# ─────────────────────────────────────────────────────────────────────────────

def make_ext_thread(
    major_mm: float,
    minor_mm: float,
    pitch_mm: float,
    length_mm: float,
    z_start: float,
) -> Part.Shape:
    """
    Build an external (male) thread solid via helix sweep.

    Strategy
    --------
    1. Construct a helical spine at the major-diameter radius.
    2. Create a 60° isosceles triangle profile (one thread tooth) in the
       XZ plane at the helix start point.
    3. Sweep the profile along the spine with Frenet framing (profile
       stays normal to the helix tangent).
    4. Fuse the swept thread teeth to the minor-diameter core cylinder.

    Falls back to a plain major-diameter cylinder if the OCCT kernel
    cannot complete the sweep (geometry guard for degenerate cases).

    Parameters
    ----------
    major_mm  : thread major diameter (mm)
    minor_mm  : thread minor diameter (mm)
    pitch_mm  : axial pitch (mm)
    length_mm : total threaded length (mm)
    z_start   : Z coordinate of the thread start face (mm)

    Returns
    -------
    Part.Shape  solid representing the threaded section
    """
    tooth_h = (major_mm - minor_mm) / 2.0   # radial tooth height
    r       = major_mm / 2.0                # helix radius (at major dia)

    # ── Spine — helix at major-diameter radius ──
    helix = Part.makeHelix(pitch_mm, length_mm, r)
    helix.translate(vec(0.0, 0.0, z_start))

    # ── Profile — 60° V-tooth cross-section ──
    # Placed in the XZ plane at x = r (where the helix begins at angle 0).
    # The tooth points radially inward toward the minor diameter.
    p0 = vec(r,            0.0, 0.0)           # root (major radius, thread start)
    p1 = vec(r - tooth_h,  0.0, pitch_mm / 2)  # tip  (minor radius, mid-pitch)
    p2 = vec(r,            0.0, pitch_mm)       # root (major radius, thread end)
    profile = Part.Wire(Part.makePolygon([p0, p1, p2, p0]))

    # ── Minor-diameter core cylinder ──
    core = Part.makeCylinder(
        minor_mm / 2.0, length_mm,
        vec(0.0, 0.0, z_start), vec(0.0, 0.0, 1.0),
    )

    # ── Sweep and fuse ──
    try:
        swept = Part.Wire(helix).makePipeShell([profile], True, True)
        solid = core.fuse(swept).removeSplitter()
    except Exception as err:
        FreeCAD.Console.PrintWarning(
            f"[Oil-Filter-Thread-Adapter] Thread sweep failed — "
            f"using cosmetic cylinder fallback. Detail: {err}\n"
        )
        # Cosmetic fallback: plain major-diameter cylinder.
        # Visually represents the thread envelope; accurate for all
        # diameters and lengths used in drawings and cross-sections.
        solid = Part.makeCylinder(
            r, length_mm,
            vec(0.0, 0.0, z_start), vec(0.0, 0.0, 1.0),
        )

    return solid


# ─────────────────────────────────────────────────────────────────────────────
# Hex collar
# ─────────────────────────────────────────────────────────────────────────────

def make_hex_collar(af_mm: float, height_mm: float, z_start: float) -> Part.Shape:
    """
    Regular hexagonal prism with flat sides aligned parallel to the X axis.

    Parameters
    ----------
    af_mm      : across-flats dimension (mm)
    height_mm  : extrusion height (mm)
    z_start    : Z coordinate of the collar bottom face (mm)
    """
    inradius      = af_mm / 2.0
    circumradius  = inradius / math.cos(math.pi / 6.0)

    pts = [
        vec(
            circumradius * math.cos(math.radians(30.0 + i * 60.0)),
            circumradius * math.sin(math.radians(30.0 + i * 60.0)),
            z_start,
        )
        for i in range(6)
    ]
    pts.append(pts[0])  # close the polygon

    face = Part.Face(Part.Wire(Part.makePolygon(pts)))
    return face.extrude(vec(0.0, 0.0, height_mm))


# ─────────────────────────────────────────────────────────────────────────────
# Chamfer helper
# ─────────────────────────────────────────────────────────────────────────────

def apply_thread_entry_chamfer(
    body: Part.Shape,
    major_mm: float,
    bore_mm: float,
    z_tip: float,
    pointing_up: bool,
    angle_deg: float = 45.0,
) -> Part.Shape:
    """
    Apply a conical lead chamfer to a thread entry or exit.

    The chamfer tapers from the bore diameter at the thread tip face to
    the full major diameter over a depth determined by the chamfer angle.

    Parameters
    ----------
    body        : the Part.Shape to modify
    major_mm    : thread major diameter (mm)
    bore_mm     : through-bore diameter (mm)
    z_tip       : Z coordinate of the thread-end face (the chamfered face)
    pointing_up : True → chamfer is at the TOP face (z_tip is the top);
                  False → chamfer is at the BOTTOM face (z_tip is Z=0)
    angle_deg   : chamfer half-angle from the thread axis (default 45°)
    """
    r_maj     = major_mm / 2.0
    r_bore    = bore_mm  / 2.0
    cham_tan  = math.tan(math.radians(angle_deg))
    cham_h    = (r_maj - r_bore) / cham_tan          # axial chamfer height

    if pointing_up:
        # Chamfer at the TOP: cone narrows from major radius → bore radius
        # as Z increases toward z_tip.
        z_cone_base = z_tip - cham_h
        cone = Part.makeCone(r_maj, r_bore, cham_h, vec(0, 0, z_cone_base), vec(0, 0, 1))
    else:
        # Chamfer at the BOTTOM: cone widens from bore radius → major radius
        # as Z increases away from z_tip.
        z_cone_base = z_tip
        cone = Part.makeCone(r_bore, r_maj, cham_h, vec(0, 0, z_cone_base), vec(0, 0, 1))

    # Cut the ring-shaped region outside the cone surface (between cone and
    # a large bounding cylinder) from the body.
    margin     = r_maj + 2.0   # slightly larger than the thread OD
    outer_cyl  = Part.makeCylinder(margin, cham_h, vec(0, 0, z_cone_base), vec(0, 0, 1))

    try:
        cut_volume = outer_cyl.cut(cone)
        body = body.cut(cut_volume)
    except Exception as err:
        FreeCAD.Console.PrintWarning(
            f"[Oil-Filter-Thread-Adapter] Chamfer cut failed — skipped. ({err})\n"
        )

    return body


# ─────────────────────────────────────────────────────────────────────────────
# Full adapter build
# ─────────────────────────────────────────────────────────────────────────────

def build() -> Part.Shape:
    """Assemble the complete adapter solid and return it."""

    # ── 1. Block-side thread section (bottom, 1"-16 UNF male) ────────────────
    block_thread = make_ext_thread(
        major_mm  = mm(BLOCK_MAJOR_IN),
        minor_mm  = mm(BLOCK_MINOR_IN),
        pitch_mm  = mm(BLOCK_PITCH_IN),
        length_mm = mm(BLOCK_LEN_IN),
        z_start   = Z0,
    )

    # ── 2. Hex collar ─────────────────────────────────────────────────────────
    hex_collar = make_hex_collar(
        af_mm     = mm(HEX_AF_IN),
        height_mm = mm(HEX_HEIGHT_IN),
        z_start   = Z1,
    )

    # ── 3. Sandwich-plate thread section (top, 13/16"-16 UNF male) ────────────
    sand_thread = make_ext_thread(
        major_mm  = mm(SAND_MAJOR_IN),
        minor_mm  = mm(SAND_MINOR_IN),
        pitch_mm  = mm(SAND_PITCH_IN),
        length_mm = mm(SAND_LEN_IN),
        z_start   = Z2,
    )

    # ── 4. Fuse all three sections ────────────────────────────────────────────
    body = block_thread.fuse(hex_collar).fuse(sand_thread)
    body = body.removeSplitter()

    # ── 5. Through-bore ───────────────────────────────────────────────────────
    # 1 mm overrun on each end ensures a clean cut through both faces.
    bore = Part.makeCylinder(
        mm(BORE_DIA_IN) / 2.0,
        TOTAL_H + 2.0,
        vec(0.0, 0.0, -1.0), vec(0.0, 0.0, 1.0),
    )
    body = body.cut(bore)

    # ── 6. O-ring groove ─────────────────────────────────────────────────────
    # Annular groove cut into the bottom face of the hex collar (the face
    # that seats against the engine block oil-filter boss flat).
    # Groove extends upward from Z1 into the hex collar body.
    og_inner_r = mm(ORING_ID_IN)  / 2.0
    og_outer_r = og_inner_r + mm(ORING_WIDTH_IN)

    oring_outer = Part.makeCylinder(
        og_outer_r, mm(ORING_DEPTH_IN), vec(0, 0, Z1), vec(0, 0, 1))
    oring_inner = Part.makeCylinder(
        og_inner_r, mm(ORING_DEPTH_IN), vec(0, 0, Z1), vec(0, 0, 1))

    oring_groove = oring_outer.cut(oring_inner)
    body = body.cut(oring_groove)

    # ── 7. Lead chamfers on both thread entries ───────────────────────────────
    bore_mm = mm(BORE_DIA_IN)

    # Bottom (block-side entry): 45° taper — helps thread onto block boss
    body = apply_thread_entry_chamfer(
        body, mm(BLOCK_MAJOR_IN), bore_mm,
        z_tip=Z0, pointing_up=False, angle_deg=CHAMFER_DEG,
    )

    # Top (sandwich-plate entry): 45° taper — helps sandwich plate thread on
    body = apply_thread_entry_chamfer(
        body, mm(SAND_MAJOR_IN), bore_mm,
        z_tip=Z3, pointing_up=True, angle_deg=CHAMFER_DEG,
    )

    return body


# ─────────────────────────────────────────────────────────────────────────────
# FreeCAD document
# ─────────────────────────────────────────────────────────────────────────────

doc   = FreeCAD.newDocument("Oil_Filter_Thread_Adapter")
shape = build()

feat        = doc.addObject("Part::Feature", "Adapter_Body")
feat.Shape  = shape
feat.Label  = "Oil Filter Adapter — 1\"-16 UNF to 13/16\"-16 UNF"

doc.recompute()

# Fit isometric view — safe no-op when running headless (freecadcmd)
try:
    import FreeCADGui
    FreeCADGui.activeDocument().activeView().viewIsometric()
    FreeCADGui.SendMsgToActiveView("ViewFit")
except Exception:
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Build summary — printed to the FreeCAD report pane / console
# ─────────────────────────────────────────────────────────────────────────────

_LINE = "=" * 62

FreeCAD.Console.PrintMessage(f"""
{_LINE}
  Oil Filter Thread Adapter — Build Summary
{_LINE}
  BLOCK SIDE (bottom)     1"-16 UNF male  →  engine block boss
  ─────────────────────────────────────────────────────────────
  Major diameter          {BLOCK_MAJOR_IN:.4f} in  /  {mm(BLOCK_MAJOR_IN):.3f} mm
  Pitch diameter          {BLOCK_PITCH_DIA:.4f} in  /  {mm(BLOCK_PITCH_DIA):.3f} mm
  Minor diameter          {BLOCK_MINOR_IN:.4f} in  /  {mm(BLOCK_MINOR_IN):.3f} mm
  Pitch                   1/{BLOCK_TPI} in  /  {mm(BLOCK_PITCH_IN):.4f} mm
  Engaged length          {BLOCK_LEN_IN:.3f} in  /  {mm(BLOCK_LEN_IN):.3f} mm
{_LINE}
  HEX COLLAR
  ─────────────────────────────────────────────────────────────
  Across-flats (AF)       {HEX_AF_IN:.3f} in  /  {mm(HEX_AF_IN):.3f} mm   (1-1/2" socket)
  Height                  {HEX_HEIGHT_IN:.3f} in  /  {mm(HEX_HEIGHT_IN):.3f} mm
  O-ring groove ID        {ORING_ID_IN:.3f} in  /  {mm(ORING_ID_IN):.3f} mm
  O-ring groove width     {ORING_WIDTH_IN:.3f} in  /  {mm(ORING_WIDTH_IN):.3f} mm
  O-ring groove depth     {ORING_DEPTH_IN:.3f} in  /  {mm(ORING_DEPTH_IN):.3f} mm
  O-ring spec             Viton -112  (0.103" cross-section)
{_LINE}
  OIL PASSAGE BORE
  ─────────────────────────────────────────────────────────────
  Bore diameter           {BORE_DIA_IN:.3f} in  /  {mm(BORE_DIA_IN):.3f} mm
{_LINE}
  SANDWICH SIDE (top)     13/16"-16 UNF male  →  sandwich plate
  ─────────────────────────────────────────────────────────────
  Major diameter          {SAND_MAJOR_IN:.4f} in  /  {mm(SAND_MAJOR_IN):.3f} mm
  Pitch diameter          {SAND_PITCH_DIA:.4f} in  /  {mm(SAND_PITCH_DIA):.3f} mm
  Minor diameter          {SAND_MINOR_IN:.4f} in  /  {mm(SAND_MINOR_IN):.3f} mm
  Pitch                   1/{SAND_TPI} in  /  {mm(SAND_PITCH_IN):.4f} mm
  Engaged length          {SAND_LEN_IN:.3f} in  /  {mm(SAND_LEN_IN):.3f} mm
{_LINE}
  OVERALL HEIGHT          {TOTAL_H / 25.4:.4f} in  /  {TOTAL_H:.3f} mm
  MATERIAL (spec)         6061-T6 billet aluminum
  FINISH (rec.)           hard anodize or electroless nickel
  CHAMFER ANGLE           {CHAMFER_DEG:.0f}° both thread entries
{_LINE}
""")
