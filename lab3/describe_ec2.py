#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:22:09 2026

@author: hamza
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
from select_ec2 import select_instance

ec2 = boto3.client("ec2", region_name="us-east-1")


def describe_instance():

    instance_id = select_instance()

    if not instance_id:
        return

    try:
        response = ec2.describe_instances(
            InstanceIds=[instance_id]
        )

        instance = response["Reservations"][0]["Instances"][0]

        tags = {
            tag["Key"]: tag["Value"]
            for tag in instance.get("Tags", [])
        }

        print("\n" + "=" * 45)
        print("           EC2 INSTANCE DETAILS")
        print("=" * 45)

        print(f"Instance ID       : {instance['InstanceId']}")
        print(f"Name              : {tags.get('Name', '(no name)')}")
        print(f"State             : {instance['State']['Name']}")
        print(f"Instance Type     : {instance['InstanceType']}")
        print(f"AMI ID            : {instance['ImageId']}")
        print(f"Availability Zone : {instance['Placement']['AvailabilityZone']}")
        print(f"Private IP        : {instance.get('PrivateIpAddress', '-')}")
        print(f"Public IP         : {instance.get('PublicIpAddress', '-')}")
        print(f"Key Pair          : {instance.get('KeyName', '-')}")
        print(f"Launch Time       : {instance['LaunchTime']}")

        print("\nSecurity Groups:")
        for group in instance.get("SecurityGroups", []):
            print(f"  {group['GroupId']} - {group['GroupName']}")

        print("\nTags:")
        if tags:
            for key, value in tags.items():
                print(f"  {key}: {value}")
        else:
            print("  No tags")

        print("=" * 45)

    except ClientError as e:
        print(f"Could not describe instance: {e}")


if __name__ == "__main__":
    describe_instance()
