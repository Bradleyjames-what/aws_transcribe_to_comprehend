import json
import logging
import os
import re
import urllib.parse
import urllib.request

import boto3

s3_client = boto3.client('s3')
comprehend_client = boto3.client('comprehend')
s3_region = os.environ['S3_REGION']
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print(f"New Event: {json.dumps(event)}")
    s3_object_key = event['Records'][0]['s3']['object']['key']
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote(s3_object_key)

    s3_obj = s3_client.get_object(Bucket=s3_bucket, Key=key)


    try:
        response = s3_obj.get()['Body'].decode('utf-8')
    except Exception as e:
        logging.exception("URL ERROR")
        raise e

    transcript_results = json.loads(response)
    transcript = transcript_results['TranscriptionJob']['Transcript']

    payload = initialize_payload(s3_object_key)
    payload['TEXT'] = transcript

    sentiment_response = batch_detect_sentiment(transcript)
    key_phrases_response = batch_detect_key_phrases(transcript)

    payload['Sentiment'] = sentiment_response['ResultList']
    payload['KeyPhrases'] = key_phrases_response['ResultList']
    print(json.dumps(payload['Sentiment'], sort_keys=True, indent=4))
    print(json.dumps(payload['KeyPhrases'], sort_keys=True, indent=4))

    sentiment_results = payload['Sentiment']
    key_phrase_results = payload['KeyPhrases']

    json_name = f"_Comprehend/ {payload['Key']} _.json"
    json_body = {
        'sentiment': sentiment_results,
        'key_phrases': key_phrase_results
        }
    final_name = json.dumps(json_name).encode('UTF-8')
    final_body = json.dumps(json_body).encode('UTF-8')

    final_put = s3_client.put_object(Body=json.dumps(final_body, sort_keys=True, indent=4), Bucket=s3_bucket, Key=final_name)
    print(final_put)


def create_presigned_url(bucket_name, S3_Key):

    S3KeyNoURLEncoding = urllib.parse.unquote(S3_Key)

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': S3KeyNoURLEncoding},
                                                ExpiresIn=604800)
    # The response contains the presigned URL
    return response


def initialize_payload(s3_key_val):
    """
    :param s3 key of put object:
    :return: dict payload {Key: regex of s3 key}
    """
    key = s3_key_val
    payload = {}
    format_key = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}(?=_)",key).group(0)
    payload['Key'] = format_key
    return payload


def batch_detect_sentiment(text_list):
    return comprehend_client.batch_detect_sentiment(
        TextList=text_list,
        LanguageCode='en'
    )


def batch_detect_key_phrases(text_list):
    return comprehend_client.batch_detect_key_phrases(
        TextList=text_list,
        LanguageCode='en'
    )
