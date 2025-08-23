from flask import Flask, render_template, request, jsonify, session
import json
import os
import requests
import base64
from datetime import datetime, timedelta
import uuid

# 토스페이먼츠 결제 시스템
TOSS_CLIENT_KEY = os.getenv('TOSS_CLIENT_KEY', 'test_ck_demo_key')
TOSS_SECRET_KEY = os.getenv('TOSS_SECRET_KEY', 'test_sk_demo_key')
TOSS_API_URL = "https://api.tosspayments.com/v1/payments"
TOSS_ENABLED = bool(TOSS_CLIENT_KEY and TOSS_SECRET_KEY and 'demo' not in TOSS_SECRET_KEY)

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
                "failUrl": f"{request.url_root}payment/fail"
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
                "Content-Type": "application/json"
            }
            
            # 결제 상태 조회
            response = requests.get(f"{TOSS_API_URL}?orderId={order_id}", headers=headers)
            
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

    # 결제 상태 업데이트
    payment_records[payment_id]["status"] = "completed"
    payment_records[payment_id]["completed_at"] = datetime.now().isoformat()

    return jsonify(
        {
            "status": "success",
            "payment_id": payment_id,
            "message": "결제가 완료되었습니다!",
            "expert_access": {
                "expert_name": payment["expert_name"],
                "duration_minutes": duration_minutes,
                "expires_at": expiry_time.isoformat(),
            },
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


@app.route("/api/experts")
def get_experts():
    experts = [
        # 기술 분야 (9명)
        {"id": 1, "name": "AI전문가", "price": 30000, "category": "기술"},
        {"id": 2, "name": "데이터과학박사", "price": 45000, "category": "기술"},
        {"id": 3, "name": "블록체인개발자", "price": 55000, "category": "기술"},
        {"id": 4, "name": "보안전문가", "price": 55000, "category": "기술"},
        {"id": 5, "name": "로봇공학자", "price": 60000, "category": "기술"},
        {"id": 6, "name": "양자컴퓨팅전문가", "price": 80000, "category": "기술"},
        {"id": 7, "name": "우주항공공학자", "price": 70000, "category": "기술"},
        {"id": 8, "name": "바이오기술자", "price": 65000, "category": "기술"},
        {"id": 9, "name": "게임개발자", "price": 40000, "category": "기술"},
        # 경영/비즈니스 (8명)
        {"id": 10, "name": "경영학박사", "price": 50000, "category": "경영"},
        {"id": 11, "name": "창업컨설턴트", "price": 60000, "category": "경영"},
        {"id": 12, "name": "마케팅전문가", "price": 35000, "category": "경영"},
        {"id": 13, "name": "영업학박사", "price": 40000, "category": "경영"},
        {"id": 14, "name": "컨설팅박사", "price": 55000, "category": "경영"},
        {"id": 15, "name": "인사관리박사", "price": 45000, "category": "경영"},
        {"id": 16, "name": "글로벌트레이더", "price": 65000, "category": "경영"},
        {"id": 17, "name": "쇼핑전문가", "price": 30000, "category": "경영"},
        # 금융/투자 (4명)
        {"id": 18, "name": "재테크박사", "price": 40000, "category": "금융"},
        {"id": 19, "name": "경제학박사", "price": 50000, "category": "금융"},
        {"id": 20, "name": "투자전문가", "price": 60000, "category": "금융"},
        {"id": 21, "name": "부동산전문가", "price": 45000, "category": "금융"},
        # 의료/건강 (4명)
        {"id": 22, "name": "의료AI전문가", "price": 80000, "category": "의료"},
        {"id": 23, "name": "건강관리사", "price": 25000, "category": "의료"},
        {"id": 24, "name": "신약개발연구원", "price": 70000, "category": "의료"},
        {"id": 25, "name": "웰니스박사", "price": 35000, "category": "의료"},
        # 교육/상담 (4명)
        {"id": 26, "name": "교육멘토", "price": 30000, "category": "교육"},
        {"id": 27, "name": "심리상담사", "price": 25000, "category": "교육"},
        {"id": 28, "name": "언어학습코치", "price": 25000, "category": "교육"},
        {"id": 29, "name": "라이프코치", "price": 30000, "category": "교육"},
        # 예술/문화 (5명)
        {"id": 30, "name": "예술학박사", "price": 35000, "category": "예술"},
        {"id": 31, "name": "음악프로듀서", "price": 45000, "category": "예술"},
        {"id": 32, "name": "문학박사", "price": 40000, "category": "예술"},
        {"id": 33, "name": "문화기획자", "price": 35000, "category": "예술"},
        {"id": 34, "name": "스토리텔러", "price": 30000, "category": "예술"},
        # 라이프스타일 (5명)
        {
            "id": 35,
            "name": "패션스타일리스트",
            "price": 35000,
            "category": "라이프스타일",
        },
        {"id": 36, "name": "여행컨설턴트", "price": 30000, "category": "라이프스타일"},
        {"id": 37, "name": "요리전문가", "price": 25000, "category": "라이프스타일"},
        {
            "id": 38,
            "name": "인테리어디자이너",
            "price": 40000,
            "category": "라이프스타일",
        },
        {
            "id": 39,
            "name": "펜트하우스컨설턴트",
            "price": 100000,
            "category": "라이프스타일",
        },
    ]
    return jsonify(experts)


@app.route("/api/goblins")
def get_goblins():
    """HTML 템플릿에서 호출하는 도깨비 목록 API"""
    goblins = [
        # 무료 체험 도깨비 (3명)
        {
            "id": 1,
            "name": "AI전문가",
            "speciality": "인공지능",
            "is_free": True,
            "emoji": "🤖",
        },
        {
            "id": 2,
            "name": "데이터과학박사",
            "speciality": "빅데이터",
            "is_free": True,
            "emoji": "📊",
        },
        {
            "id": 3,
            "name": "블록체인개발자",
            "speciality": "암호화폐",
            "is_free": True,
            "emoji": "🔗",
        },
        # 유료 도깨비 (36명)
        {
            "id": 4,
            "name": "보안전문가",
            "speciality": "사이버보안",
            "is_free": False,
            "emoji": "🛡️",
        },
        {
            "id": 5,
            "name": "로봇공학자",
            "speciality": "로봇공학",
            "is_free": False,
            "emoji": "🤖",
        },
        {
            "id": 6,
            "name": "양자컴퓨팅전문가",
            "speciality": "양자컴퓨팅",
            "is_free": False,
            "emoji": "⚛️",
        },
        {
            "id": 7,
            "name": "우주항공공학자",
            "speciality": "우주항공",
            "is_free": False,
            "emoji": "🚀",
        },
        {
            "id": 8,
            "name": "바이오기술자",
            "speciality": "생명공학",
            "is_free": False,
            "emoji": "🧬",
        },
        {
            "id": 9,
            "name": "게임개발자",
            "speciality": "게임개발",
            "is_free": False,
            "emoji": "🎮",
        },
        {
            "id": 10,
            "name": "경영학박사",
            "speciality": "경영전략",
            "is_free": False,
            "emoji": "💼",
        },
        {
            "id": 11,
            "name": "창업컨설턴트",
            "speciality": "창업지원",
            "is_free": False,
            "emoji": "🚀",
        },
        {
            "id": 12,
            "name": "마케팅전문가",
            "speciality": "브랜딩",
            "is_free": False,
            "emoji": "📈",
        },
        {
            "id": 13,
            "name": "영업학박사",
            "speciality": "세일즈",
            "is_free": False,
            "emoji": "💰",
        },
        {
            "id": 14,
            "name": "컨설팅박사",
            "speciality": "비즈니스",
            "is_free": False,
            "emoji": "📋",
        },
        {
            "id": 15,
            "name": "인사관리박사",
            "speciality": "HR",
            "is_free": False,
            "emoji": "👥",
        },
        {
            "id": 16,
            "name": "글로벌트레이더",
            "speciality": "국제무역",
            "is_free": False,
            "emoji": "🌍",
        },
        {
            "id": 17,
            "name": "쇼핑전문가",
            "speciality": "커머스",
            "is_free": False,
            "emoji": "🛒",
        },
        {
            "id": 18,
            "name": "재테크박사",
            "speciality": "투자",
            "is_free": False,
            "emoji": "💎",
        },
        {
            "id": 19,
            "name": "경제학박사",
            "speciality": "경제분석",
            "is_free": False,
            "emoji": "📊",
        },
        {
            "id": 20,
            "name": "투자전문가",
            "speciality": "자산관리",
            "is_free": False,
            "emoji": "📈",
        },
        {
            "id": 21,
            "name": "부동산전문가",
            "speciality": "부동산",
            "is_free": False,
            "emoji": "🏠",
        },
        {
            "id": 22,
            "name": "의료AI전문가",
            "speciality": "의료AI",
            "is_free": False,
            "emoji": "⚕️",
        },
        {
            "id": 23,
            "name": "건강관리사",
            "speciality": "건강관리",
            "is_free": False,
            "emoji": "💪",
        },
        {
            "id": 24,
            "name": "신약개발연구원",
            "speciality": "신약개발",
            "is_free": False,
            "emoji": "💊",
        },
        {
            "id": 25,
            "name": "웰니스박사",
            "speciality": "웰니스",
            "is_free": False,
            "emoji": "🧘",
        },
        {
            "id": 26,
            "name": "교육멘토",
            "speciality": "교육",
            "is_free": False,
            "emoji": "📚",
        },
        {
            "id": 27,
            "name": "심리상담사",
            "speciality": "심리상담",
            "is_free": False,
            "emoji": "💭",
        },
        {
            "id": 28,
            "name": "언어학습코치",
            "speciality": "언어교육",
            "is_free": False,
            "emoji": "🗣️",
        },
        {
            "id": 29,
            "name": "라이프코치",
            "speciality": "인생설계",
            "is_free": False,
            "emoji": "🎯",
        },
        {
            "id": 30,
            "name": "예술학박사",
            "speciality": "예술",
            "is_free": False,
            "emoji": "🎨",
        },
        {
            "id": 31,
            "name": "음악프로듀서",
            "speciality": "음악제작",
            "is_free": False,
            "emoji": "🎵",
        },
        {
            "id": 32,
            "name": "문학박사",
            "speciality": "문학",
            "is_free": False,
            "emoji": "📖",
        },
        {
            "id": 33,
            "name": "문화기획자",
            "speciality": "문화기획",
            "is_free": False,
            "emoji": "🎭",
        },
        {
            "id": 34,
            "name": "스토리텔러",
            "speciality": "스토리텔링",
            "is_free": False,
            "emoji": "📝",
        },
        {
            "id": 35,
            "name": "패션스타일리스트",
            "speciality": "패션",
            "is_free": False,
            "emoji": "👗",
        },
        {
            "id": 36,
            "name": "여행컨설턴트",
            "speciality": "여행",
            "is_free": False,
            "emoji": "✈️",
        },
        {
            "id": 37,
            "name": "요리전문가",
            "speciality": "요리",
            "is_free": False,
            "emoji": "👨‍🍳",
        },
        {
            "id": 38,
            "name": "인테리어디자이너",
            "speciality": "인테리어",
            "is_free": False,
            "emoji": "🏡",
        },
        {
            "id": 39,
            "name": "펜트하우스컨설턴트",
            "speciality": "럭셔리",
            "is_free": False,
            "emoji": "👑",
        },
    ]
    return jsonify({"success": True, "goblins": goblins})


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
        is_expired = datetime.now() > expiry_time

        purchased_experts.append(
            {
                "expert_id": expert_id,
                "expert_name": perm_info["expert_name"],
                "remaining_minutes": perm_info["remaining_minutes"],
                "expires_at": perm_info["expires_at"],
                "is_expired": is_expired,
                "purchased_at": perm_info["purchased_at"],
            }
        )

    return jsonify({"purchased_experts": purchased_experts})


@app.route("/api/chat/check-access", methods=["POST"])
def check_chat_access():
    """도깨비 상담 접근 권한 확인"""
    data = request.get_json()
    user_id = data.get("user_id")
    expert_id = str(data.get("expert_id"))

    if not user_id or not expert_id:
        return jsonify(
            {"status": "error", "message": "사용자 ID와 전문가 ID가 필요합니다."}
        )

    # 무료 체험 도깨비 (처음 3명은 무료)
    free_experts = ["1", "2", "3"]
    if expert_id in free_experts:
        return jsonify(
            {
                "status": "success",
                "access_granted": True,
                "message": "무료 체험 도깨비입니다.",
                "access_type": "free",
            }
        )

    # 결제된 도깨비 확인
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


@app.route("/payment/success")
def payment_success():
    """토스페이먼츠 결제 성공 페이지"""
    payment_key = request.args.get("paymentKey")
    order_id = request.args.get("orderId")
    amount = request.args.get("amount")
    
    if not payment_key or not order_id or not amount:
        return render_template("payment_result.html", 
                             status="error", 
                             message="결제 정보가 올바르지 않습니다.")
    
    try:
        # 토스페이먼츠 결제 승인 API 호출
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{TOSS_SECRET_KEY}:'.encode()).decode()}",
            "Content-Type": "application/json"
        }
        
        confirm_data = {
            "paymentKey": payment_key,
            "orderId": order_id,
            "amount": int(amount)
        }
        
        response = requests.post(f"{TOSS_API_URL}/confirm", 
                               json=confirm_data, 
                               headers=headers)
        
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
                    
                    return render_template("payment_result.html",
                                         status="success",
                                         message="결제가 성공적으로 완료되었습니다!",
                                         payment_data=payment_data,
                                         expert_name=payment_record.get("expert_name"))
        
        return render_template("payment_result.html",
                             status="error", 
                             message="결제 승인에 실패했습니다.")
            
    except Exception as e:
        print(f"Payment confirmation error: {e}")
        return render_template("payment_result.html",
                             status="error",
                             message="결제 처리 중 오류가 발생했습니다.")

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
    
    return render_template("payment_result.html",
                         status="failed",
                         message=f"결제에 실패했습니다: {error_message}",
                         error_code=error_code)

@app.route("/api/test")
def api_test():
    return {
        "status": "success",
        "message": "도깨비마을장터 API 테스트 성공!",
        "experts": 39,
    }


if __name__ == "__main__":
    app.run(debug=True)
