import boto3    #importing the boto3 module
from random import choice           #Importing the choice class from random module
import pandas as pd         #importing pandas module to add the details as dataframe to csv
from datetime import datetime   #datetime for capturing starting and ending time
import sys              #For performing systematic operations

##Random password Generation Configuration##
LENGTH_OF_PASSWORD = 10       #setting the length of the password
VALID_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?'   #allowed chars

##BOTO3 Configurations##
SESSION_OBJECT = boto3.session.Session(profile_name='root')  #Creating session object with root profile
IAM_CLIENT_OBJECT = SESSION_OBJECT.client(service_name='iam')    #creating client object for IAM service
IAM_USER_NAME = 'SuperUser'       #name of the user we are creating in IAM
POLICY_ARN = 'arn:aws:iam::aws:policy/AdministratorAccess'      #admin access ARN from IAM 

#Function to create the user using the client object, username and policy as arguments#
def createIAMUserWithConsoleAccess(clientObject, userName, password, policy):
    try:
        dataFrame = {}      #Empty Dictionary
        clientObject.create_user(UserName = userName)   #creating the user with specified username using create_user()
        #Now we will be creating the login profile with username, password and setting passwordReset to False
        clientObject.create_login_profile(UserName = userName, Password = password, PasswordResetRequired = True)
        clientObject.attach_user_policy(UserName = userName, PolicyArn = policy)    #attaching role to the user
        dataFrame['UserName'] = userName
        dataFrame['Password'] = password
        dataFrame['Policy-ARN'] = policy        #Adding the details to the dataframe
        df1 = pd.DataFrame([dataFrame], columns=dataFrame.keys()) #Creating Df with dictionary
        df1.to_csv('./usersDetails.csv',index=False)    #Writing to CSV
        print("User Name with {} has been created and details are added to CSV.. ".format(userName))
    except Exception as e: 
        if e.response['Error']['Code']=='EntityAlreadyExists':      #handling exception from botocore exceptions
            print("User with {} already exists.. Exiting the code".format(userName))
            sys.exit(0)     #exiting code if user already exists
        else:
            print("Issue creating the IAM User : {}".format(e))
            sys.exit(0)
            
#Function to create the user with programmatic access keys with client object, username and policy as arguments#
def createIAMUserWithProgrammaticAccess(clientObject, userName, password, policy):
    try:
        dataFrame = {}      #Empty Dictionary
        clientObject.create_user(UserName = userName)   #creating the user with specified username using create_user()
        #Now we will be creating the login profile with username, password and setting passwordReset to False
        response = clientObject.create_access_key(UserName = userName) #creating access keys and we get response
        dataFrame['Access-Key-ID'] = response['AccessKey']['AccessKeyId']
        dataFrame['Secret-Access-Key'] = response['AccessKey']['SecretAccessKey']
        clientObject.attach_user_policy(UserName = userName, PolicyArn = policy)    #attaching role to the user
        dataFrame['UserName'] = userName
        dataFrame['Password'] = password
        dataFrame['Policy-ARN'] = policy        #Adding the details to the dataframe
        df1 = pd.DataFrame([dataFrame], columns=dataFrame.keys()) #Creating Df with dictionary
        df1.to_csv('./usersDetails.csv',index=False)    #Writing to CSV
        print("User Name with {} has been created and details are added to CSV.. ".format(userName))
    except Exception as e: 
        if e.response['Error']['Code']=='EntityAlreadyExists':      #handling exception from botocore exceptions
            print("User with {} already exists.. Exiting the code".format(userName))
            sys.exit(0)     #exiting code if user already exists
        else:
            print("Issue creating the IAM User : {}".format(e))
            sys.exit(0)
            
def createIAMUserWithConsoleAndProgrammaticAccess(clientObject, userName, password, policy):
    try:
        dataFrame = {}      #Empty Dictionary
        clientObject.create_user(UserName = userName)   #creating the user with specified username using create_user()
        #Now we will be creating the login profile with username, password and setting passwordReset to True
        clientObject.create_login_profile(UserName = userName, Password = password, PasswordResetRequired = True)
        response = clientObject.create_access_key(UserName = userName) #creating access keys and we get response
        dataFrame['Access-Key-ID'] = response['AccessKey']['AccessKeyId']
        dataFrame['Secret-Access-Key'] = response['AccessKey']['SecretAccessKey']
        clientObject.attach_user_policy(UserName = userName, PolicyArn = policy)    #attaching role to the user
        dataFrame['UserName'] = userName
        dataFrame['Password'] = password
        dataFrame['Policy-ARN'] = policy        #Adding the details to the dataframe
        df1 = pd.DataFrame([dataFrame], columns=dataFrame.keys()) #Creating Df with dictionary
        df1.to_csv('./usersDetails.csv',index=False)    #Writing to CSV
        print("User Name with {} has been created and details are added to CSV.. ".format(userName))
    except Exception as e: 
        if e.response['Error']['Code']=='EntityAlreadyExists':      #handling exception from botocore exceptions
            print("User with {} already exists.. Exiting the code".format(userName))
            sys.exit(0)     #exiting code if user already exists
        else:
            print("Issue creating the IAM User : {}".format(e))
            sys.exit(0)
    
def generatePasswordUsingListComprehension(lenOfPassword, validChars):
    try:
        finalPassword = "".join(choice(validChars) for eachCharacter in range(lenOfPassword))
        return finalPassword
    except Exception as e: 
        print("Issue generating the password : {}".format(e))
        return -1

def startScript():
    try:
        start = datetime.now()
        password = generatePasswordUsingListComprehension(LENGTH_OF_PASSWORD,VALID_CHARACTERS)
        # createIAMUserWithConsoleAccess(IAM_CLIENT_OBJECT,IAM_USER_NAME,password,POLICY_ARN)
        # createIAMUserWithProgrammaticAccess(IAM_CLIENT_OBJECT,IAM_USER_NAME,password,POLICY_ARN)
        # createIAMUserWithConsoleAndProgrammaticAccess(IAM_CLIENT_OBJECT,IAM_USER_NAME,password,POLICY_ARN)
        endtime = datetime.now()
        timeDiff = endtime - start
        print("Time taken to complete the script : {} (HOURS : MINS : SECONDS)".format(timeDiff))
    except Exception as e: print("Issue loading the script : {}".format(e))
    
if __name__=='__main__':
    startScript()


