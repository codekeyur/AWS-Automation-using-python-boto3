import boto3
import sys

#Setup Connection to s3 via boto3 API
s3 = boto3.resource('s3')

################################
#List Objects of the Buckets
################################
for bucket in s3.bucket.all():
  print(bucket.name)
  print("---------")
  for item in bucket.objects.all():
    print("\t%s" % item.key)

################################
#Upload and Object in Bucket
################################
bucket_name = sys_argv[1]
object_name = sys_argv[1]
try:
    response = s3.Object(bucket_name, object_name).put(
        Body=open(object_name, 'rb'))
    print(response)
except Exception as e:
    print("Error while uploading an Object", e)


#################################
#Delete Object from the Bucket
#################################
try:
    response = s3.Object(bucket_name, object_name).delete(
        Body=open(object_name, 'rb'))
    print(response)
except Exception as e:
    print(f"Error While deleting Object from {bucket_name}", e)    