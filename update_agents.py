#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 새로운 12개 도깨비 딕셔너리 정의
new_ai_agents = {
    "village-chief-dokkaebi": {
        "name": "🏘️ 촌장 도깨비",
        "description": "도깨비 마을의 촌장, 모든 도깨비들을 총괄하고 마을 운영 전반을 관리하는 리더",
        "capabilities": ["마을관리", "도깨비총괄", "리더십", "종합관리"],
        "autonomy_score": 99,
        "tier": "premium",
        "icon": "🏘️",
    },
    "math-dokkaebi": {
        "name": "📐 수학 도깨비",
        "description": "수학 문제 해결, 통계 분석, 수치 계산, 알고리즘 최적화 전문가 (75.78% 성과)",
        "capabilities": ["수학문제해결", "통계분석", "수치계산", "알고리즘최적화"],
        "autonomy_score": 98,
        "tier": "premium",
        "icon": "📐",
    },
    "physics-dokkaebi": {
        "name": "⚡ 물리 도깨비",
        "description": "물리학 법칙 분석, 시뮬레이션, 실험 설계, 과학적 모델링 전문가 (100% 성과)",
        "capabilities": ["물리학분석", "시뮬레이션", "실험설계", "과학적모델링"],
        "autonomy_score": 100,
        "tier": "premium",
        "icon": "⚡",
    },
    "chemistry-dokkaebi": {
        "name": "🧪 화학 도깨비",
        "description": "화학 반응 분석, 분자 구조 예측, 실험 결과 해석, 화학공정 최적화 전문가 (90% 성과)",
        "capabilities": ["화학반응분석", "분자구조예측", "실험결과해석", "화학공정최적화"],
        "autonomy_score": 90,
        "tier": "premium",
        "icon": "🧪",
    },
    "engineering-dokkaebi": {
        "name": "🔧 공학 도깨비",
        "description": "공학 설계, 시스템 분석, 기술 최적화, 엔지니어링 솔루션 전문가 (95% 성과)",
        "capabilities": ["공학설계", "시스템분석", "기술최적화", "엔지니어링솔루션"],
        "autonomy_score": 95,
        "tier": "premium",
        "icon": "🔧",
    },
    "biology-dokkaebi": {
        "name": "🧬 생물학 도깨비",
        "description": "생물학적 데이터 분석, 유전자 연구, 생태계 모델링, 바이오 기술 전문가 (88% 성과)",
        "capabilities": ["생물학데이터분석", "유전자연구", "생태계모델링", "바이오기술"],
        "autonomy_score": 88,
        "tier": "premium",
        "icon": "🧬",
    },
    "business-strategy-dokkaebi": {
        "name": "📈 비즈니스 전략 도깨비",
        "description": "경영 전략 수립, 시장 분석, 비즈니스 모델 개발, 전략적 의사결정 전문가",
        "capabilities": ["경영전략수립", "시장분석", "비즈니스모델개발", "전략적의사결정"],
        "autonomy_score": 95,
        "tier": "enterprise",
        "icon": "📈",
    },
    "communication-dokkaebi": {
        "name": "💬 커뮤니케이션 도깨비",
        "description": "소통 전략, 대화 분석, 커뮤니케이션 최적화, 관계 관리 전문가",
        "capabilities": ["소통전략", "대화분석", "커뮤니케이션최적화", "관계관리"],
        "autonomy_score": 89,
        "tier": "standard",
        "icon": "💬",
    },
    "financial-management-dokkaebi": {
        "name": "💰 재무 관리 도깨비",
        "description": "재무 계획, 투자 분석, 리스크 관리, 포트폴리오 최적화 전문가",
        "capabilities": ["재무계획", "투자분석", "리스크관리", "포트폴리오최적화"],
        "autonomy_score": 96,
        "tier": "enterprise",
        "icon": "💰",
    },
    "innovation-creation-dokkaebi": {
        "name": "🚀 혁신 창조 도깨비",
        "description": "혁신 아이디어 창출, 창의적 문제 해결, 신기술 개발, 미래 예측 전문가",
        "capabilities": ["혁신아이디어창출", "창의적문제해결", "신기술개발", "미래예측"],
        "autonomy_score": 93,
        "tier": "premium",
        "icon": "🚀",
    },
    "technology-management-dokkaebi": {
        "name": "🔧 기술 관리 도깨비",
        "description": "기술 시스템 관리, IT 인프라 최적화, 기술 전략 수립, 디지털 혁신 전문가",
        "capabilities": ["기술시스템관리", "IT인프라최적화", "기술전략수립", "디지털혁신"],
        "autonomy_score": 94,
        "tier": "premium",
        "icon": "🔧",
    },
    "user-management-dokkaebi": {
        "name": "👥 사용자 관리 도깨비",
        "description": "사용자 경험 최적화, 고객 관리, 서비스 개선, 사용자 행동 분석 전문가",
        "capabilities": ["사용자경험최적화", "고객관리", "서비스개선", "사용자행동분석"],
        "autonomy_score": 87,
        "tier": "standard",
        "icon": "👥",
    },
}

# main.py 파일 업데이트
import re

def update_main_py():
    # main.py 파일 읽기
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ai_agents 딕셔너리 찾기 및 교체
    pattern = r'ai_agents = \{.*?\n\}'
    new_agents_str = "ai_agents = {\n"
    
    for key, value in new_ai_agents.items():
        new_agents_str += f'    "{key}": {{\n'
        new_agents_str += f'        "name": "{value["name"]}",\n'
        new_agents_str += f'        "description": "{value["description"]}",\n'
        new_agents_str += f'        "capabilities": {value["capabilities"]},\n'
        new_agents_str += f'        "autonomy_score": {value["autonomy_score"]},\n'
        new_agents_str += f'        "tier": "{value["tier"]}",\n'
        new_agents_str += f'        "icon": "{value["icon"]}",\n'
        new_agents_str += '    },\n'
    
    new_agents_str += "}"
    
    # 정규식으로 교체 (DOTALL 플래그 사용)
    updated_content = re.sub(pattern, new_agents_str, content, flags=re.DOTALL)
    
    # 파일에 쓰기
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"main.py 업데이트 완료! 총 {len(new_ai_agents)}개의 도깨비 에이전트")
    for key, value in new_ai_agents.items():
        print(f"- {value['name']}")

if __name__ == "__main__":
    update_main_py()
