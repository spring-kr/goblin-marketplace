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

# 가상 서비스 매니저 임포트
from virtual_service_manager import virtual_service_manager

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


@app.get("/demo/{service_id}", response_class=HTMLResponse)
async def demo_agent(service_id: str, token: str = "beta"):
    """가상 도깨비 에이전트 데모 페이지"""
    service_info = virtual_service_manager.service_templates.get(service_id)
    if not service_info:
        return HTMLResponse(
            "🧙‍♂️ 이런! 이 도깨비는 아직 마을에 없어요!", status_code=404
        )

    return f"""
    <html>
        <head>
            <title>{service_info['name']} - 도깨비마을장터</title>
            <style>
                body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; border-radius: 15px; text-align: center; }}
                .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                           gap: 15px; margin: 20px 0; }}
                .feature {{ background: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; }}
                .demo-area {{ background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .back-btn {{ background: #2196F3; color: white; padding: 10px 20px; 
                           text-decoration: none; border-radius: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏪 {service_info['name']} 데모</h1>
                <p>전문 분야 도깨비 에이전트 체험하기</p>
                <small>토큰: {token or '베타 체험'}</small>
            </div>
            
            <div class="features">
                {''.join([f'<div class="feature">✅ {feature}</div>' for feature in service_info['features']])}
            </div>
            
            <div class="demo-area">
                <h3>🧙‍♂️ {service_info['name']}과 대화해보세요!</h3>
                <p><strong>안녕하세요!</strong> 저는 {service_info['name']}입니다.</p>
                <p>저는 다음과 같은 일들을 도와드릴 수 있어요:</p>
                <ul>
                    {''.join([f'<li>{feature}</li>' for feature in service_info['features']])}
                </ul>
                <p><em>🎉 베타 테스트 기간 동안 무료로 이용하실 수 있습니다!</em></p>
                <p><strong>실제 서비스에서는 AI 모델과 실시간 대화가 가능합니다.</strong></p>
            </div>
            
            <a href="/" class="back-btn">🔙 도깨비마을장터로 돌아가기</a>
        </body>
    </html>
    """


@app.get("/agents", response_class=HTMLResponse)
async def all_agents():
    """모든 도깨비 에이전트 목록"""
    agents_html = ""
    for service_id, info in virtual_service_manager.service_templates.items():
        agents_html += f"""
        <div style="border: 2px solid #4CAF50; margin: 10px 0; padding: 15px; border-radius: 10px;">
            <h3>{info['name']}</h3>
            <p>특기: {', '.join(info['features'])}</p>
            <a href="/demo/{service_id}?token=beta" 
               style="background: #4CAF50; color: white; padding: 8px 15px; 
                      text-decoration: none; border-radius: 5px;">체험하기</a>
        </div>
        """

    return f"""
    <html>
        <head><title>🏪 도깨비마을장터 - 전체 에이전트</title></head>
        <body style="font-family: Arial; max-width: 1000px; margin: 50px auto; padding: 20px;">
            <h1>🏪 도깨비마을장터 - 15명의 전문 도깨비들</h1>
            <p>각 도깨비를 클릭해서 무료 체험해보세요!</p>
            {agents_html}
            <br><a href="/" style="background: #2196F3; color: white; padding: 10px 20px; 
                         text-decoration: none; border-radius: 5px;">🔙 메인으로</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    print("🏪 도깨비마을장터 BETA 서비스 시작 중...")
    print("🧙‍♂️ 촌장급 도깨비들이 대기 중입니다!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
