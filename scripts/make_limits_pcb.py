"""Carte des fins de course de la Fab : Gerber + perçage + aperçu.

La carte d'origine (M00714) n'est publiée que sous forme de schéma
(upstream/fab/docs/PCB-limits.qet). Elle est passive : 6 embases XLR 3 broches
soudées, un bornier d'alimentation 24 V et un bornier de 4 sorties. Les deux
capteurs X et les deux capteurs Y1 (PNP, normalement fermés) sont mis en série :
la sortie du premier alimente le second.

Ce script redessine la carte à partir du schéma et de l'entraxe des perçages
relevé dans la tôle du boîtier (cad/steel/fab-cu), puis vérifie les isolements.

Repère : vue de l'EXTÉRIEUR du boîtier (face avant de la carte = côté embases),
u vers la droite, v vers le bas, origine sur l'axe de l'embase en haut à gauche.

Usage :
    python3 scripts/make_limits_pcb.py            # Gerber + perçage + zip
    .venv/bin/python scripts/make_limits_pcb.py   # idem + aperçu PNG (matplotlib)
"""

from __future__ import annotations

import math
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cad" / "pcb-fins-de-course"
NAME = "fab-fins-de-course"

# --- Géométrie -------------------------------------------------------------
PITCH = 27.0                      # entraxe des embases, relevé dans la tôle (Ø22,1)
EDGE = (-7.5, -8.0, 92.0, 43.0)   # u0, v0, u1, v1 : carte de 99,5 × 51 mm
TRACK = 0.8
CLEARANCE = 0.5                   # isolement mini vérifié entre deux équipotentielles
EDGE_MARGIN = 1.0

# Embases : nom, colonne, rangée. Vue de l'extérieur : X, Y1, Z, Y2 en haut.
XLR = [("XA", "X", 0, 0), ("Y1A", "Y1", 1, 0), ("Z", "Z", 2, 0), ("Y2", "Y2", 3, 0),
       ("XB", "X", 0, 1), ("Y1B", "Y1", 1, 1)]
# Empreinte Neutrik NC3FAV (bibliothèque KiCad Connector_Audio), ramenée à l'axe.
# Vue de face, loquet en haut : 2 à gauche, 1 à droite, 3 en bas. G = contact de
# masse des variantes NC3FAV2 (trou isolé, pour que les deux variantes se montent).
XLR_PINS = {"2": (-3.81, 0.0, 3.4, 1.6), "1": (3.81, 0.0, 3.4, 1.6),
            "3": (0.0, 4.45, 2.9, 1.2), "G": (8.25, 10.16, 2.9, 1.2)}
OUT_PADS = [(44.0 + 3.5 * i, 36.0) for i in range(4)]     # bornier 4 pôles, pas 3,5
PWR_PADS = {"+": (72.11, 36.0), "-": (77.19, 36.0)}        # bornier 2 pôles, pas 5,08

pads: list[tuple[float, float, float, float, str]] = []    # u, v, Ø pastille, Ø trou, net
tracks: dict[str, list[tuple[tuple[float, float], tuple[float, float], str]]] = {"F": [], "B": []}
pin: dict[tuple[str, str], tuple[float, float]] = {}


def centre(col: int, row: int) -> tuple[float, float]:
    return col * PITCH, row * PITCH


def route(layer: str, net: str, *pts: tuple[float, float]) -> None:
    for a, b in zip(pts, pts[1:]):
        tracks[layer].append((a, b, net))


def build() -> None:
    # Équipotentielles des broches (schéma : 1 = sortie capteur, 2 = 0 V, 3 = alimentation)
    nets = {("XA", "1"): "X_SERIE", ("XB", "3"): "X_SERIE", ("XB", "1"): "OUT1",
            ("Y1A", "1"): "Y1_SERIE", ("Y1B", "3"): "Y1_SERIE", ("Y1B", "1"): "OUT2",
            ("Z", "1"): "OUT3", ("Y2", "1"): "OUT4"}
    for ref, _, col, row in XLR:
        cx, cy = centre(col, row)
        for p, (dx, dy, dia, drill) in XLR_PINS.items():
            net = nets.get((ref, p)) or {"2": "GND", "3": "+24V", "G": f"NC_{ref}"}[p]
            pin[(ref, p)] = (cx + dx, cy + dy)
            pads.append((cx + dx, cy + dy, dia, drill, net))
    for i, (u, v) in enumerate(OUT_PADS):
        pads.append((u, v, 2.2, 1.2, f"OUT{i + 1}"))
    pads.append((*PWR_PADS["+"], 2.6, 1.3, "+24V"))
    pads.append((*PWR_PADS["-"], 2.6, 1.3, "GND"))

    # 0 V, face arrière : barre en haut, descentes vers la rangée du bas et le bornier
    route("B", "GND", (pin[("XA", "2")][0], -5.0), (pin[("Y2", "2")][0], -5.0))
    for ref in ("XA", "Y1A", "Z", "Y2"):
        u, v = pin[(ref, "2")]
        route("B", "GND", (u, -5.0), (u, v))
    route("B", "GND", pin[("XA", "2")], pin[("XB", "2")])
    route("B", "GND", pin[("Y1A", "2")], pin[("Y1B", "2")])
    route("B", "GND", pin[("Y2", "2")], PWR_PADS["-"])

    # +24 V, face avant : barre sous la rangée du haut (sous les trous G)
    for ref in ("XA", "Y1A", "Z", "Y2"):
        u, v = pin[(ref, "3")]
        route("F", "+24V", (u, v), (u, 13.5))
    route("F", "+24V", (pin[("XA", "3")][0], 13.5), (pin[("Y2", "3")][0], 13.5))
    route("F", "+24V", (PWR_PADS["+"][0], 13.5), PWR_PADS["+"])

    # Mise en série : sortie du capteur du haut -> alimentation du capteur du bas
    for top, bottom, net in (("XA", "XB", "X_SERIE"), ("Y1A", "Y1B", "Y1_SERIE")):
        (u1, v1), (u3, v3) = pin[(top, "1")], pin[(bottom, "3")]
        route("B", net, (u1, v1), (u1, 18.0), (u3, 18.0 + (u1 - u3)), (u3, v3))

    # Sorties vers le bornier 1 à 4
    u, v = pin[("XB", "1")]
    route("B", "OUT1", (u, v), (u, 40.3), (OUT_PADS[0][0], 40.3), OUT_PADS[0])
    u, v = pin[("Y1B", "1")]
    route("F", "OUT2", (u, v), (u, 31.0), (OUT_PADS[1][0], 31.0), OUT_PADS[1])
    u, v = pin[("Z", "1")]
    route("B", "OUT3", (u, v), (u, 26.0), (OUT_PADS[2][0], 26.0 + (u - OUT_PADS[2][0])), OUT_PADS[2])
    u, v = pin[("Y2", "1")]
    route("F", "OUT4", (u, v), (u, 40.0), (OUT_PADS[3][0], 40.0), OUT_PADS[3])


# --- Vérifications ---------------------------------------------------------
def seg_point(a, b, p) -> float:
    (ax, ay), (bx, by), (px, py) = a, b, p
    dx, dy = bx - ax, by - ay
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def seg_seg(a, b, c, d) -> float:
    def ccw(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    if ccw(a, b, c) * ccw(a, b, d) < 0 and ccw(c, d, a) * ccw(c, d, b) < 0:
        return 0.0
    return min(seg_point(a, b, c), seg_point(a, b, d), seg_point(c, d, a), seg_point(c, d, b))


def check() -> float:
    """Isolement mini entre équipotentielles, continuité de chaque net, marge au bord."""
    worst = 99.0
    for layer in "FB":
        segs = tracks[layer]
        for i, (a, b, n1) in enumerate(segs):
            for c, d, n2 in segs[i + 1:]:
                if n1 != n2:
                    worst = min(worst, seg_seg(a, b, c, d) - TRACK)
            for u, v, dia, _, n2 in pads:
                if n1 != n2:
                    worst = min(worst, seg_point(a, b, (u, v)) - TRACK / 2 - dia / 2)
    for i, (u, v, dia, _, n1) in enumerate(pads):
        for u2, v2, dia2, _, n2 in pads[i + 1:]:
            if n1 != n2:
                worst = min(worst, math.hypot(u - u2, v - v2) - dia / 2 - dia2 / 2)
    assert worst >= CLEARANCE, f"isolement {worst:.2f} mm < {CLEARANCE}"

    u0, v0, u1, v1 = EDGE
    for u, v, dia, _, _ in pads:
        assert min(u - u0, u1 - u, v - v0, v1 - v) - dia / 2 >= EDGE_MARGIN, f"pastille trop près du bord ({u}, {v})"
    for layer in "FB":
        for a, b, _ in tracks[layer]:
            for u, v in (a, b):
                assert min(u - u0, u1 - u, v - v0, v1 - v) - TRACK / 2 >= EDGE_MARGIN

    # Continuité : toutes les pastilles d'un net doivent être reliées par ses pistes
    # (les pastilles traversantes relient les deux faces).
    by_net: dict[str, list] = {}
    for u, v, *_, net in pads:
        by_net.setdefault(net, []).append((round(u, 3), round(v, 3)))
    for net, pts in by_net.items():
        if net.startswith("NC_"):
            continue
        parent: dict = {}

        def find(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                x = parent[x]
            return x
        for layer in "FB":
            for a, b, n in tracks[layer]:
                if n == net:
                    parent[find((round(a[0], 3), round(a[1], 3)))] = find((round(b[0], 3), round(b[1], 3)))
        # un bout de piste posé sur une autre piste du même net (jonction en T)
        nodes = list(parent)
        for p in nodes:
            for layer in "FB":
                for a, b, n in tracks[layer]:
                    if n == net and seg_point(a, b, p) < 1e-6:
                        parent[find(p)] = find((round(a[0], 3), round(a[1], 3)))
        assert len({find(p) for p in pts}) == 1, f"net {net} non relié"
    return worst


# --- Sorties ---------------------------------------------------------------
GLYPHS = {
    "X": [[(0, 0), (4, 6)], [(0, 6), (4, 0)]],
    "Y": [[(0, 6), (2, 3), (4, 6)], [(2, 3), (2, 0)]],
    "Z": [[(0, 6), (4, 6), (0, 0), (4, 0)]],
    "V": [[(0, 6), (2, 0), (4, 6)]],
    "0": [[(1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)]],
    "1": [[(1, 5), (2, 6), (2, 0)], [(1, 0), (3, 0)]],
    "2": [[(0, 5), (1, 6), (3, 6), (4, 5), (4, 4), (0, 0), (4, 0)]],
    "3": [[(0, 6), (4, 6), (2, 3.5), (3, 3.5), (4, 2.5), (4, 1), (3, 0), (1, 0), (0, 1)]],
    "4": [[(3, 0), (3, 6), (0, 2), (4, 2)]],
    "+": [[(0, 3), (4, 3)], [(2, 1), (2, 5)]],
    "-": [[(0, 3), (4, 3)]],
}


def text(s: str, u: float, v: float, h: float, mirror: bool) -> list:
    """Segments d'un texte centré en (u, v). mirror=True pour la face arrière."""
    k = h / 6.0
    width = len(s) * 5 * k - k
    segs = []
    for i, ch in enumerate(s):
        for line in GLYPHS[ch]:
            pts = []
            for gx, gy in line:
                x = -width / 2 + (i * 5 + gx) * k
                pts.append((u + (-x if mirror else x), v + h / 2 - gy * k))
            segs += list(zip(pts, pts[1:]))
    return segs


def silk(side: str) -> list:
    mirror = side == "B"
    segs = []
    for _, label, col, row in XLR:
        cx, cy = centre(col, row)
        segs += text(label, cx, cy - 4.5 if side == "F" else cy + 9.0, 2.6, mirror)
    for i, (u, v) in enumerate(OUT_PADS):
        segs += text(str(i + 1), u, v - 3.0, 1.8, mirror)
    for label, (u, v) in PWR_PADS.items():
        segs += text(label, u, v - 3.0, 1.8, mirror)
    segs += text("24V", 74.65, 29.0, 1.8, mirror)
    return segs


def gx(u: float) -> float:
    return u - EDGE[0]


def gy(v: float) -> float:
    return EDGE[3] - v


def gerber(path: Path, function: str, draws: list, flashes: list) -> None:
    """draws : (a, b, largeur) ; flashes : (u, v, diamètre)."""
    sizes = sorted({round(w, 3) for *_, w in draws} | {round(d, 3) for *_, d in flashes})
    code = {s: 10 + i for i, s in enumerate(sizes)}
    fmt = lambda x: f"{round(x * 1e6):d}"
    out = ["%TF.GenerationSoftware,fab-diy,make_limits_pcb.py*%", f"%TF.FileFunction,{function}*%",
           "%FSLAX46Y46*%", "%MOMM*%", "%LPD*%"]
    out += [f"%ADD{c}C,{s:.3f}*%" for s, c in code.items()]
    out.append("G01*")
    for s in sizes:
        out.append(f"D{code[s]}*")
        for a, b, w in draws:
            if round(w, 3) == s:
                out.append(f"X{fmt(gx(a[0]))}Y{fmt(gy(a[1]))}D02*")
                out.append(f"X{fmt(gx(b[0]))}Y{fmt(gy(b[1]))}D01*")
        for u, v, d in flashes:
            if round(d, 3) == s:
                out.append(f"X{fmt(gx(u))}Y{fmt(gy(v))}D03*")
    out.append("M02*")
    path.write_text("\n".join(out) + "\n")


def drill(path: Path) -> None:
    sizes = sorted({p[3] for p in pads})
    out = ["M48", "; DRILL file, plated through holes", "FMAT,2", "METRIC,TZ"]
    out += [f"T{i + 1}C{s:.3f}" for i, s in enumerate(sizes)]
    out += ["%", "G90", "G05"]
    for i, s in enumerate(sizes):
        out.append(f"T{i + 1}")
        out += [f"X{gx(u):.3f}Y{gy(v):.3f}" for u, v, _, d, _ in pads if d == s]
    out += ["T0", "M30"]
    path.write_text("\n".join(out) + "\n")


def zip_write(z: zipfile.ZipFile, path: Path, name: str) -> None:
    """Ajoute un fichier avec une date fixe, pour que le zip soit identique d'une exécution à l'autre."""
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    z.writestr(info, path.read_bytes())


def preview(path: Path) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    fig, ax = plt.subplots(figsize=(13, 7.2), dpi=130)
    u0, v0, u1, v1 = EDGE
    ax.add_patch(plt.Rectangle((u0, v0), u1 - u0, v1 - v0, fc="#14532d", ec="black", lw=1.2))
    for _, label, col, row in XLR:
        cx, cy = centre(col, row)
        ax.add_patch(plt.Circle((cx, cy), 11.05, fc="none", ec="#d1d5db", lw=0.8, ls="--"))
        for dx, dy in ((-9.9, -9.9), (9.9, 9.9)):
            ax.add_patch(plt.Circle((cx + dx, cy + dy), 1.6, fc="none", ec="#d1d5db", lw=0.8, ls="--"))
    colors = {"B": "#60a5fa", "F": "#f87171"}
    for layer in "BF":
        for a, b, _ in tracks[layer]:
            ax.plot([a[0], b[0]], [a[1], b[1]], color=colors[layer], lw=4.2, solid_capstyle="round", alpha=0.9)
    for u, v, dia, d, net in pads:
        ax.add_patch(plt.Circle((u, v), dia / 2, fc="#fbbf24", ec="none", zorder=5))
        ax.add_patch(plt.Circle((u, v), d / 2, fc="#111827", ec="none", zorder=6))
    for a, b in silk("F"):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="white", lw=1.1, zorder=7)
    ax.plot([], [], color=colors["F"], lw=4, label="Cuivre face avant (côté embases)")
    ax.plot([], [], color=colors["B"], lw=4, label="Cuivre face arrière (côté borniers)")
    ax.plot([], [], color="#d1d5db", lw=0.8, ls="--", label="Perçages de la tôle (Ø22,1 et Ø3,2)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, -0.04), ncol=3, frameon=False, fontsize=9)
    ax.set_title("Carte des fins de course, vue de l'extérieur du boîtier "
                 f"({u1 - u0:.1f} × {v1 - v0:.0f} mm)", fontsize=11)
    ax.set_xlim(u0 - 3, u1 + 3)
    ax.set_ylim(v1 + 3, v0 - 3)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, bbox_inches="tight")
    return True


def main() -> None:
    build()
    worst = check()
    OUT.mkdir(parents=True, exist_ok=True)
    u0, v0, u1, v1 = EDGE
    pad_flash = [(u, v, dia) for u, v, dia, _, _ in pads]
    files = []
    for side, tag in (("F", "Top"), ("B", "Bot")):
        f = OUT / f"{NAME}-{side}_Cu.gbr"
        gerber(f, f"Copper,L{1 if side == 'F' else 2},{tag}", [(a, b, TRACK) for a, b, _ in tracks[side]], pad_flash)
        files.append(f)
        f = OUT / f"{NAME}-{side}_Mask.gbr"
        gerber(f, f"Soldermask,{tag}", [], [(u, v, dia + 0.1) for u, v, dia in pad_flash])
        files.append(f)
        f = OUT / f"{NAME}-{side}_SilkS.gbr"
        gerber(f, f"Legend,{tag}", [(a, b, 0.2) for a, b in silk(side)], [])
        files.append(f)
    corners = [(u0, v0), (u1, v0), (u1, v1), (u0, v1), (u0, v0)]
    f = OUT / f"{NAME}-Edge_Cuts.gbr"
    gerber(f, "Profile,NP", [(a, b, 0.1) for a, b in zip(corners, corners[1:])], [])
    files.append(f)
    f = OUT / f"{NAME}-PTH.drl"
    drill(f)
    files.append(f)
    with zipfile.ZipFile(OUT / f"{NAME}-gerber.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            zip_write(z, f, f.name)
    done = preview(OUT / "apercu.png")
    print(f"Carte {u1 - u0:.1f} x {v1 - v0:.1f} mm, {len(pads)} trous, isolement mini {worst:.2f} mm")
    print(f"{len(files)} fichiers + zip dans {OUT.relative_to(ROOT)}" + ("" if done else " (aperçu non généré : matplotlib absent)"))


if __name__ == "__main__":
    main()
