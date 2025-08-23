from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime, timedelta
import uuid

# Stripe 결제 시스템
try:
    import stripe
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_demo_key')
    STRIPE_ENABLED = True
except ImportError:
    STRIPE_ENABLED = False
    print("Stripe not installed. Using simulation mode.")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'goblin_marketplace_secret_key_2024')

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
    
    # Stripe 결제 인텐트 생성 (실제 결제)
    if STRIPE_ENABLED and amount and amount > 0:
        try:
            # Stripe 결제 인텐트 생성
            intent = stripe.PaymentIntent.create(
                amount=int(amount),  # Stripe는 원 단위가 아닌 센트 단위
                currency='krw',
                metadata={
                    'payment_id': payment_id,
                    'user_id': user_id,
                    'expert_id': expert_id,
                    'expert_name': expert_name
                },
                description=f"도깨비마을장터 - {expert_name} 상담 ({duration_minutes}분)"
            )
            
            payment_info["stripe_payment_intent_id"] = intent.id
            payment_info["stripe_client_secret"] = intent.client_secret
            payment_records[payment_id] = payment_info
            
            return jsonify({
                "status": "success",
                "payment_id": payment_id,
                "user_id": user_id,
                "stripe_client_secret": intent.client_secret,
                "stripe_publishable_key": os.getenv('STRIPE_PUBLISHABLE_KEY'),
                "amount": amount,
                "expert_name": expert_name,
                "redirect_url": f"/payment/process/{payment_id}",
                "payment_method": "stripe"
            })
            
        except Exception as e:
            print(f"Stripe error: {e}")
            # Stripe 오류 시 시뮬레이션 모드로 fallback
            pass
    
    # 시뮬레이션 모드 (개발/테스트용)
    return jsonify({
        "status": "success",
        "payment_id": payment_id,
        "user_id": user_id,
        "redirect_url": f"/payment/process/{payment_id}",
        "payment_method": "simulation",
        "message": "테스트 모드: 실제 결제 없이 권한이 부여됩니다."
    })


@app.route("/api/payment/process/<payment_id>", methods=["POST"])
def process_payment(payment_id):
    # 결제 기록 확인
    if payment_id not in payment_records:
        return jsonify({"status": "error", "message": "결제 정보를 찾을 수 없습니다."})

    payment = payment_records[payment_id]

    # Stripe 결제 확인
    if STRIPE_ENABLED and "stripe_payment_intent_id" in payment:
        try:
            # Stripe에서 결제 상태 확인
            intent = stripe.PaymentIntent.retrieve(payment["stripe_payment_intent_id"])
            
            if intent.status != "succeeded":
                return jsonify({
                    "status": "error", 
                    "message": "결제가 완료되지 않았습니다.",
                    "stripe_status": intent.status
                })
                
        except Exception as e:
            return jsonify({"status": "error", "message": f"결제 확인 중 오류: {str(e)}"})

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

    return jsonify({
        "status": "success",
        "payment_id": payment_id,
        "message": "결제가 완료되었습니다!",
        "expert_access": {
            "expert_name": payment["expert_name"],
            "duration_minutes": duration_minutes,
            "expires_at": expiry_time.isoformat(),
        },
    })


@app.route("/api/stripe/webhook", methods=["POST"])
def stripe_webhook():
    """Stripe 웹훅 처리 - 실제 결제 완료 시 권한 부여"""
    if not STRIPE_ENABLED:
        return jsonify({"error": "Stripe not enabled"}), 400
        
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    # 결제 완료 이벤트 처리
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # 메타데이터에서 결제 정보 추출
        payment_id = payment_intent.get('metadata', {}).get('payment_id')
        user_id = payment_intent.get('metadata', {}).get('user_id')
        expert_id = payment_intent.get('metadata', {}).get('expert_id')
        
        if payment_id and payment_id in payment_records:
            # 자동으로 권한 부여 (process_payment 로직과 동일)
            process_payment(payment_id)

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


@app.route("/api/test")
def api_test():
    return {
        "status": "success",
        "message": "도깨비마을장터 API 테스트 성공!",
        "experts": 39,
    }


if __name__ == "__main__":
    app.run(debug=True)
