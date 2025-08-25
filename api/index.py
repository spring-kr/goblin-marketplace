"""
🏘️ Village Chief System - Vercel 배포용 진입점
"""
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Village Chief 시스템 경로 추가
village_chief_path = os.path.join(parent_dir, 'goblin-ai-agent', 'village-chief-system', 'functions')
sys.path.insert(0, village_chief_path)

try:
    # Village Chief 시스템 import
    from village_chief import VillageChief
    
    # Flask 앱 인스턴스 생성
    village_chief = VillageChief()
    app = village_chief.app
    
    print("✅ Village Chief System 성공적으로 로드됨")
    
except Exception as e:
    print(f"❌ Village Chief System 로드 실패: {e}")
    # 폴백: 기본 Flask 앱
    from flask import Flask
    app = Flask(__name__)
    
    @app.route("/")
    def index():
        return """<!DOCTYPE html>
<html>
<head>
    <title>🏘️ Village Chief System</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #4CAF50; }
    </style>
</head>
<body>
    <h1>🏘️ Village Chief System</h1>
    <p><strong>시스템 로딩 중...</strong></p>
    <p>잠시만 기다려주세요! �</p>
</body>
</html>"""

# Vercel용 기본 설정
if __name__ != "__main__":
    # Vercel에서 실행될 때
    app.debug = False

# Vercel이 인식할 수 있도록 app을 export
application = app

if __name__ == "__main__":
    # 로컬 개발 환경에서만 실행
    app.run(host='0.0.0.0', port=5002, debug=True)
