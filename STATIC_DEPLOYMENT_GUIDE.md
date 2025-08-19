# 🚀 배포 시스템 설정 가이드

## GitHub Pages 설정

### .nojekyll 파일
- Jekyll 처리 비활성화
- 정적 파일 직접 제공
- 빌드 시간 단축

### 배포 트리거

#### deploy_trigger.py
- 배포 강제 실행용 스크립트
- 버전 관리 및 변경사항 추적
- Render/Railway 자동 배포 트리거

```python
# 배포 버전 확인
python deploy_trigger.py
```

### 정적 파일 관리

#### static/ 디렉토리
- 파비콘 및 이미지 파일
- CSS/JS 라이브러리
- 문서 및 가이드

#### 파일 구조
```
static/
├── favicon.svg      # 브랜드 아이콘
├── README.md        # 정적 파일 가이드
└── ...              # 기타 정적 자원
```

## 배포 플랫폼별 설정

### GitHub Pages
- main 브랜치 자동 배포
- .nojekyll로 Jekyll 비활성화
- 정적 파일 직접 서빙

### Render
- deploy_trigger.py로 배포 트리거
- 환경 변수 자동 주입
- HTTPS 자동 적용

### Railway
- Procfile 기반 배포
- 자동 스케일링
- 로그 모니터링

---
*DevOps 팀 문서*
