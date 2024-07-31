import boto3
import json


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Post_Hashtags'
    table = dynamodb.Table(table_name)

    try:
        response = table.scan()
        response = response['Items']
        sorted_items = sorted(response, key=lambda x: x['Counts'], reverse=True)
        return {
            'statusCode': 200,
            'body': json.dumps(sorted_items)
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }
