# Aide-mémoire — AWS Academy Learner Lab

Notes perso à garder sous la main pendant les 7 sessions du module Boto3/AWS.

**Infos clés** : région `us-east-1` · session de 4h · key pair `vockey` · rôle Lambda `LabRole`

---

## 1. Démarrer une session (à refaire à CHAQUE fois)

1. Ouvrir le Learner Lab → cliquer **Start Lab** → attendre le rond vert.
2. **AWS Details** → **Show** à côté de AWS CLI → copier le bloc de credentials.
3. Coller ce bloc dans `~/.aws/credentials` (remplacer l'ancien contenu).
4. Tester la connexion avant de coder quoi que ce soit.

> ⚠️ **Le point le plus important** : les credentials sont TEMPORAIRES.
> Ils changent à chaque Start Lab et expirent après 4h. Il faut recopier
> les 3 lignes à chaque session — c'est normal, pas un bug.

### `~/.aws/credentials`
```ini
[default]
aws_access_key_id     = ASIA...
aws_secret_access_key = ...
aws_session_token     = ...
```
*(Windows : `C:\Users\<toi>\.aws\credentials`, sans extension)*

### `~/.aws/config`
```ini
[default]
region = us-east-1
output = json
```

### Test rapide avant de commencer
```python
import boto3
sts = boto3.client("sts")
print(sts.get_caller_identity())
print("Region:", boto3.session.Session().region_name)
```
`get_caller_identity()` ne demande aucune permission → si ça plante, le souci vient des credentials, pas d'IAM.

---

## 2. Setup Python (une seule fois par machine)

```bash
python --version          # 3.9+
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install boto3
pip freeze > requirements.txt
```

---

## 3. Ce que le Learner Lab autorise (ou pas)

| Domaine | Limite | À faire |
|---|---|---|
| Régions | `us-east-1` et `us-west-2` uniquement | Toujours `us-east-1` |
| Types EC2 | nano/micro/small/medium/large | `t3.micro`, sinon `UnauthorizedOperation` |
| EC2 | max 9 instances / 32 vCPU par région | Une à la fois, terminer après usage |
| EBS | 100 Go max | Le volume racine par défaut (8 Go) suffit |
| IAM | Impossible de créer users/groups/roles | Utiliser `LabRole` pour Lambda |
| Key pair | `vockey` déjà créée (us-east-1) | `KeyName="vockey"` dans `run_instances` |
| Session | 4h puis coupure totale | Relancer Start Lab pour reset le timer |
| Budget | Crédit fixe partagé | Toujours nettoyer, même ce qui est idle |

---

## 4. Rôle Lambda — la seule vraie différence avec un compte normal

Pas moyen de créer un rôle IAM → on réutilise `LabRole`, en construisant son ARN dynamiquement à partir de son propre account ID :

```python
account_id = boto3.client("sts").get_caller_identity()["Account"]
role_arn = f"arn:aws:iam::{account_id}:role/LabRole"
# → à passer dans Role= lors de create_function()
```

---

## 5. Traduction des erreurs les plus fréquentes

| Erreur | Ça veut dire | Solution |
|---|---|---|
| `ExpiredToken` / `ExpiredTokenException` | Le token de session a expiré | Start Lab + recopier les 3 lignes |
| `InvalidClientTokenId` | Clé d'accès invalide | Credentials mal/partiellement copiées |
| `AccessDenied` | Identité ok, permission manquante | Lire le message, il donne l'action exacte |
| `UnauthorizedOperation` | Version EC2 de AccessDenied | Souvent un type d'instance/région interdit |
| `NoRegionError` | Boto3 n'a trouvé aucune région | Ajouter `region = us-east-1` dans `~/.aws/config` |
| `NoSuchBucket` | Bucket inexistant ici | Vérifier nom + région |
| `BucketAlreadyExists` | Nom pris par un autre compte AWS | Noms de bucket = globaux, ajouter un préfixe perso |
| `BucketNotEmpty` | Reste des objets dedans | Vider avant de supprimer |
| `ResourceNotFoundException` | Mauvais nom ou mauvaise région | Vérifier `Session().region_name` |
| `ResourceInUseException` | La ressource existe déjà | La réutiliser ou la supprimer d'abord |
| `ConditionalCheckFailedException` | Condition DynamoDB non remplie | Pas un crash, à gérer proprement |
| `ValidationException` | Paramètres mal formés | Revérifier la doc de l'opération |
| `ThrottlingException` | Trop d'appels trop vite | Laisser botocore retry (mode adaptive) |

---

## 6. Checklist de fin de session (à ne JAMAIS sauter)

- [ ] EC2 : toutes les instances **terminées** (pas juste stoppées)
- [ ] S3 : buckets vidés puis supprimés
- [ ] DynamoDB : tables supprimées
- [ ] Lambda : fonctions supprimées
- [ ] Console AWS : plus rien qui m'appartient
- [ ] Code commité + pushé sur mon repo Git

> ⚠️ Une instance **stoppée** ne coûte rien en compute, mais son volume EBS
> continue d'être facturé tant qu'il existe. Seul **terminate** arrête tout.

---

## 7. Les 4 patterns à retenir

**Paginator** — parce qu'AWS ne renvoie jamais tout d'un coup
```python
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket=bucket_name):
    for obj in page.get("Contents", []):   # .get() : page vide = pas de clé
        print(obj["Key"])
```

**Waiter** — parce qu'AWS répond avant d'avoir fini
```python
ec2.get_waiter("instance_running").wait(
    InstanceIds=[instance_id],
    WaiterConfig={"Delay": 15, "MaxAttempts": 40},
)
```

**Gestion d'erreur** — brancher sur le `Code`, jamais sur le `Message`
```python
from botocore.exceptions import ClientError
try:
    ...
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code == "NoSuchBucket":
        print("Bucket inexistant.")
    else:
        raise   # ne jamais avaler une erreur inconnue
```

**Logging propre**
```python
import logging, os
logging.basicConfig(level=logging.INFO,
                     format="%(asctime)s  %(levelname)-8s %(message)s")
log = logging.getLogger("toolkit")
REGION = os.environ.get("AWS_REGION", "us-east-1")
```

> 📌 **Règle du module** : ce que je crée, je le détruis. Le nettoyage
> fait partie du travail, pas une option.
