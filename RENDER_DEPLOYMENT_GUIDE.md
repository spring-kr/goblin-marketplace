# 🚀 Render 배포 가이드 (Railway 무료 대안)

## 1️⃣ Render 계정 생성
1. https://render.com 접속
2. "Get Started for Free" 클릭
3. GitHub 계정으로 가입

## 2️⃣ 웹 서비스 생성
1. Render 대시보드에서 "New +" 클릭
2. "Web Service" 선택
3. GitHub 저장소 연결: spring-kr/hyojin-ai-mvp

## 3️⃣ 배포 설정
- **Name**: hyojin-ai-mvp
- **Environment**: Python 3
- **Build Command**: pip install -r requirements.txt
- **Start Command**: uvicorn main:app --host 0.0.0.0 --port $PORT
- **Plan**: Free (0$/month)

## 4️⃣ 환경 변수 (선택사항)
- PORT: 자동 설정
- PYTHON_VERSION: 3.11.0

## 🆓 무료 플랜 제한
- **시간**: 750시간/월 (충분함)
- **메모리**: 512MB RAM
- **CPU**: 0.1 CPU 유닛
- **저장소**: 제한 없음
- **대역폭**: 100GB/월

## ⚡ 장점
- Railway와 거의 동일한 기능
- GitHub 연동 자동 배포
- 커스텀 도메인 지원
- 자동 SSL 인증서
- 무료 플랜 안정적

## 🎯 배포 완료 후
생성된 URL: https://hyojin-ai-mvp-abc123.onrender.com
