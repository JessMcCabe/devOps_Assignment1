#!/usr/bin/env python3

# imports
import boto3
import subprocess

# Part 1 Create new instance

ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId='ami-0713f98de93617bb4',
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=['sg-0990a25453de95f30'],
    UserData="""#!/bin/bash
                yum update -y
                yum install httpd -y
                systemctl enable httpd
                systemctl start httpd""",
    KeyName='webserver_key',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
             'Tags': [
                 {
                     'Key': 'Name',
                     'Value': 'WebServer'
                 },
              ]
        },
    ],
    InstanceType='t2.nano')
print (instance[0].id)


# Part 2 Create new Bucket - Call the create bucket script passing the bucket name
cmd = "./create_bucket.py assignment01-bucket1-$(date +%F-%s)"
subprocess.call(cmd, shell=True)

