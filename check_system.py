#!/usr/bin/env python3
"""
🎯 AI 도깨비마을 STEM 센터 - 자동 설정 및 확인 스크립트
매번 같은 작업을 반복하지 않도록 시스템 상태를 체크하고 자동 설정
"""

import os
import sys
import json
import requests
from pathlib import Path


def check_system_status():
    """전체 시스템 상태 확인"""
    print("🔍 시스템 상태 확인 중...")

    status = {
        "files_exist": True,
        "server_running": False,
        "context_working": False,
        "expert_system": False,
    }

    # 1. 필수 파일 확인
    required_files = ["main.py", "stem_integration_new.py", "index_stem.html"]

    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ {file} 파일이 없습니다!")
            status["files_exist"] = False
        else:
            print(f"✅ {file} 확인")

    # 2. 서버 실행 상태 확인
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=2)
        if response.status_code == 200:
            print("✅ 서버가 실행 중입니다")
            status["server_running"] = True
        else:
            print("⚠️ 서버가 응답하지 않습니다")
    except:
        print("❌ 서버가 실행되지 않았습니다")

    # 3. 전문가급 시스템 확인
    if status["server_running"]:
        try:
            test_data = {"agent_type": "assistant", "question": "테스트"}
            response = requests.post(
                "http://localhost:8000/stem/chat", json=test_data, timeout=5
            )
            result = response.json()

            if result.get("success"):
                print("✅ 전문가급 시스템 작동 중")
                status["expert_system"] = True

                # 컨텍스트 추적 확인
                if "context" in result:
                    print("✅ 컨텍스트 추적 시스템 활성화")
                    status["context_working"] = True
                else:
                    print("⚠️ 컨텍스트 추적 시스템 비활성화")
            else:
                print("❌ 전문가급 시스템 오류:", result.get("error"))
        except Exception as e:
            print(f"❌ 전문가급 시스템 테스트 실패: {e}")

    return status


def show_system_info(status):
    """시스템 정보 표시"""
    print("\n" + "=" * 50)
    print("🎯 AI 도깨비마을 STEM 센터 - 시스템 현황")
    print("=" * 50)

    print(f"📁 파일 상태: {'✅ 정상' if status['files_exist'] else '❌ 불완전'}")
    print(f"🚀 서버 상태: {'✅ 실행중' if status['server_running'] else '❌ 중단'}")
    print(
        f"🧠 전문가 시스템: {'✅ 활성화' if status['expert_system'] else '❌ 비활성화'}"
    )
    print(
        f"🔄 컨텍스트 추적: {'✅ 활성화' if status['context_working'] else '❌ 비활성화'}"
    )

    if all(status.values()):
        print("\n🎉 모든 시스템이 정상 작동 중입니다!")
        print("🌐 웹사이트: http://localhost:8000")
        print("📊 API 상태: http://localhost:8000/api/health")
        print("\n✨ 이제 매번 설정할 필요 없이 바로 사용하세요!")
    else:
        print("\n⚠️ 일부 시스템에 문제가 있습니다.")
        print("💡 'start_expert_system.bat' 파일을 실행해서 서버를 시작하세요.")


def main():
    """메인 실행 함수"""
    print("🎯 AI 도깨비마을 STEM 센터 - 자동 상태 확인")
    print("=" * 50)

    # 올바른 디렉토리인지 확인
    if not os.path.exists("main.py"):
        print("❌ 올바른 디렉토리가 아닙니다!")
        print("💡 hyojin-ai-mvp 폴더에서 실행해주세요.")
        return

    # 시스템 상태 확인
    status = check_system_status()

    # 결과 표시
    show_system_info(status)


if __name__ == "__main__":
    main()
