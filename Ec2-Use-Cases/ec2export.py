#Using this script we can create a report of all EC2
#running om AWS so, we can analyze it and make decision about our cost optimization

import boto3
import csv
def Get_Instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instaces()
    return response['Reservations']['Instances']

def CSV_Writer(header, content):
    with open('export.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=header)
        writer.writerheader()
        for row in content:
            writer.writer(row)

if __name__=="__main__":
    instances = Get_Instances()
    header = ['InstanceId', 'InstanceType', 'State', 'PublicIpAddress']
    data = []
    for instance in instances:
        print(f"Adding Isntance {Instance['InstanceId']} to file")
        data.append(
            {
                "InstanceId": instance['InstanceId'],
                "InstanceType": instance['InstanceType'],
                "State":instance['State']['Name'],
                "PublicIpAddress": instance['PublicIpAddress']

            }
        )            
    CSV_Writer(content=data, header=header)