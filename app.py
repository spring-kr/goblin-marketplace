from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)


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

    # 결제 정보 처리 (실제로는 PG사 연동)
    payment_info = {
        "payment_id": f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "expert_name": data.get("expert_name"),
        "service_type": data.get("service_type"),
        "amount": data.get("amount"),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }

    return jsonify(
        {
            "status": "success",
            "payment_id": payment_info["payment_id"],
            "redirect_url": f"/payment/process/{payment_info['payment_id']}",
        }
    )


@app.route("/api/payment/process/<payment_id>", methods=["POST"])
def process_payment(payment_id):
    # 실제 결제 처리 로직 (카카오페이, 토스페이 등)
    return jsonify(
        {
            "status": "success",
            "payment_id": payment_id,
            "message": "결제가 완료되었습니다!",
        }
    )


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
        {"id": 35, "name": "패션스타일리스트", "price": 35000, "category": "라이프스타일"},
        {"id": 36, "name": "여행컨설턴트", "price": 30000, "category": "라이프스타일"},
        {"id": 37, "name": "요리전문가", "price": 25000, "category": "라이프스타일"},
        {"id": 38, "name": "인테리어디자이너", "price": 40000, "category": "라이프스타일"},
        {"id": 39, "name": "펜트하우스컨설턴트", "price": 100000, "category": "라이프스타일"}
    ]
    return jsonify(experts)


@app.route("/api/test")
def api_test():
    return {
        "status": "success",
        "message": "도깨비마을장터 API 테스트 성공!",
        "experts": 39,
    }


if __name__ == "__main__":
    app.run(debug=True)
