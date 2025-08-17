"""
🧠 HYOJIN.AI Core Engine for Railway Deployment
"""

import json
import datetime
import random
import sqlite3
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class AIRequest:
    domain: str
    action: str
    data: Dict[str, Any]
    user_id: str
    timestamp: datetime.datetime

@dataclass 
class AIResponse:
    status: str
    result: Dict[str, Any]
    confidence: float
    processing_time: float
    error_message: Optional[str] = None

class HyojinAICore:
    """Railway 배포용 AI 엔진"""
    
    def __init__(self):
        self.version = "1.0.0-Railway"
        self.supported_domains = [
            "payment", "delivery", "shopping", 
            "realestate", "education", "jobs"
        ]
        self.initialize_database()
    
    def initialize_database(self):
        """데이터베이스 초기화"""
        self.db_path = os.environ.get("DB_PATH", "hyojin_ai.db")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                action TEXT NOT NULL,
                user_id TEXT NOT NULL,
                request_data TEXT NOT NULL,
                response_data TEXT,
                confidence REAL,
                processing_time REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def process_request(self, request: AIRequest) -> AIResponse:
        """AI 요청 처리"""
        start_time = datetime.datetime.now()
        
        try:
            if request.domain == "payment":
                result = self._process_payment(request)
            elif request.domain == "delivery":
                result = self._process_delivery(request)
            elif request.domain == "shopping":
                result = self._process_shopping(request)
            elif request.domain == "realestate":
                result = self._process_realestate(request)
            elif request.domain == "education":
                result = self._process_education(request)
            elif request.domain == "jobs":
                result = self._process_jobs(request)
            else:
                raise ValueError(f"Unsupported domain: {request.domain}")
            
            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds() * 1000
            
            confidence_value = result.get("confidence", 0.95)
            if isinstance(confidence_value, (int, float)):
                confidence = float(confidence_value)
            else:
                confidence = 0.95
            
            response = AIResponse(
                status="success",
                result=result,
                confidence=confidence,
                processing_time=processing_time
            )
            
            self._log_request(request, response)
            return response
            
        except Exception as e:
            end_time = datetime.datetime.now()
            processing_time = (end_time - start_time).total_seconds() * 1000
            
            return AIResponse(
                status="error",
                result={},
                confidence=0.0,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    def _process_payment(self, request: AIRequest) -> Dict[str, Any]:
        """결제 도메인 처리"""
        action = request.action
        data = request.data
        
        if action == "analyze_transaction":
            amount = data.get("amount", 0)
            risk_score = min(100, max(0, random.uniform(5, 25)))
            return {
                "transaction_id": f"TXN_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                "risk_score": risk_score,
                "risk_level": "low" if risk_score < 30 else "medium",
                "recommended_action": "approve" if risk_score < 50 else "review",
                "confidence": 0.94
            }
        return {"error": "Unknown action", "confidence": 0.0}
    
    def _process_delivery(self, request: AIRequest) -> Dict[str, Any]:
        """배달 도메인 처리"""
        return {
            "estimated_time": f"{random.randint(15, 45)}분",
            "distance": f"{random.uniform(2.5, 8.0):.1f}km",
            "confidence": 0.87
        }
    
    def _process_shopping(self, request: AIRequest) -> Dict[str, Any]:
        """쇼핑 도메인 처리"""
        return {
            "recommendations": [{"item": f"상품 {i}"} for i in range(3)],
            "confidence": 0.92
        }
    
    def _process_realestate(self, request: AIRequest) -> Dict[str, Any]:
        """부동산 도메인 처리"""
        return {
            "estimated_price": random.randint(500000000, 1500000000),
            "confidence": 0.85
        }
    
    def _process_education(self, request: AIRequest) -> Dict[str, Any]:
        """교육 도메인 처리"""
        return {
            "recommended_courses": [{"course": f"강의 {i}"} for i in range(3)],
            "confidence": 0.90
        }
    
    def _process_jobs(self, request: AIRequest) -> Dict[str, Any]:
        """채용 도메인 처리"""
        return {
            "matched_candidates": [{"name": f"후보자 {i}"} for i in range(3)],
            "confidence": 0.86
        }
    
    def _log_request(self, request: AIRequest, response: AIResponse):
        """요청 로깅"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ai_requests 
                (domain, action, user_id, request_data, response_data, confidence, processing_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.domain, request.action, request.user_id,
                json.dumps(request.data), json.dumps(response.result),
                response.confidence, response.processing_time
            ))
            conn.commit()
            conn.close()
        except Exception:
            pass  # 로깅 실패 시 무시
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ai_requests")
            total = cursor.fetchone()[0]
            conn.close()
            return {"total_requests": total, "version": self.version}
        except Exception:
            return {"total_requests": 0, "version": self.version}
