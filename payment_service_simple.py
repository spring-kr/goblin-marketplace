"""
HYOJIN.AI 결제 서비스 (간소화 버전)
데모 및 테스트용 결제 처리
업데이트: 2025.08.19 - 테스트 결제 시스템 안정성 개선
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException
from virtual_service_manager import virtual_service_manager
from pydantic import BaseModel
from typing import List, Dict, Any


# 결제 요청 모델들
class PaymentItem(BaseModel):
    id: str
    name: str
    type: str
    price: float


class CustomerData(BaseModel):
    name: str
    email: str
    company: str = ""
    paymentMethod: str


class PaymentRequest(BaseModel):
    token: str = ""
    amount: int
    customer: CustomerData
    items: List[PaymentItem]


class SubscriptionService:
    """구독 관리 서비스"""

    def __init__(self):
        self.subscriptions_db = {}

    def create_subscription(
        self, customer: CustomerData, items: List[PaymentItem], payment_method: str
    ) -> Dict[str, Any]:
        """새 구독 생성"""
        subscription_id = f"sub_{uuid.uuid4().hex[:8]}"
        total_amount = sum(item.price for item in items)

        subscription = {
            "id": subscription_id,
            "customer": customer.dict(),
            "items": [item.dict() for item in items],
            "total_amount": total_amount,
            "payment_method": payment_method,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "next_billing_date": (datetime.now() + timedelta(days=30)).isoformat(),
        }

        self.subscriptions_db[subscription_id] = subscription
        return subscription


class EmailService:
    """이메일 서비스 (간소화 버전)"""

    def __init__(self):
        pass

    async def send_subscription_confirmation(self, subscription_data: Dict[str, Any]):
        """구독 확인 이메일 전송 (로그만 출력)"""
        customer = subscription_data["customer"]
        print(f"📧 이메일 전송 시뮬레이션:")
        print(f"   → 받는 사람: {customer['email']}")
        print(f"   → 제목: HYOJIN.AI 구독 확인 - {subscription_data['id']}")
        print(
            f"   → 내용: 구독이 활성화되었습니다. 총 ${subscription_data['total_amount']/100:.2f}/월"
        )
        return True


class PaymentProcessor:
    """결제 처리 서비스"""

    def __init__(self):
        self.subscription_service = SubscriptionService()

    async def process_card_payment(
        self, payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """신용카드 결제 처리 (시뮬레이션)"""
        try:
            # 시뮬레이션: 실제로는 Stripe API 호출
            print(f"💳 신용카드 결제 처리 시뮬레이션")
            print(f"   → 고객: {payment_request.customer.name}")
            print(f"   → 금액: ${payment_request.amount/100:.2f}")
            print(f"   → 상품: {len(payment_request.items)}개")

            # 구독 생성
            subscription = self.subscription_service.create_subscription(
                payment_request.customer, payment_request.items, "card"
            )

            # 🔗 가상 서비스 링크 생성
            service_links = virtual_service_manager.generate_service_links(
                subscription["id"],
                [
                    {"id": item.id, "name": item.name, "price": item.price}
                    for item in payment_request.items
                ],
            )

            print(f"✅ 가상 서비스 링크 {len(service_links)}개 생성 완료")

            return {
                "success": True,
                "subscription_id": subscription["id"],
                "amount": payment_request.amount,
                "status": "active",
                "charge_id": f"ch_{uuid.uuid4().hex[:16]}",
                "service_links": service_links,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def process_paypal_payment(
        self, payment_request: PaymentRequest
    ) -> Dict[str, Any]:
        """PayPal 결제 처리 (시뮬레이션)"""
        try:
            print(f"💙 PayPal 결제 처리 시뮬레이션")
            print(f"   → 고객: {payment_request.customer.name}")
            print(f"   → 금액: ${payment_request.amount/100:.2f}")

            # 구독 생성
            subscription = self.subscription_service.create_subscription(
                payment_request.customer, payment_request.items, "paypal"
            )

            # 🔗 가상 서비스 링크 생성
            service_links = virtual_service_manager.generate_service_links(
                subscription["id"],
                [
                    {"id": item.id, "name": item.name, "price": item.price}
                    for item in payment_request.items
                ],
            )

            print(f"✅ 가상 서비스 링크 {len(service_links)}개 생성 완료")

            return {
                "success": True,
                "subscription_id": subscription["id"],
                "amount": payment_request.amount,
                "status": "active",
                "paypal_order_id": f"PAYPAL_{uuid.uuid4().hex[:12]}",
                "service_links": service_links,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def process_bank_transfer(
        self, customer: CustomerData, items: List[PaymentItem]
    ) -> Dict[str, Any]:
        """계좌이체 처리 (시뮬레이션)"""
        try:
            print(f"🏦 계좌이체 신청 처리 시뮬레이션")
            print(f"   → 고객: {customer.name}")
            print(f"   → 이메일: {customer.email}")

            # 구독 생성 (대기 상태)
            subscription = self.subscription_service.create_subscription(
                customer, items, "bank"
            )
            subscription["status"] = "pending"  # 대기 상태로 변경

            total_amount = sum(item.price for item in items)

            return {
                "success": True,
                "subscription_id": subscription["id"],
                "amount": total_amount,
                "status": "pending",
                "bank_info": {
                    "bank_name": "국민은행",
                    "account_number": "123-456-789012",
                    "account_holder": "HYOJIN.AI",
                    "amount": total_amount,
                },
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


# 서비스 인스턴스 생성
payment_processor = PaymentProcessor()
email_service = EmailService()
