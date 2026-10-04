#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:41:53 2026

@author: hamza
"""
import boto3 
from botocore.exceptions import ClientError
s3 = boto3.client("s3")

def delete_bucket():
    bucket = input("Bucket name to delete: ").strip()
    confirm_name = input("Type the bucket name again to confirm deletion: ").strip()
    
    if confirm_name == bucket:
        try:
            s3.delete_bucket(Bucket=bucket)
            print(f"Bucket '{bucket}' successfully deleted.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketNotEmpty':
                print(f"Error: Bucket '{bucket}' is not empty. You must delete all objects before deleting the bucket.")
            else:
                print(f"An error occurred: {e.response['Error']['Message']}")
    else:
        print("Confirmation failed. Bucket name did not match. Deletion canceled.")
        
if __name__ == "__main__":
    delete_bucket()
