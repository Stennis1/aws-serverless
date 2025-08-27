import json
import boto3
import os

ses = boto3.client('ses', region_name=os.environ['SES_REGION'])

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        message = body['message']

        response = ses.send_email(
            Source=os.environ['SOURCE_EMAIL'],
            Destination={'ToAddresses': [os.environ['DEST_EMAIL']]},
            Message={
                'Subject': {'Data': f"Contact Form Submission from {name}"},
                'Body': {
                    'Text': {'Data': f"Name: {name}\nEmail: {email}\nMessage:\n{message}"}
                }
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'success', 'messageId': response['MessageId']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'error', 'message': str(e)})
        }
