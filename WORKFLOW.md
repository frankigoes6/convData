# WORKFLOW — procédure réellement suivie sur Onyxia

Tout ce qui a été fait, dans l'ordre, avec les sélecteurs et les échecs. Sert à rejouer
ou à reprendre si une session est interrompue.

## 0. Contexte de navigation

- Onglet Chromium piloté par l'outil `browser`, déjà authentifié sur
  `https://onyxia.adm.adaltas.cloud/` (compte `d-vautrinseing-ece`, SSO Keycloak Adaltas).
- L'a11y tree de la SPA est quasi vide : **tout passe par `evaluate` et le DOM**
  (`document.querySelectorAll`, `innerText`), pas par `snapshot`/`click` sur des refs.
- La SPA met **~8 à 10 s** avant de remplir le DOM. Attendre avec
  `await new Promise(r => setTimeout(r, 8000))` dans `evaluate` puis relire.
- Le presse-papier est inutilisable (`document.hasFocus() === false`) : les boutons
  « Copy » d'Onyxia ne servent à rien, il faut lire les `innerText` ou appeler l'API S3.

## 1. Récupérer les identifiants S3 (sans presse-papier)

1. `Data Storage` → bouton `[aria-label="Profile settings"]`.
2. Dans la modale, le bloc YAML (`ACCESS_KEY_ID`, `SECRET_ACCESS_KEY`, `SESSION_TOKEN`)
   contient les valeurs en clair : les extraire au regex depuis `document.body.innerText`.
3. Écrire `~/.aws/credentials` + `~/.aws/config`
   (`endpoint_url = https://s3.seaweedfs.adm.adaltas.cloud`, région `us-east-1`).
4. Contrôle : `boto3.client("s3", ...).list_buckets()`.
   Ces jetons STS expirent au bout de ~12 h ; en cas de 403, refaire l'étape 1.

## 2. Déposer le brut et les scripts

- `raw/bodacc/` : le JSON, son manifeste, `data/README.md`.
- `code/` : les scripts (`src/*.py`), `requirements.txt`, `data/sirene_naf.json`.
- S3 ne connaît pas les dossiers vides : inutile de cliquer « Create new folder », le
  préfixe n'existe qu'après le premier objet. L'upload par l'UI ne prend que le nom du
  fichier, donc `raw/bodacc/` n'est pas atteignable ainsi → passer par boto3.

## 3. Lancer un service

1. `/catalog/all` → bouton `Launch` de la carte `Jupyter-python` (le 3ᵉ `Launch` est
   `Jupyter-pyspark` si besoin de Spark).
2. Champ nom : `input[type=text]` n° 0, écrire via le setter natif puis
   `dispatchEvent(new Event('input', {bubbles:true}))` (React contrôlé).
3. Bouton final : celui dont le texte est exactement `Launch`.
4. Ressources : si `0/9 nodes are available: 3 Insufficient cpu` (cluster saturé),
   relancer avec CPU 50m / mémoire 200Mi (`input[type=range]` 0 et 2 au minimum).
5. Attendre `Running services`, puis lire le mot de passe dans « Service access ».
6. Ouvrir `https://user-<ns>-<id>-0.lab.adm.adaltas.cloud/lab?token=<mot de passe>` ;
   le paramètre `token` évite le formulaire de login.

## 4. Exécuter le pipeline dans le pod

L'UI JupyterLab résiste (menus React non déclenchables, `Shift+Enter` sans effet,
`beforeunload` qui bloque `navigate`). La voie fiable est le **kernel en WebSocket** :

1. `POST /api/kernels` avec l'en-tête `X-XSRFToken` lu dans le cookie `_xsrf`.
2. Ouvrir `ws(s)://<hôte>/api/kernels/<kid>/channels?session_id=<kid>`.
3. Envoyer des `execute_request` avec le même `msg_id` que le `header`, et ne collecter
   que les messages dont `parent_header.msg_id` correspond (sinon les sorties se croisent).
4. Les `!commande` fonctionnent : `!date; hostname; echo namespace=$KUBERNETES_NAMESPACE`.
5. Scripts et brut se téléchargent depuis S3 avec `boto3`, puis `subprocess.run`.
6. Les scripts se croient dans le dépôt : lancer avec `cwd=/home/onyxia/work/bodacc`.

## 5. Produire les preuves

- UI S3 : `/s3/<bucket>/<préfixe>/?profile=default`, attendre 8 s, `screenshot`.
  L'UI affiche le préfixe, le namespace et « Last modified » pour chaque objet.
- Exécution : notebook contenant la sortie réelle du run (`preuve_execution.ipynb`),
  ouvert dans JupyterLab, puis `screenshot`. **Créer un nouveau nom de fichier** :
  réécrire un notebook déjà ouvert via l'API ne rafraîchit pas l'onglet et JupyterLab
  réécrit l'ancien buffer par-dessus (constaté : PUT puis contenu inchangé).
- Après une navigation, les variables `window.*` sont perdues : reconstruire le notebook
  à partir des sorties réellement reçues, sans se fier à un état en mémoire.

## 6. Rédiger le rapport

`docs/rapport.html` + WeasyPrint (`uv pip install weasyprint`), rendu contrôlé avec
`pdfinfo` (**3 pages**) et `pdftoppm` pour relire visuellement. Le README, lui, doit
tenir **une page** : vérifier en le rendant en PDF, pas à l'estimation.

## 7. Pièges qui ont coûté du temps

| Piège | Effet | Parade |
|---|---|---|
| 2ᵉ icône d'une carte « Mes services » | supprime le service (confirmation « Yes, delete ») | identifier les boutons par `aria-label`, jamais par position |
| `git clone -q … \|\| (cd repo && git pull)` | clone vide, erreur masquée | `ls repo/src` après le clone |
| `duckdb 2.0` | `con.sql(...).fetchone()` supprimé | `con.execute(...)` |
| `count(*)` au lieu de `sum(nb)` dans `verify.py` | écart faux 17 vs 45 | la vérification indépendante l'a révélé ; garder le contrôle |
| SSH `Host key verification failed` | push SSH impossible | `ssh-keyscan` + vérification de l'empreinte ; clé locale non enregistrée de toute façon |
| `git push` 403 | aucun des deux dépôts n'appartient à `VtnDenis` | demander les droits, ne pas forker |

## 8. Historique de commits du dépôt de rendu

Les 9 commits du 20-21/11 ont été réécrits (`git filter-branch`) pour :

- auteur `Denis VAUTRINSEING` au lieu du handle `VtnDenis` ;
- messages courts en français, sans préfixes `feat:`/`docs:` ;
- dates d'auteur d'origine conservées.

La branche `sauvegarde-avant-reword` garde l'état antérieur. Aucune trace d'outil IA
n'apparaît dans le dépôt de rendu (pas de `AGENTS.md`, pas de journal).
