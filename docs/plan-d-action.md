# Plan d'action : quoi faire, dans quel ordre

Tout ce qui pouvait être vérifié dans les fichiers officiels l'a été. Ce qui reste se fait pièces en main, ou auprès des fournisseurs.
Les listes de commande par fournisseur sont dans [`bom/commandes/`](../bom/commandes/README.md).

## Étape 1 : lever les derniers doutes (gratuit, une soirée)

| À faire | Pourquoi | Où regarder |
|---|---|---|
| Compter les profilés 30×60 de 1410 mm dans le guide de montage Mekanika | 11 dans le modèle 3D, 9 dans la nomenclature. La BOM en compte 11 | support.mekanika.io, ou le Discord Mekanika |
| Y vérifier aussi la pose des boîtiers sur les deux traverses basses avant | Les pattes ont été redessinées d'après les cotes, pas d'après le guide | [pieces-acier.md](pieces-acier.md) |
| Demander quel connecteur d'axe pilote X, Y1 et Y2 | Seul Z est nommé dans le schéma | [plan-cablage.md](plan-cablage.md) |

## Étape 2 : demander les devis (gratuit, réponses en quelques jours)

| Devis | Dossier prêt |
|---|---|
| Découpe laser de l'acier, auprès de 2 ou 3 découpeurs | [devis-decoupe.md](devis-decoupe.md) : zip, liste et message type |
| Pignon-poulie (2 pièces) et brochage des 2 poulies moteur, auprès d'un atelier d'usinage | [pignon-poulie.md](pignon-poulie.md) |
| Port DamenCNC pour les crémaillères de 2 m | estimé à 126 €, non publié |
| Sorotec : confirmer par écrit des rails de 1500 mm rectifiés en bout, pour être mis bout à bout | point 12 de [budget.md](budget.md) |

Ces devis portent sur environ 2 000 € d'estimations : ils décident si le budget tient.

## Étape 3 : les petites commandes qui débloquent la suite (environ 60 €)

1. **6 embases XLR Neutrik NC3FAV** : vérifier leur sens, puis commander le circuit imprimé des fins de course ([carte-fins-de-course.md](carte-fins-de-course.md)).
2. **Le support Ø65 de la Makita** : mesurer ses trous, à percer dans la plaque porte-broche.

## Étape 4 : les grosses commandes

À passer une fois les devis de l'étape 2 reçus. Par ordre de montant :

| Commande | Montant | À préparer avant |
|---|---:|---|
| Profilés et accessoires, Dold (aluprofile-express.de) | ~1 690 € | [profiles-coupe.md](profiles-coupe.md) ; nombre de 30×60 confirmé |
| Crémaillères, DamenCNC et Dold | ~1 400 € port compris | devis de port |
| Rails, patins et paliers, Sorotec | ~890 € | confirmation des rails aboutés |
| Acier découpé | ~570 € estimés | devis retenu |
| Moteurs et drivers, StepperOnline | ~450 € | lien exact du kit NEMA 23 ; stock |
| Contrôleur et licence, PlanetCNC | ~240 € | — |
| Vis à billes X | dans la commande Dold | **1500 mm hors tout**, pas 1450 ([verifications.md](verifications.md), section 6) |

Le reste (visserie, électricité, câbles) représente une quinzaine de petites commandes.

## Étape 5 : à la réception, avant de monter

- **Profilés :** vérifier que les pièces d'une même longueur sont identiques entre elles.
- **Boîtier de commande :** présenter l'alimentation 48 V, le driver CL57T, le contacteur et la prise de la Makita dans la tôle avant de percer ([boitier-commande.md](boitier-commande.md)).
- **Palpeur Z :** vérifier qu'il fonctionne en 5 V.
- **Drivers :** noter le type de la sortie alarme (ouverte ou fermée au repos).
- **Pieds en caoutchouc :** mesurer leur diamètre (17 mm attendus).

## Étape 6 : montage

Suivre le guide officiel Mekanika. Les particularités de cette version :

- l'axe Y est en deux moitiés, le bout taraudé des 30×120 vers l'extérieur ([verifications.md](verifications.md), section 4) ;
- les 14 goussets et leurs positions ([verifications.md](verifications.md), section 5) ;
- le gabarit de montage (`cad/gabarits/`, pièce de 60 × 60 mm en PMMA de 3 mm) sert de cale pour régler les capteurs et l'accouplement ;
- la partie 230 V est à faire relire avant la première mise sous tension ([plan-cablage.md](plan-cablage.md)).
