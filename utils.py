import os
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from google import genai
from gtts import gTTS
import time
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Sentiment(BaseModel):
    title:str
    sentiment:str
    topics:list[str]
    summary:str

class CoverageDifference(BaseModel):
    comparison: str
    impact: str

class TopicOverlap(BaseModel):
    common_topics: List[str]
    unique_topics_in_each_article: List[str]  # Fixed key name

class AnalysisModel(BaseModel):
    coverage_differences: List[CoverageDifference]
    topic_overlap: TopicOverlap
    final_sentiment_analysis: str

class TranslateModel(BaseModel):
    original:str
    translated:str

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

async def fetch_google_news(company_name,limit:int=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    url=f"https://www.google.com/search?q={company_name}+news&tbm=nws"

    response = requests.get(url,headers=headers)
    if response.status_code!=200:
        print('Retrieval Failed')
        return []

    soup=BeautifulSoup(response.text,'html.parser')

    #manually checked the class name of news article titles and description
    titles=soup.find_all('div',class_="n0jPhd ynAwRc MBeuO nDgy9d")
    descriptions = soup.find_all("div", class_="GI74Re nDgy9d")

    news_data=[]

    for i in range(min(limit,len(titles),len(descriptions))):
        title_text = titles[i].get_text(strip=True) if titles[i] else "No Title"
        desc_text = descriptions[i].get_text(strip=True) if descriptions[i] else "No Description"
        news_data.append((title_text, desc_text))
    
    return news_data


async def sentimentAnalyzer(title:str,description:str):

    prompt=f"""
        Analyze the sentiment of the following news article text. 
        Categorize it as Positive, Negative, or Neutral.
        Also extract key topics mentioned in the article.
        Provide a concise summary of the article in 2-3 sentences.
        
        Article text:
        {title}
        Article description:
        {description}
        
        Output format:
        {{
            'title':title of article
            'sentiment': "Positive/Negative/Neutral",
            'topics': ["Topic1", "Topic2", "Topic3"],
            'summary': "Concise summary of the article"
        }}
        """
    

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': Sentiment,
            },
        )
        result = json.loads(response.text)
        return result
        
    except Exception as exp:
        print(f"Error analyzing element: {exp}")
        return {
            "sentiment":"Neutral",
            "topics":["Error"],
            "summary":"Failed to analyze sentiment"
        }

async def comparative_analysis(articles:List[Dict[str,Any]])->Dict[str,Any]:
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment = article.get("sentiment","Neutral")
        sentiment_counts[sentiment]+=1
    
    all_topics = []
    for article in articles:
            all_topics.extend(article.get("topics", []))

    unique_topics = list(set(all_topics))

    articles_summary = "\n\n".join([
            f"Article {i+1}:\nTitle: {article['title']}\nSentiment: {article['sentiment']}\nTopics: {', '.join(article['topics'])}\nSummary: {article['summary']}"
            for i, article in enumerate(articles)
        ])

    prompt = f"""
        Perform a comparative analysis on the following news articles about a company.
        
        {articles_summary}
        
        Generate a comparative analysis in the following JSON format:
        {{
            "coverage_differences": [
                {{
                    "comparison": "How different articles cover the company differently",
                    "impact": "Potential impact of these differences on company perception"
                }}
            ],
            "topic_overlap": {{
                "common_topics": ["Topics that appear in multiple articles"],
                "unique_topics in each article": ["Topics that appear in only one article"]
            }},
            "final_sentiment_analysis": "Overall sentiment conclusion and potential implications"
        }}
        
        Provide 2-3 meaningful comparisons. 
        """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': AnalysisModel,
            },
        )
        result_json = json.loads(response.text)

        comparative_result = {
                "sentiment_distribution": sentiment_counts,
                **result_json
            }
        return comparative_result
        
    except Exception as exp:
        print(f"Error analyzing element: {exp}")
        return {
                "sentiment_distribution": sentiment_counts,
                "coverage_differences": [],
                "topic_overlap": {"common_topics": [], "unique_topics": []},
                "final_sentiment_analysis": "Failed to perform comparative analysis."
            }


async def generateHindiTTS(company:str,text:str):
    output_dir ="audio"
    output_file = f"{output_dir}/{company}.mp3"

    os.makedirs(output_dir, exist_ok=True)  

    prompt = f"""
        Translate the following English text to Hindi:
        
        {text}
        
        Provide only the Hindi translation, without any additional text or explanations.
        Generate a comparative analysis in the following JSON format, this is a strict rule:
        {{
            original:original_text,
            transalated:transalated_Text
        }}
        """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config={
                'response_mime_type':'application/json',
                'response_schema': TranslateModel
            }
        )

        translated_data = json.loads(response.text)
        hindi_data = translated_data["translated"]

        tts = gTTS(text=hindi_data,lang='hi')
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error while generating Hindi TTS: {e}")
        tts = gTTS(text="माफ़ करें, हम आपके अनुरोध को प्रोसेस नहीं कर सके।", lang='hi')
        tts.save(output_file)
        return output_file


