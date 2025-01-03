import json
import boto3
import os

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION = os.environ['REGION']
#METRIC = os.environ['METRIC']
DATABASE = os.environ['DATABASE']
#HOST_IN_ZABBIX = os.environ['ZABBIX_HOST_DST']
#ITEM_KEY = os.environ['ITEM_KEY']
DATABASE = os.environ['DATABASE']

def get_status(database):
    client = boto3.client('neptune', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,region_name=REGION)
    
    
    response = client.describe_db_instances(
    Filters=[
        {
            'Name': 'db-cluster-id',
            'Values': [
                DATABASE
            ]
        }
    ])
    total = (len(response["DBInstances"]))
    cont = 0
    result = '{ "data": ['
    for DBInstances in response["DBInstances"]:
        new_line = '{"DBInstance":' +'"'+ DBInstances["DBInstanceIdentifier"] +'"'+ ',"Status":'+'"'+ DBInstances["DBInstanceStatus"]+'"'+'}'
        result = result + new_line
        if (cont+1) < total:
            result = result + ","
            cont = cont+1
    result = result + "]}"

    return(result)

def get_cluster_status(database):
    client = boto3.client('neptune', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,region_name=REGION)

 

    response = client.describe_db_clusters(
    DBClusterIdentifier=database
    )

 

    Status = response["DBClusters"][0]["Status"]
    return(Status)




