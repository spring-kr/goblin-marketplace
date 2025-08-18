"""
🚀 HYOJIN.AI MVP - 12개 도메인 완전체 + 구독관리회사시스템 통합
한방에 모든 AI 도메인 구현 + 엔터프라이즈 구독관리!
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import datetime
import json
import random
import os
import uuid
from pathlib import Path

# FastAPI 앱 생성
app = FastAPI(
    title="Hyojin AI MVP + Subscription Management",
    description="12개 AI 비즈니스 도메인 + 엔터프라이즈 구독관리 시스템",
    version="2.0.0",
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# AI 에이전트 저장소 데이터
ai_agents = {
    "strategy": {
        "name": "Strategy Agent",
        "description": "McKinsey 컨설턴트 수준의 전략 기획, 시장 분석, 비즈니스 모델 설계",
        "capabilities": ["전략기획", "시장분석", "경쟁분석"],
        "autonomy_score": 95,
        "tier": "premium",
        "icon": "🔬",
    },
    "datascience": {
        "name": "DataScience Agent",
        "description": "Google AI 연구원 수준의 데이터 분석, ML 모델링, 예측 알고리즘 개발",
        "capabilities": ["데이터분석", "ML모델링", "예측분석"],
        "autonomy_score": 92,
        "tier": "premium",
        "icon": "💻",
    },
    "developer": {
        "name": "Developer Agent",
        "description": "Meta, Google 시니어 개발자 수준의 풀스택 개발, 아키텍처 설계",
        "capabilities": ["풀스택개발", "아키텍처", "코드리뷰"],
        "autonomy_score": 89,
        "tier": "standard",
        "icon": "🎯",
    },
    "marketing": {
        "name": "Marketing Agent",
        "description": "Netflix, Apple CMO 수준의 브랜딩, 캠페인 기획, 성과 최적화",
        "capabilities": ["브랜딩", "캠페인기획", "성과최적화"],
        "autonomy_score": 87,
        "tier": "standard",
        "icon": "💰",
    },
    "finance": {
        "name": "Finance Agent",
        "description": "Goldman Sachs 애널리스트 수준의 투자 분석, 리스크 관리, 포트폴리오 최적화",
        "capabilities": ["투자분석", "리스크관리", "포트폴리오"],
        "autonomy_score": 94,
        "tier": "enterprise",
        "icon": "✨",
        "status": "coming_soon",
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
@app.get("/")
async def root():
    """메인 페이지"""
    return {
        "message": "Hyojin AI MVP API",
        "status": "running",
        "domains": len(DOMAINS),
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.datetime.now().isoformat(),
    }


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
async def predict_simple(domain: str, text: str):
    """데모용 무료 예측 엔드포인트 (제한된 기능)"""
    if domain not in DOMAINS:
        raise HTTPException(status_code=404, detail=f"Domain '{domain}' not found")

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
async def get_subscription_management_dashboard():
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
async def update_subscription(request: SubscriptionUpdateRequest):
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
async def manage_domain(request: DomainManagementRequest):
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
async def get_domain_analytics(domain: str):
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
async def user_management(request: UserManagementRequest):
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
async def financial_analysis(request: FinancialAnalysisRequest):
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
async def get_system_status():
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


@app.get("/agents/marketplace")
async def get_agent_marketplace():
    """AI 에이전트 마켓플레이스 HTML 반환"""
    marketplace_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HYOJIN.AI 에이전트 마켓플레이스</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .header { text-align: center; padding: 50px 20px; color: white; }
            .header h1 { font-size: 3rem; margin-bottom: 20px; }
            .header p { font-size: 1.2rem; opacity: 0.9; }
            .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
            .agents-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; margin-bottom: 50px; }
            .agent-card { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; }
            .agent-card:hover { transform: translateY(-10px); }
            .agent-icon { font-size: 3rem; margin-bottom: 20px; text-align: center; }
            .agent-name { font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; color: #667eea; text-align: center; }
            .agent-description { line-height: 1.6; margin-bottom: 20px; opacity: 0.9; text-align: center; }
            .capabilities { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; justify-content: center; }
            .capability-tag { background: rgba(102, 126, 234, 0.2); color: #667eea; padding: 4px 12px; border-radius: 15px; font-size: 0.9rem; }
            .deploy-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 25px; border-radius: 25px; cursor: pointer; font-weight: bold; width: 100%; }
            .deploy-btn:hover { transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 AI 에이전트 마켓플레이스</h1>
            <p>박사급 전문가를 넘어서는 15가지 AI 에이전트</p>
        </div>
        
        <div class="container">
            <div class="agents-grid" id="agents-grid">
                <!-- 동적으로 로드됨 -->
            </div>
        </div>
        
        <script>
            async function loadAgents() {
                try {
                    const response = await fetch('/agents');
                    const data = await response.json();
                    
                    const grid = document.getElementById('agents-grid');
                    grid.innerHTML = '';
                    
                    Object.entries(data.agents).forEach(([type, agent]) => {
                        const card = document.createElement('div');
                        card.className = 'agent-card';
                        
                        card.innerHTML = `
                            <div class="agent-icon">${agent.icon}</div>
                            <div class="agent-name">${agent.name}</div>
                            <div class="agent-description">${agent.description}</div>
                            <div class="capabilities">
                                ${agent.capabilities.map(cap => `<span class="capability-tag">${cap}</span>`).join('')}
                            </div>
                            <button class="deploy-btn" onclick="deployAgent('${type}')">🚀 에이전트 배포</button>
                        `;
                        
                        grid.appendChild(card);
                    });
                } catch (error) {
                    console.error('에이전트 로드 오류:', error);
                }
            }
            
            async function deployAgent(agentType) {
                alert(`${agentType} 에이전트 배포 요청이 접수되었습니다!`);
            }
            
            document.addEventListener('DOMContentLoaded', loadAgents);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=marketplace_html)


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


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
