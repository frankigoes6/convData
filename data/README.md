# Dataset brut : BODACC Île-de-France 2022-2025

Fichier de données brutes extrait de l'API **BODACC, Annonces commerciales**
(DILA, publiée sur data.gouv.fr), filtré puis échantillonné pour tenir dans la
fourchette de taille imposée par le projet (1 à 5 Mo).

## Fichiers

| Fichier | Rôle |
|---|---|
| `bodacc_idf_2022_2025.json` | Données brutes (tableau JSON, 1 objet = 1 annonce) |
| `bodacc_idf_2022_2025.manifest.json` | Métadonnées machine (filtres, taille, SHA-256) |
| `../src/fetch_bodacc.py` | Script de génération reproductible |

## Caractéristiques

| | |
|---|---|
| **Taille** | 4 492 395 octets (**4,49 Mo**) |
| **Annonces** | **1 992** |
| **Période** | 2022-01-02 → 2025-12-31 |
| **SHA-256** | `5266b50adfec0161ae8ae2b777674e15ac5b3f980086044d6ea380ac15987a10` |
| **Source** | BODACC, annonces commerciales (DILA) |
| **API** | `https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/annonces-commerciales/exports/json` |
| **Licence** | Licence Ouverte / Open Licence Etalab 2.0 |

## Filtres appliqués

```text
dateparution >= '2022-01-01' AND dateparution < '2026-01-01'
AND publicationavis = 'A'                          -- avis initial (pas rectificatif)
AND familleavis IN ('collective', 'vente', 'conciliation')
AND region_code = 11                               -- Île-de-France
```

Départements couverts : 75, 77, 78, 91, 92, 93, 94, 95.

## Univers complet vs échantillon

Le filtre complet représente **171 755 annonces** (~360 Mo en JSON), soit bien
au-delà de la limite de 5 Mo. Le fichier livré en est un **échantillon
systématique** :

1. parcours chronologique complet (`ORDER BY dateparution, id`) ;
2. conservation de 1 enregistrement sur 20 (8 588 candidates) ;
3. sélection régulière de **1 992 enregistrements** répartis uniformément sur
   les 4 années, à la taille maximale ≤ 4,5 Mo.

Répartition obtenue (proche de la population) :

| Année | Annonces |
|---|---|
| 2022 | 411 |
| 2023 | 443 |
| 2024 | 531 |
| 2025 | 607 |

| Famille | Échantillon | Population |
|---|---|---|
| `collective` | 1 549 | 133 317 (77,6 %) |
| `vente` | 442 | 38 224 (22,3 %) |
| `conciliation` | 1 | 214 (0,1 %) |

> ⚠️ **Limite à documenter** : la conciliation est très rare (214 annonces en
> 4 ans en IDF). L'échantillon proportionnel n'en contient qu'une. Pour une
> analyse dédiée à cette famille, relancer le script avec un échantillonnage
> stratifié (ou récupérer les 214 annonces exhaustivement).

## Schéma (32 champs)

Champs principaux : `id`, `publicationavis`, `parution`, `dateparution`,
`numeroannonce`, `typeavis`, `typeavis_lib`, `familleavis`,
`familleavis_lib`, `numerodepartement`, `departement_nom_officiel`,
`region_code`, `region_nom_officiel`, `tribunal`, `commercant`, `ville`,
`registre`, `cp`, `url_complete`.

Champs JSON **imbriqués, stockés en texte** (à aplatir à l'étape nettoyage) :
`listepersonnes`, `listeetablissements`, `jugement`, `acte`,
`modificationsgenerales`, `radiationaurcs`, `depot`,
`listeprecedentexploitant`, `listeprecedentproprietaire`, `divers`,
`parutionavisprecedent`.

## Reproduction

```bash
python3 src/fetch_bodacc.py
```

Le script télécharge les 171 755 annonces par mois (~3 min), échantillonne et
écrit le fichier + le manifeste dans `data/`. Aucune dépendance externe
(bibliothèque standard uniquement).

## Note

Données **brutes, non nettoyées** : doublons éventuels, formats de dates et
codes à normaliser, JSON imbriqué à aplatir. Voir la section « Nettoyage » du
`README.md` principal.
