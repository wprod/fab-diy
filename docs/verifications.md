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

**Confirmé par le guide de montage officiel, qui en utilise 11** (section 9). Les deux traverses rapprochées à l'avant portent les boîtiers. La BOM est chiffrée pour 11.

## 6. Vis à billes de l'axe X : il faut bien 1500 mm

Relevé le 10 novembre 2026 dans le STEP, le long de l'axe X du portique :

| Élément | Position en X |
|---|---|
| Vis à billes, longueur hors tout **1500 mm** | de −40 à 1460 |
| Palier fixe FK12, côté moteur | de −22 à 12 |
| Palier libre FF12 (épaisseur 15 mm) | de 1448 à 1463 |
| Flasques du portique | −55 à −45 et 1485 à 1495 |

- La vis s'arrête 3 mm avant la face extérieure du palier libre. **Une vis de 1450 mm s'arrêterait à X = 1410, soit 38 mm avant ce palier** : son extrémité ne serait pas tenue.
- Sans palier au bout, une vis de 16 mm aussi longue fouette bien avant la vitesse de déplacement annoncée (20 m/min, soit 1000 tr/min avec un pas de 20 mm). Une vis plus courte n'est donc pas une option, sauf à déplacer le palier libre.
- **À commander :** longueur hors tout de 1500 mm, usinages d'extrémité standard pour FK12 (côté moteur, bout de Ø10 pour l'accouplement) et FF12.

## 7. Poulie de l'axe Y : HTD-5M, 80 dents

La pièce s'appelle « Pulley HTD3M & Pinion » dans le STEP, mais son diamètre extérieur mesuré est de **126,1 à 126,2 mm**.

| Hypothèse | Diamètre extérieur théorique |
|---|---|
| HTD-5M, 80 dents | 80 × 5 / π − 1,14 = **126,18 mm** |
| HTD-3M, 132 dents | 132 × 3 / π − 0,76 = 125,29 mm |

C'est donc bien une **5M de 80 dents**, comme chiffré. Avec la poulie moteur de 20 dents, la réduction est de 4. L'ensemble poulie et pignon fait 45 mm de large et tourne sur une vis à épaulement M10 de Ø12.

## 8. Visserie : la nomenclature couvre le modèle 3D

Contrôle du 14 novembre 2026 : chaque vis, écrou et rondelle du STEP a été compté et comparé à la nomenclature.

| Article | STEP | Nomenclature |
|---|---:|---:|
| Vis CHC M6×16 (y compris celles des cornières) | 312 | 318 |
| Vis CHC M6×20 | 66 | 66 |
| Vis CHC M5×16 | 178 | 190 |
| Rondelles larges M6 | 272 | 276 |
| Écrous coulissants M6 | 316 | 368 |
| Écrous coulissants M5 | 158 | 168 |
| Écrous frein M4 / M5 / M6 | 24 / 20 / 14 | 24 / 20 / 14 |
| Entretoises M5 de 19, 30 et 6 mm | 8 / 12 / 2 | 8 / 12 / 2 |
| Cornières de 30 | 36 | 38 |
| Cornières de 60 | 50 | 46 |

- **La visserie est cohérente** : la nomenclature couvre le modèle, avec une petite marge.
- **Seules les cornières de 60 manquent** (46 pour 50). La BOM en achète déjà 50.
- Trois petits écarts viennent du modèle lui-même : l'ensemble moteur gauche est une version plus ancienne que le droit, et n'a pas exactement les mêmes vis (M4×30, M5×45 ou M5×50, M6×25 à tête bombée). La nomenclature suit la version récente. Ces vis s'achètent par sachet, donc cela ne change rien à la commande.
- Le boîtier de commande et ses vis ne sont pas dans ce modèle : ils ne sont pas comptés ici.

## 9. Ce que confirme le guide de montage officiel

Lu le 14 novembre 2026 sur support.mekanika.io (chapitres « Table Frame » et « Machine Connection »).

| Point | Guide officiel | Ce dépôt |
|---|---|---|
| Profilés 30×60 de 1410 mm | **11** : 6 traverses (étape 1) et 5 longerons (étape 2) | 11 ✔ |
| Profilés 60×60 de 1410 mm | 6 (étapes 3 et 4) | 6 ✔ |
| Pieds 30×60 de 600 mm | 6 | 6 ✔ |
| Goussets | **14** : 6 en travers (étape 23) et 8 dans le sens de la longueur (étape 24) | 14 ✔ |
| Jonction des 30×120 | « au centre du profilé vertical », bout non taraudé vers la jonction | section 4 ✔ |
| Rails | bout à arête vive pour l'aboutage, bout ébavuré pour enfiler les patins | point 12 du budget |
| Ordre des connecteurs moteurs et capteurs | X, Y1, Z, Y2 en partant du ventilateur ; les 2 embases du bas sont X et Y1 | carte des fins de course ✔ |

La nomenclature publiée sur GitHub (9 profilés, 12 goussets) est donc en retard sur le guide.

### Deux versions du châssis

Le guide précise que son chapitre 1 vaut pour les machines livrées **depuis mars 2026**. Les deux versions utilisent les mêmes 11 profilés, placés différemment :

| | Ancienne version | Nouvelle version (guide actuel) |
|---|---|---|
| Traverses basses 30×60 | 3, dont 2 rapprochées à l'avant | 2 |
| Le 11e profilé | 3e traverse basse | « support du boîtier de commande » : un longeron fixé entre deux pieds, à 500 mm de la plaque de pied |
| Boîtier de commande | posé à plat sur les 2 traverses basses avant, sans fixation | suspendu à la verticale sur 4 pattes à encoche |
| Cornières de 60 / de 30 | 50 / 36 (comptées dans le STEP) | 46 / 40 (additionnées dans le guide) |

**Le modèle 3D de ce dépôt est l'ancienne version**, et c'est celle que ce projet suit : tous les fichiers (STEP, DXF, tôles du boîtier) lui correspondent, et le boîtier s'y pose sans aucune pièce spéciale. La BOM achète 50 cornières de 60 et 38 de 30, ce qui couvre cette version.

**Conséquence au montage :** suivre le guide officiel, sauf pour les étapes 2, 9 et 12 du chapitre 1. Au lieu de monter le « support du boîtier » à 500 mm de haut, ce profilé devient une troisième traverse basse, à 288 mm d'entraxe de la première (positions en section 5).
