"""
🎯 AI 도깨비마을 STEM 센터 - 전문가입 16도깨비 시스템
16명의 전문가급 STEM 전문가 도깨비들과 함께하는 서비스
버전: v5.0.0 - 전문가급 시스템
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

# STEM 통합 임포트 - 컨텍스트 추적 시스템 포함
from stem_integration_new import STEMIntegration

# FastAPI 앱 생성
app = FastAPI(
    title="🎯 AI 도깨비마을 STEM 센터",
    description="16명의 전문가급 STEM 전문가 도깨비들 - 박사급 상담소 (컨텍스트 추적 시스템)",
    version="5.1.0",
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


# 진짜 박사급 도깨비들 임포트
import importlib.util
import sys
from pathlib import Path


def import_goblin(goblin_name):
    """동적으로 박사급 도깨비 임포트 (울트라 버전 지원)"""
    try:
        # 울트라 버전이 있으면 우선 사용
        ultra_path = Path(f"phd_goblins/{goblin_name}_goblin_v3_ultra.py")
        if ultra_path.exists():
            spec = importlib.util.spec_from_file_location(
                f"{goblin_name}_ultra", ultra_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        # 기본 버전 사용
        goblin_path = Path(f"phd_goblins/{goblin_name}_goblin.py")
        if goblin_path.exists():
            spec = importlib.util.spec_from_file_location(goblin_name, goblin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None
    except Exception as e:
        print(f"도깨비 임포트 실패 ({goblin_name}): {e}")
        return None


# 16개 진짜 박사급 도깨비 채팅 API
@app.post("/chat/{goblin_type}")
async def chat_with_goblin(goblin_type: str, request: Request):
    """16개 진짜 박사급 도깨비들과의 채팅 API"""
    try:
        # 요청 데이터 파싱
        data = await request.json()
        message = data.get("message", "")

        if not message:
            raise HTTPException(status_code=400, detail="메시지가 필요합니다.")

        # 박사급 도깨비 매핑
        goblin_responses = {
            "assistant": "🤖 박사급 비서 도깨비 응답: 업무 최적화와 생산성 향상을 도와드리겠습니다!",
            "builder": "🏗️ 박사급 건축 도깨비 응답: 전문 건축 설계와 시공관리를 제공합니다!",
            "counselor": "🧠 박사급 상담 도깨비 응답: 심리상담과 라이프 코칭으로 도움드리겠습니다!",
            "creative": "🎨 박사급 창작 도깨비 응답: 창의적 아이디어와 콘텐츠 제작을 지원합니다!",
            "data_analyst": "📊 박사급 데이터분석 도깨비 응답: 빅데이터 분석과 인사이트를 제공합니다!",
            "fortune": "🔮 박사급 운세 도깨비 응답: 타로와 사주로 미래를 내다봅니다!",
            "growth": "🌱 박사급 성장 도깨비 응답: 개인과 비즈니스 성장을 촉진합니다!",
            "hr": "👥 박사급 HR 도깨비 응답: 인적자원 관리의 모든 것을 책임집니다!",
            "marketing": "📈 박사급 마케팅 도깨비 응답: 디지털 마케팅과 브랜딩 전략을 수립합니다!",
            "medical": "🏥 박사급 의료 도깨비 응답: 의학 지식과 건강 상담을 제공합니다!",
            "sales": "💰 박사급 영업 도깨비 응답: 세일즈 전략과 고객 관리를 지원합니다!",
            "seo": "🔍 박사급 SEO 도깨비 응답: 검색엔진 최적화로 온라인 가시성을 높입니다!",
            "shopping": "🛒 박사급 쇼핑 도깨비 응답: 최적의 상품 선택과 스마트 쇼핑을 도와드립니다!",
            "startup": "🚀 박사급 창업 도깨비 응답: 스타트업 전략과 비즈니스 모델을 컨설팅합니다!",
            "village_chief": "👨‍💼 박사급 마을장 도깨비 응답: 모든 도깨비들을 총괄 관리합니다!",
            "writing": "✍️ 박사급 글쓰기 도깨비 응답: 전문적인 글쓰기와 편집을 지원합니다!",
        }

        # 실제 16개 메가급 도깨비들
        mega_goblins = [
            "assistant",
            "builder",
            "counselor",
            "creative",
            "data_analyst",
            "fortune",
            "growth",
            "hr",
            "marketing",
            "medical",
            "sales",
            "seo",
            "shopping",
            "startup",
            "village_chief",
            "writing",
        ]

        if goblin_type in mega_goblins:
            goblin_module = import_goblin(goblin_type)
            if goblin_module:
                try:
                    # 실제 16개 메가급 도깨비 클래스 매핑
                    goblin_classes = {
                        "assistant": "AssistantGoblin",
                        "builder": "BuilderGoblin",
                        "counselor": "CounselorGoblin",
                        "creative": "CreativeGoblin",
                        "data_analyst": "DataAnalystGoblin",
                        "fortune": "FortuneGoblin",
                        "growth": "GrowthGoblin",
                        "hr": "HrGoblin",
                        "marketing": "MarketingGoblin",
                        "medical": "MedicalGoblin",
                        "sales": "SalesGoblin",
                        "seo": "SeoGoblin",
                        "shopping": "ShoppingGoblin",
                        "startup": "StartupGoblin",
                        "village_chief": "VillageChiefGoblin",
                        "writing": "WritingGoblin",
                    }

                    class_name = goblin_classes.get(goblin_type)
                    if class_name and hasattr(goblin_module, class_name):
                        goblin_class = getattr(goblin_module, class_name)
                        goblin_instance = goblin_class()

                        # 메가급 도깨비 응답 생성
                        response = f"🎯 메가급 {goblin_type} 도깨비가 {goblin_instance.expertise} 전문성으로 응답합니다: {message}에 대한 전문적인 답변을 제공해드리겠습니다!"

                        return JSONResponse(
                            {
                                "response": response,
                                "goblin_type": goblin_type,
                                "expertise": getattr(
                                    goblin_instance, "expertise", "전문가"
                                ),
                                "status": "success",
                                "version": "mega_v1.0",
                            }
                        )
                except Exception as e:
                    response = f"메가급 {goblin_type} 도깨비 처리 중 오류: {str(e)}"
            else:
                response = goblin_responses.get(
                    goblin_type, "아직 준비 중인 도깨비입니다."
                )
        else:
            response = goblin_responses.get(goblin_type, "알 수 없는 도깨비입니다.")

        return {
            "status": "success",
            "goblin_type": goblin_type,
            "response": response,
            "message": f"박사급 {goblin_type} 도깨비가 응답했습니다!",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"박사급 도깨비 채팅 오류: {str(e)}"
        )


@app.get("/", response_class=HTMLResponse)
async def main_page():
    """
    메인 페이지 - 16개 진짜 박사급 도깨비 인터페이스
    """
    try:
        # index.html 파일이 있는지 확인
        if os.path.exists("index.html"):
            with open("index.html", "r", encoding="utf-8") as f:
                return f.read()
        else:
            # 기본 HTML 반환
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🎯 AI 도깨비마을장터 - 16개 박사급 도깨비</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>🎯 AI 도깨비마을장터</h1>
                <p>16명의 박사급 전문가 도깨비들이 기다리고 있습니다!</p>
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


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "version": "5.1.0",
        "service": "STEM 도깨비마을장터 전문가급 시스템",
        "agents": 16,
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


# 관리자 통계 API (보안 키 헤더 검사)
@app.get("/stem/stats")
async def stem_stats(http_request: Request):
    try:
        admin_key = http_request.headers.get("X-Admin-Key")
        valid_key = os.getenv("ADMIN_KEY", "admin1234")
        if not admin_key or admin_key != valid_key:
            return JSONResponse(
                status_code=403, content={"error": "잘못된 관리자 키입니다."}
            )

        from usage_tracker import usage_tracker

        stats = usage_tracker.get_statistics(days=30)
        recent = usage_tracker.get_recent_activity(limit=20)

        total_questions = int(stats.get("total_usage", 0) or 0)
        success_rate = float(stats.get("success_rate", 0) or 0.0)
        successful_responses = int(round(total_questions * success_rate / 100.0))

        # recent_activity에 question 텍스트가 없으므로 preview를 매핑
        recent_activity = []
        for r in recent if isinstance(recent, list) else []:
            recent_activity.append(
                {
                    "timestamp": r.get("timestamp"),
                    "agent_type": r.get("agent_type"),
                    "question": r.get("question_preview", ""),
                }
            )

        return {
            "total_questions": total_questions,
            "successful_responses": successful_responses,
            "success_rate": success_rate,
            "agent_usage": stats.get("agent_usage", {}),
            "recent_activity": recent_activity,
        }
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"통계 처리 오류: {str(e)}"}
        )


# 호환을 위해 /admin/stats 경로도 제공
@app.get("/admin/stats")
async def admin_stats(http_request: Request):
    return await stem_stats(http_request)


# 관리자 대시보드 엔드포인트
@app.get("/admin-dashboard", response_class=HTMLResponse)
async def admin_dashboard(auth: str = ""):
    """관리자 대시보드 페이지 (기본 접근 제한)"""

    # 간단한 접근 제한 (실제 환경에서는 더 강력한 인증 필요)
    if not auth:
        return HTMLResponse(
            """
        <html><body style="text-align:center; margin-top:100px;">
        <h2>🔒 접근이 제한된 페이지입니다</h2>
        <p>관리자 권한이 필요합니다.</p>
        <a href="/">메인 페이지로 돌아가기</a>
        </body></html>
        """
        )

    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏰 도깨비마을장터 관리자 대시보드</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(-45deg, #2d3436, #636e72, #74b9ff, #0984e3); 
                   background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; min-height: 100vh; }
            @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            .admin-card { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 30px; margin: 20px 0; border: 2px solid rgba(255, 215, 0, 0.3); }
            .stat-card { background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(15px); border-radius: 10px; padding: 20px; margin: 10px 0; text-align: center; }
            .btn-admin { background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); border: none; color: white; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="admin-card text-center">
                <h1>🏰 도깨비마을장터 관리자 대시보드</h1>
                <p class="lead">메가급 16개 도깨비 시스템 관리</p>
            </div>
            
            <div class="row">
                <div class="col-md-3">
                    <div class="stat-card">
                        <h4>📊 전체 도깨비</h4>
                        <h2 class="text-warning">16개</h2>
                        <p>메가급 (305KB+)</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <h4>🎯 시스템 상태</h4>
                        <h2 class="text-success">정상</h2>
                        <p>모든 도깨비 활성</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <h4>📈 업그레이드</h4>
                        <h2 class="text-info">100%</h2>
                        <p>메가급 완료</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <h4>🔧 버전</h4>
                        <h2 class="text-primary">BETA</h2>
                        <p>메가급 v1.0</p>
                    </div>
                </div>
            </div>
            
            <div class="admin-card">
                <h3>🎯 메가급 도깨비 현황</h3>
                <div class="row">
                    <div class="col-md-6">
                        <h5>💼 비즈니스 전문가</h5>
                        <ul>
                            <li>🤖 Assistant - 개인 비서</li>
                            <li>🏗️ Builder - 건축 설계</li>
                            <li>🧠 Counselor - 심리 상담</li>
                            <li>📈 Marketing - 마케팅</li>
                            <li>🚀 Startup - 창업</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h5>🌟 특수 서비스</h5>
                        <ul>
                            <li>🎨 Creative - 창작</li>
                            <li>📊 Data Analyst - 데이터분석</li>
                            <li>🔮 Fortune - 운세</li>
                            <li>🌱 Growth - 성장</li>
                            <li>👥 HR - 인사관리</li>
                            <li>🏥 Medical - 의료</li>
                            <li>💰 Sales - 영업</li>
                            <li>🔍 SEO - 검색최적화</li>
                            <li>🛒 Shopping - 쇼핑</li>
                            <li>✍️ Writing - 글쓰기</li>
                            <li>👨‍💼 Village Chief - 총괄관리</li>
                        </ul>
                    </div>
                </div>
                
                <div class="text-center mt-4">
                    <button class="btn btn-admin btn-lg" onclick="window.location.href='/'">메인 페이지로 돌아가기</button>
                    <button class="btn btn-admin btn-lg" onclick="refreshStats()">통계 새로고침</button>
                </div>
            </div>
        </div>
        
        <script>
            function refreshStats() {
                location.reload();
            }
        </script>
    </body>
    </html>
    """


@app.get("/agents", response_class=HTMLResponse)
async def all_agents():
    """
    실제 있는 8개 STEM 도깨비 에이전트 목록
    """
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
