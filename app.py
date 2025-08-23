from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('goblin_market_v11.html')


@app.route("/mobile")
def mobile():
    return render_template('goblin_mobile_v11.html')


@app.route("/payment")
def payment():
    return render_template('payment.html')


@app.route("/api/payment/create", methods=['POST'])
def create_payment():
    data = request.get_json()
    
    # 결제 정보 처리 (실제로는 PG사 연동)
    payment_info = {
        "payment_id": f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "expert_name": data.get('expert_name'),
        "service_type": data.get('service_type'),
        "amount": data.get('amount'),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    return jsonify({
        "status": "success",
        "payment_id": payment_info["payment_id"],
        "redirect_url": f"/payment/process/{payment_info['payment_id']}"
    })


@app.route("/api/payment/process/<payment_id>", methods=['POST'])
def process_payment(payment_id):
    # 실제 결제 처리 로직 (카카오페이, 토스페이 등)
    return jsonify({
        "status": "success",
        "payment_id": payment_id,
        "message": "결제가 완료되었습니다!"
    })


@app.route("/api/experts")
def get_experts():
    experts = [
        {"id": 1, "name": "AI전문가", "price": 30000, "category": "기술"},
        {"id": 2, "name": "경영학박사", "price": 50000, "category": "경영"},
        {"id": 3, "name": "의료AI전문가", "price": 80000, "category": "의료"},
        {"id": 4, "name": "재테크박사", "price": 40000, "category": "금융"},
        {"id": 5, "name": "마케팅왕", "price": 35000, "category": "마케팅"},
        {"id": 6, "name": "심리상담사", "price": 25000, "category": "상담"},
        {"id": 7, "name": "교육멘토", "price": 30000, "category": "교육"},
        {"id": 8, "name": "창업컨설턴트", "price": 60000, "category": "창업"},
        {"id": 9, "name": "예술학박사", "price": 35000, "category": "예술"},
        {"id": 10, "name": "언어학습코치", "price": 25000, "category": "언어"},
        {"id": 11, "name": "건강지킴이", "price": 20000, "category": "건강"},
        {"id": 12, "name": "여행컨설턴트", "price": 30000, "category": "여행"},
        {"id": 13, "name": "패션스타일리스트", "price": 35000, "category": "패션"},
        {"id": 14, "name": "음악프로듀서", "price": 45000, "category": "음악"},
        {"id": 15, "name": "게임기획자", "price": 40000, "category": "게임"},
        {"id": 16, "name": "보안전문가", "price": 55000, "category": "보안"}
    ]
    return jsonify(experts)


@app.route("/api/test")
def api_test():
    return {"status": "success", "message": "도깨비마을장터 API 테스트 성공!", "experts": 16}


if __name__ == "__main__":
    app.run(debug=True)
