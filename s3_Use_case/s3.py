import boto3

def CreateBucket(name):
    s3_client = boto3.client('s3')
    bucket_created = s3_client.create_bucket(Bucket=name)
    print(bucket_created)
    return True

def DeleteBucket(name):
    s3_client = boto3.client('s3')
    bucket_deleted = s3_client.delete_bucket(Bucket=name)
    print(bucket_deleted)
    return True    



    if __name__ == "__main__":
        Name = "testbucket-s3-lab"
        CreateBucket(Name)
       #DeleteBucket(Name)