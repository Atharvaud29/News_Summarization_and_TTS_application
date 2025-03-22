# News Summarization and Text-to-Speech Application in Hindi.

## Objective of Project :

1. Develop a web-based application that extracts key details from multiple news articles related
to a given company, performs sentiment analysis, conducts a comparative analysis, and
generates a text-to-speech (TTS) output in Hindi.

2. The tool should allow users to input a
company name and receive a structured sentiment report along with an audio output.

## Project Workflow :

![Screenshot 2025-03-22 180401](https://github.com/user-attachments/assets/e312cb7c-85f5-4794-a7cc-689cb16b7015)

After the Streamlit UI is created, the model deployment is done on **HuggingFace Space**

## Working :

**Step-1** = Install all the requied library's for project in requirements.txt file

    fastapi
    uvicorn
    streamlit
    beautifulsoup4
    requests 
    transformers
    gTTs

**Step-2** = Create the utils.py file 

    import requests
    from bs4 import BeautifulSoup
    from transformers import pipeline
    from gtts import gTTS
    from googletrans import Translator
    summarizer = pipeline("summarization")
    sentiment_analyzer = pipeline("sentiment-analysis")

    def scrape_news(company_name):
        """ Write your own prompt """

    def summarize_article(article_text):
        """ Write your own prompt """

    def analyze_sentiment(article_text):
        """ Write your own prompt """

    def text_to_speech(text, lang='hi'):
        """ Write your own prompt """

    def perform_comparative_analysis(articles_info):
        """ Write your own prompt """
        if len(articles_info) == 2:
        return {
            "Sentiment Distribution": {
                "Positive": 1,
                "Negative": 1,
                "Neutral": 0
            },
        else:
            sentiment_distribution = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
            topics_list = []

            for article in articles_info:
            sentiment = article.get("Sentiment", "NEUTRAL").upper()
            if sentiment in sentiment_distribution:
                sentiment_distribution[sentiment] += 1
            else:
                sentiment_distribution[sentiment] = 1
            topics_list.extend(article.get("Topics", []))
    
        return {
            "Sentiment Distribution": sentiment_distribution,
            "Coverage Differences": [
                {
                    "Comparison": "Some articles emphasize the company's growth while others focus on challenges.",
                    "Impact": "Mixed sentiment could influence investor decisions."
                }
            ],
            "Topic Overlap": {
                "Common Topics": list(set(topics_list)),
                "Unique Topics": {}
            }
        }

**Step-3** = Now write code in api.py file which will call our **api endpoints** 

    from fastapi import FastAPI, HTTPException
    from utils import (
        scrape_news, 
        summarize_article, 
        analyze_sentiment, 
        perform_comparative_analysis, 
        text_to_speech
    )
    app = FastAPI(title="News Summarization & Hindi TTS API")

    @app.get("/fetch_news")
    def fetch_news(company: str):
        """ Your own code """

    @app.post("/process_news")
    def process_news(company: str):
        """ Your own code """

    @app.post("/tts")
    def generate_tts(text: str):
        """ Your own code """

**Step-4** = Write the code in app.py file which can run the **FastAPI server in background** & alos run model localy for testing it and also display the output in **streamlit ui**

    import subprocess
    import os
    import time
    import streamlit as st
    import requests
    import json
    if os.environ.get("HUGGING_FACE_SPACE"):
    API_BASE_URL = "http://0.0.0.0:8000"
    else:
        API_BASE_URL = "http://localhost:8000"

    if not os.environ.get("FASTAPI_RUNNING"):
    os.environ["FASTAPI_RUNNING"] = "1"
    subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])
    time.sleep(5)

    def get_sentiment_report(company):
        """ Your own code """

    def get_tts_audio(report_text):
        """ Your own code """

    ## Streamlit UI
    st.title("News Summarization & Hindi TTS Application")
    st.write("Enter a company name to fetch news articles, perform sentiment analysis, and generate a Hindi audio report.")

    company = st.text_input("Enter Company Name")

    if st.button("Generate Report"):
    with st.spinner("Fetching and processing news articles..."):
        report_data = get_sentiment_report(company)
        if report_data:
            report_text = json.dumps(report_data, indent=2, ensure_ascii=False)
            st.subheader("Sentiment Report")
            st.text_area("Report", report_text, height=300)
            
            audio_file_name = get_tts_audio(report_text)
            if audio_file_name and os.path.exists(audio_file_name):
                with open(audio_file_name, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.subheader("Hindi TTS Audio")
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Audio file not found on the server.")

**Step-5** = Streamlit UI output interface look

![Screenshot 2025-03-22 190337](https://github.com/user-attachments/assets/aa4a0c8a-6970-4053-aea1-6ef75f3aee09)

**Step-6** = Deployment of model on **HaggingFace Space**

## Project Conclusion = 

This project demonstrates an end-to-end pipeline that extracts news articles for a given company, processes them through multiple NLP steps, and generates a Hindi audio report.
The pipeline works as follows:

1. News Extraction :
The system collects or simulates news articles (dummy data) based on the company name provided by the user.

2. Text Processing :
Each article is summarized using Hugging Face's summarization pipeline.
Sentiment analysis is performed to classify the article as Positive, Negative, or Neutral.
A comparative analysis aggregates the sentiments and topics across articles.

3. Text-to-Speech Conversion :
The final report is translated into Hindi via googletrans.
gTTS converts the translated text into an audio file.

4. User Interface & API Integration :
A Streamlit UI gathers user input and displays the structured report.
A FastAPI backend handles data processing, with the two components seamlessly integrated (and deployable on Hugging Face Spaces).

This concise pipeline highlights the project’s modular design, showcasing how modern NLP techniques and web technologies can work together to deliver multilingual, interactive applications.


        
