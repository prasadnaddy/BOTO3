import boto3,sys
from datetime import datetime

AWS_CONSOLE = boto3.session.Session(profile_name='root')        #Getting the custom session with root profile name
EC2_RESOURCE = AWS_CONSOLE.resource(service_name='ec2', region_name='us-east-1')    #resource object
EC2_CLIENT = AWS_CONSOLE.client(service_name='ec2', region_name='us-east-1')        #client object

def EC2OperationsUsingResource(EC2_resource):
    try: 
        IsStarted=False
        IsStopped=False
        IsTerminated=False
        print("Welcome to the MENU Driven approach to perform specific action on EC2 instance:")
        while True:
            print("1. Start the Instance")
            print("2. Stop the Instance")
            print("3. Terminate the Instance")
            print("4. Exit Script")
            option = int(input("Enter the option here : "))
            if option==1:
                InstanceID = input("Enter the Instance ID: ")
                if(InstanceID and not(IsStarted)):
                    print("Starting the EC2 Instance......")
                    InstanceObject = EC2_resource.Instance(InstanceID)
                    InstanceObject.start()
                    IsStarted=True
                    print("Now your Instance with ID: {} is UP and RUNNING...\n".format(InstanceID))
                elif(IsStarted):
                    print("Your Instance with ID : {} is already UP and RUNNING...\n".format(InstanceID))
                else:
                    print("Enter a valid Instance ID\n")
                    continue
            elif option==2:
                InstanceID = input("Enter the Instance ID: ")
                if(InstanceID and not(IsStopped)):
                    print("Stopping the EC2 Instance........")
                    InstanceObject = EC2_resource.Instance(InstanceID)
                    stopped = InstanceObject.stop()
                    IsStopped=True
                    print("Now your Instance with ID: {} is STOPPED...\n".format(InstanceID))
                elif(IsStopped):
                    print("Your Instance with ID : {} is already STOPPED...\n".format(InstanceID))
                else:
                    print("Enter a valid Instance ID\n")
                    continue 
            elif option==3:
                InstanceID = input("Enter the Instance ID: ")
                if(InstanceID and not(IsTerminated)):
                    print("Terminating the EC2 Instance.........")
                    InstanceObject = EC2_resource.Instance(InstanceID)
                    InstanceObject.terminate()
                    IsTerminated=True
                    print("Now your Instance with ID: {} is TERMINATED...\n".format(InstanceID))
                elif(IsTerminated):
                    print("Your Instance with ID : {} is already TERMINATED...\n".format(InstanceID))
                else:
                    print("Enter a valid Instance ID\n")
                    continue
            elif option==4:
                print("Thanks for using the script... EXITING...\n")
                sys.exit(0)
            else:
                print("Invalid option entry.. EXITING..")
                sys.exit(0)
    except Exception as e: print("Issue loading the Resource Object script {}".format(e))
    
def EC2OperationsUsingClient(EC2_client):
    try:
        IsStarted=[]
        IsStopped=[]
        IsTerminated=[]
        print("Welcome to the MENU Driven approach to perform specific action on EC2 instance:")
        while True:
            print("1. Start the Instance")
            print("2. Stop the Instance")
            print("3. Terminate the Instance")
            print("4. Exit Script")
            IDInput = input("Enter the Instance ID or IDs separated by commas first to begin :")
            if IDInput:
                InstanceIDS=IDInput.split(',')
                for InstanceID in InstanceIDS:
                    IsStarted.append(False)
                    IsStopped.append(False)
                    IsTerminated.append(False)
                option = int(input("Enter the option here : ")) 
                if option==1:
                    for InstanceID,iterator in zip(InstanceIDS,IsStarted):
                        print("Current Instance ID {}".format(InstanceID))
                        if(InstanceID and not(iterator)):
                            print("Starting the EC2 Instance......")
                            EC2_client.start_instances(InstanceIds=[InstanceID])
                            IsStarted[iterator]=True
                            print("Now your Instance with ID: {} is UP and RUNNING...\n".format(InstanceID))
                        elif(iterator):
                            print("Your Instance with ID : {} is already UP and RUNNING...\n".format(InstanceID))
                        else:
                            print("Enter a valid Instance ID\n")
                            continue
                elif option==2:
                    for InstanceID,iterator in zip(InstanceIDS,IsStopped):
                        print("Current Instance ID: {}".format(InstanceID))
                        if(InstanceID and not(iterator)):
                            print("Stopping the EC2 Instance........")
                            EC2_client.stop_instances(InstanceIds=[InstanceID])
                            IsStopped[iterator]=True
                            print("Now your Instance with ID: {} is STOPPED...\n".format(InstanceID))
                        elif(iterator):
                            print("Your Instance with ID : {} is already STOPPED...\n".format(InstanceID))
                        else:
                            print("Enter a valid Instance ID\n")
                            continue 
                elif option==3:
                    for InstanceID,iterator in zip(InstanceIDS,IsTerminated):
                        print("Current Instance ID: {}".format(InstanceID))
                        if(InstanceID and not(iterator)):
                            print("Terminating the EC2 Instance........")
                            EC2_client.terminate_instances(InstanceIds=[InstanceID])
                            IsTerminated[iterator]=True
                            print("Now your Instance with ID: {} is TERMINATED...\n".format(InstanceID))
                        elif(iterator):
                            print("Your Instance with ID : {} is already TERMINATED...\n".format(InstanceID))
                        else:
                            print("Enter a valid Instance ID\n")
                            continue 
                elif option==4:
                    print("Thanks for using the script... EXITING...\n")
                    break
                else:
                    print("Invalid option entry.. EXITING..")
                    break
            else:
                print("Enter the valid Instance ID to begin the program..\n")
                continue
    except Exception as e: print("Issue loading the Client object script {}".format(e))

def main():
    try:
        start = datetime.now()
        EC2OperationsUsingResource(EC2_RESOURCE)
        EC2OperationsUsingClient(EC2_CLIENT)
        end = datetime.now()
        timeDiff=end-start                      #DatetimeObject that holds the time difference
        timeDiffInSeconds=timeDiff.total_seconds()      #Difference in Seconds
        timeDiffInMinutes=divmod(timeDiffInSeconds, 60)[0]      #Difference in minutes
        print("Start Time : {}".format(start))
        print("End Time : {}".format(end))   
        print("Time Taken to finish  : {} mins".format(str(int(float(timeDiffInMinutes)))))
    except Exception as e: print("Issue running the main function {}".format(e))
    
if __name__=='__main__':
    main()
    
