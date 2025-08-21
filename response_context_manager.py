"""
맥락 기반 응답 생성을 위한 컨텍스트 관리자
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class ContextInfo:
    """컨텍스트 정보를 담는 클래스"""

    current_time: datetime
    expertise_areas: List[str]
    depth_level: int = 1
    previous_topics: List[str] = field(default_factory=list)
    conversation_flow: Dict[str, List[str]] = field(default_factory=dict)


class ResponseContextManager:
    """맥락 기반 응답 생성 관리자"""

    def __init__(self):
        self.default_structures = {
            "insight": ["상황 분석", "핵심 포인트", "주요 고려사항"],
            "approach": ["전략적 방향", "실행 단계", "중점 영역"],
            "advice": ["구체적 조언", "주의사항", "기대효과"],
        }

    def create_expertise_based_response(
        self, question: str, agent_info: dict, context: ContextInfo
    ) -> str:
        """전문성 기반의 맥락적 응답 생성"""
        context_patterns = {
            "follow_up": len(context.previous_topics) > 0,
            "depth_required": any(
                keyword in question.lower()
                for keyword in ["자세히", "구체적", "설명", "이유", "방법"]
            ),
            "action_required": any(
                keyword in question.lower()
                for keyword in ["어떻게", "방법", "단계", "순서", "해결"]
            ),
        }

        if context_patterns["depth_required"]:
            sections = ["insight", "approach", "advice"]
        elif context_patterns["action_required"]:
            sections = ["insight", "approach"]
        else:
            sections = ["insight", "advice"]

        response_parts = []
        greeting = self._generate_greeting(
            agent_info.get("name", "도깨비"), context.current_time
        )
        response_parts.append(greeting)

        expertise = agent_info.get("expertise") or [agent_info.get("field", "전문")]
        analysis = self._analyze_with_expertise(
            question, expertise, context.depth_level
        )
        response_parts.append(analysis)

        for section in sections:
            response_parts.append(
                self._generate_section_content(section, question, agent_info, context)
            )

        response_parts.append(
            self._generate_closing(
                context_patterns["follow_up"], agent_info.get("field", "전문")
            )
        )

        return "\n\n".join(response_parts)

    def _generate_greeting(self, agent_name: str, current_time: datetime) -> str:
        hour = current_time.hour
        if 5 <= hour < 12:
            time_greeting = "좋은 아침입니다"
        elif 12 <= hour < 18:
            time_greeting = "안녕하세요"
        else:
            time_greeting = "안녕하세요"
        return f"{agent_name}입니다! {time_greeting}. 💫"

    def _analyze_with_expertise(
        self, question: str, expertise_areas: List[str], depth_level: int
    ) -> str:
        relevant = expertise_areas[:1]
        return f"귀하의 질문에 대해 {', '.join(relevant)}의 관점에서 {'심층적인' if depth_level>1 else '기본적인'} 분석을 진행했습니다."

    def _generate_section_content(
        self, section: str, question: str, agent_info: dict, context: ContextInfo
    ) -> str:
        structures = self.default_structures[section]
        return f"**{section.title()}**\n" + "\n".join([f"• {s}" for s in structures])

    def _generate_closing(self, is_follow_up: bool, field: str) -> str:
        return (
            f"추가적인 {field} 관련 질문이 있으시다면 언제든 물어보세요. 🌟"
            if is_follow_up
            else f"더 자세한 {field} 관련 상담이 필요하시면 말씀해 주세요. ✨"
        )
