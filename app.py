from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

# Vercel 환경 감지 (완전 확실한 체크)
VERCEL_ENV = (
    os.getenv("VERCEL") == "1"
    or os.getenv("VERCEL_ENV") is not None
    or os.getenv("VERCEL_URL") is not None
    or "vercel" in os.getcwd().lower()
    or "/var/task" in os.getcwd()
)

print(f"🔍 환경 감지: VERCEL_ENV={VERCEL_ENV}, CWD={os.getcwd()}")

# 🚀 서버리스 환경 전용 AI 시스템 (SQLite 완전 제거)
class VercelSafeAIManager:
    """Vercel 서버리스 환경에 최적화된 AI 매니저"""
    
    def __init__(self):
        self.experts = {
            "AI전문가": "AI와 머신러닝 전문가",
            "마케팅왕": "디지털 마케팅 전문가",
            "의료AI전문가": "의료 AI 전문가", 
            "재테크박사": "투자 및 재무 전문가",
        }
        print("✅ Vercel 안전 AI 시스템 초기화 완료!")

    def get_expert_response(self, query, expert_name="AI전문가"):
        """서버리스 최적화 응답 생성"""
        responses = {
            "AI전문가": f"🤖 AI 전문가로서 '{query}'에 대해 말씀드리면, 현재 AI 기술은 놀라운 속도로 발전하고 있습니다. 특히 자연어 처리, 컴퓨터 비전, 그리고 생성형 AI 분야에서 혁신적인 변화가 일어나고 있어, 다양한 산업에 혁신을 가져다주고 있습니다.",
            
            "마케팅왕": f"📈 마케팅 전문가로서 '{query}'를 분석해보면, 디지털 시대의 마케팅은 데이터 기반 의사결정과 개인화된 고객 경험이 핵심입니다. 소셜미디어, 콘텐츠 마케팅, 그리고 AI를 활용한 타겟팅이 성공의 열쇠라고 할 수 있습니다.",
            
            "의료AI전문가": f"🏥 의료 AI 전문가로서 '{query}'에 대해 설명드리면, 의료 분야에서 AI는 진단 정확도 향상, 치료법 개발, 그리고 환자 관리 최적화에 큰 도움을 주고 있습니다. 하지만 항상 환자 안전과 의료진의 전문성을 최우선으로 고려해야 합니다.",
            
            "재테크박사": f"💰 투자 전문가로서 '{query}'를 분석하면, 성공적인 투자는 장기적 관점, 분산투자, 그리고 지속적인 학습이 기반이 됩니다. 시장의 변동성을 이해하고 리스크를 관리하며, 자신만의 투자 철학을 갖는 것이 중요합니다."
        }
        
        return responses.get(expert_name, f"전문가 관점에서 '{query}'에 대한 상세한 분석을 제공해드리겠습니다.")

    def generate_response(self, query, expert_name="AI전문가"):
        """호환성을 위한 메서드"""
        return self.get_expert_response(query, expert_name)

# 전역 변수 초기화
real_ai_manager = VercelSafeAIManager()
AI_SYSTEM_ENABLED = True

# 서버리스 환경에서는 모든 DB 관련 시스템 비활성화
memory_manager = None
MEMORY_SYSTEM_ENABLED = False
multimodal_ai_manager = None
MULTIMODAL_SYSTEM_ENABLED = False
global_manager = None
GLOBAL_SYSTEM_ENABLED = False
dna_manager = None
DNA_SYSTEM_ENABLED = False

print("🚀 Vercel 서버리스 최적화 완료 - 모든 DB 시스템 비활성화")

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "goblin_marketplace_secret_key_2024")

print("🌟 도깨비 마을 장터 - Vercel 서버리스 모드")

@app.route("/")
def index():
    """메인 페이지"""
    return render_template("index.html")

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
        
        return jsonify({
            "response": response,
            "expert": expert,
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
    except Exception as e:
        print(f"❌ 채팅 오류: {e}")
        return jsonify({
            "error": "죄송합니다. 일시적인 오류가 발생했습니다.",
            "success": False
        }), 500

@app.route("/experts")
def get_experts():
    """전문가 목록 반환"""
    return jsonify({
        "experts": list(real_ai_manager.experts.keys()),
        "success": True
    })

@app.route("/health")
def health_check():
    """서버 상태 체크"""
    return jsonify({
        "status": "healthy",
        "environment": "vercel" if VERCEL_ENV else "local",
        "ai_system": AI_SYSTEM_ENABLED,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    if VERCEL_ENV:
        print("🚀 Vercel 환경에서 실행 중...")
    else:
        print("🖥️ 로컬 환경에서 실행 중...")
        app.run(debug=True, host="0.0.0.0", port=5000)
