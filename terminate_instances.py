#!/usr/bin/env python3
import sys
import boto3
ec2 = boto3.resource('ec2')
if sys.argv[1:] True
    for instance_id in sys.argv[1:]:
        instance = ec2.Instance(instance_id)
        response = instance.terminate()
        print (response)
else 
  print("You did not provide an instance id, please provide the id of the instance you wish to terminate")
  quit()
