# Census-Data-Standardization-and-Analysis-Pipeline

## Discription :-
The Social Media Hashtag Trend Analyzer project aims to analyze social media posts for trending hashtags efficiently. It involves creating a pipeline that processes social media posts, extracts hashtags, performs analysis using AWS Lambda functions, and generates meaningful insights and visualizations using Streamlit.


## Tools Used :-
[Python](https://www.python.org/downloads/)__, [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)__, [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)__, [AWS Lambda](https://docs.aws.amazon.com/lambda/)__, [AWS dynamodb](https://docs.aws.amazon.com/dynamodb/)__, [Streamlit](https://docs.streamlit.io/)

---

## Workflow :-
1. Submit Posts:
  * Users submit posts containing hashtags through a Streamlit web application.
  * The post is sent to an AWS Lambda function for processing.
2. Extract Hashtags:
  * The Lambda function `Social_Media_Posts.py` extracts hashtags from the post using regex.
3. Store Post Data:
  * The post content and a unique post ID are stored in the `Social_Media_Posts` DynamoDB table.
4. Update Hashtag Counts:
  * The extracted hashtags are stored and their counts are updated in the `Post_Hashtags` DynamoDB table.
5. Analyze Hashtags:
  * The Lambda function `Hashtag_analysis.py` retrieves and sorts hashtags by their usage frequency from the `Post_Hashtags` table.
6. Display Trending Hashtags:
  * The trending hashtags are displayed on the Streamlit app using a bar chart.

> [!NOTE]
1 - 4 are handled by the `Social_Media_Posts.py` Lambda function.
The Streamlit visualization is handled by the `streamlit_app.py` file.

---

### Requirements Installation
  // Install the required packages: 
  `pip install -r requirements.txt`
  
### Execute Command:

  // To run streamlit_app.py file: 
  `streamlit run streamlit_app.py`

---

> **CAUTION:** 
1. Kindly make sure that the required packages are installed.
2. Please make sure you're connected to your AWS account with proper IAM permissions for Lambda and DynamoDB before running these files.
3. Ensure that the AWS Lambda functions are deployed and connected to the correct DynamoDB tables.
4. Kindly make sure that you've installed Streamlit before running the streamlit_app.py file, if not then open the terminal and execute the command - `pip install streamlit`
5. In order to run the streamlit_app.py, open the command prompt and use the above *execute command.*
