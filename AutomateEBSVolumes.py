import boto3            #module for working with boto3 scripts

AWS_MGMT_CONSOLE = boto3.session.Session(profile_name='root')   #Working with root profile
EC2_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name='us-east-1') #working on ec2 client object

#iterating on 'regions' key in describe_regions and storing regions in a list like this using List comprehension
RegionsList = [eachRegion['RegionName'] for eachRegion in EC2_CLIENT_OBJECT.describe_regions()['Regions']]  

#Generator Comprehension object containing each regions from list, access it using next(RegionObject)
RegionObject = (eachRegion for eachRegion in RegionsList)   

while True:     #Running the infinite loop and exiting the loop after all regions are finished
    try:
        RegionName = next(RegionObject)
        EC2_SUBREGION_CLIENT_OBJECT = AWS_MGMT_CONSOLE.client(service_name='ec2',region_name=RegionName) #working on ec2 client object
        FilterByTag = {'Name':'tag:Prod','Values':['Backup']}   #Filtering volumes based on tags
        PaginatorObject = EC2_SUBREGION_CLIENT_OBJECT.get_paginator('describe_volumes') #paginator object
        WaiterObject = EC2_SUBREGION_CLIENT_OBJECT.get_waiter('snapshot_completed') #Waiter object
        #appending the list of volumes by volume ID to a list using list comprehension
        print("Working on Region : {}".format(RegionName))
        ListOfVolumeIDs = [
                           volumeDetails['VolumeId']
                           for eachPage in PaginatorObject.paginate(Filters=[FilterByTag])  
                           for eachVolume in eachPage['Volumes']
                           for volumeDetails in eachVolume['Attachments']
                           ]
        print("List of volume IDs present : {}".format(ListOfVolumeIDs))
        #Iterating over the List containing the volume id of specific region and creating snapid list comprehension
        SnapShotCreationResponseList = [  
            response := EC2_SUBREGION_CLIENT_OBJECT.create_snapshot(        #creating snapshot with this function
                Description='Taking Important Snapshot',        #description provided for the snapshot
                VolumeId=eachVolume,              #specifying the volume id
                TagSpecifications = [           #providing the tag specifications
                    {
                        'ResourceType' : 'snapshot',        #mentioning the resourcetype
                        'Tags':[
                            {
                                'Key':'Delete-On',      #providing the tag key
                                'Value': '90-Days'      #providing the tag value
                            }
                        ]
                    }
                ]
            )
            for eachVolume in ListOfVolumeIDs       #iterating over the list of volume id
        ]
        #Iterating over the response we get after the snapshot is created, so that we get the snapID in a list
        SnapShotIDList = [
            response['SnapshotId']
            for response in SnapShotCreationResponseList    
        ]
        print("Snapshot IDs list : {}".format(SnapShotIDList))
        if len(SnapShotIDList)!=0:  #Waiting for only snapshots that are getting created
            WaiterObject.wait(SnapshotIds=SnapShotIDList)   #waiting until the snapshots are created completely
            print("Snapshots are completed for {}".format(SnapShotIDList))
            print("********************************************************")
        else:
            print("No snapshots created here...")
            print("********************************************************")
    except StopIteration:     #after all regions are over, we get an exception, we handle it and break the loop to stop the process
        break   #stop the infinite loop
   





    
