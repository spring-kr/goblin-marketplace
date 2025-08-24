# Vercel 배포용 깔끔한 Flask 앱
from flask import Flask, Response, jsonify
import os

app = Flask(__name__)


@app.route("/")
def index():
    """메인 페이지"""
    html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧌 도깨비마을장터</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .goblin { font-size: 4em; margin-bottom: 20px; }
        p { color: #666; line-height: 1.6; margin-bottom: 15px; }
        .chat-box {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 16px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover { background: #5a6fd8; }
        .response {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            text-align: left;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="goblin">🧌</div>
        <h1>도깨비마을장터</h1>
        <p><strong>안녕! 나는 친근한 도깨비 AI야!</strong></p>
        <p>32명의 전문가 도깨비들이 너의 질문을 기다리고 있어~</p>
        <p>무엇이든 물어봐! 친근하게 답변해줄게! ✨</p>
        
        <div class="chat-box">
            <input type="text" id="userInput" placeholder="궁금한 걸 물어봐! 🤔" />
            <button onclick="sendMessage()">도깨비와 대화하기</button>
            <div id="response" class="response"></div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const responseDiv = document.getElementById('response');
            const message = input.value.trim();
            
            if (!message) return;
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '<p>🔮 도깨비가 생각 중...</p>';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                responseDiv.innerHTML = `
                    <p><strong>🧌 도깨비:</strong></p>
                    <p>${data.response}</p>
                `;
            } catch (error) {
                responseDiv.innerHTML = '<p>❌ 도깨비가 잠시 자리를 비웠어요... 다시 시도해주세요!</p>';
            }
            
            input.value = '';
        }
        
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
    """
    return Response(html, mimetype="text/html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """채팅 API"""
    try:
        from flask import request

        data = request.get_json()
        message = data.get("message", "")

        # 간단한 응답 로직
        response = f"안녕! 나는 도깨비야~ '{message}'에 대해 답변해줄게! 아직 개발 중이라 간단히만 답할 수 있어. 곧 완전한 기능으로 돌아올게! 🧌✨"

        return jsonify(
            {"response": response, "expert": "도깨비", "timestamp": "2025-08-24"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
