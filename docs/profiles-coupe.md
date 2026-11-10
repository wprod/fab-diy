# Profilés : fiche de coupe pour le devis

Tout est en **profilé I, rainure 6** (vérifié dans le STEP, voir [verifications.md](verifications.md)).
Aucune pièce ne dépasse 1530 mm : l'axe Y est fait de deux tronçons bout à bout.

| Réf. | Section | Longueur | Qté | Taraudage en bout | Rôle |
|---|---|---:|---:|---|---|
| M00058 | 30×120 | 1530 mm | 4 | 4 × M6, **un seul bout** | Longerons hauts de l'axe Y, 2 par côté |
| M00061 | 60×60 | 1530 mm | 2 | 4 × M6, **les deux bouts** | Poutres du portique (axe X) |
| M00060 | 60×60 | 1410 mm | 6 | aucun | 5 traverses de table, 1 traverse basse centrale |
| M00059 | 30×60 | 1410 mm | **11** | aucun | 4 longerons bas, 3 traverses basses, 4 traverses de table |
| M00930 | 30×60 | 600 mm | 6 | 2 × M6, **les deux bouts** | Pieds |
| M00055 | 30×30 | 240 mm | 2 | 1 × M6, **les deux bouts** | Supports de rail de l'axe Z |

Soit 6,12 m de 30×120, 11,52 m de 60×60, 19,11 m de 30×60 et 0,48 m de 30×30 : environ **84 kg**.

## À préciser dans la commande

- **Tolérance de longueur.** Les pièces d'une même ligne doivent être **identiques entre elles** : demander une coupe en série sur la même butée. L'écart entre deux pièces compte plus que la cote exacte, surtout pour les 6 pieds, les 4 longerons 30×120 et les traverses de 1410 mm (elles fixent l'écartement des deux rails Y).
- **Coupes d'équerre et ébavurées.** Les 30×120 se raccordent bout à bout sous le rail.
- **Quantité des 30×60 de 1410 mm :** 11 d'après le STEP, 9 d'après la nomenclature. Voir [verifications.md](verifications.md), section 5.
- **Taraudages :** M6 dans les alésages de bout du profilé, profondeur d'au moins 15 mm (les vis relevées sont des M6×20 à travers une tôle de 8 ou 10 mm).

## Ce que reçoivent les bouts taraudés (relevé dans le STEP)

| Profilé | Bout | Pièce fixée |
|---|---|---|
| 30×120 de 1530 | extérieur | Support de capteur de fin de course (8 mm), 4 × M6×20 |
| 30×120 de 1530 | jonction | rien : bout lisse |
| 60×60 de 1530 | les deux | Flasques du portique (*Gantry*, 10 mm), 4 × M6×20 par bout |
| 30×60 de 600 | bas | Plaque de pied 60×30×10 taraudée M12 |
| 30×60 de 600 | haut | à confirmer au montage |

## Fournisseur chiffré

Dold Mechatronik (aluprofile-express.de) : coupe à longueur de 50 à 6000 mm, taraudage en option par bout. Total de la catégorie « Structure alu » : ~1 197 € TTC, plus ~109 € de port GLS (colis de moins de 2 m, tranche jusqu'à 120 kg). Détail ligne par ligne dans [`bom/fab-diy-bom.csv`](../bom/fab-diy-bom.csv).
