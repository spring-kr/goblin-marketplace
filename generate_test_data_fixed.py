"""
원래 16개 도깨비 테스트 데이터 생성기
"""

import json
import random
from datetime import datetime, timedelta


def generate_test_data():
    """원래 16개 도깨비에 대한 테스트 데이터 생성"""

    # 원래 16개 도깨비
    agents = [
        "assistant",
        "builder",
        "counselor",
        "creative",
        "data_analyst",
        "fortune",
        "growth",
        "hr",
        "marketing",
        "medical",
        "sales",
        "seo",
        "shopping",
        "startup",
        "village_chief",
        "writing",
    ]

    # 각 도깨비별 샘플 질문들
    sample_questions = {
        "assistant": [
            "업무 효율성을 높이는 방법이 있을까요?",
            "일정 관리 도구 추천해주세요",
            "회의록 작성 요령을 알려주세요",
            "업무 우선순위 설정하는 법",
            "생산성 향상 팁을 알려주세요",
        ],
        "builder": [
            "웹사이트 개발 프로세스를 알려주세요",
            "파이썬과 자바스크립트 중 어떤 언어가 좋을까요?",
            "데이터베이스 설계 방법론",
            "API 개발 베스트 프랙티스",
            "프론트엔드 프레임워크 추천",
        ],
        "counselor": [
            "스트레스 관리 방법을 알려주세요",
            "인간관계에서 갈등 해결 방법",
            "자신감을 키우는 방법",
            "감정 조절하는 법",
            "우울감을 극복하는 방법",
        ],
        "creative": [
            "창의적 아이디어 발상법",
            "콘텐츠 기획 방법론",
            "디자인 영감 얻는 방법",
            "스토리텔링 기법",
            "브랜딩 아이디어 개발",
        ],
        "data_analyst": [
            "데이터 분석 도구 추천",
            "통계 분석 방법론",
            "빅데이터 처리 기법",
            "예측 모델 만드는 방법",
            "데이터 시각화 팁",
        ],
        "fortune": [
            "오늘의 운세를 봐주세요",
            "이번 달 행운의 색깔은?",
            "연애운 좋은 시기는 언제인가요?",
            "직장운 상승 방법",
            "금전운 개선 방법",
        ],
        "growth": [
            "개인 성장 계획 수립 방법",
            "목표 달성 전략",
            "자기계발 루틴 만들기",
            "역량 강화 방법",
            "성장 마인드셋 기르기",
        ],
        "hr": [
            "효과적인 인재 채용 방법",
            "직원 동기부여 전략",
            "조직 문화 개선 방안",
            "성과 평가 시스템 구축",
            "리더십 개발 프로그램",
        ],
        "marketing": [
            "디지털 마케팅 전략",
            "브랜드 포지셔닝 방법",
            "고객 세그먼테이션 기법",
            "마케팅 ROI 측정 방법",
            "소셜미디어 마케팅 팁",
        ],
        "medical": [
            "건강한 생활습관 만들기",
            "면역력 강화 방법",
            "스트레스성 질환 예방법",
            "영양 균형 잡힌 식단",
            "운동 루틴 추천",
        ],
        "sales": [
            "영업 성과 향상 방법",
            "고객 관계 관리 전략",
            "협상 스킬 향상",
            "신규 고객 개발 방법",
            "영업 프로세스 최적화",
        ],
        "seo": [
            "구글 상위 노출 방법",
            "키워드 리서치 방법",
            "백링크 구축 전략",
            "콘텐츠 SEO 최적화",
            "모바일 SEO 가이드",
        ],
        "shopping": [
            "온라인 쇼핑 할인 정보",
            "가성비 좋은 제품 추천",
            "쇼핑몰 비교 방법",
            "중고거래 안전 팁",
            "세일 정보 확인 방법",
        ],
        "startup": [
            "스타트업 창업 절차",
            "사업 계획서 작성법",
            "투자 유치 전략",
            "팀 빌딩 방법",
            "제품 개발 로드맵",
        ],
        "village_chief": [
            "커뮤니티 운영 방법",
            "갈등 조정 기법",
            "리더십 발휘 방법",
            "조직 관리 노하우",
            "의사결정 프로세스",
        ],
        "writing": [
            "보고서 작성 요령",
            "제안서 구성 방법",
            "논문 작성 가이드",
            "기술 문서 작성법",
            "콘텐츠 라이팅 팁",
        ],
    }

    # 테스트 데이터 생성
    test_data = []

    # 각 도깨비마다 랜덤하게 5-15개 질문 생성
    for agent in agents:
        num_questions = random.randint(5, 15)
        questions = sample_questions[agent]

        for i in range(num_questions):
            # 랜덤 시간 생성 (최근 30일 내)
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)

            timestamp = datetime.now() - timedelta(
                days=days_ago, hours=hours_ago, minutes=minutes_ago
            )

            # 성공/실패 랜덤 결정 (90% 성공률)
            success = random.random() < 0.9

            # 랜덤 IP 생성
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

            test_entry = {
                "agent_type": agent,
                "question": random.choice(questions),
                "success": success,
                "timestamp": timestamp.isoformat(),
                "user_ip": ip,
            }

            test_data.append(test_entry)

    # 시간순으로 정렬
    test_data.sort(key=lambda x: x["timestamp"], reverse=True)

    return test_data


def save_test_data():
    """테스트 데이터를 JSON 파일로 저장"""
    test_data = generate_test_data()

    with open("usage_logs.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(test_data)}개의 테스트 데이터가 생성되었습니다!")

    # 도깨비별 통계 출력
    agent_stats = {}
    for entry in test_data:
        agent = entry["agent_type"]
        if agent not in agent_stats:
            agent_stats[agent] = {"total": 0, "success": 0}
        agent_stats[agent]["total"] += 1
        if entry["success"]:
            agent_stats[agent]["success"] += 1

    print("\n📊 도깨비별 통계:")
    print("-" * 50)
    for agent, stats in sorted(agent_stats.items()):
        success_rate = (
            (stats["success"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        )
        print(
            f"{agent:15} | 총 {stats['total']:2}개 | 성공 {stats['success']:2}개 | 성공률 {success_rate:5.1f}%"
        )


if __name__ == "__main__":
    save_test_data()
