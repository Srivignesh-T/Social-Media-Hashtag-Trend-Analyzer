import streamlit as st
import requests

# Streamlit application layout
st.title("Social Media Post Composer")

# Input field for post composition
post_content = st.text_area("Compose your post here...")

if st.button("Post"):
    # Send post content to AWS Lambda for processing
    response = requests.post('LAMBDA_API_URL', json={"content": post_content})
    st.success("Post submitted successfully!")

if st.button("Show Trending Hashtags"):
    # Fetch trending hashtags from the backend
    response = requests.get('LAMBDA_API_URL/trending')
    trending_hashtags = response.json().get("trending_hashtags", [])
    st.write("Trending Hashtags:")
    st.write(trending_hashtags)
