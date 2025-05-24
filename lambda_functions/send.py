import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        # Parse incoming message
        body = json.loads(event.get('body', '{}'))
        message = body.get('message')
        if not message:
            raise ValueError("Missing 'message' in request body")
        
        # Get API Gateway endpoint
        request_context = event.get('requestContext', {})
        domain = request_context.get('domainName')
        stage = request_context.get('stage')
        if not domain or not stage:
            raise ValueError("Missing WebSocket endpoint information")
            
        api_gateway = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url=f"https://{domain}/{stage}"
        )

        # Get all connection IDs
        connection_ids = []
        try:
            paginator = dynamodb.get_paginator('scan')
            for page in paginator.paginate(TableName=os.environ['WEBSOCKET_TABLE']):
                for item in page.get('Items', []):
                    if 'ConnectionId' in item and 'S' in item['ConnectionId']:
                        connection_ids.append(item['ConnectionId']['S'])
        except Exception as e:
            logger.error(f"Error scanning DynamoDB: {str(e)}")
            raise

        # Broadcast message to all connections
        for conn_id in connection_ids:
            try:
                api_gateway.post_to_connection(
                    Data=json.dumps({'message': message}),
                    ConnectionId=conn_id
                )
            except api_gateway.exceptions.GoneException:
                # Connection no longer exists - could remove from DynamoDB
                logger.info(f"Connection {conn_id} gone, could be cleaned up")
            except Exception as e:
                logger.error(f"Error posting to connection {conn_id}: {str(e)}")

        return {'statusCode': 200}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }