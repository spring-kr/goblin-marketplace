@echo off
echo =======================================================
echo 🏪 도깨비마을장터 간단한 AI 에이전트 시스템 v1.0 시작
echo =======================================================

:: Python 버전 확인
python --version
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo Python 3.7 이상을 설치해주세요.
    pause
    exit /b 1
)

:: 필수 패키지 설치 (간단 버전)
echo 📦 필수 패키지 설치 중...
pip install flask

:: 콘솔 모드 또는 웹 모드 선택
echo.
echo 실행 모드를 선택하세요:
echo 1. 콘솔 모드 (터미널에서 대화)
echo 2. 웹 모드 (브라우저에서 대화)
echo.
set /p mode="모드 선택 (1 또는 2): "

if "%mode%"=="1" (
    echo 🚀 콘솔 모드로 시작 중...
    python simple_commercial_ai_v1.py
) else if "%mode%"=="2" (
    echo 🚀 웹 모드로 시작 중...
    echo 🌐 브라우저에서 http://localhost:5000 을 열어주세요.
    python simple_web_server_v1.py
) else (
    echo ❌ 잘못된 선택입니다. 다시 실행해주세요.
    pause
    exit /b 1
)

pause
