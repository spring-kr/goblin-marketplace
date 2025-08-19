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

            # 랜덤 응답 선택
            base_response = random.choice(self.agent_responses[agent_type])

            # 질문에 맞는 맞춤형 응답 생성
            custom_response = f"{base_response}\n\n질문: {question}\n\n답변: {agent_type.title()} 전문가로서 이 질문에 대해 전문적인 분석과 해결책을 제공해드리겠습니다. 구체적인 데이터와 실례를 바탕으로 상세한 설명을 준비하고 있습니다."

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
                    <p>효진의 AI 도깨비마을 STEM 센터에 오신 것을 환영합니다!</p>
                    
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
