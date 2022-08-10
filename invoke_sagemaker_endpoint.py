import os
import io
import boto3
import json
import base64
import time

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')
S3_BUCKET_NAME = 'xxxx'

def __create_uniqe_key():
    """
    Get s3 object key.
    :return:
    """
    return 'asl-%s.jpg' % int(round(time.time() * 1000))
    
def __upload_to_s3(key, file_path):
    """
    Upload file to S3
    :param key:
    :param file_path:
    :return:
    """
    result = True
    s3_client = boto3.client("s3")
    file_key = key
    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME, file_key)
    except Exception as e:
        print(e)
        result = False
    return result

def lambda_handler(event, context):
    """
    Process enter function.
    :param event:
    :param context:
    :return:
    """
    body = None
    file_key = None
    err_msg = None
    if event:
        try:
            data = json.loads(json.dumps(event))
            body = json.loads(data['body'])
        except Exception as e:
            print(e)
    else:
        err_msg = 'Parameter error, please use POST method'
        return {"statusCode": 200, "body": err_msg}

    file_key = __create_uniqe_key()

    image_64 = body.get('image64', None)
    if image_64 is None:
        return {"statusCode": 201, "body": 'image is error'}
    # print(image_64)
    # image_64 = __get_base64()

    file_path = '/tmp/%s' % file_key

    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(image_64))
        
    #__upload_to_s3(file_key,file_path)
    
    #payload = base64.b64decode(image_64)
    with open(file_path, 'rb') as f:
        payload = f.read()

    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/x-image',
                                       Body=payload)
    print(response)
    result = json.loads(response['Body'].read().decode())
    print(result)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(result)
    }
