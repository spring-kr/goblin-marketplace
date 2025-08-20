"""
🎯 AI 도깨비마을 STEM 센터 - 전문가급 16도깨비 시스템
16명의 전문가급 STEM 전문가 도깨비들과 함께하는 서비스
버전: v5.0.0 - 전문가급 시스템
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# STEM 통합 임포트
from stem_integration_new import STEMIntegration

# FastAPI 앱 생성
app = FastAPI(
    title="🎯 AI 도깨비마을 STEM 센터",
    description="16명의 전문가급 STEM 전문가 도깨비들 - 박사급 상담소",
    version="5.0.0",
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

# STEM 시스템 초기화
stem_system = STEMIntegration()


# 요청 모델 정의
class STEMRequest(BaseModel):
    agent_type: str
    question: str


# STEM 채팅 API
@app.post("/stem/chat")
async def stem_chat(request: STEMRequest, http_request: Request):
    """STEM 도깨비들과의 채팅 API"""
    try:
        # 클라이언트 IP 가져오기 (안전한 방식)
        client_ip = (
            getattr(http_request.client, "host", "unknown")
            if http_request.client
            else "unknown"
        )

        # STEM 시스템으로 질문 처리
        result = stem_system.process_question(
            agent_type=request.agent_type, question=request.question, user_ip=client_ip
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


# 메인 페이지
@app.get("/", response_class=HTMLResponse)
async def main_page():
    """메인 페이지 - STEM 전용 인터페이스"""
    try:
        # index_stem.html 파일이 있는지 확인
        if os.path.exists("index_stem.html"):
            with open("index_stem.html", "r", encoding="utf-8") as f:
                return f.read()
        else:
            # 기본 HTML 반환
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🎯 AI 도깨비마을 STEM 센터</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>🎯 AI 도깨비마을 STEM 센터</h1>
                <p>16명의 전문가급 STEM 도깨비들이 기다리고 있습니다!</p>
                <p><a href="/stem">STEM 센터 입장하기</a></p>
            </body>
            </html>
            """
    except Exception as e:
        return f"<h1>오류: {str(e)}</h1>"


# STEM 전용 페이지
@app.get("/stem", response_class=HTMLResponse)
async def stem_page():
    """STEM 전용 페이지"""
    try:
        if os.path.exists("index_stem.html"):
            with open("index_stem.html", "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "<h1>STEM 페이지를 찾을 수 없습니다.</h1>"
    except Exception as e:
        return f"<h1>오류: {str(e)}</h1>"


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


# 통계 API
@app.get("/api/stats")
async def get_stats():
    """서비스 이용 통계 조회"""
    try:
        from usage_tracker import usage_tracker

        return usage_tracker.get_statistics()
    except Exception as e:
        return {"error": f"통계 조회 실패: {str(e)}"}


# API 상태 확인
@app.get("/api/health")
async def health_check():
    """API 상태 확인"""
    return {"status": "healthy", "service": "STEM Integration Expert System"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
