# 📰 News Sentiment Analyzer

Analyze News Sentiment with AI & Web Scraping

A **full-stack** AI-powered news sentiment analysis application using:  
✅ **Frontend** → Streamlit 📊  
✅ **Backend** → FastAPI ⚡  
✅ **GenAI** → Google Gemini 2.0 Flash 🤖  
✅ **Web Scraping** → BeautifulSoup 🌐  
✅ **Package Management** → Poetry 📦

## **📌 Features**

🔍 **Web Scraping**: Fetches real-time news from Google News using BeautifulSoup.  
💬 **Sentiment Analysis**: Uses **Google Gemini 2.0 Flash** for analyzing news sentiment.  
📊 **Interactive UI**: Built with **Streamlit** for easy visualization.  
⚡ **FastAPI Backend**: Provides REST API endpoints for sentiment analysis.  
🔧 **Modular Codebase**: Utility functions are organized in the `utils/` folder.

# 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**

```
git clone https://github.com/your-repo/news-sentiment-analyzer.git
cd news-sentiment-analyzer
```

### **2️⃣ Install Poetry (if not installed)**

```
pip install poetry

```

### **3️⃣ Install Dependencies**

```
poetry install
```

### **4️⃣ Set Up Environment Variables**

Create a **`.env`** file in the project root and add:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

### **5️⃣ Run the FastAPI Backend**

```
poetry run fastapi dev api.py
```

📍 The API will be available at **http://127.0.0.1:8000**

![image](https://github.com/user-attachments/assets/555c7027-3e5a-4f9d-acc4-5a1e832d8b10)


### **6️⃣ Run the Streamlit Frontend**

Create a new powershell/cmd and run:

```
poetry run streamlit run app.py
```

📍 The UI will be available at **http://localhost:8501**

---

## **📁 Project Structure**

```
📂 news-sentiment-analyzer/
│── 📄 api.py              # FastAPI backend
│── 📄 app.py              # Streamlit frontend
│── 📄 utils.py            # Utility functions (web scraping, AI requests)
│── 📜 poetry.lock         # Poetry dependency lock file
│── 📜 pyproject.toml      # Poetry project config
│── 📜 README.md           # Project
│── 📜 requirements.txt    # Requirements
│── 📂 audio               # Transcribed Hindi audio
│──documentation (this file)

```

## **🚀 API Endpoints**

### **🔹 Sentiment Analysis API**

-   **Endpoint**: `/analyze`
-   **Method**: `POST`
-   **Request Body**

```
{
"company_name":"Tesla",
"article_limit":5
}
```

or you can check in FastAPI docs after running the server.

```
http://127.0.0.1:8000/docs
```

## **📜 License**

MIT License 🔓

🎯 **Contribute & Improve**: Feel free to open **issues & PRs**! 🚀

Adwaith PJ | ©️ 2025
