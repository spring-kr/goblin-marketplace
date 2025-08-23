from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import os
import sys
import random
import time
from datetime import datetime
from typing import Dict, Any, Optional

# AI 모델 시스템 임포트
try:
    from ai_model_loader import get_ai_manager, analyze_text_with_ai

    AI_ENABLED = True
    print("🤖 AI 모델 시스템이 로드되었습니다!")
except Exception as e:
    print(f"⚠️ AI 모델 로드 실패: {e}")
    AI_ENABLED = False

app = FastAPI(title="도깨비마을장터 API", description="16명의 박사급 AI 전문가 시스템")

# 정적 파일 서빙 (HTML, CSS, JS)
current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=current_dir), name="static")


# 요청 모델
class ChatRequest(BaseModel):
    agent_type: str
    me    elif agent_type == "financial":
        # 동적 AI 기반 금융 분석
        try:
            # AI 모델 매니저 직접 생성
            from ai_model_loader import ai_manager as global_ai_manager
            smart_response = global_ai_manager.generate_smart_response(message, "financial")
            return smart_response
        except Exception as e:
            print(f"AI 금융 분석 오류: {e}")
            return f"💰 **경제학박사급 전문가**: 현재 시장 분석 시스템을 점검 중입니다. 잠시 후 다시 문의해주세요."
# 실제 16명의 박사급 도깨비 정보 (완성된박사급에이전트생성기 기반)
AGENTS = {
    "medical": {
        "name": "의료 박사급 도깨비",
        "emoji": "🏥",
        "description": "의학박사급 전문가 - 건강관리, 응급처치, 예방의학, 생활습관, 의료정보 76가지 기능 분석",
        "specialty": "의료, 건강, 질병 진단, 예방의학, 응급처치",
        "personality": "신뢰할 수 있는, 정확한, 케어하는, 의학적 근거 기반",
        "expertise": [
            "건강관리",
            "응급처치",
            "예방의학",
            "생활습관",
            "의료정보",
            "질병예측",
            "건강검진",
            "임상의학",
            "공중보건",
            "스포츠의학",
        ],
        "keywords": [
            "건강",
            "의료",
            "병원",
            "치료",
            "예방",
            "응급",
            "질병",
            "검진",
            "증상",
            "건강관리",
        ],
        "phd_specialization": "의학박사 • 임상의학 • 예방의학 • 76가지 의료 기능 분석 전문가",
    },
    "financial": {
        "name": "금융 박사급 도깨비",
        "emoji": "💰",
        "description": "경제학박사급 전문가 - 투자분석, 리스크관리, 재무설계, 경제분석",
        "specialty": "금융, 투자, 경제 분석, 재무 계획",
        "personality": "논리적이고 분석적인, 데이터 기반 의사결정",
        "expertise": [
            "투자분석",
            "리스크관리",
            "재무설계",
            "경제분석",
            "자산관리",
            "금융상품",
            "세금최적화",
            "포트폴리오",
            "금융공학",
            "계량분석",
        ],
        "keywords": [
            "투자",
            "금융",
            "경제",
            "재무",
            "자산",
            "수익",
            "리스크",
            "포트폴리오",
            "주식",
            "채권",
        ],
        "phd_specialization": "경제학박사 • 금융공학 • 투자전략 • 리스크관리 전문가",
    },
    "legal": {
        "name": "법무 박사급 도깨비",
        "emoji": "⚖️",
        "description": "법학박사급 전문가 - 법률자문, 계약서검토, 소송대리, 법적분석",
        "specialty": "법률, 계약, 분쟁 해결, 법적 자문",
        "personality": "엄격하고 정확한, 법적 근거 중심",
        "expertise": [
            "법률자문",
            "계약서검토",
            "소송대리",
            "법적분석",
            "규제준수",
            "지적재산권",
            "기업법무",
            "민사법",
            "상법",
            "행정법",
        ],
        "keywords": [
            "법률",
            "계약",
            "소송",
            "법적",
            "권리",
            "의무",
            "규제",
            "컴플라이언스",
            "변호사",
            "판례",
        ],
        "phd_specialization": "법학박사 • 변호사 • 법무전문가 • 계약 및 분쟁해결 전문가",
    },
    "tech": {
        "name": "개발 박사급 도깨비",
        "emoji": "💻",
        "description": "컴퓨터공학박사급 전문가 - 풀스택개발, AI구현, 시스템설계, 아키텍처",
        "specialty": "개발, 프로그래밍, AI, 시스템 설계",
        "personality": "논리적이고 체계적인, 문제해결 중심",
        "expertise": [
            "풀스택개발",
            "AI구현",
            "시스템설계",
            "아키텍처",
            "데이터베이스",
            "클라우드",
            "보안",
            "알고리즘",
            "소프트웨어공학",
            "DevOps",
        ],
        "keywords": [
            "개발",
            "코딩",
            "프로그래밍",
            "AI",
            "시스템",
            "데이터베이스",
            "클라우드",
            "알고리즘",
            "소프트웨어",
            "앱",
        ],
        "phd_specialization": "컴퓨터공학박사 • AI전문가 • 시스템설계 • 소프트웨어 아키텍처 전문가",
    },
    "creative": {
        "name": "창작 박사급 도깨비",
        "emoji": "🎨",
        "description": "예술학박사급 전문가 - 디자인, 창작, 콘텐츠기획, 브랜딩",
        "specialty": "창작, 디자인, 예술, 콘텐츠",
        "personality": "창의적이고 예술적인, 영감을 주는",
        "expertise": [
            "디자인",
            "창작",
            "콘텐츠기획",
            "브랜딩",
            "UI/UX",
            "그래픽디자인",
            "영상제작",
            "일러스트",
            "웹디자인",
            "아트디렉션",
        ],
        "keywords": [
            "디자인",
            "창작",
            "예술",
            "콘텐츠",
            "브랜딩",
            "크리에이티브",
            "영상",
            "그래픽",
            "아트",
            "시각",
        ],
        "phd_specialization": "예술학박사 • 크리에이티브디렉터 • 콘텐츠기획 • 브랜드 디자인 전문가",
    },
    "marketing": {
        "name": "마케팅 박사급 도깨비",
        "emoji": "📢",
        "description": "마케팅박사급 전문가 - 디지털마케팅, 브랜드전략, 소셜미디어, 성과분석",
        "specialty": "마케팅, 브랜딩, 광고, 소셜미디어",
        "personality": "창의적이고 전략적인, 트렌드에 민감한",
        "expertise": [
            "디지털마케팅",
            "브랜드전략",
            "소셜미디어",
            "성과분석",
            "콘텐츠마케팅",
            "광고운영",
            "고객분석",
            "SEO",
            "퍼포먼스마케팅",
            "인플루언서",
        ],
        "keywords": [
            "마케팅",
            "브랜딩",
            "광고",
            "소셜",
            "콘텐츠",
            "캠페인",
            "홍보",
            "SNS",
            "브랜드",
            "고객",
        ],
        "phd_specialization": "마케팅박사 • 디지털전략 • 브랜드관리 • 소비자행동 분석 전문가",
    },
    "education": {
        "name": "교육 박사급 도깨비",
        "emoji": "🎓",
        "description": "교육학박사급 전문가 - 학습설계, 진로상담, 교육방법론, 평가시스템",
        "specialty": "교육, 학습, 진로, 상담",
        "personality": "인내심 있고 격려하는, 성장 지향적",
        "expertise": [
            "학습설계",
            "진로상담",
            "교육방법론",
            "평가시스템",
            "학습심리",
            "교육과정",
            "멘토링",
            "교수법",
            "교육공학",
            "평생교육",
        ],
        "keywords": [
            "교육",
            "학습",
            "진로",
            "상담",
            "멘토링",
            "성장",
            "발전",
            "공부",
            "교육과정",
            "평가",
        ],
        "phd_specialization": "교육학박사 • 학습심리 • 진로상담 • 교육방법론 전문가",
    },
    "hr": {
        "name": "인사 박사급 도깨비",
        "emoji": "👥",
        "description": "경영학박사급 전문가 - 인재채용, 조직관리, 성과평가, 교육훈련",
        "specialty": "인사, 조직, 채용, 평가",
        "personality": "체계적이고 공정한, 사람 중심적",
        "expertise": [
            "인재채용",
            "조직관리",
            "성과평가",
            "교육훈련",
            "노무관리",
            "조직문화",
            "리더십개발",
            "인사제도",
            "조직심리",
            "인적자원",
        ],
        "keywords": [
            "인사",
            "채용",
            "조직",
            "평가",
            "교육",
            "리더십",
            "문화",
            "HR",
            "인재",
            "성과",
        ],
        "phd_specialization": "경영학박사 • HR전문가 • 조직심리 • 인재개발 전문가",
    },
    "sales": {
        "name": "영업 박사급 도깨비",
        "emoji": "💼",
        "description": "경영학박사급 전문가 - 영업전략, 고객관리, 협상기술, 성과관리",
        "specialty": "영업, 세일즈, 고객, 협상",
        "personality": "적극적이고 설득력 있는, 관계 중심적",
        "expertise": [
            "영업전략",
            "고객관리",
            "협상기술",
            "성과관리",
            "고객발굴",
            "관계구축",
            "세일즈프로세스",
            "B2B영업",
            "CRM",
            "영업심리학",
        ],
        "keywords": [
            "영업",
            "세일즈",
            "고객",
            "협상",
            "매출",
            "관계",
            "성과",
            "판매",
            "계약",
            "클라이언트",
        ],
        "phd_specialization": "경영학박사 • 영업전략 • CRM전문가 • 협상 및 관계구축 전문가",
    },
    "research": {
        "name": "연구 박사급 도깨비",
        "emoji": "🔬",
        "description": "연구박사급 전문가 - 학술연구, 논문작성, 데이터분석, 연구방법론",
        "specialty": "연구, 논문, 학술, 분석",
        "personality": "논리적이고 체계적인, 학술적 엄밀성",
        "expertise": [
            "학술연구",
            "논문작성",
            "데이터분석",
            "연구방법론",
            "통계분석",
            "문헌조사",
            "실험설계",
            "질적연구",
            "양적연구",
            "메타분석",
        ],
        "keywords": [
            "연구",
            "논문",
            "학술",
            "분석",
            "데이터",
            "실험",
            "조사",
            "통계",
            "방법론",
            "문헌",
        ],
        "phd_specialization": "연구박사 • 논문전문가 • 학술연구 • 연구방법론 전문가",
    },
    "translation": {
        "name": "번역 박사급 도깨비",
        "emoji": "🌍",
        "description": "언어학박사급 전문가 - 다국어번역, 문서현지화, 통역, 언어분석",
        "specialty": "번역, 언어, 통역, 현지화",
        "personality": "정확하고 문화적 감수성이 높은",
        "expertise": [
            "다국어번역",
            "문서현지화",
            "통역",
            "언어분석",
            "문화적응",
            "전문번역",
            "언어교육",
            "번역기술",
            "국제화",
            "다문화",
        ],
        "keywords": [
            "번역",
            "언어",
            "통역",
            "현지화",
            "다국어",
            "문화",
            "글로벌",
            "영어",
            "외국어",
            "국제",
        ],
        "phd_specialization": "언어학박사 • 통번역 • 다문화전문가 • 언어 및 문화 분석 전문가",
    },
    "consulting": {
        "name": "컨설팅 박사급 도깨비",
        "emoji": "🎯",
        "description": "경영학박사급 전문가 - 경영컨설팅, 전략기획, 프로세스개선, 변화관리",
        "specialty": "컨설팅, 전략, 경영, 개선",
        "personality": "분석적이고 통찰력 있는, 해결책 제시형",
        "expertise": [
            "경영컨설팅",
            "전략기획",
            "프로세스개선",
            "변화관리",
            "조직진단",
            "비즈니스모델",
            "성과관리",
            "혁신전략",
            "디지털전환",
            "경영분석",
        ],
        "keywords": [
            "컨설팅",
            "전략",
            "경영",
            "개선",
            "프로세스",
            "조직",
            "성과",
            "혁신",
            "분석",
            "진단",
        ],
        "phd_specialization": "경영학박사 • 전략기획 • 비즈니스컨설팅 • 조직변화 전문가",
    },
    "psychology": {
        "name": "심리학 박사급 도깨비",
        "emoji": "🧠",
        "description": "심리학박사급 전문가 - 심리상담, 정신건강, 행동분석, 인지치료",
        "specialty": "심리, 정신건강, 상담, 치료",
        "personality": "공감적이고 따뜻한, 전문적 상담",
        "expertise": [
            "심리상담",
            "정신건강",
            "행동분석",
            "인지치료",
            "스트레스관리",
            "감정조절",
            "관계상담",
            "심리검사",
            "트라우마",
            "우울증",
        ],
        "keywords": [
            "심리",
            "정신",
            "상담",
            "치료",
            "스트레스",
            "감정",
            "관계",
            "우울",
            "불안",
            "트라우마",
        ],
        "phd_specialization": "심리학박사 • 임상심리사 • 상담전문가 • 정신건강 전문가",
    },
    "data": {
        "name": "데이터 박사급 도깨비",
        "emoji": "📊",
        "description": "통계학박사급 전문가 - 빅데이터분석, 통계모델링, AI분석, 데이터시각화",
        "specialty": "데이터, 통계, 분석, AI",
        "personality": "논리적이고 분석적인, 데이터 기반 의사결정",
        "expertise": [
            "빅데이터분석",
            "통계모델링",
            "AI분석",
            "데이터시각화",
            "머신러닝",
            "예측모델링",
            "비즈니스인텔리전스",
            "데이터마이닝",
            "통계학",
            "파이썬",
        ],
        "keywords": [
            "데이터",
            "통계",
            "분석",
            "AI",
            "머신러닝",
            "예측",
            "시각화",
            "빅데이터",
            "모델링",
            "파이썬",
        ],
        "phd_specialization": "통계학박사 • 데이터사이언스 • AI분석 • 빅데이터 전문가",
    },
    "startup": {
        "name": "스타트업 박사급 도깨비",
        "emoji": "🚀",
        "description": "창업학박사급 전문가 - 사업계획, 투자유치, 스케일업, 혁신전략",
        "specialty": "창업, 스타트업, 투자, 혁신",
        "personality": "도전적이고 혁신적인, 비전 제시형",
        "expertise": [
            "사업계획",
            "투자유치",
            "스케일업",
            "혁신전략",
            "린스타트업",
            "비즈니스모델",
            "팀빌딩",
            "벤처투자",
            "액셀러레이션",
            "기업가정신",
        ],
        "keywords": [
            "창업",
            "스타트업",
            "투자",
            "혁신",
            "사업",
            "성장",
            "스케일업",
            "벤처",
            "기업가",
            "비즈니스모델",
        ],
        "phd_specialization": "창업학박사 • 벤처투자 • 혁신전략 • 기업가정신 전문가",
    },
    "wellness": {
        "name": "웰니스 박사급 도깨비",
        "emoji": "🌿",
        "description": "웰니스박사급 전문가 - 건강관리, 라이프스타일, 정신건강, 웰빙코칭",
        "specialty": "웰니스, 건강, 라이프스타일, 웰빙",
        "personality": "케어하는, 균형적인, 전인적 접근",
        "expertise": [
            "건강관리",
            "라이프스타일",
            "정신건강",
            "웰빙코칭",
            "스트레스관리",
            "영양관리",
            "운동처방",
            "명상",
            "요가",
            "자연치유",
        ],
        "keywords": [
            "웰니스",
            "건강",
            "라이프스타일",
            "웰빙",
            "스트레스",
            "영양",
            "운동",
            "명상",
            "힐링",
            "자연",
        ],
        "phd_specialization": "웰니스박사 • 건강관리 • 라이프스타일 코칭 • 전인적 건강 전문가",
    },
}


@app.get("/", response_class=HTMLResponse)
async def home():
    """메인 페이지 반환"""
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "agents": len(AGENTS),
        "system": "PhD-level Expert System",
    }


@app.get("/agents")
async def get_agents():
    """모든 에이전트 정보 반환"""
    return {"agents": AGENTS}


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """특정 에이전트 정보 반환"""
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": AGENTS[agent_id]}


@app.post("/analyze_emotion")
async def analyze_emotion(request: dict):
    """AI 감정분석 엔드포인트"""
    if not AI_ENABLED:
        raise HTTPException(status_code=503, detail="AI 모델이 로드되지 않았습니다")

    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="텍스트가 필요합니다")

    try:
        manager = get_ai_manager()
        emotion_result = manager.analyze_emotion(text)
        context_result = manager.analyze_conversation_context(text)

        return {
            "text": text,
            "emotion_analysis": emotion_result,
            "context_analysis": context_result,
            "ai_enabled": AI_ENABLED,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 오류: {str(e)}")


@app.post("/smart_response")
async def smart_response(request: dict):
    """AI 스마트 응답 생성 엔드포인트"""
    if not AI_ENABLED:
        raise HTTPException(status_code=503, detail="AI 모델이 로드되지 않았습니다")

    text = request.get("text", "")
    agent_type = request.get("agent_type", "general")

    if not text:
        raise HTTPException(status_code=400, detail="텍스트가 필요합니다")

    try:
        manager = get_ai_manager()
        smart_response = manager.generate_smart_response(text, agent_type)
        analysis = analyze_text_with_ai(text, agent_type)

        return {
            "text": text,
            "agent_type": agent_type,
            "smart_response": smart_response,
            "full_analysis": analysis,
            "ai_enabled": AI_ENABLED,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"응답 생성 오류: {str(e)}")


@app.get("/ai_status")
async def ai_status():
    """AI 모델 상태 확인"""
    if AI_ENABLED:
        try:
            manager = get_ai_manager()
            loaded_models = (
                list(manager.loaded_models.keys())
                if hasattr(manager, "loaded_models")
                else []
            )
            return {
                "ai_enabled": True,
                "loaded_models": loaded_models,
                "model_count": len(loaded_models),
                "status": "active",
            }
        except Exception as e:
            return {"ai_enabled": False, "error": str(e), "status": "error"}
    else:
        return {"ai_enabled": False, "status": "disabled"}


@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """실제 박사급 에이전트와 채팅 (AI 모델 통합)"""
    if request.agent_type not in AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = AGENTS[request.agent_type]

    # AI 분석 수행
    ai_analysis = None
    if AI_ENABLED:
        try:
            ai_analysis = analyze_text_with_ai(request.message, request.agent_type)
        except Exception as e:
            print(f"AI 분석 오류: {e}")

    # 박사급 전문가 응답 생성 (AI 분석 정보 포함)
    response = generate_phd_expert_response(agent, request.message, ai_analysis)

    # 대화 ID 생성 (세션 관리용)
    conversation_id = f"conv_{int(time.time())}_{random.randint(1000, 9999)}"

    return {
        "agent_name": agent["name"],
        "agent_emoji": agent["emoji"],
        "response": response,
        "conversation_id": conversation_id,
        "agent_specialty": agent["specialty"],
        "phd_specialization": agent["phd_specialization"],
        "timestamp": datetime.now().isoformat(),
        "ai_analysis": ai_analysis,  # AI 분석 결과 추가
        "ai_enabled": AI_ENABLED,
    }


def generate_phd_expert_response(
    agent: Dict[str, Any], message: str, ai_analysis: Optional[Dict[str, Any]] = None
) -> str:
    """실제 박사급 전문가 응답 생성 (AI 분석 통합)"""
    agent_name = agent["name"]
    agent_emoji = agent.get("emoji", "🧙‍♂️")
    specialty = agent["specialty"]
    expertise = agent.get("expertise", [])
    phd_spec = agent.get("phd_specialization", "박사급 전문가")
    keywords = agent.get("keywords", [])

    # AI 분석 정보 추출
    emotion_info = ""
    context_info = ""
    if ai_analysis and AI_ENABLED:
        emotion_analysis = ai_analysis.get("emotion_analysis", {})
        context_analysis = ai_analysis.get("context_analysis", {})

        if emotion_analysis.get("emotion"):
            emotion_info = f"[감정분석: {emotion_analysis['emotion']}] "

        if context_analysis.get("conversation_type"):
            context_info = f"[대화유형: {context_analysis['conversation_type']}] "

    # 메시지 키워드 분석
    message_lower = message.lower()
    keyword_matches = [kw for kw in keywords if kw in message_lower]

    # 인사말 처리
    if any(greeting in message_lower for greeting in ["안녕", "hello", "hi", "헬로"]):
        base_response = f"""
{agent_emoji} **안녕하세요! {agent_name}입니다.**

🎓 **박사급 전문성**: {phd_spec}
📚 **핵심 역량**: {', '.join(expertise[:6])}
🎯 **전문 분야**: {specialty}

{agent_name}로서 박사급 전문 지식과 실무 경험을 바탕으로 최고 수준의 상담과 솔루션을 제공해드립니다.

**어떤 것이 궁금하신가요?**
• 구체적인 질문이나 상황을 말씀해주시면 전문적인 분석을 제공해드립니다
• {specialty} 분야의 최신 동향과 실무 노하우를 공유할 수 있습니다
• 단계별 실행 방안과 맞춤형 솔루션을 설계해드립니다
"""

        # AI 분석 정보가 있으면 추가
        if ai_analysis and AI_ENABLED:
            ai_info = f"\n🤖 **AI 분석**: {emotion_info}{context_info}친근한 대화를 시작해주셔서 감사합니다!"
            base_response += ai_info

        return base_response

    # 감사 인사 처리
    elif any(
        thanks in message_lower for thanks in ["감사", "고마워", "thank", "thanks"]
    ):
        base_response = f"""
{agent_emoji} **감사합니다!** 

{agent_name}로서 도움이 되어 정말 기쁩니다! 🎉

🎓 **지속적 지원**: 박사급 전문성을 바탕으로 언제든 추가적인 도움을 제공할 준비가 되어 있습니다.

📈 **향후 지원 계획**:
• {specialty} 분야의 최신 연구 동향 업데이트
• 맞춤형 심화 분석 및 컨설팅
• 장기적 관점에서의 전략적 조언

더 궁금한 점이나 새로운 주제가 있으시면 언제든 말씀해주세요!
"""

        # AI 분석 정보가 있으면 추가
        if ai_analysis and AI_ENABLED:
            ai_info = f"\n🤖 **AI 분석**: {emotion_info}{context_info}감사의 마음이 잘 전달되었습니다!"
            base_response += ai_info

        return base_response

    # 전문 분야별 심화 응답
    else:
        return generate_specialized_phd_response(
            agent, message, keyword_matches, ai_analysis
        )


def generate_specialized_phd_response(
    agent: Dict[str, Any],
    message: str,
    keyword_matches: list,
    ai_analysis: Optional[Dict[str, Any]] = None,
) -> str:
    """전문 분야별 박사급 응답 생성 (AI 분석 통합)"""
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
            emotion_info = f"[감정: {emotion_analysis['emotion']}] "

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

    if agent_type == "medical":
        medical_response = f"""{base_response}
{ai_info_section}
🏥 **의학박사급 전문 분석**: '{message}'

**📋 종합 의료 접근법**:
• **76가지 의료 기능 활용**: 증상 분석, 진단 보조, 예방의학적 접근
• **임상의학 관점**: 최신 의학 연구와 임상 데이터 기반 분석
• **예방의학 전략**: 근본 원인 파악 및 예방 중심 솔루션
• **개인맞춤 건강관리**: 생활습관, 체질, 환경 요인 종합 고려"""

        # AI 감정분석 기반 의료 조언 추가
        if ai_analysis and AI_ENABLED:
            emotion = ai_analysis.get("emotion_analysis", {}).get("emotion", "")
            urgency = ai_analysis.get("context_analysis", {}).get("urgency_level", "")

            if emotion == "부정" or urgency == "높음":
                medical_response += """

🚨 **AI 감정분석 기반 특별 권고**:
• 스트레스나 불안이 건강에 미치는 영향 고려 필요
• 정신건강 측면의 통합적 접근 권장
• 필요시 심리상담과 병행 치료 고려"""

            elif emotion == "긍정":
                medical_response += """

😊 **긍정적 마음가짐 활용 권고**:
• 현재의 긍정적 태도가 치유과정에 도움
• 낙관적 사고가 면역력 향상에 기여
• 규칙적인 운동과 건강한 생활습관 유지 권장"""

        medical_response += """

**💡 전문가 권고사항**:
1. **정확한 진단을 위한 추가 정보**: 구체적 증상, 발생 시기, 지속 기간
2. **예방의학적 접근**: 근본 원인 해결을 위한 생활습관 개선
3. **단계별 관리 계획**: 단기/중기/장기 건강관리 로드맵

⚠️ **중요**: 응급상황이나 심각한 증상 시 즉시 의료기관 방문 필요
"""
        return medical_response

    elif agent_type == "financial":
        # 동적 AI 기반 금융 분석
        try:
            # AI 모델 매니저 직접 생성
            from ai_model_loader import ai_manager as global_ai_manager
            smart_response = global_ai_manager.generate_smart_response(message, "financial")
            return smart_response
        except Exception as e:
            print(f"AI 금융 분석 오류: {e}")
            return f"💰 **경제학박사급 전문가**: 현재 시장 분석 시스템을 점검 중입니다. 잠시 후 다시 문의해주세요."
            smart_response = ai_manager.generate_smart_response(user_message, "financial")
            return smart_response
        except Exception as e:
            logger.error(f"AI 금융 분석 오류: {e}")
            return f"� **경제학박사급 전문가**: 현재 시장 분석 시스템을 점검 중입니다. 잠시 후 다시 문의해주세요."

    elif agent_type == "legal":
        return f"""{base_response}

⚖️ **법학박사급 전문 분석**: '{message}'

**📖 법률 전문가 접근법**:
• **판례법 분석**: 관련 판례 및 법원 해석 동향 검토
• **법령 체계 분석**: 해당 법률의 입법 취지 및 적용 범위
• **법적 리스크 평가**: 잠재적 법적 분쟁 요소 및 대응 방안
• **실무적 해결책**: 법리적 근거와 실무 관행의 조화

**💡 법무 전문가 조언**:
1. **법적 근거 확인**: 관련 법령 및 하위 규정 검토
2. **선례 분석**: 유사 사안의 판례 및 행정해석 연구
3. **예방적 조치**: 법적 분쟁 예방을 위한 사전 대책

⚖️ **참고**: 구체적 법률 상담은 변호사와의 직접 상담 권장
"""

    elif agent_type == "tech":
        return f"""{base_response}

💻 **컴퓨터공학박사급 전문 분석**: '{message}'

**🔧 시스템 아키텍처 관점**:
• **확장성 설계**: 마이크로서비스, 클라우드 네이티브 아키텍처
• **AI/ML 통합**: 머신러닝 파이프라인 및 AI 서비스 구조
• **보안 체계**: 제로 트러스트, DevSecOps 보안 전략
• **성능 최적화**: 로드 밸런싱, 캐싱, 데이터베이스 튜닝

**💡 기술 전문가 솔루션**:
1. **기술 스택 선정**: 요구사항에 최적화된 기술 조합
2. **개발 방법론**: 애자일, DevOps 기반 개발 프로세스
3. **품질 보증**: CI/CD, 자동화 테스트, 모니터링 체계

🚀 **혁신 기술**: 최신 트렌드와 미래 기술 동향 반영
"""

    elif agent_type == "creative":
        return f"""{base_response}

🎨 **예술학박사급 전문 분석**: '{message}'

**🎭 크리에이티브 전략 접근법**:
• **예술 이론 기반**: 미학, 색채학, 구성 원리 적용
• **사용자 중심 디자인**: UX/UI 원칙과 인간공학적 접근
• **브랜드 아이덴티티**: 브랜드 철학과 시각적 일관성 구축
• **트렌드 분석**: 현재 디자인 트렌드와 미래 방향성

**💡 크리에이티브 솔루션**:
1. **컨셉 개발**: 창의적 아이디어 발굴 및 구체화
2. **시각적 구현**: 디자인 시스템 및 가이드라인 수립
3. **성과 측정**: 크리에이티브 효과성 평가 지표

🌟 **혁신 요소**: 차별화된 창의적 접근법 제시
"""

    # 기타 전문 분야들도 유사하게 처리
    else:
        return f"""{base_response}

🎯 **박사급 전문 분석**: '{message}'

**📚 학술적 접근법**:
• **이론적 기반**: 해당 분야의 핵심 이론 및 최신 연구 동향
• **실증적 분석**: 데이터와 사례 기반 검증된 방법론 적용
• **통합적 관점**: 다학제적 접근을 통한 종합적 솔루션
• **실무적 적용**: 이론과 실무의 조화로운 구현 방안

**💡 전문가 제안**:
1. **현황 진단**: 체계적 분석을 통한 핵심 이슈 파악
2. **솔루션 설계**: 단계별 실행 계획 및 성공 지표 설정
3. **지속적 개선**: 피드백 기반 최적화 및 발전 방안

더 구체적인 상황이나 세부 요구사항을 알려주시면 맞춤형 전문 솔루션을 제공해드리겠습니다.
"""


if __name__ == "__main__":
    print("🏰 도깨비마을장터 서버를 시작합니다...")
    print("📍 http://localhost:8003 에서 접속하세요!")
    print("🧙‍♂️ 실제 16명의 박사급 도깨비가 대기 중입니다!")
    print("🎓 완성된박사급에이전트생성기 시스템 기반")

    uvicorn.run(app, host="0.0.0.0", port=8003, reload=False, log_level="info")
