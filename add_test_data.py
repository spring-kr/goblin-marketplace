"""
테스트 결제 데이터 추가 스크립트
결제 관리 앱 테스트용
"""

import sqlite3
import json
import datetime
import random


def add_test_data():
    """테스트 결제 데이터 추가"""
    conn = sqlite3.connect("hyojin_payments.db")
    cursor = conn.cursor()

    # 테이블 생성 (존재하지 않는 경우)
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

    # 테스트 고객 데이터
    test_customers = [
        {"name": "김철수", "email": "kim@test.com", "company": "테크놀로지 주식회사"},
        {"name": "이영희", "email": "lee@test.com", "company": "스마트 솔루션"},
        {"name": "박민수", "email": "park@test.com", "company": "AI 이노베이션"},
        {"name": "최지현", "email": "choi@test.com", "company": "데이터 사이언스 랩"},
        {
            "name": "정현우",
            "email": "jung@test.com",
            "company": "디지털 트랜스포메이션",
        },
        {"name": "한소영", "email": "han@test.com", "company": "클라우드 컴퓨팅"},
        {"name": "윤대호", "email": "yoon@test.com", "company": "핀테크 스타트업"},
        {"name": "임수진", "email": "lim@test.com", "company": "헬스케어 AI"},
        {"name": "강민호", "email": "kang@test.com", "company": "자율주행 연구소"},
        {"name": "오수정", "email": "oh@test.com", "company": "에듀테크 컴퍼니"},
    ]

    # 테스트 상품 데이터
    test_items = [
        {"id": "medical-ai", "name": "의료 AI 도메인", "type": "domain", "price": 199},
        {"id": "finance-ai", "name": "금융 AI 도메인", "type": "domain", "price": 179},
        {
            "id": "education-ai",
            "name": "교육 AI 도메인",
            "type": "domain",
            "price": 149,
        },
        {"id": "medical-doctor-ai", "name": "닥터 김 AI", "type": "agent", "price": 89},
        {
            "id": "finance-analyst-ai",
            "name": "애널리스트 박 AI",
            "type": "agent",
            "price": 79,
        },
        {"id": "starter-bundle", "name": "스타터 번들", "type": "bundle", "price": 399},
        {
            "id": "business-bundle",
            "name": "비즈니스 번들",
            "type": "bundle",
            "price": 899,
        },
    ]

    payment_methods = ["card", "paypal", "bank"]
    statuses = ["active", "pending", "cancelled"]

    # 20개의 테스트 결제 데이터 생성
    for i in range(20):
        customer = random.choice(test_customers)

        # 랜덤하게 1-3개의 상품 선택
        selected_items = random.sample(test_items, random.randint(1, 3))
        total_amount = sum(item["price"] for item in selected_items)

        # 랜덤 날짜 생성 (최근 30일)
        days_ago = random.randint(0, 30)
        created_at = (
            datetime.datetime.now() - datetime.timedelta(days=days_ago)
        ).isoformat()

        subscription_id = f"sub_{random.randint(100000, 999999)}"
        payment_method = random.choice(payment_methods)
        status = random.choice(statuses)

        # 가중치를 둬서 active가 더 많이 나오도록
        if random.random() < 0.6:
            status = "active"
        elif random.random() < 0.8:
            status = "pending"

        cursor.execute(
            """
            INSERT INTO payments 
            (subscription_id, customer_name, customer_email, customer_company, 
             payment_method, total_amount, status, items, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                subscription_id,
                customer["name"],
                customer["email"],
                customer["company"],
                payment_method,
                total_amount,
                status,
                json.dumps(selected_items),
                created_at,
                created_at,
            ),
        )

        print(
            f"✅ 테스트 결제 추가: {subscription_id} - {customer['name']} - ${total_amount}"
        )

    conn.commit()
    conn.close()
    print(f"\n🎉 총 20개의 테스트 결제 데이터가 추가되었습니다!")


if __name__ == "__main__":
    add_test_data()
