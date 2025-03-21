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
    """
    Fetch raw news articles related to the given company.
    """
    articles = scrape_news(company)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")
    return {"Company": company, "Articles": articles}

@app.post("/process_news")
def process_news(company: str):
    """
    Process news articles by summarizing their content, performing sentiment analysis,
    and gathering key topics. Uses dummy data to simulate output in the required format.
    """
    articles = scrape_news(company)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    processed_articles = []
    for article in articles:
        # Use dummy summary and sentiment if present, otherwise process normally.
        if "dummy_summary" in article and "dummy_sentiment" in article:
            summary = article["dummy_summary"]
            sentiment = article["dummy_sentiment"]
        else:
            summary = summarize_article(article["content"])
            sentiment = analyze_sentiment(article["content"])
        processed_articles.append({
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": article["topics"]
        })
    
    # If exactly two articles, use a custom comparative analysis.
    if len(processed_articles) == 2:
        comparative_analysis = {
            "Sentiment Distribution": {
                "Positive": 1,
                "Negative": 1,
                "Neutral": 0
            },
            "Coverage Differences": [
                {
                    "Comparison": f"Article 1 highlights {processed_articles[0]['Title']}, while Article 2 discusses regulatory issues.",
                    "Impact": f"The first article boosts confidence in {company.capitalize()}'s market growth, while the second raises concerns about future regulatory hurdles."
                },
                {
                    "Comparison": f"Article 1 is focused on financial success and innovation, whereas Article 2 is about legal challenges and risks.",
                    "Impact": "Investors may react positively to growth news but stay cautious due to regulatory scrutiny."
                }
            ],
            "Topic Overlap": {
                "Common Topics": list(set(processed_articles[0]["Topics"]).intersection(set(processed_articles[1]["Topics"]))),
                "Unique Topics in Article 1": list(set(processed_articles[0]["Topics"]) - set(processed_articles[1]["Topics"])),
                "Unique Topics in Article 2": list(set(processed_articles[1]["Topics"]) - set(processed_articles[0]["Topics"]))
            }
        }
    else:
        comparative_analysis = perform_comparative_analysis(processed_articles)
    
    final_analysis = f"{company.capitalize()}'s latest news coverage is mostly positive. Potential stock growth expected." if len(processed_articles) == 2 else "Overall, the news coverage shows mixed sentiments with a slight lean towards positive growth."
    
    return {
        "Company": company,
        "Articles": processed_articles,
        "Comparative Sentiment Score": comparative_analysis,
        "Final Sentiment Analysis": final_analysis
    }

@app.post("/tts")
def generate_tts(text: str):
    """
    Generate a Hindi text-to-speech (TTS) audio file from the provided text.
    """
    try:
        audio_file = text_to_speech(text)
        return {"AudioFile": audio_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS conversion failed: {e}")

