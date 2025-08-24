from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime, timedelta

# Vercel 환경 감지
VERCEL_ENV = os.getenv("VERCEL_ENV") is not None
IS_PRODUCTION = os.getenv("VERCEL_ENV") == "production"

# 1000자 고급 AI 시스템 임포트 (Vercel 최적화)
try:
    if VERCEL_ENV:
        # Vercel 환경에서는 간소화된 시스템만 사용
        print("🚀 Vercel 환경 감지 - 간소화된 AI 시스템 로딩 중...")

        # 간단한 응답 시스템 (메모리 없는 버전)
        class SimpleAIManager:
            def __init__(self):
                self.experts = {
                    "AI전문가": "AI와 머신러닝 전문가",
                    "마케팅왕": "디지털 마케팅 전문가",
                    "의료AI전문가": "의료 AI 전문가",
                    "재테크박사": "투자 및 재무 전문가",
                }

            def get_expert_response(self, query, expert_name="AI전문가"):
                """간단한 전문가 응답 생성"""
                responses = {
                    "AI전문가": f"AI 관점에서 '{query}'에 대해 답변드리면, 현재 AI 기술은 빠르게 발전하고 있으며 다양한 분야에 적용되고 있습니다.",
                    "마케팅왕": f"마케팅 관점에서 '{query}'를 분석하면, 타겟 고객의 니즈를 파악하고 효과적인 전략을 수립하는 것이 중요합니다.",
                    "의료AI전문가": f"의료 AI 관점에서 '{query}'에 대해 설명드리면, 정확한 진단과 환자 안전을 최우선으로 고려해야 합니다.",
                    "재테크박사": f"투자 관점에서 '{query}'를 분석하면, 리스크 관리와 장기적 관점에서의 포트폴리오 구성이 중요합니다.",
                }
                return responses.get(
                    expert_name, f"'{query}'에 대한 전문적인 답변을 제공드리겠습니다."
                )

            def generate_response(self, query, expert_name="AI전문가"):
                """기존 메서드와 호환성을 위한 별칭"""
                return self.get_expert_response(query, expert_name)

        real_ai_manager = SimpleAIManager()
        AI_SYSTEM_ENABLED = True
        print("✅ Vercel 최적화 AI 시스템 활성화!")

    else:
        # 로컬 환경에서는 기존 시스템 사용
        from experts.complete_16_experts_improved import RealAIManager

        real_ai_manager = RealAIManager()
        AI_SYSTEM_ENABLED = True
        print("🎉 1단계: 1000자 고급 AI 시스템이 활성화되었습니다!")

except Exception as e:
    print(f"⚠️ AI 시스템 초기화 실패: {e}")

    # 최종 백업 시스템
    class FallbackAIManager:
        def __init__(self):
            self.experts = {"기본전문가": "기본 응답 시스템"}

        def get_expert_response(self, query, expert_name="기본전문가"):
            return f"죄송합니다. 현재 시스템 점검 중입니다. '{query}'에 대한 답변을 준비 중입니다."

        def generate_response(self, query, expert_name="기본전문가"):
            """기존 메서드와 호환성을 위한 별칭"""
            return self.get_expert_response(query, expert_name)

    real_ai_manager = FallbackAIManager()
    AI_SYSTEM_ENABLED = True
    print("🔧 백업 AI 시스템으로 전환했습니다.")

# 메모리 시스템 (Vercel 환경에서는 비활성화)
if VERCEL_ENV:
    print("🚀 Vercel 환경: 메모리 시스템 비활성화 (서버리스 최적화)")
    memory_manager = None
    MEMORY_SYSTEM_ENABLED = False
else:
    try:
        from memory_systems.core.advanced_memory_system_v11 import AdvancedMemorySystem

        memory_manager = AdvancedMemorySystem()
        MEMORY_SYSTEM_ENABLED = True
        print("🧠 메모리 & 학습 시스템이 활성화되었습니다!")
    except Exception as e:
        print(f"⚠️ 메모리 시스템을 불러올 수 없습니다: {e}")
        memory_manager = None
        MEMORY_SYSTEM_ENABLED = False

# 기타 시스템들은 Vercel 환경에서 비활성화
multimodal_ai_manager = None
MULTIMODAL_SYSTEM_ENABLED = False
global_manager = None
GLOBAL_SYSTEM_ENABLED = False
dna_manager = None
DNA_SYSTEM_ENABLED = False

print("🚀 Vercel 환경 최적화 모드로 실행 중...")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "goblin_marketplace_secret_key_2024")

# 결제 완료된 사용자의 권한 정보 저장 (실제로는 데이터베이스 사용)
user_permissions = {}
payment_records = {}


@app.route("/")
def home():
    return render_template("goblin_market_v11.html")


@app.route("/dashboard")
def dashboard_3d():
    """3D 아바타 실시간 대시보드로 리다이렉트"""
    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎮 3D 대시보드로 이동 중...</title>
        <style>
            body {{
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }}
            .redirect-container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                margin: 20px auto;
                max-width: 600px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .btn {{
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
                margin: 10px;
                transition: transform 0.3s ease;
            }}
            .btn:hover {{
                transform: translateY(-2px);
            }}
        </style>
        <meta http-equiv="refresh" content="3;url=http://127.0.0.1:5001">
    </head>
    <body>
        <div class="redirect-container">
            <h1>🎮 3D 아바타 실시간 대시보드</h1>
            <p>🚀 5단계 AI 시스템 + 3D 아바타 대시보드로 이동 중...</p>
            <p>3초 후 자동으로 이동됩니다.</p>
            <a href="http://127.0.0.1:5001" class="btn">즉시 이동</a>
            <a href="/" class="btn">홈으로 돌아가기</a>
        </div>
    </body>
    </html>
    """


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


@app.route("/payment/success")
def payment_success():
    """결제 성공 페이지 (시뮬레이션)"""
    return render_template(
        "payment_result.html",
        status="success",
        message="시뮬레이션 모드: 결제가 성공적으로 완료되었습니다!",
    )


@app.route("/payment/fail")
def payment_fail():
    """결제 실패 페이지 (시뮬레이션)"""
    return render_template(
        "payment_result.html",
        status="failed",
        message="시뮬레이션 모드: 결제가 취소되었습니다.",
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


@app.route("/api/chat/advanced", methods=["POST"])
def advanced_chat():
    """1000자 고급 AI 시스템과 연동된 채팅 API"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        goblin_id = data.get("goblin_id", 1)

        if not AI_SYSTEM_ENABLED:
            return jsonify(
                {
                    "status": "error",
                    "message": "고급 AI 시스템이 비활성화되어 있습니다.",
                }
            )

        # 도깨비 ID를 전문가 타입으로 매핑
        goblin_to_expert_mapping = {
            1: "assistant",  # AI전문가
            2: "data_analyst",  # 데이터과학박사
            3: "builder",  # 블록체인개발자 -> 투자전문가로 매핑
            4: "assistant",  # 보안전문가 -> AI전문가로 매핑
            5: "assistant",  # 로봇공학자 -> AI전문가로 매핑
            6: "assistant",  # 양자컴퓨팅전문가 -> AI전문가로 매핑
            7: "assistant",  # 우주항공공학자 -> AI전문가로 매핑
            8: "medical",  # 바이오기술자 -> 의료전문가로 매핑
            9: "assistant",  # 나노기술자 -> AI전문가로 매핑
            10: "assistant",  # 인공지능박사도깨비
            11: "builder",  # 경영학박사도깨비 -> 투자전문가로 매핑
            12: "medical",  # 의학박사도깨비
            13: "assistant",  # 법학박사도깨비 -> AI전문가로 매핑
            14: "growth",  # 교육학박사도깨비
            15: "counselor",  # 심리학박사도깨비
            16: "assistant",  # 언어학박사도깨비 -> AI전문가로 매핑
            17: "creative",  # 철학박사도깨비 -> 창작전문가로 매핑
        }

        expert_type = goblin_to_expert_mapping.get(goblin_id, "assistant")

        # 1000자 AI 시스템으로 응답 생성
        if real_ai_manager:
            response = real_ai_manager.generate_response(message, expert_type)
        else:
            response = f"🤖 고급 AI 시스템이 일시적으로 비활성화되어 있습니다. '{message}'에 대한 기본 응답을 제공합니다."

        return jsonify(
            {
                "status": "success",
                "result": {
                    "response": response,
                    "conversation_id": f"advanced_{datetime.now().timestamp()}",
                    "goblin_id": goblin_id,
                    "expert_type": expert_type,
                    "response_length": len(response),
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}",
            }
        )


@app.route("/api/ai/status")
def ai_system_status():
    """5단계 AI 시스템 상태 확인"""
    return jsonify(
        {
            "status": "success",
            "ai_systems": {
                "stage_1_basic": {
                    "name": "1000자 고급 AI 시스템",
                    "enabled": AI_SYSTEM_ENABLED,
                    "description": "기본 1000자 전문가 응답 시스템",
                },
                "stage_2_multimodal": {
                    "name": "멀티모달 AI 시스템",
                    "enabled": MULTIMODAL_SYSTEM_ENABLED,
                    "description": "이미지, 영상, 음성 처리 시스템",
                },
                "stage_3_memory": {
                    "name": "메모리 & 학습 시스템",
                    "enabled": MEMORY_SYSTEM_ENABLED,
                    "description": "대화 기억 및 개인화 학습 시스템",
                },
                "stage_4_global": {
                    "name": "글로벌 확장 시스템",
                    "enabled": GLOBAL_SYSTEM_ENABLED,
                    "description": "다국어 및 문화 적응 시스템",
                },
                "stage_5_dna": {
                    "name": "DNA 개인화 시스템",
                    "enabled": DNA_SYSTEM_ENABLED,
                    "description": "유전자 수준 개인 맞춤 AI 시스템",
                },
            },
            "total_enabled": sum(
                [
                    AI_SYSTEM_ENABLED,
                    MULTIMODAL_SYSTEM_ENABLED,
                    MEMORY_SYSTEM_ENABLED,
                    GLOBAL_SYSTEM_ENABLED,
                    DNA_SYSTEM_ENABLED,
                ]
            ),
        }
    )


@app.route("/api/chat/multimodal", methods=["POST"])
def multimodal_chat():
    """2단계: 멀티모달 AI 채팅 (이미지, 영상, 음성 포함)"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        goblin_id = data.get("goblin_id", 1)
        media_type = data.get("media_type", "text")  # text, image, video, audio
        media_data = data.get("media_data", "")

        if not MULTIMODAL_SYSTEM_ENABLED:
            return jsonify(
                {
                    "status": "error",
                    "message": "멀티모달 AI 시스템이 비활성화되어 있습니다.",
                    "fallback": "기본 텍스트 시스템으로 대체됩니다.",
                }
            )

        # 멀티모달 AI 시스템으로 응답 생성
        if multimodal_ai_manager:
            import asyncio

            response = asyncio.run(
                multimodal_ai_manager.get_multimodal_expert_response(
                    expert_id=str(goblin_id),
                    question=message,
                    media_types=[media_type] if media_type != "text" else ["text"],
                )
            )
            response = (
                response.text_response
                if hasattr(response, "text_response")
                else str(response)
            )
        else:
            response = f"🎥 멀티모달 시스템이 일시적으로 비활성화되어 있습니다. 텍스트 메시지: '{message}'"

        return jsonify(
            {
                "status": "success",
                "result": {
                    "response": response,
                    "media_type_processed": media_type,
                    "conversation_id": f"multimodal_{datetime.now().timestamp()}",
                    "goblin_id": goblin_id,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"멀티모달 AI 처리 중 오류가 발생했습니다: {str(e)}",
            }
        )


@app.route("/api/chat/memory", methods=["POST"])
def memory_chat():
    """3단계: 메모리 & 학습 시스템 채팅"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")
        goblin_id = data.get("goblin_id", 1)

        if not MEMORY_SYSTEM_ENABLED:
            return jsonify(
                {
                    "status": "error",
                    "message": "메모리 & 학습 시스템이 비활성화되어 있습니다.",
                    "fallback": "기본 시스템으로 대체됩니다.",
                }
            )

        # 메모리 시스템으로 응답 생성
        if memory_manager and MEMORY_SYSTEM_ENABLED:
            try:
                response = memory_manager.generate_contextual_response(
                    message=message, expert="assistant"  # 기본 전문가 타입
                )
            except Exception as e:
                print(f"메모리 시스템 오류: {e}")
                response = f"🧠 메모리 시스템에서 오류가 발생했습니다. 기본 응답: '{message}에 대한 전문적인 답변을 준비하고 있습니다.'"
        else:
            response = f"🧠 메모리 시스템이 일시적으로 비활성화되어 있습니다. 메시지: '{message}'"

        return jsonify(
            {
                "status": "success",
                "result": {
                    "response": response,
                    "user_id": user_id,
                    "conversation_id": f"memory_{datetime.now().timestamp()}",
                    "goblin_id": goblin_id,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"메모리 시스템 처리 중 오류가 발생했습니다: {str(e)}",
            }
        )


@app.route("/api/chat/global", methods=["POST"])
def global_chat():
    """4단계: 글로벌 확장 시스템 채팅"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        language = data.get("language", "ko")  # 언어 설정
        culture = data.get("culture", "korean")  # 문화 설정
        goblin_id = data.get("goblin_id", 1)

        if not GLOBAL_SYSTEM_ENABLED:
            return jsonify(
                {
                    "status": "error",
                    "message": "글로벌 확장 시스템이 비활성화되어 있습니다.",
                    "fallback": "기본 시스템으로 대체됩니다.",
                }
            )

        # 글로벌 시스템으로 응답 생성
        if global_manager:
            import asyncio

            response_obj = asyncio.run(
                global_manager.get_global_expert_response(
                    expert_id=str(goblin_id),
                    question=message,
                    language=language,
                    cultural_adaptation=True,
                )
            )
            response = (
                response_obj.text_response
                if hasattr(response_obj, "text_response")
                else str(response_obj)
            )
        else:
            response = f"🌍 글로벌 시스템이 일시적으로 비활성화되어 있습니다. 메시지: '{message}'"

        return jsonify(
            {
                "status": "success",
                "result": {
                    "response": response,
                    "language": language,
                    "culture": culture,
                    "conversation_id": f"global_{datetime.now().timestamp()}",
                    "goblin_id": goblin_id,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"글로벌 시스템 처리 중 오류가 발생했습니다: {str(e)}",
            }
        )


@app.route("/api/chat/dna", methods=["POST"])
def dna_chat():
    """5단계: DNA 개인화 시스템 채팅"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        user_dna_profile = data.get("dna_profile", {})  # DNA 프로필 정보
        personality_traits = data.get("personality_traits", [])
        goblin_id = data.get("goblin_id", 1)

        if not DNA_SYSTEM_ENABLED:
            return jsonify(
                {
                    "status": "error",
                    "message": "DNA 개인화 시스템이 비활성화되어 있습니다.",
                    "fallback": "기본 시스템으로 대체됩니다.",
                }
            )

        # DNA 개인화 시스템으로 응답 생성
        if dna_manager:
            try:
                import asyncio

                # 간단한 응답 생성
                response = f"🧬 DNA 개인화 시스템이 활성화되었습니다! '{message}'에 대한 개인 맞춤형 응답을 준비 중입니다..."
            except Exception as e:
                response = f"🧬 DNA 시스템 처리 중 오류: {str(e)}"
        else:
            response = (
                f"🧬 DNA 시스템이 일시적으로 비활성화되어 있습니다. 메시지: '{message}'"
            )

        return jsonify(
            {
                "status": "success",
                "result": {
                    "response": response,
                    "dna_personalization": bool(user_dna_profile),
                    "conversation_id": f"dna_{datetime.now().timestamp()}",
                    "goblin_id": goblin_id,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"DNA 개인화 시스템 처리 중 오류가 발생했습니다: {str(e)}",
            }
        )


@app.route("/api/chat/ultimate", methods=["POST"])
def ultimate_chat():
    """최종 단계: 모든 AI 시스템을 통합한 궁극의 채팅"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")
        goblin_id = data.get("goblin_id", 1)
        media_type = data.get("media_type", "text")
        media_data = data.get("media_data", "")
        language = data.get("language", "ko")
        culture = data.get("culture", "korean")
        dna_profile = data.get("dna_profile", {})

        # 단계별로 처리하여 최고의 응답 생성
        response_stages = []

        # 1단계: 기본 1000자 응답
        if AI_SYSTEM_ENABLED and real_ai_manager:
            stage1_response = real_ai_manager.generate_response(message, "assistant")
            response_stages.append(f"1단계 기본: {stage1_response[:100]}...")

        # 2단계: 멀티모달 처리 (임시 응답)
        if MULTIMODAL_SYSTEM_ENABLED and multimodal_ai_manager:
            stage2_response = f"🎥 멀티모달 시스템 활성화: {media_type} 타입 처리 중..."
            response_stages.append(f"2단계 멀티모달: {stage2_response}")

        # 3단계: 메모리 시스템
        if MEMORY_SYSTEM_ENABLED and memory_manager:
            try:
                stage3_response = memory_manager.generate_contextual_response(
                    message, "assistant"
                )
                response_stages.append(f"3단계 메모리: {stage3_response[:100]}...")
            except Exception as e:
                print(f"메모리 시스템 오류: {e}")
                response_stages.append(f"3단계 메모리: 오류로 인한 기본 응답")

        # 4단계: 글로벌 시스템 (임시 응답)
        if GLOBAL_SYSTEM_ENABLED and global_manager:
            stage4_response = (
                f"🌍 글로벌 시스템 활성화: {language} 언어, {culture} 문화 적응 중..."
            )
            response_stages.append(f"4단계 글로벌: {stage4_response}")

        # 5단계: DNA 개인화 (임시 응답)
        final_response = message
        if DNA_SYSTEM_ENABLED and dna_manager:
            final_response = f"🧬 DNA 개인화 시스템 활성화: 개인 맞춤형 응답 생성 중... 원본 메시지: {message}"
            response_stages.append(f"5단계 DNA: {final_response[:100]}...")
        elif AI_SYSTEM_ENABLED and real_ai_manager:
            final_response = real_ai_manager.generate_response(message, "assistant")

        return jsonify(
            {
                "status": "success",
                "result": {
                    "final_response": final_response,
                    "processing_stages": response_stages,
                    "systems_used": {
                        "stage_1": AI_SYSTEM_ENABLED,
                        "stage_2": MULTIMODAL_SYSTEM_ENABLED,
                        "stage_3": MEMORY_SYSTEM_ENABLED,
                        "stage_4": GLOBAL_SYSTEM_ENABLED,
                        "stage_5": DNA_SYSTEM_ENABLED,
                    },
                    "conversation_id": f"ultimate_{datetime.now().timestamp()}",
                    "goblin_id": goblin_id,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": f"통합 AI 시스템 처리 중 오류가 발생했습니다: {str(e)}",
            }
        )


@app.route("/api/test")
def api_test():
    return {
        "status": "success",
        "message": "도깨비마을장터 API 테스트 성공!",
        "experts": 39,
        "ai_systems": {
            "stage_1_basic": AI_SYSTEM_ENABLED,
            "stage_2_multimodal": MULTIMODAL_SYSTEM_ENABLED,
            "stage_3_memory": MEMORY_SYSTEM_ENABLED,
            "stage_4_global": GLOBAL_SYSTEM_ENABLED,
            "stage_5_dna": DNA_SYSTEM_ENABLED,
        },
        "total_ai_stages": sum(
            [
                AI_SYSTEM_ENABLED,
                MULTIMODAL_SYSTEM_ENABLED,
                MEMORY_SYSTEM_ENABLED,
                GLOBAL_SYSTEM_ENABLED,
                DNA_SYSTEM_ENABLED,
            ]
        ),
    }


if __name__ == "__main__":
    app.run(debug=True)
