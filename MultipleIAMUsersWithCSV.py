import boto3                    #importing the boto3 module for boto3 scripts
from random import choice           #Importing the choice class from random module
import pandas as pd         #importing pandas module to add the details as dataframe to csv
from datetime import datetime   #datetime for capturing starting and ending time
import sys              #For performing systematic operations
from collections import defaultdict     #For dictionary operations 

##Random password Generation Configuration##
LENGTH_OF_PASSWORD = 10       #setting the length of the password
VALID_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?'   #allowed chars

##BOTO3 Configurations##
SESSION_OBJECT = boto3.session.Session(profile_name='root')  #Creating session object with root profile
IAM_CLIENT_OBJECT = SESSION_OBJECT.client(service_name='iam')    #creating client object for IAM service

dict={}     #Empty dictionary to perform merge operation while writing to csv
EmptyDF = pd.DataFrame()        #empty dataframe to append the old dataframe into this one while writing to csv

def readCsvFileUsingPandas():
    try:
        inputDataFrame = pd.read_csv('./IAMUsersRequirements.csv',index_col=False,dtype=str)
        lengthOfCsv = inputDataFrame.shape[0]       #Fetching the number of rows in the csv
        return inputDataFrame, lengthOfCsv      #returning the number of rows and dataframe
    except Exception as e: print("Issue reading the CSV file : {}".format(e))
    
def createIAMUserWithConsoleAccess(clientObject, userName, password, policy):
    try:
        dataFrame={}
        clientObject.create_user(UserName = userName)   #creating the user with specified username using create_user()
        #Now we will be creating the login profile with username, password and setting passwordReset to False
        dataFrame['Access-Key-ID']= ''      #Keeping this blank, because it is not applicable for console access
        dataFrame['Secret-Access-Key']=''   #Keeping this blank, because it is not applicable for console access
        clientObject.create_login_profile(UserName = userName, Password = password, PasswordResetRequired = True)
        clientObject.attach_user_policy(UserName = userName, PolicyArn = policy)    #attaching role to the user
        dataFrame['UserName'] = userName
        dataFrame['Password'] = password
        dataFrame['Policy-ARN'] = policy        #Adding the details to the dataframe
        print("User Name with {} has been created and details are added to CSV.. ".format(userName))
        return dataFrame
    except Exception as e: 
        if e.response['Error']['Code']=='EntityAlreadyExists':      #handling exception from botocore exceptions
            print("User with {} already exists.. Exiting the code".format(userName))
            sys.exit(0)     #exiting code if user already exists
        else:
            print("Issue creating the IAM User : {}".format(e))
            sys.exit(0)
            
def createIAMUserWithProgrammaticAccess(clientObject, userName, password, policy):
    try:
        dataFrame={}
        clientObject.create_user(UserName = userName)   #creating the user with specified username using create_user()
        #Now we will be creating the login profile with username, password and setting passwordReset to False
        response = clientObject.create_access_key(UserName = userName) #creating access keys and we get response
        dataFrame['Access-Key-ID'] = response['AccessKey']['AccessKeyId']
        dataFrame['Secret-Access-Key'] = response['AccessKey']['SecretAccessKey']
        clientObject.attach_user_policy(UserName = userName, PolicyArn = policy)    #attaching role to the user
        dataFrame['UserName'] = userName
        dataFrame['Password'] = password
        dataFrame['Policy-ARN'] = policy        #Adding the details to the dataframe
        print("User Name with {} has been created and details are added to CSV.. ".format(userName))
        return dataFrame
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
        print("User Name with {} has been created and details are added to CSV.. ".format(userName))
        return dataFrame
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
    
def writeToCSV(dictionary1,dictionary2,dictionary3):
    try:
        global EmptyDF
        parameters = locals()       #getting the parameters name:value in dictionary format
        for eachDict in parameters.values():    #We get the values here of the parameter dictionaries
            dict.update(eachDict)   #Updating the new value of dictionaries
            df = pd.DataFrame([dict], columns=dict.keys()) #Creating Df with dictionary
            EmptyDF =  pd.concat([EmptyDF,df])     #Appending the Dataframe to Original DataFrame
        EmptyDF.to_csv('./IAMUsersOutput.csv',index=False)    #Writing to CSV
    except Exception as e: print("Issue writing the files to csv: {}".format(e))
    
def startScript():
    try:
        start = datetime.now()
        inputDataFrame, usersLength = readCsvFileUsingPandas()   #Reading the csv as dataframe
        for eachUser, programmatic, consoleaccess,arn in zip(inputDataFrame['IAM_User_Name'],inputDataFrame['Programatic_Access'],inputDataFrame['Console_Access'],inputDataFrame['PolicyARN']):
            if programmatic=='Yes' and consoleaccess=='Yes':    #Both programmatic and console access
                password = generatePasswordUsingListComprehension(LENGTH_OF_PASSWORD,VALID_CHARACTERS)
                progConsoleDict = createIAMUserWithConsoleAndProgrammaticAccess(IAM_CLIENT_OBJECT,eachUser,password,arn)
            elif programmatic=='Yes' and consoleaccess=='No':   #Only Programmatic access
                password = generatePasswordUsingListComprehension(LENGTH_OF_PASSWORD,VALID_CHARACTERS)
                progDict = createIAMUserWithProgrammaticAccess(IAM_CLIENT_OBJECT,eachUser,password,arn)
            elif programmatic=='No' and consoleaccess=='Yes':   #Only Console access
                password = generatePasswordUsingListComprehension(LENGTH_OF_PASSWORD,VALID_CHARACTERS)
                consoleDict = createIAMUserWithConsoleAccess(IAM_CLIENT_OBJECT,eachUser,password,arn)
            else:
                print("Wrong input")
        writeToCSV(progConsoleDict,progDict,consoleDict)    #Finally writing the results back to CSV
        endtime = datetime.now()
        timeDiff = endtime - start
        print("Time taken to complete the script : {} (HOURS : MINS : SECONDS)".format(timeDiff))
    except Exception as e: print("Issue loading the script : {}".format(e))
    
if __name__=='__main__':
    startScript()
    
