#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 13:57:40 2026

@author: hamza
"""
import boto3
from botocore.exceptions import ClientError
 
s3 = boto3.client("s3")
REGION = boto3.session.Session().region_name

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
if __name__ == "__main__":
    create_bucket()