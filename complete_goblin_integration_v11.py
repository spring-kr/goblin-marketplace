"""
🏆 완전체 도깨비 통합 시스템 v11.0
=====================================

기존 26명 도깨비 + v11.0 고급 메모리 시스템 + 32명 전문가
- 실시간 학습
- 상황별 맞춤 응답
- 연속 대화 관리
- 피드백 기반 성능 개선
"""

from advanced_goblin_adapter_v11 import AdvancedGoblinAdapter
from advanced_memory_system_v11 import ConversationMode
import asyncio
import time
from typing import Dict, Any, Optional


class SuperGoblin:
    """v11.0 메모리 시스템과 통합된 슈퍼 도깨비"""

    def __init__(self, goblin_id: str, name: str, specialty: str, personality: str):
        self.goblin_id = goblin_id
        self.name = name
        self.specialty = specialty
        self.personality = personality

        # v11.0 고급 어댑터 연결
        self.adapter = AdvancedGoblinAdapter(f"{goblin_id}_{name}")

        # 도깨비별 고유 응답 패턴
        self.response_patterns = {
            "greeting": f"안녕하세요! {name}입니다. {specialty} 분야에서 도움드릴게요!",
            "specialty_intro": f"저는 {specialty} 전문가로서 {personality} 성격으로 도움드립니다.",
            "learning_mode": f"🧠 지금부터 학습 모드로 전환합니다. 더 나은 도움을 위해 피드백 부탁드려요!",
        }

        print(f"🚀 {name} 슈퍼도깨비 v11.0 초기화 완료")

    async def chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
        conversation_mode: str = "single",
    ) -> Dict[str, Any]:
        """고급 채팅 (v11.0)"""

        # 모드 변환
        mode_map = {
            "single": ConversationMode.SINGLE,
            "continuous": ConversationMode.CONTINUOUS,
            "deep": ConversationMode.DEEP_DIVE,
            "creative": ConversationMode.CREATIVE,
        }

        mode = mode_map.get(conversation_mode, ConversationMode.SINGLE)

        # 도깨비 전용 처리
        enhanced_message = self._enhance_message_with_goblin_context(message)

        # v11.0 고급 처리
        result = await self.adapter.process_advanced_message(
            user_id, enhanced_message, conversation_id, mode, self.specialty
        )

        # 도깨비 개성 적용
        personalized_response = self._apply_goblin_personality(result["response"])
        result["response"] = personalized_response
        result["goblin_info"] = {
            "name": self.name,
            "specialty": self.specialty,
            "personality": self.personality,
        }

        return result

    def _enhance_message_with_goblin_context(self, message: str) -> str:
        """도깨비 컨텍스트로 메시지 강화"""
        context_prefix = f"[{self.specialty} 전문분야] "
        return context_prefix + message

    def _apply_goblin_personality(self, response: str) -> str:
        """도깨비 개성 적용"""
        personality_traits = {
            "친근한": "😊 ",
            "전문적인": "🎯 ",
            "창의적인": "💡 ",
            "차분한": "🌿 ",
            "열정적인": "🔥 ",
            "꼼꼼한": "📋 ",
        }

        prefix = personality_traits.get(self.personality, "🤖 ")

        # 도깨비 이름 추가
        personalized = f"{prefix}{self.name}: {response}"

        # 전문분야 강조
        if self.specialty in response:
            personalized += f"\n\n💼 {self.specialty} 전문가로서 더 도움이 필요하시면 언제든 말씀해주세요!"

        return personalized

    async def learn_from_feedback(
        self,
        conversation_id: str,
        message_id: str,
        rating: int,
        feedback_type: str = "general",
        comment: Optional[str] = None,
    ):
        """피드백 학습"""
        self.adapter.add_user_feedback(
            conversation_id, message_id, rating, feedback_type, comment
        )

        # 도깨비별 학습 로그
        print(f"📚 {self.name} 학습 완료: {rating}점 ({feedback_type})")

    def get_performance_report(self) -> Dict[str, Any]:
        """성능 리포트"""
        performance = self.adapter.get_expert_performance()

        return {
            "goblin_name": self.name,
            "specialty": self.specialty,
            "total_experts": performance["total_experts"],
            "system_performance": performance["system_insights"],
            "top_experts": self._get_top_performing_experts(
                performance["expert_details"]
            ),
        }

    def _get_top_performing_experts(self, expert_details: Dict) -> list:
        """상위 성과 전문가"""
        sorted_experts = sorted(
            expert_details.items(), key=lambda x: x[1]["avg_rating"], reverse=True
        )
        return [(name, data["avg_rating"]) for name, data in sorted_experts[:5]]


class GoblinTeamManager:
    """도깨비 팀 매니저 v11.0"""

    def __init__(self):
        self.goblins = {}
        self.active_conversations = {}
        self._initialize_goblin_team()

    def _initialize_goblin_team(self):
        """도깨비 팀 초기화 (기존 26명 + v11.0 업그레이드)"""

        goblin_specs = [
            # 기존 핵심 도깨비들
            ("counselor", "심리상담도깨비", "심리상담", "친근한"),
            ("marketing", "마케팅도깨비", "마케팅전략", "창의적인"),
            ("finance", "재테크도깨비", "금융투자", "꼼꼼한"),
            ("health", "건강관리도깨비", "건강관리", "차분한"),
            ("education", "교육도깨비", "교육컨설팅", "전문적인"),
            # 원래 16명 박사급 도깨비들 추가
            ("ai_expert", "인공지능박사도깨비", "AI연구", "열정적인"),
            ("economics_expert", "경제학박사도깨비", "경제분석", "꼼꼼한"),
            ("art_expert", "예술학박사도깨비", "예술창작", "창의적인"),
            ("data_expert", "데이터과학박사도깨비", "데이터분석", "전문적인"),
            ("hr_expert", "인사관리박사도깨비", "인사관리", "친근한"),
            ("business_expert", "경영학박사도깨비", "경영전략", "전문적인"),
            ("sales_expert", "영업학박사도깨비", "영업전략", "열정적인"),
            ("consulting_expert", "컨설팅박사도깨비", "컨설팅", "차분한"),
            ("shopping_expert", "쇼핑박사도깨비", "구매분석", "친근한"),
            ("startup_expert", "창업학박사도깨비", "창업지원", "열정적인"),
            ("wellness_expert", "웰니스박사도깨비", "건강관리", "차분한"),
            ("writing_expert", "문학박사도깨비", "글쓰기", "창의적인"),
            # 새로운 고급 도깨비들 (v11.0)
            ("ai_specialist", "AI도깨비", "인공지능", "열정적인"),
            ("quantum_expert", "양자컴퓨팅도깨비", "양자컴퓨팅", "전문적인"),
            ("biotech_guru", "바이오도깨비", "생명공학", "꼼꼼한"),
            ("space_engineer", "우주항공도깨비", "우주항공", "창의적인"),
            ("sustainability", "환경에너지도깨비", "환경에너지", "차분한"),
            # 창의 분야
            ("creative_director", "창의기획도깨비", "창의기획", "창의적인"),
            ("storyteller", "스토리텔링도깨비", "스토리텔링", "친근한"),
            ("game_designer", "게임개발도깨비", "게임개발", "열정적인"),
            # 비즈니스 분야
            ("startup_mentor", "창업컨설팅도깨비", "창업컨설팅", "전문적인"),
            ("global_trader", "국제무역도깨비", "국제무역", "꼼꼼한"),
            # 문화 예술
            ("culture_expert", "문화기획도깨비", "문화기획", "창의적인"),
            ("music_producer", "음악제작도깨비", "음악제작", "열정적인"),
            # 기술 분야
            ("security_expert", "사이버보안도깨비", "사이버보안", "꼼꼼한"),
            ("blockchain_dev", "블록체인도깨비", "블록체인", "전문적인"),
            ("robotics_engineer", "로봇공학도깨비", "로봇공학", "창의적인"),
            # 사회 분야
            ("social_innovator", "사회혁신도깨비", "사회문제해결", "친근한"),
            ("policy_maker", "정책개발도깨비", "정책개발", "전문적인"),
            # 의료 분야
            ("medical_ai", "의료AI도깨비", "의료기술", "차분한"),
            ("pharma_researcher", "신약개발도깨비", "신약개발", "꼼꼼한"),
            # 기타 전문 분야
            ("language_tutor", "언어교육도깨비", "언어교육", "친근한"),
            ("travel_planner", "여행컨설팅도깨비", "여행컨설팅", "열정적인"),
            ("fashion_consultant", "패션스타일링도깨비", "패션스타일링", "창의적인"),
        ]

        for goblin_id, name, specialty, personality in goblin_specs:
            self.goblins[goblin_id] = SuperGoblin(
                goblin_id, name, specialty, personality
            )

        print(f"🎉 도깨비 팀 v11.0 초기화 완료: {len(self.goblins)}명")

    def get_goblin(self, goblin_id: str) -> Optional[SuperGoblin]:
        """도깨비 조회"""
        return self.goblins.get(goblin_id)

    def list_goblins(self) -> Dict[str, Dict[str, str]]:
        """도깨비 목록"""
        return {
            goblin_id: {
                "name": goblin.name,
                "specialty": goblin.specialty,
                "personality": goblin.personality,
            }
            for goblin_id, goblin in self.goblins.items()
        }

    async def chat_with_goblin(
        self,
        goblin_id: str,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
        mode: str = "single",
    ) -> Dict[str, Any]:
        """도깨비와 채팅"""

        if goblin_id not in self.goblins:
            return {"error": f"도깨비 '{goblin_id}'를 찾을 수 없습니다."}

        goblin = self.goblins[goblin_id]
        result = await goblin.chat(user_id, message, conversation_id, mode)

        # 활성 대화 추적
        if result.get("conversation_id"):
            self.active_conversations[result["conversation_id"]] = {
                "goblin_id": goblin_id,
                "user_id": user_id,
                "last_activity": time.time(),
            }

        return result

    async def team_collaboration(
        self,
        user_id: str,
        message: str,
        goblin_ids: list,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """팀 협업 (여러 도깨비 동시 참여)"""

        if not conversation_id:
            conversation_id = f"team_{user_id}_{int(time.time())}"

        team_responses = {}

        for goblin_id in goblin_ids[:5]:  # 최대 5명
            if goblin_id in self.goblins:
                result = await self.chat_with_goblin(
                    goblin_id, user_id, message, conversation_id, "continuous"
                )
                team_responses[goblin_id] = result

        # 팀 종합 응답 생성
        synthesis = self._synthesize_team_responses(team_responses)

        return {
            "conversation_id": conversation_id,
            "team_synthesis": synthesis,
            "individual_responses": team_responses,
            "participating_goblins": goblin_ids,
        }

    def _synthesize_team_responses(self, responses: Dict) -> str:
        """팀 응답 종합"""
        if not responses:
            return "팀 응답을 생성할 수 없습니다."

        synthesis = "🤝 도깨비 팀 협업 결과:\n\n"

        for i, (goblin_id, result) in enumerate(responses.items(), 1):
            goblin = self.goblins[goblin_id]
            response = result.get("response", "응답 없음")
            synthesis += f"{i}. {goblin.name} ({goblin.specialty}):\n{response}\n\n"

        synthesis += "💡 팀 종합 의견: 위 전문가들의 다양한 관점을 종합하여 최적의 해결방안을 제시해드렸습니다."

        return synthesis

    def get_team_performance(self) -> Dict[str, Any]:
        """팀 전체 성능"""
        total_performance = {
            "total_goblins": len(self.goblins),
            "active_conversations": len(self.active_conversations),
            "goblin_performances": {},
        }

        for goblin_id, goblin in self.goblins.items():
            total_performance["goblin_performances"][
                goblin_id
            ] = goblin.get_performance_report()

        return total_performance


# 실전 테스트
async def demo_complete_system():
    """완전체 시스템 데모"""

    print("🌟 완전체 도깨비 통합 시스템 v11.0 데모")
    print("=" * 60)

    # 팀 매니저 초기화
    team = GoblinTeamManager()

    # 1. 개별 도깨비 테스트
    print("\n👤 개별 도깨비 테스트:")
    result1 = await team.chat_with_goblin(
        "ai_specialist",
        "demo_user",
        "인공지능 창업 아이디어에 대해 조언해주세요",
        mode="continuous",
    )
    print(f"🤖 AI전문가: {result1['response'][:150]}...")

    # 2. 팀 협업 테스트
    print("\n🤝 팀 협업 테스트:")
    team_result = await team.team_collaboration(
        "demo_user",
        "스타트업 창업 계획서 작성 도움이 필요해요",
        ["startup_mentor", "marketing", "finance", "ai_specialist"],
    )
    print(f"👥 팀 협업: {team_result['team_synthesis'][:200]}...")

    # 3. 학습 피드백 테스트
    print("\n📚 학습 시스템 테스트:")
    goblin = team.get_goblin("ai_specialist")
    if goblin:
        await goblin.learn_from_feedback(
            result1["conversation_id"], "msg_001", 5, "helpful", "정말 도움이 되었어요!"
        )

    # 4. 성능 리포트
    print("\n📊 성능 리포트:")
    if goblin:
        performance = goblin.get_performance_report()
        print(f"도깨비: {performance['goblin_name']}")
        print(f"전문분야: {performance['specialty']}")
        print(f"시스템 성과: {performance['system_performance']}")

    print("\n🎉 완전체 시스템 데모 완료!")


if __name__ == "__main__":
    asyncio.run(demo_complete_system())
