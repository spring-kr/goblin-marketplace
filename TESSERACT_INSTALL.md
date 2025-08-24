# 📄 Tesseract OCR 설치 가이드

이미지에서 텍스트를 추출하려면 Tesseract OCR 엔진이 필요합니다.

## 🪟 Windows 설치

### 방법 1: 다운로드 설치 (권장)
1. **Tesseract 다운로드**: https://github.com/UB-Mannheim/tesseract/wiki
2. `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (최신 버전) 다운로드
3. 설치 실행 시 **한국어 언어팩 선택** 체크
4. 기본 경로 `C:\Program Files\Tesseract-OCR\` 에 설치

### 방법 2: Chocolatey 사용
```powershell
# 관리자 권한으로 PowerShell 실행
choco install tesseract
```

### 방법 3: Conda 사용
```bash
conda install -c conda-forge tesseract
```

## 🔍 설치 확인

터미널에서 다음 명령어 실행:
```bash
tesseract --version
```

성공하면 버전 정보가 출력됩니다.

## 🚨 설치 없이 사용하기

Tesseract가 설치되지 않아도 AI 기반 이미지 분석은 여전히 작동합니다:
- ✅ 이미지 기본 정보 (크기, 형식 등)
- ✅ AI를 통한 이미지 내용 분석
- ❌ 정확한 텍스트 추출 (OCR)

## 💡 이미지 텍스트 추출 팁

1. **고해상도 이미지 사용**: 300 DPI 이상 권장
2. **명확한 대비**: 검은 텍스트, 흰 배경
3. **수평 정렬**: 기울어진 텍스트는 인식률 저하
4. **지원 형식**: PNG, JPG, JPEG, GIF, BMP

문제가 계속되면 이미지를 PDF로 변환 후 업로드해보세요!
