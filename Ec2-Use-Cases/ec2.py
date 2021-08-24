import boto3

DRYRUN = True

ec2_client = boto3.client('ec2')
#to see all the images available on AWS owned by amazon.
images = ec2_client.describe_images(
    Filters=[
        {
            'Name':'name',
            'Values': [
                'amzn2-ami-hvm*',
            ]
        },
        {
            'Name':'owner-alias',
            'Values':[
                'amazon',
            ]
        },
    ],
)

#to print first ImageId in the list and using that we will launch our instace
imageId=images['Images'][0]['ImageId']
print(imageId)
instance = ec2_client.run_instances(
    ImageId=imageId,
    InstanceType = 't2.micro',
    MaxCount=1,
    MinCount=1,
    DryRun=DRYRUN
)

#verify the instance launch using correct imageId
print(instance)