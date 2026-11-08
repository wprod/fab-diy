"""Merge the pricing research (bom/chiffrage/lot-*.csv) into bom/fab-diy-bom.csv.

Each lot file has one row per BOM line (matched on ref_mekanika, or on the
designation for lines without a Mekanika reference) plus "PORT" rows for
shipping. Lots are applied in name order, so a later lot overrides an earlier
one (lot-E-materiel-possede.csv zeroes what is already owned). Rows with
ref_mekanika "AJOUT" add a line that is not in the Mekanika BOM, filed under
their `categorie` column.

VAT: the lots were researched for Belgium (TTC 21 %). A lot row may say otherwise
in an optional `tva_pays` column (e.g. "FR"). Every price is converted to the
buyer's country, PAYS below (env FAB_PAYS overrides it), by the ratio of the two
VAT rates.

Usage (rebuilds the BOM with flatten_bom.py first, so it can be re-run):
    python3 scripts/price_bom.py
"""

from __future__ import annotations

import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOM = ROOT / "bom" / "fab-diy-bom.csv"
LOTS = sorted((ROOT / "bom" / "chiffrage").glob("lot-*.csv"))
COPY = ["fournisseur", "produit", "lien", "quantite_achat", "confiance"]
TVA = {"FR": 0.20, "BE": 0.21, "DE": 0.19, "NL": 0.21}
PAYS = os.environ.get("FAB_PAYS", "FR")


def num(value: str) -> float:
    text = (value or "").replace("€", "").replace(" ", "").replace(" ", "").strip()
    if "," in text and "." in text:  # the last separator is the decimal one
        thousands = "." if text.rfind(",") > text.rfind(".") else ","
        text = text.replace(thousands, "")
    return float(text.replace(",", ".")) if text else 0.0


def ttc(p: dict, key: str) -> str:
    """Price of lot row `p` converted to TTC in PAYS (lots default to Belgian VAT)."""
    source = (p.get("tva_pays") or "BE").strip().upper()
    return f"{num(p.get(key, '')) * (1 + TVA[PAYS]) / (1 + TVA[source]):.2f}"


def main() -> None:
    # Always start from a freshly flattened BOM so the script can be re-run safely
    # (otherwise shipping and added rows would be appended again on each run).
    sys.path.insert(0, str(Path(__file__).resolve().parent))  # also works under python -I
    import flatten_bom
    flatten_bom.main()
    with open(BOM, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = list(reader.fieldnames or []), list(reader)
    by_key = {(r["ref_mekanika"] or r["designation"]): r for r in rows}
    base_notes = {id(r): r.get("notes", "") for r in rows}

    # Extra rows (shipping, additions) are keyed so a later lot replaces them too:
    # PORT by supplier, AJOUT by designation.
    extras: dict[tuple[str, str], dict] = {}
    unmatched = []
    for lot in LOTS:
        with open(lot, newline="", encoding="utf-8-sig") as fh:
            for p in csv.DictReader(fh):
                ref = (p.get("ref_mekanika") or "").strip()
                if ref.upper() == "AJOUT":
                    added = {f: (p.get(f) or "").strip() for f in COPY}
                    added.update({
                        "categorie": p.get("categorie") or "Ajouts", "designation": p["designation"],
                        "quantite": p.get("quantite_bom", "1"), "sourcing": "acheter",
                        "prix_unitaire_ttc_eur": ttc(p, "prix_unitaire_ttc_eur"),
                        "total_ttc_eur": ttc(p, "total_ttc_eur"),
                        "notes": p.get("notes", ""), "statut": "chiffre",
                    })
                    extras[("AJOUT", p["designation"].strip())] = added
                    continue
                if ref.upper() == "PORT":
                    extras[("PORT", p.get("fournisseur", "").strip().lower())] = {
                        "categorie": "Frais de port", "designation": p["designation"],
                        "fournisseur": p.get("fournisseur", ""), "quantite": 1,
                        "total_ttc_eur": ttc(p, "total_ttc_eur"),
                        "confiance": p.get("confiance", ""), "notes": p.get("notes", ""),
                        "statut": "chiffre",
                    }
                    continue
                row = by_key.get(ref or p["designation"].strip())
                if row is None:
                    unmatched.append(f"{lot.name}: {ref or p['designation']}")
                    continue
                for f in COPY:
                    row[f] = (p.get(f) or "").strip()
                row["prix_unitaire_ttc_eur"] = ttc(p, "prix_unitaire_ttc_eur")
                row["total_ttc_eur"] = ttc(p, "total_ttc_eur")
                # A later lot replaces an earlier one's notes; the BOM's own note stays.
                row["notes"] = "; ".join(x for x in (base_notes[id(row)], p.get("notes")) if x)
                row["statut"] = "chiffre"

    rows += list(extras.values())
    with open(BOM, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    by_cat, by_supplier, by_conf = defaultdict(float), defaultdict(float), defaultdict(float)
    for r in rows:
        t = num(r.get("total_ttc_eur", ""))
        by_cat[r["categorie"]] += t
        by_supplier[r.get("fournisseur") or "?"] += t
        by_conf[r.get("confiance") or "?"] += t
    total = sum(by_cat.values())
    for title, data in (("Categorie", by_cat), ("Fournisseur", by_supplier), ("Confiance", by_conf)):
        print(f"\n{title}")
        for k, v in sorted(data.items(), key=lambda kv: -kv[1]):
            print(f"  {v:10.2f} EUR  {k}")
    missing = [r["designation"] for r in rows if r.get("statut") != "chiffre"]
    print(f"\nTOTAL TTC ({PAYS}, TVA {TVA[PAYS]:.0%}) : {total:.2f} EUR  |  lignes non chiffrees : {len(missing)}")
    for m in missing:
        print("  -", m)
    if unmatched:
        print("Lignes de chiffrage sans correspondance :", *unmatched, sep="\n  ", file=sys.stderr)


if __name__ == "__main__":
    main()
