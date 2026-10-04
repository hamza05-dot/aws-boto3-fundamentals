# S3 File Manager

A menu-driven tool for buckets and objects, built around the paginator pattern.

| Duration | Services | File to submit | Pattern |
| --- | --- | --- | --- |
| 2 h 15 | S3 | `s3_manager.py` | Paginators |

---

## 1. What you are building

An interactive command-line tool that manages S3 from Python. It creates and deletes buckets, uploads and downloads objects, lists them with a paginator, generates presigned URLs, and — as a challenge — backs up a whole local folder while preserving its structure.

```text
=========================================
           S3 MANAGER
=========================================
  1. Create Bucket        5. Download File
  2. List Buckets         6. Delete File
  3. Upload File          7. Generate Presigned URL
  4. List Files           8. Delete Bucket
  9. Backup Local Folder  0. Exit
=========================================

Choose an option: _
```

---

## 2. Learning objectives

By the end of this lab you should be able to:

- Explain why S3 has no folders, and what a key prefix really is.
- Create a bucket correctly in `us-east-1` and in any other region.
- Choose between `upload_file` and `put_object`, and say why.
- Use a paginator to list every object in a bucket, not just the first thousand.
- Generate a presigned URL and explain what it grants and for how long.
- Empty a bucket before deleting it.

---

## 3. Before you start

- [ ] Lab 1 runs successfully — your credentials work today.
- [ ] You have re-copied your credentials for this session.
- [ ] You have chosen a bucket-name prefix nobody else will use (e.g. `youssef-lab2-`).
- [ ] You have a small local folder with a few files, for the challenge.

> **ℹ️ In the AWS Academy Learner Lab**
>
> - Create every bucket in `us-east-1`, which conveniently means you can skip the `CreateBucketConfiguration` branch, though your code should still handle both.
> - Block Public Access stays on. Share objects with a presigned URL, which is better practice anyway.
> - Prefix every bucket name with your own identifier. Bucket names are globally unique across every AWS account on Earth.

---

## 4. Step by step

*Build the menu loop first with stub functions that just print their own name. Then fill them in one at a time, testing each from the menu as you go.*

### Step 1 — The menu loop

Write the loop and a dispatch dictionary before any AWS code. A dictionary of options to functions is cleaner than a long `if/elif` chain and easier to extend.

```python
import sys, boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
REGION = boto3.session.Session().region_name or "us-east-1"

ACTIONS = {"1": create_bucket, "2": list_buckets, ...}

def main():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            sys.exit(0)
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid option.")
```

> **✅ Checkpoint**
> Every menu option prints its own name, and `0` exits cleanly.

---

### Step 2 — Create a bucket — and handle the `us-east-1` asymmetry

`us-east-1` is the original AWS region, and it is the only one where passing a location constraint is an error. Every other region requires it. Write the branch once and stop thinking about it.

Handle `BucketAlreadyExists` (someone else owns that name) separately from `BucketAlreadyOwnedByYou` (you already made it).

```python
def create_bucket():
    name = input("New bucket name: ").strip()
    try:
        if REGION == "us-east-1":
            s3.create_bucket(Bucket=name)
        else:
            s3.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={"LocationConstraint": REGION},
            )
        print(f"Created bucket '{name}'")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "BucketAlreadyExists":
            print("That name is taken by another AWS account.")
        elif code == "BucketAlreadyOwnedByYou":
            print("You already own that bucket.")
        else:
            print(f"[AWS ERROR] {code}")
```

> **✅ Checkpoint**
> Creating the same bucket twice gives a clear message the second time, not a traceback.

---

### Step 3 — Upload a file

Use `upload_file`, which is a managed transfer: it splits large files into a multipart upload, uploads parts in parallel and retries failures.

Let the user choose the object key, defaulting to the filename. Check the local file exists before calling AWS — a local mistake should not become an AWS error.

```python
import os

def upload_file():
    path   = input("Local file path: ").strip()
    bucket = input("Target bucket: ").strip()

    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return

    default_key = os.path.basename(path)
    key = input(f"Object key [{default_key}]: ").strip() or default_key

    s3.upload_file(path, bucket, key)
    print(f"Uploaded {path} -> s3://{bucket}/{key}")
```

> **✅ Checkpoint**
> A file appears in the bucket in the Console, under the key you chose.

---

### Step 4 — List objects with a paginator

This is the pattern of the day. `list_objects_v2` returns at most 1000 keys per response, and AWS gives you a continuation token to fetch the rest. A paginator handles that bookkeeping for you.

Note `page.get("Contents", [])` — an empty bucket returns a page with no `Contents` key at all, so indexing it directly will crash.

```python
def list_objects():
    bucket = input("Bucket name: ").strip()
    prefix = input("Prefix filter (Enter for all): ").strip()

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    total_objects = 0
    total_bytes = 0

    for page in pages:
        for obj in page.get("Contents", []):
            total_objects += 1
            total_bytes += obj["Size"]
            print(f"{obj['Key']:<50} {obj['Size']:>12,}  "
                  f"{obj['LastModified']:%Y-%m-%d %H:%M}")

    print(f"\n{total_objects} object(s), "
          f"{total_bytes / 1024 / 1024:.2f} MB")
```

> **✅ Checkpoint**
> Listing an empty bucket prints `(bucket is empty)` rather than raising `KeyError`. Listing a bucket with a prefix shows only the matching keys.

---

### Step 5 — Download and delete

`download_file` mirrors `upload_file`. `delete_object` is idempotent — S3 returns success even for a key that never existed, which is by design.

For a missing object, `download_file` raises a `ClientError` with code `'404'`. Catch it and say so.

```python
def download_file():
    bucket = input("Bucket name: ").strip()
    key    = input("Object key: ").strip()
    dest   = input("Save as: ").strip() or os.path.basename(key)

    try:
        s3.download_file(bucket, key, dest)
        print(f"Downloaded -> {dest}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("That object does not exist.")
        else:
            raise
```

> **✅ Checkpoint**
> You can upload a file, list it, download it under a new name, and open it.

---

### Step 6 — Generate a presigned URL

A presigned URL lets someone with no AWS account read a private object for a limited time. The signature is computed locally — this method makes no network call at all, and will happily sign a URL for an object that does not exist.

Let the user choose the expiry. Paste the result into a browser and confirm the file downloads.

```python
def generate_presigned_url():
    bucket  = input("Bucket name: ").strip()
    key     = input("Object key: ").strip()
    raw     = input("Valid for how many seconds? [3600]: ").strip()
    expires = int(raw) if raw.isdigit() else 3600

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires,
    )
    print(f"\nValid for {expires} seconds:\n{url}\n")
```

> **✅ Checkpoint**
> The URL opens the file in a browser. Opening the plain `https://bucket.s3.amazonaws.com/key` address without a signature gives Access Denied — try both and see the difference.

---

### Step 7 — Delete a bucket

A bucket must be completely empty before it can be deleted. Handle `BucketNotEmpty` with an instruction, not an error dump.

Ask the user to type the bucket name again to confirm. Destructive actions deserve a deliberate act, not a reflexive 'y'.

> **✅ Checkpoint**
> Deleting a non-empty bucket tells you to empty it first. Deleting an empty one succeeds.

---

## 5. Expected output

Your formatting may differ. The information must not.

```text
Choose an option: 4
Bucket name: youssef-lab2-demo
Prefix filter (Enter for all):

KEY                                                        SIZE  MODIFIED
--------------------------------------------------------------------------
backup/docs/notes.txt                                     1,204  2026-09-01 11:02
backup/images/logo.png                                   48,110  2026-09-01 11:02
report.csv                                                8,940  2026-09-01 10:55

3 object(s), 0.06 MB total
```

---

## 6. If something goes wrong

| You see | It means | Do this |
| --- | --- | --- |
| `BucketAlreadyExists` | Another AWS account owns that name | Bucket names are global. Add your own prefix |
| `BucketAlreadyOwnedByYou` | You created it earlier | Use it, or pick another name |
| `InvalidBucketName` | Uppercase, underscore or too short | Lowercase letters, digits, hyphens; 3–63 characters |
| `IllegalLocationConstraint` | Sent a constraint for `us-east-1` | Omit `CreateBucketConfiguration` in `us-east-1` |
| `BucketNotEmpty` | Objects still inside | Delete every object, then the bucket |
| `NoSuchBucket` | Wrong name, or wrong region | Check both. Print `Session().region_name` |
| `KeyError: 'Contents'` | The bucket or page is empty | Use `page.get("Contents", [])` |

---

## 7. Challenge

Add option 9: back up an entire local folder to S3, preserving its structure as key prefixes.

**Local folder → Python + Boto3 → Amazon S3**

- Walk the folder recursively with `os.walk()`.
- Turn each absolute path into a path relative to the folder the user chose, with `os.path.relpath()`.
- Replace `os.sep` with a forward slash before using it as a key.
- Count successes and failures, and report both at the end.

```python
for root, dirs, files in os.walk(folder):
    for filename in files:
        local_path = os.path.join(root, filename)

        relative = os.path.relpath(local_path, folder)
        key = prefix + relative.replace(os.sep, "/")

        s3.upload_file(local_path, bucket, key)
```

> **💡 Hint**
> The `replace(os.sep, "/")` line is not optional. On Windows `os.sep` is a backslash, and a key containing backslashes becomes one object with a strange name rather than a folder structure.

---

## 8. Cleanup — before you leave the room

- [ ] Every bucket you created is empty and deleted.
- [ ] The S3 Console shows no buckets belonging to you.
- [ ] Your script is committed to your Git repository.

---

## 9. Submission checklist

- [ ] `s3_manager.py` runs from a terminal with no editing.
- [ ] All eight menu options work, plus the backup challenge.
- [ ] Listing uses a paginator, not a bare `list_objects_v2` call.
- [ ] Bucket and object errors produce readable messages.
- [ ] The file is committed with a meaningful message.

---

*Lab 2 — S3 File Manager*
