#!/usr/bin/python3
import boto3
#import uuid
import logging
import os

ec2 = boto3.resource('ec2')
# Boto3
# Use the filter() method of the instances collection to retrieve
# all running EC2 instances.
instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:k8s.io/role/master', 'Values': ['1']},
             {'Name': 'instance-state-code', 'Values': ['16']}])
for instance in instances:
    print(instance.id, instance.instance_type)



    