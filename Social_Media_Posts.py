import json
import uuid
import boto3
import re
import logging

# Configure logging for debugging purpose in cloudwatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Extracting the post content from event
    msg = event['content']

    # Extracting the hashtags. \w matches only alphabets and numbers.
    hashtags = re.findall(r'#\w+', msg)
    logger.info(f"Extracted hashtags: {hashtags}")

    # Creating a DynamoDB table connection
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Social_Media_Posts'
    table = dynamodb.Table(table_name)

    # Generating a unique Post ID
    post_id = str(uuid.uuid4())  # Using UUID to generate a unique ID

    # Items to be inserted in the DynamoDB table
    item = {
        'id': post_id,  # Partition key
        'Post': msg
    }

    # Inserting the post data into table
    try:
        response = table.put_item(Item=item)
        logger.info(f"Post inserted with ID: {post_id}")

    except Exception as e:
        logger.error(f"Error inserting post: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'{e}')
        }

    # Uploading the hashtags to a table
    if len(hashtags) > 0:
        try:
            hashtag_table_name = 'Post_Hashtags'
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(hashtag_table_name)
            for hashtag in hashtags:
                response = table.update_item(Key={'Hashtag': hashtag},
                                             UpdateExpression='ADD #Counts:increment',
                                             ExpressionAttributeNames={'#Counts': 'Counts'},
                                             ExpressionAttributeValues={':increment': 1})
            return {
                'statusCode': 200,
                'body': json.dumps("Posted Successfully.")
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps(f'{e}')
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("Posted Successfully")
        }
