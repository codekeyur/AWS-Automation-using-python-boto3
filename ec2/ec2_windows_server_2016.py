#!/usr/bin/env python3

from time import sleep
import boto3
from  botocore.exceptions import ClientError

resource=boto3.resource('ec2')
ec2_client=boto3.client('ec2') 
vpcs = ec2_client.describe_vpcs()
vpc_id = vpcs.get('Vpcs', [{}])[0].get('VpcId','')
subnets = ec2_client.describe_subnets()
subnet_id = subnets['Subnets'][0]['SubnetId']

DRYRUN = False
print("-----------------------------------------------")
print("-------Launch Windows Server 2016 on AWS-------")
print("-----------------------------------------------")
print("In order to connect to your instance you will need key-pair please enter 1 to create new key-pair oe 2 to continue to use existing key-pair")
sleep(5)
print("""
1 - Create new key pair
2 - To continue and use existing key-pair
""")
####----Creating Key pair and Save pem file to current wdir----####
#-----------------------------------------------------------------#

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

security_group = resource.create_security_group(
                    GroupName="Windows Server Desktop Experience Security Group",
                    Description="Windows Server Desktop Sg Standard Base",
                    VpcId=vpc_id,
                    TagSpecifications=[
                                {
                                    'ResourceType': 'security-group',
                                    'Tags': [
                                               {
                                                   'Key': 'Name',
                                                   'Value': 'Windows Server Desktop Exp Standard Base Server'
                                               },
                                             ]
                                }      
                              ]
                           ) 
print("Security Group created %s " % security_group.group_id)
  

####----Define Security Rules----####
#-----------------------------------#

data = security_group.authorize_ingress(
      GroupId=security_group.group_id,
      IpPermissions=[
          { 'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
          { 'IpProtocol': 'tcp',
            'FromPort': 3389,
            'ToPort': 3389,
            'IpRanges' : [{'CidrIp': '0.0.0.0/0'}]}
          ])
print("Ingress Rules Successfully set.")

#to see all the images available on AWS owned by amazon.
images = ec2_client.describe_images(
    Filters=[
        {
            'Name':'name',
            'Values': [
                'Windows_Server-2016-English-Full-*',
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

sleep(3)

userInput=int(input())

if 1 <= userInput <=100 :
   imageid=images['Images'][10]['ImageId']
   instance = resource.create_instances(
       ImageId=imageid,
       InstanceType = 't2.micro',
       KeyName="Windows-key",
       MaxCount=1,
       MinCount=1,
       NetworkInterfaces=[{
         'SubnetId':subnet_id,
         'DeviceIndex': 0,
         'AssociatePublicIpAddress': True,
         'Groups': [
           security_group.group_id
         ]
       }],
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
   print(instance)
   #print("Instance Successfully Launched.")  
   #sleep(120)
   #print("Instance PublicDNS: %s " % instance.public_dns_name)   
else:
   print("Luanch failed !!")



