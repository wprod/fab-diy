# Plan d'action : quoi faire, dans quel ordre

Tout ce qui pouvait être vérifié dans les fichiers officiels l'a été. Ce qui reste se fait pièces en main, ou auprès des fournisseurs.
Les listes de commande par fournisseur sont dans [`bom/commandes/`](../bom/commandes/README.md).

## Étape 1 : lever les derniers doutes (gratuit, une soirée)

| À faire | Pourquoi | Où regarder |
|---|---|---|
| ~~Compter les profilés 30×60 de 1410 mm~~ | **Fait : 11**, confirmé par le guide officiel | [verifications.md](verifications.md), section 9 |
| ~~Vérifier la pose des boîtiers~~ | **Fait :** à plat sur les deux traverses basses avant, sans patte | [pieces-acier.md](pieces-acier.md) |
| ~~Savoir quel connecteur d'axe pilote X, Y1 et Y2~~ | **Fait :** Axis 1 = X, 2 = Y1, 3 = Z, 4 = Y2, d'après le profil PlanetCNC de Mekanika | [reglages-planetcnc.md](reglages-planetcnc.md) |

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

### À prévoir en plus, hors BOM

La BOM s'arrête à la machine. Pour s'en servir, il faut aussi :

- **un écran HDMI, un clavier et une souris** pour le Raspberry Pi. Le kit officiel propose en option un pavé Bluetooth et un écran tactile ; n'importe quel écran et clavier font l'affaire ;
- **des fraises** à queue de 6 ou 8 mm pour la Makita, dont une fraise à surfacer pour dresser le martyr ;
- **des brides de serrage** (les inserts M8 du martyr sont comptés, pas les brides) ;
- **une aspiration** et des protections : lunettes, casque antibruit, masque à poussières.

## Étape 4 : les grosses commandes

À passer une fois les devis de l'étape 2 reçus. Par ordre de montant :

| Commande | Montant | À préparer avant |
|---|---:|---|
| Profilés et accessoires, Dold (aluprofile-express.de) | ~1 690 € | [profiles-coupe.md](profiles-coupe.md) |
| Crémaillères, DamenCNC et Dold | ~1 400 € port compris | devis de port |
| Rails, patins et paliers, Sorotec | ~890 € | confirmation des rails aboutés |
| Acier découpé | ~590 € estimés, port compris | devis retenu |
| Moteurs et drivers, StepperOnline | ~450 € | lien exact du kit NEMA 23 ; stock |
| Contrôleur et licence, PlanetCNC | ~240 € | — |
| Vis à billes X et Z et autres pièces, AliExpress (entrepôt UE) | ~127 € estimés pour 8 articles | celle de X en **1500 mm hors tout**, pas 1450 ([verifications.md](verifications.md), section 6) |

Le reste (visserie, électricité, câbles) représente une quinzaine de petites commandes.

## Étape 5 : à la réception, avant de monter

- **Profilés :** vérifier que les pièces d'une même longueur sont identiques entre elles.
- **Boîtier de commande :** présenter l'alimentation 48 V, le driver CL57T, le contacteur et la prise de la Makita dans la tôle avant de percer ([boitier-commande.md](boitier-commande.md)).
- **Palpeur Z :** vérifier qu'il fonctionne en 5 V.
- **Drivers :** les régler sur 6400 impulsions par tour, et noter le type de la sortie alarme (ouverte ou fermée au repos).
- **Pieds en caoutchouc :** mesurer leur diamètre (17 mm attendus).

## Étape 6 : montage

Suivre le guide officiel Mekanika (support.mekanika.io), avec [notes-de-montage.md](notes-de-montage.md) à côté : cette page liste tout ce qui diffère pour cette machine. En résumé :

- **le châssis est l'ancienne version** : aux étapes 2, 9 et 12 du chapitre 1, le « support du boîtier de commande » n'est pas monté à 500 mm de haut, il devient une troisième traverse basse ([verifications.md](verifications.md), section 9) ;
- le boîtier de commande se pose à plat sur les deux traverses basses avant ;
- l'axe Y est en deux moitiés, le bout taraudé des 30×120 vers l'extérieur ([verifications.md](verifications.md), section 4) ;
- les 14 goussets et leurs positions ([verifications.md](verifications.md), section 5) ;
- les gabarits se font soi-même : 2 barres de MDF de 18 mm longues de 322,5 mm, et le petit gabarit PMMA de `cad/gabarits/` ;
- la partie 230 V est à faire relire avant la première mise sous tension ([plan-cablage.md](plan-cablage.md)).

## Étape 7 : logiciel et premier essai

Installer PlanetCNC sur le Raspberry Pi 5 (l'image de Mekanika est prévue pour le Pi 4B : deux voies sont décrites), importer le profil de Mekanika, puis suivre [reglages-planetcnc.md](reglages-planetcnc.md) : ce qu'il faut adapter, et l'ordre des vérifications avant la première prise d'origine.
