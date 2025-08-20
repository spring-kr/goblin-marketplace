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

        # 맥락 분석
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

        # 응답 구조 설정
        if context_patterns["depth_required"]:
            sections = ["insight", "approach", "advice"]
        elif context_patterns["action_required"]:
            sections = ["insight", "approach"]
        else:
            sections = ["insight", "advice"]

        # 응답 생성
        response_parts = []

        # 인사말 생성
        greeting = self._generate_greeting(agent_info["name"], context.current_time)
        response_parts.append(greeting)

        # 전문성 기반 분석
        expertise_analysis = self._analyze_with_expertise(
            question, agent_info["expertise"], context.depth_level
        )
        response_parts.append(expertise_analysis)

        # 섹션별 응답 생성
        for section in sections:
            section_content = self._generate_section_content(
                section, question, agent_info, context
            )
            response_parts.append(section_content)

        # 맺음말 생성
        closing = self._generate_closing(
            context_patterns["follow_up"], agent_info["field"]
        )
        response_parts.append(closing)

        return "\n\n".join(response_parts)

    def _generate_greeting(self, agent_name: str, current_time: datetime) -> str:
        """시간과 상황에 맞는 인사말 생성"""
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
        """전문성 영역을 기반으로 한 분석"""
        relevant_areas = []

        # 질문과 관련된 전문 영역 파악
        for area in expertise_areas:
            if any(keyword in question.lower() for keyword in area.lower().split()):
                relevant_areas.append(area)

        if not relevant_areas:
            relevant_areas = [expertise_areas[0]]  # 기본 전문 영역

        analysis_depth = "심층적인" if depth_level > 1 else "기본적인"

        return f"귀하의 질문에 대해 {', '.join(relevant_areas)}의 관점에서 {analysis_depth} 분석을 진행했습니다."

    def _generate_section_content(
        self, section: str, question: str, agent_info: dict, context: ContextInfo
    ) -> str:
        """섹션별 맥락화된 컨텐츠 생성"""
        structures = self.default_structures[section]
        content_parts = []

        for structure in structures:
            # 실제 구현에서는 여기에 각 도깨비의 전문성을 반영한
            # 구체적인 내용 생성 로직이 들어갈 것입니다.
            content_parts.append(f"• {structure}")

        return f"**{section.title()}**\n" + "\n".join(content_parts)

    def _generate_closing(self, is_follow_up: bool, field: str) -> str:
        """맥락에 맞는 맺음말 생성"""
        if is_follow_up:
            return f"추가적인 {field} 관련 질문이 있으시다면 언제든 물어보세요. 🌟"
        else:
            return f"더 자세한 {field} 관련 상담이 필요하시다면 말씀해 주세요. ✨"
