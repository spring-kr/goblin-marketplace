#!/usr/bin/env python3
"""모든 도깨비 전문가 시스템 최종 테스트"""

from stem_integration import STEMIntegration


def test_all_expert_agents():
    """16개 분야 전문가 도깨비 최종 테스트"""

    # 인스턴스 생성
    stem = STEMIntegration()

    # 올바른 agent_type 키와 테스트 질문
    test_cases = [
        ("assistant", "업무 효율성을 높이는 방법은?"),
        ("builder", "웹 애플리케이션 개발 방법론은?"),
        ("counselor", "상담 기법을 개선하려면 어떻게 해야 하나요?"),
        ("creative", "창작 아이디어 발굴법을 알려주세요"),
        ("data_analyst", "데이터 분석 프로젝트 진행 방법은?"),
        ("fortune", "올해 운세는 어떤가요?"),
        ("growth", "개인 성장 계획을 세우려면?"),
        ("hr", "인사관리 시스템 개선 방법은?"),
        ("marketing", "마케팅 전략을 어떻게 세워야 하나요?"),
        ("medical", "의료진단 정확성을 향상시키려면?"),
        ("sales", "영업 성과 향상 방법은?"),
        ("seo", "SEO 최적화 어떻게 하나요?"),
        ("shopping", "현명한 쇼핑 방법은?"),
        ("startup", "창업 전략을 어떻게 세워야 하나요?"),
        ("village_chief", "마을 전체 관리 방향은?"),
        ("writing", "글쓰기 실력 향상법은?"),
    ]

    results = []
    expert_count = 0

    print("🎯 도깨비마을 16개 분야 전문가 시스템 최종 테스트")
    print("=" * 80)

    for agent_type, question in test_cases:
        print(f"\n🤖 {agent_type.upper()} 도깨비 테스트")
        print("-" * 60)
        print(f"질문: {question}")

        try:
            # 질문 처리
            response = stem.process_question(agent_type, question, "127.0.0.1")

            if isinstance(response, dict) and "response" in response:
                resp_text = response["response"]
                response_length = len(resp_text)

                print(f"✅ 응답 길이: {response_length}자")

                # 전문가급 판단 (1000자 이상)
                is_expert = response_length >= 1000
                if is_expert:
                    expert_count += 1
                    print(f"🎖️ 전문가급 달성!")
                else:
                    print(f"⚠️ 일반급 ({response_length}자)")

                # 응답 미리보기
                print(f"응답 미리보기: {resp_text[:200]}...")

                results.append(
                    {
                        "agent": agent_type,
                        "question": question,
                        "length": response_length,
                        "is_expert": is_expert,
                        "status": "success",
                    }
                )

            else:
                print(f"❌ 오류: {response}")
                results.append(
                    {
                        "agent": agent_type,
                        "question": question,
                        "error": str(response),
                        "status": "failed",
                    }
                )

        except Exception as e:
            print(f"❌ 예외 발생: {e}")
            results.append(
                {
                    "agent": agent_type,
                    "question": question,
                    "error": str(e),
                    "status": "error",
                }
            )

    # 최종 요약
    print(f"\n{'='*80}")
    print("📊 최종 테스트 결과 요약")
    print(f"{'='*80}")

    total_tests = len(test_cases)
    successful_tests = len([r for r in results if r["status"] == "success"])
    expert_level_count = len([r for r in results if r.get("is_expert", False)])

    print(f"총 테스트: {total_tests}개 도깨비")
    print(f"성공: {successful_tests}개")
    print(f"전문가급(1000자+): {expert_level_count}개")

    if successful_tests > 0:
        expert_ratio = (expert_level_count / successful_tests) * 100
        print(f"전문가급 비율: {expert_ratio:.1f}%")
    else:
        print("전문가급 비율: 0% (모든 테스트 실패)")

    # 상세 결과
    print(f"\n📋 상세 결과:")
    for result in results:
        if result["status"] == "success":
            expert_mark = "🎖️" if result.get("is_expert", False) else "📝"
            print(f"{expert_mark} {result['agent']}: {result['length']}자")
        else:
            print(f"❌ {result['agent']}: {result.get('error', 'Unknown error')}")

    # 전문가급 미달 도깨비 개선 제안
    non_expert = [
        r for r in results if r["status"] == "success" and not r.get("is_expert", False)
    ]
    if non_expert:
        print(f"\n⚠️ 전문가급 미달 도깨비 ({len(non_expert)}개):")
        for r in non_expert:
            print(f"  - {r['agent']}: {r['length']}자 (추가 전문 지식 필요)")

    print(f"\n🎉 테스트 완료! 전문가 시스템 구축 상태: {expert_ratio:.1f}% 완성")

    return results


if __name__ == "__main__":
    test_all_expert_agents()
