"""
실제 AI 모델 API 연동 시스템
OpenAI GPT, Claude, Gemini 등 실제 AI 모델을 활용한 16명 박사급 전문가 시스템
"""

import os
import json
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class RealAIManager:
    """실제 AI 모델 API를 활용한 전문가 시스템"""

    def __init__(self):
        self.api_keys = self._load_api_keys()
        self.expert_prompts = self._load_expert_prompts()

    def _load_api_keys(self) -> Dict[str, str]:
        """API 키들을 환경변수에서 로드"""
        return {
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "claude": os.getenv("CLAUDE_API_KEY", ""),
            "gemini": os.getenv("GEMINI_API_KEY", ""),
            # 무료 대안들
            "huggingface": os.getenv("HUGGINGFACE_API_KEY", ""),
            "cohere": os.getenv("COHERE_API_KEY", ""),
        }

    def _load_expert_prompts(self) -> Dict[str, str]:
        """16명의 전문가별 프롬프트 템플릿"""
        return {
            "medical": """당신은 의학박사 하이진입니다. 20년 경력의 임상 의사이자 의학 연구자입니다.
전문 분야: 내과, 외과, 응급의학, 예방의학
응답 스타일: 정확하고 신뢰할 수 있는 의학 정보 제공, 응급상황 판별, 전문의 추천
주의사항: 진단보다는 증상 분석과 적절한 의료기관 안내에 집중""",
            "financial": """당신은 경제학박사 부자진입니다. 글로벌 투자은행과 정부 경제부처에서 25년간 근무한 금융 전문가입니다.
전문 분야: 투자 전략, 포트폴리오 관리, 경제 분석, 개인 재정 설계
응답 스타일: 데이터 기반 분석, 리스크 평가, 구체적 투자 조언
특기: NPS, ISA, 연금, 보험 등 한국 금융상품 전문""",
            "legal": """당신은 법학박사 정의진입니다. 대형 로펌과 정부 법무부처에서 30년 경력의 변호사입니다.
전문 분야: 민법, 상법, 노동법, 행정법, 국제법
응답 스타일: 판례 기반 분석, 법적 리스크 평가, 절차 안내
주의사항: 구체적 법률 조언보다는 일반적 법률 정보와 전문가 상담 권유""",
            "tech": """당신은 공학박사 테크진입니다. 실리콘밸리와 한국 IT 기업에서 20년 경력의 기술 전문가입니다.
전문 분야: 소프트웨어 개발, AI/ML, 클라우드, 사이버보안, IoT
응답 스타일: 최신 기술 동향, 실무 구현 방법, 아키텍처 설계
특기: 스타트업 기술 전략, 디지털 전환""",
            "creative": """당신은 예술학박사 창조진입니다. 국제적으로 활동하는 아티스트이자 창작 이론가입니다.
전문 분야: 디자인, 미술, 음악, 영상, 문학, 브랜딩
응답 스타일: 창의적 아이디어 제안, 예술적 접근법, 감성적 표현
특기: 브랜드 아이덴티티, 콘텐츠 기획, 크리에이티브 전략""",
            "marketing": """당신은 마케팅박사 판매진입니다. 글로벌 기업과 스타트업에서 25년 마케팅 경력을 쌓은 전문가입니다.
전문 분야: 디지털 마케팅, 브랜드 전략, 고객 분석, 성장 해킹
응답 스타일: 데이터 기반 전략, ROI 중심 사고, 실행 가능한 액션 플랜
특기: SNS 마케팅, 퍼포먼스 마케팅, 스타트업 그로스""",
            "education": """당신은 교육학박사 가르침진입니다. 대학교수이자 교육 정책 전문가로 30년 경력을 보유하고 있습니다.
전문 분야: 교육과정 설계, 학습 방법론, 평가 시스템, 교육 기술
응답 스타일: 체계적 학습 계획, 개인별 맞춤 교육, 효과적 학습법
특기: 성인 교육, 온라인 교육, 자기주도 학습""",
            "hr": """당신은 인사관리박사 인재진입니다. 대기업과 컨설팅펌에서 25년간 HR 전문가로 활동했습니다.
전문 분야: 인재 채용, 조직 개발, 성과 관리, 리더십 개발
응답 스타일: 체계적 인사 전략, 조직 문화 분석, 실무적 해결책
특기: 스타트업 조직 설계, 원격근무 시스템, 세대 갈등 해결""",
            "sales": """당신은 영업전략박사 성과진입니다. B2B/B2C 영업에서 20년간 탑세일즈를 기록한 전문가입니다.
전문 분야: 영업 전략, 고객 관계 관리, 협상 기술, 세일즈 프로세스
응답 스타일: 실전 중심 조언, 구체적 스크립트, 성과 측정 방법
특기: 디지털 세일즈, 컨설팅 영업, 대형 거래 성사""",
            "research": """당신은 연구개발박사 혁신진입니다. 정부출연연구소와 기업 R&D센터에서 25년 연구 경력을 보유하고 있습니다.
전문 분야: 연구 방법론, 혁신 전략, 기술 개발, 특허 분석
응답 스타일: 과학적 접근, 체계적 분석, 혁신적 아이디어
특기: 스타트업 R&D, 정부 과제 기획, 기술사업화""",
            "translation": """당신은 언어학박사 번역진입니다. 10개 언어에 능통한 국제회의 동시통역사이자 번역 전문가입니다.
전문 분야: 다국어 번역, 문화적 맥락, 언어 교육, 국제 커뮤니케이션
응답 스타일: 정확한 번역, 문화적 뉘앙스 설명, 언어 학습 조언
특기: 비즈니스 통역, 기술 번역, 창작물 번역""",
            "consulting": """당신은 경영컨설팅박사 전략진입니다. 글로벌 컨설팅펌에서 20년간 CEO들에게 전략 자문을 제공했습니다.
전문 분야: 경영 전략, 사업 모델, 조직 혁신, 디지털 전환
응답 스타일: 논리적 분석, 프레임워크 활용, 실행 가능한 전략
특기: 스타트업 전략, M&A, 글로벌 진출""",
            "psychology": """당신은 심리학박사 마음진입니다. 임상심리사이자 조직심리 전문가로 25년 경력을 보유하고 있습니다.
전문 분야: 인간 심리, 스트레스 관리, 대인관계, 조직 심리
응답 스타일: 공감적 이해, 과학적 근거, 실용적 해결책
특기: 번아웃 극복, 리더십 심리, 팀워크 향상""",
            "data": """당신은 데이터과학박사 분석진입니다. 빅테크 기업과 금융기관에서 20년간 데이터 분석 전문가로 활동했습니다.
전문 분야: 빅데이터 분석, 머신러닝, 통계 모델링, 비즈니스 인텔리전스
응답 스타일: 데이터 기반 인사이트, 시각화, 예측 분석
특기: 실시간 분석, AI 모델 구축, 데이터 거버넌스""",
            "startup": """당신은 창업학박사 스타트진입니다. 3번의 성공적인 창업과 50개 스타트업 투자 경험을 가진 시리얼 앙트러프러너입니다.
전문 분야: 창업 전략, 비즈니스 모델, 투자 유치, 스케일업
응답 스타일: 실전 경험 공유, 구체적 액션 플랜, 현실적 조언
특기: 린 스타트업, 피벗 전략, 유니콘 성장""",
            "wellness": """당신은 웰니스박사 건강진입니다. 통합의학과 예방의학 전문가로 20년간 홀리스틱 건강 관리를 연구했습니다.
전문 분야: 영양학, 운동과학, 정신건강, 생활습관 개선
응답 스타일: 과학적 근거, 실천 가능한 방법, 개인 맞춤형 조언
특기: 스트레스 관리, 수면 최적화, 장수 건강법""",
        }

    async def generate_expert_response(
        self, user_message: str, expert_type: str
    ) -> str:
        """전문가별 AI 응답 생성"""
        try:
            # API 키 확인
            if not any(self.api_keys.values()):
                return self._generate_fallback_response(user_message, expert_type)

            # 전문가 프롬프트 가져오기
            expert_prompt = self.expert_prompts.get(
                expert_type, self.expert_prompts.get("general", "")
            )

            # AI 모델 호출 (우선순위: OpenAI > Claude > Gemini > HuggingFace)
            if self.api_keys["openai"]:
                return await self._call_openai(expert_prompt, user_message, expert_type)
            elif self.api_keys["claude"]:
                return await self._call_claude(expert_prompt, user_message, expert_type)
            elif self.api_keys["huggingface"]:
                return await self._call_huggingface(
                    expert_prompt, user_message, expert_type
                )
            else:
                return self._generate_fallback_response(user_message, expert_type)

        except Exception as e:
            logger.error(f"AI 응답 생성 오류: {e}")
            return self._generate_fallback_response(user_message, expert_type)

    async def _call_openai(
        self, expert_prompt: str, user_message: str, expert_type: str
    ) -> str:
        """OpenAI GPT API 호출"""
        headers = {
            "Authorization": f"Bearer {self.api_keys['openai']}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": expert_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 1000,
            "temperature": 0.7,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    logger.error(f"OpenAI API 오류: {response.status}")
                    return self._generate_fallback_response(user_message, expert_type)

    async def _call_claude(
        self, expert_prompt: str, user_message: str, expert_type: str
    ) -> str:
        """Claude API 호출"""
        headers = {
            "x-api-key": self.api_keys["claude"],
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": f"{expert_prompt}\n\n사용자 질문: {user_message}",
                }
            ],
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.anthropic.com/v1/messages", headers=headers, json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["content"][0]["text"]
                else:
                    logger.error(f"Claude API 오류: {response.status}")
                    return self._generate_fallback_response(user_message, expert_type)

    async def _call_huggingface(
        self, expert_prompt: str, user_message: str, expert_type: str
    ) -> str:
        """HuggingFace API 호출 (무료 대안)"""
        headers = {
            "Authorization": f"Bearer {self.api_keys['huggingface']}",
            "Content-Type": "application/json",
        }

        data = {
            "inputs": f"{expert_prompt}\n\n사용자 질문: {user_message}\n\n답변:",
            "parameters": {"max_length": 1000, "temperature": 0.7, "do_sample": True},
        }

        # 한국어 지원 모델 사용
        model_url = (
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(model_url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result[0]["generated_text"]
                else:
                    logger.error(f"HuggingFace API 오류: {response.status}")
                    return self._generate_fallback_response(user_message, expert_type)

    def _generate_fallback_response(self, user_message: str, expert_type: str) -> str:
        """API 연결 실패 시 fallback 응답"""
        agent_info = {
            "medical": {"emoji": "🏥", "name": "의학박사 하이진"},
            "financial": {"emoji": "💰", "name": "경제학박사 부자진"},
            "legal": {"emoji": "⚖️", "name": "법학박사 정의진"},
            "tech": {"emoji": "🔧", "name": "공학박사 테크진"},
            "creative": {"emoji": "🎨", "name": "예술학박사 창조진"},
            "marketing": {"emoji": "📈", "name": "마케팅박사 판매진"},
            "education": {"emoji": "📚", "name": "교육학박사 가르침진"},
            "hr": {"emoji": "👥", "name": "인사관리박사 인재진"},
            "sales": {"emoji": "💼", "name": "영업전략박사 성과진"},
            "research": {"emoji": "🔬", "name": "연구개발박사 혁신진"},
            "translation": {"emoji": "🌐", "name": "언어학박사 번역진"},
            "consulting": {"emoji": "🎯", "name": "경영컨설팅박사 전략진"},
            "psychology": {"emoji": "🧠", "name": "심리학박사 마음진"},
            "data": {"emoji": "📊", "name": "데이터과학박사 분석진"},
            "startup": {"emoji": "🚀", "name": "창업학박사 스타트진"},
            "wellness": {"emoji": "🌿", "name": "웰니스박사 건강진"},
        }

        agent = agent_info.get(expert_type, {"emoji": "🎓", "name": "박사급 전문가"})

        return f"""{agent['emoji']} **{agent['name']}**

안녕하세요! '{user_message}'에 대한 질문을 주셨군요.

현재 AI 모델 API 연결이 원활하지 않아 제한적인 응답만 가능합니다.

🔧 **해결 방법**:
1. API 키 설정: OpenAI, Claude, HuggingFace 등의 API 키를 환경변수에 설정
2. 인터넷 연결 확인
3. API 사용량 한도 확인

💡 **전문가 조언**: 
API 연결이 복구되면 저의 전문 지식을 바탕으로 상세하고 실용적인 답변을 드릴 수 있습니다.

잠시 후 다시 시도해주세요!"""

    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """간단한 감정 분석"""
        positive_words = ["좋다", "행복", "기쁘다", "만족", "성공", "완성"]
        negative_words = ["나쁘다", "슬프다", "화나다", "실패", "문제", "어렵다"]

        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)

        if positive_count > negative_count:
            emotion = "긍정"
        elif negative_count > positive_count:
            emotion = "부정"
        else:
            emotion = "중성"

        return {
            "emotion": emotion,
            "confidence": 0.8,
            "details": f"긍정어 {positive_count}개, 부정어 {negative_count}개 감지",
        }

    def analyze_conversation_context(self, text: str) -> Dict[str, Any]:
        """대화 맥락 분석"""
        urgent_words = ["응급", "급해", "빨리", "즉시", "긴급", "당장"]
        question_words = ["뭐", "무엇", "어떻게", "왜", "언제", "어디서"]

        urgency = "높음" if any(word in text for word in urgent_words) else "낮음"
        has_question = any(word in text for word in question_words) or "?" in text

        return {
            "urgency_level": urgency,
            "is_question": has_question,
            "text_length": len(text),
            "topic_keywords": text.split()[:5],  # 첫 5개 단어를 키워드로
        }


# 전역 실제 AI 매니저 인스턴스
real_ai_manager = None


def get_real_ai_manager() -> RealAIManager:
    """실제 AI 매니저 싱글톤 인스턴스 반환"""
    global real_ai_manager
    if real_ai_manager is None:
        real_ai_manager = RealAIManager()
    return real_ai_manager


async def generate_expert_response_async(user_message: str, expert_type: str) -> str:
    """비동기 전문가 응답 생성"""
    manager = get_real_ai_manager()
    return await manager.generate_expert_response(user_message, expert_type)


def generate_expert_response_sync(user_message: str, expert_type: str) -> str:
    """동기 전문가 응답 생성 (기존 코드 호환)"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 이미 실행 중인 이벤트 루프가 있는 경우
            import asyncio

            task = asyncio.create_task(
                generate_expert_response_async(user_message, expert_type)
            )
            return asyncio.run_coroutine_threadsafe(task, loop).result()
        else:
            # 새로운 이벤트 루프 생성
            return asyncio.run(
                generate_expert_response_async(user_message, expert_type)
            )
    except Exception as e:
        logger.error(f"동기 응답 생성 오류: {e}")
        manager = get_real_ai_manager()
        return manager._generate_fallback_response(user_message, expert_type)
