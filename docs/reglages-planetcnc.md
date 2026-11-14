# Réglages PlanetCNC

Mekanika publie ses profils PlanetCNC, c'est-à-dire tous les réglages du logiciel pour chaque machine.
Cette page résume celui de la Fab Z250 et dit ce qu'il faut adapter pour cette version.

- **Source :** « PlanetCNC Mekanika Profiles (for v4.x) », fichier `FAB-Z250 261005-V4_2.zip`, sur le [centre de téléchargement Mekanika](https://support.mekanika.io/download-center/cnc-milling). Lu le 14 novembre 2026.
- Le profil n'est pas copié dans ce dépôt : il appartient à Mekanika, et il contient un fichier de licence lié à leur contrôleur. Télécharge-le chez eux.
- Il demande PlanetCNC TNG du 24 novembre 2025 ou plus récent.

**Le plus simple :** importer ce profil dans PlanetCNC, activer ta propre licence, puis corriger les quelques points de la dernière section.

## Quel connecteur pilote quel axe

C'était la dernière question ouverte du plan de câblage.

| Sortie moteur du contrôleur | Axe | Sens inversé |
|---|---|---|
| Axis 1 | **X** | non |
| Axis 2 | **Y** (moteur Y1) | oui |
| Axis 3 | **Z** | oui |
| Axis 4 | **Y** (moteur Y2, esclave) | non |

Les sorties 2 et 4 pilotent toutes deux l'axe Y : c'est le réglage du profil. Que la sortie 2 soit Y1 et la 4 Y2 se déduit des fins de course (Y1 sur l'entrée 2, Y2 sur l'entrée 4) ; le schéma ne le dit pas noir sur blanc. Si la mise d'équerre du portique bouge le mauvais côté, il suffit d'échanger les deux fiches moteur Y.

## Pas par millimètre : les drivers à 6400 impulsions par tour

| Axe | Pas par mm | D'où ça vient |
|---|---:|---|
| X | 320 | vis à billes au pas de 20 mm : 6400 / 20 |
| Y | 271,7 | pignon de 30 mm de diamètre primitif, réduction de 4 : 6400 × 4 / (π × 30) = 271,6 |
| Z | 1280 | vis à billes au pas de 5 mm : 6400 / 5 |

Ces valeurs supposent des drivers réglés sur **6400 impulsions par tour** (micropas 32). C'est le réglage à reproduire sur les CL86T et le CL57T, avec leurs interrupteurs.

Elles confirment aussi la mécanique : vis X au pas de 20 (SFS1620), vis Z au pas de 5 (SFU1605), pignon de 15 dents au module 2 et réduction de 4.

## Vitesses et courses

| Réglage | X | Y | Z |
|---|---:|---:|---:|
| Vitesse maximale | 250 mm/s (15 000 mm/min) | 250 mm/s | 50 mm/s (3 000 mm/min) |
| Accélération | 250 mm/s² | 250 mm/s² | 250 mm/s² |
| Course logicielle | 5 à 1335 mm | 5 à 2700 mm | 0 à 110 mm |

Vitesse de déplacement rapide du programme : 18 000 mm/min.

## Entrées et sorties

| Fonction | Réglage du profil |
|---|---|
| Fins de course X (les 2 capteurs en série) | entrée LIM1, inversée |
| Fins de course Y1 | entrée LIM2, inversée |
| Fin de course Z (en haut) | entrée LIM3, inversée |
| Fin de course Y2 | entrée LIM4, inversée ; sert à la mise d'équerre du portique |
| Un fin de course atteint | déclenche l'arrêt d'urgence logiciel |
| Arrêt d'urgence | activé, inversé (contact normalement fermé) |
| Palpeur d'outil | entrée IN1, vitesse de palpage 150 mm/min |
| Marche broche | sortie OUT1, temporisation de 5 s au démarrage et à l'arrêt |
| Vitesse de broche | sortie OUT6 en PWM, 24 000 tr/min au maximum |

Tout cela correspond au [plan de câblage](plan-cablage.md) et à la [carte des fins de course](carte-fins-de-course.md).

## Prise d'origine

- Ordre : Z d'abord (vers le haut), puis X, puis Y.
- Vitesses : 2000 mm/min en approche, 1000 mm/min en reprise.
- Après la prise d'origine : X et Y reculent à 10 mm, Z redescend à 105 mm.
- Mise d'équerre du portique : sur l'axe Y, à 300 mm/min, avec un recul de 10 mm.

## Ce qu'il faut adapter pour cette version

| Réglage | Dans le profil | À faire |
|---|---|---|
| Licence | celle de Mekanika | activer la tienne (achetée chez PlanetCNC) |
| Micropas des drivers | 6400 impulsions par tour | régler les CL86T et le CL57T sur 6400 |
| Sens des moteurs | sorties 2 et 3 inversées | à vérifier au premier essai : les moteurs en boucle fermée peuvent tourner dans l'autre sens que ceux d'origine |
| Vitesse de broche | PWM sur OUT6, 24 000 tr/min | sans effet avec la Makita : sa vitesse se règle à la molette |
| Marche broche | OUT1, 5 s de temporisation | inchangé : OUT1 commande le relais de la Makita |
| Alarme des drivers | absente | affecter l'entrée IN4 à un arrêt (pause ou arrêt d'urgence), une fois le type de sortie des drivers connu |
| Vitesses et accélérations | prévues pour des moteurs en boucle ouverte | garder ces valeurs pour commencer, ne les augmenter qu'après essais |

## Premier essai, portique libre

1. Débrayer les deux pignons de la crémaillère, ou commencer à très basse vitesse.
2. Vérifier chaque fin de course à la main (un objet en acier devant le capteur) : l'entrée doit changer d'état dans PlanetCNC.
3. Vérifier l'arrêt d'urgence : la puissance doit tomber et le logiciel doit le signaler.
4. Déplacer chaque axe de 10 mm et vérifier le sens, puis la distance réelle sur 100 mm.
5. Seulement ensuite, lancer une prise d'origine, la main sur l'arrêt d'urgence.
