#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:01:13 2026

@author: hamza
"""

import boto3

ec2 = boto3.client("ec2")

def list_instances():
    paginator = ec2.get_paginator("describe_instances")

    rows = []
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for inst in reservation["Instances"]:
                if inst["State"]["Name"] != "terminated":
                    rows.append(inst)
    print("\n" + "=" * 85)
    print("                    EC2 INSTANCE MANAGER")
    print("=" * 85)
    
    print(f"{'INSTANCE ID':<21} "
          f"{'TYPE':<12} "
          f"{'STATE':<12} "
          f"{'PUBLIC IP':<16} "
          f"{'NAME'}")
    
    print("-" * 85)
    
    for inst in rows:
        tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
        print(f"{inst['InstanceId']:<21} "
              f"{inst['InstanceType']:<12} "
              f"{inst['State']['Name']:<12} "
              f"{inst.get('PublicIpAddress', '-'):<16} "
              f"{tags.get('Name', '(no name)')}")
    

    return rows


if __name__ == "__main__":
    list_instances()