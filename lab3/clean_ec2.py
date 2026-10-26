#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:23:25 2026

@author: hamza
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError, WaiterError

ec2 = boto3.client("ec2", region_name="us-east-1")


def cleanup_instances():
    """Terminate lab-created EC2 instances safely."""

    try:
        response = ec2.describe_instances(
            Filters=[
                {
                    "Name": "tag:CreatedBy",
                    "Values": ["boto3-lab"]
                },
                {
                    "Name": "instance-state-name",
                    "Values": [
                        "pending",
                        "running",
                        "stopping",
                        "stopped"
                    ]
                }
            ]
        )

        instances = []

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append(instance)

        if not instances:
            print("No lab-created instances found.")
            return

        print("\nLab-created instances:")
        for instance in instances:
            tags = {
                tag["Key"]: tag["Value"]
                for tag in instance.get("Tags", [])
            }

            print(
                f"{instance['InstanceId']} | "
                f"{tags.get('Name', '(no name)')} | "
                f"{instance['State']['Name']}"
            )

        print(f"\nFound {len(instances)} instance(s).")
        confirmation = input(
            "Type YES to terminate ALL listed instances: "
        ).strip()

        if confirmation != "YES":
            print("Cleanup cancelled.")
            return

        instance_ids = [
            instance["InstanceId"]
            for instance in instances
        ]

        ec2.terminate_instances(InstanceIds=instance_ids)

        print("Termination requested. Waiting for completion...")

        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(
            InstanceIds=instance_ids,
            WaiterConfig={
                "Delay": 15,
                "MaxAttempts": 40
            }
        )

        print("Cleanup complete. All selected instances are terminated.")

    except WaiterError as e:
        print(f"Timed out waiting for termination: {e}")

    except ClientError as e:
        print(f"AWS error during cleanup: {e}")


if __name__ == "__main__":
    cleanup_instances()
