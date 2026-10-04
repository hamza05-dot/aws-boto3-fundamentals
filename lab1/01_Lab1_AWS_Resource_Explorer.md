# AWS Resource Explorer

Prove your credentials work, and meet the two ways Boto3 talks to AWS.

| Duration | Services | File to submit | Pattern |
| --- | --- | --- | --- |
| 1 h 30 | STS, S3, EC2 | `aws_resource_explorer.py` | Clients vs Resources |

---

## 1. What you are building

A single Python script that reports on the AWS account it is connected to. It prints who you are, which region you are in, which S3 buckets and EC2 instances exist, and which regions are available; and it fails politely instead of crashing when something is wrong.

```text
AWS RESOURCE EXPLORER
Lab 1 - Boto3 Fundamentals

==============================================================
  WHO AM I?
==============================================================
Account ID : 123456789012
User ID    : AROA...:user3021
ARN        : arn:aws:sts::123456789012:assumed-role/vocla.../user3021

==============================================================
  CURRENT REGION
==============================================================
Region           : us-east-1
Profile          : default

==============================================================
  S3 BUCKETS (via client)
==============================================================
  youssef-lab1-demo

Total: 1 bucket(s)
```

---

## 2. Learning objectives

By the end of this lab you should be able to:

- Explain what an SDK does and why Boto3 exists.
- Configure temporary AWS credentials and confirm they work.
- Create both a client and a resource, and describe how they differ.
- Read a nested Boto3 response without guessing at its shape.
- Catch `NoCredentialsError` and `ClientError` and report them usefully.

---

## 3. Before you start

- [ ] Python 3.9 or newer is installed (`python --version`).
- [ ] A virtual environment is created and activated.
- [ ] boto3 is installed (`pip install boto3`).
- [ ] The Learner Lab is started and shows a green circle beside AWS.
- [ ] Your three credential lines are pasted into `~/.aws/credentials`.
- [ ] `region = us-east-1` is set in `~/.aws/config`.

> **ℹ️ In the AWS Academy Learner Lab**
> Your credentials are temporary and include a session token. All three lines must be copied — access key, secret key and session token. They expire when the 4-hour lab session ends. If calls that worked ten minutes ago start failing with `ExpiredToken`, that is what happened. Work in `us-east-1` for this and every other lab in the module.

---

## 4. Step by step

*Build the script one function at a time and run it after each step. Do not write all six functions and then run it once — you will not know which one broke.*

### Step 1 — Prove the connection

Write a function `show_identity()` that calls STS and prints the account, user ID and ARN. STS answers the question "who does AWS think I am?", and needs no permission at all, so it is the ideal first call.

```python
import boto3

def show_identity():
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    print(f"Account ID : {identity['Account']}")
    print(f"User ID    : {identity['UserId']}")
    print(f"ARN        : {identity['Arn']}")

show_identity()
```

> **✅ Checkpoint**
> Running the script prints your account number. If it does not, stop here — nothing later in the lab will work.

---

### Step 2 — Report the region

Write `show_region()`. Read the region from a Session rather than hardcoding the string, so the script tells you what Boto3 actually resolved.

```python
def show_region():
    session = boto3.session.Session()
    print(f"Region  : {session.region_name}")
    print(f"Profile : {session.profile_name}")
```

> **✅ Checkpoint**
> The output says `us-east-1`. If it says `None`, your `~/.aws/config` is missing or misspelled.

---

### Step 3 — List buckets — the client way

Create a client for S3 and call `list_buckets()`. You get back a plain dictionary, exactly as AWS sent it.

Print each bucket's name and creation date. Note that `CreationDate` is already a Python `datetime` — Boto3 converted it for you.

```python
def list_buckets_with_client():
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    for bucket in response["Buckets"]:
        created = bucket["CreationDate"].strftime("%Y-%m-%d %H:%M")
        print(f"  {bucket['Name']:<45} created {created}")
```

> **✅ Checkpoint**
> The script lists your buckets, or says nothing when the account has none. An empty account is a valid result, not a failure.

---

### Step 4 — List buckets — the resource way

Now do the same thing with `boto3.resource()`. Same API underneath, different ergonomics: you iterate over objects with attributes instead of digging through dictionaries.

Put the two versions side by side in your code and read them. That comparison is the point of this step.

```python
def list_buckets_with_resource():
    s3 = boto3.resource("s3")
    for bucket in s3.buckets.all():
        print(f"  {bucket.name}")
```

> **✅ Checkpoint**
> Both functions print the same bucket names. You can explain in one sentence why the second is shorter.

---

### Step 5 — List EC2 instances — mind the nesting

`describe_instances()` returns `Instances` nested inside `Reservations`. A reservation is one launch request, so launching three instances at once gives one reservation containing three instances.

You need the double loop. Tags come back as a list of dictionaries, not a dictionary, so convert them before looking anything up.

```python
def list_instances():
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            tags = {t["Key"]: t["Value"] for t in instance.get("Tags", [])}
            print(f"  {instance['InstanceId']}  "
                  f"{instance['InstanceType']:<12} "
                  f"{instance['State']['Name']:<12} "
                  f"{tags.get('Name', '(no name)')}")
```

> **✅ Checkpoint**
> The script runs whether or not the account has instances. Using `instance['Tags']` instead of `.get('Tags', [])` will crash on an untagged instance — check that yours does not.

---

### Step 6 — List the available regions

Call `describe_regions()` and print the region names sorted, four to a line so the output stays readable.

```python
def list_regions():
    ec2 = boto3.client("ec2")
    names = sorted(r["RegionName"]
                   for r in ec2.describe_regions()["Regions"])

    for i in range(0, len(names), 4):
        print("  " + "".join(f"{n:<20}" for n in names[i:i + 4]))
```

> **✅ Checkpoint**
> Around thirty region names are printed in tidy columns.

---

### Step 7 — Fail politely

Wrap the whole `main()` in exception handling. Two exceptions matter here: `NoCredentialsError`, which means Boto3 searched every location and found nothing, and `ClientError`, which means AWS received your request and refused it.

Branch on the error `Code`, never on the `Message` — codes are a stable contract, messages are prose that AWS rewords.

```python
from botocore.exceptions import ClientError, NoCredentialsError

def main():
    try:
        show_identity()
        show_region()
        list_buckets_with_client()
        list_buckets_with_resource()
        list_instances()
        list_regions()

    except NoCredentialsError:
        print("[ERROR] No credentials found. Check ~/.aws/credentials")

    except ClientError as e:
        code = e.response["Error"]["Code"]
        print(f"[AWS ERROR] {code}: {e.response['Error']['Message']}")
        if code in ("ExpiredToken", "ExpiredTokenException"):
            print("Your session token expired. Restart the lab.")
```

> **✅ Checkpoint**
> Deliberately corrupt one character of your secret key in `~/.aws/credentials`, run the script, and confirm you get a readable message rather than a traceback. Then fix the key.

---

## 5. Expected output

Your formatting may differ. The information must not.

```text
AWS RESOURCE EXPLORER

  WHO AM I?
Account ID : 123456789012
ARN        : arn:aws:sts::123456789012:assumed-role/voclabs/user3021

  CURRENT REGION
Region : us-east-1

  S3 BUCKETS (via client)
  youssef-lab1-demo    created 2026-09-01 10:14
Total: 1 bucket(s)

  EC2 INSTANCES
No EC2 instances in this region.

  AVAILABLE AWS REGIONS
  af-south-1   ap-east-1    ap-northeast-1  ap-northeast-2
  ...
Total: 34 regions

Done.
```

---

## 6. If something goes wrong

| You see | It means | Do this |
| --- | --- | --- |
| `NoCredentialsError` | Boto3 found no credentials anywhere | Check the path and spelling of `~/.aws/credentials` |
| `ExpiredToken` | Session token has run out | Press Start Lab and re-copy all three lines |
| `NoRegionError` | No region resolved | Add `region = us-east-1` to `~/.aws/config` |
| `KeyError: 'Tags'` | The instance has no tags at all | Use `instance.get("Tags", [])` instead of `instance["Tags"]` |
| `KeyError: 'PublicIpAddress'` | A stopped instance has no public IP | Use `.get()` with a default for every optional field |
| `ModuleNotFoundError: boto3` | Wrong interpreter, or venv not active | Activate the venv, then `pip install boto3` |

---

## 7. Cleanup — before you leave the room

This lab creates nothing, so there is nothing to destroy. Get into the habit anyway — check the Console before you leave.

- [ ] The AWS Console shows no EC2 instances you started.
- [ ] The AWS Console shows no buckets you created.
- [ ] Your script is committed to your Git repository.

---

## 8. Submission checklist

- [ ] `aws_resource_explorer.py` runs end to end with no traceback.
- [ ] It prints identity, region, buckets (both ways), instances and regions.
- [ ] It handles a corrupted credential gracefully — you tested this.
- [ ] The file is committed with a meaningful message.

---

*Lab 1 — AWS Resource Explorer*
