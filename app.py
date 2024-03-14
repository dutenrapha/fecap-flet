from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

class SentimentRequest(BaseModel):
    text: str

@app.post("/sentiments")
async def get_sentiment(sentiment_request: SentimentRequest):
    sentiment = random.choice(["positivo", "negativo"])
    return {"sentiment": sentiment}