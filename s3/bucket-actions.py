#!/bin/python

import boto3
#import json

s3=boto3.client("s3")
print("-----------------------------------------")
print("Please Select from the following options.")
print("-----------------------------------------")
print("""
 1 - Create Bucket
 2 - Delete Bucket
 3 - List Existing Bucket
 4 - See objects inside the bucket
""")
userInput = int(input())

def create_bucket():
    bucketName=str(input("Enter the Bucket Name: "))
    bucket=s3.create_bucket(Bucket=bucketName)
    print(bucket)

def delete_bucket():
    list_bucket()
    print("Please enter name of the bucket that you want to delete from the following bucket list: ")
    selectedBucket=str(input())
    deleteBucket=s3.delete_bucket(
        Bucket=selectedBucket
    )
    print(deleteBucket)

def list_bucket():
    response=s3.list_buckets()
    buckets=response['Buckets']
    count = 0
    for bucket in buckets:
        count += 1
        print(count, "-" , bucket['Name'])

def list_objects():
    print("Make sure You must have at least permission to read object.")
    
if userInput == 1:
  create_bucket()
elif userInput == 2:
    delete_bucket()
elif userInput == 3:
    list_bucket()
#elif userInput ==4:
#    list_object()
else:
  print("Please select valid option.")



#bucket=s3.create_bucket(Bucket=BUCKETNAME)





