# BigData_Braud_Bretonne_Vautrin

Projet **Écosystème Big Data II**, pipeline BODACC (défaillances d'entreprises) en
Île-de-France, 2022 à 2025.

## Auteurs

- BRAUD Frank
- BRETONNE Mathis
- VAUTRIN Denis

## Prérequis

- Python 3.11+ et `pip install -r requirements.txt`
- Un accès S3 Onyxia (identifiants injectés dans un service de la plateforme)
- `git`

## Dataset

| | |
|---|---|
| **Nom** | BODACC, annonces commerciales (DILA) |
| **Source** | https://www.data.gouv.fr/datasets/bodacc, Licence Ouverte Etalab 2.0 |
| **Téléchargé le** | 2026-11-19 |
| **Taille** | 4,49 Mo · 1 992 annonces · 32 champs (`data/bodacc_idf_2022_2025.json`) |
| **Périmètre** | Île-de-France, 2022-01-01 → 2025-12-31, avis initiaux, familles `collective` / `vente` / `conciliation` |

Le filtre complet représente 171 755 annonces (~360 Mo) : le fichier livré en est un
échantillon systématique (1 sur 20, puis sélection régulière) calibré pour la fourchette
1 à 5 Mo. Détail des filtres et des limites : `data/README.md`.

## Problématique

Quels départements d'Île-de-France et quels secteurs concentrent le plus d'ouvertures de
procédures collectives entre 2022 et 2025 ? Observe-t-on une saisonnalité mensuelle ? La
part de liquidations varie-t-elle selon le secteur ?

## Chemins S3

Bucket `s3://user-d-vautrinseing-ece/` (équivalent du namespace ; rejouable avec
`s3://user-<son-namespace>/`).

```text
raw/bodacc/        bodacc_idf_2022_2025.json + manifeste + fiche dataset
code/              scripts du pipeline, déposés pour le pod
processed/bodacc/  clean/clean.parquet · naf/sirene_naf.json · agg/agg_*.parquet
```

## Reproduction

```bash
git clone https://github.com/frankigoes6/BigData_Braud_Bretonne_Vautrin.git
cd BigData_Braud_Bretonne_Vautrin
pip install -r requirements.txt

python src/build.py       # aplatissement         -> out/clean.parquet
python src/enrich_naf.py  # SIREN -> NAF (cache)  -> out/naf.parquet
python src/aggregate.py   # 3 tables analytiques  -> out/agg_*.parquet
python src/upload_s3.py --processed   # dépôt sur S3 (identifiants Onyxia)
```

Reprise après interruption : `enrich_naf.py` repart de `data/sirene_naf.json` ; les
autres étapes réécrivent leurs sorties. Rapport : `docs/rapport.pdf`. Captures d'exécution : `evidence/`.
