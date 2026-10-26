#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 14:16:05 2026

@author: hamza
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from list_ec2 import list_instances


def select_instance():
    """Display EC2 instances and return the selected instance ID."""

    instances = list_instances()

    if not instances:
        print("No instances available.")
        return None

    instance_id = input("Enter the instance ID: ").strip()

    for inst in instances:
        if inst["InstanceId"] == instance_id:
            return instance_id

    print("Invalid instance ID.")
    return None


if __name__ == "__main__":
    selected = select_instance()

    if selected:
        print("Selected instance:", selected)
