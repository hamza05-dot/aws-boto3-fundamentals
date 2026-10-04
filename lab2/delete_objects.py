#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:46:29 2026

@author: hamza
"""

import boto3
s3 =s3 = boto3.client("s3")

def delete_objects():
    bucket = input("Bucket name: ").strip()
    choice = input("Delete [1] single object, [2] multiple specific objects, or [3] ALL objects? (1/2/3): ").strip()

    if choice == "1":
        key = input("Enter object KEY to delete: ").strip()
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Object '{key}' deleted successfully.")

    elif choice == "2":
        keys_input = input("Enter object KEYs to delete (separated by commas): ")
        objects_to_delete = [{"Key": k.strip()} for k in keys_input.split(",") if k.strip()]
        
        if objects_to_delete:
            s3.delete_objects(Bucket=bucket, Delete={"Objects": objects_to_delete})
            print(f"{len(objects_to_delete)} objects deleted successfully.")
        else:
            print("No valid keys provided.")

    elif choice == "3":
        confirm = input(f"Type the bucket name again ('{bucket}') to confirm deleting ALL objects: ").strip()
        if confirm == bucket:
            paginator = s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket)
            deleted_count = 0
            for page in pages:
                if "Contents" in page:
                    objects_to_delete = [{"Key": obj["Key"]} for obj in page["Contents"]]
                    s3.delete_objects(Bucket=bucket, Delete={"Objects": objects_to_delete})
                    deleted_count += len(objects_to_delete)
            
            print(f"Success. Deleted all {deleted_count} objects. Bucket is now empty.")
        else:
            print("Confirmation failed. Action canceled.")
            
    else:
        print("Invalid choice.")
    
if __name__ == "__main__":    
    delete_objects()