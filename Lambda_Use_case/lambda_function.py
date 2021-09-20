import boto3
import json
LAMBDA_ACCESS_POLICY_ARN="arn:aws:iam::897336489748:policy/LambdaS3AccessPolicy"
LAMBDA_ROLE = "Lambda_Execution_Role"
LAMBDA_ROLE_ARN = "arn:aws:iam::897336489748:role/Lambda_Execution_Role"

def lambda_client():
    aws_lambda = boto3.client('lambda', region='us-east-1')
    """ :type : pyboto3.lambda """ # used to utilized autocomplete function of boto3 for each services
    return aws_lambda

#Need IAM roles to access other Services
#Create IAM Policy

def iam_client():
    aws_iam = boto3.client('iam') # its global service
    """ :type : pyboto3.iam """
    return aws_iam

def create_access_policy_for_lambda():
    s3_access_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:*",
                    "logs: CreateLoggroup",
                    "logs: CreateLogStream",
                    "logs: PutLogEvents"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }
    return iam_client().create_policy(
        PolicyName='LambdaS3AccessPolicy',
        PolicyDocument=json.dumps(s3_access_policy_document),
        Description="Allows lambda to access S3 resoiurces"
    )

# Creating execution Role for Lambda to run/execute functions in Lambda
 def create_execution_role_for_lambda():
     lambda_execution_role={
         "Version": "2012-1-07",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Principal": {
                     "Service": "lambda.amazonaws.com"
                 },
                 "Action": "sts:AssumeRole"
             }
         ]
     }
     return iam_client().create_role(
      RoleName=LAMBDA_ROLE,
      AssumeRolePolicyDocument=json.dumps(lambda_execution_role),
      Description = "Permissions to execute lambda functions."
     )
#Attached Policy to role
def attach_access_policy_to_execution_role():
    return iam_client().attach_role_policy(
        RoleName=LAMBDA_ROLE,
        PolicyArn=LAMBDA_ACCESS_POLICY_ARN
    )

if __name__ == '__main__':
    print(attach_access_policy_to_execution_role())





