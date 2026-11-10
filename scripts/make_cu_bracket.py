"""Patte de fixation des boîtiers (M01379, « CU-VFD Mounting plate 3 mm ») : DXF + plan de pose.

La pièce d'origine n'est dans aucun STEP officiel. Celle-ci est dessinée à partir
des cotes relevées dans les STEP (voir docs/pieces-acier.md) :

- les deux traverses basses avant (30×60, sens X) sont à 288 mm d'entraxe ;
- boîtier de commande : pieds M4 à 335 × 420 mm, donc à 23,5 mm À L'EXTÉRIEUR
  de l'axe des traverses ;
- boîtier VFD : pieds M4 à 242 × 145 mm, donc à 23,0 mm À L'INTÉRIEUR.

La patte se glisse entre le fond du boîtier et le pied en caoutchouc (trou M4),
passe sur la traverse et dépasse du boîtier dans le sens de la traverse, où deux
vis M5×12 la fixent dans la rainure du dessus.

Repère de la patte : a = le long de la traverse, positif vers l'extérieur du
boîtier ; b = en travers, positif vers l'axe de la traverse. Origine = trou M4.

Usage : .venv/bin/python scripts/make_cu_bracket.py
"""

from __future__ import annotations

import math
from pathlib import Path

import ezdxf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cad" / "steel" / "diy"
NAME = "CU_VFD_Mounting_plate_DIY_t3mm_x4"

# --- Cotes relevées ----------------------------------------------------------
RAIL_PITCH = 288.0          # entraxe des traverses basses avant (Y = -1262 et -974)
RAIL_W = 30.0
FOOT_D = 17.0               # pied caoutchouc M4
BOXES = {                   # pieds : (en travers des traverses, le long), demi-dépassement du boîtier
    "Boîtier de commande": {"feet": (335.0, 420.0), "body": (380.0, 453.0)},
    "Boîtier VFD": {"feet": (242.0, 145.0), "body": (275.0, 178.0)},
}

# --- Patte -------------------------------------------------------------------
A0, A1 = -10.0, 54.0        # 64 mm le long de la traverse
B0, B1 = -10.0, 35.0        # 45 mm en travers
RADIUS = 3.0
M4 = 4.5
SLOT_B = 23.25              # moyenne de 23,5 (commande) et 23,0 (VFD)
SLOT_LEN, SLOT_W = 9.0, 5.5  # lumière M5 : ±1,75 mm de réglage en travers
SLOTS_A = (27.0, 45.0)
BOX_END_A = 18.0            # le boîtier (capot compris) s'arrête à 18 mm du pied


def rounded_rect(x0, y0, x1, y1, r):
    k = math.tan(math.pi / 8)  # bulge d'un quart de cercle
    return [(x0 + r, y0, 0), (x1 - r, y0, k), (x1, y0 + r, 0), (x1, y1 - r, k),
            (x1 - r, y1, 0), (x0 + r, y1, k), (x0, y1 - r, 0), (x0, y0 + r, k)]


def slot(cx, cy, length, width):
    h, r = (length - width) / 2, width / 2
    return [(cx - r, cy - h, 0), (cx - r, cy + h, -1), (cx + r, cy + h, 0), (cx + r, cy - h, -1)]


def write_dxf(path: Path) -> None:
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    msp.add_lwpolyline(rounded_rect(A0, B0, A1, B1, RADIUS), format="xyb", close=True)
    msp.add_circle((0, 0), M4 / 2)
    for a in SLOTS_A:
        msp.add_lwpolyline(slot(a, SLOT_B, SLOT_LEN, SLOT_W), format="xyb", close=True)
    doc.saveas(path)


def check() -> None:
    for name, box in BOXES.items():
        offset = abs(box["feet"][0] - RAIL_PITCH) / 2
        assert abs(offset - SLOT_B) <= (SLOT_LEN - SLOT_W) / 2 - 1.0, name   # 1 mm de réserve
        # le pied touche le flanc de la traverse sans mordre dessus
        assert offset - FOOT_D / 2 - RAIL_W / 2 >= -0.6, name
        assert (box["body"][1] - box["feet"][1]) / 2 <= BOX_END_A, name
    head = 8.5 / 2                                   # tête de vis CHC M5
    assert SLOTS_A[0] - head - BOX_END_A >= 4.0      # place pour la tête et la clé
    assert A1 - SLOTS_A[1] - SLOT_W / 2 >= 6.0 and B1 - SLOT_B - SLOT_LEN / 2 >= 6.0
    assert SLOT_B + SLOT_LEN / 2 <= SLOT_B + RAIL_W / 2 and B1 <= SLOT_B + RAIL_W / 2


def preview(path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.4), dpi=130, gridspec_kw={"width_ratios": [1, 2.3]})

    # 1. La patte seule, cotée
    ax1.add_patch(FancyBboxPatch((A0 + RADIUS, B0 + RADIUS), A1 - A0 - 2 * RADIUS, B1 - B0 - 2 * RADIUS,
                                 boxstyle=f"round,pad={RADIUS}", fc="#cbd5e1", ec="black", lw=1.3))
    ax1.add_patch(Circle((0, 0), M4 / 2, fc="white", ec="black"))
    for a in SLOTS_A:
        ax1.add_patch(FancyBboxPatch((a - 0.01, SLOT_B - SLOT_LEN / 2 + SLOT_W / 2), 0.02, SLOT_LEN - SLOT_W,
                                     boxstyle=f"round,pad={SLOT_W / 2 - 0.01}", fc="white", ec="black"))
    ax1.axvline(BOX_END_A, color="#2563eb", ls="--", lw=1)
    ax1.text(BOX_END_A - 1, B0 - 3.5, "bord du boîtier", color="#2563eb", ha="right", fontsize=8)
    ax1.axhline(SLOT_B, color="#dc2626", ls="-.", lw=0.8)
    ax1.text(A0, SLOT_B + 1.2, "axe de la traverse", color="#dc2626", fontsize=8)
    ax1.annotate("Ø4,5 (pied M4)", (0, 0), (4, -6.5), fontsize=8, arrowprops={"arrowstyle": "-", "lw": 0.6})
    ax1.annotate("2 lumières 5,5 × 9 (M5)", (SLOTS_A[1], SLOT_B - 4.5), (22, 6), fontsize=8,
                 arrowprops={"arrowstyle": "-", "lw": 0.6})
    ax1.set_title(f"Patte {A1 - A0:.0f} × {B1 - B0:.0f} mm, acier 3 mm\n"
                  "lumières à 27 et 45 mm du trou M4 le long, 23,25 mm en travers", fontsize=10)
    ax1.set_xlim(A0 - 6, A1 + 6)
    ax1.set_ylim(B0 - 8, B1 + 6)
    ax1.set_aspect("equal")
    ax1.axis("off")

    # 2. Plan de pose, vue de dessus (les traverses courent horizontalement)
    for sign in (-1, 1):
        y = sign * RAIL_PITCH / 2
        ax2.add_patch(Rectangle((-620, y - RAIL_W / 2), 1240, RAIL_W, fc="#e5e7eb", ec="#6b7280"))
    centres = {"Boîtier de commande": -260.0, "Boîtier VFD": 300.0}
    for name, box in BOXES.items():
        cx = centres[name]
        across, along = box["feet"]
        w, h = box["body"][1], box["body"][0]
        ax2.add_patch(Rectangle((cx - w / 2, -h / 2), w, h, fc="#bfdbfe", ec="#1d4ed8", alpha=0.55, lw=1.2))
        ax2.text(cx, 0, f"{name}\npieds {across:.0f} × {along:.0f}", ha="center", va="center", fontsize=9)
        outward = 1 if across > RAIL_PITCH else -1      # pieds dehors ou dedans
        for sa in (-1, 1):
            for sb in (-1, 1):
                fx, fy = cx + sa * along / 2, sb * across / 2
                ax2.add_patch(Circle((fx, fy), FOOT_D / 2, fc="#111827", zorder=4))
                if sa * sb > 0:                           # 2 pattes en diagonale
                    da, db = sa, -sb * outward            # a vers l'extérieur, b vers la traverse
                    x0, x1 = sorted((fx + da * A0, fx + da * A1))
                    y0, y1 = sorted((fy + db * B0, fy + db * B1))
                    ax2.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#f59e0b", ec="black", zorder=3, alpha=0.9))
                    for a in SLOTS_A:
                        ax2.add_patch(Circle((fx + da * a, fy + db * SLOT_B), 3.2, fc="white", ec="black", zorder=5))
    ax2.set_title("Plan de pose, vue de dessus : traverses basses avant (entraxe 288 mm), "
                  "2 pattes en diagonale par boîtier", fontsize=10)
    ax2.set_xlim(-640, 640)
    ax2.set_ylim(-235, 235)
    ax2.set_aspect("equal")
    ax2.axis("off")
    fig.savefig(path, bbox_inches="tight")


def main() -> None:
    check()
    OUT.mkdir(parents=True, exist_ok=True)
    write_dxf(OUT / f"{NAME}.dxf")
    preview(OUT / "pattes-boitiers.png")
    cut = 2 * (A1 - A0 + B1 - B0) - 8 * RADIUS + 2 * math.pi * RADIUS + math.pi * M4 \
        + 2 * (2 * (SLOT_LEN - SLOT_W) + math.pi * SLOT_W)
    kg = (A1 - A0) * (B1 - B0) * 3 * 7.85e-6
    print(f"Patte {A1 - A0:.0f} x {B1 - B0:.0f} x 3 mm, {kg:.3f} kg, {cut / 1000:.2f} m de découpe, 3 perçages")


if __name__ == "__main__":
    main()
