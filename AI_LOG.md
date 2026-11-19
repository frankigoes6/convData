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

## 3. Journal

## 2026-11-19 21:43 — DeepSeek V4.1 Flash Free (OpenCode)

**Objectif de la session :** mettre en place l'espace de travail et créer ce journal.
**Demande de l'utilisateur (résumé) :** cloner les dépôts `convData` et
`BigData_Braud_Bretonne_Vautrin` dans des dossiers séparés, puis créer dans
`convData` un README destiné aux IA où chacune décrit en détail son travail.

### Ce que j'ai fait
1. Cloné `https://github.com/frankigoes6/BigData_Brau_Bretonne_Vautrin` →
   `BigData_Braud_Bretonne_Vautrin/` (dépôt quasi vide : un `README.md` de 32 o).
   > Note : le nom exact est `BigData_Braud_Bretonne_Vautrin` (vérifié via l'API GitHub).
2. Tenté de cloner `convData` → échec initial (HTTP 404, dépôt non visible),
   puis réussi au second essai (le dépôt est devenu accessible entre-temps).
3. Lu `../Consigne.md` et `README.md` pour le contexte.
4. Créé ce fichier `AI_LOG.md` (sans toucher au `README.md` existant, qui contient
   le plan de projet).

### Fichiers créés / modifiés
| Fichier | Action | Détail |
|---|---|---|
| `AI_LOG.md` | créé | Journal partagé des IA (ce fichier) |
| `README.md` | inchangé | Plan de projet existant |

### Commandes exécutées
```bash
git clone https://github.com/frankigoes6/BigData_Braud_Bretonne_Vautrin.git BigData_Braud_Bretonne_Vautrin
git clone https://github.com/frankigoes6/convData.git convData
curl -s https://api.github.com/users/frankigoes6/repos?per_page=100
```

### Résultats / preuves
- `convData/` : 2 commits (`8a1e6b8 plan`, `1780852 Initial commit`).
- `BigData_Braud_Bretonne_Vautrin/` : 1 fichier (`README.md`, 32 o).

### Décisions et justifications
- Fichier nommé `AI_LOG.md` plutôt que `README_AI.md` : évite la confusion avec
  le vrai `README.md` du rendu, et reste visible à la racine.
- Journal en français : langue de travail de l'utilisateur.
- Ajout d'une section « Contexte du projet » pour qu'une nouvelle IA soit
  opérationnelle sans relire toute l'historique.

### Problèmes rencontrés
- `convData` a d'abord renvoyé 404 (dépôt privé ou pas encore publié). Résolu
  en réessayant : le dépôt répond désormais 200 et se clone normalement.

### À faire ensuite / points ouverts
- [ ] Décider du dépôt final `bigdata_project` et de la répartition binôme.
- [ ] Figer la question de recherche et le périmètre (cf. `README.md` §0).
- [ ] Vérifier l'accès S3 Onyxia et créer le bucket.

## 2026-11-19 21:47 — DeepSeek V4.1 Flash Free (OpenCode)

**Objectif de la session :** protéger le dépôt du projet et mettre à jour les consignes IA.
**Demande de l'utilisateur (résumé) :** `BigData_Braud_Bretonne_Vautrin` est le
projet propre (évalué) : **demander la permission avant tout push ou autre
action dedans**, et ajouter cette règle aux consignes destinées aux IA.

### Ce que j'ai fait
1. Ajouté la **règle 0** en tête des règles impératives : interdiction de
   commit/push/modification/suppression/branche/config Git dans le dépôt du
   projet sans demande explicite et spécifique ; en cas de doute, demander.
2. Mis à jour la section « Contexte du projet » : `BigData_Braud_Bretonne_Vautrin`
   est identifié comme le dépôt de rendu (zone protégée) et `convData` comme le
   seul espace d'écriture libre des IA.

### Fichiers créés / modifiés
| Fichier | Action | Détail |
|---|---|---|
| `AI_LOG.md` | modifié | Règle 0 ajoutée + contexte mis à jour |

### Décisions et justifications
- La permission est **ponctuelle** : une autorisation pour un push ne vaut pas
  pour les suivants (le dépôt est noté, donc risque élevé).
- `convData` reste le bac à sable : les IA y préparent les changements et ne
  les appliquent au projet qu'après accord de l'utilisateur.

### À faire ensuite / points ouverts
- [ ] Toute IA : lire la règle 0 avant d'agir sur `BigData_Braud_Bretonne_Vautrin`.
- [ ] Demander à l'utilisateur comment il veut procéder pour les contributions
      au dépôt du projet (ex. l'IA prépare un patch dans `convData`, l'humain applique).
