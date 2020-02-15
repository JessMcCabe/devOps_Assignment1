#!/usr/bin/env python3
import sys
import boto3
import urllib.request
s3 = boto3.resource("s3")
if sys.argv[1:] is None:
  print("You did not provide a bucket name, please provide a bucket name")
else:
  # object name is the file we want to download
  bucket_name = sys.argv[1]
  object_name = 'http://devops.witdemo.net/image.jpg'
  try:
  # Use urllib request to download the file to the current directory and name it as pic.jpg
    urllib.request.urlretrieve(object_name, "pic.jpg")
  except Exception as error:
    print (error)
  try:
  # Upload the file to my own bucket
      response = s3.Object(bucket_name, "pic.jpg").put(ACL='public-read',Body=open("pic.jpg", 'rb'))
      print (response)
  except Exception as error:
      print (error)
