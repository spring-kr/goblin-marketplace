from flask import Flask, render_template, request, jsonify, render_template_string
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


# 🛡️ 초경량 AI 시스템 (DB 의존성 제로)
class UltraLightAIManager:
    """완전 서버리스 최적화 AI 매니저"""

    def __init__(self):
        self.experts = {
            "AI전문가": "AI와 머신러닝 전문가",
            "마케팅왕": "디지털 마케팅 전문가",
            "의료AI전문가": "의료 AI 전문가",
            "재테크박사": "투자 및 재무 전문가",
            "창업컨설턴트": "스타트업 및 창업 전문가",
            "개발자멘토": "프로그래밍 및 개발 전문가",
        }
        print("✅ 초경량 서버리스 AI 시스템 활성화!")

    def get_expert_response(self, query, expert_name="AI전문가"):
        """서버리스 최적화 응답 생성"""
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


if __name__ == "__main__":
    print("🖥️ 로컬 환경에서 실행 중...")
    app.run(debug=True, host="0.0.0.0", port=5000)

# Vercel 배포를 위한 WSGI 애플리케이션 객체 노출
application = app
