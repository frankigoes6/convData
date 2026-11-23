# Données brutes : BODACC Île-de-France 2022-2025

Échantillon d'annonces BODACC (DILA, data.gouv.fr), calibré pour tenir sous 5 Mo.

| | |
|---|---|
| **Fichier** | `bodacc_idf_2022_2025.json` |
| **Taille** | 4,49 Mo, 1 992 annonces |
| **Période** | 2022-01-02 → 2025-12-31 |
| **Source** | https://www.data.gouv.fr/datasets/bodacc |
| **Licence** | Licence Ouverte / Open Licence Etalab 2.0 |
| **SHA-256** | `5266b50adfec0161ae8ae2b777674e15ac5b3f980086044d6ea380ac15987a10` |

Emplacement S3 (brut) : `s3://user-f-braud-ece/raw/bodacc_idf_2022_2025.json`.

## Filtres

- Départements d'Île-de-France : 75, 77, 78, 91, 92, 93, 94, 95 (`region_code = 11`)
- `publicationavis = A` (avis initial)
- `familleavis ∈ {collective, vente, conciliation}`
- `dateparution` entre 2022-01-01 et 2025-12-31

## Échantillonnage

L'univers filtré compte **171 755 annonces** (~360 Mo). Le fichier livré est un
échantillon systématique : 1 enregistrement sur 20 parcouru dans l'ordre
chronologique, puis sélection régulière de 1 992 annonces réparties sur les
4 années.

- Par année : 2022 : 411 · 2023 : 443 · 2024 : 531 · 2025 : 607
- Par famille : collective 1 549 · vente 442 · conciliation 1 (famille rare :
  214 annonces au total sur la période)

## Champs

32 champs (voir `bodacc_idf_2022_2025.manifest.json`). Les champs JSON
imbriqués sont stockés en texte et devront être aplatis au nettoyage :
`listepersonnes`, `listeetablissements`, `jugement`, `acte`,
`modificationsgenerales`, `radiationaurcs`, `depot`,
`listeprecedentexploitant`, `listeprecedentproprietaire`, `divers`,
`parutionavisprecedent`.

## Régénération

```bash
python3 src/fetch_bodacc.py
```
