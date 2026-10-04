"""
Created on Mon Sep 28 14:22:03 2026

@author: hamza
"""
import boto3
s3 = boto3.client("s3")

def list_objects():
    bucket = input("Bucket name: ").strip()
    prefix = input("Prefix filter (Enter for all): ").strip()
 
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
 
    total_objects = 0
    total_bytes = 0
 

    print(f"\n{'KEY':<50} {'SIZE':>12}  {'MODIFIED'}")
    print("-" * 74)

    for page in pages:
        for obj in page.get("Contents", []):
            total_objects += 1
            total_bytes += obj["Size"]
            print(f"{obj['Key']:<50} {obj['Size']:>12,}  "
                  f"{obj['LastModified']:%Y-%m-%d %H:%M}")
 

    print(f"\n{total_objects} object(s), "
          f"{total_bytes / 1024 / 1024:.2f} MB total")
    
if __name__ == "__main__":
    list_objects()
