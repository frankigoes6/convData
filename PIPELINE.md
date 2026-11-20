# Pipeline BODACC — ce qui a été construit et comment le rejouer

Document de travail pour les agents IA. Le rendu évalué est le dépôt
`BigData_Braud_Bretonne_Vautrin` ; ce fichier explique la chaîne, les chiffres
obtenus et les pièges rencontrés.

## 1. Vue d'ensemble

```text
S3 raw/bodacc/                 (4,49 Mo, 1 992 annonces)
   │  quality.py       métriques de qualité, aucune correction
   │  build.py         aplatit le JSON-texte, type, dédoublonne  → clean.parquet
   │  enrich_naf.py    SIREN → code NAF (API SIRENE, cache)      → naf.parquet
   │  aggregate.py     jointure + 3 tables analytiques           → agg_*.parquet
   │  verify.py        recalcul indépendant en Python pur
   │  measure.py       CSV vs Parquet, pandas vs DuckDB
   └─ upload_s3.py      dépôt de raw/ et processed/ sur S3
```

Tout tourne avec **DuckDB** (SQL + Parquet) et la bibliothèque standard pour le
parsing : aucun cluster Spark, 4,5 Mo tiennent en mémoire.

## 2. Environnement

```bash
cd BigData_Braud_Bretonne_Vautrin
uv venv .venv && . .venv/bin/activate
uv pip install -r requirements.txt   # duckdb, pandas, pyarrow, boto3, requests
```

Pour le rapport uniquement : `uv pip install weasyprint pypdf`, puis
`weasyprint docs/rapport.html docs/rapport.pdf`.

## 3. Étapes et sorties attendues

| Commande | Sortie | Résultat mesuré |
|---|---|---|
| `python src/quality.py` | `data/quality_report.json` | 1 992 annonces, 32 colonnes, 70 SIREN absents, 0 date invalide, 1 doublon métier |
| `python src/build.py` | `out/clean.parquet` | 1 991 lignes, 703 ouvertures, 1 922 SIREN renseignés |
| `python src/enrich_naf.py` | `data/sirene_naf.json`, `out/naf.parquet` | 1 903 / 1 904 SIREN avec NAF |
| `python src/aggregate.py` | `out/agg_{mois_dept,secteur,saisonnalite}.parquet` | Paris 234, G Commerce 143, indice max 1,417 (octobre) |
| `python src/verify.py` | sortie console, code ≠ 0 si écart | 45 = 45 ouvertures (75 / 2023) |
| `python src/measure.py` | sortie console | CSV 0,76 Mo vs Parquet 0,13 Mo (5,9×), 39 ms vs 1,1 ms |
| `python src/upload_s3.py --processed` | objets S3 | 8 objets sous `raw/` et `processed/` |

Chiffres de référence (à ne pas « redécouvrir ») :

- 703 ouvertures = liquidation 506 + redressement 121 + conversion 68 + sauvegarde 9,
  après retrait des 450 clôtures, 203 états de créances, 442 ventes sans jugement.
- 632 ouvertures seulement sont exploitables par secteur (71 sans NAF).
- Paris = 234 ouvertures, soit un tiers du total ; 93 = 102, 77 = 94.
- Part de liquidations par section : 58,3 % (immobilier) à 89,1 % (services administratifs).
- Saisonnalité : creux août 0,43, pic octobre 1,42.

## 4. Modèle de données (`out/clean.parquet`)

| Colonne | Origine / traitement |
|---|---|
| `annonce_id`, `date_parution`, `famille`, `type_avis` | champs plats BODACC |
| `tribunal`, `departement`, `departement_nom`, `region`, `ville` | `numerodepartement` forcé sur 2 caractères |
| `siren`, `denomination`, `activite`, `forme_juridique` | extraits de `listepersonnes` (JSON-texte) |
| `nature_jugement`, `procedure`, `date_jugement` | extraits de `jugement` (JSON-texte) |
| `annee`, `mois`, `est_ouverture` | dérivés ; `est_ouverture` = liquidation, redressement, sauvegarde, conversion |

Règles de normalisation dans `src/common.py` : `procedure_type()` mappe 15 libellés
de jugement vers 9 types, `naf_section()` mappe la division NAF vers les 21 sections.

## 5. Layout S3

```text
s3://user-d-vautrinseing-ece/
├── code/            # scripts déposés pour exécution dans le pod
├── raw/bodacc/      # bodacc_idf_2022_2025.json (4 492 395 o), manifeste, README
└── processed/bodacc/
    ├── clean/clean.parquet         129 956 o
    ├── naf/sirene_naf.json         197 540 o
    └── agg/agg_*.parquet           3 fichiers
```

Endpoint `s3.seaweedfs.adm.adaltas.cloud`, région `us-east-1`, bucket = namespace.
Les identifiants sont des jetons STS injectés par Onyxia (12 h de validité) :
ne jamais les écrire dans le dépôt.

## 6. Exécution sur le cluster (procédure réellement utilisée)

1. Catalogue Onyxia → `Jupyter-python`, nom `bodacc`, ressources par défaut.
2. Attendre `Running services` (compter plusieurs minutes : image volumineuse).
3. Ouvrir JupyterLab avec le mot de passe affiché dans « Service access ».
4. Lancer les étapes dans le pod (`/home/onyxia/work/bodacc`) : les scripts y sont
   téléchargés depuis `s3://…/code/` et le brut depuis `s3://…/raw/bodacc/`.
5. Preuve : `evidence/05_execution_cluster.jpeg` (date, hôte, namespace, DuckDB 1.5.5,
   les 5 étapes, vérification OK).

## 7. Pièges rencontrés (utiles à la prochaine session)

- **Quota / scheduling** : `0/9 nodes are available: 3 Insufficient cpu` → deux services
  sont restés Pending ~45 min. Relancer avec 50m CPU / 200Mi suffit ; vérifier d'abord
  qu'aucun ancien service ne tourne.
- **Suppression accidentelle** : sur une carte « Mes services », le 2ᵉ bouton icône est
  *supprimer* (confirmation « Yes, delete »), pas un menu. Ne jamais cliquer à l'aveugle.
- **SPA Onyxia** : chaque route met ~8-10 s à rendre ; lire le DOM trop tôt donne une page
  vide. Les routes utiles : `/s3/<bucket>/<préfixe>/`, `/my-services`, `/catalog/all`.
- **Presse-papier** inaccessible (`document.hasFocus=false`) : passer par le DOM ou boto3.
- **DuckDB 2.0** : `con.sql(...).fetchone()` n'existe plus → `con.execute(...)`.
- **`git clone -q … || (cd repo && git pull)`** masque l'échec du clone : vérifier `ls repo/src`.
- **Notebook déjà ouvert** : réécrire le fichier via l'API ne rafraîchit pas l'onglet et
  JupyterLab peut réécrire l'ancien buffer ; créer un nouveau nom de fichier.
- **Push impossible** : `convData` et `BigData_Braud_Bretonne_Vautrin` appartiennent au même
  compte GitHub (`frankigoes6`) ; `VtnDenis` n'est collaborateur d'aucun des deux → 403.
  Ne pas créer de fork ni de dépôt de substitution sans demande explicite.

## 8. Ce qui reste ouvert

- [ ] Permissions GitHub puis `git push origin main` (9 commits locaux).
- [ ] Contributions visibles de Frank et Mathis (exigées par l'énoncé).
- [ ] Adresse de rendu inconnue : le destinataire du mail n'est pas dans l'énoncé.
- [ ] Service `bodacc3` (631654) à arrêter ; `bodacc2` Pending à supprimer.
- [ ] `vscode-pyspark-892194` supprimé par erreur : recréer le service si le volume existe.
