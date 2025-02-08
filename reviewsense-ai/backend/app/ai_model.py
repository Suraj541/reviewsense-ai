import os
from transformers import pipeline
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text: str):
    return sentiment_analyzer(text[:512])[0]

def analyze_with_gpt4(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "Analyze this review for key insights and suggested actions:"
        }, {
            "role": "user",
            "content": text
        }],
        max_tokens=200
    )
    return response.choices[0].message.content