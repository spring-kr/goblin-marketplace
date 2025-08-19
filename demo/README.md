# 🎯 데모 및 테스트 가이드

## 데모 파일

### service_demo.html
- HYOJIN.AI 가상 서비스 데모 페이지
- 12개 AI 도메인 서비스 시연
- 실시간 인터랙티브 데모

### 실행 방법
```bash
# 브라우저에서 직접 열기
open demo/service_demo.html

# 또는 로컬 서버로 실행
python -m http.server 8000
# 브라우저에서 http://localhost:8000/demo/service_demo.html 접속
```

## 테스트 데이터

### add_test_data.py
- 결제 시스템 테스트용 데이터 생성
- SQLite 데이터베이스에 샘플 데이터 추가
- 랜덤 결제 기록 생성

### 실행 방법
```bash
# 테스트 데이터 생성
python add_test_data.py

# 생성된 데이터 확인
python payment_manager_app.py
```

### 생성되는 데이터
- 고객 정보 (이름, 이메일, 전화번호)
- 결제 내역 (금액, 날짜, 상품)
- 구독 정보 (플랜, 기간, 상태)

---
*QA 팀 가이드*
