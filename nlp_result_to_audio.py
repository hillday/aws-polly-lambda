import json
import boto3
import urllib3

http = urllib3.PoolManager()


def load_json(json_file):
    # Opening JSON file
    f = open(json_file)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    content_ls = [' '.join(data['content'][str(i)]['word_list']) for i in range(len(data['content']))]
    label_ls = [int(data['content'][str(i)]['ner_label'][0]) for i in range(len(data['content']))]
    role_dict = data['role_id']
    return content_ls,label_ls,role_dict
    
def polly_request(data):
    response = http.request('POST',
                        'https://xxxx.execute-api.xxxxx.amazonaws.com/test',
                        body = json.dumps(data),
                        headers = {'Content-Type': 'application/json'},
                        retries = False)
    print(response)

def lambda_handler(event, context):
    BUCKET = 'xxxx'
    KEY = 'nlpoutput/2164082.json'
    client = boto3.client('s3')
    
    client.download_file(BUCKET,KEY,'/tmp/2164082.json')
    content_ls,label_ls,role_dict = load_json('/tmp/2164082.json')
    print(len(content_ls))
    
    # polly_request({"text":"Hello","name": "test3.mp3","voiceId":"Kendra"})
    for i in range(len(content_ls)):
        filename = str(i) + ".mp3"
        voiceId = 'Kendra'
        if label_ls[i] == 0:
            voiceId = 'Kendra'
        elif label_ls[i] == 1:
            voiceId = 'Joey'
        elif label_ls[i] == 2:
            voiceId = 'Salli'
        else:
            voiceId = 'Kimberly'
            
        polly_request({"text":content_ls[i],"name": filename,"voiceId": voiceId})
            
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('convert !')
    }
