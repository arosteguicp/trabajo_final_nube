import json
import boto3
import urllib.parse

def lambda_handler(event, context):
    client = boto3.client("rekognition")
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    #passing s3 bucket object file reference    
    response = client.detect_labels(Image = {"S3Object": {"Bucket": "karutestbucket", "Name": key}}, MaxLabels=5,  MinConfidence=90)
    labels_list = []
    for i in response['Labels']:
        if i['Categories'][0]['Name'] == 'Animals and Pets':
            labels_list.append(i['Name'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('image-labels-table')
    labels = {
        'image_key': key,
        'image_label' : str(labels_list)
        
    }
    table.put_item(Item=labels)
    return "200"
