# 🧠 HYOJIN.AI Core API

Railway 클라우드에 배포된 AI 시스템입니다.

## 🚀 배포 정보

- **플랫폼**: Railway (무료 티어)
- **프레임워크**: FastAPI
- **데이터베이스**: SQLite
- **AI 도메인**: 6개 (결제/배달/쇼핑/부동산/교육/채용)

## 📱 API 엔드포인트

### 메인
- `GET /` - API 정보
- `GET /health` - 헬스체크
- `GET /docs` - API 문서 (Swagger)

### AI 도메인들
- `POST /api/v1/payment/process` - 결제 AI
- `POST /api/v1/delivery/process` - 배달 AI
- `POST /api/v1/shopping/process` - 쇼핑 AI
- `POST /api/v1/realestate/process` - 부동산 AI
- `POST /api/v1/education/process` - 교육 AI
- `POST /api/v1/jobs/process` - 채용 AI

## 🛠️ 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

## 🚂 Railway 배포

1. Railway 계정 생성: https://railway.app
2. GitHub 연동 후 이 레포지토리 연결
3. 자동 배포 완료!

## 📊 사용 예시

```python
import requests

# 결제 분석 요청
response = requests.post("https://your-app.railway.app/api/v1/payment/process", 
    json={
        "action": "analyze_transaction",
        "data": {"amount": 50000, "merchant": "스타벅스"},
        "user_id": "user123"
    }
)

print(response.json())
```

## 📈 모니터링

- Railway 대시보드에서 실시간 로그 확인
- `/health` 엔드포인트로 상태 모니터링
- 무료 티어: 500시간/월 (월 $0)

## 🔧 개발자 정보

- 개발: HYOJIN.AI Team
- 버전: 1.0.0-MVP
- 라이센스: MIT


## 🚂 배포 옵션들

### 🥇 1순위: Render (무료 추천)
```bash
# render.yaml 설정 파일 포함됨
# 1. https://render.com 가입
# 2. GitHub 저장소 연결
# 3. 자동 배포 완료!
```

### 🥈 2순위: Vercel (서버리스)
```bash
# vercel.json 설정 파일 포함됨
# 1. https://vercel.com 가입
# 2. GitHub 저장소 연결
# 3. 서버리스 배포 완료!
```

### 🥉 3순위: Deta Space (완전무료)
```bash
# Spacefile 설정 파일 포함됨
# 1. https://deta.space 가입
# 2. CLI로 배포
# 3. 베타 서비스이지만 완전 무료!
```

## 💰 비용 비교
- **Render**: 750시간/월 무료
- **Vercel**: 서버리스 무료
- **Deta**: 완전 무료 (베타)
- **Railway**: $5/월 (유료화됨)

## 📋 배포 가이드
자세한 배포 방법은 `RENDER_DEPLOYMENT_GUIDE.md`를 참고하세요!

---
*업데이트: 2025-08-17 - 무료 배포 옵션 추가*
