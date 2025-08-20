@echo off
echo ========================================
echo 🎯 AI 도깨비마을 STEM 센터 - 자동 시작
echo 전문가급 16도깨비 + 컨텍스트 추적 시스템
echo ========================================

cd /d "d:\도깨비마을장터\hyojin-ai-mvp"

echo 📍 현재 위치: %CD%
echo 🔍 필수 파일 확인 중...

if not exist "main.py" (
    echo ❌ main.py 파일을 찾을 수 없습니다!
    pause
    exit /b 1
)

if not exist "stem_integration_new.py" (
    echo ❌ stem_integration_new.py 파일을 찾을 수 없습니다!
    pause
    exit /b 1
)

echo ✅ 모든 파일 확인 완료!
echo 🚀 서버 시작 중...
echo 📱 브라우저에서 http://localhost:8000 접속하세요
echo ⭐ 종료하려면 Ctrl+C 누르세요
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
