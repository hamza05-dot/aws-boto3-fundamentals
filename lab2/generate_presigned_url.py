#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:17:41 2026

@author: hamza
"""
import boto3
s3 = boto3.client("s3")

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
    
    
if __name__ == "__main__":
    generate_presigned_url()
