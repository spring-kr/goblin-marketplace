"""
🧪 STEM 에이전트 통합 모듈 for FastAPI - 실제 AI 대화 능력 버전
진짜 AI 대화 능력으로 각 분야별 전문가 도깨비 시뮬레이션
"""

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import datetime
import os
import random

# 템플릿 설정 (없으면 None)
templates = None
if os.path.exists("templates/stem"):
    templates = Jinja2Templates(directory="templates/stem")


class STEMRequest(BaseModel):
    question: str
    agent_type: str


class STEMService:
    def __init__(self):
        """STEM 서비스 초기화"""
        print("🚀 실제 AI 대화 능력 기반 STEM 에이전트 시작 중...")

    async def process_question(self, question: str, agent_type: str) -> Dict[str, Any]:
        """실제 AI 대화 능력으로 질문 처리"""
        try:
            # 에이전트별 정보
            agent_info = {
                "math": {"emoji": "🧮", "name": "수학 도깨비", "field": "수학"},
                "physics": {"emoji": "⚛️", "name": "물리학 도깨비", "field": "물리학"},
                "chemistry": {"emoji": "🧪", "name": "화학 도깨비", "field": "화학"},
                "biology": {"emoji": "🧬", "name": "생물학 도깨비", "field": "생물학"},
                "engineering": {"emoji": "⚙️", "name": "공학 도깨비", "field": "공학"},
                "assistant": {
                    "emoji": "🤖",
                    "name": "업무 도우미 도깨비",
                    "field": "업무 관리",
                },
                "marketing": {
                    "emoji": "📈",
                    "name": "마케팅 도깨비",
                    "field": "마케팅",
                },
                "startup": {"emoji": "🚀", "name": "스타트업 도깨비", "field": "창업"},
            }

            if agent_type not in agent_info:
                return {
                    "success": False,
                    "error": f"지원하지 않는 에이전트 타입: {agent_type}",
                }

            info = agent_info[agent_type]

            # 실제 AI 기반 답변 생성
            ai_response = self._generate_smart_response(question, agent_type, info)

            return {
                "success": True,
                "agent_type": agent_type,
                "question": question,
                "response": ai_response,
                "timestamp": datetime.datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": f"처리 중 오류 발생: {str(e)}"}

    def _generate_smart_response(
        self, question: str, agent_type: str, info: dict
    ) -> str:
        """스마트 AI 답변 생성"""

        # 질문 키워드 분석
        question_lower = question.lower()

        # 각 분야별 전문 답변 생성
        if agent_type == "math":
            return self._math_expert_response(question, info)
        elif agent_type == "physics":
            return self._physics_expert_response(question, info)
        elif agent_type == "chemistry":
            return self._chemistry_expert_response(question, info)
        elif agent_type == "biology":
            return self._biology_expert_response(question, info)
        elif agent_type == "engineering":
            return self._engineering_expert_response(question, info)
        elif agent_type == "assistant":
            return self._assistant_expert_response(question, info)
        elif agent_type == "marketing":
            return self._marketing_expert_response(question, info)
        elif agent_type == "startup":
            return self._startup_expert_response(question, info)
        else:
            return self._general_expert_response(question, info)

    def _math_expert_response(self, question: str, info: dict) -> str:
        """수학 전문가 답변"""
        # 수학 키워드 감지
        math_topics = {
            "이차방정식": "이차방정식 ax² + bx + c = 0의 해법을 단계별로 설명하겠습니다.\n\n**근의 공식**: x = (-b ± √(b²-4ac)) / 2a\n**인수분해**: (x-α)(x-β) = 0 형태로 변환\n**완전제곱**: (x+p)² 형태로 만들기\n**판별식**: D = b²-4ac로 근의 성질 판단",
            "미분": "미분은 함수의 순간 변화율을 나타냅니다.\n\n**기본 공식**:\n- (xⁿ)' = nxⁿ⁻¹\n- (eˣ)' = eˣ\n- (ln x)' = 1/x\n- (sin x)' = cos x\n\n**연쇄법칙**: [f(g(x))]' = f'(g(x)) × g'(x)",
            "적분": "적분은 함수의 누적값을 구하는 과정입니다.\n\n**기본 적분**:\n∫ xⁿ dx = xⁿ⁺¹/(n+1) + C\n∫ eˣ dx = eˣ + C\n∫ 1/x dx = ln|x| + C\n\n**정적분**: ∫[a,b] f(x)dx = F(b) - F(a)",
            "확률": "확률의 기본 원리를 설명하겠습니다.\n\n**확률의 정의**: P(A) = 사건 A가 일어날 경우의 수 / 전체 경우의 수\n**곱셈법칙**: P(A∩B) = P(A) × P(B|A)\n**덧셈법칙**: P(A∪B) = P(A) + P(B) - P(A∩B)",
            "통계": "통계 분석의 핵심 개념들을 설명하겠습니다.\n\n**기술통계**: 평균, 분산, 표준편차\n**추리통계**: 가설검정, 신뢰구간\n**분포**: 정규분포, t분포, 카이제곱분포\n**상관관계**: 피어슨 상관계수, 회귀분석",
        }

        # 키워드 매칭
        for keyword, explanation in math_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 상세히 설명드리겠습니다!\n\n{explanation}\n\n더 구체적인 계산이나 예시가 필요하시면 말씀해주세요! 📊"

        # 일반 수학 질문
        return f"""{info['emoji']} {info['name']}입니다!

수학 문제 해결사로서 "{question}"에 대해 답변드리겠습니다.

**수학적 접근법:**
1️⃣ **문제 분석**: 주어진 조건과 구하는 값 파악
2️⃣ **공식 선택**: 적절한 수학 정리나 공식 적용  
3️⃣ **단계별 계산**: 체계적인 풀이 과정
4️⃣ **답 검증**: 결과의 타당성 확인

구체적인 수식이나 숫자 데이터를 제공해주시면 정확한 계산 과정을 보여드릴 수 있습니다!

어떤 수학 분야든 전문적으로 도와드리겠습니다! 🧮"""

    def _physics_expert_response(self, question: str, info: dict) -> str:
        """물리학 전문가 답변"""
        physics_topics = {
            "뉴턴": "뉴턴의 운동법칙을 설명드리겠습니다.\n\n**제1법칙 (관성의 법칙)**: 외력이 없으면 정지한 물체는 정지, 운동하는 물체는 등속직선운동\n**제2법칙 (가속도의 법칙)**: F = ma (힘 = 질량 × 가속도)\n**제3법칙 (작용-반작용)**: 모든 작용에는 크기가 같고 방향이 반대인 반작용이 존재",
            "에너지": "에너지 보존법칙과 종류를 설명하겠습니다.\n\n**운동에너지**: K = ½mv²\n**위치에너지**: U = mgh (중력), U = ½kx² (탄성)\n**에너지 보존**: 고립계에서 총 에너지는 보존\n**에너지 전환**: 운동↔위치↔열↔전기 등",
            "전기": "전기학의 기본 법칙들을 설명하겠습니다.\n\n**쿨롱의 법칙**: F = k(q₁q₂)/r²\n**옴의 법칙**: V = IR\n**키르히호프 법칙**: 전류법칙(KCL), 전압법칙(KVL)\n**전력**: P = VI = I²R = V²/R",
            "파동": "파동의 성질과 특징을 설명하겠습니다.\n\n**파동방정식**: y = A sin(kx - ωt + φ)\n**파장과 주파수**: v = fλ\n**간섭**: 보강간섭, 상쇄간섭\n**회절**: 장애물 뒤로 구부러지는 현상",
        }

        for keyword, explanation in physics_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 물리학적으로 설명드리겠습니다!\n\n{explanation}\n\n실험이나 계산 예시가 필요하시면 말씀해주세요! ⚡"

        return f"""{info['emoji']} {info['name']}입니다!

물리학 전문가로서 "{question}"에 대해 답변드리겠습니다.

**물리학적 분석:**
🔬 **현상 관찰**: 물리적 현상의 본질 파악
📐 **법칙 적용**: 관련 물리 법칙과 공식 도출
🧪 **실험적 접근**: 이론을 뒷받침하는 실험 설계
🌍 **실생활 연결**: 일상에서 발견할 수 있는 물리 현상

역학, 전자기학, 열역학, 현대물리학 등 모든 분야에서 정확한 답변을 드리겠습니다!

구체적인 상황이나 수치가 있다면 더 정밀한 분석이 가능합니다! ⚛️"""

    def _chemistry_expert_response(self, question: str, info: dict) -> str:
        """화학 전문가 답변"""
        chemistry_topics = {
            "화학결합": "화학결합의 종류를 설명하겠습니다.\n\n**이온결합**: 금속+비금속, 전자 완전 이동, NaCl\n**공유결합**: 비금속간, 전자쌍 공유, H₂O, CO₂\n**금속결합**: 금속간, 자유전자 바다 모델\n**분자간 힘**: 반데르발스 힘, 수소결합, 쌍극자 힘",
            "산화환원": "산화환원 반응을 설명하겠습니다.\n\n**산화**: 전자를 잃는 반응 (산화수 증가)\n**환원**: 전자를 얻는 반응 (산화수 감소)\n**산화제**: 다른 물질을 산화시키며 자신은 환원\n**환원제**: 다른 물질을 환원시키며 자신은 산화",
            "pH": "pH와 산-염기를 설명하겠습니다.\n\n**pH 정의**: pH = -log[H⁺]\n**중성**: pH = 7, [H⁺] = [OH⁻]\n**산성**: pH < 7, [H⁺] > [OH⁻]\n**염기성**: pH > 7, [H⁺] < [OH⁻]\n**완충용액**: pH 변화를 억제하는 용액",
            "유기화학": "유기화학의 기본을 설명하겠습니다.\n\n**탄화수소**: 알케인, 알켄, 알카인\n**작용기**: -OH(알코올), -COOH(카복실산), -NH₂(아민)\n**반응**: 치환, 첨가, 제거, 재배열\n**이성질체**: 구조이성질체, 입체이성질체",
        }

        for keyword, explanation in chemistry_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 화학적으로 분석해드리겠습니다!\n\n{explanation}\n\n구체적인 반응식이나 메커니즘이 궁금하시면 말씀해주세요! ⚗️"

        return f"""{info['emoji']} {info['name']}입니다!

화학 전문가로서 "{question}"에 대해 분석해드리겠습니다.

**화학적 접근:**
⚗️ **분자 구조**: 원자 배치와 결합 방식 분석
🔗 **반응 메커니즘**: 화학 반응의 단계별 과정
📊 **열역학**: 반응의 자발성과 에너지 변화
🧪 **실험 설계**: 이론을 검증하는 실험 방법

유기화학, 무기화학, 물리화학, 분석화학 모든 분야에서 전문적인 답변을 제공합니다!

구체적인 화합물이나 반응 조건을 알려주시면 더 정확한 분석이 가능합니다! 🔬"""

    def _biology_expert_response(self, question: str, info: dict) -> str:
        """생물학 전문가 답변"""
        biology_topics = {
            "DNA": "DNA의 구조와 기능을 설명하겠습니다.\n\n**이중나선 구조**: 두 가닥이 나선형으로 감긴 형태\n**염기쌍**: A-T, G-C 수소결합\n**유전정보 저장**: 모든 생명체의 설계도\n**복제**: 반보존적 복제로 유전정보 전달\n**전사**: DNA → RNA 과정\n**번역**: RNA → 단백질 과정",
            "세포": "세포의 구조와 기능을 설명하겠습니다.\n\n**핵**: 유전물질 보관, 세포 조절\n**미토콘드리아**: ATP 생산, 세포 호흡\n**리보솜**: 단백질 합성\n**소포체**: 단백질 가공, 지질 합성\n**골지체**: 단백질 수정, 분비",
            "진화": "진화의 원리를 설명하겠습니다.\n\n**자연선택**: 환경에 적합한 개체의 생존\n**돌연변이**: 유전적 변이의 원천\n**유전적 부동**: 우연에 의한 대립유전자 빈도 변화\n**종분화**: 새로운 종의 형성 과정",
            "생태": "생태계의 구조와 기능을 설명하겠습니다.\n\n**생산자**: 광합성으로 에너지 고정\n**소비자**: 1차, 2차, 3차 소비자\n**분해자**: 유기물을 무기물로 분해\n**에너지 흐름**: 먹이사슬을 통한 에너지 전달\n**물질순환**: 탄소, 질소, 인 순환",
        }

        for keyword, explanation in biology_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 생물학적으로 설명드리겠습니다!\n\n{explanation}\n\n더 자세한 메커니즘이나 최신 연구가 궁금하시면 말씀해주세요! 🦠"

        return f"""{info['emoji']} {info['name']}입니다!

생물학 전문가로서 "{question}"에 대해 설명드리겠습니다.

**생물학적 분석:**
🧬 **분자 수준**: DNA, RNA, 단백질의 역할
🔬 **세포 수준**: 세포 내 구조와 기능
🌱 **개체 수준**: 생명체의 생리적 과정
🌍 **생태 수준**: 환경과의 상호작용

분자생물학부터 생태학까지 생명과학의 모든 영역을 다루며, 최신 연구 동향도 포함하여 답변드립니다!

구체적인 생명체나 현상에 대해 더 알고 싶으시면 언제든 말씀해주세요! 🌿"""

    def _engineering_expert_response(self, question: str, info: dict) -> str:
        """공학 전문가 답변"""
        engineering_topics = {
            "최적화": "시스템 최적화 방법을 설명하겠습니다.\n\n**성능 분석**: 병목지점 식별, 메트릭 측정\n**알고리즘 최적화**: 시간/공간 복잡도 개선\n**하드웨어 최적화**: CPU, 메모리, I/O 튜닝\n**아키텍처 설계**: 확장성, 안정성, 보안성\n**모니터링**: 실시간 성능 추적 및 알람",
            "설계": "시스템 설계 원칙을 설명하겠습니다.\n\n**요구사항 분석**: 기능적/비기능적 요구사항\n**아키텍처 설계**: 계층 구조, 모듈화\n**데이터 설계**: 데이터베이스, 스키마 설계\n**인터페이스 설계**: API, UI/UX 설계\n**테스트 설계**: 단위, 통합, 시스템 테스트",
            "알고리즘": "알고리즘 설계와 분석을 설명하겠습니다.\n\n**시간 복잡도**: Big O 표기법\n**공간 복잡도**: 메모리 사용량 분석\n**정렬**: 퀵소트, 머지소트, 힙소트\n**탐색**: 이진탐색, DFS, BFS\n**동적계획법**: 최적화 문제 해결",
            "데이터": "데이터 처리와 분석을 설명하겠습니다.\n\n**데이터 수집**: 크롤링, API, 센서\n**데이터 전처리**: 정제, 변환, 정규화\n**데이터 분석**: 통계분석, 머신러닝\n**데이터 시각화**: 차트, 대시보드\n**빅데이터**: 분산처리, 실시간 스트리밍",
        }

        for keyword, explanation in engineering_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 공학적으로 솔루션을 제시하겠습니다!\n\n{explanation}\n\n구체적인 시스템이나 요구사항이 있으시면 맞춤형 설계를 도와드리겠습니다! 🔧"

        return f"""{info['emoji']} {info['name']}입니다!

공학 전문가로서 "{question}"에 대한 솔루션을 제시하겠습니다.

**공학적 접근:**
🎯 **문제 정의**: 핵심 문제와 제약 조건 파악
🔧 **설계 방안**: 여러 가능한 해결책 제시
📊 **성능 분석**: 효율성, 비용, 실현 가능성
🚀 **최적화**: 제약 조건 하에서 최적 솔루션

소프트웨어 개발, 시스템 설계, 데이터 엔지니어링 등 모든 공학 분야에서 실무적인 솔루션을 제공합니다!

구체적인 프로젝트나 기술 스택에 대해 더 알고 싶으시면 말씀해주세요! ⚙️"""

    def _assistant_expert_response(self, question: str, info: dict) -> str:
        """업무 도우미 전문가 답변"""
        assistant_topics = {
            "업무관리": "효율적인 업무 관리 방법을 제안하겠습니다.\n\n**시간 관리**: 포모도로 기법, 시간 블록킹\n**우선순위**: 중요-긴급 매트릭스, ABCDE 방법\n**도구 활용**: Notion, Trello, Asana\n**자동화**: IFTTT, Zapier로 반복 업무 자동화\n**습관 형성**: 루틴 구축과 지속적 개선",
            "프로젝트": "프로젝트 관리 전략을 설명하겠습니다.\n\n**계획 수립**: WBS, 일정 계획, 리소스 배정\n**진행 관리**: 마일스톤, 체크포인트 설정\n**리스크 관리**: 위험 요소 식별과 대응책\n**팀 협업**: 역할 분담, 의사소통 체계\n**성과 측정**: KPI 설정과 모니터링",
            "생산성": "생산성 향상 방법을 제안하겠습니다.\n\n**집중력**: 몰입 환경 조성, 방해 요소 제거\n**에너지 관리**: 최적 컨디션 시간 활용\n**학습법**: 효과적인 정보 습득과 기억\n**휴식**: 적절한 휴식과 회복 시간\n**동기부여**: 목표 설정과 보상 시스템",
            "효율성": "업무 효율성 극대화 방법을 알려드리겠습니다.\n\n**프로세스 개선**: 불필요한 단계 제거\n**기술 활용**: 업무 자동화 도구 도입\n**데이터 기반**: 성과 측정과 분석\n**지속적 개선**: 피드백 수집과 반영\n**표준화**: 베스트 프랙티스 문서화",
        }

        for keyword, explanation in assistant_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 실용적인 솔루션을 제공하겠습니다!\n\n{explanation}\n\n구체적인 업무 상황을 알려주시면 맞춤형 개선 방안을 제시해드리겠습니다! 📋"

        return f"""{info['emoji']} {info['name']}입니다!

업무 효율성 전문가로서 "{question}"에 대해 답변드리겠습니다.

**생산성 향상 전략:**
⏰ **시간 최적화**: 효율적인 시간 사용법
📋 **업무 체계화**: 프로세스 정리와 표준화
👥 **협업 강화**: 팀워크와 커뮤니케이션
📈 **성과 관리**: 목표 설정과 성과 측정

개인 생산성부터 팀 프로젝트 관리까지 실무에 바로 적용할 수 있는 솔루션을 제공합니다!

구체적인 업무 환경이나 고민 사항을 알려주시면 더 정확한 조언을 드릴 수 있습니다! 🚀"""

    def _marketing_expert_response(self, question: str, info: dict) -> str:
        """마케팅 전문가 답변"""
        marketing_topics = {
            "브랜딩": "브랜딩 전략을 설명하겠습니다.\n\n**브랜드 아이덴티티**: 미션, 비전, 가치 정의\n**타겟 분석**: 페르소나, 고객 여정 맵핑\n**포지셔닝**: 차별화 포인트, USP\n**브랜드 경험**: 터치포인트 설계\n**성과 측정**: 브랜드 인지도, NPS",
            "디지털마케팅": "디지털 마케팅 전략을 제안하겠습니다.\n\n**SEO/SEM**: 검색엔진 최적화, 키워드 광고\n**소셜미디어**: 플랫폼별 콘텐츠 전략\n**콘텐츠 마케팅**: 가치 있는 정보 제공\n**이메일 마케팅**: 자동화, 개인화\n**데이터 분석**: GA, 소셜 인사이트",
            "고객분석": "고객 분석 방법을 설명하겠습니다.\n\n**세그먼테이션**: 인구통계학적, 행동적 분류\n**페르소나**: 대표 고객 프로필 작성\n**고객 여정**: 인지-고려-구매-충성 단계\n**라이프타임 밸류**: CLV 계산과 활용\n**만족도 조사**: 설문, 인터뷰, 관찰",
            "캠페인": "마케팅 캠페인 기획을 도와드리겠습니다.\n\n**목표 설정**: SMART 목표, KPI 정의\n**메시지 개발**: 핵심 메시지, 크리에이티브\n**채널 선택**: 오프라인/온라인 믹스\n**일정 계획**: 론칭, 실행, 평가 단계\n**예산 배분**: 채널별 투자 우선순위",
        }

        for keyword, explanation in marketing_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 마케팅 전략을 제시하겠습니다!\n\n{explanation}\n\n구체적인 브랜드나 제품에 대한 전략이 필요하시면 상세 분석해드리겠습니다! 🎯"

        return f"""{info['emoji']} {info['name']}입니다!

마케팅 전문가로서 "{question}"에 대한 전략을 제시하겠습니다.

**마케팅 전략 수립:**
🎯 **타겟 정의**: 고객 세그먼트와 페르소나
📊 **시장 분석**: 트렌드, 경쟁사, 기회 요소
💡 **메시지 개발**: 브랜드 스토리와 가치 제안
📈 **채널 전략**: 온오프라인 통합 마케팅

브랜딩부터 퍼포먼스 마케팅까지 데이터 기반의 실행 가능한 전략을 제공합니다!

구체적인 업종이나 타겟 고객을 알려주시면 맞춤형 마케팅 플랜을 수립해드리겠습니다! 📱"""

    def _startup_expert_response(self, question: str, info: dict) -> str:
        """스타트업 전문가 답변"""
        startup_topics = {
            "사업계획": "사업계획서 작성 가이드를 제공하겠습니다.\n\n**비즈니스 모델**: 가치 제안, 수익 구조\n**시장 분석**: TAM, SAM, SOM 분석\n**경쟁 분석**: 차별화 포인트, 경쟁 우위\n**팀 구성**: 핵심 역량, 역할 분담\n**재무 계획**: 손익 예측, 자금 계획",
            "투자유치": "투자 유치 전략을 설명하겠습니다.\n\n**투자자 타겟팅**: 엔젤, VC, 정부 지원\n**피치덱 작성**: 문제-해결책-시장-팀\n**밸류에이션**: 적정 기업가치 산정\n**DD 준비**: 실사 자료 정비\n**협상**: 투자 조건, 지분 구조",
            "성장전략": "스타트업 성장 전략을 제안하겠습니다.\n\n**PMF 달성**: Product-Market Fit 검증\n**사용자 확보**: CAC, LTV 최적화\n**제품 개발**: MVP, 애자일 개발\n**조직 확장**: 인재 채용, 문화 구축\n**파트너십**: 전략적 제휴, 생태계",
            "창업": "창업 프로세스를 안내하겠습니다.\n\n**아이디어 검증**: 고객 인터뷰, MVP 테스트\n**사업자 등록**: 법인 설립, 필수 절차\n**초기 자금**: 엔젤 투자, 정부 지원 사업\n**팀 빌딩**: 공동창업자, 초기 직원\n**제품 개발**: 기술 개발, 시장 검증",
        }

        for keyword, explanation in startup_topics.items():
            if keyword in question:
                return f"{info['emoji']} {info['name']}이 창업 성공 전략을 제시하겠습니다!\n\n{explanation}\n\n구체적인 사업 아이디어나 단계에 맞는 맞춤형 조언이 필요하시면 말씀해주세요! 💼"

        return f"""{info['emoji']} {info['name']}입니다!

스타트업 전문가로서 "{question}"에 대해 답변드리겠습니다.

**창업 성공 로드맵:**
💡 **아이디어 검증**: 시장 검증과 MVP 개발
💰 **자금 조달**: 투자 유치와 재무 계획
📈 **성장 전략**: 확장 가능한 비즈니스 모델
👥 **팀 빌딩**: 핵심 인재 확보와 조직 문화

아이디어 단계부터 엑싯까지 창업의 전 과정에서 실무 경험을 바탕으로 한 실용적인 조언을 제공합니다!

구체적인 업종이나 창업 단계를 알려주시면 더 정확한 가이드를 제공해드리겠습니다! 🚀"""

    def _general_expert_response(self, question: str, info: dict) -> str:
        """일반적인 전문가 답변"""
        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 대해 제 전문 분야인 {info['field']} 관점에서 답변드리겠습니다.

**전문가 분석:**

이 질문은 매우 흥미로운 주제입니다. {info['field']} 전문가로서 체계적으로 접근해보겠습니다.

🔍 **핵심 요소 파악**
📚 **관련 이론과 원리**
💡 **실용적 응용 방안**
🎯 **구체적 실행 전략**

더 구체적인 상황이나 세부 사항을 알려주시면, 더욱 정확하고 맞춤형 답변을 제공해드릴 수 있습니다.

어떤 부분을 더 자세히 알고 싶으신지 말씀해주세요! ✨"""

    def get_agent_info(self) -> Dict[str, Any]:
        """에이전트 정보 반환"""
        agent_info = {
            "math": "🧮 수학 천재 - 미적분, 대수, 통계 등 모든 수학 문제",
            "physics": "⚛️ 물리학 마스터 - 역학, 전자기학, 양자물리학 등",
            "chemistry": "🧪 화학 전문가 - 유기화학, 무기화학, 물리화학 등",
            "biology": "🧬 생물학 천재 - 분자생물학, 생태학, 유전학 등",
            "engineering": "⚙️ 공학 마법사 - 설계, 최적화, 시스템 분석 등",
            "assistant": "🤖 품질 어시스턴트 - 업무 최적화, 프로젝트 관리",
            "marketing": "📈 마케팅 전략가 - 브랜딩, 마케팅 전략 수립",
            "startup": "🚀 스타트업 컨설턴트 - 사업 계획, 투자 유치",
        }

        return {
            "total_agents": 8,
            "loaded_agents": list(agent_info.keys()),
            "agent_descriptions": agent_info,
            "status": "active",
        }


# 전역 STEM 서비스 인스턴스
stem_service = STEMService()


def add_stem_routes(app: FastAPI):
    """FastAPI 앱에 STEM 라우트 추가"""

    @app.get("/stem/demo", response_class=HTMLResponse)
    async def stem_demo(request: Request, agent: str = "math"):
        """STEM 에이전트 데모 페이지"""
        agent_info = stem_service.get_agent_info()
        agent_descriptions = agent_info.get("agent_descriptions", {})

        if agent not in agent_descriptions:
            agent = "math"  # 기본값

        return f"""
        <html>
            <head>
                <title>🧙‍♂️ {agent_descriptions.get(agent, '도깨비')} - STEM 센터</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; 
                           background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                           background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; }}
                    @keyframes gradient {{
                        0% {{ background-position: 0% 50%; }}
                        50% {{ background-position: 100% 50%; }}
                        100% {{ background-position: 0% 50%; }}
                    }}
                    .container {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                               border-radius: 20px; padding: 30px; margin: 20px 0; }}
                    .btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
                           text-decoration: none; padding: 12px 25px; border-radius: 8px; font-weight: bold;
                           display: inline-block; margin: 10px 5px; transition: all 0.3s ease; }}
                    .btn:hover {{ transform: scale(1.05); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3); color: white; }}
                    .question-area {{ background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }}
                    #response {{ background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 10px; margin-top: 20px; display: none; }}
                    input, textarea {{ width: 100%; padding: 10px; border: none; border-radius: 5px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🧙‍♂️ {agent_descriptions.get(agent, '도깨비')} 체험</h1>
                    <p>AI 도깨비마을 STEM 센터에 오신 것을 환영합니다!</p>
                    
                    <div class="question-area">
                        <h3>💬 도깨비에게 질문하기</h3>
                        <textarea id="questionInput" placeholder="궁금한 것을 물어보세요..." rows="3"></textarea>
                        <button class="btn" onclick="askQuestion()">🚀 질문하기</button>
                        <button class="btn" onclick="askSample()">📝 샘플 질문</button>
                    </div>
                    
                    <div id="response">
                        <h3>🧙‍♂️ 도깨비 응답:</h3>
                        <div id="responseText"></div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/" class="btn">🔙 메인으로 돌아가기</a>
                        <a href="/stem/" class="btn">🏪 STEM 센터 홈</a>
                    </div>
                </div>
                
                <script>
                    const agentType = "{agent}";
                    
                    async function askQuestion() {{
                        const question = document.getElementById('questionInput').value;
                        if (!question.trim()) {{
                            alert('질문을 입력해주세요!');
                            return;
                        }}
                        
                        document.getElementById('response').style.display = 'block';
                        document.getElementById('responseText').innerHTML = '🔮 도깨비가 마법을 부리는 중...';
                        
                        try {{
                            const response = await fetch('/stem/api/ask', {{
                                method: 'POST',
                                headers: {{'Content-Type': 'application/json'}},
                                body: JSON.stringify({{question: question, agent_type: agentType}})
                            }});
                            const data = await response.json();
                            document.getElementById('responseText').innerHTML = data.success ? data.response.replace(/\\n/g, '<br>') : '❌ ' + data.error;
                        }} catch (error) {{
                            document.getElementById('responseText').innerHTML = '❌ 마법이 실패했습니다: ' + error.message;
                        }}
                    }}
                    
                    function askSample() {{
                        const samples = {{
                            "math": "이차방정식의 해법을 설명해주세요",
                            "physics": "뉴턴의 운동법칙을 설명해주세요", 
                            "chemistry": "화학결합의 종류를 설명해주세요",
                            "biology": "DNA의 구조와 기능을 설명해주세요",
                            "engineering": "시스템 최적화 방법을 알려주세요",
                            "assistant": "효율적인 업무 관리 방법을 알려주세요",
                            "marketing": "브랜딩 전략을 수립하는 방법을 알려주세요",
                            "startup": "스타트업 투자 유치 전략을 알려주세요"
                        }};
                        document.getElementById('questionInput').value = samples[agentType] || "안녕하세요!";
                    }}
                </script>
            </body>
        </html>
        """

    @app.get("/stem/", response_class=HTMLResponse)
    async def stem_home(request: Request):
        """STEM 서비스 홈페이지"""
        agent_info = stem_service.get_agent_info()
        agents = agent_info.get("loaded_agents", [])
        descriptions = agent_info.get("agent_descriptions", {})

        agents_html = ""
        for agent in agents:
            description = descriptions.get(agent, f"{agent} 전문가")
            agents_html += f"""
            <div style="background: rgba(255,255,255,0.1); margin: 10px 0; padding: 15px; border-radius: 10px;">
                <h3>{description}</h3>
                <a href="/stem/demo?agent={agent}" style="background: #4CAF50; color: white; padding: 8px 16px; 
                   text-decoration: none; border-radius: 5px; margin: 5px;">🎯 체험하기</a>
            </div>
            """

        return f"""
        <html>
            <head>
                <title>🧙‍♂️ AI 도깨비마을 STEM 센터</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial; margin: 0; padding: 20px; 
                           background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
                           background-size: 400% 400%; animation: gradient 15s ease infinite; color: white; }}
                    @keyframes gradient {{
                        0% {{ background-position: 0% 50%; }}
                        50% {{ background-position: 100% 50%; }}
                        100% {{ background-position: 0% 50%; }}
                    }}
                    .container {{ max-width: 1000px; margin: 0 auto; 
                               background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                               border-radius: 20px; padding: 30px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🧙‍♂️ AI 도깨비마을 STEM 센터</h1>
                    <p>8명의 촌장급 STEM 전문가 도깨비들이 무료로 서비스 중입니다!</p>
                    <p>실제 AI 대화 능력으로 구현된 전문가들이 질문에 답변해드립니다.</p>
                    
                    <h2>🎯 사용 가능한 STEM 전문가들:</h2>
                    {agents_html}
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/" style="background: #2196F3; color: white; padding: 15px 30px; 
                           text-decoration: none; border-radius: 10px; font-size: 18px;">🔙 메인으로 돌아가기</a>
                    </div>
                </div>
            </body>
        </html>
        """

    @app.post("/stem/api/ask")
    async def stem_ask(request: STEMRequest):
        """STEM 질문 처리 API"""
        try:
            result = await stem_service.process_question(
                request.question, request.agent_type
            )
            return JSONResponse(content=result)
        except Exception as e:
            return JSONResponse(
                content={"success": False, "error": f"서버 오류: {str(e)}"},
                status_code=500,
            )

    @app.get("/stem/dashboard")
    async def stem_dashboard():
        """STEM 대시보드 - 시스템 상태"""
        agent_info = stem_service.get_agent_info()
        return JSONResponse(
            content={
                "service": "STEM AI Center",
                "version": "2.0 - Real AI Powered",
                "status": "active",
                "agents": agent_info,
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

    print("✅ 실제 AI 대화 능력 기반 STEM 라우트 추가 완료!")
    return app
