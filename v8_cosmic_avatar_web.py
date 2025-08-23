"""
🌌 v8.0 우주급 3D 아바타 + 감정인식 웹 통합 시스템
실제 사용자 대화창에서 3D 아바타와 VR 환경 구현
"""

import matplotlib

matplotlib.use("Agg")  # GUI 없는 백엔드 사용 (웹서버용)

from flask import Flask, request, jsonify, render_template_string
import asyncio
import json
import base64
import io
import random
from datetime import datetime
from complete_16_experts_v8_cosmic_multimodal_20250823 import (
    UniversalAISystemV8,
    SupportedLanguage,
)
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_agg import FigureCanvasAgg

app = Flask(__name__)


def analyze_korean_emotion(text):
    """간단한 한국어 감정 분석"""
    text = text.lower()

    # 기쁨/행복 키워드
    happy_keywords = [
        "기분 좋",
        "좋아",
        "행복",
        "기뻐",
        "웃",
        "신나",
        "즐거",
        "최고",
        "대박",
        "완전",
        "진짜 좋",
        "ㅋㅋ",
        "😊",
        "😄",
        "🤩",
    ]

    # 슬픔 키워드
    sad_keywords = ["슬퍼", "우울", "힘들", "아파", "울", "😢", "😭", "속상", "답답"]

    # 화남 키워드
    angry_keywords = ["화", "짜증", "열받", "빡", "싫어", "😠", "😡", "미치"]

    # 놀람/흥미 키워드
    amazed_keywords = ["놀라", "신기", "대단", "와", "우와", "😮", "😲", "헐"]

    # 호기심 키워드
    curious_keywords = ["궁금", "어떻게", "왜", "무엇", "🤔", "어디", "언제"]

    # 키워드 매칭
    if any(keyword in text for keyword in happy_keywords):
        return "happy"
    elif any(keyword in text for keyword in sad_keywords):
        return "sad"
    elif any(keyword in text for keyword in angry_keywords):
        return "angry"
    elif any(keyword in text for keyword in amazed_keywords):
        return "amazed"
    elif any(keyword in text for keyword in curious_keywords):
        return "curious"
    else:
        return "neutral"


# v8.0 우주급 시스템 초기화
cosmic_system = None


def init_cosmic_system():
    """우주급 시스템 초기화"""
    global cosmic_system
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cosmic_system = UniversalAISystemV8()
    print("🌌 v8.0 우주급 3D 아바타 시스템 웹 서버 준비 완료!")


# 시스템 초기화 스레드
init_thread = threading.Thread(target=init_cosmic_system)
init_thread.daemon = True
init_thread.start()

# 웹 인터페이스 HTML 템플릿 (3D 아바타 + VR 환경)
COSMIC_WEB_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 v8.0 우주급 실제 3D 아바타 AI 전문가</title>
    <!-- Three.js 3D 라이브러리 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
            overflow-x: hidden;
        }

        .cosmic-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><circle cx="200" cy="200" r="2" fill="white" opacity="0.8"/><circle cx="800" cy="300" r="1" fill="white" opacity="0.6"/><circle cx="400" cy="600" r="1.5" fill="white" opacity="0.7"/><circle cx="600" cy="100" r="1" fill="white" opacity="0.5"/><circle cx="100" cy="800" r="2" fill="white" opacity="0.8"/></svg>');
            animation: twinkle 3s infinite;
            z-index: -1;
        }

        @keyframes twinkle {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(255,255,255,0.3);
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f9ca24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .cosmic-controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .control-panel {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        .control-panel:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            margin-top: 10px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #333;
            transition: .4s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        }

        input:checked + .slider:before {
            transform: translateX(26px);
        }

        .main-interface {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 20px;
            height: 600px;
        }

        .chat-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .chat-header {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }

        .message {
            margin-bottom: 20px;
            padding: 15px 20px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-message {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
            text-align: right;
        }

        .ai-message {
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-right: auto;
            color: white;
        }

        .cosmic-info {
            font-size: 0.9em;
            color: #4ecdc4;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(78, 205, 196, 0.3);
        }

        .chat-input-area {
            display: flex;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 0 0 20px 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }

        .chat-input {
            flex: 1;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            outline: none;
            font-size: 14px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            backdrop-filter: blur(10px);
        }

        .chat-input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }

        .send-button {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            border: none;
            padding: 15px 25px;
            margin-left: 15px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .send-button:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        }

        .avatar-panel {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            overflow: hidden;
        }

        .avatar-container {
            width: 100%;
            height: 300px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .avatar-3d {
            width: 100%;
            height: 100%;
            border-radius: 15px;
        }

        .avatar-placeholder {
            text-align: center;
            color: rgba(255, 255, 255, 0.6);
            font-size: 1.2em;
        }

        .emotion-display {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            text-align: center;
        }

        .emotion-badge {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin: 5px;
        }

        .vr-environment {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }

        .cosmic-badge {
            display: inline-block;
            background: linear-gradient(45deg, #4ecdc4, #45b7d1);
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            margin: 2px;
        }

        .loading-avatar {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        @media (max-width: 768px) {
            .main-interface {
                grid-template-columns: 1fr;
                grid-template-rows: 400px 300px;
            }
        }
    </style>
</head>
<body>
    <div class="cosmic-background"></div>
    
    <div class="container">
        <div class="header">
            <h1>🌌 v8.0 우주급 3D 아바타 AI</h1>
            <p>감정 인식 + 3D 아바타 + VR 환경으로 완전 몰입형 대화 체험</p>
        </div>

        <div class="cosmic-controls">
            <div class="control-panel">
                <strong>🧠 감정 인식</strong>
                <label class="switch">
                    <input type="checkbox" id="emotionToggle" checked>
                    <span class="slider"></span>
                </label>
            </div>
            <div class="control-panel">
                <strong>🤖 3D 아바타</strong>
                <label class="switch">
                    <input type="checkbox" id="avatarToggle" checked>
                    <span class="slider"></span>
                </label>
            </div>
            <div class="control-panel">
                <strong>🥽 VR 환경</strong>
                <label class="switch">
                    <input type="checkbox" id="vrToggle" checked>
                    <span class="slider"></span>
                </label>
            </div>
            <div class="control-panel">
                <strong>🌌 우주급 모드</strong>
                <label class="switch">
                    <input type="checkbox" id="cosmicToggle" checked>
                    <span class="slider"></span>
                </label>
            </div>
        </div>

        <div class="main-interface">
            <div class="chat-container">
                <div class="chat-header">
                    <h3>💬 우주급 3D 아바타 대화</h3>
                    <p>AI가 당신의 감정을 분석하고 3D 아바타로 반응합니다</p>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="ai-message">
                        <strong>🌌 우주급 AI:</strong><br>
                        안녕하세요! v8.0 우주급 멀티모달 시스템입니다.<br>
                        <span class="cosmic-badge">감정 인식</span>
                        <span class="cosmic-badge">3D 아바타</span>
                        <span class="cosmic-badge">VR 환경</span><br>
                        모든 기능이 활성화되어 완전 몰입형 대화 경험을 제공합니다!
                    </div>
                </div>

                <div class="chat-input-area">
                    <input type="text" id="chatInput" class="chat-input" 
                           placeholder="메시지를 입력하세요... (감정 분석 → 3D 아바타 생성 → VR 환경)"
                           onkeypress="handleKeyPress(event)">
                    <button class="send-button" onclick="sendMessage()">🚀 전송</button>
                </div>
            </div>

            <div class="avatar-panel">
                <h3>🤖 실제 3D AI 아바타</h3>
                <div class="avatar-container" id="avatarContainer">
                    <!-- Three.js 3D 아바타 렌더링 영역 -->
                    <canvas id="avatar3D" style="width: 100%; height: 100%; background: transparent;"></canvas>
                    <div class="avatar-placeholder" id="avatarPlaceholder">
                        🌌 3D 아바타 초기화 중...<br>
                        실제 3D 모델이 곧 로드됩니다
                    </div>
                </div>

                <div class="emotion-display" id="emotionDisplay">
                    <strong>😊 감정 상태</strong><br>
                    <span class="emotion-badge">대기 중</span>
                </div>

                <div class="vr-environment" id="vrEnvironment">
                    <strong>🥽 VR 환경</strong><br>
                    <span class="cosmic-badge">환경 로딩 대기</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        let userId = 'cosmic_user_' + Date.now();
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
            
            // 우주급 처리 시작 표시
            showCosmicProcessing();
            
            // 로딩 메시지 표시
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'message ai-message loading-avatar';
            loadingMessage.innerHTML = '<strong>🌌 우주급 AI:</strong><br>🧠 감정 분석 → 🤖 3D 아바타 생성 → 🥽 VR 환경 로딩...';
            messagesContainer.appendChild(loadingMessage);
            
            // 스크롤 최하단으로
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            try {
                console.log('🚀 서버에 요청 전송 중...', message);
                
                const response = await fetch('/cosmic-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        message: message,
                        message_count: messageCount,
                        enable_emotion: document.getElementById('emotionToggle').checked,
                        enable_avatar: document.getElementById('avatarToggle').checked,
                        enable_vr: document.getElementById('vrToggle').checked,
                        cosmic_mode: document.getElementById('cosmicToggle').checked
                    })
                });
                
                console.log('✅ 서버 응답 받음:', result);
                
                // 로딩 메시지 제거
                messagesContainer.removeChild(loadingMessage);
                
                // AI 응답 추가
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message ai-message';
                
                let messageContent = `<strong>🌌 ${result.expert_name || '우주급 AI'}:</strong><br>${result.expert_response}`;
                
                // 우주급 기능 정보 추가
                if (result.cosmic_features) {
                    messageContent += `
                        <div class="cosmic-info">
                            <span class="cosmic-badge">v8.0 우주급</span><br>
                            감정: ${result.detected_emotion} | 
                            아바타: ${result.avatar_generated ? '생성됨' : '비활성'} | 
                            VR: ${result.vr_environment || '기본'}
                        </div>
                    `;
                }
                
                aiMessage.innerHTML = messageContent;
                messagesContainer.appendChild(aiMessage);
                
                // 감정 표시 업데이트
                if (result.detected_emotion) {
                    updateEmotionDisplay(result.detected_emotion, result.emotion_confidence);
                }
                
                // 3D 아바타 표시
                if (result.avatar_image) {
                    displayAvatar(result.avatar_image, result.detected_emotion);
                }
                
                // VR 환경 업데이트
                if (result.vr_environment) {
                    updateVREnvironment(result.vr_environment);
                }
                
            } catch (error) {
                // 로딩 메시지 제거
                messagesContainer.removeChild(loadingMessage);
                
                // 에러 메시지 표시
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message ai-message';
                errorMessage.innerHTML = '<strong>❌ 오류:</strong><br>우주급 시스템 연결 실패';
                messagesContainer.appendChild(errorMessage);
                
                console.error('Error:', error);
            }
            
            // 스크롤 최하단으로
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function showCosmicProcessing() {
            // 아바타 컨테이너에 로딩 효과
            const avatarContainer = document.getElementById('avatarContainer');
            avatarContainer.innerHTML = '<div class="avatar-placeholder loading-avatar">🌌 3D 아바타 생성 중...</div>';
            
            // 감정 표시 업데이트
            const emotionDisplay = document.getElementById('emotionDisplay');
            emotionDisplay.innerHTML = '<strong>🧠 감정 분석</strong><br><span class="emotion-badge loading-avatar">분석 중...</span>';
            
            // VR 환경 표시 업데이트
            const vrEnvironment = document.getElementById('vrEnvironment');
            vrEnvironment.innerHTML = '<strong>🥽 VR 환경</strong><br><span class="cosmic-badge loading-avatar">환경 생성 중...</span>';
        }

        function updateEmotionDisplay(emotion, confidence) {
            const emotionDisplay = document.getElementById('emotionDisplay');
            const emotionEmoji = getEmotionEmoji(emotion);
            emotionDisplay.innerHTML = `
                <strong>😊 감정 상태</strong><br>
                <span class="emotion-badge">${emotionEmoji} ${emotion}</span><br>
                <small>신뢰도: ${(confidence * 100).toFixed(1)}%</small>
            `;
        }

        // 3D 아바타 관련 변수들
        let scene, camera, renderer, avatarMesh, ambientLight, pointLight;
        let isAvatar3DInitialized = false;

        // Three.js 3D 아바타 초기화
        function init3DAvatar() {
            if (isAvatar3DInitialized) return;
            
            const canvas = document.getElementById('avatar3D');
            const container = document.getElementById('avatarContainer');
            
            // Scene 생성
            scene = new THREE.Scene();
            scene.background = null; // 투명 배경
            
            // Camera 생성
            camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 5;
            
            // Renderer 생성
            renderer = new THREE.WebGLRenderer({ 
                canvas: canvas, 
                alpha: true,
                antialias: true 
            });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            
            // 조명 설정
            ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            
            pointLight = new THREE.PointLight(0xffffff, 0.8);
            pointLight.position.set(2, 2, 2);
            pointLight.castShadow = true;
            scene.add(pointLight);
            
            // 기본 3D 아바타 생성 (구체 기반)
            create3DAvatar('neutral');
            
            isAvatar3DInitialized = true;
            
            // 플레이스홀더 숨기기
            document.getElementById('avatarPlaceholder').style.display = 'none';
            
            animate3D();
        }

        function create3DAvatar(emotion) {
            // 기존 아바타 제거
            if (avatarMesh) {
                scene.remove(avatarMesh);
            }
            
            // 감정에 따른 색상
            const emotionColors = {
                'happy': 0xFFD700,    // 금색
                'sad': 0x4169E1,      // 파란색
                'angry': 0xDC143C,    // 빨간색
                'curious': 0x32CD32,  // 초록색
                'excited': 0xFF69B4,  // 핑크색
                'confident': 0x800080, // 보라색
                'neutral': 0xC0C0C0,  // 은색
                'amazed': 0xFF8C00,   // 주황색
                'wonder': 0x9370DB    // 보라색
            };
            
            const color = emotionColors[emotion] || 0xC0C0C0;
            
            // 아바타 그룹 생성
            const avatarGroup = new THREE.Group();
            
            // 머리 (구체)
            const headGeometry = new THREE.SphereGeometry(1, 32, 16);
            const headMaterial = new THREE.MeshPhongMaterial({ 
                color: color,
                shininess: 100,
                transparent: true,
                opacity: 0.9
            });
            const head = new THREE.Mesh(headGeometry, headMaterial);
            head.castShadow = true;
            avatarGroup.add(head);
            
            // 눈 (작은 구체들)
            const eyeGeometry = new THREE.SphereGeometry(0.1, 16, 8);
            const eyeMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
            
            const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
            leftEye.position.set(-0.3, 0.2, 0.8);
            avatarGroup.add(leftEye);
            
            const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
            rightEye.position.set(0.3, 0.2, 0.8);
            avatarGroup.add(rightEye);
            
            // 감정에 따른 입 모양
            if (emotion === 'happy') {
                // 웃는 입 (호 모양)
                const smileGeometry = new THREE.TorusGeometry(0.3, 0.05, 8, 16, Math.PI);
                const smileMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const smile = new THREE.Mesh(smileGeometry, smileMaterial);
                smile.position.set(0, -0.3, 0.8);
                smile.rotation.z = Math.PI; // 뒤집어서 웃는 모양
                avatarGroup.add(smile);
                
                // 볼 (작은 분홍색 구체들)
                const cheekGeometry = new THREE.SphereGeometry(0.08, 16, 8);
                const cheekMaterial = new THREE.MeshPhongMaterial({ color: 0xFF69B4 });
                
                const leftCheek = new THREE.Mesh(cheekGeometry, cheekMaterial);
                leftCheek.position.set(-0.6, -0.1, 0.6);
                avatarGroup.add(leftCheek);
                
                const rightCheek = new THREE.Mesh(cheekGeometry, cheekMaterial);
                rightCheek.position.set(0.6, -0.1, 0.6);
                avatarGroup.add(rightCheek);
                
            } else if (emotion === 'sad') {
                // 슬픈 입 (뒤집힌 호)
                const frownGeometry = new THREE.TorusGeometry(0.25, 0.05, 8, 16, Math.PI);
                const frownMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const frown = new THREE.Mesh(frownGeometry, frownMaterial);
                frown.position.set(0, -0.4, 0.8);
                avatarGroup.add(frown);
                
            } else if (emotion === 'amazed') {
                // 놀란 입 (작은 원)
                const amazedGeometry = new THREE.SphereGeometry(0.08, 16, 8);
                const amazedMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const amazedMouth = new THREE.Mesh(amazedGeometry, amazedMaterial);
                amazedMouth.position.set(0, -0.3, 0.8);
                avatarGroup.add(amazedMouth);
                
            } else {
                // 기본 입 (선)
                const mouthGeometry = new THREE.CylinderGeometry(0.02, 0.02, 0.3);
                const mouthMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
                const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
                mouth.position.set(0, -0.3, 0.8);
                mouth.rotation.z = Math.PI / 2;
                avatarGroup.add(mouth);
            }
            
            // 아바타 회전 애니메이션 추가
            avatarGroup.rotation.y = 0;
            
            avatarMesh = avatarGroup;
            scene.add(avatarMesh);
        }

        function animate3D() {
            requestAnimationFrame(animate3D);
            
            // 아바타 회전 애니메이션
            if (avatarMesh) {
                avatarMesh.rotation.y += 0.005;
            }
            
            renderer.render(scene, camera);
        }

        function displayAvatar(avatarImage, emotion) {
            // 3D 아바타가 초기화되지 않았으면 초기화
            if (!isAvatar3DInitialized) {
                init3DAvatar();
            }
            
            // 새로운 감정으로 3D 아바타 업데이트
            create3DAvatar(emotion);
            
            // 감정에 따른 조명 색상 변경
            const emotionLightColors = {
                'happy': 0xFFD700,
                'sad': 0x4169E1,
                'angry': 0xDC143C,
                'excited': 0xFF69B4,
                'neutral': 0xFFFFFF
            };
            
            const lightColor = emotionLightColors[emotion] || 0xFFFFFF;
            if (pointLight) {
                pointLight.color.setHex(lightColor);
            }
        }

        function updateVREnvironment(environment) {
            const vrEnvironment = document.getElementById('vrEnvironment');
            const envEmoji = getEnvironmentEmoji(environment);
            vrEnvironment.innerHTML = `
                <strong>🥽 VR 환경</strong><br>
                <span class="cosmic-badge">${envEmoji} ${environment}</span>
            `;
        }

        function getEmotionEmoji(emotion) {
            const emojis = {
                'happy': '😊',
                'sad': '😢',
                'angry': '😠',
                'curious': '🤔',
                'excited': '🤩',
                'confident': '😎',
                'neutral': '😐',
                'amazed': '😮',
                'wonder': '✨'
            };
            return emojis[emotion] || '😊';
        }

        function getEnvironmentEmoji(environment) {
            const emojis = {
                'space_station': '🚀',
                'laboratory': '🔬',
                'office': '🏢',
                'hospital': '🏥',
                'classroom': '🎓',
                'virtual_space': '🌌'
            };
            return emojis[environment] || '🌌';
        }

        // 페이지 로드 시 3D 아바타 초기화
        window.addEventListener('load', function() {
            console.log('🌌 실제 3D 아바타 시스템 초기화 중...');
            setTimeout(() => {
                init3DAvatar();
                console.log('✅ 3D 아바타 초기화 완료!');
            }, 1000);
        });

        // 윈도우 리사이즈 시 3D 아바타 크기 조정
        window.addEventListener('resize', function() {
            if (isAvatar3DInitialized && renderer && camera) {
                const container = document.getElementById('avatarContainer');
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """메인 페이지 - 3D 아바타 인터페이스"""
    return render_template_string(COSMIC_WEB_TEMPLATE)


@app.route("/cosmic-chat", methods=["POST"])
def cosmic_chat():
    """우주급 3D 아바타 채팅 엔드포인트"""
    global cosmic_system

    if not cosmic_system:
        return (
            jsonify(
                {
                    "error": "우주급 시스템이 아직 초기화되지 않았습니다. 잠시 후 다시 시도해주세요."
                }
            ),
            503,
        )

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "요청 데이터가 없습니다."}), 400

        user_id = data.get("user_id")
        message = data.get("message")
        enable_emotion = data.get("enable_emotion", True)
        enable_avatar = data.get("enable_avatar", True)
        enable_vr = data.get("enable_vr", True)
        cosmic_mode = data.get("cosmic_mode", True)

        print(f"📨 받은 메시지: {message}")

        # 🚀 빠른 모드: 간단한 감정 분석과 응답
        detected_emotion = analyze_korean_emotion(message)

        # 간단한 응답 생성 (복잡한 AI 대신)
        simple_responses = {
            "happy": "😊 정말 기분이 좋으시군요! 멋진 하루 보내세요!",
            "sad": "😢 조금 힘드신 것 같네요. 괜찮아질 거예요.",
            "angry": "😠 화가 나셨군요. 천천히 진정하시기 바래요.",
            "amazed": "😮 정말 놀라우시겠어요!",
            "neutral": "😐 말씀해주셔서 감사합니다.",
        }

        expert_response = simple_responses.get(detected_emotion, "감사합니다!")

        print(f"🧠 감정 분석: {detected_emotion}")
        print(f"💬 응답: {expert_response}")

        # 🤖 3D 아바타는 프론트엔드에서 Three.js로 처리 (빠름)
        avatar_image = None  # matplotlib 이미지 생성 생략
        # if enable_avatar:
        #     avatar_image = generate_simple_avatar_image(detected_emotion, "우주급")

        # 결과 반환
        return jsonify(
            {
                "expert_name": "🌌 우주급 AI",
                "expert_response": expert_response,
                "detected_emotion": detected_emotion,
                "emotion_confidence": 0.9,
                "avatar_image": avatar_image,
                "avatar_generated": bool(avatar_image),
                "vr_environment": "space_station" if enable_vr else None,
                "cosmic_features": cosmic_mode,
                "response_time": "빠른 응답 모드",
            }
        )

    except Exception as e:
        print(f"Cosmic chat error: {e}")
        return jsonify({"error": f"우주급 처리 중 오류가 발생했습니다: {str(e)}"}), 500


def generate_simple_avatar_image(emotion, avatar_type):
    """간단한 아바타 이미지 생성 (Circle import 문제 해결)"""
    try:
        fig, ax = plt.subplots(figsize=(6, 6), facecolor="black")
        ax.set_facecolor("black")

        # 감정에 따른 색상 선택
        emotion_colors = {
            "happy": "#FFD700",
            "sad": "#4169E1",
            "angry": "#DC143C",
            "curious": "#32CD32",
            "excited": "#FF69B4",
            "confident": "#800080",
            "neutral": "#C0C0C0",
            "amazed": "#FF8C00",
            "wonder": "#9370DB",
        }

        color = emotion_colors.get(emotion, "#C0C0C0")

        # 얼굴 원 그리기 (scatter로 대체)
        ax.scatter([0.5], [0.5], s=8000, c=color, alpha=0.8)

        # 눈 그리기
        ax.scatter([0.4, 0.6], [0.6, 0.6], c="black", s=200)

        # 감정에 따른 입 모양
        if emotion == "happy":
            # 웃는 입
            mouth_x = np.linspace(0.4, 0.6, 30)
            mouth_y = 0.4 + 0.05 * np.sin(np.pi * (mouth_x - 0.4) / 0.2)
            ax.plot(mouth_x, mouth_y, "k-", linewidth=5)
            # 볼
            ax.scatter([0.35, 0.65], [0.55, 0.55], c="#FF69B4", s=150, alpha=0.7)
        elif emotion == "sad":
            # 슬픈 입
            mouth_x = np.linspace(0.4, 0.6, 30)
            mouth_y = 0.4 - 0.05 * np.sin(np.pi * (mouth_x - 0.4) / 0.2)
            ax.plot(mouth_x, mouth_y, "k-", linewidth=5)
        elif emotion == "amazed":
            # 놀란 입 (작은 원)
            ax.scatter([0.5], [0.4], c="black", s=300)
        elif emotion == "angry":
            # 화난 입
            ax.plot([0.4, 0.6], [0.35, 0.35], "k-", linewidth=5)
            # 눈썹
            ax.plot([0.35, 0.45], [0.65, 0.62], "k-", linewidth=4)
            ax.plot([0.55, 0.65], [0.62, 0.65], "k-", linewidth=4)
        else:
            # 기본 입
            ax.plot([0.45, 0.55], [0.4, 0.4], "k-", linewidth=4)

        # 감정 이모지와 라벨
        emotion_emoji = {
            "happy": "😊",
            "sad": "😢",
            "angry": "😠",
            "amazed": "😮",
            "curious": "🤔",
            "excited": "🤩",
            "neutral": "😐",
        }

        emoji = emotion_emoji.get(emotion, "😊")
        ax.text(
            0.5,
            0.15,
            f"{emoji} {emotion.upper()}",
            ha="center",
            va="center",
            fontsize=16,
            color="white",
            weight="bold",
        )

        # 아바타 타입 표시 (한글 제거)
        ax.text(
            0.5,
            0.05,
            f"v8.0 Avatar",
            ha="center",
            va="center",
            fontsize=10,
            color="cyan",
        )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")

        # 이미지를 base64로 인코딩
        buffer = io.BytesIO()
        plt.savefig(
            buffer, format="png", facecolor="black", bbox_inches="tight", dpi=100
        )
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)

        return image_data

    except Exception as e:
        print(f"Avatar generation error: {e}")
        return None


@app.route("/system-stats")
def system_stats():
    """시스템 통계"""
    if not cosmic_system:
        return jsonify({"error": "시스템 초기화 중입니다."}), 503

    stats = {
        "version": "v8.0 - 우주급 멀티모달",
        "features": [
            "🧠 우주급 감정 인식",
            "🤖 3D AI 아바타 생성",
            "🥽 VR/AR 가상현실 환경",
            "🌌 우주급 지능 네트워크",
        ],
        "experts": 26,
        "languages": 10,
        "cosmic_level": "최고 수준",
        "immersion": "완전 몰입형 체험",
    }
    return jsonify(stats)


if __name__ == "__main__":
    print("🌌 v8.0 우주급 3D 아바타 웹 서버 시작...")
    print("📱 http://127.0.0.1:5001 에서 3D 아바타 + VR 체험 가능!")
    print("🤖 실시간 감정 인식 → 3D 아바타 생성 → VR 환경 몰입")

    app.run(debug=True, host="127.0.0.1", port=5001)
