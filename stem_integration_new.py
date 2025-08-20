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
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
        except Exception:
            self.conversation_history = {}

    def _save_conversation_history(self):
        """대화 기록 저장"""
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
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
            "more_detail": ["구체적으로", "더 자세히", "세부적으로", "상세하게", "더 알려주세요", "자세히 설명"],
            "example": ["예시", "사례", "실제", "예를 들어", "구체적인 예", "실습"],
            "how_to": ["어떻게", "방법", "단계", "절차", "프로세스"],
            "advanced": ["고급", "심화", "전문적", "더 깊이", "고도화"],
            "practical": ["실무", "현실적", "실제로", "바로", "실행"],
            "tools": ["도구", "툴", "프로그램", "소프트웨어", "앱"],
            "troubleshooting": ["문제", "해결", "오류", "안될때", "실패"]
        }
        
        detected_intent = "general"
        for intent, keywords in follow_up_indicators.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_intent = intent
                break
        
        return {
            "intent": detected_intent,
            "is_follow_up": len(previous_topics) > 0,
            "depth_level": len(previous_topics) + 1
        }

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
            previous_topics = [conv.get("topic", "") for conv in previous_conversations[-3:]]  # 최근 3개만
            
            # 후속 질문 의도 분석
            follow_up_analysis = self._analyze_follow_up_intent(question, previous_topics)

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
            response = self._create_contextual_ai_response(
                question, agent_type, info, previous_conversations, follow_up_analysis
            )

            # 현재 대화를 기록에 추가
            current_conversation = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "topic": self._extract_topic(question),
                "intent": follow_up_analysis["intent"],
                "depth": follow_up_analysis["depth_level"]
            }
            
            if conversation_key not in self.conversation_history:
                self.conversation_history[conversation_key] = []
            
            self.conversation_history[conversation_key].append(current_conversation)
            
            # 최근 10개 대화만 유지
            if len(self.conversation_history[conversation_key]) > 10:
                self.conversation_history[conversation_key] = self.conversation_history[conversation_key][-10:]
            
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
                    "intent": follow_up_analysis["intent"]
                }
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
            "상담": ["상담", "고민", "스트레스", "관계"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        
        return "일반상담"

    def _create_contextual_ai_response(
        self, question: str, agent_type: str, info: dict, previous_conversations: list, follow_up_analysis: dict
    ) -> str:
        """컨텍스트를 고려한 AI 응답 생성"""
        
        # 후속 질문인지 확인
        if follow_up_analysis["is_follow_up"] and follow_up_analysis["depth_level"] > 1:
            return self._create_follow_up_response(question, agent_type, info, previous_conversations, follow_up_analysis)
        else:
            return self._create_natural_ai_response(question, agent_type, info)

    def _create_follow_up_response(
        self, question: str, agent_type: str, info: dict, previous_conversations: list, follow_up_analysis: dict
    ) -> str:
        """후속 질문에 대한 심화 응답 생성"""
        
        # 이전 주제들 파악
        previous_topics = [conv.get("topic", "") for conv in previous_conversations[-3:]]
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
            intro = f"{info['emoji']} 더 구체적으로 설명드리겠습니다! ({depth}단계 심화)"
            focus = "🔍 **세부 분석:**"
        elif intent == "example":
            intro = f"{info['emoji']} 실제 사례로 설명드리겠습니다!"
            focus = "📚 **구체적 사례:**"
        elif intent == "how_to":
            intro = f"{info['emoji']} 단계별 방법을 자세히 알려드리겠습니다!"
            focus = "📋 **상세 실행 방법:**"
        elif intent == "practical":
            intro = f"{info['emoji']} 실무에 바로 적용할 수 있는 방법을 알려드리겠습니다!"
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
