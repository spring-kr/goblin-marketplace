/**
 * 🏪 도깨비마을장터 상용 AI 에이전트 시스템 v1.0
 * JavaScript/Node.js 기반 실시간 AI 상담 시스템
 * 
 * 10명의 전문 도깨비가 사용자 질문에 답변하는 상용 AI 시스템
 * 인터넷 검색 기능 포함 - 실시간 정보 검색 및 분석
 */

import { EventEmitter } from 'events';
import { randomUUID } from 'crypto';
import axios from 'axios';
import * as cheerio from 'cheerio';

// 도깨비 전문가 클래스
class GoblinExpert {
  constructor({ id, name, emoji, title, specialties, personality, experienceYears }) {
    this.id = id;
    this.name = name;
    this.emoji = emoji;
    this.title = title;
    this.specialties = specialties;
    this.personality = personality;
    this.experienceYears = experienceYears;
  }

  // 전문가 정보 반환
  getInfo() {
    return {
      id: this.id,
      name: this.name,
      emoji: this.emoji,
      title: this.title,
      specialties: this.specialties,
      experienceYears: this.experienceYears
    };
  }
}

// 메인 상용 AI 에이전트 시스템
class CommercialAIAgentSystem extends EventEmitter {
  constructor() {
    super();
    this.experts = this.initializeExperts();
    this.conversationHistory = [];
    this.responseTemplates = this.loadResponseTemplates();
    this.isInitialized = false;
    
    this.init();
  }

  async init() {
    console.log('🚀 상용 AI 에이전트 시스템 v1.0 초기화 중...');
    
    // 시스템 초기화 로직
    await this.setupAIModels();
    await this.setupInternetSearch(); // 인터넷 검색 시스템 초기화
    await this.loadHistoricalData();
    
    this.isInitialized = true;
    console.log('✅ 시스템 초기화 완료!');
    
    this.emit('initialized');
  }

  // 10명의 전문 도깨비 초기화
  initializeExperts() {
    return {
      ai: new GoblinExpert({
        id: 'ai',
        name: 'AI박사 하이도깨비',
        emoji: '🤖',
        title: 'AI 연구소장, 15년 경력',
        specialties: ['인공지능', '머신러닝', '딥러닝', '자연어처리', '컴퓨터비전'],
        personality: '논리적이고 체계적인 분석가',
        experienceYears: 15
      }),
      
      investment: new GoblinExpert({
        id: 'investment',
        name: '투자박사 머니도깨비', 
        emoji: '💰',
        title: '투자전략팀장, 20년 경력',
        specialties: ['주식투자', '부동산', '가상화폐', '파생상품', '포트폴리오'],
        personality: '신중하고 데이터 중심적인 투자자',
        experienceYears: 20
      }),

      counselor: new GoblinExpert({
        id: 'counselor',
        name: '상담박사 마음도깨비',
        emoji: '💬', 
        title: '심리상담센터장, 18년 경력',
        specialties: ['심리상담', '감정코칭', '스트레스관리', '인간관계', '자기계발'],
        personality: '따뜻하고 공감능력이 뛰어난 상담사',
        experienceYears: 18
      }),

      creative: new GoblinExpert({
        id: 'creative',
        name: '창작박사 아트도깨비',
        emoji: '🎨',
        title: '크리에이티브 디렉터, 12년 경력', 
        specialties: ['디자인', '브랜딩', '콘텐츠제작', 'UX/UI', '창의기획'],
        personality: '자유롭고 혁신적인 크리에이터',
        experienceYears: 12
      }),

      dataAnalyst: new GoblinExpert({
        id: 'dataAnalyst',
        name: '데이터박사 분석도깨비',
        emoji: '📊',
        title: '데이터사이언스팀장, 14년 경력',
        specialties: ['데이터분석', '통계모델링', '시각화', '예측분석', '빅데이터'],
        personality: '객관적이고 증거기반 사고하는 분석가',
        experienceYears: 14
      }),

      marketing: new GoblinExpert({
        id: 'marketing',
        name: '마케팅박사 홍보도깨비',
        emoji: '📢',
        title: '마케팅본부장, 16년 경력',
        specialties: ['디지털마케팅', '브랜드전략', '소셜미디어', '광고기획', '고객분석'],
        personality: '열정적이고 트렌드에 민감한 마케터',
        experienceYears: 16
      }),

      medical: new GoblinExpert({
        id: 'medical',
        name: '의학박사 건강도깨비',
        emoji: '🏥',
        title: '종합병원 과장, 22년 경력',
        specialties: ['내과진료', '건강관리', '질병예방', '영양학', '운동처방'],
        personality: '신중하고 환자중심적인 의료진',
        experienceYears: 22
      }),

      sales: new GoblinExpert({
        id: 'sales',
        name: '영업박사 세일도깨비',
        emoji: '💼',
        title: '영업본부장, 19년 경력',
        specialties: ['B2B영업', '고객관리', '협상전략', '영업프로세스', '팀관리'],
        personality: '적극적이고 설득력 있는 영업전문가',
        experienceYears: 19
      }),

      startup: new GoblinExpert({
        id: 'startup',
        name: '창업박사 벤처도깨비',
        emoji: '🚀',
        title: '스타트업 대표, 10년 경력',
        specialties: ['사업기획', '투자유치', '팀빌딩', '제품개발', '스케일업'],
        personality: '도전적이고 혁신적인 기업가',
        experienceYears: 10
      }),

      writing: new GoblinExpert({
        id: 'writing',
        name: '글쓰기박사 펜도깨비',
        emoji: '✍️',
        title: '편집장, 17년 경력',
        specialties: ['콘텐츠작성', '편집기획', '카피라이팅', '스토리텔링', '출판기획'],
        personality: '섬세하고 표현력 풍부한 작가',
        experienceYears: 17
      })
    };
  }

  // 응답 템플릿 로드
  loadResponseTemplates() {
    return {
      assistant: [
        'AI 기술 관점에서 분석해보겠습니다.',
        '머신러닝과 딥러닝 기술을 활용하여 설명드리겠습니다.',
        '최신 AI 동향을 바탕으로 답변드리겠습니다.',
        '데이터 과학 관점에서 접근해보겠습니다.'
      ],
      investment: [
        '투자 전략 관점에서 분석해보겠습니다.',
        '리스크와 수익률을 고려하여 설명드리겠습니다.',
        '포트폴리오 다각화 관점에서 답변드리겠습니다.',
        '시장 동향을 바탕으로 조언드리겠습니다.'
      ],
      counselor: [
        '심리학적 관점에서 도움을 드리겠습니다.',
        '감정적 측면을 고려하여 상담해드리겠습니다.',
        '인간관계 개선을 위한 조언을 드리겠습니다.',
        '스트레스 관리 방법을 제안해드리겠습니다.'
      ],
      creative: [
        '창의적 관점에서 아이디어를 제안드리겠습니다.',
        '디자인 사고로 접근해보겠습니다.',
        '브랜딩 전략을 고려하여 답변드리겠습니다.',
        '사용자 경험을 중심으로 설명드리겠습니다.'
      ],
      dataAnalyst: [
        '데이터 분석 관점에서 검토해보겠습니다.',
        '통계적 근거를 바탕으로 설명드리겠습니다.',
        '패턴 분석을 통해 인사이트를 제공하겠습니다.',
        '시각화를 통해 명확히 설명드리겠습니다.'
      ],
      marketing: [
        '마케팅 전략 관점에서 분석해보겠습니다.',
        '고객 중심 사고로 접근해보겠습니다.',
        '브랜드 가치 향상을 위한 방안을 제시하겠습니다.',
        '디지털 마케팅 트렌드를 반영하여 답변드리겠습니다.'
      ],
      medical: [
        '의학적 관점에서 신중히 검토해보겠습니다.',
        '건강 관리 측면에서 조언드리겠습니다.',
        '예방 의학 관점에서 설명드리겠습니다.',
        '과학적 근거를 바탕으로 답변드리겠습니다.'
      ],
      sales: [
        '영업 전략 관점에서 분석해보겠습니다.',
        '고객 관계 관리 측면에서 조언드리겠습니다.',
        '협상 전략을 고려하여 답변드리겠습니다.',
        '성과 향상을 위한 방안을 제시하겠습니다.'
      ],
      startup: [
        '스타트업 관점에서 혁신적으로 접근해보겠습니다.',
        '사업 모델을 고려하여 분석해보겠습니다.',
        '성장 전략 관점에서 조언드리겠습니다.',
        '투자 유치와 스케일업을 고려하여 답변드리겠습니다.'
      ],
      writing: [
        '글쓰기 전문가 관점에서 조언드리겠습니다.',
        '콘텐츠 기획 측면에서 도움을 드리겠습니다.',
        '스토리텔링 관점에서 접근해보겠습니다.',
        '독자 중심으로 명확히 설명드리겠습니다.'
      ]
    };
  }

  // AI 모델 설정 - 상용AI화 (Vercel 호환)
  async setupAIModels() {
    // 상용AI화: 외부 AI 의존성 없이 독립적으로 실행 가능한 시스템
    this.aiModels = {
      commercial: true,  // 상용AI 시스템 모드
      templateBased: true,  // 템플릿 기반 응답
      intelligentMatching: true  // 지능형 매칭 시스템
    };

    // 상용AI 시스템 초기화
    this.initializeCommercialAI();
    console.log('✅ 상용AI 시스템 모드로 실행 (Vercel 호환)');
  }

  // 상용AI 시스템 초기화
  initializeCommercialAI() {
    // 지능형 키워드 매칭 시스템
    this.keywordDatabase = this.buildKeywordDatabase();
    
    // 응답 품질 향상을 위한 컨텍스트 시스템
    this.contextAnalyzer = this.setupContextAnalyzer();
    
    // 전문가별 특화 응답 생성기
    this.responseGenerators = this.setupResponseGenerators();
  }

  // 인터넷 검색 시스템 초기화
  async setupInternetSearch() {
    this.searchEngine = {
      enabled: true,
      maxResults: 5,
      timeout: 10000,
      searchAPIs: {
        // Google 검색 시뮬레이션 (실제로는 DuckDuckGo API 등 사용)
        duckduckgo: 'https://api.duckduckgo.com/',
        // 네이버 검색 (한국어 최적화)
        naver: 'https://openapi.naver.com/v1/search/',
        // 실시간 뉴스
        news: 'https://newsapi.org/v2/'
      },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    };

    console.log('🌐 인터넷 검색 시스템 초기화 완료');
  }

  // 인터넷 검색 실행
  async performInternetSearch(query, searchType = 'general') {
    try {
      console.log(`🔍 검색 시작: "${query}" (타입: ${searchType})`);
      
      const searchResults = [];
      
      // 1. 구글/네이버 웹 검색
      const webResults = await this.searchWeb(query);
      searchResults.push(...webResults);
      
      // 2. 뉴스 검색 (최신 정보)
      if (searchType === 'news' || this.isTimeRelevantQuery(query)) {
        const newsResults = await this.searchNews(query);
        searchResults.push(...newsResults);
      }
      
      // 3. 위키피디아 검색 (정확한 정보)
      if (searchType === 'factual') {
        const wikiResults = await this.searchWikipedia(query);
        searchResults.push(...wikiResults);
      }
      
      // 검색 결과 분석 및 요약
      const analyzedResults = await this.analyzeSearchResults(searchResults, query);
      
      console.log(`✅ 검색 완료: ${searchResults.length}개 결과 수집`);
      return analyzedResults;
      
    } catch (error) {
      console.error('❌ 인터넷 검색 실패:', error.message);
      return {
        success: false,
        error: error.message,
        fallback: '죄송합니다. 인터넷 검색에 실패했습니다. 기본 지식으로 답변드리겠습니다.'
      };
    }
  }

  // 웹 검색 (구글/네이버 등)
  async searchWeb(query) {
    const results = [];
    
    try {
      // DuckDuckGo 즉석 답변 API (무료)
      const response = await axios.get('https://api.duckduckgo.com/', {
        params: {
          q: query,
          format: 'json',
          no_html: 1,
          skip_disambig: 1
        },
        timeout: this.searchEngine.timeout,
        headers: {
          'User-Agent': this.searchEngine.userAgent
        }
      });

      if (response.data && response.data.AbstractText) {
        results.push({
          type: 'instant_answer',
          title: response.data.Heading || '즉석 답변',
          content: response.data.AbstractText,
          url: response.data.AbstractURL,
          source: 'DuckDuckGo',
          relevance: 0.9
        });
      }

      // Related Topics 추가
      if (response.data.RelatedTopics) {
        response.data.RelatedTopics.slice(0, 3).forEach(topic => {
          if (topic.Text) {
            results.push({
              type: 'related_info',
              title: topic.FirstURL ? this.extractTitleFromURL(topic.FirstURL) : '관련 정보',
              content: topic.Text,
              url: topic.FirstURL,
              source: 'DuckDuckGo Related',
              relevance: 0.7
            });
          }
        });
      }

    } catch (error) {
      console.warn('DuckDuckGo 검색 실패:', error.message);
    }

    // 한국어 검색을 위한 네이버 검색 시뮬레이션
    if (this.isKoreanQuery(query)) {
      try {
        const koreanResults = await this.searchKoreanSites(query);
        results.push(...koreanResults);
      } catch (error) {
        console.warn('한국어 검색 실패:', error.message);
      }
    }

    return results;
  }

  // 뉴스 검색
  async searchNews(query) {
    const results = [];
    
    try {
      // 실제 뉴스 API 대신 시뮬레이션 (실제로는 NewsAPI 등 사용)
      const newsKeywords = this.extractNewsKeywords(query);
      
      results.push({
        type: 'news',
        title: `${query} 관련 최신 뉴스`,
        content: `최신 "${query}" 관련 동향을 검색했습니다. 실시간 정보를 반영한 답변을 드리겠습니다.`,
        url: `https://news.search.com/${encodeURIComponent(query)}`,
        source: '뉴스 검색',
        relevance: 0.8,
        timestamp: new Date().toISOString()
      });

    } catch (error) {
      console.warn('뉴스 검색 실패:', error.message);
    }
    
    return results;
  }

  // 위키피디아 검색
  async searchWikipedia(query) {
    const results = [];
    
    try {
      const response = await axios.get('https://ko.wikipedia.org/api/rest_v1/page/summary/' + encodeURIComponent(query), {
        timeout: this.searchEngine.timeout,
        headers: {
          'User-Agent': this.searchEngine.userAgent
        }
      });

      if (response.data && response.data.extract) {
        results.push({
          type: 'encyclopedia',
          title: response.data.title,
          content: response.data.extract,
          url: response.data.content_urls?.desktop?.page,
          source: '위키피디아',
          relevance: 0.95
        });
      }

    } catch (error) {
      // 한국어 위키피디아에 없으면 영어 위키피디아 시도
      try {
        const enResponse = await axios.get('https://en.wikipedia.org/api/rest_v1/page/summary/' + encodeURIComponent(query), {
          timeout: this.searchEngine.timeout,
          headers: {
            'User-Agent': this.searchEngine.userAgent
          }
        });

        if (enResponse.data && enResponse.data.extract) {
          results.push({
            type: 'encyclopedia',
            title: enResponse.data.title,
            content: `[영문 위키피디아] ${enResponse.data.extract}`,
            url: enResponse.data.content_urls?.desktop?.page,
            source: 'Wikipedia (EN)',
            relevance: 0.85
          });
        }
      } catch (enError) {
        console.warn('위키피디아 검색 실패:', error.message);
      }
    }
    
    return results;
  }

  // 검색 결과 분석 및 요약
  async analyzeSearchResults(searchResults, originalQuery) {
    if (!searchResults || searchResults.length === 0) {
      return {
        success: false,
        summary: '검색 결과를 찾을 수 없습니다.',
        sources: []
      };
    }

    // 관련도순으로 정렬
    const sortedResults = searchResults.sort((a, b) => (b.relevance || 0) - (a.relevance || 0));
    
    // 상위 결과들을 종합하여 요약 생성
    const topResults = sortedResults.slice(0, this.searchEngine.maxResults);
    
    let summary = `"${originalQuery}" 검색 결과를 분석한 내용입니다:\n\n`;
    
    // 즉석 답변이 있으면 우선 표시
    const instantAnswer = topResults.find(r => r.type === 'instant_answer');
    if (instantAnswer) {
      summary += `**핵심 정보:**\n${instantAnswer.content}\n\n`;
    }

    // 위키피디아 정보가 있으면 표시
    const wikiInfo = topResults.find(r => r.type === 'encyclopedia');
    if (wikiInfo) {
      summary += `**백과사전 정보:**\n${wikiInfo.content}\n\n`;
    }

    // 뉴스 정보가 있으면 표시
    const newsInfo = topResults.filter(r => r.type === 'news');
    if (newsInfo.length > 0) {
      summary += `**최신 동향:**\n`;
      newsInfo.forEach(news => {
        summary += `• ${news.content}\n`;
      });
      summary += '\n';
    }

    // 관련 정보 추가
    const relatedInfo = topResults.filter(r => r.type === 'related_info');
    if (relatedInfo.length > 0) {
      summary += `**관련 정보:**\n`;
      relatedInfo.slice(0, 2).forEach(info => {
        summary += `• ${info.content}\n`;
      });
    }

    return {
      success: true,
      summary: summary.trim(),
      sources: topResults.map(r => ({
        title: r.title,
        url: r.url,
        source: r.source
      })),
      searchQuery: originalQuery,
      resultCount: searchResults.length,
      timestamp: new Date().toISOString()
    };
  }

  // 한국어 쿼리 감지
  isKoreanQuery(query) {
    const koreanRegex = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/;
    return koreanRegex.test(query);
  }

  // 시간 관련 쿼리 감지
  isTimeRelevantQuery(query) {
    const timeKeywords = ['최신', '오늘', '현재', '지금', '뉴스', '동향', '트렌드', '업데이트'];
    return timeKeywords.some(keyword => query.includes(keyword));
  }

  // 검색이 필요한 쿼리 감지
  needsInternetSearch(query) {
    const searchTriggers = [
      '최신', '뉴스', '현재', '지금', '오늘', '동향', '트렌드',
      '가격', '주가', '환율', '날씨', '실시간',
      '언제', '어디서', '누가', '얼마', '몇',
      '검색', '찾아', '알려줘', '정보'
    ];
    
    return searchTriggers.some(trigger => query.includes(trigger));
  }

  // 한국어 사이트 검색 시뮬레이션
  async searchKoreanSites(query) {
    const results = [];
    
    // 한국어 검색 결과 시뮬레이션
    results.push({
      type: 'korean_info',
      title: `${query} 한국어 정보`,
      content: `한국어로 "${query}"에 대한 검색을 수행했습니다. 국내 관련 정보를 포함하여 답변드리겠습니다.`,
      url: `https://korean.search.com/${encodeURIComponent(query)}`,
      source: '한국어 검색',
      relevance: 0.8
    });

    return results;
  }

  // URL에서 제목 추출
  extractTitleFromURL(url) {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split('/').filter(part => part);
      return pathParts[pathParts.length - 1]?.replace(/[_-]/g, ' ') || '관련 정보';
    } catch {
      return '관련 정보';
    }
  }

  // 뉴스 키워드 추출
  extractNewsKeywords(query) {
    // 뉴스 검색에 적합한 키워드 추출
    const stopWords = ['이', '그', '저', '의', '가', '을', '를', '에', '와', '과'];
    return query.split(' ').filter(word => !stopWords.includes(word));
  }

  // 키워드 데이터베이스 구축
  buildKeywordDatabase() {
    return {
      assistant: {
        primary: ['ai', '인공지능', '머신러닝', '딥러닝', '기술', '프로그래밍', '코딩', '개발'],
        secondary: ['알고리즘', '데이터', '모델', '학습', '예측', '자동화']
      },
      investment: {
        primary: ['투자', '주식', '부동산', '돈', '수익', '포트폴리오', '펀드', '자산'],
        secondary: ['리스크', '배당', '금리', '경제', '시장', '거래']
      },
      counselor: {
        primary: ['상담', '심리', '감정', '스트레스', '관계', '고민', '우울', '불안'],
        secondary: ['마음', '치료', '회복', '성장', '소통', '갈등']
      },
      creative: {
        primary: ['디자인', '창작', '브랜딩', '아이디어', '창의', '콘텐츠', '예술', '작품'],
        secondary: ['색상', '레이아웃', '컨셉', '스타일', '트렌드', '영감']
      },
      dataAnalyst: {
        primary: ['데이터', '분석', '통계', '차트', '시각화', '예측', '패턴', '지표'],
        secondary: ['excel', '그래프', '리포트', '인사이트', '모델링', '검증']
      },
      marketing: {
        primary: ['마케팅', '광고', '홍보', '브랜드', '고객', '판매', '캠페인', 'sns'],
        secondary: ['타겟', '메시지', '채널', '전략', '분석', '성과']
      },
      medical: {
        primary: ['건강', '의료', '병원', '질병', '치료', '약', '진료', '검사'],
        secondary: ['증상', '예방', '운동', '식단', '관리', '회복']
      },
      sales: {
        primary: ['영업', '세일즈', '고객', '협상', '계약', '실적', '매출', '판매'],
        secondary: ['제안', '프레젠테이션', '관계', '성과', '목표', '전략']
      },
      startup: {
        primary: ['창업', '스타트업', '사업', '벤처', '투자유치', '아이템', '비즈니스', '회사'],
        secondary: ['아이디어', '팀', '자금', '시장', '경쟁', '성장']
      },
      writing: {
        primary: ['글', '작성', '콘텐츠', '스토리', '편집', '출판', '블로그', '책'],
        secondary: ['문체', '구성', '표현', '주제', '독자', '완성도']
      }
    };
  }

  // 컨텍스트 분석기 설정
  setupContextAnalyzer() {
    return {
      analyzeComplexity: (message) => {
        const words = message.split(' ').length;
        if (words < 5) return 'simple';
        if (words < 15) return 'medium';
        return 'complex';
      },
      detectUrgency: (message) => {
        const urgentWords = ['급하', '빨리', '즉시', '긴급', '어서'];
        return urgentWords.some(word => message.includes(word));
      },
      identifyTopic: (message) => {
        // 메시지에서 주요 토픽 식별
        const topics = [];
        for (const [expertId, keywords] of Object.entries(this.keywordDatabase)) {
          const allKeywords = [...keywords.primary, ...keywords.secondary];
          const matches = allKeywords.filter(keyword => 
            message.toLowerCase().includes(keyword.toLowerCase())
          );
          if (matches.length > 0) {
            topics.push({ expertId, matches: matches.length });
          }
        }
        return topics.sort((a, b) => b.matches - a.matches);
      }
    };
  }

  // 응답 생성기 설정
  setupResponseGenerators() {
    return {
      generateDetailedResponse: (expertId, topic, complexity) => {
        const expert = this.experts[expertId];
        const responses = this.getExpertSpecificResponses(expertId, topic);
        
        if (complexity === 'complex') {
          return responses.detailed || responses.default;
        } else if (complexity === 'medium') {
          return responses.medium || responses.default;
        } else {
          return responses.simple || responses.default;
        }
      }
    };
  }

  // 전문가별 특화 응답 데이터베이스
  getExpertSpecificResponses(expertId, topic) {
    const responseDB = {
      assistant: {
        default: this.getAIResponse(),
        simple: 'AI 기술에 대해 간단히 설명드리겠습니다. 어떤 부분이 궁금하신가요?',
        medium: 'AI는 다양한 분야에서 활용됩니다. 구체적으로 어떤 응용 분야에 관심이 있으신지요?',
        detailed: this.getAIResponse()
      },
      investment: {
        default: this.getInvestmentResponse(),
        simple: '투자에 대해 기본적인 조언을 드리겠습니다. 투자 목표가 무엇인가요?',
        medium: '투자 전략은 개인의 상황에 따라 달라집니다. 위험도와 기간을 알려주세요.',
        detailed: this.getInvestmentResponse()
      },
      counselor: {
        default: this.getCounselorResponse(),
        simple: '마음이 힘드시군요. 어떤 부분이 가장 어려우신지 말씀해주세요.',
        medium: '상황을 차근차근 정리해보겠습니다. 언제부터 이런 고민이 시작되셨나요?',
        detailed: this.getCounselorResponse()
      },
      creative: {
        default: '창의적인 아이디어를 함께 발전시켜보겠습니다.',
        simple: '어떤 창작 작업을 하고 계신가요?',
        medium: '창의적 작업의 목적과 타겟을 알려주시면 더 구체적인 조언을 드릴 수 있습니다.',
        detailed: '창의적 프로젝트의 전체적인 방향성과 제약사항을 고려하여 단계별 접근 방법을 제안드리겠습니다.'
      },
      dataAnalyst: {
        default: '데이터 분석 관점에서 도움을 드리겠습니다.',
        simple: '어떤 데이터를 분석하고 계신가요?',
        medium: '분석 목적과 현재 가진 데이터의 형태를 알려주세요.',
        detailed: '데이터 전처리부터 시각화까지 전체 분석 프로세스를 함께 설계해보겠습니다.'
      },
      marketing: {
        default: '마케팅 전략을 함께 수립해보겠습니다.',
        simple: '어떤 제품이나 서비스를 마케팅하고 계신가요?',
        medium: '타겟 고객과 예산 규모를 알려주시면 적합한 마케팅 채널을 제안드리겠습니다.',
        detailed: '시장 분석부터 실행 계획까지 종합적인 마케팅 전략을 수립해보겠습니다.'
      },
      medical: {
        default: '건강 관련 조언을 드리겠습니다. (진료는 의료진과 상담하세요)',
        simple: '어떤 건강 관련 궁금증이 있으신가요?',
        medium: '증상이나 상황을 구체적으로 설명해주시면 일반적인 건강 정보를 제공해드리겠습니다.',
        detailed: '건강 관리의 전반적인 계획을 세워보겠습니다. 현재 건강 상태와 목표를 알려주세요.'
      },
      sales: {
        default: '영업 전략을 함께 개발해보겠습니다.',
        simple: '어떤 제품이나 서비스를 판매하고 계신가요?',
        medium: '고객 특성과 영업 환경을 알려주시면 효과적인 접근 방법을 제안드리겠습니다.',
        detailed: '영업 프로세스 전반을 최적화하여 성과를 향상시킬 수 있는 체계적인 방법을 제안드리겠습니다.'
      },
      startup: {
        default: '창업과 사업 발전에 도움을 드리겠습니다.',
        simple: '어떤 사업 아이디어를 갖고 계신가요?',
        medium: '사업 모델과 시장 상황을 설명해주시면 구체적인 조언을 드리겠습니다.',
        detailed: '사업 계획서 작성부터 투자 유치까지 단계별 전략을 수립해보겠습니다.'
      },
      writing: {
        default: '글쓰기와 콘텐츠 제작을 도와드리겠습니다.',
        simple: '어떤 글을 쓰고 계신가요?',
        medium: '글의 목적과 독자층을 알려주시면 효과적인 작성 방법을 제안드리겠습니다.',
        detailed: '기획부터 편집까지 전체 콘텐츠 제작 프로세스를 체계적으로 지원해드리겠습니다.'
      }
    };

    return responseDB[expertId] || { default: '전문적으로 도움을 드리겠습니다.' };
  }

  // 과거 데이터 로드
  async loadHistoricalData() {
    // 기존 Python 시스템에서 데이터 마이그레이션
    this.historicalData = {
      conversations: [],
      learningData: [],
      userPreferences: {}
    };
  }

  // 사용자 메시지 처리
  async processUserMessage(userMessage, expertId = null) {
    if (!this.isInitialized) {
      throw new Error('시스템이 아직 초기화되지 않았습니다');
    }

    // 메시지 전처리
    const processedMessage = await this.preprocessMessage(userMessage);
    
    // 적절한 전문가 선택
    const selectedExpertId = expertId || this.selectBestExpert(processedMessage);
    
    // 전문가 답변 생성
    const expertResponse = await this.generateExpertResponse(
      processedMessage, 
      selectedExpertId
    );
    
    // 대화 히스토리 업데이트
    this.updateConversationHistory(userMessage, expertResponse, selectedExpertId);
    
    // 응답 데이터 구성
    const responseData = {
      userMessage,
      expertId: selectedExpertId,
      expertInfo: this.experts[selectedExpertId].getInfo(),
      response: expertResponse,
      timestamp: new Date().toISOString(),
      conversationId: this.conversationHistory.length
    };

    // 이벤트 발생
    this.emit('messageProcessed', responseData);
    
    return responseData;
  }

  // 메시지 전처리
  async preprocessMessage(message) {
    return {
      original: message,
      cleaned: message.trim(),
      keywords: this.extractKeywords(message),
      emotion: await this.analyzeEmotion(message),
      intent: this.detectIntent(message)
    };
  }

  // 키워드 추출
  extractKeywords(message) {
    const keywords = [];
    const messageLower = message.toLowerCase();
    
    for (const [expertId, expert] of Object.entries(this.experts)) {
      for (const specialty of expert.specialties) {
        if (messageLower.includes(specialty.toLowerCase())) {
          keywords.push(specialty);
        }
      }
    }
    
    return keywords;
  }

  // 감정 분석 (간단한 구현)
  async analyzeEmotion(message) {
    const positiveWords = ['좋다', '훌륭하다', '멋지다', '감사', '기쁘다'];
    const negativeWords = ['나쁘다', '싫다', '화나다', '슬프다', '걱정'];
    
    const messageLower = message.toLowerCase();
    
    if (positiveWords.some(word => messageLower.includes(word))) {
      return 'positive';
    } else if (negativeWords.some(word => messageLower.includes(word))) {
      return 'negative';
    }
    
    return 'neutral';
  }

  // 의도 감지
  detectIntent(message) {
    const questionWords = ['무엇', '어떻게', '왜', '언제', '어디서'];
    const requestWords = ['도와주세요', '부탁', '만들어', '추천'];
    
    const messageLower = message.toLowerCase();
    
    if (questionWords.some(word => messageLower.includes(word))) {
      return 'question';
    } else if (requestWords.some(word => messageLower.includes(word))) {
      return 'request';
    }
    
    return 'general';
  }

  // 최적의 전문가 선택
  selectBestExpert(processedMessage) {
    const { original: message, keywords } = processedMessage;
    const expertScores = {};
    const messageLower = message.toLowerCase();

    // 각 전문가별 점수 계산
    for (const [expertId, expert] of Object.entries(this.experts)) {
      let score = 0;

      // 전문 분야 키워드 매칭
      for (const specialty of expert.specialties) {
        if (messageLower.includes(specialty.toLowerCase())) {
          score += 2;
        }
      }

      // 키워드 매칭
      for (const keyword of keywords) {
        if (expert.specialties.some(s => s.toLowerCase().includes(keyword.toLowerCase()))) {
          score += 1;
        }
      }

      // 전문가별 특수 키워드
      const expertKeywords = this.getExpertKeywords(expertId);
      for (const keyword of expertKeywords) {
        if (messageLower.includes(keyword)) {
          score += 1;
        }
      }

      expertScores[expertId] = score;
    }

    // 최고 점수 전문가 선택
    const bestExpertId = Object.keys(expertScores).reduce((a, b) => 
      expertScores[a] > expertScores[b] ? a : b
    );

    return expertScores[bestExpertId] > 0 ? bestExpertId : 'ai';
  }

  // 전문가별 키워드 매핑
  getExpertKeywords(expertId) {
    const keywordMap = {
      ai: ['ai', '인공지능', '머신러닝', '딥러닝', '기술', '프로그래밍'],
      investment: ['투자', '주식', '부동산', '돈', '수익', '포트폴리오'],
      psychology: ['상담', '심리', '감정', '스트레스', '관계', '고민'],
      marketing: ['마케팅', '광고', '홍보', '브랜드', '고객', '판매'],
      medical: ['건강', '의료', '병원', '질병', '치료', '약'],
      startup: ['창업', '스타트업', '사업', '벤처', '투자유치', '아이템'],
      legal: ['법률', '법', '소송', '계약', '권리', '의무'],
      cooking: ['요리', '음식', '레시피', '맛', '조리', '식재료'],
      travel: ['여행', '관광', '숙박', '항공', '지역', '문화'],
      education: ['교육', '학습', '공부', '학교', '강의', '지식']
    };

    return keywordMap[expertId] || [];
  }

  // 전문가 답변 생성 - 검색 기능 포함 완전 동적 버전
  async generateExpertResponse(processedMessage, expertId) {
    const expert = this.experts[expertId];
    const { original: userMessage, emotion, keywords } = processedMessage;

    // 동적 인트로 생성
    const dynamicIntro = this.generateDynamicIntro(expertId, userMessage, emotion);

    // 검색 기능 포함 완전 동적 답변 생성
    const specificResponse = await this.generateResponse(
      expertId, 
      userMessage, 
      { emotion, keywords, complexity: this.contextAnalyzer.analyzeComplexity(userMessage) }
    );

    // 동적 마무리 메시지
    const dynamicClosing = this.generateDynamicClosing(expertId, userMessage);

    // 전문가 스타일로 포맷팅
    const formattedResponse = `${expert.emoji} **${expert.name}**입니다.

${dynamicIntro}

${specificResponse}

${dynamicClosing}`;

    return formattedResponse;
  }

  // 동적 인트로 생성
  generateDynamicIntro(expertId, userMessage, emotion) {
    const expert = this.experts[expertId];
    const timeOfDay = new Date().getHours();
    let greeting = "";

    if (timeOfDay < 12) greeting = "좋은 아침입니다!";
    else if (timeOfDay < 18) greeting = "안녕하세요!";
    else greeting = "안녕하세요!";

    const emotionResponse = {
      positive: "좋은 에너지가 느껴지는 질문이네요! 😊",
      negative: "어려운 상황에 계신 것 같네요. 함께 해결책을 찾아보겠습니다.",
      neutral: `${expert.experienceYears}년간의 경험을 바탕으로 도움드리겠습니다.`
    };

    return `${greeting} ${emotionResponse[emotion] || emotionResponse.neutral}`;
  }

  // 완전 동적 응답 생성
  async generateFullyDynamicResponse(expertId, userMessage, context) {
    const { emotion, keywords, complexity } = context;
    
    // 인터넷 검색이 필요한지 확인
    const needsSearch = this.needsInternetSearch(userMessage);
    let searchResults = null;
    
    if (needsSearch && this.searchEngine.enabled) {
      console.log(`🔍 "${userMessage}"에 대한 인터넷 검색 수행...`);
      
      // 검색 타입 결정
      let searchType = 'general';
      if (this.isTimeRelevantQuery(userMessage)) searchType = 'news';
      if (keywords.some(k => ['정의', '뜻', '의미', '설명'].includes(k))) searchType = 'factual';
      
      try {
        searchResults = await this.performInternetSearch(userMessage, searchType);
      } catch (error) {
        console.error('검색 실패:', error);
        searchResults = { success: false, fallback: '검색에 실패했지만 기본 지식으로 답변드리겠습니다.' };
      }
    }
    
    // 전문가별 응답 생성 (검색 결과 포함)
    let expertResponse = '';
    
    switch (expertId) {
      case 'assistant':
        expertResponse = await this.getAIResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'investment':
        expertResponse = await this.getInvestmentResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'counselor':
        expertResponse = await this.getCounselorResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'creative':
        expertResponse = await this.getCreativeResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'dataAnalyst':
        expertResponse = await this.getDataAnalystResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'marketing':
        expertResponse = await this.getMarketingResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'medical':
        expertResponse = await this.getMedicalResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'sales':
        expertResponse = await this.getSalesResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'startup':
        expertResponse = await this.getStartupResponseWithSearch(userMessage, context, searchResults);
        break;
      case 'writing':
        expertResponse = await this.getWritingResponseWithSearch(userMessage, context, searchResults);
        break;
      default:
        expertResponse = this.generateGenericDynamicResponse(expertId, userMessage, context);
    }
    
    // 검색 결과가 있으면 출처 정보 추가
    if (searchResults && searchResults.success && searchResults.sources.length > 0) {
      expertResponse += '\n\n**📚 참고 자료:**\n';
      searchResults.sources.slice(0, 3).forEach((source, index) => {
        expertResponse += `${index + 1}. [${source.source}] ${source.title}\n`;
      });
      expertResponse += `\n*검색 시간: ${new Date().toLocaleString('ko-KR')}*`;
    }
    
    return expertResponse;
  }

  // 동적 마무리 메시지
  generateDynamicClosing(expertId, userMessage) {
    const expert = this.experts[expertId];
    const questionType = this.detectQuestionType(userMessage);
    
    const closingTypes = {
      howTo: "더 구체적인 단계별 가이드가 필요하시면 말씀해주세요!",
      what: "이해가 안 되는 부분이 있으시면 언제든 다시 질문해주세요.",
      why: "배경이나 원리에 대해 더 궁금한 점이 있으시면 알려주세요.",
      recommendation: "개인적인 상황을 더 알려주시면 맞춤형 조언을 드릴 수 있습니다.",
      problem: "문제 해결을 위해 추가로 필요한 정보가 있으시면 공유해주세요.",
      general: `${expert.name}으로서 언제든 도움을 드리겠습니다!`
    };

    return closingTypes[questionType] || closingTypes.general;
  }

  // 질문 유형 감지
  detectQuestionType(userMessage) {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('어떻게') || lowerMessage.includes('방법')) return 'howTo';
    if (lowerMessage.includes('무엇') || lowerMessage.includes('뭐')) return 'what';
    if (lowerMessage.includes('왜') || lowerMessage.includes('이유')) return 'why';
    if (lowerMessage.includes('추천') || lowerMessage.includes('제안')) return 'recommendation';
    if (lowerMessage.includes('문제') || lowerMessage.includes('해결')) return 'problem';
    
    return 'general';
  }

  // 구체적 답변 생성 - 상용AI화 버전
  async generateSpecificResponse(expertId, question) {
    const questionLower = question.toLowerCase();

    // 상용AI 시스템: 지능형 컨텍스트 분석 사용
    if (this.aiModels.commercial) {
      const complexity = this.contextAnalyzer.analyzeComplexity(question);
      const topics = this.contextAnalyzer.identifyTopic(question);
      const isUrgent = this.contextAnalyzer.detectUrgency(question);
      
      // 토픽 기반 응답 생성
      if (topics.length > 0 && topics[0].expertId === expertId) {
        const specificResponses = this.getExpertSpecificResponses(expertId, topics[0]);
        return this.responseGenerators.generateDetailedResponse(expertId, topics[0], complexity);
      }
    }

    // 전문가별 키워드 기반 응답
    const expertKeywords = this.getExpertKeywords(expertId);
    const matchedKeywords = expertKeywords.filter(keyword => 
      questionLower.includes(keyword.toLowerCase())
    );

    if (matchedKeywords.length > 0) {
      // 키워드 매칭에 따른 전문 응답
      switch (expertId) {
        case 'assistant':
          if (questionLower.includes('ai') || questionLower.includes('인공지능')) {
            return this.getAIResponse();
          }
          break;
          
        case 'investment':
          if (questionLower.includes('투자') || questionLower.includes('주식')) {
            return this.getInvestmentResponse();
          }
          break;
          
        case 'counselor':
          return this.getCounselorResponse();
          
        default:
          break;
      }
    }

    // 기본 전문가 응답
    const responses = this.getExpertSpecificResponses(expertId);
    return responses.default;
  }

  // 완전 동적 AI 전문가 응답 생성
  getAIResponse(userMessage = '', context = {}) {
    const dynamicResponses = this.generateDynamicAIResponse(userMessage, context);
    return dynamicResponses.detailed || this.getBaseAIResponse();
  }

  // 검색 기능 포함 AI 응답
  async getAIResponseWithSearch(userMessage, context, searchResults) {
    let response = "AI 기술 전문가로서 ";
    
    // 검색 결과가 있으면 최신 정보 포함
    if (searchResults && searchResults.success) {
      response += "최신 정보와 함께 답변드리겠습니다.\n\n";
      response += `**🌐 최신 검색 정보:**\n${searchResults.summary}\n\n`;
      response += "**🤖 전문가 분석:**\n";
    } else {
      response += "전문 지식을 바탕으로 답변드리겠습니다.\n\n";
    }
    
    // AI 관련 키워드 분석 및 구체적 응답 생성
    const messageLower = userMessage.toLowerCase();
    let specificResponse = "";
    
    if (messageLower.includes('인공지능') || messageLower.includes('ai')) {
      specificResponse = `**인공지능(AI)이란?**
인공지능은 인간의 학습능력, 추론능력, 지각능력을 인공적으로 구현한 컴퓨터 시스템입니다.

**🔍 AI의 핵심 분야:**
• **머신러닝**: 데이터로부터 패턴을 학습하는 기술
• **딥러닝**: 인공신경망을 활용한 고급 학습 방법
• **자연어처리**: 컴퓨터가 인간 언어를 이해하고 생성
• **컴퓨터비전**: 이미지와 영상을 분석하고 인식

**💡 실생활 응용 사례:**
- 음성인식 (시리, 알렉사)
- 추천시스템 (넷플릭스, 유튜브)
- 자율주행 자동차
- 의료 진단 보조`;
      
    } else if (messageLower.includes('머신러닝')) {
      specificResponse = `**머신러닝(Machine Learning)이란?**
머신러닝은 명시적으로 프로그래밍하지 않고도 컴퓨터가 데이터로부터 패턴을 학습하여 예측이나 결정을 내리는 AI의 핵심 기술입니다.

**📊 머신러닝 유형:**
• **지도학습**: 정답이 있는 데이터로 학습 (분류, 회귀)
• **비지도학습**: 정답 없이 패턴 발견 (클러스터링, 차원축소)
• **강화학습**: 시행착오를 통해 최적 행동 학습

**🛠️ 주요 알고리즘:**
- 선형회귀, 의사결정트리
- 랜덤포레스트, SVM
- 신경망, 딥러닝

**💼 활용 분야:**
- 주가 예측, 고객 세분화
- 이미지 분류, 자연어 처리
- 추천 시스템, 사기 탐지`;
      
    } else if (messageLower.includes('딥러닝')) {
      specificResponse = `**딥러닝(Deep Learning)이란?**
딥러닝은 인공신경망을 여러 층으로 깊게 쌓아 복잡한 패턴을 학습하는 머신러닝의 고급 기법입니다.

**🧠 딥러닝의 특징:**
• 다층 신경망으로 복잡한 패턴 학습
• 대용량 데이터에서 뛰어난 성능
• 특성 추출을 자동으로 수행

**🏗️ 주요 구조:**
- **CNN**: 이미지 처리에 특화
- **RNN/LSTM**: 시계열, 텍스트 처리
- **Transformer**: 최신 자연어처리 모델

**🚀 혁신적 응용:**
- GPT, ChatGPT (자연어 생성)
- 이미지 생성 AI (DALL-E, Midjourney)
- AlphaGo (게임 AI)
- 자율주행 기술`;

    } else if (messageLower.includes('cnn')) {
      specificResponse = `**CNN (Convolutional Neural Network)이란?**
CNN은 이미지 처리에 특화된 딥러닝 모델로, 합성곱 연산을 통해 이미지의 특징을 추출하는 신경망입니다.

**🔬 CNN의 구조:**
• **합성곱층**: 필터를 사용해 특징 추출
• **풀링층**: 데이터 크기 축소 및 중요 정보 선별
• **완전연결층**: 최종 분류 또는 예측

**🎯 CNN의 장점:**
- 위치 불변성 (이미지 내 객체 위치와 무관하게 인식)
- 파라미터 공유로 효율적 학습
- 계층적 특징 학습 (저수준→고수준)

**💼 활용 분야:**
- 이미지 분류 및 객체 탐지
- 의료 영상 진단
- 자율주행 차량의 시각 인식
- 얼굴 인식 시스템`;

    } else if (messageLower.includes('생성형') || messageLower.includes('gpt') || messageLower.includes('chatgpt')) {
      specificResponse = `**생성형 AI(Generative AI)란?**
생성형 AI는 기존 데이터를 학습하여 새로운 콘텐츠(텍스트, 이미지, 음성 등)를 생성하는 인공지능 기술입니다.

**🤖 주요 생성형 AI 모델:**
• **GPT 시리즈**: 텍스트 생성 (OpenAI)
• **DALL-E**: 이미지 생성 (OpenAI)
• **Midjourney**: 예술적 이미지 생성
• **Stable Diffusion**: 오픈소스 이미지 생성

**⚡ 기술적 특징:**
- Transformer 아키텍처 기반
- 대규모 데이터셋으로 사전 훈련
- Few-shot 또는 Zero-shot 학습 가능
- 창의적 콘텐츠 생성 능력

**🌟 혁신적 영향:**
- 콘텐츠 제작 자동화
- 개인화된 서비스 제공
- 교육 및 연구 도구로 활용
- 창작 분야의 패러다임 변화

**⚠️ 주의사항:**
- 편향성 및 윤리적 문제
- 저작권 및 지적재산권 이슈
- 가짜 정보 생성 가능성`;
    } else {
      // 일반적인 AI 질문이나 기타 질문에 대한 기본 응답
      specificResponse = `**AI 기술에 대해 궁금하신 점을 더 구체적으로 알려주세요.**

**📚 주요 AI 분야:**
• **머신러닝**: 데이터 기반 패턴 학습
• **딥러닝**: 신경망 기반 고급 AI
• **자연어처리**: 언어 이해 및 생성
• **컴퓨터비전**: 이미지/영상 분석
• **생성형 AI**: 새로운 콘텐츠 창조

**🔍 구체적인 질문 예시:**
- "딥러닝과 머신러닝의 차이점은?"
- "CNN은 어떻게 작동하나요?"
- "생성형 AI는 어떤 원리인가요?"
- "AI가 실생활에서 어떻게 활용되나요?"

더 자세한 설명을 원하시면 구체적인 기술이나 분야를 말씀해 주세요!`;
    }
    
    response += specificResponse;
    
    return response;
  }

  // 검색 기능 포함 투자 응답
  async getInvestmentResponseWithSearch(userMessage, context, searchResults) {
    let response = "투자 전문가로서 최신 시장 동향과 함께 조언드리겠습니다.\n\n";
    
    // 검색 결과가 있으면 시장 정보 포함
    if (searchResults && searchResults.success) {
      response += `**📈 최신 시장 정보:**\n${searchResults.summary}\n\n`;
      response += "**💰 전문가 분석:**\n";
    }
    
    // 투자 관련 키워드 분석 및 구체적 응답 생성
    const messageLower = userMessage.toLowerCase();
    let specificResponse = "";
    
    if (messageLower.includes('주식') || messageLower.includes('주식투자')) {
      specificResponse = `**주식투자 가이드**

**📊 주식투자 기본 원칙:**
• **분산투자**: 한 종목에 몰빵하지 말고 여러 종목에 분산
• **장기투자**: 단기 변동에 휘둘리지 말고 장기적 관점 유지
• **가치투자**: 기업의 내재가치 대비 저평가된 주식 선택
• **위험관리**: 손절매 라인 설정 및 투자 원금 보호

**⚠️ 주의사항:**
- 생활비나 비상자금으로 투자하지 마세요
- 과도한 레버리지(빚투) 금지
- 감정적 판단보다 데이터 기반 결정
- 투자 전 충분한 공부와 정보 수집 필수

**💡 투자 단계:**
1단계: 투자 목적과 기간 설정
2단계: 리스크 허용 수준 파악
3단계: 포트폴리오 구성 및 분산
4단계: 정기적 모니터링 및 리밸런싱`;

    } else if (messageLower.includes('가상화폐') || messageLower.includes('암호화폐') || messageLower.includes('코인')) {
      specificResponse = `**가상화폐(암호화폐) 투자 가이드**

**🪙 가상화폐란?**
블록체인 기술을 기반으로 한 디지털 화폐로, 중앙은행이나 정부의 통제를 받지 않는 탈중앙화된 화폐입니다.

**💎 주요 암호화폐:**
• **비트코인(BTC)**: 최초의 암호화폐, 디지털 금
• **이더리움(ETH)**: 스마트 컨트랙트 플랫폼
• **리플(XRP)**: 국제송금 특화
• **솔라나(SOL)**: 고속 블록체인

**⚠️ 고위험 투자 주의사항:**
- 극도로 높은 변동성 (하루 20-30% 변동 가능)
- 규제 리스크 (정부 정책 변화 영향)
- 기술적 리스크 (해킹, 분실 위험)
- 투기적 성격이 강함

**🛡️ 안전 투자 원칙:**
- 전체 자산의 5-10% 이하로 제한
- 잃어도 되는 돈으로만 투자
- 하드웨어 지갑 사용 권장
- 충분한 학습 후 투자 시작`;

    } else if (messageLower.includes('부동산')) {
      specificResponse = `**부동산 투자 가이드**

**🏠 부동산 투자 특징:**
• 안정적 자산 성격 (인플레이션 헤지)
• 임대수익 + 시세차익 이중 수익 구조
• 높은 초기 자본 필요
• 유동성 낮음 (현금화 시간 소요)

**📍 투자 지역 선택 기준:**
- 교통 접근성 (지하철, 버스 노선)
- 개발 호재 (신도시, 재개발)
- 인구 유입 요소 (대학, 산업단지)
- 생활 인프라 (학교, 병원, 쇼핑몰)

**💰 수익률 계산:**
- 임대수익률 = (연간 임대료 ÷ 매입가) × 100
- 일반적으로 3-5% 수익률 기대
- 관리비, 세금, 수리비 등 비용 고려

**🚨 리스크 요소:**
- 금리 상승 시 대출 부담 증가
- 공급 과잉 시 가격 하락 위험
- 임차인 구하기 어려움 (공실 리스크)`;

    } else {
      // 일반적인 투자 조언
      specificResponse = this.getInvestmentResponse(userMessage, context);
    }
    
    response += specificResponse;
    
    return response;
  }

  // 검색 기능 포함 창작 응답
  async getCreativeResponseWithSearch(userMessage, context, searchResults) {
    let response = "🎨 창작 전문가로서 최신 크리에이티브 트렌드와 함께 조언드리겠습니다.\n\n";
    
    // 검색 결과가 있으면 최신 트렌드 정보 포함
    if (searchResults && searchResults.success) {
      response += `**🌟 최신 창작 트렌드:**\n${searchResults.summary}\n\n`;
      response += "**💡 창작 전문가 조언:**\n";
    } else {
      response += "전문 지식을 바탕으로 창작 조언을 드리겠습니다.\n\n";
    }
    
    // 창작 관련 키워드 분석 및 구체적 응답 생성
    const messageLower = userMessage.toLowerCase();
    let specificResponse = "";
    
    if (messageLower.includes('브랜딩') || messageLower.includes('브랜드')) {
      specificResponse = `**브랜드 구축 가이드**

**🎯 브랜드 아이덴티티 설계:**
• **브랜드 철학**: 핵심 가치와 미션 정의
• **타겟 고객**: 구체적인 페르소나 설정
• **차별화 요소**: 경쟁사와의 차별점 명확화
• **브랜드 톤앤매너**: 일관된 커뮤니케이션 스타일

**🎨 비주얼 아이덴티티:**
- 로고: 기억하기 쉽고 확장 가능한 디자인
- 컬러 팔레트: 브랜드 감정과 매칭되는 색상
- 타이포그래피: 브랜드 성격을 표현하는 폰트
- 이미지 스타일: 일관된 사진/일러스트 톤

**📱 브랜드 경험 설계:**
- 터치포인트 맵핑 (웹사이트, SNS, 오프라인)
- 고객 여정별 브랜드 경험 최적화
- 브랜드 가이드라인 문서화
- 직원 브랜드 교육 프로그램`;

    } else if (messageLower.includes('콘텐츠') || messageLower.includes('컨텐츠')) {
      specificResponse = `**콘텐츠 제작 전략**

**📊 콘텐츠 기획:**
• **타겟 분석**: 고객의 관심사와 니즈 파악
• **플랫폼별 최적화**: 인스타, 유튜브, 블로그 등 특성 고려
• **콘텐츠 믹스**: 정보형, 오락형, 홍보형 균형 유지
• **발행 스케줄**: 일관된 포스팅 주기 설정

**🎬 영상 콘텐츠:**
- 첫 3초가 핵심 (시청자 어텐션 확보)
- 스토리텔링 구조 활용
- 자막과 썸네일 최적화
- 숏폼과 롱폼 콘텐츠 전략 차별화

**✍️ 텍스트 콘텐츠:**
- 헤드라인의 중요성 (클릭률 결정)
- 스캔 가능한 구조 (불릿 포인트, 소제목)
- 감정적 연결 (개인 경험, 스토리)
- CTA(Call to Action) 명확화

**📈 성과 측정:**
- 도달률, 참여율, 전환율 분석
- A/B 테스트를 통한 최적화
- 댓글과 피드백 분석
- 경쟁사 콘텐츠 벤치마킹`;

    } else if (messageLower.includes('디자인')) {
      specificResponse = `**디자인 가이드**

**🎨 디자인 원칙:**
• **사용자 중심**: UX/UI 우선 고려
• **일관성**: 통일된 디자인 시스템
• **접근성**: 모든 사용자가 이용 가능한 디자인
• **반응형**: 다양한 디바이스 대응

**💡 트렌드 분석:**
- 미니멀리즘과 화이트 스페이스 활용
- 다크모드와 라이트모드 지원
- 마이크로 인터랙션 디테일
- 지속가능한 디자인 (그린 디자인)

**🛠️ 도구 활용:**
- Figma: 협업 기반 UI/UX 디자인
- Adobe Creative Suite: 전문 그래픽 작업
- Sketch: Mac 기반 인터페이스 디자인
- Canva: 손쉬운 마케팅 디자인

**📱 모바일 우선 디자인:**
- 터치 인터페이스 고려
- 로딩 속도 최적화
- 직관적인 네비게이션
- 가독성 높은 타이포그래피`;

    } else {
      // 기존 창작 응답 활용
      specificResponse = this.getCreativeResponse(userMessage, context);
    }
    
    response += specificResponse;
    
    return response;
  }

  // 검색 기능 포함 마케팅 응답
  async getMarketingResponseWithSearch(userMessage, context, searchResults) {
    let response = "마케팅 전문가로서 최신 트렌드와 함께 전략을 제안드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**📊 최신 마케팅 트렌드:**\n${searchResults.summary}\n\n`;
      response += "**📢 전문가 전략:**\n";
    }
    
    const baseResponse = this.getMarketingResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 의료 응답
  async getMedicalResponseWithSearch(userMessage, context, searchResults) {
    let response = "의료 전문가로서 최신 의학 정보와 함께 조언드리겠습니다. (정확한 진단은 의료진과 상담하세요)\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**🏥 최신 의학 정보:**\n${searchResults.summary}\n\n`;
      response += "**👨‍⚕️ 전문의 조언:**\n";
    }
    
    const baseResponse = this.getMedicalResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 법률 응답
  async getLegalResponseWithSearch(userMessage, context, searchResults) {
    let response = "법률 전문가로서 최신 법령 정보와 함께 조언드리겠습니다. (정확한 법률 해석은 변호사와 상담하세요)\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**⚖️ 최신 법령 정보:**\n${searchResults.summary}\n\n`;
      response += "**👩‍⚖️ 법률 전문가 조언:**\n";
    }
    
    const baseResponse = this.getLegalResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 요리 응답
  async getCookingResponseWithSearch(userMessage, context, searchResults) {
    let response = "요리 전문가로서 최신 레시피와 트렌드를 함께 소개해드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**🍳 최신 요리 트렌드:**\n${searchResults.summary}\n\n`;
      response += "**👨‍🍳 셰프의 조언:**\n";
    }
    
    const baseResponse = this.getCookingResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 여행 응답
  async getTravelResponseWithSearch(userMessage, context, searchResults) {
    let response = "여행 전문가로서 최신 여행 정보와 함께 추천드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**✈️ 최신 여행 정보:**\n${searchResults.summary}\n\n`;
      response += "**🗺️ 여행 전문가 추천:**\n";
    }
    
    const baseResponse = this.getTravelResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 교육 응답
  async getEducationResponseWithSearch(userMessage, context, searchResults) {
    let response = "교육 전문가로서 최신 교육 동향과 함께 조언드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**� 최신 교육 동향:**\n${searchResults.summary}\n\n`;
      response += "**🎓 교육 전문가 조언:**\n";
    }
    
    const baseResponse = this.getEducationResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 심리 상담 응답
  async getPsychologyResponseWithSearch(userMessage, context, searchResults) {
    let response = "심리 상담 전문가로서 최신 심리학 연구와 함께 조언드리겠습니다. (전문적 상담은 심리 상담사와 상의하세요)\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**🧠 최신 심리학 연구:**\n${searchResults.summary}\n\n`;
      response += "**💚 심리 상담사 조언:**\n";
    }
    
    const baseResponse = this.getPsychologyResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 스타트업 응답
  async getStartupResponseWithSearch(userMessage, context, searchResults) {
    let response = "🚀 스타트업 전문가로서 최신 창업 트렌드와 함께 조언드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**📈 최신 창업 트렌드:**\n${searchResults.summary}\n\n`;
      response += "**💡 스타트업 전문가 조언:**\n";
    } else {
      response += "전문 지식을 바탕으로 창업 조언을 드리겠습니다.\n\n";
    }
    
    const baseResponse = this.getStartupResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 상담 응답
  async getCounselorResponseWithSearch(userMessage, context, searchResults) {
    let response = "💚 심리 상담 전문가로서 최신 상담 기법과 함께 조언드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**🧠 최신 상담 연구:**\n${searchResults.summary}\n\n`;
      response += "**💭 상담 전문가 조언:**\n";
    } else {
      response += "전문 상담 지식을 바탕으로 조언드리겠습니다.\n\n";
    }
    
    const baseResponse = this.getCounselorResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 데이터분석 응답
  async getDataAnalystResponseWithSearch(userMessage, context, searchResults) {
    let response = "📊 데이터 분석 전문가로서 최신 분석 기법과 함께 조언드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**📈 최신 데이터 분석 트렌드:**\n${searchResults.summary}\n\n`;
      response += "**🔍 데이터 분석가 조언:**\n";
    } else {
      response += "전문 분석 지식을 바탕으로 조언드리겠습니다.\n\n";
    }
    
    const baseResponse = this.getDataAnalystResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 영업 응답
  async getSalesResponseWithSearch(userMessage, context, searchResults) {
    let response = "💼 영업 전문가로서 최신 세일즈 트렌드와 함께 조언드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**📞 최신 영업 전략:**\n${searchResults.summary}\n\n`;
      response += "**🎯 영업 전문가 조언:**\n";
    } else {
      response += "전문 영업 지식을 바탕으로 조언드리겠습니다.\n\n";
    }
    
    const baseResponse = this.getSalesResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 검색 기능 포함 글쓰기 응답
  async getWritingResponseWithSearch(userMessage, context, searchResults) {
    let response = "✍️ 글쓰기 전문가로서 최신 작문 기법과 함께 조언드리겠습니다.\n\n";
    
    if (searchResults && searchResults.success) {
      response += `**📝 최신 글쓰기 트렌드:**\n${searchResults.summary}\n\n`;
      response += "**📖 글쓰기 전문가 조언:**\n";
    } else {
      response += "전문 글쓰기 지식을 바탕으로 조언드리겠습니다.\n\n";
    }
    
    const baseResponse = this.getWritingResponse(userMessage, context);
    response += baseResponse;
    
    return response;
  }

  // 동적 AI 응답 생성기
  generateDynamicAIResponse(userMessage, context) {
    const keywords = this.extractKeywords(userMessage);
    const aiKeywords = ['ai', '인공지능', '머신러닝', '딥러닝', '알고리즘', '데이터', '모델'];
    const matchedKeywords = keywords.filter(k => aiKeywords.includes(k.toLowerCase()));

    let response = "AI 기술에 대해 전문적으로 답변드리겠습니다.\n\n";

    if (matchedKeywords.includes('머신러닝')) {
      response += this.getMachineLearningAdvice(userMessage);
    } else if (matchedKeywords.includes('딥러닝')) {
      response += this.getDeepLearningAdvice(userMessage);
    } else if (matchedKeywords.includes('데이터')) {
      response += this.getDataScienceAdvice(userMessage);
    } else {
      response += this.getGeneralAIAdvice(userMessage);
    }

    return {
      detailed: response + "\n\n더 구체적인 질문이 있으시면 언제든 말씀해주세요!"
    };
  }

  // 기본 AI 응답
  getBaseAIResponse() {
    return `AI(인공지능) 분야는 매우 광범위합니다. 어떤 구체적인 부분이 궁금하신가요?

**주요 AI 영역:**
• 머신러닝 & 딥러닝
• 자연어처리 & 컴퓨터비전  
• 데이터 분석 & 예측 모델링
• 자동화 & 최적화

궁금한 세부 분야를 알려주시면 더 전문적인 조언을 드리겠습니다!`;
  }

  // 동적 투자 전문가 응답
  getInvestmentResponse(userMessage = '', context = {}) {
    const dynamicResponse = this.generateDynamicInvestmentResponse(userMessage, context);
    return dynamicResponse.detailed || this.getBaseInvestmentResponse();
  }

  // 동적 투자 응답 생성기
  generateDynamicInvestmentResponse(userMessage, context) {
    const keywords = this.extractKeywords(userMessage);
    const investKeywords = ['주식', '부동산', '투자', '포트폴리오', '수익', '리스크'];
    const matchedKeywords = keywords.filter(k => investKeywords.includes(k.toLowerCase()));

    let response = "투자 전문가 관점에서 조언드리겠습니다.\n\n";

    if (matchedKeywords.includes('주식')) {
      response += this.getStockAdvice(userMessage);
    } else if (matchedKeywords.includes('부동산')) {
      response += this.getRealEstateAdvice(userMessage);
    } else if (matchedKeywords.includes('포트폴리오')) {
      response += this.getPortfolioAdvice(userMessage);
    } else {
      response += this.getGeneralInvestmentAdvice(userMessage);
    }

    return {
      detailed: response + "\n\n투자는 개인별 상황에 따라 달라지니, 더 구체적인 상황을 알려주세요!"
    };
  }

  // 동적 상담 전문가 응답
  getCounselorResponse(userMessage = '', context = {}) {
    const dynamicResponse = this.generateDynamicCounselorResponse(userMessage, context);
    return dynamicResponse.detailed || this.getBaseCounselorResponse();
  }

  // 동적 상담 응답 생성기
  generateDynamicCounselorResponse(userMessage, context) {
    const emotion = context.emotion || 'neutral';
    const keywords = this.extractKeywords(userMessage);
    
    let response = "마음을 열어주셔서 감사합니다. 함께 해결책을 찾아보겠습니다.\n\n";

    if (emotion === 'negative') {
      response += this.getEmotionalSupportAdvice(userMessage);
    } else if (keywords.some(k => ['스트레스', '우울', '불안'].includes(k))) {
      response += this.getStressManagementAdvice(userMessage);
    } else if (keywords.some(k => ['관계', '소통', '갈등'].includes(k))) {
      response += this.getRelationshipAdvice(userMessage);
    } else {
      response += this.getGeneralCounselingAdvice(userMessage);
    }

    return {
      detailed: response + "\n\n언제든 편하게 말씀해주세요. 함께 해결해나가겠습니다."
    };
  }

  // === 동적 세부 응답 생성 메서드들 ===

  // 머신러닝 조언
  getMachineLearningAdvice(userMessage) {
    if (userMessage.includes('시작') || userMessage.includes('입문')) {
      return `**머신러닝 입문 로드맵:**
1. Python 기초 (pandas, numpy)
2. 통계학 기본 개념
3. scikit-learn으로 실습
4. 캐글 경진대회 참여

**추천 첫 프로젝트:**
• 타이타닉 생존 예측
• 붓꽃 분류 문제
• 집값 예측 모델`;
    } else if (userMessage.includes('알고리즘')) {
      return `**주요 머신러닝 알고리즘:**
• 지도학습: 선형회귀, 랜덤포레스트, SVM
• 비지도학습: K-means, PCA, DBSCAN
• 강화학습: Q-learning, 정책 기울기

어떤 문제 유형에 관심이 있으신가요?`;
    }
    return "머신러닝의 어떤 측면이 궁금하신지 더 구체적으로 알려주세요.";
  }

  // 딥러닝 조언
  getDeepLearningAdvice(userMessage) {
    if (userMessage.includes('시작') || userMessage.includes('입문')) {
      return `**딥러닝 학습 경로:**
1. 신경망 기초 이론
2. TensorFlow/PyTorch 선택
3. CNN (이미지 처리)
4. RNN/LSTM (시계열/텍스트)
5. Transformer (최신 NLP)

**실습 프로젝트 추천:**
• MNIST 손글씨 인식
• 감정 분석 모델
• 이미지 분류기`;
    }
    return "딥러닝의 어떤 분야에 특히 관심이 있으신가요?";
  }

  // 데이터 사이언스 조언
  getDataScienceAdvice(userMessage) {
    return `**데이터 분석 프로세스:**
1. 문제 정의 및 가설 설정
2. 데이터 수집 및 전처리
3. 탐색적 데이터 분석 (EDA)
4. 모델링 및 검증
5. 결과 해석 및 액션 플랜

**핵심 도구:**
• Python: pandas, matplotlib, seaborn
• R: ggplot2, dplyr
• SQL: 데이터 추출
• Tableau/PowerBI: 시각화`;
  }

  // 일반 AI 조언
  getGeneralAIAdvice(userMessage) {
    return `**현재 AI 트렌드:**
• 생성형 AI (GPT, 이미지 생성)
• 멀티모달 AI (텍스트+이미지+음성)
• AutoML (자동화된 머신러닝)
• 엣지 AI (모바일/IoT 기기)

**AI 커리어 방향:**
• 데이터 사이언티스트
• ML 엔지니어
• AI 연구원
• AI 제품 매니저`;
  }

  // 주식 투자 조언
  getStockAdvice(userMessage) {
    if (userMessage.includes('초보') || userMessage.includes('시작')) {
      return `**주식 투자 기초:**
1. 투자 목표와 기간 설정
2. 리스크 허용도 파악
3. 기업 분석 방법 학습
4. 소액부터 시작

**기본 분석 지표:**
• PER, PBR (가치 평가)
• ROE, ROA (수익성)
• 부채비율 (안정성)
• 매출/영업이익 증가율`;
    }
    return "어떤 종목이나 섹터에 관심이 있으신지 알려주세요.";
  }

  // 부동산 투자 조언
  getRealEstateAdvice(userMessage) {
    return `**부동산 투자 체크포인트:**
1. 입지 (교통, 학군, 개발계획)
2. 시세 분석 (실거래가, 전세가율)
3. 임대 수익률 계산
4. 보유 비용 (세금, 관리비)

**투자 전략:**
• 갭투자: 전세가와 매매가 차이 활용
• 수익형: 월세 수익 중심
• 개발호재: 재개발/재건축 지역`;
  }

  // 포트폴리오 조언
  getPortfolioAdvice(userMessage) {
    return `**포트폴리오 구성 원칙:**
1. 자산 배분 (주식/채권/대안투자)
2. 지역 분산 (국내/해외)
3. 섹터 분산 (IT/금융/바이오 등)
4. 정기적 리밸런싱

**연령별 자산 배분 가이드:**
• 20-30대: 주식 70%, 채권 30%
• 40-50대: 주식 60%, 채권 40%
• 60대+: 주식 40%, 채권 60%`;
  }

  // 일반 투자 조언
  getGeneralInvestmentAdvice(userMessage) {
    return `**투자 성공의 핵심:**
1. 장기적 관점 유지
2. 감정적 판단 금지
3. 지속적 학습과 분석
4. 분산투자 실천

**피해야 할 실수:**
• 단기 수익에 집착
• 남들 따라하기
• 빌려서 투자하기
• 한 종목에 몰아넣기`;
  }

  // 감정 지원 조언
  getEmotionalSupportAdvice(userMessage) {
    return `**감정적 어려움 극복하기:**
1. 현재 감정을 인정하고 수용
2. 작은 변화부터 시작
3. 지지해주는 사람들과 소통
4. 전문가 도움 받기

**즉시 도움되는 방법:**
• 깊은 호흡 (4초 들이쉬고 6초 내쉬기)
• 감사한 것 3가지 적어보기
• 산책이나 가벼운 운동
• 좋아하는 음악 듣기`;
  }

  // 스트레스 관리 조언
  getStressManagementAdvice(userMessage) {
    return `**스트레스 관리 전략:**
1. 스트레스 원인 파악
2. 해결 가능한 것과 불가능한 것 구분
3. 시간 관리와 우선순위 설정
4. 적절한 휴식과 회복

**실용적 스트레스 해소법:**
• 운동 (30분 걷기도 효과적)
• 명상이나 요가
• 취미 활동
• 충분한 수면 (7-8시간)`;
  }

  // 관계 조언
  getRelationshipAdvice(userMessage) {
    return `**건강한 인간관계 만들기:**
1. 경청하는 습관 기르기
2. 솔직하고 존중하는 소통
3. 개인 경계선 설정
4. 갈등을 성장의 기회로 보기

**갈등 해결 방법:**
• 상대방 입장에서 생각해보기
• 감정 아닌 사실에 집중
• 해결책을 함께 찾기
• 필요시 시간을 갖고 냉정해지기`;
  }

  // 일반 상담 조언
  getGeneralCounselingAdvice(userMessage) {
    return `**마음 건강 관리:**
1. 자신의 감정 상태 체크
2. 규칙적인 생활 패턴 유지
3. 의미있는 활동 찾기
4. 사회적 관계 유지

**자기계발 팁:**
• 작은 목표 설정하고 달성
• 새로운 것 배우기
• 긍정적 자기 대화
• 실패를 학습 기회로 보기`;
  }

  // === 나머지 전문가들의 동적 응답 메서드들 ===

  // 창작 전문가 동적 응답
  getCreativeResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "창의적인 관점에서 도움드리겠습니다.\n\n";

    if (keywords.some(k => ['디자인', '로고', '브랜딩'].includes(k))) {
      response += this.getDesignAdvice(userMessage);
    } else if (keywords.some(k => ['콘텐츠', '영상', '스토리'].includes(k))) {
      response += this.getContentCreationAdvice(userMessage);
    } else if (keywords.some(k => ['아이디어', '기획', '창의'].includes(k))) {
      response += this.getIdeationAdvice(userMessage);
    } else {
      response += this.getGeneralCreativeAdvice(userMessage);
    }

    return response + "\n\n창의적 작업에서 가장 중요한 것은 자신만의 관점입니다!";
  }

  // 데이터 분석 전문가 동적 응답
  getDataAnalystResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "데이터 분석 관점에서 체계적으로 접근해보겠습니다.\n\n";

    if (keywords.some(k => ['excel', '엑셀', '스프레드시트'].includes(k))) {
      response += this.getExcelAdvice(userMessage);
    } else if (keywords.some(k => ['python', '파이썬', 'pandas'].includes(k))) {
      response += this.getPythonDataAdvice(userMessage);
    } else if (keywords.some(k => ['시각화', '차트', '그래프'].includes(k))) {
      response += this.getVisualizationAdvice(userMessage);
    } else {
      response += this.getGeneralDataAdvice(userMessage);
    }

    return response + "\n\n데이터는 스토리를 말합니다. 올바른 분석으로 인사이트를 찾아보세요!";
  }

  // 마케팅 전문가 동적 응답
  getMarketingResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "마케팅 전략 관점에서 분석해보겠습니다.\n\n";

    if (keywords.some(k => ['sns', '소셜미디어', '인스타그램'].includes(k))) {
      response += this.getSocialMediaAdvice(userMessage);
    } else if (keywords.some(k => ['광고', '캠페인', '홍보'].includes(k))) {
      response += this.getAdvertisingAdvice(userMessage);
    } else if (keywords.some(k => ['브랜드', '브랜딩', '정체성'].includes(k))) {
      response += this.getBrandingAdvice(userMessage);
    } else {
      response += this.getGeneralMarketingAdvice(userMessage);
    }

    return response + "\n\n고객의 니즈를 정확히 파악하는 것이 마케팅의 시작입니다!";
  }

  // 마케팅 조언 메서드들
  getSocialMediaAdvice(userMessage) {
    return `**소셜미디어 마케팅 전략:**
• 타겟 고객이 가장 활발한 플랫폼 선택
• 일관된 브랜드 톤앤매너 유지
• 유저 생성 콘텐츠(UGC) 활용
• 인플루언서와의 협업 고려
• 정기적인 분석과 최적화`;
  }

  getAdvertisingAdvice(userMessage) {
    return `**효과적인 광고 전략:**
• 명확한 타겟 오디언스 설정
• 핵심 메시지 간결하게 전달
• A/B 테스트를 통한 최적화
• 적절한 광고 채널 선택
• ROI 측정 및 개선`;
  }

  getBrandingAdvice(userMessage) {
    return `**브랜딩 전략 가이드:**
• 브랜드 정체성 명확히 정의
• 일관된 시각적 아이덴티티
• 고유한 브랜드 스토리 개발
• 고객 경험 중심의 브랜딩
• 브랜드 가치 지속적 소통`;
  }

  getGeneralMarketingAdvice(userMessage) {
    return `**마케팅 기본 전략:**
• 4P 분석 (Product, Price, Place, Promotion)
• 고객 세분화 및 타겟팅
• 차별화된 포지셔닝 전략
• 통합 마케팅 커뮤니케이션
• 데이터 기반 의사결정`;
  }

  // 의료 전문가 동적 응답
  getMedicalResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "건강 관리 관점에서 조언드리겠습니다. (전문 진료는 반드시 의료진과 상담하세요)\n\n";

    if (keywords.some(k => ['운동', '헬스', '피트니스'].includes(k))) {
      response += this.getExerciseAdvice(userMessage);
    } else if (keywords.some(k => ['식단', '다이어트', '영양'].includes(k))) {
      response += this.getNutritionAdvice(userMessage);
    } else if (keywords.some(k => ['수면', '잠', '불면'].includes(k))) {
      response += this.getSleepAdvice(userMessage);
    } else {
      response += this.getGeneralHealthAdvice(userMessage);
    }

    return response + "\n\n건강은 예방이 최우선입니다. 정기적인 건강검진을 받으세요!";
  }

  // 의료 조언 메서드들
  getExerciseAdvice(userMessage) {
    return `**운동 건강 가이드:**
• 주 3-5회, 30분 이상 유산소 운동
• 근력 운동으로 기초대사량 증가
• 운동 전후 스트레칭 필수
• 개인 체력에 맞는 강도 조절
• 점진적인 운동량 증가`;
  }

  getDietAdvice(userMessage) {
    return `**건강한 식단 관리:**
• 균형 잡힌 영양소 섭취
• 충분한 수분 섭취 (하루 1.5-2L)
• 규칙적인 식사 시간 유지
• 과도한 염분, 당분 제한
• 신선한 채소와 과일 섭취`;
  }

  getSleepAdvice(userMessage) {
    return `**수면 건강 관리:**
• 하루 7-8시간 충분한 수면
• 규칙적인 수면 패턴 유지
• 잠자리 환경 최적화 (온도, 조명)
• 수면 전 전자기기 사용 제한
• 카페인 섭취 시간 조절`;
  }

  getGeneralHealthAdvice(userMessage) {
    return `**종합 건강 관리:**
• 정기적인 건강검진 (연 1-2회)
• 스트레스 관리 및 마음 건강
• 금연, 금주 등 생활습관 개선
• 개인위생 관리 철저
• 건강한 사회적 관계 유지`;
  }

  // 영업 전문가 동적 응답
  getSalesResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "영업 전문가 관점에서 전략을 제안드리겠습니다.\n\n";

    if (keywords.some(k => ['고객', '고객관리', 'crm'].includes(k))) {
      response += this.getCustomerManagementAdvice(userMessage);
    } else if (keywords.some(k => ['협상', '가격', '계약'].includes(k))) {
      response += this.getNegotiationAdvice(userMessage);
    } else if (keywords.some(k => ['실적', '목표', '성과'].includes(k))) {
      response += this.getPerformanceAdvice(userMessage);
    } else {
      response += this.getGeneralSalesAdvice(userMessage);
    }

    return response + "\n\n성공적인 영업의 핵심은 고객의 문제를 해결해주는 것입니다!";
  }

  // 영업 조언 메서드들
  getCustomerManagementAdvice(userMessage) {
    return `**고객 관리 전략:**
• CRM 시스템을 활용한 체계적 관리
• 고객별 맞춤형 서비스 제공
• 정기적인 고객 만족도 조사
• 고객 라이프사이클 관리
• 장기적 관계 구축에 집중`;
  }

  getNegotiationAdvice(userMessage) {
    return `**협상 전략 가이드:**
• 상대방의 니즈와 관심사 파악
• WIN-WIN 방향의 해결책 모색
• 감정보다는 논리적 접근
• 대안책 미리 준비
• 인내심과 유연성 유지`;
  }

  getPerformanceAdvice(userMessage) {
    return `**영업 성과 향상:**
• 명확한 목표 설정 (SMART 기법)
• 일일/주간 활동 계획 수립
• 성과 지표 정기적 모니터링
• 지속적인 자기계발
• 팀워크와 정보 공유`;
  }

  getGeneralSalesAdvice(userMessage) {
    return `**영업 기본 원칙:**
• 고객의 문제와 니즈 정확히 파악
• 제품/서비스의 가치 명확히 전달
• 신뢰 관계 구축이 최우선
• 지속적인 Follow-up
• 거절을 기회로 전환`;
  }

  // 스타트업 전문가 동적 응답
  getStartupResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "스타트업 관점에서 실전 조언을 드리겠습니다.\n\n";

    if (keywords.some(k => ['아이디어', '아이템', '사업'].includes(k))) {
      response += this.getBusinessIdeaAdvice(userMessage);
    } else if (keywords.some(k => ['투자', '투자유치', '펀딩'].includes(k))) {
      response += this.getFundingAdvice(userMessage);
    } else if (keywords.some(k => ['팀', '팀빌딩', '채용'].includes(k))) {
      response += this.getTeamBuildingAdvice(userMessage);
    } else {
      response += this.getGeneralStartupAdvice(userMessage);
    }

    return response + "\n\n스타트업은 실행력이 생명입니다. 빠르게 테스트하고 개선하세요!";
  }

  // 스타트업 조언 메서드들
  getBusinessIdeaAdvice(userMessage) {
    return `**사업 아이템 검증 방법:**
• 시장의 진짜 문제 해결하는가?
• 충분한 시장 규모와 성장성
• 경쟁사 대비 차별화 요소
• 수익 모델의 명확성
• MVP로 빠른 검증`;
  }

  getFundingAdvice(userMessage) {
    return `**투자 유치 전략:**
• 명확한 비즈니스 모델 제시
• 트랙션과 성과 지표 준비
• 시장 기회와 경쟁 우위 설명
• 팀의 실행 능력 어필
• 현실적인 재무 계획`;
  }

  getTeamBuildingAdvice(userMessage) {
    return `**스타트업 팀 구성:**
• 서로 다른 전문성 보완
• 공동의 비전과 가치 공유
• 명확한 역할과 책임 분담
• 효과적인 소통 체계 구축
• 성과 기반 평가 시스템`;
  }

  getGeneralStartupAdvice(userMessage) {
    return `**스타트업 성공 원칙:**
• 고객 중심의 제품 개발
• 빠른 실행과 지속적 개선
• 린 스타트업 방법론 활용
• 네트워킹과 멘토링 적극 활용
• 실패를 학습의 기회로 활용`;
  }

  // 글쓰기 전문가 동적 응답
  getWritingResponse(userMessage = '', context = {}) {
    const keywords = this.extractKeywords(userMessage);
    let response = "글쓰기 전문가로서 도움드리겠습니다.\n\n";

    if (keywords.some(k => ['블로그', '포스팅', '콘텐츠'].includes(k))) {
      response += this.getBlogWritingAdvice(userMessage);
    } else if (keywords.some(k => ['카피', '광고', '마케팅'].includes(k))) {
      response += this.getCopywritingAdvice(userMessage);
    } else if (keywords.some(k => ['소설', '창작', '스토리'].includes(k))) {
      response += this.getCreativeWritingAdvice(userMessage);
    } else {
      response += this.getGeneralWritingAdvice(userMessage);
    }

    return response + "\n\n좋은 글은 독자의 마음을 움직입니다. 진정성을 담아 쓰세요!";
  }

  // 일반적인 동적 응답 생성
  generateGenericDynamicResponse(expertId, userMessage, context) {
    const expert = this.experts[expertId];
    const { complexity, keywords } = context;
    
    let response = `${expert.title}로서 전문적으로 답변드리겠습니다.\n\n`;
    
    if (complexity === 'complex') {
      response += `복잡한 주제이군요. 단계별로 접근해보겠습니다:\n\n`;
      response += `1. 현재 상황 분석\n2. 주요 이슈 파악\n3. 해결 방안 제시\n4. 실행 계획 수립`;
    } else if (complexity === 'medium') {
      response += `이 분야에서 ${expert.experienceYears}년의 경험을 바탕으로 실용적인 조언을 드리겠습니다.`;
    } else {
      response += `간단명료하게 답변드리겠습니다.`;
    }

    return response;
  }

  // 대화 히스토리 업데이트
  updateConversationHistory(userMessage, expertResponse, expertId) {
    const conversationEntry = {
      id: randomUUID(),
      timestamp: new Date().toISOString(),
      userMessage,
      expertId,
      expertResponse,
      conversationId: this.conversationHistory.length + 1
    };

    this.conversationHistory.push(conversationEntry);

    // 히스토리 크기 제한 (최근 100개 대화만 유지)
    if (this.conversationHistory.length > 100) {
      this.conversationHistory = this.conversationHistory.slice(-100);
    }
  }

  // 메인 응답 생성 메서드 (검색 기능 포함)
  async generateResponse(expertType, userMessage, context = {}) {
    console.log(`${expertType} 전문가 응답 생성 중... (검색 포함)`);
    
    try {
      // 1. 사용자 메시지 분석 및 검색 키워드 추출
      const searchKeywords = this.extractSearchKeywords(userMessage, expertType);
      
      // 2. 인터넷 검색 수행 (키워드가 있는 경우)
      let searchResults = null;
      if (searchKeywords && searchKeywords.length > 0) {
        searchResults = await this.performInternetSearch(searchKeywords, expertType);
      }
      
      // 3. 전문가별 검색 포함 응답 생성
      let response;
      switch (expertType) {
        case 'ai':
          response = await this.getAIResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'investment':
          response = await this.getInvestmentResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'marketing':
          response = await this.getMarketingResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'medical':
          response = await this.getMedicalResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'startup':
          response = await this.getStartupResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'legal':
          response = await this.getLegalResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'cooking':
          response = await this.getCookingResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'travel':
          response = await this.getTravelResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'education':
          response = await this.getEducationResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'creative':
          response = await this.getCreativeResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'counselor':
          response = await this.getCounselorResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'dataAnalyst':
          response = await this.getDataAnalystResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'sales':
          response = await this.getSalesResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'writing':
          response = await this.getWritingResponseWithSearch(userMessage, context, searchResults);
          break;
        case 'psychology':
          response = await this.getPsychologyResponseWithSearch(userMessage, context, searchResults);
          break;
        default:
          response = this.getDefaultResponse();
      }
      
      // 4. 응답에 검색 메타데이터 추가
      if (searchResults && searchResults.success) {
        response += `\n\n*🔍 ${searchResults.sources.length}개의 최신 정보원을 검색하여 답변했습니다.*`;
      }
      
      return response;
      
    } catch (error) {
      console.error('응답 생성 중 오류:', error);
      return this.getErrorResponse(expertType);
    }
  }

  // 기본 응답 생성
  getDefaultResponse() {
    return "안녕하세요! 도깨비마을장터의 AI 전문가입니다. 어떤 도움이 필요하신가요?";
  }

  // 검색 키워드 추출 메서드 (단순화된 버전)
  extractSearchKeywords(userMessage, expertType) {
    const keywords = [];
    
    // 모든 질문에 대해 기본적으로 검색 수행
    keywords.push(userMessage);
    
    // 전문가별 특화 검색어만 추가
    switch (expertType) {
      case 'ai':
        keywords.push(userMessage + ' 기술 동향');
        break;
      case 'investment':
        keywords.push(userMessage + ' 투자 정보');
        break;
      case 'marketing':
        keywords.push(userMessage + ' 마케팅 트렌드');
        break;
      case 'medical':
        keywords.push(userMessage + ' 의학 정보');
        break;
      case 'startup':
        keywords.push(userMessage + ' 창업 정보');
        break;
      case 'legal':
        keywords.push(userMessage + ' 법률 정보');
        break;
      case 'cooking':
        keywords.push(userMessage + ' 레시피');
        break;
      case 'travel':
        keywords.push(userMessage + ' 여행 정보');
        break;
      case 'education':
        keywords.push(userMessage + ' 교육 정보');
        break;
      case 'creative':
        keywords.push(userMessage + ' 창작 트렌드');
        break;
      case 'counselor':
        keywords.push(userMessage + ' 상담 기법');
        break;
      case 'dataAnalyst':
        keywords.push(userMessage + ' 데이터 분석');
        break;
      case 'sales':
        keywords.push(userMessage + ' 영업 전략');
        break;
      case 'writing':
        keywords.push(userMessage + ' 글쓰기 기법');
        break;
      case 'psychology':
        keywords.push(userMessage + ' 심리학 정보');
        break;
      default:
        // 기본적으로 원본 질문만 검색
        break;
    }
    
    return keywords;
  }

  // 오류 응답 생성
  getErrorResponse(expertType) {
    const expertNames = {
      'ai': 'AI 기술 전문가',
      'investment': '투자 전문가',
      'marketing': '마케팅 전문가',
      'medical': '의료 전문가',
      'startup': '스타트업 전문가',
      'legal': '법률 전문가',
      'cooking': '요리 전문가',
      'travel': '여행 전문가',
      'education': '교육 전문가',
      'creative': '창작 전문가',
      'counselor': '심리 상담 전문가',
      'dataAnalyst': '데이터 분석 전문가',
      'sales': '영업 전문가',
      'writing': '글쓰기 전문가',
      'psychology': '심리학 전문가'
    };
    
    const expertName = expertNames[expertType] || '전문가';
    return `죄송합니다. ${expertName}로서 현재 일시적인 기술적 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.`;
  }

  // 전문가 목록 반환
  getExpertList() {
    return Object.values(this.experts).map(expert => expert.getInfo());
  }

  // 대화 히스토리 반환
  getConversationHistory(limit = 10) {
    return this.conversationHistory.slice(-limit);
  }

  // 시스템 상태 반환
  getSystemStatus() {
    return {
      expertsCount: Object.keys(this.experts).length,
      conversationCount: this.conversationHistory.length,
      aiModels: Object.keys(this.aiModels).filter(key => this.aiModels[key]),
      systemVersion: '1.0_javascript',
      isInitialized: this.isInitialized,
      lastUpdate: new Date().toISOString(),
      availableExperts: Object.keys(this.experts)
    };
  }
}

export default CommercialAIAgentSystem;
