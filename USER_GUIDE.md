# 🚀 HYOJIN.AI AI 에이전트 저장소 사용자 가이드

## 🎯 빠른 시작 가이드

### 1️⃣ 플랫폼 접속
- **메인 플랫폼**: https://hyojin-ai-mvp.onrender.com/
- **AI 마켓플레이스**: https://hyojin-ai-mvp.onrender.com/agents/marketplace
- **관리자 대시보드**: https://hyojin-ai-mvp.onrender.com/admin/subscription-management

### 2️⃣ 계정 생성 및 구독
1. 메인 페이지에서 **"무료 체험 시작하기"** 클릭
2. 이메일, 회사명, 플랜 선택
3. 7일 무료 체험 자동 시작
4. AI 에이전트 마켓플레이스 즉시 이용 가능

---

## 🤖 AI 에이전트 사용 방법

### 📋 1단계: 마켓플레이스 탐색
```
🏪 AI 에이전트 마켓플레이스 접속
→ 15개 전문 에이전트 카탈로그 확인
→ 각 에이전트의 자율성 지수 및 역량 검토
→ 플랜별 접근 가능한 에이전트 확인
```

### 🎯 2단계: 에이전트 선택
| 플랜 | 이용 가능 에이전트 | 개수 |
|------|------------------|------|
| **Trial** | Developer, Marketing | 2개 |
| **Startup** | Strategy, Developer, Marketing | 3개 |
| **Professional** | Strategy, DataScience, Developer, Marketing, Finance | 5개 |
| **Enterprise** | 모든 에이전트 + 독점 기능 | 5개+ |

### ⚡ 3단계: 에이전트 배포
1. **마켓플레이스에서 원하는 에이전트 선택**
2. **"🚀 에이전트 배포" 버튼 클릭**
3. **이메일 주소 입력** (구독자 확인용)
4. **배포 완료 알림 및 배포 ID 수령**

---

## 🎨 에이전트별 활용 가이드

### 🔬 Strategy Agent (전략 에이전트)
**🎯 전문 분야**: McKinsey 컨설턴트 수준의 전략 기획
- **활용 사례**: 시장 진입 전략, 경쟁사 분석, 비즈니스 모델 설계
- **자율성 지수**: 95%
- **필요 플랜**: Startup 이상
```
📝 사용 예시:
"중국 시장 진입을 위한 3년 전략 계획을 수립해주세요.
경쟁사는 A사, B사이며, 우리 제품은 스마트 홈 IoT입니다."
```

### 💻 DataScience Agent (데이터사이언스 에이전트)
**🎯 전문 분야**: Google AI 연구원 수준의 데이터 분석
- **활용 사례**: 고객 행동 예측, 매출 예측, 추천 시스템 구축
- **자율성 지수**: 92%
- **필요 플랜**: Professional 이상
```
📊 사용 예시:
"고객 구매 이력 데이터를 바탕으로 다음 분기 매출을 예측하고,
상위 20% 고객의 특성을 분석해주세요."
```

### 🎯 Developer Agent (개발 에이전트)
**🎯 전문 분야**: Meta, Google 시니어 개발자 수준의 풀스택 개발
- **활용 사례**: 웹 애플리케이션 개발, API 설계, 코드 리팩토링
- **자율성 지수**: 89%
- **필요 플랜**: Trial 이상 (모든 플랜)
```
💻 사용 예시:
"React와 FastAPI를 사용해서 todo 앱을 만들어주세요.
사용자 인증, CRUD 기능, 실시간 동기화가 필요합니다."
```

### 💰 Marketing Agent (마케팅 에이전트)
**🎯 전문 분야**: Netflix, Apple CMO 수준의 브랜딩 및 캠페인
- **활용 사례**: 캠페인 전략, 브랜드 포지셔닝, 성과 최적화
- **자율성 지수**: 87%
- **필요 플랜**: Trial 이상 (모든 플랜)
```
🎪 사용 예시:
"Z세대를 타겟으로 한 소셜미디어 마케팅 캠페인을 기획해주세요.
제품은 친환경 화장품이고 예산은 월 500만원입니다."
```

### ✨ Finance Agent (금융 에이전트)
**🎯 전문 분야**: Goldman Sachs 애널리스트 수준의 투자 분석
- **활용 사례**: 포트폴리오 최적화, 리스크 분석, 투자 전략
- **자율성 지수**: 94%
- **필요 플랜**: Professional 이상
- **상태**: 🚀 Coming Soon
```
💎 사용 예시:
"1억원 투자 자금으로 향후 5년간 연 10% 수익을 목표로 한
포트폴리오를 구성하고 리스크를 분석해주세요."
```

---

## 🔧 고급 기능 활용

### 📊 API 직접 호출
개발자를 위한 직접 API 호출 방법:

```javascript
// 에이전트 실행 API 호출
const executeAgent = async (agentType, task) => {
    const response = await fetch('https://hyojin-ai-mvp.onrender.com/agents/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            agent_type: agentType,
            task_description: task,
            parameters: {}
        })
    });
    
    const result = await response.json();
    return result;
};

// 사용 예시
const result = await executeAgent('strategy', '시장 분석 요청');
console.log(result);
```

### 🔗 웹훅 연동
에이전트 실행 결과를 자동으로 받는 방법:

```python
# 웹훅 URL 설정 (향후 기능)
webhook_config = {
    "url": "https://your-domain.com/webhook",
    "events": ["agent_completed", "agent_failed"],
    "secret": "your_webhook_secret"
}
```

---

## 🎛️ 관리자 기능

### 📊 구독관리 대시보드 사용법
**접속**: https://hyojin-ai-mvp.onrender.com/admin/subscription-management

#### 주요 기능:
1. **📈 실시간 통계 모니터링**
   - 총 구독자 수
   - 무료체험 중인 사용자
   - 유료 구독자 수
   - 총 API 호출 횟수

2. **👥 구독자 관리**
   - 구독자 목록 조회
   - 플랜 변경
   - 계정 일시정지/재활성화
   - 사용량 모니터링

3. **🤖 에이전트 배포 현황**
   - 에이전트별 사용 통계
   - 인기 에이전트 순위
   - 성능 메트릭 확인

### 🔄 시스템 상태 확인
**접속**: https://hyojin-ai-mvp.onrender.com/admin/system-status

```json
{
    "status": "healthy",
    "version": "3.0.0",
    "ai_agents": {
        "total": 5,
        "available": 4,
        "coming_soon": 1
    },
    "uptime": "99.9%"
}
```

---

## 🎯 플랜별 상세 비교

### 💡 Trial (무료 체험)
- **🕐 기간**: 7일
- **🤖 에이전트**: Developer, Marketing (2개)
- **📞 지원**: 이메일 지원
- **💰 가격**: 무료

### 🚀 Startup
- **🤖 에이전트**: Strategy, Developer, Marketing (3개)
- **⏱️ 작업시간**: 월 1,000시간
- **📞 지원**: 24시간 내 응답
- **💰 가격**: ₩299,000/월

### 💼 Professional
- **🤖 에이전트**: 5개 모든 기본 에이전트
- **⏱️ 작업시간**: 월 5,000시간
- **🔧 추가기능**: 커스텀 에이전트 생성, API 통합
- **💰 가격**: ₩899,000/월

### 🏢 Enterprise
- **🤖 에이전트**: 15개 모든 에이전트 + 독점 기능
- **⏱️ 작업시간**: 무제한
- **🏆 특별혜택**: 온프레미스 배포, SLA 보장, 전담 지원팀
- **💰 가격**: ₩2,999,000/월

---

## 🆘 문제 해결 (FAQ)

### ❓ 자주 묻는 질문

**Q: 에이전트 배포가 안 되요**
```
A: 다음을 확인해주세요:
1. 구독자 이메일이 정확한지 확인
2. 현재 플랜에서 해당 에이전트 이용 가능한지 확인
3. 브라우저 새로고침 후 재시도
4. 네트워크 연결 상태 확인
```

**Q: 에이전트가 응답하지 않아요**
```
A: 일반적인 해결 방법:
1. 작업 설명을 더 구체적으로 작성
2. 복잡한 작업은 단계별로 분할 요청
3. 30초 이상 기다려보기
4. 다른 에이전트로 시도해보기
```

**Q: 플랜 업그레이드는 어떻게 하나요?**
```
A: 업그레이드 방법:
1. 관리자 대시보드 접속
2. "플랜 변경" 버튼 클릭
3. 원하는 플랜 선택
4. 결제 정보 입력
5. 즉시 적용 (다운타임 없음)
```

### 🔧 기술 지원

**📧 이메일 지원**: support@hyojin-ai.com
**📞 전화 지원**: 1588-0000 (Enterprise 플랜)
**💬 실시간 채팅**: 플랫폼 내 지원 채널

### 🌐 추가 리소스

- **📚 API 문서**: https://hyojin-ai-mvp.onrender.com/docs
- **🎥 튜토리얼 영상**: YouTube 채널 (준비 중)
- **💬 커뮤니티**: Discord 서버 (준비 중)
- **📖 블로그**: 기술 블로그 (준비 중)

---

## 🎉 성공 사례

### 🏆 Case Study 1: 스타트업 A사
**업종**: 핀테크  
**사용 에이전트**: Strategy + DataScience  
**성과**: 시장 분석 시간 80% 단축, 데이터 기반 의사결정 향상

### 🏆 Case Study 2: 중견기업 B사
**업종**: 이커머스  
**사용 에이전트**: Marketing + Developer  
**성과**: 개발 속도 3배 향상, 마케팅 ROI 150% 개선

---

**📅 가이드 최종 업데이트**: 2025년 1월 18일  
**📱 플랫폼 버전**: HYOJIN.AI MVP v3.0  
**🎯 지원 언어**: 한국어, 영어 (준비 중)  

---

> 🚀 **지금 시작하세요!**  
> 7일 무료 체험으로 AI 에이전트의 놀라운 능력을 직접 경험해보세요!  
> **https://hyojin-ai-mvp.onrender.com** 👈 클릭하여 시작! 🎯
