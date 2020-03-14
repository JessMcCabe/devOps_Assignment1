#!/usr/bin/env python3

# imports
import boto3
import subprocess
import time 
import config as cfg

# Create varaible to store paramteres provided in cofig file

SecurityGroupIds = cfg.SecurityGroupIds
KeyName= cfg.KeyName
BucketName=cfg.BucketName
PemKey=cfg.PemKey

# Create new instance

print("START Step: Create new nano instance")

try:
  ec2 = boto3.resource('ec2')
  instance = ec2.create_instances(
      ImageId='ami-0713f98de93617bb4',
      MinCount=1,
      MaxCount=1,
      SecurityGroupIds=[SecurityGroupIds],
      UserData="""#!/bin/bash
                  yum update -y
                  yum install httpd -y
                  systemctl enable httpd
                  systemctl start httpd""",
      KeyName=KeyName,
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
  print("COMPLETE Step: Create new nano instance")
except Exception as error:
  print (error)
  print("ERROR in Step: Create new nano instance")







# Get the private IP address of the newly created ec2 instance
# 
# Call reload so the information is up to date
# Wait until the instance is running

try:
  instance=ec2.Instance(myInstId)
  instance.reload()

  print("WAIT until instance is running")

  instance.wait_until_running()
  instance.reload()
  myIP=instance.public_ip_address
  print("The public IP address is:")
  print (myIP)
except:
  print (error)


instance.reload()





# Create & Build html home page
# 
# Build Up the command strings in a variable
# Run the command using subprocess.run

try:
  print("START Step: Create index.html")

  cmd1 = "echo '<html>' > index.html"
  cmd2 = "echo 'Public IP Address: " + myIP + "'>> index.html"
  cmd3 = """curl --silent http://169.254.169.254/latest/meta-data/instance-id >> index.html"""

  subprocess.run(cmd1, shell=True)

  subprocess.run(cmd2, shell=True)

  subprocess.run(cmd3, shell=True)

  print("COMPLETE Step: Create index.html")
except:
  print (error)
  print("ERROR in Step: Create index.html")






# Create new Bucket - Call the create bucket script passing the bucket name
# 
# create_bucket.py expects 1 parameter - This is a unique bucket name


try:
  print("START Step: Create new bucket")
  cmd = "./create_bucket.py " + BucketName
  subprocess.run(cmd, shell=True)

  print("COMPLETE Step: Create new bucket")
except:
 print(error)
 print("ERROR in Step: Create new bucket")






# Wait for Status checks to complete
# 
# Generally found it takes up to 2 minutes for the checks to complete
# System Status Check and Instance Status Check 



print("Wait for Status Checks to Complete - 2 minutes remaining")
time.sleep(30)
instance.reload()


print("Wait for Status Checks to Complete - 1 minute 30 seconds remaining")
time.sleep(30)
instance.reload()


print("Wait for Status Checks to Complete - 1 minute remaining")
time.sleep(30)
instance.reload()


print("Wait for Status Checks to Complete - 30 seconds remaining")
time.sleep(30)
instance.reload()


print("Wait Complete")






# Create Index.html page 
# 
# Copy it to /var/www/html/

try:
  print("START Step: Secure Copy index.html to ec2 instance home")

  cmd6 = "scp -o StrictHostKeyChecking=no -rp -i " + PemKey + " index.html ec2-user@" + myIP + ":"
  subprocess.run(cmd6, shell=True)

  print("COMPLETED Step: Secure Copy index.html to ec2 instance home")


  print("START Step: SSH on to instance and copy index.html to /var/www/html/")

  cmd7 = "ssh -t -o StrictHostKeyChecking=no -i " + PemKey + " ec2-user@" + myIP + " 'sudo cp index.html /var/www/html/'"
  subprocess.run(cmd7, shell=True)

  print("COMPLETED Step: SSH on to instance and copy index.html to /var/www/html/")

except:
 print(error)
 print("ERROR in Step: Index.html creation and copy")






