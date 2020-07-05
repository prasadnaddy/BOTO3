import boto3        #Importing BOTO3 module
from datetime import datetime

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name="root")   #Accessing AWS Console with root credentials

def ListIAMUsers():
    try:
        IAM_CONSOLE_AWS = AWS_MGMT_CONSOLE.resource('iam')  #Opening the IAM service
        for each_user in IAM_CONSOLE_AWS.users.all():       #Getting all the users from IAM
            print(each_user.name)                           #Printing the users names
    except Exception as e: print("Error listing users from IAM")   

def ListS3Buckets():
    try:
        S3_CONSOLE_AWS = AWS_MGMT_CONSOLE.resource('s3')        #Opening the S3 Service
        for each_bucket in S3_CONSOLE_AWS.buckets.all():        #Getting all the S3 buckets from S3
            print(each_bucket.name)                                #Printing each buckets
        
    except Exception as e: print("Error listing the S3 Buckets")
    
def ListIAMUsersWithClient():
    try:
        IAM_CONSOLE_AWS = AWS_MGMT_CONSOLE.client('iam')  #Opening the IAM service
        for each_user in IAM_CONSOLE_AWS.list_users()['Users']:       #Getting all the users from IAM
            print(each_user['UserName'])                           #Printing the users names
    except Exception as e: print("Error listing users from IAM")
    
def ListIAMUsersWithoutDefaultSession():
    try:
        IAM_CONSOLE_AWS = boto3.resource('iam')  #Opening the IAM service with default session
        for each_user in IAM_CONSOLE_AWS.users.all():       #Getting all the users from IAM
            print(each_user.name)                           #Printing the users names
    except Exception as e: print("Error listing users from IAM")
    
def AWSServicesUsingClientObject():
    try:
        IAM_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='iam', region_name='us-east-1')  #Opening the IAM service with custom session
        IAMResponse = IAM_CONSOLE_AWS.list_users()      #Iterating over Response Dictionary
        for each_user in IAMResponse['Users']:
            print("UserName : "+each_user['UserName'])      #Printing every user in IAM
            
        EC2_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='ec2', region_name='us-east-1')
        EC2Response = EC2_CONSOLE_AWS.describe_instances()  #response json for ec2 instances description
        for sub_list in EC2Response['Reservations']:           #Iterating over reservations
            for each_instance in sub_list['Instances']:         #iterating over instances
                print("Instance ID: "+each_instance['InstanceId'])      #We get all the instance IDs here
                
        S3_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='s3', region_name='us-east-1')
        S3Response = S3_CONSOLE_AWS.list_buckets()      #Response Dictionary
        for each_bucket in S3Response['Buckets']:       #Iterating over key "Buckets"
            print("Bucket Name : "+each_bucket['Name'])     #printing every buckets from s3 
            
    except Exception as e: print("Error working on AWS Services using Client object")
    
def AWSServicesUsingResourceObject():
    try:
        IAM_CONSOLE_AWS = AWS_MGMT_CONSOLE.resource(service_name='iam', region_name='us-east-1')  #Opening the IAM service with custom session
        print("The IAM Users present in the console are :")
        for each_user in IAM_CONSOLE_AWS.users.all():
            print(each_user.name)
        
        print("Applying limit on results:")
        for each_user in IAM_CONSOLE_AWS.users.limit(1):
            print(each_user.name)
         
        EC2_CONSOLE_AWS = AWS_MGMT_CONSOLE.resource(service_name='ec2', region_name='us-east-1')
        print("Fetching all the EC2 instances ID from the console")
        for each_instance in EC2_CONSOLE_AWS.instances.all():           
            print(each_instance.id)
                
        S3_CONSOLE_AWS = AWS_MGMT_CONSOLE.resource(service_name='s3', region_name='us-east-1')
        for each_bucket in S3_CONSOLE_AWS.buckets.all():       
            print("Bucket Name : "+each_bucket.name)     #printing every buckets from s3 
            
    except Exception as e: print("Error working on AWS Services using Client object")
    
def GetAccountIDUsingSTSClientObject():
    try:
        STS_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='sts', region_name='us-east-1')  #Opening the STS service with custom session
        stsResponse = STS_CONSOLE_AWS.get_caller_identity()
        print("Account ID is : "+stsResponse['Account'])
        print("User name inside the ARN is : "+stsResponse['Arn'])
            
    except Exception as e: print("Error getting the Account ID Using STS using Client object {}".format(e))
    
def WorkingOnEC2ServicesUsingClientObject():
    try:
        EC2_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='ec2', region_name='us-east-1')  #Opening the ec2 service with custom session
        EC2Response = EC2_CONSOLE_AWS.describe_instances()  #response json for ec2 instances description
        for sub_list in EC2Response['Reservations']:           #Iterating over reservations
            for each_instance in sub_list['Instances']:         #iterating over instances
                print("=================")                      #Instance separator
                print("Instance ID: {}\nInstance Image ID: {}\nInstance Launch Time: {}\nInstance State is: {}".format(each_instance['InstanceId'],each_instance['ImageId'],each_instance['LaunchTime'].strftime("%Y-%m-%d"),each_instance['State']['Name']))      #We get all the instance details here
            
        EC2VolumesResponse = EC2_CONSOLE_AWS.describe_volumes()
        for sub_list in EC2VolumesResponse['Volumes']:
            print("=================")                      #Volumes Separator
            print("The Volume ID is: {}\nAvailability Zone: {}\nVolume Type: {}".format(sub_list['VolumeId'],sub_list['AvailabilityZone'],sub_list['VolumeType']))

        EC2SecurityGroupsResponse = EC2_CONSOLE_AWS.describe_security_groups()    #Function to get the security groups
        print("The Security groups present are:")   
        for sub_list in EC2SecurityGroupsResponse['SecurityGroups']:    #Iterating over SecurityGroups Key
            print("{}".format(sub_list['GroupName']))                  #Group names are present in 'GroupName'
    except Exception as e: print("Error getting required lists of EC2 using Client object {}".format(e))

def MetaObjectExample():
    try:
        EC2_CONSOLE_RESOURCE = AWS_MGMT_CONSOLE.resource(service_name='ec2')
        for each_region in EC2_CONSOLE_RESOURCE.meta.client.describe_regions()['Regions']:  #Iterating over Regions Key
            print("{}".format(each_region['RegionName']))       #We get Regions under 'RegionName' key
    except Exception as e: print("Error Performing the Meta operation : {}".format(e))
    
def ResourceCollectionsExample():
    try:
        EC2_CONSOLE_RESOURCE = AWS_MGMT_CONSOLE.resource(service_name='ec2')
        for each_instance in EC2_CONSOLE_RESOURCE.instances.all():      #All Property for getting all instances
            print(each_instance.id)         #Printing the ID of the instances
            
        for each_limitted_instances in EC2_CONSOLE_RESOURCE.instances.limit(10):    #Limiting to specified number
            print(each_limitted_instances.id)       #Displaying only top 10 instance ID
        
        InstanceStateFilter={'Name':'instance-state-name','Values':['running','stopped']}     #Filter to get only running and stopped instances
        InstanceTypeFilter={'Name':'instance-type','Values':['t2.micro']} #Filter to fetch only t2.micro Instances
        for each_filtered_instances in EC2_CONSOLE_RESOURCE.instances.filter(Filters=[InstanceStateFilter,InstanceTypeFilter]):   #Passing List of filters
            print(each_filtered_instances.id)       #Instance ID Filtered with only running and stopped status along with t2.micro type
    except Exception as e: print("Issue working on collections : {}".format(e))

def CollectionsConceptForEC2():
    try:
        EC2_CONSOLE_RESOURCE = AWS_MGMT_CONSOLE.resource(service_name='ec2',region_name='us-east-1')    #resource object
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        
        AllInstanceIDS=[]       #List to store all the instance ID
        
        for each_id in EC2_CONSOLE_RESOURCE.instances.all():        #Collecting all instance ID
            AllInstanceIDS.append(each_id.id)               #appending to list
            
        waiter = EC2_CONSOLE_CLIENT.get_waiter('instance_running')      #Waiter object for running instances
        
        print("Starting all the instances....")
        EC2_CONSOLE_RESOURCE.instances.start()          #Starting the instances
        waiter.wait(InstanceIds=AllInstanceIDS)     #Wait for all instances to move from pending to running state
        print("All instances are moved to running state...")

    except Exception as e: print("Issue occured while performing operations on EC2 : {}".format(e))
    
def FilterBasedOnTagNames():
    try:
        EC2_CONSOLE_RESOURCE = AWS_MGMT_CONSOLE.resource(service_name='ec2',region_name='us-east-1')    #resource object
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        
        ResourceTagID=[]    #List to store the filtered instance ID
        ClientTagID=[]      #List of client object filtered Instances ID
        
        TagFilter = {'Name':'tag:Name','Values':['NON_PROD']}       #filtering non_prod servers
        
        for each_id in EC2_CONSOLE_RESOURCE.instances.filter(Filters=[TagFilter]):  #Iterating over the filter
            ResourceTagID.append(each_id.id)        #appending the ID to TagID List
            
        for each_item in EC2_CONSOLE_CLIENT.describe_instances(Filters=[TagFilter])['Reservations']:    #Iterate over Reservations
            for each_instances in each_item['Instances']:       #Iterating over Instances Key
                ClientTagID.append(each_instances['InstanceId'])       #InstanceID key has the instances ID
        
    except Exception as e: print("Unable to filter the instances based on tagnames : {}".format(e))

def StartInstancesBasedOnIDWithWaiter():
    try:
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        ClientTagID=[]      #List of client object filtered Instances ID
        
        TagFilter = {'Name':'tag:Name','Values':['NON_PROD']}       #filtering non_prod servers
        
        for each_item in EC2_CONSOLE_CLIENT.describe_instances(Filters=[TagFilter])['Reservations']:    #Iterate over Reservations
            for each_instances in each_item['Instances']:       #Iterating over Instances Key
                ClientTagID.append(each_instances['InstanceId'])       #InstanceID key has the instances ID
                
        print("Starting the Non-prod instances:....")
        EC2_CONSOLE_CLIENT.start_instances(InstanceIds=ClientTagID)     #based on the tag IDs
        waiter = EC2_CONSOLE_CLIENT.get_waiter('instance_running')      #Waiter object for client
        waiter.wait(InstanceIds=ClientTagID)                        #Wait until the instances are moved to running state
        
        print("Your Non prod instances are now up and running...")
        
    except Exception as e: print("Unable to start instances : {}".format(e))

def CleanUpVolumesByResourceObject():
    try:
        EC2_CONSOLE_RESOURCE = AWS_MGMT_CONSOLE.resource(service_name='ec2',region_name='us-east-1')    #resource object
        StateFilter={'Name':'status','Values':['available']}
        for eachVolume in EC2_CONSOLE_RESOURCE.volumes.filter(Filters=[StateFilter]):   #To get all the volumes
            if not eachVolume.tags:     #To get only the volumes without tags
                print("Unused and Untagged Volumes are : ")
                print("Volume ID : {}\tVolume State: {}\tVolume Tag: {}".format(eachVolume.id,eachVolume.state,eachVolume.tags))
                print("Deleting the unused and untagged volumes:")
                eachVolume.delete()     #This function is used to delete the volumes
    except Exception as e: print("Issue cleaning up the volumes: {}".format(e))
    
def CleanUpVolumesByClientObject():
    try:
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        print("Deleting the Unused and untagged volumes..")
        for eachVolume in EC2_CONSOLE_CLIENT.describe_volumes()['Volumes']: #Iterating over the Volumes Key
            if not 'Tags' in eachVolume and eachVolume['State']=='available':  #If there is no Key named Tags, then we will be printing the volumes
                print("{} is deleted".format(eachVolume['VolumeId']))
                EC2_CONSOLE_CLIENT.delete_volume(VolumeId=eachVolume['VolumeId'])
            else:
                print("There are no untagged and unused volumes")
    except Exception as e: print("Issue cleaning up the volumes: {}".format(e))

def ListSnapshotsByResourceObject():
    try:
        EC2_CONSOLE_RESOURCE = AWS_MGMT_CONSOLE.resource(service_name='ec2',region_name='us-east-1')    #resource object
        STS_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='sts', region_name='us-east-1')  #Opening the STS service with custom session
        stsResponse = STS_CONSOLE_AWS.get_caller_identity()
        OwnerID = stsResponse['Account']        #Getting our Account ID
        for snap in EC2_CONSOLE_RESOURCE.snapshots.filter(OwnerIds=[OwnerID]):  #Getting snaps based on AccountID
            print(snap.id)     #printing all the snaps
    except Exception as e: print("Issue listing the snapshots: {}".format(e))

def ListSnapshotsByClientObject():
    try:
        OwnerIDList=[]
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        STS_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='sts', region_name='us-east-1')  #Opening the STS service with custom session
        stsResponse = STS_CONSOLE_AWS.get_caller_identity()
        OwnerIDList.append(stsResponse['Account'])       #Getting our Account ID
        for snap in EC2_CONSOLE_CLIENT.describe_snapshots(OwnerIds=OwnerIDList)['Snapshots']:   #based on our AccountID
            print(snap['SnapshotId'])       #Printing the SnapID
    except Exception as e: print("Issue listing the snapshots: {}".format(e))
    
def ListSnapshotsBasedOnSizeUsingClientObject():
    try:
        OwnerIDList=[]
        SizeFilterList=[]
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        STS_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='sts', region_name='us-east-1')  #Opening the STS service with custom session
        stsResponse = STS_CONSOLE_AWS.get_caller_identity()
        OwnerIDList.append(stsResponse['Account'])       #Getting our Account ID
        SizeFilter={'Name':'volume-size','Values':['8']}           #Specifying size in GB
        SizeFilterList.append(SizeFilter)   #We need to pass filters as list, so appending filter to a list
        for snap in EC2_CONSOLE_CLIENT.describe_snapshots(OwnerIds=OwnerIDList,Filters=SizeFilterList)['Snapshots']:   #based on our AccountID
            print(snap['SnapshotId'])       #Printing the SnapID
    except Exception as e: print("Issue listing the snapshots: {}".format(e))
    
def ListSnapshotsBasedOnStartTimeUsingClientObject():
    try:
        OwnerIDList=[]
        EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object
        STS_CONSOLE_AWS = AWS_MGMT_CONSOLE.client(service_name='sts', region_name='us-east-1')  #Opening the STS service with custom session
        stsResponse = STS_CONSOLE_AWS.get_caller_identity()
        OwnerIDList.append(stsResponse['Account'])       #Getting our Account ID
        today = datetime.now()
        StartTime = str(datetime(today.year,today.month,today.day,10,10,21)) #Time matching condition
        
        for snap in EC2_CONSOLE_CLIENT.describe_snapshots(OwnerIds=OwnerIDList)['Snapshots']:   #based on our AccountID
            if snap['StartTime'].strftime("%Y-%m-%d %H:%M:%S")==StartTime:  #Check if snap time matches condition
                print(snap['SnapshotId'],snap['StartTime'].strftime("%Y-%m-%d %H:%M:%S"))       #Printing the SnapID, SnapTime after parsing datetime
            else:   #Otherwise
                print("No snapshots created for the time : {}".format(StartTime))
    except Exception as e: print("Issue listing the snapshots: {}".format(e))
    
def GetUserDetailsFromIAM():
    try:
        IAM_CLIENT = AWS_MGMT_CONSOLE.client(service_name='iam')    #client object, as IAM is global so no region
        clientObject = IAM_CLIENT.get_user(UserName='Practise')['User']    #getting details of 'Practise' user
        print(clientObject['UserName'],clientObject['UserId'],clientObject['Arn'],clientObject['CreateDate'].strftime("%Y-%m-%d"))
    except Exception as e: print("Issue listing the user's details : {}".format(e))
    
def GetAllUsersDetailsFromIAM():
    try:
        IAM_CLIENT = AWS_MGMT_CONSOLE.client(service_name='iam')    #client object, as IAM is global so no region
        for eachUser in IAM_CLIENT.list_users()['Users']:    #getting details of all users in IAM
            print(eachUser['UserName'],eachUser['UserId'],eachUser['Arn'],eachUser['CreateDate'].strftime("%Y-%m-%d"))
    except Exception as e: print("Issue listing the user's details : {}".format(e))
    
def GetGroupInformationFromIAM():
    try:
        IAM_CLIENT = AWS_MGMT_CONSOLE.client(service_name='iam')    #client object, as IAM is global so no region
        for eachGroup in IAM_CLIENT.list_groups()['Groups']:
            print(eachGroup['Arn'],eachGroup['GroupId'],eachGroup['GroupName'],eachGroup['CreateDate'].strftime("%Y-%m-%d"))
    except Exception as e: print("Issue listing the group details : {}".format(e))
    
GetGroupInformationFromIAM()
