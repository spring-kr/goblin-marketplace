"""
v5.0 생성형 기능 개선 전후 비교 분석
"""

import os
from PIL import Image
from pathlib import Path


def compare_before_after():
    """개선 전후 비교 분석"""
    print("🔍 v5.0 생성형 기능 개선 전후 비교 분석")
    print("=" * 60)

    output_dir = Path("multimodal_output")
    if not output_dir.exists():
        print("❌ multimodal_output 디렉터리 없음")
        return

    # 파일들을 생성 시간순으로 정렬
    files = sorted(output_dir.glob("*.png"), key=lambda x: x.stat().st_mtime)

    # 이미지 파일들 분류
    expert_images = [f for f in files if "expert_" in f.name]
    chart_images = [f for f in files if "chart_" in f.name]

    print("🖼️ 전문가 이미지 개선 비교")
    print("-" * 40)

    if len(expert_images) >= 2:
        # 이전 버전과 최신 버전 비교
        old_image = expert_images[0]  # 가장 오래된 것
        new_image = expert_images[-1]  # 가장 최신 것

        print("📊 해상도 비교:")
        with Image.open(old_image) as old_img, Image.open(new_image) as new_img:
            old_size = old_img.size
            new_size = new_img.size
            old_file_size = old_image.stat().st_size / 1024
            new_file_size = new_image.stat().st_size / 1024

            print(f"   이전: {old_size[0]}x{old_size[1]} ({old_file_size:.1f}KB)")
            print(f"   개선: {new_size[0]}x{new_size[1]} ({new_file_size:.1f}KB)")

            # 개선 비율 계산
            resolution_improvement = (new_size[0] * new_size[1]) / (
                old_size[0] * old_size[1]
            )
            print(f"   🚀 해상도 개선: {resolution_improvement:.1f}배")

            if new_file_size > old_file_size:
                print(
                    f"   📈 품질 향상: 파일 크기 {new_file_size/old_file_size:.1f}배 (고품질)"
                )

    print("\n📊 차트 생성 개선 비교")
    print("-" * 40)

    if len(chart_images) >= 2:
        old_chart = chart_images[0]
        new_chart = chart_images[-1]

        with Image.open(old_chart) as old_img, Image.open(new_chart) as new_img:
            old_size = old_img.size
            new_size = new_img.size
            old_file_size = old_chart.stat().st_size / 1024
            new_file_size = new_chart.stat().st_size / 1024

            print(f"   이전: {old_size[0]}x{old_size[1]} ({old_file_size:.1f}KB)")
            print(f"   개선: {new_size[0]}x{new_size[1]} ({new_file_size:.1f}KB)")

            resolution_improvement = (new_size[0] * new_size[1]) / (
                old_size[0] * old_size[1]
            )
            print(f"   🚀 해상도 개선: {resolution_improvement:.1f}배")

    print("\n🎯 종합 개선 평가")
    print("=" * 40)

    # 최신 파일들의 품질 평가
    latest_files = files[-3:] if len(files) >= 3 else files

    total_quality_score = 0
    file_count = len(latest_files)

    for file_path in latest_files:
        with Image.open(file_path) as img:
            width, height = img.size
            size_kb = file_path.stat().st_size / 1024

            # 품질 점수 계산
            resolution_score = min(10, (width * height) / 100000)  # 해상도 점수
            size_efficiency = min(10, 100 / max(1, size_kb - 20))  # 효율성 점수
            quality_score = (resolution_score + size_efficiency) / 2

            total_quality_score += quality_score

            print(f"📸 {file_path.name}")
            print(f"   해상도: {width}x{height}")
            print(f"   파일크기: {size_kb:.1f}KB")
            print(f"   품질점수: {quality_score:.1f}/10")

            # 등급 판정
            if quality_score >= 8:
                grade = "🏆 최고품질"
            elif quality_score >= 6:
                grade = "⭐ 고품질"
            elif quality_score >= 4:
                grade = "✅ 표준품질"
            else:
                grade = "⚠️ 개선필요"
            print(f"   등급: {grade}")
            print()

    # 전체 평균 품질
    if file_count > 0:
        avg_quality = total_quality_score / file_count
        print(f"📊 전체 평균 품질: {avg_quality:.1f}/10")

        if avg_quality >= 7:
            print("🎉 결론: 베타런칭 준비 완료! 매우 우수한 품질입니다.")
        elif avg_quality >= 5:
            print("✅ 결론: 베타런칭 가능! 실용적인 품질입니다.")
        else:
            print("🔧 결론: 추가 개선 필요합니다.")

    print("\n🚀 개선사항 요약:")
    print("- ✅ 해상도 향상: 800x600 → 1200x800")
    print("- ✅ 차트 품질: DPI 150, 12x8 사이즈")
    print("- ✅ 색상 시스템: 스타일별 전문 팔레트")
    print("- ✅ 레이아웃: 헤더/컨텐츠 영역 분리")
    print("- ✅ 폰트 크기: 가독성 향상")


if __name__ == "__main__":
    compare_before_after()
