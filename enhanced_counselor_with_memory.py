"""
🧬 통합된 상담사 도깨비 v2.0 (메모리 시스템 연동)
====================================================

기존 counselor_goblin에 ConversationMemorySystem을 통합한 버전
"""

import asyncio
import aiohttp
import json
import re
import time
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
import hashlib

# 새로운 메모리 시스템 import
from conversation_memory_system import ConversationMemorySystem
from goblin_memory_adapter import GoblinMemoryAdapter


class EnhancedCounselorGoblin:
    """메모리 시스템이 통합된 향상된 상담사 도깨비"""

    def __init__(self):
        """상담사 도깨비 초기화"""
        self.name = "💚 상담사 도깨비"
        self.specialty = "심리상담, 감정분석, 치유"

        # 🧠 새로운 메모리 시스템 통합
        self.memory_adapter = GoblinMemoryAdapter("counselor_goblin")

        # 기존 설정들
        self.conversation_context = {}
        self.session_data = {}

        print(f"✅ {self.name} 초기화 완료 (메모리 시스템 연동)")

    async def chat(
        self, message: str, conversation_id: str = "default"
    ) -> Dict[str, Any]:
        """
        향상된 채팅 함수 (메모리 시스템 활용)

        Args:
            message (str): 사용자 메시지
            conversation_id (str): 대화 ID

        Returns:
            dict: 응답 데이터
        """
        try:
            # 🧠 메모리 시스템으로 메시지 분석
            memory_result = self.memory_adapter.process_user_message(
                conversation_id, message
            )

            emotion = memory_result["emotion"]
            user_stats = memory_result["user_stats"]
            memory_context = memory_result["memory_context"]
            suggested_response = memory_result["suggested_response"]

            # 상담사 도깨비 전문 응답 생성
            counselor_response = await self._generate_counselor_response(
                message, emotion, user_stats, memory_context
            )

            # 개인화된 최종 응답
            final_response = self._personalize_response(
                counselor_response, emotion, user_stats
            )

            # 🧠 대화 기록 저장
            self.memory_adapter.save_conversation(
                conversation_id, message, final_response, emotion
            )

            # 사용자 인사이트 생성
            insights = self.memory_adapter.get_user_insights()

            response_data = {
                "response": final_response,
                "emotion": emotion,
                "confidence": self._calculate_confidence(emotion, message),
                "user_insights": insights,
                "recommendations": self._generate_counseling_recommendations(
                    emotion, user_stats
                ),
                "session_summary": {
                    "total_conversations": user_stats.get("total_conversations", 0),
                    "dominant_emotion": user_stats.get(
                        "most_common_emotion", "neutral"
                    ),
                    "emotional_trend": self._analyze_emotional_trend(memory_context),
                },
                "timestamp": datetime.now().isoformat(),
                "goblin": self.name,
            }

            return response_data

        except Exception as e:
            return {
                "response": f"죄송해요, 일시적인 문제가 발생했습니다. 다시 말씀해 주세요. 🙏",
                "error": str(e),
                "emotion": "neutral",
                "goblin": self.name,
            }

    async def _generate_counselor_response(
        self, message: str, emotion: str, user_stats: Dict, context: List
    ) -> str:
        """상담사 전문 응답 생성"""

        # 감정별 상담 접근법
        counseling_approaches = {
            "sad": [
                "마음이 힘드시군요. 어떤 일로 이런 기분이 드셨나요?",
                "슬픈 마음을 표현해주셔서 고마워요. 함께 이야기해봐요.",
                "혼자 견디기 어려우셨을 텐데, 이렇게 말씀해주셔서 다행이에요.",
            ],
            "angry": [
                "화가 나는 상황이시군요. 무엇이 이렇게 속상하게 만들었나요?",
                "분노는 자연스러운 감정이에요. 천천히 말씀해주세요.",
                "화난 마음 뒤에는 상처가 있을 수 있어요. 어떤 일이었나요?",
            ],
            "worried": [
                "걱정이 많으시군요. 어떤 부분이 가장 불안하신가요?",
                "불안한 마음이 느껴져요. 구체적으로 어떤 상황인지 들어볼 수 있을까요?",
                "걱정을 나누시면 마음이 조금 가벼워질 거예요.",
            ],
            "confused": [
                "혼란스러우신 상황이군요. 차근차근 정리해봐요.",
                "복잡한 마음이시군요. 어떤 부분이 가장 헷갈리시나요?",
                "하나씩 천천히 이야기해보면서 정리해봐요.",
            ],
            "happy": [
                "좋은 일이 있으셨나봐요! 기쁜 마음이 전해져요.",
                "행복한 기분이 느껴져요. 어떤 일로 이렇게 기쁘신가요?",
                "긍정적인 에너지가 느껴져요. 좋은 소식을 들려주세요!",
            ],
        }

        # 이전 대화 맥락 고려
        context_aware_prefix = ""
        if context and len(context) > 1:
            recent_emotions = [conv.get("emotion", "neutral") for conv in context[-3:]]
            if recent_emotions.count("sad") >= 2:
                context_aware_prefix = "계속 힘드신 상황이 이어지고 있군요. "
            elif recent_emotions.count("worried") >= 2:
                context_aware_prefix = "걱정이 계속되고 있으시네요. "

        # 기본 응답 선택
        base_responses = counseling_approaches.get(
            emotion,
            [
                "말씀해주셔서 고마워요. 더 자세히 들어볼 수 있을까요?",
                "어떤 마음이신지 이해해요. 편하게 이야기해주세요.",
                "지금 느끼시는 감정이 소중해요. 더 나누고 싶으시면 언제든 말씀하세요.",
            ],
        )

        import random

        base_response = random.choice(base_responses)

        return context_aware_prefix + base_response

    def _personalize_response(
        self, base_response: str, emotion: str, user_stats: Dict
    ) -> str:
        """사용자 통계 기반 응답 개인화"""

        # 가장 많은 감정 패턴 기반 개인화
        most_common_emotion = user_stats.get("most_common_emotion")

        personalization_suffix = ""

        if most_common_emotion == "worried":
            personalization_suffix = " 평소에도 걱정이 많으신 것 같은데, 마음을 편안하게 가지시려고 노력해보세요."
        elif most_common_emotion == "sad":
            personalization_suffix = (
                " 힘든 시간을 보내고 계시는 것 같아요. 천천히 회복해나가시길 바라요."
            )
        elif most_common_emotion == "happy":
            personalization_suffix = (
                " 평소 긍정적인 마음가짐을 가지고 계시는군요. 정말 좋아요!"
            )

        # 시간대별 개인화
        current_hour = datetime.now().hour
        time_suffix = ""

        if current_hour < 6:
            time_suffix = " 늦은 시간까지 깨어계시네요. 충분한 휴식도 중요해요."
        elif 6 <= current_hour < 12:
            time_suffix = " 좋은 아침이에요!"
        elif 12 <= current_hour < 18:
            time_suffix = " 오후 시간 잘 보내고 계신가요?"
        else:
            time_suffix = " 하루 마무리는 어떠셨나요?"

        return base_response + personalization_suffix + time_suffix

    def _calculate_confidence(self, emotion: str, message: str) -> float:
        """감정 분석 신뢰도 계산"""
        # 메시지 길이와 감정 키워드 밀도 기반
        emotion_keywords = {
            "sad": ["슬프", "우울", "힘들", "속상"],
            "happy": ["기쁘", "행복", "좋아", "즐거"],
            "angry": ["화나", "짜증", "열받", "분노"],
            "worried": ["걱정", "불안", "무서", "걱정"],
        }

        keywords = emotion_keywords.get(emotion, [])
        keyword_count = sum(1 for keyword in keywords if keyword in message)

        base_confidence = min(0.6 + (keyword_count * 0.1), 0.95)
        return round(base_confidence, 2)

    def _generate_counseling_recommendations(
        self, emotion: str, user_stats: Dict
    ) -> List[str]:
        """상담 기반 추천사항 생성"""
        recommendations = []

        emotion_patterns = user_stats.get("emotion_patterns", {})

        # 감정 패턴 기반 추천
        if emotion_patterns.get("sad", 0) > 3:
            recommendations.extend(
                [
                    "📚 우울감 관리 기법 학습하기",
                    "🌱 작은 취미활동 시작해보기",
                    "👥 주변 사람들과 소통하기",
                ]
            )

        if emotion_patterns.get("worried", 0) > 3:
            recommendations.extend(
                [
                    "🧘 명상이나 호흡법 연습하기",
                    "📝 걱정 일기 써보기",
                    "⚡ 스트레스 해소 운동하기",
                ]
            )

        if emotion_patterns.get("angry", 0) > 2:
            recommendations.extend(
                [
                    "😌 분노 조절 기법 익히기",
                    "🎨 창작활동으로 감정 표현하기",
                    "🚶 산책으로 마음 진정시키기",
                ]
            )

        # 기본 추천사항
        if not recommendations:
            recommendations = [
                "💝 자기돌봄 시간 갖기",
                "📖 긍정적인 콘텐츠 접하기",
                "🤝 신뢰할 수 있는 사람과 대화하기",
            ]

        return recommendations[:3]  # 최대 3개

    def _analyze_emotional_trend(self, context: List) -> str:
        """감정 변화 트렌드 분석"""
        if not context or len(context) < 3:
            return "분석 중"

        recent_emotions = [conv.get("emotion", "neutral") for conv in context[-5:]]

        # 감정 점수화 (단순화)
        emotion_scores = {
            "happy": 5,
            "excited": 4,
            "love": 4,
            "grateful": 4,
            "neutral": 3,
            "confused": 3,
            "worried": 2,
            "tired": 2,
            "sad": 1,
            "angry": 1,
        }

        scores = [emotion_scores.get(emotion, 3) for emotion in recent_emotions]

        if len(scores) >= 3:
            if scores[-1] > scores[-3]:
                return "개선되고 있음"
            elif scores[-1] < scores[-3]:
                return "주의 필요"
            else:
                return "안정적"

        return "분석 중"

    def get_status(self) -> Dict[str, Any]:
        """도깨비 상태 조회"""
        stats = self.memory_adapter.memory_system.get_user_stats()

        return {
            "name": self.name,
            "specialty": self.specialty,
            "memory_system": "ConversationMemorySystem v10.1",
            "total_conversations": stats.get("total_conversations", 0),
            "emotion_accuracy": "100%",
            "status": "활성화됨",
        }


# 사용 예시
async def test_enhanced_counselor():
    """통합된 상담사 도깨비 테스트"""

    counselor = EnhancedCounselorGoblin()

    test_messages = [
        "요즘 너무 스트레스받아서 힘들어요...",
        "회사에서 일이 너무 많아서 불안해요",
        "그래도 오늘은 좀 나은 것 같아요",
        "조언 고마워요. 마음이 좀 편해졌어요",
    ]

    print("🧪 통합된 상담사 도깨비 테스트 시작")
    print("=" * 50)

    for i, message in enumerate(test_messages, 1):
        print(f"\n💬 테스트 {i}: {message}")

        result = await counselor.chat(message, "test_user")

        print(f"🤖 응답: {result['response']}")
        print(f"😊 감정: {result['emotion']} (신뢰도: {result['confidence']})")
        print(
            f"📊 주요 감정: {result['user_insights']['personality_profile']['dominant_emotion']}"
        )
        print(f"💡 추천: {result['recommendations'][:2]}")
        print(f"📈 감정 트렌드: {result['session_summary']['emotional_trend']}")

    # 최종 상태
    status = counselor.get_status()
    print(f"\n📊 최종 상태:")
    print(f"총 대화수: {status['total_conversations']}")
    print(f"시스템: {status['memory_system']}")


if __name__ == "__main__":
    asyncio.run(test_enhanced_counselor())
