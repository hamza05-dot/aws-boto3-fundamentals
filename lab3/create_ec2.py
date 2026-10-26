
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import WaiterError, ClientError
from ami_save import get_latest_amazon_linux_ami


def launch_instance():
    """Launch an EC2 instance and wait until it is running."""

    ec2 = boto3.client("ec2")

    try:
        ami_id = get_latest_amazon_linux_ami()
        print("Using AMI:", ami_id)

        name = input("Donner votre EC2 name : ").strip()

        if not name:
            print("Instance name cannot be empty.")
            return

        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType="t3.micro",
            MinCount=1,
            MaxCount=1,
            KeyName="vockey",
            TagSpecifications=[{
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": name},
                    {"Key": "CreatedBy", "Value": "boto3-lab"},
                ],
            }],
        )

        instance_id = response["Instances"][0]["InstanceId"]

        print(f"Launched {instance_id}")
        print("Initial state:",
              response["Instances"][0]["State"]["Name"])

        try:
            print("Waiting for the instance to reach 'running'...")

            waiter = ec2.get_waiter("instance_running")
            waiter.wait(
                InstanceIds=[instance_id],
                WaiterConfig={"Delay": 15, "MaxAttempts": 40},
            )

            print("Instance is running.")

        except WaiterError as e:
            print(f"Timed out waiting for the instance: {e}")
            return

        detail = ec2.describe_instances(
            InstanceIds=[instance_id]
        )
        instance = detail["Reservations"][0]["Instances"][0]

        print("Public IP:",
              instance.get("PublicIpAddress", "not assigned"))

    except ClientError as e:
        print(f"AWS error: {e}")


if __name__ == "__main__":
    launch_instance()
