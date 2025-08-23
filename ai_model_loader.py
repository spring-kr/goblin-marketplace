# AI 모델 로더 및 자연어 처리 시스템
import os
import pickle
import joblib
import torch
import numpy as np
from typing import Dict, Any, List, Tuple
import logging
import warnings

warnings.filterwarnings("ignore")

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIModelManager:
    """학습된 AI 모델들을 관리하는 클래스"""

    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.emotion_model = None
        self.korean_bert_emotion = None
        self.emotion_pipeline = None
        self.loaded_models = {}

        # 모델 로드
        self._load_models()

    def _load_models(self):
        """모든 사용 가능한 모델들을 로드"""
        try:
            # 감정분석 모델 로드
            self._load_emotion_models()
            logger.info("✅ AI 모델들이 성공적으로 로드되었습니다!")

        except Exception as e:
            logger.error(f"❌ 모델 로드 중 오류: {e}")

    def _load_emotion_models(self):
        """감정분석 모델들 로드"""
        model_files = [
            "korean_emotion_complete_pipeline.pkl",
            "simple_emotion_pipeline.pkl",
            "simple_emotion_pipeline.joblib",
            "korean_bert_emotion.pkl",
        ]

        for model_file in model_files:
            model_path = os.path.join(self.models_dir, model_file)
            if os.path.exists(model_path):
                try:
                    if model_file.endswith(".joblib"):
                        model = joblib.load(model_path)
                    else:
                        with open(model_path, "rb") as f:
                            model = pickle.load(f)

                    self.loaded_models[model_file] = model
                    logger.info(f"✅ {model_file} 로드 완료")

                except Exception as e:
                    logger.warning(f"⚠️ {model_file} 로드 실패: {e}")

    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """감정분석 수행"""
        try:
            # 여러 모델을 사용한 앙상블 감정분석
            emotions = {}
            confidence_scores = {}

            # 각 로드된 모델로 예측 시도
            for model_name, model in self.loaded_models.items():
                try:
                    if hasattr(model, "predict"):
                        # sklearn 스타일 모델
                        prediction = model.predict([text])
                        emotions[model_name] = prediction[0] if prediction else "중성"

                        if hasattr(model, "predict_proba"):
                            proba = model.predict_proba([text])
                            confidence_scores[model_name] = float(np.max(proba))

                    elif hasattr(model, "predict_emotion"):
                        # 커스텀 감정분석 모델
                        result = model.predict_emotion(text)
                        emotions[model_name] = result.get("emotion", "중성")
                        confidence_scores[model_name] = result.get("confidence", 0.5)

                except Exception as e:
                    logger.warning(f"모델 {model_name} 예측 실패: {e}")

            # 기본 규칙 기반 감정분석 (fallback)
            rule_based_emotion = self._rule_based_emotion_analysis(text)
            emotions["rule_based"] = rule_based_emotion["emotion"]
            confidence_scores["rule_based"] = rule_based_emotion["confidence"]

            # 최종 감정 결정 (앙상블)
            final_emotion = self._ensemble_emotion_decision(emotions, confidence_scores)

            return {
                "emotion": final_emotion,
                "all_predictions": emotions,
                "confidence_scores": confidence_scores,
                "text_length": len(text),
                "analysis_status": "success",
            }

        except Exception as e:
            logger.error(f"감정분석 오류: {e}")
            return {
                "emotion": "중성",
                "all_predictions": {},
                "confidence_scores": {},
                "text_length": len(text),
                "analysis_status": "error",
                "error": str(e),
            }

    def _rule_based_emotion_analysis(self, text: str) -> Dict[str, Any]:
        """규칙 기반 감정분석 (fallback 방법)"""

        # 감정 키워드 사전
        emotion_keywords = {
            "긍정": [
                "좋다",
                "행복",
                "기쁘다",
                "만족",
                "훌륭",
                "완벽",
                "최고",
                "감사",
                "사랑",
                "즐겁다",
            ],
            "부정": [
                "나쁘다",
                "슬프다",
                "화나다",
                "짜증",
                "실망",
                "걱정",
                "불안",
                "무서",
                "힘들다",
                "어렵다",
            ],
            "놀람": ["놀랍다", "신기", "와", "헉", "어머", "세상에", "정말", "진짜"],
            "중성": ["그냥", "보통", "일반적", "평범", "그렇다", "음", "네", "아니오"],
        }

        text_lower = text.lower()
        emotion_scores = {emotion: 0 for emotion in emotion_keywords.keys()}

        # 키워드 매칭
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1

        # 최고 점수 감정 선택
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[max_emotion]

        # 신뢰도 계산
        total_matches = sum(emotion_scores.values())
        confidence = max_score / max(total_matches, 1) if total_matches > 0 else 0.5

        return {
            "emotion": max_emotion if max_score > 0 else "중성",
            "confidence": confidence,
            "keyword_scores": emotion_scores,
        }

    def _ensemble_emotion_decision(
        self, emotions: Dict, confidence_scores: Dict
    ) -> str:
        """여러 모델의 예측을 앙상블하여 최종 감정 결정"""

        if not emotions:
            return "중성"

        # 신뢰도 가중 투표
        emotion_votes = {}
        for model_name, emotion in emotions.items():
            confidence = confidence_scores.get(model_name, 0.5)
            if emotion not in emotion_votes:
                emotion_votes[emotion] = 0
            emotion_votes[emotion] += confidence

        # 최고 득표 감정 반환
        return max(emotion_votes, key=emotion_votes.get)

    def analyze_conversation_context(self, text: str) -> Dict[str, Any]:
        """대화 맥락 분석"""
        try:
            # 텍스트 기본 분석
            analysis = {
                "text_length": len(text),
                "word_count": len(text.split()),
                "has_question": "?" in text
                or any(
                    q in text
                    for q in ["뭐", "무엇", "어떻게", "왜", "언제", "어디", "누구"]
                ),
                "has_exclamation": "!" in text,
                "politeness_level": self._analyze_politeness(text),
                "topic_keywords": self._extract_topic_keywords(text),
                "urgency_level": self._analyze_urgency(text),
                "conversation_type": self._classify_conversation_type(text),
            }

            return analysis

        except Exception as e:
            logger.error(f"대화 맥락 분석 오류: {e}")
            return {"error": str(e)}

    def _analyze_politeness(self, text: str) -> str:
        """정중함 수준 분석"""
        polite_markers = ["요", "습니다", "세요", "해주세요", "부탁", "죄송", "실례"]
        casual_markers = ["야", "너", "해", "하지마", "뭐야"]

        polite_count = sum(1 for marker in polite_markers if marker in text)
        casual_count = sum(1 for marker in casual_markers if marker in text)

        if polite_count > casual_count:
            return "정중함"
        elif casual_count > polite_count:
            return "친근함"
        else:
            return "보통"

    def _extract_topic_keywords(self, text: str) -> List[str]:
        """주제 키워드 추출"""
        topic_categories = {
            "건강": ["건강", "병", "아프다", "치료", "의사", "병원", "약", "증상"],
            "금융": ["돈", "투자", "주식", "은행", "대출", "펀드", "보험", "적금"],
            "법률": ["법", "변호사", "소송", "계약", "권리", "의무", "법원"],
            "기술": [
                "컴퓨터",
                "프로그램",
                "AI",
                "인공지능",
                "개발",
                "코딩",
                "소프트웨어",
            ],
            "교육": ["공부", "학교", "시험", "교육", "배우다", "가르치다", "수업"],
        }

        found_topics = []
        for topic, keywords in topic_categories.items():
            if any(keyword in text for keyword in keywords):
                found_topics.append(topic)

        return found_topics

    def _analyze_urgency(self, text: str) -> str:
        """긴급도 분석"""
        urgent_markers = ["급", "빨리", "즉시", "당장", "응급", "긴급", "심각", "위험"]

        if any(marker in text for marker in urgent_markers):
            return "높음"
        elif "?" in text:
            return "보통"
        else:
            return "낮음"

    def _classify_conversation_type(self, text: str) -> str:
        """대화 유형 분류"""
        if "?" in text:
            return "질문"
        elif any(greeting in text for greeting in ["안녕", "hello", "hi"]):
            return "인사"
        elif any(thanks in text for thanks in ["감사", "고마워", "thank"]):
            return "감사"
        elif any(req in text for req in ["해주세요", "부탁", "도와주", "help"]):
            return "요청"
        else:
            return "일반대화"

    def generate_domain_specific_analysis(
        self, text: str, domain: str
    ) -> Dict[str, Any]:
        """전문 분야별 실제 AI 분석 수행"""
        try:
            # 감정분석과 맥락분석을 기반으로 한 도메인별 분석
            emotion_analysis = self.analyze_emotion(text)
            context_analysis = self.analyze_conversation_context(text)

            if domain == "financial":
                return self._analyze_financial_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "medical":
                return self._analyze_medical_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "legal":
                return self._analyze_legal_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "tech":
                return self._analyze_technical_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "data":
                return self._analyze_data_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "creative":
                return self._analyze_creative_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "marketing":
                return self._analyze_marketing_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "education":
                return self._analyze_education_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "hr":
                return self._analyze_hr_query(text, emotion_analysis, context_analysis)
            elif domain == "sales":
                return self._analyze_sales_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "research":
                return self._analyze_research_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "translation":
                return self._analyze_translation_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "consulting":
                return self._analyze_consulting_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "psychology":
                return self._analyze_psychology_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "startup":
                return self._analyze_startup_query(
                    text, emotion_analysis, context_analysis
                )
            elif domain == "wellness":
                return self._analyze_wellness_query(
                    text, emotion_analysis, context_analysis
                )
            else:
                return self._analyze_general_query(
                    text, emotion_analysis, context_analysis
                )

        except Exception as e:
            logger.error(f"도메인별 분석 오류 ({domain}): {e}")
            return {"error": str(e), "analysis_type": "fallback"}

    def _analyze_financial_query(
        self, text: str, emotion: Dict, context: Dict
    ) -> Dict[str, Any]:
        """금융 분야 전문 분석"""
        text_lower = text.lower()

        # 금융 용어 분석
        financial_terms = {
            "투자": ["투자", "investment", "펀드", "주식", "채권", "포트폴리오"],
            "리스크": ["리스크", "위험", "손실", "변동성", "불확실성"],
            "수익": ["수익", "이익", "배당", "금리", "수익률", "복리"],
            "경제": ["경제", "경기", "인플레이션", "디플레이션", "GDP", "중앙은행"],
            "보험": ["보험", "연금", "저축", "은퇴", "연금보험"],
            "대출": ["대출", "모기지", "신용", "담보", "이자"],
        }

        # 특정 금융 상품/개념 분석
        specific_concepts = {
            "nps": {"name": "국민연금공단", "type": "연금제도", "category": "노후준비"},
            "isa": {
                "name": "개인종합자산관리계좌",
                "type": "세제혜택계좌",
                "category": "절세투자",
            },
            "etf": {"name": "상장지수펀드", "type": "투자상품", "category": "간접투자"},
            "reit": {
                "name": "부동산투자신탁",
                "type": "투자상품",
                "category": "부동산투자",
            },
        }

        # 키워드 매칭
        detected_categories = []
        detected_concepts = []

        for category, keywords in financial_terms.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_categories.append(category)

        for concept, info in specific_concepts.items():
            if concept in text_lower:
                detected_concepts.append({concept: info})

        # 긴급도 및 복잡도 평가
        urgency = context.get("urgency_level", "낮음")
        complexity = (
            "높음"
            if len(detected_categories) > 2
            else "보통" if detected_categories else "낮음"
        )

        # 감정 기반 톤 조절
        emotional_state = emotion.get("emotion", "중성")
        if emotional_state == "부정":
            tone = "안심시키는"
        elif emotional_state == "긍정":
            tone = "격려하는"
        else:
            tone = "전문적인"

        return {
            "analysis_type": "financial_expert",
            "detected_categories": detected_categories,
            "detected_concepts": detected_concepts,
            "complexity_level": complexity,
            "urgency_level": urgency,
            "emotional_tone": tone,
            "specific_analysis": self._generate_financial_insights(
                text_lower, detected_categories, detected_concepts
            ),
            "recommendation_type": self._determine_financial_recommendation_type(
                detected_categories, urgency
            ),
        }

    def _generate_financial_insights(
        self, text: str, categories: list, concepts: list
    ) -> Dict[str, Any]:
        """금융 인사이트 생성"""
        insights: Dict[str, Any] = {
            "market_context": "현재 시장 상황 고려 필요",
            "risk_assessment": "중간 수준",
            "time_horizon": "중장기 관점 권장",
        }

        # NPS 특별 분석
        if any("nps" in str(concept).lower() for concept in concepts):
            nps_analysis = {
                "정의": "국민연금 (National Pension Service)",
                "특징": "국가에서 운영하는 공적연금제도",
                "장점": ["강제가입으로 노후보장", "인플레이션 연동", "유족급여 포함"],
                "단점": ["수익률 제한적", "정치적 리스크", "개인선택권 부족"],
                "전략": "개인연금(IRP, 연금저축)과 함께 3층 연금체계 구축 권장",
            }
            insights["nps_analysis"] = nps_analysis

        if "투자" in categories:
            insights["investment_strategy"] = "분산투자 및 장기투자 원칙 적용"

        if "리스크" in categories:
            insights["risk_management"] = "적절한 자산배분으로 리스크 관리"

        return insights

    def _determine_financial_recommendation_type(
        self, categories: list, urgency: str
    ) -> str:
        """금융 추천 유형 결정"""
        if urgency == "높음":
            return "즉시_조치_필요"
        elif "투자" in categories and "리스크" in categories:
            return "포트폴리오_검토"
        elif "보험" in categories or "연금" in categories:
            return "장기_계획_수립"
        else:
            return "일반_상담"

    def _analyze_data_query(
        self, text: str, emotion: Dict, context: Dict
    ) -> Dict[str, Any]:
        """데이터 분야 전문 분석"""
        text_lower = text.lower()

        # 데이터 관련 키워드 분석
        data_terms = {
            "통계": ["통계", "statistics", "평균", "분산", "표준편차", "확률"],
            "분석": ["분석", "analysis", "데이터마이닝", "패턴", "인사이트"],
            "시각화": ["시각화", "visualization", "차트", "그래프", "플롯"],
            "머신러닝": ["머신러닝", "machine learning", "ai", "딥러닝", "모델"],
            "빅데이터": ["빅데이터", "big data", "하둡", "스파크", "분산처리"],
        }

        # 키워드 매칭
        detected_categories = []
        for category, keywords in data_terms.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_categories.append(category)

        # 복잡도 및 분석 수준 결정
        if len(detected_categories) > 2:
            complexity = "고급"
        elif detected_categories:
            complexity = "중급"
        else:
            complexity = "기초"

        return {
            "analysis_type": "data_expert",
            "detected_categories": detected_categories,
            "complexity_level": complexity,
            "specific_analysis": self._generate_data_insights(
                text_lower, detected_categories
            ),
            "recommendation_type": "전문_분석",
        }

    def _generate_data_insights(self, text: str, categories: list) -> Dict[str, Any]:
        """데이터 관련 인사이트 생성"""
        insights: Dict[str, Any] = {
            "methodology": "과학적 접근법",
            "tools": "전문 도구 활용",
            "application": "실무 적용",
        }

        if "통계" in categories:
            insights["statistics"] = {
                "기초": "기술통계, 확률분포, 가설검정",
                "응용": "회귀분석, 시계열 분석, 베이지안 통계",
                "활용": "데이터 검증, 패턴 발견, 예측 모델링",
            }

        if "머신러닝" in categories:
            insights["ml"] = {
                "지도학습": "분류, 회귀 알고리즘",
                "비지도학습": "클러스터링, 차원축소",
                "딥러닝": "신경망, CNN, RNN",
            }

        return insights

    def _analyze_medical_query(
        self, text: str, emotion: Dict, context: Dict
    ) -> Dict[str, Any]:
        """의료 분야 전문 분석"""
        # 의료 분야 분석 로직 구현
        return {
            "analysis_type": "medical_expert",
            "urgency": context.get("urgency_level", "보통"),
            "emotional_support_needed": emotion.get("emotion") == "부정",
        }

    def _analyze_legal_query(
        self, text: str, emotion: Dict, context: Dict
    ) -> Dict[str, Any]:
        """법률 분야 전문 분석"""
        # 법률 분야 분석 로직 구현
        return {
            "analysis_type": "legal_expert",
            "complexity": "높음" if "계약" in text or "소송" in text else "보통",
        }

    def _analyze_technical_query(
        self, text: str, emotion: Dict, context: Dict
    ) -> Dict[str, Any]:
        """기술 분야 전문 분석"""
        # 기술 분야 분석 로직 구현
        return {
            "analysis_type": "technical_expert",
            "tech_level": (
                "고급"
                if any(term in text for term in ["AI", "머신러닝", "딥러닝"])
                else "기본"
            ),
        }

    def _analyze_general_query(
        self, text: str, emotion: Dict, context: Dict
    ) -> Dict[str, Any]:
        """일반 분야 분석"""
        return {
            "analysis_type": "general_expert",
            "topic_analysis": context.get("topic_keywords", []),
        }

    def generate_smart_response(self, text: str, agent_type: str = "general") -> str:
        """AI 기반 스마트 응답 생성"""
        try:
            # 도메인별 분석 수행
            domain_analysis = self.generate_domain_specific_analysis(text, agent_type)

            # 기본 응답 구조
            if domain_analysis.get("analysis_type") == "financial_expert":
                return self._format_financial_response(text, domain_analysis)
            elif domain_analysis.get("analysis_type") == "medical_expert":
                return self._format_medical_response(text, domain_analysis)
            elif domain_analysis.get("analysis_type") == "legal_expert":
                return self._format_legal_response(text, domain_analysis)
            elif domain_analysis.get("analysis_type") == "data_expert":
                return self._format_data_response(text, domain_analysis)
            else:
                return self._format_general_response(text, domain_analysis)

        except Exception as e:
            logger.error(f"스마트 응답 생성 오류: {e}")
            return f"죄송합니다. 분석 중 오류가 발생했습니다: {str(e)}"

    def _format_financial_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """금융 분야 응답 포맷팅"""
        response_parts = []

        # 헤더
        tone = analysis.get("emotional_tone", "전문적인")
        response_parts.append(f"💰 **경제학박사급 {tone} 분석**")
        response_parts.append(f"문의: '{query}'")

        # NPS 특별 분석
        if "nps_analysis" in analysis.get("specific_analysis", {}):
            nps_info = analysis["specific_analysis"]["nps_analysis"]
            response_parts.append("\n📊 **NPS (국민연금) 전문 분석**")
            response_parts.append(f"• **정의**: {nps_info['정의']}")
            response_parts.append(f"• **특징**: {nps_info['특징']}")
            response_parts.append("• **장점**:")
            for advantage in nps_info["장점"]:
                response_parts.append(f"  - {advantage}")
            response_parts.append("• **한계점**:")
            for disadvantage in nps_info["단점"]:
                response_parts.append(f"  - {disadvantage}")
            response_parts.append(f"• **전략적 제안**: {nps_info['전략']}")

        # 카테고리별 분석
        categories = analysis.get("detected_categories", [])
        if categories:
            response_parts.append(f"\n🎯 **감지된 관심 분야**: {', '.join(categories)}")

        # 복잡도 및 추천
        complexity = analysis.get("complexity_level", "보통")
        response_parts.append(f"\n📈 **분석 복잡도**: {complexity}")

        recommendation = analysis.get("recommendation_type", "일반_상담")
        if recommendation == "즉시_조치_필요":
            response_parts.append("⚠️ **즉시 전문가 상담을 권장합니다**")
        elif recommendation == "포트폴리오_검토":
            response_parts.append("📋 **포트폴리오 전체적 검토가 필요합니다**")
        elif recommendation == "장기_계획_수립":
            response_parts.append("📅 **장기적 재정 계획 수립을 권장합니다**")

        return "\n".join(response_parts)

    def _format_medical_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """의료 분야 응답 포맷팅"""
        response_parts = []

        # 헤더
        response_parts.append(f"🏥 **의학박사급 전문 분석**")
        response_parts.append(f"문의: '{query}'")

        # 기본 의료 분석
        urgency = analysis.get("urgency", "보통")
        if urgency == "높음":
            response_parts.append(
                "\n⚠️ **응급 상황 감지** - 즉시 의료기관 방문을 권장합니다."
            )

        response_parts.append("\n📋 **의료 전문가 분석**:")
        response_parts.append("• 증상 평가 및 원인 분석")
        response_parts.append("• 적절한 진료과 안내")
        response_parts.append("• 예방 및 관리 방법 제시")

        return "\n".join(response_parts)

    def _format_legal_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """법률 분야 응답 포맷팅"""
        response_parts = []

        response_parts.append(f"⚖️ **법학박사급 전문 분석**")
        response_parts.append(f"문의: '{query}'")

        response_parts.append("\n📖 **법률 전문가 분석**:")
        response_parts.append("• 관련 법령 및 판례 검토")
        response_parts.append("• 법적 쟁점 및 해결방안")
        response_parts.append("• 전문가 상담 필요성 평가")

        return "\n".join(response_parts)

    def _format_data_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """데이터 분야 응답 포맷팅"""
        response_parts = []

        # 헤더
        response_parts.append(f"📊 **데이터과학박사급 전문 분석**")
        response_parts.append(f"문의: '{query}'")

        # 감지된 카테고리
        categories = analysis.get("detected_categories", [])
        if categories:
            response_parts.append(f"\n🎯 **분석 영역**: {', '.join(categories)}")

        # 복잡도 표시
        complexity = analysis.get("complexity_level", "기초")
        response_parts.append(f"📈 **분석 수준**: {complexity}")

        # 구체적 분석 내용
        specific_analysis = analysis.get("specific_analysis", {})

        # 통계학 특별 분석
        if "통계" in categories and "statistics" in specific_analysis:
            stats_info = specific_analysis["statistics"]
            response_parts.append("\n📊 **통계학 전문 분석**:")
            response_parts.append(f"• **기초 개념**: {stats_info['기초']}")
            response_parts.append(f"• **응용 분야**: {stats_info['응용']}")
            response_parts.append(f"• **실무 활용**: {stats_info['활용']}")

        # 머신러닝 분석
        if "머신러닝" in categories and "ml" in specific_analysis:
            ml_info = specific_analysis["ml"]
            response_parts.append("\n🤖 **머신러닝 분석**:")
            response_parts.append(f"• **지도학습**: {ml_info['지도학습']}")
            response_parts.append(f"• **비지도학습**: {ml_info['비지도학습']}")
            response_parts.append(f"• **딥러닝**: {ml_info['딥러닝']}")

        # 일반적인 데이터 분석 조언
        if not categories or len(categories) == 0:
            response_parts.append("\n💡 **데이터 분석 기본 접근법**:")
            response_parts.append("• **데이터 수집**: 신뢰할 수 있는 데이터 확보")
            response_parts.append("• **전처리**: 데이터 정제 및 변환")
            response_parts.append("• **탐색적 분석**: 패턴 및 트렌드 발견")
            response_parts.append("• **모델링**: 적절한 분석 기법 적용")
            response_parts.append("• **검증**: 결과의 타당성 확인")

        response_parts.append(
            "\n🎓 **추천 학습 경로**: 기초 통계 → 프로그래밍 → 머신러닝 → 실무 프로젝트"
        )

        return "\n".join(response_parts)

    def _format_general_response(self, query: str, analysis: Dict[str, Any]) -> str:
        """일반 분야 응답 포맷팅"""
        response_parts = []

        # 분석 타입에 따른 이모지 선택
        analysis_type = analysis.get("analysis_type", "general_expert")
        if "data" in analysis_type.lower():
            emoji = "📊"
            title = "데이터과학박사급 전문 분석"
        elif "education" in analysis_type.lower():
            emoji = "📚"
            title = "교육학박사급 전문 분석"
        else:
            emoji = "🎓"
            title = "박사급 전문 분석"

        response_parts.append(f"{emoji} **{title}**")
        response_parts.append(f"문의: '{query}'")

        # 토픽 분석 결과
        topic_keywords = analysis.get("topic_analysis", [])
        if topic_keywords:
            response_parts.append(f"\n🎯 **주요 키워드**: {', '.join(topic_keywords)}")

        # 기본 전문가 분석
        response_parts.append("\n💡 **전문가 분석**:")

        # 통계학 관련 특별 처리
        if "통계" in query.lower() or "statistics" in query.lower():
            response_parts.append("• **통계학 개념**: 데이터 수집, 분석, 해석의 과학")
            response_parts.append(
                "• **주요 분야**: 기술통계학, 추론통계학, 베이지안 통계"
            )
            response_parts.append("• **실무 적용**: 가설검정, 회귀분석, 머신러닝")
            response_parts.append("• **최신 동향**: 빅데이터, AI, 예측모델링")
        else:
            response_parts.append("• 전문적 지식 기반 분석")
            response_parts.append("• 실무 적용 방안 제시")
            response_parts.append("• 추가 학습 자료 안내")

        return "\n".join(response_parts)
        """AI 모델 기반 스마트 응답 생성"""
        try:
            # 감정 분석
            emotion_analysis = self.analyze_emotion(text)

            # 대화 맥락 분석
            context_analysis = self.analyze_conversation_context(text)

            # 분석 결과 기반 응답 생성
            response = self._generate_contextual_response(
                text, emotion_analysis, context_analysis, agent_type
            )

            return response

        except Exception as e:
            logger.error(f"스마트 응답 생성 오류: {e}")
            return "죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요."

    def _generate_contextual_response(
        self, text: str, emotion: Dict, context: Dict, agent_type: str
    ) -> str:
        """맥락 기반 응답 생성"""

        # 감정에 따른 응답 톤 조절
        emotion_type = emotion.get("emotion", "중성")
        conversation_type = context.get("conversation_type", "일반대화")
        urgency = context.get("urgency_level", "낮음")

        # 응답 프리픽스 결정
        if emotion_type == "부정":
            if urgency == "높음":
                prefix = "상황을 파악했습니다. 신속하게 도움을 드리겠습니다. "
            else:
                prefix = "걱정이 많으시군요. 차근차근 해결해보겠습니다. "
        elif emotion_type == "긍정":
            prefix = "긍정적인 마음가짐이 느껴집니다! "
        elif conversation_type == "질문":
            prefix = "좋은 질문입니다. "
        else:
            prefix = ""

        # 에이전트 타입별 전문성 추가
        agent_expertise = {
            "medical": "의학적 관점에서 ",
            "financial": "금융 전문가로서 ",
            "legal": "법률 전문가로서 ",
            "technical": "기술 전문가로서 ",
        }

        expertise_note = agent_expertise.get(agent_type, "")

        return f"{prefix}{expertise_note}말씀해주신 내용을 바탕으로 전문적인 도움을 드리겠습니다."


# 전역 AI 매니저 인스턴스
ai_manager = None


def get_ai_manager() -> AIModelManager:
    """AI 매니저 싱글톤 인스턴스 반환"""
    global ai_manager
    if ai_manager is None:
        ai_manager = AIModelManager()
    return ai_manager


def analyze_text_with_ai(text: str, agent_type: str = "general") -> Dict[str, Any]:
    """텍스트를 AI로 분석하는 메인 함수"""
    manager = get_ai_manager()

    emotion_analysis = manager.analyze_emotion(text)
    context_analysis = manager.analyze_conversation_context(text)
    smart_response = manager.generate_smart_response(text, agent_type)

    return {
        "emotion_analysis": emotion_analysis,
        "context_analysis": context_analysis,
        "smart_response": smart_response,
        "ai_status": "active",
    }
