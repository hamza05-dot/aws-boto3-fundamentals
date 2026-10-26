#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:20:02 2026

@author: hamza
"""

import boto3

ec2 = boto3.client("ec2")

response = ec2.describe_security_groups(
    Filters=[
        {
            "Name": "tag:CreatedBy",
            "Values": ["boto3-lab"]
        }
    ]
)

for group in response["SecurityGroups"]:
    group_id = group["GroupId"]

    ec2.delete_security_group(
        GroupId=group_id
    )

    print("Deleted security group:", group_id)