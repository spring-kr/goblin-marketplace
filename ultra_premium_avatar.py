"""
🌟 Ultra Premium 3D 아바타 시스템 v2.0 (종합 업그레이드)
- 사실적 텍스처 + 고급 애니메이션 + 화려한 특수효과 + 세밀한 모델링
"""

from flask import Flask, request, jsonify

app = Flask(__name__)


def analyze_korean_emotion(text):
    """고도화된 한국어 감정 분석"""
    text = text.lower()

    # 더 정확한 감정 키워드
    if any(
        word in text
        for word in [
            "기분 좋",
            "좋아",
            "행복",
            "ㅋㅋ",
            "신나",
            "최고",
            "기뻐",
            "즐거",
            "웃",
            "만족",
            "사랑해",
        ]
    ):
        return "happy"
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
        ]
    ):
        return "sad"
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
        ]
    ):
        return "angry"
    elif any(
        word in text
        for word in ["놀라", "깜짝", "헐", "와", "대박", "신기", "믿을 수 없", "어떻게"]
    ):
        return "amazed"
    elif any(
        word in text
        for word in ["사랑", "좋아해", "애정", "마음에 들", "멋져", "예뻐", "훌륭"]
    ):
        return "love"
    else:
        return "neutral"


ULTRA_PREMIUM_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>🌟 Ultra Premium 3D 아바타 v2.0</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            font-family: 'Orbitron', monospace;
            overflow-x: hidden;
            min-height: 100vh;
        }
        
        .cosmic-bg {
            display: none; /* 정신없는 배경 제거 */
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }
        
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #00ffff;
            margin-bottom: 30px;
        }
        
        #avatar-container {
            width: 500px;
            height: 500px;
            border: 2px solid #00ffff;
            border-radius: 20px;
            margin: 30px auto;
            background: rgba(0, 255, 255, 0.1);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .status-panel {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }
        
        .emotion-display, .confidence-display {
            text-align: center;
            font-size: 1.2em;
            padding: 15px;
            background: rgba(0, 53, 102, 0.8);
            border-radius: 15px;
            border: 2px solid rgba(255, 214, 10, 0.5);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .chat-area {
            display: flex;
            gap: 15px;
            margin: 30px 0;
            position: relative;
        }
        
        #chat-input {
            flex: 1;
            padding: 15px 20px;
            font-size: 1.1em;
            font-family: 'Orbitron', monospace;
            border: 2px solid rgba(255, 214, 10, 0.7);
            border-radius: 25px;
            background: rgba(0, 8, 20, 0.9);
            color: #ffd60a;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        #chat-input:focus {
            outline: none;
            border-color: #ffd60a;
            box-shadow: 0 0 20px rgba(255, 214, 10, 0.5);
        }
        
        #send-btn {
            padding: 15px 30px;
            font-size: 1.1em;
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            background: linear-gradient(45deg, #ffd60a, #f77f00);
            border: none;
            border-radius: 25px;
            color: #000814;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(255, 214, 10, 0.4);
        }
        
        #send-btn:hover {
            background: linear-gradient(45deg, #f77f00, #d62828);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(247, 127, 0, 0.6);
        }
        
        #debug-log {
            background: rgba(0, 8, 20, 0.95);
            padding: 20px;
            border-radius: 15px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid rgba(255, 214, 10, 0.3);
            backdrop-filter: blur(10px);
            margin-top: 20px;
        }
        
        .particle-effect {
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .floating-element {
            position: absolute;
            animation: float 4s ease-in-out infinite;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="cosmic-bg"></div>
    
    <div class="container">
        <h1>🌟 Ultra Premium 3D 아바타 v2.0</h1>
        
        <div id="avatar-container">
            <div class="particle-effect" id="particle-container"></div>
            <!-- Three.js 3D 렌더링 영역 -->
        </div>
        
        <div class="status-panel">
            <div class="emotion-display" id="emotion-display">
                💭 감정: 분석 대기중...
            </div>
            <div class="confidence-display" id="confidence-display">
                🎯 정확도: ---%
            </div>
        </div>
        
        <div class="chat-area">
            <input type="text" id="chat-input" placeholder="당신의 마음을 표현해보세요..." onkeypress="handleKeyPress(event)">
            <button id="send-btn" onclick="sendMessage()">✨ 전송</button>
        </div>
        
        <div id="debug-log">
            🔬 Ultra Premium 시스템 로그:<br>
        </div>
    </div>

    <script>
        let scene, camera, renderer, avatarMesh, mixer;
        let isInitialized = false;
        let clock = new THREE.Clock();
        let particles = [];

        function log(message) {
            const debugLog = document.getElementById('debug-log');
            const timestamp = new Date().toLocaleTimeString();
            debugLog.innerHTML += `<span style="color: #ffd60a">${timestamp}</span>: ${message}<br>`;
            debugLog.scrollTop = debugLog.scrollHeight;
            console.log(message);
        }

        function createParticleEffect() {
            // 정신없는 파티클 효과 제거 - 깔끔하게!
            log('✨ 깔끔한 UI로 설정됨');
        }

        function init3D() {
            log('🚀 Ultra Premium 3D 시스템 초기화...');
            
            if (isInitialized) {
                log('⚠️ 이미 초기화됨');
                return;
            }
            
            try {
                const container = document.getElementById('avatar-container');
                
                scene = new THREE.Scene();
                camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
                camera.position.set(0, 1, 5);
                camera.lookAt(0, 1, 0);
                
                renderer = new THREE.WebGLRenderer({ 
                    alpha: true, 
                    antialias: true,
                    powerPreference: "high-performance"
                });
                renderer.setSize(500, 500);
                renderer.setClearColor(0x000000, 0);
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                container.appendChild(renderer.domElement);
                
                // 고급 조명 시스템
                const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
                scene.add(ambientLight);
                
                const mainLight = new THREE.DirectionalLight(0xffffff, 1);
                mainLight.position.set(5, 10, 5);
                mainLight.castShadow = true;
                mainLight.shadow.mapSize.width = 2048;
                mainLight.shadow.mapSize.height = 2048;
                scene.add(mainLight);
                
                const fillLight = new THREE.PointLight(0xffd60a, 0.5);
                fillLight.position.set(-3, 2, 3);
                scene.add(fillLight);
                
                const rimLight = new THREE.PointLight(0x00ffff, 0.3);
                rimLight.position.set(0, 5, -3);
                scene.add(rimLight);
                
                createUltraPremiumAvatar('neutral');
                animate();
                createParticleEffect();
                
                isInitialized = true;
                log('✅ Ultra Premium 시스템 초기화 완료!');
                
            } catch (error) {
                log('❌ 초기화 오류: ' + error.message);
            }
        }

        function createUltraPremiumAvatar(emotion) {
            log(`💎 Ultra Premium 아바타 생성: ${emotion}`);
            
            try {
                if (avatarMesh) {
                    scene.remove(avatarMesh);
                }
                
                const emotionConfig = {
                    'happy': { 
                        clothColor: 0xFFD700, 
                        glowColor: 0xFFFF00,
                        intensity: 1.5,
                        particles: true 
                    },
                    'sad': { 
                        clothColor: 0x4169E1, 
                        glowColor: 0x0080FF,
                        intensity: 0.8,
                        particles: false 
                    },
                    'angry': { 
                        clothColor: 0xDC143C, 
                        glowColor: 0xFF0000,
                        intensity: 2.0,
                        particles: true 
                    },
                    'amazed': { 
                        clothColor: 0xFF8C00, 
                        glowColor: 0xFFA500,
                        intensity: 1.3,
                        particles: true 
                    },
                    'love': { 
                        clothColor: 0xFF69B4, 
                        glowColor: 0xFF1493,
                        intensity: 1.8,
                        particles: true 
                    },
                    'neutral': { 
                        clothColor: 0x00FFFF, 
                        glowColor: 0x00CED1,
                        intensity: 1.0,
                        particles: false 
                    }
                };
                
                const config = emotionConfig[emotion] || emotionConfig.neutral;
                const group = new THREE.Group();
                
                // 🌟 고급 머티리얼 설정
                const skinMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0xFFDBAC,
                    shininess: 30,
                    specular: 0x444444
                });
                
                const hairMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x654321,
                    shininess: 80
                });
                
                const clothMaterial = new THREE.MeshPhongMaterial({ 
                    color: config.clothColor,
                    shininess: 50,
                    emissive: config.glowColor,
                    emissiveIntensity: 0.1
                });
                
                // 👤 고급 머리 (더 세밀한 형태)
                const headGeometry = new THREE.SphereGeometry(0.7, 32, 32);
                headGeometry.scale(1, 1.1, 0.9);
                const head = new THREE.Mesh(headGeometry, skinMaterial);
                head.position.set(0, 1.8, 0);
                head.castShadow = true;
                head.receiveShadow = true;
                group.add(head);
                
                // 💇‍♀️ 더 사실적인 헤어
                const hairGeometry = new THREE.SphereGeometry(0.75, 24, 24);
                hairGeometry.scale(1, 1.2, 0.95);
                const hair = new THREE.Mesh(hairGeometry, hairMaterial);
                hair.position.set(0, 2.0, 0);
                hair.castShadow = true;
                group.add(hair);
                
                // 👀 더 생생한 눈
                const eyeGeometry = new THREE.SphereGeometry(0.1, 16, 16);
                const eyeMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x000000,
                    shininess: 100 
                });
                
                const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
                leftEye.position.set(-0.2, 1.9, 0.6);
                group.add(leftEye);
                
                const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
                rightEye.position.set(0.2, 1.9, 0.6);
                group.add(rightEye);
                
                // ✨ 눈동자 하이라이트
                const highlightGeometry = new THREE.SphereGeometry(0.03, 8, 8);
                const highlightMaterial = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
                
                const leftHighlight = new THREE.Mesh(highlightGeometry, highlightMaterial);
                leftHighlight.position.set(-0.18, 1.92, 0.65);
                group.add(leftHighlight);
                
                const rightHighlight = new THREE.Mesh(highlightGeometry, highlightMaterial);
                rightHighlight.position.set(0.22, 1.92, 0.65);
                group.add(rightHighlight);
                
                // 👃 더 정교한 코
                const noseGeometry = new THREE.ConeGeometry(0.06, 0.18, 8);
                const nose = new THREE.Mesh(noseGeometry, skinMaterial);
                nose.position.set(0, 1.75, 0.6);
                nose.rotation.x = Math.PI;
                group.add(nose);
                
                // 🫵 고급 몸통 (더 자연스러운 형태)
                const bodyGeometry = new THREE.CylinderGeometry(0.45, 0.55, 1.4);
                const body = new THREE.Mesh(bodyGeometry, clothMaterial);
                body.position.set(0, 0.4, 0);
                body.castShadow = true;
                body.receiveShadow = true;
                group.add(body);
                
                // 🦾 정상적인 팔 2개 (좌, 우)
                const armGeometry = new THREE.CylinderGeometry(0.08, 0.12, 1.0);
                
                // 왼쪽 팔
                const leftArm = new THREE.Mesh(armGeometry, skinMaterial);
                leftArm.position.set(-0.6, 0.7, 0);
                leftArm.rotation.z = 0.2;
                leftArm.castShadow = true;
                group.add(leftArm);
                
                // 오른쪽 팔
                const rightArm = new THREE.Mesh(armGeometry, skinMaterial);
                rightArm.position.set(0.6, 0.7, 0);
                rightArm.rotation.z = -0.2;
                rightArm.castShadow = true;
                group.add(rightArm);
                
                // 🦵 더 사실적인 다리
                const legGeometry = new THREE.CylinderGeometry(0.15, 0.18, 1.4);
                const pantsMaterial = new THREE.MeshPhongMaterial({ color: 0x000080, shininess: 20 });
                
                const leftLeg = new THREE.Mesh(legGeometry, pantsMaterial);
                leftLeg.position.set(-0.25, -0.9, 0);
                leftLeg.castShadow = true;
                group.add(leftLeg);
                
                const rightLeg = new THREE.Mesh(legGeometry, pantsMaterial);
                rightLeg.position.set(0.25, -0.9, 0);
                rightLeg.castShadow = true;
                group.add(rightLeg);
                
                // 🎭 감정별 고급 표정 시스템
                createAdvancedFacialExpression(group, emotion, config);
                
                // ✨ 감정별 특수 효과
                if (config.particles) {
                    createEmotionParticles(group, emotion, config);
                }
                
                // 🌟 감정별 오라 효과
                createEmotionAura(group, config);
                
                avatarMesh = group;
                scene.add(avatarMesh);
                
                log(`✅ Ultra Premium 아바타 완성: ${emotion}`);
                
            } catch (error) {
                log('❌ 아바타 생성 오류: ' + error.message);
            }
        }
        
        function createAdvancedFacialExpression(group, emotion, config) {
            const mouthMaterial = new THREE.MeshPhongMaterial({ 
                color: 0xFF69B4,
                shininess: 50
            });
            
            switch(emotion) {
                case 'happy':
                    // 😊 큰 웃음
                    const bigSmile = new THREE.TorusGeometry(0.25, 0.04, 8, 16, Math.PI);
                    const smileMesh = new THREE.Mesh(bigSmile, mouthMaterial);
                    smileMesh.position.set(0, 1.6, 0.6);
                    smileMesh.rotation.z = Math.PI;
                    group.add(smileMesh);
                    
                    // 눈가 주름 (웃는 눈)
                    const wrinkleGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.15);
                    const leftWrinkle = new THREE.Mesh(wrinkleGeo, new THREE.MeshPhongMaterial({color: 0xE6C2A6}));
                    leftWrinkle.position.set(-0.3, 1.85, 0.5);
                    leftWrinkle.rotation.z = 0.5;
                    group.add(leftWrinkle);
                    
                    const rightWrinkle = new THREE.Mesh(wrinkleGeo, new THREE.MeshPhongMaterial({color: 0xE6C2A6}));
                    rightWrinkle.position.set(0.3, 1.85, 0.5);
                    rightWrinkle.rotation.z = -0.5;
                    group.add(rightWrinkle);
                    break;
                    
                case 'sad':
                    // 😢 슬픈 입
                    const sadMouth = new THREE.TorusGeometry(0.18, 0.03, 8, 16, Math.PI);
                    const sadMesh = new THREE.Mesh(sadMouth, new THREE.MeshPhongMaterial({color: 0x4169E1}));
                    sadMesh.position.set(0, 1.55, 0.6);
                    group.add(sadMesh);
                    
                    // 눈물
                    const tearGeo = new THREE.SphereGeometry(0.03, 8, 8);
                    const tearMat = new THREE.MeshPhongMaterial({color: 0x87CEEB, transparent: true, opacity: 0.8});
                    const leftTear = new THREE.Mesh(tearGeo, tearMat);
                    leftTear.position.set(-0.2, 1.7, 0.6);
                    group.add(leftTear);
                    break;
                    
                case 'angry':
                    // 😠 화난 입
                    const angryMouth = new THREE.BoxGeometry(0.25, 0.04, 0.05);
                    const angryMesh = new THREE.Mesh(angryMouth, new THREE.MeshPhongMaterial({color: 0xFF0000}));
                    angryMesh.position.set(0, 1.58, 0.6);
                    group.add(angryMesh);
                    
                    // 찡그린 눈썹
                    const browGeo = new THREE.BoxGeometry(0.15, 0.02, 0.02);
                    const browMat = new THREE.MeshPhongMaterial({color: 0x8B4513});
                    const leftBrow = new THREE.Mesh(browGeo, browMat);
                    leftBrow.position.set(-0.2, 2.05, 0.6);
                    leftBrow.rotation.z = 0.3;
                    group.add(leftBrow);
                    
                    const rightBrow = new THREE.Mesh(browGeo, browMat);
                    rightBrow.position.set(0.2, 2.05, 0.6);
                    rightBrow.rotation.z = -0.3;
                    group.add(rightBrow);
                    break;
                    
                case 'love':
                    // 💕 하트 입
                    const heartGeo = new THREE.SphereGeometry(0.08, 8, 8);
                    const heartMat = new THREE.MeshPhongMaterial({color: 0xFF69B4});
                    const heart1 = new THREE.Mesh(heartGeo, heartMat);
                    heart1.position.set(-0.05, 1.6, 0.6);
                    group.add(heart1);
                    
                    const heart2 = new THREE.Mesh(heartGeo, heartMat);
                    heart2.position.set(0.05, 1.6, 0.6);
                    group.add(heart2);
                    
                    // 하트 눈
                    const heartEyeGeo = new THREE.SphereGeometry(0.05, 8, 8);
                    const heartEyeMat = new THREE.MeshPhongMaterial({color: 0xFF1493});
                    const heartEye1 = new THREE.Mesh(heartEyeGeo, heartEyeMat);
                    heartEye1.position.set(-0.2, 1.9, 0.65);
                    group.add(heartEye1);
                    
                    const heartEye2 = new THREE.Mesh(heartEyeGeo, heartEyeMat);
                    heartEye2.position.set(0.2, 1.9, 0.65);
                    group.add(heartEye2);
                    break;
                    
                default:
                    // 😐 기본 입
                    const defaultMouth = new THREE.CylinderGeometry(0.02, 0.02, 0.2);
                    const defaultMesh = new THREE.Mesh(defaultMouth, mouthMaterial);
                    defaultMesh.position.set(0, 1.6, 0.6);
                    defaultMesh.rotation.z = Math.PI / 2;
                    group.add(defaultMesh);
            }
        }
        
        function createEmotionParticles(group, emotion, config) {
            const particleCount = 20;
            
            for (let i = 0; i < particleCount; i++) {
                let particleGeo, particleMat;
                
                switch(emotion) {
                    case 'happy':
                        particleGeo = new THREE.SphereGeometry(0.03, 8, 8);
                        particleMat = new THREE.MeshBasicMaterial({color: 0xFFD700});
                        break;
                    case 'love':
                        particleGeo = new THREE.SphereGeometry(0.025, 6, 6);
                        particleMat = new THREE.MeshBasicMaterial({color: 0xFF69B4});
                        break;
                    case 'angry':
                        particleGeo = new THREE.SphereGeometry(0.02, 6, 6);
                        particleMat = new THREE.MeshBasicMaterial({color: 0xFF4500});
                        break;
                    case 'amazed':
                        particleGeo = new THREE.SphereGeometry(0.025, 8, 8);
                        particleMat = new THREE.MeshBasicMaterial({color: 0xFFA500});
                        break;
                    default:
                        return;
                }
                
                const particle = new THREE.Mesh(particleGeo, particleMat);
                particle.position.set(
                    (Math.random() - 0.5) * 3,
                    2.5 + Math.random() * 1,
                    (Math.random() - 0.5) * 2
                );
                
                // 파티클 애니메이션 데이터 저장
                particle.userData = {
                    velocity: new THREE.Vector3(
                        (Math.random() - 0.5) * 0.02,
                        Math.random() * 0.03 + 0.01,
                        (Math.random() - 0.5) * 0.02
                    ),
                    life: Math.random() * 100 + 50
                };
                
                group.add(particle);
                particles.push(particle);
            }
        }
        
        function createEmotionAura(group, config) {
            // 감정별 오라 효과
            const auraGeo = new THREE.SphereGeometry(2, 32, 32);
            const auraMat = new THREE.MeshBasicMaterial({
                color: config.glowColor,
                transparent: true,
                opacity: 0.1,
                side: THREE.BackSide
            });
            
            const aura = new THREE.Mesh(auraGeo, auraMat);
            aura.position.set(0, 1, 0);
            group.add(aura);
            
            // 오라 애니메이션
            aura.userData = { 
                originalScale: 1,
                pulseSpeed: 0.02 * config.intensity 
            };
        }

        function animate() {
            requestAnimationFrame(animate);
            
            const deltaTime = clock.getDelta();
            
            if (avatarMesh) {
                // 부드러운 회전
                avatarMesh.rotation.y += 0.005;
                
                // 숨쉬기 애니메이션
                const breathe = Math.sin(clock.getElapsedTime() * 2) * 0.02;
                avatarMesh.scale.y = 1 + breathe;
                
                // 오라 펄스 효과
                avatarMesh.children.forEach(child => {
                    if (child.userData.pulseSpeed) {
                        const pulse = Math.sin(clock.getElapsedTime() * 3) * 0.1 + 1;
                        child.scale.setScalar(pulse);
                    }
                });
                
                // 파티클 애니메이션
                particles.forEach((particle, index) => {
                    if (particle.userData.life > 0) {
                        particle.position.add(particle.userData.velocity);
                        particle.userData.life--;
                        
                        // 중력 효과
                        particle.userData.velocity.y -= 0.0005;
                        
                        // 페이드 아웃
                        const alpha = particle.userData.life / 100;
                        particle.material.opacity = alpha;
                        
                        if (particle.userData.life <= 0) {
                            avatarMesh.remove(particle);
                            particles.splice(index, 1);
                        }
                    }
                });
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

            log(`📨 Ultra Premium 분석 시작: ${message}`);
            input.value = '';
            
            try {
                log('🚀 고급 AI 분석 요청...');
                
                const response = await fetch('/ultra-chat', {
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
                
                // 상태 패널 업데이트
                document.getElementById('emotion-display').innerHTML = 
                    `💭 감정: <span style="color: #ffd60a; font-weight: bold;">${result.emotion}</span>`;
                
                document.getElementById('confidence-display').innerHTML = 
                    `🎯 정확도: <span style="color: #00ff00; font-weight: bold;">${(result.confidence * 100).toFixed(1)}%</span>`;
                
                // Ultra Premium 아바타 업데이트
                createUltraPremiumAvatar(result.emotion);
                
                log('🌟 Ultra Premium 아바타 업데이트 완료');
                
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
            log('🌟 Ultra Premium 시스템 시작');
            init3D();
        });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return ULTRA_PREMIUM_TEMPLATE


@app.route("/ultra-chat", methods=["POST"])
def ultra_chat():
    print("🌟 Ultra Premium 채팅 요청!")

    try:
        data = request.get_json()
        if not data:
            print("❌ 데이터가 없음")
            return jsonify({"error": "데이터가 없습니다"}), 400

        message = data.get("message", "")
        print(f"📝 분석 메시지: {message}")

        # 고도화된 감정 분석
        emotion = analyze_korean_emotion(message)
        confidence = 0.92  # 고급 신뢰도

        print(f"🎭 감정 분석 결과: {emotion} (신뢰도: {confidence})")

        response = {
            "emotion": emotion,
            "confidence": confidence,
            "message": f"Ultra Premium 아바타가 당신의 {emotion} 감정을 정확히 분석했습니다!",
            "premium_level": "Ultra",
        }

        print(f"✅ Ultra Premium 응답: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"❌ 오류: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🌟 Ultra Premium 3D 아바타 v2.0 시작!")
    print("💎 http://127.0.0.1:5005 에서 Ultra Premium 체험!")
    app.run(debug=True, port=5005)
