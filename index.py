from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>도깨비마을장터</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial; padding: 20px; text-align: center;">
    <h1>🧙‍♂️ 도깨비마을장터</h1>
    <h2>Vercel 배포 성공! 🎉</h2>
    <p>39명 전문가 도깨비 서비스</p>
    <div style="margin: 20px; padding: 20px; background: #f0f0f0; border-radius: 10px;">
        <h3>주요 도깨비들:</h3>
        <p>💼 마케팅도깨비 | 💰 재테크도깨비 | 🧠 심리상담도깨비</p>
        <p>🤖 AI박사도깨비 | 📊 데이터과학도깨비</p>
    </div>
    <button onclick="alert('곧 전체 서비스가 출시됩니다!')" 
            style="padding: 15px 30px; background: #4CAF50; color: white; border: none; border-radius: 10px; font-size: 16px;">
        🚀 서비스 시작하기
    </button>
</body>
</html>
    """)

@app.route("/api/status")
def status():
    return jsonify({"status": "ok", "message": "도깨비마을장터 v11.7", "goblins": 39})

if __name__ == "__main__":
    app.run()
