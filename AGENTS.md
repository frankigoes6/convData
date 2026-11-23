# AGENTS.md — convData

Espace de travail IA du projet Big Data « Défaillances d'entreprises (BODACC) ».
Tous les documents du dépôt sont en **français** : écrire en français.

## Règle n° 0 — deux dépôts appartiennent à `frankigoes6`

`convData` (ce dépôt) et le dépôt de rendu `BigData_Braud_Bretonne_Vautrin` sont
hébergés sur le compte GitHub `frankigoes6`. L'utilisateur local (`VtnDenis`) **n'est
collaborateur d'aucun des deux** : tout `git push` renvoie 403.

- Ne **jamais** créer de fork, de dépôt de substitution, ni de PR sans demande
  explicite : la réponse à « je ne peux pas pousser » est « 403, il faut les droits ».
- Ne rien modifier dans `BigData_Braud_Bretonne_Vautrin` sans demande explicite pour
  cette action précise : il est évalué. Le travail d'exploration se fait ici.

## Rôle des fichiers

| Fichier | Rôle |
|---|---|
| `AI_LOG.md` | Journal inter-IA : **append-only**, une entrée datée par session, commit `docs(ai-log): <résumé>` |
| `PIPELINE.md` | **Ce qui a été construit** : étapes, chiffres de référence, layout S3, pièges Onyxia |
| `WORKFLOW.md` | **Comment ça a été fait** : procédure de navigation, sélecteurs, kernel WebSocket, échecs |
| `README.md` | Plan de travail du projet (pas la doc de ce dépôt) |
| `Ecosysteme_Big_Data_II_project.md` | Énoncé officiel (anglais) : c'est la source de vérité des attentes |
| `data/`, `src/` | Copie de travail du dataset et du script de génération |

Dans `AI_LOG.md` : ne jamais réécrire une entrée passée ; une décision qui change
s'ajoute dans une nouvelle entrée référencée. Aucun secret (clé S3, token, mot de passe
Jupyter). Écrire des faits vérifiables (chemins, commandes, chiffres, codes de sortie).

## Le dépôt de rendu

`../BigData_Braud_Bretonne_Vautrin` : `README.md`, `src/` (pipeline DuckDB),
`evidence/` (5 captures), `docs/` (rapport HTML + PDF), `out/` (git-ignoré).

```bash
cd ../BigData_Braud_Bretonne_Vautrin
uv venv .venv && . .venv/bin/activate && uv pip install -r requirements.txt
python src/quality.py && python src/build.py && python src/enrich_naf.py
python src/aggregate.py && python src/verify.py && python src/measure.py
```

`verify.py` doit sortir « OK : résultats identiques » ; c'est le seul contrôle
automatisé du projet (pas de suite de tests, pas de CI).

## Pièges vérifiés (ne pas les redécouvrir)

- **NAF absent du BODACC** : joint par SIREN via `recherche-entreprises.api.gouv.fr`,
  cache `data/sirene_naf.json` (1 903/1 904). L'API coupe les rafales : 5 threads max.
- **`jugement` et `listepersonnes` sont du texte JSON**, pas des objets.
- **Champs piégeux** : `commercant` concatène plusieurs entités ; `jugement.nature`
  mélange ouvertures, clôtures et états de créances — seules les ouvertures comptent.
- **Onyxia** : routes en `/s3/<bucket>/<préfixe>/`, pages qui mettent ~8-10 s à rendre,
  quota CPU saturable (`0/9 nodes available`), 2ᵉ icône d'une carte service = **supprimer**.
- **DuckDB 2.0** : `con.sql(...).fetchone()` n'existe plus, utiliser `con.execute(...)`.

## Discrétion IA dans le dépôt de rendu

`BigData_Braud_Bretonne_Vautrin` doit passer pour un travail humain : **aucune trace
d'outil IA**.

- Auteur des commits : `Denis VAUTRINSEING <117896625+VtnDenis@users.noreply.github.com>`.
- Messages courts, en français, sans préfixe `feat:` / `fix:` / `docs:`.
- Pas de `AGENTS.md`, pas de journal, pas de mot « agent » : la doc IA vit dans `convData`.
- Le détail technique retiré du README va dans `docs/PIPELINE.md` (contenu neutre).
- `convData`, à l'inverse : tout documenter, sans rien garder pour soi.

Une **empreinte SHA256** fournie par l'utilisateur n'est pas une clé d'accès : elle
identifie un serveur, elle n'autorise rien. Celles de `github.com` publiées par GitHub
sont `+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` (ed25519) et
`uNiVztksCsDhcc0u9e8BujQXVUpKZIDTMczCvj3tD2s` (rsa).

## État au 2026-11-21

Pipeline complet exécuté sur S3 et dans un pod Onyxia, preuves et rapport produits.
Les deux dépôts sont **poussés** sur `main` : `3a72e12` pour le rendu, `HEAD` ici.
Détail : `PIPELINE.md` §7-8.
