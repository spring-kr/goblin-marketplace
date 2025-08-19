# 💳 결제 시스템 가이드

## 결제 시스템 구성

### 주요 파일들
- `payment_service.py` - 실제 Stripe/PayPal 결제 처리
- `payment_service_simple.py` - 테스트용 간소화 결제
- `payment_manager_app.py` - 윈도우 관리 앱
- `payment_admin_dashboard.html` - 관리자 대시보드
- `payment_success.html` - 결제 성공 페이지

### 결제 흐름
1. 사용자 결제 요청
2. 결제 정보 검증
3. 외부 결제 게이트웨이 연동
4. 결제 결과 처리
5. 사용자 알림

### 테스트 모드
```python
# 테스트용 카드 번호
CARD_NUMBER = "4242424242424242"
CVC = "123"
EXPIRY = "12/34"
```

### 환경 변수
```env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

---
*결제팀 문서*
