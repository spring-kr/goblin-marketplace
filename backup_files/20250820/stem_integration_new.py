"""
🎯 AI 도깨비마을 STEM 센터 - 실제 AI 대화 시스템
진짜 AI처럼 자연스럽고 맥락적인 응답을 제공하는 16개 도깨비 시스템
"""

import random
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
import json
import os


class STEMIntegration:
    """STEM 도깨비들과의 실제 AI 대화 시스템"""

    def __init__(self):
        self.system_name = "🏰 도깨비마을장터 박사급 AI 상담소"
        # 대화 기록 저장을 위한 딕셔너리 (간단한 메모리 저장)
        self.conversation_history = {}
        self.context_file = "conversation_context.json"
        self._load_conversation_history()

    def _load_conversation_history(self):
        """대화 기록 로드"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, "r", encoding="utf-8") as f:
                    self.conversation_history = json.load(f)
        except Exception:
            self.conversation_history = {}

    def _save_conversation_history(self):
        """대화 기록 저장"""
        try:
            with open(self.context_file, "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _get_conversation_key(self, user_ip: str, agent_type: str) -> str:
        """사용자-에이전트별 대화 키 생성"""
        key = f"{user_ip}_{agent_type}"
        return hashlib.md5(key.encode()).hexdigest()[:16]

    def _analyze_follow_up_intent(self, question: str, previous_topics: list) -> dict:
        """후속 질문 의도 분석 - 간단 규칙 기반"""
        q = (question or "").strip().lower()

        indicators = {
            "more_detail": ["구체적으로", "더 자세히", "세부", "상세"],
            "example": ["예시", "사례", "예를 들어"],
            "how_to": ["어떻게", "방법", "단계", "절차"],
            "advanced": ["고급", "심화", "전문", "더 깊이"],
            "practical": ["실무", "현실적", "바로", "실행"],
        }

        intent = "general"
        for k, words in indicators.items():
            if any(w in q for w in words):
                intent = k
                break

        # 간단한 follow-up 신호
        follow_signals = [
            "다시",
            "이어",
            "추가",
            "더",
            "계속",
            "앞에서",
            "방금",
            "위 내용",
        ]
        is_follow_up = False
        if previous_topics:
            recent_topics = [
                t.lower() for t in previous_topics[-3:] if isinstance(t, str)
            ]
            if any(sig in q for sig in follow_signals) or any(
                t and t in q for t in recent_topics
            ):
                is_follow_up = True

        depth_level = 1 + min(2, len(previous_topics)) if is_follow_up else 1

        return {
            "is_follow_up": is_follow_up,
            "intent": intent,
            "depth_level": depth_level,
        }

    def process_question(
        self, agent_type: str, question: str, user_ip: str
    ) -> Dict[str, Any]:
        """사용자 질문 처리 (동적 응답)"""
        try:
            try:
                from usage_tracker import usage_tracker  # 지표 기록
            except Exception:
                usage_tracker = None

            info_map = self.get_agent_info().get("agents", {})
            if agent_type not in info_map:
                if usage_tracker:
                    usage_tracker.log_usage(agent_type, question, False, user_ip)
                return {
                    "success": False,
                    "error": f"지원하지 않는 에이전트 타입: {agent_type}",
                }

            if not question or len(question.strip()) < 2:
                if usage_tracker:
                    usage_tracker.log_usage(agent_type, question, False, user_ip)
                return {
                    "success": False,
                    "error": "질문이 너무 짧습니다. 최소 2글자 이상 입력해주세요.",
                }

            conversation_key = self._get_conversation_key(user_ip, agent_type)
            previous_conversations = self.conversation_history.get(conversation_key, [])
            previous_topics = [c.get("topic", "") for c in previous_conversations]

            follow_up = self._analyze_follow_up_intent(question, previous_topics)

            info = info_map[agent_type]
            if follow_up.get("is_follow_up"):
                response = self._create_follow_up_response(
                    question, agent_type, info, previous_conversations, follow_up
                )
            else:
                response = self._create_natural_ai_response(question, agent_type, info)

            # 대화 로그 업데이트
            current = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "topic": self._extract_topic(question),
                "intent": follow_up.get("intent", "general"),
                "depth": follow_up.get("depth_level", 1),
            }
            self.conversation_history.setdefault(conversation_key, []).append(current)
            if len(self.conversation_history[conversation_key]) > 10:
                self.conversation_history[conversation_key] = self.conversation_history[
                    conversation_key
                ][-10:]
            self._save_conversation_history()

            if usage_tracker:
                usage_tracker.log_usage(agent_type, question, True, user_ip)

            return {
                "success": True,
                "agent": {
                    "type": agent_type,
                    "name": info["name"],
                    "emoji": info["emoji"],
                    "field": info["field"],
                },
                "response": response,
                "context": {
                    "previous_topics": previous_topics[-3:],
                    "intent": current["intent"],
                    "depth": current["depth"],
                },
            }
        except Exception as e:
            try:
                from usage_tracker import usage_tracker

                usage_tracker.log_usage(agent_type, question, False, user_ip)
            except Exception:
                pass
            return {"success": False, "error": f"처리 중 오류가 발생했습니다: {str(e)}"}

    def _create_follow_up_response(
        self,
        question: str,
        agent_type: str,
        info: dict,
        previous_conversations: list,
        follow_up_analysis: dict,
    ) -> str:
        """후속 질문 심화 응답 - 컨텍스트 매니저 사용"""
        from response_context_manager import ResponseContextManager, ContextInfo

        previous_topics = [
            conv.get("topic", "") for conv in previous_conversations[-3:]
        ]
        depth = follow_up_analysis.get("depth_level", 2)
        intent = follow_up_analysis.get("intent", "general")

        # expertise_areas 비어있을 경우 field를 기본 전문영역으로 사용 (항상 List[str])
        expertise_areas: list[str] = []
        raw_exp = info.get("expertise")
        if isinstance(raw_exp, list):
            expertise_areas = [str(x) for x in raw_exp if isinstance(x, str)]
        if not expertise_areas:
            expertise_areas = [str(info.get("field", "전문"))]

        context_info = ContextInfo(
            current_time=datetime.now(),
            expertise_areas=expertise_areas,
            depth_level=depth,
            previous_topics=previous_topics,
            conversation_flow={"intent": [intent]},
        )

        manager = ResponseContextManager()
        return manager.create_expertise_based_response(question, info, context_info)

    def _extract_topic(self, question: str) -> str:
        """질문에서 간단한 토픽 추출 (선형 슬라이스)"""
        q = (question or "").strip()
        return q[:30] if len(q) > 30 else q

    def _create_natural_ai_response(
        self, question: str, agent_type: str, info: dict
    ) -> str:
        """실제 AI처럼 자연스럽고 맥락적인 응답 생성"""

        # 도깨비별 전문 분야와 성격 정의
        agent_personalities = {
            "assistant": {
                "role": "효율적이고 체계적인 업무 관리 전문가",
                "style": "실용적이고 구체적인 조언",
                "expertise": ["시간관리", "업무효율", "생산성", "계획수립", "조직관리"],
            },
            # ... (백업 스냅샷)
        }

        personality = agent_personalities.get(
            agent_type,
            {"role": "전문가", "style": "도움이 되는 조언", "expertise": ["전문상담"]},
        )

        # 질문 분석 및 맥락적 응답 생성
        return self._generate_contextual_response(question, info, personality)

    def _generate_contextual_response(
        self, question: str, info: dict, personality: dict
    ) -> str:
        """맥락을 고려한 자연스러운 응답 생성"""
        question_lower = question.lower()
        if any(
            expertise in question_lower for expertise in personality.get("expertise", [])
        ):
            return self._generate_expert_response(question, info, personality)
        return self._generate_general_expert_response(question, info, personality)

    def _generate_expert_response(
        self, question: str, info: dict, personality: dict
    ) -> str:
        from response_context_manager import ResponseContextManager, ContextInfo
        from datetime import datetime

        context_info = ContextInfo(
            current_time=datetime.now(),
            expertise_areas=personality.get("expertise", []),
            depth_level=1,
            previous_topics=[],
            conversation_flow={},
        )
        manager = ResponseContextManager()
        return manager.create_expertise_based_response(question, info, context_info)

    def _generate_general_expert_response(
        self, question: str, info: dict, personality: dict
    ) -> str:
        from response_context_manager import ResponseContextManager, ContextInfo
        from datetime import datetime

        context_info = ContextInfo(
            current_time=datetime.now(),
            expertise_areas=personality.get("expertise", []),
            depth_level=1,
            previous_topics=[],
            conversation_flow={},
        )
        manager = ResponseContextManager()
        return manager.create_expertise_based_response(question, info, context_info)

    def get_agent_info(self) -> Dict[str, Any]:
        agent_info = {
            "assistant": {"emoji": "🤖", "name": "박사급 비서 도깨비", "field": "업무 관리"},
            # ... (백업 스냅샷)
        }
        return {
            "total_agents": len(agent_info),
            "agents": agent_info,
            "categories": {
                "업무&관리": ["assistant", "hr", "village_chief", "growth"],
                # ... (백업 스냅샷)
            },
        }


# 전역 인스턴스
stem_ai = STEMIntegration()
