#!/usr/bin/env python3
"""
서버 상태 및 전문가 목록 확인
"""

import requests
import json


def check_server_status():
    """서버 상태 확인"""
    try:
        response = requests.get("http://localhost:8005/ai_status")
        if response.status_code == 200:
            result = response.json()
            print("✅ 서버 연결 성공!")
            print(f"AI 활성화: {result.get('ai_enabled', False)}")
            print(f"시스템 타입: {result.get('ai_type', 'Unknown')}")
            return True
        else:
            print(f"❌ 서버 응답 오류: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return False


def get_agents():
    """전문가 목록 가져오기"""
    try:
        response = requests.get("http://localhost:8005/agents")
        if response.status_code == 200:
            result = response.json()
            print("\n📋 전문가 목록:")
            for agent_type, info in result.items():
                print(f"  {info['emoji']} {agent_type}: {info['name']}")
            return True
        else:
            print(f"❌ 전문가 목록 오류: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 전문가 목록 실패: {e}")
        return False


print("🔍 서버 상태 확인 중...")
if check_server_status():
    get_agents()
else:
    print("서버가 실행되지 않았거나 연결할 수 없습니다.")
    print("http://localhost:8005 에서 서버가 실행 중인지 확인하세요.")
