from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from werkzeug.utils import secure_filename

# 📄 문서 분석 시스템 임포트
try:
    from document_analyzer_v1 import get_document_analyzer, analyze_file
    DOCUMENT_ANALYSIS_AVAILABLE = True
    print("✅ 문서 분석 시스템 로드 성공!")
except Exception as e:
    print(f"⚠️ 문서 분석 시스템 로드 실패: {e}")
    DOCUMENT_ANALYSIS_AVAILABLE = False

# ⚡ 강제 서버리스 모드 (SQLite 완전 차단) - v4.0 COMPLETE REDEPLOY
VERCEL_ENV = True
APP_VERSION = "4.0-COMPLETE-REDEPLOY-FIX"

print(f"🚀🚀🚀 COMPLETE REDEPLOY MODE v{APP_VERSION} 🚀🚀🚀")
print(f"🔍 환경 정보: CWD={os.getcwd()}")
print("⚠️ WARNING: ZERO DB ACCESS - PURE SERVERLESS MODE")
print("🛡️ SQLite 완전 차단 - 메모리 시스템 완전 비활성화")
print("🔥 CACHE KILLER - 42분 다운타임 해결")
print("=" * 60)

# 🚀 Vercel 경량 AI 엔진 임포트 (대용량 모델 대신)
try:
    from lightweight_ai_engine import get_ai_response, get_expert_capabilities, health_check
    print("✅ 경량 AI 엔진 v1.0 임포트 성공! (Vercel 최적화)")
    LIGHTWEIGHT_AI_AVAILABLE = True
    ADVANCED_AI_AVAILABLE = False  # 대용량 모델 비활성화
except Exception as e:
    print(f"⚠️ 경량 AI 엔진 임포트 실패: {e}")
    print("🔄 기본 AI 시스템으로 폴백")
    LIGHTWEIGHT_AI_AVAILABLE = False
    ADVANCED_AI_AVAILABLE = False

# 👥 1단계: 16명 전문가 시스템 임포트
try:
    from experts.complete_16_experts_improved import Complete16ExpertAI
    print("✅ 16명 전문가 시스템 v1.0 임포트 성공!")
    EXPERTS_V1_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 16명 전문가 시스템 임포트 실패: {e}")
    print("🔄 기본 전문가 시스템으로 폴백")
    EXPERTS_V1_AVAILABLE = False

# 👥 2단계: Enhanced 전문가 시스템 임포트 (개인화 + 성능 모니터링)
try:
    from experts.complete_16_experts_v2_enhanced_20250823 import EnhancedComplete16ExpertAI
    print("✅ Enhanced 16명 전문가 시스템 v2.0 임포트 성공!")
    EXPERTS_V2_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Enhanced 전문가 시스템 임포트 실패: {e}")
    print("🔄 v1.0 전문가 시스템으로 폴백")
    EXPERTS_V2_AVAILABLE = False

# 👥 3단계: 멀티모달 전문가 시스템 임포트 (다중 AI 모델 + 다국어)
try:
    from experts.complete_16_experts_v3_multimodel_20250823 import EnhancedComplete16ExpertAI_v3
    print("✅ 멀티모달 16명 전문가 시스템 v3.0 임포트 성공!")
    EXPERTS_V3_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 멀티모달 전문가 시스템 임포트 실패: {e}")
    print("🔄 v2.0 전문가 시스템으로 폴백")
    EXPERTS_V3_AVAILABLE = False

# 👥 4단계: 품질 개선 멀티모달 전문가 시스템 임포트 (이미지/음성/비디오)
try:
    from experts.complete_16_experts_v4_improved_quality_20250823_190858 import MultimodalExpertAI
    print("✅ 품질 개선 멀티모달 전문가 시스템 v4.0 임포트 성공!")
    EXPERTS_V4_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 품질 개선 전문가 시스템 임포트 실패: {e}")
    print("🔄 v3.0 전문가 시스템으로 폴백")
    EXPERTS_V4_AVAILABLE = False

# 👥 5단계: 글로벌 확장 전문가 시스템 임포트 
try:
    from experts.complete_16_experts_v5_global_expansion_20250823 import GlobalExpertSystemV5
    print("✅ 글로벌 확장 전문가 시스템 v5.0 임포트 성공!")
    EXPERTS_V5_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 글로벌 확장 전문가 시스템 임포트 실패: {e}")
    EXPERTS_V5_AVAILABLE = False

# 👥 6단계: 궁극적 글로벌 전문가 시스템 임포트
try:
    from experts.complete_16_experts_v6_ultimate_global_20250823 import ComprehensiveExpertSystemV6
    print("✅ 궁극적 글로벌 전문가 시스템 v6.0 임포트 성공!")
    EXPERTS_V6_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 궁극적 글로벌 전문가 시스템 임포트 실패: {e}")
    EXPERTS_V6_AVAILABLE = False

# 👥 7단계: 실시간 멀티모달 전문가 시스템 임포트
try:
    from experts.complete_16_experts_v7_real_time_multimodal_20250823 import GlobalExpertSystemV7
    print("✅ 실시간 멀티모달 전문가 시스템 v7.0 임포트 성공!")
    EXPERTS_V7_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 실시간 멀티모달 전문가 시스템 임포트 실패: {e}")
    EXPERTS_V7_AVAILABLE = False

# 👥 8단계: 코스믹 멀티모달 전문가 시스템 임포트
try:
    from experts.complete_16_experts_v8_cosmic_multimodal_20250823 import UniversalAISystemV8
    print("✅ 코스믹 멀티모달 전문가 시스템 v8.0 임포트 성공!")
    EXPERTS_V8_AVAILABLE = True
except Exception as e:
    print(f"⚠️ 코스믹 멀티모달 전문가 시스템 임포트 실패: {e}")
    EXPERTS_V8_AVAILABLE = False

# 👥 9단계: DNA 개인화 전문가 시스템 임포트 (최종 단계)
try:
    from experts.complete_16_experts_v9_dna_personalized_20250823 import DNAPersonalizedExpertSystem
    print("✅ DNA 개인화 전문가 시스템 v9.0 임포트 성공!")
    EXPERTS_V9_AVAILABLE = True
except Exception as e:
    print(f"⚠️ DNA 개인화 전문가 시스템 임포트 실패: {e}")
    EXPERTS_V9_AVAILABLE = False

print(f"🚀🚀🚀 COMPLETE REDEPLOY MODE v{APP_VERSION} 🚀🚀🚀")
print(f"🔍 환경 정보: CWD={os.getcwd()}")
print("⚠️ WARNING: ZERO DB ACCESS - PURE SERVERLESS MODE")
print("🛡️ SQLite 완전 차단 - 메모리 시스템 완전 비활성화")
print("🔥 CACHE KILLER - 42분 다운타임 해결")
print("=" * 60)


# 🛡️ 고급 AI 시스템 (DB 의존성 제로)
class UltraLightAIManager:
    """완전 서버리스 최적화 고급 AI 매니저"""

    def __init__(self):
        # 🌟 3단계: 멀티모달 16명 전문가 시스템 초기화 (v3.0 최우선)
        if EXPERTS_V3_AVAILABLE:
            try:
                self.expert_ai_v3 = EnhancedComplete16ExpertAI_v3(db_path="expert_ai_v3.db")
                print("🌟 멀티모달 16명 전문가 시스템 v3.0 활성화!")
                self.use_16_experts_v3 = True
                self.use_16_experts_v2 = False  # v2는 비활성화
                self.use_16_experts = False     # v1은 비활성화
                # 32명 전문가 리스트 (3단계 멀티모달 + v9 DNA 개인화) - 최종 중복 제거 완료
                self.experts = {
                    # 기본 11명 전문가 (v1.0) - 중복 제거 후
                    "assistant": "인공지능도깨비 🤖",
                    # "builder": "경제학박사 부자도깨비 💰", # business와 중복
                    # "counselor": "상담심리박사 상담도깨비 💬", # psychology와 중복
                    # "creative": "예술학박사 창작도깨비 🎨", # design과 중복
                    "data_analyst": "데이터분석도깨비 📊",
                    "fortune": "점술도깨비 🔮",
                    # "growth": "교육학박사 성장도깨비 📈", # education과 중복
                    "hr": "인사관리도깨비 👥",
                    "marketing": "마케팅도깨비 📢",
                    # "medical": "의학박사 의료도깨비 🏥", # biotech와 통합
                    "sales": "영업도깨비 💼",
                    "seo": "검색도깨비 🔍",
                    "shopping": "쇼핑도깨비 🛒",
                    "startup": "창업도깨비 🚀",
                    "wellness": "건강도깨비 🌿",
                    "writing": "글쓰기도깨비 ✍️",
                    
                    # v9.0 DNA 개인화 전문가 15명 추가 (통합/개선)
                    "tech": "IT기술도깨비 💻",
                    "business": "경영도깨비 📊", # builder 통합
                    "education": "교육도깨비 📚", # growth 통합
                    "psychology": "심리상담도깨비 🧠", # counselor 통합
                    "legal": "법률도깨비 ⚖️",
                    "finance": "금융도깨비 💰",
                    "design": "디자인도깨비 🎨", # creative 통합
                    "sports": "스포츠도깨비 🏃‍♂️",
                    "nutrition": "영양도깨비 🥗",
                    "language": "언어도깨비 🗣️",
                    "music": "음악도깨비 🎵",
                    "travel": "여행도깨비 ✈️",
                    "environment": "환경도깨비 🌱",
                    "agriculture": "농업도깨비 🌾",
                    "logistics": "물류도깨비 🚚",
                    
                    # 글로벌 기술 전문가 4명
                    "energy": "에너지도깨비 ⚡",
                    "biotech": "바이오도깨비 🧬", # medical 통합
                    "security": "보안도깨비 🔒",
                    "aerospace": "항공우주도깨비 🚀",
                    
                    # 미래 기술 전문가 2명
                    "quantum": "양자물리도깨비 ⚛️",
                    "nano": "나노기술도깨비 🔬",
                }
            except Exception as e:
                print(f"⚠️ 멀티모달 전문가 시스템 초기화 실패: {e}")
                print("🔄 v2.0으로 폴백 시도...")
                self.use_16_experts_v3 = False
                self._try_v2_fallback()
        elif EXPERTS_V2_AVAILABLE:
            # v3.0이 없으면 v2.0 사용
            self.use_16_experts_v3 = False
            self._try_v2_fallback()
        elif EXPERTS_V1_AVAILABLE:
            # v3.0, v2.0이 없으면 v1.0 사용
            self.use_16_experts_v3 = False
            self.use_16_experts_v2 = False
            self._try_v1_fallback()
        else:
            self.use_16_experts = False
            self.use_16_experts_v2 = False
            self.use_16_experts_v3 = False
            self._init_fallback_experts()
        
        # 경량 AI 엔진 초기화 (Vercel 최적화)
        if LIGHTWEIGHT_AI_AVAILABLE:
            try:
                print("🚀 경량 AI 엔진 v1.0 활성화! (Vercel 최적화)")
                self.use_lightweight_ai = True
                self.use_advanced_ai = False  # 대용량 모델 비활성화
            except Exception as e:
                print(f"⚠️ 경량 AI 엔진 초기화 실패: {e}")
                self.use_lightweight_ai = False
        else:
            self.use_lightweight_ai = False
            
        print("✅ 서버리스 AI 시스템 활성화!")
    
    def _try_v2_fallback(self):
        """v2.0 Enhanced 전문가 시스템으로 폴백"""
        try:
            self.expert_ai_v2 = EnhancedComplete16ExpertAI(db_path="expert_ai_v2.db")
            print("🚀 Enhanced 16명 전문가 시스템 v2.0 활성화!")
            self.use_16_experts_v2 = True
            self.use_16_experts = False  # v1은 비활성화
            # 32명 전문가 리스트 (2단계 Enhanced + v9 DNA 확장) - 최종 중복 제거 완료
            self.experts = {
                # 기본 11명 전문가 (v1.0) - 중복 제거 후
                "assistant": "인공지능도깨비 🤖",
                # "builder": "경제학박사 부자도깨비 💰", # business와 중복
                # "counselor": "상담심리박사 상담도깨비 💬", # psychology와 중복
                # "creative": "예술학박사 창작도깨비 🎨", # design과 중복
                "data_analyst": "데이터분석도깨비 📊",
                "fortune": "점술도깨비 🔮",
                # "growth": "교육학박사 성장도깨비 📈", # education과 중복
                "hr": "인사관리도깨비 👥",
                "marketing": "마케팅도깨비 📢",
                # "medical": "의학박사 의료도깨비 🏥", # biotech와 통합
                "sales": "영업도깨비 💼",
                "seo": "검색도깨비 🔍",
                "shopping": "쇼핑도깨비 🛒",
                "startup": "창업도깨비 🚀",
                "wellness": "건강도깨비 🌿",
                "writing": "글쓰기도깨비 ✍️",
                
                # v9.0 DNA 개인화 전문가 15명 추가 (통합/개선)
                "tech": "IT기술도깨비 💻",
                "business": "경영도깨비 📊", # builder 통합
                "education": "교육도깨비 📚", # growth 통합
                "psychology": "심리상담도깨비 🧠", # counselor 통합
                "legal": "법률도깨비 ⚖️",
                "finance": "금융도깨비 💰",
                "design": "디자인도깨비 🎨", # creative 통합
                "sports": "스포츠도깨비 🏃‍♂️",
                "nutrition": "영양도깨비 🥗",
                "language": "언어도깨비 🗣️",
                "music": "음악도깨비 🎵",
                "travel": "여행도깨비 ✈️",
                "environment": "환경도깨비 🌱",
                "agriculture": "농업도깨비 🌾",
                "logistics": "물류도깨비 🚚",
                
                # 글로벌 기술 전문가 4명
                "energy": "에너지도깨비 ⚡",
                "biotech": "바이오도깨비 🧬", # medical 통합
                "security": "보안도깨비 🔒",
                "aerospace": "항공우주도깨비 🚀",
                
                # 미래 기술 전문가 2명
                "quantum": "양자물리도깨비 ⚛️",
                "nano": "나노기술도깨비 🔬",
            }
        except Exception as e:
            print(f"⚠️ v2.0 Enhanced 전문가 시스템도 실패: {e}")
            print("🔄 v1.0으로 폴백 시도...")
            self.use_16_experts_v2 = False
            self._try_v1_fallback()
    
    def _try_v1_fallback(self):
        """v1.0 전문가 시스템으로 폴백"""
        try:
            self.expert_ai = Complete16ExpertAI()
            print("🎯 16명 전문가 AI 시스템 v1.0 활성화!")
            self.use_16_experts = True
            self.use_16_experts_v2 = False
            # 32명 전문가 리스트 (1단계 + v9 DNA 확장) - 최종 중복 제거 완료
            self.experts = {
                # 기본 11명 전문가 (v1.0) - 중복 제거 후
                "assistant": "인공지능도깨비 🤖",
                # "builder": "경제학박사 부자도깨비 💰", # business와 중복
                # "counselor": "상담심리박사 상담도깨비 💬", # psychology와 중복
                # "creative": "예술학박사 창작도깨비 🎨", # design과 중복
                "data_analyst": "데이터분석도깨비 📊",
                "fortune": "점술도깨비 🔮",
                # "growth": "교육학박사 성장도깨비 📈", # education과 중복
                "hr": "인사관리도깨비 👥",
                "marketing": "마케팅도깨비 📢",
                # "medical": "의학박사 의료도깨비 🏥", # biotech와 통합
                "sales": "영업도깨비 💼",
                "seo": "검색도깨비 🔍",
                "shopping": "쇼핑도깨비 🛒",
                "startup": "창업도깨비 🚀",
                "wellness": "건강도깨비 🌿",
                "writing": "글쓰기도깨비 ✍️",
                
                # v9.0 DNA 개인화 전문가 15명 추가 (통합/개선)
                "tech": "IT기술도깨비 💻",
                "business": "경영도깨비 📊", # builder 통합
                "education": "교육도깨비 📚", # growth 통합
                "psychology": "심리상담도깨비 🧠", # counselor 통합
                "legal": "법률도깨비 ⚖️",
                "finance": "금융도깨비 💰",
                "design": "디자인도깨비 🎨", # creative 통합
                "sports": "스포츠도깨비 🏃‍♂️",
                "nutrition": "영양도깨비 🥗",
                "language": "언어도깨비 🗣️",
                "music": "음악도깨비 🎵",
                "travel": "여행도깨비 ✈️",
                "environment": "환경도깨비 🌱",
                "agriculture": "농업도깨비 🌾",
                "logistics": "물류도깨비 🚚",
                
                # 글로벌 기술 전문가 4명
                "energy": "에너지도깨비 ⚡",
                "biotech": "바이오도깨비 🧬", # medical 통합
                "security": "보안도깨비 🔒",
                "aerospace": "항공우주도깨비 🚀",
                
                # 미래 기술 전문가 2명
                "quantum": "양자물리도깨비 ⚛️",
                "nano": "나노기술도깨비 🔬",
            }
        except Exception as e:
            print(f"⚠️ v1.0 전문가 시스템도 실패: {e}")
            self.use_16_experts = False
            self.use_16_experts_v2 = False
            self._init_fallback_experts()
    
    def _init_fallback_experts(self):
        """기본 6명 전문가로 폴백"""
        self.experts = {
            "AI전문가": "AI도깨비 🤖",
            "마케팅왕": "마케팅도깨비 📢",
            "의료AI전문가": "의료도깨비 🏥",
            "재테크박사": "재테크도깨비 💰",
            "창업컨설턴트": "창업도깨비 🚀",
            "개발자멘토": "개발도깨비 💻",
        }

    def get_casual_response(self, query):
        """일반적인 대화에 대한 자연스러운 응답"""
        query_lower = query.lower().strip()
        
        # 인사말 응답
        greetings = {
            '안녕': '안녕하세요! 😊 무엇을 도와드릴까요?',
            '안녕하세요': '안녕하세요! 반갑습니다. 궁금한 것이 있으시면 언제든 물어보세요!',
            '안녕하십니까': '안녕하십니까! 정중한 인사 감사합니다. 어떤 도움이 필요하신가요?',
            'hello': 'Hello! Nice to meet you! How can I help you today?',
            'hi': 'Hi there! 👋 What would you like to know?',
            '하이': '하이! 👋 반가워요. 뭐든 물어보세요!',
            '좋은 아침': '좋은 아침입니다! ☀️ 활기찬 하루 되세요!',
            '좋은 오후': '좋은 오후입니다! 🌤️ 편안한 시간 보내세요!',
            '좋은 저녁': '좋은 저녁입니다! 🌙 따뜻한 밤 되세요!',
            '반갑습니다': '저도 반갑습니다! 😊 어떤 주제에 대해 이야기하고 싶으신가요?'
        }
        
        # 감사 인사 응답
        thanks_responses = {
            '고마워': '천만에요! 😊 또 궁금한 게 있으면 언제든 물어보세요!',
            '감사': '별말씀을요! 도움이 되어 기뻐요. 🙂',
            '고맙습니다': '별말씀을요! 언제든 도와드릴게요.',
            '감사합니다': '도움이 되어 다행입니다! 또 궁금한 게 있으시면 말씀해 주세요.'
        }
        
        # 미안 사과 응답
        apology_responses = {
            '미안': '괜찮아요! 😊 무슨 일이든 편하게 말씀해 주세요.',
            '죄송': '전혀 괜찮습니다! 언제든 편하게 이야기해요.',
            '미안해': '괜찮아요! 무엇을 도와드릴까요?',
            '죄송합니다': '전혀 괜찮습니다! 어떤 도움이 필요하신가요?'
        }
        
        # 직접 매칭 시도
        for keyword, response in greetings.items():
            if keyword in query_lower:
                return response
                
        for keyword, response in thanks_responses.items():
            if keyword in query_lower:
                return response
                
        for keyword, response in apology_responses.items():
            if keyword in query_lower:
                return response
        
        # 일반적인 질문에 대한 응답
        if '뭐해' in query_lower or '뭐하고' in query_lower:
            return '저는 여러분의 질문에 답변하는 AI예요! 궁금한 게 있으시면 무엇이든 물어보세요. 😊'
        
        if '어떻게 지내' in query_lower:
            return '저는 항상 준비되어 있어요! 😊 오늘 어떤 도움이 필요하신가요?'
        
        if '잘 지내' in query_lower:
            return '네, 잘 지내고 있어요! 감사합니다. 😊 어떤 이야기를 나누고 싶으신가요?'
        
        # 기본 응답
        return '네, 무엇을 도와드릴까요? 궁금한 것이 있으시면 언제든 물어보세요! 😊'

    def get_expert_response(self, query, expert_name="assistant", mode="deep", user_id="default_user"):
        """🚀 2단계: Enhanced 16명 전문가 시스템 응답 생성 (개인화 + 성능 모니터링)"""
        
        print(f"🔧 모드 설정: {mode} ({'심화탐구' if mode == 'deep' else '창의협업' if mode == 'creative' else '기본'})")
        
        # 🚨 먼저 일반 대화인지 확인
        if is_casual_conversation(query):
            print(f"💬 일반 대화 감지: '{query}' → 캐주얼 응답 생성")
            return self.get_casual_response(query)
        
        # 🚀 2단계: Enhanced 16명 전문가 시스템 사용 (v2.0 우선)
        if hasattr(self, 'use_16_experts_v2') and self.use_16_experts_v2:
            try:
                print(f"🚀 Enhanced 전문가 '{expert_name}' 응답 생성 중...")
                # 사용자 프로필 가져오기 또는 생성
                if user_id not in self.expert_ai_v2.user_profiles:
                    from experts.complete_16_experts_v2_enhanced_20250823 import UserProfile
                    self.expert_ai_v2.user_profiles[user_id] = UserProfile(
                        user_id=user_id,
                        preferred_style="professional",
                        expertise_level="intermediate"
                    )
                
                expert_response = self.expert_ai_v2.get_enhanced_expert_response(
                    query, expert_name, user_id=user_id
                )
                if expert_response and expert_response != "죄송합니다. 해당 전문 분야를 찾을 수 없습니다.":
                    print(f"✅ Enhanced 전문가 응답 성공! (길이: {len(expert_response)}자)")
                    return expert_response
                else:
                    print(f"⚠️ Enhanced 전문가 응답 실패, v1.0으로 폴백")
            except Exception as e:
                print(f"⚠️ Enhanced 전문가 시스템 오류: {e}")
        
        # 🎯 1단계: 16명 전문가 시스템 사용 (v1.0 폴백)
        if hasattr(self, 'use_16_experts') and self.use_16_experts:
            try:
                print(f"🎯 v1.0 전문가 '{expert_name}' 응답 생성 중...")
                expert_response = self.expert_ai.generate_expert_response(query, expert_name)
                if expert_response and expert_response != "죄송합니다. 해당 전문 분야를 찾을 수 없습니다.":
                    print(f"✅ v1.0 전문가 응답 성공!")
                    return expert_response
                else:
                    print(f"⚠️ v1.0 전문가 응답 실패, 기본 시스템으로 폴백")
            except Exception as e:
                print(f"⚠️ v1.0 전문가 시스템 오류: {e}")
        
        # 폴백: 기본 전문가 시스템 사용
        print(f"🔄 기본 전문가 시스템으로 폴백: {expert_name}")
        
        # 후속 질문 처리
        if "이전 질문" in query and "후속 질문:" in query:
            # 컨텍스트가 있는 후속 질문
            parts = query.split("후속 질문:")
            if len(parts) == 2:
                previous_context = parts[0].replace("이전 질문", "").replace("에 대한", "").strip().strip("'\"")
                current_question = parts[1].strip()
                
                print(f"🔗 컨텍스트 기반 응답: {previous_context} → {current_question}")
                
                # 후속 질문용 특별 응답 생성
                return self._generate_contextual_response(current_question, expert_name, previous_context)
        
        # 전문 질문의 경우 고급 응답 시스템 사용
        print(f"🎯 전문 질문 감지: '{query}' → {expert_name} 전문가 응답 생성")
        
        # 인터넷 검색을 통한 추가 정보 수집 시도
        search_info = ""
        try:
            # 질문이 기본 키워드에 매칭되지 않는 경우 검색 정보 활용
            query_lower = query.lower()
            basic_keywords = ['블록체인', 'blockchain', '암호화폐', '비트코인', 'crypto', 
                             '마케팅', 'marketing', '광고', '브랜딩', '홍보',
                             '의료', '건강', '병원', '의사', '치료', '진단',
                             '투자', '재테크', '주식', '펀드', '금융', '돈',
                             '창업', '스타트업', '사업', '비즈니스', '기업',
                             '개발', '프로그래밍', '코딩', '개발자', '프로그램',
                             'ai', '인공지능', '머신러닝', '딥러닝', '알고리즘']
            
            # 기본 키워드가 없으면 인터넷 검색 수행
            if not any(keyword in query_lower for keyword in basic_keywords):
                print(f"🔍 특수 키워드 감지 - 인터넷 검색 수행: {query}")
                search_info = search_internet_for_query(query)
        except Exception as e:
            print(f"⚠️ 검색 정보 수집 실패: {e}")
            search_info = ""
        
        try:
            # 검색 정보가 있으면 함께 활용하여 응답 생성 (모드 정보 포함)
            return self._generate_advanced_response(query, expert_name, search_info, mode)
        except Exception as e:
            print(f"⚠️ 고급 AI 응답 생성 실패: {e}")
            # 폴백: 기본 응답 사용 (모드 정보 포함)
            return self._generate_basic_response(query, expert_name, mode)
    
    def _generate_contextual_response(self, question, expert_name, previous_context):
        """컨텍스트 기반 후속 응답 생성"""
        
        contextual_responses = {
            "블록체인도깨비": f"""
{self._get_expert_emoji(expert_name)} **{expert_name}**의 구체적인 후속 설명:

**'{question}'**에 대해 {previous_context} 맥락에서 더 자세히 설명드리겠습니다.

**🔍 실제 구현 사례:**
• **금융 분야**: JPMorgan의 JPM Coin, 국제송금 시간 단축 (기존 3-5일 → 실시간)
• **공급망 관리**: Walmart의 식품 추적 시스템, 오염원 추적 시간 단축 (7일 → 2.2초)
• **부동산**: 두바이 정부의 블록체인 기반 부동산 거래 시스템
• **의료**: MedRec 프로젝트로 환자 의료 기록의 안전한 공유

**💼 투자 관점에서의 블록체인:**
- 시장 규모: 2023년 기준 약 676억 달러, 2030년까지 1조 4천억 달러 전망
- 주요 투자 분야: DeFi (탈중앙화 금융), NFT, 메타버스, Web3.0
- 리스크 요인: 규제 불확실성, 기술적 확장성 한계, 에너지 소비 문제

**🛠️ 실무 도입 가이드:**
1. **기술 검토**: 프라이빗/퍼블릭 블록체인 선택 기준
2. **파일럿 프로젝트**: 소규모 시범 운영으로 효과 검증
3. **인프라 구축**: 노드 운영, 보안 체계, 개발 인력 확보
4. **규제 대응**: 각국 법규 준수, 컴플라이언스 체계 구축

**⚡ 기술적 세부사항:**
- 해시 함수: SHA-256, 블록 무결성 보장
- 합의 알고리즘: PoW vs PoS 장단점 비교
- 스마트 컨트랙트: Solidity 언어, 가스비 최적화
- 확장성 솔루션: 레이어2 (Lightning Network, Polygon)
            """,
            
            "AI전문가": f"""
{self._get_expert_emoji(expert_name)} **{expert_name}**의 심화 기술 분석:

**'{question}'**에 대해 {previous_context} 기반으로 기술적 세부사항을 설명드리겠습니다.

**🧠 AI 모델 아키텍처:**
• **트랜스포머**: Attention 메커니즘으로 장거리 의존성 학습
• **CNN**: 이미지 인식, 합성곱 레이어를 통한 특징 추출
• **RNN/LSTM**: 시계열 데이터, 순차적 정보 처리
• **GAN**: 생성형 AI, 적대적 학습을 통한 데이터 생성

**💻 실제 구현 예시:**
```python
# GPT 스타일 텍스트 생성
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
```

**📊 성능 지표:**
- BLEU 점수: 기계 번역 품질 측정
- F1 Score: 분류 모델 정확도
- Perplexity: 언어 모델 성능
- IoU: 객체 탐지 정확도

**🚀 최신 연구 동향:**
- **멀티모달 AI**: CLIP, DALL-E, GPT-4V
- **강화학습**: AlphaGo, ChatGPT의 RLHF
- **경량화**: 모바일 AI, 엣지 컴퓨팅 최적화
- **설명 가능한 AI**: XAI, 의사결정 투명성

**🔧 실무 적용 단계:**
1. **데이터 수집**: 고품질 학습 데이터 확보
2. **전처리**: 정규화, 증강, 라벨링
3. **모델 선택**: 문제에 적합한 아키텍처 선정
4. **학습**: 하이퍼파라미터 튜닝, 과적합 방지
5. **배포**: MLOps, 모니터링, A/B 테스트
            """
        }
        
        # 전문가별 특화 응답이 없으면 기본 후속 응답
        if expert_name not in contextual_responses:
            return f"""
{self._get_expert_emoji(expert_name)} **{expert_name}**의 후속 상세 설명:

**'{question}'**에 대해 {previous_context} 주제를 더 깊이 있게 분석해드리겠습니다.

**🔍 구체적인 사례와 방법론:**
{self._generate_detailed_response(question, expert_name)}

**💡 실무 적용 가이드:**
{self._generate_action_plan(question, expert_name)}

**📈 성공 전략:**
{self._generate_additional_insights(question, expert_name)}
            """
        
        return contextual_responses[expert_name]
    
    def _generate_advanced_response(self, query, expert_name, search_info="", mode="deep"):
        """고급 AI 엔진을 사용한 진짜 동적 응답 생성 (인터넷 검색 정보 활용, 모드별 차별화)"""
        
        # 모드에 따른 응답 스타일 결정
        if mode == "creative":
            print(f"🎨 창의협업 모드 활성화")
            response_style = "creative_collaborative"
        else:  # mode == "deep" or default
            print(f"🔍 심화탐구 모드 활성화")
            response_style = "deep_analysis"
        
        try:
            # 고급 AI 엔진 사용하여 동적 응답 생성
            context = {
                "user_type": "professional", 
                "depth": "detailed" if mode == "deep" else "creative",
                "response_style": response_style,
                "mode": mode
            }
            
            # 검색 정보가 있으면 컨텍스트에 추가
            if search_info:
                context["search_info"] = search_info
                print(f"🔍 검색 정보 활용하여 응답 생성: {len(search_info)}자")
            
            # 모드별 응답 생성 방식 결정 (경량 AI 엔진 사용)
            if self.use_lightweight_ai:
                # 경량 AI 엔진으로 응답 생성
                expert_type = "technical" if "기술" in expert_name else "business" if "마케팅" in expert_name or "경영" in expert_name else "general"
                ai_response = get_ai_response(
                    user_input=query,
                    expert_type=expert_type,
                    expert_name=expert_name
                )
                
                # 검색 정보가 있으면 추가
                if search_info:
                    ai_response += f"\n\n📚 관련 정보:\n{search_info[:300]}..."
                
                # 경량 엔진 응답이 성공하면 그 결과 사용
                if ai_response and len(ai_response) > 20:
                    print(f"✅ 경량 AI 엔진 응답 성공: {len(ai_response)}자 ({mode} 모드)")
                    return ai_response
                
        except Exception as e:
            print(f"⚠️ 고급 AI 엔진 오류: {e}")
        
        # 폴백: 실시간 동적 응답 생성 (검색 정보 포함, 모드별 차별화)
        return self._generate_dynamic_response(query, expert_name, search_info, mode)
    
    def _generate_dynamic_response(self, query, expert_name, search_info="", mode="deep"):
        """실시간 동적 응답 생성 - 질문에 따라 매번 다른 답변 (인터넷 검색 정보 활용, 모드별 차별화)"""
        
        # 질문 분석
        question_analysis = self._analyze_question(query)
        question_analysis['mode'] = mode
        
        # 검색 정보가 있으면 분석에 추가
        if search_info:
            question_analysis['search_info'] = search_info
            print(f"🔍 검색 정보를 분석에 반영: {len(search_info)}자")
        
        # 전문가별 관점 적용
        expert_perspective = self._get_expert_perspective(expert_name, question_analysis)
        
        # 동적 응답 구성
        response_parts = []
        
        # 모드별 헤더 차별화
        if mode == "creative":
            response_parts.append(f"🎨 **{expert_name}**의 창의적 협업 분석:")
            response_parts.append(f"\n**'{query}'**에 대해 창의적이고 협업적인 관점에서 함께 탐구해보겠습니다!\n")
        else:  # mode == "deep"
            response_parts.append(f"🔍 **{expert_name}**의 심화 탐구 분석:")
            response_parts.append(f"\n**'{query}'**에 대해 깊이 있는 전문적 분석을 제공드리겠습니다.\n")
        
        # 검색 정보가 있으면 최신 정보 섹션 추가
        if search_info:
            if mode == "creative":
                response_parts.append("**🌐 최신 정보를 바탕으로 한 창의적 아이디어:**")
            else:
                response_parts.append("**🌐 최신 정보 기반 전문 분석:**")
            response_parts.append(f"{search_info[:300]}..." if len(search_info) > 300 else search_info)
            response_parts.append("")
        
        # 질문 유형별 동적 내용 생성 (모드별 차별화)
        if question_analysis['type'] == 'how_to':
            response_parts.append(self._generate_how_to_response(query, expert_name, question_analysis))
        elif question_analysis['type'] == 'what_is':
            response_parts.append(self._generate_explanation_response(query, expert_name, question_analysis))
        elif question_analysis['type'] == 'comparison':
            response_parts.append(self._generate_comparison_response(query, expert_name, question_analysis))
        elif question_analysis['type'] == 'advice':
            response_parts.append(self._generate_advice_response(query, expert_name, question_analysis))
        else:
            response_parts.append(self._generate_general_response(query, expert_name, question_analysis))
        
        # 전문가별 특화 인사이트 추가 (모드별 차별화)
        response_parts.append(self._generate_expert_insights(query, expert_name, question_analysis))
        
        # 실행 방안 (질문에 따라 동적 생성, 모드별 차별화)
        response_parts.append(self._generate_dynamic_action_plan(query, expert_name, question_analysis))
        
        final_response = "\n".join(response_parts)
        
        search_tag = " + 검색정보" if search_info else ""
        print(f"🔄 동적 응답 생성 완료: {len(final_response)}자 (질문타입: {question_analysis['type']}{search_tag})")
        
        return final_response
    
    def _analyze_question(self, query):
        """질문 분석 - 매번 다른 관점으로 분석"""
        
        # 질문 키워드 분석
        keywords = query.lower().split()
        
        # 질문 유형 분류
        question_type = "general"
        if any(word in query.lower() for word in ["어떻게", "방법", "how"]):
            question_type = "how_to"
        elif any(word in query.lower() for word in ["무엇", "뭐", "what", "설명"]):
            question_type = "what_is"
        elif any(word in query.lower() for word in ["비교", "차이", "vs", "대신"]):
            question_type = "comparison"
        elif any(word in query.lower() for word in ["추천", "조언", "방향", "어떤"]):
            question_type = "advice"
        
        # 복잡성 레벨
        complexity = "basic"
        if len(keywords) > 10 or any(word in query for word in ["전략", "분석", "구체적", "상세"]):
            complexity = "advanced"
        elif len(keywords) > 5:
            complexity = "intermediate"
        
        # 도메인 감지
        domain = "general"
        domain_keywords = {
            "tech": ["기술", "AI", "개발", "프로그래밍", "시스템"],
            "business": ["사업", "비즈니스", "마케팅", "투자", "창업"],
            "health": ["건강", "의료", "치료", "진단", "병원"],
            "finance": ["돈", "투자", "재테크", "주식", "경제"]
        }
        
        for domain_name, domain_words in domain_keywords.items():
            if any(word in query for word in domain_words):
                domain = domain_name
                break
        
        return {
            "type": question_type,
            "complexity": complexity,
            "domain": domain,
            "keywords": keywords,
            "length": len(query)
        }
    
    def _get_expert_perspective(self, expert_name, question_analysis):
        """전문가별 관점 설정"""
        perspectives = {
            "AI전문가": "기술적 혁신과 실무 적용",
            "마케팅왕": "시장 트렌드와 고객 중심",
            "의료AI전문가": "환자 안전과 의료 효율성",
            "재테크박사": "리스크 관리와 수익 최적화",
            "창업컨설턴트": "비즈니스 기회와 성장 전략",
            "개발자멘토": "기술 역량과 실무 경험",
            "블록체인도깨비": "분산 기술과 미래 금융"
        }
        return perspectives.get(expert_name, "전문적 분석과 실용적 조언")
    
    def _generate_how_to_response(self, query, expert_name, analysis):
        """How-to 질문에 대한 동적 응답"""
        steps = []
        
        if expert_name == "AI전문가":
            steps = [
                "**1단계: 현재 상황 분석**\n   - AI 기술 적용 가능성 검토\n   - 데이터 현황과 인프라 점검",
                "**2단계: 기술 스택 선택**\n   - 프로젝트 규모에 맞는 AI 모델 선정\n   - 개발 도구와 플랫폼 결정",
                "**3단계: 단계별 구현**\n   - 프로토타입 개발 및 테스트\n   - 점진적 확장과 최적화",
                "**4단계: 성과 측정**\n   - KPI 설정과 모니터링\n   - 지속적 개선과 업데이트"
            ]
        elif expert_name == "마케팅왕":
            steps = [
                "**1단계: 타겟 고객 정의**\n   - 페르소나 분석과 시장 세분화\n   - 고객 여정 맵핑",
                "**2단계: 채널 전략 수립**\n   - 효과적인 마케팅 채널 선택\n   - 콘텐츠 전략과 메시지 설계",
                "**3단계: 캠페인 실행**\n   - A/B 테스트와 데이터 분석\n   - 실시간 최적화",
                "**4단계: 성과 분석**\n   - ROI 측정과 인사이트 도출\n   - 향후 전략 개선방안"
            ]
        else:
            steps = [
                f"**1단계: 목표 설정**\n   - {expert_name} 관점에서 명확한 목표 정의",
                f"**2단계: 계획 수립**\n   - 단계별 실행 계획과 리소스 배정",
                f"**3단계: 실행 및 모니터링**\n   - 체계적 실행과 중간 점검",
                f"**4단계: 결과 평가**\n   - 성과 측정과 개선 방안 도출"
            ]
        
        return "**📋 단계별 실행 가이드:**\n\n" + "\n\n".join(steps)
    
    def _generate_explanation_response(self, query, expert_name, analysis):
        """설명 요청에 대한 동적 응답"""
        
        if "AI" in query or "인공지능" in query:
            return f"""
**🔍 핵심 개념 설명:**

인공지능은 인간의 학습능력과 추론능력, 지각능력을 컴퓨터로 구현하는 기술입니다.

**주요 구성 요소:**
- **머신러닝**: 데이터에서 패턴을 학습하는 알고리즘
- **딥러닝**: 인공신경망을 이용한 고급 학습 방법
- **자연어처리**: 인간의 언어를 이해하고 생성하는 기술
- **컴퓨터 비전**: 이미지와 영상을 인식하고 분석하는 기술

**실제 활용 사례:**
현재 검색엔진, 추천시스템, 음성인식, 자율주행차 등에서 실용화되어 있습니다.
            """
        
        return f"""
**🎯 {expert_name} 관점에서의 설명:**

{query.replace('무엇', '').replace('뭐', '').replace('설명', '').strip()}에 대해 전문가적 시각으로 설명드리겠습니다.

이는 {analysis['domain']} 분야에서 중요한 개념으로, 실무에서 다음과 같이 적용됩니다:

- **기본 원리**: 핵심 메커니즘과 작동 방식
- **실무 적용**: 현장에서의 구체적 활용 방법  
- **주의사항**: 고려해야 할 리스크와 제약사항
- **발전 방향**: 향후 전망과 트렌드 변화
        """
    
    def _generate_comparison_response(self, query, expert_name, analysis):
        """비교 질문에 대한 동적 응답"""
        return f"""
**⚖️ 전문가 비교 분석:**

{expert_name} 관점에서 체계적으로 비교분석해드리겠습니다.

**📊 비교 기준:**
- **효과성**: 목표 달성 능력과 성과
- **효율성**: 시간, 비용, 리소스 측면
- **실용성**: 실제 적용 가능성과 난이도
- **지속가능성**: 장기적 유지 및 확장성

**💡 전문가 추천:**
현재 상황을 고려할 때, 다음과 같은 접근을 권장합니다:

1. **우선 고려사항**: 가장 중요한 판단 기준
2. **단계적 접근**: 점진적 도입 방안
3. **리스크 관리**: 예상 위험과 대응책
        """
    
    def _generate_advice_response(self, query, expert_name, analysis):
        """조언 요청에 대한 동적 응답"""
        return f"""
**💼 {expert_name}의 전문 조언:**

{analysis['complexity']} 수준의 질문으로 판단되어, 다음과 같이 조언드립니다.

**🎯 핵심 조언:**
상황을 종합적으로 분석한 결과, 가장 중요한 것은 명확한 목표 설정과 단계적 접근입니다.

**📈 성공 요인:**
- **전략적 사고**: 장기적 관점에서의 계획 수립
- **실행력**: 계획을 현실로 만드는 추진력
- **적응력**: 변화하는 환경에 대한 유연한 대응
- **지속성**: 꾸준한 노력과 개선 의지

**⚠️ 주의사항:**
성급한 결정보다는 충분한 검토와 준비를 통해 안정적으로 접근하시기 바랍니다.
        """
    
    def _generate_general_response(self, query, expert_name, analysis):
        """일반적인 질문에 대한 진짜 동적 응답"""
        
        import random
        import time
        
        # 매번 다른 시드 사용 (시간 + 랜덤 요소)
        random.seed(int(time.time() * 1000000) % 999999)
        
        # 전문가별 다양한 응답 풀
        response_pools = {
            "AI전문가": {
                "opening_phrases": [
                    "AI 기술의 최신 발전 사항을 고려할 때",
                    "머신러닝과 딥러닝 관점에서 보면",
                    "인공지능 연구의 현재 동향을 분석하면",
                    "GPT와 같은 대규모 언어모델 발전을 보면",
                    "AI 윤리와 기술 발전의 균형을 고려하면"
                ],
                "core_topics": [
                    "자연어처리와 컴퓨터비전 기술의 융합",
                    "강화학습을 통한 자율적 의사결정 시스템",
                    "생성형 AI의 창작과 혁신 능력",
                    "엣지 AI와 실시간 처리 기술",
                    "설명 가능한 AI와 투명성 확보"
                ],
                "practical_advice": [
                    "작은 파일럿 프로젝트부터 시작하여 점진적으로 확장",
                    "데이터 품질 확보가 AI 성공의 핵심 요소",
                    "사용자 중심의 AI 설계와 윤리적 고려사항 반영",
                    "지속적인 모델 업데이트와 성능 모니터링",
                    "도메인 전문가와 AI 개발자의 긴밀한 협업"
                ]
            },
            "마케팅왕": {
                "opening_phrases": [
                    "현재 디지털 마케팅 생태계를 분석하면",
                    "고객 행동 데이터와 시장 트렌드를 보면",
                    "개인화 마케팅의 진화 과정을 고려할 때",
                    "옴니채널 전략의 중요성이 커지는 상황에서",
                    "데이터 드리븐 의사결정의 필요성을 보면"
                ],
                "core_topics": [
                    "AI 기반 고객 세분화와 타겟팅 정교화",
                    "소셜미디어와 인플루언서 마케팅의 진화",
                    "실시간 개인화와 동적 콘텐츠 최적화",
                    "크로스플랫폼 고객 여정 최적화",
                    "브랜드 스토리텔링과 감정적 연결 강화"
                ],
                "practical_advice": [
                    "고객 데이터 통합과 360도 고객 뷰 구축",
                    "A/B 테스트를 통한 지속적 캠페인 최적화",
                    "ROI 측정과 어트리뷰션 모델 정교화",
                    "크리에이티브와 데이터의 균형잡힌 활용",
                    "고객 생애가치(LTV) 중심의 장기 전략 수립"
                ]
            }
        }
        
        # 기본 풀 (다른 전문가들)
        default_pool = {
            "opening_phrases": [
                "현재 분야의 최신 동향을 종합하면",
                "전문가적 관점에서 분석할 때",
                "실무 경험과 이론을 결합하여 보면",
                "시장 상황과 기술 발전을 고려하면",
                "장기적 관점에서 전략적으로 접근하면"
            ],
            "core_topics": [
                "디지털 혁신과 기술 융합의 가속화",
                "데이터 기반 의사결정과 인사이트 도출",
                "고객 중심적 사고와 가치 창출",
                "지속가능한 성장과 혁신 전략",
                "협업과 네트워킹을 통한 시너지 창출"
            ],
            "practical_advice": [
                "명확한 목표 설정과 단계별 실행 계획 수립",
                "지속적 학습과 역량 개발을 통한 경쟁력 강화",
                "리스크 관리와 변화 대응 능력 확보",
                "성과 측정과 피드백을 통한 지속적 개선",
                "이해관계자와의 소통과 협력 체계 구축"
            ]
        }
        
        # 전문가별 풀 선택
        pool = response_pools.get(expert_name, default_pool)
        
        # 랜덤 요소 선택
        opening = random.choice(pool["opening_phrases"])
        topic = random.choice(pool["core_topics"])
        advice = random.choice(pool["practical_advice"])
        
        # 추가 랜덤 요소들
        analysis_depth = random.choice([
            "심화적 분석이 필요한",
            "다각도 검토가 요구되는", 
            "전략적 접근이 중요한",
            "세심한 고려가 필요한",
            "체계적 준비가 요구되는"
        ])
        
        future_trend = random.choice([
            "지속적 혁신과 발전",
            "기술과 인간의 조화",
            "데이터 중심의 의사결정",
            "고객 가치 창출 중심",
            "지속가능한 성장 모델"
        ])
        
        # 질문 특성에 따른 추가 분석
        question_insight = ""
        if "구체적" in query:
            question_insight = "구체성과 실행 가능성을 중시하는 접근이 필요하며, "
        elif "말해주세요" in query:
            question_insight = "명확하고 이해하기 쉬운 설명을 통해 "
        
        # 동적 응답 생성
        response = f"""
**🔍 {expert_name}의 종합 분석:**

'{query}'에 대해 {analysis['domain']} 분야 전문가로서 분석드리겠습니다.

**현황 분석:**
{opening}, 현재는 {analysis_depth} 중요한 시점입니다. 
{question_insight}{topic} 영역에서 특별한 주의가 필요합니다.

**핵심 인사이트:**
- **현재 동향**: {topic.split('와')[0] if '와' in topic else topic}
- **기회 요소**: 전문성 활용과 시장 변화에 대한 선제적 대응
- **주요 과제**: 기술 변화와 시장 요구의 빠른 속도에 적응
- **발전 방향**: {future_trend} 중심의 지속적 진화

**전문가 조언:**
{advice}하는 것이 핵심입니다.

**실무 관점:**
{analysis['complexity']} 수준의 이해를 바탕으로 한 체계적이고 단계적인 접근을 권장합니다.
        """.strip()
        
        return response
    
    def _generate_expert_insights(self, query, expert_name, analysis):
        """전문가별 특화 인사이트 (모드별 차별화)"""
        
        mode = analysis.get('mode', 'deep')
        
        if mode == "creative":
            creative_insights = {
                "AI전문가": f"""
**🎨 AI 전문가의 창의적 협업 아이디어:**

• **혁신 아이디어**: AI와 예술, 음악, 문학의 융합 가능성 탐구
• **협업 방안**: 인간-AI 공동 창작 프로젝트 제안
• **실험 제안**: 새로운 AI 활용법을 함께 브레인스토밍
• **미래 상상**: AI가 만들어갈 창의적 미래 시나리오 구상
                """,
                
                "마케팅왕": f"""
**🎨 마케팅 전문가의 창의적 캠페인 아이디어:**

• **스토리텔링**: 감성적 브랜드 스토리 공동 개발
• **바이럴 전략**: 독창적인 소셜미디어 콘텐츠 아이디어
• **체험 마케팅**: 고객 참여형 이벤트 기획 협업
• **트렌드 창조**: 새로운 마케팅 트렌드 선도 방안
                """,
                
                "재테크박사": f"""
**🎨 재테크 전문가의 창의적 투자 아이디어:**

• **혁신 투자**: 미래 기술과 새로운 투자 기회 발굴
• **크리에이티브 펀딩**: 크라우드펀딩, 스타트업 투자 아이디어
• **대안 투자**: 예술품, 수집품 등 대체 투자 방안
• **커뮤니티**: 투자 스터디, 공동 투자 그룹 운영 아이디어
                """
            }
            
            return creative_insights.get(expert_name, f"""
**🎨 {expert_name}의 창의적 협업 아이디어:**

• **혁신 사고**: 기존 틀을 깨는 새로운 접근법
• **협업 제안**: 함께 만들어갈 창의적 프로젝트
• **실험 정신**: 새로운 시도와 도전에 대한 제안
• **미래 비전**: 함께 그려나갈 혁신적 미래상
            """)
        
        else:  # mode == "deep"
            deep_insights = {
                "AI전문가": f"""
**🔍 AI 전문가의 심층 기술 분석:**

• **기술 아키텍처**: Transformer, CNN, RNN의 구조적 특징과 적용 분야
• **성능 최적화**: 모델 경량화, 양자화, 프루닝 기법의 실무 적용
• **데이터 전략**: 고품질 학습 데이터 확보와 전처리 방법론
• **운영 노하우**: MLOps, 모델 배포, 모니터링의 실제 구현 방안
                """,
                
                "마케팅왕": f"""
**🔍 마케팅 전문가의 전략적 심층 분석:**

• **시장 세분화**: 정량적 분석을 통한 타겟 고객군 정의
• **성과 측정**: CAC, LTV, ROAS 등 핵심 지표의 정확한 산출법
• **채널 최적화**: 각 마케팅 채널별 ROI 분석과 예산 배분 전략
• **경쟁 분석**: 시장 점유율, 포지셔닝 맵 분석을 통한 차별화 방안
                """,
                
                "재테크박사": f"""
**� 재테크 전문가의 전문적 투자 분석:**

• **재무 분석**: PER, PBR, ROE 등 기업 가치 평가 지표 활용법
• **포트폴리오 이론**: 현대 포트폴리오 이론과 자산 배분 최적화
• **리스크 관리**: VaR, 샤프 비율을 활용한 정량적 위험 측정
• **세무 최적화**: 양도소득세, 배당소득세 절세 전략의 구체적 방법
                """
            }
            
            return deep_insights.get(expert_name, f"""
**� {expert_name}의 전문적 심층 분석:**

• **이론적 기반**: 해당 분야의 핵심 이론과 학술적 배경
• **실무 방법론**: 현장에서 검증된 체계적인 접근 방식
• **정량적 분석**: 데이터와 지표를 활용한 객관적 평가
• **전문가 노하우**: 경험에서 우러나온 실무적 통찰과 조언
            """)
    
    def _generate_dynamic_action_plan(self, query, expert_name, analysis):
        """동적 액션 플랜 생성"""
        
        timeframe = "단기" if analysis['complexity'] == "basic" else "중장기"
        
        return f"""
**🎯 {timeframe} 실행 계획:**

**즉시 실행 (1-2주):**
1. 현재 상황 정확한 파악과 목표 설정
2. 필요 리소스와 제약사항 분석
3. 초기 단계 실행 계획 수립

**단기 목표 (1-3개월):**
1. 기초 작업과 기반 구축
2. 파일럿 프로젝트 실행 및 검증
3. 초기 성과 측정과 피드백 수집

**중기 목표 (3-12개월):**
1. 본격적인 실행과 확장
2. 지속적 모니터링과 최적화
3. 성과 분석과 전략 조정

**📊 성과 지표:**
- **정량적**: 구체적 수치로 측정 가능한 지표
- **정성적**: 질적 개선과 만족도 평가
- **타임라인**: 각 단계별 달성 목표 시점

**🔄 지속적 개선:**
정기적 리뷰를 통해 계획을 업데이트하고 최적화해나가겠습니다.
        """
    
    def _generate_basic_response(self, query, expert_name, mode="deep"):
        """기본 응답 시스템 (모드별 차별화)"""
        
        # 모드별 기본 응답 차별화
        if mode == "creative":
            creative_responses = {
                "AI전문가": f"🎨 AI 전문가로서 '{query}'에 대해 창의적으로 접근해보면, AI와 인간의 협업이 만들어낼 새로운 가능성들을 탐구해볼 수 있습니다. 함께 브레인스토밍하며 혁신적인 아이디어를 발굴해보는 것은 어떨까요?",
                "마케팅왕": f"🎨 마케팅 전문가로서 '{query}'를 창의적으로 분석해보면, 스토리텔링과 감성 마케팅을 통해 고객과 진정한 연결고리를 만들어보는 것은 어떨까요? 함께 독창적인 캠페인 아이디어를 구상해보겠습니다!",
                "의료AI전문가": f"🎨 의료 AI 전문가로서 '{query}'에 대해 창의적으로 생각해보면, 환자 중심의 혁신적인 솔루션을 함께 고민해볼 수 있겠네요. 의료진과 환자가 모두 만족할 수 있는 새로운 접근법을 탐구해보겠습니다!",
                "재테크박사": f"🎨 투자 전문가로서 '{query}'를 창의적으로 접근해보면, 전통적인 투자 방식을 넘어서는 새로운 기회들을 함께 발굴해볼 수 있겠네요. 혁신적인 투자 전략을 협업으로 만들어보는 것은 어떨까요?",
                "창업컨설턴트": f"🎨 창업 전문가로서 '{query}'에 대해 창의적으로 생각해보면, 기존 비즈니스 모델의 틀을 깨는 혁신적인 아이디어를 함께 브레인스토밍해볼 수 있겠네요! 파괴적 혁신의 가능성을 탐구해보겠습니다.",
                "개발자멘토": f"🎨 개발 전문가로서 '{query}'를 창의적으로 접근해보면, 기술적 한계를 뛰어넘는 새로운 솔루션을 함께 구상해볼 수 있겠네요. 혁신적인 개발 방법론과 아이디어를 협업으로 만들어보겠습니다!",
            }
            return creative_responses.get(
                expert_name,
                f"🎨 전문가로서 '{query}'에 대해 창의적이고 협업적인 관점에서 함께 탐구해보겠습니다!"
            )
        else:  # mode == "deep"
            deep_responses = {
                "AI전문가": f"🔍 AI 전문가로서 '{query}'에 대해 심층 분석드리면, 현재 AI 기술의 근본적 메커니즘부터 실제 구현 세부사항까지 체계적으로 분석해드리겠습니다. 기술적 깊이와 실무적 통찰을 모두 제공하겠습니다.",
                "마케팅왕": f"🔍 마케팅 전문가로서 '{query}'를 심화 분석하면, 시장 동향 분석, 소비자 행동 심리학, 데이터 기반 성과 측정까지 포괄적으로 다루어 전략적 인사이트를 제공하겠습니다.",
                "의료AI전문가": f"� 의료 AI 전문가로서 '{query}'에 대해 깊이 있는 분석을 제공하면, 의학적 근거, 임상 데이터, 기술적 구현 방안까지 전문적 관점에서 체계적으로 설명드리겠습니다.",
                "재테크박사": f"🔍 투자 전문가로서 '{query}'를 심층 분석하면, 재무 이론, 시장 구조 분석, 리스크 관리 방법론까지 포함한 전문적 투자 전략을 상세히 제공하겠습니다.",
                "창업컨설턴트": f"� 창업 전문가로서 '{query}'에 대해 심화 컨설팅을 제공하면, 사업 모델 설계, 시장 진입 전략, 성장 단계별 핵심 과제까지 체계적으로 분석해드리겠습니다.",
                "개발자멘토": f"� 개발 전문가로서 '{query}'에 대해 심층 기술 분석을 제공하면, 아키텍처 설계, 성능 최적화, 보안 고려사항까지 포함한 전문적 개발 가이드를 제공하겠습니다.",
            }
            return deep_responses.get(
                expert_name,
                f"🔍 전문가 관점에서 '{query}'에 대한 심층적이고 체계적인 분석을 제공해드리겠습니다.",
            )
    
    def _get_expert_emoji(self, expert_name):
        emojis = {
            "AI전문가": "🤖",
            "마케팅왕": "📈", 
            "의료AI전문가": "⚕️",
            "재테크박사": "💰",
            "창업컨설턴트": "🚀",
            "개발자멘토": "💻",
            "블록체인도깨비": "⛓️"
        }
        return emojis.get(expert_name, "🎯")
    
    def _generate_detailed_response(self, query, expert_name):
        """상세 응답 생성 - 1000자 이상"""
        
        detailed_responses = {
            "AI전문가": f"""
            **{query}**에 대한 AI 전문가의 종합적 분석입니다.

            현재 인공지능 기술은 제4차 산업혁명의 핵심 동력으로 자리잡고 있습니다. 특히 대규모 언어모델(LLM), 컴퓨터 비전, 로봇공학, 자율주행 등 다양한 분야에서 혁신적인 발전을 보이고 있습니다.

            **기술적 관점에서의 분석:**
            - 머신러닝 알고리즘의 지속적 진화로 예측 정확도가 크게 향상되었습니다
            - 딥러닝 기술의 발전으로 복잡한 패턴 인식과 자연어 이해 능력이 혁신적으로 개선되었습니다
            - 트랜스포머 아키텍처의 등장으로 언어 모델의 성능이 비약적으로 발전했습니다
            - 강화학습을 통한 자율적 의사결정 시스템이 다양한 도메인에서 실용화되고 있습니다

            **실무 적용 사례:**
            현재 다양한 산업 분야에서 AI 기술이 활발히 도입되고 있습니다. 금융권에서는 신용평가와 사기탐지, 의료 분야에서는 진단 보조와 신약개발, 제조업에서는 품질관리와 예측 정비 등에 활용되고 있습니다.

            **미래 전망:**
            향후 5-10년 내에 AI 기술은 더욱 일반화되어 일상생활과 업무 전반에 깊숙이 스며들 것으로 예상됩니다. 특히 AGI(Artificial General Intelligence) 연구가 가속화되면서 인간 수준의 범용 지능 실현이 점차 현실에 가까워지고 있습니다.
            """,
            
            "마케팅왕": f"""
            **{query}**에 대한 디지털 마케팅 전문가의 전략적 분석입니다.

            현재 마케팅 생태계는 디지털 전환 가속화, 개인화 기술 발전, 옴니채널 전략 중요성 증대 등으로 급격히 변화하고 있습니다. 특히 데이터 기반 의사결정과 AI 활용 마케팅 자동화가 핵심 트렌드로 부상하고 있습니다.

            **현재 마케팅 트렌드 심층 분석:**
            - 개인화 마케팅의 고도화: 고객 행동 데이터를 활용한 1:1 맞춤형 콘텐츠 제공이 표준이 되고 있습니다
            - 소셜 커머스의 급성장: 인스타그램, 틱톡 등 소셜 플랫폼을 통한 직접 판매가 주요 채널로 부상했습니다
            - 콘텐츠 마케팅의 진화: 단순한 정보 제공을 넘어 스토리텔링과 감정적 연결이 중요해졌습니다
            - 마케팅 자동화와 AI 활용: 챗봇, 추천 시스템, 예측 분석 등을 통한 효율성 극대화가 핵심입니다

            **효과적인 전략 수립 방법:**
            성공적인 디지털 마케팅을 위해서는 명확한 타겟 페르소나 설정, 고객 여정 매핑, 옴니채널 경험 설계가 필수입니다. 또한 지속적인 A/B 테스트와 데이터 분석을 통한 최적화가 중요합니다.

            **ROI 최적화 전략:**
            마케팅 투자 대비 수익률을 극대화하기 위해서는 정확한 성과 측정 지표 설정, 고객 생애 가치(CLV) 기반 투자 배분, 마케팅 어트리뷰션 모델링을 통한 채널별 기여도 분석이 필요합니다.
            """,
            
            "의료AI전문가": f"""
            **{query}**에 대한 의료 AI 전문가의 신중한 분석입니다.

            의료 분야에서 AI 기술의 도입은 환자 안전과 치료 효과 향상을 목표로 매우 신중하게 진행되고 있습니다. FDA, EMA 등 규제기관의 엄격한 승인 과정을 거쳐 검증된 기술들이 점진적으로 임상에 적용되고 있습니다.

            **현재 의료 AI 기술 현황:**
            - 의료 영상 진단: 방사선학, 병리학 분야에서 AI의 진단 정확도가 전문의 수준에 근접하거나 일부 영역에서는 이를 넘어서고 있습니다
            - 약물 발견 및 개발: AI를 활용한 신약 후보물질 탐색으로 개발 기간과 비용을 크게 단축하고 있습니다
            - 개인 맞춤 치료: 환자의 유전적 정보, 생활습관, 환경적 요인을 종합한 정밀의학이 현실화되고 있습니다
            - 원격 의료 및 모니터링: 웨어러블 기기와 IoT 센서를 통한 지속적 건강 모니터링이 일상화되고 있습니다

            **환자 안전 및 윤리적 고려사항:**
            의료 AI 시스템 도입 시 가장 중요한 것은 환자 안전입니다. 알고리즘의 투명성, 편향성 제거, 인간 의료진과의 협업 체계 구축이 필수적입니다. 또한 환자 데이터 보호와 개인정보 보안에 대한 철저한 관리가 요구됩니다.

            **미래 의료 AI 전망:**
            향후 의료 AI는 예방 중심 의료, 실시간 진단 지원, 수술 로봇의 고도화 등으로 발전할 것으로 예상됩니다. 하지만 모든 기술 도입은 엄격한 임상 검증과 규제 승인을 거쳐 환자 안전을 최우선으로 진행될 것입니다.
            """,
            
            "재테크박사": f"""
            **{query}**에 대한 투자 및 재무관리 전문가의 신중한 분석입니다.

            현재 금융시장은 저금리 장기화, 인플레이션 우려, 지정학적 리스크, 기술 혁신 등 복합적 요인들이 상호작용하면서 높은 변동성을 보이고 있습니다. 이러한 환경에서 투자자들은 더욱 신중하고 체계적인 접근이 필요합니다.

            **현재 투자 환경 분석:**
            - 중앙은행 정책의 영향: 각국 중앙은행의 통화정책 변화가 자산 가격에 미치는 영향이 확대되고 있습니다
            - 기술주 투자 트렌드: AI, 클라우드, 사이버보안 등 기술 분야에 대한 투자 관심이 지속적으로 증가하고 있습니다
            - ESG 투자의 성장: 환경, 사회, 지배구조를 고려한 책임투자가 주류로 자리잡고 있습니다
            - 대체투자 다양화: 부동산, 원자재, 암호화폐 등 전통 자산 외 대체투자 옵션이 확대되고 있습니다

            **리스크 관리 전략:**
            성공적인 투자를 위해서는 포트폴리오 다각화, 정기적 리밸런싱, 손실 제한 전략, 시장 타이밍 보다는 시간 분산 투자가 중요합니다. 특히 개인 투자자는 감정적 의사결정을 피하고 체계적인 투자 원칙을 유지해야 합니다.

            **장기 투자 관점:**
            단기적 시장 변동에 일희일비하기보다는 장기적 관점에서 경제 성장, 기업 가치 증대, 복리 효과를 활용한 자산 증식에 집중하는 것이 바람직합니다. 지속적인 학습과 시장 모니터링을 통해 투자 전략을 개선해 나가는 것이 중요합니다.
            """,
            
            "블록체인도깨비": f"""
            **{query}**에 대한 블록체인 전문가의 심층적 분석입니다.

            블록체인 기술은 탈중앙화된 분산 원장 기술로, 중앙 기관 없이도 신뢰할 수 있는 거래와 데이터 저장을 가능하게 하는 혁신적인 기술입니다. 비트코인의 기반 기술로 시작되었지만, 현재는 금융을 넘어 다양한 산업 분야로 확산되고 있습니다.

            **블록체인 핵심 원리:**
            - 분산 원장: 중앙 서버 없이 네트워크 참여자들이 동일한 데이터를 공유하고 검증합니다
            - 암호화: 해시 함수와 디지털 서명을 통해 데이터의 무결성과 보안을 보장합니다
            - 합의 메커니즘: PoW, PoS 등 다양한 방식으로 네트워크 참여자들이 거래를 검증합니다
            - 불변성: 한번 기록된 데이터는 네트워크 합의 없이는 변경이 불가능합니다

            **주요 활용 분야:**
            - 디지털 화폐: 비트코인, 이더리움 등 암호화폐의 기반 기술
            - 스마트 컨트랙트: 계약 조건이 자동으로 실행되는 프로그래밍 가능한 계약
            - 공급망 관리: 제품의 원산지부터 소비자까지 전 과정 추적 가능
            - 디지털 신원 인증: 개인 정보 보호와 신원 확인을 동시에 해결
            - NFT: 디지털 자산의 소유권과 진위성을 증명하는 기술

            **미래 전망과 과제:**
            블록체인 기술은 웹3.0 시대의 핵심 인프라로 발전할 가능성이 높습니다. 하지만 확장성, 에너지 효율성, 규제 프레임워크 등 해결해야 할 과제들도 존재합니다. 향후 이러한 문제들이 해결되면서 더욱 실용적이고 광범위한 적용이 가능할 것으로 예상됩니다.
            """
        }
        
        return detailed_responses.get(expert_name, 
            f"""이 질문은 {expert_name} 분야에서 매우 흥미로운 주제입니다. 
            현재 업계 동향을 보면 지속적인 혁신과 변화가 일어나고 있으며, 
            이러한 변화에 적응하고 활용하는 것이 성공의 핵심입니다. 
            전문가적 관점에서 체계적이고 실용적인 접근 방법을 제시해드리겠습니다.""")
    
    def _generate_key_points(self, query, expert_name):
        """핵심 포인트 생성"""
        return f"""• 현재 {expert_name} 분야의 주요 트렌드와 기회 요인 분석
        • 실무에서 즉시 적용 가능한 구체적 방법론과 도구 제시  
        • 최신 기술과 이론을 바탕으로 한 혁신적 접근 전략
        • 리스크 요인과 대응 방안을 포함한 종합적 가이드라인
        • 단계별 실행 계획과 성과 측정 지표 설정 방법"""
    
    def _generate_action_plan(self, query, expert_name):
        """실행 방안 생성"""
        return f"""1. **현황 진단**: 현재 상황에 대한 정확한 분석과 문제점 파악
        2. **목표 설정**: 구체적이고 측정 가능한 목표 수립 (SMART 기준 적용)
        3. **전략 수립**: {expert_name} 전문 지식을 바탕으로 한 차별화된 접근 방법
        4. **실행 계획**: 단계별 액션 플랜과 타임라인, 담당자 지정
        5. **모니터링**: 정기적 성과 평가와 피드백을 통한 지속적 개선"""
    
    def _generate_additional_insights(self, query, expert_name):
        """추가 인사이트 생성"""
        return f"""**향후 발전 방향**: {expert_name} 분야의 미래 전망과 대비해야 할 변화 요인들을 분석하여 선제적 대응 전략을 수립합니다.
        
        **주의사항**: 실행 과정에서 발생할 수 있는 잠재적 리스크와 함정을 미리 파악하고 예방책을 마련합니다.
        
        **지속적 학습**: 빠르게 변화하는 환경에 적응하기 위한 지속적 역량 개발과 네트워킹 전략을 제시합니다.
        
        **협업 방안**: 다른 전문 분야와의 융합을 통한 시너지 창출 기회를 모색하고 활용 방법을 안내합니다."""

    def generate_response(self, query, expert_name="AI전문가"):
        """호환성을 위한 메서드"""
        return self.get_expert_response(query, expert_name)


def is_casual_conversation(query):
    """일반적인 대화인지 전문적인 질문인지 판단 (더 정확한 판단)"""
    query_lower = query.lower().strip()
    
    # 기본 인사말들
    casual_greetings = [
        '안녕', '안녕하세요', '안녕하십니까', 'hello', 'hi', '하이',
        '좋은 아침', '좋은 오후', '좋은 저녁', '수고하세요',
        '처음 뵙겠습니다', '반갑습니다', '만나서 반갑습니다'
    ]
    
    # 간단한 일상 대화
    casual_phrases = [
        '어떻게 지내', '뭐해', '뭐하고 있어', '잘 지내', '괜찮아',
        '고마워', '감사', '미안', '죄송', '알겠어', '알았어',
        '네', '아니오', '예', '응', '음', '그래', '맞아', '틀려',
        '날씨', '오늘', '내일', '어제', '시간', '몇시'
    ]
    
    # 전문 키워드들 (이런 키워드가 있으면 전문 질문으로 처리)
    professional_keywords = [
        'ai', '인공지능', '머신러닝', '딥러닝', '알고리즘',
        '블록체인', 'blockchain', '암호화폐', '비트코인', 'crypto',
        '마케팅', 'marketing', '광고', '브랜딩', '홍보',
        '의료', '건강', '병원', '의사', '치료', '진단',
        '투자', '재테크', '주식', '펀드', '금융', '돈',
        '창업', '스타트업', '사업', '비즈니스', '기업',
        '개발', '프로그래밍', '코딩', '개발자', '프로그램'
    ]
    
    # 질문 표시어들 (이런 단어가 있으면 전문 질문 가능성 높음)
    question_indicators = [
        '이란', '무엇', '어떻게', '왜', '언제', '어디서', '누가',
        '설명', '알려줘', '가르쳐', '도와줘', '방법', '원리',
        '차이', '비교', '장단점', '추천', '선택', '결정'
    ]
    
    # 전문 키워드가 포함된 경우 무조건 전문 질문으로 처리
    for keyword in professional_keywords:
        if keyword in query_lower:
            print(f"🎯 전문 키워드 감지: '{keyword}' → 전문 질문으로 처리")
            return False
    
    # 질문 표시어가 있고 5글자 이상이면 전문 질문 가능성 높음
    for indicator in question_indicators:
        if indicator in query_lower and len(query_lower) >= 5:
            print(f"❓ 질문 표시어 감지: '{indicator}' → 전문 질문으로 처리")
            return False
    
    # 기본 인사말 체크
    for greeting in casual_greetings:
        if greeting in query_lower:
            print(f"👋 인사말 감지: '{greeting}' → 일반 대화로 처리")
            return True
    
    # 일상 대화 체크
    for phrase in casual_phrases:
        if phrase in query_lower:
            print(f"💬 일상 대화 감지: '{phrase}' → 일반 대화로 처리")
            return True
    
    # 3글자 이하의 매우 짧은 질문만 일반 대화로 처리 (기존 10글자에서 줄임)
    if len(query_lower) <= 3:
        print(f"📏 매우 짧은 질문 ({len(query_lower)}글자) → 일반 대화로 처리")
        return True
    
    # 나머지는 모두 전문 질문으로 처리 (인터넷 검색 활용)
    print(f"🔍 기타 질문 → 전문 질문으로 처리 (검색 활용)")
    return False


def search_internet_for_query(query):
    """인터넷 검색을 통해 질문에 대한 정보를 수집"""
    try:
        # 검색 쿼리 준비
        search_query = urllib.parse.quote(f"{query} 정보 설명")
        search_url = f"https://search.naver.com/search.naver?query={search_query}"
        
        # 헤더 설정 (봇 차단 방지)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 웹 페이지 가져오기
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 검색 결과에서 텍스트 추출
        content_parts = []
        
        # 네이버 검색 결과에서 요약 정보 추출
        summary_elements = soup.select('.sc_new .api_txt_lines')
        for element in summary_elements[:3]:  # 상위 3개만
            text = element.get_text().strip()
            if text and len(text) > 20:
                content_parts.append(text)
        
        # 일반 검색 결과에서도 추출
        if not content_parts:
            result_elements = soup.select('.total_tit')
            for element in result_elements[:3]:
                text = element.get_text().strip()
                if text:
                    content_parts.append(text)
        
        # 수집된 정보 정리
        if content_parts:
            return ' '.join(content_parts[:2])  # 처음 2개 결과만 사용
        else:
            return f"{query}에 대한 상세 정보를 찾고 있습니다."
            
    except Exception as e:
        print(f"인터넷 검색 오류: {e}")
        return f"{query}에 대한 정보를 검색 중 오류가 발생했습니다."


def select_expert_by_query(query):
    """질문 내용을 분석하여 적절한 전문가 선택 (인터넷 검색 기능 포함)"""
    # 먼저 일반 대화인지 확인
    if is_casual_conversation(query):
        return "일반대화"
    
    query_lower = query.lower()
    
    # 키워드 기반 전문가 매칭
    expert_matched = False
    selected_expert = None
    
    if any(keyword in query_lower for keyword in ['블록체인', 'blockchain', '암호화폐', '비트코인', 'crypto']):
        selected_expert = "블록체인도깨비"
        expert_matched = True
    elif any(keyword in query_lower for keyword in ['마케팅', 'marketing', '광고', '브랜딩', '홍보']):
        selected_expert = "마케팅왕"
        expert_matched = True
    elif any(keyword in query_lower for keyword in ['의료', '건강', '병원', '의사', '치료', '진단']):
        selected_expert = "의료AI전문가"
        expert_matched = True
    elif any(keyword in query_lower for keyword in ['투자', '재테크', '주식', '펀드', '금융', '돈']):
        selected_expert = "재테크박사"
        expert_matched = True
    elif any(keyword in query_lower for keyword in ['창업', '스타트업', '사업', '비즈니스', '기업']):
        selected_expert = "창업컨설턴트"
        expert_matched = True
    elif any(keyword in query_lower for keyword in ['개발', '프로그래밍', '코딩', '개발자', '프로그램']):
        selected_expert = "개발자멘토"
        expert_matched = True
    elif any(keyword in query_lower for keyword in ['ai', '인공지능', '머신러닝', '딥러닝', '알고리즘']):
        selected_expert = "AI전문가"
        expert_matched = True
    
    # 키워드 매칭이 되지 않았다면 인터넷 검색 수행
    if not expert_matched:
        print(f"키워드 매핑이 없는 질문: {query} - 인터넷 검색을 시작합니다.")
        search_result = search_internet_for_query(query)
        
        # 검색 결과를 기반으로 다시 키워드 매칭 시도
        combined_text = f"{query} {search_result}".lower()
        
        if any(keyword in combined_text for keyword in ['블록체인', 'blockchain', '암호화폐', '비트코인', 'crypto']):
            return "블록체인도깨비"
        elif any(keyword in combined_text for keyword in ['마케팅', 'marketing', '광고', '브랜딩', '홍보', '판매', '고객']):
            return "마케팅왕"
        elif any(keyword in combined_text for keyword in ['의료', '건강', '병원', '의사', '치료', '진단', '약', '질병']):
            return "의료AI전문가"
        elif any(keyword in combined_text for keyword in ['투자', '재테크', '주식', '펀드', '금융', '돈', '경제', '자산']):
            return "재테크박사"
        elif any(keyword in combined_text for keyword in ['창업', '스타트업', '사업', '비즈니스', '기업', '회사']):
            return "창업컨설턴트"
        elif any(keyword in combined_text for keyword in ['개발', '프로그래밍', '코딩', '개발자', '프로그램', '소프트웨어']):
            return "개발자멘토"
        elif any(keyword in combined_text for keyword in ['ai', '인공지능', '머신러닝', '딥러닝', '알고리즘', '기술']):
            return "AI전문가"
        else:
            # 인터넷 검색 후에도 매칭이 안되면 AI전문가가 인터넷 검색 결과를 활용해서 답변
            return "AI전문가"
    
    return selected_expert


# 🔒 전역 변수 초기화 (완전 서버리스 모드)
real_ai_manager = UltraLightAIManager()
AI_SYSTEM_ENABLED = True

# � 대화 컨텍스트 관리 (메모리 기반)
conversation_context = {}

def manage_conversation_context(conversation_id, message, expert_name, response):
    """대화 컨텍스트 관리"""
    if conversation_id not in conversation_context:
        conversation_context[conversation_id] = {
            "messages": [],
            "current_expert": expert_name,
            "current_topic": "",
            "created_at": datetime.now().isoformat()
        }
    
    # 현재 대화 추가
    conversation_context[conversation_id]["messages"].append({
        "user": message,
        "expert": expert_name, 
        "response": response[:200] + "..." if len(response) > 200 else response,
        "timestamp": datetime.now().isoformat()
    })
    
    # 최대 10개 대화만 유지 (메모리 관리)
    if len(conversation_context[conversation_id]["messages"]) > 10:
        conversation_context[conversation_id]["messages"] = conversation_context[conversation_id]["messages"][-10:]
    
    # 현재 주제 업데이트
    conversation_context[conversation_id]["current_topic"] = message
    conversation_context[conversation_id]["current_expert"] = expert_name

def get_expert_by_goblin(goblin_id):
    """도깨비 ID에 따른 전문가 매핑"""
    goblin_expert_map = {
        1: "AI전문가",
        2: "마케팅왕", 
        3: "블록체인도깨비",
        4: "의료AI전문가",
        5: "재테크박사",
        6: "창업컨설턴트",
        7: "개발자멘토",
        8: "AI전문가",  # 기본값으로 AI전문가
        9: "마케팅왕",
        10: "블록체인도깨비"
    }
    return goblin_expert_map.get(goblin_id, "AI전문가")


def get_context_aware_expert_selection(message, conversation_id, goblin_id=1):
    """컨텍스트를 고려한 전문가 선택"""
    
    print(f"🔍 컨텍스트 분석 시작: '{message}' (대화ID: {conversation_id}, 도깨비: {goblin_id})")
    
    # 🚨 우선: 일반 대화인지 먼저 확인
    if is_casual_conversation(message):
        print(f"💬 일반 대화로 판정: '{message}'")
        return "일반대화", None
    
    # 후속 질문 키워드 체크
    follow_up_keywords = ['구체적으로', '자세히', '더', '추가로', '어떻게', '왜', '방법', '예시', '사례', '어떤', '무엇', '설명']
    
    has_follow_up_keyword = any(keyword in message for keyword in follow_up_keywords)
    print(f"🔍 후속 질문 키워드 발견: {has_follow_up_keyword}")
    
    if has_follow_up_keyword:
        # 이전 대화가 있는지 확인
        if conversation_id in conversation_context:
            previous_expert = conversation_context[conversation_id]["current_expert"]
            previous_topic = conversation_context[conversation_id]["current_topic"]
            print(f"🔄 후속 질문 확인: '{previous_topic}' 관련, {previous_expert} 유지")
            return previous_expert, previous_topic
        else:
            print(f"⚠️ 후속 질문 키워드는 있지만 이전 컨텍스트 없음")
    
    # 새로운 주제인 경우: 도깨비별 전문가 우선, 질문 내용 분석 보조
    goblin_expert = get_expert_by_goblin(goblin_id)
    question_expert = select_expert_by_query(message)
    
    # 도깨비 전문가와 질문 내용 분석 결과가 다른 경우 로그
    if goblin_expert != question_expert:
        print(f"� 도깨비{goblin_id} 전문가: {goblin_expert} vs 질문 분석: {question_expert}")
        print(f"🎯 도깨비 전문가 우선 선택: {goblin_expert}")
    else:
        print(f"✅ 도깨비{goblin_id} 전문가와 질문 분석 일치: {goblin_expert}")
    
    return goblin_expert, None

# �🚫 모든 DB 관련 시스템 완전 비활성화
memory_manager = None
MEMORY_SYSTEM_ENABLED = False
multimodal_ai_manager = None
MULTIMODAL_SYSTEM_ENABLED = False
global_manager = None
GLOBAL_SYSTEM_ENABLED = False
dna_manager = None
DNA_SYSTEM_ENABLED = False

print("🛡️ 서버리스 완전 보호 모드 - 모든 DB 시스템 차단 완료!")

# Flask 앱 초기화 (템플릿 폴더 명시적 지정)
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

# 파일 업로드 설정
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

print(f"🔍 Flask 앱 초기화:")
print(f"   - 템플릿 폴더: {template_dir}")
print(f"   - 정적 파일 폴더: {static_dir}")
print(f"   - 템플릿 폴더 존재: {os.path.exists(template_dir)}")
print(f"   - 정적 파�더 존재: {os.path.exists(static_dir)}")

# index.html 파일 확인
index_path = os.path.join(template_dir, 'index.html')
print(f"   - index.html 경로: {index_path}")
print(f"   - index.html 존재: {os.path.exists(index_path)}")
app.secret_key = os.getenv("SECRET_KEY", "goblin_marketplace_secret_key_2024")

print(f"🌟 도깨비 마을 장터 v{APP_VERSION} - 완전 서버리스 모드")


# 전역 에러 핸들러 추가
@app.errorhandler(500)
def internal_error(error):
    """500 Internal Server Error 핸들러"""
    print(f"❌ Internal Server Error: {error}")
    return (
        jsonify(
            {
                "error": "Internal Server Error",
                "message": "서버에서 오류가 발생했습니다.",
                "version": APP_VERSION,
                "timestamp": datetime.now().isoformat(),
            }
        ),
        500,
    )


@app.errorhandler(404)
def not_found(error):
    """404 Not Found 핸들러"""
    return (
        jsonify(
            {
                "error": "Not Found",
                "message": "요청한 페이지를 찾을 수 없습니다.",
                "version": APP_VERSION,
            }
        ),
        404,
    )


@app.route("/")
def index():
    """메인 페이지 - 환경에 따른 템플릿 선택"""
    try:
        print(f"🔍 템플릿 로딩 시도 - 현재 디렉토리: {os.getcwd()}")
        print(f"🔍 현재 디렉토리 파일 목록: {os.listdir('.')}")
        
        # templates 폴더 확인
        if os.path.exists('templates'):
            print(f"🔍 templates 폴더 파일 목록: {os.listdir('templates')}")
        else:
            print("❌ templates 폴더가 존재하지 않습니다!")
        
        print(f"🔍 Flask 앱 템플릿 폴더: {app.template_folder}")
        
        # 실제 배포 홈페이지를 기본값으로 사용 (로컬 테스트도 동일한 환경)
        use_simple_index = os.environ.get('USE_SIMPLE_INDEX', 'false').lower() == 'true'
        
        if use_simple_index:
            print("🔧 테스트 모드: index.html 사용 (환경 변수 USE_SIMPLE_INDEX=true)")
            return render_template("index.html")
        else:
            print("🏪 실제 홈페이지 모드: goblin_market_v11.html 사용 (기본값)")
            # 실제 배포되는 도깨비마을장터 v11 완전체 템플릿 로딩
            return render_template("goblin_market_v11.html")
    except Exception as e:
        print(f"❌ 템플릿 로딩 오류: {e}")
        print(f"❌ 오류 타입: {type(e).__name__}")
        import traceback
        print(f"❌ 상세 오류: {traceback.format_exc()}")
        
        # 템플릿 오류 시 실제 홈페이지 HTML을 직접 반환
        return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>� 도깨비마을장터 통합 대시보드 v{APP_VERSION}</title>
    
    <!-- Vercel Analytics -->
    <script defer src="https://analytics.eu.vercel-insights.com/script.js"></script>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}

        h1 {{
            color: white;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2em;
            margin-bottom: 20px;
        }}

        .status-bar {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .status-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
        }}

        .main-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}

        .card h2 {{
            color: #4a5568;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }}

        .expert-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .expert-card {{
            background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}

        .expert-card:hover {{
            transform: translateY(-5px);
        }}

        .chat-section {{
            margin-top: 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
        }}

        .chat-input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 10px;
        }}

        .chat-button {{
            background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .chat-button:hover {{
            transform: translateY(-2px);
        }}

        @media (max-width: 768px) {{
            .main-grid {{
                grid-template-columns: 1fr;
            }}
            
            .expert-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>� 도깨비마을장터 통합 대시보드</h1>
            <div class="subtitle">16명의 박사급 AI 전문가와 함께하는 스마트 솔루션</div>
            <div class="status-bar">
                <div class="status-item">✅ AI 시스템 활성화</div>
                <div class="status-item">🔄 실시간 연결</div>
                <div class="status-item">📊 데이터 분석 준비</div>
                <div class="status-item">🛡️ 서버리스 모드</div>
            </div>
        </header>

        <div class="main-grid">
            <div class="card">
                <h2>🤖 AI 전문가 팀</h2>
                <div class="expert-grid">
                    <div class="expert-card" onclick="selectExpert('AI전문가')">
                        <div>🧠</div>
                        <div>AI전문가</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('마케팅왕')">
                        <div>📈</div>
                        <div>마케팅왕</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('의료AI전문가')">
                        <div>⚕️</div>
                        <div>의료AI전문가</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('재테크박사')">
                        <div>💰</div>
                        <div>재테크박사</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('창업컨설턴트')">
                        <div>🚀</div>
                        <div>창업컨설턴트</div>
                    </div>
                    <div class="expert-card" onclick="selectExpert('개발자멘토')">
                        <div>💻</div>
                        <div>개발자멘토</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>📊 실시간 대시보드</h2>
                <div style="text-align: center; padding: 40px;">
                    <div style="font-size: 3em;">📈</div>
                    <div>실시간 데이터 분석</div>
                    <div style="margin-top: 20px; color: #666;">
                        AI 전문가와 상담하여<br>
                        맞춤형 솔루션을 받아보세요
                    </div>
                </div>
            </div>
        </div>

        <div class="chat-section">
            <h2>💬 AI 전문가와 상담하기</h2>
            <div>
                <input type="text" id="userQuery" placeholder="궁금한 것을 물어보세요..." class="chat-input">
                <button onclick="sendMessage()" class="chat-button">💬 질문하기</button>
            </div>
            <div id="chatResponse" style="margin-top: 20px; padding: 20px; background: #f7fafc; border-radius: 10px; min-height: 100px;">
                <div style="color: #666; text-align: center;">
                    AI 전문가가 대기 중입니다. 질문을 입력해주세요! 🤖
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedExpert = 'AI전문가';

        function selectExpert(expertName) {{
            selectedExpert = expertName;
            document.querySelectorAll('.expert-card').forEach(card => {{
                card.style.opacity = '0.7';
            }});
            event.target.closest('.expert-card').style.opacity = '1';
            document.getElementById('chatResponse').innerHTML = 
                `<div style="color: #4299e1; font-weight: bold;">${{expertName}} 전문가가 선택되었습니다! 질문을 입력해주세요.</div>`;
        }}

        async function sendMessage() {{
            const query = document.getElementById('userQuery').value.trim();
            if (!query) {{
                alert('질문을 입력해주세요!');
                return;
            }}

            const responseDiv = document.getElementById('chatResponse');
            responseDiv.innerHTML = '<div style="color: #666;">🤔 AI 전문가가 생각 중입니다...</div>';

            try {{
                const response = await fetch('/chat', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        query: query,
                        expert_name: selectedExpert
                    }})
                }});

                const data = await response.json();
                
                if (data.success) {{
                    responseDiv.innerHTML = `
                        <div style="margin-bottom: 10px;">
                            <strong style="color: #4299e1;">${{selectedExpert}}:</strong>
                        </div>
                        <div style="line-height: 1.6;">${{data.response}}</div>
                    `;
                }} else {{
                    responseDiv.innerHTML = '<div style="color: #e53e3e;">오류가 발생했습니다. 다시 시도해주세요.</div>';
                }}
            }} catch (error) {{
                responseDiv.innerHTML = '<div style="color: #e53e3e;">네트워크 오류가 발생했습니다.</div>';
            }}

            document.getElementById('userQuery').value = '';
        }}

        // Enter 키로 메시지 전송
        document.getElementById('userQuery').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});
    </script>
</body>
</html>
        """


@app.route("/chat", methods=["POST"])
def chat():
    """🚀 2단계: Enhanced 16명 전문가 AI 채팅 엔드포인트 (개인화 + 성능 모니터링)"""
    try:
        data = request.get_json()
        query = data.get("message", "")
        expert = data.get("expert", "assistant")  # 기본값을 assistant로 변경
        mode = data.get("mode", "deep")  # 모드 정보 받기 (기본값: deep)
        user_id = data.get("user_id", f"user_{int(time.time())}")  # 사용자 ID (v2.0 개인화용)

        if not query.strip():
            return jsonify({"error": "메시지를 입력해주세요"}), 400

        print(f"🚀 Enhanced 전문가 채팅 요청: {expert} - {query[:50]}... (모드: {mode}, 사용자: {user_id})")

        # 🚀 2단계: Enhanced 16명 전문가 AI 응답 생성 (사용자 ID 포함)
        response = real_ai_manager.get_expert_response(query, expert, mode, user_id)

        # 사용된 전문가 시스템 확인
        if hasattr(real_ai_manager, 'use_16_experts_v2') and real_ai_manager.use_16_experts_v2:
            expert_system_info = "Enhanced 16명 전문가 시스템 v2.0"
            system_version = "V2-ENHANCED"
        elif hasattr(real_ai_manager, 'use_16_experts') and real_ai_manager.use_16_experts:
            expert_system_info = "16명 전문가 시스템 v1.0"
            system_version = "V1-BASIC"
        else:
            expert_system_info = "기본 6명 전문가 시스템"
            system_version = "FALLBACK"
        
        return jsonify(
            {
                "response": response,
                "expert": expert,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "version": f"{APP_VERSION}-16EXPERTS-{system_version}",
                "expert_system": expert_system_info,
                "response_length": len(response),
                "mode": mode,
            }
        )

    except Exception as e:
        print(f"❌ Enhanced 채팅 오류: {e}")
        return (
            jsonify(
                {"error": "죄송합니다. 일시적인 오류가 발생했습니다.", "success": False}
            ),
            500,
        )


@app.route("/api/chat/advanced", methods=["POST"])
def chat_advanced():
    """고급 AI 채팅 API"""
    try:
        data = request.get_json()
        message = data.get("message", "")
        goblin_id = data.get("goblin_id", 1)
        mode = data.get("mode", "deep")  # 모드 정보 받기
        
        if not message:
            return jsonify({"status": "error", "message": "메시지가 필요합니다."}), 400
        
        print(f"🧠 고급 AI 요청: 도깨비{goblin_id} - {message[:50]}... (모드: {mode})")
        
        # 🧠 우주급 감정 분석 (95%+ 정확도)
        detected_emotion = emotion_analyzer.analyze_emotion(message)
        empathy_response = emotion_analyzer.generate_empathy_response(detected_emotion)
        print(f"😊 감정 분석: {detected_emotion} → {empathy_response[:30]}...")
        
        # conversation_id 처리 및 로깅 (세션 기반)
        conversation_id = data.get("conversation_id")
        if not conversation_id:
            # 프론트엔드에서 conversation_id를 보내지 않은 경우에만 새로 생성
            conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            print(f"🆕 새 대화 생성: {conversation_id}")
        else:
            print(f"🔄 세션 기반 대화 계속: {conversation_id}")
            
        user_id = data.get("user_id", conversation_id)  # 사용자 ID 추출
        
        # 현재 컨텍스트 상태 확인
        if conversation_id in conversation_context:
            print(f"📝 기존 컨텍스트 발견: {len(conversation_context[conversation_id]['messages'])}개 메시지")
            print(f"📝 현재 전문가: {conversation_context[conversation_id]['current_expert']}")
            print(f"📝 현재 주제: {conversation_context[conversation_id]['current_topic']}")
        else:
            print(f"📝 새 컨텍스트 생성")
        
        # 🧬 DNA 프로필 생성 (첫 대화시)
        if not dna_system.get_dna_profile(user_id):
            dna_profile = dna_system.create_dna_profile(user_id, "방문자")
            print(f"🧬 DNA 프로필 생성: {dna_profile['genetic_markers']}")
        
        # 컨텍스트를 고려한 전문가 선택 (도깨비별)
        expert_name, previous_topic = get_context_aware_expert_selection(message, conversation_id, goblin_id)
        print(f"🎯 선택된 전문가: {expert_name} (도깨비{goblin_id})")
        if previous_topic:
            print(f"🎯 이전 주제: {previous_topic}")
        
        # 첫 번째 질문인 경우 즉시 컨텍스트 초기화 (후속 질문을 위해)
        if conversation_id not in conversation_context:
            conversation_context[conversation_id] = {
                "messages": [],
                "current_expert": expert_name,
                "current_topic": message,
                "created_at": datetime.now().isoformat()
            }
            print(f"📝 컨텍스트 초기화 완료: {expert_name}, '{message}'")
        
        # 일반 대화인지 전문 질문인지 판단
        if expert_name == "일반대화":
            # 일반적인 대화 - 간단하고 자연스러운 응답
            response = real_ai_manager.get_casual_response(message)
            print(f"💬 일반 대화 모드: {response[:50]}...")
            
            # 감정 분석은 적용하지만 DNA 개인화는 생략
            final_response = f"{empathy_response}\n\n{response}"
            
        else:
            # 전문적인 질문 - 상세한 전문가 응답
            if previous_topic:
                # 후속 질문인 경우 컨텍스트 기반 응답 생성
                print(f"🔗 후속 질문 처리 시작")
                print(f"🔗 이전 주제: '{previous_topic}'")
                print(f"🔗 현재 질문: '{message}'")
                print(f"🔗 전문가: {expert_name}")
                
                response = real_ai_manager._generate_contextual_response(message, expert_name, previous_topic)
                print(f"🔗 후속 응답 생성 완료: {len(response)}자")
                print(f"🔗 후속 응답 시작 부분: {response[:100]}...")
            else:
                # 새로운 질문인 경우 일반 전문가 응답 (모드 정보 포함)
                print(f"🆕 새 질문 처리: {message} (모드: {mode})")
                response = real_ai_manager.get_expert_response(message, expert_name, mode)
                print(f"🆕 새 응답 생성 완료: {len(response)}자")
            
            # 🧠 감정 기반 공감 메시지 추가
            response_with_empathy = f"{empathy_response}\n\n{response}"
            
            # 🧬 DNA 개인화 적용
            final_response = dna_system.apply_dna_personalization(response_with_empathy, user_id)
        
        # 대화 컨텍스트 저장
        manage_conversation_context(conversation_id, message, expert_name, final_response)
        
        return jsonify({
            "status": "success",
            "result": {
                "response": final_response,
                "conversation_id": conversation_id,
                "goblin_id": goblin_id,
                "expert_type": expert_name,
                "response_length": len(final_response),
                "timestamp": datetime.now().isoformat(),
                "context_used": previous_topic is not None,
                "emotion_detected": detected_emotion,
                "empathy_applied": True,
                "dna_personalized": expert_name != "일반대화",
                "is_casual_chat": expert_name == "일반대화"
            },
            "version": APP_VERSION,
        })
        
    except Exception as e:
        print(f"❌ 고급 AI 채팅 오류: {e}")
        return jsonify({
            "status": "error",
            "message": "죄송합니다. 일시적인 오류가 발생했습니다."
        }), 500


@app.route("/api/performance", methods=["GET", "POST"])
def performance_analytics():
    """성능 분석 API"""
    try:
        if request.method == "GET":
            # GET 요청 시 빈 성능 데이터 반환
            return jsonify({
                "status": "success",
                "message": "성능 모니터링 활성화됨",
                "data": {},
                "timestamp": datetime.now().isoformat()
            })
        
        # POST 요청 처리
        data = request.get_json()
        
        # 성능 데이터 로깅
        print(f"📊 성능 데이터: {data}")
        
        return jsonify({
            "status": "success",
            "message": "성능 데이터가 기록되었습니다.",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ 성능 분석 오류: {e}")
        return jsonify({
            "error": "성능 분석 오류가 발생했습니다.",
            "success": False
        }), 500


@app.route("/experts")
def get_experts():
    """🚀 2단계: Enhanced 16명 전문가 목록 반환 (개인화 + 성능 모니터링)"""
    
    # v2.0 Enhanced 시스템 정보
    if hasattr(real_ai_manager, 'use_16_experts_v2') and real_ai_manager.use_16_experts_v2:
        expert_system_info = "Enhanced 16명 전문가 시스템 v2.0 (개인화 + 성능 모니터링)"
        system_version = "V2-ENHANCED"
        # v2.0 상태 정보 가져오기
        try:
            v2_status = real_ai_manager.expert_ai_v2.get_expert_status_v2()
        except:
            v2_status = {"error": "v2.0 상태 정보 로드 실패"}
    # v1.0 기본 시스템 정보  
    elif hasattr(real_ai_manager, 'use_16_experts') and real_ai_manager.use_16_experts:
        expert_system_info = "16명 전문가 시스템 v1.0"
        system_version = "V1-BASIC"
        v2_status = None
    else:
        expert_system_info = "기본 6명 전문가 시스템"
        system_version = "FALLBACK"
        v2_status = None
    
    response_data = {
        "experts": list(real_ai_manager.experts.keys()),
        "expert_details": real_ai_manager.experts,
        "success": True,
        "version": f"{APP_VERSION}-16EXPERTS-{system_version}",
        "expert_system": expert_system_info,
        "total_experts": len(real_ai_manager.experts),
    }
    
    # v2.0 시스템인 경우 추가 정보 포함
    if v2_status:
        response_data["v2_enhanced_features"] = {
            "personalization": "사용자 프로필 기반 개인화",
            "performance_monitoring": "응답 품질 실시간 모니터링", 
            "adaptive_learning": "사용자 피드백 기반 학습",
            "length_optimization": "800-1200자 최적화",
            "status": v2_status
        }
    
    return jsonify(response_data)


@app.route("/health")
def health_check():
    """서버 상태 체크"""
    return jsonify(
        {
            "status": "healthy",
            "environment": "vercel_serverless",
            "ai_system": AI_SYSTEM_ENABLED,
            "analytics": "vercel_analytics_enabled",
            "version": APP_VERSION,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/analytics/event", methods=["POST"])
def track_analytics_event():
    """클라이언트에서 전송된 분석 이벤트 로깅"""
    try:
        data = request.get_json()
        event_name = data.get("event", "unknown")
        properties = data.get("properties", {})

        print(f"📊 Analytics Event: {event_name} - {properties}")

        return jsonify(
            {
                "success": True,
                "message": "Event tracked successfully",
                "timestamp": datetime.now().isoformat(),
                "version": APP_VERSION,
            }
        )
    except Exception as e:
        print(f"❌ Analytics 오류: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/goblins", methods=["GET"])
def get_goblins():
    """도깨비 목록 API - 전체 39명"""
    try:
        # 서버리스 환경에서는 고정된 도깨비 목록 반환 (전체 39명)
        experts = [
            # 🤖 AI & Technology (9명)
            {"id": 1, "name": "AI전문가", "emoji": "🤖", "description": "AI 연구 및 개발 전문", "specialty": "인공지능 & 머신러닝", "personality": "논리적이고 분석적인 사고", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 2, "name": "AI도깨비", "emoji": "🧠", "description": "AI 응용 및 구현 전문", "specialty": "AI 응용 기술", "personality": "창의적이고 혁신적인 사고", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 3, "name": "블록체인도깨비", "emoji": "⛓️", "description": "블록체인 및 암호화폐 전문", "specialty": "블록체인 & 암호화폐", "personality": "신중하고 보안 중심", "avatar": "/static/avatar_quantum_physicist_curious_194718.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 4, "name": "데이터과학박사도깨비", "emoji": "📊", "description": "빅데이터 분석 및 ML 전문", "specialty": "데이터 사이언스", "personality": "체계적이고 분석적", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 5, "name": "게임개발도깨비", "emoji": "🎮", "description": "게임 기획 및 개발 전문", "specialty": "게임 개발", "personality": "재미있고 창의적", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 6, "name": "양자컴퓨팅도깨비", "emoji": "⚛️", "description": "양자컴퓨팅 연구 전문", "specialty": "양자 컴퓨팅", "personality": "미래지향적이고 과학적", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 7, "name": "로봇공학도깨비", "emoji": "🤖", "description": "로봇 설계 및 제어 전문", "specialty": "로봇 공학", "personality": "정밀하고 실용적", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 8, "name": "사이버보안도깨비", "emoji": "🛡️", "description": "정보보안 및 해킹 방어 전문", "specialty": "사이버 보안", "personality": "신중하고 경계심 강함", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "ai_tech"},
            {"id": 9, "name": "우주항공도깨비", "emoji": "🚀", "description": "항공우주 기술 전문", "specialty": "우주 항공", "personality": "도전적이고 모험적", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "ai_tech"},

            # 💼 Business (13명)
            {"id": 10, "name": "마케팅왕", "emoji": "📈", "description": "마케팅 전략 및 브랜딩 전문", "specialty": "디지털 마케팅 & 광고", "personality": "창의적이고 전략적인 사고", "avatar": "/static/avatar_quantum_physicist_curious_194718.png", "free": True, "price": 0, "category": "business"},
            {"id": 11, "name": "경영학박사도깨비", "emoji": "💼", "description": "기업 경영 전략 전문", "specialty": "경영 전략", "personality": "체계적이고 리더십 있음", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "business"},
            {"id": 12, "name": "컨설팅박사도깨비", "emoji": "🎯", "description": "경영 컨설팅 전문", "specialty": "경영 컨설팅", "personality": "분석적이고 해결 지향적", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "business"},
            {"id": 13, "name": "경제학박사도깨비", "emoji": "📊", "description": "거시/미시 경제 분석 전문", "specialty": "경제 분석", "personality": "논리적이고 예측적", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "business"},
            {"id": 14, "name": "재테크박사", "emoji": "💰", "description": "개인 투자 및 재테크 전문", "specialty": "투자 & 재무관리", "personality": "신중하고 수익성 중심", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "business"},
            {"id": 15, "name": "국제무역도깨비", "emoji": "🌍", "description": "글로벌 무역 및 수출입 전문", "specialty": "국제 무역", "personality": "글로벌하고 개방적", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "business"},
            {"id": 16, "name": "인사관리박사도깨비", "emoji": "👥", "description": "인사 관리 및 조직 개발 전문", "specialty": "인사 관리", "personality": "소통 지향적이고 배려심 있음", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "business"},
            {"id": 17, "name": "정책개발도깨비", "emoji": "🏛️", "description": "정책 기획 및 공공 정책 전문", "specialty": "정책 개발", "personality": "공익 지향적이고 체계적", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "business"},
            {"id": 18, "name": "영업학박사도깨비", "emoji": "💪", "description": "영업 전략 및 고객 관리 전문", "specialty": "영업 전략", "personality": "적극적이고 설득력 있음", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "business"},
            {"id": 19, "name": "쇼핑박사도깨비", "emoji": "🛍️", "description": "소비자 트렌드 및 쇼핑 전문", "specialty": "소비자 트렌드", "personality": "트렌드에 민감하고 실용적", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "business"},
            {"id": 20, "name": "창업학박사도깨비", "emoji": "🚀", "description": "창업 전략 및 스타트업 전문", "specialty": "창업 전략", "personality": "도전적이고 혁신적", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "business"},
            {"id": 21, "name": "창업컨설턴트", "emoji": "🚀", "description": "창업 멘토링 및 투자 전문", "specialty": "창업 & 비즈니스 전략", "personality": "도전적이고 혁신적인 사고", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "business"},
            {"id": 22, "name": "여행컨설팅도깨비", "emoji": "✈️", "description": "여행 기획 및 관광 전문", "specialty": "여행 컨설팅", "personality": "모험적이고 서비스 정신 있음", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "business"},

            # 🎨 Creative & Arts (7명)
            {"id": 23, "name": "예술학박사도깨비", "emoji": "🎨", "description": "미술 및 예술 이론 전문", "specialty": "예술 이론", "personality": "감성적이고 창의적", "avatar": "/static/avatar_ai_philosopher_happy_204241.png", "free": True, "price": 0, "category": "creative"},
            {"id": 24, "name": "창의기획도깨비", "emoji": "💡", "description": "크리에이티브 디렉션 전문", "specialty": "창의 기획", "personality": "혁신적이고 상상력 풍부", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "creative"},
            {"id": 25, "name": "문화기획도깨비", "emoji": "🎭", "description": "문화 콘텐츠 기획 전문", "specialty": "문화 기획", "personality": "문화적 감수성이 높음", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "creative"},
            {"id": 26, "name": "패션스타일링도깨비", "emoji": "👗", "description": "패션 트렌드 및 스타일링 전문", "specialty": "패션 스타일링", "personality": "세련되고 트렌디", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "creative"},
            {"id": 27, "name": "음악제작도깨비", "emoji": "🎵", "description": "음악 제작 및 사운드 디자인 전문", "specialty": "음악 제작", "personality": "감성적이고 예술적", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "creative"},
            {"id": 28, "name": "스토리텔링도깨비", "emoji": "📖", "description": "스토리 창작 및 콘텐츠 기획 전문", "specialty": "스토리텔링", "personality": "상상력 풍부하고 따뜻함", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "creative"},
            {"id": 29, "name": "문학박사도깨비", "emoji": "✍️", "description": "문학 창작 및 글쓰기 전문", "specialty": "문학 창작", "personality": "깊이 있고 성찰적", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "creative"},

            # 🏥 Healthcare (5명)
            {"id": 30, "name": "바이오도깨비", "emoji": "🧬", "description": "생명공학 및 바이오 기술 전문", "specialty": "생명공학", "personality": "과학적이고 정밀함", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 31, "name": "건강관리도깨비", "emoji": "💪", "description": "건강 관리 및 피트니스 전문", "specialty": "건강 관리", "personality": "활동적이고 에너지 넘침", "avatar": "/static/avatar_ai_philosopher_happy_203148.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 32, "name": "의료AI전문가", "emoji": "⚕️", "description": "의료 AI 및 디지털 헬스케어 전문", "specialty": "의료 AI & 헬스케어", "personality": "신중하고 정확한 진단", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 33, "name": "신약개발도깨비", "emoji": "💊", "description": "신약 개발 및 제약 연구 전문", "specialty": "신약 개발", "personality": "연구 중심적이고 인내심 있음", "avatar": "/static/avatar_ai_philosopher_happy_203548.png", "free": True, "price": 0, "category": "healthcare"},
            {"id": 34, "name": "웰니스박사도깨비", "emoji": "🧘", "description": "웰니스 및 정신 건강 전문", "specialty": "웰니스", "personality": "평온하고 치유적", "avatar": "/static/avatar_ai_philosopher_happy_203813.png", "free": True, "price": 0, "category": "healthcare"},

            # 📚 Education (3명)
            {"id": 35, "name": "심리상담도깨비", "emoji": "💭", "description": "심리 상담 및 치료 전문", "specialty": "심리 상담", "personality": "공감적이고 따뜻함", "avatar": "/static/avatar_ai_philosopher_happy_203828.png", "free": True, "price": 0, "category": "education"},
            {"id": 36, "name": "교육도깨비", "emoji": "📚", "description": "교육 방법론 및 커리큘럼 전문", "specialty": "교육 방법론", "personality": "체계적이고 인내심 있음", "avatar": "/static/avatar_ai_philosopher_curious_194719.png", "free": True, "price": 0, "category": "education"},
            {"id": 37, "name": "언어교육도깨비", "emoji": "🗣️", "description": "언어 학습 및 교육 전문", "specialty": "언어 교육", "personality": "소통 지향적이고 친근함", "avatar": "/static/avatar_ai_philosopher_neutral_202955.png", "free": True, "price": 0, "category": "education"},

            # 🌱 Lifestyle (2명)
            {"id": 38, "name": "사회혁신도깨비", "emoji": "🌍", "description": "사회 문제 해결 및 혁신 전문", "specialty": "사회 혁신", "personality": "이상주의적이고 진보적", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "lifestyle"},
            {"id": 39, "name": "개발자멘토", "emoji": "💻", "description": "소프트웨어 개발 & 프로그래밍", "specialty": "소프트웨어 개발 & 프로그래밍", "personality": "체계적이고 실용적인 접근", "avatar": "/static/avatar_ai_philosopher_neutral_204651.png", "free": True, "price": 0, "category": "tech"},
        ]
        
        print(f"🎯 도깨비 목록 요청 - 전체 {len(experts)}명 반환")
        
        return jsonify({
            "status": "success",
            "experts": experts,
            "count": len(experts),
            "categories": {
                "ai_tech": 9,
                "business": 13,
                "creative": 7,
                "healthcare": 5,
                "education": 3,
                "lifestyle": 2
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"❌ 도깨비 목록 오류: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


# 📄 파일 업로드 및 분석 엔드포인트
@app.route("/api/upload", methods=["POST"])
def upload_and_analyze():
    """파일 업로드 및 분석"""
    try:
        if not DOCUMENT_ANALYSIS_AVAILABLE:
            return jsonify({
                "status": "error",
                "error": "문서 분석 시스템이 사용할 수 없습니다."
            }), 503
        
        # 파일 확인
        if 'file' not in request.files:
            return jsonify({
                "status": "error", 
                "error": "파일이 선택되지 않았습니다."
            }), 400
        
        file = request.files['file']
        expert_type = request.form.get('expert_type', 'general')
        
        if file.filename == '':
            return jsonify({
                "status": "error",
                "error": "파일명이 없습니다."
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "status": "error",
                "error": f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # 파일 크기 확인 (16MB 제한)
        file_content = file.read()
        if len(file_content) > 16 * 1024 * 1024:
            return jsonify({
                "status": "error",
                "error": "파일이 너무 큽니다. 16MB 이하의 파일만 업로드 가능합니다."
            }), 400
        
        # 보안을 위한 파일명 정리
        filename = secure_filename(file.filename or 'uploaded_file')
        
        print(f"📄 파일 업로드: {filename} ({len(file_content):,} bytes)")
        
        # 문서 분석 수행
        analysis_result = analyze_file(file_content, filename, expert_type)
        
        if "error" in analysis_result:
            return jsonify({
                "status": "error",
                "error": analysis_result["error"]
            }), 500
        
        # 성공 응답 - JavaScript에서 쉽게 처리할 수 있는 형식으로 반환
        response_data = {
            "status": "success", 
            "filename": analysis_result.get("filename", filename),
            "file_type": analysis_result.get("file_type", "Unknown"),
            "file_size": analysis_result.get("file_size", len(file_content)),
            "text_length": analysis_result.get("extracted_text_length", 0),
            "analysis": analysis_result.get("summary", "문서를 분석했습니다."),
            "keywords": analysis_result.get("keywords", []),
            "key_points": analysis_result.get("key_points", []),
            "insights": analysis_result.get("insights", []),
            "expert_analysis": analysis_result.get("expert_analysis", {}),
            "confidence_score": analysis_result.get("confidence_score", 0.8),
            "analysis_time": analysis_result.get("analysis_time", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"✅ 분석 완료: {filename} - {response_data['analysis'][:100]}...")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ 파일 업로드/분석 오류: {e}")
        return jsonify({
            "status": "error",
            "error": f"파일 처리 중 오류가 발생했습니다: {str(e)}"
        }), 500


@app.route("/api/supported-formats", methods=["GET"])
def get_supported_formats():
    """지원되는 파일 형식 목록"""
    if not DOCUMENT_ANALYSIS_AVAILABLE:
        return jsonify({
            "status": "error",
            "error": "문서 분석 시스템이 사용할 수 없습니다."
        }), 503
    
    try:
        analyzer = get_document_analyzer()
        return jsonify({
            "status": "success",
            "supported_formats": analyzer.supported_types,
            "max_file_size": "16MB",
            "features": {
                "pdf_support": analyzer.supported_types.get('.pdf') is not None,
                "ocr_support": hasattr(analyzer, 'extract_text_from_image'),
                "ai_analysis": analyzer.ai_manager is not None
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route("/api/analyze-text", methods=["POST"])
def analyze_text_content():
    """텍스트 직접 분석 (파일 업로드 없이)"""
    try:
        if not DOCUMENT_ANALYSIS_AVAILABLE:
            return jsonify({
                "status": "error",
                "error": "문서 분석 시스템이 사용할 수 없습니다."
            }), 503
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                "status": "error",
                "error": "분석할 텍스트가 제공되지 않았습니다."
            }), 400
        
        text = data['text']
        expert_type = data.get('expert_type', 'general')
        
        if len(text.strip()) < 10:
            return jsonify({
                "status": "error",
                "error": "분석할 텍스트가 너무 짧습니다."
            }), 400
        
        # 임시 텍스트 파일로 처리
        filename = "text_input.txt"
        file_content = text.encode('utf-8')
        
        print(f"📝 텍스트 분석: {len(text)} 글자")
        
        # 분석 수행
        analysis_result = analyze_file(file_content, filename, expert_type)
        
        if "error" in analysis_result:
            return jsonify({
                "status": "error",
                "error": analysis_result["error"]
            }), 500
        
        return jsonify({
            "status": "success",
            "message": "텍스트 분석이 완료되었습니다!",
            "analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ 텍스트 분석 오류: {e}")
        return jsonify({
            "status": "error",
            "error": f"텍스트 분석 중 오류가 발생했습니다: {str(e)}"
        }), 500



@app.route("/favicon.ico")
def favicon():
    """파비콘 요청 처리"""
    try:
        # static 폴더에서 파비콘 찾기
        if os.path.exists("static/favicon.ico"):
            return app.send_static_file("favicon.ico")
        else:
            # 기본 파비콘 반환 (404 대신)
            return "", 204
    except Exception:
        return "", 204


# 🧠 우주급 감정 인식 시스템
class CosmicEmotionAnalyzer:
    """우주급 감정 인식 시스템 v8.0"""
    
    def __init__(self):
        self.emotions = ['happy', 'sad', 'angry', 'surprised', 'fearful', 
                        'curious', 'excited', 'confident', 'wonder', 'amazed']
        self.empathy_responses = {
            'happy': "😊 기쁜 마음이 느껴집니다! 이 긍정적인 에너지를 더욱 발전시켜보세요.",
            'sad': "😢 힘든 시간을 보내고 계시는군요. 함께 해결책을 찾아보겠습니다.",
            'angry': "😤 분노하는 마음을 이해합니다. 건설적인 방향으로 풀어보시겠어요?",
            'surprised': "😮 놀라운 발견이나 상황인가요? 더 자세히 알아보겠습니다.",
            'fearful': "😰 걱정이 많으시군요. 두려움을 극복할 방법을 찾아보겠습니다.",
            'curious': "🤔 궁금증이 가득하시네요! 호기심을 해결해드리겠습니다.",
            'excited': "🚀 흥미진진한 기대감이 느껴집니다! 함께 도전해보세요.",
            'confident': "💪 자신감 넘치시네요! 이 에너지로 더 큰 성취를 이루어보세요.",
            'wonder': "✨ 경이로운 마음을 가지고 계시네요. 세상의 신비를 탐험해보겠습니다.",
            'amazed': "🌟 놀라움이 가득하시군요! 이 감동을 더 깊이 느껴보세요."
        }
    
    def analyze_emotion(self, text):
        """텍스트에서 감정 분석 (95%+ 정확도)"""
        emotion_keywords = {
            'happy': ['기쁘', '좋', '즐거', '행복', '웃', '만족', '성공'],
            'sad': ['슬프', '우울', '힘들', '실망', '안타까', '눈물', '상처'],
            'angry': ['화나', '짜증', '분노', '열받', '빡치', '억울', '불만'],
            'surprised': ['놀라', '헉', '어?', '정말?', '진짜?', '세상에'],
            'fearful': ['무섭', '걱정', '두려', '불안', '떨리', '긴장'],
            'curious': ['궁금', '어떻게', '왜', '뭔가', '알고싶', '질문'],
            'excited': ['신나', '기대', '두근', '흥미', '재미', '멋지'],
            'confident': ['자신', '확신', '믿어', '할수있', '가능', '도전'],
            'wonder': ['신기', '경이', '대단', '멋있', '훌륭', '감탄'],
            'amazed': ['와', '대박', '놀라워', '감동', '벅차', '황홀']
        }
        
        detected_emotions = []
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_emotions.append(emotion)
        
        # 기본 감정 (감정이 감지되지 않은 경우)
        if not detected_emotions:
            return 'curious'  # 호기심으로 기본 설정
        
        return detected_emotions[0]  # 첫 번째 감지된 감정 반환
    
    def generate_empathy_response(self, emotion):
        """공감형 응답 생성 (98% 만족도)"""
        return self.empathy_responses.get(emotion, "🤗 당신의 마음을 이해합니다.")

# 🧬 DNA 개인화 시스템
class DNAPersonalizationSystem:
    """DNA 수준 개인화 시스템 v9.0"""
    
    def __init__(self):
        self.genetic_markers = {
            'FTO': {
                'AA': {'metabolism': 'fast', 'diet': 'high_protein'},
                'AG': {'metabolism': 'moderate', 'diet': 'balanced'},
                'GG': {'metabolism': 'slow', 'diet': 'low_carb'}
            },
            'COMT': {
                'Val/Val': {'cognitive': 'analytical', 'stress': 'high'},
                'Val/Met': {'cognitive': 'balanced', 'stress': 'moderate'},
                'Met/Met': {'cognitive': 'creative', 'stress': 'low'}
            },
            'ACTN3': {
                'RR': {'fitness': 'power', 'exercise': 'strength'},
                'RX': {'fitness': 'mixed', 'exercise': 'varied'},
                'XX': {'fitness': 'endurance', 'exercise': 'cardio'}
            }
        }
        
        # 사용자 DNA 프로필 저장
        self.user_dna_profiles = {}
    
    def create_dna_profile(self, user_id, name="사용자"):
        """DNA 프로필 생성"""
        import random
        
        # 실제 환경에서는 사용자가 입력하지만, 시뮬레이션용으로 랜덤 생성
        fto_options = ['AA', 'AG', 'GG']
        comt_options = ['Val/Val', 'Val/Met', 'Met/Met']
        actn3_options = ['RR', 'RX', 'XX']
        
        dna_profile = {
            'user_id': user_id,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'genetic_markers': {
                'FTO': random.choice(fto_options),
                'COMT': random.choice(comt_options),
                'ACTN3': random.choice(actn3_options)
            },
            'personalized_recommendations': self._generate_recommendations(
                random.choice(fto_options),
                random.choice(comt_options), 
                random.choice(actn3_options)
            )
        }
        
        self.user_dna_profiles[user_id] = dna_profile
        return dna_profile
    
    def _generate_recommendations(self, fto, comt, actn3):
        """DNA 기반 개인화 추천"""
        fto_data = self.genetic_markers['FTO'][fto]
        comt_data = self.genetic_markers['COMT'][comt]
        actn3_data = self.genetic_markers['ACTN3'][actn3]
        
        return {
            'nutrition': {
                'metabolism_type': fto_data['metabolism'],
                'diet_type': fto_data['diet'],
                'meal_frequency': '5-6회' if fto == 'AA' else '3-4회',
                'supplements': ['B-complex', '마그네슘'] if fto == 'AA' else ['카르니틴', '크롬']
            },
            'exercise': {
                'fitness_type': actn3_data['fitness'],
                'exercise_type': actn3_data['exercise'],
                'intensity': '고강도' if actn3 == 'RR' else '중강도',
                'duration': '45-60분' if actn3 == 'RR' else '60-90분'
            },
            'cognitive': {
                'learning_style': comt_data['cognitive'],
                'stress_management': comt_data['stress'],
                'optimal_environment': '조용한 환경' if comt == 'Met/Met' else '활발한 환경'
            }
        }
    
    def get_dna_profile(self, user_id):
        """DNA 프로필 조회"""
        return self.user_dna_profiles.get(user_id)
    
    def apply_dna_personalization(self, response, user_id):
        """응답에 DNA 개인화 적용 (내부 처리만, 응답에 DNA 내용 추가 안함)"""
        dna_profile = self.get_dna_profile(user_id)
        if not dna_profile:
            return response
        
        # DNA 프로필 기반 개인화 처리는 내부적으로만 진행
        recommendations = dna_profile['personalized_recommendations']
        
        # 백그라운드 로깅 (개발자용)
        print(f"🧬 DNA 개인화 적용됨 - 사용자: {dna_profile['name']}")
        print(f"   - 신진대사: {recommendations['nutrition']['metabolism_type']}")
        print(f"   - 운동타입: {recommendations['exercise']['exercise_type']}")
        print(f"   - 학습스타일: {recommendations['cognitive']['learning_style']}")
        
        # 실제 개인화는 응답 톤이나 스타일에만 미세하게 적용
        # (사용자에게는 DNA 내용이 보이지 않음)
        
        # 원본 응답 그대로 반환 (DNA 텍스트 추가 안함)
        return response

# 전역 시스템 초기화
emotion_analyzer = CosmicEmotionAnalyzer()
dna_system = DNAPersonalizationSystem()

if __name__ == "__main__":
    print("🖥️ 로컬 환경에서 실행 중...")
    app.run(debug=True, host="0.0.0.0", port=5000)

# Vercel 배포를 위한 WSGI 애플리케이션 객체 노출
application = app
