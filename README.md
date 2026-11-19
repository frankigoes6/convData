# Plan de projet : Défaillances d'entreprises (BODACC)

**Rendu : vendredi 4 décembre 2026** (mail + PDF + dépôt Git public)
**Dépôt : `bigdata_project`** (public, ≥ 10 commits sur plusieurs jours, 2 contributeurs)

## 0. Cadrage (à figer en premier)

- [ ] **Question de recherche (3 phrases max)** :
  > Quels secteurs (NAF) et quelles régions concentrent le plus d'ouvertures de procédures collectives sur [période] ? Observe-t-on une saisonnalité mensuelle ? Certains secteurs ont-ils une part de liquidations plus élevée ?
- [ ] **Périmètre** : type d'annonce = procédures collectives, [région ou départements], [1 à 3 ans]
- [ ] **Taille brute cible** : entre 1 et 5 Mo (à mesurer après téléchargement)
- [ ] **Outils retenus** : stockage S3 Onyxia, traitement [Spark / DuckDB / SQL], format de sortie Parquet
- [ ] **Vérification indépendante** : chiffre de référence (site BODACC ou série INSEE)

## 1. Mise en place

- [ ] Créer le dépôt `bigdata_project` (public), ajouter le binôme en collaborateur
- [ ] Vérifier `git config user.name` / `user.email` chez les deux
- [ ] Créer l'arborescence : `README.md`, `evidence/`, `src/`, `k8s/`
- [ ] Lancer un service Onyxia (VSCode / Jupyter) et tester l'accès S3
- [ ] Créer le bucket et les préfixes : `raw/bodacc/`, `processed/bodacc/`

## 2. Ingestion

- [ ] Script de téléchargement dans `src/` (API ou export CSV de la DILA)
- [ ] Noter : URL, licence, date de téléchargement, taille exacte
- [ ] Dépôt du brut dans `s3://<bucket>/raw/bodacc/`
- [ ] 📸 Capture : contenu du bucket (brut)

## 3. Exploration et qualité des données

À chiffrer pour le rapport (nombre de lignes touchées à chaque fois) :
- [ ] Nombre total de lignes et de colonnes brutes
- [ ] Doublons (même procédure annoncée plusieurs fois, rectificatifs)
- [ ] Dates dans des formats différents ou invalides
- [ ] Codes NAF manquants ou invalides
- [ ] SIREN mal formatés
- [ ] Champs JSON imbriqués à aplatir
- [ ] Libellés de tribunaux, départements ou régions incohérents

## 4. Nettoyage et transformation

- [ ] Aplatir le JSON, typer les colonnes
- [ ] Dédoublonner, normaliser dates et codes
- [ ] Rattacher département → région (table de référence)
- [ ] Rattacher NAF → grand secteur (table de référence)
- [ ] Normaliser les types de procédure (sauvegarde, redressement, liquidation)
- [ ] Écrire le dataset nettoyé dans `processed/bodacc/clean/` (Parquet)

## 5. Agrégations (cœur de l'analyse)

- [ ] Nombre de défaillances par secteur × région × mois
- [ ] Classement des secteurs et des régions
- [ ] Indice de saisonnalité (écart d'un mois à la moyenne annuelle)
- [ ] Part de liquidations par secteur
- [ ] Écrire les tables finales dans `processed/bodacc/agg/` (Parquet)
- [ ] 📸 Capture : contenu du bucket (traité)

## 6. Vérification indépendante

- [ ] Choisir un résultat (ex. nombre de jugements d'un département sur un mois)
- [ ] Le recalculer autrement (Python pur, site BODACC ou série INSEE)
- [ ] Comparer, expliquer l'écart éventuel
- [ ] 📸 Capture de la comparaison

## 7. Mesures pour justifier les choix techniques

À mesurer vous-mêmes (temps d'exécution, taille) :
- [ ] CSV vs Parquet (taille et temps de lecture)
- [ ] Outil A vs outil B (ex. Spark vs DuckDB)
- [ ] Au moins une alternative écartée, avec la raison chiffrée

## 8. Preuves d'exécution

Chaque capture doit montrer **namespace/ID Onyxia + date + heure**, et être numérotée.
- [ ] `01_bucket_raw.png`
- [ ] `02_ingestion_trace.png`
- [ ] `03_nettoyage_trace.png`
- [ ] `04_agregation_trace.png`
- [ ] `05_bucket_processed.png`
- [ ] `06_verification.png`
- [ ] Une trace d'exécution par composant utilisé (Spark, job k8s, etc.)

## 9. README (1 page, dans cet ordre)

- [ ] Auteurs (NOM, Prénom)
- [ ] Prérequis
- [ ] Dataset : nom, URL, licence, date de téléchargement, taille
- [ ] Problématique (3 phrases max)
- [ ] Chemins S3 (brut et traité)
- [ ] Procédure de reproduction pas à pas (commandes, redémarrage)

## 10. Rapport PDF (4 pages max, annexes comprises)

- [ ] Problématique, justification, description du dataset (source, taille, schéma)
- [ ] Schéma du workflow + choix techniques + alternatives écartées (mesures à l'appui)
- [ ] Problèmes de qualité (exemples réels, nombre de lignes, traitement)
- [ ] Résultats et limites
- [ ] Et avec un dataset 100× plus gros (partitionnement, Spark distribué, skew, Parquet)
- [ ] Preuves référencées dans le texte
- [ ] Lien du dépôt Git
- [ ] Initiatives supplémentaires décrites

## 11. Envoi

- [ ] Sujet : `Ecosystème Big Data II - GrXX - NOM1 Prénom1 - NOM2 Prénom2`
- [ ] PDF joint, 4 pages max, lien Git inclus
- [ ] Relecture croisée avant envoi

## Répartition proposée (à ajuster)

| Étape | Personne 1 | Personne 2 |
|---|---|---|
| Cadrage, mise en place | ✅ | ✅ |
| Ingestion + S3 | ✅ | |
| Exploration / qualité | | ✅ |
| Nettoyage | ✅ | |
| Agrégations | | ✅ |
| Vérification + mesures | ✅ | ✅ |
| README | | ✅ |
| Rapport | ✅ | ✅ |

> Chacun doit avoir des commits visibles : commitez par étape, pas tout d'un coup à la fin.

## Calendrier proposé

| Dates | Objectif |
|---|---|
| 19-21 nov | Cadrage, dépôt, accès S3, ingestion |
| 22-25 nov | Exploration, qualité, nettoyage |
| 26-29 nov | Agrégations, vérification, mesures |
| 30 nov - 1er déc | Captures, README |
| 2-3 déc | Rapport PDF, relecture |
| **4 déc** | **Envoi (avec marge de sécurité : -1 pt par jour de retard)** |

## 12. Stockage S3 — état et mise en place pour Bretonne et Vautrin

**Bucket de référence : `user-f-braud-ece`** (bucket personnel Onyxia de Braud).

```text
s3://user-f-braud-ece/
├── raw/
│   └── bodacc_idf_2022_2025.json     # 4,49 Mo — 1 992 annonces (brut)
└── processed/
    └── bodacc/                       # à créer : clean/ et agg/
```

### Peut-on tous travailler sur le même S3 ?

**Oui**, de deux façons :

1. **Un bucket partagé** (le plus simple pour le rendu) : les trois membres
   utilisent `user-f-braud-ece` avec **la même paire de clés S3**
   (*Mon compte → Mes clés S3*).
   - Avantages : un seul chemin à documenter, preuves cohérentes, pas de
     duplication des 4,5 Mo.
   - Limites : une seule identité (pas de traçabilité par personne), et si le
     propriétaire du bucket quitte le groupe, l'accès est perdu.
   - **Ne jamais committer les clés** ; les révoquer en fin de projet.
2. **Un bucket par personne, même arborescence** : chacun crée `raw/` et
   `processed/` dans son bucket personnel et y copie les données. Le README
   documente `user-f-braud-ece` comme bucket de référence ; chaque membre peut
   rejouer le pipeline chez lui.
   - Avantages : accès indépendant, traçabilité.
   - Limite : les chemins S3 diffèrent d'une personne à l'autre (le rapport doit
     préciser lequel a servi aux captures).

> Pour la correction, le plus lisible reste **un bucket de référence unique**
> (option 1), avec les captures faites dessus.

### Procédure identique pour Bretonne et Vautrin

1. **Récupérer le dépôt et les données** :
   ```bash
   git clone git@github.com:frankigoes6/BigData_Braud_Bretonne_Vautrin.git
   cd BigData_Braud_Bretonne_Vautrin
   ```
2. **Récupérer les identifiants S3** : *Mon compte → Mes clés S3* (access key +
   secret key) et l'endpoint affiché à côté. Configurer le client :
   ```bash
   aws configure
   # Access Key / Secret Key / region us-east-1 / format json
   export S3_ENDPOINT="<endpoint indiqué dans Mon compte>"   # ex. https://minio.lab.sspcloud.fr
   ```
3. **Envoyer les données** :

   *Option 1 — bucket partagé (clés de Braud) :*
   ```bash
   aws s3 cp data/bodacc_idf_2022_2025.json \
     "s3://user-f-braud-ece/raw/" --endpoint-url "$S3_ENDPOINT"
   ```

   *Option 2 — bucket personnel :*
   ```bash
   BUCKET="<son-bucket>"
   aws s3 mb "s3://$BUCKET" --endpoint-url "$S3_ENDPOINT"
   aws s3 cp data/bodacc_idf_2022_2025.json \
     "s3://$BUCKET/raw/" --endpoint-url "$S3_ENDPOINT"
   ```

4. **Vérifier l'intégrité** :
   ```bash
   aws s3 ls "s3://user-f-braud-ece/raw/" --endpoint-url "$S3_ENDPOINT"
   # attendu : bodacc_idf_2022_2025.json  4492395 octets
   ```
   SHA-256 attendu :
   `5266b50adfec0161ae8ae2b777674e15ac5b3f980086044d6ea380ac15987a10`.

5. **Faire sa propre capture** `evidence/0X_bucket_raw_<nom>.png` (bucket,
   préfixe, fichier, ID et date/heure visibles) si le bucket est personnel.

> ⚠️ Les clés S3 ne doivent **jamais** apparaître dans le dépôt, le README ou
> une capture d'écran.

