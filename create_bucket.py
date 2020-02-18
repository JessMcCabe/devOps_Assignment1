#!/usr/bin/env python3
import sys
import boto3
import urllib.request

# Location to retrieve image from
object_name = 'http://devops.witdemo.net/image.jpg'

# Create a bucket accepting a parameter to name the bucket
# Save the name of the created bucket
s3 = boto3.resource("s3")
if sys.argv[1:] is None:
  print("You did not provide a bucket name, please provide a unique bucket name")
else:
  for bucket_name in sys.argv[1:]:
    try:
        response = s3.create_bucket(Bucket=bucket_name, ACL='public-read',CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        created_bucket = response.name
        print (created_bucket)
    except Exception as error:
        print (error)

# Load Image to bucket (must run after image has been retrieved from server)

try:
  # Use urllib request to download the file to the current directory and name it as pic.jpg
  urllib.request.urlretrieve(object_name, "pic.jpg")
except Exception as error:
  print (error)
try:
  # Upload the file to newly created bucket and make public
  response = s3.Object(created_bucket, "pic.jpg").put(ACL='public-read',Body=open("pic.jpg", 'rb'))
  print (response)
except Exception as error:
  print (error)
