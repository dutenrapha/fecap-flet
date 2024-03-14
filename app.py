from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()

emojis = ["😀", "😍", "🎉", "🚀", "💡", "👍", "👏"]

@app.get("/api/emoji")
async def get_random_emoji():
    return random.choice(emojis)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
