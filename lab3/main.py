
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from list_ec2 import list_instances
from create_ec2 import launch_instance
from ec2_actions import (
    start_instance,
    stop_instance,
    reboot_instance,
    terminate_instance,
)
from describe_ec2 import describe_instance
from add_tag import add_tag
from clean_ec2 import cleanup_instances


def main():
    actions = {
        "1": ("List instances", list_instances),
        "2": ("Launch instance", launch_instance),
        "3": ("Start instance", start_instance),
        "4": ("Stop instance", stop_instance),
        "5": ("Reboot instance", reboot_instance),
        "6": ("Describe instance", describe_instance),
        "7": ("Add tag", add_tag),
        "8": ("Terminate instance", terminate_instance),
        "9": ("Cleanup lab instances", cleanup_instances),
    }

    while True:
        print("\n" + "=" * 40)
        print("       EC2 INSTANCE MANAGER")
        print("=" * 40)

        for number, (label, _) in actions.items():
            print(f"{number}. {label}")

        print("0. Exit")
        print("=" * 40)

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Exiting EC2 Manager.")
            break

        action = actions.get(choice)

        if action:
            try:
                action[1]()
            except Exception as error:
                print(f"Operation failed: {error}")
        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()
