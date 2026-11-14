# Plan de câblage

Deux parties :

1. **Le câblage d'origine**, relevé fil par fil dans les schémas officiels (`upstream/fab/docs/Control Unit FAB.qet` et `VFD unit.qet`).
2. **Ce que change cette version** : moteurs en boucle fermée, alimentation 48 V, coupure de puissance câblée, Makita à la place de la broche.

La partie 1 est lue dans les schémas. La partie 2 est une proposition. Les choix faits sont expliqués en partie 3, et les points à confirmer sur les notices sont en partie 4. Rien de tout cela n'a été câblé ni essayé.

> Le secteur 230 V est mortel. Si tu n'as pas l'habitude de câbler une armoire, fais relire la partie puissance par quelqu'un qui l'a.

## 1. Câblage d'origine

### Secteur et alimentations

| De | Vers |
|---|---|
| Embase C14, phase | fusible → interrupteur (L1 → T1) → L des alimentations 72 V et 24 V |
| Embase C14, neutre | interrupteur (L2 → T2) → N des deux alimentations |
| Embase C14, terre | terre des deux alimentations, tôle du boîtier, douille banane de mise à la terre |
| Alimentation 72 V, + et − | V+ et GND des 4 drivers |
| Alimentation 72 V, − | corps des 4 embases XLR moteur |
| Alimentation 24 V | ventilateur, carte des fins de course, PlanetCNC (+24V, GND), carte PWM (VCC), convertisseur 24 V → 5 V |
| Convertisseur 24 V → 5 V | USB-C du Raspberry Pi |

### Contrôleur vers drivers

Les drivers sont câblés en **cathode commune** : PUL−, DIR− et ENA− sont reliés ensemble au GND du connecteur d'axe ; les signaux arrivent sur PUL+, DIR+ et ENA+.

| Connecteur du PlanetCNC | Driver | Moteur |
|---|---|---|
| Axis 1 (STEP, DIR, ENA, GND) | driver du bas du schéma | **X** |
| Axis 2 | 3e driver | **Y1** |
| Axis 3 | 2e driver, nommé « Z » dans le schéma | **Z** |
| Axis 4 | 1er driver | **Y2** |

Seul l'axe Z est nommé dans le schéma. L'attribution de X et de Y vient du profil PlanetCNC publié par Mekanika, où les sorties 2 et 4 pilotent toutes deux l'axe Y ([reglages-planetcnc.md](reglages-planetcnc.md)).

Les sorties d'alarme des drivers (ALM+, ALM−) ne sont pas câblées dans l'original.

### Drivers vers moteurs (embases XLR 4 broches)

| Borne du driver | Broche XLR 4 |
|---|---|
| A+ | 2 |
| A− | 1 |
| B+ | 3 |
| B− | 4 |
| *(corps de l'embase)* | − de l'alimentation 72 V |

Câbles moteur d'origine : X 340 cm, Y1 340 cm, Y2 530 cm, Z 570 cm. En façade, les embases sont dans l'ordre X, Y1, Z, Y2 en partant du ventilateur (plan de raccordement du guide officiel) ; les fiches métalliques sont celles des moteurs.

### Fins de course

Voir [carte-fins-de-course.md](carte-fins-de-course.md). En résumé :

| Carte des fins de course | Optocoupleur | PlanetCNC |
|---|---|---|
| Sortie 1 (les 2 capteurs X en série) | In1 → V1 | LIM1 |
| Sortie 2 (les 2 capteurs Y1 en série) | In2 → V2 | LIM2 |
| Sortie 3 (Z) | In3 → V3 | LIM3 |
| Sortie 4 (Y2) | In4 → V4 | LIM4 |
| | G côté sortie | GND |

Câbles capteurs d'origine : Y1− 180 cm, Y2− 270 cm, Y1+ 330 cm, X− 350 cm, X+ 530 cm, Z+ 580 cm.

### Entrées et sorties en façade (connecteurs GX12)

| Connecteur | Broche | Va vers |
|---|---|---|
| Arrêt d'urgence (2 broches) | 1 | GND du PlanetCNC |
| | 2 | entrée E-Stop du PlanetCNC, et broche 3 du connecteur laser |
| Palpeur Z (3 broches) | 1 | GND |
| | 2 | IN1 |
| | 3 | **+5 V** |
| Input 2 (2 broches) | 1 / 2 | IN2 / GND |
| Input 3 (2 broches) | 1 / 2 | IN3 / GND |
| Commande VFD (5 broches) | 1 | libre |
| | 2 | GND de la carte PWM |
| | 3 | sortie 0-10 V de la carte PWM (consigne de vitesse) |
| | 4 | OUT1 (marche broche) |
| | 5 | +5 V |
| Commande laser (5 broches) | 1 | OUT6, relié aussi à l'entrée PWM de la carte PWM |
| | 2 | GND |
| | 3 | ligne d'arrêt d'urgence |
| | 4 | OUT2 |

IN4 est libre. Le PlanetCNC est relié au Raspberry Pi par son port USB-B.

### Boîtier VFD d'origine

| De | Vers |
|---|---|
| C14 avec filtre → interrupteur → disjoncteur 10 A | entrées R et S du variateur |
| Variateur U, V, W | embase Speakon vers la broche ; terre sur la 4e broche |
| GX12 broche 2 | ACM du variateur et masse du module relais 5 V |
| GX12 broche 3 | VI du variateur (consigne 0-10 V) |
| GX12 broche 4 | entrée IN du module relais |
| GX12 broche 5 | alimentation 5 V du module relais |
| Contact du module relais (COM, NO) | DCM et FOR du variateur (marche avant) |

## 2. Ce que change cette version

### Chaîne de puissance

```mermaid
flowchart LR
  C14[C14 + fusible] --> DJ[Disjoncteur 15 A]
  DJ --> A24[Alimentation 24 V]
  DJ --> K[Contacteur 25 A]
  K --> A72[Alimentation 72 V]
  K --> A48[Alimentation 48 V]
  K --> R[Relais 25 A]
  R --> M[Prise de la Makita]
  A24 --> CTRL[PlanetCNC, Pi, capteurs, ventilateur]
  A72 --> D86[3 drivers CL86T : X, Y1, Y2]
  A48 --> D57[Driver CL57T : Z]
```

- **Le 24 V reste hors contacteur** : après un arrêt d'urgence, le contrôleur, le Pi et les capteurs restent alimentés et la position est gardée.
- **Auto-maintien du contacteur :** la bobine est alimentée à travers le contact NF n° 1 de l'arrêt d'urgence, puis le bouton marche (NO) en parallèle avec un contact auxiliaire NO du contacteur. Après une coupure, rien ne repart sans appui sur le bouton marche.
- **Contact NF n° 2 de l'arrêt d'urgence :** vers l'entrée E-Stop du PlanetCNC, par le connecteur GX12 2 broches d'origine.
- **Tout ce circuit de commande est en 24 V** : la bobine du contacteur est en 24 V CC, alimentée par le 24 V du boîtier.

### Drivers en boucle fermée

| Liaison | Câblage |
|---|---|
| Signaux STEP, DIR, ENA | comme l'original, en cathode commune sur les mêmes connecteurs d'axe |
| Puissance des 3 CL86T | alimentation 72 V, comme l'original |
| Puissance du CL57T | alimentation **48 V** séparée. Ne jamais le relier au 72 V |
| Moteurs | comme l'original, par les XLR 4 broches : A+, A−, B+, B− |
| Codeurs | câble du kit + rallonge, jusqu'au bornier codeur de chaque driver, par presse-étoupe (voir [boitier-commande.md](boitier-commande.md)) |
| Alarmes | les 4 sorties ALM en parallèle sur **IN4**, retour au GND |

- **Rallonges codeur :** Y2 et Z ont des câbles moteur de 5,3 et 5,7 m ; prendre des rallonges de 5 m en plus des 1,7 m du kit. Les faire passer dans les chaînes avec les câbles moteur, blindage relié d'un seul côté, au boîtier.
- **Alarme :** c'est le gain principal de la boucle fermée sur un portique à deux moteurs. Si un driver décroche, la machine s'arrête au lieu de se mettre en travers.

### Arrêt d'urgence et bouton marche

| De | Vers |
|---|---|
| +24 V | GX12 « Input 3 » broche 1 → contact NF n° 1 de l'arrêt d'urgence → broche 2 |
| GX12 « Input 3 » broche 2 | bouton marche (NO), en parallèle avec le contact auxiliaire NO du contacteur |
| Sortie du bouton marche | bobine du contacteur (A1) ; A2 au 0 V |
| GX12 « E-Stop » broches 1 et 2 | contact NF n° 2 de l'arrêt d'urgence, comme l'original |

- Le connecteur « Input 3 » ne va donc plus à l'entrée IN3 du PlanetCNC : il sert à la boucle de la bobine. « Input 2 » reste libre.
- Un seul câble de 4 conducteurs part du bouton d'arrêt d'urgence et se termine par deux fiches GX12 2 broches.
- Le bouton marche est sur le boîtier de commande (perçage Ø22).

### Makita

Il n'y a pas de boîtier relais : tout est dans le boîtier de commande.

| De | Vers |
|---|---|
| Sortie du contacteur, phase et neutre | contacts du relais 25 A → prise 2P+T de la Makita, sur la paroi du fond |
| Terre | directement à la prise |
| OUT1 et +5 V du PlanetCNC | module relais 5 V (entrée IN et alimentation), comme dans le boîtier VFD d'origine |
| +24 V | contact du module relais 5 V → bobine du relais 25 A ; retour au 0 V |

Les connecteurs « Commande VFD » et la carte PWM ne servent pas avec la Makita. Ils restent utiles le jour où la broche 2,2 kW et son variateur remplacent l'affleureuse : il faudra alors découper le boîtier VFD et le câbler comme l'original.

## 3. Choix faits, et pourquoi

1. **Contacteur à bobine 24 V CC**, et non 230 V. Le bouton d'arrêt d'urgence est déporté au bout d'un câble : avec une bobine 230 V, ce câble et son connecteur GX12 porteraient le secteur. En 24 V, rien de dangereux ne sort du boîtier par ce câble.
2. **Arrêt d'urgence sur deux GX12 2 broches** déjà présents (« E-Stop » et « Input 3 »). Aucun connecteur à ajouter, seulement un câble de 4 conducteurs.
3. **Relais et prise de la Makita dans le boîtier de commande.** Un boîtier relais séparé aurait demandé une liaison secteur entre les deux boîtiers, avec une embase de sortie en plus. On économise aussi les tôles du boîtier VFD (environ 70 € avec son embase), reportées au jour où il y aura un variateur.
4. **Bouton marche sur le boîtier de commande.** Le mettre près de l'arrêt d'urgence serait un peu plus pratique, mais ajouterait 2 conducteurs et un boîtier de bouton.

Ces choix sont dans `bom/chiffrage/lot-K-cablage.csv`. Pour revenir en arrière, il suffit de supprimer ce fichier et de relancer `python3 scripts/price_bom.py`.

## 4. À confirmer sur les notices

- **Palpeur Z :** l'original l'alimente en **5 V**. Celui de la BOM est annoncé « 24 V, 3 fils ». Vérifier qu'il fonctionne en 5 V, ou l'alimenter en 24 V et s'assurer que sa sortie ne renvoie pas 24 V sur IN1.
- **Bornes des CL86T et CL57T :** noms et ordre des bornes codeur, et type de la sortie alarme (ouverte ou fermée au repos, réglable sur certains modèles). Le câblage en parallèle suppose une sortie qui se ferme en cas de défaut ; si elle s'ouvre, il faut câbler les 4 en série.
- **Entrées du PlanetCNC :** niveau actif de IN4 et de E-Stop, et type des sorties OUT1 (peut-elle commander directement le module relais ?).
- **Sections :** 1,5 mm² pour le secteur et le 72 V jusqu'aux drivers, 2,5 mm² entre contacteur, relais et prise de la Makita, 0,25 à 0,5 mm² pour les signaux. Embouts sertis sur tous les fils souples.
