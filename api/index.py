# Vercel 서버리스 함수 - 확실한 인식을 위한 구조
from flask import Flask, Response, jsonify, request
import json

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    """모든 경로를 처리하는 메인 핸들러"""
    
    if path == "" or path == "index" or path == "home":
        # 메인 페이지 HTML 반환
        html_content = """<!DOCTYPE html>
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
            color: #333;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
        }
        h1 { color: #333; margin-bottom: 20px; font-size: 2.5em; }
        .goblin { font-size: 5em; margin-bottom: 20px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 20%, 50%, 80%, 100% { transform: translateY(0); } 40% { transform: translateY(-10px); } 60% { transform: translateY(-5px); } }
        p { color: #666; line-height: 1.8; margin-bottom: 15px; font-size: 1.1em; }
        .highlight { color: #667eea; font-weight: bold; }
        .chat-box {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus { border-color: #667eea; outline: none; }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: transform 0.2s;
            font-weight: bold;
        }
        button:hover { transform: translateY(-2px); }
        .response {
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            text-align: left;
            display: none;
            border-left: 4px solid #667eea;
        }
        .status { 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            background: #4CAF50; 
            color: white; 
            padding: 10px 20px; 
            border-radius: 5px; 
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="status">✅ 서버 연결됨</div>
    <div class="container">
        <div class="goblin">🧌</div>
        <h1>도깨비마을장터</h1>
        <p><span class="highlight">안녕! 나는 친근한 도깨비 AI야!</span></p>
        <p>32명의 전문가 도깨비들이 너의 질문을 기다리고 있어~</p>
        <p>무엇이든 물어봐! <strong>친근하게 답변해줄게!</strong> ✨</p>
        
        <div class="chat-box">
            <input type="text" id="userInput" placeholder="궁금한 걸 물어봐! 🤔 (예: AI에 대해 알려줘)" />
            <button onclick="sendMessage()">🧌 도깨비와 대화하기</button>
            <div id="response" class="response"></div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const responseDiv = document.getElementById('response');
            const message = input.value.trim();
            
            if (!message) {
                alert('메시지를 입력해주세요!');
                return;
            }
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '<p>🔮 도깨비가 생각 중... 잠깐만!</p>';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error('서버 응답 오류');
                }
                
                const data = await response.json();
                responseDiv.innerHTML = `
                    <p><strong>🧌 ${data.expert || '도깨비'}:</strong></p>
                    <p style="margin-top: 10px; line-height: 1.6;">${data.response}</p>
                    <p style="margin-top: 15px; font-size: 0.9em; color: #888;">📅 ${data.timestamp || new Date().toLocaleString()}</p>
                `;
            } catch (error) {
                responseDiv.innerHTML = '<p style="color: #e74c3c;">❌ 도깨비가 잠시 자리를 비웠어요... 다시 시도해주세요!</p>';
                console.error('Error:', error);
            }
            
            input.value = '';
        }
        
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // 페이지 로드 시 웰컴 메시지
        window.onload = function() {
            console.log('🧌 도깨비마을장터에 오신 것을 환영합니다!');
        };
    </script>
</body>
</html>"""
        
        return Response(html_content, mimetype='text/html; charset=utf-8')
    
    elif path == "api/chat":
        # 채팅 API 처리
        return handle_chat()
    
    else:
        # 기타 경로는 메인으로 리다이렉트
        return catch_all("")

def handle_chat():
    """채팅 처리 함수"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '데이터가 없습니다'}), 400
            
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': '메시지를 입력해주세요'}), 400
        
        # 간단한 응답 로직 (나중에 확장 가능)
        responses = {
            'ai': '안녕! 나는 AI 전문가 도깨비야! 🤖 인공지능에 대해 뭐든 물어봐!',
            '인공지능': '인공지능은 정말 재미있는 분야야! 머신러닝, 딥러닝 등 다양한 기술이 있어~',
            '안녕': '안녕! 반가워! 🧌 오늘 뭘 도와줄까?',
            '도움': '물론이야! 뭐든 물어봐! AI, 마케팅, 투자, 창업 등 32명의 전문가가 있어!'
        }
        
        # 키워드 매칭
        response_text = "안녕! 나는 도깨비야~ ✨ 아직 개발 중이라 간단히만 답할 수 있지만, 곧 완전한 기능으로 돌아올게! 🧌"
        
        for keyword, response in responses.items():
            if keyword.lower() in message.lower():
                response_text = response
                break
        
        return jsonify({
            'response': response_text,
            'expert': '친근한 도깨비',
            'timestamp': '2025-08-24',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'서버 오류: {str(e)}',
            'status': 'error'
        }), 500

# Vercel 핸들러
def handler(request):
    """Vercel serverless function handler"""
    with app.test_request_context(request.url, method=request.method):
        return app.full_dispatch_request()

# 로컬 실행용
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
