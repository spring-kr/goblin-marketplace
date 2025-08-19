# 🎯 STEM급 에이전트 구독 서비스 - Render 배포 가이드

## 🚀 Render 배포 방법

### 1단계: GitHub 저장소 준비
1. STEM_Agent_Collection 폴더를 새로운 GitHub 저장소로 업로드
2. 다음 파일들이 루트에 있는지 확인:
   - `integrated_subscription_service.py` (메인 앱 파일)
   - `requirements.txt` (Python 패키지 목록)
   - `Procfile` (Render 실행 명령)
   - `runtime.txt` (Python 버전)

### 2단계: Render 계정 생성 및 서비스 생성
1. https://render.com 접속 후 GitHub 계정으로 로그인
2. "New +" → "Web Service" 선택
3. GitHub 저장소 연결
4. 다음 설정 입력:
   - **Name**: `hyojin-stem-agents`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn integrated_subscription_service:app`
   - **Plan**: Free (무료)

### 3단계: 환경 변수 설정
Environment Variables에서 다음 추가:
- `FLASK_ENV`: `production`
- `PYTHONPATH`: `/opt/render/project/src`

### 4단계: 배포 및 확인
1. "Create Web Service" 클릭
2. 배포 로그 확인
3. 배포 완료 후 `https://hyojin-stem-agents.onrender.com` 접속 테스트

## 📁 필요한 파일 구조

```
STEM_Agent_Collection/
├── integrated_subscription_service.py  # 메인 Flask 앱
├── requirements.txt                     # Python 패키지
├── Procfile                            # Render 실행 명령
├── runtime.txt                         # Python 버전
├── templates/                          # HTML 템플릿
│   ├── token_login.html
│   └── stem_dashboard.html
├── math_genius_20250819_134854_response.py
├── physics_master_20250819_134854_response.py
├── chemistry_expert_20250819_134854_response.py
├── biology_genius_20250819_134854_response.py
├── engineering_wizard_20250819_134854_response.py
├── real_quality_assistant.py
├── marketing_strategist.py
└── startup_consultant.py
```

## 🔧 배포 후 설정

### GitHub Pages 업데이트
`hyojin-ai-mvp` 저장소의 `index.html`에서:
```javascript
const stemServiceUrl = 'https://hyojin-stem-agents.onrender.com';
```

### 서비스 연결 테스트
1. https://hyojin-ai-mvp.onrender.com 접속
2. 상품 구매 및 결제
3. 생성된 토큰으로 https://hyojin-stem-agents.onrender.com 로그인
4. 8개 에이전트와 대화 테스트

## 🎯 완성된 서비스 플로우

```
사용자 → hyojin-ai-mvp.onrender.com → 구독 구매 → 토큰 생성
     ↓
토큰 복사 → hyojin-stem-agents.onrender.com → 로그인 → AI 대화
```

## 💡 배포 팁

1. **무료 플랜 제한**: Render 무료 플랜은 15분 비활성 시 슬립 모드
2. **첫 접속 지연**: 슬립 모드에서 깨어나는데 30초-1분 소요
3. **로그 확인**: Render 대시보드에서 실시간 로그 모니터링 가능
4. **도메인 설정**: 커스텀 도메인 연결 가능 (유료 플랜)

## 🔥 성공 확인

배포 성공 시 로그에 다음 메시지 표시:
```
✅ math 에이전트 로드 성공
✅ physics 에이전트 로드 성공
✅ chemistry 에이전트 로드 성공
✅ biology 에이전트 로드 성공
✅ engineering 에이전트 로드 성공
✅ assistant 에이전트 로드 성공
✅ marketing 에이전트 로드 성공
✅ startup 에이전트 로드 성공
🎯 STEM급 에이전트 구독 서비스 시작!
```

**이제 전 세계 어디서나 STEM급 에이전트와 대화할 수 있습니다!** 🌍✨
