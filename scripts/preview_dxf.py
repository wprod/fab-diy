"""Render every DXF under a folder into one contact sheet PNG, to eyeball the cuts.

Usage:
    .venv/bin/python scripts/preview_dxf.py cad/steel cad/steel/preview.png
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Arc, Circle  # noqa: E402


def draw(ax, path: Path) -> None:
    for e in ezdxf.readfile(path).modelspace():
        kind = e.dxftype()
        if kind == "LINE":
            s, t = e.dxf.start, e.dxf.end
            ax.plot([s.x, t.x], [s.y, t.y], "k-", lw=0.7)
        elif kind == "CIRCLE":
            c = e.dxf.center
            ax.add_patch(Circle((c.x, c.y), e.dxf.radius, fill=False, lw=0.7))
        elif kind == "ARC":
            c, r = e.dxf.center, e.dxf.radius
            ax.add_patch(Arc((c.x, c.y), 2 * r, 2 * r, theta1=e.dxf.start_angle,
                             theta2=e.dxf.end_angle, lw=0.7))
        elif kind == "LWPOLYLINE":
            pts = list(e.get_points("xy"))
            ax.plot([p[0] for p in pts], [p[1] for p in pts], "k-", lw=0.7)
    ax.autoscale_view()
    ax.set_aspect("equal", adjustable="datalim")


def main(folder: Path, out: Path) -> None:
    files = sorted(folder.rglob("*.dxf"))
    cols = 4
    rows = math.ceil(len(files) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3.4), squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for ax, f in zip(axes.flat, files):
        draw(ax, f)
        ax.set_title(f.stem.replace("_", " "), fontsize=8)
    fig.savefig(out, dpi=110, facecolor="white", bbox_inches="tight")
    print(f"{len(files)} DXF -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
