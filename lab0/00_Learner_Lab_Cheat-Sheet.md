# AWS Academy Learner Lab — Survival Sheet

Keep this next to your keyboard for all seven sessions. Almost every problem you will hit in this module is on this page.

| Region | Session length | Key pair | Lambda role |
| --- | --- | --- | --- |
| `us-east-1` | 4 hours | `vockey` | `LabRole` |

---

## 1. Starting the lab, every single time

1. Open the Learner Lab and click **Start Lab**. Wait for the circle beside AWS to turn green.
2. Click **AWS Details**, then **Show** beside AWS CLI. You will see a block of credentials.
3. Copy that whole block into `~/.aws/credentials`, replacing whatever is already there.
4. Run your connection test before writing any other code.

> **⚠️ The single most important thing on this page**
> Your credentials are **temporary**. They change every time you press Start Lab, and they expire when the 4-hour session ends. You must re-copy all three lines at the start of every session. This is not a bug and it will not stop happening.

### `~/.aws/credentials`

*On Windows this file is at `C:\Users\<you>\.aws\credentials` — with no file extension.*

```ini
[default]
aws_access_key_id     = ASIA...............
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/.............
aws_session_token     = IQoJb3JpZ2luX2VjE...........................
```

### `~/.aws/config`

```ini
[default]
region = us-east-1
output = json
```

### Prove it works before doing anything else

```python
import boto3

sts = boto3.client("sts")
print(sts.get_caller_identity())
print("Region:", boto3.session.Session().region_name)
```

> `get_caller_identity()` needs no permission at all. If it fails, the problem is your credentials — never your IAM policy.

---

## 2. Setting up Python (once, on your machine)

```bash
python --version                # 3.9 or newer

python -m venv venv
source venv/bin/activate        # Windows:  venv\Scripts\activate

pip install boto3
pip freeze > requirements.txt
```

---

## 3. What the Learner Lab will and will not let you do

| Area | The limit | What to do about it |
| --- | --- | --- |
| **Regions** | `us-east-1` and `us-west-2` only | Use `us-east-1` for everything in this module |
| **EC2 types** | nano, micro, small, medium, large | Use `t3.micro`. Anything bigger fails with `UnauthorizedOperation` |
| **EC2 count** | 9 instances, 32 vCPU per region | Launch one at a time and terminate when finished |
| **EBS volumes** | 100 GB maximum | The default 8 GB root volume is fine |
| **IAM** | Cannot create users, groups or roles | Use the pre-existing `LabRole` for Lambda |
| **Key pairs** | `vockey` already exists (`us-east-1`) | Pass `KeyName="vockey"` to `run_instances` |
| **Session** | 4 hours, then everything stops | Press Start Lab again to reset the timer |
| **Budget** | A fixed shared credit | Terminate everything. Idle resources spend it for nothing |

---

## 4. The Lambda role — the one place lab code differs

You cannot create an IAM role, so you cannot create the execution role a Lambda function normally needs. A role called `LabRole` already exists in your account. Build its ARN from your own account ID rather than typing it:

```python
sts      = boto3.client("sts")
account  = sts.get_caller_identity()["Account"]
role_arn = f"arn:aws:iam::{account}:role/LabRole"

lambda_client.create_function(
    FunctionName=name,
    Runtime="python3.13",
    Role=role_arn,                     # <- this line
    Handler="lambda_function.lambda_handler",
    Code={"ZipFile": package_bytes},
)
```

---

## 5. Error codes, translated

| Error code | What it really means | Fix |
| --- | --- | --- |
| `ExpiredToken` | Session token has run out | Press Start Lab, re-copy all three credential lines |
| `ExpiredTokenException` | Same thing, different service | Same fix |
| `InvalidClientTokenId` | Access key is not valid here | You pasted a partial or stale block. Re-copy it |
| `AccessDenied` | Valid identity, missing permission | Read the message — it names the exact action |
| `UnauthorizedOperation` | The EC2 form of `AccessDenied` | Usually a forbidden instance type or region |
| `NoRegionError` | Boto3 found no region at all | Add `region = us-east-1` to `~/.aws/config` |
| `NoSuchBucket` | Bucket does not exist here | Check the name, then check the region |
| `BucketAlreadyExists` | Another AWS account owns that name | Bucket names are global. Add your own prefix |
| `BucketNotEmpty` | Bucket still contains objects | Delete every object first, then the bucket |
| `ResourceNotFoundException` | Wrong name, or wrong region | Print `Session().region_name` and check |
| `ResourceInUseException` | The table or function already exists | Use it, or delete it first |
| `ConditionalCheckFailedException` | Your DynamoDB condition held | Not a crash — handle it and tell the user |
| `ValidationException` | Malformed parameters | Re-read the docs for that operation |
| `ThrottlingException` | You are calling too fast | Let botocore retry; use adaptive retry mode |

---

## 6. End-of-session cleanup checklist

Run through this before you close your laptop. Every session, without exception.

- [ ] **EC2** — every instance you launched is terminated (not just stopped).
- [ ] **S3** — every bucket you created is empty and deleted.
- [ ] **DynamoDB** — every table you created is deleted.
- [ ] **Lambda** — every function you deployed is deleted.
- [ ] The AWS Console shows nothing left that belongs to you.
- [ ] Your work is committed and pushed to your Git repository.

> **⚠️ Stopped is not the same as cleaned up**
> A stopped EC2 instance costs nothing for compute, but its EBS volume is still billed for as long as it exists. Only **terminate** actually stops every charge.

---

## 7. The four patterns, in one place

### Paginator — because AWS never returns everything

```python
paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=name):
    for obj in page.get("Contents", []):     # .get - an empty page has no key
        print(obj["Key"])
```

### Waiter — because AWS answers before it finishes

```python
ec2.get_waiter("instance_running").wait(
    InstanceIds=[instance_id],
    WaiterConfig={"Delay": 15, "MaxAttempts": 40},
)
```

### Error codes — branch on `Code`, never on `Message`

```python
from botocore.exceptions import ClientError

try:
    ...
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code == "NoSuchBucket":
        print("That bucket does not exist.")
    else:
        raise                                # never swallow the unknown
```

### Logging and configuration

```python
import logging, os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)-8s %(message)s")
log = logging.getLogger("toolkit")

REGION = os.environ.get("AWS_REGION", "us-east-1")
```

> **📌 Rule for the whole module**
> If you created it, you destroy it. Cleanup is not an afterthought in cloud automation — it is half the job.

---

*Learner Lab Survival Sheet*
