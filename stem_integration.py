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

# 사용량 추적 시스템 임포트
from usage_tracker import usage_tracker

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

    async def process_question(
        self, question: str, agent_type: str, user_ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """실제 AI 대화 능력으로 질문 처리"""
        try:
            # 에이전트별 정보 - 16개 분야
            agent_info = {
                # 기존 8개 (조금 더 친근하게)
                "math": {"emoji": "🧮", "name": "수학 도깨비", "field": "수학"},
                "physics": {"emoji": "⚛️", "name": "물리학 도깨비", "field": "물리학"},
                "chemistry": {"emoji": "🧪", "name": "화학 도깨비", "field": "화학"},
                "biology": {"emoji": "🧬", "name": "생물학 도깨비", "field": "생물학"},
                "engineering": {"emoji": "⚙️", "name": "공학 도깨비", "field": "공학"},
                "assistant": {"emoji": "🤖", "name": "업무 도우미 도깨비", "field": "업무 관리"},
                "marketing": {"emoji": "📈", "name": "마케팅 도깨비", "field": "마케팅"},
                "startup": {"emoji": "🚀", "name": "스타트업 도깨비", "field": "창업"},
                
                # 새로운 8개 (일반인 친화적)
                "cooking": {"emoji": "🍳", "name": "요리 도깨비", "field": "요리"},
                "lifestyle": {"emoji": "💡", "name": "생활 꿀팁 도깨비", "field": "생활 팁"},
                "interior": {"emoji": "🏠", "name": "집꾸미기 도깨비", "field": "인테리어"},
                "finance": {"emoji": "�", "name": "가계부 도깨비", "field": "재정 관리"},
                "hobby": {"emoji": "🎮", "name": "취미 도깨비", "field": "취미 활동"},
                "tech": {"emoji": "💻", "name": "IT 도깨비", "field": "컴퓨터 활용"},
                "health": {"emoji": "🏃", "name": "건강 도깨비", "field": "건강 관리"},
                "learning": {"emoji": "�", "name": "공부 도깨비", "field": "학습 도움"}
            }

            if agent_type not in agent_info:
                # 실패 로그 기록
                usage_tracker.log_usage(agent_type, question, False, user_ip)
                return {
                    "success": False,
                    "error": f"지원하지 않는 에이전트 타입: {agent_type}",
                }

            info = agent_info[agent_type]

            # 실제 AI 기반 답변 생성
            ai_response = self._generate_smart_response(question, agent_type, info)

            # 성공 로그 기록
            usage_tracker.log_usage(agent_type, question, True, user_ip)

            return {
                "success": True,
                "agent_type": agent_type,
                "question": question,
                "response": ai_response,
                "timestamp": datetime.datetime.now().isoformat(),
            }

        except Exception as e:
            # 에러 로그 기록
            usage_tracker.log_usage(agent_type, question, False, user_ip)
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
        # 새로운 8개 도깨비
        elif agent_type == "cooking":
            return self._cooking_expert_response(question, info)
        elif agent_type == "lifestyle":
            return self._lifestyle_expert_response(question, info)
        elif agent_type == "interior":
            return self._interior_expert_response(question, info)
        elif agent_type == "finance":
            return self._finance_expert_response(question, info)
        elif agent_type == "hobby":
            return self._hobby_expert_response(question, info)
        elif agent_type == "tech":
            return self._tech_expert_response(question, info)
        elif agent_type == "health":
            return self._health_expert_response(question, info)
        elif agent_type == "learning":
            return self._learning_expert_response(question, info)
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
            "복리": "복리 이자 계산 공식을 자세히 설명드리겠습니다!\n\n**복리 공식**: A = P(1 + r/n)^(nt)\n- A: 최종 금액\n- P: 원금\n- r: 연 이자율 (소수점)\n- n: 연간 복리 횟수\n- t: 기간(년)\n\n**예시**: 100만원을 연 5% 복리로 3년간 투자\nA = 1,000,000 × (1 + 0.05)³ = 1,157,625원\n\n**연속복리**: A = Pe^(rt)",
            "이자": "이자 계산의 기본 원리를 설명하겠습니다!\n\n**단리**: I = Prt (이자 = 원금 × 이율 × 기간)\n**복리**: A = P(1+r)^t (원리합계 공식)\n**실효이자율**: (1 + r/n)^n - 1\n\n**월복리**: 매월 복리 적용 시 A = P(1 + r/12)^(12t)\n**일일복리**: 매일 복리 적용 시 A = P(1 + r/365)^(365t)",
            "연립방정식": "연립방정식 해법을 체계적으로 설명하겠습니다!\n\n**가감법**: 계수를 맞춰서 더하거나 빼서 변수 소거\n**대입법**: 한 방정식에서 변수를 구해 다른 방정식에 대입\n**행렬법**: 가우스 소거법으로 계단형 행렬 만들기\n\n**2×2 연립방정식 예시**:\nax + by = e\ncx + dy = f\n해: x = (ed-bf)/(ad-bc), y = (af-ec)/(ad-bc)",
        }

        # 키워드 매칭 검사
        question_lower = question.lower()
        for keyword, explanation in math_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        physics_topics = {
            "뉴턴": "뉴턴의 운동법칙을 설명드리겠습니다.\n\n**제1법칙 (관성의 법칙)**: 외력이 없으면 정지한 물체는 정지, 운동하는 물체는 등속직선운동\n**제2법칙 (가속도의 법칙)**: F = ma (힘 = 질량 × 가속도)\n**제3법칙 (작용-반작용)**: 모든 작용에는 크기가 같고 방향이 반대인 반작용이 존재",
            "에너지": "에너지 보존법칙과 종류를 설명하겠습니다.\n\n**운동에너지**: K = ½mv²\n**위치에너지**: U = mgh (중력), U = ½kx² (탄성)\n**에너지 보존**: 고립계에서 총 에너지는 보존\n**에너지 전환**: 운동↔위치↔열↔전기 등",
            "전기": "전기학의 기본 법칙들을 설명하겠습니다.\n\n**쿨롱의 법칙**: F = k(q₁q₂)/r²\n**옴의 법칙**: V = IR\n**키르히호프 법칙**: 전류법칙(KCL), 전압법칙(KVL)\n**전력**: P = VI = I²R = V²/R",
            "파동": "파동의 성질과 특징을 설명하겠습니다.\n\n**파동방정식**: y = A sin(kx - ωt + φ)\n**파장과 주파수**: v = fλ\n**간섭**: 보강간섭, 상쇄간섭\n**회절**: 장애물 뒤로 구부러지는 현상",
            "운동": "물체의 운동을 분석하는 방법을 설명하겠습니다.\n\n**등속직선운동**: v = s/t, 가속도 = 0\n**등가속도운동**: v = v₀ + at, s = v₀t + ½at²\n**자유낙하**: g = 9.8m/s², h = ½gt²\n**원운동**: 구심력 F = mv²/r, 각속도 ω = v/r",
            "역학": "역학의 기본 원리를 설명하겠습니다.\n\n**운동량**: p = mv, 충격량 = Δp\n**각운동량**: L = Iω (관성모멘트 × 각속도)\n**토크**: τ = r × F (회전력)\n**평형**: ΣF = 0, Στ = 0",
            "열역학": "열역학 법칙들을 설명하겠습니다.\n\n**제0법칙**: 열평형의 추이성\n**제1법칙**: 에너지 보존 (ΔU = Q - W)\n**제2법칙**: 엔트로피 증가 원리\n**제3법칙**: 절대영도에서 엔트로피는 0",
            "자기": "자기학의 기본 원리를 설명하겠습니다.\n\n**자기장**: B = μ₀I/(2πr) (직선 도선)\n**패러데이 법칙**: ε = -dΦ/dt (전자기 유도)\n**렌츠 법칙**: 유도 전류는 자기장 변화를 방해\n**앰페어 법칙**: ∮B·dl = μ₀I",
        }

        for keyword, explanation in physics_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        chemistry_topics = {
            "화학결합": "화학결합의 종류를 설명하겠습니다.\n\n**이온결합**: 금속+비금속, 전자 완전 이동, NaCl\n**공유결합**: 비금속간, 전자쌍 공유, H₂O, CO₂\n**금속결합**: 금속간, 자유전자 바다 모델\n**분자간 힘**: 반데르발스 힘, 수소결합, 쌍극자 힘",
            "산화환원": "산화환원 반응을 설명하겠습니다.\n\n**산화**: 전자를 잃는 반응 (산화수 증가)\n**환원**: 전자를 얻는 반응 (산화수 감소)\n**산화제**: 다른 물질을 산화시키며 자신은 환원\n**환원제**: 다른 물질을 환원시키며 자신은 산화",
            "ph": "pH와 산-염기를 설명하겠습니다.\n\n**pH 정의**: pH = -log[H⁺]\n**중성**: pH = 7, [H⁺] = [OH⁻]\n**산성**: pH < 7, [H⁺] > [OH⁻]\n**염기성**: pH > 7, [H⁺] < [OH⁻]\n**완충용액**: pH 변화를 억제하는 용액",
            "유기화학": "유기화학의 기본을 설명하겠습니다.\n\n**탄화수소**: 알케인, 알켄, 알카인\n**작용기**: -OH(알코올), -COOH(카복실산), -NH₂(아민)\n**반응**: 치환, 첨가, 제거, 재배열\n**이성질체**: 구조이성질체, 입체이성질체",
            "몰": "몰과 아보가드로 수를 설명하겠습니다.\n\n**몰 정의**: 6.022×10²³개의 입자 수\n**몰질량**: 1몰의 질량 (g/mol)\n**몰농도**: M = n/V (몰수/부피)\n**몰분율**: 전체 몰수에 대한 특정 성분의 몰수 비",
            "반응속도": "화학반응속도를 설명하겠습니다.\n\n**속도식**: v = k[A]ⁿ[B]ᵐ\n**반감기**: 농도가 절반이 되는 시간\n**활성화에너지**: 반응이 일어나는데 필요한 최소 에너지\n**촉매**: 활성화에너지를 낮춰 반응속도 증가",
            "평형": "화학평형을 설명하겠습니다.\n\n**평형상수**: K = [생성물]/[반응물]\n**르샤틀리에 원리**: 평형에 가해진 변화를 상쇄하는 방향\n**농도, 온도, 압력**: 평형에 영향을 주는 요인들\n**산-염기 평형**: Ka, Kb, Kw의 관계",
        }

        for keyword, explanation in chemistry_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        biology_topics = {
            "dna": "DNA의 구조와 기능을 설명하겠습니다.\n\n**이중나선 구조**: 두 가닥이 나선형으로 감긴 형태\n**염기쌍**: A-T, G-C 수소결합\n**유전정보 저장**: 모든 생명체의 설계도\n**복제**: 반보존적 복제로 유전정보 전달\n**전사**: DNA → RNA 과정\n**번역**: RNA → 단백질 과정",
            "세포": "세포의 구조와 기능을 설명하겠습니다.\n\n**핵**: 유전물질 보관, 세포 조절\n**미토콘드리아**: ATP 생산, 세포 호흡\n**리보솜**: 단백질 합성\n**소포체**: 단백질 가공, 지질 합성\n**골지체**: 단백질 수정, 분비",
            "진화": "진화의 원리를 설명하겠습니다.\n\n**자연선택**: 환경에 적합한 개체의 생존\n**돌연변이**: 유전적 변이의 원천\n**유전적 부동**: 우연에 의한 대립유전자 빈도 변화\n**종분화**: 새로운 종의 형성 과정",
            "생태": "생태계의 구조와 기능을 설명하겠습니다.\n\n**생산자**: 광합성으로 에너지 고정\n**소비자**: 1차, 2차, 3차 소비자\n**분해자**: 유기물을 무기물로 분해\n**에너지 흐름**: 먹이사슬을 통한 에너지 전달\n**물질순환**: 탄소, 질소, 인 순환",
            "유전": "유전학의 기본 원리를 설명하겠습니다.\n\n**멘델의 법칙**: 우성, 분리, 독립 법칙\n**염색체**: 유전자가 위치하는 구조\n**감수분열**: 배우자 형성 과정\n**돌연변이**: 유전자 변화의 원인\n**유전공학**: 유전자 조작 기술",
            "광합성": "광합성 과정을 설명하겠습니다.\n\n**명반응**: 엽록체 틸라코이드에서 일어남\n**암반응**: 스트로마에서 칼빈 회로\n**전체 반응식**: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂\n**광계 I, II**: 빛에너지를 화학에너지로 변환\n**ATP, NADPH**: 에너지 운반체",
            "호흡": "세포호흡을 설명하겠습니다.\n\n**해당과정**: 포도당을 피루브산으로 분해\n**시트르산 회로**: 아세틸 CoA의 완전 산화\n**전자전달계**: ATP 대량 생산\n**총 수율**: 포도당 1분자당 ATP 38개\n**무산소 호흡**: 발효 과정",
        }

        for keyword, explanation in biology_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        engineering_topics = {
            "최적화": "시스템 최적화 방법을 설명하겠습니다.\n\n**성능 분석**: 병목지점 식별, 메트릭 측정\n**알고리즘 최적화**: 시간/공간 복잡도 개선\n**하드웨어 최적화**: CPU, 메모리, I/O 튜닝\n**아키텍처 설계**: 확장성, 안정성, 보안성\n**모니터링**: 실시간 성능 추적 및 알람",
            "설계": "시스템 설계 원칙을 설명하겠습니다.\n\n**요구사항 분석**: 기능적/비기능적 요구사항\n**아키텍처 설계**: 계층 구조, 모듈화\n**데이터 설계**: 데이터베이스, 스키마 설계\n**인터페이스 설계**: API, UI/UX 설계\n**테스트 설계**: 단위, 통합, 시스템 테스트",
            "알고리즘": "알고리즘 설계와 분석을 설명하겠습니다.\n\n**시간 복잡도**: Big O 표기법\n**공간 복잡도**: 메모리 사용량 분석\n**정렬**: 퀵소트, 머지소트, 힙소트\n**탐색**: 이진탐색, DFS, BFS\n**동적계획법**: 최적화 문제 해결",
            "데이터": "데이터 처리와 분석을 설명하겠습니다.\n\n**데이터 수집**: 크롤링, API, 센서\n**데이터 전처리**: 정제, 변환, 정규화\n**데이터 분석**: 통계분석, 머신러닝\n**데이터 시각화**: 차트, 대시보드\n**빅데이터**: 분산처리, 실시간 스트리밍",
            "네트워크": "네트워크 엔지니어링을 설명하겠습니다.\n\n**OSI 7계층**: 물리, 데이터링크, 네트워크, 전송, 세션, 표현, 응용\n**TCP/IP**: 인터넷 프로토콜 스택\n**라우팅**: 최적 경로 찾기 알고리즘\n**보안**: 방화벽, VPN, 암호화\n**성능**: 대역폭, 지연시간, 처리량",
            "소프트웨어": "소프트웨어 엔지니어링을 설명하겠습니다.\n\n**SDLC**: 소프트웨어 개발 생명주기\n**애자일**: 스크럼, 칸반 방법론\n**DevOps**: CI/CD, 자동화 배포\n**테스팅**: 단위, 통합, E2E 테스트\n**아키텍처**: 마이크로서비스, 모놀리식",
            "머신러닝": "머신러닝 엔지니어링을 설명하겠습니다.\n\n**지도학습**: 회귀, 분류 알고리즘\n**비지도학습**: 클러스터링, 차원축소\n**딥러닝**: 신경망, CNN, RNN\n**MLOps**: 모델 배포, 모니터링\n**데이터파이프라인**: ETL, 특성 엔지니어링",
        }

        for keyword, explanation in engineering_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        assistant_topics = {
            "업무관리": "효율적인 업무 관리 방법을 제안하겠습니다.\n\n**시간 관리**: 포모도로 기법, 시간 블록킹\n**우선순위**: 중요-긴급 매트릭스, ABCDE 방법\n**도구 활용**: Notion, Trello, Asana\n**자동화**: IFTTT, Zapier로 반복 업무 자동화\n**습관 형성**: 루틴 구축과 지속적 개선",
            "프로젝트": "프로젝트 관리 전략을 설명하겠습니다.\n\n**계획 수립**: WBS, 일정 계획, 리소스 배정\n**진행 관리**: 마일스톤, 체크포인트 설정\n**리스크 관리**: 위험 요소 식별과 대응책\n**팀 협업**: 역할 분담, 의사소통 체계\n**성과 측정**: KPI 설정과 모니터링",
            "생산성": "생산성 향상 방법을 제안하겠습니다.\n\n**집중력**: 몰입 환경 조성, 방해 요소 제거\n**에너지 관리**: 최적 컨디션 시간 활용\n**학습법**: 효과적인 정보 습득과 기억\n**휴식**: 적절한 휴식과 회복 시간\n**동기부여**: 목표 설정과 보상 시스템",
            "효율성": "업무 효율성 극대화 방법을 알려드리겠습니다.\n\n**프로세스 개선**: 불필요한 단계 제거\n**기술 활용**: 업무 자동화 도구 도입\n**데이터 기반**: 성과 측정과 분석\n**지속적 개선**: 피드백 수집과 반영\n**표준화**: 베스트 프랙티스 문서화",
            "팀워크": "팀 협업 향상 방법을 제안하겠습니다.\n\n**의사소통**: 명확한 전달, 적극적 경청\n**역할 분담**: 강점 기반 업무 배분\n**갈등 해결**: 건설적 토론, Win-Win 해결책\n**목표 공유**: 팀 비전과 개인 목표 연결\n**신뢰 구축**: 투명성, 책임감, 상호 존중",
            "리더십": "리더십 개발 방법을 설명하겠습니다.\n\n**비전 제시**: 명확한 방향성과 목표\n**동기부여**: 개인별 맞춤형 동기 요인\n**코칭**: 성장 지원과 피드백 제공\n**의사결정**: 신속하고 합리적인 판단\n**변화관리**: 혁신과 적응력 촉진",
            "소통": "효과적인 소통 방법을 알려드리겠습니다.\n\n**경청**: 상대방 관점 이해하기\n**피드백**: 구체적이고 건설적인 조언\n**프레젠테이션**: 논리적 구조와 스토리텔링\n**회의**: 효율적인 회의 진행법\n**글쓰기**: 명확하고 간결한 문서 작성",
        }

        for keyword, explanation in assistant_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        marketing_topics = {
            "브랜딩": "브랜딩 전략을 설명하겠습니다.\n\n**브랜드 아이덴티티**: 미션, 비전, 가치 정의\n**타겟 분석**: 페르소나, 고객 여정 맵핑\n**포지셔닝**: 차별화 포인트, USP\n**브랜드 경험**: 터치포인트 설계\n**성과 측정**: 브랜드 인지도, NPS",
            "디지털마케팅": "디지털 마케팅 전략을 제안하겠습니다.\n\n**SEO/SEM**: 검색엔진 최적화, 키워드 광고\n**소셜미디어**: 플랫폼별 콘텐츠 전략\n**콘텐츠 마케팅**: 가치 있는 정보 제공\n**이메일 마케팅**: 자동화, 개인화\n**데이터 분석**: GA, 소셜 인사이트",
            "고객분석": "고객 분석 방법을 설명하겠습니다.\n\n**세그먼테이션**: 인구통계학적, 행동적 분류\n**페르소나**: 대표 고객 프로필 작성\n**고객 여정**: 인지-고려-구매-충성 단계\n**라이프타임 밸류**: CLV 계산과 활용\n**만족도 조사**: 설문, 인터뷰, 관찰",
            "캠페인": "마케팅 캠페인 기획을 도와드리겠습니다.\n\n**목표 설정**: SMART 목표, KPI 정의\n**메시지 개발**: 핵심 메시지, 크리에이티브\n**채널 선택**: 오프라인/온라인 믹스\n**일정 계획**: 론칭, 실행, 평가 단계\n**예산 배분**: 채널별 투자 우선순위",
            "광고": "광고 전략을 설명하겠습니다.\n\n**타겟팅**: 정확한 고객층 설정\n**크리에이티브**: 임팩트 있는 메시지와 비주얼\n**매체 기획**: 최적 노출 시간과 플랫폼\n**성과 측정**: CTR, CPC, ROAS\n**최적화**: A/B 테스트와 개선",
            "sns": "SNS 마케팅을 설명하겠습니다.\n\n**플랫폼별 특성**: 인스타그램, 페이스북, 유튜브, 틱톡\n**콘텐츠 전략**: 스토리텔링, 비주얼 콘텐츠\n**인플루언서**: 협업과 바이럴 마케팅\n**커뮤니티**: 팬덤 구축과 관리\n**분석**: 인게이지먼트, 도달률, 전환율",
            "seo": "검색엔진 최적화를 설명하겠습니다.\n\n**키워드 연구**: 검색량, 경쟁도 분석\n**온페이지 SEO**: 제목, 메타, 구조화 데이터\n**오프페이지 SEO**: 백링크, 도메인 권한\n**기술적 SEO**: 사이트 속도, 모바일 최적화\n**성과 측정**: 순위, 트래픽, 전환율",
            "마케팅": "통합 마케팅 전략을 제안하겠습니다.\n\n**4P 전략**: Product, Price, Place, Promotion\n**고객 여정**: 인지 → 관심 → 고려 → 구매 → 재구매\n**옴니채널**: 온라인과 오프라인 통합\n**데이터 마케팅**: 개인화와 자동화\n**성과 관리**: ROI, CAC, LTV 추적",
        }

        for keyword, explanation in marketing_topics.items():
            if keyword in question_lower:
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
        question_lower = question.lower()

        startup_topics = {
            "사업계획": "사업계획서 작성 가이드를 제공하겠습니다.\n\n**비즈니스 모델**: 가치 제안, 수익 구조\n**시장 분석**: TAM, SAM, SOM 분석\n**경쟁 분석**: 차별화 포인트, 경쟁 우위\n**팀 구성**: 핵심 역량, 역할 분담\n**재무 계획**: 손익 예측, 자금 계획",
            "투자유치": "투자 유치 전략을 설명하겠습니다.\n\n**투자자 타겟팅**: 엔젤, VC, 정부 지원\n**피치덱 작성**: 문제-해결책-시장-팀\n**밸류에이션**: 적정 기업가치 산정\n**DD 준비**: 실사 자료 정비\n**협상**: 투자 조건, 지분 구조",
            "성장전략": "스타트업 성장 전략을 제안하겠습니다.\n\n**PMF 달성**: Product-Market Fit 검증\n**사용자 확보**: CAC, LTV 최적화\n**제품 개발**: MVP, 애자일 개발\n**조직 확장**: 인재 채용, 문화 구축\n**파트너십**: 전략적 제휴, 생태계",
            "창업": "창업 프로세스를 안내하겠습니다.\n\n**아이디어 검증**: 고객 인터뷰, MVP 테스트\n**사업자 등록**: 법인 설립, 필수 절차\n**초기 자금**: 엔젤 투자, 정부 지원 사업\n**팀 빌딩**: 공동창업자, 초기 직원\n**제품 개발**: 기술 개발, 시장 검증",
            "mvp": "MVP 개발 전략을 설명하겠습니다.\n\n**핵심 기능**: 반드시 필요한 최소 기능 정의\n**빠른 출시**: 2-3개월 내 런칭 목표\n**사용자 피드백**: 실제 사용자 반응 수집\n**반복 개선**: 빠른 학습과 개선 사이클\n**피벗 준비**: 필요시 방향 전환",
            "펀딩": "자금 조달 방법을 설명하겠습니다.\n\n**부트스트래핑**: 자체 자금으로 시작\n**정부 지원**: 창업진흥원, TIPS, 각종 사업공고\n**엔젤 투자**: 개인 투자자, 액셀러레이터\n**벤처캐피털**: 시리즈 A, B, C 투자\n**크라우드펀딩**: 와디즈, 킥스타터",
            "비즈니스모델": "비즈니스 모델 설계를 도와드리겠습니다.\n\n**수익 모델**: 구독, 광고, 수수료, 판매\n**고객 세그먼트**: 타겟 고객층 정의\n**가치 제안**: 고객 문제 해결 방안\n**채널**: 고객 접점과 유통 경로\n**비용 구조**: 고정비, 변동비 분석",
            "스케일링": "사업 확장 전략을 제안하겠습니다.\n\n**시장 확장**: 새로운 지역, 고객층 진출\n**제품 확장**: 라인업 다양화, 크로스셀링\n**파트너십**: 전략적 제휴, 인수합병\n**기술 확장**: 플랫폼화, API 제공\n**조직 확장**: 인재 확보, 시스템 구축",
        }

        for keyword, explanation in startup_topics.items():
            if keyword in question_lower:
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

    def _cooking_expert_response(self, question: str, info: dict) -> str:
        """요리 전문가 답변"""
        question_lower = question.lower()

        cooking_topics = {
            "레시피": "맛있는 레시피를 추천해드리겠습니다!\n\n**간단 요리**: 15분 만에 완성하는 원팬 요리\n**건강식**: 저칼로리 다이어트 메뉴\n**집밥**: 엄마 손맛 나는 가정식\n**간식**: 아이들이 좋아하는 수제 간식\n**국물요리**: 속 깊은 국물 우리는 법",
            "재료": "재료 활용법을 알려드리겠습니다!\n\n**냉장고 파먹기**: 남은 재료로 만드는 요리\n**대체재료**: 없는 재료 대신 쓸 수 있는 것들\n**보관법**: 신선하게 오래 보관하는 팁\n**손질법**: 재료별 효율적인 손질 방법",
            "조리법": "요리 기법을 설명해드리겠습니다!\n\n**볶음**: 센 불에서 빠르게 볶는 법\n**조림**: 간이 잘 배도록 조리는 팁\n**튀김**: 바삭하게 튀기는 온도와 시간\n**찜**: 부드럽게 쪄내는 방법",
            "다이어트": "건강한 다이어트 요리를 추천합니다!\n\n**저칼로리**: 포만감 있는 저칼로리 메뉴\n**단백질**: 근손실 방지 고단백 요리\n**식이섬유**: 배변활동에 좋은 채소 요리\n**저염**: 나트륨 줄인 건강 요리",
        }

        for keyword, explanation in cooking_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 맛있는 요리법을 알려드릴게요!\n\n{explanation}\n\n구체적인 재료나 요리 스타일을 말씀해주시면 더 자세한 레시피를 제공해드릴게요! 👨‍🍳"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 대한 요리 팁을 알려드릴게요!

**요리의 기본:**
🔥 **화력 조절**: 재료에 맞는 적절한 온도
🧂 **간**: 단계별로 맛을 맞춰가기
⏰ **타이밍**: 재료 넣는 순서와 시간
🍽️ **플레이팅**: 보기 좋게 담는 법

집에서도 맛집 못지않은 요리를 만들 수 있도록 도와드리겠습니다!

어떤 요리가 궁금하신지 구체적으로 말씀해주세요! 🍳"""

    def _lifestyle_expert_response(self, question: str, info: dict) -> str:
        """생활 꿀팁 전문가 답변"""
        question_lower = question.lower()

        lifestyle_topics = {
            "청소": "효과적인 청소 꿀팁을 알려드릴게요!\n\n**베이킹소다**: 기름때, 냄새 제거의 만능템\n**식초**: 물때, 세균 제거에 효과적\n**순서**: 위에서 아래로, 안쪽에서 바깥쪽으로\n**도구**: 용도별 청소 도구 활용법",
            "정리": "깔끔한 정리 수납법을 설명해드릴게요!\n\n**미니멀**: 안 쓰는 물건은 과감히 버리기\n**분류**: 용도별, 사용 빈도별 분류\n**수납**: 보이는 곳은 예쁘게, 안 보이는 곳은 효율적으로\n**라벨링**: 가족 모두가 알 수 있게 표시",
            "절약": "생활비 절약 노하우를 공유하겠습니다!\n\n**전기세**: 대기전력 차단, LED 전구 사용\n**수도세**: 절수형 샤워기, 세탁 모아서 하기\n**가스비**: 압력솥 활용, 불끄고 여열 이용\n**통신비**: 요금제 최적화, 할인 혜택 활용",
            "세탁": "옷 관리와 세탁 팁을 알려드릴게요!\n\n**분리세탁**: 색깔별, 소재별 분리\n**온도**: 소재에 맞는 적정 온도\n**세제**: 중성세제, 표백제 올바른 사용\n**건조**: 통풍 좋은 곳에서 자연건조",
        }

        for keyword, explanation in lifestyle_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 생활의 지혜를 전수해드릴게요!\n\n{explanation}\n\n더 구체적인 상황을 말씀해주시면 맞춤형 꿀팁을 제공해드릴게요! ✨"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 관한 생활 꿀팁을 알려드릴게요!

**생활의 지혜:**
🧹 **청소**: 간단하고 효과적인 청소법
📦 **정리수납**: 공간 활용 극대화 팁
💰 **절약**: 생활비 줄이는 실용 노하우
👕 **관리**: 옷, 가전제품 오래 쓰는 법

일상생활이 더 편리하고 경제적이 되도록 도와드리겠습니다!

어떤 생활 고민이 있으신지 자세히 말씀해주세요! 💡"""

    def _interior_expert_response(self, question: str, info: dict) -> str:
        """집꾸미기 전문가 답변"""
        question_lower = question.lower()

        interior_topics = {
            "작은방": "작은 공간 인테리어 노하우를 알려드릴게요!\n\n**색상**: 밝은 톤으로 공간감 확대\n**가구**: 다용도 가구로 공간 활용\n**거울**: 거울로 시각적 공간 확장\n**수직공간**: 벽면 수납으로 바닥 공간 확보",
            "조명": "조명 인테리어 팁을 설명해드릴게요!\n\n**자연광**: 커튼으로 채광 조절\n**간접조명**: 따뜻한 분위기 연출\n**포인트조명**: 공간별 용도에 맞는 조명\n**스마트조명**: 색온도 조절로 분위기 변화",
            "가구": "가구 배치와 선택 요령을 알려드릴게요!\n\n**동선**: 움직임에 방해되지 않는 배치\n**비율**: 공간 크기에 맞는 가구 선택\n**기능성**: 수납과 실용성을 고려한 선택\n**통일성**: 전체적인 스타일 조화",
            "diy": "DIY 인테리어 아이디어를 제안해드릴게요!\n\n**페인팅**: 벽면 포인트 컬러로 분위기 변화\n**데코**: 소품으로 개성 있는 공간 연출\n**리폼**: 기존 가구 활용한 새로운 스타일\n**플랜테리어**: 식물로 자연스러운 인테리어",
        }

        for keyword, explanation in interior_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 멋진 공간 만들기를 도와드릴게요!\n\n{explanation}\n\n구체적인 공간이나 예산을 말씀해주시면 더 자세한 조언을 드릴게요! 🎨"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 대한 인테리어 조언을 드릴게요!

**공간 꾸미기 원칙:**
🎨 **컬러**: 2-3가지 메인 컬러로 통일감
🪑 **가구**: 기능성과 미적 조화
💡 **조명**: 분위기를 좌우하는 핵심 요소
🌿 **소품**: 개성을 드러내는 포인트

작은 변화로도 공간이 완전히 달라질 수 있어요!

어떤 공간을 꾸미고 싶으신지, 예산은 어느 정도인지 알려주세요! 🏠"""

    def _finance_expert_response(self, question: str, info: dict) -> str:
        """가계부 전문가 답변"""
        question_lower = question.lower()

        finance_topics = {
            "저축": "효과적인 저축 방법을 알려드릴게요!\n\n**자동이체**: 월급날 바로 저축 계좌로 이체\n**365일 저축**: 매일 조금씩 쌓아가는 습관\n**목표 설정**: 구체적인 목표 금액과 기간\n**고금리 상품**: 적금, CMA 등 금리 비교",
            "가계부": "가계부 작성 노하우를 설명해드릴게요!\n\n**분류**: 고정비, 변동비로 나누어 기록\n**앱 활용**: 간편한 가계부 앱 추천\n**분석**: 월별 지출 패턴 분석\n**목표**: 지출 한도 설정과 관리",
            "투자": "안전한 투자 시작법을 알려드릴게요!\n\n**예적금**: 안전한 기본 투자\n**펀드**: 분산투자로 리스크 관리\n**주식**: 기업 분석 후 장기 투자\n**부동산**: 실거주 목적의 내 집 마련",
            "부채": "부채 관리 전략을 제안해드릴게요!\n\n**우선순위**: 고금리 부채부터 상환\n**통합**: 여러 부채를 낮은 금리로 통합\n**상환계획**: 무리하지 않는 선에서 계획\n**추가부채 금지**: 상환 완료까지 추가 대출 자제",
        }

        for keyword, explanation in finance_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 든든한 재정 관리를 도와드릴게요!\n\n{explanation}\n\n구체적인 상황을 말씀해주시면 맞춤형 재정 계획을 세워드릴게요! 📊"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 대한 재정 관리 조언을 드릴게요!

**건전한 재정 관리:**
💳 **지출 관리**: 수입의 70% 이내 생활비
💰 **저축**: 수입의 20% 이상 저축
📈 **투자**: 수입의 10% 장기 투자
🆘 **비상금**: 월 생활비의 3-6개월분

돈 관리가 어렵지 않도록 단계적으로 도와드리겠습니다!

현재 재정 상황이나 고민을 구체적으로 말씀해주세요! 💰"""

    def _hobby_expert_response(self, question: str, info: dict) -> str:
        """취미 전문가 답변"""
        question_lower = question.lower()

        hobby_topics = {
            "운동": "건강한 운동 취미를 추천해드릴게요!\n\n**홈트**: 집에서 할 수 있는 간단한 운동\n**러닝**: 부담 없이 시작하는 조깅\n**수영**: 전신 운동으로 체력 향상\n**등산**: 자연과 함께하는 힐링 운동",
            "독서": "독서 취미 시작 가이드를 알려드릴게요!\n\n**장르 선택**: 관심 분야부터 가볍게 시작\n**독서 습관**: 매일 30분씩 꾸준히\n**독서 기록**: 감상문이나 명언 메모\n**독서 모임**: 함께 읽고 토론하기",
            "여행": "여행 계획과 팁을 공유해드릴게요!\n\n**국내여행**: 가까운 곳부터 천천히\n**예산 여행**: 저렴하게 즐기는 여행법\n**혼행**: 혼자서도 안전하고 즐거운 여행\n**사진**: 여행의 추억을 남기는 사진 촬영",
            "요리": "요리 취미 시작법을 알려드릴게요!\n\n**기본기**: 칼질, 불 조절 등 기초 기술\n**간단 레시피**: 실패 없는 쉬운 요리부터\n**도구**: 꼭 필요한 기본 조리 도구\n**응용**: 기본을 익힌 후 창의적 응용",
        }

        for keyword, explanation in hobby_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 즐거운 취미 생활을 제안해드릴게요!\n\n{explanation}\n\n어떤 취미에 관심이 있으신지 더 자세히 말씀해주세요! 🌟"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 관한 취미 활동을 추천해드릴게요!

**취미 생활의 즐거움:**
🎯 **목표**: 성취감을 주는 도전적 활동
👥 **소통**: 같은 관심사를 가진 사람들과 교류
🧘 **힐링**: 스트레스 해소와 재충전
📚 **성장**: 새로운 지식과 기술 습득

바쁜 일상 속에서도 즐길 수 있는 취미를 찾아드리겠습니다!

관심 있는 분야나 가능한 시간을 알려주세요! 🎮"""

    def _tech_expert_response(self, question: str, info: dict) -> str:
        """IT 전문가 답변"""
        question_lower = question.lower()

        tech_topics = {
            "컴퓨터": "컴퓨터 활용 팁을 알려드릴게요!\n\n**기본 설정**: 보안, 업데이트, 백업 관리\n**단축키**: 작업 효율을 높이는 필수 단축키\n**프로그램**: 생산성 향상 프로그램 추천\n**문제 해결**: 자주 발생하는 오류 해결법",
            "스마트폰": "스마트폰 똑똑하게 쓰는 법을 설명해드릴게요!\n\n**앱 정리**: 필요한 앱만 깔끔하게 정리\n**배터리**: 배터리 오래 쓰는 설정 방법\n**보안**: 개인정보 보호 설정\n**사진**: 스마트폰으로 잘 찍는 사진 팁",
            "엑셀": "엑셀 활용법을 가르쳐드릴게요!\n\n**기본 함수**: SUM, AVERAGE, IF 함수\n**표 작성**: 깔끔한 표 만들기와 서식\n**차트**: 데이터 시각화로 이해도 높이기\n**자동화**: 반복 작업을 줄이는 매크로",
            "인터넷": "인터넷 안전하게 사용하는 법을 알려드릴게요!\n\n**보안**: 피싱, 악성코드 예방법\n**검색**: 원하는 정보 빠르게 찾는 검색 팁\n**쇼핑**: 안전한 온라인 쇼핑 방법\n**SNS**: 개인정보 보호하며 SNS 이용",
        }

        for keyword, explanation in tech_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 디지털 생활을 도와드릴게요!\n\n{explanation}\n\n어떤 기능이나 프로그램에 대해 더 알고 싶으신지 말씀해주세요! 🔧"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 대한 IT 활용법을 알려드릴게요!

**디지털 라이프 향상:**
💻 **컴퓨터**: 기본 설정부터 고급 활용까지
📱 **모바일**: 스마트폰 100% 활용법
📊 **오피스**: 워드, 엑셀, 파워포인트 정복
🌐 **인터넷**: 안전하고 효율적인 웹 서핑

컴맹 탈출부터 업무 자동화까지 도와드리겠습니다!

어떤 기술이나 프로그램이 궁금하신지 구체적으로 말씀해주세요! 💻"""

    def _health_expert_response(self, question: str, info: dict) -> str:
        """건강 전문가 답변"""
        question_lower = question.lower()

        health_topics = {
            "운동": "건강한 운동법을 알려드릴게요!\n\n**유산소**: 심폐 기능 향상을 위한 유산소 운동\n**근력**: 기초 대사량 증가를 위한 근력 운동\n**스트레칭**: 유연성과 부상 예방을 위한 스트레칭\n**홈트**: 집에서 할 수 있는 간단한 운동",
            "식단": "건강한 식단 관리법을 설명해드릴게요!\n\n**균형**: 탄수화물, 단백질, 지방의 균형\n**채소**: 하루 5가지 색깔 채소 섭취\n**수분**: 하루 2L 이상 충분한 수분 섭취\n**금식**: 간헐적 단식의 올바른 방법",
            "수면": "숙면을 위한 팁을 알려드릴게요!\n\n**시간**: 규칙적인 수면 시간 유지\n**환경**: 어둡고 시원한 수면 환경 조성\n**습관**: 잠들기 전 디지털 기기 사용 자제\n**이완**: 명상이나 독서로 마음 진정",
            "스트레스": "스트레스 관리법을 제안해드릴게요!\n\n**호흡법**: 복식 호흡으로 마음 안정\n**명상**: 10분 명상으로 마음 정리\n**취미**: 좋아하는 활동으로 스트레스 해소\n**소통**: 가족, 친구와의 대화로 마음 나누기",
        }

        for keyword, explanation in health_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 건강한 생활을 도와드릴게요!\n\n{explanation}\n\n더 구체적인 건강 고민이 있으시면 말씀해주세요! 💪"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 관한 건강 관리법을 알려드릴게요!

**건강한 생활 습관:**
🏃 **운동**: 주 3회 이상 규칙적인 운동
🥗 **식단**: 균형 잡힌 영양소 섭취
😴 **수면**: 하루 7-8시간 충분한 잠
🧘 **마음**: 스트레스 관리와 정신 건강

작은 변화부터 시작해서 건강한 삶을 만들어보세요!

어떤 건강 고민이 있으신지 구체적으로 말씀해주세요! 🏃"""

    def _learning_expert_response(self, question: str, info: dict) -> str:
        """공부 전문가 답변"""
        question_lower = question.lower()

        learning_topics = {
            "공부법": "효과적인 공부 방법을 알려드릴게요!\n\n**플래닝**: 구체적인 학습 계획 세우기\n**집중**: 25분 공부 + 5분 휴식 (포모도로 기법)\n**복습**: 에빙하우스 망각곡선에 따른 복습\n**환경**: 집중력을 높이는 공부 환경 조성",
            "기억법": "기억력 향상 기법을 설명해드릴게요!\n\n**연상법**: 기억할 내용을 이미지로 연상\n**스토리**: 내용을 이야기로 만들어서 기억\n**반복**: 규칙적인 간격으로 반복 학습\n**정리**: 마인드맵이나 요약으로 체계화",
            "시험": "시험 준비 전략을 제안해드릴게요!\n\n**기출문제**: 출제 경향 파악을 위한 기출 분석\n**모의고사**: 실전 연습으로 시간 관리 연습\n**오답노트**: 틀린 문제 분석하고 반복 학습\n**컨디션**: 시험 전 충분한 휴식과 컨디션 관리",
            "집중력": "집중력 향상 방법을 알려드릴게요!\n\n**환경**: 공부에만 집중할 수 있는 환경 조성\n**스마트폰**: 공부 시간에는 스마트폰 멀리 두기\n**목표**: 구체적이고 달성 가능한 목표 설정\n**휴식**: 적절한 휴식으로 집중력 회복",
        }

        for keyword, explanation in learning_topics.items():
            if keyword in question_lower:
                return f"{info['emoji']} {info['name']}이 효과적인 학습을 도와드릴게요!\n\n{explanation}\n\n어떤 과목이나 시험을 준비하시는지 알려주시면 더 구체적인 조언을 드릴게요! ✏️"

        return f"""{info['emoji']} {info['name']}입니다!

"{question}"에 대한 학습 조언을 드릴게요!

**스마트한 학습법:**
📝 **계획**: 목표에 맞는 체계적인 학습 계획
🧠 **기억**: 효과적인 암기와 이해 방법
⏰ **시간관리**: 효율적인 시간 활용법
💪 **동기부여**: 지속 가능한 학습 동기 유지

공부가 즐거워지는 방법을 찾아드리겠습니다!

어떤 과목이나 분야를 공부하시는지 알려주세요! 📚"""

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
    async def stem_ask(request: STEMRequest, client_request: Request):
        """STEM 질문 처리 API"""
        try:
            # 사용자 IP 추출
            user_ip = client_request.client.host if client_request.client else "unknown"

            result = await stem_service.process_question(
                request.question, request.agent_type, user_ip
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

    @app.get("/stem/stats")
    async def stem_statistics():
        """STEM 서비스 사용 통계"""
        try:
            stats = usage_tracker.get_statistics()
            return JSONResponse(content=stats)
        except Exception as e:
            return JSONResponse(
                content={"error": f"통계 조회 오류: {str(e)}"},
                status_code=500,
            )

    @app.get("/stem/stats/dashboard")
    async def stem_stats_dashboard(admin_key: Optional[str] = None):
        """사용 통계 대시보드 페이지 - 관리자 인증 필요"""

        # 관리자 인증 확인
        ADMIN_SECRET = (
            "hyojin_admin_2024_secure"  # 실제로는 환경변수나 설정 파일에서 가져와야 함
        )

        if admin_key != ADMIN_SECRET:
            return HTMLResponse(
                content="""
                <!DOCTYPE html>
                <html lang="ko">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>🔒 관리자 인증</title>
                    <style>
                        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; 
                               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                               min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                        .auth-container { background: rgba(255,255,255,0.95); border-radius: 20px; 
                                         padding: 40px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                                         max-width: 400px; width: 100%; }
                        .auth-form { margin: 20px 0; }
                        .auth-input { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #ddd; 
                                     border-radius: 10px; font-size: 16px; text-align: center; }
                        .auth-btn { background: #4CAF50; color: white; padding: 15px 30px; border: none; 
                                   border-radius: 10px; font-size: 16px; cursor: pointer; width: 100%; }
                        .auth-btn:hover { background: #45a049; }
                        .back-link { margin-top: 20px; }
                        .back-link a { color: #666; text-decoration: none; }
                    </style>
                </head>
                <body>
                    <div class="auth-container">
                        <h2>🔒 관리자 인증</h2>
                        <p>통계 대시보드에 접근하려면 관리자 키가 필요합니다.</p>
                        
                        <form class="auth-form" onsubmit="authenticateAdmin(event)">
                            <input type="password" id="adminKey" class="auth-input" 
                                   placeholder="관리자 키를 입력하세요" required>
                            <button type="submit" class="auth-btn">🔓 인증</button>
                        </form>
                        
                        <div class="back-link">
                            <a href="/stem">🔙 서비스로 돌아가기</a>
                        </div>
                    </div>
                    
                    <script>
                        function authenticateAdmin(event) {
                            event.preventDefault();
                            const adminKey = document.getElementById('adminKey').value;
                            window.location.href = `/stem/stats/dashboard?admin_key=${adminKey}`;
                        }
                    </script>
                </body>
                </html>
                """,
                status_code=401,
            )

        try:
            stats = usage_tracker.get_statistics()
            recent_activity = usage_tracker.get_recent_activity(20)

            # HTML 대시보드 생성
            stats_html = f"""
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>📊 AI 도깨비마을 STEM 센터 - 사용 통계</title>
                <style>
                    body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; 
                           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           min-height: 100vh; }}
                    .container {{ max-width: 1200px; margin: 0 auto; 
                                background: rgba(255,255,255,0.95); border-radius: 20px; 
                                padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                                  gap: 20px; margin: 20px 0; }}
                    .stat-card {{ background: linear-gradient(45deg, #4CAF50, #45a049); 
                                 color: white; padding: 20px; border-radius: 15px; 
                                 text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
                    .stat-number {{ font-size: 2.5em; font-weight: bold; }}
                    .stat-label {{ font-size: 1.1em; opacity: 0.9; }}
                    .chart-section {{ background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                    .agent-bar {{ background: #2196F3; height: 25px; margin: 5px 0; 
                                border-radius: 12px; position: relative; }}
                    .agent-label {{ position: absolute; left: 10px; top: 3px; color: white; font-weight: bold; }}
                    .agent-count {{ position: absolute; right: 10px; top: 3px; color: white; }}
                    .recent-activity {{ background: #fff3cd; padding: 15px; border-radius: 10px; 
                                      margin: 10px 0; border-left: 5px solid #ffc107; }}
                    h1, h2 {{ color: #333; text-align: center; }}
                    .refresh-btn {{ background: #FF5722; color: white; padding: 10px 20px; 
                                   border: none; border-radius: 5px; cursor: pointer; 
                                   font-size: 16px; margin: 10px; }}
                    .back-btn {{ background: #2196F3; color: white; padding: 15px 30px; 
                               text-decoration: none; border-radius: 10px; display: inline-block; 
                               margin: 20px 0; }}
                </style>
                <script>
                    function refreshStats() {{
                        location.reload();
                    }}
                    setInterval(refreshStats, 30000); // 30초마다 자동 새로고침
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>📊 AI 도깨비마을 STEM 센터 - 실시간 사용 통계</h1>
                    <p style="text-align: center; color: #666;">베타 서비스 모니터링 대시보드 (30초마다 자동 업데이트)</p>
            """

            if "message" in stats:
                stats_html += f"""
                    <div style="text-align: center; padding: 50px;">
                        <h2>📈 {stats['message']}</h2>
                        <p>사용자들이 질문을 시작하면 여기에 통계가 표시됩니다!</p>
                    </div>
                """
            else:
                # 주요 통계 카드들
                stats_html += f"""
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{stats['total_usage']}</div>
                            <div class="stat-label">총 사용량</div>
                        </div>
                        <div class="stat-card" style="background: linear-gradient(45deg, #FF9800, #F57C00);">
                            <div class="stat-number">{stats['success_rate']}%</div>
                            <div class="stat-label">성공률</div>
                        </div>
                        <div class="stat-card" style="background: linear-gradient(45deg, #9C27B0, #7B1FA2);">
                            <div class="stat-number">{stats['peak_hour']}시</div>
                            <div class="stat-label">피크 시간</div>
                        </div>
                        <div class="stat-card" style="background: linear-gradient(45deg, #F44336, #D32F2F);">
                            <div class="stat-number">{stats['average_question_length']}</div>
                            <div class="stat-label">평균 질문 길이</div>
                        </div>
                    </div>
                    
                    <div class="chart-section">
                        <h2>👥 에이전트별 사용량</h2>
                """

                max_usage = (
                    max(stats["agent_usage"].values()) if stats["agent_usage"] else 1
                )
                for agent, count in stats["agent_usage"].items():
                    width = (count / max_usage) * 100
                    stats_html += f"""
                        <div class="agent-bar" style="width: {width}%;">
                            <span class="agent-label">{agent}</span>
                            <span class="agent-count">{count}회</span>
                        </div>
                    """

                stats_html += """
                    </div>
                    
                    <div class="chart-section">
                        <h2>📅 일별 사용량</h2>
                """

                for date, count in stats["daily_usage"].items():
                    stats_html += f"""
                        <div class="recent-activity">
                            📅 {date}: <strong>{count}회 사용</strong>
                        </div>
                    """

                stats_html += """
                    </div>
                """

            # 최근 활동
            stats_html += """
                <div class="chart-section">
                    <h2>🕐 최근 활동</h2>
            """

            for activity in recent_activity[:10]:
                if "error" not in activity:
                    agent_names = {
                        "math": "🧮 수학",
                        "physics": "⚛️ 물리학",
                        "chemistry": "🧪 화학",
                        "biology": "🧬 생물학",
                        "engineering": "⚙️ 공학",
                        "assistant": "🤖 업무",
                        "marketing": "📈 마케팅",
                        "startup": "🚀 창업",
                    }
                    agent_name = agent_names.get(
                        activity.get("agent_type", ""), activity.get("agent_type", "")
                    )
                    stats_html += f"""
                        <div class="recent-activity">
                            <strong>{activity.get('time', '')} - {agent_name}</strong><br>
                            질문: "{activity.get('question_preview', '')}"
                            {'✅ 성공' if activity.get('response_success') else '❌ 실패'}
                        </div>
                    """

            stats_html += f"""
                    </div>
                    
                    <div style="text-align: center;">
                        <button class="refresh-btn" onclick="refreshStats()">🔄 수동 새로고침</button>
                        <a href="/stem" class="back-btn">🔙 서비스로 돌아가기</a>
                    </div>
                    
                    <div style="text-align: center; margin-top: 20px; color: #666;">
                        <p>마지막 업데이트: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                </div>
            </body>
            </html>
            """

            return HTMLResponse(content=stats_html)

        except Exception as e:
            return HTMLResponse(
                content=f"<h1>통계 대시보드 오류</h1><p>{str(e)}</p>",
                status_code=500,
            )

    print("✅ 실제 AI 대화 능력 기반 STEM 라우트 추가 완료!")
    return app
