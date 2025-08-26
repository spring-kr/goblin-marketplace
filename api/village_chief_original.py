from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# 전역 변수
conversation_memory = {}
user_profiles = {}
context_depth = 5


def master_analyze_user_message(message, conversation_id):
    """원본 촌장 시스템의 마스터급 사용자 메시지 분석"""

    # 전문적인 키워드 확인
    professional_keywords = [
        # 아이디어 생성 관련
        "아이디어",
        "생성",
        "만들어",
        "제작",
        "개발",
        "디자인",
        "창작",
        "기획",
        "구상",
        "발상",
        "계획",
        "설계",
        "구축",
        "작성",
        "완성",
        "실행",
        # 비즈니스 관련
        "스타트업",
        "투자",
        "경영",
        "전략",
        "마케팅",
        "비즈니스",
        "사업",
        "회사",
        "기업",
        "창업",
        "브랜딩",
        "매출",
        "수익",
        "성장",
        "융자",
        "펀딩",
        "벤처",
        "창업자",
        "nps",
        "스코어",
        "지표",
        "kpi",
        "roi",
        "고객",
        "만족도",
        "추천",
        "재구매",
        "mvp",
        "pmf",
        "cac",
        "ltv",
        # 기술 관련
        "기술",
        "소프트웨어",
        "시스템",
        "프로그래밍",
        "알고리즘",
        "데이터",
        "AI",
        "머신러닝",
        "클라우드",
        "보안",
        "네트워크",
        "앱",
        "웹",
        "플랫폼",
    ]

    message_lower = message.lower()
    detected_keywords = [
        keyword for keyword in professional_keywords if keyword in message_lower
    ]

    # 의도 분석
    intent = "general"
    if any(kw in message_lower for kw in ["아이디어", "생성", "만들어"]):
        intent = "idea_generation"
    elif any(kw in message_lower for kw in ["비즈니스", "사업", "창업"]):
        intent = "business_consultation"
    elif any(kw in message_lower for kw in ["마케팅", "홍보", "광고"]):
        intent = "marketing_strategy"
    elif any(kw in message_lower for kw in ["안녕", "hello", "hi"]):
        intent = "greeting"

    # 감정 분석
    emotion = "neutral"
    if any(kw in message_lower for kw in ["좋아", "감사", "고마워", "만족"]):
        emotion = "positive"
    elif any(kw in message_lower for kw in ["문제", "어려워", "힘들어", "안돼"]):
        emotion = "negative"
    elif any(kw in message_lower for kw in ["궁금", "알고싶어", "배우고싶어"]):
        emotion = "curious"

    return {
        "detected_keywords": detected_keywords,
        "intent": intent,
        "emotion": emotion,
        "urgency": "medium",
        "domain": "general",
        "complexity": len(message.split()),
        "language_style": "formal" if "습니다" in message else "casual",
    }


def generate_master_response(message, analysis, conversation_id):
    """원본 촌장 시스템의 응답 생성"""

    intent = analysis.get("intent", "general")
    emotion = analysis.get("emotion", "neutral")
    detected_keywords = analysis.get("detected_keywords", [])

    # 감정에 따른 인사말
    if emotion == "positive":
        greeting = "호호! 좋은 기운이 느껴지는군요! "
    elif emotion == "negative":
        greeting = "어허, 뭔가 고민이 있어 보이는구나. "
    elif emotion == "curious":
        greeting = "오호! 궁금한 게 많은 분이군요! "
    else:
        greeting = "어서 오게나! "

    # 의도별 응답 생성
    if intent == "idea_generation":
        return f"""{greeting}아이디어 생성이라고? 이 촌장이 직접 나서겠다네!

🎯 어떤 분야의 아이디어가 필요한가?
• 📊 비즈니스 아이디어 - 돈 되는 사업 아이템이지!
• 💡 창업 아이템 - 젊은이들 창업할 때 좋은 것들이야
• 📱 앱/서비스 아이디어 - 요즘 세상은 다 앱이더라고
• 🎨 창작/콘텐츠 아이디어 - 재미있는 걸 만들어보자꾸나
• 🔧 문제해결 아이디어 - 골치 아픈 문제를 해결해주지

구체적으로 말해보게나, 이 촌장이 속시원히 도와주겠다네! 크하하!"""

    elif intent == "business_consultation":
        return f"""{greeting}사업 이야기인가? 이 촌장이 마을에서 장사도 해봤거든!

💼 촌장의 비즈니스 비법을 전수하겠다네:
• 📈 사업계획서 - 제대로 된 계획이 반이야!
• 💰 투자유치 - 돈 구하는 법도 알려주지
• 📊 시장분석 - 어디서 장사해야 잘 되는지 말이야
• 🎯 마케팅 전략 - 손님 끌어오는 방법이지!
• 📋 사업모델 - 어떻게 돈을 벌 것인가?

뭐부터 도와달라는 건가? 촌장이 다 알려주겠다네!"""

    elif intent == "marketing_strategy":
        return f"""{greeting}홍보와 마케팅 말인가? 촌장이 마을 축제도 홍보해봤다네!

📢 촌장의 마케팅 노하우:
• 🎯 손님 찾기 - 누가 우리 고객인지 알아야지
• 📱 SNS 마케팅 - 요즘엔 인터넷으로 다 하더라고
• 💡 홍보 아이디어 - 사람들 눈길 끌 방법들 말이야
• 🏷️ 브랜드 이름 - 기억하기 쉬운 이름이 좋지!
• 📊 성과 측정 - 얼마나 잘 됐는지 봐야 하거든

어떤 걸 도와달라는 건가? 촌장이 속시원히 알려주지!"""

    elif intent == "greeting":
        return f"""{greeting}나는 이 마을의 촌장도깨비라네!

🏘️ 촌장이 도와줄 수 있는 것들:
• 🎯 아이디어 만들기 - 기발한 생각들을 짜내주지!
• 💼 사업 상담 - 장사 잘 되는 방법 알려주고
• 📊 시장 분석 - 어디가 돈 될지 알아봐주고
• 📢 홍보 전략 - 사람들한테 알리는 방법도!
• 🔧 문제 해결 - 골치 아픈 일들도 풀어주지

"아이디어 생성해줘", "사업 도와줘" 이런 식으로 편하게 말해보게나!
이 촌장이 다 해결해주겠다네! 크하하!"""

    else:
        # 감지된 키워드가 있으면 전문 응답
        if detected_keywords:
            return f"""{greeting}'{', '.join(detected_keywords[:3])}'에 대해 물어보는군요!

촌장이 이런 걸 도와줄 수 있다네:
• 🎯 아이디어 생성하기 - 기발한 생각 짜내주고
• 💼 사업 조언하기 - 돈 버는 방법 알려주고
• 📢 마케팅 전략 - 홍보하는 비법 전수해주지!

더 구체적으로 말해보게나, 예를 들어:
"카페 창업 아이디어 생성해줘" 이런 식으로 말이야!
촌장이 속시원히 해결해드리겠다네! 🎯"""

        # 일반 응답
        return f"""{greeting}'{message}'... 음, 그런 말씀이군요!

촌장이 더 잘 도와드리려면 이런 식으로 말씀해 보세요:
• "아이디어 생성해줘" - 기발한 생각 짜내드리고
• "사업 계획 도와줘" - 장사 잘 되는 방법 알려드리고  
• "마케팅 전략 짜줘" - 홍보하는 비법 전수해드리지!

예를 들면: "펫샵 창업 아이디어 생성해줘" 이런 식으로 말이야!
촌장이 속시원히 해결해드리겠다네! 크하하!"""


def update_conversation_memory(conversation_id, message, sender):
    """대화 메모리 업데이트"""
    if conversation_id not in conversation_memory:
        conversation_memory[conversation_id] = []

    conversation_memory[conversation_id].append(
        {"sender": sender, "message": message, "timestamp": datetime.now().isoformat()}
    )

    # 메모리 크기 제한
    if len(conversation_memory[conversation_id]) > context_depth * 2:
        conversation_memory[conversation_id] = conversation_memory[conversation_id][
            -context_depth * 2 :
        ]


@app.route("/")
def hello():
    return """<!DOCTYPE html>
<html>
<head>
    <title>🏘️ Village Chief System</title>
    <meta charset="utf-8">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { 
            text-align: center; 
            color: #fff; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .chat-container { 
            background: rgba(255,255,255,0.9); 
            color: #333; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
        }
        .input-group { 
            display: flex; 
            gap: 10px; 
            margin: 20px 0; 
        }
        input[type="text"] { 
            flex: 1; 
            padding: 12px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            font-size: 16px;
        }
        button { 
            padding: 12px 24px; 
            background: #4CAF50; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px;
        }
        button:hover { background: #45a049; }
        .message { 
            margin: 10px 0; 
            padding: 15px; 
            border-radius: 8px; 
            border-left: 4px solid #4CAF50;
            line-height: 1.5;
        }
        .user-message { border-left-color: #2196F3; background: #e3f2fd; }
        .ai-message { border-left-color: #4CAF50; background: #e8f5e8; }
        .ai-message strong { color: #2e7d32; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏘️ Village Chief System</h1>
        <p style="text-align: center;"><strong>촌장도깨비가 여러분을 도와드립니다!</strong></p>
        
        <div class="chat-container">
            <div id="chatHistory"></div>
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="메시지를 입력하세요... (예: 아이디어 생성해줘)" />
                <button onclick="sendMessage()">전송</button>
            </div>
        </div>
    </div>
    
    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            // 사용자 메시지 표시
            addMessage('사용자', message, 'user-message');
            input.value = '';
            
            // API 호출
            fetch('/api/master-conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('촌장도깨비', data.ai_response || '응답을 받을 수 없습니다.', 'ai-message');
            })
            .catch(error => {
                addMessage('시스템', '오류가 발생했습니다: ' + error.message, 'ai-message');
            });
        }
        
        function addMessage(sender, message, className) {
            const history = document.getElementById('chatHistory');
            const div = document.createElement('div');
            div.className = 'message ' + className;
            div.innerHTML = '<strong>' + sender + ':</strong> ' + message.replace(/\\n/g, '<br>');
            history.appendChild(div);
            history.scrollTop = history.scrollHeight;
        }
        
        // 엔터키로 전송
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        
        // 초기 메시지
        addMessage('촌장도깨비', '어서 오게나! 나는 이 마을의 촌장도깨비라네! 아이디어 생성, 사업 상담, 마케팅 전략 등 뭐든지 도와주겠다네! "아이디어 생성해줘" 이런 식으로 편하게 말해보게! 크하하! 🎯', 'ai-message');
    </script>
</body>
</html>"""


@app.route("/api/master-conversation", methods=["POST"])
def master_conversation():
    """원본 촌장 시스템의 마스터 대화 API"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        conversation_id = data.get("conversation_id", "default_session")

        # 대화 메모리 업데이트
        update_conversation_memory(conversation_id, message, "user")

        # 메시지 분석
        analysis = master_analyze_user_message(message, conversation_id)

        print(f"🔍 감지된 전문 키워드: {analysis['detected_keywords']}")
        print(f"🎯 의도: {analysis['intent']}")

        # 응답 생성
        response = generate_master_response(message, analysis, conversation_id)

        # AI 응답을 메모리에 저장
        update_conversation_memory(conversation_id, response, "ai")

        return jsonify(
            {
                "type": "마스터 AI 대화",
                "user_message": message,
                "ai_response": response,
                "analysis": analysis,
                "context_used": len(conversation_memory.get(conversation_id, [])),
                "timestamp": datetime.now().isoformat(),
                "conversation_id": conversation_id,
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "ai_response": f"어허! 뭔가 문제가 생겼다네: {str(e)}",
                    "status": "error",
                }
            ),
            500,
        )


@app.route("/api/test")
def test():
    return {
        "status": "ok",
        "message": "Village Chief 원본 시스템 정상 작동",
        "version": "촌장 오리지널",
    }


if __name__ == "__main__":
    app.run(debug=True)
