from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>🧙‍♂️ 도깨비마을장터</h1><p>Vercel 유료플랜 배포 성공!</p>"


if __name__ == "__main__":
    app.run()
