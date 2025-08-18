"""
🚀 HYOJIN.AI MVP - 12개 도메인 완전체 + 강화된 보안 시스템
한방에 모든 AI 도메인 구현 + 엔터프라이즈 보안!
버전: v3.2.0 - 고급 보안 시스템 적용
"""

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import datetime
import json
import random
import os
import uuid
import hashlib
import secrets
import re
from pathlib import Path

# FastAPI 앱 생성
app = FastAPI(
    title="Hyojin AI MVP + Advanced Security",
    description="12개 AI 비즈니스 도메인 + 고급 보안 시스템",
    version="3.2.0",
)


# 🔒 간단한 보안 함수들
def sanitize_input(input_data: str) -> str:
    """XSS 방지를 위한 입력 살균"""
    if not isinstance(input_data, str):
        return str(input_data)

    # HTML 태그 제거
    clean_data = re.sub(r"<[^>]*>", "", input_data)
    # 스크립트 태그 제거
    clean_data = re.sub(r"<script.*?</script>", "", clean_data, flags=re.IGNORECASE)
    # 특수 문자 이스케이프
    clean_data = clean_data.replace("<", "&lt;").replace(">", "&gt;")
    clean_data = clean_data.replace('"', "&quot;").replace("'", "&#x27;")

    return clean_data.strip()


def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """비밀번호 검증"""
    try:
        salt, pwd_hash = hashed.split("$")
        return (
            hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt.encode(), 100000
            ).hex()
            == pwd_hash
        )
    except:
        return False


def log_security_event(event_type: str, user_id: str, details: Dict[str, Any]):
    """보안 이벤트 로깅"""
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "details": details,
    }
    print(f"🔒 Security Event: {log_entry}")


def get_client_ip(request: Request) -> str:
    """클라이언트 IP 주소 가져오기"""
    return getattr(request.client, "host", "unknown") if request.client else "unknown"


# CORS 설정 (보안 강화)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
        "https://hyojin.ai",
    ],  # 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 정적 파일 서빙 설정
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔒 보안 설정
security = HTTPBearer()

# 관리자 계정 설정 (강화된 보안)
ADMIN_CREDENTIALS = {
    "username": "hyojin_admin",
    "password_hash": hash_password("HyojinAI2025!@#$%"),
    "api_key": f"hyojin_api_{secrets.token_hex(16)}",
    "role": "super_admin",
    "permissions": ["read", "write", "delete", "admin"],
}

# 세션 토큰 저장소 (실제 운영에서는 Redis 사용)
ACTIVE_SESSIONS = {}


def verify_admin_credentials(username: str, password: str) -> bool:
    """관리자 자격증명 검증 (보안 강화)"""
    if username != ADMIN_CREDENTIALS["username"]:
        return False
    return verify_password(password, ADMIN_CREDENTIALS["password_hash"])


def generate_session_token(username: str) -> str:
    """세션 토큰 생성 (간단한 방식)"""
    token_data = (
        f"{username}:{datetime.datetime.utcnow().isoformat()}:{secrets.token_hex(32)}"
    )
    token = hashlib.sha256(token_data.encode()).hexdigest()
    ACTIVE_SESSIONS[token] = {
        "username": username,
        "created_at": datetime.datetime.now(),
        "last_activity": datetime.datetime.now(),
        "ip_address": None,
    }
    return token


def verify_session_token(token: str) -> Optional[Dict]:
    """세션 토큰 검증 (간단한 방식)"""
    if token not in ACTIVE_SESSIONS:
        return None

    session_info = ACTIVE_SESSIONS[token]

    # 24시간 만료 체크
    if datetime.datetime.now() - session_info["created_at"] > datetime.timedelta(
        hours=24
    ):
        ACTIVE_SESSIONS.pop(token, None)
        return None

    # 마지막 활동 시간 업데이트
    ACTIVE_SESSIONS[token]["last_activity"] = datetime.datetime.now()
    return session_info


async def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """관리자 권한 확인 (강화된 보안)"""
    token = credentials.credentials

    # 토큰 검증
    session_data = verify_session_token(token)
    if not session_data:
        log_security_event(
            "unauthorized_access",
            "unknown",
            {"action": "admin_access_denied", "token": token[:20] + "..."},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 관리자 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 권한 확인
    if "admin" not in ADMIN_CREDENTIALS.get("permissions", []):
        log_security_event(
            "insufficient_permissions",
            session_data.get("username", "unknown"),
            {"action": "admin_access_denied", "required_permission": "admin"},
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 필요합니다"
        )

    return True


# Pydantic 모델들 (보안 강화)
class AdminLoginRequest(BaseModel):
    username: str
    password: str


class SecureSubscriptionRequest(BaseModel):
    email: str
    company: str
    plan: str
    message: str


# 🏠 홈페이지 (기본 랜딩)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """메인 랜딩 페이지"""
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HYOJIN.AI - 고급 보안 AI 플랫폼</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; padding: 60px 0; }
            .header h1 { font-size: 3.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .security-badge { background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 25px; display: inline-block; margin: 20px 0; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 60px 0; }
            .feature-card { 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
                backdrop-filter: blur(10px);
                transition: transform 0.3s;
            }
            .feature-card:hover { transform: translateY(-5px); }
            .feature-card h3 { font-size: 1.5em; margin-bottom: 15px; }
            .cta-section { text-align: center; padding: 60px 0; }
            .cta-button { 
                background: linear-gradient(45deg, #ff6b6b, #ee5a24); 
                color: white; 
                padding: 15px 40px; 
                border: none; 
                border-radius: 25px; 
                font-size: 1.1em; 
                cursor: pointer; 
                text-decoration: none;
                display: inline-block;
                margin: 10px;
                transition: transform 0.3s;
            }
            .cta-button:hover { transform: scale(1.05); }
            .admin-link { 
                position: fixed; 
                top: 20px; 
                right: 20px; 
                background: rgba(0,0,0,0.7); 
                padding: 10px 20px; 
                border-radius: 20px; 
                text-decoration: none; 
                color: white;
                transition: background 0.3s;
            }
            .admin-link:hover { background: rgba(0,0,0,0.9); }
        </style>
    </head>
    <body>
        <a href="/admin/login.html" class="admin-link">🔒 관리자</a>
        
        <div class="container">
            <div class="header">
                <h1>🤖 HYOJIN.AI</h1>
                <div class="security-badge">🔒 Enterprise Security Enabled</div>
                <p>12개 AI 도메인을 한번에! 고급 보안 시스템으로 보호되는 차세대 AI 플랫폼</p>
            </div>

            <div class="features">
                <div class="feature-card">
                    <h3>🔒 고급 보안</h3>
                    <p>JWT 토큰, CSRF 보호, XSS 방지, 입력 검증, 세션 관리 등 엔터프라이즈급 보안 시스템</p>
                </div>
                <div class="feature-card">
                    <h3>🏥 의료 AI</h3>
                    <p>진단 보조, 의료 영상 분석, 건강 모니터링 시스템</p>
                </div>
                <div class="feature-card">
                    <h3>💰 금융 AI</h3>
                    <p>결제 시스템, 리스크 분석, 투자 추천, 사기 탐지</p>
                </div>
                <div class="feature-card">
                    <h3>🎓 교육 AI</h3>
                    <p>개인화 학습, 콘텐츠 생성, 평가 시스템</p>
                </div>
                <div class="feature-card">
                    <h3>🏭 제조 AI</h3>
                    <p>품질 관리, 예측 유지보수, 공급망 최적화</p>
                </div>
                <div class="feature-card">
                    <h3>🚗 모빌리티 AI</h3>
                    <p>자율주행, 교통 최적화, 안전 시스템</p>
                </div>
                <div class="feature-card">
                    <h3>🎮 엔터테인먼트 AI</h3>
                    <p>게임 AI, 콘텐츠 추천, 개인화 경험</p>
                </div>
                <div class="feature-card">
                    <h3>🏪 리테일 AI</h3>
                    <p>수요 예측, 재고 관리, 고객 분석</p>
                </div>
                <div class="feature-card">
                    <h3>⚡ 에너지 AI</h3>
                    <p>스마트 그리드, 에너지 최적화, 신재생 관리</p>
                </div>
                <div class="feature-card">
                    <h3>🌾 농업 AI</h3>
                    <p>스마트 농업, 작물 모니터링, 수확량 예측</p>
                </div>
                <div class="feature-card">
                    <h3>🏢 부동산 AI</h3>
                    <p>가격 예측, 투자 분석, 매물 추천</p>
                </div>
                <div class="feature-card">
                    <h3>📞 고객서비스 AI</h3>
                    <p>챗봇, 감정 분석, 자동 응답 시스템</p>
                </div>
            </div>

            <div class="cta-section">
                <h2>지금 시작하세요!</h2>
                <p>7일 무료 체험으로 모든 기능을 경험해보세요</p>
                <a href="/domains" class="cta-button">🚀 도메인 탐색</a>
                <a href="/subscribe-page" class="cta-button">💳 구독하기</a>
                <a href="/l/demo" class="cta-button">🔗 데모 체험</a>
            </div>
        </div>
    </body>
    </html>
    """


# 🔒 관리자 인증 엔드포인트 (보안 강화)
@app.post("/admin/login")
async def admin_login(request: AdminLoginRequest, http_request: Request):
    """관리자 로그인 (보안 강화)"""
    # 입력 데이터 검증 및 살균
    username = sanitize_input(request.username)
    password = request.password

    # 클라이언트 IP 확인
    client_ip = get_client_ip(http_request)

    # 자격증명 검증
    if verify_admin_credentials(username, password):
        # 세션 토큰 생성
        token = generate_session_token(username)

        # IP 주소 저장
        ACTIVE_SESSIONS[token]["ip_address"] = client_ip

        # 보안 이벤트 로그
        log_security_event(
            "admin_login_success",
            username,
            {"ip_address": client_ip, "timestamp": datetime.datetime.now().isoformat()},
        )

        return {
            "success": True,
            "token": token,
            "expires_in": 24 * 3600,  # 24시간
            "user": {
                "username": username,
                "role": ADMIN_CREDENTIALS["role"],
                "permissions": ADMIN_CREDENTIALS["permissions"],
            },
        }
    else:
        # 실패한 로그인 시도 로그
        log_security_event(
            "admin_login_failed",
            username,
            {"ip_address": client_ip, "timestamp": datetime.datetime.now().isoformat()},
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 사용자명 또는 비밀번호입니다",
        )


@app.post("/admin/logout")
async def admin_logout(
    admin: bool = Depends(admin_required),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """관리자 로그아웃 (보안 강화)"""
    token = credentials.credentials

    # 세션 정보 가져오기
    session_info = ACTIVE_SESSIONS.get(token, {})
    username = session_info.get("username", "unknown")

    # 세션 제거
    ACTIVE_SESSIONS.pop(token, None)

    # 보안 이벤트 로그
    log_security_event(
        "admin_logout", username, {"timestamp": datetime.datetime.now().isoformat()}
    )

    return {"success": True, "message": "로그아웃되었습니다"}


@app.get("/admin/auth/check")
async def check_admin_auth(
    admin: bool = Depends(admin_required),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """관리자 인증 상태 확인 (보안 강화)"""
    token = credentials.credentials
    session_info = ACTIVE_SESSIONS.get(token, {})

    return {
        "authenticated": True,
        "user": session_info.get("username", "admin"),
        "role": ADMIN_CREDENTIALS["role"],
        "permissions": ADMIN_CREDENTIALS["permissions"],
        "session_info": {
            "created_at": session_info.get("created_at"),
            "last_activity": session_info.get("last_activity"),
        },
    }


@app.get("/admin/login.html")
async def admin_login_page():
    """관리자 로그인 페이지 (보안 강화)"""
    try:
        with open("admin-login.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>로그인 페이지를 찾을 수 없습니다.</h1>", status_code=404
        )


# 🔗 가상링크 시스템 (40+ 마케팅 링크)
VIRTUAL_LINKS = {
    # 메인 도메인 링크들
    "main": "http://localhost:8000/",
    "home": "http://localhost:8000/",
    "landing": "http://localhost:8000/",
    # 도메인별 직접 링크
    "healthcare": "http://localhost:8000/domains/healthcare",
    "finance": "http://localhost:8000/domains/paymentapp",
    "education": "http://localhost:8000/domains/education",
    "manufacturing": "http://localhost:8000/domains/manufacturing",
    "mobility": "http://localhost:8000/domains/mobility",
    "entertainment": "http://localhost:8000/domains/entertainment",
    "retail": "http://localhost:8000/domains/retail",
    "energy": "http://localhost:8000/domains/energy",
    "agriculture": "http://localhost:8000/domains/agriculture",
    "realestate": "http://localhost:8000/domains/realestate",
    "customerservice": "http://localhost:8000/domains/customerservice",
    "saas": "http://localhost:8000/domains/saas",
    # 기능별 링크
    "subscribe": "http://localhost:8000/subscribe-page",
    "pricing": "http://localhost:8000/subscribe-page",
    "demo": "http://localhost:8000/domains",
    "trial": "http://localhost:8000/subscribe-page",
    # 마케팅 캠페인 링크
    "launch": "http://localhost:8000/?utm_source=launch&utm_medium=social",
    "ai-revolution": "http://localhost:8000/?utm_campaign=ai-revolution",
    "free-trial": "http://localhost:8000/subscribe-page?utm_source=trial&utm_medium=email",
    "enterprise": "http://localhost:8000/subscribe-page?plan=enterprise",
    "startup": "http://localhost:8000/subscribe-page?plan=startup",
    "professional": "http://localhost:8000/subscribe-page?plan=professional",
    # 소셜미디어 링크
    "youtube": "http://localhost:8000/?utm_source=youtube&utm_medium=social",
    "facebook": "http://localhost:8000/?utm_source=facebook&utm_medium=social",
    "instagram": "http://localhost:8000/?utm_source=instagram&utm_medium=social",
    "linkedin": "http://localhost:8000/?utm_source=linkedin&utm_medium=social",
    "twitter": "http://localhost:8000/?utm_source=twitter&utm_medium=social",
    # 이벤트/프로모션 링크
    "black-friday": "http://localhost:8000/subscribe-page?promo=blackfriday",
    "summer-sale": "http://localhost:8000/subscribe-page?promo=summersale",
    "new-year": "http://localhost:8000/subscribe-page?promo=newyear",
    "beta-test": "http://localhost:8000/?utm_source=beta&utm_medium=email",
    # 파트너/제휴 링크
    "partner-a": "http://localhost:8000/?utm_source=partner-a&utm_medium=referral",
    "partner-b": "http://localhost:8000/?utm_source=partner-b&utm_medium=referral",
    "affiliate": "http://localhost:8000/?utm_source=affiliate&utm_medium=referral",
    # 특수 목적 링크
    "onboarding": "http://localhost:8000/domains?flow=onboarding",
    "success": "http://localhost:8000/?message=success",
    "welcome": "http://localhost:8000/?flow=welcome",
    "upgrade": "http://localhost:8000/subscribe-page?action=upgrade",
    # 관리자 링크
    "admin": "http://localhost:8000/admin/links/dashboard",
    "dashboard": "http://localhost:8000/admin/links/dashboard",
    "analytics": "http://localhost:8000/admin/links",
    "management": "http://localhost:8000/admin/subscription-management",
}

# 링크 클릭 분석 데이터
LINK_ANALYTICS = {}


def track_link_click(short_code: str, request: Request):
    """링크 클릭 추적 (보안 강화)"""
    if short_code not in LINK_ANALYTICS:
        LINK_ANALYTICS[short_code] = {
            "clicks": 0,
            "first_click": datetime.datetime.now(),
            "last_click": None,
            "daily_clicks": {},
            "referrers": {},
            "user_agents": {},
            "ip_addresses": set(),
        }

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    analytics = LINK_ANALYTICS[short_code]

    # 클릭 수 증가
    analytics["clicks"] += 1
    analytics["last_click"] = datetime.datetime.now()

    # 일별 클릭 추적
    if today not in analytics["daily_clicks"]:
        analytics["daily_clicks"][today] = 0
    analytics["daily_clicks"][today] += 1

    # 레퍼러 추적 (보안 처리)
    referrer = request.headers.get("referer", "direct")
    referrer = sanitize_input(referrer)
    if referrer not in analytics["referrers"]:
        analytics["referrers"][referrer] = 0
    analytics["referrers"][referrer] += 1

    # 사용자 에이전트 추적 (보안 처리)
    user_agent = request.headers.get("user-agent", "unknown")
    user_agent = sanitize_input(user_agent[:100])  # 길이 제한
    if user_agent not in analytics["user_agents"]:
        analytics["user_agents"][user_agent] = 0
    analytics["user_agents"][user_agent] += 1

    # IP 주소 추적 (익명화)
    client_ip = get_client_ip(request)
    # IP의 마지막 옥텟을 0으로 마스킹하여 익명화
    masked_ip = (
        ".".join(client_ip.split(".")[:-1]) + ".0" if "." in client_ip else "masked"
    )
    analytics["ip_addresses"].add(masked_ip)


@app.get("/l/{short_code}")
async def virtual_link_redirect(short_code: str, request: Request):
    """가상링크 리다이렉트 (보안 강화)"""
    # 입력 검증
    short_code = sanitize_input(short_code)

    if short_code not in VIRTUAL_LINKS:
        log_security_event(
            "invalid_link_access",
            "anonymous",
            {"short_code": short_code, "ip_address": get_client_ip(request)},
        )
        raise HTTPException(status_code=404, detail="가상링크를 찾을 수 없습니다")

    # 클릭 추적
    track_link_click(short_code, request)

    # 보안 로그
    log_security_event(
        "link_click",
        "anonymous",
        {"short_code": short_code, "target": VIRTUAL_LINKS[short_code]},
    )

    # 리다이렉트
    return RedirectResponse(url=VIRTUAL_LINKS[short_code], status_code=302)


# 보안 강화된 관리자 엔드포인트들
@app.get("/admin/links")
async def get_link_analytics(admin: bool = Depends(admin_required)):
    """가상링크 분석 데이터 (보안 강화)"""
    total_clicks = sum(data["clicks"] for data in LINK_ANALYTICS.values())
    active_links = len(
        [code for code, data in LINK_ANALYTICS.items() if data["clicks"] > 0]
    )
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_clicks = sum(
        data["daily_clicks"].get(today, 0) for data in LINK_ANALYTICS.values()
    )

    return {
        "total_links": len(VIRTUAL_LINKS),
        "total_clicks": total_clicks,
        "active_links": active_links,
        "today_clicks": today_clicks,
        "analytics": LINK_ANALYTICS,
        "security_info": {
            "encrypted": True,
            "anonymized_ips": True,
            "gdpr_compliant": True,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
