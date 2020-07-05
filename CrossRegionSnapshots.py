import boto3            #importing the boto3 module

SOURCE_REGION = 'us-east-1'     #setting the source region to copy the snapshots
DEST_REGION = 'us-east-2'       #setting the destination region to migrate snapshots

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name='root')   #working with root profile
EC2_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name=SOURCE_REGION)   #ec2 client object
STS_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='sts',region_name=SOURCE_REGION)   #sts client object for account number
EC2_DEST_OBJECT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name=DEST_REGION)   #dest region ec2 client object

accountID = STS_CLIENT_OBJECT.get_caller_identity()['Account']      #fetching our account ID

backupFilter = {'Name':'tag:Backup','Values':['Yes']}   #filter for fetching snapshots based on tags
waiterObject = EC2_DEST_OBJECT.get_waiter('snapshot_completed')     #waiter object for destination object

#using list comprehension to contain all the list of snapshots with provided filters
backupSnapsList=[
    eachSnap['SnapshotId']
    for eachSnap in EC2_CLIENT_OBJECT.describe_snapshots(OwnerIds=[accountID],Filters=[backupFilter])['Snapshots']    #iterating on 'Snapshots' key
]

#copying the snapshot to the destination region using copy_snapshot() 
for eachSnap in backupSnapsList:
    print("Taking backup for {} into {}".format(eachSnap,DEST_REGION))
    EC2_DEST_OBJECT.copy_snapshot(
        Description='Copy of the snapshot',
        SourceRegion=SOURCE_REGION,
        SourceSnapshotId=eachSnap
    )

#changing tag to complete after done
for eachSnap in backupSnapsList:
    print("Deleting the old tag for {}".format(eachSnap))
    EC2_CLIENT_OBJECT.delete_tags(
        Resources=[eachSnap],       #passing our snapshot id as resource parameter
        Tags=[
            {
                'Key':'Backup',
                'Value':'Yes'
            }
        ]
    )
    print("Renaming the new tag for {}".format(eachSnap))
    EC2_CLIENT_OBJECT.create_tags(
        Resources=[eachSnap],       #passing our snapshot id as resource parameter
        Tags=[
            {
                'Key':'Backup',
                'Value':'Complete'
            }
        ]
    )




    

