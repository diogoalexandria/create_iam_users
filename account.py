import boto3

def get_account():
    client = boto3.client("sts")
    return client.get_caller_identity()["Account"] 
    