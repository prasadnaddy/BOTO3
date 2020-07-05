import json
import boto3

def lambda_handler(event, context):
    masterNode = "i-0c3161e49064246a9"
    slaveNode = "i-07b9bf30e368d6cab"
    secondaryIP = "172.31.89.168"
    
    ec2Object = boto3.resource('ec2','us-east-1')   #Resource object
    masterServer = ec2Object.Instance(masterNode)   #Master instance object
    
    if masterServer.state['Name']=="running":   #check if master is down
        print("Master server is up and running..")
        
    else:
        slaveServer = ec2Object.Instance(slaveNode) #slave server object
        masterNetInterface = masterServer.network_interfaces_attribute[0]
        slaveNetInterface = slaveServer.network_interfaces_attribute[0]
        masterNetIntID = masterNetInterface['NetworkInterfaceId']
        slaveNetIntID = slaveNetInterface['NetworkInterfaceId']
        ec2ClientObject = boto3.client('ec2','us-east-1')   #client object
        ec2ClientObject.unassign_private_ip_addresses(
            NetworkInterfaceId=masterNetIntID,   #master network interface ID
            PrivateIpAddresses = [secondaryIP]  #Secondary IP of master
            )
        ec2ClientObject.assign_private_ip_addresses(
            AllowReassignment = True,
            NetworkInterfaceId = slaveNetIntID,  #slave network interface ID
            PrivateIpAddresses = [secondaryIP]  #secondary IP of master to slave
            )
    return {
        'statusCode': 200,
        'body': json.dumps('Program executed successfully!')
    }
