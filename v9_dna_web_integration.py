"""
🧬 v9.0 DNA 수준 개인화 시스템 웹 통합 데모
실제 사용자 대화창에서 개인화 기능 구현
"""

from flask import Flask, request, jsonify, render_template_string
import asyncio
import json
from datetime import datetime
from complete_16_experts_v9_real_dna_personalization_20250823 import (
    DNAPersonalizedExpertSystem,
)
import threading

app = Flask(__name__)

# v9.0 DNA 개인화 시스템 초기화
dna_system = None


def init_system():
    """시스템 초기화 (비동기)"""
    global dna_system
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    dna_system = DNAPersonalizedExpertSystem()
    print("🧬 v9.0 DNA 수준 개인화 시스템 웹 서버 준비 완료!")


# 시스템 초기화 스레드
init_thread = threading.Thread(target=init_system)
init_thread.daemon = True
init_thread.start()

# 웹 인터페이스 HTML 템플릿
WEB_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧬 v9.0 DNA 수준 개인화 AI 전문가</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .dna-info {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }

        .personalization-status {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .status-card {
            background: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .status-card.active {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }

        .chat-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            height: 500px;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
        }

        .chat-header {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 15px 15px 0 0;
            text-align: center;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.5);
        }

        .message {
            margin-bottom: 15px;
            padding: 12px 15px;
            border-radius: 10px;
            max-width: 80%;
            word-wrap: break-word;
        }

        .user-message {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
            text-align: right;
        }

        .ai-message {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e0e0e0;
            margin-right: auto;
        }

        .personalization-info {
            font-size: 0.9em;
            color: #666;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #eee;
        }

        .chat-input-area {
            display: flex;
            padding: 15px;
            background: white;
            border-radius: 0 0 15px 15px;
            border-top: 1px solid #e0e0e0;
        }

        .chat-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }

        .send-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            margin-left: 10px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .user-profile {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }

        .profile-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }

        .profile-item {
            text-align: center;
            padding: 10px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
        }

        .loading {
            opacity: 0.7;
            font-style: italic;
        }

        .dna-badge {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 v9.0 DNA 수준 개인화 AI</h1>
            <p>깊은 맥락 분석 + 정교한 개인화로 완전히 다른 응답을 경험하세요</p>
        </div>

        <div class="dna-info">
            <h3>🎯 개인화 상태</h3>
            <div class="personalization-status" id="personalizationStatus">
                <div class="status-card">
                    <strong>🗣️ 의사소통</strong><br>
                    <span id="commStyle">분석 대기</span>
                </div>
                <div class="status-card">
                    <strong>🎓 전문성</strong><br>
                    <span id="expertiseLevel">분석 대기</span>
                </div>
                <div class="status-card">
                    <strong>😊 현재 분위기</strong><br>
                    <span id="currentMood">분석 대기</span>
                </div>
                <div class="status-card">
                    <strong>⚡ 긴급도</strong><br>
                    <span id="urgencyLevel">분석 대기</span>
                </div>
            </div>
        </div>

        <div class="chat-container">
            <div class="chat-header">
                <h3>💬 DNA 수준 개인화 대화</h3>
                <p>당신의 스타일에 맞춰 완전히 다른 답변을 제공합니다</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="ai-message">
                    <strong>🧬 DNA AI:</strong><br>
                    안녕하세요! v9.0 DNA 수준 개인화 시스템입니다.<br>
                    당신의 첫 메시지를 통해 의사소통 스타일, 전문성 수준, 현재 분위기 등을 분석하여<br>
                    <span class="dna-badge">DNA 수준</span>에서 완전히 개인화된 응답을 제공하겠습니다!
                </div>
            </div>

            <div class="chat-input-area">
                <input type="text" id="chatInput" class="chat-input" 
                       placeholder="메시지를 입력하세요... (첫 메시지로 개인화 분석이 시작됩니다)"
                       onkeypress="handleKeyPress(event)">
                <button class="send-button" onclick="sendMessage()">전송</button>
            </div>
        </div>

        <div class="user-profile" id="userProfile" style="display: none;">
            <h3>👤 당신의 DNA 프로필</h3>
            <div class="profile-grid" id="profileGrid">
                <!-- 프로필 정보가 여기에 동적으로 추가됩니다 -->
            </div>
        </div>
    </div>

    <script>
        let userId = 'web_user_' + Date.now();
        let messageCount = 0;

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;

            const messagesContainer = document.getElementById('chatMessages');
            
            // 사용자 메시지 추가
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.innerHTML = `<strong>나:</strong><br>${message}`;
            messagesContainer.appendChild(userMessage);
            
            // 입력창 비우기
            input.value = '';
            messageCount++;
            
            // 로딩 메시지 표시
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'message ai-message loading';
            loadingMessage.innerHTML = '<strong>🧬 DNA AI:</strong><br>개인화 분석 중... 💭';
            messagesContainer.appendChild(loadingMessage);
            
            // 스크롤 최하단으로
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        message: message,
                        message_count: messageCount
                    })
                });
                
                const result = await response.json();
                
                // 로딩 메시지 제거
                messagesContainer.removeChild(loadingMessage);
                
                // AI 응답 추가
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message ai-message';
                
                let messageContent = `<strong>🧬 ${result.expert}:</strong><br>${result.response}`;
                
                // 개인화 정보 추가
                if (result.personalization_info) {
                    messageContent += `
                        <div class="personalization-info">
                            <span class="dna-badge">DNA 개인화 적용</span><br>
                            스타일: ${result.personalization_info.style}<br>
                            레벨: ${result.personalization_info.level}
                        </div>
                    `;
                }
                
                aiMessage.innerHTML = messageContent;
                messagesContainer.appendChild(aiMessage);
                
                // 개인화 상태 업데이트
                if (result.user_analysis) {
                    updatePersonalizationStatus(result.user_analysis);
                }
                
                // 사용자 프로필 표시
                if (result.user_profile) {
                    updateUserProfile(result.user_profile);
                }
                
            } catch (error) {
                // 로딩 메시지 제거
                messagesContainer.removeChild(loadingMessage);
                
                // 에러 메시지 표시
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message ai-message';
                errorMessage.innerHTML = '<strong>❌ 오류:</strong><br>메시지 전송 중 문제가 발생했습니다.';
                messagesContainer.appendChild(errorMessage);
                
                console.error('Error:', error);
            }
            
            // 스크롤 최하단으로
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function updatePersonalizationStatus(analysis) {
            document.getElementById('commStyle').textContent = analysis.communication_style || '분석중';
            document.getElementById('expertiseLevel').textContent = analysis.expertise_level || '분석중';
            document.getElementById('currentMood').textContent = analysis.current_mood || '분석중';
            document.getElementById('urgencyLevel').textContent = analysis.urgency || '분석중';
            
            // 상태 카드 활성화
            const cards = document.querySelectorAll('.status-card');
            cards.forEach(card => card.classList.add('active'));
        }

        function updateUserProfile(profile) {
            const profileContainer = document.getElementById('userProfile');
            const profileGrid = document.getElementById('profileGrid');
            
            profileGrid.innerHTML = `
                <div class="profile-item">
                    <strong>의사소통</strong><br>
                    ${profile.communication_style}
                </div>
                <div class="profile-item">
                    <strong>정보 선호</strong><br>
                    ${profile.information_preference}
                </div>
                <div class="profile-item">
                    <strong>학습 스타일</strong><br>
                    ${profile.learning_style}
                </div>
                <div class="profile-item">
                    <strong>전문성</strong><br>
                    ${profile.expertise_level}
                </div>
                <div class="profile-item">
                    <strong>상호작용</strong><br>
                    ${profile.interaction_count}회
                </div>
                <div class="profile-item">
                    <strong>완성도</strong><br>
                    ${profile.profile_completeness}
                </div>
            `;
            
            profileContainer.style.display = 'block';
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """메인 페이지"""
    return render_template_string(WEB_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
    """개인화된 채팅 엔드포인트"""
    global dna_system

    if not dna_system:
        return (
            jsonify(
                {
                    "error": "시스템이 아직 초기화되지 않았습니다. 잠시 후 다시 시도해주세요."
                }
            ),
            503,
        )

    try:
        data = request.json
        user_id = data.get("user_id")
        message = data.get("message")
        message_count = data.get("message_count", 1)

        # 비동기 함수를 동기적으로 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # v9.0 DNA 개인화 상담 실행
        result = loop.run_until_complete(
            dna_system.get_personalized_consultation(
                user_id=user_id, query=message, expert_type="auto", language="ko"
            )
        )

        # 사용자 프로필 가져오기
        profile_summary = dna_system.get_user_profile_summary(user_id)

        # 응답 구성
        response_data = {
            "expert": result["expert"],
            "response": result["response"],
            "personalization_level": result["personalization_level"],
            "personalization_info": {
                "style": f"{result['style_applied']['tone']} + {result['style_applied']['detail_level']}",
                "level": result["personalization_level"],
            },
            "user_analysis": (
                {
                    "communication_style": profile_summary.get(
                        "communication_style", "분석중"
                    ),
                    "expertise_level": profile_summary.get("expertise_level", "분석중"),
                    "current_mood": profile_summary.get("current_mood", "분석중"),
                    "urgency": profile_summary.get("patience_level", "분석중"),
                }
                if profile_summary.get("status") != "no_profile"
                else None
            ),
            "user_profile": (
                {
                    "communication_style": profile_summary.get(
                        "communication_style", "분석중"
                    ),
                    "information_preference": profile_summary.get(
                        "learning_style", "분석중"
                    ),
                    "learning_style": profile_summary.get("learning_style", "분석중"),
                    "expertise_level": profile_summary.get("expertise_level", "분석중"),
                    "interaction_count": profile_summary.get("interaction_count", 0),
                    "profile_completeness": profile_summary.get(
                        "profile_completeness", "0%"
                    ),
                }
                if profile_summary.get("status") != "no_profile"
                else None
            ),
            "next_suggestions": result.get("next_suggestions", []),
            "predictive_help": result.get("predictive_help", []),
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": f"처리 중 오류가 발생했습니다: {str(e)}"}), 500


@app.route("/system-stats")
def system_stats():
    """시스템 통계"""
    if not dna_system:
        return jsonify({"error": "시스템 초기화 중입니다."}), 503

    stats = dna_system.get_system_stats()
    return jsonify(stats)


if __name__ == "__main__":
    print("🧬 v9.0 DNA 수준 개인화 웹 서버 시작...")
    print("📱 http://127.0.0.1:5000 에서 개인화 대화 체험 가능!")
    print("🎯 실시간으로 사용자 스타일 분석하여 완전히 다른 응답 제공")

    app.run(debug=True, host="127.0.0.1", port=5000)
