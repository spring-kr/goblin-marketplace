# 🚂 Railway 배포 가이드

## 1️⃣ Railway 계정 준비

1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. 무료 계정 생성

## 2️⃣ 프로젝트 업로드

### GitHub 방식 (추천)
```bash
# Git 초기화
git init
git add .
git commit -m "Initial commit"

# GitHub에 레포지토리 생성 후
git remote add origin https://github.com/username/hyojin-ai-mvp.git
git push -u origin main
```

### 직접 업로드 방식
1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 레포지토리 연결

## 3️⃣ 환경 변수 설정

Railway 대시보드에서:
- `PORT`: 8000 (자동 설정됨)
- `DB_PATH`: /app/data/hyojin_ai.db

## 4️⃣ 배포 확인

1. 배포 로그 확인
2. 생성된 URL로 접속
3. `/health` 엔드포인트 테스트
4. `/docs`에서 API 문서 확인

## 🎯 배포 후 테스트

```bash
# 헬스체크
curl https://your-app.railway.app/health

# AI API 테스트
curl -X POST "https://your-app.railway.app/api/v1/payment/process" \
  -H "Content-Type: application/json" \
  -d '{"action": "analyze_transaction", "data": {"amount": 10000}}'
```

## 📊 무료 티어 제한

- **CPU**: 제한적
- **메모리**: 512MB
- **시간**: 500시간/월
- **대역폭**: 제한적
- **저장소**: 1GB

## 🚀 다음 단계

1. 커스텀 도메인 연결
2. 데이터베이스 업그레이드 (PostgreSQL)
3. Redis 캐시 추가
4. 모니터링 시스템 구축
