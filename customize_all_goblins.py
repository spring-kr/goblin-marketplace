import os
import re


def customize_# 실제 16개 도깨비 정의 (index.html 기준)
goblins = [
    ("assistant", "개인 비서 및 업무 효율성", "AssistantGoblin"),
    ("builder", "건축 설계 및 건설 관리", "BuilderGoblin"),
    ("counselor", "심리 상담 및 정신 건강", "CounselorGoblin"),
    ("creative", "창작 및 콘텐츠 제작", "CreativeGoblin"),
    ("data_analyst", "빅데이터 분석 및 인사이트 제공", "DataAnalystGoblin"),
    ("fortune", "타로 및 사주 운세 상담", "FortuneGoblin"),
    ("growth", "개인 및 비즈니스 성장 컨설팅", "GrowthGoblin"),
    ("hr", "인적자원 관리 및 채용", "HrGoblin"),
    ("marketing", "디지털 마케팅 및 브랜드 전략", "MarketingGoblin"),
    ("medical", "의료 진단 및 건강 상담", "MedicalGoblin"),
    ("sales", "영업 전략 및 고객 관리", "SalesGoblin"),
    ("seo", "검색엔진 최적화 및 온라인 마케팅", "SeoGoblin"),
    ("shopping", "스마트 쇼핑 및 상품 추천", "ShoppingGoblin"),
    ("startup", "창업 컨설팅 및 비즈니스 개발", "StartupGoblin"),
    ("village_chief", "전체 도깨비 총괄 관리", "VillageChiefGoblin"),
    ("writing", "전문 글쓰기 및 편집", "WritingGoblin")
] expertise_description, class_name):
    """각 도깨비를 전문 분야에 맞게 커스터마이징"""
    file_path = f"phd_goblins/{goblin_name}_goblin.py"

    if not os.path.exists(file_path):
        print(f"❌ {file_path} 파일이 없습니다.")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 클래스명 변경: VillageChiefLoader -> [Name]Goblin
    content = content.replace("class VillageChiefLoader:", f"class {class_name}:")
    content = content.replace("VillageChiefLoader()", f"{class_name}()")
    content = content.replace(
        "VillageChiefLoader 초기화 완료!", f"{class_name} 초기화 완료!"
    )

    # 2. 전문성 추가
    init_pattern = r"(self\.context_depth = 5  # 기억할 대화 깊이)"
    replacement = f'\\1\n        self.expertise = "{expertise_description}"  # {goblin_name} 전문성'
    content = re.sub(init_pattern, replacement, content)

    # 3. 주석 변경
    content = content.replace(
        "# Village Chief Function Loader 클래스",
        f"# {class_name} Function Loader 클래스",
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ {goblin_name}_goblin.py 커스터마이징 완료!")
    return True


# 16개 도깨비 정의
goblins = [
    ("assistant", "개인 비서 및 업무 효율성", "AssistantGoblin"),
    ("builder", "건축 설계 및 건설 관리", "BuilderGoblin"),
    ("counselor", "심리 상담 및 정신 건강", "CounselorGoblin"),
    ("marketing", "디지털 마케팅 및 브랜드 전략", "MarketingGoblin"),
    ("startup", "창업 컨설팅 및 비즈니스 개발", "StartupGoblin"),
    ("chef", "요리 및 음식 전문가", "ChefGoblin"),
    ("doctor", "의료 진단 및 건강 관리", "DoctorGoblin"),
    ("education", "교육 과정 설계 및 학습 지도", "EducationGoblin"),
    ("finance", "금융 투자 및 자산 관리", "FinanceGoblin"),
    ("legal", "법률 자문 및 계약 검토", "LegalGoblin"),
    ("entertainment", "엔터테인먼트 기획 및 콘텐츠 제작", "EntertainmentGoblin"),
    ("agriculture", "농업 기술 및 작물 관리", "AgricultureGoblin"),
    ("security", "보안 시스템 및 위험 관리", "SecurityGoblin"),
    ("logistics", "물류 최적화 및 공급망 관리", "LogisticsGoblin"),
    ("energy", "에너지 효율 및 재생 에너지", "EnergyGoblin"),
    ("research", "학술 연구 및 데이터 분석", "ResearchGoblin"),
]


def main():
    print("🚀 16개 메가급 도깨비 커스터마이징 시작!")

    success_count = 0
    for goblin_name, expertise, class_name in goblins:
        if customize_goblin(goblin_name, expertise, class_name):
            success_count += 1

    print(f"\n🎉 커스터마이징 완료: {success_count}/{len(goblins)} 성공!")

    # 파일 크기 확인
    print("\n📊 파일 크기 확인:")
    for goblin_name, _, _ in goblins:
        file_path = f"phd_goblins/{goblin_name}_goblin.py"
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  {goblin_name}_goblin.py: {size:,} bytes")


if __name__ == "__main__":
    main()
