#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:14:58 2026

@author: hamza
"""

import boto3

ssm = boto3.client("ssm")

def get_latest_amazon_linux_ami():
    parameter = ("/aws/service/ami-amazon-linux-latest/"
                 "al2023-ami-kernel-default-x86_64")
    response = ssm.get_parameter(Name=parameter)
    return response["Parameter"]["Value"]

if __name__ == "__main__":
    print(get_latest_amazon_linux_ami())