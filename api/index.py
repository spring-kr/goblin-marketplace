from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """<!DOCTYPE html>
<html>
<head>
    <title>🧌 도깨비마을장터</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #4CAF50; }
    </style>
</head>
<body>
    <h1>🧌 도깨비마을장터</h1>
    <p><strong>성공! 웹페이지가 정상적으로 표시되었습니다!</strong></p>
    <p>더 이상 다운로드되지 않아요! 🎉</p>
    <button onclick="alert('도깨비 버튼 클릭!')">도깨비 버튼</button>
</body>
</html>"""

# Vercel이 자동으로 인식하는 Flask 앱
if __name__ == "__main__":
    app.run(debug=True)
