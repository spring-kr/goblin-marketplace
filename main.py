"""
🎯 AI 도깨비마을 STEM 센터 BETA - 무료 체험 서비스
8명의 촌장급 STEM 전문가 도깨비들과 함께하는 베타 서비스
버전: v4.1.0 - STEM 전용 최적화
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

# STEM 통합 임포트
from stem_integration import add_stem_routes

# FastAPI 앱 생성
app = FastAPI(
    title="🎯 AI 도깨비마을 STEM 센터",
    description="8명의 촌장급 STEM 전문가 도깨비들 + 무료 베타 체험",
    version="4.1.0",
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
add_stem_routes(app)


# 서버 시작시 샘플 데이터 확인 및 생성
@app.on_event("startup")
async def startup_event():
    """서버 시작시 실행되는 이벤트"""
    try:
        # 사용량 로그 확인
        from usage_tracker import usage_tracker

        stats = usage_tracker.get_statistics()

        # 데이터가 없으면 샘플 데이터 생성
        if stats.get("total_usage", 0) == 0:
            print("🔄 사용량 데이터가 없어 샘플 데이터를 생성합니다...")
            try:
                from generate_test_data import generate_test_data

                generate_test_data()
                print("✅ 샘플 데이터 생성 완료!")
            except Exception as e:
                print(f"⚠️ 샘플 데이터 생성 실패: {e}")
        else:
            print(f"📊 기존 사용량 데이터 {stats['total_usage']}개 발견")

    except Exception as e:
        print(f"⚠️ 시작 이벤트 처리 중 오류: {e}")


@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지 - STEM 베타 서비스 소개"""
    try:
        with open("index_stem.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body>
                <h1>🎯 AI 도깨비마을 STEM 센터</h1>
                <p>8명의 촌장급 STEM 전문가 도깨비들이 무료로 서비스 중입니다!</p>
                <a href="/stem">🧙‍♂️ STEM 서비스 이용하기</a>
            </body>
        </html>
        """


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "version": "4.1.0",
        "service": "STEM 도깨비마을장터 BETA",
        "agents": 8,
    }


@app.get("/demo/{service_id}", response_class=HTMLResponse)
async def demo_redirect(service_id: str):
    """가상 도깨비 데모는 제거됨 - STEM 서비스로 리다이렉트"""
    return HTMLResponse(
        """
    <html>
        <head>
            <meta http-equiv="refresh" content="3; url=/">
        </head>
        <body style="text-align: center; font-family: Arial; padding: 50px;">
            <h2>🧙‍♂️ 실제 있는 STEM 도깨비들을 만나보세요!</h2>
            <p>가상 도깨비는 제거되었습니다.</p>
            <p>3초 후 메인 페이지로 이동합니다...</p>
            <a href="/">지금 바로 이동하기</a>
        </body>
    </html>
    """
    )


@app.get("/stem", response_class=HTMLResponse)
async def stem_service():
    """STEM 도깨비 서비스 메인 페이지"""
    try:
        with open("index_stem.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(
            """
        <html>
            <head><title>STEM 서비스 오류</title></head>
            <body>
                <h1>❌ STEM 서비스 파일을 찾을 수 없습니다</h1>
                <p>index_stem.html 파일이 필요합니다.</p>
                <a href="/">홈으로 돌아가기</a>
            </body>
        </html>
        """,
            status_code=404,
        )


@app.get("/agents", response_class=HTMLResponse)
async def all_agents():
    """실제 있는 8개 STEM 도깨비 에이전트 목록"""
    stem_agents = {
        "math": {
            "name": "🧮 수학 전문가 도깨비",
            "features": ["미적분", "대수", "통계", "수학적 모델링"],
        },
        "physics": {
            "name": "⚛️ 물리학 전문가 도깨비",
            "features": ["역학", "전자기학", "양자물리", "물리 현상 분석"],
        },
        "chemistry": {
            "name": "🧪 화학 전문가 도깨비",
            "features": ["유기화학", "무기화학", "화학 반응", "분자 구조"],
        },
        "biology": {
            "name": "🧬 생물학 전문가 도깨비",
            "features": ["분자생물학", "생태학", "유전학", "생명 현상"],
        },
        "engineering": {
            "name": "⚙️ 공학 전문가 도깨비",
            "features": ["공학 설계", "시스템 분석", "최적화", "혁신 솔루션"],
        },
        "assistant": {
            "name": "🤖 업무 도우미 도깨비",
            "features": ["업무 최적화", "프로젝트 관리", "효율성", "품질 관리"],
        },
        "marketing": {
            "name": "📈 마케팅 전문가 도깨비",
            "features": ["마케팅 전략", "브랜딩", "시장 분석", "고객 인사이트"],
        },
        "startup": {
            "name": "🚀 스타트업 전문가 도깨비",
            "features": ["스타트업 전략", "사업 계획", "투자 유치", "비즈니스 모델"],
        },
    }

    agents_html = ""
    for agent_id, info in stem_agents.items():
        agents_html += f"""
        <div style="border: 2px solid #4CAF50; margin: 10px 0; padding: 15px; border-radius: 10px;">
            <h3>{info['name']}</h3>
            <p>전문 분야: {', '.join(info['features'])}</p>
            <a href="/stem/demo?agent={agent_id}" 
               style="background: #4CAF50; color: white; padding: 8px 15px; 
                      text-decoration: none; border-radius: 5px;">체험하기</a>
        </div>
        """

    return f"""
    <html>
        <head><title>🎯 AI 도깨비마을 STEM 센터</title></head>
        <body style="font-family: Arial; max-width: 1000px; margin: 50px auto; padding: 20px;">
            <h1>🎯 AI 도깨비마을 STEM 센터</h1>
            <p>8명의 STEM 전문가 도깨비들을 무료로 체험해보세요!</p>
            {agents_html}
            <br><a href="/" style="background: #2196F3; color: white; padding: 10px 20px; 
                         text-decoration: none; border-radius: 5px;">🔙 메인으로</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    print("🎯 AI 도깨비마을 STEM 센터 시작 중...")
    print("🧙‍♂️ 8명의 STEM 전문가 도깨비들이 대기 중입니다!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
