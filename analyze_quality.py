"""
v5.0 생성형 콘텐츠 품질 분석 도구
"""

import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def analyze_image_quality(image_path):
    """이미지 품질 분석"""
    try:
        with Image.open(image_path) as img:
            # 기본 정보
            width, height = img.size
            mode = img.mode
            format_type = img.format

            # 이미지를 numpy 배열로 변환
            img_array = np.array(img)

            # 품질 메트릭 계산
            resolution_score = min(10, (width * height) / 100000)  # 해상도 점수

            # 색상 다양성 분석
            if len(img_array.shape) == 3:  # 컬러 이미지
                color_variance = np.var(img_array.flatten())
                color_diversity = min(10, color_variance / 1000)
            else:
                color_diversity = 5  # 흑백 이미지

            # 선명도 분석 (간단한 엣지 검출)
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array

            # 라플라시안 필터로 선명도 측정
            laplacian_var = np.var(np.gradient(gray))
            sharpness_score = min(10, laplacian_var / 100)

            return {
                "file_name": os.path.basename(image_path),
                "resolution": f"{width}x{height}",
                "format": format_type,
                "mode": mode,
                "file_size_kb": os.path.getsize(image_path) / 1024,
                "resolution_score": round(resolution_score, 2),
                "color_diversity": round(color_diversity, 2),
                "sharpness_score": round(sharpness_score, 2),
                "overall_quality": round(
                    (resolution_score + color_diversity + sharpness_score) / 3, 2
                ),
            }
    except Exception as e:
        return {"error": str(e)}


def analyze_all_generated_content():
    """생성된 모든 콘텐츠 품질 분석"""
    output_dir = Path("multimodal_output")

    if not output_dir.exists():
        print("❌ multimodal_output 디렉터리가 없습니다.")
        return

    print("🔍 v5.0 생성형 콘텐츠 품질 분석")
    print("=" * 60)

    image_files = list(output_dir.glob("*.png"))

    if not image_files:
        print("❌ 분석할 이미지 파일이 없습니다.")
        return

    print(f"📊 총 {len(image_files)}개 파일 분석 중...")
    print()

    expert_images = []
    chart_images = []
    infographic_images = []

    for img_path in sorted(image_files, key=lambda x: x.stat().st_mtime, reverse=True):
        analysis = analyze_image_quality(str(img_path))

        if "error" in analysis:
            print(f"❌ {img_path.name}: {analysis['error']}")
            continue

        # 파일 타입별 분류
        if "expert_" in img_path.name:
            expert_images.append(analysis)
        elif "chart_" in img_path.name:
            chart_images.append(analysis)
        elif "infographic_" in img_path.name:
            infographic_images.append(analysis)

    # 전문가 이미지 분석
    if expert_images:
        print("🧑‍💼 전문가 이미지 품질 분석")
        print("-" * 40)
        for img in expert_images[:3]:  # 최근 3개만
            print(f"📸 {img['file_name']}")
            print(f"   📏 해상도: {img['resolution']} ({img['resolution_score']}/10)")
            print(f"   🎨 색상 다양성: {img['color_diversity']}/10")
            print(f"   🔍 선명도: {img['sharpness_score']}/10")
            print(f"   📊 종합 품질: {img['overall_quality']}/10")
            print(f"   💾 파일 크기: {img['file_size_kb']:.1f}KB")

            # 품질 등급 판정
            if img["overall_quality"] >= 8:
                grade = "🏆 최고"
            elif img["overall_quality"] >= 6:
                grade = "⭐ 양호"
            elif img["overall_quality"] >= 4:
                grade = "✅ 보통"
            else:
                grade = "⚠️ 개선 필요"
            print(f"   🎯 품질 등급: {grade}")
            print()

    # 차트 이미지 분석
    if chart_images:
        print("📊 차트 이미지 품질 분석")
        print("-" * 40)
        for img in chart_images[:3]:  # 최근 3개만
            print(f"📈 {img['file_name']}")
            print(f"   📏 해상도: {img['resolution']} ({img['resolution_score']}/10)")
            print(f"   🎨 색상 다양성: {img['color_diversity']}/10")
            print(f"   🔍 선명도: {img['sharpness_score']}/10")
            print(f"   📊 종합 품질: {img['overall_quality']}/10")
            print(f"   💾 파일 크기: {img['file_size_kb']:.1f}KB")

            # 차트 특화 품질 판정
            if img["overall_quality"] >= 7 and img["file_size_kb"] > 50:
                grade = "🏆 고품질 차트"
            elif img["overall_quality"] >= 5:
                grade = "⭐ 실용적"
            else:
                grade = "⚠️ 개선 필요"
            print(f"   🎯 차트 품질: {grade}")
            print()

    # 종합 품질 평가
    all_images = expert_images + chart_images + infographic_images
    if all_images:
        avg_quality = sum(img["overall_quality"] for img in all_images) / len(
            all_images
        )
        avg_size = sum(img["file_size_kb"] for img in all_images) / len(all_images)

        print("🎯 종합 품질 평가")
        print("=" * 40)
        print(f"📊 평균 품질 점수: {avg_quality:.2f}/10")
        print(f"💾 평균 파일 크기: {avg_size:.1f}KB")

        if avg_quality >= 7:
            print("🏆 전체적으로 매우 좋은 품질입니다!")
        elif avg_quality >= 5:
            print("⭐ 실용적인 수준의 품질입니다.")
        else:
            print("⚠️ 품질 개선이 필요합니다.")

    print("\n🔧 품질 개선 제안:")
    print("- 해상도 향상: 1200x800 이상 권장")
    print("- 폰트 크기 최적화: 가독성 향상")
    print("- 색상 조합 개선: 대비 강화")
    print("- 파일 압축 최적화: 품질 유지하며 용량 최적화")


if __name__ == "__main__":
    analyze_all_generated_content()
