import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    return get_secret_value_response["SecretString"]
