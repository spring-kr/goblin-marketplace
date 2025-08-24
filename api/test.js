module.exports = (req, res) => {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.status(200).send(`
    <!DOCTYPE html>
    <html>
    <head>
        <title>도깨비 테스트</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>🧌 도깨비마을장터</h1>
        <p>Node.js 버전으로 테스트 중!</p>
        <p>이제 다운로드되지 않고 웹페이지로 나오나요?</p>
    </body>
    </html>
  `);
};
