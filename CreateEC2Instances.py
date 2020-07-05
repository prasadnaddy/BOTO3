import logging
import sys
import boto3

#Class to Format the log file as colours based on the Level of logging
class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"            #Assigning the Color codes for each colours
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,               #Assigning the Colours to each Logging Levels
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)                 #Returning the log Formatter
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)                  #Lowest level of logging will be set to DEBUG Mode

# create console handler with a higher log level
ch = logging.FileHandler('./logs/OutputLog.log')        #Filehandler will contain the path to log file
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())                  #Calling the CustomFormatter Class to get colour codes
logger.addHandler(ch)

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name="root")   #Accessing AWS Console with root credentials

EC2_CONSOLE_CLIENT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1')    #client object

def clearLog():
    with open("./logs/OutputLog.log","w") as file:  #Opening a file in write mode and closing it will clear contents
        file.close()

def createInstances(Ec2Client):
    try:
        response = Ec2Client.run_instances(     #Run_Instances is used to launch an instance
        BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {

                        'DeleteOnTermination': True,
                        'VolumeSize': 8,                    #Size in GB
                        'VolumeType': 'gp2'                 #type of volume
                    },
                },
            ],
            ImageId='ami-09d95fab7fff3776c',            #First Linux Image
            InstanceType='t2.micro',                    #Instance type
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': False                    #For Cloud-watch
            },
            SecurityGroupIds=[
                'secure-group',                     #Security group name
            ],
        )   
        for res in response['Instances']:       #Iterating over Instances Key to get ID
            print("Instance created with ID: {}".format(res['InstanceId']))
        logger.info("Ec2 instance created with ID : {}".format(res['InstanceId']))
    except Exception as e: 
        print("Issue creating the Instances : {}".format(e))
        logger.error("Issue creating the Instances : {}".format(e))
        
def startScript():
    try:
        clearLog()
        createInstances(EC2_CONSOLE_CLIENT)
    except Exception as e: logger.error("Issue creating the Instances : {}".format(e))

if __name__=='__main__':
    startScript()

  


