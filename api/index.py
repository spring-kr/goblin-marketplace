# Vercel Python Serverless Function
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """<!DOCTYPE html>
<html>
<head>
    <title>도깨비 테스트</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>🧌 도깨비마을장터</h1>
    <p>드디어 성공! 다운로드되지 않고 웹페이지로 표시되나요?</p>
    <script>
        console.log('웹페이지가 정상 로드됨!');
    </script>
</body>
</html>"""

# Vercel에서 필요한 핸들러
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == "__main__":
    app.run(debug=True)
