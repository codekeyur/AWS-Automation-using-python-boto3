import boto3

def CreateBucket(name):
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=name)
    return True

def DeleteBucket(name):
    s3_client = boto3.client('s3')
    s3_client.delete_bucket(Bucket=name)
    return True    



    if __name__ == "__main__":
        Name = "testbucket-s3-lab"
        CreateBucket(Name)
       #DeleteBucket(Name)