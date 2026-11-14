# Découpe laser : dossier de demande de devis

Tout est prêt dans [`cad/steel/devis/`](../cad/steel/devis/) :

- **`fab-diy-decoupe-laser.zip`** : les fichiers rangés par épaisseur (DXF pour les plaques, STEP pour les tôles pliées) et la liste ;
- **`liste-decoupe.csv`** : une ligne par pièce, avec l'épaisseur, la quantité et les reprises à prévoir.

Pour le régénérer : `python3 scripts/make_laser_quote.py`.

## Contenu

| Épaisseur | Références | Pièces |
|---|---:|---:|
| 10 mm | 2 | 8 |
| 8 mm | 10 | 28 |
| 3 mm | 2 | 6 |
| 1,5 mm | 2 | 2 |
| **Total** | **16** | **44** |

Acier S235 partout (la nuance n'est pas indiquée par Mekanika : voir [pieces-acier.md](pieces-acier.md)).

Ne sont pas dans le dossier :
- les deux tôles du boîtier VFD, reportées tant que la Makita sert de broche ;
- le gabarit de montage en PMMA (`cad/gabarits/`), à demander à un découpeur de plastique ;
- le circuit imprimé des fins de course, qui se commande chez un fabricant de circuits ;
- la patte de blocage des boîtiers, facultative.

## Où demander

Les découpeurs en ligne donnent un prix dès le téléversement des fichiers : Laserboost, Xometry ou Fractory. Un métallier ou un chaudronnier local est souvent moins cher pour un lot comme celui-ci, et il peut faire les taraudages. Demander au moins deux devis : la fourchette estimée va de 320 à 850 €.

## Message à joindre

> Bonjour,
>
> Je souhaite un devis pour la découpe laser d'un lot de pièces en acier S235, pour une machine CNC que je construis à titre personnel.
>
> Le lot comprend 44 pièces en 16 références : 8 pièces en 10 mm, 28 en 8 mm, 6 en 3 mm et 2 en 1,5 mm. Les fichiers sont joints, rangés par épaisseur, avec la liste des quantités (liste-decoupe.csv).
>
> - Les plaques sont fournies en DXF à l'échelle 1, en millimètres.
> - Trois références sont des tôles pliées, fournies en STEP 3D : un support en 3 mm à 1 pli (4 pièces) et les 2 tôles d'un boîtier en 1,5 mm. Merci de me dire si vous faites le pliage, et le développé à partir du STEP.
> - Certains trous font moins que l'épaisseur de la tôle (Ø4,3 à Ø5,5 dans du 8 mm). Pouvez-vous les pointer au laser, ou les percer ?
> - Quelques trous sont à tarauder (M5, M6, M12 : voir la colonne « reprises » de la liste). Merci de chiffrer cette option à part.
> - Finition : brut, ébavuré. Merci de chiffrer en option un thermolaquage noir.
>
> Pouvez-vous m'indiquer le prix, le délai et les frais de livraison pour la France ?
>
> Merci d'avance.

## Avant d'envoyer

1. **Plaque porte-broche :** elle est dessinée pour une broche Ø80. Avec la Makita, les trous du support Ø65 sont à percer à la main dans la plaque de 8 mm, une fois le support reçu.
2. **Boîtier de commande :** aucune modification des tôles n'est nécessaire avant la découpe ([boitier-commande.md](boitier-commande.md)).
3. **Logo :** la plaque arrière du portique porte le logo Mekanika découpé. À garder pour un usage personnel, à retirer du DXF si tu comptes vendre la machine.
4. **Pattes des boîtiers :** elles ne sont plus dans le dossier. Le boîtier se pose à plat sur deux traverses, sans patte ([pieces-acier.md](pieces-acier.md)). La patte de blocage de `cad/steel/diy/` est facultative : l'ajouter au devis si tu veux visser le boîtier.
