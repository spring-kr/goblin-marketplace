"""
Delivery API Router
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import datetime
from app.core.ai_engine import AIRequest, HyojinAICore

router = APIRouter()
ai_engine = HyojinAICore()

class DeliveryRequest(BaseModel):
    action: str
    data: Dict[str, Any]
    user_id: str = "anonymous"

@router.post("/process")
async def process_delivery(request: DeliveryRequest):
    """
    Delivery 도메인 AI 처리
    """
    try:
        ai_request = AIRequest(
            domain="delivery",
            action=request.action,
            data=request.data,
            user_id=request.user_id,
            timestamp=datetime.datetime.now()
        )
        
        response = ai_engine.process_request(ai_request)
        
        return {
            "status": response.status,
            "result": response.result,
            "confidence": response.confidence,
            "processing_time": response.processing_time,
            "error": response.error_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info")
async def get_delivery_info():
    """
    Delivery 도메인 정보
    """
    return {
        "domain": "delivery",
        "description": "Delivery AI 시스템",
        "available_actions": ["process"],
        "status": "active"
    }
