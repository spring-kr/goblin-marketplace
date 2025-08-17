#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7일 무료체험 시스템 테스트 스크립트
"""

import requests
import json
import time
from datetime import datetime

# 테스트 서버 URL
BASE_URL = "https://hyojin-ai-mvp.onrender.com"


def test_subscription_flow():
    """구독 및 체험 시스템 전체 플로우 테스트"""
    print("🧪 7일 무료체험 시스템 테스트 시작!")
    print("=" * 50)

    # 테스트 이메일
    test_email = f"test_trial_{int(time.time())}@example.com"
    print(f"📧 테스트 이메일: {test_email}")

    # 1. 구독 신청 (자동으로 7일 체험 시작)
    print("\n1️⃣ 구독 신청 및 7일 체험 시작...")
    subscribe_data = {
        "email": test_email,
        "company": "테스트 회사",
        "plan": "trial",
        "message": "AI 데이터 분석에 관심이 있습니다",
    }

    try:
        response = requests.post(f"{BASE_URL}/subscribe", json=subscribe_data)
        if response.status_code == 200:
            print("✅ 구독 신청 성공!")
            print(f"   응답: {response.json()}")
        else:
            print(f"❌ 구독 실패: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ 구독 요청 오류: {e}")
        return

    # 2. 사용자 상태 확인
    print("\n2️⃣ 사용자 상태 확인...")
    try:
        response = requests.get(f"{BASE_URL}/status/{test_email}")
        if response.status_code == 200:
            status = response.json()
            print("✅ 상태 확인 성공!")
            print(f"   계획: {status['plan']}")
            print(f"   체험 만료일: {status['trial_expires']}")
            print(f"   남은 일수: {status['days_remaining']}일")
            print(f"   일일 호출 한도: {status['usage']['max_daily_calls']}")
            print(f"   사용 가능한 도메인: {status['access']['available_domains']}개")
        else:
            print(f"❌ 상태 확인 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 상태 확인 오류: {e}")
        return

    # 3. 인증된 예측 API 테스트
    print("\n3️⃣ 인증된 예측 API 테스트...")
    test_data = {
        "email": test_email,
        "domain": "paymentapp",
        "text": "결제 시스템에 문제가 있어요",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict/auth",
            json=test_data,
        )
        if response.status_code == 200:
            print("✅ 인증된 예측 성공!")
            result = response.json()
            print(f"   도메인: {result['domain']}")
            result_text = str(result["result"])
            print(f"   결과: {result_text[:100]}...")
            print(f"   사용량: {result.get('usage', 'N/A')}")
        else:
            print(f"❌ 예측 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 예측 요청 오류: {e}")

    # 4. 여러 번 호출하여 사용량 증가 테스트
    print("\n4️⃣ 사용량 한도 테스트 (5회 연속 호출)...")
    for i in range(5):
        try:
            response = requests.post(
                f"{BASE_URL}/predict/auth",
                json=test_data,
            )
            if response.status_code == 200:
                result = response.json()
                usage = result.get("usage", {})
                print(
                    f"   {i+1}회: {usage.get('daily_calls', '?')}/{usage.get('max_calls', '?')} 호출"
                )
            else:
                print(f"   {i+1}회 실패: {response.status_code}")
                break
        except Exception as e:
            print(f"   {i+1}회 오류: {e}")
            break

        time.sleep(1)  # 1초 대기

    # 5. 최종 상태 확인
    print("\n5️⃣ 최종 사용량 상태 확인...")
    try:
        response = requests.get(f"{BASE_URL}/status/{test_email}")
        if response.status_code == 200:
            status = response.json()
            print("✅ 최종 상태:")
            print(f"   총 호출 수: {status['usage']['total_calls']}")
            print(f"   오늘 호출 수: {status['usage']['daily_calls']}")
            print(f"   남은 호출 수: {status['usage']['remaining_calls']}")
        else:
            print(f"❌ 최종 상태 확인 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 최종 상태 확인 오류: {e}")

    print("\n" + "=" * 50)
    print("🎉 7일 무료체험 시스템 테스트 완료!")


def test_trial_expiry():
    """체험 만료 시뮬레이션 테스트"""
    print("\n🕐 체험 만료 시뮬레이션 테스트...")

    # 이미 만료된 가상의 사용자로 테스트
    expired_email = "expired_test@example.com"

    # 만료된 계정으로 예측 시도
    test_data = {
        "email": expired_email,
        "domain": "paymentapp",
        "text": "테스트 데이터",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/predict/auth",
            json=test_data,
        )

        if response.status_code == 404:
            print("✅ 미등록 사용자 차단 성공!")
        elif response.status_code == 403:
            print("✅ 만료된 체험 차단 성공!")
        else:
            print(f"⚠️ 예상과 다른 응답: {response.status_code}")
    except Exception as e:
        print(f"❌ 만료 테스트 오류: {e}")


if __name__ == "__main__":
    try:
        test_subscription_flow()
        test_trial_expiry()
    except KeyboardInterrupt:
        print("\n\n⏹️ 테스트 중단됨")
    except Exception as e:
        print(f"\n❌ 테스트 실행 오류: {e}")
