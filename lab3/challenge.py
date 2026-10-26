#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from ami_save import get_latest_amazon_linux_ami
import urllib.request
import urllib.error
import time

ec2 = boto3.client("ec2")

response = ec2.describe_vpcs(
    Filters=[
        {"Name": "isDefault", "Values": ["true"]}
    ]
)

vpc_id = response["Vpcs"][0]["VpcId"]

response = ec2.create_security_group(
    GroupName="boto3-lab-web",
    Description="Allow HTTP traffic for the Boto3 lab",
    VpcId=vpc_id,
    TagSpecifications=[
        {
            "ResourceType": "security-group",
            "Tags": [
                {"Key": "CreatedBy", "Value": "boto3-lab"}
            ]
        }
    ]
)

group_id = response["GroupId"]
print("Security Group ID:", group_id)

ec2.authorize_security_group_ingress(
    GroupId=group_id,
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [
                {"CidrIp": "0.0.0.0/0"}
            ]
        }
    ]
)

script1 = """#!/bin/bash
dnf install -y httpd
echo "<h1>Hello from Server 1</h1><p>Deployed by Hamza</p>" > /var/www/html/index.html
systemctl enable --now httpd
"""

script2 = """#!/bin/bash
dnf install -y httpd
echo "<h1>Hello from Server 2</h1><p>Deployed by Hamza</p>" > /var/www/html/index.html
systemctl enable --now httpd
"""

instances = []

for name, script in [
    ("web-server-1", script1),
    ("web-server-2", script2)
]:
    response = ec2.run_instances(
        ImageId=get_latest_amazon_linux_ami(),
        InstanceType="t3.micro",
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[group_id],
        UserData=script,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": name},
                    {"Key": "CreatedBy", "Value": "boto3-lab"}
                ]
            }
        ]
    )

    instance_id = response["Instances"][0]["InstanceId"]
    instances.append(instance_id)
    print(name, ":", instance_id)

for instance_id in instances:
    print("Waiting for instance to start:", instance_id)
    ec2.get_waiter("instance_running").wait(
        InstanceIds=[instance_id]
    )

    print("Waiting for instance status checks:", instance_id)
    ec2.get_waiter("instance_status_ok").wait(
        InstanceIds=[instance_id]
    )

response = ec2.describe_instances(
    InstanceIds=instances
)

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        name = next(
            tag["Value"]
            for tag in instance.get("Tags", [])
            if tag["Key"] == "Name"
        )

        public_ip = instance.get("PublicIpAddress")
        url = f"http://{public_ip}"

        print(name, "URL:", url)

        for attempt in range(6):
            try:
                with urllib.request.urlopen(url, timeout=10) as page:
                    print("HTTP Status:", page.status)
                    print("Page content:")
                    print(page.read().decode("utf-8"))
                break
            except urllib.error.URLError as e:
                if attempt == 5:
                    print("Could not access the web page:", e)
                else:
                    time.sleep(10)