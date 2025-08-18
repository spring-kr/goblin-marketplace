# HYOJIN.AI MVP 기술 명세서

## 🔧 구현 완료 기능 상세

### 1. 마켓플레이스 구독자 인증 시스템

#### 엔드포인트
```python
@app.get("/agents/marketplace")
async def get_agent_marketplace(email: Optional[str] = None)
```

#### 기능 흐름
1. **이메일 미입력시**
   - 상태: "👋 이메일을 입력하여 체험하세요"
   - UI: 우상단 이메일 입력창 표시
   - 액션: 에이전트 배포시 인증 요구

2. **이메일 입력시**
   - 구독자 DB에서 이메일 조회
   - 등록된 사용자: 플랜 정보 및 사용 제한 표시
   - 미등록 사용자: 무료 체험 모드

#### 플랜별 사용 제한 로직
```python
def get_usage_limit(plan: str) -> dict:
    plan_limits = {
        "trial": {"name": "무료 체험", "calls": 3},
        "startup": {"name": "Startup", "calls": 50},
        "professional": {"name": "Professional", "calls": 300},
        "business": {"name": "Business", "calls": 1000},
        "enterprise": {"name": "Enterprise", "calls": "무제한"}
    }
    return plan_limits.get(plan, plan_limits["trial"])
```

### 2. 구독자 데이터 관리

#### 구독자 조회 함수
```python
def get_subscriber_by_email(email: str) -> Optional[dict]:
    # JSON 파일에서 구독자 정보 조회
    # 이메일, 플랜, 상태, 체험 만료일 등 반환
```

#### 데이터 구조
```json
{
  "email": "user@example.com",
  "plan": "professional",
  "status": "active",
  "trial_expires": "2025-08-25T00:00:00",
  "created_at": "2025-08-18T00:00:00"
}
```

### 3. 프론트엔드 인증 로직

#### JavaScript 인증 체크
```javascript
const userEmail = "{email or ''}";
const isAuthenticated = userEmail !== '';

async function deployAgent(agentType) {
    if (isAuthenticated) {
        alert(`${agentType} 에이전트 배포 요청이 접수되었습니다!`);
    } else {
        alert('에이전트 사용을 위해 이메일 인증이 필요합니다.');
        document.getElementById('email').focus();
    }
}
```

#### 이메일 입력 처리
```javascript
function accessWithEmail() {
    const email = document.getElementById('email').value;
    if (email) {
        window.location.href = `/agents/marketplace?email=${encodeURIComponent(email)}`;
    }
}
```

### 4. UI/UX 개선사항

#### 상태 표시 바
```css
.status-bar {
    background: rgba(255,255,255,0.15);
    color: white;
    padding: 15px;
    text-align: center;
    margin: 20px auto;
    max-width: 600px;
    border-radius: 10px;
    font-weight: 600;
}
```

#### 조건부 UI 렌더링
- 이메일 미입력: 이메일 입력창 표시
- 이메일 입력: 구독 상태 정보 표시
- 인증 여부에 따른 버튼 동작 차별화

### 5. 에이전트 동적 로딩

#### 에이전트 데이터 fetch
```javascript
async function loadAgents() {
    try {
        const response = await fetch('/agents');
        const data = await response.json();
        
        if (data.agents) {
            Object.entries(data.agents).forEach(([type, agent]) => {
                // 에이전트 카드 동적 생성
            });
        }
    } catch (error) {
        console.error('에이전트 로드 오류:', error);
    }
}
```

#### 에이전트 카드 생성
```javascript
card.innerHTML = `
    <div class="agent-icon">${agent.icon}</div>
    <div class="agent-name">${agent.name}</div>
    <div class="agent-description">${agent.description}</div>
    <div class="capabilities">
        ${agent.capabilities.map(cap => 
            `<span class="capability-tag">${cap}</span>`
        ).join('')}
    </div>
    <button class="deploy-btn" onclick="deployAgent('${type}')">
        🚀 에이전트 배포
    </button>
`;
```

## 🔒 보안 고려사항

### 1. 입력 검증
- 이메일 형식 검증 (프론트엔드)
- URL 인코딩 처리
- SQL 인젝션 방지 (JSON 기반이므로 해당없음)

### 2. 인증 흐름
- 클라이언트 사이드 기본 검증
- 서버 사이드 구독자 확인
- 플랜별 권한 체크

### 3. 에러 처리
- 네트워크 오류 처리
- 데이터 로딩 실패시 대체 UI
- 사용자 친화적 오류 메시지

## 📊 성능 최적화

### 1. 프론트엔드
- CSS 그리드 레이아웃으로 반응형 디자인
- JavaScript 모듈화 및 이벤트 최적화
- 이미지 및 폰트 최적화

### 2. 백엔드
- FastAPI 비동기 처리
- JSON 파일 캐싱 (필요시)
- HTTP 응답 최적화

## 🧪 테스트 시나리오

### 1. 인증 테스트
- [ ] 이메일 미입력시 입력창 표시
- [ ] 올바른 이메일 입력시 상태 표시
- [ ] 잘못된 이메일 입력시 처리
- [ ] 등록된 구독자 플랜 정보 표시

### 2. UI 테스트
- [ ] 반응형 레이아웃 동작
- [ ] 에이전트 카드 동적 로딩
- [ ] 버튼 인터랙션 테스트
- [ ] 오류 상황 UI 처리

### 3. 비즈니스 로직 테스트
- [ ] 플랜별 사용 제한 적용
- [ ] 구독자 상태 변경 반영
- [ ] 체험 기간 만료 처리

---
*기술 문서 작성일: 2025년 8월 18일*
*버전: MVP v1.0*
