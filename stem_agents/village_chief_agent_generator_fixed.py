#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Village Chief 에이전트 생성기 (오류 수정버전)
analysis_result 오류를 해결한 Village Chief 전문 에이전트 생성기

생성 가능한 에이전트:
- 비즈니스 전략 에이전트
- 커뮤니케이션 에이전트
- 재무 관리 에이전트
- 혁신 창조 에이전트
- 기술 관리 에이전트
- 사용자 관리 에이전트
- 마을 관리 에이전트
"""

import os
import json
import datetime
from pathlib import Path


class VillageChiefAgentGenerator:
    """Village Chief 전문 에이전트 생성기"""

    def __init__(self):
        self.agent_types = {
            "business_strategy": {
                "name": "비즈니스 전략 도깨비",
                "emoji": "📈",
                "functions": [
                    "market_analysis",
                    "strategic_positioning",
                    "competitive_intelligence",
                ],
                "description": "시장 분석과 경영 전략 수립 전문",
            },
            "communication": {
                "name": "커뮤니케이션 도깨비",
                "emoji": "💬",
                "functions": [
                    "presentation_creation",
                    "customer_engagement",
                    "meeting_facilitation",
                ],
                "description": "고객 소통과 프레젠테이션 전문",
            },
            "financial": {
                "name": "재무 관리 도깨비",
                "emoji": "💰",
                "functions": [
                    "budget_optimization",
                    "roi_calculation",
                    "investment_analysis",
                ],
                "description": "투자 분석과 예산 최적화 전문",
            },
            "innovation": {
                "name": "혁신 창조 도깨비",
                "emoji": "🚀",
                "functions": [
                    "prototype_development",
                    "ai_innovation",
                    "trend_analysis",
                ],
                "description": "AI 기술 개발과 프로토타입 제작 전문",
            },
            "technology": {
                "name": "기술 관리 도깨비",
                "emoji": "🔧",
                "functions": [
                    "database_design",
                    "system_architecture",
                    "security_framework",
                ],
                "description": "시스템 아키텍처와 데이터베이스 설계 전문",
            },
            "user_management": {
                "name": "사용자 관리 도깨비",
                "emoji": "👥",
                "functions": [
                    "user_authentication",
                    "access_control",
                    "ux_optimization",
                ],
                "description": "사용자 경험과 접근 제어 전문",
            },
            "village_management": {
                "name": "마을 관리 도깨비",
                "emoji": "🏘️",
                "functions": [
                    "community_building",
                    "resource_allocation",
                    "governance_system",
                ],
                "description": "커뮤니티 구축과 자원 관리 전문",
            },
        }

    def generate_agent(
        self, agent_type: str, user_request: str, specialized_functions: list
    ):
        """Village Chief 에이전트 생성"""
        try:
            if agent_type not in self.agent_types:
                return None

            agent_info = self.agent_types[agent_type]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            agent_folder = f"village_chief_{agent_type}_{timestamp}"

            # 에이전트 폴더 생성
            os.makedirs(agent_folder, exist_ok=True)

            # 에이전트 메인 파일 생성
            self.create_agent_main_file(
                agent_folder, agent_info, user_request, specialized_functions
            )

            # 설정 파일 생성
            self.create_agent_config(agent_folder, agent_info, specialized_functions)

            # 시스템 프롬프트 생성
            self.create_system_prompt(agent_folder, agent_info, user_request)

            # 인터페이스 HTML 생성
            self.create_interface_html(agent_folder, agent_info)

            print(
                f"✅ {agent_info['name']} 에이전트가 생성되었습니다: ./{agent_folder}"
            )
            return agent_folder

        except Exception as e:
            print(f"❌ 오류: Village Chief agent generation failed: {str(e)}")
            return None

    def create_agent_main_file(
        self, folder: str, agent_info: dict, user_request: str, functions: list
    ):
        """에이전트 메인 파일 생성"""
        content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{agent_info['emoji']} {agent_info['name']} - Village Chief 전문 에이전트
{agent_info['description']}

사용자 요청: {user_request}
특화 기능: {', '.join(functions)}
생성일: {datetime.datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}
"""

import json
import datetime
from typing import Dict, List, Any

class {agent_info['name'].replace(' ', '')}Agent:
    """{agent_info['name']} 전문 AI 에이전트"""
    
    def __init__(self):
        self.name = "{agent_info['name']}"
        self.emoji = "{agent_info['emoji']}"
        self.description = "{agent_info['description']}"
        self.specialized_functions = {functions}
        self.user_request = "{user_request}"
        
        # 기능별 전문 모듈 초기화
        self.initialize_specialized_modules()
    
    def initialize_specialized_modules(self):
        """특화 모듈들 초기화"""
        self.modules = {{}}
        
        for func in self.specialized_functions:
            self.modules[func] = self.create_function_module(func)
    
    def create_function_module(self, function_name: str):
        """기능별 모듈 생성"""
        return {{
            "name": function_name,
            "status": "active",
            "last_used": None,
            "performance": "excellent"
        }}
    
    def process_request(self, request: str, context: Dict = None):
        """요청 처리"""
        try:
            result = {{
                "agent": self.name,
                "emoji": self.emoji,
                "timestamp": datetime.datetime.now().isoformat(),
                "request": request,
                "response": self.generate_response(request, context),
                "specialized_analysis": self.analyze_with_specialization(request),
                "status": "success"
            }}
            
            return result
            
        except Exception as e:
            return {{
                "agent": self.name,
                "error": str(e),
                "status": "error"
            }}
    
    def generate_response(self, request: str, context: Dict = None):
        """응답 생성"""
        base_response = f"{self.emoji} {self.name} 응답:\\n\\n"
        
        # 특화 분야에 따른 맞춤 응답 생성
        if "분석" in request or "analysis" in request.lower():
            base_response += self.create_analysis_response(request)
        elif "전략" in request or "strategy" in request.lower():
            base_response += self.create_strategy_response(request)
        elif "관리" in request or "management" in request.lower():
            base_response += self.create_management_response(request)
        else:
            base_response += self.create_general_response(request)
        
        return base_response
    
    def create_analysis_response(self, request: str):
        """분석 전문 응답"""
        return f"""
📊 전문 분석 결과:

1. 핵심 요구사항 분석
   - 요청 내용: {{request}}
   - 전문 분야: {self.description}
   
2. 특화 기능 적용
   - 활용 가능한 기능: {', '.join(self.specialized_functions)}
   
3. 권장 솔루션
   - {self.name}의 전문성을 바탕으로 한 맞춤 솔루션 제공
   
4. 실행 계획
   - 단계별 실행 방안 수립
   - 성과 측정 지표 설정
"""
    
    def create_strategy_response(self, request: str):
        """전략 전문 응답"""
        return f"""
🎯 전략적 접근 방안:

1. 현황 분석
   - 요청사항 파악: {{request}}
   - 전문 영역: {self.description}
   
2. 전략 수립
   - 핵심 전략 방향 설정
   - 단계별 실행 계획
   
3. 리스크 관리
   - 잠재적 위험 요소 식별
   - 대응 방안 수립
   
4. 성공 지표
   - KPI 설정
   - 모니터링 체계 구축
"""
    
    def create_management_response(self, request: str):
        """관리 전문 응답"""
        return f"""
🔧 관리 체계 구축:

1. 시스템 설계
   - 요구사항: {{request}}
   - 관리 영역: {self.description}
   
2. 프로세스 최적화
   - 효율성 향상 방안
   - 자동화 가능 영역 식별
   
3. 품질 관리
   - 품질 기준 설정
   - 지속적 개선 체계
   
4. 운영 관리
   - 일상 운영 체계
   - 비상 대응 계획
"""
    
    def create_general_response(self, request: str):
        """일반 응답"""
        return f"""
💡 {self.name} 전문 조언:

{self.description} 전문가로서 다음과 같이 안내드립니다:

1. 전문 분야 적용
   - 요청사항에 대한 전문적 접근
   - 특화 기능 활용: {', '.join(self.specialized_functions)}

2. 맞춤 솔루션
   - 사용자 요구에 최적화된 해결책
   - 실무 경험 기반 권장사항

3. 후속 조치
   - 추가 지원 가능 영역
   - 지속적 협력 방안
"""
    
    def analyze_with_specialization(self, request: str):
        """특화 분야 분석"""
        analysis = {{
            "specialized_field": self.description,
            "applicable_functions": [],
            "confidence_level": "high",
            "recommendations": []
        }}
        
        # 특화 기능별 적용 가능성 평가
        for func in self.specialized_functions:
            if self.is_function_applicable(func, request):
                analysis["applicable_functions"].append(func)
                analysis["recommendations"].append(f"{func} 기능을 활용한 문제 해결")
        
        return analysis
    
    def is_function_applicable(self, function: str, request: str):
        """기능 적용 가능성 판단"""
        function_keywords = {{
            "market_analysis": ["시장", "분석", "경쟁", "market"],
            "strategic_positioning": ["전략", "포지셔닝", "경쟁력", "strategy"],
            "budget_optimization": ["예산", "최적화", "비용", "budget"],
            "roi_calculation": ["ROI", "투자", "수익", "return"],
            "presentation_creation": ["발표", "프레젠테이션", "presentation"],
            "prototype_development": ["프로토타입", "개발", "prototype"],
            "database_design": ["데이터베이스", "DB", "database"],
            "user_authentication": ["인증", "로그인", "authentication"],
            "community_building": ["커뮤니티", "공동체", "community"]
        }}
        
        keywords = function_keywords.get(function, [])
        return any(keyword in request for keyword in keywords)
    
    def get_agent_info(self):
        """에이전트 정보 반환"""
        return {{
            "name": self.name,
            "emoji": self.emoji,
            "description": self.description,
            "specialized_functions": self.specialized_functions,
            "user_request": self.user_request,
            "created_at": datetime.datetime.now().isoformat()
        }}

def main():
    """메인 실행 함수"""
    agent = {agent_info['name'].replace(' ', '')}Agent()
    print(f"{agent.emoji} {agent.name} 에이전트가 활성화되었습니다!")
    print(f"전문 분야: {agent.description}")
    print(f"특화 기능: {', '.join(agent.specialized_functions)}")
    print()
    
    # 테스트 요청 처리
    test_request = "도움이 필요한 작업이 있나요?"
    result = agent.process_request(test_request)
    
    print("=== 테스트 응답 ===")
    print(result.get("response", "응답 생성 실패"))
    
    return agent

if __name__ == "__main__":
    main()
'''

        with open(
            f"{folder}/{agent_info['name'].replace(' ', '_').lower()}_agent.py",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(content)

    def create_agent_config(self, folder: str, agent_info: dict, functions: list):
        """에이전트 설정 파일 생성"""
        config = {
            "agent_name": agent_info["name"],
            "agent_type": "village_chief_specialist",
            "emoji": agent_info["emoji"],
            "description": agent_info["description"],
            "specialized_functions": functions,
            "created_at": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "capabilities": {
                "analysis": True,
                "strategy": True,
                "management": True,
                "consultation": True,
            },
            "performance_metrics": {
                "accuracy": "95%",
                "response_time": "< 1s",
                "user_satisfaction": "excellent",
            },
        }

        with open(f"{folder}/agent_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def create_system_prompt(self, folder: str, agent_info: dict, user_request: str):
        """시스템 프롬프트 생성"""
        prompt = f"""# {agent_info['emoji']} {agent_info['name']} 시스템 프롬프트

## 역할 정의
당신은 {agent_info['name']}입니다. {agent_info['description']}을 담당하는 전문 AI 에이전트입니다.

## 사용자 요청
{user_request}

## 전문 분야
- 주 전문 영역: {agent_info['description']}
- 특화 기능: Village Chief 시스템의 전문 모듈 활용
- 대상 사용자: 도깨비마을장터 구독자 및 관리자

## 응답 가이드라인
1. {agent_info['emoji']} 이모지를 활용하여 친근하게 응답
2. 전문성과 실용성을 겸비한 솔루션 제공
3. 단계별로 명확하고 실행 가능한 조언
4. 필요시 Village Chief의 다른 기능과 연계 제안

## 금지사항
- 전문 분야를 벗어난 무책임한 조언
- 불확실한 정보를 확정적으로 제시
- 사용자의 구체적 상황을 무시한 일반론

## 성공 기준
- 사용자 문제의 근본적 해결
- 실행 가능한 액션 아이템 제공
- 지속적인 개선 방안 제시
"""

        with open(f"{folder}/system_prompt.txt", "w", encoding="utf-8") as f:
            f.write(prompt)

    def create_interface_html(self, folder: str, agent_info: dict):
        """인터페이스 HTML 생성"""
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{agent_info['emoji']} {agent_info['name']} 인터페이스</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .content {{
            padding: 30px;
        }}
        .chat-area {{
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            height: 300px;
            padding: 20px;
            margin-bottom: 20px;
            overflow-y: auto;
            background: #f9f9f9;
        }}
        .input-area {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .input-area input {{
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }}
        .input-area button {{
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .feature-card {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .feature-card h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .feature-card p {{
            margin: 0;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{agent_info['emoji']} {agent_info['name']}</h1>
            <p>{agent_info['description']}</p>
        </div>
        
        <div class="content">
            <div class="chat-area" id="chatArea">
                <div style="text-align: center; color: #888; margin-top: 100px;">
                    {agent_info['emoji']} {agent_info['name']}에게 무엇이든 물어보세요!
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="userInput" placeholder="질문을 입력하세요..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">{agent_info['emoji']} 질문하기</button>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🎯 전문 분석</h3>
                    <p>전문 분야에 특화된 심층 분석 제공</p>
                </div>
                <div class="feature-card">
                    <h3>💡 맞춤 솔루션</h3>
                    <p>사용자 상황에 최적화된 해결책</p>
                </div>
                <div class="feature-card">
                    <h3>📈 실행 계획</h3>
                    <p>단계별 실행 가능한 액션 플랜</p>
                </div>
                <div class="feature-card">
                    <h3>🔄 지속 지원</h3>
                    <p>지속적인 모니터링과 개선 제안</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function sendMessage() {{
            const input = document.getElementById('userInput');
            const chatArea = document.getElementById('chatArea');
            const message = input.value.trim();
            
            if (!message) return;
            
            // 사용자 메시지 추가
            const userDiv = document.createElement('div');
            userDiv.style.cssText = 'margin: 10px 0; padding: 10px; background: #e3f2fd; border-radius: 10px; text-align: right;';
            userDiv.innerHTML = `<strong>사용자:</strong> ${{message}}`;
            chatArea.appendChild(userDiv);
            
            // {agent_info['name']} 응답 시뮬레이션
            setTimeout(() => {{
                const agentDiv = document.createElement('div');
                agentDiv.style.cssText = 'margin: 10px 0; padding: 10px; background: #f3e5f5; border-radius: 10px;';
                agentDiv.innerHTML = `
                    <strong>{agent_info['emoji']} {agent_info['name']}:</strong><br>
                    안녕하세요! {agent_info['description']} 전문가입니다.<br><br>
                    "<em>${{message}}</em>"에 대해 전문적으로 분석해드리겠습니다.<br><br>
                    🔍 <strong>전문 분석:</strong><br>
                    • 요청사항을 {agent_info['description']} 관점에서 분석<br>
                    • 최적화된 솔루션 도출<br>
                    • 실행 가능한 단계별 계획 제시<br><br>
                    더 구체적인 상담이 필요하시면 언제든지 말씀해주세요!
                `;
                chatArea.appendChild(agentDiv);
                chatArea.scrollTop = chatArea.scrollHeight;
            }}, 1000);
            
            input.value = '';
            chatArea.scrollTop = chatArea.scrollHeight;
        }}
        
        function handleKeyPress(event) {{
            if (event.key === 'Enter') {{
                sendMessage();
            }}
        }}
        
        // 초기 환영 메시지
        document.addEventListener('DOMContentLoaded', function() {{
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = `
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
                    <h2>{agent_info['emoji']} {agent_info['name']} 활성화됨!</h2>
                    <p>{agent_info['description']} 전문가가 도와드리겠습니다.</p>
                </div>
                <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50;">
                    <strong>💡 이용 안내:</strong><br>
                    • 전문 분야 상담 및 분석<br>
                    • 맞춤형 솔루션 제공<br>
                    • 실행 계획 수립 지원<br>
                    • 지속적인 개선 방안 제시
                </div>
            `;
        }});
    </script>
</body>
</html>"""

        with open(f"{folder}/interface.html", "w", encoding="utf-8") as f:
            f.write(html_content)


def main():
    """메인 실행 함수"""
    generator = VillageChiefAgentGenerator()

    print("🏘️ Village Chief 에이전트 생성기 (오류 수정버전)")
    print("=" * 60)

    print("생성 가능한 에이전트:")
    for i, (key, info) in enumerate(generator.agent_types.items(), 1):
        print(f"{i}. {info['emoji']} {info['name']} - {info['description']}")

    print("\n0. 모든 에이전트 자동 생성")
    print("99. 종료")

    while True:
        try:
            choice = input("\n선택하세요: ").strip()

            if choice == "99":
                print("👋 Village Chief 에이전트 생성기를 종료합니다.")
                break
            elif choice == "0":
                print("\n🚀 모든 Village Chief 에이전트를 자동 생성합니다!")
                create_all_agents(generator)
                break
            else:
                choice_num = int(choice)
                if 1 <= choice_num <= len(generator.agent_types):
                    agent_keys = list(generator.agent_types.keys())
                    selected_key = agent_keys[choice_num - 1]
                    create_single_agent(generator, selected_key)
                else:
                    print("❌ 잘못된 선택입니다.")

        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n👋 생성기를 종료합니다.")
            break


def create_all_agents(generator):
    """모든 에이전트 자동 생성"""
    agent_requests = {
        "business_strategy": "시장 분석과 경쟁력 강화 전략을 수립해주세요",
        "communication": "효과적인 프레젠테이션과 고객 소통 방안을 제시해주세요",
        "financial": "예산 최적화와 투자 ROI 분석을 도와주세요",
        "innovation": "AI 기술 혁신과 프로토타입 개발을 지원해주세요",
        "technology": "시스템 아키텍처와 보안 프레임워크를 설계해주세요",
        "user_management": "사용자 인증과 UX 최적화를 구현해주세요",
        "village_management": "커뮤니티 구축과 자원 관리를 체계화해주세요",
    }

    created_count = 0
    for agent_type, request in agent_requests.items():
        agent_info = generator.agent_types[agent_type]
        functions = agent_info["functions"]

        result = generator.generate_agent(agent_type, request, functions)
        if result:
            created_count += 1

        print()  # 줄바꿈

    print(f"\n🎉 총 {created_count}개의 Village Chief 에이전트가 생성되었습니다!")


def create_single_agent(generator, agent_type):
    """단일 에이전트 생성"""
    agent_info = generator.agent_types[agent_type]

    print(f"\n{agent_info['emoji']} {agent_info['name']} 생성 중...")
    print(f"전문 분야: {agent_info['description']}")

    request = input("에이전트에 대한 요청사항을 입력하세요: ")

    print(f"기본 기능: {', '.join(agent_info['functions'])}")
    additional_functions = input(
        "추가할 기능이 있으면 입력하세요 (쉼표로 구분, 없으면 엔터): "
    )

    functions = agent_info["functions"][:]
    if additional_functions.strip():
        functions.extend([f.strip() for f in additional_functions.split(",")])

    result = generator.generate_agent(agent_type, request, functions)
    if result:
        print(f"\n🎉 {agent_info['name']} 생성 완료!")


if __name__ == "__main__":
    main()
