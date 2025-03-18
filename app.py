import streamlit as st
import requests
import pandas as pd
import os
from typing import Dict, Any, List
import json
import time

# Set page config
st.set_page_config(
    page_title="News Sentiment Analyzer",
    page_icon="📰",
    layout="wide"
)


# API endpoint for fastapi
API_URL = os.getenv("API_URL", "http://localhost:8000")


def render_comparative_analysis(analysis: Dict[str, Any]):
    st.subheader("Comparative Analysis")
    st.write("##### Sentiment Distribution")
    sentiment_dist = analysis.get("sentiment_distribution", {})
    if sentiment_dist:
        # Create a pie chart
        sentiment_df = pd.DataFrame({
            "Sentiment": list(sentiment_dist.keys()),
            "Count": list(sentiment_dist.values())
        })
        st.bar_chart(sentiment_df.set_index("Sentiment"))

    st.write("##### Coverage Differences")
    coverage_diff = analysis.get("coverage_differences", [])
    for i, diff in enumerate(coverage_diff):
        st.markdown(f"**Comparison {i+1}: ** {diff.get('comparison', '')}")
        st.markdown(f"**Impact: ** {diff.get('impact', '')}")
        st.markdown("---")
    
    st.write("##### Topic Analysis")
    topic_overlap = analysis.get("topic_overlap", {})
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Common Topics:**")
        common_topics = topic_overlap.get("common_topics", [])
        if common_topics:
            for topic in common_topics:
                st.markdown(f"- {topic}")
        else:
            st.markdown("No common topics found")
    
    with col2:
        st.markdown("**Unique Topics:**")
        unique_topics = topic_overlap.get("unique_topics_in_each_article", [])
        if unique_topics:
            for topic in unique_topics:
                st.markdown(f"- {topic}")
        else:
            st.markdown("No unique topics found")


def render_articles(articles: List[dict[Any]]):
    st.subheader("Article Analysis")
    if articles:
        for i, article in enumerate(articles):
            with st.expander(f"Article {i+1}: {article['title']}"):
                st.markdown(f"**Sentiment:** {article['sentiment']}")
                st.markdown(f"**Summary:** {article['summary']}")
                st.markdown("**Topics:**")
                for topic in article.get('topics', []):
                    st.markdown(f"- {topic}")
    else:
        st.warning("No articles found")


def main():
    st.title("News Sentiment Analyzer")
    st.markdown("""
    This app analyzes sentiment from news articles about a company.It extracts key information, performs sentiment analysis, and provides a comparative overview.
    """)

    with st.form("company_form"):
        company_name = st.text_input("Enter Company Name", "Tesla")
        article_limit = st.slider("Number of Articles to Analyze", min_value=3, max_value=15, value=10)
        
        submitted = st.form_submit_button("Analyze")
        
        if submitted:
            if not company_name:
                st.error("Please enter a company name")
                return
            
            with st.spinner(f"Analyzing news for {company_name}..."):
                try:
                    response = requests.post(
                        f"{API_URL}/analyze",
                        json={"company_name": company_name, "article_limit": article_limit}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Analysis completed successfully!")
                        
                        st.header(f"Analysis Results for {data['Company']}")
                        
                        st.subheader("Final Sentiment Analysis")
                        st.info(data.get("Final Sentiment Analysis", "No final analysis available"))
                        
                        st.subheader("Hindi Audio Summary")
                      
                        audio_path = data.get("audio_path")
                        print(audio_path)
                        if audio_path:
                            st.markdown(f"[📥 Download Audio]({audio_path})", unsafe_allow_html=True)
                        else:
                            st.warning("Audio file not available")
                        
                        render_comparative_analysis(data.get("Comparative Sentiment Score", {}))
                        
                        render_articles(data.get('Articles',[]))
                        
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    st.sidebar.title("About")
    st.sidebar.info("""
    This application uses:
    - BeautifulSoup for web scraping
    - Gemini AI for sentiment analysis
    - FastAPI for backend services
    - gTTS for Hindi text-to-speech
    """)
    
    # Display API status
    try:
        health_response = requests.get(f"{API_URL}/health")
        if health_response.status_code == 200:
            st.sidebar.success("API is online")
        else:
            st.sidebar.error("API is offline")
    except:
        st.sidebar.error("Cannot connect to API")

if __name__ == "__main__":
    main()