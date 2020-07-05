import boto3        #module for working with boto3
from datetime import datetime   #working with datetime objects
import pandas as pd     #working with dataframes

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name="root")   #Accessing AWS Console with root credentials
IAM_CLIENT = AWS_MGMT_CONSOLE.client(service_name='iam')    #client object

df = pd.DataFrame()     #Empty DataFrame
Collection={}           #Empty Collection Dictionary

def ListUsers(clientObject):
    try:
        global df
        for eachUser in clientObject.list_users()['Users']:   #Iterating over Users key to get info about users
            Collection['Arn'] = eachUser['Arn']
            Collection['CreationDate'] = eachUser['CreateDate'].strftime("%Y-%m-%d")     #Fetching required attributes
            Collection['UserId'] = eachUser['UserId']
            Collection['UserName'] = eachUser['UserName']
            for eachGroup in clientObject.list_groups_for_user(UserName=Collection['UserName'])['Groups']:  #Separate loop for groups
                Collection['GroupName'] = eachGroup['GroupName']
                Collection['GroupCreatedOn'] = eachGroup['CreateDate'].strftime("%Y-%m-%d")
                for eachPolicy in clientObject.list_attached_group_policies(GroupName = eachGroup['GroupName'])['AttachedPolicies']:
                    Collection['Policy'] = eachPolicy['PolicyName'] #separate loop for policies
            df1 = pd.DataFrame([Collection], columns=Collection.keys()) #Creating Df with dictionary
            df =  pd.concat([df,df1])     #Appending the Dataframe to Original DataFrame
        return df
    except Exception as e: print("Issue listing the users: {}".format(e))
    
def writeToCSV(DataFrame):
    try:
        DataFrame.to_csv('./IAMInventory.csv',index=False)  #ignoring the index column while writing to csv
        print("CSV has been Updated..")
    except Exception as e: print("Issue writing to CSV : {}".format(e))
    
def startScript():
    try:
        start = datetime.now()      #starting time of the script
        dataFrame = ListUsers(IAM_CLIENT)   #function to list user attributes and store in a dataframe
        writeToCSV(dataFrame)       #writing the dataframe to csv
        endtime = datetime.now()        #endtime of the script
        timeDiff = endtime - start      #total time taken for completion
        print("Time taken to finish the script : {} (HOURS : MINS : SECONDS)".format(timeDiff))
    except Exception as e: print("Issue running the main script : {}".format(e))
    
if __name__=='__main__':
    startScript()
    

