import boto3
import session
from botocore.exceptions import ClientError
 

 ARN_ACCESS_KEY = " "
 ARN_SECRET_ACCESS_KEY = " "
 ##########################################
 #Define Access key and Secret Access Key ID
 ##########################################
 session = Session(aws_access_key = ARN_ACCESS_KEY,
                   aws_secret_access_key = ARN_SECRET_ACCESS_KEY,
                   region = "us-east-1" )

 ec2_client = session.client('ec2',region = "us-east-1")

 #########################################
 #Filter Production Volumes
 #########################################

 try:
     ec2_volumes = ec2_client.describe_volumes(Filters = [
         {
             "Name": "tag-key",
             "Values": ["Enviornment"]
         },
         {
             "Name": "tag-key",
             "Values": ["Prod"]
         }
     ])
#########################################     
#Get Volumes ID
#########################################
     for volume in ec2_volumes.get("Volumes",[]):
      volume_id = volume.get("VolumeId") 

#########################################     
#Create Snapshot of Volumes
#########################################

      try:
         snapshot = ec2_client.create_snapshot(VolumeId = volume_id,
                                               Descriptioin = "created using script")
         print(snapshot("SnapShotId"))
      except ClientError as e:
         print("Error in snapshot", e)   
 except ClientError as e:
    print("Error in volume", e)                                                  
      

