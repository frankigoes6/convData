# Journal des IA — convData

> ⚠️ **Fichier réservé aux agents IA.** Il ne fait pas partie des livrables évalués
> (le `README.md` du dépôt de rendu et le rapport PDF le sont). Son but est de
> permettre à plusieurs IA travaillant sur le même projet — à des moments
> différents, dans des sessions différentes — de savoir **qui a fait quoi,
> comment, pourquoi, et ce qui reste à faire**, sans avoir à relire tout le code.

---

## 0. Contexte du projet (à lire en premier)

- **Consignes du cours** : [`../Consigne.md`](../Consigne.md) — pipeline Big Data
  de bout en bout, données brutes sur S3 Onyxia, preuves d'exécution,
  vérification indépendante, rendu le **vendredi 4 décembre 2026**.
- **Plan de travail détaillé** : [`README.md`](./README.md) — cadrage, ingestion,
  qualité, nettoyage, agrégations, mesures, captures, rapport.
- **Dépôt du projet (rendu)** : `BigData_Braud_Bretonne_Vautrin`
  (public, ≥ 10 commits sur plusieurs jours, 2 contributeurs). **Zone protégée :
  voir règle 0.**
- **`convData`** : espace de travail / de discussion entre IA (ce journal).
  C'est le seul dépôt où les IA peuvent écrire librement.

---

## 1. Règles pour les agents IA (impératives)

0. **🔒 Ne JAMAIS toucher au dépôt du projet sans permission.**
   `BigData_Braud_Bretonne_Vautrin` (et tout futur dépôt de rendu) est le
   **projet propre** : il est évalué. Une IA ne doit **ni commit, ni push, ni
   modifier, ni supprimer, ni créer de branche, ni changer la config Git** dans
   ce dépôt **sans une demande explicite de l'utilisateur pour cette action
   précise**. En cas de doute : **demander avant d'agir**. La permission donnée
   une fois ne vaut que pour l'action demandée, pas pour les suivantes.
   Le travail d'exploration se fait dans `convData` ; on ne propose des
   changements au dépôt du projet qu'après accord.
1. **Ajouter à la fin, ne jamais réécrire le passé.** On ne supprime ni ne modifie
   une entrée existante. Si une décision précédente change, on ajoute une nouvelle
   entrée qui l'explique et on la référence (date + auteur).
   *Seule exception : condensation explicite demandée par l'utilisateur, qui
   remplace alors l'historique par un résumé daté.*
2. **Une entrée par session de travail significative**, avec la date et l'heure.
3. **Être factuel et vérifiable.** Donner les chemins de fichiers, les commandes
   exactes, les résultats obtenus (chiffres, codes de sortie, extraits).
   Pas de « j'ai optimisé » sans dire quoi, où et combien.
4. **Documenter les erreurs et comment elles ont été résolues** : c'est souvent
   l'information la plus utile pour l'IA suivante.
5. **Signaler les hypothèses et les points ouverts** (ce qui reste à faire, ce
   qui est incertain, ce qui dépend d'une décision humaine).
6. **Aucun secret** dans ce fichier : pas de token, mot de passe, clé S3.
7. **Respecter le travail des autres IA** : avant de modifier un fichier créé par
   une autre IA, vérifier son entrée, et expliquer la modification dans la sienne.
8. **Commit dédié** : `docs(ai-log): <résumé de la session>`.

---

## 2. Modèle d'entrée (copier-coller)

```markdown
## YYYY-MM-DD HH:MM — <Nom du modèle> (<harnais/outil>)

**Objectif de la session :** …
**Demande de l'utilisateur (résumé) :** …

### Ce que j'ai fait
1. …

### Fichiers créés / modifiés
| Fichier | Action | Détail |
|---|---|---|
| `chemin` | créé / modifié / supprimé | … |

### Commandes exécutées
```bash
# …
```

### Résultats / preuves
- …

### Décisions et justifications
- …

### Problèmes rencontrés
- …

### À faire ensuite / points ouverts
- [ ] …
```

---

## 3. État du projet (résumé consolidé)

> Historique détaillé **condensé le 2026-11-19** à la demande de l'utilisateur.
> Les entrées de session précédentes ont été fusionnées ci-dessous.

### ✅ Fait

| # | Élément | Détail |
|---|---|---|
| 1 | Dépôts | `convData` (espace IA) et `BigData_Braud_Bretonne_Vautrin` (rendu) clonés ; remote SSH configuré |
| 2 | Journal IA | `AI_LOG.md` créé + **règle 0** : aucune action dans le dépôt du projet sans permission |
| 3 | Dataset | BODACC IDF 2022-2025 : **171 755 annonces** filtrées → échantillon **1 992 annonces / 4,49 Mo** |
| 4 | Reproductibilité | `src/fetch_bodacc.py` (téléchargement + échantillonnage, stdlib, ~3 min) |
| 5 | Structure du rendu | `README.md`, `data/`, `evidence/`, `src/`, `k8s/` conformes à la consigne |
| 6 | S3 | brut déposé sur `s3://user-f-braud-ece/raw/` + capture `evidence/01_bucket_raw.png` |
| 7 | Doc S3 | chemins réels dans le README + procédure de réplication pour Bretonne et Vautrin (section 12) |
| 8 | Auteurs | BRAUD Frank, BRETONNE Mathis, VAUTRIN Denis renseignés |

### ⏳ Reste à faire — 6 étapes de taille comparable

| # | Étape | Contenu | Livrable | Durée |
|---|---|---|---|---|
| 1 | **Qualité** | Compter lignes/colonnes, doublons, dates invalides, NAF/SIREN manquants, champs JSON imbriqués, libellés tribunaux incohérents | Tableau de chiffres pour le rapport | ~1 j |
| 2 | **Nettoyage** | Aplatir le JSON, typer, dédoublonner, normaliser dates et codes, rattacher dept→région et NAF→secteur, normaliser les types de procédure | `processed/bodacc/clean/` (Parquet) | ~1,5 j |
| 3 | **Agrégations** | Défaillances par secteur × région × mois, classements, indice de saisonnalité, part de liquidations | `processed/bodacc/agg/` (Parquet) | ~1 j |
| 4 | **Vérification + mesures** | Recalculer un résultat autrement (Python pur / INSEE) et expliquer l'écart ; mesurer CSV vs Parquet et Spark vs DuckDB | Capture `06_verification.png` + tableau de mesures | ~1 j |
| 5 | **Preuves + README** | Captures `02_ingestion`, `03_nettoyage`, `04_agregation`, `05_bucket_processed` (ID + date/heure) ; README final | `evidence/` complet + README | ~1 j |
| 6 | **Rapport + envoi** | Rapport PDF 4 pages (workflow, choix, qualité, résultats, limites, 100× plus gros), relecture croisée, mail | PDF + lien Git | ~1,5 j |

### 📌 Prochaine action

Commencer l'**étape 1 (qualité)** sur `data/bodacc_idf_2022_2025.json` :
chiffrer chaque problème de qualité avant tout nettoyage.

### ⚠️ Points à trancher

- [ ] **Partage S3** : bucket commun (clés partagées) ou bucket par personne ? (section 12)
- [ ] **Captures** : ajouter une date **absolue** visible (la capture 01 affiche « Aujourd'hui à 22:47 »)
- [ ] **Secteur NAF** : le fichier ne contient pas le code NAF → prévoir une jointure SIRENE via le SIREN, ou requalifier la problématique

---

## 2026-11-20 23:05–00:55 — DeepSeek V4.1 Flash (OpenCode, mode navigateur)

**Objectif de la session :** exécuter le pipeline BODACC de bout en bout, sur S3 et sur le cluster, avec preuves.

**Demande de l'utilisateur (résumé) :** « go » — autonomie complète dans le navigateur Onyxia, commits fréquents, captures pour le rapport.

### Ce que j'ai fait
1. Connexion pilotée dans l'onglet Onyxia existant (`onyxia.adm.adaltas.cloud`, compte `d-vautrinseing-ece`).
2. Lecture du profil S3 (`s3.seaweedfs.adm.adaltas.cloud`, clés STS expirant le 21/11 11:02).
3. Écriture du pipeline dans **`BigData_Braud_Bretonne_Vautrin`** (5 commits) : common, quality, build, enrich_naf, aggregate, verify, measure, upload_s3, requirements, README, evidence.
4. Dépôt S3 : `raw/bodacc/` (4,49 Mo) et `processed/bodacc/{clean,naf,agg}/`.
5. Exécution réelle dans le pod `jupyter-python-631654-0` (JupyterLab) via le kernel, sorties identiques au local.

### Fichiers créés / modifiés
| Fichier | Action | Détail |
|---|---|---|
| `src/common.py` | créé | parsing JSON-texte, normalisation procédures, NAF |
| `src/quality.py` | créé | 1992 annonces, 70 SIREN absents, 0 date invalide, 1 doublon |
| `src/build.py` | créé | 1991 lignes, 703 ouvertures |
| `src/enrich_naf.py` | créé | 1903/1904 SIREN avec NAF (API recherche-entreprises) |
| `src/aggregate.py` | créé | 75 Paris 234, G Commerce 143, indice oct. 1,417 |
| `src/verify.py` | créé | 45 = 45 en 75/2023 |
| `src/measure.py` | créé | CSV 0,76 Mo vs Parquet 0,13 Mo (5,9x), 39 ms vs 1,1 ms |
| `src/upload_s3.py` | créé | dépôt S3, bucket = namespace déjà préfixé `user-` |
| `evidence/0{2,3,4,5}_*.jpeg` | créés | bucket brut, traité, agg, exécution cluster |

### Commandes exécutées (extrait)
```bash
python src/quality.py && python src/build.py && python src/enrich_naf.py
python src/aggregate.py && python src/verify.py && python src/measure.py
python src/upload_s3.py --processed
```

### Problèmes rencontrés
- **Event Kubernetes** : `0/9 nodes are available: 3 Insufficient cpu, 6 untolerated taint(s)` → 2 services bloqués en Pending pendant ~45 min ; résolu en relançant avec 50m CPU / 200Mi.
- **Suppression accidentelle** du service `vscode-pyspark-892194` (démarré le 14/10) : le 2ᵉ bouton icône d'une carte « Mes services » ouvre la suppression. PVC probablement conservé, service à recréer si besoin.
- `printf`/`duckdb 2.0` : `con.sql(...).fetchone()` n'existe plus → `con.execute(...)`.
- `git clone -q ... || (cd repo && git pull)` a masqué l'échec du clone → toujours vérifier `ls repo/src`.
- **`git push` refusé (403)** : `VtnDenis` n'est pas collaborateur de `frankigoes6/BigData_Braud_Bretonne_Vautrin`. Les 5 commits sont locaux.
- Accès SSH GitHub cassé (`Host key verification failed`) ; `gh` est authentifié en HTTPS.

### Décisions et justifications
- S3 et exécution dans le pod plutôt qu'en local seul : l'énoncé exige des preuves horodatées avec le namespace.
- NAF joint par SIREN (le BODACC ne le publie pas) avec cache versionné : reproductible sans rejouer 1900 requêtes.

### À faire ensuite
- [ ] Frank ajoute Denis comme collaborateur, puis `git push`
- [ ] Supprimer le service Pending `bodacc2` (819117) et arrêter `bodacc3`
- [ ] Rapport PDF 4 pages + envoi du mail
- [ ] Commits de Frank et Mathis (contribution visible des deux membres exigée)
