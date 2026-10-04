#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:10:10 2026

@author: hamza
"""

import os
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

def backup_folder():
    """Sauvegarde un dossier local entier sur S3 en préservant sa structure."""
    folder = input("Local folder path to backup: ").strip()
    
    if not os.path.isdir(folder):
        print(f"Error: Local folder '{folder}' does not exist.")
        return

    bucket = input("Target S3 Bucket name: ").strip()
    prefix = input("S3 Prefix filter/folder (Enter for root): ").strip()
    if prefix and not prefix.endswith("/"):
        prefix += "/"

    success_count = 0
    failure_count = 0

    print("\nStarting backup...")
    print("-" * 50)

 
    for root, dirs, files in os.walk(folder):
        for filename in files:
            local_path = os.path.join(root, filename)
            
           
            relative = os.path.relpath(local_path, folder)
            
            
            key = prefix + relative.replace(os.sep, "/")
            
            try:
                
                s3.upload_file(local_path, bucket, key)
                print(f"Uploaded: {relative} -> s3://{bucket}/{key}")
                success_count += 1
            except ClientError as e:
                print(f"Failed to upload {relative}: {e.response['Error']['Message']}")
                failure_count += 1
            except Exception as e:
                print(f"Failed to upload {relative}: {str(e)}")
                failure_count += 1

    
    print("-" * 50)
    print(f"Backup complete: {success_count} success(es), {failure_count} failure(s).")


if __name__ == "__main__":
    backup_folder()
