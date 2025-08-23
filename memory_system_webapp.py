#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 대화 기억/학습 시스템 Flask 통합 예시
"""

from flask import Flask, render_template_string, request, jsonify
from conversation_memory_system import ConversationMemorySystem
import time

app = Flask(__name__)

# 메모리 시스템 초기화
memory_system = ConversationMemorySystem("webapp_memory.json")

# 웹 인터페이스 템플릿
WEBAPP_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>🧠 대화 기억/학습 시스템 데모</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .stats-panel {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .chat-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 80%;
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin-left: auto;
            text-align: right;
        }
        
        .bot-message {
            background: rgba(255, 255, 255, 0.2);
            margin-right: auto;
        }
        
        .emotion-tag {
            font-size: 0.8em;
            background: rgba(255, 255, 255, 0.3);
            padding: 2px 8px;
            border-radius: 10px;
            margin-left: 10px;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
        }
        
        #chat-input {
            flex: 1;
            padding: 15px;
            font-size: 1em;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            outline: none;
        }
        
        #send-btn {
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 25px;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        
        #send-btn:hover {
            opacity: 0.8;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #ffffff;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .emotion-chart {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        
        .emotion-item {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 대화 기억/학습 시스템 데모</h1>
        
        <div class="stats-panel">
            <h3>📊 학습 통계</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="total-conversations">0</div>
                    <div class="stat-label">총 대화 수</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="most-emotion">-</div>
                    <div class="stat-label">주요 감정</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="active-hour">-</div>
                    <div class="stat-label">활발한 시간</div>
                </div>
            </div>
            <div class="emotion-chart" id="emotion-chart">
                <!-- 감정 차트가 여기 표시됩니다 -->
            </div>
        </div>
        
        <div class="chat-container" id="chat-container">
            <div class="message bot-message">
                안녕하세요! 저는 당신의 대화를 기억하고 학습하는 AI입니다. 
                무엇이든 편하게 말씀해 주세요! 😊
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="chat-input" placeholder="메시지를 입력하세요...">
            <button id="send-btn" onclick="sendMessage()">전송</button>
        </div>
    </div>

    <script>
        let conversationCount = 0;

        function updateStats(stats) {
            document.getElementById('total-conversations').textContent = stats.total_conversations || 0;
            document.getElementById('most-emotion').textContent = stats.most_common_emotion || '-';
            document.getElementById('active-hour').textContent = stats.most_active_hour ? stats.most_active_hour + '시' : '-';
            
            // 감정 차트 업데이트
            const emotionChart = document.getElementById('emotion-chart');
            emotionChart.innerHTML = '';
            
            if (stats.emotion_patterns) {
                Object.entries(stats.emotion_patterns).forEach(([emotion, count]) => {
                    const emotionItem = document.createElement('div');
                    emotionItem.className = 'emotion-item';
                    emotionItem.textContent = `${emotion}: ${count}`;
                    emotionChart.appendChild(emotionItem);
                });
            }
        }

        function addMessage(message, isUser, emotion = null) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            let content = message;
            if (emotion && !isUser) {
                content += `<span class="emotion-tag">${emotion}</span>`;
            }
            
            messageDiv.innerHTML = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // 사용자 메시지 표시
            addMessage(message, true);
            input.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error('서버 응답 오류');
                }
                
                const result = await response.json();
                
                // 봇 응답 표시
                addMessage(result.response, false, result.emotion);
                
                // 통계 업데이트
                updateStats(result.stats);
                
            } catch (error) {
                addMessage('죄송합니다. 오류가 발생했습니다: ' + error.message, false);
                console.error('Error:', error);
            }
        }

        // Enter 키로 전송
        document.getElementById('chat-input').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        // 페이지 로드 시 초기 통계 가져오기
        window.addEventListener('load', async function() {
            try {
                const response = await fetch('/stats');
                if (response.ok) {
                    const stats = await response.json();
                    updateStats(stats);
                }
            } catch (error) {
                console.error('초기 통계 로드 실패:', error);
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """메인 페이지"""
    return render_template_string(WEBAPP_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
    """채팅 API"""
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "메시지가 없습니다"}), 400

        # 감정 분석 및 학습
        emotion = memory_system.analyze_user_patterns(user_message)

        # 개인화된 응답 생성
        bot_response = memory_system.get_personalized_response(emotion, user_message)

        # 대화 기록 저장
        memory_system.add_conversation(user_message, bot_response, emotion)

        # 사용자 통계
        stats = memory_system.get_user_stats()

        return jsonify(
            {
                "response": bot_response,
                "emotion": emotion,
                "stats": stats,
                "timestamp": time.time(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats", methods=["GET"])
def get_stats():
    """통계 조회 API"""
    try:
        stats = memory_system.get_user_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clear-memory", methods=["POST"])
def clear_memory():
    """메모리 초기화 API"""
    try:
        success = memory_system.clear_memory()
        return jsonify(
            {
                "success": success,
                "message": (
                    "메모리가 초기화되었습니다" if success else "초기화에 실패했습니다"
                ),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/export-memory", methods=["GET"])
def export_memory():
    """메모리 내보내기 API"""
    try:
        stats = memory_system.get_user_stats()
        export_data = {
            "conversation_history": memory_system.conversation_history,
            "user_preferences": memory_system.user_preferences,
            "stats": stats,
            "export_time": time.time(),
        }
        return jsonify(export_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 대화 기억/학습 시스템 웹앱 시작!")
    print("📱 http://127.0.0.1:5009 에서 테스트하세요!")
    print("🧠 모든 대화가 자동으로 학습됩니다.")

    app.run(host="127.0.0.1", port=5009, debug=True)
