const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// MIME 타입 강제 설정
app.use((req, res, next) => {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache');
  next();
});

// 정적 파일 제공
app.use(express.static('.'));

// 모든 요청을 index.html로
app.get('*', (req, res) => {
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
  console.log(`🧌 도깨비마을장터 서버 실행: http://localhost:${port}`);
});
