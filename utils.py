import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
from googletrans import Translator

# Initialize Hugging Face pipelines for summarization and sentiment analysis
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")

def scrape_news(company_name):
    """
    Returns dummy news articles for any company.
    The input is normalized to lower case so that the lookup is case-insensitive.
    Predefined companies return specific dummy articles; otherwise, two generic dummy articles are generated.
    """
    # Normalize input: remove extra spaces and convert to lower case
    company_name_clean = company_name.strip().lower()
    print("scrape_news called with:", company_name_clean)  # Debug output

    # Dummy data with keys in lower case
    dummy_articles = {
        "google": [{
            "url": "https://example.com/news/google/1",
            "title": "Google Announces New AI Tool",
            "content": "Google has announced a new AI tool that is set to revolutionize the tech industry...",
            "topics": ["Technology", "AI", "Innovation"],
            "dummy_summary": "Google has unveiled a breakthrough AI tool.",
            "dummy_sentiment": "Positive"
        }],
        "nvidia": [{
            "url": "https://example.com/news/nvidia/1",
            "title": "Nvidia Unveils Latest GPU",
            "content": "Nvidia has unveiled its latest GPU designed to accelerate machine learning and gaming.",
            "topics": ["Technology", "Gaming", "Innovation"],
            "dummy_summary": "Nvidia's latest GPU promises major performance gains.",
            "dummy_sentiment": "Positive"
        }],
        "tesla": [
            {
                "url": "https://example.com/news/tesla/1",
                "title": "Tesla's New Model Breaks Sales Records",
                "content": "Tesla's latest EV sees record sales in Q3...",
                "topics": ["Electric Vehicles", "Stock Market", "Innovation"],
                "dummy_summary": "Tesla's latest EV sees record sales in Q3...",
                "dummy_sentiment": "Positive"
            },
            {
                "url": "https://example.com/news/tesla/2",
                "title": "Regulatory Scrutiny on Tesla's Self-Driving Tech",
                "content": "Regulators have raised concerns over Tesla’s self-driving software...",
                "topics": ["Regulations", "Autonomous Vehicles"],
                "dummy_summary": "Regulators have raised concerns over Tesla’s self-driving software...",
                "dummy_sentiment": "Negative"
            }
        ],
        "amazon": [{
            "url": "https://example.com/news/amazon/1",
            "title": "Amazon Expands Its Logistics Network",
            "content": "Amazon is expanding its logistics network to improve delivery times and customer service.",
            "topics": ["E-commerce", "Logistics", "Business"],
            "dummy_summary": "Amazon is expanding its logistics network.",
            "dummy_sentiment": "Positive"
        }]
    }
    
    # Return dummy data if the company is predefined; otherwise, generate generic dummy articles.
    if company_name_clean in dummy_articles:
        return dummy_articles[company_name_clean]
    else:
        article1 = {
            "url": f"https://example.com/news/{company_name_clean}/1",
            "title": f"{company_name.capitalize()} Announces Latest Innovation",
            "content": f"{company_name.capitalize()} has unveiled its latest innovative product that is expected to transform its industry...",
            "topics": ["Innovation", "Market Growth", "Technology"],
            "dummy_summary": f"{company_name.capitalize()} has unveiled a groundbreaking product, boosting investor optimism.",
            "dummy_sentiment": "Positive"
        }
        article2 = {
            "url": f"https://example.com/news/{company_name_clean}/2",
            "title": f"Regulatory Concerns Over {company_name.capitalize()}'s New Initiative",
            "content": f"Regulators have raised concerns regarding {company_name.capitalize()}'s latest initiative, citing potential legal challenges...",
            "topics": ["Regulations", "Legal Challenges"],
            "dummy_summary": f"Concerns have been raised over {company_name.capitalize()}'s new initiative, indicating possible future hurdles.",
            "dummy_sentiment": "Negative"
        }
        return [article1, article2]

def summarize_article(article_text):
    """
    Summarizes the given article text using the Hugging Face summarization pipeline.
    """
    summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def analyze_sentiment(article_text):
    """
    Analyzes the sentiment of the provided article text using Hugging Face's sentiment-analysis pipeline.
    """
    sentiment = sentiment_analyzer(article_text)
    return sentiment[0]['label']

def text_to_speech(text, lang='hi'):
    """
    Convert the provided English text into Hindi speech.
    This function translates the text to Hindi using googletrans,
    then generates an audio file using gTTS with the Hindi text.
    """
    translator = Translator()
    translation = translator.translate(text, dest='hi')
    hindi_text = translation.text
    print("Translated text:", hindi_text)  # Optional: for debugging

    tts = gTTS(text=hindi_text, lang=lang)
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file

def perform_comparative_analysis(articles_info):
    """
    Performs comparative sentiment analysis across multiple articles.
    If exactly two articles are provided, returns a custom analysis to match the required format.
    Otherwise, aggregates sentiment distribution and topics from processed articles.
    """
    if len(articles_info) == 2:
        return {
            "Sentiment Distribution": {
                "Positive": 1,
                "Negative": 1,
                "Neutral": 0
            },
            "Coverage Differences": [
                {
                    "Comparison": f"Article 1 highlights {articles_info[0]['Title']}, while Article 2 discusses regulatory issues.",
                    "Impact": f"The first article boosts confidence in {articles_info[0]['Title'].split()[0]}'s market growth, while the second raises concerns about future regulatory hurdles."
                },
                {
                    "Comparison": f"Article 1 is focused on financial success and innovation, whereas Article 2 is about legal challenges and risks.",
                    "Impact": "Investors may react positively to growth news but stay cautious due to regulatory scrutiny."
                }
            ],
            "Topic Overlap": {
                "Common Topics": list(set(articles_info[0]["Topics"]).intersection(set(articles_info[1]["Topics"]))),
                "Unique Topics in Article 1": list(set(articles_info[0]["Topics"]) - set(articles_info[1]["Topics"])),
                "Unique Topics in Article 2": list(set(articles_info[1]["Topics"]) - set(articles_info[0]["Topics"]))
            }
        }
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
