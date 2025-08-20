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
        """후속 질문 의도 분석"""
        question_lower = question.lower()

        follow_up_indicators = {
            "more_detail": [
                "구체적으로",
                "더 자세히",
                "세부적으로",
                "상세하게",
                "더 알려주세요",
                "자세히 설명",
            ],
            "example": ["예시", "사례", "실제", "예를 들어", "구체적인 예", "실습"],
            "how_to": ["어떻게", "방법", "단계", "절차", "프로세스"],
            "advanced": ["고급", "심화", "전문적", "더 깊이", "고도화"],
            "practical": ["실무", "현실적", "실제로", "바로", "실행"],
            "tools": ["도구", "툴", "프로그램", "소프트웨어", "앱"],
            "troubleshooting": ["문제", "해결", "오류", "안될때", "실패"],
        }

        detected_intent = "general"
        for intent, keywords in follow_up_indicators.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_intent = intent
                break

        return {
            "intent": detected_intent,
            "is_follow_up": len(previous_topics) > 0,
            "depth_level": len(previous_topics) + 1,
        }

    def _get_fortune_response(self, question: str, agent_profile: dict) -> str:
        """운세 도깨비 전용 응답 생성 로직"""
        fortune_types = {
            "연애운": {
                "aspects": ["현재 연애 기운", "미래의 인연", "관계의 발전 방향"],
                "predictions": [
                    "새로운 만남의 기회가 찾아올",
                    "기존 인연이 더욱 깊어질",
                    "잠시 인연을 돌아보며 성찰이 필요할",
                ],
                "advices": [
                    "자신을 더 사랑하고 가꾸는 시간을 가지세요",
                    "상대방의 마음을 더 깊이 이해하려 노력해보세요",
                    "긍정적인 에너지로 새로운 인연을 맞이할 준비를 하세요",
                ],
            },
            "사업운": {
                "aspects": ["사업의 흐름", "투자 시기", "동업 관계"],
                "predictions": [
                    "새로운 기회가 열릴",
                    "안정적인 성장이 예상되는",
                    "신중한 판단이 필요한",
                ],
                "advices": [
                    "철저한 준비로 기회를 놓치지 마세요",
                    "장기적 관점에서 전략을 세워보세요",
                    "신뢰할 수 있는 파트너와 협력하세요",
                ],
            },
        }

        question_lower = question.lower()
        fortune_type = "general"
        for ftype in fortune_types:
            if ftype in question:
                fortune_type = ftype
                break

        if fortune_type in fortune_types:
            data = fortune_types[fortune_type]
            aspect = random.choice(data["aspects"])
            prediction = random.choice(data["predictions"])
            advice = random.choice(data["advices"])

            pattern = agent_profile["response_patterns"].get(
                fortune_type, agent_profile["response_patterns"]["general"]
            )
            return pattern.format(aspect=aspect, prediction=prediction, advice=advice)

        return f"귀하의 운세를 살펴보니, 긍정적인 변화의 기운이 감지됩니다. 이 시기를 잘 활용하시기 바랍니다."

    def process_question(
        self, agent_type: str, question: str, user_ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """실제 AI 대화 능력으로 질문 처리 - 컨텍스트 추적 포함"""
        try:
            from usage_tracker import usage_tracker

            # 사용자 IP가 없으면 기본값 설정
            if not user_ip:
                user_ip = "unknown"

            # 대화 기록 키 생성
            conversation_key = self._get_conversation_key(user_ip, agent_type)

            # 이전 대화 기록 가져오기
            previous_conversations = self.conversation_history.get(conversation_key, [])
            previous_topics = [
                conv.get("topic", "") for conv in previous_conversations[-3:]
            ]  # 최근 3개만

            # 후속 질문 의도 분석
            follow_up_analysis = self._analyze_follow_up_intent(
                question, previous_topics
            )

            # 원래 16개 도깨비 정보
            agent_info = {
                "assistant": {
                    "emoji": "🤖",
                    "name": "박사급 비서 도깨비",
                    "field": "업무 관리",
                },
                "builder": {"emoji": "💻", "name": "빌더 도깨비", "field": "개발"},
                "counselor": {"emoji": "💬", "name": "상담 도깨비", "field": "상담"},
                "creative": {"emoji": "🎨", "name": "창작 도깨비", "field": "창작"},
                "data_analyst": {
                    "emoji": "📊",
                    "name": "데이터분석 도깨비",
                    "field": "데이터 분석",
                },
                "fortune": {"emoji": "🔮", "name": "운세 도깨비", "field": "운세"},
                "growth": {"emoji": "🌱", "name": "성장 도깨비", "field": "성장"},
                "hr": {"emoji": "👥", "name": "HR 도깨비", "field": "인사 관리"},
                "marketing": {
                    "emoji": "📢",
                    "name": "마케팅 도깨비",
                    "field": "마케팅",
                },
                "medical": {"emoji": "🏥", "name": "의료 도깨비", "field": "의료"},
                "sales": {"emoji": "💰", "name": "영업 도깨비", "field": "영업"},
                "seo": {"emoji": "🔍", "name": "SEO 도깨비", "field": "검색 최적화"},
                "shopping": {"emoji": "🛒", "name": "쇼핑 도깨비", "field": "쇼핑"},
                "startup": {
                    "emoji": "🚀",
                    "name": "스타트업 도깨비",
                    "field": "창업전략",
                },
                "village_chief": {
                    "emoji": "👑",
                    "name": "이장 도깨비",
                    "field": "마을 관리",
                },
                "writing": {
                    "emoji": "✍️",
                    "name": "박사급 문서 작성 도깨비",
                    "field": "문서 작성",
                },
            }

            if agent_type not in agent_info:
                # 실패 로그 기록
                usage_tracker.log_usage(agent_type, question, False, user_ip)
                return {
                    "success": False,
                    "error": f"지원하지 않는 에이전트 타입: {agent_type}",
                }

            # 질문 유효성 검사
            if not question or len(question.strip()) < 2:
                usage_tracker.log_usage(agent_type, question, False, user_ip)
                return {
                    "success": False,
                    "error": "질문이 너무 짧습니다. 최소 2글자 이상 입력해주세요.",
                }

            # 도깨비별 전문 응답 생성 (컨텍스트 포함)
            info = agent_info[agent_type]

            # 운세 도깨비인 경우 특별 처리
            if agent_type == "fortune":
                response = self._get_fortune_response(question, info)
            else:
                response = self._create_contextual_ai_response(
                    question,
                    agent_type,
                    info,
                    previous_conversations,
                    follow_up_analysis,
                )

            # 현재 대화를 기록에 추가
            current_conversation = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "topic": self._extract_topic(question),
                "intent": follow_up_analysis["intent"],
                "depth": follow_up_analysis["depth_level"],
            }

            if conversation_key not in self.conversation_history:
                self.conversation_history[conversation_key] = []

            self.conversation_history[conversation_key].append(current_conversation)

            # 최근 10개 대화만 유지
            if len(self.conversation_history[conversation_key]) > 10:
                self.conversation_history[conversation_key] = self.conversation_history[
                    conversation_key
                ][-10:]

            # 대화 기록 저장
            self._save_conversation_history()

            # 성공 로그 기록
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
                "timestamp": datetime.now().isoformat(),
                "context": {
                    "is_follow_up": follow_up_analysis["is_follow_up"],
                    "depth_level": follow_up_analysis["depth_level"],
                    "intent": follow_up_analysis["intent"],
                },
            }

        except Exception as e:
            # 에러 로그 기록
            usage_tracker.log_usage(agent_type, question, False, user_ip)
            return {"success": False, "error": f"처리 중 오류가 발생했습니다: {str(e)}"}

    def _extract_topic(self, question: str) -> str:
        """질문에서 주제 추출"""
        # 간단한 주제 추출 로직
        question_lower = question.lower()

        topic_keywords = {
            "시간관리": ["시간", "일정", "스케줄", "계획"],
            "업무효율": ["효율", "생산성", "업무", "일"],
            "기술": ["개발", "프로그래밍", "코딩", "기술"],
            "마케팅": ["마케팅", "광고", "홍보", "브랜드"],
            "건강": ["건강", "운동", "의료", "병원"],
            "창작": ["창작", "디자인", "글쓰기", "아이디어"],
            "상담": ["상담", "고민", "스트레스", "관계"],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic

        return "일반상담"

    def _create_contextual_ai_response(
        self,
        question: str,
        agent_type: str,
        info: dict,
        previous_conversations: list,
        follow_up_analysis: dict,
    ) -> str:
        """컨텍스트를 고려한 AI 응답 생성"""

        # 후속 질문인지 확인
        if follow_up_analysis["is_follow_up"] and follow_up_analysis["depth_level"] > 1:
            return self._create_follow_up_response(
                question, agent_type, info, previous_conversations, follow_up_analysis
            )
        else:
            return self._create_natural_ai_response(question, agent_type, info)

    def _create_follow_up_response(
        self,
        question: str,
        agent_type: str,
        info: dict,
        previous_conversations: list,
        follow_up_analysis: dict,
    ) -> str:
        """후속 질문에 대한 심화 응답 생성"""

        # 이전 주제들 파악
        previous_topics = [
            conv.get("topic", "") for conv in previous_conversations[-3:]
        ]
        main_topic = previous_topics[-1] if previous_topics else "일반상담"

        intent = follow_up_analysis["intent"]
        depth = follow_up_analysis["depth_level"]

        # 기존 함수들을 활용한 심화 응답
        detailed_solution = self._get_detailed_solution(question, info["field"])
        practical_steps = self._get_practical_steps(question, info["field"])
        expert_tips = self._get_expert_tips(question, info["field"])
        deep_analysis = self._get_deep_analysis(question, info["field"])

        # 의도별 맞춤 응답
        if intent == "more_detail":
            intro = (
                f"{info['emoji']} 더 구체적으로 설명드리겠습니다! ({depth}단계 심화)"
            )
            focus = "🔍 **세부 분석:**"
        elif intent == "example":
            intro = f"{info['emoji']} 실제 사례로 설명드리겠습니다!"
            focus = "📚 **구체적 사례:**"
        elif intent == "how_to":
            intro = f"{info['emoji']} 단계별 방법을 자세히 알려드리겠습니다!"
            focus = "📋 **상세 실행 방법:**"
        elif intent == "practical":
            intro = (
                f"{info['emoji']} 실무에 바로 적용할 수 있는 방법을 알려드리겠습니다!"
            )
            focus = "⚡ **실무 적용법:**"
        elif intent == "advanced":
            intro = f"{info['emoji']} 고급 수준의 내용을 다뤄보겠습니다!"
            focus = "🎓 **전문가 수준:**"
        else:
            intro = f"{info['emoji']} 더 깊이 있게 설명드리겠습니다!"
            focus = "💡 **심화 내용:**"

        return f"""{intro}

이전에 {main_topic}에 대해 기본적인 내용을 말씀드렸는데, 이제 더욱 구체적이고 실용적인 부분을 다뤄보겠습니다.

{focus}
{detailed_solution}

🛠️ **심화 실행 방법:**
{practical_steps}

⭐ **전문가 노하우 (레벨 {depth}):**
{expert_tips}

� **깊이 있는 분석:**
{deep_analysis}

💬 **다음 단계 제안:**
- 더 구체적인 상황을 알려주시면 맞춤형 조언 제공
- 실제 적용 중 어려움이 있으면 문제 해결 방법 안내
- 성과 측정이나 개선 방법에 대한 추가 상담 가능

{info['field']} 전문가로서 {depth}단계 심화 상담을 제공했습니다. 더 궁금한 점이나 구체적인 상황이 있으시면 언제든 말씀해주세요!"""

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
            "builder": {
                "role": "창의적이고 실용적인 개발 전문가",
                "style": "기술적이면서도 이해하기 쉬운 설명",
                "expertise": [
                    "프로그래밍",
                    "웹개발",
                    "앱개발",
                    "시스템설계",
                    "기술아키텍처",
                ],
            },
            "counselor": {
                "role": "따뜻하고 공감능력이 뛰어난 상담 전문가",
                "style": "경청하고 공감하며 따뜻한 조언",
                "expertise": [
                    "심리상담",
                    "갈등해결",
                    "스트레스관리",
                    "인간관계",
                    "감정관리",
                ],
            },
            "creative": {
                "role": "영감이 넘치고 창의적인 아이디어 전문가",
                "style": "독창적이고 흥미로운 아이디어 제시",
                "expertise": ["창작", "디자인", "브랜딩", "콘텐츠기획", "아이디어발상"],
            },
            "data_analyst": {
                "role": "논리적이고 분석적인 데이터 전문가",
                "style": "근거와 데이터를 바탕으로 한 객관적 분석",
                "expertise": [
                    "데이터분석",
                    "통계",
                    "시각화",
                    "예측모델링",
                    "비즈니스인텔리전스",
                ],
            },
            "fortune": {
                "role": "신비롭고 지혜로운 운세 전문가",
                "style": "신비로우면서도 희망적인 메시지",
                "expertise": ["운세", "점성술", "타로", "풍수", "운명해석"],
                "response_patterns": {
                    "연애운": "지금 당신의 {aspect}에 대해 타로카드와 별자리를 함께 살펴보니, {prediction}입니다. {advice}",
                    "사업운": "현재 귀하의 {aspect}을 풍수와 운세로 분석해보니, {prediction}이 보입니다. {advice}",
                    "금전운": "재물과 관련된 {aspect}을 점성술로 살펴보니, {prediction}의 기운이 감지됩니다. {advice}",
                    "건강운": "건강과 관련된 {aspect}을 사주로 확인해보니, {prediction}이 나타납니다. {advice}",
                    "general": "귀하의 {aspect}에 대한 운세를 살펴보니, {prediction}이 보입니다. {advice}",
                },
            },
            "growth": {
                "role": "동기부여가 넘치는 성장 전문가",
                "style": "격려하고 동기부여하는 긍정적 조언",
                "expertise": [
                    "자기계발",
                    "목표설정",
                    "습관형성",
                    "동기부여",
                    "성장전략",
                ],
            },
            "hr": {
                "role": "사람 중심의 인사 관리 전문가",
                "style": "배려 깊고 공정한 인사 관리 조언",
                "expertise": ["채용", "인사평가", "조직문화", "리더십", "팀관리"],
            },
            "marketing": {
                "role": "트렌드에 민감한 마케팅 전문가",
                "style": "창의적이고 실행 가능한 마케팅 전략",
                "expertise": [
                    "브랜드마케팅",
                    "디지털마케팅",
                    "고객분석",
                    "마케팅전략",
                    "광고기획",
                ],
            },
            "medical": {
                "role": "신뢰할 수 있는 의료 정보 전문가",
                "style": "정확하고 신중한 의학 정보 제공",
                "expertise": [
                    "건강관리",
                    "질병예방",
                    "의학정보",
                    "건강검진",
                    "생활습관",
                ],
            },
            "sales": {
                "role": "열정적이고 설득력 있는 영업 전문가",
                "style": "적극적이고 성과지향적인 영업 조언",
                "expertise": ["영업전략", "고객관계", "협상기술", "매출관리", "세일즈"],
            },
            "seo": {
                "role": "검색엔진에 정통한 SEO 전문가",
                "style": "기술적이면서도 실무적인 SEO 조언",
                "expertise": [
                    "검색최적화",
                    "키워드분석",
                    "웹사이트최적화",
                    "구글SEO",
                    "콘텐츠SEO",
                ],
            },
            "shopping": {
                "role": "합리적이고 트렌드에 민감한 쇼핑 전문가",
                "style": "실용적이고 경제적인 구매 조언",
                "expertise": [
                    "제품비교",
                    "가격분석",
                    "쇼핑팁",
                    "소비패턴",
                    "구매가이드",
                ],
            },
            "startup": {
                "role": "도전정신이 강한 창업 전문가",
                "style": "현실적이면서도 꿈을 응원하는 창업 조언",
                "expertise": [
                    "창업전략",
                    "비즈니스모델",
                    "투자유치",
                    "스타트업경영",
                    "사업계획",
                ],
            },
            "village_chief": {
                "role": "경험이 풍부하고 지혜로운 리더",
                "style": "포용력 있고 균형잡힌 종합적 조언",
                "expertise": [
                    "리더십",
                    "조직관리",
                    "갈등조정",
                    "의사결정",
                    "커뮤니티관리",
                ],
            },
            "writing": {
                "role": "문장력이 뛰어난 글쓰기 전문가",
                "style": "명확하고 품격 있는 문서 작성 조언",
                "expertise": [
                    "문서작성",
                    "글쓰기",
                    "논문작성",
                    "보고서",
                    "콘텐츠라이팅",
                ],
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

        # 질문 길이와 복잡도 분석
        question_length = len(question)
        question_lower = question.lower()

        # 인사말 처리
        greetings = ["안녕", "하이", "헬로", "hi", "hello"]
        if (
            any(greeting in question_lower for greeting in greetings)
            and question_length < 20
        ):
            responses = [
                f"{info['emoji']} 안녕하세요! {info['name']}입니다! 어떤 {info['field']} 관련 도움이 필요하신가요?",
                f"{info['emoji']} 반갑습니다! {info['name']}가 인사드려요. {info['field']} 전문가로서 최선을 다해 도와드리겠습니다!",
                f"{info['emoji']} 안녕하세요! {info['field']} 전문가 {info['name']}입니다. 무엇을 도와드릴까요?",
            ]
            return random.choice(responses)

        # 감사 표현 처리
        thanks = ["고마워", "감사", "고맙", "thanks", "thank"]
        if any(thank in question_lower for thank in thanks):
            responses = [
                f"{info['emoji']} 별말씀을요! {info['name']}로서 도움이 되었다니 정말 기쁩니다!",
                f"{info['emoji']} 천만에요! {info['field']} 관련해서 언제든 찾아주세요!",
                f"{info['emoji']} 도움이 되어서 다행이에요! {info['name']}는 항상 여기 있습니다!",
            ]
            return random.choice(responses)

        # 전문 분야 키워드가 포함된 경우
        if any(
            expertise in question_lower
            for expertise in personality.get("expertise", [])
        ):
            return self._generate_expert_response(question, info, personality)

        # 일반적인 질문에 대한 전문가적 관점 제시
        return self._generate_general_expert_response(question, info, personality)

    def _generate_expert_response(
        self, question: str, info: dict, personality: dict
    ) -> str:
        """전문 분야 관련 응답 생성 - 더 길고 구체적인 응답"""

        specific_solution = self._get_detailed_solution(question, info["field"])
        practical_steps = self._get_practical_steps(question, info["field"])
        expert_tips = self._get_expert_tips(question, info["field"])

        return f"""{info['emoji']} {info['name']}입니다!

'{question}'에 대해 {personality['role']}로서 전문적이고 상세한 답변을 드리겠습니다.

🎯 **심층 전문가 분석:**
질문하신 내용은 {info['field']} 분야에서 매우 중요한 주제입니다. {personality['style']}와 함께 실무에서 바로 적용할 수 있는 구체적인 방법론을 제시해드리겠습니다.

💡 **상세 솔루션:**
{specific_solution}

📋 **단계별 실행 방안:**
{practical_steps}

⭐ **전문가 노하우:**
{expert_tips}

🔍 **심화 분석:**
{self._get_deep_analysis(question, info["field"])}

✨ **성공 사례 및 주의사항:**
{self._get_success_cases_and_warnings(info["field"])}

🚀 **다음 단계 로드맵:**
이 조언을 바탕으로 단계적으로 실행해보시고, 진행 과정에서 궁금한 점이나 구체적인 상황에 대한 추가 조언이 필요하시면 언제든 말씀해주세요. {info['field']} 전문가로서 더욱 세밀한 가이드를 제공해드리겠습니다!"""

    def _generate_general_expert_response(
        self, question: str, info: dict, personality: dict
    ) -> str:
        """일반적인 질문에 대한 전문가 관점 응답 - 더 길고 구체적인 응답"""

        field_analysis = self._get_comprehensive_analysis(question, info["field"])
        strategic_approach = self._get_strategic_approach(question, info["field"])
        implementation_guide = self._get_implementation_guide(info["field"])

        return f"""{info['emoji']} {info['name']}입니다!

'{question}'에 대해 {info['field']} 전문가로서 종합적이고 심층적인 관점을 제공해드리겠습니다.

🔍 **전문가 종합 진단:**
{personality['role']}로서 이 문제를 다각도로 분석해보면, {info['field']} 영역에서 고려해야 할 핵심 요소들이 여러 가지 있습니다.

💭 **전략적 접근 방법:**
{strategic_approach}

📊 **세부 분석:**
{field_analysis}

🛠️ **실행 가이드:**
{implementation_guide}

⚡ **즉시 적용 가능한 방법:**
{self._get_immediate_actions(info["field"])}

🎯 **장기적 전략:**
{self._get_long_term_strategy(info["field"])}

📞 **전문 상담 안내:**
{info['field']} 분야의 특성상 개별 상황에 따라 접근 방법이 달라질 수 있습니다. 구체적인 상황이나 추가적인 배경 정보를 알려주시면, {personality['role']}로서 더욱 정밀하고 맞춤형 솔루션을 제공해드릴 수 있습니다. 

언제든 세부적인 질문이나 후속 상담이 필요하시면 {info['name']}를 찾아주세요!"""

    def _get_specific_solution(self, question: str, field: str) -> str:
        """분야별 구체적 솔루션 제공"""

        solutions = {
            "업무 관리": "효율적인 시간 관리와 우선순위 설정을 통해 생산성을 극대화하고, 체계적인 업무 프로세스를 구축하세요.",
            "개발": "문제를 단계별로 분해하고, 적절한 기술 스택을 선택하여 확장 가능한 솔루션을 설계해보세요.",
            "상담": "먼저 감정을 충분히 인정하고 수용한 후, 건설적인 해결 방안을 함께 모색해나가는 것이 중요합니다.",
            "창작": "기존의 틀에서 벗어나 새로운 관점으로 접근하고, 다양한 영감의 원천을 탐색해보세요.",
            "데이터 분석": "데이터의 품질을 먼저 검증하고, 적절한 분석 방법론을 적용하여 의미 있는 인사이트를 도출하세요.",
            "운세": "현재의 에너지 흐름을 이해하고, 긍정적인 마음가짐으로 좋은 기운을 끌어당기세요.",
            "성장": "작은 습관부터 시작하여 꾸준히 실천하고, 단계적으로 목표를 확장해나가세요.",
            "인사 관리": "구성원 개개인의 강점을 파악하고, 공정하고 투명한 시스템을 통해 조직 역량을 극대화하세요.",
            "마케팅": "타겟 고객의 니즈를 정확히 파악하고, 차별화된 가치 제안을 통해 브랜드 경쟁력을 강화하세요.",
            "의료": "정확한 진단과 전문의 상담을 받으시고, 예방 중심의 건강한 생활습관을 유지하세요.",
            "영업": "고객의 입장에서 생각하고, 진정성 있는 관계 구축을 통해 신뢰를 바탕으로 한 영업을 하세요.",
            "검색 최적화": "사용자 의도에 맞는 고품질 콘텐츠를 제작하고, 기술적 SEO를 체계적으로 최적화하세요.",
            "쇼핑": "신중한 비교검토를 통해 가성비를 따져보고, 실제 필요성을 고려한 합리적 소비를 하세요.",
            "창업": "시장 검증을 통해 실제 고객 문제를 해결하는 솔루션을 개발하고, 점진적으로 사업을 확장하세요.",
            "마을 관리": "모든 구성원의 의견을 듣고 조율하여, 공동체 전체의 이익을 고려한 균형잡힌 의사결정을 하세요.",
            "문서 작성": "명확한 구조와 논리적 흐름을 갖추고, 독자의 입장에서 이해하기 쉽게 작성하세요.",
        }

        return solutions.get(
            field,
            "전문적인 관점에서 체계적으로 접근하고, 실행 가능한 방안을 단계별로 수립해보세요.",
        )

    def _get_field_specific_advice(self, question: str, field: str) -> str:
        """분야별 맞춤 조언 제공"""

        advice = {
            "업무 관리": "시간 관리 매트릭스를 활용해 중요도와 긴급도를 분류하고, 집중 시간을 확보하세요.",
            "개발": "MVP(최소 실행 제품)부터 시작해서 사용자 피드백을 받으며 반복 개선해나가세요.",
            "상담": "경청의 자세로 상대방의 마음을 충분히 이해하고, 함께 해결책을 찾아가세요.",
            "창작": "다양한 경험과 관찰을 통해 영감을 축적하고, 실험정신을 갖고 도전해보세요.",
            "데이터 분석": "가설을 세우고 데이터로 검증하는 과정을 반복하여 신뢰할 수 있는 결과를 도출하세요.",
            "운세": "현재에 충실하면서도 미래에 대한 긍정적 비전을 갖고 행동하세요.",
            "성장": "SMART 목표 설정법을 활용해 구체적이고 측정 가능한 목표를 수립하세요.",
            "인사 관리": "정기적인 1:1 면담과 피드백을 통해 구성원과 소통하고 성장을 지원하세요.",
            "마케팅": "고객 여정을 분석하고 각 단계별 최적의 터치포인트를 설계하세요.",
            "의료": "정기 건강검진과 함께 균형잡힌 식단, 규칙적인 운동으로 건강을 관리하세요.",
            "영업": "고객의 니즈를 파악하고 그에 맞는 솔루션을 제시하는 컨설팅 영업을 하세요.",
            "검색 최적화": "키워드 리서치부터 시작해서 콘텐츠 최적화와 기술적 SEO를 병행하세요.",
            "쇼핑": "가격 비교 사이트를 활용하고, 리뷰와 평점을 꼼꼼히 확인한 후 구매하세요.",
            "창업": "린 스타트업 방법론을 적용해 빠른 실험과 학습을 통해 사업 모델을 검증하세요.",
            "마을 관리": "투명한 소통 채널을 구축하고, 정기적인 의견 수렴을 통해 민주적으로 운영하세요.",
            "문서 작성": "5W1H 원칙에 따라 정보를 정리하고, 단락별 핵심 메시지를 명확히 하세요.",
        }

        return advice.get(
            field, "전문 지식을 바탕으로 단계적이고 실용적인 접근 방법을 찾아보세요."
        )

    def _get_detailed_solution(self, question: str, field: str) -> str:
        """분야별 상세 솔루션 제공"""

        detailed_solutions = {
            "업무 관리": """
📊 **시간 관리 체계 구축:**
• 아이젠하워 매트릭스를 활용한 업무 우선순위 분류
• 25분 집중 + 5분 휴식 포모도로 기법 적용
• 일일/주간/월간 목표 설정 및 검토 시스템 구축

⚡ **생산성 극대화 전략:**
• 2분 룰: 2분 내 처리 가능한 업무는 즉시 완료
• 배치 처리: 유사한 업무들을 특정 시간대에 몰아서 처리
• 깊은 작업 시간 확보: 하루 중 가장 집중력이 높은 시간대 활용

🔄 **업무 프로세스 최적화:**
• 반복 업무의 자동화 및 템플릿화
• 업무 위임 및 분산 체계 구축
• 정기적인 업무 프로세스 리뷰 및 개선""",
            "개발": """
🏗️ **아키텍처 설계 원칙:**
• SOLID 원칙을 적용한 확장 가능한 구조 설계
• 마이크로서비스 vs 모놀리식 아키텍처 선택 기준
• API 설계 시 RESTful 원칙 및 GraphQL 고려사항

💻 **개발 방법론:**
• 애자일/스크럼을 통한 반복적 개발 프로세스
• TDD(테스트 주도 개발)로 안정적인 코드 작성
• CI/CD 파이프라인 구축으로 배포 자동화

🔧 **기술 스택 선택:**
• 프로젝트 요구사항에 맞는 최적 기술 조합
• 성능, 확장성, 유지보수성을 고려한 기술 선택
• 팀의 기술 역량과 학습 곡선 고려""",
            "창작": """
🎨 **창작 프로세스:**
• 브레인스토밍 → 아이디어 정리 → 프로토타입 → 피드백 → 개선
• 다양한 창작 기법: 마인드맵, 스토리보드, 무드보드 활용
• 창작 일지 작성으로 아이디어와 영감 기록 관리

💡 **영감 발굴 전략:**
• 다양한 분야의 작품 감상 및 분석
• 일상 관찰과 경험을 통한 소재 발굴
• 타 분야와의 융합을 통한 새로운 관점 창출

🚀 **완성도 향상:**
• 초안 완성 후 충분한 휴지기를 거친 객관적 검토
• 다양한 관점의 피드백 수집 및 반영
• 지속적인 수정과 개선을 통한 품질 향상""",
            "창업전략": """
🚀 **MVP 기반 린 스타트업 전략:**
• 최소기능제품(MVP) 개발로 빠른 시장 검증 - 3개월 내 출시 목표
• 구축-측정-학습 사이클로 2주마다 고객 피드백 반영
• 피벗(Pivot) vs 인내(Persevere) 판단 기준: 핵심지표 3개월 추이 분석

💰 **수익모델 및 단위경제학:**
• LTV(고객생애가치) ÷ CAC(고객획득비용) ≥ 3 달성이 최우선
• 수익모델 다각화: 구독(SaaS), 수수료(플랫폼), 프리미엄(프리미엄)
• 캐시플로우 브레이크이븐 포인트 18개월 내 달성 계획

📊 **시장 검증 및 진입 전략:**
• TAM $10B - SAM $1B - SOM $100M 시장 규모 분석
• 초기 타겟: 1000명의 열성고객(Early Adopter) 확보가 성공의 열쇠
• 네트워크 효과 설계: 사용자 증가가 서비스 가치 향상으로 이어지는 구조

🎯 **투자 유치 및 자금 계획:**
• 시드투자: 제품개발 + 초기팀 구성 (6-12개월 런웨이)
• 시리즈A: 시장 적합성 증명 후 확장 자금 (ARR $1M 달성 후)
• 피치덱 핵심: 문제-솔루션-시장규모-트랙션-팀-재무계획 6요소""",
            "스타트업경영": """
🚀 **MVP 기반 린 스타트업 전략:**
• 최소기능제품(MVP) 개발로 빠른 시장 검증 - 3개월 내 출시 목표
• 구축-측정-학습 사이클로 2주마다 고객 피드백 반영
• 피벗(Pivot) vs 인내(Persevere) 판단 기준: 핵심지표 3개월 추이 분석

💰 **수익모델 및 단위경제학:**
• LTV(고객생애가치) ÷ CAC(고객획득비용) ≥ 3 달성이 최우선
• 수익모델 다각화: 구독(SaaS), 수수료(플랫폼), 프리미엄(프리미엄)
• 캐시플로우 브레이크이븐 포인트 18개월 내 달성 계획

📊 **시장 검증 및 진입 전략:**
• TAM $10B - SAM $1B - SOM $100M 시장 규모 분석
• 초기 타겟: 1000명의 열성고객(Early Adopter) 확보가 성공의 열쇠
• 네트워크 효과 설계: 사용자 증가가 서비스 가치 향상으로 이어지는 구조""",
            "상담": """
💬 **상담 기법 및 이론:**
• 칼 로저스의 인간중심 상담 접근법 적용
• 인지행동치료(CBT) 기법을 통한 문제 해결
• 해결중심단기치료(SFBT)로 강점 기반 접근
• 게슈탈트 치료의 현재 중심적 접근 활용
• 정신분석학적 통찰을 통한 무의식 탐색
• 행동주의 기법을 활용한 행동 수정 전략

🎯 **상담 과정 관리:**
• 초기 라포 형성을 위한 공감적 경청 기술
• 구조화된 상담 프로세스: 접수-사정-개입-종결
• SOAP 노트를 활용한 체계적 상담 기록 관리
• 상담 목표 설정 및 진전도 평가 방법
• 내담자 중심 치료 계획 수립 및 진행
• 상담 윤리 및 비밀보장 원칙 철저 준수

🧠 **심리적 개입 전략:**
• 감정 조절 기술 훈련 및 마음챙김 적용
• 인지 왜곡 패턴 인식 및 수정 작업
• 대인관계 기술 향상을 위한 역할 연습
• 트라우마 상담 시 안정화 우선 원칙
• 스트레스 관리 및 회복탄력성 강화 훈련
• 자아존중감 향상을 위한 구체적 개입

🔍 **전문 상담 영역:**
• 가족상담: 시스템적 접근으로 가족역학 개선
• 부부상담: 의사소통 스킬 향상 및 갈등 해결
• 청소년상담: 발달 단계별 맞춤 상담 접근
• 직장인상담: 번아웃 예방 및 직무스트레스 관리
• 중독상담: 12단계 프로그램 및 재발 방지 계획
• 그리움상담: 상실감 극복 및 애도 과정 지원""",
            "데이터 분석": """
📊 **데이터 수집 및 전처리:**
• ETL 파이프라인 구축으로 실시간 데이터 수집 자동화
• 데이터 품질 관리: 결측치, 이상치 처리 및 데이터 무결성 확보
• 다양한 데이터 소스 통합 및 표준화 작업
• 개인정보보호 및 데이터 거버넌스 준수
• 빅데이터 처리를 위한 분산 컴퓨팅 환경 구축
• 실시간 스트리밍 데이터 처리 및 배치 처리 최적화

📈 **통계적 분석 및 모델링:**
• 기술통계에서 추론통계까지 단계적 분석 접근
• 머신러닝 알고리즘 선택: 지도/비지도/강화학습 적용
• 교차검증 및 하이퍼파라미터 튜닝으로 모델 성능 최적화
• A/B 테스트 설계 및 통계적 유의성 검증
• 시계열 분석을 통한 트렌드 및 계절성 파악
• 딥러닝 모델 구축: CNN, RNN, Transformer 활용

💡 **비즈니스 인사이트 도출:**
• 탐색적 데이터 분석(EDA)을 통한 패턴 발굴
• 고객 세그멘테이션 및 행동 패턴 분석
• 예측 모델링으로 미래 트렌드 예측
• 실행 가능한 권고사항 도출 및 의사결정 지원
• 고객 생애가치(CLV) 및 이탈 예측 모델링
• 가격 최적화 및 수요 예측 분석

🔧 **데이터 사이언스 도구:**
• Python/R을 활용한 고급 통계 분석
• SQL 데이터베이스 쿼리 최적화 및 성능 튜닝
• Tableau/Power BI를 통한 인터랙티브 대시보드 구축
• Apache Spark를 활용한 대용량 데이터 처리
• MLOps 파이프라인 구축으로 모델 배포 자동화
• 클라우드 기반 데이터 플랫폼 설계 및 운영""",
            "운세": """
🔮 **운세 분석 체계:**
• 사주팔자 기반 전통 동양 운명학 분석
• 서양 점성술과 타로카드 해석 병행
• 음양오행 이론을 통한 균형 상태 진단
• 개인 생년월일시를 통한 맞춤형 운세 분석
• 주역(I-Ching) 64괘를 통한 상황별 길흉 판단
• 수비학(Numerology)을 활용한 개인 수 분석

🎯 **생활 영역별 운세:**
• 사업운: 투자 타이밍, 사업 파트너십, 확장 시기 분석
• 연애운: 인연 만남 시기, 관계 발전 방향, 결혼 적기 예측
• 건강운: 주의해야 할 건강 이슈, 체질 개선 방법 제시
• 재물운: 수입 증대 시기, 투자 방향, 금전 관리 요령
• 학업운: 시험 성공 시기, 진학 방향, 학습 효율 향상법
• 이사운: 최적의 이주 시기, 방향, 주거 환경 선택

⭐ **운세 활용 전략:**
• 좋은 운세 시기의 적극적 활용법
• 어려운 시기의 현명한 대처 방안
• 개인별 행운 색상, 방향, 숫자 활용
• 정기적 운세 점검을 통한 인생 계획 수립
• 궁합 분석을 통한 인간관계 개선 방법
• 길일 선택으로 중요한 일정 최적화

🌟 **심화 운세 상담:**
• 10년 대운 분석으로 인생 전환점 예측
• 월별 세운 분석으로 단기 계획 수립 지원
• 일진 분석을 통한 일상 의사결정 가이드
• 꿈해몽을 통한 잠재의식 메시지 해석
• 관상학을 통한 성격 및 운명 분석
• 택일학을 활용한 중요 행사 일정 선정""",
            "데이터 분석": """
📊 **데이터 수집 및 전처리:**
• ETL 파이프라인 구축으로 실시간 데이터 수집 자동화
• 데이터 품질 관리: 결측치, 이상치 처리 및 데이터 무결성 확보
• 다양한 데이터 소스 통합: DB, API, 웹 스크래핑, IoT 센서
• 데이터 정규화 및 표준화로 분석 효율성 향상
• NoSQL과 빅데이터 처리를 위한 분산 저장 시스템 구축
• 실시간 스트리밍 데이터 처리 아키텍처 설계

� **고급 분석 기법 및 모델링:**
• 머신러닝 모델: 분류, 회귀, 클러스터링, 딥러닝 알고리즘 적용
• 시계열 분석: ARIMA, Prophet을 활용한 예측 모델링
• A/B 테스트 설계 및 통계적 유의성 검증
• 생존 분석 및 코호트 분석으로 고객 행동 패턴 파악
• 자연어 처리(NLP) 및 텍스트 마이닝 기법 활용
• 네트워크 분석 및 그래프 이론 적용한 관계 분석

� **비즈니스 인사이트 도출:**
• KPI 대시보드 구축 및 실시간 모니터링 시스템
• 고객 세그멘테이션 및 개인화 추천 시스템 개발
• 매출 예측 모델 및 수익성 분석 프레임워크
• 마케팅 캠페인 효과 측정 및 ROI 분석
• 운영 최적화를 위한 프로세스 마이닝 및 병목 지점 분석
• 리스크 관리 및 이상 거래 탐지 시스템 구축

🛠️ **분석 도구 및 기술 스택:**
• Python/R 기반 데이터 과학 생태계 활용
• SQL 최적화 및 데이터베이스 성능 튜닝
• 클라우드 플랫폼(AWS, GCP, Azure) 분석 서비스 활용
• Tableau, Power BI를 통한 인터랙티브 시각화
• Apache Spark, Hadoop을 활용한 빅데이터 처리
• Docker/Kubernetes 기반 분석 환경 컨테이너화

🔮 **AI 및 예측 분석:**
• 딥러닝 모델(CNN, RNN, Transformer) 개발 및 배포
• AutoML 도구 활용한 자동화된 모델 선택 및 튜닝
• 강화학습을 통한 동적 의사결정 시스템 구축
• 앙상블 기법으로 모델 성능 향상 및 안정성 확보
• 모델 해석 가능성(Explainable AI) 확보 방안
• MLOps 파이프라인 구축으로 모델 생명주기 관리""",
            "운세": """
🔮 **운세 분석 체계:**
• 사주팔자 기반 전통 동양 운명학 분석
• 서양 점성술과 타로카드 해석 병행
• 음양오행 이론을 통한 균형 상태 진단
• 개인 생년월일시를 통한 맞춤형 운세 해석
• 천간지지 조합으로 성격 특성 및 재능 분석
• 대운과 세운의 상호작용으로 시기별 운세 예측

� **개인 운세 세부 분석:**
• 사주 정통 해석: 일간을 중심으로 한 오행 균형 분석
• 십신론 적용한 성격 유형 및 인간관계 패턴 파악
• 용신 찾기를 통한 개인 맞춤 개운법 제시
• 공망, 형충파해 등 특수 조합 해석 및 대응법
• 월령과 절기를 고려한 정밀 사주 분석
• 결혼, 취업, 사업 등 분야별 맞춤 운세 상담

📅 **시기별 운세 및 주기 분석:**
• 10년 대운과 1년 세운의 상호작용 해석
• 월별, 일별 세부 운세 흐름 예측
• 생체 리듬과 우주 에너지 주기 분석
• 중요 결정 시기 및 피해야 할 시점 제시
• 계절별 오행 에너지 변화에 따른 건강 운세
• 음력과 양력 기준 각각의 운세 해석 차이점

🏠 **풍수지리 및 환경 운세:**
• 주거 환경과 운세의 상관관계 분석
• 방위학을 활용한 최적 이사 시기 및 방향 제시
• 사무실, 상점 등 사업장 풍수 진단 및 개선법
• 색상 운세학을 통한 라이프스타일 개선 제안
• 명당 자리 찾기 및 혈자리 감정 기법
• 현대 도시 풍수와 전통 풍수의 통합 접근법

🔮 **점술 및 예언 기법:**
• 타로카드 78장 완전 해석 및 스프레드 기법
• 주역(易經) 64괘를 통한 상황 분석 및 해법 제시
• 관상학 및 수상학을 통한 성격 및 운명 분석
• 꿈 해몽 및 무의식 메시지 해석
• 숫자 운세학(수비학) 활용한 개인 번호 분석
• 신점 및 영적 가이던스를 통한 내면 통찰

💎 **개운법 및 액막이:**
• 개인 맞춤 부적 제작 및 착용법 지도
• 오행 보강을 위한 생활 습관 개선 가이드
• 액막이 의식 및 정화 방법 전수
• 개명, 상호명 작명을 통한 운세 개선
• 보석 및 천연석 활용한 에너지 밸런싱
• 명상 및 기도를 통한 영적 성장 방법론""",
            "성장": """
🌱 **개인 성장 프레임워크:**
• 성장 마인드셋 vs 고정 마인드셋 구분 및 전환
• SMART 목표 설정법을 넘어선 OKR(목표-핵심결과) 도입
• 강점 기반 성장 전략: CliftonStrengths 활용법
• 7가지 습관을 통한 지속적 자기계발
• 성격유형(MBTI, 에니어그램) 기반 맞춤 성장 전략
• 라이프 밸런스 휠을 통한 전방위적 성장 관리

📚 **학습 및 역량 개발:**
• 70-20-10 학습 모델: 경험-멘토링-교육 균형
• 액션러닝을 통한 실무 문제 해결 능력 향상
• 리플렉션 저널링으로 경험의 의미화
• 크로스 펑셔널 스킬 개발로 T자형 인재 성장
• 언러닝(Unlearning) 과정을 통한 기존 습관 개선
• 마이크로러닝을 활용한 지속 가능한 학습 체계

🎯 **목표 달성 시스템:**
• 백캐스팅 기법으로 미래에서 현재로 역산 계획
• 습관 스택킹을 통한 점진적 변화 관리
• 1% 개선 원칙으로 복리 효과 창출
• 피드백 루프 구축으로 지속적 조정
• 시간 블록킹을 통한 성장 활동 시간 확보
• 책임감 파트너(Accountability Partner) 시스템 활용

🔥 **동기부여 및 지속성:**
• 내재적 동기와 외재적 동기의 균형적 활용
• 작은 성공의 축적을 통한 자신감 구축
• 실패를 학습 기회로 전환하는 회복탄력성 개발
• 성장 공동체 참여를 통한 동기 부여 지속
• 비전 보드 작성으로 목표 시각화 및 몰입 강화
• 정기적 성찰을 통한 성장 방향 재정립

💡 **리더십 및 영향력 개발:**
• 개인 브랜딩을 통한 전문성 어필 및 네트워킹
• 멘토링 스킬 개발로 타인의 성장 도움
• 창의적 사고력 향상을 위한 브레인스토밍 기법
• 비판적 사고력 강화로 합리적 의사결정 능력 배양
• 협업 및 팀워크 스킬로 집단 지성 활용
• 글로벌 마인드셋 개발 및 문화적 감수성 향상""",
            "인사 관리": """
👥 **전략적 인사관리:**
• 조직 목표와 연계된 인사 전략 수립
• 역량 기반 인사관리 시스템 구축
• 인사정보시스템(HRIS) 도입 및 활용
• 조직문화 진단 및 개선 프로그램 운영
• 조직 개발(OD) 컨설팅을 통한 체계적 변화 관리
• 워크포스 플래닝으로 미래 인력 수요 예측

🔍 **채용 및 선발:**
• 직무분석을 통한 정확한 직무요건 도출
• 구조화 면접 및 역량면접 설계
• 다면평가 및 어세스먼트 센터 운영
• 온보딩 프로그램을 통한 신입직원 적응 지원
• AI 채용 도구 활용으로 편견 없는 선발 프로세스
• 레퍼런스 체크 및 백그라운드 검증 시스템

📈 **성과관리 및 평가:**
• 목표관리제(MBO)와 핵심성과지표(KPI) 연계
• 360도 피드백을 통한 다면적 평가
• 성과급 및 인센티브 제도 설계
• 성과개선계획(PIP) 수립 및 실행
• 연속적 성과 관리(Continuous Performance Management)
• 성과와 역량의 9-Box Grid 활용한 인재 포트폴리오

🎓 **교육훈련 및 개발:**
• 교육체계도(Training Road Map) 구축
• 리더십 개발 프로그램 설계 및 운영
• 멘토링 및 코칭 시스템 도입
• 경력개발계획(CDP) 수립 지원
• e-러닝 플랫폼 구축 및 마이크로러닝 도입
• 액션러닝 및 프로젝트 기반 학습 프로그램

💼 **보상 및 복리후생:**
• 직무가치평가를 통한 공정한 보상 체계
• 전사적 보상 철학 및 정책 수립
• 탄력적 복리후생제도(카페테리아 플랜) 도입
• 워라밸 향상을 위한 유연근무제 운영
• 직원 참여 프로그램 및 소통 채널 확대
• 퇴직 관리 및 아웃플레이스먼트 서비스 제공""",
            "마케팅": """
📢 **디지털 마케팅 통합 전략:**
• SEO/SEM 최적화로 검색 트래픽 200% 증가 목표
• 소셜미디어 마케팅: 인스타그램, 페이스북, 틱톡 채널별 맞춤 콘텐츠
• 이메일 마케팅: 개방률 25%, 클릭률 3% 이상 달성 KPI
• 인플루언서 마케팅을 통한 브랜드 신뢰도 향상
• 콘텐츠 마케팅으로 브랜드 전문성 구축 및 SEO 시너지
• 마케팅 자동화 도구 활용한 리드 너처링 최적화

🎯 **고객 여정 최적화:**
• AIDA 모델 기반 퍼널 설계: 인지-관심-욕구-행동 단계별 최적화
• 고객 세그멘테이션: 데모그래픽, 행동, 심리그래픽 기준 타겟팅
• 리텐션 마케팅: 고객 생애가치(CLV) 30% 향상 전략
• 옴니채널 경험 설계로 일관된 브랜드 메시지 전달
• 개인화 마케팅을 통한 고객별 맞춤 경험 제공
• 고객 이탈 예측 모델 구축 및 예방 캠페인 운영

💡 **브랜드 포지셔닝 및 메시지:**
• 경쟁 차별화 요소 발굴 및 USP(고유판매제안) 개발
• 브랜드 아이덴티티 구축: 로고, 컬러, 톤앤매너 일관성
• 스토리텔링을 통한 감성적 연결 강화
• 브랜드 인지도 측정 및 지속적 모니터링
• 브랜드 아키텍처 설계로 포트폴리오 브랜드 관리
• 위기 상황 브랜드 커뮤니케이션 전략 수립

📊 **데이터 기반 마케팅:**
• 구글 애널리틱스 4를 활용한 고급 웹 분석
• 고객 행동 분석을 통한 UX/UI 개선 인사이트 도출
• A/B 테스트를 통한 마케팅 메시지 최적화
• 마케팅 어트리뷰션 모델링으로 채널별 기여도 분석
• 예측 분석을 통한 마케팅 ROI 극대화
• 실시간 대시보드 구축으로 캠페인 성과 모니터링

🚀 **신규 마케팅 채널 및 기법:**
• 바이럴 마케팅 전략 수립 및 실행
• 게이미피케이션을 활용한 고객 참여 증대
• AR/VR 기술을 활용한 혁신적 브랜드 경험
• 팟캐스트 및 웨비나 마케팅으로 전문성 어필
• 커뮤니티 마케팅을 통한 충성 고객 기반 구축
• 파트너십 마케팅으로 브랜드 시너지 창출""",
            "의료": """
🏥 **진단 및 치료 프로세스:**
• 체계적 임상 추론을 통한 정확한 진단
• 근거 기반 의학(EBM) 적용한 치료 계획 수립
• 환자 안전 우선 원칙과 의료 오류 예방 시스템
• 다학제 팀 접근을 통한 통합적 치료
• 임상 가이드라인 준수 및 최신 의학 지식 적용
• 환자 개별 특성을 고려한 개인 맞춤형 치료

👨‍⚕️ **환자 중심 의료 서비스:**
• 환자-의료진 소통 강화를 위한 커뮤니케이션 스킬
• 개별 환자 특성을 고려한 맞춤형 치료 계획
• 인포름드 컨센트를 통한 치료 과정 투명화
• 환자 만족도 향상을 위한 서비스 개선
• 문화적 다양성을 고려한 의료 서비스 제공
• 환자 권리 보장 및 윤리적 의료 실천

🔬 **의료 기술 및 혁신:**
• 디지털 헬스케어 기술 도입 및 활용
• AI 진단 보조 시스템과 정밀의료 적용
• 원격의료 시스템 구축 및 모니터링
• 지속적인 의학 교육과 최신 연구 동향 파악
• 로봇 수술 및 미니멀 인베이시브 기술 활용
• 3D 프린팅, VR/AR 기술의 의료 분야 적용

⚕️ **예방 의학 및 건강 증진:**
• 생활습관 개선을 통한 질병 예방 프로그램
• 정기 건강검진 체계 구축 및 조기 발견 시스템
• 개인별 건강 위험도 평가 및 맞춤 관리 계획
• 지역사회 기반 공중보건 프로그램 운영
• 만성질환 관리를 위한 통합 케어 시스템
• 정신건강 스크리닝 및 통합적 치료 접근

📊 **의료 품질 관리:**
• 의료 성과 지표 모니터링 및 개선
• 감염 관리 및 병원 안전 시스템 구축
• 의료진 역량 강화를 위한 지속적 교육
• 의료사고 예방을 위한 안전 문화 조성
• 환자 안전 보고 시스템 및 개선 프로세스
• 의료 서비스 표준화 및 프로토콜 개발""",
            "영업": """
💰 **전략적 영업 접근:**
• 컨설턴트형 영업으로 고객 문제 해결 중심 접근
• 스핀 세일즈(SPIN Selling) 기법으로 니즈 발굴
• 솔루션 영업을 통한 가치 기반 판매
• CRM 시스템 활용한 고객 관계 관리
• 인사이트 셀링으로 고객에게 새로운 관점 제공
• 챌린저 세일즈 방식으로 고객 사고 변화 유도

📊 **영업 프로세스 최적화:**
• 리드 생성부터 계약 체결까지 세일즈 퍼널 관리
• 영업 단계별 전환율 분석 및 개선
• 파이프라인 관리를 통한 매출 예측 정확도 향상
• A/B 테스트를 통한 영업 스크립트 최적화
• 영업 사이클 단축을 위한 프로세스 효율화
• 디지털 세일즈 도구 활용한 생산성 극대화

🎯 **고객 세분화 및 타겟팅:**
• RFM 분석을 통한 고객 가치 세분화
• 고객 생애 가치(CLV) 계산 및 활용
• 페르소나 기반 맞춤형 영업 전략 수립
• 크로스셀링 및 업셀링 기회 발굴
• ICP(Ideal Customer Profile) 정의 및 활용
• 어카운트 기반 마케팅(ABM) 전략 실행

🤝 **관계 영업 및 네트워킹:**
• 장기적 관점의 신뢰 관계 구축
• 고객 의사결정권자와의 전략적 네트워킹
• 레퍼런스 고객 확보 및 활용 전략
• 고객 성공 관리를 통한 갱신율 향상
• 파트너 채널 개발 및 관리
• 업계 전문성 구축으로 thought leader 포지셔닝

📈 **영업 성과 관리:**
• KPI 기반 성과 측정 및 개선
• 영업팀 코칭 및 스킬 개발 프로그램
• 인센티브 설계를 통한 동기부여 체계
• 영업 데이터 분석을 통한 인사이트 도출
• 경쟁사 대응 전략 수립 및 실행
• 시장 변화에 따른 영업 전략 조정

🚀 **디지털 영업 혁신:**
• 소셜 셀링을 통한 온라인 관계 구축
• 영업 자동화 도구 활용한 효율성 극대화
• 데이터 기반 영업 인사이트 도출
• 옴니채널 영업 전략으로 고객 접점 확대
• AI 기반 리드 스코어링 및 예측 분석
• 가상 영업 환경에서의 효과적 소통 기법""",
            "검색 최적화": """
🔍 **기술적 SEO 최적화:**
• 크롤링 및 인덱싱 최적화를 위한 robots.txt 설정
• XML 사이트맵 생성 및 구글 서치 콘솔 연동
• 페이지 로딩 속도 최적화: Core Web Vitals 개선
• 모바일 퍼스트 인덱싱에 대응한 반응형 웹 구축
• 구조화된 데이터(Schema Markup) 적용으로 리치 스니펫 확보
• 내부 링크 구조 최적화 및 URL 구조 개선

📝 **콘텐츠 SEO 전략:**
• 키워드 리서치: 검색량, 경쟁도, 상업적 의도 분석
• E-A-T(전문성-권위성-신뢰성) 기반 콘텐츠 제작
• 구조화된 데이터(Schema Markup) 적용
• 사용자 검색 의도에 맞는 콘텐츠 최적화
• 롱테일 키워드 전략으로 틈새 트래픽 확보
• 콘텐츠 클러스터링으로 토픽 어쏘리티 구축

🔗 **링크 빌딩 및 오프페이지 SEO:**
• 권위 있는 사이트로부터 백링크 확보 전략
• 내부 링크 구조 최적화로 링크 주스 분배
• 앵커 텍스트 다양화 및 자연스러운 링크 프로필 구축
• 소셜 시그널 및 브랜드 멘션 증대
• 게스트 포스팅 및 콘텐츠 파트너십 전략
• 로컬 SEO 최적화로 지역 검색 가시성 향상

📊 **SEO 분석 및 모니터링:**
• 구글 애널리틱스와 서치 콘솔 데이터 분석
• 키워드 순위 추적 및 경쟁사 분석
• SEO 성과 지표(CTR, 세션 시간, 이탈률) 모니터링
• A/B 테스트를 통한 메타태그 최적화
• 기술적 SEO 오류 정기 진단 및 해결
• ROI 기반 SEO 성과 측정 및 보고

🚀 **고급 SEO 전략:**
• 음성 검색 최적화를 위한 대화형 콘텐츠 제작
• AI 검색 엔진에 대응한 콘텐츠 전략 수립
• 국제 SEO를 위한 다국어 사이트 최적화
• 엔터프라이즈 SEO 전략 및 대규모 사이트 관리
• SEO와 다른 마케팅 채널의 통합 전략
• 미래 검색 트렌드 대응 및 혁신적 접근법""",
            "쇼핑": """
🛒 **스마트 쇼핑 전략:**
• 가격 비교 사이트 및 앱 활용한 최적 가격 탐색
• 쿠폰 및 할인 정보 통합 관리 시스템 구축
• 계절별 세일 시즌 캘린더 활용한 전략적 구매
• 중고 거래 플랫폼 활용한 합리적 소비
• 그룹 바잉 및 공동구매를 통한 비용 절약
• 라이브 커머스 및 소셜 쇼핑 활용 전략

💳 **결제 및 혜택 최적화:**
• 신용카드 할인 및 적립 혜택 비교 분석
• 멤버십 및 구독 서비스 가치 평가
• 현금 결제 vs 카드 결제 손익 계산
• 포인트 및 마일리지 효율적 활용법
• 간편결제 서비스별 혜택 비교 및 선택
• 분할결제 및 후불결제 서비스 활용 전략

🔍 **상품 검증 및 품질 평가:**
• 상품 리뷰 신뢰도 판별법 및 페이크 리뷰 식별
• 브랜드별 품질 기준 및 성가비 분석
• AS 서비스 및 반품 정책 사전 확인
• 제품 수명 주기 고려한 장기적 가치 평가
• 인증 마크 및 품질 보증 기준 이해
• 소비자 리포트 및 전문가 리뷰 활용법

📱 **디지털 쇼핑 노하우:**
• 모바일 쇼핑앱 최적 활용법 및 알림 설정
• AI 기반 개인화 쇼핑 추천 시스템 활용
• 소셜 커머스 및 인플루언서 마케팅 판별법
• 온라인 전용 상품 vs 오프라인 연계 상품 비교
• 가상현실(VR) 및 증강현실(AR) 쇼핑 체험
• 구독 경제 서비스의 비용 효율성 분석

🌱 **지속 가능한 소비:**
• 친환경 제품 선택 기준 및 인증 마크 이해
• 제로 웨이스트 쇼핑 및 리필 스테이션 활용
• 로컬 브랜드 및 사회적 기업 제품 우선 구매
• 업사이클링 및 리퍼브 제품 활용 전략
• 탄소 발자국 고려한 배송 옵션 선택
• 윤리적 소비를 위한 브랜드 가치 평가""",
            "마을 관리": """
👑 **통합적 리더십 전략:**
• 각 분야 전문 도깨비들의 역량 최대화 조율
• 부서간 시너지 창출을 위한 크로스 펑셔널 팀 운영
• 데이터 기반 의사결정을 위한 통합 대시보드 구축
• 변화 관리 리더십으로 조직 혁신 주도
• 전략적 비전 수립 및 조직 전체 목표 정렬
• 갈등 해결 및 합의 도출을 위한 조정 역할

🎯 **서비스 품질 관리:**
• 16개 분야 전문 서비스의 일관된 품질 기준 확립
• 고객 만족도 측정 및 개선 계획 수립
• 서비스 수준 협약(SLA) 관리 및 모니터링
• 지속적 개선을 위한 PDCA 사이클 운영
• 서비스 표준화 및 프로세스 최적화
• 고객 피드백 수집 및 반영 체계 구축

📊 **성과 측정 및 관리:**
• 분야별 KPI 설정 및 통합 성과 관리 시스템
• 균형성과표(BSC)를 통한 다면적 성과 평가
• 벤치마킹을 통한 경쟁력 분석 및 개선
• ROI 기반 투자 우선순위 결정
• 정기적 성과 리뷰 및 개선 계획 수립
• 예측 분석을 통한 미래 성과 전망

🤝 **이해관계자 관리:**
• 주민(사용자) 니즈 수렴 및 의견 반영 체계
• 투명한 커뮤니케이션을 통한 신뢰 구축
• 갈등 조정 및 합의 도출 메커니즘 운영
• 파트너십 구축을 통한 생태계 확장
• 커뮤니티 참여 증진 프로그램 운영
• 소통 채널 다양화 및 접근성 향상

🔮 **미래 전략 및 혁신:**
• 디지털 트랜스포메이션 로드맵 수립
• 신기술 도입 및 혁신 프로젝트 관리
• 지속 가능한 발전을 위한 ESG 경영
• 위기 관리 및 비상 계획 수립
• 조직 학습 문화 조성 및 지식 관리
• 차세대 리더 육성 및 승계 계획""",
            "문서 작성": """
✍️ **문서 구조 설계:**
• 피라미드 구조를 활용한 논리적 정보 배치
• 5W1H 원칙에 따른 체계적 정보 정리
• 독자 맞춤형 문서 톤앤매너 설정
• 문서 유형별 템플릿화 및 표준화
• 정보 아키텍처 설계로 복잡한 내용 체계화
• 스토리텔링 기법을 활용한 매력적 구성

📝 **효과적 글쓰기 기법:**
• PREP(Point-Reason-Example-Point) 구조 활용
• 능동태 우선 사용으로 명확한 표현
• 구체적 수치와 사례를 통한 설득력 강화
• 시각적 요소(차트, 도표) 활용한 가독성 향상
• 패러그래프 라이팅으로 논리적 전개
• 전환어 및 연결어 활용한 자연스러운 흐름

🎯 **목적별 문서 작성:**
• 제안서: 문제 정의-해결 방안-기대 효과 구조
• 보고서: 요약-현황-분석-결론-권고사항 순서
• 매뉴얼: 단계별 프로세스와 예외 상황 대응법
• 프레젠테이션: 스토리텔링과 핵심 메시지 집중
• 기획서: 배경-목표-전략-실행계획-평가 체계
• 계약서: 명확한 조건 명시 및 법적 리스크 고려

📊 **협업 문서 관리:**
• 버전 관리 시스템을 통한 문서 이력 추적
• 실시간 협업 도구 활용한 효율적 공동 작업
• 피드백 수집 및 반영 프로세스 체계화
• 문서 접근 권한 관리 및 보안 정책 수립
• 문서 생명주기 관리 및 아카이브 전략
• 지식 관리 시스템 구축 및 재활용 체계

🔍 **품질 관리 및 검토:**
• 다단계 검토 프로세스: 자가검토-동료검토-최종검토
• 가독성 지수 측정 및 개선
• 문법 검사 도구 활용 및 맞춤법 정확성 확보
• 독자 피드백 수집 및 반영 체계 구축
• 문서 효과성 측정 및 개선 지표 설정
• 전문가 검토 및 팩트체킹 프로세스

💡 **창의적 글쓰기:**
• 브레인스토밍 및 마인드맵을 통한 아이디어 발굴
• 메타포 및 비유 활용한 복잡한 개념 설명
• 감정적 어필과 논리적 설득의 균형
• 독창적 관점 및 차별화된 인사이트 제시
• 멀티미디어 요소 활용한 풍부한 콘텐츠 구성
• 인터랙티브 요소 도입으로 독자 참여 유도""",
        }

        return detailed_solutions.get(
            field,
            f"{field} 분야의 전문적이고 체계적인 접근 방법을 통해 문제를 해결하고 목표를 달성할 수 있습니다.",
        )

    def _get_practical_steps(self, question: str, field: str) -> str:
        """실용적 단계별 실행 방안"""

        steps = {
            "업무 관리": """
1️⃣ **1단계: 현재 상황 분석 (1주)**
   • 현재 업무 패턴 및 시간 사용 분석
   • 업무 우선순위 및 중요도 평가
   • 방해 요소 및 비효율 구간 파악

2️⃣ **2단계: 시스템 구축 (2주)**
   • 개인 업무 관리 도구 선택 및 설정
   • 일일/주간 계획 수립 루틴 확립
   • 업무 분류 체계 및 우선순위 기준 설정

3️⃣ **3단계: 실행 및 모니터링 (4주)**
   • 새로운 업무 방식 적용 및 습관화
   • 주간 단위 성과 측정 및 분석
   • 필요에 따른 방법론 조정 및 개선""",
            "개발": """
1️⃣ **1단계: 요구사항 분석 및 설계**
   • 프로젝트 목표 및 성공 기준 명확화
   • 기능 요구사항 및 비기능 요구사항 정의
   • 시스템 아키텍처 및 기술 스택 결정

2️⃣ **2단계: MVP 개발**
   • 핵심 기능 우선순위 선정
   • 프로토타입 개발 및 초기 테스트
   • 사용자 피드백 수집 및 검증

3️⃣ **3단계: 반복 개발 및 개선**
   • 스프린트 단위 기능 추가 및 개선
   • 지속적인 테스트 및 품질 관리
   • 성능 최적화 및 확장성 개선""",
            "창작": """
1️⃣ **1단계: 아이디어 발굴 및 구체화**
   • 창작 주제 및 방향성 설정
   • 레퍼런스 조사 및 영감 수집
   • 초기 컨셉 스케치 및 아이디어 정리

2️⃣ **2단계: 창작 실행**
   • 상세 기획 및 스토리보드 작성
   • 단계별 창작 과정 실행
   • 중간 점검 및 방향성 조정

3️⃣ **3단계: 완성 및 발표**
   • 최종 검토 및 품질 개선
   • 발표 및 배포 준비
   • 피드백 수집 및 향후 계획 수립""",
            "창업전략": """
1️⃣ **1단계: 아이디어 검증 및 시장 조사 (1-2개월)**
   • 고객 문제 발굴 및 페인 포인트 명확화
   • 100명 이상 타겟 고객 인터뷰 실시
   • 경쟁사 분석 및 차별화 포인트 도출

2️⃣ **2단계: MVP 개발 및 초기 검증 (3-4개월)**
   • 핵심 기능만 포함한 MVP 설계 및 개발
   • 베타 사용자 50-100명 확보 및 피드백 수집
   • 초기 비즈니스 모델 설계 및 수익화 방안 수립

3️⃣ **3단계: 시장 진입 및 초기 성장 (6-12개월)**
   • 제품-시장 적합성(PMF) 달성을 위한 지속적 개선
   • 초기 1000명 사용자 확보 및 재구매율 30% 이상 달성
   • 시드 투자 유치 및 팀 확장 (개발 2명, 마케팅 1명)""",
            "스타트업경영": """
1️⃣ **1단계: 아이디어 검증 및 시장 조사 (1-2개월)**
   • 고객 문제 발굴 및 페인 포인트 명확화
   • 100명 이상 타겟 고객 인터뷰 실시
   • 경쟁사 분석 및 차별화 포인트 도출

2️⃣ **2단계: MVP 개발 및 초기 검증 (3-4개월)**
   • 핵심 기능만 포함한 MVP 설계 및 개발
   • 베타 사용자 50-100명 확보 및 피드백 수집
   • 초기 비즈니스 모델 설계 및 수익화 방안 수립

3️⃣ **3단계: 시장 진입 및 초기 성장 (6-12개월)**
   • 제품-시장 적합성(PMF) 달성을 위한 지속적 개선
   • 초기 1000명 사용자 확보 및 재구매율 30% 이상 달성
   • 시드 투자 유치 및 팀 확장 (개발 2명, 마케팅 1명)""",
        }

        return steps.get(
            field, f"{field} 분야의 체계적인 단계별 접근을 통해 목표를 달성하세요."
        )

    def _get_expert_tips(self, question: str, field: str) -> str:
        """전문가 노하우 및 팁"""

        tips = {
            "업무 관리": """
🔥 **실전 노하우:**
• 메일 확인은 하루 3회로 제한하여 집중력 유지
• 15분 룰: 복잡한 업무도 15분간 시작해보면 저항감 극복
• 에너지 레벨에 맞는 업무 배치 (오전=창작업무, 오후=단순업무)

⚠️ **주의사항:**
• 완벽주의 함정에 빠지지 말고 80% 완성도에서 다음 단계로
• 멀티태스킹보다는 집중적인 단일 작업이 더 효율적
• 번아웃 방지를 위한 적절한 휴식과 여유 시간 확보""",
            "개발": """
🔥 **개발 노하우:**
• 코드 리뷰를 통한 지속적인 품질 향상
• 문서화는 미래의 나와 팀을 위한 투자
• 라이브러리 선택 시 커뮤니티 활성도와 유지보수 상태 고려

⚠️ **피해야 할 함정:**
• 과도한 최적화보다는 가독성과 유지보수성 우선
• 새로운 기술 도입 시 충분한 검증 과정 필요
• 기술 부채 누적 방지를 위한 정기적인 리팩토링""",
            "창작": """
🔥 **창작 노하우:**
• 아이디어 고갈 시에는 기존 작품의 재해석이나 조합 시도
• 창작 블록 극복법: 환경 변화, 산책, 다른 활동으로 전환
• 비판적 시각과 창작 모드를 분리하여 창의성 보호

⚠️ **창작 함정:**
• 첫 작품부터 완벽을 추구하지 말고 완성에 집중
• 타인의 평가에 과도하게 의존하지 말고 자신만의 기준 확립
• 영감 대기보다는 규칙적인 창작 습관으로 실력 향상""",
            "창업전략": """
🔥 **창업 성공 노하우:**
• 고객과의 직접 대화가 모든 가정보다 중요 - 매주 최소 10명 고객 인터뷰
• 실패 빠르게, 학습 빠르게: 3개월 내 결과 안 나오면 피벗 고려
• 창업자 시간의 80%는 고객 개발과 제품 개발에만 투자

⚠️ **창업 함정:**
• '아이디어가 좋으면 성공한다' 착각 - 실행력과 지속력이 90%
• 완벽한 제품 만들기 전에 시장 출시 - 고객이 원하는 걸 만들어야 함
• 초기 자금을 마케팅보다는 제품 개발과 팀 구성에 집중""",
            "스타트업경영": """
🔥 **창업 성공 노하우:**
• 고객과의 직접 대화가 모든 가정보다 중요 - 매주 최소 10명 고객 인터뷰
• 실패 빠르게, 학습 빠르게: 3개월 내 결과 안 나오면 피벗 고려
• 창업자 시간의 80%는 고객 개발과 제품 개발에만 투자

⚠️ **창업 함정:**
• '아이디어가 좋으면 성공한다' 착각 - 실행력과 지속력이 90%
• 완벽한 제품 만들기 전에 시장 출시 - 고객이 원하는 걸 만들어야 함
• 초기 자금을 마케팅보다는 제품 개발과 팀 구성에 집중""",
        }

        return tips.get(
            field,
            f"{field} 분야에서 성공하기 위한 전문가만의 실전 노하우를 적용해보세요.",
        )

    def _get_deep_analysis(self, question: str, field: str) -> str:
        """심화 분석"""

        analysis = {
            "업무 관리": "업무 관리의 핵심은 시간이 아닌 에너지 관리입니다. 개인의 생체리듬과 에너지 패턴을 파악하여 중요한 업무를 고에너지 시간대에 배치하고, 루틴 업무는 저에너지 시간대에 처리하는 것이 효율성을 극대화하는 비결입니다.",
            "개발": "성공적인 개발 프로젝트의 핵심은 기술적 완성도보다는 사용자 문제 해결에 있습니다. 기술 스택 선택과 아키텍처 설계 시 현재 요구사항뿐만 아니라 미래 확장 가능성을 고려한 균형점을 찾는 것이 중요합니다.",
            "창작": "진정한 창작은 기존의 것을 완전히 새롭게 만드는 것이 아니라, 기존 요소들의 새로운 조합과 개인적 해석을 통해 독창성을 발현하는 것입니다. 모방에서 시작하여 점진적으로 자신만의 스타일을 발전시키는 것이 효과적입니다.",
            "창업전략": "성공적인 창업의 핵심은 '고객이 정말 돈을 지불하고 싶어하는 문제'를 해결하는 것입니다. 기술이나 아이디어가 아무리 뛰어나도 시장에서 검증되지 않으면 의미가 없습니다. MVP를 통한 빠른 시장 검증과 고객 피드백 기반의 지속적 개선이 성공의 열쇠입니다.",
            "스타트업경영": "성공적인 창업의 핵심은 '고객이 정말 돈을 지불하고 싶어하는 문제'를 해결하는 것입니다. 기술이나 아이디어가 아무리 뛰어나도 시장에서 검증되지 않으면 의미가 없습니다. MVP를 통한 빠른 시장 검증과 고객 피드백 기반의 지속적 개선이 성공의 열쇠입니다.",
        }

        return analysis.get(
            field, f"{field} 분야의 본질적 이해를 바탕으로 한 전문적 접근이 필요합니다."
        )

    def _get_success_cases_and_warnings(self, field: str) -> str:
        """성공 사례 및 주의사항"""

        cases = {
            "업무 관리": """
✅ **성공 사례:** 글로벌 기업 CEO들이 공통적으로 사용하는 '시간 블록킹' 기법으로 하루를 미리 계획된 블록으로 나누어 관리
⚠️ **주의사항:** 과도한 계획으로 인한 스트레스보다는 80% 계획 + 20% 여유 공간 확보가 현실적""",
            "개발": """
✅ **성공 사례:** 넷플릭스의 마이크로서비스 아키텍처로 확장성과 안정성을 동시에 확보한 사례
⚠️ **주의사항:** 복잡한 아키텍처보다는 현재 팀 규모와 요구사항에 적합한 단순한 구조가 더 효과적일 수 있음""",
            "창작": """
✅ **성공 사례:** 픽사의 스토리텔링 방법론으로 기술적 혁신과 감정적 공감을 결합한 작품 창작
⚠️ **주의사항:** 트렌드만 따라가는 창작보다는 개인의 고유한 관점과 경험을 바탕으로 한 진정성 있는 작품이 더 오래 기억됨""",
        }

        return cases.get(
            field,
            f"{field} 분야의 실제 성공 사례를 참고하되, 개별 상황에 맞는 적용이 중요합니다.",
        )

    def _get_comprehensive_analysis(self, question: str, field: str) -> str:
        """종합적 분석"""

        return f"{field} 분야에서 제기된 문제는 단순히 기술적 해결책만으로는 완전한 해결이 어려우며, 인간적 요소, 환경적 요인, 그리고 장기적 관점을 모두 고려한 통합적 접근이 필요합니다."

    def _get_strategic_approach(self, question: str, field: str) -> str:
        """전략적 접근법"""

        approaches = {
            "업무 관리": "개인의 업무 스타일과 조직 문화를 조화시키면서, 단기 효율성과 장기 지속가능성의 균형을 맞추는 전략적 접근",
            "개발": "비즈니스 요구사항과 기술적 제약사항을 고려한 점진적 개발 전략으로, 위험을 최소화하면서 가치 창출을 극대화",
            "창작": "개인의 창작 철학과 시장의 요구를 균형있게 반영하여, 예술적 완성도와 대중적 어필을 동시에 추구하는 전략",
        }

        return approaches.get(
            field, f"{field} 분야의 특성을 고려한 맞춤형 전략적 접근이 필요합니다."
        )

    def _get_implementation_guide(self, field: str) -> str:
        """구현 가이드"""

        guides = {
            "업무 관리": "현재 업무 패턴 분석 → 개선 포인트 식별 → 단계적 변화 적용 → 효과 측정 → 지속적 개선의 순환 구조로 실행",
            "개발": "요구사항 정의 → 프로토타입 개발 → 사용자 검증 → 반복 개선 → 확장의 애자일 방식으로 점진적 구현",
            "창작": "아이디어 발굴 → 컨셉 구체화 → 시안 제작 → 피드백 반영 → 최종 완성의 반복적 창작 프로세스로 진행",
        }

        return guides.get(
            field,
            f"{field} 분야의 체계적인 구현 방법론을 적용하여 단계적으로 진행하세요.",
        )

    def _get_immediate_actions(self, field: str) -> str:
        """즉시 실행 가능한 방법"""

        actions = {
            "업무 관리": "오늘부터 시작: ① 하루 가장 중요한 업무 3개 선정 ② 집중 시간 1시간 확보 ③ 업무 종료 시 다음날 계획 5분 투자",
            "개발": "지금 바로 시작: ① 프로젝트 요구사항 한 줄 정리 ② 가장 단순한 기능부터 구현 ③ 15분 내 실행 가능한 프로토타입 제작",
            "창작": "당장 실행: ① 스마트폰으로 일상의 흥미로운 순간 사진 촬영 ② 10분간 자유로운 스케치나 글쓰기 ③ 좋아하는 작품 하나 선정하여 분석",
        }

        return actions.get(
            field,
            f"{field} 분야에서 지금 당장 시작할 수 있는 작은 행동부터 시작해보세요.",
        )

    def _get_long_term_strategy(self, field: str) -> str:
        """장기적 전략"""

        strategies = {
            "업무 관리": "6개월 목표: 개인 맞춤형 업무 시스템 완성 / 1년 목표: 업무 효율성 50% 향상 및 워라밸 확립 / 3년 목표: 전문성 기반 업무 자동화 시스템 구축",
            "개발": "6개월: 핵심 기능 완성 및 사용자 검증 / 1년: 확장성 있는 플랫폼 구축 / 3년: 업계 표준이 되는 솔루션 개발",
            "창작": "6개월: 개인 스타일 확립 / 1년: 대표작 완성 및 인지도 구축 / 3년: 창작 영역 확장 및 영향력 있는 작가로 성장",
        }

        return strategies.get(
            field,
            f"{field} 분야에서의 장기적 성장과 발전을 위한 단계별 전략을 수립하여 실행하세요.",
        )

    def get_agent_info(self) -> Dict[str, Any]:
        """도깨비 정보 반환 (프론트엔드용)"""
        agent_info = {
            "assistant": {
                "emoji": "🤖",
                "name": "박사급 비서 도깨비",
                "field": "업무 관리",
            },
            "builder": {"emoji": "💻", "name": "빌더 도깨비", "field": "개발"},
            "counselor": {"emoji": "💬", "name": "상담 도깨비", "field": "상담"},
            "creative": {"emoji": "🎨", "name": "창작 도깨비", "field": "창작"},
            "data_analyst": {
                "emoji": "📊",
                "name": "데이터분석 도깨비",
                "field": "데이터 분석",
            },
            "fortune": {"emoji": "🔮", "name": "운세 도깨비", "field": "운세"},
            "growth": {"emoji": "🌱", "name": "성장 도깨비", "field": "성장"},
            "hr": {"emoji": "👥", "name": "HR 도깨비", "field": "인사 관리"},
            "marketing": {
                "emoji": "📢",
                "name": "마케팅 도깨비",
                "field": "마케팅",
            },
            "medical": {"emoji": "🏥", "name": "의료 도깨비", "field": "의료"},
            "sales": {"emoji": "💰", "name": "영업 도깨비", "field": "영업"},
            "seo": {"emoji": "🔍", "name": "SEO 도깨비", "field": "검색 최적화"},
            "shopping": {"emoji": "🛒", "name": "쇼핑 도깨비", "field": "쇼핑"},
            "startup": {"emoji": "🚀", "name": "스타트업 도깨비", "field": "창업"},
            "village_chief": {
                "emoji": "👑",
                "name": "이장 도깨비",
                "field": "마을 관리",
            },
            "writing": {
                "emoji": "✍️",
                "name": "박사급 문서 작성 도깨비",
                "field": "문서 작성",
            },
        }

        return {
            "total_agents": len(agent_info),
            "agents": agent_info,
            "categories": {
                "업무&관리": ["assistant", "hr", "village_chief", "growth"],
                "창작&마케팅": ["creative", "marketing", "writing", "seo"],
                "기술&분석": ["builder", "data_analyst", "medical", "startup"],
                "생활&상담": ["counselor", "fortune", "sales", "shopping"],
            },
        }


# 전역 인스턴스
stem_ai = STEMIntegration()


def add_stem_routes(app):
    """FastAPI 앱에 STEM 라우트 추가"""
    from fastapi import Request
    from fastapi.responses import HTMLResponse

    @app.post("/stem/chat")
    async def stem_chat(request: Request):
        """STEM 도깨비와 채팅"""
        try:
            data = await request.json()
            agent_type = data.get("agent_type")
            question = data.get("question")
            user_ip = request.client.host if request.client else "unknown"

            result = stem_ai.process_question(agent_type, question, user_ip)
            return result
        except Exception as e:
            return {"success": False, "error": f"서버 오류: {str(e)}"}

    @app.get("/stem/info")
    async def stem_info():
        """STEM 도깨비 정보 조회"""
        return stem_ai.get_agent_info()

    @app.get("/stem/stats")
    async def stem_stats():
        """STEM 사용 통계 조회"""
        try:
            from usage_tracker import usage_tracker

            return usage_tracker.get_statistics()
        except Exception as e:
            return {"error": f"통계 조회 실패: {str(e)}"}

    @app.get("/stem", response_class=HTMLResponse)
    async def stem_page():
        """STEM 도깨비 메인 페이지"""
        try:
            with open("index_stem.html", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "<h1>STEM 페이지를 찾을 수 없습니다</h1>"
