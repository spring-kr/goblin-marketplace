"""
🌌 v8.0 간단한 3D 아바타 채팅 시스템 (빠른 응답용)
"""

import matplotlib

matplotlib.use("Agg")

from flask import Flask, request, jsonify, render_template_string
import json
import base64
import io
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)


def analyze_korean_emotion(text):
    """간단한 한국어 감정 분석"""
    text = text.lower()

    if any(
        word in text
        for word in ["기분 좋", "좋아", "행복", "ㅋㅋ", "신나", "최고", "굿"]
    ):
        return "happy", 0.9
    elif any(word in text for word in ["슬프", "우울", "힘들", "안좋", "속상"]):
        return "sad", 0.8
    elif any(word in text for word in ["화나", "짜증", "열받", "빡쳐", "싫어"]):
        return "angry", 0.8
    elif any(word in text for word in ["놀라", "깜짝", "헐", "와", "대박"]):
        return "amazed", 0.7
    else:
        return "neutral", 0.6


def generate_simple_response(emotion, message):
    """간단한 응답 생성"""
    responses = {
        "happy": "😊 기분이 좋으시네요! 정말 멋져요!",
        "sad": "😢 조금 힘드시군요. 괜찮아질 거예요.",
        "angry": "😠 화가 나셨군요. 천천히 진정해보세요.",
        "amazed": "😮 정말 놀라우시겠어요!",
        "neutral": "😐 말씀해주셔서 감사합니다.",
    }
    return responses.get(emotion, "감사합니다!")


SIMPLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 빠른 3D 아바타 채팅</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            font-family: Arial, sans-serif;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 20px;
        }
        
        .chat-area {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #00ffff;
        }
        
        .avatar-area {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #00ffff;
            text-align: center;
        }
        
        #avatar-container {
            width: 100%;
            height: 300px;
            margin: 20px 0;
        }
        
        #chat-messages {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #333;
            padding: 10px;
            margin-bottom: 20px;
            background: rgba(0, 0, 0, 0.2);
        }
        
        .message {
            margin: 10px 0;
            padding: 8px;
            border-radius: 5px;
        }
        
        .user-message {
            background: #0066cc;
            text-align: right;
        }
        
        .ai-message {
            background: #006600;
        }
        
        .chat-input-area {
            display: flex;
            gap: 10px;
        }
        
        #chat-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 5px;
            background: rgba(0, 0, 0, 0.5);
            color: white;
        }
        
        #send-btn {
            padding: 10px 20px;
            background: #00ffff;
            color: black;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .emotion-display {
            margin: 10px 0;
            padding: 10px;
            background: rgba(0, 255, 255, 0.1);
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">🌌 빠른 3D 아바타 채팅</h1>
    
    <div class="container">
        <div class="chat-area">
            <h3>💬 채팅</h3>
            <div id="chat-messages">
                <div class="message ai-message">
                    <strong>🤖 AI:</strong> 안녕하세요! 메시지를 보내면 3D 아바타가 감정에 따라 변화합니다!
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="chat-input" placeholder="메시지를 입력하세요..." onkeypress="handleKeyPress(event)">
                <button id="send-btn" onclick="sendMessage()">전송</button>
            </div>
        </div>
        
        <div class="avatar-area">
            <h3>🤖 3D 아바타</h3>
            <div id="avatar-container"></div>
            <div class="emotion-display" id="emotion-display">
                감정: 대기 중...
            </div>
        </div>
    </div>

    <script>
        let scene, camera, renderer, avatarMesh;
        let isInitialized = false;

        function init3D() {
            if (isInitialized) return;
            
            const container = document.getElementById('avatar-container');
            
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 5;
            
            renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setClearColor(0x000000, 0);
            container.appendChild(renderer.domElement);
            
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            
            const pointLight = new THREE.PointLight(0xffffff, 0.8);
            pointLight.position.set(2, 2, 2);
            scene.add(pointLight);
            
            createAvatar('neutral');
            animate();
            
            isInitialized = true;
            console.log('3D 아바타 초기화 완료!');
        }

        function createAvatar(emotion) {
            if (avatarMesh) {
                scene.remove(avatarMesh);
            }
            
            const colors = {
                'happy': 0xFFD700,
                'sad': 0x4169E1,
                'angry': 0xDC143C,
                'amazed': 0xFF8C00,
                'neutral': 0xC0C0C0
            };
            
            const color = colors[emotion] || 0xC0C0C0;
            const group = new THREE.Group();
            
            // 머리
            const headGeo = new THREE.SphereGeometry(1, 32, 16);
            const headMat = new THREE.MeshPhongMaterial({ color: color });
            const head = new THREE.Mesh(headGeo, headMat);
            group.add(head);
            
            // 눈
            const eyeGeo = new THREE.SphereGeometry(0.1, 16, 8);
            const eyeMat = new THREE.MeshPhongMaterial({ color: 0x000000 });
            
            const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
            leftEye.position.set(-0.3, 0.2, 0.8);
            group.add(leftEye);
            
            const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
            rightEye.position.set(0.3, 0.2, 0.8);
            group.add(rightEye);
            
            // 감정별 입
            if (emotion === 'happy') {
                const smileGeo = new THREE.TorusGeometry(0.3, 0.05, 8, 16, Math.PI);
                const smileMat = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const smile = new THREE.Mesh(smileGeo, smileMat);
                smile.position.set(0, -0.3, 0.8);
                smile.rotation.z = Math.PI;
                group.add(smile);
            } else if (emotion === 'sad') {
                const frownGeo = new THREE.TorusGeometry(0.25, 0.05, 8, 16, Math.PI);
                const frownMat = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const frown = new THREE.Mesh(frownGeo, frownMat);
                frown.position.set(0, -0.4, 0.8);
                group.add(frown);
            } else {
                const mouthGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.3);
                const mouthMat = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const mouth = new THREE.Mesh(mouthGeo, mouthMat);
                mouth.position.set(0, -0.3, 0.8);
                mouth.rotation.z = Math.PI / 2;
                group.add(mouth);
            }
            
            avatarMesh = group;
            scene.add(avatarMesh);
        }

        function animate() {
            requestAnimationFrame(animate);
            if (avatarMesh) {
                avatarMesh.rotation.y += 0.01;
            }
            renderer.render(scene, camera);
        }

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // 사용자 메시지 표시
            addMessage(message, 'user');
            input.value = '';
            
            try {
                // 서버로 요청
                const response = await fetch('/quick-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const result = await response.json();
                
                // AI 응답 표시
                addMessage(result.response, 'ai');
                
                // 감정 표시 업데이트
                document.getElementById('emotion-display').innerHTML = 
                    `감정: ${result.emotion} (${(result.confidence * 100).toFixed(1)}%)`;
                
                // 3D 아바타 업데이트
                createAvatar(result.emotion);
                
            } catch (error) {
                console.error('Error:', error);
                addMessage('죄송합니다. 오류가 발생했습니다.', 'ai');
            }
        }

        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = `<strong>😊 사용자:</strong> ${text}`;
            } else {
                messageDiv.innerHTML = `<strong>🤖 AI:</strong> ${text}`;
            }
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', () => {
            setTimeout(init3D, 500);
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(SIMPLE_TEMPLATE)


@app.route("/quick-chat", methods=["POST"])
def quick_chat():
    """빠른 채팅 응답"""
    try:
        data = request.get_json()
        message = data.get("message", "")

        print(f"📨 받은 메시지: {message}")

        # 감정 분석
        emotion, confidence = analyze_korean_emotion(message)

        # 간단한 응답 생성
        response = generate_simple_response(emotion, message)

        print(f"🧠 감정 분석: {emotion} ({confidence:.1f})")
        print(f"💬 응답: {response}")

        return jsonify(
            {"response": response, "emotion": emotion, "confidence": confidence}
        )

    except Exception as e:
        print(f"❌ 오류: {e}")
        return (
            jsonify(
                {
                    "response": "죄송합니다. 오류가 발생했습니다.",
                    "emotion": "neutral",
                    "confidence": 0.5,
                }
            ),
            500,
        )


if __name__ == "__main__":
    print("🌌 빠른 3D 아바타 채팅 시스템 시작!")
    print("📱 http://127.0.0.1:5002 에서 테스트 가능!")
    app.run(host="127.0.0.1", port=5002, debug=True)
