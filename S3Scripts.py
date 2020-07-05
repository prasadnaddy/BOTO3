try:        #writing a try-except block to detect the boto3 module, if not installed then install it automatically
    import sys,subprocess   #calling the sys and subprocess modules for installing pip packages if not found
    import boto3        #calling the boto3 module
    
except ModuleNotFoundError as e:
    package = (str(e).split(" ")[-1]).replace("'","")       #getting the modulename from exception message
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])    #calling pip -m install command
    print("{} was missing and has been installed successfully...".format(package))  #printing the message on screen
    
finally:    #executing the set of codes after handling modulenotfound error
    AWS_MGMT_CONSOLE = boto3.session.Session(profile_name='root')       #working on root profile
    S3_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='s3',region_name='us-east-1')   #s3 client object
    
    paginatorObject =  S3_CLIENT_OBJECT.get_paginator('list_objects')   #paginator object
    
    #function to list all the buckets using client object
    def listBuckets():
        try:
            for eachBucket in S3_CLIENT_OBJECT.list_buckets()['Buckets']:   #iterating over 'Buckets' key
                print("Bucket Name : {}\tCreation Date: {}".format(
                    eachBucket['Name'],
                    eachBucket['CreationDate'].strftime('%Y-%m-%d'))
                )
        except Exception as e: print("Issue listing buckets: {}".format(e))

    def listObjectsInBucket():
        try:
            BucketName = 'cf-templates-4u351hjm9psg-us-east-1'
            for eachPage in paginatorObject.paginate(Bucket=BucketName):    #paginating over objects in a bucket
                for eachObject in eachPage['Contents']:   #iterating over 'contents' key
                    print("Object Name: {}".format(eachObject['Key']))
        except Exception as e: print("Issue listing objects: {}".format(e))

    listObjectsInBucket()