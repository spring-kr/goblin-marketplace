# 📚 API 문서

## 주요 엔드포인트

### 메인 페이지
- `GET /` - 홈페이지
- `GET /shop` - 쇼핑 페이지

### 결제 시스템
- `POST /create-payment-intent` - 결제 인텐트 생성
- `GET /payment-success` - 결제 성공 페이지

### AI 에이전트 관리
- `GET /agents` - 에이전트 목록
- `POST /agents/update` - 에이전트 업데이트

### 관리자 도구
- `GET /admin` - 관리자 대시보드
- `GET /payment-admin` - 결제 관리

## 응답 형식

```json
{
  "status": "success",
  "data": {},
  "message": "Operation completed"
}
```

---
*API 팀 문서*
