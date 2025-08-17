from fastapi import FastAPI
from app.core.ai_engine import HyojinAICore
import uvicorn

app = FastAPI(title="HYOJIN.AI Serverless", version="1.0.0")
ai_engine = HyojinAICore()

@app.get("/")
def root():
    return {"message": "🧠 HYOJIN.AI Serverless on Vercel", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "platform": "vercel"}

# Vercel용 핸들러
handler = app
