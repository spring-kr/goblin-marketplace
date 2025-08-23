"""
👤 리얼리스틱 3D 아바타 시스템 (현실적 인간형)
🧠 v10.1 대화 기억/학습 시스템 추가
"""

from flask import Flask, request, jsonify
import json
import os
import time

app = Flask(__name__)

# 🧠 대화 기억 저장소
MEMORY_FILE = "conversation_memory.json"
conversation_history = []
user_preferences = {}


def load_memory():
    """대화 기억 불러오기"""
    global conversation_history, user_preferences
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                conversation_history = data.get("history", [])
                user_preferences = data.get("preferences", {})
    except Exception as e:
        print(f"🧠 메모리 로드 실패: {e}")


def save_memory():
    """대화 기억 저장하기"""
    try:
        data = {
            "history": conversation_history[-100:],  # 최근 100개만 저장
            "preferences": user_preferences,
        }
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"🧠 메모리 저장 실패: {e}")


def analyze_user_patterns(text):
    """사용자 패턴 분석 및 학습"""
    global user_preferences

    # 감정 패턴 학습
    emotion = analyze_korean_emotion(text)
    if "emotion_patterns" not in user_preferences:
        user_preferences["emotion_patterns"] = {}

    if emotion in user_preferences["emotion_patterns"]:
        user_preferences["emotion_patterns"][emotion] += 1
    else:
        user_preferences["emotion_patterns"][emotion] = 1

    # 선호 키워드 학습
    if "favorite_words" not in user_preferences:
        user_preferences["favorite_words"] = {}

    words = text.split()
    for word in words:
        if len(word) > 1:  # 한 글자 제외
            if word in user_preferences["favorite_words"]:
                user_preferences["favorite_words"][word] += 1
            else:
                user_preferences["favorite_words"][word] = 1

    return emotion


def get_personalized_response(emotion, text):
    """개인화된 응답 생성"""
    base_responses = {
        "happy": [
            "정말 기쁘시겠어요! 😊",
            "행복한 기분이 전해져요!",
            "좋은 일이 있으셨나봐요!",
        ],
        "sad": ["힘든 시간이시군요 😢", "괜찮아질 거예요", "함께 이겨내요"],
        "angry": ["화가 나셨군요 😠", "스트레스 받으셨나봐요", "잠시 숨을 고르세요"],
        "excited": ["정말 신나시겠어요! 🤩", "저도 기대돼요!", "흥미진진하네요!"],
        "worried": [
            "걱정이 많으시겠어요 😰",
            "모든 게 잘 될 거예요",
            "너무 걱정하지 마세요",
        ],
        "tired": ["많이 피곤하시겠어요 😴", "좀 쉬세요", "무리하지 마세요"],
        "grateful": ["감사한 마음이 느껴져요 🙏", "정말 다행이네요!", "감동적이에요"],
        "confused": ["헷갈리시는군요 😕", "차근차근 생각해봐요", "복잡하시겠어요"],
        "confident": ["자신감이 넘치시네요! 😎", "멋져요!", "당당하세요!"],
        "shy": ["부끄러워하시는군요 😊", "괜찮아요", "천천히 말씀하세요"],
        "love": ["사랑스러운 마음이 느껴져요 💕", "따뜻해요", "마음이 예뻐요"],
        "amazed": ["정말 놀라우시겠어요! 😲", "대단하네요!", "신기해요!"],
    }

    responses = base_responses.get(emotion, ["그렇군요", "이해해요", "말씀해주세요"])

    # 사용자 패턴 기반 개인화
    if "emotion_patterns" in user_preferences:
        most_common_emotion = max(
            user_preferences["emotion_patterns"],
            key=user_preferences["emotion_patterns"].get,
        )

        # 자주 사용하는 감정에 따라 응답 스타일 조정
        if most_common_emotion == "happy":
            responses = [r + " 항상 긍정적이시네요!" for r in responses]
        elif most_common_emotion == "sad":
            responses = [r + " 힘내세요!" for r in responses]

    return responses[0]  # 첫 번째 응답 반환


# 앱 시작 시 메모리 로드
load_memory()


def analyze_korean_emotion(text):
    """🧠 v10.0 확장된 30가지 감정 분석 시스템"""
    text = text.lower()

    # 1. 기쁨/행복 계열
    if any(
        word in text
        for word in [
            "기분 좋",
            "좋아",
            "행복",
            "기뻐",
            "즐거",
            "신나",
            "최고",
            "완벽",
            "멋져",
            "환상적",
            "대단해",
            "훌륭",
            "ㅋㅋ",
            "하하",
            "웃",
            "만족",
            "성공",
            "이루었",
            "사랑해",
        ]
    ):
        return "happy"

    # 2. 슬픔/우울 계열
    elif any(
        word in text
        for word in [
            "슬프",
            "우울",
            "힘들",
            "안좋",
            "속상",
            "눈물",
            "서러",
            "외로",
            "공허",
            "실망",
            "좌절",
            "막막",
            "암울",
            "절망",
            "비참",
            "처참",
        ]
    ):
        return "sad"

    # 3. 분노/짜증 계열
    elif any(
        word in text
        for word in [
            "화나",
            "짜증",
            "열받",
            "빡쳐",
            "분노",
            "악",
            "미치",
            "싫어",
            "스트레스",
            "답답",
            "빡",
            "어이없",
            "황당",
            "미친",
            "개빡",
            "쪽팔",
        ]
    ):
        return "angry"

    # 4. 놀람/감탄 계열
    elif any(
        word in text
        for word in [
            "놀라",
            "깜짝",
            "헐",
            "와",
            "대박",
            "신기",
            "믿을 수 없",
            "어떻게",
            "세상에",
            "어머",
            "헉",
            "우와",
            "와우",
            "까무러",
        ]
    ):
        return "amazed"

    # 5. 사랑/애정 계열
    elif any(
        word in text
        for word in [
            "사랑",
            "좋아해",
            "애정",
            "마음에 들",
            "예뻐",
            "귀여",
            "달콤",
            "포근",
            "따뜻",
            "감동",
            "고마워",
            "소중",
            "아끼",
        ]
    ):
        return "love"

    # 6. 흥미진진/기대 계열
    elif any(
        word in text
        for word in [
            "흥미",
            "기대",
            "설레",
            "두근",
            "궁금",
            "재미",
            "호기심",
            "즐거운",
            "기다려",
            "관심",
            "몰입",
        ]
    ):
        return "excited"

    # 7. 걱정/불안 계열
    elif any(
        word in text
        for word in [
            "걱정",
            "불안",
            "무서",
            "두려",
            "염려",
            "근심",
            "긴장",
            "떨려",
            "조마조마",
            "심난",
            "겁나",
            "무시무시",
        ]
    ):
        return "worried"

    # 8. 피곤/지침 계열
    elif any(
        word in text
        for word in [
            "피곤",
            "지쳐",
            "힘빠져",
            "나른",
            "졸려",
            "번아웃",
            "탈진",
            "기운없",
            "지겨",
            "권태",
            "무기력",
            "귀찮",
        ]
    ):
        return "tired"

    # 9. 감사/고마움 계열
    elif any(
        word in text
        for word in [
            "감사",
            "고마워",
            "고맙",
            "땡큐",
            "은혜",
            "축복",
            "다행",
            "고마운",
            "진심",
            "깊이",
        ]
    ):
        return "grateful"

    # 10. 혼란/당황 계열
    elif any(
        word in text
        for word in [
            "헷갈려",
            "모르겠",
            "당황",
            "혼란",
            "어리둥절",
            "이해안돼",
            "복잡",
            "어색",
            "애매",
            "갈팡질팡",
        ]
    ):
        return "confused"

    # 11. 자신감/당당 계열
    elif any(
        word in text
        for word in [
            "자신있",
            "당당",
            "확신",
            "자랑",
            "뿌듯",
            "잘났",
            "성취",
            "승리",
            "이겼",
            "대견",
            "자부심",
        ]
    ):
        return "confident"

    # 12. 부끄러움/수줍음 계열
    elif any(
        word in text
        for word in [
            "부끄러",
            "창피",
            "민망",
            "수줍",
            "쑥스러",
            "얼굴빨개",
            "어이없어",
            "쪽팔려",
            "떨려",
        ]
    ):
        return "shy"

    else:
        return "neutral"


REALISTIC_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>👤 리얼리스틱 3D 아바타</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #2c3e50 100%);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            font-size: 2em;
            color: #ecf0f1;
            margin-bottom: 30px;
            font-weight: 300;
        }
        
        #avatar-container {
            width: 600px;
            height: 600px;
            border: 2px solid #7f8c8d;
            border-radius: 15px;
            margin: 30px auto;
            background: rgba(52, 73, 94, 0.8);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .status-panel {
            display: flex;
            gap: 20px;
            margin: 30px 0;
            justify-content: center;
        }
        
        .emotion-display, .confidence-display {
            text-align: center;
            font-size: 1.1em;
            padding: 12px 20px;
            background: rgba(52, 73, 94, 0.9);
            border-radius: 10px;
            border: 1px solid #7f8c8d;
            min-width: 150px;
        }
        
        .chat-area {
            display: flex;
            gap: 15px;
            margin: 30px 0;
        }
        
        #chat-input {
            flex: 1;
            padding: 12px 18px;
            font-size: 1em;
            border: 2px solid #7f8c8d;
            border-radius: 25px;
            background: rgba(44, 62, 80, 0.9);
            color: #ecf0f1;
            outline: none;
        }
        
        #chat-input:focus {
            border-color: #3498db;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
        }
        
        #send-btn {
            padding: 12px 25px;
            font-size: 1em;
            background: linear-gradient(45deg, #3498db, #2980b9);
            border: none;
            border-radius: 25px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        #send-btn:hover {
            background: linear-gradient(45deg, #2980b9, #3498db);
            transform: translateY(-2px);
        }
        
        #debug-log {
            background: rgba(44, 62, 80, 0.95);
            padding: 15px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #7f8c8d;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>👤 리얼리스틱 3D 아바타</h1>
        
        <div id="avatar-container">
            <!-- Three.js 3D 렌더링 영역 -->
        </div>
        
        <div class="status-panel">
            <div class="emotion-display" id="emotion-display">
                😊 감정: 분석 중...
            </div>
            <div class="confidence-display" id="confidence-display">
                📊 정확도: ---%
            </div>
            <div class="memory-display" id="memory-display">
                🧠 메모리: 학습 준비 중...
            </div>
            <div class="conversation-count" id="conversation-count">
                💬 대화 수: 0회
            </div>
        </div>
        
        <div class="chat-area">
            <input type="text" id="chat-input" placeholder="당신의 감정을 표현해보세요... (AI가 학습합니다)">
            <button id="send-btn" onclick="sendMessage()">전송</button>
            <button id="memory-btn" onclick="showMemoryStats()" style="margin-left: 10px; background: #9b59b6; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer;">🧠 기억</button>
            <button id="reset-btn" onclick="resetMemory()" style="margin-left: 5px; background: #e74c3c; color: white; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer;">🗑️ 초기화</button>
        </div>
        
        <div id="debug-log">
            🔍 리얼리스틱 시스템 로그:<br>
        </div>
    </div>

    <script>
        let scene, camera, renderer, avatarMesh;
        let isInitialized = false;
        let clock = new THREE.Clock();

        function log(message) {
            const debugLog = document.getElementById('debug-log');
            const timestamp = new Date().toLocaleTimeString();
            debugLog.innerHTML += `<span style="color: #3498db">${timestamp}</span>: ${message}<br>`;
            debugLog.scrollTop = debugLog.scrollHeight;
            console.log(message);
        }

        function init3D() {
            log('🌟 리얼리스틱 3D 시스템 초기화...');
            
            if (isInitialized) {
                log('⚠️ 이미 초기화됨');
                return;
            }
            
            try {
                const container = document.getElementById('avatar-container');
                
                scene = new THREE.Scene();
                camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
                camera.position.set(0, 1.7, 4);
                camera.lookAt(0, 1.7, 0);
                
                renderer = new THREE.WebGLRenderer({ 
                    alpha: true, 
                    antialias: true,
                    powerPreference: "high-performance"
                });
                renderer.setSize(600, 600);
                renderer.setClearColor(0x000000, 0);
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                container.appendChild(renderer.domElement);
                
                // 사실적인 조명 시스템
                const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
                scene.add(ambientLight);
                
                const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
                mainLight.position.set(3, 8, 5);
                mainLight.castShadow = true;
                mainLight.shadow.mapSize.width = 2048;
                mainLight.shadow.mapSize.height = 2048;
                scene.add(mainLight);
                
                const fillLight = new THREE.PointLight(0x87ceeb, 0.4);
                fillLight.position.set(-2, 3, 2);
                scene.add(fillLight);
                
                const rimLight = new THREE.PointLight(0xffd700, 0.2);
                rimLight.position.set(0, 6, -2);
                scene.add(rimLight);
                
                createRealisticAvatar('neutral');
                animate();
                
                isInitialized = true;
                log('✅ 리얼리스틱 시스템 초기화 완료!');
                
            } catch (error) {
                log('❌ 초기화 오류: ' + error.message);
            }
        }

        function createRealisticAvatar(emotion) {
            log(`👤 리얼리스틱 아바타 생성: ${emotion}`);
            
            try {
                if (avatarMesh) {
                    scene.remove(avatarMesh);
                }
                
                const emotionConfig = {
                    'happy': { clothColor: 0x3498db, intensity: 1.2 },
                    'sad': { clothColor: 0x7f8c8d, intensity: 0.8 },
                    'angry': { clothColor: 0xe74c3c, intensity: 1.5 },
                    'amazed': { clothColor: 0xf39c12, intensity: 1.3 },
                    'love': { clothColor: 0xe91e63, intensity: 1.4 },
                    'neutral': { clothColor: 0x34495e, intensity: 1.0 }
                };
                
                const config = emotionConfig[emotion] || emotionConfig.neutral;
                const group = new THREE.Group();
                
                // 🎨 리얼리스틱 머티리얼
                const skinMaterial = new THREE.MeshLambertMaterial({ 
                    color: 0xffdbac,
                    transparent: true,
                    opacity: 0.95
                });
                
                const hairMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x8b4513,
                    shininess: 20
                });
                
                const clothMaterial = new THREE.MeshLambertMaterial({ 
                    color: config.clothColor
                });
                
                const eyeMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x333333,
                    shininess: 100
                });
                
                // 👤 리얼리스틱 헤드 (더 정교한 형태)
                const headGroup = new THREE.Group();
                
                // 메인 헤드 (타원형)
                const headGeometry = new THREE.SphereGeometry(0.5, 32, 32);
                headGeometry.scale(1, 1.1, 0.85);
                const head = new THREE.Mesh(headGeometry, skinMaterial);
                head.castShadow = true;
                head.receiveShadow = true;
                headGroup.add(head);
                
                // 목
                const neckGeometry = new THREE.CylinderGeometry(0.25, 0.3, 0.4);
                const neck = new THREE.Mesh(neckGeometry, skinMaterial);
                neck.position.set(0, -0.4, 0);
                neck.castShadow = true;
                headGroup.add(neck);
                
                // 더 사실적인 눈
                const eyeGeometry = new THREE.SphereGeometry(0.08, 16, 16);
                
                const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
                leftEye.position.set(-0.18, 0.1, 0.42);
                headGroup.add(leftEye);
                
                const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
                rightEye.position.set(0.18, 0.1, 0.42);
                headGroup.add(rightEye);
                
                // 눈동자 하이라이트
                const pupilGeometry = new THREE.SphereGeometry(0.02, 8, 8);
                const pupilMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
                
                const leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
                leftPupil.position.set(-0.16, 0.12, 0.48);
                headGroup.add(leftPupil);
                
                const rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
                rightPupil.position.set(0.20, 0.12, 0.48);
                headGroup.add(rightPupil);
                
                // 리얼리스틱 코
                const noseGeometry = new THREE.ConeGeometry(0.04, 0.12, 8);
                const nose = new THREE.Mesh(noseGeometry, skinMaterial);
                nose.position.set(0, 0, 0.45);
                nose.rotation.x = Math.PI;
                headGroup.add(nose);
                
                // 더 자연스러운 머리카락
                const hairGeometry = new THREE.SphereGeometry(0.52, 24, 24);
                hairGeometry.scale(1, 1.2, 0.9);
                const hair = new THREE.Mesh(hairGeometry, hairMaterial);
                hair.position.set(0, 0.2, -0.1);
                hair.castShadow = true;
                headGroup.add(hair);
                
                headGroup.position.set(0, 2.4, 0);
                group.add(headGroup);
                
                // 🫵 리얼리스틱 몸통 (더 자연스러운 형태)
                const torsoGeometry = new THREE.CylinderGeometry(0.35, 0.45, 1.0);
                const torso = new THREE.Mesh(torsoGeometry, clothMaterial);
                torso.position.set(0, 1.5, 0);
                torso.castShadow = true;
                torso.receiveShadow = true;
                group.add(torso);
                
                // 가슴 부분 (더 자연스러운 체형)
                const chestGeometry = new THREE.SphereGeometry(0.4, 16, 16);
                chestGeometry.scale(1, 0.6, 0.8);
                const chest = new THREE.Mesh(chestGeometry, clothMaterial);
                chest.position.set(0, 1.8, 0);
                chest.castShadow = true;
                group.add(chest);
                
                // 🦾 간단하고 자연스러운 팔 (일직선 연결)
                const armGeometry = new THREE.CylinderGeometry(0.07, 0.05, 1.2);
                
                // 왼쪽 팔 (어깨에서 손까지 일직선)
                const leftArm = new THREE.Mesh(armGeometry, skinMaterial);
                leftArm.position.set(-0.45, 1.4, 0);
                leftArm.rotation.z = -0.4;  // 안쪽으로 기울어진 각도 (반대로)
                leftArm.castShadow = true;
                group.add(leftArm);
                
                // 오른쪽 팔 (어깨에서 손까지 일직선)
                const rightArm = new THREE.Mesh(armGeometry, skinMaterial);
                rightArm.position.set(0.45, 1.4, 0);
                rightArm.rotation.z = 0.4;  // 안쪽으로 기울어진 각도 (반대로)
                rightArm.castShadow = true;
                group.add(rightArm);
                
                // 손 (팔 끝에 정확히 연결)
                const handGeometry = new THREE.SphereGeometry(0.08, 12, 12);
                handGeometry.scale(1.3, 1, 0.8);  // 손 모양으로 조정
                
                const leftHand = new THREE.Mesh(handGeometry, skinMaterial);
                leftHand.position.set(-0.2, 0.8, 0);  // 안쪽으로 이동
                leftHand.castShadow = true;
                group.add(leftHand);
                
                const rightHand = new THREE.Mesh(handGeometry, skinMaterial);
                rightHand.position.set(0.2, 0.8, 0);  // 안쪽으로 이동
                rightHand.castShadow = true;
                group.add(rightHand);
                rightHand.castShadow = true;
                group.add(rightHand);
                
                // 🦵 리얼리스틱 다리
                const pantsMaterial = new THREE.MeshLambertMaterial({ color: 0x2c3e50 });
                
                // 허리
                const waistGeometry = new THREE.CylinderGeometry(0.4, 0.35, 0.3);
                const waist = new THREE.Mesh(waistGeometry, pantsMaterial);
                waist.position.set(0, 0.85, 0);
                waist.castShadow = true;
                group.add(waist);
                
                // 왼쪽 다리
                const leftThighGeometry = new THREE.CylinderGeometry(0.12, 0.15, 0.8);
                const leftThigh = new THREE.Mesh(leftThighGeometry, pantsMaterial);
                leftThigh.position.set(-0.15, 0.3, 0);
                leftThigh.castShadow = true;
                group.add(leftThigh);
                
                const leftKnee = new THREE.SphereGeometry(0.1, 10, 10);
                const leftKneeMesh = new THREE.Mesh(leftKnee, pantsMaterial);
                leftKneeMesh.position.set(-0.15, -0.1, 0);
                leftKneeMesh.castShadow = true;
                group.add(leftKneeMesh);
                
                const leftShinGeometry = new THREE.CylinderGeometry(0.1, 0.12, 0.7);
                const leftShin = new THREE.Mesh(leftShinGeometry, pantsMaterial);
                leftShin.position.set(-0.15, -0.55, 0);
                leftShin.castShadow = true;
                group.add(leftShin);
                
                // 오른쪽 다리
                const rightThighGeometry = new THREE.CylinderGeometry(0.12, 0.15, 0.8);
                const rightThigh = new THREE.Mesh(rightThighGeometry, pantsMaterial);
                rightThigh.position.set(0.15, 0.3, 0);
                rightThigh.castShadow = true;
                group.add(rightThigh);
                
                const rightKnee = new THREE.SphereGeometry(0.1, 10, 10);
                const rightKneeMesh = new THREE.Mesh(rightKnee, pantsMaterial);
                rightKneeMesh.position.set(0.15, -0.1, 0);
                rightKneeMesh.castShadow = true;
                group.add(rightKneeMesh);
                
                const rightShinGeometry = new THREE.CylinderGeometry(0.1, 0.12, 0.7);
                const rightShin = new THREE.Mesh(rightShinGeometry, pantsMaterial);
                rightShin.position.set(0.15, -0.55, 0);
                rightShin.castShadow = true;
                group.add(rightShin);
                
                // 👟 신발
                const shoeGeometry = new THREE.BoxGeometry(0.15, 0.08, 0.3);
                const shoeMaterial = new THREE.MeshLambertMaterial({ color: 0x2c3e50 });
                
                const leftShoe = new THREE.Mesh(shoeGeometry, shoeMaterial);
                leftShoe.position.set(-0.15, -0.95, 0.1);
                leftShoe.castShadow = true;
                group.add(leftShoe);
                
                const rightShoe = new THREE.Mesh(shoeGeometry, shoeMaterial);
                rightShoe.position.set(0.15, -0.95, 0.1);
                rightShoe.castShadow = true;
                group.add(rightShoe);
                
                // 🎭 리얼리스틱 감정 표현
                createRealisticFacialExpression(headGroup, emotion);
                
                avatarMesh = group;
                scene.add(avatarMesh);
                
                log(`✅ 리얼리스틱 아바타 완성: ${emotion}`);
                
            } catch (error) {
                log('❌ 아바타 생성 오류: ' + error.message);
            }
        
        function createRealisticFacialExpression(headGroup, emotion) {
            const mouthMaterial = new THREE.MeshLambertMaterial({ color: 0xff6b6b });
            
            switch(emotion) {
                case 'happy':
                    // 😊 자연스러운 웃음
                    const smileGeometry = new THREE.TorusGeometry(0.15, 0.02, 6, 12, Math.PI);
                    const smile = new THREE.Mesh(smileGeometry, mouthMaterial);
                    smile.position.set(0, -0.15, 0.42);
                    smile.rotation.z = Math.PI;
                    headGroup.add(smile);
                    
                    // 웃는 눈 (약간 감긴)
                    const eyeCrinkleGeo = new THREE.CylinderGeometry(0.01, 0.01, 0.1);
                    const crinkleMat = new THREE.MeshLambertMaterial({color: 0xe6c2a6});
                    
                    const leftCrinkle = new THREE.Mesh(eyeCrinkleGeo, crinkleMat);
                    leftCrinkle.position.set(-0.25, 0.05, 0.4);
                    leftCrinkle.rotation.z = 0.5;
                    headGroup.add(leftCrinkle);
                    
                    const rightCrinkle = new THREE.Mesh(eyeCrinkleGeo, crinkleMat);
                    rightCrinkle.position.set(0.25, 0.05, 0.4);
                    rightCrinkle.rotation.z = -0.5;
                    headGroup.add(rightCrinkle);
                    break;
                    
                case 'sad':
                    // 😢 슬픈 표정
                    const sadMouthGeo = new THREE.TorusGeometry(0.12, 0.02, 6, 12, Math.PI);
                    const sadMouth = new THREE.Mesh(sadMouthGeo, new THREE.MeshLambertMaterial({color: 0x95a5a6}));
                    sadMouth.position.set(0, -0.2, 0.42);
                    headGroup.add(sadMouth);
                    
                    // 눈물
                    const tearGeo = new THREE.SphereGeometry(0.02, 8, 8);
                    const tearMat = new THREE.MeshLambertMaterial({color: 0x3498db, transparent: true, opacity: 0.7});
                    const tear = new THREE.Mesh(tearGeo, tearMat);
                    tear.position.set(-0.2, 0.05, 0.45);
                    headGroup.add(tear);
                    break;
                    
                case 'angry':
                    // 😠 화난 표정
                    const angryMouthGeo = new THREE.BoxGeometry(0.15, 0.02, 0.03);
                    const angryMouth = new THREE.Mesh(angryMouthGeo, new THREE.MeshLambertMaterial({color: 0xe74c3c}));
                    angryMouth.position.set(0, -0.18, 0.42);
                    headGroup.add(angryMouth);
                    
                    // 찡그린 이마
                    const browGeo = new THREE.BoxGeometry(0.1, 0.01, 0.01);
                    const browMat = new THREE.MeshLambertMaterial({color: 0xe6c2a6});
                    
                    const leftBrow = new THREE.Mesh(browGeo, browMat);
                    leftBrow.position.set(-0.15, 0.25, 0.4);
                    leftBrow.rotation.z = 0.3;
                    headGroup.add(leftBrow);
                    
                    const rightBrow = new THREE.Mesh(browGeo, browMat);
                    rightBrow.position.set(0.15, 0.25, 0.4);
                    rightBrow.rotation.z = -0.3;
                    headGroup.add(rightBrow);
                    break;
                    
                case 'love':
                    // 💕 사랑스러운 표정
                    const loveMouthGeo = new THREE.SphereGeometry(0.05, 8, 8);
                    const loveMouth = new THREE.Mesh(loveMouthGeo, new THREE.MeshLambertMaterial({color: 0xe91e63}));
                    loveMouth.position.set(0, -0.15, 0.42);
                    headGroup.add(loveMouth);
                    
                    // 하트 뺨
                    const heartGeo = new THREE.SphereGeometry(0.03, 6, 6);
                    const heartMat = new THREE.MeshLambertMaterial({color: 0xff9999});
                    
                    const leftBlush = new THREE.Mesh(heartGeo, heartMat);
                    leftBlush.position.set(-0.3, -0.05, 0.4);
                    headGroup.add(leftBlush);
                    
                    const rightBlush = new THREE.Mesh(heartGeo, heartMat);
                    rightBlush.position.set(0.3, -0.05, 0.4);
                    headGroup.add(rightBlush);
                    break;
                    
                case 'amazed':
                    // 😲 놀란 표정
                    const amazedMouthGeo = new THREE.SphereGeometry(0.06, 8, 8);
                    const amazedMouth = new THREE.Mesh(amazedMouthGeo, new THREE.MeshLambertMaterial({color: 0x34495e}));
                    amazedMouth.position.set(0, -0.16, 0.42);
                    headGroup.add(amazedMouth);
                    
                    // 놀란 눈 (크게 뜬 눈)
                    const amazedEyeGeo = new THREE.SphereGeometry(0.1, 12, 12);
                    const amazedEyeMat = new THREE.MeshLambertMaterial({color: 0xffffff});
                    
                    const leftAmazedEye = new THREE.Mesh(amazedEyeGeo, amazedEyeMat);
                    leftAmazedEye.position.set(-0.18, 0.1, 0.45);
                    headGroup.add(leftAmazedEye);
                    
                    const rightAmazedEye = new THREE.Mesh(amazedEyeGeo, amazedEyeMat);
                    rightAmazedEye.position.set(0.18, 0.1, 0.45);
                    headGroup.add(rightAmazedEye);
                    break;
                    
                case 'excited':
                    // 🤩 흥미진진한 표정 (반짝이는 눈)
                    const excitedMouthGeo = new THREE.TorusGeometry(0.18, 0.03, 8, 16, Math.PI);
                    const excitedMouth = new THREE.Mesh(excitedMouthGeo, new THREE.MeshLambertMaterial({color: 0xf39c12}));
                    excitedMouth.position.set(0, -0.15, 0.42);
                    excitedMouth.rotation.z = Math.PI;
                    headGroup.add(excitedMouth);
                    
                    // 반짝이는 눈
                    const starGeo = new THREE.SphereGeometry(0.02, 6, 6);
                    const starMat = new THREE.MeshLambertMaterial({color: 0xffd700});
                    const leftStar = new THREE.Mesh(starGeo, starMat);
                    leftStar.position.set(-0.15, 0.12, 0.48);
                    headGroup.add(leftStar);
                    
                    const rightStar = new THREE.Mesh(starGeo, starMat);
                    rightStar.position.set(0.23, 0.12, 0.48);
                    headGroup.add(rightStar);
                    break;
                    
                case 'worried':
                    // 😰 걱정스러운 표정
                    const worriedMouthGeo = new THREE.TorusGeometry(0.1, 0.015, 6, 12, Math.PI);
                    const worriedMouth = new THREE.Mesh(worriedMouthGeo, new THREE.MeshLambertMaterial({color: 0x7f8c8d}));
                    worriedMouth.position.set(0, -0.18, 0.42);
                    headGroup.add(worriedMouth);
                    
                    // 걱정 주름
                    const wrinkleGeo = new THREE.BoxGeometry(0.05, 0.005, 0.01);
                    const wrinkleMat = new THREE.MeshLambertMaterial({color: 0xd4c4a0});
                    const wrinkle = new THREE.Mesh(wrinkleGeo, wrinkleMat);
                    wrinkle.position.set(0, 0.2, 0.4);
                    headGroup.add(wrinkle);
                    break;
                    
                case 'tired':
                    // 😴 피곤한 표정 (반쯤 감긴 눈)
                    const tiredMouthGeo = new THREE.CylinderGeometry(0.008, 0.008, 0.08);
                    const tiredMouth = new THREE.Mesh(tiredMouthGeo, new THREE.MeshLambertMaterial({color: 0x95a5a6}));
                    tiredMouth.position.set(0, -0.16, 0.42);
                    tiredMouth.rotation.z = Math.PI / 2;
                    headGroup.add(tiredMouth);
                    
                    // 반쯤 감긴 눈
                    const sleepyEyeGeo = new THREE.BoxGeometry(0.12, 0.01, 0.01);
                    const sleepyEyeMat = new THREE.MeshLambertMaterial({color: 0xe6c2a6});
                    const leftSleepy = new THREE.Mesh(sleepyEyeGeo, sleepyEyeMat);
                    leftSleepy.position.set(-0.18, 0.08, 0.42);
                    headGroup.add(leftSleepy);
                    
                    const rightSleepy = new THREE.Mesh(sleepyEyeGeo, sleepyEyeMat);
                    rightSleepy.position.set(0.18, 0.08, 0.42);
                    headGroup.add(rightSleepy);
                    break;
                    
                case 'grateful':
                    // 🙏 감사한 표정 (따뜻한 미소)
                    const gratefulMouthGeo = new THREE.TorusGeometry(0.13, 0.02, 6, 12, Math.PI * 0.8);
                    const gratefulMouth = new THREE.Mesh(gratefulMouthGeo, new THREE.MeshLambertMaterial({color: 0xe67e22}));
                    gratefulMouth.position.set(0, -0.15, 0.42);
                    gratefulMouth.rotation.z = Math.PI;
                    headGroup.add(gratefulMouth);
                    
                    // 따뜻한 눈
                    const warmGeo = new THREE.SphereGeometry(0.015, 8, 8);
                    const warmMat = new THREE.MeshLambertMaterial({color: 0xf39c12});
                    const leftWarm = new THREE.Mesh(warmGeo, warmMat);
                    leftWarm.position.set(-0.16, 0.12, 0.48);
                    headGroup.add(leftWarm);
                    
                    const rightWarm = new THREE.Mesh(warmGeo, warmMat);
                    rightWarm.position.set(0.20, 0.12, 0.48);
                    headGroup.add(rightWarm);
                    break;
                    
                case 'confused':
                    // 😕 혼란스러운 표정
                    const confusedMouthGeo = new THREE.TorusGeometry(0.08, 0.015, 6, 12, Math.PI * 0.7);
                    const confusedMouth = new THREE.Mesh(confusedMouthGeo, new THREE.MeshLambertMaterial({color: 0x95a5a6}));
                    confusedMouth.position.set(0.02, -0.17, 0.42);
                    confusedMouth.rotation.z = Math.PI * 0.9;
                    headGroup.add(confusedMouth);
                    
                    // 물음표 모양 눈썹
                    const questionGeo = new THREE.TorusGeometry(0.03, 0.005, 4, 8, Math.PI * 1.2);
                    const questionMat = new THREE.MeshLambertMaterial({color: 0xe6c2a6});
                    const questionBrow = new THREE.Mesh(questionGeo, questionMat);
                    questionBrow.position.set(0, 0.22, 0.4);
                    headGroup.add(questionBrow);
                    break;
                    
                case 'confident':
                    // 😎 자신감 있는 표정
                    const confidentMouthGeo = new THREE.BoxGeometry(0.12, 0.025, 0.02);
                    const confidentMouth = new THREE.Mesh(confidentMouthGeo, new THREE.MeshLambertMaterial({color: 0x2ecc71}));
                    confidentMouth.position.set(0, -0.15, 0.42);
                    headGroup.add(confidentMouth);
                    
                    // 당당한 눈
                    const coolGeo = new THREE.BoxGeometry(0.08, 0.03, 0.01);
                    const coolMat = new THREE.MeshLambertMaterial({color: 0x34495e});
                    const leftCool = new THREE.Mesh(coolGeo, coolMat);
                    leftCool.position.set(-0.18, 0.1, 0.42);
                    headGroup.add(leftCool);
                    
                    const rightCool = new THREE.Mesh(coolGeo, coolMat);
                    rightCool.position.set(0.18, 0.1, 0.42);
                    headGroup.add(rightCool);
                    break;
                    
                case 'shy':
                    // 😊 부끄러운 표정 (붉어진 뺨)
                    const shyMouthGeo = new THREE.SphereGeometry(0.04, 8, 8);
                    const shyMouth = new THREE.Mesh(shyMouthGeo, new THREE.MeshLambertMaterial({color: 0xff7675}));
                    shyMouth.position.set(0, -0.16, 0.42);
                    headGroup.add(shyMouth);
                    
                    // 붉어진 뺨
                    const blushGeo = new THREE.SphereGeometry(0.04, 8, 8);
                    const blushMat = new THREE.MeshLambertMaterial({color: 0xff6b9d});
                    const leftBlushShy = new THREE.Mesh(blushGeo, blushMat);
                    leftBlushShy.position.set(-0.25, -0.05, 0.4);
                    headGroup.add(leftBlushShy);
                    
                    const rightBlushShy = new THREE.Mesh(blushGeo, blushMat);
                    rightBlushShy.position.set(0.25, -0.05, 0.4);
                    headGroup.add(rightBlushShy);
                    break;
                    
                default:
                    // 😐 기본 표정
                    const neutralMouthGeo = new THREE.CylinderGeometry(0.01, 0.01, 0.12);
                    const neutralMouth = new THREE.Mesh(neutralMouthGeo, mouthMaterial);
                    neutralMouth.position.set(0, -0.15, 0.42);
                    neutralMouth.rotation.z = Math.PI / 2;
                    headGroup.add(neutralMouth);
                    break;
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            
            const deltaTime = clock.getDelta();
            
            if (avatarMesh) {
                // 회전 제거 - 고정된 자세
                
                // 리얼리스틱 숨쉬기
                const breathe = Math.sin(clock.getElapsedTime() * 1.5) * 0.015;
                avatarMesh.scale.y = 1 + breathe;
                
                // 미세한 머리 움직임
                const headMove = Math.sin(clock.getElapsedTime() * 0.8) * 0.05;
                if (avatarMesh.children[0]) {
                    avatarMesh.children[0].rotation.y = headMove;
                }
            }
            
            renderer.render(scene, camera);
        }

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) {
                log('⚠️ 메시지가 비어있음');
                return;
            }

            log(`📨 리얼리스틱 분석: ${message}`);
            input.value = '';
            
            try {
                log('🚀 감정 분석 중...');
                
                const response = await fetch('/realistic-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                log('📡 서버 응답: ' + response.status);
                
                if (!response.ok) {
                    throw new Error('서버 응답 오류: ' + response.status);
                }
                
                const result = await response.json();
                log('✅ 분석 완료: ' + JSON.stringify(result));
                
                // UI 업데이트
                document.getElementById('emotion-display').innerHTML = 
                    `😊 감정: <span style="color: #3498db; font-weight: bold;">${result.emotion}</span>`;
                
                document.getElementById('confidence-display').innerHTML = 
                    `📊 정확도: <span style="color: #27ae60; font-weight: bold;">${(result.confidence * 100).toFixed(1)}%</span>`;
                
                // 🧠 v10.1 메모리 상태 업데이트
                if (result.memory_status) {
                    document.getElementById('memory-display').innerHTML = 
                        `🧠 메모리: <span style="color: #9b59b6; font-weight: bold;">${result.memory_status}</span>`;
                }
                
                if (result.conversation_count !== undefined) {
                    document.getElementById('conversation-count').innerHTML = 
                        `💬 대화 수: <span style="color: #f39c12; font-weight: bold;">${result.conversation_count}회</span>`;
                }
                
                // 리얼리스틱 아바타 업데이트
                createRealisticAvatar(result.emotion);
                
                log('🎯 리얼리스틱 아바타 업데이트 완료');
                log(`🧠 학습 상태: ${result.memory_status || '정보 없음'}`);
                
            } catch (error) {
                log('❌ 오류 발생: ' + error.message);
                console.error('Error:', error);
            }
        }

        // 🧠 메모리 통계 보기
        async function showMemoryStats() {
            try {
                const response = await fetch('/memory-stats');
                const stats = await response.json();
                
                let statsText = `🧠 학습 메모리 상태\\n\\n`;
                statsText += `총 대화 수: ${stats.총_대화_수}\\n`;
                statsText += `가장 많이 사용한 감정: ${stats.가장_많이_사용한_감정}\\n`;
                statsText += `학습 상태: ${stats.학습_데이터_상태}\\n\\n`;
                
                if (stats.감정_패턴 && Object.keys(stats.감정_패턴).length > 0) {
                    statsText += `감정 패턴:\\n`;
                    for (const [emotion, count] of Object.entries(stats.감정_패턴)) {
                        statsText += `  ${emotion}: ${count}회\\n`;
                    }
                }
                
                alert(statsText);
                log('🧠 메모리 통계 조회 완료');
                
            } catch (error) {
                alert('메모리 통계를 불러오는데 실패했습니다: ' + error.message);
                log('❌ 메모리 통계 오류: ' + error.message);
            }
        }

        // 🗑️ 메모리 초기화
        async function resetMemory() {
            if (!confirm('정말로 모든 학습 데이터를 삭제하시겠습니까?\\n이 작업은 되돌릴 수 없습니다.')) {
                return;
            }
            
            try {
                const response = await fetch('/reset-memory', { method: 'POST' });
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert('메모리가 초기화되었습니다!');
                    document.getElementById('memory-display').innerHTML = '🧠 메모리: 초기화됨';
                    document.getElementById('conversation-count').innerHTML = '💬 대화 수: 0회';
                    log('🗑️ 메모리 초기화 완료');
                } else {
                    throw new Error(result.error || '초기화 실패');
                }
                
            } catch (error) {
                alert('메모리 초기화에 실패했습니다: ' + error.message);
                log('❌ 메모리 초기화 오류: ' + error.message);
            }
        }
                
            } catch (error) {
                log('❌ 오류 발생: ' + error.message);
                console.error('Error:', error);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // 페이지 로드 시 초기화
        window.addEventListener('load', function() {
            log('🌟 리얼리스틱 시스템 시작');
            init3D();
            
            // 입력 필드에 이벤트 리스너 추가
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.addEventListener('keypress', handleKeyPress);
            }
        });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return REALISTIC_TEMPLATE


@app.route("/realistic-chat", methods=["POST"])
def realistic_chat():
    print("👤 리얼리스틱 채팅 요청!")

    try:
        data = request.get_json()
        if not data:
            print("❌ 데이터가 없음")
            return jsonify({"error": "데이터가 없습니다"}), 400

        message = data.get("message", "")
        print(f"📝 분석 메시지: {message}")

        # 🧠 v10.1 대화 기억/학습 시스템
        emotion = analyze_user_patterns(message)
        confidence = 0.89  # 리얼리스틱 신뢰도

        # 개인화된 응답 생성
        ai_response = get_personalized_response(emotion, message)

        # 대화 히스토리에 추가
        conversation_entry = {
            "timestamp": str(time.time()),
            "user_message": message,
            "emotion": emotion,
            "ai_response": ai_response,
        }
        conversation_history.append(conversation_entry)

        # 메모리 저장
        save_memory()

        print(f"🎭 감정 분석 결과: {emotion} (신뢰도: {confidence})")
        print(f"🧠 학습된 패턴: {len(user_preferences.get('emotion_patterns', {}))}")

        response = {
            "emotion": emotion,
            "confidence": confidence,
            "message": ai_response,
            "avatar_type": "realistic",
            "conversation_count": len(conversation_history),
            "learned_patterns": user_preferences.get("emotion_patterns", {}),
            "memory_status": f"대화 {len(conversation_history)}회 기억 중",
        }

        print(f"✅ 리얼리스틱 응답: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"❌ 오류: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/memory-stats", methods=["GET"])
def memory_stats():
    """🧠 메모리 통계 조회"""
    try:
        stats = {
            "총_대화_수": len(conversation_history),
            "감정_패턴": user_preferences.get("emotion_patterns", {}),
            "최근_대화": conversation_history[-5:] if conversation_history else [],
            "가장_많이_사용한_감정": max(
                user_preferences.get("emotion_patterns", {}),
                key=user_preferences.get("emotion_patterns", {}).get,
                default="없음",
            ),
            "학습_데이터_상태": "활성화" if conversation_history else "대기중",
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reset-memory", methods=["POST"])
def reset_memory():
    """🧠 메모리 초기화"""
    global conversation_history, user_preferences
    try:
        conversation_history = []
        user_preferences = {}
        save_memory()
        return jsonify({"message": "메모리가 초기화되었습니다", "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("👤 리얼리스틱 3D 아바타 시작!")
    print("🎯 http://127.0.0.1:5006 에서 현실적 체험!")
    app.run(debug=True, port=5006)
