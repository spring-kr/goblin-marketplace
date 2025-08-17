# 📤 GitHub 업로드 가이드

## 🎯 저장소 정보
- **저장소명**: hyojin-ai-mvp
- **GitHub URL**: https://github.com/spring-kr/hyojin-ai-mvp
- **생성일**: 2025-08-17 18:18:26

## 🔄 업로드 완료된 파일들
- `main.py` - FastAPI 메인 애플리케이션
- `requirements.txt` - Python 의존성
- `Procfile` - Railway 실행 명령
- `railway.json` - Railway 설정
- `README.md` - 프로젝트 문서
- `app/` - AI 엔진 및 API 코드

## 🚂 Railway 배포 방법

### 1단계: Railway 계정 생성
1. https://railway.app 접속
2. "Login with GitHub" 클릭
3. GitHub 계정으로 로그인

### 2단계: 프로젝트 생성
1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. "hyojin-ai-mvp" 저장소 선택

### 3단계: 자동 배포
1. Railway가 자동으로 빌드 시작
2. 5-10분 후 배포 완료
3. 생성된 URL 확인

### 4단계: 테스트
```bash
# 생성된 URL로 테스트 (예시)
curl https://your-app.railway.app/health
curl https://your-app.railway.app/docs
```

## 🔧 로컬 테스트

```bash
# 프로젝트 클론
git clone https://github.com/spring-kr/hyojin-ai-mvp.git
cd hyojin-ai-mvp

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

## 💰 비용 정보
- **Railway 무료 티어**: 500시간/월
- **GitHub**: 무료 (퍼블릭 저장소)
- **총 비용**: $0/월

## 🎉 배포 완료 후
1. API 문서: `https://your-app.railway.app/docs`
2. 헬스체크: `https://your-app.railway.app/health`
3. AI 테스트: 각 도메인 API 엔드포인트 사용

## 📞 지원
- Railway 문서: https://docs.railway.app
- GitHub Issues: https://github.com/spring-kr/hyojin-ai-mvp/issues
