#!/usr/bin/env python3
"""
🎓 모든 도깨비용 박사급 응답 시스템
Universal PhD Response System for All Goblins

이 파일은 모든 도깨비의 응답을 박사급 수준으로 향상시키는 공통 시스템입니다.
상용 AI들의 강점을 모두 통합한 차세대 박사급 시스템입니다.
"""

# 범용 박사급 시스템 import
try:
    from universal_phd_system import (
        apply_phd_enhancement,
        get_phd_capabilities_for_goblin,
    )

    PHD_SYSTEM_AVAILABLE = True
except ImportError:
    PHD_SYSTEM_AVAILABLE = False

# 상용 AI 강점 통합 시스템 import
try:
    from commercial_ai_strengths_integrator import (
        generate_super_enhanced_response,
        apply_commercial_ai_strengths,
    )

    COMMERCIAL_AI_STRENGTHS_AVAILABLE = True
except ImportError:
    COMMERCIAL_AI_STRENGTHS_AVAILABLE = False


def generate_enhanced_goblin_response(goblin_config: dict, user_message: str) -> str:
    """모든 도깨비에 적용되는 박사급 향상 응답 생성기 (상용 AI 강점 통합)"""

    # 1차: 상용 AI 강점 통합 시스템 적용 (최우선)
    if COMMERCIAL_AI_STRENGTHS_AVAILABLE:
        try:
            super_enhanced_response = generate_super_enhanced_response(
                goblin_config, user_message
            )
            return super_enhanced_response
        except Exception as e:
            # 상용 AI 강점 시스템 실패 시 기존 박사급 시스템으로 fallback
            print(f"⚠️ 상용 AI 강점 시스템 오류: {e}")

    # 2차: 기존 박사급 시스템 적용
    if PHD_SYSTEM_AVAILABLE:
        try:
            base_response = generate_base_response(goblin_config, user_message)
            enhanced_response = apply_phd_enhancement(
                goblin_config, user_message, base_response
            )
            return enhanced_response
        except Exception as e:
            print(f"⚠️ 박사급 시스템 오류: {e}")

    # 3차: 기본 응답 시스템 (최종 fallback)
    return generate_base_response(goblin_config, user_message)


def generate_base_response(goblin_config: dict, user_message: str) -> str:
    """도깨비별 기본 응답 생성"""

    goblin_name = goblin_config.get("name", "도깨비")
    expertise = goblin_config.get("expertise", [])
    personality = goblin_config.get("personality", "전문적이고 도움이 되는")

    # 상세 정보 요청 감지
    if any(
        keyword in user_message.lower()
        for keyword in ["구체적", "자세히", "더", "완전", "마스터", "박사급"]
    ):
        return generate_detailed_response(goblin_config, user_message)

    # 기본 응답 패턴
    detected_area = "종합적인 지원"
    for area in expertise:
        if area.lower() in user_message.lower():
            detected_area = area
            break

    response = f"""{goblin_name}가 {detected_area} 도와드리겠습니다! ✨

🎯 **{detected_area} 핵심 포인트:**
{chr(10).join([f"• {point}" for point in expertise[:3]])}

💡 **맞춤형 조언:**
{personality} 관점에서 단계별로 안내해드리겠습니다.

📚 **전문 지식 활용:**
실무에서 바로 적용할 수 있는 구체적인 방법을 제시합니다.

더 자세한 정보가 필요하시면 '구체적으로' 또는 '박사급 분석'이라고 말씀해주세요!"""

    return response


def generate_detailed_response(goblin_config: dict, user_message: str) -> str:
    """상세 가이드 응답 생성"""

    goblin_name = goblin_config.get("name", "도깨비")
    expertise = goblin_config.get("expertise", [])
    detailed_knowledge = goblin_config.get("detailed_knowledge", [])

    detailed_guide = f"""{goblin_name} 완전 마스터 가이드 🧙‍♂️

🎓 **박사급 전문 지식 영역:**
{chr(10).join([f"• {knowledge}" for knowledge in detailed_knowledge])}

🎯 **체계적 맞춤형 솔루션:**
1️⃣ **현황 분석** - 정확한 문제 파악 및 진단
2️⃣ **전략 수립** - 과학적 접근법 기반 계획 설계  
3️⃣ **실행 계획** - 단계별 구체적 실행 방안
4️⃣ **성과 측정** - 객관적 지표 기반 평가
5️⃣ **지속 개선** - 피드백 기반 최적화

💡 **실용적 도구 및 방법론:**
• 체크리스트 제공 및 활용 가이드
• 검증된 템플릿 및 프레임워크
• 단계별 실행 매뉴얼 및 가이드라인
• 성과 측정 지표 및 KPI 설정

🔬 **과학적 검증 방법:**
• 데이터 기반 의사결정 프로세스
• 근거 중심 접근법 (Evidence-Based Practice)
• 지속적 모니터링 및 피드백 루프
• 최신 연구 동향 및 모범 사례 적용

🌟 **{goblin_name}만의 특별한 전문성:**
박사급 수준의 깊이 있는 분석과 실무 적용 가능한 구체적 솔루션을 제공합니다.

🎯 **5개 도메인 융합 분석:**
• 🏢 Business: 비즈니스 전략 및 성과 최적화
• 📈 Economics: 경제적 타당성 및 투자 효과 분석  
• 🧠 Psychology: 심리적 요인 및 행동 변화 분석
• ⚙️ Engineering: 시스템 최적화 및 효율성 분석
• 🏥 Medical: 건강 및 웰빙 관점 통합 분석

어떤 부분부터 시작하고 싶으신가요? 박사급 전문성으로 더 구체적으로 도와드릴게요! 🚀"""

    return detailed_guide


def detect_special_requests(user_message: str) -> dict:
    """특별한 요청 감지 (데이터 분석, 문서 생성 등)"""

    request_types = {
        "data_analysis": ["데이터", "분석", "통계", "지표", "측정", "평가"],
        "document_generation": ["문서", "보고서", "작성", "생성", "만들어"],
        "strategy_planning": ["전략", "계획", "방안", "로드맵", "설계"],
        "problem_solving": ["문제", "해결", "개선", "최적화", "효율"],
        "consultation": ["상담", "조언", "컨설팅", "가이드", "도움"],
    }

    message_lower = user_message.lower()
    detected_requests = {}

    for request_type, keywords in request_types.items():
        score = sum(1 for keyword in keywords if keyword in message_lower)
        if score > 0:
            detected_requests[request_type] = score

    return detected_requests


def generate_specialized_response(
    goblin_config: dict, user_message: str, request_type: str
) -> str:
    """특화된 요청에 대한 응답 생성"""

    goblin_name = goblin_config.get("name", "도깨비")

    if request_type == "data_analysis":
        return f"""
📊 **{goblin_name} 데이터 분석 전문 서비스**

🔍 **분석 프로세스:**
1. 데이터 수집 및 정제
2. 탐색적 데이터 분석 (EDA)  
3. 통계적 분석 및 모델링
4. 인사이트 도출 및 시각화
5. 액션 플랜 수립

📈 **제공 분석:**
• 기술통계 분석 및 트렌드 파악
• 상관관계 및 인과관계 분석
• 예측 모델링 및 시나리오 분석
• 비즈니스 인사이트 및 권고사항

어떤 데이터를 분석하고 싶으신가요?
"""

    elif request_type == "document_generation":
        return f"""
📝 **{goblin_name} 문서 생성 전문 서비스**

📋 **생성 가능 문서:**
• 비즈니스 보고서 및 제안서
• 기술 명세서 및 가이드
• 분석 보고서 및 인사이트
• 전략 기획서 및 로드맵

✨ **고급 기능:**
• 6가지 문서 개선 (용어사전/상세설명/예시/다이어그램/참고자료/요약)
• 데이터 기반 자동 분석
• 박사급 품질 보증
• 맞춤형 스타일 적용

어떤 문서를 생성하고 싶으신가요?
"""

    else:
        return generate_base_response(goblin_config, user_message)


# 모든 도깨비가 사용할 수 있는 공통 함수들
def apply_universal_enhancements(goblin_config: dict) -> dict:
    """모든 도깨비에 범용 향상 기능 적용"""

    # 박사급 5개 도메인 추가
    enhanced_config = goblin_config.copy()

    # 기존 expertise에 박사급 도메인 능력 추가
    existing_expertise = enhanced_config.get("expertise", [])
    phd_expertise = [
        "박사급비즈니스분석",
        "경제학적타당성분석",
        "심리학적행동분석",
        "공학적시스템최적화",
        "의학적건강관리",
    ]

    enhanced_config["expertise"] = existing_expertise + phd_expertise

    # 고급 기능 추가
    advanced_features = enhanced_config.get("advanced_features", {})
    phd_features = {
        "phd_business_analysis": True,
        "phd_economics_analysis": True,
        "phd_psychology_analysis": True,
        "phd_engineering_analysis": True,
        "phd_medical_analysis": True,
        "data_analysis": True,
        "document_generation": True,
        "conversation_detection": True,
        "multi_domain_fusion": True,
    }

    enhanced_config["advanced_features"] = {**advanced_features, **phd_features}

    # 박사급 도메인 정보 추가
    enhanced_config["phd_domains"] = [
        "business",  # 경영학 박사급
        "economics",  # 경제학 박사급
        "psychology",  # 심리학 박사급
        "engineering",  # 공학 박사급
        "medical",  # 의학 박사급
    ]

    return enhanced_config


# Export 함수들
__all__ = [
    "generate_enhanced_goblin_response",
    "apply_universal_enhancements",
    "detect_special_requests",
    "generate_specialized_response",
]
