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

# 개선된 16명 전문가 AI 시스템 임포트
try:
    from complete_16_experts_improved import RealAIManager

    real_ai_manager = RealAIManager()
    AI_ENABLED = True
    print("🎉 개선된 16명 박사급 전문가 시스템이 활성화되었습니다!")
    print("💡 도메인 특화 응답 시스템 - 정확도 향상!")
    print("� AI/투자/상담/창작/데이터/운세/성장/HR/마케팅/의료/영업/SEO/쇼핑/창업/웰니스/글쓰기")
except ImportError as e:
    print(f"⚠️ 전문가 시스템을 불러올 수 없습니다: {e}")
    real_ai_manager = None
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
    "assistant": {"name": "인공지능박사 하이도깨비", "emoji": "🤖"},
    "builder": {"name": "경제학박사 부자도깨비", "emoji": "💰"},
    "counselor": {"name": "상담심리박사 상담도깨비", "emoji": "💬"},
    "creative": {"name": "예술학박사 창작도깨비", "emoji": "🎨"},
    "data_analyst": {"name": "데이터과학박사 분석도깨비", "emoji": "📊"},
    "fortune": {"name": "마케팅박사 마케팅도깨비", "emoji": "�"},
    "growth": {"name": "교육학박사 가르도깨비", "emoji": "�"},
    "hr": {"name": "인사관리박사 인재도깨비", "emoji": "👥"},
    "marketing": {"name": "경영학박사 세일도깨비", "emoji": "💼"},
    "medical": {"name": "의학박사 의료도깨비", "emoji": "🏥"},
    "sales": {"name": "영업학박사 세일도깨비", "emoji": "💰"},
    "seo": {"name": "컨설팅박사 조언도깨비", "emoji": "🔍"},
    "shopping": {"name": "쇼핑박사 구매도깨비", "emoji": "🛒"},
    "startup": {"name": "창업학박사 스타트도깨비", "emoji": "�"},
    "village_chief": {"name": "웰니스박사 건강도깨비", "emoji": "🌿"},
    "writing": {"name": "문학박사 글쓰기도깨비", "emoji": "✍️"},
}


def generate_specialized_phd_response(
    agent: Dict[str, Any],
    message: str,
    keyword_matches: list,
    ai_analysis: Optional[Dict[str, Any]] = None,
) -> str:
    """실제 AI 모델을 활용한 전문가 응답 생성"""
    agent_name = agent["name"]
    agent_emoji = agent.get("emoji", "🧙‍♂️")
    agent_type = None

    # 에이전트 타입 추출
    for key, value in AGENTS.items():
        if value["name"] == agent_name:
            agent_type = key
            break

    # 실제 AI 모델을 통한 전문가 응답 생성
    if AI_ENABLED and real_ai_manager is not None:
        try:
            # 개선된 AI 모델을 통한 전문가 응답
            expert_response = real_ai_manager.generate_expert_response(
                message, agent_type or "assistant"
            )
            return expert_response
        except Exception as e:
            print(f"실제 AI 연동 오류: {e}")
            return f"{agent_emoji} **{agent_name}**: 현재 AI 연결이 원활하지 않습니다. 잠시 후 다시 시도해주세요."
    else:
        return f"{agent_emoji} **{agent_name}**: AI 시스템이 비활성화되어 있습니다. 관리자에게 문의해주세요."


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """채팅 엔드포인트 (완전 동적 AI 분석)"""
    try:
        agent_info = AGENTS.get(request.agent_type)
        if not agent_info:
            raise HTTPException(status_code=400, detail="잘못된 에이전트 타입입니다.")

        # 실제 AI 분석 수행 (활성화된 경우)
        ai_analysis = None
        if AI_ENABLED and real_ai_manager is not None:
            try:
                emotion_analysis = real_ai_manager.analyze_emotion(request.message)
                context_analysis = real_ai_manager.analyze_conversation_context(
                    [request.message]  # 리스트로 변환
                )
                ai_analysis = {
                    "emotion_analysis": emotion_analysis,
                    "context_analysis": context_analysis,
                }
            except Exception as e:
                print(f"AI 분석 실패: {e}")

        # 키워드 매칭 (기본 분석)
        keywords = [request.message.lower()]

        # 실제 AI 모델을 통한 전문가 응답 생성
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
    """실제 AI 시스템 상태 확인"""
    status: Dict[str, Any] = {"ai_enabled": AI_ENABLED}
    if AI_ENABLED and real_ai_manager is not None:
        try:
            # 실제 AI 모델 상태 확인
            test_emotion = real_ai_manager.analyze_emotion("테스트")
            status["emotion_analysis"] = "작동중"
            status["models_loaded"] = True
            status["ai_type"] = "실제 AI 모델 (GPT/Claude/HuggingFace)"

            # API 키 상태 확인
            api_keys = real_ai_manager.api_keys
            status["available_apis"] = []
            if api_keys.get("openai"):
                status["available_apis"].append("OpenAI GPT")
            if api_keys.get("claude"):
                status["available_apis"].append("Claude")
            if api_keys.get("huggingface"):
                status["available_apis"].append("HuggingFace")

            if not status["available_apis"]:
                status["available_apis"] = ["Fallback 모드 (API 키 없음)"]

        except Exception as e:
            status["error"] = str(e)
            status["models_loaded"] = False

    return status


@app.get("/", response_class=HTMLResponse)
async def read_index():
    """메인 페이지"""
    try:
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(current_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html 파일을 찾을 수 없습니다.</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>오류 발생: {str(e)}</h1>")


@app.get("/test", response_class=HTMLResponse)
async def read_test():
    """자동 테스트 페이지"""
    try:
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(current_dir, "auto_test.html")
        with open(test_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>auto_test.html 파일을 찾을 수 없습니다.</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>테스트 페이지 오류: {str(e)}</h1>")


# 파비콘 엔드포인트 추가
@app.get("/favicon.ico")
async def favicon():
    """파비콘 처리"""
    return {"message": "No favicon"}


if __name__ == "__main__":
    print("🚀 하이퍼 박사급 도깨비 전문가 시스템 시작...")
    print(f"AI 시스템 상태: {'✅ 활성화' if AI_ENABLED else '❌ 비활성화'}")
    print("서버 주소: http://localhost:8005")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8005)
