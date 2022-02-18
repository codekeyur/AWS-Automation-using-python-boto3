#!/usr/bin/env python3

import boto3
from  botocore.exceptions import ClientError

DRYRUN = False

print("-----------------------------------------------")
print("-------Launch Windows Server 2016 on AWS-------")
print("-----------------------------------------------")
print("In order to connect to your instance you will need key-pair please enter 1 to create new key-pair oe 2 to continue to use existing key-pair")
print("""
1 - Create new key pair
2 - To continue and use existing key-pair
""")
####----Creating Key pair and Save pem file to current wdir----####
#-----------------------------------------------------------------#
ec2_client=boto3.client('ec2')
def create_key_pair():
     key_pair=ec2_client.create_key_pair(KeyName='Windows-key')
     private_key=key_pair['KeyMaterial']
     with open('Windows-key.pem', 'w') as f:
       f.write(private_key)
     
userInputKeyPair=int(input())

if userInputKeyPair == 1:
   create_key_pair()

print("------Creating Security Group------")
print("-----------------------------------")

response = ec2_client.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId','')
try:
  response = ec2_client.create_security_group(
                    GroupName="Windows Server Security Group",
                    Description="Windows Server Sg",
                    VpcId=vpc_id,
                    TagSpecifications=[
                                {
                                    'ResourceType': 'security-group',
                                    'Tags': [
                                               {
                                                   'Key': 'Name',
                                                   'Value': 'Windows Server Sg'
                                               },
                                             ]
                                }      
                              ]
                           ) 
  security_group_id=response['GroupId']
  print("Security Group created %s in vpc %s." % (security_group_id,vpc_id))
  

####----Define Security Rules----####
#-----------------------------------#
  data = ec2_client.authorize_security_group_ingress(
      GroupId=security_group_id,
      IpPermissions=[
          { 'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
          { 'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges' : [{'CidrIp': '0.0.0.0/0'}]}
          ])
  print("Ingress Successfully set %s." % data)

except ClientError as e:
  print(e)

#to see all the images available on AWS owned by amazon.
images = ec2_client.describe_images(
    Filters=[
        {
            'Name':'name',
            'Values': [
                'Windows_Server-2016-English-Core-Base*',
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
count=0
os=images['Images']
for ami in os:
    count += 1
    print(count, "-",ami['ImageLocation']) 

print("----------------------------------------------")
print("------Select which image you want to use------")
print("----------------------------------------------")

userInput=int(input())

if userInput == 1:
   imageid=images['Images'][0]['ImageId']
   instance = ec2_client.run_instances(
       ImageId=imageid,
       InstanceType = 't2.micro',
       KeyName="Windows-key",
       MaxCount=1,
       MinCount=1,
       SecurityGroupIds=security_group_id,
       DryRun=DRYRUN,
       TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Windows Server 2016'
                },
            ]
        }
      ]
    )
   print("Instance Successfully Launched")     
else:
   print("Luanch failed !!")

#verify the instance launch using correct imageId


