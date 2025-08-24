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
from typing import Dict, Any

# 16명의 박사급 도깨비 시스템 경로 추가
sys.path.append(r"D:\도깨비마을장터\완성된박사급에이전트생성기")

# 실제 박사급 에이전트 생성기 불러오기
try:
    from 완성된박사급ai에이전트생성기 import GoblinAgentGenerator
    goblin_generator = GoblinAgentGenerator()
    REAL_GOBLINS_AVAILABLE = True
    print("✅ 실제 16명의 박사급 도깨비 시스템 로드 완료!")
except ImportError as e:
    print(f"⚠️ 박사급 도깨비 시스템 로드 실패: {e}")
    REAL_GOBLINS_AVAILABLE = False

app = FastAPI(title="도깨비마을장터 API", description="16명의 박사급 AI 전문가 시스템")

# 정적 파일 서빙 (HTML, CSS, JS)
current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=current_dir), name="static")

# 요청 모델
class ChatRequest(BaseModel):
    agent_id: str
    message: str
    user_id: str = "user_001"

class ChatResponse(BaseModel):
    agent_name: str
    response: str
    emotion: str = "neutral"
    confidence: float = 0.8

# 16명의 박사급 도깨비 정보 (실제 시스템 기반)
AGENTS = {
    "medical": {
        "name": "의료 박사급 도깨비",
        "emoji": "🏥",
        "description": "의학박사급 전문가 - 건강관리, 응급처치, 예방의학, 생활습관, 의료정보 76가지 기능 분석",
        "specialty": "의료, 건강, 질병 진단, 예방의학, 응급처치",
        "personality": "신뢰할 수 있는, 정확한, 케어하는, 의학적 근거 기반",
        "expertise": ["건강관리", "응급처치", "예방의학", "생활습관", "의료정보", "질병예측", "건강검진"],
        "keywords": ["건강", "의료", "병원", "치료", "예방", "응급", "질병", "검진"]
    },
    "financial": {
        "name": "금융 박사급 도깨비", 
        "emoji": "💰",
        "description": "경제학박사급 전문가 - 투자분석, 리스크관리, 재무설계, 경제분석",
        "specialty": "금융, 투자, 경제 분석, 재무 계획",
        "personality": "논리적이고 분석적인, 데이터 기반 의사결정",
        "expertise": ["투자분석", "리스크관리", "재무설계", "경제분석", "자산관리", "금융상품", "세금최적화"],
        "keywords": ["투자", "금융", "경제", "재무", "자산", "수익", "리스크", "포트폴리오"]
    },
    "legal": {
        "name": "법무 박사급 도깨비",
        "emoji": "⚖️", 
        "description": "법학박사급 전문가 - 법률자문, 계약서검토, 소송대리, 법적분석",
        "specialty": "법률, 계약, 분쟁 해결, 법적 자문",
        "personality": "엄격하고 정확한, 법적 근거 중심",
        "expertise": ["법률자문", "계약서검토", "소송대리", "법적분석", "규제준수", "지적재산권", "기업법무"],
        "keywords": ["법률", "계약", "소송", "법적", "권리", "의무", "규제", "컴플라이언스"]
    },
    "tech": {
        "name": "개발 박사급 도깨비",
        "emoji": "💻",
        "description": "컴퓨터공학박사급 전문가 - 풀스택개발, AI구현, 시스템설계, 아키텍처",
        "specialty": "개발, 프로그래밍, AI, 시스템 설계",
        "personality": "논리적이고 체계적인, 문제해결 중심",
        "expertise": ["풀스택개발", "AI구현", "시스템설계", "아키텍처", "데이터베이스", "클라우드", "보안"],
        "keywords": ["개발", "코딩", "프로그래밍", "AI", "시스템", "데이터베이스", "클라우드"]
    },
    "creative": {
        "name": "창작 박사급 도깨비",
        "emoji": "🎨",
        "description": "예술학박사급 전문가 - 디자인, 창작, 콘텐츠기획, 브랜딩",
        "specialty": "창작, 디자인, 예술, 콘텐츠",
        "personality": "창의적이고 예술적인, 영감을 주는",
        "expertise": ["디자인", "창작", "콘텐츠기획", "브랜딩", "UI/UX", "그래픽디자인", "영상제작"],
        "keywords": ["디자인", "창작", "예술", "콘텐츠", "브랜딩", "크리에이티브", "영상"]
    },
    "marketing": {
        "name": "마케팅 박사급 도깨비",
        "emoji": "📢",
        "description": "마케팅박사급 전문가 - 디지털마케팅, 브랜드전략, 소셜미디어, 성과분석",
        "specialty": "마케팅, 브랜딩, 광고, 소셜미디어",
        "personality": "창의적이고 전략적인, 트렌드에 민감한",
        "expertise": ["디지털마케팅", "브랜드전략", "소셜미디어", "성과분석", "콘텐츠마케팅", "광고운영", "고객분석"],
        "keywords": ["마케팅", "브랜딩", "광고", "소셜", "콘텐츠", "캠페인", "홍보"]
    },
    "education": {
        "name": "교육 박사급 도깨비",
        "emoji": "🎓",
        "description": "교육학박사급 전문가 - 학습설계, 진로상담, 교육방법론, 평가시스템",
        "specialty": "교육, 학습, 진로, 상담",
        "personality": "인내심 있고 격려하는, 성장 지향적",
        "expertise": ["학습설계", "진로상담", "교육방법론", "평가시스템", "학습심리", "교육과정", "멘토링"],
        "keywords": ["교육", "학습", "진로", "상담", "멘토링", "성장", "발전"]
    },
    "hr": {
        "name": "인사 박사급 도깨비",
        "emoji": "👥",
        "description": "경영학박사급 전문가 - 인재채용, 조직관리, 성과평가, 교육훈련",
        "specialty": "인사, 조직, 채용, 평가",
        "personality": "체계적이고 공정한, 사람 중심적",
        "expertise": ["인재채용", "조직관리", "성과평가", "교육훈련", "노무관리", "조직문화", "리더십개발"],
        "keywords": ["인사", "채용", "조직", "평가", "교육", "리더십", "문화"]
    },
    "sales": {
        "name": "영업 박사급 도깨비",
        "emoji": "💼",
        "description": "경영학박사급 전문가 - 영업전략, 고객관리, 협상기술, 성과관리",
        "specialty": "영업, 세일즈, 고객, 협상",
        "personality": "적극적이고 설득력 있는, 관계 중심적",
        "expertise": ["영업전략", "고객관리", "협상기술", "성과관리", "고객발굴", "관계구축", "세일즈프로세스"],
        "keywords": ["영업", "세일즈", "고객", "협상", "매출", "관계", "성과"]
    },
    "research": {
        "name": "연구 박사급 도깨비",
        "emoji": "🔬",
        "description": "연구박사급 전문가 - 학술연구, 논문작성, 데이터분석, 연구방법론",
        "specialty": "연구, 논문, 학술, 분석",
        "personality": "논리적이고 체계적인, 학술적 엄밀성",
        "expertise": ["학술연구", "논문작성", "데이터분석", "연구방법론", "통계분석", "문헌조사", "실험설계"],
        "keywords": ["연구", "논문", "학술", "분석", "데이터", "실험", "조사"]
    },
    "translation": {
        "name": "번역 박사급 도깨비",
        "emoji": "🌍",
        "description": "언어학박사급 전문가 - 다국어번역, 문서현지화, 통역, 언어분석",
        "specialty": "번역, 언어, 통역, 현지화",
        "personality": "정확하고 문화적 감수성이 높은",
        "expertise": ["다국어번역", "문서현지화", "통역", "언어분석", "문화적응", "전문번역", "언어교육"],
        "keywords": ["번역", "언어", "통역", "현지화", "다국어", "문화", "글로벌"]
    },
    "consulting": {
        "name": "컨설팅 박사급 도깨비",
        "emoji": "🎯",
        "description": "경영학박사급 전문가 - 경영컨설팅, 전략기획, 프로세스개선, 변화관리",
        "specialty": "컨설팅, 전략, 경영, 개선",
        "personality": "분석적이고 통찰력 있는, 해결책 제시형",
        "expertise": ["경영컨설팅", "전략기획", "프로세스개선", "변화관리", "조직진단", "비즈니스모델", "성과관리"],
        "keywords": ["컨설팅", "전략", "경영", "개선", "프로세스", "조직", "성과"]
    },
    "psychology": {
        "name": "심리학 박사급 도깨비",
        "emoji": "🧠",
        "description": "심리학박사급 전문가 - 심리상담, 정신건강, 행동분석, 인지치료",
        "specialty": "심리, 정신건강, 상담, 치료",
        "personality": "공감적이고 따뜻한, 전문적 상담",
        "expertise": ["심리상담", "정신건강", "행동분석", "인지치료", "스트레스관리", "감정조절", "관계상담"],
        "keywords": ["심리", "정신", "상담", "치료", "스트레스", "감정", "관계"]
    },
    "data": {
        "name": "데이터 박사급 도깨비",
        "emoji": "📊",
        "description": "통계학박사급 전문가 - 빅데이터분석, 통계모델링, AI분석, 데이터시각화",
        "specialty": "데이터, 통계, 분석, AI",
        "personality": "논리적이고 분석적인, 데이터 기반 의사결정",
        "expertise": ["빅데이터분석", "통계모델링", "AI분석", "데이터시각화", "머신러닝", "예측모델링", "비즈니스인텔리전스"],
        "keywords": ["데이터", "통계", "분석", "AI", "머신러닝", "예측", "시각화"]
    },
    "startup": {
        "name": "스타트업 박사급 도깨비",
        "emoji": "🚀", 
        "description": "창업학박사급 전문가 - 사업계획, 투자유치, 스케일업, 혁신전략",
        "specialty": "창업, 스타트업, 투자, 혁신",
        "personality": "도전적이고 혁신적인, 비전 제시형",
        "expertise": ["사업계획", "투자유치", "스케일업", "혁신전략", "린스타트업", "비즈니스모델", "팀빌딩"],
        "keywords": ["창업", "스타트업", "투자", "혁신", "사업", "성장", "스케일업"]
    },
    "wellness": {
        "name": "웰니스 박사급 도깨비",
        "emoji": "🌿",
        "description": "웰니스박사급 전문가 - 건강관리, 라이프스타일, 정신건강, 웰빙코칭",
        "specialty": "웰니스, 건강, 라이프스타일, 웰빙",
        "personality": "케어하는, 균형적인, 전인적 접근",
        "expertise": ["건강관리", "라이프스타일", "정신건강", "웰빙코칭", "스트레스관리", "영양관리", "운동처방"],
        "keywords": ["웰니스", "건강", "라이프스타일", "웰빙", "스트레스", "영양", "운동"]
    }
}
    "creative": {
        "name": "창작 도깨비 🎨",
        "description": "스토리텔링, 디자인, 브랜딩 전문가",
        "specialty": "창작, 디자인, 예술",
        "personality": "상상력이 풍부한 창작 전문가"
    },
    "tech": {
        "name": "개발 도깨비 💻",
        "description": "풀스택개발, AI모델구현, 시스템아키텍처 전문가",
        "specialty": "개발, 프로그래밍, AI",
        "personality": "논리적이고 체계적인 개발 전문가"
    },
    "marketing": {
        "name": "마케팅 도깨비 📢",
        "description": "디지털마케팅, SNS전략, 브랜드관리 전문가",
        "specialty": "마케팅, 홍보, 브랜딩",
        "personality": "적극적이고 창의적인 마케팅 전문가"
    },
    "education": {
        "name": "교육 도깨비 🎓",
        "description": "맞춤형학습, 진로상담, 교육과정설계 전문가",
        "specialty": "교육, 학습, 진로",
        "personality": "친근하고 이해심 많은 교육 전문가"
    },
    "hr": {
        "name": "인사 도깨비 👥",
        "description": "인재채용, 성과관리, 조직문화 전문가",
        "specialty": "인사, 채용, 조직관리",
        "personality": "통찰력 있고 공정한 인사 전문가"
    },
    "sales": {
        "name": "영업 도깨비 🤝",
        "description": "영업전략, 고객관리, 협상기술 전문가",
        "specialty": "영업, 고객관리, 협상",
        "personality": "적극적이고 설득력 있는 영업 전문가"
    },
    "research": {
        "name": "연구 도깨비 🔬",
        "description": "학술연구, 논문분석, 데이터사이언스 전문가",
        "specialty": "연구, 분석, 학술",
        "personality": "꼼꼼하고 분석적인 연구 전문가"
    },
    "translation": {
        "name": "번역 도깨비 🌍",
        "description": "다국어번역, 문서현지화, 국제비즈니스 전문가",
        "specialty": "번역, 언어, 국제업무",
        "personality": "정확하고 문화적 이해가 깊은 번역 전문가"
    },
    "consulting": {
        "name": "컨설턴트 도깨비 📊",
        "description": "경영컨설팅, 전략기획, 비즈니스모델 전문가",
        "specialty": "컨설팅, 전략, 경영",
        "personality": "통찰력 있고 전략적인 컨설팅 전문가"
    },
    "psychology": {
        "name": "심리 도깨비 🧠",
        "description": "심리상담, 정신건강, 행동분석 전문가",
        "specialty": "심리, 상담, 정신건강",
        "personality": "공감능력이 뛰어난 심리 전문가"
    },
    "data": {
        "name": "데이터 도깨비 📈",
        "description": "빅데이터분석, AI모델링, 비즈니스인텔리전스 전문가",
        "specialty": "데이터, 분석, AI",
        "personality": "논리적이고 데이터 기반의 분석 전문가"
    },
    "startup": {
        "name": "창업 도깨비 🚀",
        "description": "스타트업창업, 비즈니스모델, 투자유치 전문가",
        "specialty": "창업, 스타트업, 비즈니스",
        "personality": "도전적이고 혁신적인 창업 전문가"
    },
    "wellness": {
        "name": "웰니스 도깨비 🧘",
        "description": "건강관리, 영양상담, 라이프스타일 전문가",
        "specialty": "건강, 웰니스, 라이프스타일",
        "personality": "따뜻하고 돌봄이 가득한 웰니스 전문가"
    }
}

@app.get("/", response_class=HTMLResponse)
async def home():
    """메인 페이지 반환"""
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "agents": len(AGENTS)}

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

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """박사급 에이전트와 채팅"""
    if request.agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = AGENTS[request.agent_id]
    
    # 박사급 전문가 응답 생성
    response = generate_agent_response(agent, request.message)
    
    # 대화 ID 생성 (세션 관리용)
    conversation_id = f"conv_{int(time.time())}_{random.randint(1000, 9999)}"
    
    return {
        "agent_name": agent["name"],
        "agent_emoji": agent["emoji"],
        "response": response,
        "conversation_id": conversation_id,
        "agent_specialty": agent["specialty"],
        "timestamp": datetime.now().isoformat()
    }

def generate_agent_response(agent: Dict[str, Any], message: str) -> str:
    """실제 박사급 에이전트와 연동된 응답 생성"""
    agent_name = agent["name"]
    agent_emoji = agent.get("emoji", "🧙‍♂️")
    specialty = agent["specialty"]
    expertise = agent.get("expertise", [])
    
    # 실제 박사급 시스템 사용 시도
    if REAL_GOBLINS_AVAILABLE:
        try:
            # 메시지 분석
            analysis = goblin_generator.analyze_goblin_request(message)
            
            # 박사급 전문성 기반 응답 생성
            if "안녕" in message or "hello" in message.lower():
                return f"{agent_emoji} 안녕하세요! 저는 **{agent_name}**입니다.\n\n🎓 **전문 분야**: {specialty}\n📚 **핵심 역량**: {', '.join(expertise[:5])}\n\n박사급 전문 지식을 바탕으로 최고 수준의 상담과 솔루션을 제공해드립니다. 어떤 것이 궁금하신가요?"
            
            elif "도움" in message or "help" in message.lower():
                return f"{agent_emoji} 물론입니다! **{agent_name}**로서 최선을 다해 도와드리겠습니다.\n\n🔍 **분석 접근법**:\n• 현황 파악 및 문제 정의\n• 전문 이론 기반 해결책 설계\n• 단계별 실행 방안 제시\n• 성과 측정 및 지속적 개선\n\n구체적으로 어떤 부분에서 도움이 필요하신지 자세히 말씀해주세요!"
            
            elif "감사" in message or "thank" in message.lower():
                return f"{agent_emoji} 감사합니다! **{agent_name}**로서 도움이 되어 정말 기쁩니다.\n\n박사급 전문성을 통해 더 나은 솔루션을 지속적으로 제공하겠습니다. 언제든 추가 질문이 있으시면 말씀해주세요!\n\n🎯 **지속 지원**: {specialty} 분야의 최신 동향과 전문 지식을 계속 업데이트하며 서비스하겠습니다."
            
            else:
                # 전문 분야별 박사급 맞춤 응답
                return generate_expert_response_by_field(agent, message, analysis)
                
        except Exception as e:
            print(f"박사급 시스템 연동 오류: {e}")
    
    # 기본 응답 (폴백)
    if "안녕" in message or "hello" in message.lower():
        return f"{agent_emoji} 안녕하세요! 저는 **{agent_name}**입니다. {specialty} 분야의 전문가로서 도움을 드리겠습니다! 어떤 것이 궁금하신가요?"
    
    elif "도움" in message or "help" in message.lower():
        return f"{agent_emoji} 물론입니다! 저는 {specialty} 전문가입니다. 구체적으로 어떤 부분에서 도움이 필요하신지 말씀해주세요."
    
    elif "감사" in message or "thank" in message.lower():
        return f"{agent_emoji} 천만에요! **{agent_name}**로서 도움이 되어 기쁩니다. 언제든 {specialty} 관련해서 더 궁금한 것이 있으시면 말씀해주세요!"
    
    else:
        return generate_basic_expert_response(agent, message)

def generate_expert_response_by_field(agent: Dict[str, Any], message: str, analysis: Dict[str, Any]) -> str:
    """전문 분야별 박사급 응답 생성"""
    agent_name = agent["name"]
    agent_emoji = agent.get("emoji", "🧙‍♂️")
    
    # 의료 분야
    if "의료" in agent_name:
        return f"""{agent_emoji} **의료 박사급 전문가**로서 '{message}'에 대해 분석해드리겠습니다.

🏥 **전문 의료 분석**:
• 76가지 의료 기능을 활용한 종합 진단
• 예방의학 관점에서의 체계적 접근
• 최신 의학 연구 기반 권고사항
• 개인맞춤형 건강 관리 방안

💡 **권고사항**: 정확한 진단을 위해 구체적인 증상, 기간, 기존 병력 등을 알려주시면 더 정밀한 의료 자문을 제공해드릴 수 있습니다.

⚠️ **중요**: 응급상황이거나 심각한 증상이 있으시면 즉시 의료기관을 방문하시기 바랍니다."""
    
    # 금융 분야
    elif "금융" in agent_name:
        return f"""{agent_emoji} **금융 박사급 전문가**로서 '{message}'에 대해 분석해드리겠습니다.

💰 **전문 금융 분석**:
• 포트폴리오 이론 기반 리스크 분석
• 경제학적 관점에서의 투자 전략
• 데이터 기반 시장 분석 및 예측
• 개인 재무상황 맞춤형 설계

📊 **분석 요소**: 투자 목표, 리스크 성향, 투자 기간, 현재 자산 상황 등을 종합적으로 고려하여 최적의 금융 솔루션을 제시하겠습니다."""
    
    # 기술 분야
    elif "개발" in agent_name or "기술" in agent_name:
        return f"""{agent_emoji} **기술 박사급 전문가**로서 '{message}'에 대해 분석해드리겠습니다.

💻 **전문 기술 분석**:
• 시스템 아키텍처 설계 관점
• AI 및 최신 기술 트렌드 적용
• 확장성과 보안을 고려한 솔루션
• 성능 최적화 및 유지보수성

🔧 **기술 접근법**: 현재 기술 스택, 요구사항, 제약사항 등을 파악하여 최적의 기술 솔루션을 설계해드리겠습니다."""
    
    # 기본 전문가 응답
    else:
        return f"""{agent_emoji} **박사급 전문가**로서 '{message}'에 대해 분석해드리겠습니다.

🎯 **전문 분석 접근법**:
• 이론적 기반 및 학술적 배경 분석
• 현황 분석 및 핵심 요인 파악
• 실무적 적용 방안 제시
• 성과 측정 및 지속적 개선

더 구체적인 상황이나 요구사항을 알려주시면 맞춤형 전문 솔루션을 제공해드리겠습니다."""

def generate_basic_expert_response(agent: Dict[str, Any], message: str) -> str:
    """기본 전문가 응답 생성 (폴백)"""
    agent_name = agent["name"]
    agent_emoji = agent.get("emoji", "🧙‍♂️")
    specialty = agent["specialty"]
    
    return f"""{agent_emoji} **{agent_name}**로서 '{message}'에 대해 전문적인 관점에서 도움을 드리겠습니다.

🎯 **전문 분야**: {specialty}

박사급 전문 지식과 경험을 바탕으로 체계적인 분석과 솔루션을 제공해드리겠습니다. 더 구체적인 질문이나 세부사항을 알려주시면 더욱 정확하고 도움이 되는 답변을 드릴 수 있습니다."""

if __name__ == "__main__":
    print("🏰 도깨비마을장터 서버를 시작합니다...")
    print("📍 http://localhost:8000 에서 접속하세요!")
    print("🧙‍♂️ 16명의 박사급 도깨비가 대기 중입니다!")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
