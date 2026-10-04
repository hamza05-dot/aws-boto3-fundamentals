# Notes perso — Lab 1 : AWS Resource Explorer (Boto3)

Objectif du lab : un script Python qui se connecte à mon compte AWS et
rapporte qui je suis, où je suis, et ce qui existe (buckets S3,
instances EC2, régions dispo) — sans planter si un truc ne va pas.

- **Durée estimée** : ~1h30
- **Services touchés** : STS, S3, EC2
- **Fichier à rendre** : `aws_resource_explorer.py`
- **Concept central** : client vs resource

---

## Objectifs pédagogiques (ce que je dois savoir faire après)

- Expliquer à quoi sert un SDK et pourquoi Boto3 existe
- Configurer des credentials temporaires et vérifier qu'ils marchent
- Créer un client ET une resource, et dire la différence entre les deux
- Lire une réponse Boto3 imbriquée sans deviner sa structure
- Attraper `NoCredentialsError` et `ClientError` proprement

---

## Checklist avant de commencer

- [ ] Python 3.9+ installé
- [ ] venv créé et activé
- [ ] `boto3` installé
- [ ] Learner Lab démarré (rond vert)
- [ ] `~/.aws/credentials` à jour (3 lignes)
- [ ] `region = us-east-1` dans `~/.aws/config`

---

## Plan de développement (une fonction à la fois, testée à chaque étape)

Je ne code pas tout d'un coup — je fais une fonction, je la teste, puis
je passe à la suivante. Sinon si ça plante je ne sais pas laquelle est
en cause.

### Étape 1 — Vérifier la connexion (`show_identity`)
- Appeler STS pour savoir "qui suis-je" côté AWS (account, user id, ARN).
- STS ne demande aucune permission → c'est le meilleur premier test.
- **Check** : si l'account ID ne s'affiche pas, rien d'autre ne marchera → je m'arrête ici et je corrige les credentials d'abord.

### Étape 2 — Afficher la région (`show_region`)
- Lire la région depuis une `Session` plutôt que de l'écrire en dur, pour être sûr de ce que Boto3 a réellement résolu.
- **Check** : si ça affiche `None` au lieu de `us-east-1`, mon `~/.aws/config` est absent ou mal écrit.

### Étape 3 — Lister les buckets S3, version "client"
- Un client renvoie un dictionnaire brut, tel qu'AWS l'envoie.
- Afficher nom + date de création de chaque bucket (la date arrive déjà convertie en `datetime` par Boto3).
- **Check** : un compte vide qui n'affiche rien est un résultat valide, pas un bug.

### Étape 4 — Lister les buckets S3, version "resource"
- Même résultat, mais avec des objets Python à attributs plutôt que des clés de dictionnaire.
- Je mets les deux versions côte à côte pour comparer et être capable d'expliquer en une phrase pourquoi la version resource est plus courte.

### Étape 5 — Lister les instances EC2 (attention à l'imbrication)
- La réponse imbrique les instances DANS des réservations (une réservation = une commande de lancement, donc 3 instances lancées ensemble = 1 réservation avec 3 instances).
- Il faut donc une double boucle.
- Les tags reviennent sous forme de liste de dictionnaires, pas un dictionnaire direct → il faut les transformer avant de les utiliser.
- **Piège à éviter** : utiliser `instance["Tags"]` directement plante sur une instance sans tag → utiliser `.get("Tags", [])`.

### Étape 6 — Lister les régions disponibles
- Appeler `describe_regions()`, trier les noms, et les afficher en colonnes (par ex. 4 par ligne) pour que ce soit lisible.
- Résultat attendu : une trentaine de régions.

### Étape 7 — Gérer les erreurs proprement
- Envelopper l'exécution principale dans un `try/except`.
- Deux exceptions à connaître :
  - `NoCredentialsError` → Boto3 n'a trouvé aucun credential nulle part.
  - `ClientError` → AWS a reçu la requête et l'a refusée.
- Toujours brancher sur le **code d'erreur**, jamais sur le message (le message est du texte qui peut changer, le code est stable).
- **Test à faire volontairement** : corrompre un caractère de la secret key, relancer le script, vérifier que j'obtiens un message clair et pas un traceback brut. Remettre la clé correcte après.

---

## Sortie attendue (à quoi ça doit ressembler globalement)

- Une section "qui suis-je" (account, ARN)
- Une section région courante
- Une section buckets S3 (via client) avec un total
- Une section instances EC2 (ou un message clair s'il n'y en a pas)
- Une section régions disponibles, en colonnes, avec un total
- Un message final genre "Done."

Le format exact peut différer du modèle du prof, l'important c'est que
les informations affichées soient correctes.

---

## Table de dépannage rapide

| Je vois | Ça veut dire | Je fais |
|---|---|---|
| `NoCredentialsError` | Aucun credential trouvé | Vérifier chemin/orthographe de `~/.aws/credentials` |
| `ExpiredToken` | Token de session expiré | Start Lab + recopier les 3 lignes |
| `NoRegionError` | Aucune région résolue | Ajouter `region = us-east-1` dans `~/.aws/config` |
| `KeyError: 'Tags'` | Instance sans aucun tag | Utiliser `.get("Tags", [])` |
| `KeyError: 'PublicIpAddress'` | Instance stoppée = pas d'IP publique | `.get()` avec valeur par défaut partout où c'est optionnel |
| `ModuleNotFoundError: boto3` | Mauvais interpréteur / venv pas actif | Activer le venv, `pip install boto3` |

---

## Nettoyage avant de quitter

Ce lab ne crée rien de facturable, mais je prends quand même le réflexe :

- [ ] Vérifier la Console : aucune instance EC2 démarrée par moi
- [ ] Vérifier la Console : aucun bucket créé par moi
- [ ] Script commité sur mon repo Git

## Checklist de rendu

- [ ] `aws_resource_explorer.py` tourne du début à la fin sans traceback
- [ ] Affiche bien : identité, région, buckets (2 méthodes), instances, régions
- [ ] Gère un credential corrompu sans planter (testé)
- [ ] Commit avec un message clair
