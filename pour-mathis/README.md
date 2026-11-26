# Pour Mathis

Ce dossier contient ce qui a été retiré du dépôt de rendu, pour que tu puisses écrire
ta part : cinq morceaux de code, plus la documentation et le rapport.

Le dépôt concerné est `../BigData_Braud_Bretonne_Vautrin`. Le pipeline fonctionne
jusqu'à `build.py`, qui produit le fichier propre. Ce qui manque, c'est ce qui est
décrit ici.

Deux dossiers :

- `code/` : les versions de référence des scripts et de la fonction à réécrire.
- `reference/` : le README du rendu, le README des données, le rapport PDF et le rapport
  de qualité tels qu'ils étaient. À reprendre, pas à recopier tels quels.

## 1. Les quatre scripts à écrire

Les versions de référence sont dans `code/`. Elles marchent, mais tu n'es pas obligé de
les copier : tu peux écrire autrement, du moment que les sorties sont les mêmes. Ce qui
compte, ce sont les contrôles de la dernière colonne.

| Fichier à créer | Ce qu'il doit faire | Contrôle |
|---|---|---|
| `src/quality.py` | Compter ce qui ne va pas dans le fichier brut, sans rien corriger | doit écrire `data/quality_report.json` avec 1 992 lignes et les valeurs du tableau ci-dessous |
| `src/verify.py` | Recompter les ouvertures de Paris en 2023 sans DuckDB, en Python pur | doit afficher 45 et 45, et sortir en code d'erreur sinon |
| `src/aggregate.py` | Agréger `out/clean.parquet` et `out/naf.parquet` en trois tables : ouvertures par mois et département, par section NAF avec la part de liquidations, et indice de saisonnalité | Paris 234, Seine-Saint-Denis 102, Seine-et-Marne 94, `G Commerce` 143, `F Construction` 129 |
| `src/measure.py` | Comparer CSV et Parquet, puis pandas et DuckDB | Parquet autour de 0,13 Mo contre 0,76 Mo en CSV, et une lecture beaucoup plus rapide |

Valeurs attendues de `quality.py` : 1 992 lignes, 32 colonnes, 1 992 identifiants
uniques, 0 JSON invalide, 0 date invalide, 70 SIREN absents, 0 code NAF, 1 doublon métier,
familles `vente` 442, `collective` 1 549, `conciliation` 1.

## 2. La fonction NAF à écrire

`src/common.py` n'a plus de fonction `naf_section`. `enrich_naf.py` l'importe, donc tant
qu'elle manque, le script échoue. C'est normal.

Elle prend un code NAF (`"43.21A"`) et rend la section (`"F"`) avec son libellé. La table
des 21 sections est dans `code/naf_section.py` si tu veux t'en servir. Les bornes sont le
seul piège : la division est faite des deux premiers chiffres.

Contrôle : après avoir relancé `enrich_naf.py` puis `aggregate.py`, tu dois retrouver
1 903 NAF sur 1 904 SIREN, 688 ouvertures avec un secteur, et `G Commerce` en tête avec
143 ouvertures.

## 3. La documentation

Le dépôt garde `README.md` et `data/README.md` dans la version de Frank. Tu peux les
compléter (la partie pipeline et les commandes manquent), mais ne les réécris pas de
zéro et ne supprime pas son contenu.

Le `README.md` doit tenir sur une page et suivre cet ordre : auteurs, prérequis, dataset
(nom, URL, licence, date de téléchargement, taille), problématique en trois phrases,
chemins S3 pour le brut et le traité, procédure de reproduction avec les commandes.

Le `data/README.md` décrit le fichier brut : source, filtres, échantillonnage, schéma,
limites.

## 4. Le rapport

Le PDF est à refaire. Quatre pages maximum, en français, avec dans l'ordre : la
problématique et le dataset, un schéma du workflow et les choix techniques justifiés par
des mesures, les problèmes de qualité avec des exemples réels, les résultats et les
limites, ce qui changerait avec un jeu de données cent fois plus gros, et les preuves
d'exécution. Le lien du dépôt doit y figurer.

Toutes les preuves sont déjà dans `evidence/`. Elles montrent le namespace et l'heure.

## 5. Les chiffres à utiliser

Ils sont déjà vérifiés, ne pas les recalculer à la main.

| | |
|---|---|
| Annonces brutes | 1 992, 32 champs, 4,49 Mo |
| Après nettoyage | 1 991 lignes, 1 doublon supprimé |
| Ouvertures | 703, dont 505 liquidations, 121 redressements, 68 conversions, 9 sauvegardes |
| Ouvertures avec secteur | 688 |
| Paris | 234 ouvertures |
| Seine-Saint-Denis / Seine-et-Marne | 102 / 94 |
| G Commerce / F Construction | 143 / 129 |
| Part de liquidations | 58,3 % dans l'immobilier, 75 à 89 % ailleurs |
| Saisonnalité | août 0,43, octobre 1,42 |
| Vérification | 45 ouvertures à Paris en 2023, trouvées de deux façons |
| CSV contre Parquet | 0,76 Mo contre 0,13 Mo, lecture 39 ms contre 1,1 ms |

## 6. Règles

Ne modifie pas `build.py` ni le reste de `common.py` : le rapport et les
captures reposent sur leurs sorties. Si tu changes quelque chose là-dedans, il faut tout
relancer et corriger les chiffres partout.

Avant de pousser, lance `python src/verify.py` : il doit afficher deux fois 45.

Pour les commits : ton nom, un message court en français, et un commit par étape plutôt
qu'un seul gros à la fin.
