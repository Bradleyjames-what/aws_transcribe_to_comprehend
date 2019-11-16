import json
import os
import re
import boto3
import uuid

s3 = boto3.client('s3')

s3_region = os.environ['S3_REGION']
state_machine_arn = os.environ['STATE_MACHINE_ARN']


def lambda_handler(event, context):
    print(json.dumps(event))
    step_client = boto3.client('stepfunctions')

    s3_key = event['Records'][0]['s3']['object']['key']
    s3_bucket_name = event['Records'][0]['s3']['bucket']['name']

    contact_id = get_contact_id(s3_key)
    job_name = f'{contact_id}{str(uuid.uuid4())}'

    s3_url = f'https://s3-{s3_region}.amazonaws.com/{s3_bucket_name}/{s3_key}'

    step_input = {
        'S3ObjectURL': s3_url,
        'ContactID': contact_id,
        'job_name': job_name
        }

    response = step_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(step_input)
    )

    print("Step Function Response:")
    print(response)
    return {
        'statusCode': 200,
        'body': 'Successfully Initiated Step Function!'
    }


# Regular Expression to create a unique ID for the Job in Step Function
def get_contact_id(s3_key_val):
    key = s3_key_val
    contact_id = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(?=_)",
                           key).group(0)
    print(contact_id)
    return contact_id