/**
 * 🏪 도깨비마을장터 상용 AI 에이전트 웹 서버
 * Express + Socket.IO 기반 실시간 웹 애플리케이션
 */

import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import winston from 'winston';

import CommercialAIAgentSystem from './CommercialAIAgent.js';

// ES Module에서 __dirname 구하기
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 환경 변수 로드
dotenv.config();

// 로거 설정
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'commercial-ai-server' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Express 앱 초기화
const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CORS_ORIGINS || "*",
    methods: ["GET", "POST"]
  }
});

// AI 시스템 인스턴스
let aiSystem = null;

// 미들웨어 설정
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "ws:", "wss:"],
    },
  },
}));

app.use(compression());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15분
  max: 100, // 최대 100 요청
  message: { error: '너무 많은 요청입니다. 잠시 후 다시 시도해주세요.' }
});
app.use('/api/', limiter);

// Socket.IO 클라이언트 파일 제공
app.get('/socket.io/socket.io.js', (req, res) => {
  res.sendFile(path.join(__dirname, '../node_modules/socket.io/client-dist/socket.io.js'));
});

// Favicon 제공
app.get('/favicon.ico', (req, res) => {
  res.status(204).end();
});

// 메인 페이지 라우트 (정적 파일 서빙보다 먼저)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// 정적 파일 서빙
app.use(express.static(path.join(__dirname, '../public')));

// AI 시스템 초기화
async function initializeAISystem() {
  try {
    logger.info('AI 시스템 초기화 시작...');
    aiSystem = new CommercialAIAgentSystem();
    
    // 초기화 완료 대기
    await new Promise((resolve) => {
      aiSystem.on('initialized', resolve);
    });
    
    logger.info('✅ AI 시스템 초기화 완료');
    return aiSystem;
  } catch (error) {
    logger.error('❌ AI 시스템 초기화 실패:', error);
    throw error;
  }
}

// 전문가 목록 API
app.get('/api/experts', async (req, res) => {
  try {
    if (!aiSystem) {
      return res.status(503).json({
        success: false,
        error: '시스템이 아직 초기화되지 않았습니다.'
      });
    }

    const experts = aiSystem.getExpertList();
    res.json({
      success: true,
      experts
    });
  } catch (error) {
    logger.error('전문가 목록 조회 실패:', error);
    res.status(500).json({
      success: false,
      error: '전문가 목록을 불러올 수 없습니다.'
    });
  }
});

// 채팅 API
app.post('/api/chat', async (req, res) => {
  try {
    if (!aiSystem) {
      return res.status(503).json({
        success: false,
        error: '시스템이 아직 초기화되지 않았습니다.'
      });
    }

    const { message, expertId } = req.body;

    if (!message || typeof message !== 'string' || message.trim().length === 0) {
      return res.status(400).json({
        success: false,
        error: '유효한 메시지를 입력해주세요.'
      });
    }

    if (message.length > 2000) {
      return res.status(400).json({
        success: false,
        error: '메시지가 너무 깁니다. (최대 2000자)'
      });
    }

    const response = await aiSystem.processUserMessage(message.trim(), expertId);
    
    res.json({
      success: true,
      response
    });

  } catch (error) {
    logger.error('채팅 처리 실패:', error);
    res.status(500).json({
      success: false,
      error: '죄송합니다. 답변 생성 중 오류가 발생했습니다.'
    });
  }
});

// 대화 히스토리 API
app.get('/api/history', async (req, res) => {
  try {
    if (!aiSystem) {
      return res.status(503).json({
        success: false,
        error: '시스템이 아직 초기화되지 않았습니다.'
      });
    }

    const limit = Math.min(parseInt(req.query.limit) || 20, 100);
    const history = aiSystem.getConversationHistory(limit);
    
    res.json({
      success: true,
      history
    });
  } catch (error) {
    logger.error('히스토리 조회 실패:', error);
    res.status(500).json({
      success: false,
      error: '대화 히스토리를 불러올 수 없습니다.'
    });
  }
});

// 시스템 상태 API
app.get('/api/status', async (req, res) => {
  try {
    if (!aiSystem) {
      return res.json({
        success: true,
        status: {
          isInitialized: false,
          message: '시스템 초기화 중...'
        }
      });
    }

    const status = aiSystem.getSystemStatus();
    res.json({
      success: true,
      status
    });
  } catch (error) {
    logger.error('상태 조회 실패:', error);
    res.status(500).json({
      success: false,
      error: '시스템 상태를 확인할 수 없습니다.'
    });
  }
});

// 헬스체크 API
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Socket.IO 이벤트 핸들러
io.on('connection', (socket) => {
  logger.info(`클라이언트 연결: ${socket.id}`);
  
  // 연결 시 전문가 목록 전송
  if (aiSystem) {
    socket.emit('experts_list', {
      success: true,
      experts: aiSystem.getExpertList()
    });
  }

  // 메시지 처리
  socket.on('send_message', async (data) => {
    try {
      if (!aiSystem) {
        socket.emit('error', {
          message: '시스템이 아직 초기화되지 않았습니다.'
        });
        return;
      }

      const { message, expertId } = data;

      if (!message || typeof message !== 'string' || message.trim().length === 0) {
        socket.emit('error', {
          message: '유효한 메시지를 입력해주세요.'
        });
        return;
      }

      logger.info(`메시지 수신 [${socket.id}]: ${message.substring(0, 50)}...`);

      // 처리 중 상태 전송
      socket.emit('processing', {
        message: '답변을 생성하고 있습니다...'
      });

      // AI 응답 생성
      const response = await aiSystem.processUserMessage(message.trim(), expertId);

      // 응답 전송
      socket.emit('message_response', {
        success: true,
        response,
        timestamp: new Date().toISOString()
      });

      logger.info(`응답 전송 완료 [${socket.id}]`);

    } catch (error) {
      logger.error(`메시지 처리 실패 [${socket.id}]:`, error);
      socket.emit('error', {
        message: '죄송합니다. 답변 생성 중 오류가 발생했습니다.'
      });
    }
  });

  // 전문가 목록 요청
  socket.on('get_experts', () => {
    if (aiSystem) {
      socket.emit('experts_list', {
        success: true,
        experts: aiSystem.getExpertList()
      });
    } else {
      socket.emit('error', {
        message: '시스템이 아직 초기화되지 않았습니다.'
      });
    }
  });

  // 히스토리 요청
  socket.on('get_history', (data) => {
    try {
      if (!aiSystem) {
        socket.emit('error', {
          message: '시스템이 아직 초기화되지 않았습니다.'
        });
        return;
      }

      const limit = Math.min(data?.limit || 10, 50);
      const history = aiSystem.getConversationHistory(limit);
      
      socket.emit('history_response', {
        success: true,
        history
      });
    } catch (error) {
      logger.error('히스토리 조회 실패:', error);
      socket.emit('error', {
        message: '대화 히스토리를 불러올 수 없습니다.'
      });
    }
  });

  // 연결 해제
  socket.on('disconnect', () => {
    logger.info(`클라이언트 연결 해제: ${socket.id}`);
  });

  // 에러 처리
  socket.on('error', (error) => {
    logger.error(`Socket 에러 [${socket.id}]:`, error);
  });
});

// 전역 에러 핸들러
app.use((err, req, res, next) => {
  logger.error('전역 에러:', err);
  res.status(500).json({
    success: false,
    error: '내부 서버 오류가 발생했습니다.'
  });
});

// 404 핸들러
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: '요청한 리소스를 찾을 수 없습니다.'
  });
});

// 서버 시작
async function startServer() {
  try {
    // AI 시스템 초기화
    await initializeAISystem();

    const port = process.env.PORT || 3000;
    const host = process.env.HOST || '0.0.0.0';

    server.listen(port, host, () => {
      logger.info('=' .repeat(60));
      logger.info('🚀 도깨비마을장터 상용 AI 에이전트 서버 v1.0 시작!');
      logger.info(`🌐 서버 주소: http://${host}:${port}`);
      logger.info(`🔧 환경: ${process.env.NODE_ENV || 'development'}`);
      logger.info(`📊 전문가 수: ${aiSystem.getExpertList().length}명`);
      logger.info('=' .repeat(60));
    });

    // Graceful shutdown
    process.on('SIGTERM', () => {
      logger.info('SIGTERM 신호 수신. 서버를 정상 종료합니다...');
      server.close(() => {
        logger.info('서버가 정상적으로 종료되었습니다.');
        process.exit(0);
      });
    });

    process.on('SIGINT', () => {
      logger.info('SIGINT 신호 수신. 서버를 정상 종료합니다...');
      server.close(() => {
        logger.info('서버가 정상적으로 종료되었습니다.');
        process.exit(0);
      });
    });

  } catch (error) {
    logger.error('서버 시작 실패:', error);
    process.exit(1);
  }
}

// 서버 시작
startServer();

export { app, server, io };
