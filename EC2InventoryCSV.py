import boto3
import pandas
from datetime import datetime

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name="root")   #Accessing AWS Console with root credentials
EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object

df = pandas.DataFrame()     #Empty DataFrame
Collection={}           #Empty Collection Dictionary

def GetInstancesCount():
    try:
        InstancesCount=[]
        for InstReserv in EC2_CONSOLE_CLIENT.describe_instances()['Reservations']:
            for Instances in InstReserv['Instances']:
                InstancesCount.append(Instances['InstanceId'])     #Storing All the instances ID and it helps to find the count of instances
        return InstancesCount
    except Exception as e: print("Issue appending the instances count List: {}".format(e))
    
def GetInstancesTags():
    try:    
        InstanceNames = [Tags['Value'] for InstReserv in EC2_CONSOLE_CLIENT.describe_instances()['Reservations'] for Instances in InstReserv['Instances'] for Tags in Instances['Tags']]
        return InstanceNames
    except Exception as e: print("Issue getting the Instance Tags: {}".format(e))
    
def CreateDataFrame(InstancesCount,InstanceNames,EmptyDF):
    try:
        for Serial, InstanceResrv, Tags, Volumes, KeyPair in zip(range(1,len(InstancesCount)+1),EC2_CONSOLE_CLIENT.describe_instances()['Reservations'],InstanceNames,EC2_CONSOLE_CLIENT.describe_volumes()['Volumes'],EC2_CONSOLE_CLIENT.describe_key_pairs()['KeyPairs']):
            Collection['SerialNumber']=Serial
            Collection['InstanceName']=Tags
            for Instances in InstanceResrv['Instances']:    #Iterating one more time to get Instance Info
                Collection['InstanceID']=Instances['InstanceId']
                Collection['InstanceType']=Instances['InstanceType']
                Collection['Architecture']=Instances['Architecture']
                Collection['LaunchTime']=Instances['LaunchTime'].strftime("%Y-%m-%d")
                Collection['PrivateIPAddress']=Instances['PrivateIpAddress']
            Collection['VolumeID'] = Volumes['VolumeId']    #With just single iteration we will be getting the Volumes
            Collection['VolumeType'] = Volumes['VolumeType']
            Collection['VolumeState'] = Volumes['State']
            Collection['KeyPairName'] = KeyPair['KeyName']  #Single iterations is enough for KeyPairs
            df1 = pandas.DataFrame([Collection], columns=Collection.keys()) #Creating Df with dictionary
            EmptyDF =  pandas.concat([EmptyDF,df1])     #Appending the Dataframe to Original DataFrame
        return EmptyDF
    except Exception as e: print("Issue creating the dataframe: {}".format(e))

def WriteToCsv(DataFrame):
    try:
        DataFrame.to_csv("EC2Inventory.csv",index=False)
    except Exception as e: print("Issue writing to CSV: {}".format(e))
    
def StartScript():
    try:
        StartTime = datetime.now()
        print("Getting Instances Count..")
        InstancesCount = GetInstancesCount()
        print("Getting the Instance Tagnames...")
        InstancesNames = GetInstancesTags()
        print("Creating the DataFrame from the Information from Console...")
        FinalDataFrame = CreateDataFrame(InstancesCount,InstancesNames,df)
        print("Writing to CSV...")
        WriteToCsv(FinalDataFrame)
        print("Finished writing to CSV...")
        EndTime = datetime.now()
        TimeDiff = EndTime - StartTime
        print("Time taken to finish the script : {}".format(TimeDiff))
    except Exception as e: print("Issue executing the main script: {}".format(e))
    
if __name__=='__main__':
    StartScript()
    
    