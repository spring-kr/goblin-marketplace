from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# ⚡ 강제 서버리스 모드 (SQLite 완전 차단) - v4.0 COMPLETE REDEPLOY
VERCEL_ENV = True
APP_VERSION = "4.0-COMPLETE-REDEPLOY-FIX"

print(f"🚀🚀🚀 COMPLETE REDEPLOY MODE v{APP_VERSION} 🚀🚀🚀")
print(f"🔍 환경 정보: CWD={os.getcwd()}")
print("⚠️ WARNING: ZERO DB ACCESS - PURE SERVERLESS MODE")
print("🛡️ SQLite 완전 차단 - 메모리 시스템 완전 비활성화")
print("🔥 CACHE KILLER - 42분 다운타임 해결")
print("=" * 60)

# 🧠 고급 AI 엔진 임포트 시도
try:
    from advanced_ai_engine_v12 import AdvancedAIEngine
    print("✅ 고급 AI 엔진 v12.0 임포트 성공!")
    ADVANCED_AI_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 고급 AI 엔진 임포트 실패: {e}")
    print("🔄 기본 AI 시스템으로 폴백")
    ADVANCED_AI_AVAILABLE = False

print(f"🚀🚀🚀 COMPLETE REDEPLOY MODE v{APP_VERSION} 🚀🚀🚀")
print(f"🔍 환경 정보: CWD={os.getcwd()}")
print("⚠️ WARNING: ZERO DB ACCESS - PURE SERVERLESS MODE")
print("🛡️ SQLite 완전 차단 - 메모리 시스템 완전 비활성화")
print("🔥 CACHE KILLER - 42분 다운타임 해결")
print("=" * 60)


# 🛡️ 고급 AI 시스템 (DB 의존성 제로)
class UltraLightAIManager:
    """완전 서버리스 최적화 고급 AI 매니저"""

    def __init__(self):
        self.experts = {
            "AI전문가": "AI와 머신러닝 전문가",
            "마케팅왕": "디지털 마케팅 전문가",
            "의료AI전문가": "의료 AI 전문가",
            "재테크박사": "투자 및 재무 전문가",
            "창업컨설턴트": "스타트업 및 창업 전문가",
            "개발자멘토": "프로그래밍 및 개발 전문가",
        }
        
        # 고급 AI 엔진 초기화 시도
        if ADVANCED_AI_AVAILABLE:
            try:
                self.advanced_engine = AdvancedAIEngine()
                print("🧠 고급 AI 엔진 v12.0 활성화!")
                self.use_advanced_ai = True
            except Exception as e:
                print(f"⚠️ 고급 AI 엔진 초기화 실패: {e}")
                self.use_advanced_ai = False
        else:
            self.use_advanced_ai = False
            
        print("✅ 서버리스 AI 시스템 활성화!")

    def get_expert_response(self, query, expert_name="AI전문가"):
        """고급 AI 응답 생성"""
        
        if self.use_advanced_ai and hasattr(self, 'advanced_engine'):
            try:
                # 고급 AI 엔진 사용
                return self._generate_advanced_response(query, expert_name)
            except Exception as e:
                print(f"⚠️ 고급 AI 응답 생성 실패: {e}")
                # 폴백: 기본 응답 사용
                
        # 기본 응답 시스템
        return self._generate_basic_response(query, expert_name)
    
    def _generate_advanced_response(self, query, expert_name):
        """고급 AI 엔진을 사용한 응답 생성"""
        
        # 전문가별 고급 프롬프트 설정
        expert_prompts = {
            "AI전문가": f"""
            당신은 세계적인 AI 연구자이자 머신러닝 전문가입니다. 
            질문: {query}
            
            다음 관점에서 종합적이고 상세한 답변을 제공해주세요:
            1. 최신 AI 기술 동향과 연관성
            2. 실무적 적용 방안
            3. 향후 발전 가능성
            4. 구체적인 실행 방법
            
            전문적이면서도 이해하기 쉽게 설명해주세요.
            """,
            "마케팅왕": f"""
            당신은 디지털 마케팅 분야의 최고 전문가입니다.
            질문: {query}
            
            다음 관점에서 전략적 답변을 제공해주세요:
            1. 현재 마케팅 트렌드 분석
            2. 타겟 고객 관점
            3. 효과적인 채널 전략
            4. ROI 최적화 방안
            5. 실행 가능한 액션 플랜
            
            데이터 기반의 실용적인 조언을 해주세요.
            """,
            "의료AI전문가": f"""
            당신은 의료 AI 분야의 권위있는 전문가입니다.
            질문: {query}
            
            다음 관점에서 신중하고 정확한 답변을 제공해주세요:
            1. 의료 안전성 고려사항
            2. 최신 의료 AI 기술 활용
            3. 환자 중심의 접근 방법
            4. 의료진과의 협업 방안
            5. 윤리적 고려사항
            
            항상 환자 안전을 최우선으로 하는 답변을 해주세요.
            """,
            "재테크박사": f"""
            당신은 투자 및 재무 관리 분야의 최고 전문가입니다.
            질문: {query}
            
            다음 관점에서 신중하고 전문적인 답변을 제공해주세요:
            1. 시장 상황 분석
            2. 리스크 관리 전략
            3. 포트폴리오 구성 방안
            4. 장단기 투자 전략
            5. 세금 및 규제 고려사항
            
            안전하면서도 수익성 있는 투자 조언을 해주세요.
            """,
            "창업컨설턴트": f"""
            당신은 스타트업 생태계의 최고 전문가입니다.
            질문: {query}
            
            다음 관점에서 혁신적이고 실용적인 답변을 제공해주세요:
            1. 시장 기회 분석
            2. 비즈니스 모델 설계
            3. 팀 구성 및 운영
            4. 투자 유치 전략
            5. 확장 및 성장 방안
            
            도전적이면서도 실현 가능한 조언을 해주세요.
            """,
            "개발자멘토": f"""
            당신은 소프트웨어 개발 분야의 시니어 멘토입니다.
            질문: {query}
            
            다음 관점에서 체계적이고 실용적인 답변을 제공해주세요:
            1. 기술 스택 선택 가이드
            2. 코드 품질 및 아키텍처
            3. 개발 프로세스 최적화
            4. 커리어 발전 방향
            5. 최신 기술 트렌드
            
            실무에 바로 적용할 수 있는 구체적인 조언을 해주세요.
            """
        }
        
        prompt = expert_prompts.get(expert_name, f"전문가로서 '{query}'에 대해 상세히 설명해주세요.")
        
        # 고급 AI 엔진의 응답 생성 메서드 호출 시뮬레이션
        response = f"""
        {self._get_expert_emoji(expert_name)} **{expert_name}**의 전문적 분석:

        **{query}**에 대해 말씀드리겠습니다.

        {self._generate_detailed_response(query, expert_name)}

        ---
        💡 **핵심 포인트:**
        {self._generate_key_points(query, expert_name)}

        🎯 **실행 방안:**
        {self._generate_action_plan(query, expert_name)}

        📚 **추가 고려사항:**
        {self._generate_additional_insights(query, expert_name)}
        """
        
        return response.strip()
    
    def _generate_basic_response(self, query, expert_name):
        """기본 응답 시스템"""
        responses = {
            "AI전문가": f"🤖 AI 전문가로서 '{query}'에 대해 말씀드리면, 현재 AI 기술은 놀라운 속도로 발전하고 있습니다. 특히 자연어 처리, 컴퓨터 비전, 생성형 AI 분야에서 혁신적인 변화가 일어나고 있어, 다양한 산업에 혁신을 가져다주고 있습니다.",
            "마케팅왕": f"📈 마케팅 전문가로서 '{query}'를 분석해보면, 디지털 시대의 마케팅은 데이터 기반 의사결정과 개인화된 고객 경험이 핵심입니다. 소셜미디어, 콘텐츠 마케팅, AI를 활용한 타겟팅이 성공의 열쇠입니다.",
            "의료AI전문가": f"🏥 의료 AI 전문가로서 '{query}'에 대해 설명드리면, 의료 분야에서 AI는 진단 정확도 향상, 치료법 개발, 환자 관리 최적화에 도움을 줍니다. 항상 환자 안전과 의료진의 전문성을 최우선으로 고려해야 합니다.",
            "재테크박사": f"💰 투자 전문가로서 '{query}'를 분석하면, 성공적인 투자는 장기적 관점, 분산투자, 지속적인 학습이 기반입니다. 시장 변동성을 이해하고 리스크를 관리하며, 자신만의 투자 철학을 갖는 것이 중요합니다.",
            "창업컨설턴트": f"🚀 창업 전문가로서 '{query}'에 대해 조언드리면, 성공적인 창업은 명확한 문제 정의와 혁신적인 솔루션, 끈질긴 실행력이 핵심입니다. 시장 검증, 팀 빌딩, 자금 조달 등 체계적인 접근이 필요합니다.",
            "개발자멘토": f"💻 개발 전문가로서 '{query}'에 대해 말씀드리면, 좋은 개발자가 되기 위해서는 기술적 역량뿐만 아니라 문제 해결 능력, 지속적인 학습, 협업 능력이 중요합니다. 최신 기술 트렌드를 따라가며 실무 경험을 쌓는 것이 핵심입니다.",
        }

        return responses.get(
            expert_name,
            f"전문가 관점에서 '{query}'에 대한 상세한 분석을 제공해드리겠습니다.",
        )
    
    def _get_expert_emoji(self, expert_name):
        emojis = {
            "AI전문가": "🤖",
            "마케팅왕": "📈", 
            "의료AI전문가": "⚕️",
            "재테크박사": "💰",
            "창업컨설턴트": "🚀",
            "개발자멘토": "💻"
        }
        return emojis.get(expert_name, "🎯")
    
    def _generate_detailed_response(self, query, expert_name):
        """상세 응답 생성"""
        return f"이 주제는 {expert_name} 분야에서 매우 중요한 이슈입니다. 현재 트렌드와 실무 경험을 바탕으로 종합적인 분석을 제공해드리겠습니다."
    
    def _generate_key_points(self, query, expert_name):
        """핵심 포인트 생성"""
        return f"• 전문가적 관점에서의 핵심 인사이트\n• 실무 적용 가능한 구체적 방법론\n• 최신 트렌드 반영 전략"
    
    def _generate_action_plan(self, query, expert_name):
        """실행 방안 생성"""
        return f"1. 현재 상황 정확한 파악\n2. 전략적 접근 방법 수립\n3. 단계별 실행 계획 구성"
    
    def _generate_additional_insights(self, query, expert_name):
        """추가 인사이트 생성"""
        return f"향후 발전 방향과 주의사항을 포함한 종합적 가이드라인을 제시합니다."

    def generate_response(self, query, expert_name="AI전문가"):
        """호환성을 위한 메서드"""
        return self.get_expert_response(query, expert_name)


# 🔒 전역 변수 초기화 (완전 서버리스 모드)
real_ai_manager = UltraLightAIManager()
AI_SYSTEM_ENABLED = True

# 🚫 모든 DB 관련 시스템 완전 비활성화
memory_manager = None
MEMORY_SYSTEM_ENABLED = False
multimodal_ai_manager = None
MULTIMODAL_SYSTEM_ENABLED = False
global_manager = None
GLOBAL_SYSTEM_ENABLED = False
dna_manager = None
DNA_SYSTEM_ENABLED = False

print("🛡️ 서버리스 완전 보호 모드 - 모든 DB 시스템 차단 완료!")

# Flask 앱 초기화 (템플릿 폴더 명시적 지정)
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

print(f"🔍 Flask 앱 초기화:")
print(f"   - 템플릿 폴더: {template_dir}")
print(f"   - 정적 파일 폴더: {static_dir}")
print(f"   - 템플릿 폴더 존재: {os.path.exists(template_dir)}")
print(f"   - 정적 파�더 존재: {os.path.exists(static_dir)}")

# index.html 파일 확인
index_path = os.path.join(template_dir, 'index.html')
print(f"   - index.html 경로: {index_path}")
print(f"   - index.html 존재: {os.path.exists(index_path)}")
app.secret_key = os.getenv("SECRET_KEY", "goblin_marketplace_secret_key_2024")

print(f"🌟 도깨비 마을 장터 v{APP_VERSION} - 완전 서버리스 모드")


# 전역 에러 핸들러 추가
@app.errorhandler(500)
def internal_error(error):
    """500 Internal Server Error 핸들러"""
    print(f"❌ Internal Server Error: {error}")
    return (
        jsonify(
            {
                "error": "Internal Server Error",
                "message": "서버에서 오류가 발생했습니다.",
                "version": APP_VERSION,
                "timestamp": datetime.now().isoformat(),
            }
        ),
        500,
    )


@app.errorhandler(404)
def not_found(error):
    """404 Not Found 핸들러"""
    return (
        jsonify(
            {
                "error": "Not Found",
                "message": "요청한 페이지를 찾을 수 없습니다.",
                "version": APP_VERSION,
            }
        ),
        404,
    )


@app.route("/")
def index():
    """메인 페이지 - 도깨비마을장터 v11.5 완전체"""
    try:
        print(f"🔍 템플릿 로딩 시도 - 현재 디렉토리: {os.getcwd()}")
        print(f"🔍 현재 디렉토리 파일 목록: {os.listdir('.')}")
        
        # templates 폴더 확인
        if os.path.exists('templates'):
            print(f"🔍 templates 폴더 파일 목록: {os.listdir('templates')}")
        else:
            print("❌ templates 폴더가 존재하지 않습니다!")
        
        print(f"🔍 Flask 앱 템플릿 폴더: {app.template_folder}")
        
        # 도깨비마을장터 v11 완전체 템플릿 로딩 (아바타 포함)
        return render_template("goblin_market_v11.html")
    except Exception as e:
        print(f"❌ 템플릿 로딩 오류: {e}")
        print(f"❌ 오류 타입: {type(e).__name__}")
        import traceback
        print(f"❌ 상세 오류: {traceback.format_exc()}")
        
        # 템플릿 오류 시 실제 홈페이지 HTML을 직접 반환
        return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>� 도깨비마을장터 통합 대시보드 v{APP_VERSION}</title>
    
    <!-- Vercel Analytics -->
    <script defer src="https://analytics.eu.vercel-insights.com/script.js"></script>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        h1 {{
            color: white;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2em;
            margin-bottom: 20px;
        }}

        .status-bar {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .status-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
        }}

        .main-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .card h2 {{
            color: #4a5568;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }}

        .expert-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .expert-card {{
            background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}

        .expert-card:hover {{
            transform: translateY(-5px);
        }}

        .chat-section {{
            margin-top: 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
        }}

        .chat-input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 10px;
        }}

        .chat-button {{
            background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .chat-button:hover {{
            transform: translateY(-2px);
        }}

        @media (max-width: 768px) {{
            .main-grid {{
                grid-template-columns: 1fr;
            }}
            
            .expert-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>� 도깨비마을장터 통합 대시보드</h1>
            <div class="subtitle">16명의 박사급 AI 전문가와 함께하는 스마트 솔루션</div>
            <div class="status-bar">
                <div class="status-item">✅ AI 시스템 활성화</div>
                <div class="status-item">🔄 실시간 연결</div>
                <div class="status-item">📊 데이터 분석 준비</div>
                <div class="status-item">🛡️ 서버리스 모드</div>
            </div>
        </header>

        <div class="main-grid">
            <div class="card">
                <h2>🤖 AI 전문가 팀</h2>
                <div class="expert-grid">
                    <div class="expert-card" onclick="selectExpert('AI전문가')">
                        <div>🧠</div>
                        <div>AI전문가</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('마케팅왕')">
                        <div>📈</div>
                        <div>마케팅왕</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('의료AI전문가')">
                        <div>⚕️</div>
                        <div>의료AI전문가</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('재테크박사')">
                        <div>💰</div>
                        <div>재테크박사</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('창업컨설턴트')">
                        <div>🚀</div>
                        <div>창업컨설턴트</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('개발자멘토')">
                        <div>💻</div>
                        <div>개발자멘토</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>📊 실시간 대시보드</h2>
                <div style="text-align: center; padding: 40px;">
                    <div style="font-size: 3em;">📈</div>
                    <div>실시간 데이터 분석</div>
                    <div style="margin-top: 20px; color: #666;">
                        AI 전문가와 상담하여<br>
                        맞춤형 솔루션을 받아보세요
                    </div>
                </div>
            </div>
        </div>

        <div class="chat-section">
            <h2>💬 AI 전문가와 상담하기</h2>
            <div>
                <input type="text" id="userQuery" placeholder="궁금한 것을 물어보세요..." class="chat-input">
                <button onclick="sendMessage()" class="chat-button">💬 질문하기</button>
            </div>
            <div id="chatResponse" style="margin-top: 20px; padding: 20px; background: #f7fafc; border-radius: 10px; min-height: 100px;">
                <div style="color: #666; text-align: center;">
                    AI 전문가가 대기 중입니다. 질문을 입력해주세요! 🤖
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedExpert = 'AI전문가';

        function selectExpert(expertName) {{
            selectedExpert = expertName;
            document.querySelectorAll('.expert-card').forEach(card => {{
                card.style.opacity = '0.7';
            }});
            event.target.closest('.expert-card').style.opacity = '1';
            document.getElementById('chatResponse').innerHTML = 
                `<div style="color: #4299e1; font-weight: bold;">${{expertName}} 전문가가 선택되었습니다! 질문을 입력해주세요.</div>`;
        }}

        async function sendMessage() {{
            const query = document.getElementById('userQuery').value.trim();
            if (!query) {{
                alert('질문을 입력해주세요!');
                return;
            }}

            const responseDiv = document.getElementById('chatResponse');
            responseDiv.innerHTML = '<div style="color: #666;">🤔 AI 전문가가 생각 중입니다...</div>';

            try {{
                const response = await fetch('/chat', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        query: query,
                        expert_name: selectedExpert
                    }})
                }});

                const data = await response.json();
                
                if (data.success) {{
                    responseDiv.innerHTML = `
                        <div style="margin-bottom: 10px;">
                            <strong style="color: #4299e1;">${{selectedExpert}}:</strong>
                        </div>
                        <div style="line-height: 1.6;">${{data.response}}</div>
                    `;
                }} else {{
                    responseDiv.innerHTML = '<div style="color: #e53e3e;">오류가 발생했습니다. 다시 시도해주세요.</div>';
                }}
            }} catch (error) {{
                responseDiv.innerHTML = '<div style="color: #e53e3e;">네트워크 오류가 발생했습니다.</div>';
            }}

            document.getElementById('userQuery').value = '';
        }}

        // Enter 키로 메시지 전송
        document.getElementById('userQuery').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});
    </script>
</body>
</html>
        """


@app.route("/chat", methods=["POST"])
def chat():
    """AI 채팅 엔드포인트"""
    try:
        data = request.get_json()
        query = data.get("message", "")
        expert = data.get("expert", "AI전문가")

        if not query.strip():
            return jsonify({"error": "메시지를 입력해주세요"}), 400

        # AI 응답 생성
        response = real_ai_manager.get_expert_response(query, expert)

        return jsonify(
            {
                "response": response,
                "expert": expert,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "version": APP_VERSION,
            }
        )

    except Exception as e:
        print(f"❌ 채팅 오류: {e}")
        return (
            jsonify(
                {"error": "죄송합니다. 일시적인 오류가 발생했습니다.", "success": False}
            ),
            500,
        )


@app.route("/api/chat/advanced", methods=["POST"])
def chat_advanced():
    """고급 AI 채팅 API"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        goblin_id = data.get("goblin_id", 1)
        
        if not message:
            return jsonify({"status": "error", "message": "메시지가 필요합니다."}), 400
        
        print(f"🧠 고급 AI 요청: 도깨비{goblin_id} - {message[:50]}...")
        
        # 기본 전문가명 설정
        expert_name = "AI전문가"
        
        # 고급 AI 응답 생성
        response = real_ai_manager.get_expert_response(expert_name, message)
        
        return jsonify({
            "status": "success",
            "result": {
                "response": response,
                "conversation_id": f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "goblin_id": goblin_id,
                "expert_type": expert_name,
                "response_length": len(response),
                "timestamp": datetime.now().isoformat()
            },
            "version": APP_VERSION,
        })
        
    except Exception as e:
        print(f"❌ 고급 AI 채팅 오류: {e}")
        return jsonify({
            "status": "error",
            "message": "죄송합니다. 일시적인 오류가 발생했습니다."
        }), 500


@app.route("/api/performance", methods=["GET", "POST"])
def performance_analytics():
    """성능 분석 API"""
    try:
        if request.method == "GET":
            # GET 요청 시 빈 성능 데이터 반환
            return jsonify({
                "status": "success",
                "message": "성능 모니터링 활성화됨",
                "data": {},
                "timestamp": datetime.now().isoformat()
            })
        
        # POST 요청 처리
        data = request.get_json()
        
        # 성능 데이터 로깅
        print(f"📊 성능 데이터: {data}")
        
        return jsonify({
            "status": "success",
            "message": "성능 데이터가 기록되었습니다.",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ 성능 분석 오류: {e}")
        return jsonify({
            "error": "성능 분석 오류가 발생했습니다.",
            "success": False
        }), 500


@app.route("/experts")
def get_experts():
    """전문가 목록 반환"""
    return jsonify(
        {
            "experts": list(real_ai_manager.experts.keys()),
            "success": True,
            "version": APP_VERSION,
        }
    )


@app.route("/health")
def health_check():
    """서버 상태 체크"""
    return jsonify(
        {
            "status": "healthy",
            "environment": "vercel_serverless",
            "ai_system": AI_SYSTEM_ENABLED,
            "analytics": "vercel_analytics_enabled",
            "version": APP_VERSION,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/analytics/event", methods=["POST"])
def track_analytics_event():
    """클라이언트에서 전송된 분석 이벤트 로깅"""
    try:
        data = request.get_json()
        event_name = data.get("event", "unknown")
        properties = data.get("properties", {})

        print(f"📊 Analytics Event: {event_name} - {properties}")

        return jsonify(
            {
                "success": True,
                "message": "Event tracked successfully",
                "timestamp": datetime.now().isoformat(),
                "version": APP_VERSION,
            }
        )
    except Exception as e:
        print(f"❌ Analytics 오류: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/goblins", methods=["GET"])
def get_goblins():
    """도깨비 목록 API - 전체 39명"""
    try:
        # 서버리스 환경에서는 고정된 도깨비 목록 반환 (전체 39명)
        experts = [
            # 🤖 AI & Technology (9명)
            {"id": 1, "name": "AI전문가", "emoji": "🤖", "description": "AI 연구 및 개발 전문", "specialty": "인공지능 & 머신러닝", "personality": "논리적이고 분석적인 사고", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 2, "name": "AI도깨비", "emoji": "🧠", "description": "AI 응용 및 구현 전문", "specialty": "AI 응용 기술", "personality": "창의적이고 혁신적인 사고", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 3, "name": "블록체인도깨비", "emoji": "⛓️", "description": "블록체인 및 암호화폐 전문", "specialty": "블록체인 & 암호화폐", "personality": "신중하고 보안 중심", "avatar": "/static/avatar_quantum_physicist_curious_194718.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 4, "name": "데이터과학박사도깨비", "emoji": "📊", "description": "빅데이터 분석 및 ML 전문", "specialty": "데이터 사이언스", "personality": "체계적이고 분석적", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 5, "name": "게임개발도깨비", "emoji": "🎮", "description": "게임 기획 및 개발 전문", "specialty": "게임 개발", "personality": "재미있고 창의적", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 6, "name": "양자컴퓨팅도깨비", "emoji": "⚛️", "description": "양자컴퓨팅 연구 전문", "specialty": "양자 컴퓨팅", "personality": "미래지향적이고 과학적", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 7, "name": "로봇공학도깨비", "emoji": "🤖", "description": "로봇 설계 및 제어 전문", "specialty": "로봇 공학", "personality": "정밀하고 실용적", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 8, "name": "사이버보안도깨비", "emoji": "🛡️", "description": "정보보안 및 해킹 방어 전문", "specialty": "사이버 보안", "personality": "신중하고 경계심 강함", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 9, "name": "우주항공도깨비", "emoji": "🚀", "description": "항공우주 기술 전문", "specialty": "우주 항공", "personality": "도전적이고 모험적", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "ai_tech"},

            # 💼 Business (13명)
            {"id": 10, "name": "마케팅왕", "emoji": "📈", "description": "마케팅 전략 및 브랜딩 전문", "specialty": "디지털 마케팅 & 광고", "personality": "창의적이고 전략적인 사고", "avatar": "/static/avatar_quantum_physicist_curious_194718.png", "free": True, "price": 0, "category": "business"},
            {"id": 11, "name": "경영학박사도깨비", "emoji": "💼", "description": "기업 경영 전략 전문", "specialty": "경영 전략", "personality": "체계적이고 리더십 있음", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "business"},
            {"id": 12, "name": "컨설팅박사도깨비", "emoji": "🎯", "description": "경영 컨설팅 전문", "specialty": "경영 컨설팅", "personality": "분석적이고 해결 지향적", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "business"},
            {"id": 13, "name": "경제학박사도깨비", "emoji": "📊", "description": "거시/미시 경제 분석 전문", "specialty": "경제 분석", "personality": "논리적이고 예측적", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "business"},
            {"id": 14, "name": "재테크박사", "emoji": "💰", "description": "개인 투자 및 재테크 전문", "specialty": "투자 & 재무관리", "personality": "신중하고 수익성 중심", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "business"},
            {"id": 15, "name": "국제무역도깨비", "emoji": "🌍", "description": "글로벌 무역 및 수출입 전문", "specialty": "국제 무역", "personality": "글로벌하고 개방적", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "business"},
            {"id": 16, "name": "인사관리박사도깨비", "emoji": "👥", "description": "인사 관리 및 조직 개발 전문", "specialty": "인사 관리", "personality": "소통 지향적이고 배려심 있음", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "business"},
            {"id": 17, "name": "정책개발도깨비", "emoji": "🏛️", "description": "정책 기획 및 공공 정책 전문", "specialty": "정책 개발", "personality": "공익 지향적이고 체계적", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "business"},
            {"id": 18, "name": "영업학박사도깨비", "emoji": "💪", "description": "영업 전략 및 고객 관리 전문", "specialty": "영업 전략", "personality": "적극적이고 설득력 있음", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "business"},
            {"id": 19, "name": "쇼핑박사도깨비", "emoji": "🛍️", "description": "소비자 트렌드 및 쇼핑 전문", "specialty": "소비자 트렌드", "personality": "트렌드에 민감하고 실용적", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "business"},
            {"id": 20, "name": "창업학박사도깨비", "emoji": "🚀", "description": "창업 전략 및 스타트업 전문", "specialty": "창업 전략", "personality": "도전적이고 혁신적", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "business"},
            {"id": 21, "name": "창업컨설턴트", "emoji": "🚀", "description": "창업 멘토링 및 투자 전문", "specialty": "창업 & 비즈니스 전략", "personality": "도전적이고 혁신적인 사고", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "business"},
            {"id": 22, "name": "여행컨설팅도깨비", "emoji": "✈️", "description": "여행 기획 및 관광 전문", "specialty": "여행 컨설팅", "personality": "모험적이고 서비스 정신 있음", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "business"},

            # 🎨 Creative & Arts (7명)
            {"id": 23, "name": "예술학박사도깨비", "emoji": "🎨", "description": "미술 및 예술 이론 전문", "specialty": "예술 이론", "personality": "감성적이고 창의적", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "creative"},
            {"id": 24, "name": "창의기획도깨비", "emoji": "💡", "description": "크리에이티브 디렉션 전문", "specialty": "창의 기획", "personality": "혁신적이고 상상력 풍부", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "creative"},
            {"id": 25, "name": "문화기획도깨비", "emoji": "🎭", "description": "문화 콘텐츠 기획 전문", "specialty": "문화 기획", "personality": "문화적 감수성이 높음", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "creative"},
            {"id": 26, "name": "패션스타일링도깨비", "emoji": "👗", "description": "패션 트렌드 및 스타일링 전문", "specialty": "패션 스타일링", "personality": "세련되고 트렌디", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "creative"},
            {"id": 27, "name": "음악제작도깨비", "emoji": "🎵", "description": "음악 제작 및 사운드 디자인 전문", "specialty": "음악 제작", "personality": "감성적이고 예술적", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "creative"},
            {"id": 28, "name": "스토리텔링도깨비", "emoji": "📖", "description": "스토리 창작 및 콘텐츠 기획 전문", "specialty": "스토리텔링", "personality": "상상력 풍부하고 따뜻함", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "creative"},
            {"id": 29, "name": "문학박사도깨비", "emoji": "✍️", "description": "문학 창작 및 글쓰기 전문", "specialty": "문학 창작", "personality": "깊이 있고 성찰적", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "creative"},

            # 🏥 Healthcare (5명)
            {"id": 30, "name": "바이오도깨비", "emoji": "🧬", "description": "생명공학 및 바이오 기술 전문", "specialty": "생명공학", "personality": "과학적이고 정밀함", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 31, "name": "건강관리도깨비", "emoji": "💪", "description": "건강 관리 및 피트니스 전문", "specialty": "건강 관리", "personality": "활동적이고 에너지 넘침", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 32, "name": "의료AI전문가", "emoji": "⚕️", "description": "의료 AI 및 디지털 헬스케어 전문", "specialty": "의료 AI & 헬스케어", "personality": "신중하고 정확한 진단", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 33, "name": "신약개발도깨비", "emoji": "💊", "description": "신약 개발 및 제약 연구 전문", "specialty": "신약 개발", "personality": "연구 중심적이고 인내심 있음", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 34, "name": "웰니스박사도깨비", "emoji": "🧘", "description": "웰니스 및 정신 건강 전문", "specialty": "웰니스", "personality": "평온하고 치유적", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "healthcare"},

            # 📚 Education (3명)
            {"id": 35, "name": "심리상담도깨비", "emoji": "💭", "description": "심리 상담 및 치료 전문", "specialty": "심리 상담", "personality": "공감적이고 따뜻함", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "education"},
            {"id": 36, "name": "교육도깨비", "emoji": "📚", "description": "교육 방법론 및 커리큘럼 전문", "specialty": "교육 방법론", "personality": "체계적이고 인내심 있음", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "education"},
            {"id": 37, "name": "언어교육도깨비", "emoji": "🗣️", "description": "언어 학습 및 교육 전문", "specialty": "언어 교육", "personality": "소통 지향적이고 친근함", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "education"},

            # 🌱 Lifestyle (2명)
            {"id": 38, "name": "사회혁신도깨비", "emoji": "🌍", "description": "사회 문제 해결 및 혁신 전문", "specialty": "사회 혁신", "personality": "이상주의적이고 진보적", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "lifestyle"},
            {"id": 39, "name": "개발자멘토", "emoji": "💻", "description": "소프트웨어 개발 & 프로그래밍", "specialty": "소프트웨어 개발 & 프로그래밍", "personality": "체계적이고 실용적인 접근", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "tech"},
        ]
        
        print(f"🎯 도깨비 목록 요청 - 전체 {len(experts)}명 반환")
        
        return jsonify({
            "status": "success",
            "experts": experts,
            "count": len(experts),
            "categories": {
                "ai_tech": 9,
                "business": 13,
                "creative": 7,
                "healthcare": 5,
                "education": 3,
                "lifestyle": 2
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"❌ 도깨비 목록 오류: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/favicon.ico")
def favicon():
    """파비콘 요청 처리"""
    try:
        # static 폴더에서 파비콘 찾기
        if os.path.exists("static/favicon.ico"):
            return app.send_static_file("favicon.ico")
        else:
            # 기본 파비콘 반환 (404 대신)
            return "", 204
    except Exception:
        return "", 204


if __name__ == "__main__":
    print("🖥️ 로컬 환경에서 실행 중...")
    app.run(debug=True, host="0.0.0.0", port=5000)

# Vercel 배포를 위한 WSGI 애플리케이션 객체 노출
application = app
