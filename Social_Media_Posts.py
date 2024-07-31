import json
import uuid
import boto3
import re


def lambda_handler(event, context):
    # Extracting the post content from event
    msg = event['content']

    # Extracting the hashtags. \w matches only alphabets and numbers.
    hashtags = re.findall(r'#\w+', msg)

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
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'{e}')
        }

    # Uploading the hashtags to a table
    if len(hashtags) > 0:
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Post_Hashtags')
            for hashtag in hashtags:
                response = table.update_item(Key={'Hashtag': hashtag},
                                             UpdateExpression='SET #Counts = if_not_exists(#Counts, :start) + :increment',
                                             ExpressionAttributeNames={'#Counts': 'Counts'},
                                             ExpressionAttributeValues={':increment': 1, ':start': 0},
                                             ReturnValues="UPDATED_NEW")
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
