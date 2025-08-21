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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel


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

            info = info_map[agent_type].copy()  # 복사본 생성
            info["type"] = agent_type  # agent_type을 info에 추가

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
            "data_analyst": {
                "role": "데이터 기반 인사이트 분석 전문가",
                "style": "통계적이고 논리적인 분석",
                "expertise": ["데이터분석", "통계", "머신러닝", "비즈니스인텔리전스"],
            },
            "creative": {
                "role": "창의적 아이디어 및 디자인 전문가",
                "style": "혁신적이고 창의적인 제안",
                "expertise": ["브레인스토밍", "디자인씽킹", "창의성", "혁신"],
            },
            "hr": {
                "role": "인사 관리 및 조직 문화 전문가",
                "style": "인간 중심적이고 체계적인 접근",
                "expertise": ["인사관리", "조직문화", "채용", "교육훈련"],
            },
            "marketing": {
                "role": "마케팅 전략 및 브랜딩 전문가",
                "style": "전략적이고 창의적인 마케팅",
                "expertise": ["마케팅전략", "브랜딩", "고객분석", "캠페인"],
            },
            "sales": {
                "role": "영업 전략 및 고객 관계 전문가",
                "style": "설득력 있고 고객 중심적",
                "expertise": ["영업전략", "고객관리", "협상", "세일즈"],
            },
            "builder": {
                "role": "시스템 개발 및 구축 전문가",
                "style": "기술적이고 실용적인 솔루션",
                "expertise": ["프로그래밍", "시스템설계", "개발", "기술컨설팅"],
            },
            "counselor": {
                "role": "심리 상담 및 멘탈 케어 전문가",
                "style": "공감적이고 치유적인 접근",
                "expertise": ["심리상담", "멘탈헬스", "치료", "코칭"],
            },
            "fortune": {
                "role": "운세 및 점술 전문가",
                "style": "신비롭고 직관적인 해석",
                "expertise": ["운세", "타로", "명리학", "점술"],
            },
            "growth": {
                "role": "성장 전략 및 발전 전문가",
                "style": "미래 지향적이고 전략적",
                "expertise": ["성장전략", "사업확장", "혁신", "발전계획"],
            },
            "seo": {
                "role": "SEO 및 디지털 마케팅 전문가",
                "style": "데이터 기반 최적화",
                "expertise": ["SEO", "검색엔진", "디지털마케팅", "웹최적화"],
            },
            "shopping": {
                "role": "쇼핑몰 및 커머스 전문가",
                "style": "고객 경험 중심적",
                "expertise": ["이커머스", "쇼핑몰운영", "온라인판매", "고객경험"],
            },
            "startup": {
                "role": "스타트업 창업 및 사업 기획 전문가",
                "style": "혁신적이고 실행 중심적",
                "expertise": ["창업", "사업계획", "투자유치", "스타트업"],
            },
            "medical": {
                "role": "의료 및 건강 관리 전문가",
                "style": "과학적이고 신중한 조언",
                "expertise": ["의료", "건강관리", "예방의학", "의료상담"],
            },
            "village_chief": {
                "role": "리더십 및 조직 관리 전문가",
                "style": "리더십 있고 책임감 있는",
                "expertise": ["리더십", "조직관리", "의사결정", "팀빌딩"],
            },
            "writing": {
                "role": "글쓰기 및 콘텐츠 제작 전문가",
                "style": "창작적이고 표현력 풍부한",
                "expertise": ["글쓰기", "콘텐츠제작", "편집", "스토리텔링"],
            },
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
            expertise in question_lower
            for expertise in personality.get("expertise", [])
        ):
            return self._generate_expert_response(question, info, personality)
        return self._generate_general_expert_response(question, info, personality)

    def _generate_expert_response(
        self, question: str, info: dict, personality: dict
    ) -> str:
        """실제 도깨비 파일을 호출하여 전문 응답 생성 (자연스러운 대화 엔진 적용)"""
        try:
            # 자연스러운 대화 엔진 임포트
            from natural_conversation_engine import get_natural_response

            # 에이전트 타입에 따라 실제 도깨비 파일 호출
            agent_type = info.get("type", "assistant")

            # 자연스러운 대화 엔진으로 응답 생성
            try:
                return get_natural_response(question, agent_type, info)
            except Exception as e:
                print(f"자연스러운 대화 엔진 실패: {e}")
                # 백업 응답 시스템
                return self._generate_backup_friendly_response(
                    question, agent_type, info
                )

        except Exception as e:
            print(f"도깨비 호출 실패 ({agent_type}): {e}")
            return self._generate_backup_friendly_response(question, agent_type, info)

    def _generate_backup_friendly_response(
        self, question: str, agent_type: str, info: dict
    ) -> str:
        """백업용 친근한 응답 생성"""
        agent_name = info.get("name", f"{agent_type} 도깨비")
        agent_emoji = info.get("emoji", "🤖")
        field = info.get("field", "전문 분야")

        # 친근한 인사말
        friendly_greetings = [
            f"안녕하세요! {agent_emoji} {agent_name}이에요! 😊",
            f"반가워요! {agent_emoji} {agent_name}입니다! 🤗",
            f"어서오세요! {agent_emoji} {agent_name}이에요! ✨",
        ]

        greeting = random.choice(friendly_greetings)

        # 질문에 대한 공감적 반응
        empathy_responses = [
            "정말 좋은 질문이네요!",
            "흥미로운 주제를 말씀해주셨어요!",
            "저도 그런 것들이 정말 궁금해요!",
            "와, 멋진 질문이에요!",
        ]

        empathy = random.choice(empathy_responses)

        # 전문성 + 친근함
        expertise_part = (
            f"{field} 전문가로서 도움드릴 수 있는 부분이 정말 많을 것 같아요."
        )

        # 대화 유도
        conversation_starters = [
            "어떤 부분이 가장 궁금하신가요?",
            "구체적으로 어떤 상황인지 더 들려주세요!",
            "어떤 결과를 기대하고 계신가요?",
            "제가 어떻게 도와드릴까요?",
        ]

        starter = random.choice(conversation_starters)

        return (
            f"{greeting}\n\n{empathy} {expertise_part}\n\n{starter} 편하게 대화해요! 💫"
        )

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
            "assistant": {
                "emoji": "🤖",
                "name": "박사급 비서 도깨비",
                "field": "업무 관리",
            },
            "data_analyst": {
                "emoji": "📊",
                "name": "박사급 데이터 분석 도깨비",
                "field": "빅데이터 분석",
            },
            "creative": {
                "emoji": "🎨",
                "name": "박사급 창의 도깨비",
                "field": "창의적 아이디어",
            },
            "hr": {
                "emoji": "👥",
                "name": "박사급 인사 도깨비",
                "field": "인사 관리",
            },
            "marketing": {
                "emoji": "📈",
                "name": "박사급 마케팅 도깨비",
                "field": "마케팅 전략",
            },
            "sales": {
                "emoji": "💼",
                "name": "박사급 영업 도깨비",
                "field": "영업 전략",
            },
            "builder": {
                "emoji": "🏗️",
                "name": "박사급 개발 도깨비",
                "field": "시스템 개발",
            },
            "counselor": {
                "emoji": "💝",
                "name": "박사급 상담 도깨비",
                "field": "심리 상담",
            },
            "fortune": {
                "emoji": "🔮",
                "name": "박사급 운세 도깨비",
                "field": "운세 점술",
            },
            "growth": {
                "emoji": "📈",
                "name": "박사급 성장 도깨비",
                "field": "성장 전략",
            },
            "seo": {
                "emoji": "🔍",
                "name": "박사급 SEO 도깨비",
                "field": "SEO 최적화",
            },
            "shopping": {
                "emoji": "🛒",
                "name": "박사급 쇼핑 도깨비",
                "field": "쇼핑몰 운영",
            },
            "startup": {
                "emoji": "🚀",
                "name": "박사급 스타트업 도깨비",
                "field": "창업 컨설팅",
            },
            "medical": {
                "emoji": "⚕️",
                "name": "박사급 의료 도깨비",
                "field": "의료 상담",
            },
            "village_chief": {
                "emoji": "👑",
                "name": "박사급 촌장 도깨비",
                "field": "리더십 관리",
            },
            "writing": {
                "emoji": "✍️",
                "name": "박사급 글쓰기 도깨비",
                "field": "콘텐츠 제작",
            },
        }
        return {
            "total_agents": len(agent_info),
            "agents": agent_info,
            "categories": {
                "업무&관리": ["assistant", "hr", "village_chief", "growth"],
                "비즈니스": ["marketing", "sales", "startup", "seo"],
                "창작&개발": ["creative", "builder", "writing", "shopping"],
                "상담&서비스": ["counselor", "fortune", "data_analyst", "medical"],
            },
        }


# 전역 인스턴스
stem_ai = STEMIntegration()

# FastAPI 앱 생성
app = FastAPI(
    title="🏰 도깨비마을장터 AI 상담소",
    description="16개 전문 도깨비들의 박사급 상담 서비스",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (CSS, JS, 이미지 등)
app.mount("/static", StaticFiles(directory="."), name="static")


# 요청 모델
class ChatRequest(BaseModel):
    message: str
    agent_type: str


class ChatResponse(BaseModel):
    response: str
    agent_name: str
    agent_emoji: str


@app.get("/")
async def root():
    """홈페이지"""
    return FileResponse("index.html")


@app.get("/index.html")
async def index():
    """메인 페이지"""
    return FileResponse("index.html")


@app.get("/agents")
async def get_agents():
    """사용 가능한 에이전트 목록 조회"""
    return stem_ai.get_agent_info()


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """도깨비와 대화하기"""
    try:
        # 도깨비와 대화 (임시 IP 사용)
        result = stem_ai.process_question(
            agent_type=request.agent_type, question=request.message, user_ip="127.0.0.1"
        )

        # 에이전트 정보 가져오기
        agent_info = stem_ai.get_agent_info()
        agent_data = agent_info["agents"].get(request.agent_type, {})

        return ChatResponse(
            response=result.get("response", "죄송합니다. 응답을 생성할 수 없습니다."),
            agent_name=agent_data.get("name", f"{request.agent_type} 도깨비"),
            agent_emoji=agent_data.get("emoji", "🤖"),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"도깨비와 대화 중 오류가 발생했습니다: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
