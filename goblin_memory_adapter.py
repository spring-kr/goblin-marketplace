"""
🔗 도깨비-메모리시스템 통합 어댑터 v1.0
=============================================

기존 도깨비 시스템들과 새로운 ConversationMemorySystem을 연결하는 어댑터
"""

from conversation_memory_system import ConversationMemorySystem
from typing import Dict, Any, Optional
import json


class GoblinMemoryAdapter:
    """도깨비와 메모리 시스템을 연결하는 어댑터"""

    def __init__(self, goblin_name: str):
        """
        어댑터 초기화

        Args:
            goblin_name (str): 도깨비 이름 (파일명에 사용)
        """
        self.goblin_name = goblin_name
        self.memory_system = ConversationMemorySystem(f"{goblin_name}_memory.json")

    def process_user_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        사용자 메시지 처리 및 감정 분석

        Args:
            user_id (str): 사용자 ID
            message (str): 사용자 메시지

        Returns:
            dict: 처리 결과 (감정, 개인화 정보 등)
        """
        # 감정 분석 및 패턴 학습
        emotion = self.memory_system.analyze_user_patterns(message)

        # 개인화된 응답 생성
        personalized_response = self.memory_system.get_personalized_response(
            emotion, message
        )

        # 사용자 통계
        user_stats = self.memory_system.get_user_stats()

        return {
            "emotion": emotion,
            "suggested_response": personalized_response,
            "user_stats": user_stats,
            "memory_context": self.get_recent_context(user_id, 5),
        }

    def save_conversation(
        self, user_id: str, user_message: str, bot_response: str, emotion: str
    ):
        """
        대화 기록 저장

        Args:
            user_id (str): 사용자 ID
            user_message (str): 사용자 메시지
            bot_response (str): 봇 응답
            emotion (str): 감지된 감정
        """
        # 메모리 시스템에 저장
        self.memory_system.add_conversation(user_message, bot_response, emotion)

    def get_recent_context(self, user_id: str, count: int = 5) -> list:
        """
        최근 대화 맥락 가져오기

        Args:
            user_id (str): 사용자 ID
            count (int): 가져올 대화 수

        Returns:
            list: 최근 대화 기록
        """
        return (
            self.memory_system.conversation_history[-count:]
            if self.memory_system.conversation_history
            else []
        )

    def get_emotion_analysis(self, text: str) -> str:
        """
        감정 분석만 수행

        Args:
            text (str): 분석할 텍스트

        Returns:
            str: 감지된 감정
        """
        return self.memory_system.analyze_korean_emotion(text)

    def get_user_insights(self) -> Dict[str, Any]:
        """
        사용자 인사이트 제공

        Returns:
            dict: 사용자 분석 정보
        """
        stats = self.memory_system.get_user_stats()

        insights = {
            "personality_profile": {
                "dominant_emotion": stats.get("most_common_emotion", "neutral"),
                "communication_pattern": self._analyze_communication_pattern(stats),
                "activity_pattern": self._analyze_activity_pattern(stats),
            },
            "recommendations": self._generate_recommendations(stats),
            "conversation_summary": {
                "total_conversations": stats.get("total_conversations", 0),
                "emotion_distribution": stats.get("emotion_patterns", {}),
                "favorite_topics": list(stats.get("favorite_words", {}).keys())[:5],
            },
        }

        return insights

    def _analyze_communication_pattern(self, stats: Dict) -> str:
        """대화 패턴 분석"""
        emotion_patterns = stats.get("emotion_patterns", {})

        if not emotion_patterns:
            return "분석 중"

        # 주요 감정 분석
        dominant_emotions = sorted(
            emotion_patterns.items(), key=lambda x: x[1], reverse=True
        )[:3]

        if dominant_emotions[0][0] in ["happy", "excited", "love"]:
            return "긍정적이고 활발한 소통"
        elif dominant_emotions[0][0] in ["worried", "sad", "confused"]:
            return "신중하고 세심한 소통"
        elif dominant_emotions[0][0] in ["confident", "amazed"]:
            return "자신감 있고 호기심 많은 소통"
        else:
            return "균형잡힌 소통"

    def _analyze_activity_pattern(self, stats: Dict) -> str:
        """활동 패턴 분석"""
        time_patterns = stats.get("time_patterns", {})

        if not time_patterns:
            return "분석 중"

        # 가장 활발한 시간대
        active_hour = stats.get("most_active_hour")

        if active_hour:
            hour = int(active_hour)
            if 6 <= hour < 12:
                return "아침형 인간"
            elif 12 <= hour < 18:
                return "오후 활동적"
            elif 18 <= hour < 22:
                return "저녁형 인간"
            else:
                return "야간형 인간"

        return "규칙적인 활동"

    def _generate_recommendations(self, stats: Dict) -> list:
        """개인화 추천 생성"""
        recommendations = []

        emotion_patterns = stats.get("emotion_patterns", {})
        most_common = stats.get("most_common_emotion")

        if most_common == "worried":
            recommendations.extend(
                ["스트레스 관리 기법 안내", "긍정적 사고 유도", "단계별 문제 해결 접근"]
            )
        elif most_common == "excited":
            recommendations.extend(
                [
                    "심화 학습 콘텐츠 제공",
                    "새로운 도전 과제 제시",
                    "창의적 아이디어 공유",
                ]
            )
        elif most_common == "confused":
            recommendations.extend(
                ["명확한 단계별 설명", "시각적 자료 활용", "반복 학습 지원"]
            )

        return recommendations


# 사용 예시
if __name__ == "__main__":
    # 특정 도깨비용 어댑터 생성
    counselor_adapter = GoblinMemoryAdapter("counselor_goblin")

    # 사용자 메시지 처리
    result = counselor_adapter.process_user_message(
        "user123", "오늘 너무 스트레스받아요..."
    )
    print(f"감정: {result['emotion']}")
    print(f"제안 응답: {result['suggested_response']}")

    # 대화 저장
    counselor_adapter.save_conversation(
        "user123",
        "오늘 너무 스트레스받아요...",
        "스트레스가 많으시군요. 어떤 일로 힘드신가요?",
        result["emotion"],
    )

    # 사용자 인사이트
    insights = counselor_adapter.get_user_insights()
    print(f"사용자 성향: {insights['personality_profile']}")
    print(f"추천사항: {insights['recommendations']}")
