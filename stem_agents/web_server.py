#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 STEM급 에이전트 웹 서버
사용자가 실제로 에이전트들과 상호작용할 수 있는 Flask 웹 서버
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import importlib.util
from datetime import datetime

app = Flask(__name__)


# 에이전트 응답 함수들을 동적으로 로드
def load_agent_response_function(agent_file):
    """에이전트 응답 파일에서 함수를 동적으로 로드"""
    try:
        spec = importlib.util.spec_from_file_location("agent_module", agent_file)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)

        # 각 에이전트별 응답 함수 찾기
        for attr_name in dir(agent_module):
            if "response" in attr_name.lower() and callable(
                getattr(agent_module, attr_name)
            ):
                return getattr(agent_module, attr_name)
        return None
    except Exception as e:
        print(f"에이전트 로드 실패 {agent_file}: {e}")
        return None


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

# 에이전트 응답 함수들 로드
agent_functions = {}
for agent_name, filename in AGENT_FILES.items():
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(file_path):
        func = load_agent_response_function(file_path)
        if func:
            agent_functions[agent_name] = func
            print(f"✅ {agent_name} 에이전트 로드 성공")
        else:
            print(f"❌ {agent_name} 에이전트 함수 로드 실패")
    else:
        print(f"❌ {agent_name} 에이전트 파일 없음: {filename}")


@app.route("/")
def dashboard():
    """메인 대시보드 페이지"""
    return send_from_directory(".", "user_dashboard.html")


@app.route("/api/ask", methods=["POST"])
def ask_agent():
    """에이전트에게 질문하기 API"""
    try:
        data = request.get_json()
        agent_type = data.get("agent_type")
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "질문을 입력해주세요."}), 400

        if agent_type not in agent_functions:
            return jsonify({"error": f"{agent_type} 에이전트를 찾을 수 없습니다."}), 404

        # 에이전트 함수 호출
        response_func = agent_functions[agent_type]
        response = response_func(question)

        return jsonify(
            {
                "success": True,
                "response": response,
                "agent_type": agent_type,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    except Exception as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "서버 오류가 발생했습니다."}), 500


@app.route("/api/agents")
def get_agents():
    """사용 가능한 에이전트 목록 API"""
    agents_info = {}
    for agent_name in agent_functions.keys():
        agents_info[agent_name] = {
            "name": agent_name,
            "status": "active",
            "file": AGENT_FILES.get(agent_name, "unknown"),
        }

    return jsonify(
        {
            "total_agents": len(agent_functions),
            "active_agents": agents_info,
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@app.route("/health")
def health_check():
    """서버 상태 확인"""
    return jsonify(
        {
            "status": "healthy",
            "loaded_agents": len(agent_functions),
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": "🎯 STEM급 에이전트 서버가 정상 작동 중입니다!",
        }
    )


# 정적 파일 서빙
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


if __name__ == "__main__":
    print("🎯 STEM급 에이전트 웹 서버 시작!")
    print("=" * 50)
    print(f"📊 로드된 에이전트: {len(agent_functions)}개")

    for agent_name in agent_functions.keys():
        print(f"  ✅ {agent_name}")

    print("=" * 50)
    print("🌐 웹 브라우저에서 http://localhost:5000 접속하세요!")
    print("🔥 박사급에서 고블린으로 진화한 AI들과 대화해보세요!")

    app.run(host="0.0.0.0", port=5000, debug=True)
