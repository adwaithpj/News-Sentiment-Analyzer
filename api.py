from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import time
import tempfile
from .utils import fetch_google_news, sentimentAnalyzer,comparative_analysis,generateHindiTTS

app = FastAPI(title="News Sentiment Analysis API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_dir = tempfile.mkdtemp()

class CompanyRequest(BaseModel):
    company_name: str
    article_limit: int = 10

class ArticleResponse(BaseModel):
    url: str
    title: str
    summary: str
    sentiment: str
    topics: List[str]

class CompanyAnalysisResponse(BaseModel):
    CompanyAnalysisResponsecompany: str
    Articles: List[ArticleResponse]
    Comparative_analysis: Dict[str, Any]
    final_sentiment_analysis: str
    audio_path: Optional[str] = None




@app.post("/analyze")
async def analyze_company(request: CompanyRequest, background_tasks: BackgroundTasks):
    articles = await fetch_google_news(request.company_name,request.article_limit)
    
    sentiment_analyzed_data=[]
    for article in articles:
        sentiment_analyzed_data.append(await sentimentAnalyzer(article[0],article[1]))
    
    comparative_analyzed_data = await comparative_analysis(sentiment_analyzed_data)
    new_comparative_analyzed_data = {key: value for key, value in comparative_analyzed_data.items() if key != "final_sentiment_analysis"}
    audio_path = await generateHindiTTS(request.company_name,comparative_analyzed_data['final_sentiment_analysis'])

    final_result = {
        "Company":request.company_name,
        "Articles":sentiment_analyzed_data,
        "Comparative Sentiment Score":new_comparative_analyzed_data,
        "Final Sentiment Analysis":comparative_analyzed_data['final_sentiment_analysis'],
        "audio_path":audio_path
    }

    return final_result


def cleanup_old_files(directory: str, max_age: int = 3600):
    """Clean up files older than max_age seconds."""
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and current_time - os.path.getmtime(file_path) > max_age:
            os.remove(file_path)
    
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
