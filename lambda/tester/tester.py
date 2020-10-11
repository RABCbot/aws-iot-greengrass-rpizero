import boto3
import json

client = boto3.client('iot-data', region_name='us-east-1')

def lambda_handler(event, context):
    response = client.publish(
        topic='home/services/trigger',
        qos=0,
        payload=json.dumps(event)
    )
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }
