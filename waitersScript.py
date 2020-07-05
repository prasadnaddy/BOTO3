import boto3
import time

#Accessing AWS Console using the Root profile
AWS_CONSOLE = boto3.session.Session(profile_name='root')

def waiterFunctionUsingWhileLoop():
    try:
        #We are taking both EC2 Resource and Client objects here
        EC2_RESOURCE = AWS_CONSOLE.resource(service_name='ec2',region_name='us-east-1')
        EC2_CLIENT = AWS_CONSOLE.client(service_name='ec2',region_name='us-east-1')

        INSTANCE_OBJECT = EC2_RESOURCE.Instance('i-0c3161e49064246a9')      #Working on BOTO3 instance by its ID

        print("Starting the Instance....")
        INSTANCE_OBJECT.start()     #Function to start the instance
        while True:     #Simple Waiter loop
            INSTANCE_OBJECT = EC2_RESOURCE.Instance('i-0c3161e49064246a9')          #Working on BOTO3 instance by ID
            print("Current Instance State: {}".format(INSTANCE_OBJECT.state['Name']))       #Fetching current state
            if INSTANCE_OBJECT.state['Name']=='running':        #If state=running, exit the loop
                break
            else:                   #Else, wait for the status to be changed back to running state
                print("Waiting for the status to be changed to Running state..")
                time.sleep(5)       #Wait for next 5 seconds
        print("Instance is up and running...")          #Now instance is started..
    except Exception as e: print("Issue starting the instance : {}".format(e))
    
def waiterFunctionUsingResourceWaiters():
    try:
        #We are taking only EC2 Resource objects here
        EC2_RESOURCE = AWS_CONSOLE.resource(service_name='ec2',region_name='us-east-1')
        INSTANCE_OBJECT = EC2_RESOURCE.Instance('i-0c3161e49064246a9')      #Working on BOTO3 instance by its ID
        print("Starting the Instance....")
        INSTANCE_OBJECT.start()     #Function to start the instance
        INSTANCE_OBJECT.wait_until_running()       #predefined function to wait until state changes to running state
        print("Instance is up and running...")          #Now instance is started..
    except Exception as e: print("Issue starting the instance : {}".format(e))

def waiterFunctionUsingClientWaiters():
    try:
        #We are taking only EC2 Resource objects here
        EC2_CLIENT = AWS_CONSOLE.client(service_name='ec2',region_name='us-east-1') #Client Object
        print("Starting the Instance....")
        EC2_CLIENT.start_instances(InstanceIds=['i-0c3161e49064246a9'])     #Starting EC2 instance using ID
        waiter = EC2_CLIENT.get_waiter('instance_running')          #Creating the waiter to wait for running status
        waiter.wait(InstanceIds=['i-0c3161e49064246a9'])        #Waiter object with instance ID
        print("Instance is up and running...")          #Now instance is started..
    except Exception as e: print("Issue starting the instance : {}".format(e))

def waiterFunctionUsingResourceObject_ClientWaiter():
    try:
        #We are taking only EC2 Resource objects here
        EC2_RESOURCE = AWS_CONSOLE.resource(service_name='ec2',region_name='us-east-1') #Resource Object
        EC2_CLIENT = AWS_CONSOLE.client(service_name='ec2',region_name='us-east-1') #Client Object
        print("Starting the Instance....")
        INSTANCE_OBJECT = EC2_RESOURCE.Instance('i-0c3161e49064246a9')
        INSTANCE_OBJECT.start()     #Starting EC2 instance using ID
        waiter = EC2_CLIENT.get_waiter('instance_running')          #Creating the waiter to wait for running status
        waiter.wait(InstanceIds=['i-0c3161e49064246a9'])        #Waiter object with instance ID
        print("Instance is up and running...")          #Now instance is started..
    except Exception as e: print("Issue starting the instance : {}".format(e))
    
