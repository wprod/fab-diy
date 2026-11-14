"""Listes de commande par fournisseur, à partir de bom/fab-diy-bom.csv.

Écrit bom/commandes/<fournisseur>.csv (une ligne par article à acheter, port compris)
et bom/commandes/README.md (récapitulatif trié par montant).

Usage : python3 scripts/make_orders.py   (après scripts/price_bom.py)
"""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOM = ROOT / "bom" / "fab-diy-bom.csv"
OUT = ROOT / "bom" / "commandes"
SKIP = {"", "—", "Déjà possédé"}
COLS = ["ref_mekanika", "designation", "produit", "quantite_achat", "prix_unitaire_ttc_eur",
        "total_ttc_eur", "confiance", "lien", "notes"]


def slug(name: str) -> str:
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60]


def main() -> None:
    groups: dict[str, list[dict]] = defaultdict(list)
    with open(BOM, newline="") as fh:
        for r in csv.DictReader(fh):
            total = float(r["total_ttc_eur"] or 0)
            if r["fournisseur"].strip() in SKIP or total == 0:
                continue
            groups[r["fournisseur"].strip()].append(r)
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.csv"):
        old.unlink()
    lines = ["# Listes de commande par fournisseur", "",
             "Générées par `scripts/make_orders.py` à partir de [`fab-diy-bom.csv`](../fab-diy-bom.csv). "
             "Prix TTC France, port compris quand il est chiffré.", "",
             "| Fournisseur | Articles | Total TTC | dont estimé | Liste |", "|---|---:|---:|---:|---|"]
    grand = 0.0
    for name, rows in sorted(groups.items(), key=lambda kv: -sum(float(r["total_ttc_eur"]) for r in kv[1])):
        path = OUT / f"{slug(name)}.csv"
        with open(path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: (r["categorie"] == "Frais de port", r["designation"])))
        total = sum(float(r["total_ttc_eur"]) for r in rows)
        guess = sum(float(r["total_ttc_eur"]) for r in rows if r["confiance"] != "vérifié")
        grand += total
        lines.append(f"| {name} | {len(rows)} | {total:.0f} € | {guess:.0f} € | [`{path.name}`]({path.name}) |")
    lines += [f"| **Total** | | **{grand:.0f} €** | | |", ""]
    (OUT / "README.md").write_text("\n".join(lines))
    print(f"{len(groups)} fournisseurs, {grand:.2f} EUR -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
