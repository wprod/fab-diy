# Fab DIY

Construire soi-même une CNC grand format à partir des fichiers open source de la
**[Mekanika Fab](https://www.mekanika.io/fr/products/fab)** : surface de travail 1330 × 2700 mm,
rails HGR20, vis à billes sur X et Z, double crémaillère module 2 sur Y,
NEMA34 6 A, contrôleur PlanetCNC, broche 2,2 kW.

- Dépôt officiel : <https://github.com/mekanika-dev/fab>
- Guide de montage : <https://support.mekanika.io/products/fab-cnc>
- Modèle 3D dans le navigateur : [Fab](https://a360.co/4mOqgvm), [boîtier de commande](https://a360.co/46sqwel)
- Discord Mekanika : <https://discord.gg/n7RsBtUdGc>

## Contenu

```
fab-diy/
├── bom/
│   ├── commandes/           Listes de commande par fournisseur (générées)
│   ├── fab-diy-bom.csv      Liste d'achat chiffrée : 191 lignes + port, fournisseur, lien, prix TTC
│   └── chiffrage/           Recherche de prix par lot (A structure, B guidage, C électronique, D visserie/acier)
├── cad/
│   ├── source/              STEP officiels (Git LFS, ~280 Mo, non versionnés)
│   ├── pcb-fins-de-course/  Carte des fins de course : Gerber, perçage, aperçu
│   ├── gabarits/            Gabarit de montage officiel (DXF, PMMA 3 mm, 60 × 60 mm)
│   └── steel/               Pièces acier extraites des STEP
│       ├── fab/             Machine : 13 DXF + STEP par pièce + parts.csv
│       ├── fab-cu/          Boîtier de commande : base + capot (tôle pliée)
│       ├── vfd-cu/          Boîtier du variateur : base + capot (tôle pliée)
│       ├── devis/           Dossier de demande de devis : zip des fichiers et liste des pièces
│       ├── diy/             Pièces redessinées : pattes de fixation des boîtiers (DXF + plan de pose)
│       └── preview.png      Aperçu de tous les DXF
├── docs/
│   ├── plan-d-action.md     Par où commencer : vérifications, devis, commandes, dans l'ordre
│   ├── budget.md            Synthèse du chiffrage France (~7 220 € TTC), fournisseurs alternatifs, variantes, points à régler
│   ├── verifications.md     Mesures dans le STEP : rainures, cornières, crémaillère, axe Y en tronçons, comptages
│   ├── profiles-coupe.md    Fiche de coupe et de taraudage des profilés, à joindre au devis
│   ├── devis-decoupe.md     Demande de devis pour la découpe laser : contenu du dossier, message type
│   ├── pignon-poulie.md     Fiche d'usinage du pignon-poulie de l'axe Y, cotes relevées dans le STEP
│   ├── plan-cablage.md      Câblage d'origine relevé dans les schémas, modifications, décisions à prendre
│   ├── boitier-commande.md  Implantation des ajouts de la boucle fermée dans le boîtier de commande
│   ├── carte-fins-de-course.md  Schéma décodé, câblage, composants, points à vérifier
│   └── pieces-acier.md      Correspondance nomenclature ↔ DXF, écarts, conseils de découpe
├── scripts/
│   ├── flatten_bom.py       Nomenclatures ERP imbriquées → liste d'achat
│   ├── price_bom.py         Fusionne bom/chiffrage/ dans la liste d'achat et totalise
│   ├── make_limits_pcb.py   Génère la carte des fins de course (Gerber) et vérifie les isolements
│   ├── make_orders.py       Listes de commande par fournisseur, à partir de la BOM
│   ├── make_laser_quote.py  Dossier de devis laser : liste des pièces et zip des fichiers
│   ├── make_cu_bracket.py   Patte de fixation des boîtiers : DXF et plan de pose
│   ├── extract_steel.py     STEP → DXF (plaques) / STEP (tôles pliées)
│   └── preview_dxf.py       Planche d'aperçu des DXF
├── upstream/fab/            Clone du dépôt officiel (nomenclatures, schémas, notice)
└── LICENSES/                CERN-OHL-S-2.0 et CC-BY-SA-4.0 (licences d'origine)
```

## Régénérer

```bash
# 1. Sources officielles (sans git-lfs : on prend les STEP via media.githubusercontent.com)
git clone https://github.com/mekanika-dev/fab.git upstream/fab
mkdir -p cad/source && cd cad/source && for f in "FAB V1.0.stp" "FAB-CU V1.0.stp" "VFD-CU V1.2.stp"; do
  curl -fL -o "$f" "https://media.githubusercontent.com/media/mekanika-dev/fab/main/cad/${f// /%20}"; done; cd ../..

# 2. Environnement Python (OpenCascade + ezdxf)
uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -r requirements.txt

# 3. Liste d'achat, puis chiffrage (les prix viennent de bom/chiffrage/*.csv)
python3 scripts/flatten_bom.py && python3 scripts/price_bom.py && python3 scripts/make_orders.py

# 4. Pièces acier (~1 min et ~2 Go de RAM pour le STEP principal)
.venv/bin/python scripts/extract_steel.py "cad/source/FAB V1.0.stp"   cad/steel/fab
.venv/bin/python scripts/extract_steel.py "cad/source/FAB-CU V1.0.stp" cad/steel/fab-cu
.venv/bin/python scripts/extract_steel.py "cad/source/VFD-CU V1.2.stp" cad/steel/vfd-cu
.venv/bin/python scripts/preview_dxf.py cad/steel cad/steel/preview.png
```

## Feuille de route

**Par où commencer : [`docs/plan-d-action.md`](docs/plan-d-action.md).**

- [x] Récupérer les fichiers officiels (nomenclatures, STEP, schémas, notice)
- [x] Liste d'achat aplatie avec catégories
- [x] DXF des plaques acier + STEP des tôles pliées
- [x] Chiffrer la liste d'achat pour la France : ~7 220 € TTC, voir `docs/budget.md`
- [x] Goussets : 14, positions relevées dans le STEP (`docs/verifications.md`)
- [x] Profilés 30×60 de 1410 mm : 11, confirmé par le guide de montage officiel (`docs/verifications.md`, section 9)
- [x] Fixation des boîtiers : posés à plat sur les deux traverses basses avant, comme dans le guide officiel pour ce châssis. Pattes facultatives, voir `docs/pieces-acier.md`
- [x] Vérifier rainures, cornières et crémaillère dans le STEP : voir `docs/verifications.md`
- [ ] Régler les points restants de `docs/budget.md`. Faits : vis X (1500 mm confirmés), poulie Y (5M 80 dents), implantation du boîtier. Plan de câblage rédigé (`docs/plan-cablage.md`, choix faits dans le lot K). Fiche d'usinage du pignon-poulie (`docs/pignon-poulie.md`). Restent : trouver l'atelier (pignon-poulie, brochage des poulies moteur), devis de port
- [ ] Devis réel découpe laser et pliage. Dossier prêt à envoyer : `docs/devis-decoupe.md`
- [ ] Profilés : devis coupe à longueur + taraudage M6 aux extrémités. Fiche prête : `docs/profiles-coupe.md`
- [ ] Électronique : carte des fins de course. Redessinée, Gerber prêts (`docs/carte-fins-de-course.md`) ; à vérifier avec une embase en main, puis à faire fabriquer
- [x] Choix du contrôle : PlanetCNC Mk3/4 sur le Raspberry Pi 5 (comme l'original), moteurs en boucle fermée
- [ ] Gabarits de montage : DXF copié dans `cad/gabarits/`, à faire découper (PMMA 3 mm)
- [ ] Montage en suivant le guide officiel

## Points ouverts

- **La broche n'est pas dans la nomenclature.** Seul le variateur y figure ; trois lignes ont été ajoutées à la main dans la BOM (broche, pinces ER20, support).
- **Carte des fins de course :** Mekanika ne publie que le schéma. La carte est redessinée dans `cad/pcb-fins-de-course/`, mais elle n'a pas encore été fabriquée ni essayée.
- **PlanetCNC n'est pas libre.** Le contrôleur Mk3/4 et sa licence sont à acheter chez PlanetCNC. Le projet le garde, comme l'original : grblHAL a été étudié puis écarté (voir `docs/budget.md`).

## Licence

Les fichiers d'origine sont © 2025 Mekanika SRL :
- **CAO :** CERN-OHL-S-2.0.
- **Nomenclatures et docs :** CC-BY-SA-4.0.

Les DXF/STEP extraits ici sont des dérivés et restent sous **CERN-OHL-S-2.0**. Usage personnel libre. Si tu distribues ou vends une machine dérivée, tu dois publier tes sources modifiées sous la même licence.
Le nom et le logo Mekanika ne sont pas couverts par ces licences.
