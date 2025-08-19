# 🔧 개발 환경 설정

## 환경 변수 템플릿

```env
# 결제 시스템 설정
STRIPE_PUBLISHABLE_KEY=pk_test_example
STRIPE_SECRET_KEY=sk_test_example

# 서버 설정
PORT=8000
HOST=0.0.0.0

# 개발 모드
DEBUG=True
```

## 개발 도구

### 코드 포맷팅
```bash
pip install black flake8
black *.py
flake8 *.py
```

### 테스트 실행
```bash
pip install pytest
pytest tests/
```

---
*개발팀 설정 가이드*
