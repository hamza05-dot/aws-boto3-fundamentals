
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
from select_ec2 import select_instance

ec2 = boto3.client("ec2", region_name="us-east-1")


def add_tag():

    instance_id = select_instance()

    if not instance_id:
        return

    key = input("Enter tag key: ").strip()
    value = input("Enter tag value: ").strip()

    if not key or not value:
        print("Tag key and value cannot be empty.")
        return

    try:
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[{"Key": key, "Value": value}]
        )

        print(f"Tag added successfully to {instance_id}.")
        print(f"{key} = {value}")

    except ClientError as e:
        print(f"Could not add tag: {e}")


if __name__ == "__main__":
    add_tag()
