#!/usr/bin/env python3
"""
간단한 MVP 테스트 - 단계별 실행
"""

import requests
import json
import time


def test_step_by_step():
    print("🚀 HYOJIN.AI MVP 단계별 테스트")
    print("=" * 50)

    # 1. 기본 서버 상태
    print("\n1️⃣ 서버 상태 확인")
    try:
        r = requests.get("https://hyojin-ai-mvp.onrender.com/", timeout=10)
        print(f"✅ Render 서버: {r.status_code}")
    except:
        print("❌ Render 서버 접속 실패")

    # 2. 구독자 수 확인
    print("\n2️⃣ 구독자 현황")
    try:
        r = requests.get("https://hyojin-ai-mvp.onrender.com/subscribers", timeout=10)
        if r.status_code == 200:
            data = r.json()
            count = len(data.get("subscribers", []))
            print(f"👥 현재 구독자: {count}명")
            if data.get("subscribers"):
                latest = data["subscribers"][-1]
                print(f"📧 최근: {latest.get('email')}")
        else:
            print(f"❌ 구독자 조회 실패: {r.status_code}")
    except Exception as e:
        print(f"❌ 구독자 조회 오류: {e}")

    # 3. AI 도메인 테스트 (3개만)
    print("\n3️⃣ AI 도메인 테스트 (샘플)")
    domains = [
        ("paymentapp", "결제 문제"),
        ("deliveryservice", "배송 요청"),
        ("onlineshopping", "상품 추천"),
    ]

    working = 0
    for domain, text in domains:
        try:
            r = requests.get(
                "https://hyojin-ai-mvp.onrender.com/predict",
                params={"domain": domain, "text": text},
                timeout=8,
            )
            if r.status_code == 200 and r.json().get("prediction"):
                print(f"✅ {domain}: 작동")
                working += 1
            else:
                print(f"❌ {domain}: 실패")
        except:
            print(f"❌ {domain}: 오류")

    print(f"📊 AI 도메인: {working}/{len(domains)} 작동")

    # 4. 구독 테스트
    print("\n4️⃣ 구독 시스템 테스트")
    test_email = f"test_{int(time.time())}@example.com"
    try:
        r = requests.post(
            "https://hyojin-ai-mvp.onrender.com/subscribe",
            json={
                "email": test_email,
                "company": "테스트",
                "plan": "professional",
                "phone": "010-1234-5678",
            },
            timeout=10,
        )
        if r.status_code == 200 and r.json().get("success"):
            print(f"✅ 구독 성공: {test_email}")
        else:
            print(f"❌ 구독 실패: {r.text}")
    except Exception as e:
        print(f"❌ 구독 오류: {e}")

    # 5. 홍보용 링크
    print("\n🎯 홍보용 링크")
    print("📱 랜딩페이지: https://hyojin-ai.github.io/hyojin-ai-mvp/")
    print("🔧 API 데모: https://hyojin-ai-mvp.onrender.com/")
    print(
        "🤖 AI 테스트: https://hyojin-ai-mvp.onrender.com/predict?domain=paymentapp&text=테스트"
    )


if __name__ == "__main__":
    test_step_by_step()
