#!/usr/bin/env python3

# imports
import boto3
import subprocess
import time 
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
myInstId=instance[0].id
print (instance[0].id)




# Get the private IP address of the newly created ec2 instance
instance=ec2.Instance(myInstId)
instance.reload()


instance.wait_until_running()
instance.reload()
myIP=instance.public_ip_address
print (myIP)


instance.reload()
# Creat & Build html home page
cmd1 = "echo '<html>' > index.html"
cmd2 = cmd2 = "echo 'Private IP Address: " + myIP + "'>> index.html"
cmd3 = """curl --silent http://169.254.169.254/latest/meta-data/instance-id/ >> index.html"""

subprocess.run(cmd1, shell=True)

subprocess.run(cmd2, shell=True)

subprocess.run(cmd3, shell=True)

# Part 2 Create new Bucket - Call the create bucket script passing the bucket name
cmd = "./create_bucket.py assignment01-bucket1-$(date +%F-%s)"
subprocess.run(cmd, shell=True)

print("Wait for Status Checks to Complete")
time.sleep(120)
instance.reload()
cmd6 = "scp -o StrictHostKeyChecking=no -rp -i /home/jess/webserver_key.pem index.html ec2-user@" + myIP + ":"
subprocess.run(cmd6, shell=True)

cmd7 = "ssh -t -o StrictHostKeyChecking=no -i /home/jess/webserver_key.pem ec2-user@" + myIP + " 'sudo cp index.html /var/www/html/'"
subprocess.run(cmd7, shell=True)



