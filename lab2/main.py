#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:52:00 2026

@author: hamza
"""
import sys


try:
    from create_bucket import create_bucket
    from list_bucket import list_buckets
    from upload_file import upload_file      
    from list_objects import list_objects
    from download_file import download_file  
    from delete_objects import delete_objects
    from generate_presigned_url import generate_presigned_url
    from delete_bucket import delete_bucket
    from backup_folder import backup_folder

except ImportError as e:
    print(f"Erreur d'importation : {e}")
    print("Assurez-vous que tous vos scripts .py contiennent bien les fonctions associées.")

def menu():
    while True:
        print("\n=========================================")
        print("           S3 MANAGER")
        print("=========================================")
        print("  1. Create Bucket        5. Download File")
        print("  2. List Buckets         6. Delete File (Objects)")
        print("  3. Upload File          7. Generate Presigned URL")
        print("  4. List Files           8. Delete Bucket")
        print("  9. Backup Local Folder  0. Exit")
        print("=========================================")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            create_bucket()
        elif choice == "2":
            list_buckets()
        elif choice == "3":
            upload_file()
        elif choice == "4":
            list_objects()
        elif choice == "5":
            download_file()
        elif choice == "6":
            delete_objects()
        elif choice == "7":
            generate_presigned_url()
        elif choice == "8":
            delete_bucket()
        elif choice == "9":
            backup_folder()
        elif choice == "0":
            print("Exiting S3 Manager. Goodbye!")
            sys.exit(0)
        else:2
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    menu()
