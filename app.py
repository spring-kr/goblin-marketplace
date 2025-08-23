from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🧙‍♂️ 도깨비마을장터</h1>
    <h2>Vercel 유료플랜 배포 성공! 🎉</h2>
    <p>39명 전문가 도깨비 서비스</p>
    '''

if __name__ == '__main__':
    app.run()
