"""
테스트용 사용량 데이터 생성기
실제 사용 패턴을 시뮬레이션하여 통계 대시보드 테스트용
"""

import json
import datetime
import random
import os


def generate_test_data():
    """테스트용 사용량 데이터 생성"""

    # 로그 파일 초기화
    log_file = "usage_log.json"
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    # 에이전트 타입들 (16개)
    agents = [
        "math", "physics", "chemistry", "biology", "engineering", "assistant", "marketing", "startup",
        "cooking", "lifestyle", "interior", "finance", "hobby", "tech", "health", "learning"
    ]

    # 샘플 질문들
    sample_questions = {
        # 기존 8개 (전문 분야)
        "math": ["미적분 공식을 알려주세요", "복리 이자 계산 방법", "확률 문제 풀이"],
        "physics": ["뉴턴의 법칙 설명", "전자기학 기본 원리", "양자역학 개념"],
        "chemistry": ["화학 반응식 균형", "분자 구조 분석", "유기화학 기초"],
        "biology": ["세포 분열 과정", "DNA 구조", "진화론 원리"],
        "engineering": ["시스템 설계 방법", "회로 분석", "구조 역학"],
        "assistant": ["업무 효율성 개선", "일정 관리 방법", "팀 협업 도구"],
        "marketing": ["마케팅 전략 수립", "브랜딩 방법", "고객 분석"],
        "startup": ["사업 계획서 작성", "투자 유치 방법", "창업 아이템 발굴"],
        
        # 새로운 8개 (일상 생활)
        "cooking": ["오늘 저녁 뭐 해먹지?", "간단한 다이어트 요리", "냉장고 파먹기 레시피"],
        "lifestyle": ["전기세 절약 방법", "옷 깨끗하게 세탁하는 법", "청소 꿀팁"],
        "interior": ["작은 방 인테리어", "저렴하게 방 꾸미기", "조명으로 분위기 바꾸기"],
        "finance": ["용돈 관리 방법", "적금 추천", "생활비 절약 팁"],
        "hobby": ["새로운 취미 추천", "주말에 뭐 하지?", "운동 시작하는 법"],
        "tech": ["엑셀 기초 사용법", "스마트폰 사진 잘 찍는 법", "컴퓨터 느려질 때"],
        "health": ["다이어트 식단", "홈트레이닝 추천", "불면증 해결법"],
        "learning": ["효과적인 공부법", "집중력 키우는 방법", "암기 잘하는 법"]
    }

    # 지난 7일간의 데이터 생성
    for days_ago in range(7, 0, -1):
        date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

        # 하루에 랜덤하게 5-20개의 사용량 생성
        daily_usage = random.randint(5, 20)

        for _ in range(daily_usage):
            # 랜덤 시간 생성 (업무시간대에 더 많이)
            hour = random.choices(
                range(24),
                weights=[
                    1,
                    1,
                    1,
                    1,
                    1,
                    2,
                    3,
                    4,
                    5,
                    8,
                    10,
                    12,
                    10,
                    8,
                    6,
                    5,
                    4,
                    3,
                    2,
                    2,
                    2,
                    1,
                    1,
                    1,
                ],
            )[0]

            test_time = date.replace(
                hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59)
            )

            # 랜덤 에이전트 선택 (일상 생활 도깨비들이 더 인기있도록)
            agent = random.choices(
                agents, 
                weights=[
                    # 전문 분야 (낮은 가중치)
                    1, 1, 1, 1, 1, 1.5, 1.5, 1,  # math~startup
                    # 일상 생활 (높은 가중치)  
                    4, 3, 3, 3.5, 3, 4, 3.5, 2.5  # cooking~learning
                ]
            )[0]

            # 해당 에이전트의 샘플 질문 선택
            question = random.choice(sample_questions[agent])

            # 성공률 95%
            success = random.random() < 0.95

            # 가짜 IP 생성
            fake_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"

            # 로그 생성 (시간을 과거로 설정)
            log_entry = {
                "timestamp": test_time.isoformat(),
                "date": test_time.strftime("%Y-%m-%d"),
                "time": test_time.strftime("%H:%M:%S"),
                "agent_type": agent,
                "question_length": len(question),
                "question_preview": (
                    question[:50] + "..." if len(question) > 50 else question
                ),
                "response_success": success,
                "user_ip": fake_ip,
                "weekday": test_time.strftime("%A"),
                "hour": test_time.hour,
            }

            # 기존 로그에 추가
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)

                logs.append(log_entry)

                with open(log_file, "w", encoding="utf-8") as f:
                    json.dump(logs, f, ensure_ascii=False, indent=2)

            except Exception as e:
                print(f"로그 추가 오류: {e}")

    total_logs = daily_usage * 7
    print(
        f"✅ 테스트 데이터 생성 완료! 총 {total_logs}개의 샘플 로그가 추가되었습니다."
    )


if __name__ == "__main__":
    generate_test_data()
