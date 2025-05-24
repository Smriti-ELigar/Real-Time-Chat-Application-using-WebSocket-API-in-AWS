import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        connection_id = event.get('requestContext', {}).get('connectionId')
        if not connection_id:
            raise ValueError("Missing connectionId in request context")

        dynamodb.put_item(
            TableName=os.environ['WEBSOCKET_TABLE'],
            Item={'ConnectionId': {'S': connection_id}}
        )

        return {'statusCode': 200}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }