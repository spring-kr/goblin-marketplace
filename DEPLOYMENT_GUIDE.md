# 🚀 배포 가이드

## 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn main:app --reload --port 8000

# 브라우저에서 확인
# http://localhost:8000
```

## 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# 필요한 환경 변수 설정
STRIPE_PUBLISHABLE_KEY=your_key_here
STRIPE_SECRET_KEY=your_secret_here
```

## 배포 플랫폼

- **Render**: render.yaml 사용
- **Railway**: Procfile 사용  
- **Vercel**: main.py 엔트리포인트

---
*DevOps 팀 작성*
