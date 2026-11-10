# Budget DIY : chiffrage pour la France

Chiffrage ligne par ligne de [`bom/fab-diy-bom.csv`](../bom/fab-diy-bom.csv) : 191 lignes, plus quelques ajouts et les frais de port.
Prix **TTC pour un particulier en France (TVA 20 %)**, livraison en France. Prix relevés le 8 novembre 2026.
Les recherches sont dans [`bom/chiffrage/`](../bom/chiffrage/), rangées en lots appliqués dans l'ordre. Un lot plus récent remplace les prix d'un lot plus ancien :

| Lot | Contenu |
|---|---|
| A, B, C, D | Premier chiffrage : structure, guidage, électronique, visserie et acier |
| E | Matériel déjà possédé : Makita, Raspberry Pi 5 |
| F | Fournisseurs alternatifs à qualité égale : crémaillères, rails |
| G | France : frais de port, prises au standard français |
| H | Visserie livrée en France |
| I | Moteurs en boucle fermée, martyr |
| J | Revue finale : arrêt d'urgence câblé, relais 25 A pour la Makita, poulies clavetées |

Pour tout recalculer : `python3 scripts/price_bom.py`. Pour un chiffrage belge : `FAB_PAYS=BE python3 scripts/price_bom.py`.

## Total

| | Montant TTC |
|---|---|
| **Total chiffré, port compris** | **≈ 7 290 €** |
| dont prix lus sur la page produit | 4 908 € (67 %) |
| dont estimations | 2 381 € (acier découpé, sécurité électrique, articles AliExpress, port) |
| Avec 10 % d'imprévus (fils, outillage, oublis) | ≈ 8 020 € |
| Variante économique (voir plus bas) | ≈ 5 740 € |
| Avec le kit broche 2,2 kW + VFD au lieu de la Makita | ≈ 7 430 € |
| **Kit officiel Mekanika**, « Pack Fab dès 12 463 € HT » | ≈ 14 960 € TTC |

**Ce qui a changé depuis le premier chiffrage (~7 530 €) :**

| Changement | Effet |
|---|---:|
| Makita et Raspberry Pi 5 déjà possédés (lot E) | ≈ −215 € |
| Crémaillères Gambini de 2 m chez DamenCNC (lot F) | ≈ −296 € |
| Rails, patins et paliers chez Sorotec (lot F) | ≈ −131 € |
| TVA française à 20 % au lieu de 21 % | ≈ −57 € |
| Frais de port vers la France (lot G) | ≈ +17 € |
| Visserie chez TME et Motedis.fr au lieu de Wegertseder (lot H) | ≈ −90 € |
| Moteurs en boucle fermée et martyr (lot I) | ≈ +288 € |
| Revue finale : arrêt d'urgence câblé, relais 25 A, poulies clavetées (lot J) | ≈ +181 € |

## Matériel déjà possédé

**Raspberry Pi 5 16 Go** à la place du Pi 4 2 Go :
- PlanetCNC TNGv2 a une version « RaspberryPi 5 (64bit) » (version du 2026-08-12).
- Mêmes trous de fixation que le Pi 4.
- Deux ajouts : un convertisseur 24 V → 5 V **5 A** (avec 3 A, l'USB est bridé à 600 mA) et un ventilateur actif.

**Affleureuse Makita** à la place du kit broche 2,2 kW + VFD :
- **Hypothèse :** RT0701C/RT0702C, corps Ø65 mm. À confirmer.
- **Ajouts :**
  - un support alu Ø65 mm (à vérifier : un vrai 65,0 mm d'alésage) ;
  - une prise de façade 2P+T.
- **Spindle plate :** percer ses trous au gabarit du support Ø65 avant la découpe.
- **Le boîtier VFD devient un boîtier relais.** PlanetCNC (M3/M5) pilote le module relais 5 V d'origine, qui commande un relais 25 A alimentant la Makita. Ce relais est en aval du contacteur d'arrêt d'urgence (lot J) : **l'arrêt d'urgence coupe la Makita électriquement**, sans dépendre du logiciel.
- **Limites :**
  - 710 W, 3 fois moins de puissance ;
  - vitesse réglée à la main, minimum 10 000 tr/min ;
  - plus bruyante (charbons) ;
  - fraises de 8 mm de queue maximum.
- **Usage :** très bien pour démarrer sur bois, MDF et plastiques. La broche reste l'évolution naturelle.

## Fournisseurs alternatifs, à qualité égale

| Poste | Avant | Après | Pourquoi c'est équivalent |
|---|---:|---:|---|
| Crémaillères | 1 684 € (Dold, 6 × 1 m) | 1 403 € port compris (DamenCNC 2 × 2 m + Dold 2 × 1 m) | Gambini (Italie), qualité 6, rectifiée sur toutes les faces, dents trempées à 56-60 HRC. **Le STEP du vendeur a été mesuré** : 24×24, ligne primitive 22 mm, même perçage que Dold. Une jonction de moins par côté |
| Rails, patins, paliers | 1 013 € (Dold) | 887 € port compris (Sorotec Blue Line) | Dold ne vend pas du HIWIN mais un compatible HGR sans marque (classe P, précharge moyenne). Sorotec Blue Line est du même niveau |
| Visserie | ~408 € (Wegertseder) | 321 € port compris (TME + Motedis.fr) | DIN 912 en 8.8 minimum : **Bossard** noirci chez TME, zingué blanc chez Motedis (même résistance, l'aspect seul change). Les deux livrent les particuliers en France |

**Non retenu :**
- **Motedis** pour les cornières et écrous : prix de déstockage avec 0 pièce disponible à ce prix.
- **Profilés :** Dold reste le moins cher avec coupe et taraudage.
- **Misumi :** rainure 8 et vente aux professionnels seulement.
- **Wegertseder :** ne livre pas tous les particuliers hors Allemagne et Autriche.
- **Vrai HIWIN :** ~100 € de plus. C'est une montée en qualité possible, pas une économie.

## Moteurs en boucle fermée (lot I)

La commande reste **PlanetCNC Mk3/4 + licence sur le Raspberry Pi 5**, comme l'original : tout le boîtier, la carte des fins de course et le câblage de la Fab sont conçus pour elle. Les drivers en boucle fermée acceptent ses signaux step/dir 5 V. Seuls les moteurs changent, en gardant le niveau de l'original ou mieux :

| Poste | Avant | Après | Pourquoi |
|---|---|---|---|
| X, Y1, Y2 | 3 NEMA 34 8,2 N·m en boucle ouverte + drivers 2DM860H | **3 kits StepperOnline 1-CL86T-S90-V41** : NEMA 34 **9 N·m** en boucle fermée + driver CL86T, 94 € le kit | Plus de couple, et un moteur qui ne perd plus de pas sans le dire. Arbre Ø14 claveté inchangé, driver 24-110 V : l'alimentation 72 V reste |
| Z | NEMA 23 3 N·m + 2DM860H sous 72 V | **Kit 1-CL57T-S30A-V41** neuf (NEMA 23 3 N·m en boucle fermée), 71 €, + **alimentation Mean Well LRS-350-48** (40 €) | La XE-PRO garde son moteur. Le driver CL57T monte à 48 V au maximum, d'où l'alimentation 48 V séparée. Arbre Ø8 inchangé |
| Martyr | — | 2 panneaux MDF 18 mm 2500×1220 + 50 inserts M8 acier, ~135 € | N'était pas dans la nomenclature Mekanika |

**À savoir :**
- Les kits n'ont que 1,7 m de câble codeur : 4 rallonges sont comptées (~48 €, estimation). Les prendre prévues pour chaîne porte-câbles.
- Relier la sortie alarme des 4 drivers à une entrée du contrôleur PlanetCNC, pour arrêter la machine dès qu'un driver signale une erreur de suivi. C'est le vrai gain de la boucle fermée sur un portique à deux moteurs. Nombre d'entrées libres sur la Mk3/4 à vérifier.
- grblHAL (carte Flexi-HAL, ~171 €) a été étudié puis écarté : il aurait fallu changer les capteurs, la carte des fins de course, le relais et redessiner le boîtier.
- Le MDF 18 mm des enseignes couvre 1220 des 1250 mm de course X. Pour tout couvrir : MDF 19 mm en 2800×2070 chez un négoce bois, sur devis.

## Sécurité électrique (lot J)

La revue finale a trouvé que la nomenclature n'avait **aucune coupure de puissance câblée**. L'arrêt d'urgence allait seulement au contrôleur : il dépendait du logiciel, ce qui n'est pas une sécurité. Chaîne retenue :

`C14 + fusible → disjoncteur 15 A → contacteur 25 A (bobine 230 V, auto-maintien) → alimentations 72 V et 48 V, relais Makita (et plus tard VFD)`

- **Arrêt d'urgence Schneider XB5 à 2 contacts NF :** le premier coupe la bobine du contacteur, le second va à l'entrée arrêt d'urgence de PlanetCNC.
- **Bouton marche vert :** après un arrêt d'urgence ou une coupure secteur, rien ne redémarre seul.
- **Alimentation 24 V hors contacteur :** la carte, le Pi et les capteurs restent alimentés et gardent la position.
- **Relais Makita 25 A à bobine 24 V :** le module relais 5 V d'origine ne doit pas couper le secteur d'un moteur universel (ses contacts collent au courant d'appel). Il commande la bobine du relais 25 A.

## Par poste

| Poste | TTC | Commentaire |
|---|---:|---|
| Guidage & transmission | 2 620 € | Crémaillères Q6 rectifiées : **1 277 €**. Rails HGR20 Sorotec : 441 €. Poulies Y clavetées |
| Structure alu | 1 197 € | Profilés coupés et taraudés M6 chez Dold. 11 profilés 30×60 de 1410 mm, comme dans le STEP (la nomenclature en compte 9) |
| Moteurs & électronique | 833 € | Kits en boucle fermée (NEMA 34 9 N·m ×3, NEMA 23), alimentations 72, 48 et 24 V, PlanetCNC (carte + licence 226 €), relais 25 A. Raspberry Pi déjà possédé |
| Visserie & fixations | 729 € | Cornières et écrous coulissants chez Dold, vis chez TME et Motedis.fr |
| Pièces acier découpées | 590 € | **Estimation**, fourchette ~360 à ~945 € selon le découpeur |
| Frais de port | 516 € | ~16 envois, dont 126 € chez DamenCNC (barres de 2 m, estimation prudente) et 52 € chez StepperOnline |
| Câblage & connectique | 285 € | Prises et multiprise au standard français, rallonges codeur |
| Gestion des câbles | 160 € | Chaînes, chemin de câbles, goulottes |
| Capteurs & sécurité | 157 € | 6 inductifs M12 PNP, palpeur, arrêt d'urgence 2 NF, contacteur de puissance, bouton marche |
| Broche | 20 € | Makita déjà possédée : seulement le support Ø65 |
| Martyr, gabarits, impression 3D, divers | 183 € | Dont martyr MDF et inserts acier : 135 € |

**Fournisseurs principaux :**
- Dold Mechatronik : ~2 600 €, en deux commandes (profilés via aluprofile-express.de, et mécanique : 2 crémaillères de 1 m, pignons, accouplements).
- Sorotec : 887 € (rails, patins, paliers, port compris).
- DamenCNC : ~810 € (2 crémaillères de 2 m, port compris).
- Découpe laser : ~700 €.
- AliExpress : ~430 €.
- StepperOnline : 452 € (4 kits en boucle fermée, rallonges, port compris).
- PlanetCNC : 240 € (carte Mk3/4, licence, port).
- Motedis.fr : 235 €.
- Reichelt : 207 €.
- Matériel électrique de sécurité (Reichelt, RS ou Conrad) : ~143 € (contacteur, relais 25 A, arrêt d'urgence XB5, bouton marche, rail DIN).
- TME : 156 €.

## Variante économique (≈ −1 545 €, avec perte de qualité)

| Changement | Économie | Contrepartie |
|---|---:|---|
| Crémaillères M2 chinoises au lieu des Q6 rectifiées | ≈ −1 060 € | Plus de jeu et d'erreur de pas sur Y (2,7 m). C'est le compromis le plus visible sur la précision. Il faut reprendre la section 24×24, la hauteur primitive de 22 mm et le perçage d'origine (voir verifications.md) |
| Rails HGR20 et patins AliExpress au lieu de Sorotec | ≈ −485 € | Qualité et précharge variables d'un lot à l'autre |

## À régler avant de commander

1. **Arbres moteurs.** Les NEMA 34 en boucle fermée (34HS46-6004D-E1000, 9 N·m) ont un arbre Ø14 mm claveté au lieu de 12,7, et le NEMA 23 un arbre Ø8 au lieu de 6,35. **Lot J :** les 2 poulies Y sont à faire brocher (clavette 5 mm DIN 6885) et l'accouplement X passe à moyeux serrants. Trouver l'atelier de brochage, ou une poulie vendue clavetée.
2. ~~**NEMA23 à 72 V.**~~ **Réglé :** le driver CL57T a sa propre alimentation 48 V. **Stock :** il ne restait que 2 kits NEMA 23 à l'entrepôt allemand le 8 novembre.
3. **Pignon-poulie de l'axe Y.** C'est une pièce spéciale Mekanika, introuvable toute faite, et Mekanika ne publie pas le prix de ses pièces détachées. Chiffrée en pignon M2 Z15 (Dold) + poulie HTD-5M 80T (AliExpress) + assemblage en atelier, ~70 € l'ensemble, non trempé.
4. **Vis à billes X de 1500 mm.** Beaucoup de vendeurs plafonnent à 1450 mm. L'écrou SFS1620 doit faire Ø28 pour entrer dans le boîtier DSG16H.
5. ~~**Rainure du 60×60.**~~ **Vérifié** ([verifications.md](verifications.md)) : tout est en rainure 6, et les crémaillères Dold et Gambini sont identiques à celle du STEP.
6. **Licence PlanetCNC.** Elle est vendue à part, incluse dans les 240 €. Sans elle, la carte est limitée à 25 lignes de G-code. **TVA StepperOnline :** le panier n'ajoute aucune ligne de TVA depuis l'entrepôt allemand ; les prix sont lus comme TTC, à confirmer au paiement.
7. ~~**Visserie Wegertseder.**~~ **Réglé :** TME et Motedis.fr livrent les particuliers en France.
   - Ruptures de stock chez TME : DIN 912 M4×45 et ISO 7379 M10×50 (prix estimés). La M4×55 n'existe que par 200, à 26 €.
   - ISO 7380 M3×4 : uniquement en inox A2. Ça suffit pour les vis de capot des boîtiers.
8. **Port DamenCNC** pour des barres de 2 m : estimé à 126 €, non publié. **Demander un devis de port** avant de commander.
9. **Chaîne porte-câbles.** Chiffrée en 24×60 au lieu de 25×50 : vérifier les embouts face aux supports acier.
10. **Acier.** Seul un vrai devis (téléverser les DXF/STEP de `cad/steel/`) donnera le prix. Les trous de Ø4,3 à 5,5 dans le 8 mm sont à faire pointer puis percer.
11. **Boîtier de commande (tôles M00279/M00280).** Il est dessiné pour PlanetCNC, les drivers 2DM860H et une seule alimentation. Les CL86T ont l'encombrement des 2DM860H. **Avant la découpe laser**, vérifier que le driver CL57T, l'alimentation LRS-350-48 (215×115×30 mm), le contacteur, le relais sur rail DIN et 4 embases codeur y tiennent, et ajouter leurs perçages. Une tôle découpée ne se reprend pas.
12. **Rails Y aboutés.** L'original achète des rails « docking », appairés pour être mis bout à bout. Faire confirmer par écrit à Sorotec des rails rectifiés en bout, marqués par paire, avec un pas de trous continu à la jonction. Sinon, il y aura une marche à chaque raccord.
13. **Plan de câblage moteurs, codeurs et capteurs.** Les câbles d'origine étaient vendus montés (Belram). Il faut fixer les connecteurs de façade : XLR4 femelles de câble et XLR3 mâles pour les capteurs, et des embases pour les 4 câbles codeur, que la nomenclature n'a pas. Les contacts Micro-Fit étaient prévus pour l'ancien moteur Z. Les câbles Y2 et Z font 5,3 et 5,7 m : prendre des rallonges codeur de 5 m, en plus des 1,7 m du kit.
14. **Fins de course :** câblage d'origine (6 capteurs PNP NF, carte d'adaptation à optocoupleurs). Il n'y a que le schéma QElectroTech : faire le PCB d'après lui ou prendre une carte optocoupleur du commerce.
15. **Alimentation 48 V :** son potentiomètre monte jusqu'à ~52,8 V. La laisser à 48 V au plus (limite du CL57T). Récupérer le lien exact du kit NEMA 23 avant de commander.
16. ~~**Goussets.**~~ **Réglé :** 14, comme dans le modèle 3D. Les 14 positions sont relevées dans [verifications.md](verifications.md), section 5. La ligne est chiffrée pour 14.
17. **Profilés 30×60 de 1410 mm :** 11 dans le modèle 3D, 9 dans la nomenclature. La ligne est chiffrée pour 11 (+62 €). À confirmer avec le guide de montage ou sur le Discord avant de commander : 2 profilés en trop coûtent peu, 2 en moins bloquent le montage.

## Ce que le DIY ne remplace pas

Le kit officiel inclut ce que ce budget ne compte pas :
- la garantie de 5 ans et le support ;
- des pièces livrées prêtes à monter : pignon-poulie, crémaillères et profilés appairés ;
- un montage annoncé à ~25 h, contre plusieurs semaines de sourcing et d'usinage en DIY.

L'économie réelle tourne autour de **6 900 à 7 700 €** (imprévus compris ou non), ou **~9 200 €** en variante économique. Avec la Makita, la machine n'est pas tout à fait équivalente : compter ~145 € de plus pour la broche 2,2 kW.
