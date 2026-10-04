#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:44:28 2026

@author: hamza
"""

import boto3

s3 = boto3.client("s3")

def list_buckets():
    """Affiche la liste de tous les buckets S3 de votre compte."""
    print("\nCREATION DATE        BUCKET NAME")
    print("-" * 50)
    
    response = s3.list_buckets()
    for bucket in response.get('Buckets', []):
        print(f"{bucket['CreationDate']:%Y-%m-%d %H:%M}     {bucket['Name']}")
        
if __name__ == "__main__":
    list_buckets()