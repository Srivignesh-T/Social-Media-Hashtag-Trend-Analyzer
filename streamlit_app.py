import boto3
import os
import json
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

# Load environment variables from .env file
load_dotenv()

access_key_id = os.getenv('ACCESS_KEY_ID')
secret_key_id = os.getenv('SECRET_ACCESS_KEY')
region = os.getenv('REGION')
# Creating a session to access Lambda
session = boto3.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_key_id,
    region_name=region
)

# Creating a Lambda client
lambda_client = session.client('lambda')

# Creating a streamlit app
st.title("Social Media Hashtag Trend Analyzer")

# Text input for posting a message
post = st.text_input("Type your post here", key="post_input")

# Button to submit post
if st.button("Submit Post"):
    if post:
        # initializes the chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        with st.chat_message("user"):
            st.markdown(post)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": post})

        # inputs for the Lambda function
        payload = {
            'content': post
        }
        st.write(payload)  # Using st.write for debugging purposes

        # Invoking Lambda function to store the message
        response = lambda_client.invoke(
            FunctionName='Social_Media_Posts',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))

        with st.chat_message("assistant"):
            st.markdown(response_payload)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_payload})

# Button to list trending hashtags
if st.button("Trending Hashtags"):
    response = lambda_client.invoke(
        FunctionName='Hashtag_analysis',
        InvocationType='RequestResponse'
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    response_payload = response_payload['body']

    # Displaying the output in table
    df = pd.DataFrame(response_payload)
    columns = {'Counts': 'No_Of_Uses', 'Hashtag': 'Hashtag'}
    df.rename(columns=columns, inplace=True)
    st.write('\n')
    st.dataframe(df)
    st.write('\n')
    st.bar_chart(df, x='Hashtag', y='No_Of_Uses')

# Displaying initial information
st.write("""INFO: \n
This is a Social Media Posts Trend Analyzer App. The Post Analyzer App can receive a post, \n
and check for the hashtags used. In the backend which is then stored and processed in \n
order to analyze the trend of the hashtags used while posting in this App. \n\n
Click the buttons above and try the App :) """)

