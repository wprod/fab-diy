# Pignon-poulie de l'axe Y : fiche pour l'atelier

Il en faut **2, identiques**. C'est une pièce spéciale Mekanika (M01685), introuvable toute faite.
Cette fiche donne les cotes relevées dans le STEP officiel, pour faire fabriquer ou assembler la pièce.

![Coupe du pignon-poulie](img/pignon-poulie.png)

## Cotes relevées dans le STEP

| Élément | Cote |
|---|---|
| Longueur totale | 45 mm |
| **Pignon** | module 2, **15 dents**, Ø34 en tête, Ø25,8 en pied, largeur 25 mm |
| **Poulie** | HTD-5M, **80 dents**, Ø126,18 extérieur, largeur 20 mm, sans flasque |
| Alésage central | Ø12,2 (la pièce tourne librement sur un axe fixe de Ø12) |
| Logement côté poulie | Ø37 × 12 mm de profondeur |
| Logement côté pignon | Ø18 × 4 mm, au fond d'un dégagement de Ø19 × 10,1 mm |

La pièce ne transmet aucun couple à un arbre : la courroie entraîne la poulie, le pignon solidaire roule sur la crémaillère, et l'ensemble tourne fou sur une vis à épaulement M10 de Ø12 × 50 (ISO 7379), fixée dans la plaque d'entraînement.

Réduction : poulie moteur de 20 dents, soit **4:1**. Le diamètre primitif du pignon est de 30 mm : un tour de pignon fait avancer le portique de 94,25 mm.

## Roulements : un écart entre le STEP et la nomenclature

| Source | Côté poulie | Côté pignon |
|---|---|---|
| STEP (pièce « Q5_03 v6 ») | logement Ø37 × 12 → **6301-2RS** (12 × 37 × 12) | logement Ø18 × 4 → roulement 12 × 18 × 4 (type 6701) |
| Nomenclature (« Pinion v2 ») | 6301-2RS | **6801-ZZ** (12 × 21 × 5) |

La nomenclature décrit donc une version plus récente que le STEP, avec un roulement un peu plus gros côté pignon et trois entretoises (12 × 16 × 3, 12 × 18 × 8, 12 × 18 × 18).

**Conseil :** suivre le STEP, qui est la seule géométrie complète disponible, et monter un 6701 côté pignon. Un logement de Ø21 pour le 6801 ne laisserait que 2,4 mm de matière sous les dents (pied à Ø25,8). Si l'atelier préfère le 6801, il faut le lui faire valider. Dans ce cas, deux 6701 sont à acheter à la place des deux 6801 de la BOM (quelques euros).

## Deux façons de l'obtenir

1. **Assemblage, comme chiffré (~70 € par ensemble).** Un pignon M2 Z15 du commerce (Dold, C45, largeur 20) et une poulie HTD-5M 80 dents du commerce, usinés puis assemblés : alésages et logements ci-dessus, pignon emmanché, collé et goupillé dans la poulie.
   - Le pignon du commerce fait 20 mm de large au lieu de 25 : vérifier avec l'atelier que la denture reste en face de la crémaillère (24 mm de large).
   - Le pignon C45 n'est pas trempé : c'est une pièce d'usure, à surveiller.
2. **Pièce monobloc sur plan**, taillée par un atelier d'engrenages. Plus cher, mais conforme à l'original, et on peut demander une denture trempée.

## À donner à l'atelier

- cette fiche et le dessin ;
- une vis à épaulement ISO 7379 Ø12 × 50 M10 et les deux roulements, pour ajuster les logements ;
- la tolérance attendue : logements de roulements en H7, concentricité de la denture du pignon par rapport aux logements meilleure que 0,05 mm. C'est elle qui fait la régularité de l'axe Y.

## Poulies moteur

Pour mémoire, les poulies côté moteur (M00733) sont des HTD-5M de 20 dents : Ø30,69 extérieur, flasques de Ø36, 17 mm entre flasques, 26 mm de long. L'original a un alésage de 12,7 mm ; cette version les prend en alésage 14 H7 avec une rainure de clavette de 5 mm, pour les arbres Ø14 clavetés des moteurs en boucle fermée.
