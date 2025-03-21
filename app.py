import subprocess
import os
import time
import streamlit as st
import requests
import json

# Determine the API base URL based on the environment.
# For local testing, use localhost; for Spaces, use 0.0.0.0.
if os.environ.get("HUGGING_FACE_SPACE"):
    API_BASE_URL = "http://0.0.0.0:8000"
else:
    API_BASE_URL = "http://localhost:8000"

# Start the FastAPI server in a background process if not already running.
if not os.environ.get("FASTAPI_RUNNING"):
    os.environ["FASTAPI_RUNNING"] = "1"
    # Start the server on 0.0.0.0 so it works in Spaces.
    subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])
    # Wait a few seconds to ensure the API server has started.
    time.sleep(5)

def get_sentiment_report(company):
    """
    Calls the /process_news API endpoint to get the sentiment report.
    """
    try:
        response = requests.post(f"{API_BASE_URL}/process_news", params={"company": company})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return None

def get_tts_audio(report_text):
    """
    Calls the /tts API endpoint to generate Hindi TTS audio from the report text.
    """
    try:
        response = requests.post(f"{API_BASE_URL}/tts", params={"text": report_text})
        if response.status_code == 200:
            data = response.json()
            audio_file = data.get("AudioFile")
            return audio_file
        else:
            st.error(f"TTS API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error calling TTS API: {e}")
        return None

st.title("News Summarization & Hindi TTS Application")
st.write("Enter a company name to fetch news articles, perform sentiment analysis, and generate a Hindi audio report.")

# Company input
company = st.text_input("Enter Company Name", "Tesla")

if st.button("Generate Report"):
    with st.spinner("Fetching and processing news articles..."):
        report_data = get_sentiment_report(company)
        if report_data:
            # Format the JSON output for readability.
            report_text = json.dumps(report_data, indent=2, ensure_ascii=False)
            st.subheader("Sentiment Report")
            st.text_area("Report", report_text, height=300)
            
            # Get the TTS audio file from the API.
            audio_file_name = get_tts_audio(report_text)
            if audio_file_name and os.path.exists(audio_file_name):
                with open(audio_file_name, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.subheader("Hindi TTS Audio")
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Audio file not found on the server.")

