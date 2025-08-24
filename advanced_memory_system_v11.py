"""
🧠 대화 기억/학습 시스템 v11.0 - 실시간 학습 & 32명 전문가 지원
=================================================================

v10.1 → v11.0 주요 업그레이드:
1. 전문가 16명 → 32명 확장
2. 실시간 피드백 학습 시스템
3. 상황별 맞춤 응답 엔진
4. 연속 대화 컨텍스트 관리
5. 대화 패턴 분석 AI
"""

import json
import os
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import sqlite3
from pathlib import Path


class ConversationMode(Enum):
    """대화 모드 정의"""

    SINGLE = "단일 질문"
    CONTINUOUS = "연속 대화"
    DEEP_DIVE = "심화 탐구"
    PROBLEM_SOLVING = "문제 해결"
    CREATIVE = "창의적 협업"


class FeedbackType(Enum):
    """피드백 유형"""

    POSITIVE = "좋음"
    NEGATIVE = "나쁨"
    HELPFUL = "도움됨"
    IRRELEVANT = "관련없음"
    MORE_DETAIL = "더 자세히"
    SIMPLER = "더 간단히"


@dataclass
class ConversationContext:
    """연속 대화 컨텍스트"""

    conversation_id: str
    mode: ConversationMode
    topic: str
    expert_chain: List[str]  # 참여한 전문가들
    context_history: List[Dict]
    current_goal: str
    progress: float  # 0.0 ~ 1.0
    last_updated: float


@dataclass
class UserFeedback:
    """사용자 피드백 데이터"""

    conversation_id: str
    message_id: str
    feedback_type: FeedbackType
    rating: int  # 1-5
    comment: Optional[str]
    timestamp: float


class AdvancedMemorySystem:
    """고급 메모리 및 학습 시스템 v11.0"""

    def __init__(self, memory_file: str = "advanced_memory_v11.json"):
        """시스템 초기화"""
        self.memory_file = memory_file
        self.db_file = memory_file.replace(".json", ".db")

        # 기본 데이터 구조
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.feedback_history: List[UserFeedback] = []
        self.context_sessions: Dict[str, ConversationContext] = {}

        # 실시간 학습 데이터
        self.pattern_learning: Dict[str, Any] = {}
        self.expert_performance: Dict[str, Dict] = {}
        self.adaptation_rules: List[Dict] = []

        # 32명 전문가 시스템
        self.experts = self._initialize_32_experts()

        # 데이터베이스 초기화
        self._init_database()
        self.load_memory()

        print(f"🧠 AdvancedMemorySystem v11.0 초기화 완료")
        print(f"📊 32명 전문가 시스템 활성화")
        print(f"🔄 실시간 학습 모드 ON")

    def _initialize_32_experts(self) -> Dict[str, Dict]:
        """32명 전문가 시스템 초기화"""
        experts = {
            # 기존 16명 (개선)
            "counselor": {"name": "💚 상담사", "field": "심리상담", "level": "박사급"},
            "marketing": {
                "name": "📈 마케터",
                "field": "마케팅전략",
                "level": "박사급",
            },
            "finance": {"name": "💰 금융사", "field": "금융투자", "level": "박사급"},
            "medical": {"name": "👨‍⚕️ 의사", "field": "의료진단", "level": "박사급"},
            "education": {
                "name": "👩‍🏫 교육자",
                "field": "교육설계",
                "level": "박사급",
            },
            "creative": {"name": "🎨 창작자", "field": "예술창작", "level": "박사급"},
            "tech": {"name": "💻 개발자", "field": "기술개발", "level": "박사급"},
            "business": {"name": "🏢 경영자", "field": "경영전략", "level": "박사급"},
            "legal": {"name": "⚖️ 변호사", "field": "법률상담", "level": "박사급"},
            "environment": {
                "name": "🌱 환경학자",
                "field": "환경보호",
                "level": "박사급",
            },
            "music": {"name": "🎵 음악가", "field": "음악창작", "level": "박사급"},
            "literature": {"name": "📚 문학가", "field": "문학창작", "level": "박사급"},
            "science": {"name": "🔬 과학자", "field": "과학연구", "level": "박사급"},
            "cooking": {"name": "🍳 요리사", "field": "요리예술", "level": "박사급"},
            "travel": {"name": "✈️ 여행가", "field": "여행기획", "level": "박사급"},
            "health": {"name": "🏃 건강사", "field": "건강관리", "level": "박사급"},
            # 신규 16명 (v11.0 추가)
            "ai_researcher": {
                "name": "🤖 AI연구자",
                "field": "인공지능",
                "level": "노벨급",
            },
            "quantum": {
                "name": "⚛️ 양자물리학자",
                "field": "양자컴퓨팅",
                "level": "노벨급",
            },
            "biotech": {
                "name": "🧬 바이오테크",
                "field": "생명공학",
                "level": "노벨급",
            },
            "space": {"name": "🚀 우주학자", "field": "우주과학", "level": "노벨급"},
            "climate": {"name": "🌍 기후학자", "field": "기후변화", "level": "노벨급"},
            "neuro": {"name": "🧠 뇌과학자", "field": "신경과학", "level": "노벨급"},
            "crypto": {"name": "₿ 암호학자", "field": "블록체인", "level": "전설급"},
            "metaverse": {
                "name": "🌐 메타버스",
                "field": "가상현실",
                "level": "전설급",
            },
            "sustainability": {
                "name": "♻️ 지속가능",
                "field": "지속경영",
                "level": "전설급",
            },
            "data_scientist": {
                "name": "📊 데이터학자",
                "field": "빅데이터",
                "level": "전설급",
            },
            "social_impact": {
                "name": "🤝 사회혁신",
                "field": "사회문제",
                "level": "전설급",
            },
            "future_trend": {
                "name": "🔮 미래학자",
                "field": "미래예측",
                "level": "전설급",
            },
            "innovation": {"name": "💡 혁신가", "field": "혁신전략", "level": "전설급"},
            "philosopher": {
                "name": "🤔 철학자",
                "field": "철학사상",
                "level": "전설급",
            },
            "linguist": {"name": "🗣️ 언어학자", "field": "언어분석", "level": "전설급"},
            "anthropologist": {
                "name": "🏛️ 인류학자",
                "field": "문화연구",
                "level": "전설급",
            },
        }

        return experts

    def _init_database(self):
        """SQLite 데이터베이스 초기화 (Vercel 환경 최적화)"""
        try:
            # Vercel 환경에서는 /tmp 디렉토리 사용
            import tempfile
            if not os.path.exists(os.path.dirname(self.db_file)):
                # 임시 디렉토리에 데이터베이스 생성
                temp_dir = tempfile.gettempdir()
                self.db_file = os.path.join(temp_dir, "advanced_memory_v11.db")
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # 테이블 생성
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    user_message TEXT,
                    bot_response TEXT,
                    emotion TEXT,
                    expert TEXT,
                    timestamp REAL,
                    context_data TEXT
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    message_id TEXT,
                    feedback_type TEXT,
                    rating INTEGER,
                    comment TEXT,
                    timestamp REAL
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    pattern_data TEXT,
                    confidence REAL,
                    usage_count INTEGER,
                    last_updated REAL
                )
            """
            )

            conn.commit()
            conn.close()
            print(f"📁 데이터베이스 초기화 완료: {self.db_file}")
            
        except Exception as e:
            print(f"⚠️ 데이터베이스 초기화 실패 (메모리 모드로 전환): {e}")
            # 메모리 모드로 전환
            self.db_file = ":memory:"

    def add_feedback(
        self,
        conversation_id: str,
        message_id: str,
        feedback_type: FeedbackType,
        rating: int,
        comment: str = "",
    ):
        """사용자 피드백 추가 및 실시간 학습"""

        feedback = UserFeedback(
            conversation_id=conversation_id,
            message_id=message_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
            timestamp=time.time(),
        )

        self.feedback_history.append(feedback)

        # 데이터베이스 저장
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO feedback (conversation_id, message_id, feedback_type, rating, comment, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                conversation_id,
                message_id,
                feedback_type.value,
                rating,
                comment,
                feedback.timestamp,
            ),
        )
        conn.commit()
        conn.close()

        # 🔄 실시간 학습 실행
        self._real_time_learning(feedback)

        print(f"📝 피드백 저장됨: {feedback_type.value} (평점: {rating})")

    def _real_time_learning(self, feedback: UserFeedback):
        """실시간 학습 알고리즘"""

        # 1. 응답 품질 패턴 학습
        if feedback.rating >= 4:  # 좋은 피드백
            self._reinforce_positive_pattern(feedback)
        elif feedback.rating <= 2:  # 나쁜 피드백
            self._adjust_negative_pattern(feedback)

        # 2. 전문가 성능 업데이트
        self._update_expert_performance(feedback)

        # 3. 적응 규칙 생성/수정
        self._generate_adaptation_rules(feedback)

    def _reinforce_positive_pattern(self, feedback: UserFeedback):
        """긍정적 패턴 강화"""
        pattern_key = f"positive_{feedback.conversation_id}"

        if pattern_key not in self.pattern_learning:
            self.pattern_learning[pattern_key] = {
                "type": "positive_reinforcement",
                "confidence": 0.1,
                "examples": [],
                "characteristics": [],
            }

        # 신뢰도 증가
        self.pattern_learning[pattern_key]["confidence"] = min(
            self.pattern_learning[pattern_key]["confidence"] + 0.1, 1.0
        )

        print(f"✅ 긍정 패턴 강화: {pattern_key}")

    def _adjust_negative_pattern(self, feedback: UserFeedback):
        """부정적 패턴 조정"""
        pattern_key = f"negative_{feedback.conversation_id}"

        # 개선 방향 결정
        if feedback.feedback_type == FeedbackType.MORE_DETAIL:
            self._add_adaptation_rule("increase_detail", feedback.conversation_id)
        elif feedback.feedback_type == FeedbackType.SIMPLER:
            self._add_adaptation_rule("simplify_response", feedback.conversation_id)
        elif feedback.feedback_type == FeedbackType.IRRELEVANT:
            self._add_adaptation_rule("improve_relevance", feedback.conversation_id)

        print(f"🔧 부정 패턴 조정: {feedback.feedback_type.value}")

    def _add_adaptation_rule(self, rule_type: str, conversation_id: str):
        """적응 규칙 추가"""
        rule = {
            "type": rule_type,
            "conversation_id": conversation_id,
            "created": time.time(),
            "weight": 1.0,
        }

        self.adaptation_rules.append(rule)
        print(f"📋 적응 규칙 추가: {rule_type}")

    def _update_expert_performance(self, feedback: UserFeedback):
        """전문가 성능 업데이트"""
        conversation_id = feedback.conversation_id
        rating = feedback.rating

        if conversation_id in self.context_sessions:
            context = self.context_sessions[conversation_id]
            for expert in context.expert_chain:
                if expert not in self.expert_performance:
                    self.expert_performance[expert] = {
                        "usage_count": 0,
                        "total_rating": 0,
                        "avg_rating": 0.0,
                        "feedback_count": 0,
                    }

                perf = self.expert_performance[expert]
                perf["usage_count"] += 1
                perf["total_rating"] += rating
                perf["feedback_count"] += 1
                perf["avg_rating"] = perf["total_rating"] / perf["feedback_count"]

                print(f"📊 {expert} 성능 업데이트: {perf['avg_rating']:.2f}")

    def _generate_adaptation_rules(self, feedback: UserFeedback):
        """적응 규칙 생성"""
        # 피드백 유형별 규칙 생성
        if feedback.feedback_type == FeedbackType.MORE_DETAIL:
            self._add_adaptation_rule("increase_detail", feedback.conversation_id)
        elif feedback.feedback_type == FeedbackType.SIMPLER:
            self._add_adaptation_rule("simplify_response", feedback.conversation_id)
        elif feedback.feedback_type == FeedbackType.IRRELEVANT:
            self._add_adaptation_rule("improve_relevance", feedback.conversation_id)
        elif feedback.rating >= 4:
            self._add_adaptation_rule("maintain_style", feedback.conversation_id)

    def select_best_experts(
        self, message: str, emotion: str, context: Optional[ConversationContext] = None
    ) -> List[str]:
        """상황에 맞는 최적 전문가 선택 (3-5명)"""

        # 1. 키워드 기반 1차 필터링
        keyword_matches = self._keyword_matching(message)

        # 2. 감정 기반 필터링
        emotion_matches = self._emotion_expert_matching(emotion)

        # 3. 컨텍스트 기반 필터링 (연속 대화)
        context_matches = []
        if context:
            context_matches = self._context_expert_matching(context)

        # 4. 성능 기반 정렬
        performance_scores = self._calculate_expert_scores(
            keyword_matches, emotion_matches, context_matches
        )

        # 5. 상위 3-5명 선택
        selected_experts = sorted(
            performance_scores.items(), key=lambda x: x[1], reverse=True
        )[:5]

        expert_names = [expert[0] for expert in selected_experts]

        print(f"🎯 선택된 전문가: {expert_names}")
        return expert_names

    def _keyword_matching(self, message: str) -> List[str]:
        """키워드 기반 전문가 매칭"""
        message_lower = message.lower()

        keyword_map = {
            "counselor": ["마음", "스트레스", "상담", "심리", "감정", "우울", "불안"],
            "marketing": ["마케팅", "브랜드", "광고", "홍보", "판매", "고객"],
            "finance": ["투자", "돈", "주식", "부동산", "금융", "경제", "재테크"],
            "medical": ["건강", "병원", "의사", "치료", "약", "증상", "진료"],
            "tech": ["프로그래밍", "개발", "코딩", "앱", "웹사이트", "AI", "기술"],
            "ai_researcher": ["인공지능", "머신러닝", "딥러닝", "AI", "알고리즘"],
            "quantum": ["양자", "퀀텀", "물리학", "컴퓨팅"],
            "space": ["우주", "천체", "로켓", "행성", "은하"],
            "philosophy": ["철학", "존재", "인생", "의미", "가치관", "윤리"],
        }

        matches = []
        for expert, keywords in keyword_map.items():
            if any(keyword in message_lower for keyword in keywords):
                matches.append(expert)

        return matches

    def _emotion_expert_matching(self, emotion: str) -> List[str]:
        """감정별 최적 전문가 매칭"""
        emotion_map = {
            "sad": ["counselor", "philosopher", "health"],
            "worried": ["counselor", "medical", "finance"],
            "angry": ["counselor", "legal", "philosopher"],
            "confused": ["education", "counselor", "philosopher"],
            "excited": ["creative", "innovation", "future_trend"],
            "happy": ["creative", "social_impact", "travel"],
            "grateful": ["philosopher", "social_impact", "counselor"],
        }

        return emotion_map.get(emotion, ["counselor"])

    def _context_expert_matching(self, context: ConversationContext) -> List[str]:
        """컨텍스트 기반 전문가 매칭"""
        # 이전 전문가 체인 고려
        previous_experts = context.expert_chain

        # 연관 전문가 추천
        related_map = {
            "marketing": ["business", "creative", "data_scientist"],
            "finance": ["business", "data_scientist", "future_trend"],
            "tech": ["ai_researcher", "data_scientist", "innovation"],
            "medical": ["biotech", "neuro", "health"],
            "education": ["innovation", "social_impact", "future_trend"],
        }

        suggestions = []
        for expert in previous_experts:
            if expert in related_map:
                suggestions.extend(related_map[expert])

        return list(set(suggestions))  # 중복 제거

    def _calculate_expert_scores(
        self,
        keyword_matches: List[str],
        emotion_matches: List[str],
        context_matches: List[str],
    ) -> Dict[str, float]:
        """전문가별 종합 점수 계산"""
        scores = {}

        # 기본 점수 초기화
        for expert in self.experts.keys():
            scores[expert] = 0.0

        # 키워드 매칭 점수 (40%)
        for expert in keyword_matches:
            scores[expert] += 4.0

        # 감정 매칭 점수 (30%)
        for expert in emotion_matches:
            scores[expert] += 3.0

        # 컨텍스트 매칭 점수 (20%)
        for expert in context_matches:
            scores[expert] += 2.0

        # 성능 기반 보너스 (10%)
        for expert in self.expert_performance:
            performance = self.expert_performance[expert]
            avg_rating = performance.get("avg_rating", 3.0)
            scores[expert] += (avg_rating - 3.0) * 1.0

        return scores

    def create_conversation_context(
        self, conversation_id: str, mode: ConversationMode, topic: str
    ) -> ConversationContext:
        """연속 대화 컨텍스트 생성"""
        context = ConversationContext(
            conversation_id=conversation_id,
            mode=mode,
            topic=topic,
            expert_chain=[],
            context_history=[],
            current_goal="대화 시작",
            progress=0.0,
            last_updated=time.time(),
        )

        self.context_sessions[conversation_id] = context
        print(f"🔄 연속 대화 컨텍스트 생성: {topic}")

        return context

    def update_conversation_context(
        self,
        conversation_id: str,
        message: str,
        response: str,
        expert: str,
        emotion: str,
    ):
        """대화 컨텍스트 업데이트"""
        if conversation_id not in self.context_sessions:
            return

        context = self.context_sessions[conversation_id]

        # 전문가 체인 업데이트
        if expert not in context.expert_chain:
            context.expert_chain.append(expert)

        # 히스토리 추가
        context.context_history.append(
            {
                "message": message,
                "response": response,
                "expert": expert,
                "emotion": emotion,
                "timestamp": time.time(),
            }
        )

        # 진행도 업데이트
        context.progress = min(context.progress + 0.1, 1.0)
        context.last_updated = time.time()

        print(f"🔄 컨텍스트 업데이트: {expert} 참여")

    def generate_contextual_response(
        self, message: str, expert: str, context: Optional[ConversationContext] = None
    ) -> str:
        """컨텍스트 기반 응답 생성"""
        base_response = self._generate_expert_response(message, expert)

        if not context or not context.context_history:
            return base_response

        # 연속성 추가
        continuity_phrase = self._generate_continuity_phrase(context)

        # 적응 규칙 적용
        adapted_response = self._apply_adaptation_rules(
            base_response, context.conversation_id
        )

        return f"{continuity_phrase} {adapted_response}"

    def _generate_continuity_phrase(self, context: ConversationContext) -> str:
        """연속성 문구 생성"""
        if len(context.context_history) == 1:
            return "앞서 말씀하신 내용을 바탕으로,"
        elif len(context.context_history) <= 3:
            return "지금까지의 대화를 종합해보면,"
        else:
            return "전체적인 맥락에서 보면,"

    def _apply_adaptation_rules(self, response: str, conversation_id: str) -> str:
        """적응 규칙 적용"""
        adapted = response

        for rule in self.adaptation_rules:
            if rule["conversation_id"] == conversation_id:
                if rule["type"] == "increase_detail":
                    adapted += " (더 자세한 설명을 원하시면 말씀해 주세요.)"
                elif rule["type"] == "simplify_response":
                    adapted = self._simplify_text(adapted)
                elif rule["type"] == "improve_relevance":
                    adapted = f"구체적으로 말씀드리면, {adapted}"

        return adapted

    def _simplify_text(self, text: str) -> str:
        """텍스트 간소화"""
        # 긴 문장을 짧게 분할
        sentences = text.split(".")
        if len(sentences) > 2:
            return ". ".join(sentences[:2]) + "."
        return text

    def _generate_expert_response(self, message: str, expert: str) -> str:
        """전문가별 특화 응답 생성"""
        expert_info = self.experts.get(expert, {})
        expert_name = expert_info.get("name", "전문가")

        # 전문가별 기본 응답 템플릿
        response_templates = {
            "counselor": f"{expert_name}로서, 마음을 편안하게 갖고 함께 해결해봐요.",
            "ai_researcher": f"{expert_name}로서, 최신 AI 기술 관점에서 분석해드리겠습니다.",
            "quantum": f"{expert_name}로서, 양자역학적 접근으로 설명드리겠습니다.",
            "philosopher": f"{expert_name}로서, 철학적 관점에서 깊이 생각해봅시다.",
        }

        return response_templates.get(expert, f"{expert_name}로서 도움드리겠습니다.")

    def get_learning_insights(self) -> Dict[str, Any]:
        """학습 인사이트 조회"""
        return {
            "total_feedback": len(self.feedback_history),
            "avg_rating": self._calculate_avg_rating(),
            "learning_patterns": len(self.pattern_learning),
            "adaptation_rules": len(self.adaptation_rules),
            "expert_count": len(self.experts),
            "active_contexts": len(self.context_sessions),
        }

    def _calculate_avg_rating(self) -> float:
        """평균 평점 계산"""
        if not self.feedback_history:
            return 0.0

        total_rating = sum(f.rating for f in self.feedback_history)
        return round(total_rating / len(self.feedback_history), 2)

    def save_memory(self) -> bool:
        """메모리 저장"""
        try:
            data = {
                "conversation_history": self.conversation_history,
                "user_preferences": self.user_preferences,
                "pattern_learning": self.pattern_learning,
                "expert_performance": self.expert_performance,
                "adaptation_rules": self.adaptation_rules,
                "experts": self.experts,
                "version": "11.0",
                "last_updated": time.time(),
            }

            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"🧠 메모리 저장 완료 (v11.0)")
            return True
        except Exception as e:
            print(f"❌ 메모리 저장 실패: {e}")
            return False

    def load_memory(self) -> bool:
        """메모리 로드"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.conversation_history = data.get("conversation_history", [])
                self.user_preferences = data.get("user_preferences", {})
                self.pattern_learning = data.get("pattern_learning", {})
                self.expert_performance = data.get("expert_performance", {})
                self.adaptation_rules = data.get("adaptation_rules", [])

                print(f"🧠 메모리 로드 완료: {len(self.conversation_history)}개 대화")
                return True
            else:
                print("🧠 새로운 메모리 파일 생성")
                return True
        except Exception as e:
            print(f"❌ 메모리 로드 실패: {e}")
            return False


# 사용 예시
if __name__ == "__main__":
    # v11.0 시스템 초기화
    advanced_system = AdvancedMemorySystem()

    # 연속 대화 컨텍스트 생성
    context = advanced_system.create_conversation_context(
        "test_session", ConversationMode.CONTINUOUS, "AI와 미래 기술"
    )

    # 최적 전문가 선택
    message = "인공지능이 미래에 어떤 영향을 미칠까요?"
    experts = advanced_system.select_best_experts(message, "excited", context)

    print(f"💬 메시지: {message}")
    print(f"🎯 선택된 전문가: {experts}")

    # 피드백 추가
    advanced_system.add_feedback(
        "test_session", "msg_001", FeedbackType.HELPFUL, 5, "정말 유용한 답변이었어요!"
    )

    # 학습 인사이트 조회
    insights = advanced_system.get_learning_insights()
    print(f"📊 학습 현황: {insights}")

    # 메모리 저장
    advanced_system.save_memory()
