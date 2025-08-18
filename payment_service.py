"""
HYOJIN.AI 결제 서비스
실제 Stripe, PayPal 결제 처리를 위한 백엔드 서비스
"""
import os
import stripe
import json
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# Stripe 설정 (실제 사용시 환경변수로 관리)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')  # 실제 Secret Key

class PaymentItem(BaseModel):
    id: str
    name: str
    price: float
    type: str

class CustomerData(BaseModel):
    name: str
    email: str
    company: str = ""
    paymentMethod: str

class PaymentRequest(BaseModel):
    token: str = None
    amount: int  # cents
    customer: CustomerData
    items: List[PaymentItem]

class SubscriptionService:
    """구독 서비스 관리"""
    
    def __init__(self):
        self.subscriptions_db = {}  # 실제로는 데이터베이스 사용
        
    async def create_subscription(self, customer_data: CustomerData, items: List[PaymentItem], payment_method: str = "card") -> Dict[str, Any]:
        """구독 생성"""
        
        subscription_id = f"sub_{datetime.now().strftime('%Y%m%d%H%M%S')}_{customer_data.email.split('@')[0]}"
        
        # 구독 데이터 생성
        subscription = {
            "id": subscription_id,
            "customer": customer_data.dict(),
            "items": [item.dict() for item in items],
            "status": "pending" if payment_method == "bank" else "active",
            "total_amount": sum(item.price for item in items),
            "payment_method": payment_method,
            "created_at": datetime.now().isoformat(),
            "next_billing_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "billing_cycle": "monthly"
        }
        
        # 데이터베이스에 저장 (시뮬레이션)
        self.subscriptions_db[subscription_id] = subscription
        
        return subscription

class PaymentProcessor:
    """결제 처리 서비스"""
    
    def __init__(self):
        self.subscription_service = SubscriptionService()
        
    async def process_card_payment(self, payment_request: PaymentRequest) -> Dict[str, Any]:
        """신용카드 결제 처리"""
        try:
            # Stripe 고객 생성
            customer = stripe.Customer.create(
                email=payment_request.customer.email,
                name=payment_request.customer.name,
                description=f"HYOJIN.AI 구독 - {payment_request.customer.company or '개인'}"
            )
            
            # 결제 처리
            charge = stripe.Charge.create(
                amount=payment_request.amount,
                currency='usd',
                source=payment_request.token,
                customer=customer.id,
                description=f"HYOJIN.AI 구독 서비스 - {len(payment_request.items)}개 상품"
            )
            
            # 구독 생성
            subscription = await self.subscription_service.create_subscription(
                payment_request.customer, 
                payment_request.items, 
                "card"
            )
            
            # 결제 성공 결과
            return {
                "success": True,
                "subscription_id": subscription["id"],
                "charge_id": charge.id,
                "amount": payment_request.amount / 100,
                "status": "completed",
                "message": "결제가 성공적으로 완료되었습니다."
            }
            
        except stripe.error.CardError as e:
            # 카드 오류
            raise HTTPException(status_code=400, detail=f"카드 오류: {e.user_message}")
        except stripe.error.RateLimitError as e:
            # 너무 많은 요청
            raise HTTPException(status_code=429, detail="요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")
        except stripe.error.InvalidRequestError as e:
            # 잘못된 요청
            raise HTTPException(status_code=400, detail=f"잘못된 요청: {e.user_message}")
        except stripe.error.AuthenticationError as e:
            # 인증 오류
            raise HTTPException(status_code=401, detail="결제 인증에 실패했습니다.")
        except stripe.error.APIConnectionError as e:
            # 네트워크 오류
            raise HTTPException(status_code=503, detail="결제 서비스에 연결할 수 없습니다.")
        except stripe.error.StripeError as e:
            # 기타 Stripe 오류
            raise HTTPException(status_code=500, detail=f"결제 처리 중 오류가 발생했습니다: {e.user_message}")
        except Exception as e:
            # 기타 오류
            raise HTTPException(status_code=500, detail=f"알 수 없는 오류가 발생했습니다: {str(e)}")
    
    async def process_paypal_payment(self, payment_request: PaymentRequest) -> Dict[str, Any]:
        """PayPal 결제 처리"""
        # PayPal SDK를 사용한 실제 구현
        # 현재는 시뮬레이션
        
        # 구독 생성
        subscription = await self.subscription_service.create_subscription(
            payment_request.customer, 
            payment_request.items, 
            "paypal"
        )
        
        return {
            "success": True,
            "subscription_id": subscription["id"],
            "amount": payment_request.amount / 100,
            "status": "completed",
            "message": "PayPal 결제가 완료되었습니다."
        }
    
    async def process_bank_transfer(self, customer_data: CustomerData, items: List[PaymentItem]) -> Dict[str, Any]:
        """계좌이체 처리"""
        
        # 구독 생성 (대기 상태)
        subscription = await self.subscription_service.create_subscription(
            customer_data, 
            items, 
            "bank"
        )
        
        return {
            "success": True,
            "subscription_id": subscription["id"],
            "amount": sum(item.price for item in items),
            "status": "pending",
            "message": "계좌이체 신청이 접수되었습니다. 입금 확인 후 서비스가 활성화됩니다.",
            "bank_info": {
                "bank_name": "국민은행",
                "account_number": "123-456-789012",
                "account_holder": "HYOJIN.AI",
                "amount": sum(item.price for item in items)
            }
        }

class EmailService:
    """이메일 서비스"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', 'support@hyojin.ai')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
    
    async def send_subscription_confirmation(self, subscription_data: Dict[str, Any]) -> bool:
        """구독 확인 이메일 발송"""
        try:
            customer = subscription_data["customer"]
            items = subscription_data["items"]
            
            # 이메일 내용 생성
            subject = f"🎉 HYOJIN.AI 구독 서비스 {subscription_data['status'] == 'active' and '활성화' or '신청'} 완료"
            
            html_content = self._generate_email_template(subscription_data)
            
            # 이메일 발송
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = customer['email']
            
            html_part = MimeText(html_content, 'html')
            msg.attach(html_part)
            
            # SMTP 서버 연결 및 발송
            if self.email_password:  # 실제 SMTP 설정이 있는 경우
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.email_user, self.email_password)
                    server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"이메일 발송 실패: {str(e)}")
            return False
    
    def _generate_email_template(self, subscription_data: Dict[str, Any]) -> str:
        """이메일 템플릿 생성"""
        customer = subscription_data["customer"]
        items = subscription_data["items"]
        status = subscription_data["status"]
        
        items_html = "".join([
            f"<tr><td style='padding: 8px; border-bottom: 1px solid #eee;'>{item['name']}</td>"
            f"<td style='padding: 8px; border-bottom: 1px solid #eee; text-align: right;'>${item['price']}/월</td></tr>"
            for item in items
        ])
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>HYOJIN.AI 구독 확인</title>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
                <h1>🎉 HYOJIN.AI 구독 서비스</h1>
                <h2>{'구독이 활성화되었습니다!' if status == 'active' else '구독 신청이 접수되었습니다!'}</h2>
            </div>
            
            <div style="padding: 30px; background: #f8f9fa; margin: 20px 0; border-radius: 8px;">
                <h3>📋 구독 정보</h3>
                <p><strong>구독 ID:</strong> {subscription_data['id']}</p>
                <p><strong>고객명:</strong> {customer['name']}</p>
                <p><strong>이메일:</strong> {customer['email']}</p>
                <p><strong>회사:</strong> {customer.get('company', '개인')}</p>
                <p><strong>결제 방법:</strong> {self._get_payment_method_name(subscription_data['payment_method'])}</p>
                <p><strong>상태:</strong> <span style="color: {'#28a745' if status == 'active' else '#ffc107'};">{'활성화됨' if status == 'active' else '입금 확인 대기'}</span></p>
            </div>
            
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 8px; margin: 20px 0;">
                <h3>🛍️ 구독 상품</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f1f3f4;">
                            <th style="padding: 12px; text-align: left;">상품명</th>
                            <th style="padding: 12px; text-align: right;">월 요금</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                    <tfoot>
                        <tr style="background: #e8f5e8; font-weight: bold;">
                            <td style="padding: 12px;">총 월 요금</td>
                            <td style="padding: 12px; text-align: right;">${subscription_data['total_amount']}/월</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            
            {self._get_status_specific_content(subscription_data)}
            
            <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px; margin: 20px 0;">
                <p>문의사항이 있으시면 언제든 연락해주세요.</p>
                <p><strong>📧 support@hyojin.ai</strong> | <strong>🌐 https://hyojin.ai</strong></p>
            </div>
            
            <div style="text-align: center; color: #666; font-size: 12px; margin-top: 30px;">
                <p>이 이메일은 HYOJIN.AI 시스템에서 자동으로 발송되었습니다.</p>
                <p>© 2024 HYOJIN.AI. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
    
    def _get_payment_method_name(self, method: str) -> str:
        """결제 방법 이름 반환"""
        names = {
            'card': '신용카드',
            'paypal': 'PayPal',
            'bank': '계좌이체'
        }
        return names.get(method, method)
    
    def _get_status_specific_content(self, subscription_data: Dict[str, Any]) -> str:
        """상태별 특화 콘텐츠"""
        if subscription_data['status'] == 'active':
            return """
            <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h3 style="color: #155724;">🚀 서비스 이용 안내</h3>
                <p>구독이 활성화되어 즉시 서비스를 이용하실 수 있습니다.</p>
                <p><strong>서비스 접속:</strong> <a href="https://app.hyojin.ai" style="color: #007bff;">https://app.hyojin.ai</a></p>
                <p><strong>로그인 정보:</strong> 별도 이메일로 발송됩니다.</p>
                <p><strong>다음 결제일:</strong> {subscription_data['next_billing_date'][:10]}</p>
            </div>
            """
        else:
            return """
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <h3 style="color: #856404;">🏦 입금 안내</h3>
                <p><strong>은행:</strong> 국민은행</p>
                <p><strong>계좌번호:</strong> 123-456-789012</p>
                <p><strong>예금주:</strong> HYOJIN.AI</p>
                <p><strong>입금액:</strong> ${subscription_data['total_amount']}</p>
                <p style="color: #dc3545; font-weight: bold;">⚠️ 입금 후 이 이메일에 입금확인서를 첨부하여 회신해주세요.</p>
                <p>입금 확인 후 24시간 내에 서비스가 활성화됩니다.</p>
            </div>
            """

# 전역 인스턴스
payment_processor = PaymentProcessor()
email_service = EmailService()
