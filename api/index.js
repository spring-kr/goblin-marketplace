module.exports = (req, res) => {
  // CORS 헤더 설정
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // HTML 콘텐츠 타입 명시적 설정
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache');
  
  const html = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧌 도깨비마을장터</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
            animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 { 
            color: #333; 
            margin-bottom: 20px; 
            font-size: 3em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .goblin { 
            font-size: 6em; 
            margin-bottom: 20px; 
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        p { 
            color: #666; 
            line-height: 1.8; 
            margin-bottom: 15px; 
            font-size: 1.2em;
        }
        .success {
            background: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: bold;
            font-size: 1.3em;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            margin: 10px;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .status {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="status">✅ Node.js 서버 실행중</div>
    
    <div class="container">
        <div class="goblin">🧌</div>
        <h1>도깨비마을장터</h1>
        
        <div class="success">
            🎉 드디어 성공! 🎉<br>
            웹페이지가 정상적으로 표시됩니다!
        </div>
        
        <p><strong>Node.js 서버리스 함수로 동작중!</strong></p>
        <p>더 이상 파일 다운로드가 되지 않아요!</p>
        <p>32명의 전문가 도깨비들이 곧 돌아올 예정이에요! ✨</p>
        
        <button onclick="testFunction()">🧌 도깨비 테스트</button>
        <button onclick="showTime()">⏰ 현재 시간</button>
        
        <div id="result" style="margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 8px; display: none;"></div>
    </div>

    <script>
        console.log('🧌 도깨비마을장터 Node.js 버전 로드 완료!');
        
        function testFunction() {
            const result = document.getElementById('result');
            result.style.display = 'block';
            result.innerHTML = '<strong>🧌 도깨비 테스트 성공!</strong><br>JavaScript도 정상 동작합니다!';
        }
        
        function showTime() {
            const result = document.getElementById('result');
            const now = new Date();
            result.style.display = 'block';
            result.innerHTML = '<strong>⏰ 현재 시간:</strong><br>' + now.toLocaleString('ko-KR');
        }
        
        // 페이지 로드 완료 시
        window.addEventListener('load', function() {
            console.log('페이지 로드 완료 - 다운로드 문제 해결!');
        });
    </script>
</body>
</html>`;

  res.status(200).send(html);
};
