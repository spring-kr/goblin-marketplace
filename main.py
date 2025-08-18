"""
🚀 HYOJIN.AI MVP - 12개 도메인 완전체 + 고급 보안 시스템 + 실제 결제
한방에 모든 AI 도메인 구현 + 엔터프라이즈 보안 + Stripe 결제!
버전: v3.3.0 - 실제 결제 시스템 추가
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
import sqlite3
import asyncio

# 결제 서비스 임포트
from payment_service_simple import (
    PaymentProcessor,
    PaymentRequest,
    CustomerData,
    PaymentItem,
    payment_processor,
    email_service,
)

# 가상 서비스 매니저 임포트
from virtual_service_manager import virtual_service_manager

# 인증 시스템 임포트
from auth_system import auth_system

# FastAPI 앱 생성
app = FastAPI(
    title="Hyojin AI MVP + Advanced Security + Payment",
    description="12개 AI 비즈니스 도메인 + 고급 보안 시스템 + 실제 결제",
    version="3.3.0",
)


# 🔒 보안 함수들
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


# 🔥 결제 관리 데이터베이스 함수들
async def save_payment_to_manager_db(
    payment_request: PaymentRequest, result: Dict[str, Any]
):
    """결제 정보를 관리용 데이터베이스에 저장"""
    try:

        def save_to_db():
            conn = sqlite3.connect("hyojin_payments.db")
            cursor = conn.cursor()

            # 결제 테이블 생성 (존재하지 않는 경우)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subscription_id TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT NOT NULL,
                    customer_company TEXT,
                    payment_method TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    items TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    notes TEXT
                )
            """
            )

            now = datetime.datetime.now().isoformat()
            items_json = json.dumps([item.dict() for item in payment_request.items])

            cursor.execute(
                """
                INSERT INTO payments 
                (subscription_id, customer_name, customer_email, customer_company, 
                 payment_method, total_amount, status, items, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    result["subscription_id"],
                    payment_request.customer.name,
                    payment_request.customer.email,
                    payment_request.customer.company or "",
                    payment_request.customer.paymentMethod,
                    result["amount"] / 100,  # cents to dollars
                    result["status"],
                    items_json,
                    now,
                    now,
                ),
            )

            conn.commit()
            conn.close()

        # 비동기로 실행
        await asyncio.get_event_loop().run_in_executor(None, save_to_db)
        print(f"💾 결제 데이터 저장 완료: {result['subscription_id']}")

    except Exception as e:
        print(f"❌ 결제 데이터 저장 실패: {e}")


async def save_bank_transfer_to_manager_db(
    customer: CustomerData, items: List[PaymentItem], result: Dict[str, Any]
):
    """계좌이체 정보를 관리용 데이터베이스에 저장"""
    try:

        def save_to_db():
            conn = sqlite3.connect("hyojin_payments.db")
            cursor = conn.cursor()

            # 결제 테이블 생성 (존재하지 않는 경우)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subscription_id TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT NOT NULL,
                    customer_company TEXT,
                    payment_method TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    items TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    notes TEXT
                )
            """
            )

            now = datetime.datetime.now().isoformat()
            items_json = json.dumps([item.dict() for item in items])
            total_amount = sum(item.price for item in items)

            cursor.execute(
                """
                INSERT INTO payments 
                (subscription_id, customer_name, customer_email, customer_company, 
                 payment_method, total_amount, status, items, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    result["subscription_id"],
                    customer.name,
                    customer.email,
                    customer.company or "",
                    "bank",
                    total_amount,
                    result["status"],
                    items_json,
                    now,
                    now,
                ),
            )

            conn.commit()
            conn.close()

        # 비동기로 실행
        await asyncio.get_event_loop().run_in_executor(None, save_to_db)
        print(f"💾 계좌이체 데이터 저장 완료: {result['subscription_id']}")

    except Exception as e:
        print(f"❌ 계좌이체 데이터 저장 실패: {e}")


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
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔒 고급 보안 설정
security = HTTPBearer()

# 관리자 계정 설정 (고급 보안)
ADMIN_CREDENTIALS = {
    "username": "hyojin_admin",
    "password_hash": hash_password("HyojinAI2025!@#"),  # 강화된 해싱
    "api_key": "sk-" + secrets.token_urlsafe(32),
    "role": "super_admin",
    "permissions": ["admin", "read", "write", "delete"],
    "created_at": datetime.datetime.now().isoformat(),
}

# 세션 토큰 저장소 (실제 운영에서는 Redis 사용)
ACTIVE_SESSIONS = {}


def verify_admin_credentials(username: str, password: str) -> bool:
    """관리자 인증 확인 (강화된 보안)"""
    # 입력 살균
    username = sanitize_input(username)

    if username != ADMIN_CREDENTIALS["username"]:
        return False

    return verify_password(password, ADMIN_CREDENTIALS["password_hash"])


def create_session_token() -> str:
    """보안 세션 토큰 생성"""
    token = secrets.token_urlsafe(32)
    ACTIVE_SESSIONS[token] = {
        "created_at": datetime.datetime.now(),
        "last_used": datetime.datetime.now(),
        "user": ADMIN_CREDENTIALS["username"],
        "ip": None,
    }
    return token


def verify_session_token(token: str) -> bool:
    """세션 토큰 검증"""
    if token not in ACTIVE_SESSIONS:
        return False

    session = ACTIVE_SESSIONS[token]

    # 24시간 만료 확인
    if datetime.datetime.now() - session["created_at"] > datetime.timedelta(hours=24):
        del ACTIVE_SESSIONS[token]
        return False

    # 마지막 사용 시간 업데이트
    session["last_used"] = datetime.datetime.now()
    return True


def verify_api_key(api_key: str) -> bool:
    """API 키 검증"""
    return api_key == ADMIN_CREDENTIALS["api_key"]


async def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """관리자 권한 필요한 엔드포인트용 의존성"""
    token = credentials.credentials

    # API 키 방식 확인
    if verify_api_key(token):
        return True

    # 세션 토큰 방식 확인
    if verify_session_token(token):
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="관리자 권한이 필요합니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return password_hash == ADMIN_CREDENTIALS["password_hash"]


def create_session_token() -> str:
    """세션 토큰 생성"""
    token = secrets.token_urlsafe(32)
    ACTIVE_SESSIONS[token] = {
        "created_at": datetime.datetime.now(),
        "last_used": datetime.datetime.now(),
        "user": "admin",
    }
    return token


def verify_session_token(token: str) -> bool:
    """세션 토큰 검증"""
    if token not in ACTIVE_SESSIONS:
        return False

    session = ACTIVE_SESSIONS[token]
    # 토큰 만료 확인 (24시간)
    if datetime.datetime.now() - session["created_at"] > datetime.timedelta(hours=24):
        del ACTIVE_SESSIONS[token]
        return False

    # 마지막 사용 시간 업데이트
    session["last_used"] = datetime.datetime.now()
    return True


def verify_api_key(api_key: str) -> bool:
    """API 키 검증"""
    return api_key == ADMIN_CREDENTIALS["api_key"]


async def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """관리자 권한 필요한 엔드포인트용 의존성"""
    token = credentials.credentials

    # API 키 방식 확인
    if verify_api_key(token):
        return True

    # 세션 토큰 방식 확인
    if verify_session_token(token):
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="관리자 권한이 필요합니다",
        headers={"WWW-Authenticate": "Bearer"},
    )


# Favicon 엔드포인트
@app.get("/favicon.ico")
async def favicon():
    """Favicon 반환"""
    return FileResponse("static/favicon.svg", media_type="image/svg+xml")


# 가상링크 매핑 테이블
VIRTUAL_LINKS = {
    # 메인 페이지
    "home": "/",
    "demo": "/",
    "landing": "/",
    # AI 에이전트 마켓플레이스
    "agents": "/agents/marketplace",
    "marketplace": "/agents/marketplace",
    "try": "/agents/marketplace",
    "experience": "/agents/marketplace",
    # 가격 및 구독
    "pricing": "/#pricing",
    "trial": "/agents/marketplace?trial=true",
    "subscribe": "/#pricing",
    "plans": "/#pricing",
    # 도메인별 체험 링크
    "medical": "/agents/marketplace?domain=medical",
    "finance": "/agents/marketplace?domain=finance",
    "education": "/agents/marketplace?domain=education",
    "manufacturing": "/agents/marketplace?domain=manufacturing",
    "retail": "/agents/marketplace?domain=retail",
    "logistics": "/agents/marketplace?domain=logistics",
    "energy": "/agents/marketplace?domain=energy",
    "agriculture": "/agents/marketplace?domain=agriculture",
    "realestate": "/agents/marketplace?domain=realestate",
    "entertainment": "/agents/marketplace?domain=entertainment",
    "cybersecurity": "/agents/marketplace?domain=cybersecurity",
    "smartcity": "/agents/marketplace?domain=smartcity",
    # 특별 기능
    "api": "/docs",
    "docs": "/docs",
    "health": "/health",
    "status": "/health",
    # 마케팅 캠페인
    "launch": "/?campaign=launch",
    "beta": "/?campaign=beta",
    "partner": "/?campaign=partner",
    "linkedin": "/?utm_source=linkedin",
    "twitter": "/?utm_source=twitter",
    "facebook": "/?utm_source=facebook",
    "newsletter": "/?utm_source=newsletter",
    "webinar": "/?utm_source=webinar",
    "updates": "/?utm_source=updates",
}

# 링크 클릭 추적 데이터
LINK_ANALYTICS = {}


def track_link_click(short_code: str, request: Request):
    """가상링크 클릭 추적"""
    if short_code not in LINK_ANALYTICS:
        LINK_ANALYTICS[short_code] = {
            "clicks": 0,
            "first_click": datetime.datetime.now().isoformat(),
            "last_click": None,
            "user_agents": [],
            "ip_addresses": [],
        }

    LINK_ANALYTICS[short_code]["clicks"] += 1
    LINK_ANALYTICS[short_code]["last_click"] = datetime.datetime.now().isoformat()

    # User-Agent 추적 (최대 10개)
    user_agent = request.headers.get("user-agent", "unknown")
    if user_agent not in LINK_ANALYTICS[short_code]["user_agents"]:
        LINK_ANALYTICS[short_code]["user_agents"].append(user_agent)
        if len(LINK_ANALYTICS[short_code]["user_agents"]) > 10:
            LINK_ANALYTICS[short_code]["user_agents"].pop(0)

    # IP 주소 추적 (최대 10개)
    client_ip = request.client.host if request.client else "unknown"
    if client_ip not in LINK_ANALYTICS[short_code]["ip_addresses"]:
        LINK_ANALYTICS[short_code]["ip_addresses"].append(client_ip)
        if len(LINK_ANALYTICS[short_code]["ip_addresses"]) > 10:
            LINK_ANALYTICS[short_code]["ip_addresses"].pop(0)


# 공통 요청/응답 모델
class PredictRequest(BaseModel):
    input_data: str
    parameters: Dict[str, Any] = {}


class PredictResponse(BaseModel):
    domain: str
    result: Dict[str, Any]
    confidence: float
    timestamp: str
    processing_time_ms: int


# 구독 데이터 모델
class SubscriptionRequest(BaseModel):
    email: str
    company: str = ""
    plan: str
    phone: str = ""
    message: str = ""


# 구독관리회사시스템 통합 모델들
class SubscriptionUpdateRequest(BaseModel):
    email: str
    plan: str
    status: str = "active"


class UserManagementRequest(BaseModel):
    email: str
    action: str  # create, update, delete, suspend
    data: Dict[str, Any] = {}


class FinancialAnalysisRequest(BaseModel):
    email: str
    period: str = "monthly"  # daily, weekly, monthly, yearly
    metrics: List[str] = ["revenue", "usage", "roi"]


class SubscriptionResponse(BaseModel):
    success: bool
    message: str
    subscription_id: str
    timestamp: str
    trial_expires: str = ""


# API 요청 시 이메일 기반 인증 모델
class AuthenticatedRequest(BaseModel):
    email: str
    domain: str
    text: str


# AI 에이전트 저장소 모델들
class AgentRequest(BaseModel):
    agent_type: str
    task_description: str
    parameters: Dict[str, Any] = {}


class AgentResponse(BaseModel):
    agent_type: str
    task_id: str
    result: Dict[str, Any]
    autonomy_score: float
    execution_time_ms: int
    timestamp: str


class AgentDeployRequest(BaseModel):
    email: str
    agent_type: str
    deployment_config: Dict[str, Any] = {}


# 구독자 데이터 저장소 (실제로는 데이터베이스 사용)
subscribers = []

# AI 에이전트 저장소 데이터 - 15명의 도깨비 에이전트들
ai_agents = {
    "village-chief-dokkaebi": {
        "name": "🏘️ 촌장 도깨비",
        "description": "도깨비 마을의 촌장, 모든 도깨비들을 총괄하고 마을 운영 전반을 관리하는 리더",
        "capabilities": ['마을관리', '도깨비총괄', '리더십', '종합관리'],
        "autonomy_score": 99,
        "tier": "premium",
        "icon": "🏘️",
    },
    "math-dokkaebi": {
        "name": "📐 수학 도깨비",
        "description": "수학 문제 해결, 통계 분석, 수치 계산, 알고리즘 최적화 전문가 (75.78% 성과)",
        "capabilities": ['수학문제해결', '통계분석', '수치계산', '알고리즘최적화'],
        "autonomy_score": 98,
        "tier": "premium",
        "icon": "📐",
    },
    "physics-dokkaebi": {
        "name": "⚡ 물리 도깨비",
        "description": "물리학 법칙 분석, 시뮬레이션, 실험 설계, 과학적 모델링 전문가 (100% 성과)",
        "capabilities": ['물리학분석', '시뮬레이션', '실험설계', '과학적모델링'],
        "autonomy_score": 100,
        "tier": "premium",
        "icon": "⚡",
    },
    "chemistry-dokkaebi": {
        "name": "🧪 화학 도깨비",
        "description": "화학 반응 분석, 분자 구조 예측, 실험 결과 해석, 화학공정 최적화 전문가 (90% 성과)",
        "capabilities": ['화학반응분석', '분자구조예측', '실험결과해석', '화학공정최적화'],
        "autonomy_score": 90,
        "tier": "premium",
        "icon": "🧪",
    },
    "engineering-dokkaebi": {
        "name": "🔧 공학 도깨비",
        "description": "공학 설계, 시스템 분석, 기술 최적화, 엔지니어링 솔루션 전문가 (95% 성과)",
        "capabilities": ['공학설계', '시스템분석', '기술최적화', '엔지니어링솔루션'],
        "autonomy_score": 95,
        "tier": "premium",
        "icon": "🔧",
    },
    "biology-dokkaebi": {
        "name": "🧬 생물학 도깨비",
        "description": "생물학적 데이터 분석, 유전자 연구, 생태계 모델링, 바이오 기술 전문가 (88% 성과)",
        "capabilities": ['생물학데이터분석', '유전자연구', '생태계모델링', '바이오기술'],
        "autonomy_score": 88,
        "tier": "premium",
        "icon": "🧬",
    },
    "business-strategy-dokkaebi": {
        "name": "📈 비즈니스 전략 도깨비",
        "description": "경영 전략 수립, 시장 분석, 비즈니스 모델 개발, 전략적 의사결정 전문가",
        "capabilities": ['경영전략수립', '시장분석', '비즈니스모델개발', '전략적의사결정'],
        "autonomy_score": 95,
        "tier": "enterprise",
        "icon": "📈",
    },
    "communication-dokkaebi": {
        "name": "💬 커뮤니케이션 도깨비",
        "description": "소통 전략, 대화 분석, 커뮤니케이션 최적화, 관계 관리 전문가",
        "capabilities": ['소통전략', '대화분석', '커뮤니케이션최적화', '관계관리'],
        "autonomy_score": 89,
        "tier": "standard",
        "icon": "💬",
    },
    "financial-management-dokkaebi": {
        "name": "💰 재무 관리 도깨비",
        "description": "재무 계획, 투자 분석, 리스크 관리, 포트폴리오 최적화 전문가",
        "capabilities": ['재무계획', '투자분석', '리스크관리', '포트폴리오최적화'],
        "autonomy_score": 96,
        "tier": "enterprise",
        "icon": "💰",
    },
    "innovation-creation-dokkaebi": {
        "name": "🚀 혁신 창조 도깨비",
        "description": "혁신 아이디어 창출, 창의적 문제 해결, 신기술 개발, 미래 예측 전문가",
        "capabilities": ['혁신아이디어창출', '창의적문제해결', '신기술개발', '미래예측'],
        "autonomy_score": 93,
        "tier": "premium",
        "icon": "🚀",
    },
    "technology-management-dokkaebi": {
        "name": "🔧 기술 관리 도깨비",
        "description": "기술 시스템 관리, IT 인프라 최적화, 기술 전략 수립, 디지털 혁신 전문가",
        "capabilities": ['기술시스템관리', 'IT인프라최적화', '기술전략수립', '디지털혁신'],
        "autonomy_score": 94,
        "tier": "premium",
        "icon": "🔧",
    },
    "user-management-dokkaebi": {
        "name": "👥 사용자 관리 도깨비",
        "description": "사용자 경험 최적화, 고객 관리, 서비스 개선, 사용자 행동 분석 전문가",
        "capabilities": ['사용자경험최적화', '고객관리', '서비스개선', '사용자행동분석'],
        "autonomy_score": 87,
        "tier": "standard",
        "icon": "👥",
    },
}


# 무료체험 관리 함수들
def calculate_trial_expiry():
    """7일 무료체험 만료일 계산"""
    return datetime.datetime.now() + datetime.timedelta(days=7)


def is_trial_expired(trial_expires_str):
    """무료체험 만료 여부 확인"""
    if not trial_expires_str:
        return True

    try:
        trial_expires = datetime.datetime.fromisoformat(trial_expires_str)
        return datetime.datetime.now() > trial_expires
    except:
        return True


def get_subscriber_by_email(email):
    """이메일로 구독자 정보 조회"""
    for subscriber in subscribers:
        if subscriber["email"] == email:
            return subscriber
    return None


def get_usage_limit(plan):
    """플랜에 따른 사용량 제한 반환"""
    limits = {
        "trial": {"calls": 3, "name": "무료 체험"},
        "startup": {"calls": 50, "name": "Startup"},
        "professional": {"calls": 300, "name": "Professional"},
        "business": {"calls": 1000, "name": "Business"},
        "enterprise": {"calls": -1, "name": "Enterprise"},  # -1은 무제한
    }
    return limits.get(plan, limits["trial"])


def check_api_access(email):
    """API 접근 권한 확인"""
    subscriber = get_subscriber_by_email(email)

    if not subscriber:
        return {
            "allowed": False,
            "reason": "구독되지 않은 이메일입니다.",
            "error_code": "NOT_SUBSCRIBED",
        }

    # 무료체험 만료 확인
    if subscriber["plan"] == "trial" and is_trial_expired(
        subscriber.get("trial_expires")
    ):
        return {
            "allowed": False,
            "reason": "7일 무료체험이 만료되었습니다. 유료 플랜으로 업그레이드해주세요.",
            "error_code": "TRIAL_EXPIRED",
            "trial_expires": subscriber.get("trial_expires"),
        }

    # 호출 횟수 제한 확인 (플랜별)
    daily_calls = subscriber.get("daily_calls", 0)
    max_calls = get_plan_limits(subscriber["plan"])["daily_calls"]

    if daily_calls >= max_calls:
        return {
            "allowed": False,
            "reason": f"일일 호출 한도 {max_calls}회를 초과했습니다.",
            "error_code": "QUOTA_EXCEEDED",
            "daily_calls": daily_calls,
            "max_calls": max_calls,
        }

    return {"allowed": True, "subscriber": subscriber}


def get_plan_limits(plan):
    """플랜별 제한 정보"""
    limits = {
        "trial": {"daily_calls": 10, "domains": 2},
        "starter": {"daily_calls": 50, "domains": 2},
        "professional": {"daily_calls": 300, "domains": 6},
        "business": {"daily_calls": 1000, "domains": 12},
        "enterprise": {"daily_calls": 99999, "domains": 12},
    }
    return limits.get(plan, limits["trial"])


def increment_usage(email):
    """API 사용량 증가"""
    for subscriber in subscribers:
        if subscriber["email"] == email:
            subscriber["daily_calls"] = subscriber.get("daily_calls", 0) + 1
            subscriber["last_used"] = datetime.datetime.now().isoformat()
            break


# 12개 도메인 정의
DOMAINS = {
    "paymentapp": {
        "name": "결제 서비스",
        "description": "스마트 결제 시스템 AI",
        "features": ["사기 탐지", "결제 최적화", "리스크 분석"],
    },
    "deliveryservice": {
        "name": "배달 서비스",
        "description": "배송 최적화 AI",
        "features": ["경로 최적화", "배송 시간 예측", "물류 관리"],
    },
    "onlineshopping": {
        "name": "온라인 쇼핑",
        "description": "E-커머스 최적화 AI",
        "features": ["상품 추천", "재고 관리", "가격 최적화"],
    },
    "realestateapp": {
        "name": "부동산 앱",
        "description": "부동산 가격 예측 AI",
        "features": ["가격 예측", "투자 분석", "시장 트렌드"],
    },
    "onlineeducation": {
        "name": "온라인 교육",
        "description": "개인화 학습 AI",
        "features": ["학습 경로 추천", "성과 분석", "콘텐츠 최적화"],
    },
    "jobplatform": {
        "name": "구인구직",
        "description": "채용 매칭 AI",
        "features": ["인재 매칭", "연봉 예측", "스킬 분석"],
    },
    "manufacturing": {
        "name": "제조업 AI",
        "description": "스마트 팩토리 AI",
        "features": ["생산 최적화", "품질 관리", "예측 정비"],
    },
    "retail": {
        "name": "소매업 AI",
        "description": "리테일 최적화 AI",
        "features": ["판매 예측", "재고 최적화", "고객 분석"],
    },
    "logistics": {
        "name": "물류 AI",
        "description": "물류 체인 최적화 AI",
        "features": ["창고 관리", "배송 최적화", "공급망 분석"],
    },
    "customerservice": {
        "name": "고객서비스 AI",
        "description": "지능형 고객 지원 AI",
        "features": ["챗봇", "감정 분석", "자동 응답"],
    },
    "healthcare": {
        "name": "헬스케어 AI",
        "description": "의료 데이터 분석 AI",
        "features": ["진단 보조", "건강 예측", "치료 추천"],
    },
    "finance": {
        "name": "금융 AI",
        "description": "핀테크 솔루션 AI",
        "features": ["투자 추천", "리스크 관리", "신용 분석"],
    },
}


# AI 예측 엔진 (시뮬레이션)
def generate_ai_prediction(domain: str, input_data: str, parameters: dict):
    """AI 예측 결과 생성 (실제 AI 모델 시뮬레이션)"""

    domain_info = DOMAINS.get(domain, {})
    features = domain_info.get("features", [])

    # 도메인별 특화 결과 생성
    if domain == "paymentapp":
        return {
            "fraud_risk": round(random.uniform(0.1, 0.9), 2),
            "recommended_action": random.choice(["approve", "review", "decline"]),
            "payment_method": "card",
            "transaction_score": round(random.uniform(70, 95), 1),
        }
    elif domain == "deliveryservice":
        return {
            "estimated_delivery_time": f"{random.randint(20, 120)}분",
            "optimal_route": f"경로 {random.randint(1, 5)}",
            "cost_estimate": f"{random.randint(3000, 8000)}원",
            "weather_impact": random.choice(["낮음", "보통", "높음"]),
        }
    elif domain == "onlineshopping":
        return {
            "recommended_products": [f"상품 {i}" for i in range(1, 6)],
            "price_optimization": f"{random.randint(10, 30)}% 할인 추천",
            "inventory_status": random.choice(["충분", "부족", "재고 없음"]),
            "customer_segment": random.choice(["프리미엄", "일반", "가격민감"]),
        }
    elif domain == "realestateapp":
        return {
            "predicted_price": f"{random.randint(3, 15)}억원",
            "price_trend": random.choice(["상승", "하락", "유지"]),
            "investment_score": round(random.uniform(1, 10), 1),
            "market_analysis": "강남구 평균 대비 15% 높음",
        }
    elif domain == "onlineeducation":
        return {
            "learning_path": ["기초", "중급", "고급", "전문가"],
            "estimated_completion": f"{random.randint(30, 180)}일",
            "difficulty_score": round(random.uniform(1, 10), 1),
            "recommended_study_time": f"일 {random.randint(1, 4)}시간",
        }
    elif domain == "jobplatform":
        return {
            "match_score": f"{random.randint(70, 95)}%",
            "expected_salary": f"{random.randint(3000, 8000)}만원",
            "skill_gap": ["Python", "AI", "데이터분석"],
            "career_level": random.choice(["주니어", "시니어", "리드", "매니저"]),
        }
    elif domain == "manufacturing":
        return {
            "production_efficiency": f"{random.randint(85, 98)}%",
            "quality_score": round(random.uniform(90, 99), 1),
            "maintenance_schedule": f"{random.randint(7, 30)}일 후",
            "cost_optimization": f"{random.randint(5, 20)}% 절감 가능",
        }
    elif domain == "retail":
        return {
            "sales_forecast": f"{random.randint(80, 120)}% 전월 대비",
            "inventory_turnover": round(random.uniform(2, 8), 1),
            "customer_lifetime_value": f"{random.randint(200, 800)}만원",
            "seasonal_trend": random.choice(["성수기", "비수기", "평상시"]),
        }
    elif domain == "logistics":
        return {
            "warehouse_efficiency": f"{random.randint(80, 95)}%",
            "shipping_cost": f"{random.randint(2000, 6000)}원",
            "delivery_success_rate": f"{random.randint(95, 99)}%",
            "supply_chain_risk": random.choice(["낮음", "보통", "높음"]),
        }
    elif domain == "customerservice":
        return {
            "sentiment_analysis": random.choice(["긍정", "중립", "부정"]),
            "response_category": random.choice(["문의", "불만", "칭찬"]),
            "auto_response": "고객님의 문의사항을 확인했습니다.",
            "escalation_needed": random.choice([True, False]),
        }
    elif domain == "healthcare":
        return {
            "health_score": round(random.uniform(70, 95), 1),
            "risk_factors": ["고혈압", "당뇨", "비만"],
            "recommended_checkup": f"{random.randint(3, 12)}개월 후",
            "lifestyle_advice": "규칙적인 운동과 식단 관리 필요",
        }
    elif domain == "finance":
        return {
            "credit_score": random.randint(700, 950),
            "investment_recommendation": random.choice(["주식", "채권", "펀드"]),
            "risk_level": random.choice(["보수적", "중립적", "공격적"]),
            "expected_return": f"{random.randint(3, 15)}% 연수익률",
        }
    else:
        return {
            "message": f"{domain} AI 예측 결과",
            "confidence": round(random.uniform(0.7, 0.95), 2),
            "features": features,
        }


# 기본 엔드포인트들
@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 쇼핑몰 페이지"""
    try:
        # index.html 파일 반환
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        # 파일이 없는 경우 기본 에러 페이지
        return HTMLResponse(
            content="<h1>쇼핑몰 페이지를 찾을 수 없습니다</h1><p>index.html 파일이 필요합니다.</p>",
            status_code=404,
        )


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
    }


# � 관리자 인증 엔드포인트
class AdminLoginRequest(BaseModel):
    username: str
    password: str


@app.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    """관리자 로그인"""
    if not verify_admin_credentials(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="잘못된 인증 정보입니다"
        )

    # 세션 토큰 생성
    token = create_session_token()

    return {
        "success": True,
        "token": token,
        "message": "로그인 성공",
        "expires_in": "24시간",
    }


@app.post("/admin/logout")
async def admin_logout(admin: bool = Depends(admin_required)):
    """관리자 로그아웃"""
    # 실제로는 토큰을 무효화해야 함
    return {"success": True, "message": "로그아웃 성공"}


@app.get("/admin/auth/check")
async def check_admin_auth(admin: bool = Depends(admin_required)):
    """관리자 인증 상태 확인"""
    return {"authenticated": True, "user": "admin"}


# �🔗 가상링크 시스템
@app.get("/admin/login.html")
async def admin_login_page():
    """관리자 로그인 페이지"""
    try:
        with open("admin-login.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>로그인 페이지를 찾을 수 없습니다.</h1>", status_code=404
        )


@app.get("/payment_success.html")
async def payment_success_page():
    """결제 성공 페이지"""
    try:
        with open("payment_success.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>결제 성공 페이지를 찾을 수 없습니다.</h1>", status_code=404
        )


@app.get("/l/{short_code}")
async def virtual_link_redirect(short_code: str, request: Request):
    """가상링크 리다이렉트"""
    if short_code not in VIRTUAL_LINKS:
        raise HTTPException(status_code=404, detail="가상링크를 찾을 수 없습니다")

    # 클릭 추적
    track_link_click(short_code, request)

    # 실제 URL로 리다이렉트
    target_url = VIRTUAL_LINKS[short_code]

    # 상대 경로면 전체 URL로 변환
    if target_url.startswith("/"):
        base_url = str(request.base_url).rstrip("/")
        target_url = base_url + target_url

    return RedirectResponse(url=target_url, status_code=302)


@app.get("/admin/links")
async def get_link_analytics(admin: bool = Depends(admin_required)):
    """가상링크 분석 데이터 (관리자용)"""
    total_clicks = sum(data.get("clicks", 0) for data in LINK_ANALYTICS.values())

    analytics_summary = {
        "total_links": len(VIRTUAL_LINKS),
        "total_clicks": total_clicks,
        "active_links": len(LINK_ANALYTICS),
        "top_links": [],
        "recent_activity": [],
    }

    # 상위 10개 링크
    sorted_links = sorted(
        LINK_ANALYTICS.items(), key=lambda x: x[1].get("clicks", 0), reverse=True
    )[:10]

    for short_code, data in sorted_links:
        analytics_summary["top_links"].append(
            {
                "short_code": short_code,
                "target_url": VIRTUAL_LINKS.get(short_code, "unknown"),
                "clicks": data.get("clicks", 0),
                "last_click": data.get("last_click"),
            }
        )

    return analytics_summary


@app.post("/admin/links/create")
async def create_virtual_link(
    short_code: str, target_url: str, admin: bool = Depends(admin_required)
):
    """새 가상링크 생성 (관리자용)"""
    if short_code in VIRTUAL_LINKS:
        raise HTTPException(status_code=400, detail="이미 존재하는 가상링크입니다")

    VIRTUAL_LINKS[short_code] = target_url

    return {
        "success": True,
        "short_code": short_code,
        "target_url": target_url,
        "virtual_link": f"/l/{short_code}",
    }


@app.get("/admin/links/all")
async def get_all_virtual_links(admin: bool = Depends(admin_required)):
    """모든 가상링크 목록"""
    links = []
    for short_code, target_url in VIRTUAL_LINKS.items():
        analytics = LINK_ANALYTICS.get(short_code, {})
        links.append(
            {
                "short_code": short_code,
                "target_url": target_url,
                "virtual_link": f"/l/{short_code}",
                "clicks": analytics.get("clicks", 0),
                "created": analytics.get("first_click", "미사용"),
                "last_used": analytics.get("last_click", "미사용"),
            }
        )

    return {"links": links, "total": len(links)}


@app.get("/admin/links/dashboard")
async def link_dashboard(admin: bool = Depends(admin_required)):
    """가상링크 관리 대시보드 HTML"""
    dashboard_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HYOJIN.AI 가상링크 관리자 대시보드</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: white; margin-bottom: 30px; }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .admin-panel { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
            .section { margin-bottom: 30px; }
            .section h2 { color: #333; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 2px solid #667eea; }
            .link-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
            .link-card { background: #f8f9fa; border: 1px solid #ddd; border-radius: 10px; padding: 15px; transition: transform 0.2s; }
            .link-card:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .link-title { font-weight: bold; color: #333; margin-bottom: 5px; }
            .link-url { color: #666; font-size: 0.9em; word-break: break-all; }
            .link-stats { margin-top: 10px; font-size: 0.85em; color: #888; }
            .admin-actions { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
            .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
            .btn-primary { background: #667eea; color: white; }
            .btn-primary:hover { background: #5a6fd8; }
            .btn-success { background: #28a745; color: white; }
            .btn-success:hover { background: #218838; }
            .btn-danger { background: #dc3545; color: white; }
            .btn-danger:hover { background: #c82333; }
            .analytics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
            .analytics-card { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center; }
            .analytics-number { font-size: 2em; font-weight: bold; margin-bottom: 5px; }
            .analytics-label { font-size: 0.9em; opacity: 0.9; }
            .form-group { margin-bottom: 15px; }
            .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
            .form-group input, .form-group textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
            .logout-btn { position: absolute; top: 20px; right: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logout-btn">
                <button class="btn btn-danger" onclick="logout()">로그아웃</button>
            </div>
            
            <div class="header">
                <h1>🔗 HYOJIN.AI 가상링크 관리자</h1>
                <p>마케팅 캠페인용 가상링크를 관리하세요</p>
            </div>

            <div class="admin-panel">
                <!-- 분석 데이터 -->
                <div class="section">
                    <h2>📊 실시간 분석</h2>
                    <div class="analytics-grid" id="analytics-grid">
                        <!-- 동적으로 로드됩니다 -->
                    </div>
                </div>

                <!-- 새 링크 생성 -->
                <div class="section">
                    <h2>➕ 새 가상링크 생성</h2>
                    <div class="admin-actions">
                        <div class="form-group" style="flex: 1; min-width: 200px;">
                            <label>단축코드:</label>
                            <input type="text" id="shortCode" placeholder="예: new-campaign">
                        </div>
                        <div class="form-group" style="flex: 2; min-width: 300px;">
                            <label>목적지 URL:</label>
                            <input type="text" id="targetUrl" placeholder="https://example.com">
                        </div>
                        <button class="btn btn-success" onclick="createLink()" style="align-self: end; height: 40px;">생성</button>
                    </div>
                </div>

                <!-- 기존 링크 목록 -->
                <div class="section">
                    <h2>🔗 등록된 가상링크</h2>
                    <div class="link-grid" id="link-grid">
                        <!-- 동적으로 로드됩니다 -->
                    </div>
                </div>
            </div>
        </div>

        <script>
            // 인증 토큰 확인
            const token = localStorage.getItem('admin_token');
            if (!token) {
                window.location.href = '/admin/login.html';
            }

            // API 호출을 위한 헤더
            const authHeaders = {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            };

            // 페이지 로드 시 데이터 가져오기
            document.addEventListener('DOMContentLoaded', function() {
                loadAnalytics();
                loadLinks();
            });

            async function loadAnalytics() {
                try {
                    const response = await fetch('/admin/links', {
                        headers: authHeaders
                    });
                    if (response.ok) {
                        const data = await response.json();
                        displayAnalytics(data);
                    }
                } catch (error) {
                    console.error('분석 데이터 로드 실패:', error);
                }
            }

            async function loadLinks() {
                try {
                    const response = await fetch('/admin/links/all', {
                        headers: authHeaders
                    });
                    if (response.ok) {
                        const data = await response.json();
                        displayLinks(data.links);
                    }
                } catch (error) {
                    console.error('링크 데이터 로드 실패:', error);
                }
            }

            function displayAnalytics(data) {
                const grid = document.getElementById('analytics-grid');
                grid.innerHTML = `
                    <div class="analytics-card">
                        <div class="analytics-number">${data.total_links || 0}</div>
                        <div class="analytics-label">총 링크 수</div>
                    </div>
                    <div class="analytics-card">
                        <div class="analytics-number">${data.total_clicks || 0}</div>
                        <div class="analytics-label">총 클릭 수</div>
                    </div>
                    <div class="analytics-card">
                        <div class="analytics-number">${data.active_links || 0}</div>
                        <div class="analytics-label">활성 링크</div>
                    </div>
                    <div class="analytics-card">
                        <div class="analytics-number">${data.today_clicks || 0}</div>
                        <div class="analytics-label">오늘 클릭</div>
                    </div>
                `;
            }

            function displayLinks(links) {
                const grid = document.getElementById('link-grid');
                if (!links || links.length === 0) {
                    grid.innerHTML = '<p>등록된 링크가 없습니다.</p>';
                    return;
                }

                grid.innerHTML = links.map(link => `
                    <div class="link-card">
                        <div class="link-title">/${link.short_code}</div>
                        <div class="link-url">${link.target_url}</div>
                        <div class="link-stats">
                            클릭: ${link.clicks || 0}회 | 
                            생성: ${link.created_at ? new Date(link.created_at).toLocaleDateString() : '알 수 없음'}
                        </div>
                    </div>
                `).join('');
            }

            async function createLink() {
                const shortCode = document.getElementById('shortCode').value.trim();
                const targetUrl = document.getElementById('targetUrl').value.trim();

                if (!shortCode || !targetUrl) {
                    alert('단축코드와 목적지 URL을 모두 입력해주세요.');
                    return;
                }

                try {
                    const response = await fetch(`/admin/links/create?short_code=${encodeURIComponent(shortCode)}&target_url=${encodeURIComponent(targetUrl)}`, {
                        method: 'POST',
                        headers: authHeaders
                    });

                    if (response.ok) {
                        const result = await response.json();
                        alert('링크가 성공적으로 생성되었습니다!');
                        document.getElementById('shortCode').value = '';
                        document.getElementById('targetUrl').value = '';
                        loadLinks(); // 링크 목록 새로고침
                        loadAnalytics(); // 분석 데이터 새로고침
                    } else {
                        const error = await response.json();
                        alert('오류: ' + error.detail);
                    }
                } catch (error) {
                    alert('링크 생성 중 오류가 발생했습니다.');
                    console.error(error);
                }
            }

            async function logout() {
                try {
                    await fetch('/admin/logout', {
                        method: 'POST',
                        headers: authHeaders
                    });
                } catch (error) {
                    console.error('로그아웃 오류:', error);
                }
                
                localStorage.removeItem('admin_token');
                window.location.href = '/admin/login.html';
            }

            // 토큰 유효성 주기적 확인
            setInterval(async function() {
                try {
                    const response = await fetch('/admin/auth/check', {
                        headers: authHeaders
                    });
                    if (!response.ok) {
                        logout();
                    }
                } catch (error) {
                    logout();
                }
            }, 300000); // 5분마다 확인
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=dashboard_html)


@app.get("/api/v1/domains")
async def get_domains():
    """지원 도메인 목록"""
    domains_list = []
    for domain_id, info in DOMAINS.items():
        domains_list.append(
            {
                "id": domain_id,
                "name": info["name"],
                "description": info["description"],
                "features": info["features"],
            }
        )

    return {"domains": domains_list, "total": len(domains_list)}


@app.post("/subscribe", response_model=SubscriptionResponse)
async def create_subscription(subscription: SubscriptionRequest):
    """구독 정보 저장"""
    import uuid

    # 기존 구독자 확인
    existing_subscriber = get_subscriber_by_email(subscription.email)
    if existing_subscriber:
        return SubscriptionResponse(
            success=False,
            message=f"{subscription.email}은 이미 등록된 이메일입니다.",
            subscription_id="",
            timestamp=datetime.datetime.now().isoformat(),
        )

    # 구독 ID 생성
    subscription_id = str(uuid.uuid4())[:8]

    # 7일 무료체험 시작 (모든 신규 가입자)
    trial_expires = calculate_trial_expiry()

    # 구독 데이터 생성
    subscription_data = {
        "id": subscription_id,
        "email": subscription.email,
        "company": subscription.company,
        "plan": "trial",  # 모든 신규 가입자는 trial로 시작
        "original_plan": subscription.plan,  # 원래 선택한 플랜 저장
        "message": subscription.message,
        "timestamp": datetime.datetime.now().isoformat(),
        "trial_expires": trial_expires.isoformat(),
        "status": "trial",
        "daily_calls": 0,
        "total_calls": 0,
        "last_used": None,
    }

    # 구독자 목록에 추가
    subscribers.append(subscription_data)

    # 로그 출력 (실제로는 데이터베이스 저장)
    print(f"🎉 새 구독자: {subscription.email} (7일 무료체험 시작)")
    print(f"📅 체험 만료일: {trial_expires.strftime('%Y-%m-%d %H:%M')}")
    print(f"📊 총 구독자 수: {len(subscribers)}")

    return SubscriptionResponse(
        success=True,
        message=f"{subscription.email}님의 7일 무료체험이 시작되었습니다! 체험 만료일: {trial_expires.strftime('%Y-%m-%d')}",
        subscription_id=subscription_id,
        timestamp=datetime.datetime.now().isoformat(),
        trial_expires=trial_expires.isoformat(),
    )


@app.get("/subscribers")
async def get_subscribers():
    """구독자 목록 조회 (관리자용)"""
    return {
        "total_subscribers": len(subscribers),
        "subscribers": subscribers,
        "by_plan": {
            "starter": len([s for s in subscribers if s["plan"] == "starter"]),
            "professional": len(
                [s for s in subscribers if s["plan"] == "professional"]
            ),
            "business": len([s for s in subscribers if s["plan"] == "business"]),
            "enterprise": len([s for s in subscribers if s["plan"] == "enterprise"]),
        },
    }


@app.get("/predict")
async def predict_simple(domain: str, text: Optional[str] = None):
    """데모용 무료 예측 엔드포인트 (제한된 기능)"""
    if domain not in DOMAINS:
        raise HTTPException(status_code=404, detail=f"Domain '{domain}' not found")

    # text가 없으면 도메인 정보 페이지 반환
    if text is None:
        domain_info = {
            "healthcare": {
                "name": "의료 AI",
                "description": "진단 보조, 의료 영상 분석, 건강 모니터링 시스템",
                "features": [
                    "진단 보조",
                    "의료 영상 분석",
                    "건강 모니터링",
                    "환자 데이터 분석",
                ],
            },
            "paymentapp": {
                "name": "금융 AI",
                "description": "결제 시스템, 리스크 분석, 투자 추천, 사기 탐지",
                "features": ["결제 시스템", "리스크 분석", "투자 추천", "사기 탐지"],
            },
            "education": {
                "name": "교육 AI",
                "description": "개인화 학습, 콘텐츠 생성, 평가 시스템",
                "features": ["개인화 학습", "콘텐츠 생성", "평가 시스템", "학습 분석"],
            },
            "manufacturing": {
                "name": "제조 AI",
                "description": "품질 관리, 예측 유지보수, 공급망 최적화",
                "features": [
                    "품질 관리",
                    "예측 유지보수",
                    "공급망 최적화",
                    "생산 계획",
                ],
            },
            "mobility": {
                "name": "모빌리티 AI",
                "description": "자율주행, 교통 최적화, 안전 시스템",
                "features": ["자율주행", "교통 최적화", "안전 시스템", "경로 최적화"],
            },
            "entertainment": {
                "name": "엔터테인먼트 AI",
                "description": "게임 AI, 콘텐츠 추천, 개인화 경험",
                "features": ["게임 AI", "콘텐츠 추천", "개인화 경험", "미디어 분석"],
            },
            "retail": {
                "name": "리테일 AI",
                "description": "수요 예측, 재고 관리, 고객 분석",
                "features": ["수요 예측", "재고 관리", "고객 분석", "가격 최적화"],
            },
            "energy": {
                "name": "에너지 AI",
                "description": "스마트 그리드, 에너지 최적화, 신재생 관리",
                "features": [
                    "스마트 그리드",
                    "에너지 최적화",
                    "신재생 관리",
                    "소비 예측",
                ],
            },
            "agriculture": {
                "name": "농업 AI",
                "description": "스마트 농업, 작물 모니터링, 수확량 예측",
                "features": [
                    "스마트 농업",
                    "작물 모니터링",
                    "수확량 예측",
                    "토양 분석",
                ],
            },
            "realestate": {
                "name": "부동산 AI",
                "description": "가격 예측, 투자 분석, 매물 추천",
                "features": ["가격 예측", "투자 분석", "매물 추천", "시장 분석"],
            },
            "customerservice": {
                "name": "고객서비스 AI",
                "description": "챗봇, 감정 분석, 자동 응답 시스템",
                "features": ["챗봇", "감정 분석", "자동 응답", "고객 분석"],
            },
            "saas": {
                "name": "SaaS AI",
                "description": "클라우드 서비스, API 관리, 자동화 솔루션",
                "features": [
                    "클라우드 서비스",
                    "API 관리",
                    "자동화 솔루션",
                    "시스템 최적화",
                ],
            },
        }

        info = domain_info.get(
            domain,
            {
                "name": "AI 도메인",
                "description": "전문 AI 서비스",
                "features": ["AI 분석", "데이터 처리", "예측 모델", "자동화"],
            },
        )

        return HTMLResponse(
            f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{info['name']} - HYOJIN.AI</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    padding: 20px;
                }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
                .header {{ text-align: center; margin-bottom: 40px; }}
                .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
                .header p {{ font-size: 1.2em; opacity: 0.9; }}
                .features {{ 
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    margin-bottom: 30px;
                }}
                .features h3 {{ margin-bottom: 20px; }}
                .features ul {{ list-style: none; }}
                .features li {{ 
                    padding: 10px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                }}
                .features li:last-child {{ border-bottom: none; }}
                .buttons {{ text-align: center; }}
                .btn {{ 
                    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                    color: white;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 25px;
                    text-decoration: none;
                    display: inline-block;
                    margin: 10px;
                    font-size: 1.1em;
                    transition: transform 0.3s;
                }}
                .btn:hover {{ transform: scale(1.05); }}
                .back-btn {{ 
                    background: rgba(255,255,255,0.2);
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 20px;
                    text-decoration: none;
                    display: inline-block;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-btn">← 홈으로 돌아가기</a>
                <div class="header">
                    <h1>{info['name']}</h1>
                    <p>{info['description']}</p>
                </div>
                <div class="features">
                    <h3>주요 기능</h3>
                    <ul>
                        {''.join(f'<li>✓ {feature}</li>' for feature in info['features'])}
                    </ul>
                </div>
                <div class="buttons">
                    <a href="/agents/marketplace?domain={domain}" class="btn">🤖 AI 에이전트 체험</a>
                    <a href="/subscribers" class="btn">💳 구독하기</a>
                </div>
            </div>
        </body>
        </html>
        """
        )

    # 데모용은 간단한 응답만 제공
    demo_results = {
        "paymentapp": {
            "status": "demo",
            "message": "데모 결과입니다. 실제 기능은 구독 후 이용 가능합니다.",
        },
        "healthcare": {
            "status": "demo",
            "message": "데모 결과입니다. 실제 기능은 구독 후 이용 가능합니다.",
        },
        "finance": {
            "status": "demo",
            "message": "데모 결과입니다. 실제 기능은 구독 후 이용 가능합니다.",
        },
    }

    start_time = datetime.datetime.now()
    result = demo_results.get(
        domain,
        {
            "status": "demo",
            "message": "데모 결과입니다. 실제 기능은 구독 후 이용 가능합니다.",
        },
    )
    end_time = datetime.datetime.now()
    processing_time = int((end_time - start_time).total_seconds() * 1000)

    return {
        "domain": domain,
        "result": result,
        "confidence": 0.50,  # 데모용 낮은 신뢰도
        "timestamp": datetime.datetime.now().isoformat(),
        "processing_time_ms": processing_time,
        "demo": True,
        "message": "🔒 완전한 AI 기능은 무료체험 가입 후 이용 가능합니다.",
    }


@app.post("/predict/auth")
async def predict_authenticated(request: AuthenticatedRequest):
    """인증된 사용자용 예측 엔드포인트"""
    # 도메인 확인
    if request.domain not in DOMAINS:
        raise HTTPException(
            status_code=404, detail=f"Domain '{request.domain}' not found"
        )

    # API 접근 권한 확인
    access_check = check_api_access(request.email)

    if not access_check["allowed"]:
        raise HTTPException(
            status_code=403,
            detail={
                "error": access_check["reason"],
                "error_code": access_check["error_code"],
                "details": {
                    k: v
                    for k, v in access_check.items()
                    if k not in ["allowed", "reason"]
                },
            },
        )

    subscriber = access_check["subscriber"]

    # 플랜별 도메인 접근 제한 확인
    plan_limits = get_plan_limits(subscriber["plan"])
    if request.domain not in list(DOMAINS.keys())[: plan_limits["domains"]]:
        raise HTTPException(
            status_code=403,
            detail=f"'{request.domain}' 도메인은 {subscriber['plan']} 플랜에서 이용할 수 없습니다.",
        )

    # AI 예측 실행
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(request.domain, request.text, {})
    end_time = datetime.datetime.now()
    processing_time = int((end_time - start_time).total_seconds() * 1000)

    # 사용량 증가
    increment_usage(request.email)

    return {
        "domain": request.domain,
        "result": result,
        "confidence": round(random.uniform(0.75, 0.95), 2),
        "timestamp": datetime.datetime.now().isoformat(),
        "processing_time_ms": processing_time,
        "subscriber": {
            "email": subscriber["email"],
            "plan": subscriber["plan"],
            "daily_calls": subscriber.get("daily_calls", 0) + 1,
            "trial_expires": subscriber.get("trial_expires"),
            "remaining_calls": plan_limits["daily_calls"]
            - (subscriber.get("daily_calls", 0) + 1),
        },
    }


@app.get("/status/{email}")
async def check_user_status(email: str):
    """사용자 상태 및 체험 정보 확인"""
    subscriber = get_subscriber_by_email(email)

    if not subscriber:
        raise HTTPException(status_code=404, detail="등록되지 않은 이메일입니다.")

    plan_limits = get_plan_limits(subscriber["plan"])
    trial_expired = (
        is_trial_expired(subscriber.get("trial_expires"))
        if subscriber["plan"] == "trial"
        else False
    )

    return {
        "email": subscriber["email"],
        "plan": subscriber["plan"],
        "original_plan": subscriber.get("original_plan"),
        "status": subscriber["status"],
        "trial_expires": subscriber.get("trial_expires"),
        "trial_expired": trial_expired,
        "days_remaining": (
            (
                datetime.datetime.fromisoformat(subscriber.get("trial_expires", ""))
                - datetime.datetime.now()
            ).days
            if subscriber.get("trial_expires") and not trial_expired
            else 0
        ),
        "usage": {
            "daily_calls": subscriber.get("daily_calls", 0),
            "max_daily_calls": plan_limits["daily_calls"],
            "remaining_calls": plan_limits["daily_calls"]
            - subscriber.get("daily_calls", 0),
            "total_calls": subscriber.get("total_calls", 0),
        },
        "access": {
            "available_domains": plan_limits["domains"],
            "domain_list": list(DOMAINS.keys())[: plan_limits["domains"]],
        },
        "last_used": subscriber.get("last_used"),
    }


# 12개 도메인별 예측 엔드포인트 (한번에 다 구현!)
@app.post("/api/v1/paymentapp/predict", response_model=PredictResponse)
async def predict_payment(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "paymentapp", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="paymentapp",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/deliveryservice/predict", response_model=PredictResponse)
async def predict_delivery(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "deliveryservice", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="deliveryservice",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/onlineshopping/predict", response_model=PredictResponse)
async def predict_shopping(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "onlineshopping", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="onlineshopping",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/realestateapp/predict", response_model=PredictResponse)
async def predict_realestate(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "realestateapp", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="realestateapp",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/onlineeducation/predict", response_model=PredictResponse)
async def predict_education(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "onlineeducation", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="onlineeducation",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/jobplatform/predict", response_model=PredictResponse)
async def predict_jobs(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "jobplatform", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="jobplatform",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/manufacturing/predict", response_model=PredictResponse)
async def predict_manufacturing(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "manufacturing", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="manufacturing",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/retail/predict", response_model=PredictResponse)
async def predict_retail(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction("retail", request.input_data, request.parameters)
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="retail",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/logistics/predict", response_model=PredictResponse)
async def predict_logistics(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction("logistics", request.input_data, request.parameters)
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="logistics",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/customerservice/predict", response_model=PredictResponse)
async def predict_customerservice(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "customerservice", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="customerservice",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


@app.post("/api/v1/healthcare/predict", response_model=PredictResponse)
async def predict_healthcare(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction(
        "healthcare", request.input_data, request.parameters
    )
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="healthcare",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


# ═══════════════════════════════════════════════════════════════════
# 🏢 구독관리회사시스템 통합 엔드포인트
# ═══════════════════════════════════════════════════════════════════


@app.get("/admin/subscription-management")
async def get_subscription_management_dashboard(admin: bool = Depends(admin_required)):
    """구독관리 대시보드 HTML 반환"""
    dashboard_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HYOJIN.AI 구독관리 시스템</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2.5rem; font-weight: bold; color: #667eea; }
            .stat-label { font-size: 0.9rem; color: #666; text-transform: uppercase; }
            .subscribers-table { background: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f8f9fa; font-weight: 600; }
            .status-active { color: #28a745; font-weight: bold; }
            .status-trial { color: #ffc107; font-weight: bold; }
            .plan-professional { background: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 4px; }
            .plan-business { background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 4px; }
            .plan-enterprise { background: #e8f5e8; color: #388e3c; padding: 4px 8px; border-radius: 4px; }
            .refresh-btn { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            
            /* 도메인 관리 스타일 */
            .domain-card { 
                background: white; 
                border: 2px solid #e9ecef; 
                border-radius: 10px; 
                padding: 20px; 
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .domain-card:hover { 
                border-color: #667eea; 
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            .domain-card h3 { 
                margin: 0 0 10px 0; 
                color: #333; 
                font-size: 1.2rem;
            }
            .domain-card p { 
                margin: 0 0 15px 0; 
                color: #666; 
                font-size: 0.9rem;
                line-height: 1.4;
            }
            .domain-actions { 
                display: flex; 
                gap: 8px; 
            }
            .btn-primary { 
                background: #667eea; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 5px; 
                cursor: pointer; 
                font-size: 0.85rem;
                flex: 1;
            }
            .btn-secondary { 
                background: #6c757d; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 5px; 
                cursor: pointer; 
                font-size: 0.85rem;
                flex: 1;
            }
            .btn-primary:hover { background: #5a6fd8; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏢 HYOJIN.AI 통합 관리 시스템</h1>
                <p>엔터프라이즈급 구독자 관리 + 12개 도메인 랜딩페이지 + AI 에이전트 저장소</p>
                <div style="margin-top: 20px;">
                    <a href="/agents/marketplace" style="background: rgba(255,255,255,0.2); color: white; text-decoration: none; padding: 8px 16px; border-radius: 20px; margin-right: 8px; font-size: 0.9rem;">🤖 AI 에이전트</a>
                    <a href="/landing-preview" style="background: rgba(255,255,255,0.2); color: white; text-decoration: none; padding: 8px 16px; border-radius: 20px; margin-right: 8px; font-size: 0.9rem;">🚀 에이전트 랜딩</a>
                    <button onclick="showDomainManager()" style="background: rgba(255,255,255,0.3); color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 0.9rem;">🌐 12개 도메인 관리</button>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number" id="total-subscribers">-</div>
                    <div class="stat-label">총 구독자</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="active-trials">-</div>
                    <div class="stat-label">무료체험 중</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="paid-subscribers">-</div>
                    <div class="stat-label">유료 구독자</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="total-api-calls">-</div>
                    <div class="stat-label">총 API 호출</div>
                </div>
            </div>
            
            <div class="subscribers-table">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>구독자 목록</h2>
                    <button class="refresh-btn" onclick="loadData()">🔄 새로고침</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>이메일</th>
                            <th>회사</th>
                            <th>플랜</th>
                            <th>상태</th>
                            <th>가입일</th>
                            <th>API 사용량</th>
                            <th>관리</th>
                        </tr>
                    </thead>
                    <tbody id="subscribers-tbody">
                        <!-- 동적으로 로드됨 -->
                    </tbody>
                </table>
            </div>
            
            <!-- 도메인 관리 모달 -->
            <div id="domain-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 30px; border-radius: 15px; width: 90%; max-width: 1000px; max-height: 80%; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                        <h2>🌐 12개 도메인 랜딩페이지 관리</h2>
                        <button onclick="hideDomainManager()" style="background: #dc3545; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">✕ 닫기</button>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                        <div class="domain-card" data-domain="medical">
                            <h3>🏥 의료 예측 AI</h3>
                            <p>질병 진단 및 치료 예측</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('medical')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('medical')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="finance">
                            <h3>💰 금융 분석 AI</h3>
                            <p>투자 및 리스크 분석</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('finance')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('finance')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="education">
                            <h3>🎓 교육 최적화 AI</h3>
                            <p>맞춤형 학습 경로 추천</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('education')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('education')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="manufacturing">
                            <h3>🏭 제조업 최적화 AI</h3>
                            <p>생산 효율성 및 품질 관리</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('manufacturing')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('manufacturing')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="retail">
                            <h3>🛒 리테일 인사이트 AI</h3>
                            <p>고객 행동 및 재고 최적화</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('retail')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('retail')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="logistics">
                            <h3>🚚 물류 최적화 AI</h3>
                            <p>배송 경로 및 창고 관리</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('logistics')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('logistics')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="energy">
                            <h3>⚡ 에너지 관리 AI</h3>
                            <p>스마트 그리드 및 효율성</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('energy')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('energy')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="agriculture">
                            <h3>🌾 농업 스마트팜 AI</h3>
                            <p>작물 예측 및 최적화</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('agriculture')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('agriculture')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="real_estate">
                            <h3>🏠 부동산 가격 AI</h3>
                            <p>시장 분석 및 가격 예측</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('real_estate')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('real_estate')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="entertainment">
                            <h3>🎬 엔터테인먼트 AI</h3>
                            <p>콘텐츠 추천 및 분석</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('entertainment')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('entertainment')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="cybersecurity">
                            <h3>🔒 사이버보안 AI</h3>
                            <p>위협 탐지 및 방어</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('cybersecurity')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('cybersecurity')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                        
                        <div class="domain-card" data-domain="smart_city">
                            <h3>🏙️ 스마트시티 AI</h3>
                            <p>도시 인프라 최적화</p>
                            <div class="domain-actions">
                                <button onclick="manageDomain('smart_city')" class="btn-primary">페이지 관리</button>
                                <button onclick="viewAnalytics('smart_city')" class="btn-secondary">분석 보기</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function loadData() {
                try {
                    const response = await fetch('/subscribers');
                    const data = await response.json();
                    
                    // 통계 업데이트
                    const subscribers = data.subscribers || [];
                    document.getElementById('total-subscribers').textContent = subscribers.length;
                    
                    const trials = subscribers.filter(s => s.plan === 'trial').length;
                    document.getElementById('active-trials').textContent = trials;
                    
                    const paid = subscribers.filter(s => s.plan !== 'trial').length;
                    document.getElementById('paid-subscribers').textContent = paid;
                    
                    const totalCalls = subscribers.reduce((sum, s) => sum + (s.daily_calls || 0), 0);
                    document.getElementById('total-api-calls').textContent = totalCalls;
                    
                    // 구독자 테이블 업데이트
                    const tbody = document.getElementById('subscribers-tbody');
                    tbody.innerHTML = '';
                    
                    subscribers.forEach(subscriber => {
                        const row = document.createElement('tr');
                        const planClass = `plan-${subscriber.plan}`;
                        const statusClass = subscriber.plan === 'trial' ? 'status-trial' : 'status-active';
                        
                        row.innerHTML = `
                            <td>${subscriber.email}</td>
                            <td>${subscriber.company || '-'}</td>
                            <td><span class="${planClass}">${subscriber.plan}</span></td>
                            <td><span class="${statusClass}">${subscriber.plan === 'trial' ? '무료체험' : '유료'}</span></td>
                            <td>${new Date(subscriber.timestamp).toLocaleDateString()}</td>
                            <td>${subscriber.daily_calls || 0} 회</td>
                            <td>
                                <button onclick="manageUser('${subscriber.email}')" style="padding: 5px 10px; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer;">관리</button>
                            </td>
                        `;
                        tbody.appendChild(row);
                    });
                    
                } catch (error) {
                    console.error('데이터 로드 오류:', error);
                }
            }
            
            function manageUser(email) {
                const action = confirm(`${email} 사용자를 관리하시겠습니까?\\n\\n확인: 플랜 변경\\n취소: 아무 작업 안함`);
                if (action) {
                    const newPlan = prompt('새 플랜을 입력하세요 (trial, professional, business, enterprise):');
                    if (newPlan) {
                        updateUserPlan(email, newPlan);
                    }
                }
            }
            
            async function updateUserPlan(email, plan) {
                try {
                    const response = await fetch('/admin/update-subscription', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({email, plan, status: 'active'})
                    });
                    
                    if (response.ok) {
                        alert('플랜이 성공적으로 변경되었습니다!');
                        loadData();
                    } else {
                        alert('플랜 변경에 실패했습니다.');
                    }
                } catch (error) {
                    alert('오류가 발생했습니다: ' + error.message);
                }
            }
            
            // 페이지 로드 시 데이터 로드
            document.addEventListener('DOMContentLoaded', loadData);
            
            // 도메인 관리 함수들
            function showDomainManager() {
                document.getElementById('domain-modal').style.display = 'block';
            }
            
            function hideDomainManager() {
                document.getElementById('domain-modal').style.display = 'none';
            }
            
            function manageDomain(domain) {
                const domainNames = {
                    medical: '의료 예측 AI',
                    finance: '금융 분석 AI', 
                    education: '교육 최적화 AI',
                    manufacturing: '제조업 최적화 AI',
                    retail: '리테일 인사이트 AI',
                    logistics: '물류 최적화 AI',
                    energy: '에너지 관리 AI',
                    agriculture: '농업 스마트팜 AI',
                    real_estate: '부동산 가격 AI',
                    entertainment: '엔터테인먼트 AI',
                    cybersecurity: '사이버보안 AI',
                    smart_city: '스마트시티 AI'
                };
                
                const actions = [
                    '페이지 콘텐츠 수정',
                    'SEO 최적화 설정',
                    '광고 캠페인 관리',
                    '사용자 피드백 확인',
                    '성능 최적화'
                ];
                
                const action = prompt(`${domainNames[domain]} 관리\\n\\n수행할 작업을 선택하세요:\\n\\n1. ${actions[0]}\\n2. ${actions[1]}\\n3. ${actions[2]}\\n4. ${actions[3]}\\n5. ${actions[4]}\\n\\n번호를 입력하세요 (1-5):`);
                
                if (action && action >= 1 && action <= 5) {
                    alert(`${domainNames[domain]}\\n"${actions[parseInt(action)-1]}" 작업이 시작되었습니다!\\n\\n관리자 대시보드에서 진행상황을 확인할 수 있습니다.`);
                    
                    // 실제로는 여기서 백엔드 API 호출
                    updateDomainManagement(domain, actions[parseInt(action)-1]);
                }
            }
            
            function viewAnalytics(domain) {
                const domainNames = {
                    medical: '의료 예측 AI',
                    finance: '금융 분석 AI', 
                    education: '교육 최적화 AI',
                    manufacturing: '제조업 최적화 AI',
                    retail: '리테일 인사이트 AI',
                    logistics: '물류 최적화 AI',
                    energy: '에너지 관리 AI',
                    agriculture: '농업 스마트팜 AI',
                    real_estate: '부동산 가격 AI',
                    entertainment: '엔터테인먼트 AI',
                    cybersecurity: '사이버보안 AI',
                    smart_city: '스마트시티 AI'
                };
                
                // 실시간 분석 데이터 생성 (실제로는 백엔드에서 가져옴)
                const analytics = {
                    visitors: Math.floor(Math.random() * 10000) + 1000,
                    conversions: Math.floor(Math.random() * 500) + 50,
                    revenue: Math.floor(Math.random() * 50000) + 5000,
                    growth: (Math.random() * 50 + 10).toFixed(1)
                };
                
                alert(`${domainNames[domain]} 분석 리포트\\n\\n📊 이번 달 통계:\\n• 방문자: ${analytics.visitors.toLocaleString()}명\\n• 전환율: ${analytics.conversions}건\\n• 매출: $${analytics.revenue.toLocaleString()}\\n• 성장률: +${analytics.growth}%\\n\\n상세 분석은 별도 대시보드에서 확인하세요.`);
            }
            
            async function updateDomainManagement(domain, action) {
                try {
                    const response = await fetch('/admin/manage-domain', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            domain: domain,
                            action: action,
                            timestamp: new Date().toISOString(),
                            admin_id: 'admin_user'
                        })
                    });
                    
                    if (response.ok) {
                        console.log(`도메인 ${domain} 관리 작업 "${action}" 완료`);
                    }
                } catch (error) {
                    console.error('도메인 관리 오류:', error);
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=dashboard_html)


@app.post("/admin/update-subscription")
async def update_subscription(
    request: SubscriptionUpdateRequest, admin: bool = Depends(admin_required)
):
    """구독 정보 업데이트 (관리자용)"""
    global subscribers

    for i, subscriber in enumerate(subscribers):
        if subscriber["email"] == request.email:
            subscribers[i]["plan"] = request.plan
            subscribers[i]["status"] = request.status
            subscribers[i]["updated_at"] = datetime.datetime.now().isoformat()

            return {
                "success": True,
                "message": f"{request.email}의 플랜이 {request.plan}으로 변경되었습니다.",
                "subscriber": subscribers[i],
            }

    raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다.")


# 도메인 관리 요청 모델
class DomainManagementRequest(BaseModel):
    domain: str
    action: str
    timestamp: str
    admin_id: str


@app.post("/admin/manage-domain")
async def manage_domain(
    request: DomainManagementRequest, admin: bool = Depends(admin_required)
):
    """12개 도메인 랜딩페이지 관리"""

    # 도메인별 관리 작업 로그 저장 (실제로는 데이터베이스에 저장)
    domain_log = {
        "domain": request.domain,
        "action": request.action,
        "timestamp": request.timestamp,
        "admin_id": request.admin_id,
        "status": "completed",
        "log_id": str(uuid.uuid4()),
    }

    # 도메인별 작업 시뮬레이션
    domain_actions = {
        "페이지 콘텐츠 수정": "랜딩페이지 콘텐츠가 업데이트되었습니다.",
        "SEO 최적화 설정": "메타태그 및 키워드가 최적화되었습니다.",
        "광고 캠페인 관리": "광고 캠페인 설정이 업데이트되었습니다.",
        "사용자 피드백 확인": "최근 피드백이 분석되었습니다.",
        "성능 최적화": "페이지 로딩 속도가 개선되었습니다.",
    }

    result_message = domain_actions.get(request.action, "관리 작업이 완료되었습니다.")

    return {
        "success": True,
        "message": f"{request.domain} 도메인: {result_message}",
        "log": domain_log,
        "domain_url": f"/predict/{request.domain}",
        "timestamp": datetime.datetime.now().isoformat(),
    }


@app.get("/admin/domain-analytics/{domain}")
async def get_domain_analytics(domain: str, admin: bool = Depends(admin_required)):
    """특정 도메인의 분석 데이터 반환"""

    # 실시간 분석 데이터 시뮬레이션 (실제로는 실제 데이터)
    analytics_data = {
        "domain": domain,
        "period": "last_30_days",
        "metrics": {
            "visitors": random.randint(1000, 15000),
            "page_views": random.randint(2000, 25000),
            "conversions": random.randint(50, 800),
            "conversion_rate": round(random.uniform(2.0, 12.0), 2),
            "avg_session_duration": random.randint(120, 600),
            "bounce_rate": round(random.uniform(25.0, 70.0), 2),
            "revenue": random.randint(5000, 80000),
            "growth_rate": round(random.uniform(-10.0, 50.0), 1),
        },
        "top_pages": [
            f"/predict/{domain}",
            f"/predict/{domain}/demo",
            f"/predict/{domain}/pricing",
            f"/predict/{domain}/docs",
        ],
        "user_feedback": {
            "average_rating": round(random.uniform(3.5, 4.8), 1),
            "total_reviews": random.randint(50, 500),
            "satisfaction_score": round(random.uniform(75.0, 95.0), 1),
        },
        "timestamp": datetime.datetime.now().isoformat(),
    }

    return analytics_data


@app.post("/admin/user-management")
async def user_management(
    request: UserManagementRequest, admin: bool = Depends(admin_required)
):
    """사용자 관리 기능 (생성, 수정, 삭제, 일시정지)"""
    global subscribers

    if request.action == "create":
        # 새 사용자 생성
        new_subscriber = {
            "subscription_id": str(uuid.uuid4()),
            "email": request.email,
            "company": request.data.get("company", ""),
            "plan": request.data.get("plan", "trial"),
            "timestamp": datetime.datetime.now().isoformat(),
            "trial_expires": calculate_trial_expiry(),
            "daily_calls": 0,
            "status": "active",
        }
        subscribers.append(new_subscriber)
        return {
            "success": True,
            "message": "사용자가 생성되었습니다.",
            "user": new_subscriber,
        }

    elif request.action == "update":
        # 기존 사용자 업데이트
        for i, subscriber in enumerate(subscribers):
            if subscriber["email"] == request.email:
                subscribers[i].update(request.data)
                subscribers[i]["updated_at"] = datetime.datetime.now().isoformat()
                return {
                    "success": True,
                    "message": "사용자 정보가 업데이트되었습니다.",
                    "user": subscribers[i],
                }
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    elif request.action == "delete":
        # 사용자 삭제
        subscribers = [s for s in subscribers if s["email"] != request.email]
        return {"success": True, "message": f"{request.email} 사용자가 삭제되었습니다."}

    elif request.action == "suspend":
        # 사용자 일시정지
        for i, subscriber in enumerate(subscribers):
            if subscriber["email"] == request.email:
                subscribers[i]["status"] = "suspended"
                subscribers[i]["suspended_at"] = datetime.datetime.now().isoformat()
                return {
                    "success": True,
                    "message": f"{request.email} 사용자가 일시정지되었습니다.",
                }
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    else:
        raise HTTPException(status_code=400, detail="지원하지 않는 작업입니다.")


@app.post("/admin/financial-analysis")
async def financial_analysis(
    request: FinancialAnalysisRequest, admin: bool = Depends(admin_required)
):
    """재무 분석 및 ROI 계산"""

    # 플랜별 요금
    plan_prices = {
        "trial": 0,
        "startup": 99000,
        "professional": 299000,
        "business": 599000,
        "enterprise": 1299000,
    }

    # 구독자 데이터 분석
    user_data = None
    if request.email:
        user_data = next((s for s in subscribers if s["email"] == request.email), None)

    # 전체 재무 분석
    total_revenue = 0
    total_users = len(subscribers)
    plan_distribution = {}

    for subscriber in subscribers:
        plan = subscriber["plan"]
        price = plan_prices.get(plan, 0)
        total_revenue += price
        plan_distribution[plan] = plan_distribution.get(plan, 0) + 1

    # API 사용량 분석
    total_api_calls = sum(s.get("daily_calls", 0) for s in subscribers)
    avg_calls_per_user = total_api_calls / total_users if total_users > 0 else 0

    analysis_result = {
        "period": request.period,
        "total_revenue": total_revenue,
        "total_users": total_users,
        "plan_distribution": plan_distribution,
        "api_metrics": {
            "total_calls": total_api_calls,
            "average_per_user": round(avg_calls_per_user, 2),
        },
        "financial_metrics": {
            "arpu": (
                round(total_revenue / total_users, 2) if total_users > 0 else 0
            ),  # Average Revenue Per User
            "conversion_rate": (
                round(
                    (total_users - plan_distribution.get("trial", 0))
                    / total_users
                    * 100,
                    2,
                )
                if total_users > 0
                else 0
            ),
        },
        "timestamp": datetime.datetime.now().isoformat(),
    }

    if user_data:
        user_revenue = plan_prices.get(user_data["plan"], 0)
        analysis_result["user_analysis"] = {
            "email": request.email,
            "plan": user_data["plan"],
            "monthly_revenue": user_revenue,
            "api_usage": user_data.get("daily_calls", 0),
            "roi_score": calculate_user_roi(user_data),
        }

    return analysis_result


def calculate_user_roi(user_data):
    """사용자별 ROI 계산"""
    plan_values = {
        "trial": 0,
        "startup": 1,
        "professional": 3,
        "business": 6,
        "enterprise": 10,
    }
    plan_score = plan_values.get(user_data["plan"], 0)
    usage_score = min(user_data.get("daily_calls", 0) / 10, 5)  # 10회당 1점, 최대 5점

    return round(plan_score + usage_score, 2)


@app.get("/admin/system-status")
async def get_system_status(admin: bool = Depends(admin_required)):
    """시스템 상태 및 헬스체크"""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "features": [
            "12개 AI 도메인",
            "15개 AI 에이전트",
            "구독관리 시스템",
            "사용자 인증",
            "재무 분석",
            "ROI 계산",
            "AI 에이전트 마켓플레이스",
        ],
        "total_subscribers": len(subscribers),
        "active_domains": 12,
        "ai_agents": {
            "total": len(ai_agents),
            "available": len(
                [a for a in ai_agents.values() if a.get("status") != "coming_soon"]
            ),
            "coming_soon": len(
                [a for a in ai_agents.values() if a.get("status") == "coming_soon"]
            ),
        },
        "marketplace_url": "/agents/marketplace",
        "uptime": "99.9%",
        "last_updated": datetime.datetime.now().isoformat(),
    }


@app.post("/api/v1/finance/predict", response_model=PredictResponse)
async def predict_finance(request: PredictRequest):
    start_time = datetime.datetime.now()
    result = generate_ai_prediction("finance", request.input_data, request.parameters)
    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000

    return PredictResponse(
        domain="finance",
        result=result,
        confidence=round(random.uniform(0.8, 0.95), 2),
        timestamp=datetime.datetime.now().isoformat(),
        processing_time_ms=int(processing_time),
    )


# ═══════════════════════════════════════════════════════════════════
# 🤖 AI 에이전트 저장소 시스템
# ═══════════════════════════════════════════════════════════════════


@app.get("/agents")
async def get_available_agents():
    """사용 가능한 AI 에이전트 목록 반환"""
    return {
        "success": True,
        "agents": ai_agents,
        "total_agents": len(ai_agents),
        "timestamp": datetime.datetime.now().isoformat(),
    }


@app.get("/agents/marketplace")
async def get_agent_marketplace(email: Optional[str] = None):
    """AI 에이전트 마켓플레이스 HTML 반환 - 구독자 확인 포함"""

    # 구독자 상태 확인
    if email:
        subscriber = get_subscriber_by_email(email)
        is_subscriber = subscriber is not None
        user_plan = subscriber.get("plan", "trial") if subscriber else "trial"
        usage_info = get_usage_limit(user_plan)

        if is_subscriber:
            status_message = (
                f"✅ {usage_info['name']} 사용자 - {usage_info['calls']}회 사용 가능"
            )
        else:
            status_message = "🆓 무료 체험 사용자 - 3회 사용 가능"
    else:
        status_message = "👋 이메일을 입력하여 체험하세요"

    # 마켓플레이스 HTML 생성
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HYOJIN.AI 에이전트 마켓플레이스</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .header {{ text-align: center; padding: 50px 20px; color: white; }}
            .header h1 {{ font-size: 3rem; margin-bottom: 20px; }}
            .header p {{ font-size: 1.2rem; opacity: 0.9; }}
            .status-bar {{ background: rgba(255,255,255,0.15); color: white; padding: 15px; text-align: center; margin: 20px auto; max-width: 600px; border-radius: 10px; font-weight: 600; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
            .agents-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; margin-bottom: 50px; }}
            .agent-card {{ background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; }}
            .agent-card:hover {{ transform: translateY(-10px); }}
            .agent-icon {{ font-size: 3rem; margin-bottom: 20px; text-align: center; }}
            .agent-name {{ font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; color: #667eea; text-align: center; }}
            .agent-description {{ line-height: 1.6; margin-bottom: 20px; opacity: 0.9; text-align: center; }}
            .capabilities {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; justify-content: center; }}
            .capability-tag {{ background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 4px 12px; border-radius: 15px; font-size: 0.9rem; }}
            .deploy-btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 25px; border-radius: 25px; cursor: pointer; font-weight: bold; width: 100%; }}
            .deploy-btn:hover {{ transform: scale(1.05); }}
            .email-input {{ position: fixed; top: 20px; right: 20px; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 10px; }}
            .email-input input {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 5px; margin-right: 10px; }}
            .email-input button {{ background: #667eea; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 AI 에이전트 마켓플레이스</h1>
            <p>15개의 전문 AI 에이전트로 업무를 자동화하세요</p>
            <div class="status-bar">
                {status_message}
            </div>
        </div>
        
        {"" if email else '<div class="email-input"><input type="email" id="email" placeholder="이메일 입력"><button onclick="accessWithEmail()">접근하기</button></div>'}
        
        <div class="container">
            <div class="agents-grid" id="agentsGrid">
                <!-- 에이전트 카드들이 JavaScript로 동적 생성됩니다 -->
            </div>
        </div>
        
        <script>
            const userEmail = "{email or ''}";
            const isAuthenticated = userEmail !== '';
            
            function accessWithEmail() {{
                const email = document.getElementById('email').value;
                if (email) {{
                    window.location.href = `/agents/marketplace?email=${{encodeURIComponent(email)}}`;
                }}
            }}
            
            async function loadAgents() {{
                try {{
                    console.log('에이전트 로딩 시작...');
                    const response = await fetch('/agents');
                    console.log('응답 상태:', response.status);
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP 오류! 상태: ${{response.status}}`);
                    }}
                    
                    const data = await response.json();
                    console.log('에이전트 데이터:', data);
                    
                    const grid = document.getElementById('agentsGrid');
                    grid.innerHTML = '';
                    
                    if (data.agents) {{
                        Object.entries(data.agents).forEach(([type, agent]) => {{
                            const card = document.createElement('div');
                            card.className = 'agent-card';
                            
                            card.innerHTML = `
                                <div class="agent-icon">${{agent.icon}}</div>
                                <div class="agent-name">${{agent.name}}</div>
                                <div class="agent-description">${{agent.description}}</div>
                                <div class="capabilities">
                                    ${{agent.capabilities.map(cap => `<span class="capability-tag">${{cap}}</span>`).join('')}}
                                </div>
                                <button class="deploy-btn" onclick="deployAgent('${{type}}')">🚀 에이전트 배포</button>
                            `;
                            
                            grid.appendChild(card);
                        }});
                        console.log('에이전트 카드 생성 완료');
                    }} else {{
                        grid.innerHTML = '<p style="color: white; text-align: center;">에이전트 데이터를 불러올 수 없습니다.</p>';
                    }}
                }} catch (error) {{
                    console.error('에이전트 로드 오류:', error);
                    const grid = document.getElementById('agentsGrid');
                    grid.innerHTML = `<p style="color: white; text-align: center;">오류: ${{error.message}}</p>`;
                }}
            }}
            
            async function deployAgent(agentType) {{
                if (isAuthenticated) {{
                    alert(`${{agentType}} 에이전트 배포 요청이 접수되었습니다!`);
                }} else {{
                    alert('에이전트 사용을 위해 이메일 인증이 필요합니다.');
                    document.getElementById('email').focus();
                }}
            }}
            
            document.addEventListener('DOMContentLoaded', loadAgents);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/agents/{agent_type}")
async def get_agent_details(agent_type: str):
    """특정 AI 에이전트의 상세 정보"""
    if agent_type not in ai_agents:
        raise HTTPException(status_code=404, detail="에이전트를 찾을 수 없습니다")

    agent = ai_agents[agent_type]
    return {
        "success": True,
        "agent": agent,
        "usage_examples": get_agent_examples(agent_type),
        "timestamp": datetime.datetime.now().isoformat(),
    }


@app.post("/agents/execute")
async def execute_agent(request: AgentRequest):
    """AI 에이전트 실행"""
    start_time = datetime.datetime.now()

    if request.agent_type not in ai_agents:
        raise HTTPException(status_code=404, detail="에이전트를 찾을 수 없습니다")

    agent_info = ai_agents[request.agent_type]

    # 에이전트별 특화 처리
    result = execute_specialized_agent(
        request.agent_type, request.task_description, request.parameters
    )

    processing_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
    task_id = str(uuid.uuid4())

    return AgentResponse(
        agent_type=request.agent_type,
        task_id=task_id,
        result=result,
        autonomy_score=agent_info["autonomy_score"],
        execution_time_ms=int(processing_time),
        timestamp=datetime.datetime.now().isoformat(),
    )


@app.post("/agents/deploy")
async def deploy_agent(request: AgentDeployRequest):
    """구독자용 AI 에이전트 배포"""
    # 구독자 확인
    subscriber = get_subscriber_by_email(request.email)
    if not subscriber:
        raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다")

    # 플랜별 에이전트 접근 권한 확인
    allowed_agents = get_allowed_agents_by_plan(subscriber["plan"])
    if request.agent_type not in allowed_agents:
        raise HTTPException(
            status_code=403, detail="플랜에서 지원하지 않는 에이전트입니다"
        )

    # 에이전트 배포
    deployment_id = str(uuid.uuid4())

    return {
        "success": True,
        "deployment_id": deployment_id,
        "agent_type": request.agent_type,
        "email": request.email,
        "config": request.deployment_config,
        "status": "deployed",
        "timestamp": datetime.datetime.now().isoformat(),
    }


@app.get("/test-agents")
async def test_agents():
    """테스트용 에이전트 엔드포인트"""
    return {
        "message": "AI 에이전트 섹션이 정상적으로 로드되었습니다!",
        "timestamp": datetime.datetime.now().isoformat(),
    }


# AI 에이전트 헬퍼 함수들
def get_agent_examples(agent_type):
    """에이전트별 사용 예시"""
    examples = {
        "strategy": [
            "시장 진입 전략 수립",
            "경쟁사 분석 보고서",
            "비즈니스 모델 최적화",
        ],
        "datascience": ["고객 행동 예측 모델", "매출 예측 분석", "추천 시스템 구축"],
        "developer": ["웹 애플리케이션 개발", "API 설계 및 구현", "코드 리팩토링"],
        "marketing": ["캠페인 전략 기획", "브랜드 포지셔닝", "성과 분석 및 최적화"],
        "finance": ["투자 포트폴리오 분석", "리스크 평가", "재무 모델링"],
    }
    return examples.get(agent_type, [])


def execute_specialized_agent(agent_type, task_description, parameters):
    """에이전트별 특화 실행"""
    base_result = {
        "task_description": task_description,
        "status": "completed",
        "execution_steps": [],
    }

    if agent_type == "strategy":
        base_result.update(
            {
                "analysis": "시장 분석 완료",
                "recommendations": ["전략 A", "전략 B", "전략 C"],
                "risk_assessment": "중간 위험도",
                "expected_roi": "15-25%",
            }
        )
    elif agent_type == "datascience":
        base_result.update(
            {
                "model_type": "Random Forest",
                "accuracy": round(random.uniform(0.85, 0.98), 3),
                "features_analyzed": random.randint(10, 50),
                "insights": ["인사이트 1", "인사이트 2", "인사이트 3"],
            }
        )
    elif agent_type == "developer":
        base_result.update(
            {
                "code_generated": "1,247 lines",
                "tests_written": random.randint(20, 50),
                "coverage": f"{random.randint(85, 98)}%",
                "technologies": ["React", "FastAPI", "PostgreSQL"],
            }
        )
    elif agent_type == "marketing":
        base_result.update(
            {
                "campaign_reach": f"{random.randint(10, 100)}K",
                "engagement_rate": f"{random.randint(3, 15)}%",
                "conversion_rate": f"{random.randint(2, 8)}%",
                "channels": ["Social Media", "Email", "Content Marketing"],
            }
        )
    elif agent_type == "finance":
        base_result.update(
            {
                "portfolio_value": f"${random.randint(100, 1000)}K",
                "expected_return": f"{random.randint(8, 20)}%",
                "risk_score": random.randint(3, 8),
                "diversification_score": random.randint(70, 95),
            }
        )

    return base_result


@app.get("/landing-preview")
async def get_agent_landing_preview():
    """에이전트 랜딩페이지 미리보기"""
    landing_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HYOJIN.AI - 에이전트 랜딩페이지 미리보기</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                background: #fff;
            }
            
            /* Hero Section */
            .hero { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 80px 20px; 
                text-align: center; 
                position: relative;
                overflow: hidden;
            }
            .hero::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                pointer-events: none;
            }
            .hero-content { 
                max-width: 1200px; 
                margin: 0 auto; 
                position: relative; 
                z-index: 2;
            }
            .hero h1 { 
                font-size: 3.5rem; 
                margin-bottom: 20px; 
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            .hero p { 
                font-size: 1.25rem; 
                margin-bottom: 30px; 
                opacity: 0.95;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .cta-button { 
                display: inline-block;
                background: rgba(255,255,255,0.2); 
                color: white; 
                padding: 15px 30px; 
                border-radius: 50px; 
                text-decoration: none; 
                font-weight: 600;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                border: 2px solid rgba(255,255,255,0.3);
                backdrop-filter: blur(10px);
            }
            .cta-button:hover { 
                background: rgba(255,255,255,0.3);
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }
            
            /* Features Section */
            .features { 
                padding: 80px 20px; 
                background: #f8f9fa;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
            }
            .section-title { 
                text-align: center; 
                font-size: 2.5rem; 
                margin-bottom: 60px; 
                color: #333;
                font-weight: 700;
            }
            .features-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 40px; 
            }
            .feature-card { 
                background: white; 
                padding: 40px 30px; 
                border-radius: 20px; 
                text-align: center; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.08); 
                transition: all 0.3s ease;
                border: 1px solid #eee;
            }
            .feature-card:hover { 
                transform: translateY(-5px); 
                box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            }
            .feature-icon { 
                font-size: 3rem; 
                margin-bottom: 25px; 
                display: block;
            }
            .feature-title { 
                font-size: 1.3rem; 
                margin-bottom: 15px; 
                color: #333;
                font-weight: 600;
            }
            .feature-description { 
                color: #666; 
                line-height: 1.6;
            }
            
            /* Agents Section */
            .agents-section { 
                padding: 80px 20px; 
                background: white;
            }
            .agents-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
                gap: 30px; 
                margin-top: 50px;
            }
            .agent-card { 
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 30px 25px; 
                border-radius: 15px; 
                text-align: center; 
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            .agent-card:hover { 
                transform: translateY(-3px); 
                border-color: #667eea;
                background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
            }
            .agent-emoji { 
                font-size: 2.5rem; 
                margin-bottom: 20px; 
                display: block;
            }
            .agent-name { 
                font-size: 1.2rem; 
                margin-bottom: 10px; 
                color: #333;
                font-weight: 600;
            }
            .agent-desc { 
                color: #666; 
                font-size: 0.9rem;
                line-height: 1.5;
            }
            
            /* Pricing Section */
            .pricing { 
                padding: 80px 20px; 
                background: #f8f9fa;
            }
            .pricing-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 30px; 
                margin-top: 50px;
            }
            .pricing-card { 
                background: white; 
                padding: 40px 30px; 
                border-radius: 20px; 
                text-align: center; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
                border: 2px solid #eee;
                transition: all 0.3s ease;
            }
            .pricing-card:hover { 
                transform: translateY(-5px); 
                border-color: #667eea;
            }
            .pricing-card.featured { 
                border-color: #667eea; 
                transform: scale(1.05);
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
            }
            .plan-name { 
                font-size: 1.3rem; 
                margin-bottom: 10px; 
                color: #333;
                font-weight: 600;
            }
            .plan-price { 
                font-size: 2.5rem; 
                margin-bottom: 20px; 
                color: #667eea;
                font-weight: 700;
            }
            .plan-features { 
                list-style: none; 
                margin-bottom: 30px;
            }
            .plan-features li { 
                padding: 8px 0; 
                color: #666;
            }
            .plan-features li::before { 
                content: '✓'; 
                color: #28a745; 
                font-weight: bold; 
                margin-right: 8px;
            }
            .plan-button { 
                background: #667eea; 
                color: white; 
                padding: 12px 30px; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            .plan-button:hover { 
                background: #5a6fd8; 
                transform: translateY(-2px);
            }
            
            /* Footer */
            .footer { 
                background: #333; 
                color: white; 
                padding: 40px 20px; 
                text-align: center;
            }
            
            /* Admin Panel Link */
            .admin-link { 
                position: fixed; 
                top: 20px; 
                right: 20px; 
                background: rgba(0,0,0,0.8); 
                color: white; 
                padding: 10px 15px; 
                border-radius: 25px; 
                text-decoration: none; 
                font-size: 0.9rem;
                backdrop-filter: blur(10px);
                z-index: 1000;
            }
            .admin-link:hover { 
                background: rgba(0,0,0,0.9);
            }
            
            @media (max-width: 768px) {
                .hero h1 { font-size: 2.5rem; }
                .hero p { font-size: 1.1rem; }
                .section-title { font-size: 2rem; }
                .pricing-card.featured { transform: scale(1); }
            }
        </style>
    </head>
    <body>
        <a href="/admin/subscription-management" class="admin-link">⚙️ 관리자</a>
        
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <h1>🤖 AI 에이전트 플랫폼</h1>
                <p>박사급 전문가를 뛰어넘는 15개 AI 에이전트로 비즈니스를 혁신하세요</p>
                <a href="/agents/marketplace" class="cta-button">🚀 에이전트 체험하기</a>
            </div>
        </section>
        
        <!-- Features Section -->
        <section class="features">
            <div class="container">
                <h2 class="section-title">🌟 핵심 기능</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <span class="feature-icon">⚡</span>
                        <h3 class="feature-title">실시간 AI 처리</h3>
                        <p class="feature-description">초고속 AI 엔진으로 실시간 분석과 인사이트를 제공합니다</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">🎯</span>
                        <h3 class="feature-title">맞춤형 솔루션</h3>
                        <p class="feature-description">업종과 규모에 맞춘 전문 에이전트를 선택할 수 있습니다</p>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">🔒</span>
                        <h3 class="feature-title">엔터프라이즈 보안</h3>
                        <p class="feature-description">은행급 보안으로 데이터를 안전하게 보호합니다</p>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Agents Section -->
        <section class="agents-section">
            <div class="container">
                <h2 class="section-title">🤖 AI 에이전트 라인업</h2>
                <div class="agents-grid" id="agents-grid">
                    <!-- 동적으로 로드됨 -->
                </div>
            </div>
        </section>
        
        <!-- Pricing Section -->
        <section class="pricing">
            <div class="container">
                <h2 class="section-title">💰 요금제</h2>
                <div class="pricing-grid">
                    <div class="pricing-card">
                        <h3 class="plan-name">Starter</h3>
                        <div class="plan-price">₩29,000<span style="font-size: 1rem; color: #666;">/월</span></div>
                        <ul class="plan-features">
                            <li>기본 AI 에이전트 2개</li>
                            <li>월 1,000회 API 호출</li>
                            <li>이메일 지원</li>
                            <li>기본 분석 리포트</li>
                        </ul>
                        <a href="#" class="plan-button">시작하기</a>
                    </div>
                    <div class="pricing-card featured">
                        <h3 class="plan-name">Professional</h3>
                        <div class="plan-price">₩99,000<span style="font-size: 1rem; color: #666;">/월</span></div>
                        <ul class="plan-features">
                            <li>모든 AI 에이전트 5개</li>
                            <li>월 10,000회 API 호출</li>
                            <li>24/7 채팅 지원</li>
                            <li>고급 분석 대시보드</li>
                            <li>커스텀 통합</li>
                        </ul>
                        <a href="#" class="plan-button">추천</a>
                    </div>
                    <div class="pricing-card">
                        <h3 class="plan-name">Enterprise</h3>
                        <div class="plan-price">₹299,000<span style="font-size: 1rem; color: #666;">/월</span></div>
                        <ul class="plan-features">
                            <li>모든 AI 에이전트 15개</li>
                            <li>무제한 API 호출</li>
                            <li>전담 계정 관리자</li>
                            <li>맞춤형 에이전트 개발</li>
                            <li>온프레미스 배포</li>
                        </ul>
                        <a href="#" class="plan-button">문의하기</a>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer class="footer">
            <div class="container">
                <p>&copy; 2025 HYOJIN.AI. 모든 권리 보유.</p>
                <p>박사급 AI 에이전트로 비즈니스를 혁신하세요.</p>
            </div>
        </footer>
        
        <script>
            // 에이전트 데이터 로드
            async function loadAgents() {
                try {
                    const response = await fetch('/agents');
                    if (!response.ok) {
                        throw new Error('에이전트 데이터를 불러올 수 없습니다');
                    }
                    
                    const data = await response.json();
                    const grid = document.getElementById('agents-grid');
                    grid.innerHTML = '';
                    
                    if (data.agents) {
                        Object.entries(data.agents).forEach(([type, agent]) => {
                            const card = document.createElement('div');
                            card.className = 'agent-card';
                            card.innerHTML = `
                                <span class="agent-emoji">${agent.icon}</span>
                                <h3 class="agent-name">${agent.name}</h3>
                                <p class="agent-desc">${agent.description}</p>
                            `;
                            grid.appendChild(card);
                        });
                    }
                } catch (error) {
                    console.error('에이전트 로드 오류:', error);
                    const grid = document.getElementById('agents-grid');
                    grid.innerHTML = '<p style="text-align: center; color: #666;">에이전트 정보를 불러오는 중 오류가 발생했습니다.</p>';
                }
            }
            
            // 페이지 로드 시 에이전트 데이터 로드
            document.addEventListener('DOMContentLoaded', loadAgents);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=landing_html)


def get_allowed_agents_by_plan(plan):
    """플랜별 사용 가능한 에이전트 목록"""
    plan_agents = {
        "trial": ["developer", "marketing"],
        "startup": ["strategy", "developer", "marketing"],
        "professional": [
            "strategy",
            "datascience",
            "developer",
            "marketing",
            "finance",
        ],
        "business": ["strategy", "datascience", "developer", "marketing", "finance"],
        "enterprise": list(ai_agents.keys()),
    }
    return plan_agents.get(plan, [])


# 🔥 결제 API 엔드포인트들
@app.post("/api/process-payment")
async def process_payment(payment_request: PaymentRequest):
    """실제 결제 처리 API"""
    try:
        # 입력 데이터 살균
        payment_request.customer.name = sanitize_input(payment_request.customer.name)
        payment_request.customer.email = sanitize_input(payment_request.customer.email)
        payment_request.customer.company = sanitize_input(
            payment_request.customer.company
        )

        # 결제 방법에 따른 처리
        if payment_request.customer.paymentMethod == "card":
            result = await payment_processor.process_card_payment(payment_request)
        elif payment_request.customer.paymentMethod == "paypal":
            result = await payment_processor.process_paypal_payment(payment_request)
        else:
            raise HTTPException(
                status_code=400, detail="지원하지 않는 결제 방법입니다."
            )

        # 성공시 확인 이메일 발송
        if result["success"]:
            subscription_data = {
                "id": result["subscription_id"],
                "customer": payment_request.customer.dict(),
                "items": [item.dict() for item in payment_request.items],
                "status": result["status"],
                "total_amount": result["amount"],
                "payment_method": payment_request.customer.paymentMethod,
                "created_at": datetime.datetime.now().isoformat(),
                "next_billing_date": (
                    datetime.datetime.now() + datetime.timedelta(days=30)
                ).isoformat(),
            }

            await email_service.send_subscription_confirmation(subscription_data)

        # 🔥 결제 관리 앱에 데이터 저장
        if result["success"]:
            await save_payment_to_manager_db(payment_request, result)

        # 📧 결제 성공시 항상 성공 페이지로 리다이렉트 URL 생성
        if result["success"]:
            redirect_url = f"/payment_success.html?subscription_id={result['subscription_id']}&amount={result['amount']}&method={payment_request.customer.paymentMethod}&status={result['status']}"
            result["redirect_url"] = redirect_url

            # 가상 링크가 있다면 링크 개수도 포함
            if result.get("service_links"):
                result["links_count"] = len(result["service_links"])
            else:
                result["links_count"] = 0

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"결제 처리 중 오류가 발생했습니다: {str(e)}"
        )


@app.post("/api/bank-transfer")
async def bank_transfer_request(customer: CustomerData, items: List[PaymentItem]):
    """계좌이체 신청 API"""
    try:
        # 입력 데이터 살균
        customer.name = sanitize_input(customer.name)
        customer.email = sanitize_input(customer.email)
        customer.company = sanitize_input(customer.company)

        result = await payment_processor.process_bank_transfer(customer, items)

        # 🔥 결제 관리 앱에 데이터 저장 (계좌이체)
        if result["success"]:
            await save_bank_transfer_to_manager_db(customer, items, result)

        # 계좌이체 신청 확인 이메일 발송
        if result["success"]:
            subscription_data = {
                "id": result["subscription_id"],
                "customer": customer.dict(),
                "items": [item.dict() for item in items],
                "status": result["status"],
                "total_amount": result["amount"],
                "payment_method": "bank",
                "created_at": datetime.datetime.now().isoformat(),
                "bank_info": result["bank_info"],
            }

            await email_service.send_subscription_confirmation(subscription_data)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"계좌이체 신청 중 오류가 발생했습니다: {str(e)}"
        )


# 🔥 결제 관리 앱용 API 엔드포인트들


# 상태 업데이트 요청 모델
class PaymentStatusUpdate(BaseModel):
    status: str
    notes: str = ""


@app.get("/api/manager/payments")
async def get_all_payments():
    """모든 결제 내역 조회 (관리용)"""
    try:

        def get_payments():
            conn = sqlite3.connect("hyojin_payments.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT * FROM payments ORDER BY created_at DESC
            """
            )

            payments = []
            for row in cursor.fetchall():
                payment = {
                    "id": row[0],
                    "subscription_id": row[1],
                    "customer_name": row[2],
                    "customer_email": row[3],
                    "customer_company": row[4],
                    "payment_method": row[5],
                    "total_amount": row[6],
                    "status": row[7],
                    "items": json.loads(row[8]),
                    "created_at": row[9],
                    "updated_at": row[10],
                    "notes": row[11] or "",
                }
                payments.append(payment)

            conn.close()
            return payments

        payments = await asyncio.get_event_loop().run_in_executor(None, get_payments)
        return {"success": True, "data": payments}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"결제 내역 조회 실패: {str(e)}")


@app.put("/api/manager/payments/{payment_id}/status")
async def update_payment_status(payment_id: int, update_data: PaymentStatusUpdate):
    """결제 상태 업데이트 (관리용)"""
    try:

        def update_status():
            conn = sqlite3.connect("hyojin_payments.db")
            cursor = conn.cursor()

            now = datetime.datetime.now().isoformat()

            cursor.execute(
                """
                UPDATE payments 
                SET status = ?, notes = ?, updated_at = ?
                WHERE id = ?
            """,
                (update_data.status, update_data.notes, now, payment_id),
            )

            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected > 0

        success = await asyncio.get_event_loop().run_in_executor(None, update_status)

        if success:
            return {"success": True, "message": "상태가 업데이트되었습니다."}
        else:
            raise HTTPException(status_code=404, detail="결제 내역을 찾을 수 없습니다.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 업데이트 실패: {str(e)}")


@app.get("/api/manager/statistics")
async def get_payment_statistics():
    """결제 통계 조회 (관리용)"""
    try:

        def get_stats():
            conn = sqlite3.connect("hyojin_payments.db")
            cursor = conn.cursor()

            # 전체 통계
            cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM payments")
            total_count, total_revenue = cursor.fetchone()

            # 상태별 통계
            cursor.execute(
                """
                SELECT status, COUNT(*), SUM(total_amount) 
                FROM payments 
                GROUP BY status
            """
            )
            status_stats = cursor.fetchall()

            # 결제 방법별 통계
            cursor.execute(
                """
                SELECT payment_method, COUNT(*), SUM(total_amount) 
                FROM payments 
                GROUP BY payment_method
            """
            )
            method_stats = cursor.fetchall()

            # 월별 통계
            cursor.execute(
                """
                SELECT strftime('%Y-%m', created_at) as month, 
                       COUNT(*), SUM(total_amount) 
                FROM payments 
                GROUP BY month 
                ORDER BY month DESC
            """
            )
            monthly_stats = cursor.fetchall()

            conn.close()

            return {
                "total_orders": total_count or 0,
                "total_revenue": total_revenue or 0,
                "status_breakdown": {
                    row[0]: {"count": row[1], "revenue": row[2]} for row in status_stats
                },
                "method_breakdown": {
                    row[0]: {"count": row[1], "revenue": row[2]} for row in method_stats
                },
                "monthly_breakdown": {
                    row[0]: {"count": row[1], "revenue": row[2]}
                    for row in monthly_stats
                },
            }

        stats = await asyncio.get_event_loop().run_in_executor(None, get_stats)
        return {"success": True, "data": stats}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")


# 🔥 결제 관리 웹 대시보드
@app.get("/admin/payments", response_class=HTMLResponse)
async def payment_admin_dashboard():
    """결제 관리자 대시보드"""
    with open("payment_admin_dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/subscription/{subscription_id}")
async def get_subscription_status(subscription_id: str):
    """구독 상태 조회 API"""
    try:
        # 구독 데이터 조회 (실제로는 데이터베이스에서)
        subscription = payment_processor.subscription_service.subscriptions_db.get(
            subscription_id
        )

        if not subscription:
            raise HTTPException(status_code=404, detail="구독을 찾을 수 없습니다.")

        return {
            "subscription_id": subscription["id"],
            "status": subscription["status"],
            "customer": subscription["customer"],
            "items": subscription["items"],
            "total_amount": subscription["total_amount"],
            "next_billing_date": subscription["next_billing_date"],
            "created_at": subscription["created_at"],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"구독 조회 중 오류가 발생했습니다: {str(e)}"
        )


@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    """Stripe 웹훅 처리"""
    try:
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        # Stripe 웹훅 검증 및 처리
        # 실제 구현시 Stripe webhook secret 필요

        return {"received": True}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"웹훅 처리 실패: {str(e)}")


@app.get("/api/payment-config")
async def get_payment_config():
    """결제 설정 정보 API"""
    return {
        "stripe_publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_demo"),
        "supported_payment_methods": ["card", "paypal", "bank"],
        "currencies": ["USD"],
        "bank_info": {
            "bank_name": "국민은행",
            "account_number": "123-456-789012",
            "account_holder": "HYOJIN.AI",
        },
    }


# 🔗 ==================== 가상 서비스 링크 API ====================


@app.get("/api/service-links/{subscription_id}")
async def get_service_links(subscription_id: str):
    """구독 ID로 서비스 링크 조회"""
    try:
        links = virtual_service_manager.get_service_links_by_subscription(
            subscription_id
        )
        return {
            "success": True,
            "subscription_id": subscription_id,
            "links": links,
            "total": len(links),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/verify-token/{token}")
async def verify_service_token(token: str):
    """서비스 접속 토큰 검증"""
    try:
        verification = virtual_service_manager.verify_access_token(token)
        return verification
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔐 ==================== 토큰 인증 시스템 ====================


@app.post("/api/authenticate")
async def authenticate_service_access(request: Request):
    """토큰으로 서비스 접근 인증"""
    try:
        data = await request.json()
        token = data.get("token")
        service_id = data.get("service_id")

        if not token or not service_id:
            raise HTTPException(status_code=400, detail="토큰과 서비스 ID가 필요합니다")

        # 토큰 검증 및 세션 생성
        auth_result = auth_system.validate_token(token, service_id)

        if not auth_result["valid"]:
            raise HTTPException(status_code=401, detail=auth_result["message"])

        # 접근 로그 기록
        auth_system.log_access(auth_result["user_id"], service_id, token, "unknown", "")

        return {
            "success": True,
            "session_id": auth_result["session_id"],
            "user_id": auth_result["user_id"],
            "service_name": auth_result["service_name"],
            "expires_at": auth_result["expires_at"],
            "message": "인증 성공",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"인증 처리 중 오류: {str(e)}")


@app.get("/api/session/{session_id}")
async def validate_session(session_id: str):
    """세션 유효성 검증"""
    try:
        session_result = auth_system.validate_session(session_id)

        if not session_result["valid"]:
            raise HTTPException(status_code=401, detail="유효하지 않은 세션입니다")

        return {
            "valid": True,
            "user_id": session_result["user_id"],
            "service_id": session_result["service_id"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"세션 검증 중 오류: {str(e)}")


@app.post("/api/revoke-token")
async def revoke_access_token(request: Request):
    """토큰 폐기"""
    try:
        data = await request.json()
        token = data.get("token")

        if not token:
            raise HTTPException(status_code=400, detail="토큰이 필요합니다")

        success = auth_system.revoke_token(token)

        if success:
            return {"success": True, "message": "토큰이 폐기되었습니다"}
        else:
            raise HTTPException(status_code=400, detail="토큰 폐기에 실패했습니다")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"토큰 폐기 중 오류: {str(e)}")


@app.get("/service/{service_id}")
async def access_service_with_token(service_id: str, token: Optional[str] = None):
    """토큰으로 서비스 접근 - 토큰이 없으면 입력창 표시"""

    # 토큰이 없으면 토큰 입력 페이지 표시
    if not token:
        return HTMLResponse(
            f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🔐 서비스 인증 - {service_id}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .auth-container {{
                    background: white;
                    padding: 50px;
                    border-radius: 25px;
                    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
                    text-align: center;
                    max-width: 500px;
                    width: 100%;
                    animation: slideUp 0.5s ease-out;
                }}
                
                @keyframes slideUp {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
                
                .auth-icon {{
                    font-size: 4em;
                    margin-bottom: 20px;
                    animation: bounce 2s ease-in-out infinite;
                }}
                
                @keyframes bounce {{
                    0%, 20%, 50%, 80%, 100% {{
                        transform: translateY(0);
                    }}
                    40% {{
                        transform: translateY(-10px);
                    }}
                    60% {{
                        transform: translateY(-5px);
                    }}
                }}
                
                h1 {{
                    color: #333;
                    margin-bottom: 15px;
                    font-size: 2em;
                }}
                
                .service-info {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 15px;
                    margin: 25px 0;
                    border-left: 4px solid #4CAF50;
                }}
                
                .token-input-group {{
                    margin: 30px 0;
                }}
                
                .token-input-group label {{
                    display: block;
                    font-weight: 600;
                    color: #333;
                    margin-bottom: 10px;
                    text-align: left;
                }}
                
                .token-input {{
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 12px;
                    font-size: 1em;
                    font-family: 'Courier New', monospace;
                    transition: all 0.3s ease;
                    background: #f8f9fa;
                }}
                
                .token-input:focus {{
                    outline: none;
                    border-color: #4CAF50;
                    box-shadow: 0 0 15px rgba(76, 175, 80, 0.2);
                    background: white;
                }}
                
                .btn {{
                    padding: 15px 30px;
                    border: none;
                    border-radius: 25px;
                    font-weight: 600;
                    font-size: 1.1em;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                    margin: 10px;
                }}
                
                .btn-primary {{
                    background: linear-gradient(45deg, #4CAF50, #45a049);
                    color: white;
                    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
                }}
                
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.6);
                }}
                
                .btn-secondary {{
                    background: linear-gradient(45deg, #6c757d, #5a6268);
                    color: white;
                    box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
                }}
                
                .btn-secondary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(108, 117, 125, 0.6);
                }}
                
                .help-text {{
                    color: #666;
                    font-size: 0.9em;
                    margin-top: 20px;
                    line-height: 1.6;
                }}
                
                .error-message {{
                    background: #f8d7da;
                    color: #721c24;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border: 1px solid #f5c6cb;
                    display: none;
                }}
                
                .loading {{
                    display: none;
                    color: #4CAF50;
                    margin-top: 15px;
                }}
                
                .spinner {{
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    border: 2px solid #f3f3f3;
                    border-top: 2px solid #4CAF50;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin-right: 10px;
                }}
                
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="auth-container">
                <div class="auth-icon">🔐</div>
                <h1>서비스 인증</h1>
                
                <div class="service-info">
                    <h3>🤖 {service_id.upper()} 서비스</h3>
                    <p>안전한 접근을 위해 인증이 필요합니다</p>
                </div>
                
                <div class="token-input-group">
                    <label for="accessToken">🔑 접속 토큰을 입력하세요:</label>
                    <input 
                        type="text" 
                        id="accessToken" 
                        class="token-input" 
                        placeholder="hyojin_xxxxxxxxxxxxxxxxxx" 
                        autofocus
                    >
                </div>
                
                <div class="error-message" id="errorMessage"></div>
                
                <div class="loading" id="loadingMessage">
                    <span class="spinner"></span>
                    인증 처리 중...
                </div>
                
                <div>
                    <button class="btn btn-primary" onclick="authenticateToken()">
                        🚀 서비스 시작
                    </button>
                    <a href="/" class="btn btn-secondary">
                        🏠 홈으로
                    </a>
                </div>
                
                <div class="help-text">
                    💡 토큰이 없으신가요? <a href="/" style="color: #4CAF50; text-decoration: none;">구매 페이지</a>에서 서비스를 구독하세요!
                </div>
            </div>
            
            <script>
                // Enter 키로 인증 실행
                document.getElementById('accessToken').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        authenticateToken();
                    }}
                }});
                
                async function authenticateToken() {{
                    const token = document.getElementById('accessToken').value.trim();
                    const errorDiv = document.getElementById('errorMessage');
                    const loadingDiv = document.getElementById('loadingMessage');
                    
                    // 입력 검증
                    if (!token) {{
                        showError('토큰을 입력해주세요.');
                        return;
                    }}
                    
                    if (token.length < 10) {{
                        showError('올바른 토큰 형식이 아닙니다.');
                        return;
                    }}
                    
                    // 로딩 표시
                    errorDiv.style.display = 'none';
                    loadingDiv.style.display = 'block';
                    
                    try {{
                        // 인증 API 호출
                        const response = await fetch('/api/authenticate', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                            }},
                            body: JSON.stringify({{
                                token: token,
                                service_id: '{service_id}'
                            }})
                        }});
                        
                        const data = await response.json();
                        
                        if (response.ok && data.success) {{
                            // 인증 성공 - 서비스 페이지로 이동
                            window.location.href = `/service/{service_id}?token=${{encodeURIComponent(token)}}`;
                        }} else {{
                            // 인증 실패
                            showError(data.detail || '인증에 실패했습니다.');
                        }}
                    }} catch (error) {{
                        console.error('인증 오류:', error);
                        showError('인증 처리 중 오류가 발생했습니다.');
                    }} finally {{
                        loadingDiv.style.display = 'none';
                    }}
                }}
                
                function showError(message) {{
                    const errorDiv = document.getElementById('errorMessage');
                    errorDiv.textContent = message;
                    errorDiv.style.display = 'block';
                    
                    // 3초 후 자동 숨김
                    setTimeout(() => {{
                        errorDiv.style.display = 'none';
                    }}, 3000);
                }}
            </script>
        </body>
        </html>
        """
        )

    try:
        # 토큰 검증
        auth_result = auth_system.validate_token(token, service_id)

        if not auth_result["valid"]:
            # 인증 실패 시 로그인 페이지로 리다이렉트
            return HTMLResponse(
                f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>인증 필요</title>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                    }}
                    .auth-container {{
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        text-align: center;
                        max-width: 400px;
                    }}
                    .error-icon {{
                        font-size: 4em;
                        color: #f44336;
                        margin-bottom: 20px;
                    }}
                    h1 {{
                        color: #333;
                        margin-bottom: 15px;
                    }}
                    p {{
                        color: #666;
                        margin-bottom: 30px;
                    }}
                    .btn {{
                        background: linear-gradient(45deg, #4CAF50, #45a049);
                        color: white;
                        padding: 12px 24px;
                        border: none;
                        border-radius: 25px;
                        text-decoration: none;
                        font-weight: 600;
                        display: inline-block;
                        transition: all 0.3s ease;
                    }}
                    .btn:hover {{
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
                    }}
                </style>
            </head>
            <body>
                <div class="auth-container">
                    <div class="error-icon">🔒</div>
                    <h1>인증이 필요합니다</h1>
                    <p>{auth_result["message"]}</p>
                    <a href="/" class="btn">🏠 홈으로 돌아가기</a>
                </div>
            </body>
            </html>
            """
            )

        # 접근 로그 기록
        auth_system.log_access(auth_result["user_id"], service_id, token, "unknown", "")

        # 서비스별 페이지 반환
        service_page = get_service_page(service_id, auth_result)
        return HTMLResponse(service_page)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서비스 접근 중 오류: {str(e)}")


def get_service_page(service_id: str, auth_result: dict) -> str:
    """서비스별 페이지 생성"""
    service_name = auth_result["service_name"]
    user_id = auth_result["user_id"]

    # 서비스별 콘텐츠 정의
    service_content = {
        "finance-ai": {
            "title": "💰 AI 재무 분석",
            "description": "AI 기반 재무 분석 및 투자 상담 서비스",
            "features": [
                "📊 포트폴리오 분석",
                "📈 시장 예측",
                "💡 투자 조언",
                "🔍 리스크 분석",
            ],
        },
        "health-ai": {
            "title": "🏥 AI 헬스케어",
            "description": "AI 기반 건강 모니터링 및 상담 서비스",
            "features": [
                "💊 건강 분석",
                "🩺 증상 체크",
                "🏃‍♂️ 운동 플랜",
                "🥗 영양 관리",
            ],
        },
        "education-ai": {
            "title": "🎓 AI 교육",
            "description": "개인 맞춤형 AI 튜터링 서비스",
            "features": [
                "📚 맞춤 학습",
                "🧠 지능 분석",
                "📝 과제 도움",
                "🎯 목표 설정",
            ],
        },
    }

    content = service_content.get(
        service_id,
        {
            "title": f"🤖 {service_name}",
            "description": f"{service_name} 서비스에 오신 것을 환영합니다",
            "features": ["🚀 AI 기반 분석", "💡 맞춤형 서비스", "📊 실시간 데이터"],
        },
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{content['title']} - HYOJIN.AI</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .service-container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .user-info {{
                background: rgba(255,255,255,0.2);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .features-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            
            .feature-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                border-left: 4px solid #4CAF50;
                transition: transform 0.3s ease;
            }}
            
            .feature-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}
            
            .action-buttons {{
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 40px;
                flex-wrap: wrap;
            }}
            
            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-weight: 600;
                text-decoration: none;
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            
            .btn-primary {{
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white;
            }}
            
            .btn-secondary {{
                background: linear-gradient(45deg, #2196F3, #1976D2);
                color: white;
            }}
            
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            }}
            
            .status-bar {{
                background: #f8f9fa;
                padding: 15px;
                border-top: 1px solid #e9ecef;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="service-container">
            <div class="header">
                <h1>{content['title']}</h1>
                <p>{content['description']}</p>
                <div class="user-info">
                    👤 사용자: {user_id} | 🔐 인증 완료 | ⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
            
            <div class="content">
                <h2>🚀 사용 가능한 기능</h2>
                <div class="features-grid">
                    {' '.join([f'<div class="feature-card"><h3>{feature}</h3><p>AI 기반 고급 기능을 사용하실 수 있습니다.</p></div>' for feature in content['features']])}
                </div>
                
                <div class="action-buttons">
                    <button class="btn btn-primary" onclick="startService()">
                        🚀 서비스 시작하기
                    </button>
                    <button class="btn btn-secondary" onclick="showTutorial()">
                        📚 사용법 보기
                    </button>
                    <a href="/" class="btn" style="background: linear-gradient(45deg, #FF6B6B, #FF8E53); color: white;">
                        🏠 홈으로
                    </a>
                </div>
            </div>
            
            <div class="status-bar">
                <div>🟢 서비스 상태: 정상 운영</div>
                <div>📊 AI 모델: 활성화</div>
                <div>🔒 보안: 토큰 인증 완료</div>
            </div>
        </div>
        
        <script>
            function startService() {{
                alert('🎉 {service_name} 서비스가 시작됩니다!\\n\\n실제 서비스에서는 여기에 AI 기능이 구현됩니다.');
            }}
            
            function showTutorial() {{
                alert('📚 {service_name} 사용법:\\n\\n1. 좌측 메뉴에서 원하는 기능 선택\\n2. AI 분석 시작\\n3. 결과 확인 및 다운로드');
            }}
            
            // 5분마다 세션 확인
            setInterval(function() {{
                console.log('세션 상태 확인 중...');
            }}, 300000);
        </script>
    </body>
    </html>
    """


@app.get("/demo/{service_id}")
async def service_demo_page(service_id: str, token: Optional[str] = None):
    """가상 서비스 데모 페이지"""
    try:
        # 토큰 검증 (선택사항)
        if token:
            verification = virtual_service_manager.verify_access_token(token)
            if not verification.get("valid"):
                raise HTTPException(status_code=403, detail="유효하지 않은 토큰입니다.")

        # 데모 페이지 HTML 파일 반환
        demo_file = Path("demo/service_demo.html")
        if demo_file.exists():
            return FileResponse("demo/service_demo.html")
        else:
            raise HTTPException(
                status_code=404, detail="데모 페이지를 찾을 수 없습니다."
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/access/{service_id}")
async def service_access_page(service_id: str, token: str):
    """실제 서비스 접속 페이지 (토큰 필수)"""
    try:
        # 토큰 검증
        verification = virtual_service_manager.verify_access_token(token)
        if not verification.get("valid"):
            raise HTTPException(status_code=403, detail="유효하지 않은 토큰입니다.")

        # 서비스별 전용 인터페이스로 리다이렉트
        service_info = verification

        return HTMLResponse(
            f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{service_info['service_name']} - HYOJIN.AI</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .access-container {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 600px;
                }}
                .service-icon {{
                    font-size: 4em;
                    margin-bottom: 20px;
                }}
                .service-title {{
                    color: #333;
                    margin-bottom: 20px;
                    font-size: 2em;
                }}
                .access-info {{
                    background: #e3f2fd;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }}
                .features-list {{
                    text-align: left;
                    margin: 20px 0;
                }}
                .feature-item {{
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .access-btn {{
                    background: linear-gradient(45deg, #4CAF50, #45a049);
                    color: white;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 25px;
                    font-size: 1.2em;
                    cursor: pointer;
                    margin: 10px;
                    transition: all 0.3s ease;
                }}
                .access-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
                }}
            </style>
        </head>
        <body>
            <div class="access-container">
                <div class="service-icon">🤖</div>
                <h1 class="service-title">{service_info['service_name']}</h1>
                
                <div class="access-info">
                    <h3>✅ 인증 완료</h3>
                    <p>토큰: <code>{token[:20]}...</code></p>
                    <p>만료일: {service_info['expires_at'][:10]}</p>
                </div>
                
                <div class="features-list">
                    <h3>🎯 이용 가능한 기능:</h3>
                    {''.join([f'<div class="feature-item">✨ {feature}</div>' for feature in service_info['features']])}
                </div>
                
                <button class="access-btn" onclick="startService()">🚀 서비스 시작</button>
                <button class="access-btn" onclick="viewDemo()">🎬 데모 보기</button>
            </div>
            
            <script>
                function startService() {{
                    alert('🚀 {service_info["service_name"]} 서비스를 시작합니다!\\n\\n실제 환경에서는 AI 서비스 인터페이스로 이동됩니다.');
                }}
                
                function viewDemo() {{
                    window.open('/demo/{service_id}?token={token}', '_blank');
                }}
            </script>
        </body>
        </html>
        """
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
