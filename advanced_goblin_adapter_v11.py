"""
🚀 고급 도깨비 어댑터 v11.0 - 32명 전문가 & 실시간 학습
==========================================================

v10.1 → v11.0 업그레이드:
- 32명 전문가 지원
- 실시간 피드백 학습
- 연속 대화 관리
- 상황별 맞춤 응답
"""

from advanced_memory_system_v11 import (
    AdvancedMemorySystem,
    ConversationMode,
    FeedbackType,
    ConversationContext,
)
from typing import Dict, Any, List, Optional
import time
import asyncio


class AdvancedGoblinAdapter:
    """고급 도깨비 어댑터 v11.0"""

    def __init__(self, goblin_name: str):
        """어댑터 초기화"""
        self.goblin_name = goblin_name
        self.memory_system = AdvancedMemorySystem(
            f"{goblin_name}_advanced_memory_v11.json"
        )
        self.active_contexts: Dict[str, ConversationContext] = {}

        print(f"🚀 {goblin_name} 고급 어댑터 v11.0 초기화 완료")
        print(f"👥 32명 전문가 시스템 활성화")

    async def process_advanced_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
        mode: ConversationMode = ConversationMode.SINGLE,
        topic: Optional[str] = None,
    ) -> Dict[str, Any]:
        """고급 메시지 처리 (v11.0)"""

        if not conversation_id:
            conversation_id = f"{user_id}_{int(time.time())}"

        # 🔄 연속 대화 컨텍스트 관리
        context = self._get_or_create_context(
            conversation_id, mode, topic or "일반 대화"
        )

        # 🧠 감정 분석 (메모리 시스템에서 분석 기능 사용)
        emotion = self._analyze_emotion(message)

        # 🎯 최적 전문가 선택 (3-5명)
        selected_experts = self.memory_system.select_best_experts(
            message, emotion, context
        )

        # 💫 다중 전문가 응답 생성
        expert_responses = await self._generate_multi_expert_responses(
            message, selected_experts, context
        )

        # 🔀 최적 응답 합성
        final_response = self._synthesize_responses(expert_responses, context)

        # 📝 컨텍스트 업데이트
        primary_expert = selected_experts[0] if selected_experts else "general"
        self.memory_system.update_conversation_context(
            conversation_id, message, final_response, primary_expert, emotion
        )

        # 📊 응답 데이터 구성
        response_data = {
            "response": final_response,
            "emotion": emotion,
            "selected_experts": selected_experts,
            "expert_responses": expert_responses,
            "conversation_mode": mode.value,
            "context_progress": context.progress,
            "expert_chain": context.expert_chain,
            "learning_insights": self.memory_system.get_learning_insights(),
            "conversation_id": conversation_id,
            "timestamp": time.time(),
        }

        return response_data

    def _analyze_emotion(self, message: str) -> str:
        """감정 분석 (v11.0 호환)"""
        # 간단한 감정 분석 구현
        emotion_keywords = {
            "기쁨": ["기쁘", "행복", "좋아", "감사", "만족", "신나", "즐거"],
            "슬픔": ["슬프", "우울", "힘들", "아프", "괴로", "눈물", "절망"],
            "분노": ["화나", "짜증", "분노", "열받", "빡치", "억울", "괘념"],
            "불안": ["걱정", "불안", "두려", "무서", "긴장", "스트레스"],
            "호기심": ["궁금", "알고 싶", "관심", "흥미", "신기", "어떻게"],
            "확신": ["확실", "분명", "틀림없", "확신", "당연"],
            "의구심": ["의심", "확실하지", "정말", "진짜", "혹시"],
            "놀람": ["놀라", "깜짝", "어머", "헉", "와"],
            "차분함": ["차분", "평온", "안정", "고요", "편안"],
        }

        message_lower = message.lower()
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion

        return "중립"

    def _get_or_create_context(
        self, conversation_id: Optional[str], mode: ConversationMode, topic: str
    ) -> ConversationContext:
        """컨텍스트 가져오기 또는 생성"""

        # conversation_id가 None인 경우 새로 생성
        if conversation_id is None:
            conversation_id = f"auto_{int(time.time())}"

        if conversation_id in self.memory_system.context_sessions:
            return self.memory_system.context_sessions[conversation_id]

        # 새 컨텍스트 생성
        context = self.memory_system.create_conversation_context(
            conversation_id, mode, topic
        )

        return context

    async def _generate_multi_expert_responses(
        self, message: str, experts: List[str], context: ConversationContext
    ) -> Dict[str, str]:
        """다중 전문가 응답 생성"""

        responses = {}

        for expert in experts:
            try:
                # 전문가별 특화 응답 생성
                expert_response = self.memory_system.generate_contextual_response(
                    message, expert, context
                )
                responses[expert] = expert_response

                # 짧은 지연 (실제 처리 시뮬레이션)
                await asyncio.sleep(0.1)

            except Exception as e:
                print(f"⚠️ {expert} 응답 생성 실패: {e}")
                responses[expert] = "죄송합니다. 일시적인 문제가 발생했습니다."

        return responses

    def _synthesize_responses(
        self, expert_responses: Dict[str, str], context: ConversationContext
    ) -> str:
        """전문가 응답 합성"""

        if not expert_responses:
            return "죄송합니다. 현재 응답을 생성할 수 없습니다."

        # 1. 주 응답 선택 (첫 번째 전문가)
        primary_expert = list(expert_responses.keys())[0]
        primary_response = expert_responses[primary_expert]

        # 2. 단일 전문가인 경우
        if len(expert_responses) == 1:
            return primary_response

        # 3. 다중 전문가 의견 통합
        if context.mode == ConversationMode.DEEP_DIVE:
            return self._create_comprehensive_response(expert_responses)
        elif context.mode == ConversationMode.CREATIVE:
            return self._create_creative_synthesis(expert_responses)
        else:
            return self._create_balanced_response(expert_responses)

    def _create_comprehensive_response(self, responses: Dict[str, str]) -> str:
        """종합적 응답 생성 (심화 탐구 모드)"""

        expert_names = list(responses.keys())
        main_response = responses[expert_names[0]]

        additional_perspectives = []
        for expert in expert_names[1:3]:  # 최대 3개 관점
            expert_info = self.memory_system.experts.get(expert, {})
            expert_name = expert_info.get("name", expert)
            additional_perspectives.append(f"{expert_name}: {responses[expert]}")

        if additional_perspectives:
            synthesis = f"{main_response}\n\n🔍 추가 전문가 의견:\n"
            synthesis += "\n".join(additional_perspectives)
            return synthesis

        return main_response

    def _create_creative_synthesis(self, responses: Dict[str, str]) -> str:
        """창의적 응답 합성 (창의 협업 모드)"""

        # 모든 응답을 창의적으로 융합
        all_responses = list(responses.values())

        synthesis = "💡 창의적 융합 관점:\n\n"
        synthesis += f"{all_responses[0]}"

        if len(all_responses) > 1:
            synthesis += f"\n\n🎨 또한, {all_responses[1]}"

        if len(all_responses) > 2:
            synthesis += f"\n\n✨ 더 나아가, {all_responses[2]}"

        return synthesis

    def _create_balanced_response(self, responses: Dict[str, str]) -> str:
        """균형잡힌 응답 생성 (일반 모드)"""

        primary_response = list(responses.values())[0]

        # 간단한 추가 의견 (최대 1개)
        if len(responses) > 1:
            secondary_expert = list(responses.keys())[1]
            secondary_response = responses[secondary_expert]
            expert_info = self.memory_system.experts.get(secondary_expert, {})
            expert_name = expert_info.get("name", secondary_expert)

            return f"{primary_response}\n\n💭 {expert_name}의 추가 의견: {secondary_response}"

        return primary_response

    def add_user_feedback(
        self,
        conversation_id: str,
        message_id: str,
        rating: int,
        feedback_type: str = "general",
        comment: Optional[str] = None,
    ):
        """사용자 피드백 추가"""

        # 문자열을 FeedbackType으로 변환
        feedback_map = {
            "positive": FeedbackType.POSITIVE,
            "negative": FeedbackType.NEGATIVE,
            "helpful": FeedbackType.HELPFUL,
            "irrelevant": FeedbackType.IRRELEVANT,
            "more_detail": FeedbackType.MORE_DETAIL,
            "simpler": FeedbackType.SIMPLER,
            "general": FeedbackType.POSITIVE if rating >= 4 else FeedbackType.NEGATIVE,
        }

        feedback_type_enum = feedback_map.get(feedback_type, FeedbackType.POSITIVE)

        self.memory_system.add_feedback(
            conversation_id, message_id, feedback_type_enum, rating, comment or ""
        )

        print(f"📝 피드백 처리 완료: {rating}점 ({feedback_type})")

    def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """대화 요약 조회"""

        if conversation_id not in self.memory_system.context_sessions:
            return {"error": "대화 세션을 찾을 수 없습니다"}

        context = self.memory_system.context_sessions[conversation_id]

        summary = {
            "conversation_id": conversation_id,
            "mode": context.mode.value,
            "topic": context.topic,
            "progress": context.progress,
            "expert_chain": context.expert_chain,
            "total_exchanges": len(context.context_history),
            "duration": (
                time.time() - context.context_history[0]["timestamp"]
                if context.context_history
                else 0
            ),
            "last_updated": context.last_updated,
        }

        return summary

    def recommend_next_actions(self, conversation_id: str) -> List[str]:
        """다음 행동 추천"""

        if conversation_id not in self.memory_system.context_sessions:
            return ["새로운 대화를 시작해보세요."]

        context = self.memory_system.context_sessions[conversation_id]
        recommendations = []

        # 진행도 기반 추천
        if context.progress < 0.3:
            recommendations.append("더 구체적인 질문을 해보세요")
            recommendations.append("관심 있는 세부 분야를 알려주세요")
        elif context.progress < 0.7:
            recommendations.append("다른 관점에서 접근해볼까요?")
            recommendations.append("실제 적용 방안을 논의해보세요")
        else:
            recommendations.append("결론을 정리해볼까요?")
            recommendations.append("추가 학습 자료를 요청해보세요")

        # 전문가 체인 기반 추천
        if len(context.expert_chain) == 1:
            recommendations.append("다른 전문가의 의견도 들어보세요")

        return recommendations[:3]  # 최대 3개

    def get_expert_performance(self) -> Dict[str, Any]:
        """전문가 성능 조회"""

        insights = self.memory_system.get_learning_insights()
        expert_stats = {}

        for expert_id, expert_info in self.memory_system.experts.items():
            expert_stats[expert_id] = {
                "name": expert_info["name"],
                "field": expert_info["field"],
                "level": expert_info["level"],
                "usage_count": self.memory_system.expert_performance.get(
                    expert_id, {}
                ).get("usage_count", 0),
                "avg_rating": self.memory_system.expert_performance.get(
                    expert_id, {}
                ).get("avg_rating", 0.0),
            }

        return {
            "total_experts": len(self.memory_system.experts),
            "expert_details": expert_stats,
            "system_insights": insights,
        }


# 사용 예시 및 테스트
async def test_advanced_adapter():
    """고급 어댑터 테스트"""

    adapter = AdvancedGoblinAdapter("advanced_test")

    print("🧪 고급 어댑터 v11.0 테스트 시작")
    print("=" * 60)

    # 1. 단일 대화 테스트
    print("\n📝 단일 대화 테스트:")
    result1 = await adapter.process_advanced_message(
        "user123",
        "인공지능과 양자컴퓨팅의 미래에 대해 알고 싶어요",
        mode=ConversationMode.SINGLE,
    )

    print(f"🤖 응답: {result1['response'][:100]}...")
    print(f"🎯 선택된 전문가: {result1['selected_experts']}")
    print(f"😊 감정: {result1['emotion']}")

    # 2. 연속 대화 테스트
    print("\n🔄 연속 대화 테스트:")
    conversation_id = result1["conversation_id"]

    result2 = await adapter.process_advanced_message(
        "user123",
        "좀 더 구체적인 응용 분야를 알려주세요",
        conversation_id=conversation_id,
        mode=ConversationMode.CONTINUOUS,
    )

    print(f"🤖 응답: {result2['response'][:100]}...")
    print(f"🎯 전문가 체인: {result2['expert_chain']}")
    print(f"📊 진행도: {result2['context_progress']:.1%}")

    # 3. 피드백 테스트
    print("\n📝 피드백 테스트:")
    adapter.add_user_feedback(
        conversation_id, "msg_001", 5, "helpful", "정말 유용했어요!"
    )

    # 4. 추천 시스템 테스트
    print("\n💡 추천 시스템 테스트:")
    recommendations = adapter.recommend_next_actions(conversation_id)
    print(f"추천 행동: {recommendations}")

    # 5. 대화 요약
    print("\n📋 대화 요약:")
    summary = adapter.get_conversation_summary(conversation_id)
    print(f"대화 주제: {summary['topic']}")
    print(f"참여 전문가: {summary['expert_chain']}")
    print(f"진행도: {summary['progress']:.1%}")

    # 6. 전문가 성능
    print("\n👥 전문가 성능:")
    performance = adapter.get_expert_performance()
    print(f"총 전문가 수: {performance['total_experts']}")
    print(f"시스템 인사이트: {performance['system_insights']}")


if __name__ == "__main__":
    asyncio.run(test_advanced_adapter())
