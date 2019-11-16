import boto3
import json
import os

s3_region = os.environ['S3_REGION']
transcribe = boto3.client('transcribe')
step_client = boto3.client('stepfunctions')
state_machine_arn = os.environ['STATE_MACHINE_ARN']


def lambda_handler(event, context):
    print(json.dumps(event))
    file_object = event['S3ObjectURL']
    contact_id = event['ContactID']
    job_name = event['job_name']

    try:
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f'{file_object}'},
            MediaFormat='wav',
            LanguageCode='en-US',
        )
    except Exception as inst:
        print(inst)
        raise inst
    status = response['ResponseMetadata']['HTTPStatusCode']
    if status == 200:
        response['ContactId'] = contact_id
        print(response)
        return response['TranscriptionJob']
    else:
        raise Exception("Transcription job failed to start")
