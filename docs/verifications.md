# Vérifications dans le STEP officiel (8 novembre 2026)

Mesures faites directement sur la géométrie de `cad/source/FAB V1.0.stp` (OpenCascade).
Objectif : confirmer que les références chiffrées dans `bom/chiffrage/` vont réellement sur la machine.

## 1. Rainures des profilés : tout est en rainure 6

Chaque profilé est coupé à mi-longueur, puis la rainure est mesurée à plusieurs profondeurs.

| Profilé (nom dans le STEP) | Section | Entrée en surface | **Col (ouverture mini)** | Lèvre |
|---|---|---|---|---|
| 1410mm I-type profile 6060 / 1410mm 6060 profile | 60×60 | 8,2 mm (chanfrein 1 mm) | **6,2 mm** | 2,5 mm |
| I-type profile 3060 (1410 et 600) | 30×60 | 8,2–8,35 mm | **6,2–6,35 mm** | 2,4–2,5 mm |
| I-type profile 30120 | 30×120 | 8,35 mm | **6,35 mm** | 2,4 mm |
| V-Type profile 6060 (gantry, 1530) | 60×60 | 9,35 mm (chanfrein 45° « V ») | **6,35 mm** | 2,4 mm |
| V-type profile 3030 (chariot X, 240) | 30×30 | 9,35 mm | **6,35 mm** | 2,4 mm |

![Coupes des rainures](img/rainures-profiles.png)

**Conclusions :**
- **Le 60×60 est bien en rainure 6.** Le « Groove 8 » de la nomenclature désigne la cornière, pas le profilé. Le chiffrage (Dold « I-Typ Nut 6 » partout, écrous coulissants Nut 6) est **correct**.
- **Profilés « V » :** les quatre profilés nommés « V » (2 × 60×60 du gantry, 2 × 30×30 du chariot X) ont seulement une entrée chanfreinée à 45°. Le col est le même 6,35 mm. **Aucune roue ne roule dessus** : les 4 roues V-slot sont dans les ensembles moteur-pignon de l'axe Y (2 par côté). Des profilés I standard conviennent, comme chiffré.

## 2. Cornières

![Coupes des cornières](img/cornieres.png)

- **Cornière 60×60 (« Gubo », 50 pièces dans le STEP) :** base plate **sans nez de centrage**, trous de Ø8,2. Elle se fixe avec vis M6 + rondelle large DIN9021 sur écrou coulissant rainure 6 : c'est pour ça que la nomenclature compte 276 rondelles M6×18. La cornière Dold 67250 « sans nez » retenue convient.
- **Cornière 30 (« Dold », 36 pièces dans le STEP) :** avec nez de centrage rainure 6. Le chiffrage (Dold art. 62378, I-Typ Nut 6) correspond à la pièce nommée dans le STEP.

## 3. Crémaillère : identique à la référence Dold chiffrée

| Cote | STEP officiel | Dold GG-445-020-0210 « mit Bohrbild » |
|---|---|---|
| Section × longueur | 24 × 24 × 1005,31 mm | 24 × 24 × 1005,31 mm |
| Module / dents | M2 (hauteur de dent 4,5 mm) | M2, 160 dents, ligne primitive h = 22 |
| Trous de fixation | Ø7 lamé Ø11, profondeur 7 | d1 = 7, d2 = 11, t = 7 |
| Position du 1er trou / entraxe | 62,8 mm puis tous les 125,66 mm (8 trous) | a = 62,83, l = 125,66 |
| Trous de goupille | Ø5,7 à 31,3 mm des bouts, 942,7 mm d'entraxe | d3 = 5,7, a1 = 31,3, l1 = 942,7 |

**Conclusion :** c'est exactement la même pièce. Le numéro fabricant 445-020-0210 est une référence **Mädler**, que Dold revend.
- **Variante à commander :** « L1=1000, **mit Bohrbild** », c'est-à-dire avec les perçages. Le lien de la BOM pointe bien vers elle.
- **Autre source possible :** Mädler en direct, prix non vérifié.
- **Variante économique :** des crémaillères moins chères devront reprendre cette section 24×24, ce perçage et la hauteur primitive de 22 mm. Sinon les plaques d'entraînement et les supports ne tombent plus en face.

## 4. Axe Y : aucun profilé de plus de 1530 mm

Vérifié le 10 novembre 2026 en relevant la position de chaque pièce du STEP. Y est mesuré dans le repère du modèle ; la jonction est à Y = 105.

| Élément | Par côté | Jonction |
|---|---|---|
| Longeron haut 30×120 (porte le rail et la crémaillère) | 2 × 1530 mm = 3060 mm | Y = 105, au-dessus du pied central |
| Rail HGR20 | 2 × 1500 mm | Y = 105, au même endroit |
| Crémaillère M2 | 3 × 1005,31 mm | Y = −398 et Y = 608 : décalées, la crémaillère du milieu enjambe la jonction |
| Longeron bas 30×60 | 2 × 1410 mm | de part et d'autre du pied central (Y = 75 à 135) |
| Pieds 30×60 de 600 mm | 3 : avant, milieu, arrière | le pied du milieu est sous la jonction |

- **Pas d'éclisse à la jonction.** Les deux 30×120 sont simplement mis bout à bout. Ils sont tenus par le pied central (2 cornières de 30), un gousset de chaque côté, la traverse 60×60 de la table et celle du bas, placées à la jonction.
- **Sens des 30×120 :** le bout taraudé (4 × M6) va **à l'extérieur**. Il reçoit le support de capteur (*Limit switches support*, 4 vis M6×20). Le bout lisse va à la jonction.
- **Alignement :** le rail et le profilé se raccordent au même endroit. L'alignement des deux moitiés se règle donc à cette jonction, avec la crémaillère du milieu et la règle. Voir le point 12 de [budget.md](budget.md) sur les rails aboutés.

## 5. Comptages : goussets et profilés 30×60

**Goussets (*Triangulation v6*) : 14.** La nomenclature en donne 12. Les 14 du STEP forment un ensemble symétrique :

| Position | Nombre |
|---|---:|
| Dans le sens Y, contre les pieds d'angle (1 par pied) | 4 |
| Dans le sens Y, de part et d'autre des pieds du milieu (2 par pied) | 4 |
| Dans le sens X, contre chaque pied (avant, milieu, arrière ; 1 par pied) | 6 |

En retirer 2 laisserait un pied sans contreventement. **On en découpe 14.** Le DXF et le chiffrage sont déjà à 14.

**Profilés 30×60 de 1410 mm : 11.** La nomenclature en donne 9.

| Position | Nombre |
|---|---:|
| Longerons bas, sens Y (2 par côté) | 4 |
| Traverses basses, sens X (Y = −1262, −974 et 1472) | 3 |
| Traverses de table, sens X, entre les 60×60 | 4 |

Les 60×60 de 1410 mm sont bien 6 dans les deux sources : 5 traverses de table et 1 traverse basse au milieu.

L'écart n'est pas expliqué : le guide de montage en ligne (support.mekanika.io) n'a pas pu être consulté depuis cette session. Les traverses basses ne sont pas symétriques (2 à l'avant, 1 à l'arrière), donc 2 d'entre elles sont peut-être optionnelles. **La BOM est chiffrée pour 11** (+62 €), à confirmer avant de commander.
