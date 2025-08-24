# 🚀 Vercel 배포용 경량 AI 시스템
# 대용량 AI 모델 대신 텍스트 기반 간단 응답 시스템 사용

import random
import json
import os


class LightweightAIEngine:
    """Vercel 호환 경량 AI 엔진"""

    def __init__(self):
        self.response_templates = {
            "general": [
                "안녕하세요! 도깨비마을장터에서 도와드리겠습니다.",
                "궁금한 점이 있으시면 언제든 말씀해주세요.",
                "도깨비마을장터의 전문가들이 최선을 다해 도와드리겠습니다.",
            ],
            "technical": [
                "기술적인 문제는 IT기술도깨비가 해결해드리겠습니다.",
                "시스템 관련 질문이시군요. 자세히 알아보겠습니다.",
                "기술 전문가가 분석해드리겠습니다.",
            ],
            "business": [
                "비즈니스 관련 조언을 드리겠습니다.",
                "사업 전략에 대해 상담해드리겠습니다.",
                "마케팅 전문가가 도와드리겠습니다.",
            ],
        }

        self.expert_responses = {
            "인공지능도깨비": "AI 관련 질문에 전문적으로 답변드리겠습니다. 🤖",
            "데이터분석도깨비": "데이터 분석과 인사이트를 제공해드리겠습니다. 📊",
            "마케팅도깨비": "마케팅 전략과 브랜딩에 대해 조언드리겠습니다. 📢",
            "IT기술도깨비": "기술적 해결책을 찾아드리겠습니다. 💻",
            "창업도깨비": "창업과 사업 아이디어에 대해 상담해드리겠습니다. 🚀",
        }

    def generate_response(self, user_input, expert_type="general", expert_name=None):
        """경량 응답 생성"""
        try:
            # 전문가별 특화 응답
            if expert_name and expert_name in self.expert_responses:
                base_response = self.expert_responses[expert_name]
            else:
                # 카테고리별 템플릿 응답
                templates = self.response_templates.get(
                    expert_type, self.response_templates["general"]
                )
                base_response = random.choice(templates)

            # 사용자 입력에 따른 간단한 키워드 매칭
            if any(
                keyword in user_input.lower()
                for keyword in ["안녕", "안녕하세요", "hello"]
            ):
                return f"안녕하세요! {base_response}"
            elif any(
                keyword in user_input.lower() for keyword in ["감사", "고마워", "thank"]
            ):
                return (
                    f"천만에요! {base_response} 더 도움이 필요하시면 언제든 말씀하세요."
                )
            elif any(
                keyword in user_input.lower() for keyword in ["도움", "help", "질문"]
            ):
                return f"{base_response} 구체적으로 어떤 부분을 도와드릴까요?"
            else:
                return f"{base_response} 입력하신 '{user_input[:50]}...'에 대해 더 자세히 설명해드릴게요."

        except Exception as e:
            return "죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요."

    def get_expert_info(self, expert_name):
        """전문가 정보 반환"""
        expert_details = {
            "인공지능도깨비": {
                "specialty": "인공지능, 머신러닝, 데이터 과학",
                "description": "AI 기술과 머신러닝 솔루션 전문가",
                "emoji": "🤖",
            },
            "데이터분석도깨비": {
                "specialty": "데이터 분석, 통계, 비즈니스 인텔리전스",
                "description": "데이터 기반 의사결정 지원 전문가",
                "emoji": "📊",
            },
            "마케팅도깨비": {
                "specialty": "디지털 마케팅, 브랜딩, SNS 마케팅",
                "description": "브랜드 성장과 마케팅 전략 전문가",
                "emoji": "📢",
            },
        }

        return expert_details.get(
            expert_name,
            {
                "specialty": "종합 상담",
                "description": "다양한 분야의 전문 상담",
                "emoji": "🧙‍♂️",
            },
        )


# 전역 인스턴스
lightweight_ai = LightweightAIEngine()


def get_ai_response(user_input, expert_type="general", expert_name=None):
    """간단한 AI 응답 생성 함수"""
    return lightweight_ai.generate_response(user_input, expert_type, expert_name)


def get_expert_capabilities(expert_name):
    """전문가 역량 정보"""
    return lightweight_ai.get_expert_info(expert_name)


# Vercel용 최적화 함수들
def health_check():
    """시스템 상태 확인"""
    return {"status": "healthy", "ai_engine": "lightweight", "version": "1.0"}


def get_available_experts():
    """사용 가능한 전문가 목록"""
    return list(lightweight_ai.expert_responses.keys())
