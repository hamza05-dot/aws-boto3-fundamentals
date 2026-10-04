#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:11:57 2026

@author: hamza
"""
import os,boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
REGION = boto3.session.Session().region_name

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
            
if __name__ == "__main__":
    download_file()