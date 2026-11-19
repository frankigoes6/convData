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
