from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('goblin_market_v11.html')


@app.route("/mobile")
def mobile():
    return render_template('goblin_mobile_v11.html')


@app.route("/api/test")
def api_test():
    return {"status": "success", "message": "도깨비마을장터 API 테스트 성공!", "experts": 16}


if __name__ == "__main__":
    app.run(debug=True)
