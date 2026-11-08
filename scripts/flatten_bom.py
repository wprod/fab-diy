"""Flatten Mekanika's nested ERP BOMs into one DIY shopping list.

The upstream CSVs are an Odoo "exploded" export: one row per (component, parent),
`level` giving the depth, and quantities ALREADY multiplied by the parents
(e.g. 3x "FAB - Nema34 Motor" -> 3x "Nema34 Stepper Motor", not 9). Only leaves
are real parts; kits and bags are containers. This script keeps the leaves,
sums identical references and adds a category, a sourcing type and empty
supplier/price columns to fill in.

Usage:
    python3 scripts/flatten_bom.py            # writes bom/fab-diy-bom.csv
"""

from __future__ import annotations

import csv
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream" / "fab" / "bom"
SOURCES = ["FAB V1.0.csv", "VFD-CU V1.2.csv"]  # FAB already contains the FAB-CU tree
OUT = ROOT / "bom" / "fab-diy-bom.csv"

# Not in the upstream BOM: sold with the pack, needed to cut anything.
EXTRA = [
    ("Broche / Spindle", "", "Broche 2,2 kW refroidie air, ER20, 6000-24000 tr/min, 220 V", 1,
     "acheter", "Hors BOM upstream : vendue avec le pack. Doit correspondre au variateur 220 V."),
    ("Broche / Spindle", "", "Jeu de pinces ER20 (1-13 mm)", 1, "acheter", "Hors BOM upstream."),
    ("Broche / Spindle", "", "Support de broche Ø80 mm", 1, "acheter",
     "A verifier dans le STEP (Spindle plate) : diametre et entraxe des trous."),
    ("Pieces acier (a fabriquer)", "", "Spindle plate 8 mm (plaque porte-broche)", 1,
     "fabriquer (laser/pliage)",
     "Hors BOM upstream (vendue avec la broche). DXF : cad/steel/fab/dxf/Spindle_plate_t8mm_x1.dxf"),
]

# First matching rule wins: (category, sourcing type, regex)
RULES = [
    ("Pieces acier (a fabriquer)", "fabriquer (laser/pliage)", r"steels? parts|mounting plate"),
    ("Gabarits de montage", "fabriquer (decoupe)", r"mounting gauge|pmma"),
    ("Impression 3D", "imprimer 3D", r"3d print"),
    ("Structure alu", "acheter (coupe + taraudage)", r"alu profile"),
    ("Moteurs & electronique", "acheter",
     r"nema|motor driver|smps|controller|license|raspberry|optocoupler|pwm|microsd|"
     r"pcb|terminal block|xlr 3 pole|converter|fan|inverter|relay|usb key"),
    ("Guidage & transmission", "acheter",
     r"linear (rail|block)|ballscrew|\brack\b|pinion|pulley|belt|bearing|ff12|fk12|"
     r"nut housing|motor coupler|offset spacer|spacer -|spring|brush|v-slot"),
    ("Capteurs & securite", "acheter", r"inductive sensor pnp|probe z|emergency stop|circuit breaker"),
    ("Cablage & connectique", "acheter",
     r"cable(?! (tie|chain|tray|trunking|holder|cover))|xlr|gx12|usb|hdmi|rj45|micro-fit|"
     r"wago|ferrule|fuse|c14|rocker|banana|ring terminal|spade|power distribution|speakon"),
    ("Gestion des cables", "acheter",
     r"cable (tie|chain|tray|trunking|holder|cover)|cantilever|varibox"),
    ("Visserie & fixations", "acheter",
     r"screw|nut|washer|spacer|bracket|foot|end connection plate|rubber"),
]

FIELDS = ["categorie", "ref_mekanika", "designation", "quantite", "sourcing",
          "fournisseur", "produit", "lien", "prix_unitaire_ttc_eur", "quantite_achat",
          "total_ttc_eur", "confiance", "statut", "notes"]


def classify(name: str) -> tuple[str, str]:
    for category, sourcing, pattern in RULES:
        if re.search(pattern, name, re.IGNORECASE):
            return category, sourcing
    return "Divers", "acheter"


def leaves(path: Path):
    """Yield (ref, name, qty) for every leaf; quantities are already exploded."""
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("has_child_bom", "False") != "True" and int(row["level"]) > 0:
                yield (row["component_reference"], row["component_name"].strip(),
                       float(row["component_quantity"]))


def main() -> None:
    items: OrderedDict[str, dict] = OrderedDict()
    for name in SOURCES:
        for ref, designation, qty in leaves(UPSTREAM / name):
            if ref in items:
                items[ref]["quantite"] += qty
                continue
            category, sourcing = classify(designation)
            items[ref] = {"categorie": category, "ref_mekanika": ref,
                          "designation": designation, "quantite": qty, "sourcing": sourcing}

    rows = list(items.values())
    for category, ref, designation, qty, sourcing, notes in EXTRA:
        rows.append({"categorie": category, "ref_mekanika": ref, "designation": designation,
                     "quantite": qty, "sourcing": sourcing, "notes": notes})

    order = [r[0] for r in RULES] + ["Broche / Spindle", "Divers"]
    rows.sort(key=lambda r: (order.index(r["categorie"]), r["designation"].lower()))
    for r in rows:
        q = r["quantite"]
        r["quantite"] = int(q) if float(q).is_integer() else round(q, 2)
        r.setdefault("statut", "a sourcer")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    counts: OrderedDict[str, int] = OrderedDict()
    for r in rows:
        counts[r["categorie"]] = counts.get(r["categorie"], 0) + 1
    for category, n in counts.items():
        print(f"{n:4}  {category}")
    print(f"{len(rows):4}  lignes -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
