# 🧪 테스트 환경 설정 가이드

## 테스트 데이터베이스 설정

### SQLite 데이터베이스 초기화
```python
# add_test_data.py 실행으로 테스트 DB 생성
python add_test_data.py
```

### 테스트 데이터 구조
```sql
-- 고객 테이블
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT
);

-- 결제 테이블  
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    date TEXT,
    product TEXT
);
```

## 데모 환경 테스트

### 브라우저 테스트
- Chrome, Firefox, Safari 호환성 확인
- 모바일 반응형 디자인 테스트
- JavaScript 기능 동작 확인

### 성능 테스트
- 페이지 로딩 속도
- 데이터 처리 성능
- 메모리 사용량

### 보안 테스트
- XSS 방어 확인
- CSRF 토큰 검증
- 입력 데이터 검증

---
*테스트 팀 문서*
