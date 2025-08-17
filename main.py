"""
🚂 HYOJIN.AI Railway 배포용 메인 앱
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import json
from datetime import datetime
from app.core.ai_engine import HyojinAICore
from app.api import payment, delivery, shopping, realestate, education, jobs

# FastAPI 앱 생성
app = FastAPI(
    title="HYOJIN.AI Core API",
    description="6개 도메인 AI 시스템",
    version="1.0.0-MVP"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# AI 엔진 초기화
ai_engine = HyojinAICore()

@app.get("/")
async def root():
    """메인 페이지"""
    return {
        "message": "🧠 HYOJIN.AI Core API",
        "version": "1.0.0-MVP",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "domains": "/api/v1/domains",
            "payment": "/api/v1/payment/*",
            "delivery": "/api/v1/delivery/*",
            "shopping": "/api/v1/shopping/*",
            "realestate": "/api/v1/realestate/*",
            "education": "/api/v1/education/*",
            "jobs": "/api/v1/jobs/*"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        stats = ai_engine.get_stats()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "ai_engine": stats,
            "database": "connected",
            "memory_usage": "normal"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/api/v1/domains")
async def get_domains():
    """지원 도메인 목록"""
    return {
        "domains": ai_engine.supported_domains,
        "total": len(ai_engine.supported_domains),
        "description": "HYOJIN.AI가 지원하는 AI 도메인들"
    }

# 도메인별 라우터 포함
app.include_router(payment.router, prefix="/api/v1/payment", tags=["Payment"])
app.include_router(delivery.router, prefix="/api/v1/delivery", tags=["Delivery"])
app.include_router(shopping.router, prefix="/api/v1/shopping", tags=["Shopping"])
app.include_router(realestate.router, prefix="/api/v1/realestate", tags=["RealEstate"])
app.include_router(education.router, prefix="/api/v1/education", tags=["Education"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
