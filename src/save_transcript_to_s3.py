import json
import os
from urllib.request import urlopen

import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print(event)

    transcript_bucket = os.environ['transcipt_bucket_name']
    try:
        transcript_name = event["TranscriptionJobName"]
        link = event["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_path = f"/tmp/{transcript_name}.json"
        f = urlopen(link)
        transcript_str = f.read()
        transcript_obj = json.loads(transcript_str)
        with open(transcript_path, 'w') as outfile:
            json.dump(transcript_obj, outfile)

        response = s3.put_object(transcript_path, transcript_bucket, f"transcripts/{transcript_name}")
        return response

    except Exception as e:
        raise e
