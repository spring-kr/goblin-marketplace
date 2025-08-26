"""
🏘️ Village Chief System - Vercel 배포용 진입점
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Village Chief 시스템 import (전체 모듈 import)
    import village_chief

    # Flask 앱 가져오기
    app = village_chief.app

    print("✅ Village Chief System 성공적으로 로드됨")

except Exception as e:
    print(f"❌ Village Chief System 로드 실패: {e}")
    # 폴백: 기본 Flask 앱
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def index():
        return (
            """<!DOCTYPE html>
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
    <p><strong>시스템 로딩 실패</strong></p>
    <p>오류: """
            + str(e)
            + """</p>
</body>
</html>"""
        )


# Vercel용 기본 설정
if __name__ != "__main__":
    # Vercel에서 실행될 때
    app.debug = False

# Vercel이 인식할 수 있도록 app을 export
application = app
