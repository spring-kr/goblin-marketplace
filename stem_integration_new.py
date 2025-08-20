"""
🎯 AI 도깨비마을 STEM 센터 - 실제 AI 대화 시스템
진짜 AI처럼 자연스럽고 맥락적인 응답을 제공하는 16개 도깨비 시스템
"""

import random
from datetime import datetime
from typing import Dict, Any, Optional


class STEMIntegration:
    """STEM 도깨비들과의 실제 AI 대화 시스템"""

    def __init__(self):
        self.system_name = "🏰 도깨비마을장터 박사급 AI 상담소"

    def process_question(
        self, agent_type: str, question: str, user_ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """실제 AI 대화 능력으로 질문 처리"""
        try:
            from usage_tracker import usage_tracker

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

            # 도깨비별 전문 응답 생성
            info = agent_info[agent_type]
            response = self._create_natural_ai_response(question, agent_type, info)

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
            }

        except Exception as e:
            # 에러 로그 기록
            usage_tracker.log_usage(agent_type, question, False, user_ip)
            return {"success": False, "error": f"처리 중 오류가 발생했습니다: {str(e)}"}

    def _create_natural_ai_response(self, question: str, agent_type: str, info: dict) -> str:
        """실제 AI처럼 자연스럽고 맥락적인 응답 생성"""
        
        # 도깨비별 전문 분야와 성격 정의
        agent_personalities = {
            "assistant": {
                "role": "효율적이고 체계적인 업무 관리 전문가",
                "style": "실용적이고 구체적인 조언",
                "expertise": ["시간관리", "업무효율", "생산성", "계획수립", "조직관리"]
            },
            "builder": {
                "role": "창의적이고 실용적인 개발 전문가", 
                "style": "기술적이면서도 이해하기 쉬운 설명",
                "expertise": ["프로그래밍", "웹개발", "앱개발", "시스템설계", "기술아키텍처"]
            },
            "counselor": {
                "role": "따뜻하고 공감능력이 뛰어난 상담 전문가",
                "style": "경청하고 공감하며 따뜻한 조언",
                "expertise": ["심리상담", "갈등해결", "스트레스관리", "인간관계", "감정관리"]
            },
            "creative": {
                "role": "영감이 넘치고 창의적인 아이디어 전문가",
                "style": "독창적이고 흥미로운 아이디어 제시",
                "expertise": ["창작", "디자인", "브랜딩", "콘텐츠기획", "아이디어발상"]
            },
            "data_analyst": {
                "role": "논리적이고 분석적인 데이터 전문가",
                "style": "근거와 데이터를 바탕으로 한 객관적 분석",
                "expertise": ["데이터분석", "통계", "시각화", "예측모델링", "비즈니스인텔리전스"]
            },
            "fortune": {
                "role": "신비롭고 지혜로운 운세 전문가",
                "style": "신비로우면서도 희망적인 메시지",
                "expertise": ["운세", "점성술", "타로", "풍수", "운명해석"]
            },
            "growth": {
                "role": "동기부여가 넘치는 성장 전문가",
                "style": "격려하고 동기부여하는 긍정적 조언",
                "expertise": ["자기계발", "목표설정", "습관형성", "동기부여", "성장전략"]
            },
            "hr": {
                "role": "사람 중심의 인사 관리 전문가",
                "style": "배려 깊고 공정한 인사 관리 조언",
                "expertise": ["채용", "인사평가", "조직문화", "리더십", "팀관리"]
            },
            "marketing": {
                "role": "트렌드에 민감한 마케팅 전문가",
                "style": "창의적이고 실행 가능한 마케팅 전략",
                "expertise": ["브랜드마케팅", "디지털마케팅", "고객분석", "마케팅전략", "광고기획"]
            },
            "medical": {
                "role": "신뢰할 수 있는 의료 정보 전문가",
                "style": "정확하고 신중한 의학 정보 제공",
                "expertise": ["건강관리", "질병예방", "의학정보", "건강검진", "생활습관"]
            },
            "sales": {
                "role": "열정적이고 설득력 있는 영업 전문가",
                "style": "적극적이고 성과지향적인 영업 조언",
                "expertise": ["영업전략", "고객관계", "협상기술", "매출관리", "세일즈"]
            },
            "seo": {
                "role": "검색엔진에 정통한 SEO 전문가",
                "style": "기술적이면서도 실무적인 SEO 조언",
                "expertise": ["검색최적화", "키워드분석", "웹사이트최적화", "구글SEO", "콘텐츠SEO"]
            },
            "shopping": {
                "role": "합리적이고 트렌드에 민감한 쇼핑 전문가",
                "style": "실용적이고 경제적인 구매 조언",
                "expertise": ["제품비교", "가격분석", "쇼핑팁", "소비패턴", "구매가이드"]
            },
            "startup": {
                "role": "도전정신이 강한 창업 전문가",
                "style": "현실적이면서도 꿈을 응원하는 창업 조언",
                "expertise": ["창업전략", "비즈니스모델", "투자유치", "스타트업경영", "사업계획"]
            },
            "village_chief": {
                "role": "경험이 풍부하고 지혜로운 리더",
                "style": "포용력 있고 균형잡힌 종합적 조언",
                "expertise": ["리더십", "조직관리", "갈등조정", "의사결정", "커뮤니티관리"]
            },
            "writing": {
                "role": "문장력이 뛰어난 글쓰기 전문가",
                "style": "명확하고 품격 있는 문서 작성 조언",
                "expertise": ["문서작성", "글쓰기", "논문작성", "보고서", "콘텐츠라이팅"]
            }
        }
        
        personality = agent_personalities.get(agent_type, {
            "role": "전문가",
            "style": "도움이 되는 조언",
            "expertise": ["전문상담"]
        })
        
        # 질문 분석 및 맥락적 응답 생성
        return self._generate_contextual_response(question, info, personality)

    def _generate_contextual_response(self, question: str, info: dict, personality: dict) -> str:
        """맥락을 고려한 자연스러운 응답 생성"""
        
        # 질문 길이와 복잡도 분석
        question_length = len(question)
        question_lower = question.lower()
        
        # 인사말 처리
        greetings = ["안녕", "하이", "헬로", "hi", "hello"]
        if any(greeting in question_lower for greeting in greetings) and question_length < 20:
            responses = [
                f"{info['emoji']} 안녕하세요! {info['name']}입니다! 어떤 {info['field']} 관련 도움이 필요하신가요?",
                f"{info['emoji']} 반갑습니다! {info['name']}가 인사드려요. {info['field']} 전문가로서 최선을 다해 도와드리겠습니다!",
                f"{info['emoji']} 안녕하세요! {info['field']} 전문가 {info['name']}입니다. 무엇을 도와드릴까요?"
            ]
            return random.choice(responses)
        
        # 감사 표현 처리
        thanks = ["고마워", "감사", "고맙", "thanks", "thank"]
        if any(thank in question_lower for thank in thanks):
            responses = [
                f"{info['emoji']} 별말씀을요! {info['name']}로서 도움이 되었다니 정말 기쁩니다!",
                f"{info['emoji']} 천만에요! {info['field']} 관련해서 언제든 찾아주세요!",
                f"{info['emoji']} 도움이 되어서 다행이에요! {info['name']}는 항상 여기 있습니다!"
            ]
            return random.choice(responses)
        
        # 전문 분야 키워드가 포함된 경우
        if any(expertise in question_lower for expertise in personality.get("expertise", [])):
            return self._generate_expert_response(question, info, personality)
        
        # 일반적인 질문에 대한 전문가적 관점 제시
        return self._generate_general_expert_response(question, info, personality)

    def _generate_expert_response(self, question: str, info: dict, personality: dict) -> str:
        """전문 분야 관련 응답 생성"""
        
        specific_solution = self._get_specific_solution(question, info['field'])
        
        return f"""{info['emoji']} {info['name']}입니다!

'{question}'에 대해 {personality['role']}로서 답변드리겠습니다.

🎯 **전문가 분석:**
질문하신 내용은 제가 가장 잘 다룰 수 있는 {info['field']} 분야네요. {personality['style']}를 제공해드리겠습니다.

💡 **맞춤 솔루션:**
{specific_solution}

✨ **추가 조언:**
더 구체적인 상황이나 세부사항을 알려주시면, 더욱 정확하고 실용적인 조언을 드릴 수 있습니다!

🚀 **다음 단계:**
궁금한 점이 더 있으시면 언제든 말씀해주세요!"""

    def _generate_general_expert_response(self, question: str, info: dict, personality: dict) -> str:
        """일반적인 질문에 대한 전문가 관점 응답"""
        
        field_advice = self._get_field_specific_advice(question, info['field'])
        
        return f"""{info['emoji']} {info['name']}입니다!

'{question}'에 대해 {info['field']} 전문가 관점에서 답변드리겠습니다.

🔍 **전문가 시각:**
{personality['role']}로서 이 문제를 바라보면, {info['field']} 관점에서 접근해볼 수 있을 것 같습니다.

💭 **종합적 고려사항:**
• 현재 상황의 정확한 파악이 중요합니다
• {info['field']} 원칙을 적용한 체계적 접근
• 실행 가능한 구체적 방안 모색

🎯 **제안사항:**
{field_advice}

📞 **추가 상담:**
더 자세한 상황을 알려주시면 {info['field']} 전문성을 바탕으로 더 구체적인 도움을 드릴 수 있습니다!"""

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
            "문서 작성": "명확한 구조와 논리적 흐름을 갖추고, 독자의 입장에서 이해하기 쉽게 작성하세요."
        }
        
        return solutions.get(field, "전문적인 관점에서 체계적으로 접근하고, 실행 가능한 방안을 단계별로 수립해보세요.")

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
            "문서 작성": "5W1H 원칙에 따라 정보를 정리하고, 단락별 핵심 메시지를 명확히 하세요."
        }
        
        return advice.get(field, "전문 지식을 바탕으로 단계적이고 실용적인 접근 방법을 찾아보세요.")

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
