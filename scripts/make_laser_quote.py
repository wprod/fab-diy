"""Dossier de demande de devis pour la découpe laser : liste des pièces + zip des fichiers.

Lit les `parts.csv` écrits par extract_steel.py et ajoute les pièces redessinées
(cad/steel/diy). Écrit dans cad/steel/devis/ :
- liste-decoupe.csv : une ligne par pièce (fichier, épaisseur, quantité, plis, reprises) ;
- fab-diy-decoupe-laser.zip : les DXF des plaques, les STEP des tôles pliées, la liste.

Usage : python3 scripts/make_laser_quote.py
"""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEEL = ROOT / "cad" / "steel"
OUT = STEEL / "devis"

# Boîtier VFD : reporté tant que la Makita sert de broche (bom/chiffrage/lot-K-cablage.csv).
ASSEMBLIES = ["fab", "fab-cu"]
QTY = {"Triangulation v6": 14}  # 14 goussets (STEP), la nomenclature en compte 12
# Reprises après découpe, par début de nom de pièce (relevées dans docs/pieces-acier.md).
REWORK = {
    "Fab XL - Z_plate": "8 trous Ø5,04 à tarauder M6",
    "Gantry_V2": "1 trou Ø10,2 à tarauder M12",
    "Rack & Pinion drive plate": "4 trous Ø4,3 à tarauder M5 ; découper 2 pièces identiques (une se retourne)",
    "Foot Plate 3060": "trou central à tarauder M12",
    "Gantry back plate": "logo découpé, vu en miroir dans le DXF",
    "Spindle plate": "percée pour une broche Ø80 ; trous du support Makita Ø65 à percer à la main",
    "Fab Control Unit": "tôle pliée : le développé est à calculer par le découpeur ; écrous à sertir M3 à poser",
    "Cable chain support": "tôle pliée, 1 pli",
}
EXTRA: list[dict] = []  # la patte de boîtier redessinée (cad/steel/diy) est facultative : hors devis


def parts() -> list[dict]:
    rows = []
    for asm in ASSEMBLIES:
        with open(STEEL / asm / "parts.csv", newline="") as fh:
            for p in csv.DictReader(fh):
                files = p["files"].split()
                want = ".dxf" if p["kind"] == "flat" else ".step"
                rel = next(f for f in files if f.endswith(want))
                rework = next((v for k, v in REWORK.items() if p["name"].startswith(k)), "")
                rows.append({"name": p["name"], "qty": QTY.get(p["name"], int(p["qty"])), "kind": p["kind"],
                             "thickness_mm": float(p["thickness_mm"]), "flat_size_mm": p["flat_size_mm"],
                             "file": STEEL / asm / rel, "rework": rework})
    return rows + EXTRA


def main() -> None:
    rows = sorted(parts(), key=lambda r: (-r["thickness_mm"], r["kind"], r["name"]))
    OUT.mkdir(parents=True, exist_ok=True)
    listing = OUT / "liste-decoupe.csv"
    with open(listing, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fichier", "piece", "matiere", "epaisseur_mm", "quantite", "type", "dimensions_mm", "reprises"])
        for r in rows:
            assert r["file"].exists(), r["file"]
            w.writerow([r["file"].name, r["name"], "acier S235", f"{r['thickness_mm']:g}", r["qty"],
                        "plaque (DXF)" if r["kind"] == "flat" else "tôle pliée (STEP)",
                        r["flat_size_mm"], r["rework"]])
    with zipfile.ZipFile(OUT / "fab-diy-decoupe-laser.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(listing, listing.name)
        for r in rows:
            z.write(r["file"], f"{r['thickness_mm']:g}mm/{r['file'].name}")
    by_t: dict[float, list[int]] = {}
    for r in rows:
        by_t.setdefault(r["thickness_mm"], [0, 0])
        by_t[r["thickness_mm"]][0] += 1
        by_t[r["thickness_mm"]][1] += r["qty"]
    for t, (refs, n) in sorted(by_t.items(), reverse=True):
        print(f"{t:g} mm : {refs} références, {n} pièces")
    print(f"Total : {len(rows)} références, {sum(r['qty'] for r in rows)} pièces -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
