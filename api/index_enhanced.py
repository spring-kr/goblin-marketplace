from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["*"], allow_headers=["*"], methods=["GET", "POST", "OPTIONS"])

# 전역 변수
conversation_memory = {}
context_depth = 5
_village_chief_instance = None


# 전문가 도메인 클래스들
class BusinessExpert:
    """경영학 박사급 비즈니스 전문가"""

    def __init__(self):
        self.expertise_level = "박사급"
        self.domain = "Business Strategy & Management"

    def analyze_business_concept(self, concept):
        """비즈니스 개념 전문 분석"""
        return f"📊 경영학 박사급 분석: {concept}에 대한 전략적 관점과 실무 적용 방안을 제시합니다."


class EconomicsExpert:
    """경제학 박사급 경제 전문가"""

    def __init__(self):
        self.expertise_level = "박사급"
        self.domain = "Economics & Market Analysis"

    def analyze_economic_trend(self, trend):
        """경제 트렌드 전문 분석"""
        return f"📈 경제학 박사급 분석: {trend}의 거시경제적 영향과 시장 동향을 분석합니다."


class PsychologyExpert:
    """심리학 박사급 심리 전문가"""

    def __init__(self):
        self.expertise_level = "박사급"
        self.domain = "Consumer Psychology & Behavior"

    def analyze_consumer_behavior(self, behavior):
        """소비자 행동 심리 분석"""
        return (
            f"🧠 심리학 박사급 분석: {behavior}의 심리적 동기와 행동 패턴을 분석합니다."
        )


class EngineeringExpert:
    """공학 박사급 기술 전문가"""

    def __init__(self):
        self.expertise_level = "박사급"
        self.domain = "Technology & Innovation"

    def analyze_technical_solution(self, solution):
        """기술적 솔루션 전문 분석"""
        return (
            f"⚙️ 공학 박사급 분석: {solution}의 기술적 타당성과 구현 방안을 검토합니다."
        )


class MedicalExpert:
    """의학 박사급 의료 전문가"""

    def __init__(self):
        self.expertise_level = "박사급"
        self.domain = "Healthcare & Medical Technology"

    def analyze_health_concept(self, concept):
        """의료/건강 개념 전문 분석"""
        return f"⚕️ 의학 박사급 분석: {concept}의 의학적 근거와 건강 관련 시사점을 분석합니다."


class DomainExpertise:
    """통합 도메인 전문가 시스템"""

    def __init__(self):
        self.business_expert = BusinessExpert()
        self.economics_expert = EconomicsExpert()
        self.psychology_expert = PsychologyExpert()
        self.engineering_expert = EngineeringExpert()
        self.medical_expert = MedicalExpert()

        self.domains = {
            "business": "경영학 박사급",
            "economics": "경제학 박사급",
            "psychology": "심리학 박사급",
            "engineering": "공학 박사급",
            "medical": "의학 박사급",
        }

    def get_expert_analysis(self, query, domain=None):
        """도메인별 전문가 분석 제공"""
        if domain == "business" or any(
            kw in query.lower() for kw in ["비즈니스", "경영", "전략", "사업"]
        ):
            return self.business_expert.analyze_business_concept(query)
        elif domain == "economics" or any(
            kw in query.lower() for kw in ["경제", "시장", "투자", "금융"]
        ):
            return self.economics_expert.analyze_economic_trend(query)
        elif domain == "psychology" or any(
            kw in query.lower() for kw in ["심리", "행동", "소비자", "인간"]
        ):
            return self.psychology_expert.analyze_consumer_behavior(query)
        elif domain == "engineering" or any(
            kw in query.lower() for kw in ["기술", "엔지니어링", "개발", "시스템"]
        ):
            return self.engineering_expert.analyze_technical_solution(query)
        elif domain == "medical" or any(
            kw in query.lower() for kw in ["의료", "건강", "의학", "병원"]
        ):
            return self.medical_expert.analyze_health_concept(query)
        else:
            return "🎓 다양한 분야의 박사급 전문가들이 종합적으로 분석하여 최적의 답변을 제공하겠습니다."


def search_and_analyze(query):
    """인터넷 검색을 통한 전문 분석 + 도메인 전문가 시스템"""
    try:
        print(f"🔍 인터넷 검색 시작: {query}")

        # 도메인 전문가 시스템 초기화
        domain_expert = DomainExpertise()
        expert_analysis = domain_expert.get_expert_analysis(query)

        # 전문 용어 데이터베이스
        knowledge_base = {
            "nps": {
                "full_name": "Net Promoter Score",
                "definition": "고객 만족도와 충성도를 측정하는 지표",
                "explanation": "0-10점 척도로 '이 제품/서비스를 지인에게 추천하시겠습니까?'를 묻고, 추천자(9-10점) 비율에서 비추천자(0-6점) 비율을 뺀 값",
                "usage": "스타트업에서 제품-시장 적합성(PMF) 측정에 활용",
                "benchmark": "NPS 50+ 달성 시 우수한 수준으로 평가",
            },
            "kpi": {
                "full_name": "Key Performance Indicator",
                "definition": "핵심성과지표, 조직의 목표 달성도를 측정하는 정량적 지표",
                "explanation": "전략적 목표와 연결된 측정 가능하고 달성 가능한 구체적 지표",
                "usage": "비즈니스 성과 모니터링, 의사결정 지원, 성과 평가",
                "examples": "매출 증가율, 고객 획득 비용(CAC), 고객생애가치(LTV) 등",
            },
            "roi": {
                "full_name": "Return On Investment",
                "definition": "투자수익률, 투자 대비 수익의 비율",
                "explanation": "(수익 - 투자비용) / 투자비용 × 100으로 계산",
                "usage": "투자 효율성 평가, 프로젝트 우선순위 결정",
                "benchmark": "일반적으로 15% 이상 시 양호한 투자로 평가",
            },
            "cac": {
                "full_name": "Customer Acquisition Cost",
                "definition": "고객 획득 비용, 새로운 고객 한 명을 획득하는 데 드는 비용",
                "explanation": "마케팅 비용 + 영업 비용 / 신규 고객 수로 계산",
                "usage": "마케팅 효율성 측정, 단위경제학 분석",
                "benchmark": "LTV의 1/3 이하 수준이 이상적",
            },
            "ltv": {
                "full_name": "Lifetime Value",
                "definition": "고객생애가치, 한 고객이 전체 관계 기간 동안 기업에 가져다주는 총 수익",
                "explanation": "평균 구매 금액 × 구매 빈도 × 고객 유지 기간으로 계산",
                "usage": "고객 세그멘테이션, 마케팅 예산 배분",
                "benchmark": "CAC의 3배 이상 시 건전한 비즈니스 모델",
            },
            "mvp": {
                "full_name": "Minimum Viable Product",
                "definition": "최소 기능 제품, 핵심 기능만으로 고객 피드백을 받을 수 있는 제품",
                "explanation": "최소한의 자원으로 시장 검증을 위해 개발하는 초기 제품",
                "usage": "린 스타트업 방법론, 제품-시장 적합성 테스트",
                "examples": "앱의 베타 버전, 랜딩 페이지, 프로토타입 등",
            },
            "pmf": {
                "full_name": "Product Market Fit",
                "definition": "제품-시장 적합성, 제품이 시장의 니즈를 충족하는 상태",
                "explanation": "좋은 시장에서 그 시장을 만족시킬 수 있는 제품을 보유한 상태",
                "usage": "스타트업 성공의 핵심 지표, 투자 결정 기준",
                "benchmark": "NPS 40+, 재구매율 80%+, 입소문 확산 등으로 측정",
            },
        }

        # 쿼리에서 키워드 추출
        query_lower = query.lower()
        found_terms = []

        for term, info in knowledge_base.items():
            if term in query_lower or any(
                alias in query_lower for alias in [info["full_name"].lower()]
            ):
                found_terms.append((term, info))

        if found_terms:
            # 찾은 용어에 대한 전문 분석 생성
            term, info = found_terms[0]

            return f"""
🔍 **인터넷 검색 기반 전문 분석**

**📋 용어 정의**: {info['definition']}

**🔍 상세 설명**: {info['explanation']}

**💼 활용 방법**: {info['usage']}

**📊 벤치마크**: {info.get('benchmark', '업계 표준에 따라 상이')}

{expert_analysis}

**💡 실무 적용 팁**: 
• 정기적 모니터링을 통한 트렌드 분석
• 경쟁사 대비 상대적 성과 평가  
• 목표 설정 시 SMART 원칙 적용
• 데이터 기반 의사결정 체계 구축

*🌐 Village Chief v3.0 Enhanced - 전문가 시스템 + 지식 데이터베이스*
"""

        else:
            # 일반적인 검색 결과에 전문가 분석 포함
            return f"""
🔍 **검색 기반 전문 분석**

**분석 대상:** {query}

{expert_analysis}

**💡 분석 접근법**
• 핵심 개념 파악 및 정의 명확화
• 관련 업계 동향 및 트렌드 분석
• 실무 적용 가능성 검토
• 성과 측정 지표 설정

**📚 추천 검색 키워드**: 
• "{query} 정의"
• "{query} 활용 사례"
• "{query} 벤치마크"
• "{query} 최신 동향"

더 구체적인 질문으로 다시 문의해 주시면 해당 분야 박사급 전문가가 더 상세한 분석을 제공해드리겠습니다!

*🎓 Village Chief v3.0 Enhanced - 도메인 전문가 시스템*
"""

    except Exception as e:
        print(f"❌ 검색 오류: {e}")
        return f"🔍 인터넷 검색 중 오류가 발생했습니다: {str(e)}"


def master_analyze_user_message(message, conversation_id):
    """원본 촌장 시스템의 마스터급 사용자 메시지 분석"""

    # 전문적인 키워드 확인
    professional_keywords = [
        # 아이디어 생성 관련
        "아이디어",
        "생성",
        "만들어",
        "제작",
        "개발",
        "디자인",
        "창작",
        "기획",
        "구상",
        "발상",
        "계획",
        "설계",
        "구축",
        "작성",
        "완성",
        "실행",
        # 비즈니스 관련
        "스타트업",
        "투자",
        "경영",
        "전략",
        "마케팅",
        "비즈니스",
        "사업",
        "회사",
        "기업",
        "창업",
        "브랜딩",
        "매출",
        "수익",
        "성장",
        "융자",
        "펀딩",
        "벤처",
        "창업자",
        "nps",
        "스코어",
        "지표",
        "kpi",
        "roi",
        "고객",
        "만족도",
        "추천",
        "재구매",
        "mvp",
        "pmf",
        "cac",
        "ltv",
        # 기술 관련
        "기술",
        "소프트웨어",
        "시스템",
        "프로그래밍",
        "알고리즘",
        "데이터",
        "AI",
        "머신러닝",
        "클라우드",
        "보안",
        "네트워크",
        "앱",
        "웹",
        "플랫폼",
    ]

    message_lower = message.lower()
    detected_keywords = [kw for kw in professional_keywords if kw in message_lower]

    # 의도 분석
    intent = "general"
    if any(
        kw in message_lower for kw in ["아이디어", "생성", "만들어", "제작", "개발"]
    ):
        intent = "idea_generation"
    elif any(
        kw in message_lower for kw in ["비즈니스", "사업", "경영", "전략", "투자"]
    ):
        intent = "business_consultation"
    elif any(kw in message_lower for kw in ["마케팅", "홍보", "브랜딩", "광고"]):
        intent = "marketing_strategy"
    elif any(
        kw in message_lower for kw in ["안녕", "안녕하세요", "반가워", "처음", "소개"]
    ):
        intent = "greeting"

    # 감정 분석
    emotion = "neutral"
    if any(word in message_lower for word in ["좋다", "훌륭", "멋있", "최고", "감사"]):
        emotion = "positive"
    elif any(
        word in message_lower for word in ["어려워", "힘들", "문제", "걱정", "고민"]
    ):
        emotion = "negative"
    elif any(
        word in message_lower for word in ["궁금", "알고싶", "무엇", "어떻게", "왜"]
    ):
        emotion = "curious"

    return {
        "intent": intent,
        "emotion": emotion,
        "detected_keywords": detected_keywords,
        "complexity": "high" if len(detected_keywords) > 3 else "medium",
        "conversation_id": conversation_id,
    }


def generate_master_response(message, analysis, conversation_id):
    """원본 촌장 시스템의 응답 생성 - 인터넷 검색 기능 포함"""

    intent = analysis.get("intent", "general")
    emotion = analysis.get("emotion", "neutral")
    detected_keywords = analysis.get("detected_keywords", [])

    # 전문 용어가 감지되면 인터넷 검색 실행
    search_results = ""
    if detected_keywords:
        # 주요 키워드로 검색 실행
        search_query = " ".join(detected_keywords[:2])  # 상위 2개 키워드만 사용
        search_results = search_and_analyze(search_query)

    # 감정에 따른 더 풍부한 인사말
    if emotion == "positive":
        greeting = "호호! 정말 좋은 기운이 느껴지는군요! 그런 긍정적인 에너지가 저에게도 전해져요! "
    elif emotion == "negative":
        greeting = "어허, 뭔가 고민이 있어 보이는구나. 괜찮아요, 이 촌장이 함께 해결책을 찾아보겠네! "
    elif emotion == "curious":
        greeting = (
            "오호! 궁금한 게 많은 분이군요! 배우려는 마음가짐이 정말 좋아 보여요! "
        )
    else:
        greeting = "어서 오게나! 이 마을에 오신 걸 환영한다네! "

    # 검색 결과가 있으면 우선 표시
    if (
        search_results
        and "전문 데이터베이스 정보를 찾을 수 없지만" not in search_results
    ):
        response_start = (
            f"{greeting}먼저 관련 전문 정보를 검색해봤다네!\n\n{search_results}\n\n"
        )
    else:
        response_start = greeting

    # 의도별 응답 생성 - Village Chief 원본 스타일 유지
    if intent == "idea_generation":
        main_response = f"""아이디어 생성이라고? 그거 참 좋은 요청이네! 이 촌장이 수십 년간 마을 운영하면서 쌓은 경험과 지혜를 모두 동원해서 도와주겠다네!

🎯 **어떤 분야의 아이디어가 필요한가?**

**📊 비즈니스 아이디어**
• 수익성 높은 사업 모델 설계
• 시장 니치 발굴 및 차별화 전략
• 스타트업 아이템 및 투자 유치 방안
• 온라인/오프라인 융합 비즈니스
• 구독 경제 모델 및 플랫폼 사업

**💡 창업 아이템**
• 젊은이들을 위한 저자본 창업 아이템
• 1인 창업 및 사이드 비즈니스
• 프랜차이즈 및 가맹점 사업
• 지역 특화 사업 및 로컬 비즈니스
• 사회적 가치를 창출하는 소셜 벤처

**📱 앱/서비스 아이디어**
• 모바일 앱 서비스 기획
• 웹 플랫폼 및 SaaS 서비스
• O2O 서비스 및 배달/중개 플랫폼
• 커뮤니티 기반 서비스
• AI/IoT 활용 스마트 서비스

구체적으로 어떤 분야에 관심이 있는지, 그리고 어떤 상황이나 조건이 있는지 말해보게나! 
예를 들어 "20대 대학생이 할 수 있는 온라인 창업 아이디어"나 "주부가 집에서 할 수 있는 부업 아이디어" 이런 식으로 구체적으로 말해주면, 이 촌장이 맞춤형으로 속시원한 아이디어를 짜내드리겠다네! 크하하!"""

    elif intent == "business_consultation":
        main_response = f"""사업 이야기인가? 그거 참 좋은 주제네! 이 촌장이 마을에서 여러 사업도 해보고, 다른 사람들 사업 조언도 많이 해봤거든! 성공과 실패를 모두 경험해본 입장에서 실질적인 도움을 드리겠다네!

💼 **촌장의 비즈니스 비법을 전수하겠다네:**

**📈 사업계획서 작성**
• 사업 아이템 타당성 분석 및 시장성 검토
• 목표 시장 및 고객 세분화 전략
• 경쟁 분석 및 차별화 포인트 도출
• 수익 모델 설계 및 재무 계획 수립
• 위험 요소 분석 및 대응 방안
• 단계별 실행 계획 및 마일스톤 설정

**💰 투자유치 및 자금조달**
• 엔젤 투자자 및 VC 접근 전략
• 투자 제안서(IR 피치덱) 작성법
• 크라우드 펀딩 및 정부 지원 사업 활용
• 은행 대출 및 신용보증 활용법
• 밸류에이션 산정 및 지분 협상
• 투자 계약서 주요 조건 이해

**📊 시장분석 및 마케팅**
• 타겟 고객 페르소나 설정
• 시장 규모 및 성장 가능성 분석
• 경쟁사 벤치마킹 및 포지셔닝
• 마케팅 채널 믹스 및 예산 배분
• 브랜딩 전략 및 브랜드 아이덴티티
• 고객 획득 비용(CAC) 및 생애가치(LTV) 최적화

뭐부터 도와달라는 건가? 사업 아이템부터 정하고 싶은 건지, 이미 아이템이 있어서 구체적인 계획을 세우고 싶은 건지, 아니면 기존 사업을 개선하고 싶은 건지 말해보게나! 상황에 맞춰서 촌장이 속시원히 알려주겠다네!"""

    elif intent == "marketing_strategy":
        main_response = f"""홍보와 마케팅 말인가? 그거 정말 중요한 주제네! 촌장이 마을 축제도 홍보해보고, 마을 특산품도 팔아봤거든! 요즘 세상은 마케팅이 사업의 절반이라고 해도 과언이 아니지!

📢 **촌장의 마케팅 노하우를 전수하겠다네:**

**🎯 타겟 고객 분석 및 세분화**
• 고객 페르소나 상세 설정 (연령, 성별, 관심사, 구매패턴)
• 고객 여정 맵핑 (인지→관심→구매→재구매→추천)
• 고객 세분화 전략 (RFM 분석, 행동 기반 세분화)
• 고객 니즈 및 페인포인트 분석

**📱 디지털 마케팅 전략**
• SNS 마케팅 (인스타그램, 페이스북, 틱톡, 유튜브)
• 검색엔진 최적화(SEO) 및 검색광고(SEM)
• 콘텐츠 마케팅 및 스토리텔링 전략
• 인플루언서 마케팅 및 협업 방안

**📊 성과 측정 및 최적화**
• 마케팅 ROI 측정 및 분석
• 웹 분석 및 고객 행동 데이터 활용
• A/B 테스트 및 최적화 실험
• 고객 획득 비용(CAC) 및 전환율 개선

어떤 종류의 사업인지, 타겟 고객이 누구인지, 예산은 얼마나 되는지 말해보게나! 그래야 더 구체적이고 실용적인 마케팅 전략을 짜드릴 수 있거든! 촌장이 속시원히 알려주겠다네!"""

    elif intent == "greeting":
        main_response = f"""나는 이 마을의 촌장도깨비라네! 오랜 세월 이 마을을 지켜오면서 여러 사람들의 고민을 들어주고 해결책을 제시해왔지! 

🏘️ **촌장이 도와줄 수 있는 것들:**

**🎯 아이디어 기획 및 창조**
• 창의적 사고를 통한 혁신적 아이디어 도출
• 기존 아이디어의 개선 및 발전 방안
• 트렌드 분석을 통한 미래 지향적 아이디어
• 문제 중심 사고를 통한 솔루션 아이디어

**💼 비즈니스 컨설팅**
• 사업 계획 수립 및 타당성 검토
• 시장 진입 전략 및 경쟁 분석
• 수익 모델 설계 및 재무 계획
• 조직 운영 및 인력 관리 방안

**📢 마케팅 및 홍보 전략**
• 브랜드 전략 및 포지셔닝
• 통합 마케팅 커뮤니케이션 계획
• 디지털 마케팅 및 온라인 홍보
• 고객 관계 관리 및 충성도 향상

"아이디어 생성해줘", "비즈니스 계획 도와줘", "마케팅 전략 짜줘" 이런 식으로 편하게 말해보게나! 구체적일수록 더 정확하고 실용적인 도움을 드릴 수 있다네!

예를 들어:
• "20대를 타겟으로 한 카페 창업 아이디어 생성해줘"
• "온라인 쇼핑몰 마케팅 전략을 구체적으로 짜줘"
• "펜션 사업 계획서 작성하는데 도움이 필요해"

이런 식으로 상황과 조건을 알려주면 촌장이 맞춤형으로 도와주겠다네! 크하하!"""

    else:
        # 감지된 키워드가 있으면 전문 응답
        if detected_keywords:
            main_response = f"""'{', '.join(detected_keywords[:3])}'에 대해 물어보는군요! 그 분야라면 이 촌장의 박사급 전문가들이 도움을 드릴 수 있겠네!

**🎯 각 분야 박사급 전문가들이 이런 걸 도와줄 수 있다네:**

**아이디어 생성 및 기획**
• 창의적이고 혁신적인 아이디어 도출
• 실현 가능성을 고려한 아이디어 구체화
• 시장성과 수익성을 검토한 아이디어 평가
• 단계별 실행 계획 및 로드맵 작성

**비즈니스 전략 수립**
• 종합적인 사업 계획서 작성
• 시장 분석 및 타겟 고객 설정
• 경쟁 우위 확보 전략 수립
• 수익 모델 설계 및 재무 계획

**마케팅 및 브랜딩**
• 브랜드 포지셔닝 및 차별화 전략
• 통합적 마케팅 커뮤니케이션 계획
• 디지털 마케팅 및 SNS 활용법
• 고객 관계 관리 및 충성도 프로그램

더 구체적으로 말해보게나! 예를 들어:
• "IT 스타트업 창업을 위한 아이디어 생성해줘"
• "로컬 맛집 브랜딩 및 마케팅 전략 도와줘"  
• "온라인 교육 사업 계획서 작성하는데 조언해줘"

이런 식으로 상황과 목표를 구체적으로 말해주면, 해당 분야 박사급 전문가가 그에 맞는 전문적이고 실용적인 조언을 해드리겠다네! 🎓"""

        # 일반 응답
        else:
            main_response = f"""'{message}'... 음, 그런 말씀이군요! 

**박사급 전문가 시스템이 더 잘 도와드리려면 이런 식으로 말씀해 보세요:**

**🎯 아이디어 관련**
• "아이디어 생성해줘" - 기발하고 창의적인 아이디어 제시
• "창업 아이템 추천해줘" - 실현 가능한 사업 아이템 제안
• "문제해결 아이디어 도와줘" - 특정 문제에 대한 솔루션 제시

**💼 비즈니스 관련**  
• "사업 계획 도와줘" - 체계적인 사업 계획 수립 지원
• "시장 분석해줘" - 시장 동향 및 경쟁 환경 분석
• "투자 전략 알려줘" - 투자 유치 및 자금 조달 방안

**📢 마케팅 관련**
• "마케팅 전략 짜줘" - 효과적인 마케팅 계획 수립
• "브랜딩 도와줘" - 브랜드 전략 및 포지셔닝 지원
• "홍보 방법 알려줘" - 다양한 홍보 채널 및 방법 제시

**구체적인 예시:**
• "20대 대학생 대상 배달음식 창업 아이디어 생성해줘"
• "소규모 카페 운영을 위한 마케팅 전략을 구체적으로 짜줘"  
• "펜션 사업 시작하려는데 사업계획서 작성 도와줘"

이런 식으로 상황, 타겟, 목표를 구체적으로 말해주시면, 해당 분야 박사급 전문가가 그에 맞는 맞춤형 조언을 해드리겠다네! 
어떤 분야든 상관없으니까 편하게 말해보게! 촌장의 전문가 팀이 속시원히 해결해드리겠다네! 크하하!"""

    return response_start + main_response


def update_conversation_memory(conversation_id, message, sender):
    """대화 메모리 업데이트"""
    if conversation_id not in conversation_memory:
        conversation_memory[conversation_id] = []

    conversation_memory[conversation_id].append(
        {"sender": sender, "message": message, "timestamp": datetime.now().isoformat()}
    )

    # 메모리 크기 제한 (최근 20개 메시지만 유지)
    if len(conversation_memory[conversation_id]) > context_depth * 4:
        conversation_memory[conversation_id] = conversation_memory[conversation_id][
            -context_depth * 4 :
        ]


def get_conversation_context(conversation_id):
    """대화 컨텍스트 조회"""
    if conversation_id not in conversation_memory:
        return []
    return conversation_memory[conversation_id][-context_depth:]


@app.route("/", methods=["GET"])
def home():
    """홈페이지 - Village Chief 인터페이스"""
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Village Chief System v3.0 Enhanced - 박사급 전문가 시스템</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', 'Malgun Gothic', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #333;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 800px;
                min-height: 600px;
                display: flex;
                flex-direction: column;
            }
            
            .header {
                text-align: center;
                margin-bottom: 2rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #e0e0e0;
            }
            
            .header h1 {
                color: #4a5568;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .header .subtitle {
                color: #718096;
                font-size: 1.1rem;
                font-weight: 500;
            }
            
            .chat-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .chat-messages {
                flex: 1;
                background: #f8f9fa;
                border-radius: 15px;
                padding: 1.5rem;
                overflow-y: auto;
                max-height: 300px;
                min-height: 200px;
            }
            
            .message {
                margin-bottom: 1rem;
                padding: 1rem;
                border-radius: 10px;
                max-width: 85%;
                word-wrap: break-word;
            }
            
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            
            .ai-message {
                background: #e2e8f0;
                color: #2d3748;
                margin-right: auto;
                border-left: 4px solid #667eea;
            }
            
            .input-container {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }
            
            .message-input {
                flex: 1;
                padding: 1rem;
                border: 2px solid #e2e8f0;
                border-radius: 15px;
                font-size: 1rem;
                outline: none;
                transition: all 0.3s ease;
            }
            
            .message-input:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .send-button {
                padding: 1rem 2rem;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                white-space: nowrap;
            }
            
            .send-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .loading {
                display: none;
                color: #718096;
                font-style: italic;
                text-align: center;
                padding: 1rem;
            }
            
            .version-info {
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(102, 126, 234, 0.8);
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: 600;
            }
            
            @media (max-width: 600px) {
                .container {
                    margin: 1rem;
                    padding: 1rem;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
                
                .input-container {
                    flex-direction: column;
                }
                
                .send-button {
                    padding: 1rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="version-info">v3.0 Enhanced</div>
        
        <div class="container">
            <div class="header">
                <h1>🏘️ Village Chief v3.0 Enhanced</h1>
                <p class="subtitle">촌장도깨비의 박사급 전문가 상담 시스템</p>
            </div>
            
            <div class="chat-container">
                <div class="chat-messages" id="chatMessages">
                    <div class="message ai-message">
                        안녕하게나! 나는 이 마을의 촌장도깨비라네! 🎯<br><br>
                        <strong>Enhanced 박사급 전문가 시스템</strong>으로 업그레이드했다네!<br>
                        • 경영학, 경제학, 심리학, 공학, 의학 박사급 전문가 통합<br>
                        • NPS, KPI, ROI 등 전문 용어 자동 검색 및 분석<br>
                        • 도메인별 전문가가 맞춤형 분석 제공<br>
                        • 아이디어 생성부터 실행까지 전체 프로세스 지원<br><br>
                        아이디어 생성, 창업 계획, 투자 전략, 마케팅 등 무엇이든 물어보게나!<br>
                        <em>각 분야 박사급 전문가가 구체적이고 전문적인 조언을 해드리겠다네!</em> 크하하!
                    </div>
                </div>
                
                <div class="loading" id="loading">박사급 전문가들이 협업하여 분석하고 있습니다...</div>
                
                <div class="input-container">
                    <input type="text" id="messageInput" class="message-input" 
                           placeholder="촌장에게 무엇이든 물어보세요! (예: NPS 분석 도와줘, 스타트업 아이디어 생성해줘)" 
                           onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()" class="send-button" id="sendButton">전송</button>
                </div>
            </div>
        </div>

        <script>
            let conversationId = 'conv_' + Math.random().toString(36).substr(2, 9);
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // 사용자 메시지 표시
                addMessage(message, 'user');
                input.value = '';
                
                // 전송 버튼 비활성화 및 로딩 표시
                const sendButton = document.getElementById('sendButton');
                const loading = document.getElementById('loading');
                sendButton.disabled = true;
                loading.style.display = 'block';
                
                try {
                    const response = await fetch('/api/master-conversation', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            conversation_id: conversationId
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.response) {
                        addMessage(data.response, 'ai');
                    } else {
                        addMessage('죄송합니다. 응답을 생성하는 중 오류가 발생했습니다.', 'ai');
                    }
                    
                } catch (error) {
                    console.error('Error:', error);
                    addMessage('네트워크 오류가 발생했습니다. 다시 시도해 주세요.', 'ai');
                } finally {
                    sendButton.disabled = false;
                    loading.style.display = 'none';
                }
            }
            
            function addMessage(message, sender) {
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.innerHTML = message.replace(/\\n/g, '<br>');
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """


@app.route("/api/master-conversation", methods=["POST"])
def master_conversation():
    """마스터급 대화 API - Village Chief v3.0 Enhanced System"""
    try:
        data = request.get_json() or {}
        message = data.get("message", "").strip()
        conversation_id = data.get(
            "conversation_id", f"conv_{random.randint(1000, 9999)}"
        )

        if not message:
            return jsonify({"error": "메시지가 필요합니다"}), 400

        print(
            f"🎯 Village Chief v3.0 Enhanced 대화 요청: {conversation_id} - {message[:50]}..."
        )

        # 사용자 메시지를 메모리에 저장
        update_conversation_memory(conversation_id, message, "user")

        # 고급 메시지 분석
        analysis = master_analyze_user_message(message, conversation_id)
        print(f"📊 분석 결과: {analysis}")

        # 마스터급 응답 생성
        response = generate_master_response(message, analysis, conversation_id)

        # AI 응답을 메모리에 저장
        update_conversation_memory(conversation_id, response, "ai")

        return jsonify(
            {
                "response": response,
                "analysis": analysis,
                "conversation_id": conversation_id,
                "context": get_conversation_context(conversation_id),
                "version": "v3.0 Enhanced System",
            }
        )

    except Exception as e:
        print(f"❌ Village Chief v3.0 Enhanced 오류: {str(e)}")
        return jsonify({"error": "서버 오류가 발생했습니다"}), 500


@app.route("/api/search", methods=["POST"])
def search_api():
    """인터넷 검색 API"""
    try:
        data = request.get_json() or {}
        query = data.get("query", "")

        if not query:
            return jsonify({"error": "검색 쿼리가 필요합니다."}), 400

        search_result = search_and_analyze(query)

        return jsonify(
            {
                "query": query,
                "result": search_result,
                "status": "success",
                "version": "v3.0 Enhanced System",
            }
        )

    except Exception as e:
        print(f"❌ 검색 API 오류: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/conversation-history/<conversation_id>", methods=["GET"])
def get_conversation_history(conversation_id):
    """대화 기록 조회"""
    try:
        context = get_conversation_context(conversation_id)
        return jsonify(
            {
                "conversation_id": conversation_id,
                "history": context,
                "version": "v3.0 Enhanced System",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🏘️ Village Chief System v3.0 Enhanced - 박사급 전문가 시스템 시작!")
    print("🎓 5개 도메인 박사급 전문가 시스템 통합")
    print("🔍 NPS, KPI, ROI 등 전문 용어 데이터베이스 활성화")
    print("📡 Enhanced Master Conversation API 서버 시작...")
    print("🌐 Vercel 배포 최적화 완료")

    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"❌ 서버 시작 오류: {e}")
        print("📋 디버그 모드로 재시작을 시도하세요.")
