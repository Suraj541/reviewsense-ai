from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from .database import get_db
from .auth import verify_token
from .ai_model import analyze_sentiment, analyze_with_gpt4
from .social_apis import fetch_tweets, fetch_instagram_comments
from pymongo.collection import Collection

app = FastAPI()
security = HTTPBearer()

@app.post("/analyze")
async def analyze_review(text: str, 
                        db: Collection = Depends(get_db),
                        user: dict = Depends(verify_token)):
    try:
        sentiment = analyze_sentiment(text)
        result = {
            "text": text,
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        }
        db.insert_one(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/gpt4")
async def analyze_gpt4(text: str, user: dict = Depends(verify_token)):
    try:
        return {"analysis": analyze_with_gpt4(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/social/tweets")
async def get_tweets(query: str, user: dict = Depends(verify_token)):
    try:
        return fetch_tweets(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/social/instagram")
async def get_instagram(media_id: str, user: dict = Depends(verify_token)):
    try:
        return fetch_instagram_comments(media_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))