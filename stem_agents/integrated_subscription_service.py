#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 통합 STEM급 에이전트 구독 서비스
GitHub Pages → 구독 → 토큰 → STEM급 에이전트 사용 플로우 연결
"""

from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import sqlite3
import os
import sys
import json
import datetime
import uuid
import importlib.util
from functools import wraps

app = Flask(__name__)
app.secret_key = "stem-goblin-subscription-2025"

# 구독 데이터베이스 경로
SUBSCRIPTION_DB = "d:/도깨비마을장터/구독관리회사시스템/subscription_management.db"

# 에이전트 파일들 경로
AGENT_BASE_PATH = "d:/도깨비마을장터/완성된박사급에이전트생성기/STEM_Agent_Collection"

# 에이전트 매핑
AGENT_FILES = {
    "math": "math_genius_20250819_134854_response.py",
    "physics": "physics_master_20250819_134854_response.py", 
    "chemistry": "chemistry_expert_20250819_134854_response.py",
    "biology": "biology_genius_20250819_134854_response.py",
    "engineering": "engineering_wizard_20250819_134854_response.py",
    "assistant": "real_quality_assistant.py",
    "marketing": "marketing_strategist.py",
    "startup": "startup_consultant.py",
}


class SubscriptionValidator:
    """구독 토큰 검증 시스템"""

    def __init__(self):
        self.db_path = SUBSCRIPTION_DB

    def validate_token(self, token: str) -> dict:
        """토큰 검증 및 구독 정보 반환"""
        try:
            # STEM 토큰 형식 검증: stem-{subscription_id}-{timestamp}-{random_id}
            if not token.startswith('stem-'):
                return {"valid": False, "error": "유효하지 않은 토큰 형식입니다."}
            
            # 토큰 파싱
            token_parts = token.split('-')
            if len(token_parts) < 4:
                return {"valid": False, "error": "토큰 형식이 올바르지 않습니다."}
            
            subscription_id = token_parts[1]
            timestamp = token_parts[2]
            
            # 토큰 생성 시간 검증 (30일 유효)
            try:
                token_time = int(timestamp)
                current_time = int(datetime.datetime.now().timestamp() * 1000)
                if current_time - token_time > 30 * 24 * 60 * 60 * 1000:  # 30일
                    return {"valid": False, "error": "토큰이 만료되었습니다."}
            except ValueError:
                return {"valid": False, "error": "토큰 시간 형식이 올바르지 않습니다."}
            
            # 실제 데이터베이스가 있는 경우 검증
            if os.path.exists(self.db_path):
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()

                    # 토큰으로 구독자 정보 조회 (기존 로직)
                    cursor.execute(
                        """
                        SELECT s.id, s.email, s.company, s.plan, s.status, 
                               s.created_at, s.trial_expires, s.subscription_expires,
                               t.token, t.created_at as token_created
                        FROM subscribers s
                        JOIN access_tokens t ON s.id = t.subscriber_id
                        WHERE t.token = ? AND s.status = 'active'
                    """,
                        (token,),
                    )

                    result = cursor.fetchone()

                    if result:
                        return {
                            "valid": True,
                            "subscriber_id": result[0],
                            "email": result[1],
                            "company": result[2],
                            "plan": result[3],
                            "status": result[4],
                            "subscription_expires": result[7],
                            "token_created": result[9],
                        }
            
            # 데이터베이스가 없거나 토큰이 없는 경우 임시 검증 로직
            # GitHub Pages에서 생성된 새 토큰은 유효한 것으로 처리
            return {
                "valid": True,
                "subscriber_id": subscription_id,
                "email": "github-subscriber@hyojin.ai",
                "company": "GitHub Pages Subscriber",
                "plan": "stem_premium",
                "status": "active",
                "subscription_expires": None,  # 무제한
                "token_created": timestamp,
            }

        except Exception as e:
            return {"valid": False, "error": f"토큰 검증 오류: {str(e)}"}

    def log_usage(self, token: str, agent_type: str, question: str):
        """사용 로그 기록"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 사용 로그 테이블이 없으면 생성
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS usage_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        token TEXT,
                        agent_type TEXT,
                        question TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )

                # 로그 저장
                cursor.execute(
                    """
                    INSERT INTO usage_logs (token, agent_type, question)
                    VALUES (?, ?, ?)
                """,
                    (token, agent_type, question),
                )

                conn.commit()

        except Exception as e:
            print(f"사용 로그 저장 실패: {e}")


class AgentLoader:
    """STEM급 에이전트 로더"""

    def __init__(self):
        self.agent_functions = {}
        self.load_all_agents()

    def load_agent_function(self, agent_file):
        """에이전트 응답 함수 로드"""
        try:
            full_path = os.path.join(AGENT_BASE_PATH, agent_file)
            spec = importlib.util.spec_from_file_location("agent_module", full_path)
            if spec is None or spec.loader is None:
                return None
                
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)

            # 응답 함수 찾기 - 더 정확한 패턴 매칭
            for attr_name in dir(agent_module):
                attr = getattr(agent_module, attr_name)
                if callable(attr) and (
                    "response" in attr_name.lower() or 
                    attr_name.startswith("generate_") or
                    attr_name == "generate_math_response" or
                    attr_name == "generate_assistant_response" or
                    attr_name == "generate_marketing_response" or
                    attr_name == "generate_startup_response"
                ):
                    print(f"🔍 {agent_file}에서 함수 발견: {attr_name}")
                    return attr
            return None
        except Exception as e:
            print(f"에이전트 로드 실패 {agent_file}: {e}")
            return None

    def load_all_agents(self):
        """모든 에이전트 로드"""
        for agent_name, filename in AGENT_FILES.items():
            func = self.load_agent_function(filename)
            if func:
                self.agent_functions[agent_name] = func
                print(f"✅ {agent_name} 에이전트 로드 성공")
            else:
                print(f"❌ {agent_name} 에이전트 로드 실패")


# 전역 인스턴스
validator = SubscriptionValidator()
agent_loader = AgentLoader()


def require_subscription(f):
    """구독 토큰 검증 데코레이터"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get("access_token") or request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "토큰이 필요합니다.", "redirect": "/login"}), 401

        # Bearer 토큰 처리
        if token.startswith("Bearer "):
            token = token[7:]

        validation_result = validator.validate_token(token)

        if not validation_result["valid"]:
            return (
                jsonify({"error": validation_result["error"], "redirect": "/login"}),
                401,
            )

        # 요청에 구독 정보 추가 (세션에 저장)
        session['subscription_info'] = validation_result
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    """메인 페이지 - 토큰 입력 또는 대시보드"""
    if "access_token" in session:
        return redirect("/dashboard")
    return render_template("token_login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """토큰 로그인"""
    if request.method == "POST":
        data = request.get_json()
        token = data.get("token", "").strip()

        if not token:
            return jsonify({"error": "토큰을 입력해주세요."}), 400

        validation_result = validator.validate_token(token)

        if validation_result["valid"]:
            session["access_token"] = token
            session["subscriber_info"] = validation_result

            return jsonify(
                {"success": True, "message": "로그인 성공!", "redirect": "/dashboard"}
            )
        else:
            return jsonify({"error": validation_result["error"]}), 401

    return render_template("token_login.html")


@app.route("/dashboard")
@require_subscription
def dashboard():
    """STEM급 에이전트 대시보드"""
    subscriber_info = session.get('subscription_info', {})
    
    # 사용량 통계 가져오기 (임시 함수)
    def get_usage_stats(token):
        """사용량 통계 조회"""
        return {
            "total_questions": 0,
            "today_questions": 0,
        }
    
    usage_stats = get_usage_stats(session.get("access_token", ""))
    
    # 이용 가능한 에이전트 목록
    available_agents = [
        {"id": "math", "name": "수학 천재 고블린", "emoji": "🧮", "description": "복잡한 수학 문제 해결"},
        {"id": "physics", "name": "물리학 마스터", "emoji": "⚗️", "description": "물리학 이론과 실험 해석"},
        {"id": "chemistry", "name": "화학 전문가", "emoji": "🧪", "description": "화학 반응과 분석 전문"},
        {"id": "biology", "name": "생물학 천재", "emoji": "🧬", "description": "생명과학과 생물학 연구"},
        {"id": "engineering", "name": "공학 마법사", "emoji": "⚙️", "description": "공학 설계와 문제 해결"},
        {"id": "assistant", "name": "AI 어시스턴트", "emoji": "🤖", "description": "종합적인 AI 지원"},
        {"id": "marketing", "name": "마케팅 전략가", "emoji": "📊", "description": "마케팅 전략과 분석"},
        {"id": "startup", "name": "스타트업 컨설턴트", "emoji": "🚀", "description": "창업과 비즈니스 컨설팅"},
    ]
    
    return render_template(
        "stem_dashboard.html", 
        user_token=session.get("access_token", ""),
        usage_stats=usage_stats,
        available_agents=available_agents,
        subscriber_info=subscriber_info
    )


@app.route("/api/ask", methods=["POST"])
@require_subscription
def ask_agent():
    """에이전트에게 질문하기 (구독자 전용)"""
    try:
        data = request.get_json()
        agent_type = data.get("agent_type")
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "질문을 입력해주세요."}), 400

        if agent_type not in agent_loader.agent_functions:
            return jsonify({"error": f"{agent_type} 에이전트를 찾을 수 없습니다."}), 404

        # 사용 로그 기록
        token = session.get("access_token")
        if token:
            validator.log_usage(token, agent_type, question)

        # 에이전트 함수 호출
        response_func = agent_loader.agent_functions[agent_type]
        response = response_func(question)

        return jsonify(
            {
                "success": True,
                "response": response,
                "agent_type": agent_type,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subscriber": session.get('subscription_info', {}).get("email", "unknown"),
            }
        )

    except Exception as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "서버 오류가 발생했습니다."}), 500


@app.route("/api/subscription/info")
@require_subscription
def subscription_info():
    """구독 정보 조회"""
    return jsonify(
        {
            "subscription": session.get('subscription_info', {}),
            "available_agents": list(agent_loader.agent_functions.keys()),
            "total_agents": len(agent_loader.agent_functions),
        }
    )


@app.route("/logout")
def logout():
    """로그아웃"""
    session.clear()
    return redirect("/")


@app.route("/health")
def health_check():
    """서버 상태 확인"""
    return jsonify(
        {
            "status": "healthy",
            "loaded_agents": len(agent_loader.agent_functions),
            "database_connected": os.path.exists(SUBSCRIPTION_DB),
            "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "🎯 STEM급 구독 서비스가 정상 작동 중입니다!",
        }
    )


if __name__ == "__main__":
    print("🎯 STEM급 에이전트 구독 서비스 시작!")
    print("=" * 60)
    print("🔗 통합 플로우:")
    print("  1. GitHub Pages 랜딩 → 구독 구매")
    print("  2. 결제 성공 → 토큰 발급")
    print("  3. 토큰 입장 → STEM급 에이전트 사용")
    print("=" * 60)
    print(f"📊 로드된 에이전트: {len(agent_loader.agent_functions)}개")

    for agent_name in agent_loader.agent_functions.keys():
        print(f"  ✅ {agent_name}")

    print("=" * 60)
    print("🌐 STEM급 에이전트 구독 서비스가 시작됩니다!")
    print("🔥 구독자만 박사급 고블린들과 대화할 수 있습니다!")

    # 배포 환경 감지
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
