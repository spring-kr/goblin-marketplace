"""
하드코딩된 응답 제거 및 동적 AI 분석 적용된 박사급 전문가 시스템
"""

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json
import re
from datetime import datetime

# AI 모델 로더 임포트
try:
    from ai_model_loader import ai_manager

    AI_ENABLED = True
    print("✅ AI 모델 시스템이 활성화되었습니다.")
except ImportError as e:
    print(f"⚠️ AI 모델을 불러올 수 없습니다: {e}")
    AI_ENABLED = False

# FastAPI 앱 생성
app = FastAPI(title="하이퍼 박사급 도깨비 전문가 시스템", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 모델
class ChatRequest(BaseModel):
    agent_type: str
    message: str


# 실제 16명의 박사급 도깨비 정보
AGENTS = {
    "medical": {"name": "의학박사 하이진", "emoji": "🏥"},
    "financial": {"name": "경제학박사 부자진", "emoji": "💰"},
    "legal": {"name": "법학박사 정의진", "emoji": "⚖️"},
    "tech": {"name": "공학박사 테크진", "emoji": "🔧"},
    "creative": {"name": "예술학박사 창조진", "emoji": "🎨"},
    "marketing": {"name": "마케팅박사 판매진", "emoji": "📈"},
    "education": {"name": "교육학박사 가르침진", "emoji": "📚"},
    "hr": {"name": "인사관리박사 인재진", "emoji": "👥"},
    "sales": {"name": "영업전략박사 성과진", "emoji": "💼"},
    "research": {"name": "연구개발박사 혁신진", "emoji": "🔬"},
    "translation": {"name": "언어학박사 번역진", "emoji": "🌐"},
    "consulting": {"name": "경영컨설팅박사 전략진", "emoji": "🎯"},
    "psychology": {"name": "심리학박사 마음진", "emoji": "🧠"},
    "data": {"name": "데이터과학박사 분석진", "emoji": "📊"},
    "startup": {"name": "창업학박사 스타트진", "emoji": "🚀"},
    "wellness": {"name": "웰니스박사 건강진", "emoji": "🌿"},
}


def generate_specialized_phd_response(
    agent: Dict[str, Any],
    message: str,
    keyword_matches: list,
    ai_analysis: Optional[Dict[str, Any]] = None,
) -> str:
    """전문 분야별 박사급 응답 생성 (동적 AI 분석 적용)"""
    agent_name = agent["name"]
    agent_emoji = agent.get("emoji", "🧙‍♂️")
    agent_type = None

    # AI 분석 정보 추출
    emotion_info = ""
    context_info = ""

    if ai_analysis and AI_ENABLED:
        emotion_analysis = ai_analysis.get("emotion_analysis", {})
        context_analysis = ai_analysis.get("context_analysis", {})

        if emotion_analysis.get("emotion"):
            emotion = emotion_analysis["emotion"]
            emotion_info = f"[감정: {emotion}] "

        if context_analysis.get("urgency_level"):
            urgency = context_analysis["urgency_level"]
            if urgency == "높음":
                context_info = f"[긴급도: {urgency}] "

    # 에이전트 타입 추출
    for key, value in AGENTS.items():
        if value["name"] == agent_name:
            agent_type = key
            break

    base_response = f"{agent_emoji} **{agent_name}** 박사급 전문 분석"

    # AI 분석 정보 추가
    ai_info_section = ""
    if ai_analysis and AI_ENABLED:
        ai_info_section = f"\n🤖 **AI 분석**: {emotion_info}{context_info}\n"

    # 동적 AI 기반 응답 생성
    if agent_type == "financial":
        try:
            if AI_ENABLED:
                smart_response = ai_manager.generate_smart_response(
                    message, "financial"
                )
                return smart_response
            else:
                return f"💰 **경제학박사급 전문가**: AI 분석 시스템이 비활성화되어 있습니다. 기본 상담을 진행합니다."
        except Exception as e:
            print(f"AI 금융 분석 오류: {e}")
            return f"💰 **경제학박사급 전문가**: 현재 시장 분석 시스템을 점검 중입니다. 잠시 후 다시 문의해주세요."

    elif agent_type == "medical":
        try:
            if AI_ENABLED:
                smart_response = ai_manager.generate_smart_response(message, "medical")
                return smart_response
            else:
                return f"🏥 **의학박사급 전문가**: AI 분석 시스템이 비활성화되어 있습니다. 기본 상담을 진행합니다."
        except Exception as e:
            print(f"AI 의료 분석 오류: {e}")
            return f"🏥 **의학박사급 전문가**: 현재 의료 분석 시스템을 점검 중입니다. 잠시 후 다시 문의해주세요."

    # 다른 전문 분야들도 동적 AI 분석 적용
    else:
        try:
            if AI_ENABLED:
                smart_response = ai_manager.generate_smart_response(
                    message, agent_type or "general"
                )
                return smart_response
            else:
                return f"{agent_emoji} **{agent_name}**: AI 분석 시스템이 비활성화되어 있습니다. 기본 상담을 진행합니다."
        except Exception as e:
            print(f"AI 분석 오류 ({agent_type}): {e}")
            return f"{agent_emoji} **{agent_name}**: 현재 분석 시스템을 점검 중입니다. 잠시 후 다시 문의해주세요."


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """채팅 엔드포인트 (완전 동적 AI 분석)"""
    try:
        agent_info = AGENTS.get(request.agent_type)
        if not agent_info:
            raise HTTPException(status_code=400, detail="잘못된 에이전트 타입입니다.")

        # AI 분석 수행 (활성화된 경우)
        ai_analysis = None
        if AI_ENABLED:
            try:
                emotion_analysis = ai_manager.analyze_emotion(request.message)
                context_analysis = ai_manager.analyze_conversation_context(
                    request.message
                )
                ai_analysis = {
                    "emotion_analysis": emotion_analysis,
                    "context_analysis": context_analysis,
                }
            except Exception as e:
                print(f"AI 분석 실패: {e}")

        # 키워드 매칭 (기본 분석)
        keywords = [request.message.lower()]

        # 동적 응답 생성
        response = generate_specialized_phd_response(
            agent_info, request.message, keywords, ai_analysis
        )

        return {
            "success": True,
            "response": response,
            "agent": agent_info["name"],
            "ai_enabled": AI_ENABLED,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.get("/agents")
async def get_agents():
    """에이전트 목록 조회"""
    return {"agents": AGENTS, "ai_enabled": AI_ENABLED}


@app.get("/ai_status")
async def ai_status():
    """AI 시스템 상태 확인"""
    status: Dict[str, Any] = {"ai_enabled": AI_ENABLED}
    if AI_ENABLED:
        try:
            # AI 모델 상태 확인
            test_emotion = ai_manager.analyze_emotion("테스트")
            status["emotion_analysis"] = "작동중"
            status["models_loaded"] = True
        except Exception as e:
            status["error"] = str(e)
            status["models_loaded"] = False

    return status


# 정적 파일 서빙
app.mount("/", StaticFiles(directory=".", html=True), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index():
    """메인 페이지"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html 파일을 찾을 수 없습니다.</h1>")


if __name__ == "__main__":
    print("🚀 하이퍼 박사급 도깨비 전문가 시스템 시작...")
    print(f"AI 시스템 상태: {'✅ 활성화' if AI_ENABLED else '❌ 비활성화'}")
    print("서버 주소: http://localhost:8003")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8003)
