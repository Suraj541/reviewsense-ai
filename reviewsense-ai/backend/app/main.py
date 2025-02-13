from fastapi import FastAPI, Depends, HTTPException, UploadFile, Response
from fastapi.security import HTTPBearer
from pymongo.collection import Collection
from .database import get_db
from .auth import verify_token
from .ai_model import analyze_sentiment, analyze_with_gpt4
from .social_apis import fetch_tweets, fetch_instagram_comments
from .file_processor import FileProcessor

app = FastAPI()
security = HTTPBearer()

# Existing Endpoints
@app.post("/analyze")
async def analyze_review(
    text: str,
    db: Collection = Depends(get_db),
    user: dict = Depends(verify_token)
):
    """
    Analyze a single review text for sentiment.
    """
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
async def analyze_gpt4(
    text: str,
    user: dict = Depends(verify_token)
):
    """
    Get advanced insights using GPT-4.
    """
    try:
        return {"analysis": analyze_with_gpt4(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/social/tweets")
async def get_tweets(
    query: str,
    user: dict = Depends(verify_token)
):
    """
    Fetch tweets related to a query.
    """
    try:
        return fetch_tweets(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/social/instagram")
async def get_instagram(
    media_id: str,
    user: dict = Depends(verify_token)
):
    """
    Fetch Instagram comments for a media ID.
    """
    try:
        return fetch_instagram_comments(media_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Endpoints for File Processing
@app.post("/analyze/excel")
async def analyze_excel(
    file: UploadFile,
    user: dict = Depends(verify_token)
):
    """
    Analyze reviews from an Excel/CSV file.
    """
    try:
        contents = await file.read()
        reviews = FileProcessor.process_excel(contents)
        analyzed = [{
            **r,
            "sentiment": analyze_sentiment(r['review_text'])["label"],
            "confidence": analyze_sentiment(r['review_text'])["score"]
        } for r in reviews]
        
        # Generate Excel report
        report = FileProcessor.generate_report(analyzed, 'excel')
        return Response(
            content=report,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=analysis_report.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/pdf")
async def analyze_pdf(
    file: UploadFile,
    user: dict = Depends(verify_token)
):
    """
    Analyze text from a PDF file.
    """
    try:
        contents = await file.read()
        text = FileProcessor.process_pdf(contents)
        analysis = analyze_sentiment(text)
        return {
            "original_text": text,
            "sentiment": analysis['label'],
            "confidence": analysis['score'],
            "gpt_insights": analyze_with_gpt4(text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
