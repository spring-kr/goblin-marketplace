@echo off
echo =======================================================
echo 🏪 도깨비마을장터 AI 에이전트 시스템 v1.0 시작
echo =======================================================

:: Python 버전 확인
python --version
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

:: 가상환경 확인 및 생성
if not exist "venv" (
    echo 🔧 가상환경 생성 중...
    python -m venv venv
)

:: 가상환경 활성화
echo 🔧 가상환경 활성화...
call venv\Scripts\activate

:: 의존성 설치
echo 📦 필수 패키지 설치 중...
pip install --upgrade pip
pip install -r requirements_commercial_v1.txt

:: 환경 변수 파일 확인
if not exist ".env" (
    if exist ".env.commercial" (
        echo 🔧 환경 변수 파일 생성...
        copy .env.commercial .env
    ) else (
        echo ⚠️ 환경 변수 파일이 없습니다. .env.commercial을 참고하여 .env 파일을 생성하세요.
    )
)

:: 시스템 시작
echo 🚀 시스템 시작 중...
python commercial_launcher_v1.py dev

pause
