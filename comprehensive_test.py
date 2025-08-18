#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HYOJIN.AI MVP 종합 테스트 스크립트
- 가상링크 홍보용 (저장소 2개)
- 구독신청시 저장완료
- 각 도메인 및 AI 에이전트 실제 구동여부
- 구독자 가상링크로 구동여부
"""

import requests
import json
import time
from datetime import datetime


def test_github_pages():
    """1. GitHub Pages 랜딩페이지 테스트"""
    print("🌐 === 1. GitHub Pages 랜딩페이지 테스트 ===")
    try:
        response = requests.get(
            "https://hyojin-ai.github.io/hyojin-ai-mvp/", timeout=10
        )
        print(f"✅ GitHub Pages 상태: {response.status_code}")

        content = response.text
        keywords = [
            "AI 오케스트레이션",
            "엔터프라이즈",
            "Professional",
            "토스, 쿠팡",
            "Startup",
        ]
        found = [k for k in keywords if k in content]

        if found:
            print(f"✅ 엔터프라이즈 업그레이드 확인됨: {found}")
        else:
            print("⚠️ 엔터프라이즈 키워드 미확인")

        print(f"📄 페이지 크기: {len(content):,} bytes")
        print("🎯 GitHub Pages 홍보용 링크: https://hyojin-ai.github.io/hyojin-ai-mvp/")

        return True
    except Exception as e:
        print(f"❌ GitHub Pages 오류: {e}")
        return False


def test_render_backend():
    """2. Render 백엔드 API 서버 테스트"""
    print("\n🔧 === 2. Render 백엔드 API 서버 테스트 ===")
    try:
        # 기본 상태 확인
        response = requests.get("https://hyojin-ai-mvp.onrender.com/", timeout=15)
        print(f"✅ Render API 서버 상태: {response.status_code}")
        print(f"📡 응답: {response.text[:150]}...")

        # 구독자 수 확인
        subscribers_response = requests.get(
            "https://hyojin-ai-mvp.onrender.com/subscribers", timeout=15
        )
        if subscribers_response.status_code == 200:
            subscribers_data = subscribers_response.json()
            subscriber_count = len(subscribers_data.get("subscribers", []))
            print(f"👥 현재 구독자 수: {subscriber_count}")

            if subscribers_data.get("subscribers"):
                latest = subscribers_data["subscribers"][-1]
                print(f"📧 최근 구독자: {latest.get('email', 'N/A')}")
                print(f"📅 가입일: {latest.get('timestamp', 'N/A')}")

        print("🎯 Render API 홍보용 링크: https://hyojin-ai-mvp.onrender.com/")
        return True

    except Exception as e:
        print(f"❌ Render API 오류: {e}")
        return False


def test_subscription():
    """3. 구독신청시 저장완료 테스트"""
    print("\n📧 === 3. 구독신청 저장완료 테스트 ===")

    test_email = f"test_user_{int(time.time())}@example.com"
    test_data = {
        "email": test_email,
        "company": "테스트 회사",
        "plan": "professional",
        "phone": "010-1234-5678",
    }

    try:
        print(f"📤 테스트 구독 신청: {test_email}")
        response = requests.post(
            "https://hyojin-ai-mvp.onrender.com/subscribe", json=test_data, timeout=15
        )

        print(f"✅ 구독 응답 상태: {response.status_code}")
        result = response.json()

        if result.get("success"):
            print(f"✅ 구독 성공!")
            print(f"📧 구독 ID: {result.get('subscription_id')}")
            print(f"📅 등록 시간: {result.get('timestamp')}")
            return True
        else:
            print(f"❌ 구독 실패: {result}")
            return False

    except Exception as e:
        print(f"❌ 구독 테스트 오류: {e}")
        return False


def test_ai_domains():
    """4. 각 도메인 및 AI 에이전트 실제 구동여부 테스트"""
    print("\n🤖 === 4. AI 도메인 및 에이전트 구동 테스트 ===")

    domains = [
        ("paymentapp", "결제 사기 감지 요청"),
        ("deliveryservice", "배송 최적화 요청"),
        ("onlineshopping", "상품 추천 요청"),
        ("realestateapp", "부동산 가격 예측"),
        ("onlineeducation", "학습 추천"),
        ("jobplatform", "인재 매칭"),
        ("finance", "리스크 분석"),
        ("healthcare", "진단 보조"),
        ("manufacturing", "품질 관리"),
        ("retail", "재고 최적화"),
        ("logistics", "배송 루트"),
        ("customerservice", "고객 문의"),
    ]

    working_domains = []
    failed_domains = []

    for domain, test_text in domains:
        try:
            print(f"🔍 테스트 중: {domain}")
            response = requests.get(
                f"https://hyojin-ai-mvp.onrender.com/predict",
                params={"domain": domain, "text": test_text},
                timeout=10,
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("prediction"):
                    print(f"  ✅ {domain}: 정상 작동")
                    working_domains.append(domain)
                else:
                    print(f"  ⚠️ {domain}: 응답 없음")
                    failed_domains.append(domain)
            else:
                print(f"  ❌ {domain}: HTTP {response.status_code}")
                failed_domains.append(domain)

        except Exception as e:
            print(f"  ❌ {domain}: {str(e)[:50]}...")
            failed_domains.append(domain)

    print(f"\n📊 AI 도메인 테스트 결과:")
    print(f"✅ 정상 작동: {len(working_domains)}/{len(domains)}")
    print(f"❌ 실패: {len(failed_domains)}/{len(domains)}")

    if working_domains:
        print(
            f"✅ 작동 도메인: {', '.join(working_domains[:5])}{'...' if len(working_domains) > 5 else ''}"
        )
    if failed_domains:
        print(
            f"❌ 실패 도메인: {', '.join(failed_domains[:5])}{'...' if len(failed_domains) > 5 else ''}"
        )

    return len(working_domains) > len(failed_domains)


def test_subscriber_access():
    """5. 구독자 가상링크로 구동여부 테스트"""
    print("\n🔑 === 5. 구독자 API 액세스 테스트 ===")

    try:
        # 먼저 구독자 목록에서 실제 구독자 확인
        subscribers_response = requests.get(
            "https://hyojin-ai-mvp.onrender.com/subscribers", timeout=10
        )

        if subscribers_response.status_code == 200:
            subscribers_data = subscribers_response.json()
            subscribers = subscribers_data.get("subscribers", [])

            if subscribers:
                # 최근 구독자로 테스트
                test_subscriber = subscribers[-1]
                test_email = test_subscriber["email"]

                print(f"👤 테스트 구독자: {test_email}")

                # 인증된 API 호출 테스트
                auth_response = requests.post(
                    "https://hyojin-ai-mvp.onrender.com/predict/auth",
                    json={
                        "email": test_email,
                        "domain": "paymentapp",
                        "text": "결제 사기 감지 테스트",
                    },
                    timeout=10,
                )

                print(f"🔐 인증 API 상태: {auth_response.status_code}")

                if auth_response.status_code == 200:
                    result = auth_response.json()
                    print(f"✅ 구독자 액세스 성공!")
                    print(f"🤖 AI 응답: {result.get('prediction', 'N/A')[:100]}...")
                    print(f"📊 사용량: {result.get('usage_count', 'N/A')}")
                    return True
                else:
                    print(f"❌ 구독자 액세스 실패: {auth_response.text}")
                    return False
            else:
                print("⚠️ 등록된 구독자가 없습니다")
                return False
        else:
            print(f"❌ 구독자 목록 조회 실패: {subscribers_response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 구독자 액세스 테스트 오류: {e}")
        return False


def main():
    """종합 테스트 실행"""
    print("🚀 HYOJIN.AI MVP 종합 테스트 시작")
    print("=" * 60)

    results = {}

    # 각 테스트 실행
    results["github_pages"] = test_github_pages()
    results["render_backend"] = test_render_backend()
    results["subscription"] = test_subscription()
    results["ai_domains"] = test_ai_domains()
    results["subscriber_access"] = test_subscriber_access()

    # 최종 결과 요약
    print("\n" + "=" * 60)
    print("📋 === 종합 테스트 결과 요약 ===")

    total_tests = len(results)
    passed_tests = sum(results.values())

    print(f"✅ 통과: {passed_tests}/{total_tests}")
    print(f"❌ 실패: {total_tests - passed_tests}/{total_tests}")
    print(f"📊 성공률: {(passed_tests/total_tests)*100:.1f}%")

    print("\n📝 상세 결과:")
    test_names = {
        "github_pages": "1. GitHub Pages 랜딩페이지",
        "render_backend": "2. Render 백엔드 API",
        "subscription": "3. 구독신청 저장완료",
        "ai_domains": "4. AI 도메인 구동",
        "subscriber_access": "5. 구독자 API 액세스",
    }

    for key, result in results.items():
        status = "✅ 통과" if result else "❌ 실패"
        print(f"  {test_names[key]}: {status}")

    # 홍보용 링크 제공
    print("\n🎯 === 홍보용 링크 ===")
    print("📱 랜딩페이지: https://hyojin-ai.github.io/hyojin-ai-mvp/")
    print("🔧 API 서버: https://hyojin-ai-mvp.onrender.com/")
    print("📧 구독 테스트: 랜딩페이지에서 직접 구독 가능")

    if passed_tests == total_tests:
        print("\n🎉 모든 테스트 통과! MVP가 완벽하게 작동합니다!")
    else:
        print(
            f"\n⚠️ {total_tests - passed_tests}개 테스트 실패. 추가 점검이 필요합니다."
        )


if __name__ == "__main__":
    main()
