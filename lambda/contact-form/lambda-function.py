import json
import boto3
import os
import base64

ses = boto3.client('ses', region_name=os.environ['SES_REGION'])

def lambda_handler(event, context):
    try:
        # Debug log the incoming event
        print("EVENT RECEIVED:", json.dumps(event))

        # Handle both API Gateway proxy and direct JSON events
        if "body" in event:
            body_raw = event["body"] or "{}"
            # Decode if base64-encoded
            if event.get("isBase64Encoded"):
                body_raw = base64.b64decode(body_raw).decode("utf-8")
            body = json.loads(body_raw)
        else:
            body = event  # direct invocation

        # Extract fields with safe defaults
        name = body.get("name", "No name")
        email = body.get("email", "no-reply@example.com")
        message = body.get("message", "")

        # Send email via SES
        response = ses.send_email(
            Source=os.environ['SOURCE_EMAIL'],
            Destination={
                'ToAddresses': os.environ['DEST_EMAIL'].split(',')  # supports multiple recipients
            },
            Message={
                'Subject': {'Data': f"Contact Form Submission from {name}"},
                'Body': {
                    'Text': {
                        'Data': f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
                    }
                }
            },
            ReplyToAddresses=[email] if email else []
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "messageId": response["MessageId"]
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }
