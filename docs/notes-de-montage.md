# Notes de montage : ce qui diffère du guide officiel

Le montage suit le [guide officiel Mekanika](https://support.mekanika.io/products/fab-cnc/assembly-guide).
Cette page liste seulement ce qui change pour cette machine, et ce que le guide apprend sur les pièces à préparer.
Elle s'appuie sur la lecture complète du guide, le 14 novembre 2026.

## Ce qui change par rapport au guide

| Chapitre du guide | Ce que dit le guide | Ce qu'il faut faire ici |
|---|---|---|
| 1, étapes 2 et 12 | un profilé 30×60 sert de « support du boîtier de commande », fixé à 500 mm de haut | il devient une **troisième traverse basse**, à l'avant, à 288 mm d'entraxe de la première |
| 1, étape 9 | 2 traverses basses 30×60 | 3 traverses basses : 2 à l'avant, 1 à l'arrière ([verifications.md](verifications.md), section 5) |
| 5, étape 4 | broche 2,2 kW sur sa plaque d'interface | support Ø65 de la Makita, trous à percer dans la plaque |
| 7 | moteurs NEMA 34 à arbre de 12,7 mm | arbres Ø14 clavetés : poulies alésées à 14 avec rainure de clavette |
| 11, étape 1 | boîtiers suspendus à la verticale sur 4 pattes | boîtier de commande **posé à plat** sur les 2 traverses basses avant ([pieces-acier.md](pieces-acier.md)) |
| 11 | boîtier VFD | pas de boîtier VFD : relais et prise de la Makita dans le boîtier de commande ([plan-cablage.md](plan-cablage.md)) |

Pourquoi ces écarts sur le châssis : le guide décrit les machines livrées depuis mars 2026, alors que le modèle 3D publié, que suit ce projet, est la version précédente. Les deux utilisent les mêmes profilés.

## Gabarits : à faire soi-même

Le kit officiel fournit trois gabarits. Seul le plus petit a un plan publié.

| Gabarit du guide | À quoi il sert | Ici |
|---|---|---|
| « Frame assembly gauge » (chapitre 1, étape 22) | cale l'écart entre deux traverses de table pendant le serrage | **2 barres de MDF de 18 mm, longues de 322,5 mm**, coupées dans une chute du martyr. L'écart est le même partout (relevé dans le STEP) |
| « Assembly gauge 18 mm » (chapitre 7, étape 5) | aligne la poulie moteur sur la poulie du pignon | la même barre, posée à plat : c'est son épaisseur de 18 mm qui sert |
| « Rail assembly gauge » (chapitre 1, étape 19) | tient le rail à la bonne hauteur pendant le serrage | une mesure : **le dessus du rail est à 35,0 mm sous le dessus du profilé 30×120** (soit le dessous du rail à 65,0 mm du bas). Une cale de 35 mm ou la jauge de profondeur d'un pied à coulisse suffit |
| Gabarit PMMA de 60 × 60 mm | réglage des capteurs, passage des câbles dans les clips | `cad/gabarits/FAB_Mounting_Gauge.dxf`, à faire découper |

Les deux barres doivent avoir **exactement la même longueur** : les couper ensemble, en une passe. Leur longueur absolue compte moins que leur égalité.

## Pignon de l'axe Y : ordre d'empilage (chapitre 7, étape 4)

Sur la vis à épaulement Ø12 × 50, dans cet ordre en partant de la tête :

1. entretoise A, 12 × 16 × 3 ;
2. petit roulement 12 × 21 × 5 ;
3. entretoise C, 12 × 18 × 18, chanfrein côté petit roulement ;
4. le pignon-poulie ;
5. gros roulement 12 × 37 × 12 ;
6. entretoise B, 12 × 18 × 8 ;
7. la plaque d'entraînement, puis l'écrou frein M10, serré à 10 N·m.

Cet empilage fixe les alésages du pignon-poulie : voir [pignon-poulie.md](pignon-poulie.md).

## Autres points relevés dans le guide

- **Rails Y :** le bout à arête vive sert à l'aboutage, le bout ébavuré à enfiler les patins. Bout non taraudé du 30×120 vers la jonction (chapitre 1, étapes 13 à 17).
- **Chaîne porte-câbles Y :** 1500 + 400 = **1900 mm**, et non 1800 comme dans la nomenclature. Un 4e sachet de 1 m est ajouté à la BOM.
- **Supports de chaîne :** les 4 supports servent d'abord, à deux, de cale pour poser le portique (chapitre 6), puis sont démontés et remontés à leur place définitive (chapitre 9).
- **Tension de la courroie :** deux galets sur une vis M5×50, poussés contre la courroie dans une lumière de la plaque (chapitre 7, étape 7).
- **Pression du pignon sur la crémaillère :** un ressort sur une vis M5×50, serré en laissant 2 à 3 mm de course (chapitre 8, étape 8).
- **Mise à niveau :** elle se fait par le pied du milieu, avant de serrer la jonction des longerons (chapitre 1, étape 18).
- **Arrêt d'urgence :** à l'avant gauche, sur le profilé avant, câble vers le bas (chapitre 9, étape 14).
- **Capteurs :** X−, X+ et Y1−, Y1+ se branchent indifféremment sur les deux embases de leur axe.

## Options du guide qui ne concernent pas cette machine

Le guide couvre trois hauteurs d'axe Z (Z250, Z350, Z600). Cette machine est la **Z250** : ignorer les étapes marquées « Z600 only » (frein d'axe Z, plaque d'adaptation, guide de chaîne) et les cotes Z350.
