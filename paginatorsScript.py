import boto3        #module for working with boto3

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name='root')   #configuring with root profile
IAM_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='iam') #running on IAM with client object
EC2_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1') #ec2 client object

paginatorObject = IAM_CLIENT_OBJECT.get_paginator('list_users') #paginator object on list_users function

#Function to get the count of users from pages
def getUsersCountInPages():
    try:
        for eachPage in paginatorObject.paginate():     #iterating over the paginator object to get the pages
            print(len(eachPage['Users']))       #getting count of users on each page
    except Exception as e: print("Issue fetching the users count from PAGES: {}".format(e))       

#function to get the usernames from the pages
def getUserNamesInPages():
    try:
        for eachPage in paginatorObject.paginate(): #iterating over the paginator object to get pages
            for eachUser in eachPage['Users']:      #iterating over the key 'Users' to get each user info
                print(eachUser['UserName'])         #printing the username of each user one by one
    except Exception as e: print("Issue getting the usernames : {}".format(e))
    
#function to list all the instances id from the pages
def listInstancesFromPages():
    try:
        EC2PaginatorObject = EC2_CLIENT_OBJECT.get_paginator('describe_instances')  #ec2 paginator object
        for eachPage in EC2PaginatorObject.paginate():  #iterating over the paginator object to get pages
            for eachInstances in eachPage['Reservations']:  #iterating over the key 'Reservations'
                for eachInstance in eachInstances['Instances']: #iterating over the key 'instances'
                    print(eachInstance['InstanceId'])       #printing all the instance id from console
    except Exception as e: print("Issue listing the instance id : {}".format(e))
    
