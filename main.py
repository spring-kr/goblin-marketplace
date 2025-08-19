"""
🚀 도깨비마을장터 BETA - 무료 체험 서비스
촌장급 도깨비 전문가들과 함께하는 STEM 베타 서비스
버전: v4.0.0 - 베타 서비스 최적화
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

# STEM 통합 임포트
from stem_integration import setup_stem_routes

# FastAPI 앱 생성
app = FastAPI(
    title="🏪 도깨비마을장터 BETA - 촌장급 도깨비 에이전트",
    description="8명의 촌장급 도깨비 전문가들 + 무료 베타 체험",
    version="4.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# STEM 라우트 설정
setup_stem_routes(app)

@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지 - 베타 서비스 소개"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body>
                <h1>🏪 도깨비마을장터 BETA</h1>
                <p>촌장급 도깨비 전문가들이 무료로 서비스 중입니다!</p>
                <a href="/stem">🧙‍♂️ STEM 서비스 이용하기</a>
            </body>
        </html>
        """

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "version": "4.0.0", "service": "도깨비마을장터 BETA"}

if __name__ == "__main__":
    import uvicorn
    print("🏪 도깨비마을장터 BETA 서비스 시작 중...")
    print("🧙‍♂️ 촌장급 도깨비들이 대기 중입니다!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
