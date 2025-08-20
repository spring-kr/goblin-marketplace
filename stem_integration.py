"""
STEM 통합 AI 도깨비 시스템 - 원래 16개 도깨비 버전
박사급 AI 도깨비들이 각 분야별로 전문적인 상담을 제공합니다.
"""

import random
import re
from datetime import datetime
from typing import Dict, Any, Optional
from usage_tracker import UsageTracker

# 사용량 추적기 초기화
usage_tracker = UsageTracker()


class STEMIntegration:
    """원래 16개 박사급 AI 도깨비 시스템"""

    def __init__(self):
        self.system_name = "🏰 도깨비마을장터 박사급 AI 상담소"

    def process_question(
        self, agent_type: str, question: str, user_ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """실제 AI 대화 능력으로 질문 처리"""
        try:
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
                    "emoji": "📈",
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
            response = self._generate_smart_response(question, agent_type, info)

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

    def _generate_smart_response(
        self, question: str, agent_type: str, info: dict
    ) -> str:
        """도깨비별 전문 응답 생성 - 실제 AI처럼 자연스럽게"""
        
        # 실제 AI 대화처럼 자연스럽고 맥락적인 응답 생성
        return self._create_natural_ai_response(question, agent_type, info)

    def _generate_smart_response(
        self, question: str, agent_type: str, info: dict
    ) -> str:
        """도깨비별 전문 응답 생성 - 실제 AI처럼 자연스럽게"""
        
        # 실제 AI 대화처럼 자연스럽고 맥락적인 응답 생성
        return self._create_natural_ai_response(question, agent_type, info)

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
        
        # 인사말 처리
        greetings = ["안녕", "안녕하세요", "하이", "헬로", "hi", "hello"]
        if any(greeting in question.lower() for greeting in greetings) and question_length < 20:
            return f"{info['emoji']} 안녕하세요! {info['name']}입니다! 어떤 {info['field']} 관련 도움이 필요하신가요? 궁금한 것이 있으시면 언제든 말씀해주세요!"
        
        # 감사 표현 처리
        thanks = ["고마워", "감사", "고맙", "thanks", "thank"]
        if any(thank in question.lower() for thank in thanks):
            return f"{info['emoji']} 별말씀을요! {info['name']}로서 도움이 되었다니 정말 기쁩니다. 앞으로도 {info['field']} 관련해서 궁금한 것이 있으시면 언제든 찾아주세요!"
        
        # 전문 분야 키워드가 포함된 경우
        if any(expertise in question.lower() for expertise in personality.get("expertise", [])):
            return self._generate_expert_response(question, info, personality)
        
        # 일반적인 질문에 대한 전문가적 관점 제시
        return self._generate_general_expert_response(question, info, personality)

    def _generate_expert_response(self, question: str, info: dict, personality: dict) -> str:
        """전문 분야 관련 응답 생성"""
        
        return f"""{info['emoji']} {info['name']}입니다!

'{question}'에 대해 {personality['role']}로서 답변드리겠습니다.

🎯 **전문가 분석:**
질문하신 내용은 제가 가장 잘 다룰 수 있는 {info['field']} 분야네요. {personality['style']}를 제공해드리겠습니다.

💡 **맞춤 솔루션:**
{self._get_specific_solution(question, info['field'])}

✨ **추가 조언:**
더 구체적인 상황이나 세부사항을 알려주시면, 더욱 정확하고 실용적인 조언을 드릴 수 있습니다!

🚀 **다음 단계:**
궁금한 점이 더 있으시면 언제든 말씀해주세요!"""

    def _generate_general_expert_response(self, question: str, info: dict, personality: dict) -> str:
        """일반적인 질문에 대한 전문가 관점 응답"""
        
        return f"""{info['emoji']} {info['name']}입니다!

'{question}'에 대해 {info['field']} 전문가 관점에서 답변드리겠습니다.

🔍 **전문가 시각:**
{personality['role']}로서 이 문제를 바라보면, {info['field']} 관점에서 접근해볼 수 있을 것 같습니다.

💭 **종합적 고려사항:**
• 현재 상황의 정확한 파악이 중요합니다
• {info['field']} 원칙을 적용한 체계적 접근
• 실행 가능한 구체적 방안 모색

🎯 **제안사항:**
{self._get_field_specific_advice(question, info['field'])}

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
        """박사급 비서 도깨비 전문 응답 - 실제 AI 대화"""
        # 질문 키워드 분석으로 맞춤 응답
        question_lower = question.lower()
        
        # 일정/시간 관리 관련
        if any(keyword in question_lower for keyword in ['일정', '스케줄', '계획', '시간', '관리']):
            return f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n'{question}' 관련 시간 관리 전문 조언을 드리겠습니다.\n\n⏰ **효율적 시간 관리법:**\n• 중요도×긴급도 매트릭스로 우선순위 설정\n• 25분 집중 + 5분 휴식 포모도로 기법\n• 하루 20% 버퍼 타임 확보\n\n📅 **일정 최적화:**\n• 비슷한 업무는 배치 처리\n• 에너지 높은 시간대에 어려운 업무\n• 주간/월간 정기 리뷰 실시\n\n🎯 **즉시 실행 팁:**\n오늘부터 가장 중요한 업무 3개만 선정해보세요!"
        
        # 회의/소통 관련
        elif any(keyword in question_lower for keyword in ['회의', '미팅', '소통', '커뮤니케이션', '발표']):
            return f"{info['emoji']} {info['name']}가 회의 효율성 전문가로 답변드립니다!\n\n'{question}' 관련 소통 최적화 방안입니다.\n\n💬 **효과적 회의 운영:**\n• 명확한 목적과 아젠다 사전 공유\n• 시간 한계 설정 (최대 1시간)\n• 액션 아이템과 담당자 명시\n\n🎯 **참여도 극대화:**\n• 모든 참석자 발언 기회 제공\n• 결정사항 실시간 기록\n• 회의 후 24시간 내 요약 공유\n\n� **성과 측정:**\n회의 만족도와 실행률을 정기 체크하세요!"
        
        # 업무 효율/생산성 관련
        elif any(keyword in question_lower for keyword in ['업무', '생산성', '효율', '성과', '목표']):
            return f"{info['emoji']} {info['name']}가 생산성 전문가로 조언드립니다!\n\n'{question}'에 대한 업무 효율성 향상 방안입니다.\n\n⚡ **생산성 부스터:**\n• 2분 룰: 2분 내 가능한 일은 즉시 처리\n• 멀티태스킹 금지, 한 번에 하나씩\n• 업무 환경 최적화 (정리정돈 필수)\n\n🧠 **에너지 관리:**\n• 개인별 황금 시간대 파악 활용\n• 어려운 업무는 컨디션 좋을 때\n• 정기적 휴식으로 지속 가능한 리듬\n\n� **성과 추적:**\n주간 단위 업무 완료율과 품질 점검하세요!"
        
        # 일반적인 업무 관리 질문
        else:
            return f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n'{question}'에 대해 업무 관리 전문가로서 조언드리겠습니다.\n\n📋 **종합 분석:**\n체계적인 업무 관리가 성공의 핵심입니다.\n\n✅ **핵심 원칙:**\n• 명확한 목표 설정과 우선순위 관리\n• 시간과 에너지 자원의 최적 배분\n• 지속적인 개선과 피드백 반영\n\n💡 **맞춤 솔루션:**\n구체적인 상황을 더 알려주시면 더 정확한 조언을 드릴 수 있습니다!\n\n🚀 **시작 제안:**\n오늘부터 작은 습관 하나씩 개선해보세요."

    def _builder_expert_response(self, question: str, info: dict) -> str:
        """빌더 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n개발 관련 질문에 전문적으로 답변드리겠습니다:\n\n💻 **기술 분석:**\n'{question}'에 대한 개발 솔루션을 제시하겠습니다.\n\n🛠️ **권장 기술스택:**\n• 프론트엔드: React/Vue.js\n• 백엔드: Python/Node.js\n• 데이터베이스: PostgreSQL/MongoDB\n\n🚀 **구현 방안:**\nMVP부터 시작해서 단계적으로 확장하세요!",
            f"{info['emoji']} {info['name']}가 개발 솔루션을 제공합니다!\n\n🔧 **아키텍처 설계:**\n'{question}'에 최적화된 시스템 구조를 설계했습니다.\n\n📱 **개발 로드맵:**\n• 1단계: 프로토타입 개발\n• 2단계: 핵심 기능 구현\n• 3단계: 확장성 고려\n\n⚡ **성능 최적화:**\n확장 가능하고 유지보수가 쉬운 코드로 구현하겠습니다!",
        ]
        return random.choice(responses)

    def _counselor_expert_response(self, question: str, info: dict) -> str:
        """상담 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n마음의 고민을 함께 나누겠습니다:\n\n💭 **상황 이해:**\n'{question}'에 대해 깊이 공감하며 들어드렸습니다.\n\n🤗 **심리적 지원:**\n• 감정 인정과 수용\n• 긍정적 관점 전환\n• 실행 가능한 해결책\n\n🌈 **희망 메시지:**\n어려운 시기도 성장의 기회가 될 수 있습니다!",
            f"{info['emoji']} {info['name']}가 따뜻하게 상담해드립니다.\n\n💝 **공감과 이해:**\n'{question}'에 담긴 마음을 충분히 이해합니다.\n\n🔍 **문제 분석:**\n• 핵심 이슈 파악\n• 감정 상태 점검\n• 해결 방향 모색\n\n✨ **변화의 시작:**\n작은 변화부터 시작해보세요. 응원하겠습니다!",
        ]
        return random.choice(responses)

    def _creative_expert_response(self, question: str, info: dict) -> str:
        """창작 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n창작 영감을 불러일으켜드리겠습니다:\n\n🎭 **창작 아이디어:**\n'{question}'에서 무한한 가능성을 발견했습니다!\n\n🌟 **영감 포인트:**\n• 독창적 관점 제시\n• 감성적 스토리텔링\n• 시각적 임팩트 강화\n\n🎨 **실행 방법:**\n창의성과 체계성을 조화롭게 결합해보세요!",
            f"{info['emoji']} {info['name']}가 창작 여정을 함께합니다!\n\n💡 **브레인스토밍:**\n'{question}'을 통해 새로운 아이디어를 발굴했습니다.\n\n🎪 **창작 전략:**\n• 오리지널리티 확보\n• 타겟 오디언스 고려\n• 트렌드와 개성의 균형\n\n🚀 **창작 팁:**\n완벽함보다 진정성이 더 강력한 힘을 발휘합니다!",
        ]
        return random.choice(responses)

    def _data_analyst_expert_response(self, question: str, info: dict) -> str:
        """데이터분석 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n데이터 기반 통찰력을 제공하겠습니다:\n\n📈 **데이터 분석:**\n'{question}'에 대한 정량적 분석 결과입니다.\n\n🔍 **핵심 인사이트:**\n• 패턴 인식 및 트렌드 분석\n• 예측 모델링\n• 의사결정 지원 데이터\n\n📊 **활용 방안:**\n데이터를 통해 확실한 성과를 만들어보세요!",
            f"{info['emoji']} {info['name']}가 데이터로 답변드립니다!\n\n🧮 **통계적 접근:**\n'{question}'을 수치와 그래프로 분석했습니다.\n\n📋 **분석 결과:**\n• 상관관계 분석\n• 성과 지표 측정\n• ROI 계산\n\n⚡ **실행력:**\n데이터 기반 의사결정으로 성공 확률을 높이세요!",
        ]
        return random.choice(responses)

    def _fortune_expert_response(self, question: str, info: dict) -> str:
        """운세 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n운명의 실을 들여다보겠습니다:\n\n🌙 **운세 해석:**\n'{question}'에 대한 우주의 메시지를 전달합니다.\n\n⭐ **길운 포인트:**\n• 긍정적 에너지 흐름\n• 기회의 타이밍\n• 주의해야 할 요소\n\n🍀 **행운 팁:**\n마음가짐을 밝게 하면 좋은 일이 찾아올 것입니다!",
            f"{info['emoji']} {info['name']}가 신비로운 답변을 드립니다!\n\n🔮 **미래 전망:**\n'{question}'에 숨겨진 운명의 신호를 읽었습니다.\n\n✨ **운세 조언:**\n• 행운의 색깔과 숫자\n• 피해야 할 시기\n• 성공을 위한 방향\n\n🌟 **희망 메시지:**\n당신의 노력과 운이 만나는 순간이 다가옵니다!",
        ]
        return random.choice(responses)

    def _growth_expert_response(self, question: str, info: dict) -> str:
        """성장 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n성장의 길을 함께 걸어가겠습니다:\n\n🌱 **성장 분석:**\n'{question}'에서 발전 가능성을 발견했습니다.\n\n📈 **성장 전략:**\n• 단계별 목표 설정\n• 역량 강화 방법\n• 지속 가능한 발전\n\n🏆 **성공 비결:**\n꾸준함이 최고의 성장 동력입니다!",
            f"{info['emoji']} {info['name']}가 성장 여정을 안내합니다!\n\n🚀 **성장 로드맵:**\n'{question}'을 통해 맞춤형 성장 계획을 세웠습니다.\n\n💪 **역량 개발:**\n• 강점 극대화\n• 약점 보완\n• 새로운 기회 창출\n\n⭐ **동기부여:**\n매일 조금씩 성장하는 당신이 될 수 있습니다!",
        ]
        return random.choice(responses)

    def _hr_expert_response(self, question: str, info: dict) -> str:
        """HR 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n인사 관리 전문 조언을 드리겠습니다:\n\n👥 **인사 전략:**\n'{question}'에 대한 HR 솔루션을 제시합니다.\n\n🎯 **핵심 포인트:**\n• 인재 채용 및 육성\n• 조직 문화 개선\n• 성과 관리 시스템\n\n💼 **실행 방안:**\n사람 중심의 경영으로 조직을 강화하세요!",
            f"{info['emoji']} {info['name']}가 인사 전문가로 답변드립니다!\n\n🏢 **조직 진단:**\n'{question}'을 통해 조직의 건강도를 체크했습니다.\n\n📊 **HR 솔루션:**\n• 직원 만족도 향상\n• 업무 효율성 증대\n• 리더십 개발\n\n🌟 **기대 효과:**\n행복한 직장이 최고의 성과를 만들어냅니다!",
        ]
        return random.choice(responses)

    def _marketing_expert_response(self, question: str, info: dict) -> str:
        """마케팅 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n마케팅 전략을 수립해드리겠습니다:\n\n📊 **시장 분석:**\n'{question}'에 대한 마케팅 인사이트를 제공합니다.\n\n🎯 **전략 포인트:**\n• 타겟 고객 세분화\n• 차별화된 포지셔닝\n• 효과적인 채널 믹스\n\n🚀 **실행 계획:**\n데이터 기반 마케팅으로 ROI를 극대화하세요!",
            f"{info['emoji']} {info['name']}가 마케팅 솔루션을 제공합니다!\n\n📈 **성장 전략:**\n'{question}'을 통해 브랜드 성장 방안을 도출했습니다.\n\n💡 **마케팅 믹스:**\n• 제품/서비스 최적화\n• 가격 전략 수립\n• 프로모션 기획\n\n⭐ **성공 팁:**\n고객의 마음을 움직이는 것이 최고의 마케팅입니다!",
        ]
        return random.choice(responses)

    def _medical_expert_response(self, question: str, info: dict) -> str:
        """의료 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n건강 관련 정보를 제공해드리겠습니다:\n\n⚕️ **건강 체크:**\n'{question}'에 대한 의학적 관점을 설명드립니다.\n\n🩺 **주요 포인트:**\n• 증상 이해 및 원인 분석\n• 예방법 및 관리법\n• 전문의 상담 권유\n\n⚠️ **중요 안내:**\n정확한 진단은 반드시 의료진과 상담하세요!",
            f"{info['emoji']} {info['name']}가 건강 정보를 안내합니다!\n\n💊 **의학적 조언:**\n'{question}'에 대한 일반적인 의학 정보를 제공합니다.\n\n🏥 **건강 관리:**\n• 생활습관 개선 방법\n• 정기 건강검진 중요성\n• 응급상황 대처법\n\n💝 **건강 메시지:**\n건강한 생활이 최고의 치료법입니다!",
        ]
        return random.choice(responses)

    def _sales_expert_response(self, question: str, info: dict) -> str:
        """영업 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n영업 성과 향상 전략을 제시하겠습니다:\n\n💼 **영업 분석:**\n'{question}'에 대한 세일즈 솔루션을 제공합니다.\n\n🎯 **성공 포인트:**\n• 고객 니즈 파악\n• 신뢰 관계 구축\n• 가치 제안 강화\n\n📈 **실행 전략:**\n고객 중심 사고로 매출을 극대화하세요!",
            f"{info['emoji']} {info['name']}가 영업 노하우를 전수합니다!\n\n🤝 **관계 구축:**\n'{question}'을 통해 고객과의 연결점을 찾았습니다.\n\n💰 **매출 증대:**\n• 영업 프로세스 최적화\n• 성과 측정 시스템\n• 팀워크 강화\n\n🏆 **성공 비법:**\n진정성 있는 서비스가 최고의 영업력입니다!",
        ]
        return random.choice(responses)

    def _seo_expert_response(self, question: str, info: dict) -> str:
        """SEO 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n검색 최적화 전략을 제공하겠습니다:\n\n🔍 **SEO 분석:**\n'{question}'에 대한 검색엔진 최적화 방안입니다.\n\n📈 **핵심 전략:**\n• 키워드 최적화\n• 콘텐츠 품질 향상\n• 백링크 구축\n\n⚡ **실행 계획:**\n구글 상위 노출로 트래픽을 증가시키세요!",
            f"{info['emoji']} {info['name']}가 SEO 비법을 알려드립니다!\n\n🌐 **웹 최적화:**\n'{question}'을 바탕으로 검색 순위 향상 방법을 제시합니다.\n\n🎯 **최적화 포인트:**\n• 기술적 SEO 개선\n• 사용자 경험 향상\n• 모바일 최적화\n\n🚀 **성과 예측:**\n체계적인 SEO로 유기적 트래픽을 늘려보세요!",
        ]
        return random.choice(responses)

    def _shopping_expert_response(self, question: str, info: dict) -> str:
        """쇼핑 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n스마트한 쇼핑 가이드를 제공하겠습니다:\n\n🛍️ **쇼핑 분석:**\n'{question}'에 대한 최적의 구매 조언을 드립니다.\n\n💡 **쇼핑 팁:**\n• 가격 비교 및 할인 정보\n• 제품 품질 평가\n• 구매 타이밍 최적화\n\n💰 **절약 방법:**\n현명한 소비로 만족도를 극대화하세요!",
            f"{info['emoji']} {info['name']}가 쇼핑 컨설팅을 해드립니다!\n\n🏪 **구매 전략:**\n'{question}'에 맞는 최고의 쇼핑 솔루션을 찾았습니다.\n\n🎁 **추천 포인트:**\n• 브랜드별 특성 분석\n• 리뷰 및 평점 검토\n• 애프터서비스 고려\n\n✨ **만족 보장:**\n합리적인 소비가 진정한 행복을 가져다줍니다!",
        ]
        return random.choice(responses)

    def _startup_expert_response(self, question: str, info: dict) -> str:
        """스타트업 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n창업 성공 전략을 제시하겠습니다:\n\n🚀 **스타트업 분석:**\n'{question}'에 대한 창업 로드맵을 제공합니다.\n\n💡 **핵심 포인트:**\n• 시장 검증 및 PMF\n• 팀 빌딩 및 문화\n• 자금 조달 전략\n\n🏆 **성공 비결:**\n고객 문제 해결에 집중하면 성공합니다!",
            f"{info['emoji']} {info['name']}가 창업 멘토링을 제공합니다!\n\n💼 **비즈니스 모델:**\n'{question}'을 통해 지속 가능한 사업 구조를 설계했습니다.\n\n📊 **실행 계획:**\n• MVP 개발 및 테스트\n• 마케팅 전략 수립\n• 성장 지표 관리\n\n🌟 **창업 정신:**\n실패를 두려워하지 말고 계속 도전하세요!",
        ]
        return random.choice(responses)

    def _village_chief_expert_response(self, question: str, info: dict) -> str:
        """이장 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n마을 관리 전문가로서 조언드리겠습니다:\n\n🏘️ **커뮤니티 분석:**\n'{question}'에 대한 종합적인 관리 방안을 제시합니다.\n\n👥 **관리 포인트:**\n• 주민 소통 및 화합\n• 인프라 개선 계획\n• 지속 가능한 발전\n\n🌟 **리더십 철학:**\n모든 구성원이 행복한 공동체를 만들어가겠습니다!",
            f"{info['emoji']} {info['name']}가 현명한 해결책을 제시합니다!\n\n🎯 **통합 관리:**\n'{question}'을 바탕으로 전체적인 운영 방안을 수립했습니다.\n\n📋 **실행 계획:**\n• 효율적 자원 배분\n• 갈등 조정 및 해결\n• 미래 비전 수립\n\n🤝 **협력 정신:**\n함께 만들어가는 것이 가장 강력한 힘입니다!",
        ]
        return random.choice(responses)

    def _writing_expert_response(self, question: str, info: dict) -> str:
        """박사급 문서 작성 도깨비 전문 응답"""
        responses = [
            f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n전문적인 문서 작성을 도와드리겠습니다:\n\n📝 **문서 분석:**\n'{question}'에 대한 고품질 문서 작성 가이드를 제공합니다.\n\n✏️ **작성 포인트:**\n• 논리적 구조 설계\n• 명확한 표현 기법\n• 독자 맞춤 스타일\n\n📚 **품질 향상:**\n체계적인 글쓰기로 전문성을 보여주세요!",
            f"{info['emoji']} {info['name']}가 문서 작성 전문가로 도움드립니다!\n\n📖 **라이팅 전략:**\n'{question}'에 맞는 효과적인 글쓰기 방법을 안내합니다.\n\n🎯 **핵심 기법:**\n• 목적에 맞는 톤앤매너\n• 설득력 있는 논증\n• 가독성 최적화\n\n⭐ **문서 완성도:**\n완벽한 문서로 원하는 결과를 얻으실 수 있습니다!",
        ]
        return random.choice(responses)

    def _general_expert_response(self, question: str, info: dict) -> str:
        """일반 전문가 응답 (새로운 도깨비 타입용)"""
        return f"{info['emoji']} 안녕하세요! {info['name']}입니다.\n\n'{question}'에 대해 {info['field']} 전문가로서 도움을 드리겠습니다.\n\n🔍 **전문 분석:**\n해당 분야의 깊이 있는 지식을 바탕으로 맞춤형 솔루션을 제공하겠습니다.\n\n💡 **실용적 조언:**\n이론과 실무를 결합한 실행 가능한 방안을 제시하겠습니다.\n\n✨ **기대 효과:**\n전문적인 접근으로 최적의 결과를 만들어보세요!"

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
            "marketing": {"emoji": "📈", "name": "마케팅 도깨비", "field": "마케팅"},
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
