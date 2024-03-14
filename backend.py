from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()

class SentimentRequest(BaseModel):
    text: str

@app.post("/sentiments")
async def get_sentiment(sentiment_request: SentimentRequest):
    sentiment = random.choice(["positivo", "negativo"])
    return {"sentiment": sentiment}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
