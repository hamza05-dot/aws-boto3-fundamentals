#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:10:04 2026

@author: hamza
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError, WaiterError
from list_ec2 import list_instances
from select_ec2 import select_instance

ec2 = boto3.client("ec2", region_name="us-east-1")



def start_instance():
    instance_id = select_instance()
    if not instance_id:
        return

    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        change = response["StartingInstances"][0]

        print(
            f"{change['PreviousState']['Name']} -> "
            f"{change['CurrentState']['Name']}"
        )

        ec2.get_waiter("instance_running").wait(
            InstanceIds=[instance_id],
            WaiterConfig={"Delay": 15, "MaxAttempts": 40},
        )

        print("Instance is running.")

    except (ClientError, WaiterError) as e:
        print(f"Could not start instance: {e}")


def stop_instance():
    """Stop a running instance and wait until it is stopped."""
    instance_id = select_instance()
    if not instance_id:
        return

    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        change = response["StoppingInstances"][0]

        print(
            f"{change['PreviousState']['Name']} -> "
            f"{change['CurrentState']['Name']}"
        )

        ec2.get_waiter("instance_stopped").wait(
            InstanceIds=[instance_id],
            WaiterConfig={"Delay": 15, "MaxAttempts": 40},
        )

        print("Instance is stopped.")

    except (ClientError, WaiterError) as e:
        print(f"Could not stop instance: {e}")


def reboot_instance():
    instance_id = select_instance()
    if not instance_id:
        return

    try:
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"Reboot request sent for {instance_id}.")

    except ClientError as e:
        print(f"Could not reboot instance: {e}")


def terminate_instance():
    instance_id = select_instance()
    if not instance_id:
        return

    confirmation = input(
        f"Type YES to terminate {instance_id}: "
    ).strip()

    if confirmation != "YES":
        print("Termination cancelled.")
        return

    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        change = response["TerminatingInstances"][0]

        print(
            f"{change['PreviousState']['Name']} -> "
            f"{change['CurrentState']['Name']}"
        )

        ec2.get_waiter("instance_terminated").wait(
            InstanceIds=[instance_id],
            WaiterConfig={"Delay": 15, "MaxAttempts": 40},
        )

        print("Instance terminated.")

    except (ClientError, WaiterError) as e:
        print(f"Could not terminate instance: {e}")


if __name__ == "__main__":
    actions = {
        "1": start_instance,
        "2": stop_instance,
        "3": reboot_instance,
        "4": terminate_instance,
    }

    while True:
        print("\n========== EC2 ACTIONS ==========")
        print("1. Start instance")
        print("2. Stop instance")
        print("3. Reboot instance")
        print("4. Terminate instance")
        print("0. Exit")
        print("=================================")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Exiting.")
            break

        action = actions.get(choice)

        if action:
            action()
        else:
            print("Invalid choice.")
