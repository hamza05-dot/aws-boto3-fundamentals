#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:05:36 2026

@author: hamza
"""

import os,boto3 
s3 = boto3.client("s3")
REGION = boto3.session.Session().region_name

 
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
    
if __name__ == "__main__":
    upload_file()

