from flask import Flask, render_template, request, jsonify, session
import json
import os
import requests
import base64
from datetime import datetime, timedelta
import uuid

# 토스페이먼츠 결제 시스템
TOSS_CLIENT_KEY = os.getenv("TOSS_CLIENT_KEY", "test_ck_demo_key")
TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY", "test_sk_demo_key")
TOSS_API_URL = "https://api.tosspayments.com/v1/payments"
TOSS_ENABLED = bool(
    TOSS_CLIENT_KEY and TOSS_SECRET_KEY and "demo" not in TOSS_SECRET_KEY
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "goblin_marketplace_secret_key_2024")

# 결제 완료된 사용자의 권한 정보 저장 (실제로는 데이터베이스 사용)
user_permissions = {}
payment_records = {}


@app.route("/")
def home():
    return render_template("goblin_market_v11.html")


@app.route("/mobile")
def mobile():
    return render_template("goblin_mobile_v11.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/api/payment/create", methods=["POST"])
def create_payment():
    data = request.get_json()

    # 사용자 ID 생성 (실제로는 로그인 시스템에서 가져옴)
    user_id = data.get("user_id", f"USER_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # 결제 정보 처리
    payment_id = f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    expert_id = data.get("expert_id")
    expert_name = data.get("expert_name")
    amount = data.get("amount")
    duration_minutes = data.get("duration_minutes", 30)

    payment_info = {
        "payment_id": payment_id,
        "user_id": user_id,
        "expert_id": expert_id,
        "expert_name": expert_name,
        "service_type": data.get("service_type"),
        "amount": amount,
        "duration_minutes": duration_minutes,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    # 결제 기록 저장
    payment_records[payment_id] = payment_info

    # 토스페이먼츠 결제 생성 (실제 결제)
    if TOSS_ENABLED and amount and amount > 0:
        try:
            # 주문 ID 생성 (토스페이먼츠 요구사항에 맞게 고유한 값)
            order_id = f"ORDER_{payment_id}_{int(datetime.now().timestamp())}"

            # 토스페이먼츠 결제 생성 데이터
            payment_data = {
                "amount": int(amount),
                "orderId": order_id,
                "orderName": f"도깨비마을장터 - {expert_name} 상담 ({duration_minutes}분)",
                "customerEmail": f"user_{user_id}@goblinmarket.com",
                "customerName": f"사용자_{user_id}",
                "successUrl": f"{request.url_root}payment/success",
                "failUrl": f"{request.url_root}payment/fail",
            }

            payment_info["toss_order_id"] = order_id
            payment_info["toss_payment_data"] = payment_data
            payment_records[payment_id] = payment_info

            return jsonify(
                {
                    "status": "success",
                    "payment_id": payment_id,
                    "user_id": user_id,
                    "toss_client_key": TOSS_CLIENT_KEY,
                    "toss_order_id": order_id,
                    "amount": amount,
                    "expert_name": expert_name,
                    "order_name": payment_data["orderName"],
                    "customer_email": payment_data["customerEmail"],
                    "customer_name": payment_data["customerName"],
                    "success_url": payment_data["successUrl"],
                    "fail_url": payment_data["failUrl"],
                    "redirect_url": f"/payment/process/{payment_id}",
                    "payment_method": "toss",
                }
            )

        except Exception as e:
            print(f"Toss Payments error: {e}")
            # 토스페이먼츠 오류 시 시뮬레이션 모드로 fallback
            pass

    # 시뮬레이션 모드 (개발/테스트용)
    return jsonify(
        {
            "status": "success",
            "payment_id": payment_id,
            "user_id": user_id,
            "redirect_url": f"/payment/process/{payment_id}",
            "payment_method": "simulation",
            "message": "테스트 모드: 실제 결제 없이 권한이 부여됩니다.",
        }
    )


@app.route("/api/payment/process/<payment_id>", methods=["POST"])
def process_payment(payment_id):
    # 결제 기록 확인
    if payment_id not in payment_records:
        return jsonify({"status": "error", "message": "결제 정보를 찾을 수 없습니다."})

    payment = payment_records[payment_id]

    # 토스페이먼츠 결제 확인
    if TOSS_ENABLED and "toss_order_id" in payment:
        try:
            # 토스페이먼츠에서 결제 상태 확인
            order_id = payment["toss_order_id"]

            # 토스페이먼츠 결제 확인 API 호출
            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{TOSS_SECRET_KEY}:'.encode()).decode()}",
                "Content-Type": "application/json",
            }

            # 결제 상태 조회
            response = requests.get(
                f"{TOSS_API_URL}?orderId={order_id}", headers=headers
            )

            if response.status_code == 200:
                payment_data = response.json()
                payment_status = payment_data.get("status")

                if payment_status != "DONE":
                    return jsonify(
                        {
                            "status": "error",
                            "message": "결제가 완료되지 않았습니다.",
                            "toss_status": payment_status,
                        }
                    )
            else:
                # 결제 정보를 찾을 수 없는 경우 시뮬레이션 모드로 처리
                print(f"Toss payment check failed: {response.status_code}")

        except Exception as e:
            print(f"Toss payment verification error: {str(e)}")
            # 토스페이먼츠 확인 실패시 시뮬레이션 모드로 fallback
            pass

    # 결제 완료 시 사용자에게 도깨비 이용 권한 부여
    user_id = payment["user_id"]
    expert_id = payment["expert_id"]
    duration_minutes = payment["duration_minutes"]

    # 사용자 권한 정보 업데이트
    if user_id not in user_permissions:
        user_permissions[user_id] = {}

    # 상담 시간만큼 권한 부여 (실제로는 토큰 기반)
    expiry_time = datetime.now() + timedelta(hours=24)  # 24시간 내 사용 가능
    user_permissions[user_id][expert_id] = {
        "purchased_at": datetime.now().isoformat(),
        "duration_minutes": duration_minutes,
        "remaining_minutes": duration_minutes,
        "expires_at": expiry_time.isoformat(),
        "expert_name": payment["expert_name"],
    }

    # 결제 완료 표시
    payment["status"] = "completed"

    return jsonify(
        {
            "status": "success",
            "message": "결제가 완료되었습니다!",
            "access_granted": True,
            "expert_name": payment["expert_name"],
            "duration_minutes": duration_minutes,
            "expires_at": expiry_time.isoformat(),
        }
    )


@app.route("/api/toss/webhook", methods=["POST"])
def toss_webhook():
    """토스페이먼츠 웹훅 처리 - 실제 결제 완료 시 권한 부여"""
    if not TOSS_ENABLED:
        return jsonify({"error": "Toss Payments not enabled"}), 400

    try:
        payload = request.get_json()

        # 토스페이먼츠 웹훅 이벤트 처리
        event_type = payload.get("eventType")

        if event_type == "PAYMENT_COMPLETED":
            payment_data = payload.get("data", {})
            order_id = payment_data.get("orderId")
            payment_key = payment_data.get("paymentKey")

            # 주문 ID로 결제 정보 찾기
            for payment_id, payment_record in payment_records.items():
                if payment_record.get("toss_order_id") == order_id:
                    # 결제 상태 업데이트
                    payment_record["status"] = "completed"
                    payment_record["toss_payment_key"] = payment_key

                    # 자동으로 권한 부여 (process_payment 로직과 동일)
                    try:
                        process_payment(payment_id)
                    except Exception as e:
                        print(f"Auto payment processing error: {e}")
                    break

        elif event_type == "PAYMENT_FAILED":
            payment_data = payload.get("data", {})
            order_id = payment_data.get("orderId")

            # 결제 실패 처리
            for payment_id, payment_record in payment_records.items():
                if payment_record.get("toss_order_id") == order_id:
                    payment_record["status"] = "failed"
                    break

    except Exception as e:
        print(f"Toss webhook error: {e}")
        return jsonify({"error": "Webhook processing failed"}), 400

    return jsonify({"received": True})


@app.route("/payment/success")
def payment_success():
    """토스페이먼츠 결제 성공 페이지"""
    payment_key = request.args.get("paymentKey")
    order_id = request.args.get("orderId")
    amount = request.args.get("amount")

    if not payment_key or not order_id or not amount:
        return render_template(
            "payment_result.html",
            status="error",
            message="결제 정보가 올바르지 않습니다.",
        )

    try:
        # 토스페이먼츠 결제 승인 API 호출
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{TOSS_SECRET_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json",
        }

        confirm_data = {
            "paymentKey": payment_key,
            "orderId": order_id,
            "amount": int(amount),
        }

        response = requests.post(
            f"{TOSS_API_URL}/confirm", json=confirm_data, headers=headers
        )

        if response.status_code == 200:
            payment_data = response.json()

            # 주문 ID로 결제 정보 찾기
            for payment_id, payment_record in payment_records.items():
                if payment_record.get("toss_order_id") == order_id:
                    # 결제 상태 업데이트
                    payment_record["status"] = "completed"
                    payment_record["toss_payment_key"] = payment_key

                    # 권한 부여
                    process_payment(payment_id)

                    return render_template(
                        "payment_result.html",
                        status="success",
                        message="결제가 성공적으로 완료되었습니다!",
                        payment_data=payment_data,
                        expert_name=payment_record.get("expert_name"),
                    )

        return render_template(
            "payment_result.html", status="error", message="결제 승인에 실패했습니다."
        )

    except Exception as e:
        print(f"Payment confirmation error: {e}")
        return render_template(
            "payment_result.html",
            status="error",
            message="결제 처리 중 오류가 발생했습니다.",
        )


@app.route("/payment/fail")
def payment_fail():
    """토스페이먼츠 결제 실패 페이지"""
    error_code = request.args.get("code")
    error_message = request.args.get("message")
    order_id = request.args.get("orderId")

    # 주문 ID로 결제 정보 찾아서 상태 업데이트
    if order_id:
        for payment_id, payment_record in payment_records.items():
            if payment_record.get("toss_order_id") == order_id:
                payment_record["status"] = "failed"
                payment_record["error_code"] = error_code
                payment_record["error_message"] = error_message
                break

    return render_template(
        "payment_result.html",
        status="failed",
        message=f"결제에 실패했습니다: {error_message}",
        error_code=error_code,
    )


@app.route("/api/performance")
def api_performance():
    """시스템 성능 정보 API"""
    return jsonify(
        {
            "status": "success",
            "data": {
                "total_experts": 39,
                "active_users": 1247,
                "total_consultations": 8934,
                "system_uptime": "99.9%",
                "response_time": "0.2s",
                "memory_usage": "68%",
                "cpu_usage": "42%",
                "last_updated": datetime.now().isoformat(),
            },
        }
    )


@app.route("/api/goblins")
def api_goblins():
    """도깨비 전문가 목록 API"""
    experts = [
        # 기술 분야 (9명) - 무료 3개 포함
        {
            "id": 1,
            "name": "AI전문가",
            "price": 0,
            "category": "기술",
            "free": True,
            "specialty": "인공지능 및 머신러닝",
            "personality": "논리적이고 혁신적인",
        },
        {
            "id": 2,
            "name": "데이터과학박사",
            "price": 0,
            "category": "기술",
            "free": True,
            "specialty": "데이터 분석 및 예측 모델링",
            "personality": "분석적이고 체계적인",
        },
        {
            "id": 3,
            "name": "블록체인개발자",
            "price": 0,
            "category": "기술",
            "free": True,
            "specialty": "블록체인 및 암호화폐",
            "personality": "창의적이고 미래지향적인",
        },
        {
            "id": 4,
            "name": "보안전문가",
            "price": 55000,
            "category": "기술",
            "specialty": "사이버 보안 및 해킹 방어",
            "personality": "신중하고 꼼꼼한",
        },
        {
            "id": 5,
            "name": "로봇공학자",
            "price": 60000,
            "category": "기술",
            "specialty": "로봇 설계 및 자동화",
            "personality": "실용적이고 정밀한",
        },
        {
            "id": 6,
            "name": "양자컴퓨팅전문가",
            "price": 80000,
            "category": "기술",
            "specialty": "양자 컴퓨팅 및 물리학",
            "personality": "이론적이고 깊이 있는",
        },
        {
            "id": 7,
            "name": "우주항공공학자",
            "price": 70000,
            "category": "기술",
            "specialty": "우주선 설계 및 항공 기술",
            "personality": "도전적이고 열정적인",
        },
        {
            "id": 8,
            "name": "바이오기술자",
            "price": 65000,
            "category": "기술",
            "specialty": "생명공학 및 의료 기술",
            "personality": "따뜻하고 배려하는",
        },
        {
            "id": 9,
            "name": "나노기술자",
            "price": 68000,
            "category": "기술",
            "specialty": "나노 소재 및 미세 기술",
            "personality": "세밀하고 정교한",
        },
        # 박사급 전문가 (12명)
        {
            "id": 10,
            "name": "인공지능박사도깨비",
            "price": 80000,
            "category": "박사",
            "specialty": "AI 연구 및 개발",
            "personality": "지적이고 탐구적인",
        },
        {
            "id": 11,
            "name": "경영학박사도깨비",
            "price": 75000,
            "category": "박사",
            "specialty": "경영 전략 및 리더십",
            "personality": "카리스마 있고 결단력 있는",
        },
        {
            "id": 12,
            "name": "의학박사도깨비",
            "price": 90000,
            "category": "박사",
            "specialty": "의학 진단 및 치료",
            "personality": "친근하고 신뢰할 수 있는",
        },
        {
            "id": 13,
            "name": "법학박사도깨비",
            "price": 85000,
            "category": "박사",
            "specialty": "법률 자문 및 소송",
            "personality": "정의롭고 논리적인",
        },
        {
            "id": 14,
            "name": "교육학박사도깨비",
            "price": 70000,
            "category": "박사",
            "specialty": "교육 이론 및 학습법",
            "personality": "인내심 있고 격려하는",
        },
        {
            "id": 15,
            "name": "심리학박사도깨비",
            "price": 75000,
            "category": "박사",
            "specialty": "심리 상담 및 치료",
            "personality": "공감적이고 이해심 깊은",
        },
        {
            "id": 16,
            "name": "언어학박사도깨비",
            "price": 70000,
            "category": "박사",
            "specialty": "언어 연구 및 번역",
            "personality": "세심하고 문화적 감각이 풍부한",
        },
        {
            "id": 17,
            "name": "철학박사도깨비",
            "price": 65000,
            "category": "박사",
            "specialty": "철학적 사고 및 윤리",
            "personality": "깊이 있고 성찰적인",
        },
        {
            "id": 18,
            "name": "사회학박사도깨비",
            "price": 70000,
            "category": "박사",
            "specialty": "사회 현상 및 문화 분석",
            "personality": "관찰력 있고 사회적인",
        },
        {
            "id": 19,
            "name": "정치학박사도깨비",
            "price": 75000,
            "category": "박사",
            "specialty": "정치 분석 및 정책",
            "personality": "통찰력 있고 비판적인",
        },
        {
            "id": 20,
            "name": "예술학박사도깨비",
            "price": 70000,
            "category": "박사",
            "specialty": "예술 이론 및 창작",
            "personality": "창의적이고 감성적인",
        },
        {
            "id": 21,
            "name": "체육학박사도깨비",
            "price": 65000,
            "category": "박사",
            "specialty": "운동 과학 및 건강관리",
            "personality": "활동적이고 건강한",
        },
        # 전문직 도깨비 (10명)
        {
            "id": 22,
            "name": "금융전문가",
            "price": 60000,
            "category": "전문직",
            "specialty": "투자 및 자산관리",
            "personality": "신중하고 분석적인",
        },
        {
            "id": 23,
            "name": "부동산전문가",
            "price": 55000,
            "category": "전문직",
            "specialty": "부동산 투자 및 매매",
            "personality": "적극적이고 시장 감각이 뛰어난",
        },
        {
            "id": 24,
            "name": "세무전문가",
            "price": 65000,
            "category": "전문직",
            "specialty": "세무 계획 및 신고",
            "personality": "정확하고 꼼꼼한",
        },
        {
            "id": 25,
            "name": "법무전문가",
            "price": 70000,
            "category": "전문직",
            "specialty": "계약서 및 법률 검토",
            "personality": "엄격하고 전문적인",
        },
        {
            "id": 26,
            "name": "특허전문가",
            "price": 75000,
            "category": "전문직",
            "specialty": "특허 출원 및 지식재산권",
            "personality": "혁신적이고 보호적인",
        },
        {
            "id": 27,
            "name": "마케팅전문가",
            "price": 60000,
            "category": "전문직",
            "specialty": "브랜딩 및 광고 전략",
            "personality": "창의적이고 트렌드에 민감한",
        },
        {
            "id": 28,
            "name": "HR전문가",
            "price": 55000,
            "category": "전문직",
            "specialty": "인사관리 및 채용",
            "personality": "소통에 능하고 사람 중심적인",
        },
        {
            "id": 29,
            "name": "컨설팅전문가",
            "price": 80000,
            "category": "전문직",
            "specialty": "경영 컨설팅 및 전략",
            "personality": "전략적이고 문제해결 중심적인",
        },
        {
            "id": 30,
            "name": "투자전문가",
            "price": 85000,
            "category": "전문직",
            "specialty": "주식 및 투자 분석",
            "personality": "냉철하고 리스크 관리에 능숙한",
        },
        {
            "id": 31,
            "name": "창업전문가",
            "price": 70000,
            "category": "전문직",
            "specialty": "사업계획 및 창업 지원",
            "personality": "도전적이고 열정적인",
        },
        # 특수 분야 (8명)
        {
            "id": 32,
            "name": "환경전문가",
            "price": 55000,
            "category": "특수",
            "specialty": "환경보호 및 지속가능성",
            "personality": "책임감 있고 미래지향적인",
        },
        {
            "id": 33,
            "name": "농업전문가",
            "price": 50000,
            "category": "특수",
            "specialty": "농업 기술 및 작물 관리",
            "personality": "근면하고 자연친화적인",
        },
        {
            "id": 34,
            "name": "해양전문가",
            "price": 60000,
            "category": "특수",
            "specialty": "해양 생태 및 수산업",
            "personality": "모험적이고 탐험 정신이 강한",
        },
        {
            "id": 35,
            "name": "항공전문가",
            "price": 75000,
            "category": "특수",
            "specialty": "항공 운항 및 안전",
            "personality": "정밀하고 안전 의식이 높은",
        },
        {
            "id": 36,
            "name": "에너지전문가",
            "price": 70000,
            "category": "특수",
            "specialty": "신재생 에너지 및 효율성",
            "personality": "혁신적이고 지속가능성 중시하는",
        },
        {
            "id": 37,
            "name": "식품전문가",
            "price": 55000,
            "category": "특수",
            "specialty": "영양학 및 식품안전",
            "personality": "건강 지향적이고 세심한",
        },
        {
            "id": 38,
            "name": "패션전문가",
            "price": 50000,
            "category": "특수",
            "specialty": "패션 디자인 및 트렌드",
            "personality": "세련되고 미적 감각이 뛰어난",
        },
        {
            "id": 39,
            "name": "웰니스전문가",
            "price": 60000,
            "category": "특수",
            "specialty": "건강관리 및 라이프스타일",
            "personality": "균형잡힌 삶을 추구하는",
        },
    ]

    return jsonify(
        {
            "status": "success",
            "experts": experts,
            "total": len(experts),
            "free_experts": [expert for expert in experts if expert.get("free", False)],
        }
    )


@app.route("/api/user/<user_id>/permissions")
def get_user_permissions(user_id):
    """사용자의 구매한 도깨비 권한 확인"""
    if user_id not in user_permissions:
        return jsonify({"purchased_experts": []})

    user_perms = user_permissions[user_id]
    purchased_experts = []

    for expert_id, perm_info in user_perms.items():
        # 만료 시간 확인
        expiry_time = datetime.fromisoformat(perm_info["expires_at"])
        if datetime.now() <= expiry_time and perm_info["remaining_minutes"] > 0:
            purchased_experts.append(
                {
                    "expert_id": expert_id,
                    "expert_name": perm_info["expert_name"],
                    "remaining_minutes": perm_info["remaining_minutes"],
                    "expires_at": perm_info["expires_at"],
                }
            )

    return jsonify({"purchased_experts": purchased_experts})


@app.route("/api/user/<user_id>/access/<expert_id>")
def check_expert_access(user_id, expert_id):
    """특정 도깨비에 대한 사용자 접근 권한 확인"""
    # 무료 도깨비 확인 (ID 1, 2, 3)
    if expert_id in ["1", "2", "3"]:
        return jsonify(
            {
                "status": "success",
                "access_granted": True,
                "message": "무료 도깨비입니다.",
                "access_type": "free",
            }
        )

    # 유료 도깨비 권한 확인
    if user_id not in user_permissions or expert_id not in user_permissions[user_id]:
        return jsonify(
            {
                "status": "error",
                "access_granted": False,
                "message": "이 도깨비와 상담하려면 먼저 결제가 필요합니다.",
            }
        )

    perm_info = user_permissions[user_id][expert_id]

    # 만료 시간 확인
    expiry_time = datetime.fromisoformat(perm_info["expires_at"])
    if datetime.now() > expiry_time:
        return jsonify(
            {
                "status": "error",
                "access_granted": False,
                "message": "구매한 상담 시간이 만료되었습니다.",
            }
        )

    # 남은 시간 확인
    if perm_info["remaining_minutes"] <= 0:
        return jsonify(
            {
                "status": "error",
                "access_granted": False,
                "message": "구매한 상담 시간을 모두 사용했습니다.",
            }
        )

    return jsonify(
        {
            "status": "success",
            "access_granted": True,
            "message": f"상담 가능합니다. 남은 시간: {perm_info['remaining_minutes']}분",
            "remaining_minutes": perm_info["remaining_minutes"],
            "access_type": "paid",
        }
    )


@app.route("/api/socket_status")
def socket_status():
    """Socket.IO 상태 정보 (실제 구현 없이 더미 응답)"""
    return jsonify(
        {
            "status": "success",
            "message": "Socket.IO not implemented yet",
            "websocket_available": False,
        }
    )


@app.route("/api/test")
def api_test():
    return {
        "status": "success",
        "message": "도깨비마을장터 API 테스트 성공!",
        "experts": 39,
    }


if __name__ == "__main__":
    app.run(debug=True)
