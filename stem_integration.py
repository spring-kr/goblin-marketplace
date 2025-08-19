"""
🧪 STEM 에이전트 통합 모듈 for FastAPI (간단 버전)
기본 응답 기능으로 8개 STEM 에이전트 시뮬레이션
"""

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import datetime
import os
import random

# 템플릿 설정 (없으면 None)
templates = None
if os.path.exists("templates/stem"):
    templates = Jinja2Templates(directory="templates/stem")


class STEMRequest(BaseModel):
    question: str
    agent_type: str


class STEMService:
    def __init__(self):
        """STEM 서비스 초기화"""
        self.agent_responses = {
            "math": [
                "🧮 수학 문제를 분석 중입니다... 미적분, 대수, 통계 분야의 전문 지식을 활용하겠습니다.",
                "📊 수학적 모델링과 계산을 통해 정확한 답을 제공하겠습니다.",
                "🔢 복잡한 수학 개념을 이해하기 쉽게 설명해드리겠습니다.",
            ],
            "physics": [
                "⚛️ 물리학 법칙을 적용하여 분석하겠습니다. 역학, 전자기학, 양자물리 전문가입니다.",
                "🌌 물리 현상을 깊이 있게 탐구하고 설명해드리겠습니다.",
                "⚡ 복잡한 물리 개념을 직관적으로 이해할 수 있도록 도와드리겠습니다.",
            ],
            "chemistry": [
                "🧪 화학 반응과 분자 구조를 분석하겠습니다. 유기화학, 무기화학 전문가입니다.",
                "⚗️ 화학적 성질과 반응 메커니즘을 상세히 설명해드리겠습니다.",
                "🔬 실험 설계와 화학 분석에 대한 전문적 조언을 제공하겠습니다.",
            ],
            "biology": [
                "🧬 생물학적 시스템을 분석하겠습니다. 분자생물학, 생태학, 유전학 전문가입니다.",
                "🦠 생명 현상과 생물학적 과정을 자세히 설명해드리겠습니다.",
                "🌱 생물 다양성과 진화 과정에 대한 깊이 있는 통찰을 제공하겠습니다.",
            ],
            "engineering": [
                "⚙️ 공학적 설계와 시스템 분석을 수행하겠습니다. 최적화와 효율성을 고려합니다.",
                "🔧 기술적 문제 해결과 혁신적 솔루션을 제안하겠습니다.",
                "🏗️ 실용적이고 안전한 엔지니어링 접근법을 제시하겠습니다.",
            ],
            "assistant": [
                "🤖 업무 최적화와 프로젝트 관리 전문가입니다. 효율적인 솔루션을 제안하겠습니다.",
                "📋 체계적인 업무 프로세스와 품질 관리 방법을 안내하겠습니다.",
                "⏰ 시간 관리와 생산성 향상 전략을 제공하겠습니다.",
            ],
            "marketing": [
                "📈 마케팅 전략과 브랜딩 전문가입니다. 시장 분석과 고객 인사이트를 제공하겠습니다.",
                "🎯 타겟 마케팅과 효과적인 캠페인 전략을 수립하겠습니다.",
                "💡 창의적인 마케팅 아이디어와 실행 방안을 제안하겠습니다.",
            ],
            "startup": [
                "🚀 스타트업 전략과 사업 계획 전문가입니다. 성공적인 창업을 위한 가이드를 제공하겠습니다.",
                "💰 투자 유치와 비즈니스 모델 개발에 대한 조언을 드리겠습니다.",
                "📊 시장 진입 전략과 성장 계획을 함께 수립하겠습니다.",
            ],
        }
        print(f"✅ {len(self.agent_responses)}개 STEM 에이전트 시뮬레이션 준비 완료")

    async def process_question(self, question: str, agent_type: str) -> Dict[str, Any]:
        """질문 처리"""
        try:
            if agent_type not in self.agent_responses:
                return {
                    "success": False,
                    "error": f"지원하지 않는 에이전트 타입: {agent_type}",
                }

            # 에이전트별 구체적인 답변 생성
            specific_answers = {
                "math": {
                    "이차방정식의 해법을 설명해주세요": """
🧮 이차방정식 ax² + bx + c = 0의 해법을 설명드리겠습니다!

**1. 근의 공식 (가장 일반적인 방법)**
x = (-b ± √(b²-4ac)) / 2a

**2. 인수분해법**
예: x² - 5x + 6 = 0 → (x-2)(x-3) = 0 → x = 2 또는 x = 3

**3. 완전제곱식으로 만들기**
예: x² + 6x + 5 = 0 → (x+3)² - 9 + 5 = 0 → (x+3)² = 4 → x = -1 또는 x = -5

**4. 판별식으로 근의 개수 확인**
D = b²-4ac
- D > 0: 서로 다른 두 실근
- D = 0: 중근 (한 개의 실근)  
- D < 0: 복소수 근

실제 계산 예시를 들어보시겠어요? 🚀
                    """,
                    "default": "🧮 수학 문제를 해결해드리겠습니다! 구체적인 수식이나 문제를 알려주시면 단계별로 자세히 설명해드릴게요. 미적분, 대수, 통계, 기하학 등 모든 분야 대응 가능합니다! 📊"
                },
                "physics": {
                    "뉴턴의 운동법칙을 설명해주세요": """
⚛️ 뉴턴의 3가지 운동법칙을 명확하게 설명드리겠습니다!

**제1법칙 (관성의 법칙)**
- 정지한 물체는 계속 정지, 운동하는 물체는 계속 등속운동
- 외력이 작용하지 않는 한 운동상태 불변
- 예: 급브레이크 시 몸이 앞으로 쏠리는 현상

**제2법칙 (가속도의 법칙)**  
- F = ma (힘 = 질량 × 가속도)
- 힘이 클수록, 질량이 작을수록 가속도 증가
- 예: 같은 힘으로 밀어도 가벼운 물체가 더 빨리 가속

**제3법칙 (작용-반작용의 법칙)**
- 모든 작용에는 크기가 같고 방향이 반대인 반작용 존재
- 예: 걸을 때 발로 땅을 밀면, 땅도 발을 같은 힘으로 밂

실생활 적용 예시나 문제 풀이가 필요하시면 말씀해주세요! ⚡
                    """,
                    "default": "⚛️ 물리학 현상을 분석해드리겠습니다! 역학, 전자기학, 열역학, 양자물리학 등 어떤 분야든 구체적인 공식과 실례로 설명해드릴게요! 🌌"
                },
                "chemistry": {
                    "화학결합의 종류를 설명해주세요": """
🧪 화학결합의 3가지 주요 유형을 자세히 설명드리겠습니다!

**1. 이온결합 (Ionic Bond)**
- 금속 + 비금속 간의 결합
- 전자 완전 이동 → 양이온/음이온 형성
- 예: NaCl (소금) - Na⁺ + Cl⁻
- 특징: 높은 녹는점, 수용액에서 전기전도

**2. 공유결합 (Covalent Bond)**
- 비금속 원소들 간의 결합  
- 전자쌍 공유로 안정한 전자배치
- 예: H₂O, CO₂, CH₄
- 특징: 분자 형성, 다양한 물성

**3. 금속결합 (Metallic Bond)**
- 금속 원자들 간의 결합
- 자유전자의 바다 모델
- 예: Fe, Cu, Al 등 순금속
- 특징: 전기전도성, 연성, 전성

각 결합의 세부 메커니즘이나 혼성궤도론에 대해 더 알고 싶으시면 말씀해주세요! ⚗️
                    """,
                    "default": "🧪 화학 반응과 분자 구조를 분석해드리겠습니다! 유기화학, 무기화학, 물리화학 등 모든 분야의 반응 메커니즘과 실험 설계를 도와드릴게요! 🔬"
                },
                "biology": {
                    "DNA의 구조와 기능을 설명해주세요": """
🧬 DNA의 구조와 기능을 체계적으로 설명드리겠습니다!

**DNA 구조**
- **이중나선 구조**: 2개의 상보적 가닥이 나선형으로 감김
- **염기쌍**: A-T, G-C (수소결합으로 연결)
- **백본**: 당-인산 결합으로 구성된 골격 구조
- **직경**: 약 2nm, 염기쌍 간격: 0.34nm

**주요 기능**
1. **유전정보 저장**: 모든 생명체의 설계도
2. **정보 전달**: DNA → RNA → 단백질 (중심원리)
3. **복제**: 반보존적 복제로 유전정보 전승
4. **돌연변이**: 진화의 원동력

**실제 응용**
- PCR 기술, DNA 지문법
- 유전자 치료, CRISPR 유전자 편집
- 법의학, 친자확인

분자생물학 실험이나 유전학 원리에 대해 더 궁금한 점이 있으시면 언제든 말씀해주세요! 🦠
                    """,
                    "default": "🧬 생명 현상을 분석해드리겠습니다! 분자생물학, 세포생물학, 유전학, 생태학 등 생명과학의 모든 분야를 다루며, 최신 연구 동향까지 설명해드릴게요! 🌱"
                },
                "engineering": {
                    "시스템 최적화 방법을 알려주세요": """
⚙️ 시스템 최적화의 체계적 접근법을 알려드리겠습니다!

**1. 현상 분석 단계**
- 병목지점 식별 (Bottleneck Analysis)
- 성능 메트릭 정의 및 측정
- 리소스 사용률 모니터링

**2. 최적화 전략**
- **알고리즘 최적화**: 시간/공간 복잡도 개선
- **하드웨어 최적화**: CPU, 메모리, I/O 튜닝  
- **아키텍처 최적화**: 로드밸런싱, 캐싱, CDN

**3. 실무 적용 기법**
- A/B 테스팅으로 성능 비교
- 점진적 개선 (Kaizen)
- 자동화 도구 활용

**4. 측정 및 모니터링**
- KPI 설정 (응답시간, 처리량, 에러율)
- 실시간 대시보드 구축
- 알림 시스템 운영

구체적인 시스템이나 프로젝트에 대한 최적화 방안이 필요하시면 상세히 분석해드릴게요! 🚀
                    """,
                    "default": "⚙️ 공학적 문제를 해결해드리겠습니다! 시스템 설계, 최적화, 자동화 등 엔지니어링의 모든 분야에서 실무적이고 구체적인 솔루션을 제공해드릴게요! 🔧"
                },
                "assistant": {
                    "효율적인 업무 관리 방법을 알려주세요": """
🤖 효율적인 업무 관리의 핵심 전략을 알려드리겠습니다!

**1. 시간 관리 기법**
- **포모도로 기법**: 25분 집중 + 5분 휴식
- **시간 블록킹**: 업무별 시간대 할당
- **2분 규칙**: 2분 내 처리 가능한 일은 즉시 실행

**2. 우선순위 매트릭스**
- **중요-긴급 매트릭스**: 4사분면으로 업무 분류
- **ABCDE 방법**: 중요도에 따른 순서 부여
- **파레토 법칙**: 핵심 20%에 집중

**3. 디지털 도구 활용**
- 프로젝트 관리: Notion, Trello, Asana
- 시간 추적: RescueTime, Toggl
- 자동화: IFTTT, Zapier

**4. 협업 최적화**
- 정기 체크인 미팅
- 명확한 역할 분담
- 문서화 및 지식 공유

**5. 개인 루틴 구축**
- 아침 루틴으로 하루 계획
- 일과 후 복기 시간
- 주간/월간 회고

구체적인 업무 환경에 맞는 맞춤형 시스템이 필요하시면 상세히 설계해드릴게요! 📋
                    """,
                    "default": "🤖 업무 효율성을 극대화해드리겠습니다! 프로젝트 관리, 시간 관리, 팀 협업, 생산성 향상 등 업무의 모든 영역에서 실용적인 솔루션을 제공해드릴게요! 📊"
                },
                "marketing": {
                    "브랜딩 전략을 수립하는 방법을 알려주세요": """
📈 효과적인 브랜딩 전략 수립 가이드를 제공해드리겠습니다!

**1. 브랜드 아이덴티티 정의**
- **미션**: 브랜드의 존재 이유
- **비전**: 추구하는 미래상  
- **가치**: 브랜드 핵심 원칙
- **페르소나**: 브랜드 성격과 톤앤매너

**2. 타겟 오디언스 분석**
- 데모그래픽 분석 (연령, 성별, 소득)
- 사이코그래픽 분석 (라이프스타일, 가치관)
- 페인포인트 및 니즈 파악
- 고객 여정 맵핑 (Customer Journey)

**3. 포지셔닝 전략**
- 경쟁사 분석 및 차별화 포인트
- USP (Unique Selling Proposition) 정의
- 브랜드 포지셔닝 맵 작성

**4. 브랜드 터치포인트 설계**
- 로고, 컬러, 타이포그래피
- 웹사이트, SNS, 패키징
- 고객 서비스, 매장 경험

**5. 성과 측정 KPI**
- 브랜드 인지도, 선호도
- 고객 충성도 (NPS)
- 매출 기여도

실제 브랜드나 업종에 맞는 구체적인 전략이 필요하시면 상세 분석해드릴게요! 🎯
                    """,
                    "default": "📈 마케팅 전략을 수립해드리겠습니다! 브랜딩, 디지털 마케팅, 고객 분석, 캠페인 기획 등 마케팅의 모든 영역에서 데이터 기반의 실행 가능한 전략을 제공해드릴게요! 💡"
                },
                "startup": {
                    "스타트업 투자 유치 전략을 알려주세요": """
🚀 성공적인 투자 유치를 위한 전략을 알려드리겠습니다!

**1. 투자 준비 단계**
- **사업계획서**: 명확한 비즈니스 모델과 성장 전략
- **재무 모델링**: 3-5년 수익 예측 및 자금 계획
- **MVP/트랙션**: 시장 검증 가능한 초기 성과
- **팀 구성**: 핵심 역량을 갖춘 창업팀

**2. 투자자 타겟팅**
- **엔젤 투자자**: 개인 고액 자산가, 시드 단계
- **VC**: 벤처캐피털, 시리즈 A 이후
- **정부 지원**: K-스타트업, 중기부 사업
- **크라우드펀딩**: 와디즈, 펀딩포유

**3. 피칭 전략**
- **Problem-Solution Fit**: 명확한 문제 정의와 해결책
- **Market Size**: TAM, SAM, SOM 분석
- **Competitive Advantage**: 차별화된 경쟁력
- **Go-to-Market**: 구체적인 시장 진입 전략

**4. 밸류에이션 및 협상**
- 유사 기업 비교 분석
- 적정 지분 희석률 계산
- 투자 조건 (liquidation preference 등)

**5. 투자 후 관리**
- 정기 투자자 리포트
- 마일스톤 달성 및 소통
- 후속 투자 라운드 준비

구체적인 업종이나 단계에 맞는 맞춤형 전략이 필요하시면 상세히 분석해드릴게요! 💼
                    """,
                    "default": "🚀 스타트업 성공을 위한 전략을 제공해드리겠습니다! 사업 계획, 투자 유치, 팀 빌딩, 제품 개발, 시장 진입 등 창업의 모든 단계에서 실무적인 가이드를 제공해드릴게요! 💡"
                }
            }

            # 질문에 맞는 구체적인 답변 찾기
            agent_answers = specific_answers.get(agent_type, {})
            
            # 정확히 일치하는 질문이 있는지 확인
            for sample_question, detailed_answer in agent_answers.items():
                if sample_question != "default" and sample_question in question:
                    return {
                        "success": True,
                        "agent_type": agent_type,
                        "question": question,
                        "response": detailed_answer.strip(),
                        "timestamp": datetime.datetime.now().isoformat(),
                    }
            
            # 기본 응답 사용
            base_response = random.choice(self.agent_responses[agent_type])
            default_answer = agent_answers.get("default", f"{agent_type.title()} 전문가로서 구체적인 답변을 제공하겠습니다!")
            
            custom_response = f"{base_response}\n\n{default_answer}"

            return {
                "success": True,
                "agent_type": agent_type,
                "question": question,
                "response": custom_response,
                "timestamp": datetime.datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": f"처리 중 오류 발생: {str(e)}"}

    def get_agent_info(self) -> Dict[str, Any]:
        """에이전트 정보 반환"""
        agent_info = {
            "math": "🧮 수학 천재 - 미적분, 대수, 통계 등 모든 수학 문제",
            "physics": "⚛️ 물리학 마스터 - 역학, 전자기학, 양자물리학 등",
            "chemistry": "🧪 화학 전문가 - 유기화학, 무기화학, 물리화학 등",
            "biology": "🧬 생물학 천재 - 분자생물학, 생태학, 유전학 등",
            "engineering": "⚙️ 공학 마법사 - 설계, 최적화, 시스템 분석 등",
            "assistant": "🤖 품질 어시스턴트 - 업무 최적화, 프로젝트 관리",
            "marketing": "📈 마케팅 전략가 - 브랜딩, 마케팅 전략 수립",
            "startup": "🚀 스타트업 컨설턴트 - 사업 계획, 투자 유치",
        }

        return {
            "total_agents": len(self.agent_responses),
            "loaded_agents": list(self.agent_responses.keys()),
            "agent_descriptions": agent_info,
            "status": "active",
        }


# STEM 서비스 인스턴스
stem_service = STEMService()


def setup_stem_routes(app: FastAPI):
    """FastAPI 앱에 STEM 라우트 추가"""

    @app.get("/stem/demo", response_class=HTMLResponse)
    async def stem_demo(request: Request, agent: str = "math"):
        """STEM 에이전트 데모 페이지"""
        agent_info = stem_service.get_agent_info()
        agent_descriptions = agent_info.get("agent_descriptions", {})

        if agent not in agent_descriptions:
            agent = "math"  # 기본값

        return f"""
        <html>
            <head>
                <title>🧙‍♂️ {agent_descriptions.get(agent, '도깨비')} - STEM 센터</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; 
                           background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                           background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; }}
                    @keyframes gradient {{
                        0% {{ background-position: 0% 50%; }}
                        50% {{ background-position: 100% 50%; }}
                        100% {{ background-position: 0% 50%; }}
                    }}
                    .container {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                               border-radius: 20px; padding: 30px; margin: 20px 0; }}
                    .btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
                           text-decoration: none; padding: 12px 25px; border-radius: 8px; font-weight: bold;
                           display: inline-block; margin: 10px 5px; transition: all 0.3s ease; }}
                    .btn:hover {{ transform: scale(1.05); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3); color: white; }}
                    .question-area {{ background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }}
                    #response {{ background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; margin-top: 20px; display: none; }}
                    input, textarea {{ width: 100%; padding: 10px; border: none; border-radius: 5px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🧙‍♂️ {agent_descriptions.get(agent, '도깨비')} 체험</h1>
                    <p>AI 도깨비마을 STEM 센터에 오신 것을 환영합니다!</p>
                    
                    <div class="question-area">
                        <h3>💬 도깨비에게 질문하기</h3>
                        <textarea id="questionInput" placeholder="궁금한 것을 물어보세요..." rows="3"></textarea>
                        <button class="btn" onclick="askQuestion()">🚀 질문하기</button>
                        <button class="btn" onclick="askSample()">📝 샘플 질문</button>
                    </div>
                    
                    <div id="response">
                        <h3>🧙‍♂️ 도깨비 응답:</h3>
                        <div id="responseText"></div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/" class="btn">🔙 메인으로 돌아가기</a>
                        <a href="/stem/" class="btn">🏪 STEM 센터 홈</a>
                    </div>
                </div>
                
                <script>
                    const agentType = "{agent}";
                    
                    async function askQuestion() {{
                        const question = document.getElementById('questionInput').value;
                        if (!question.trim()) {{
                            alert('질문을 입력해주세요!');
                            return;
                        }}
                        
                        document.getElementById('response').style.display = 'block';
                        document.getElementById('responseText').innerHTML = '🔮 도깨비가 마법을 부리는 중...';
                        
                        try {{
                            const response = await fetch('/stem/api/ask', {{
                                method: 'POST',
                                headers: {{'Content-Type': 'application/json'}},
                                body: JSON.stringify({{question: question, agent_type: agentType}})
                            }});
                            const data = await response.json();
                            document.getElementById('responseText').innerHTML = data.success ? data.response : '❌ ' + data.error;
                        }} catch (error) {{
                            document.getElementById('responseText').innerHTML = '❌ 마법이 실패했습니다: ' + error.message;
                        }}
                    }}
                    
                    function askSample() {{
                        const samples = {{
                            "math": "이차방정식의 해법을 설명해주세요",
                            "physics": "뉴턴의 운동법칙을 설명해주세요", 
                            "chemistry": "화학결합의 종류를 설명해주세요",
                            "biology": "DNA의 구조와 기능을 설명해주세요",
                            "engineering": "시스템 최적화 방법을 알려주세요",
                            "assistant": "효율적인 업무 관리 방법을 알려주세요",
                            "marketing": "브랜딩 전략을 수립하는 방법을 알려주세요",
                            "startup": "스타트업 투자 유치 전략을 알려주세요"
                        }};
                        document.getElementById('questionInput').value = samples[agentType] || "안녕하세요!";
                    }}
                </script>
            </body>
        </html>
        """

    @app.get("/stem/", response_class=HTMLResponse)
    async def stem_login_page(request: Request):
        """STEM 로그인 페이지"""
        return """
        <html>
            <head><title>🧙‍♂️ 도깨비마을 STEM 서비스</title></head>
            <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
                <h1>🏪 도깨비마을장터 BETA - STEM 서비스</h1>
                <h2>🧙‍♂️ 촌장급 도깨비 전문가들</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;">
                    <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px;">
                        <h3>🧮 수학촌장 도깨비</h3>
                        <p>미적분, 통계, 대수 마법을 부리는 촌장급 도깨비</p>
                        <button onclick="askAgent('math', '이차방정식을 풀어주세요')" style="background: #4CAF50; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">질문하기</button>
                    </div>
                    <div style="border: 2px solid #2196F3; padding: 15px; border-radius: 10px;">
                        <h3>⚛️ 물리촌장 도깨비</h3>
                        <p>역학, 전자기학 마법을 다루는 촌장급 도깨비</p>
                        <button onclick="askAgent('physics', '뉴턴의 법칙을 설명해주세요')" style="background: #2196F3; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">질문하기</button>
                    </div>
                    <div style="border: 2px solid #FF9800; padding: 15px; border-radius: 10px;">
                        <h3>🧪 화학촌장 도깨비</h3>
                        <p>유기화학, 무기화학 연금술의 촌장급 도깨비</p>
                        <button onclick="askAgent('chemistry', '화학결합을 설명해주세요')" style="background: #FF9800; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">질문하기</button>
                    </div>
                    <div style="border: 2px solid #9C27B0; padding: 15px; border-radius: 10px;">
                        <h3>🧬 생물촌장 도깨비</h3>
                        <p>분자생물학, 유전학 마법의 촌장급 도깨비</p>
                        <button onclick="askAgent('biology', 'DNA 구조를 설명해주세요')" style="background: #9C27B0; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">질문하기</button>
                    </div>
                </div>
                <div id="response" style="margin-top: 30px; padding: 20px; background: #f5f5f5; border-radius: 10px; display: none;">
                    <h3>🧙‍♂️ 도깨비 응답:</h3>
                    <div id="responseText"></div>
                </div>
                <script>
                    async function askAgent(agent, question) {
                        document.getElementById('response').style.display = 'block';
                        document.getElementById('responseText').innerHTML = '🔮 도깨비가 마법을 부리는 중...';
                        
                        try {
                            const response = await fetch('/stem/api/ask', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({agent: agent, question: question})
                            });
                            const data = await response.json();
                            document.getElementById('responseText').innerHTML = data.response;
                        } catch (error) {
                            document.getElementById('responseText').innerHTML = '❌ 마법이 실패했습니다: ' + error.message;
                        }
                    }
                </script>
            </body>
        </html>
        """

    @app.get("/stem/dashboard", response_class=HTMLResponse)
    async def stem_dashboard(request: Request, token: Optional[str] = None):
        """STEM 대시보드"""
        return await stem_login_page(request)  # 베타에서는 같은 페이지 사용

    @app.post("/stem/api/ask")
    async def stem_ask_question(request: STEMRequest):
        """STEM 질문 처리 API"""
        result = await stem_service.process_question(
            request.question, request.agent_type
        )
        return JSONResponse(content=result)

    @app.get("/stem/api/agents")
    async def stem_get_agents():
        """사용 가능한 에이전트 목록"""
        return JSONResponse(content=stem_service.get_agent_info())

    @app.post("/stem/login")
    async def stem_login(request: Request, subscription_token: str = Form(...)):
        """STEM 토큰 로그인"""
        # 간단한 토큰 검증 (실제로는 더 복잡한 검증 필요)
        if len(subscription_token) >= 10:
            return RedirectResponse(
                url=f"/stem/dashboard?token={subscription_token}", status_code=302
            )
        else:
            return HTMLResponse(
                """
                <html>
                    <body style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px;">
                        <h1>🏪 도깨비마을장터 BETA</h1>
                        <h2>❌ 유효하지 않은 토큰입니다.</h2>
                        <p><a href="/stem/">🔙 다시 시도하기</a></p>
                    </body>
                </html>
            """
            )

    print("✅ STEM 라우트 설정 완료")
    print("📍 사용 가능한 STEM 엔드포인트:")
    print("   - GET  /stem/           : 로그인 페이지")
    print("   - GET  /stem/dashboard  : 대시보드")
    print("   - POST /stem/api/ask    : 질문 처리")
    print("   - GET  /stem/api/agents : 에이전트 목록")
    print("   - POST /stem/login      : 토큰 로그인")
