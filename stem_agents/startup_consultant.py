#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 스타트업 도깨비 - 고품질 창업 및 비즈니스 성장 전문가
Advanced Startup Consultant AI with Professional Business Strategy
"""

import sqlite3
import json
import datetime
import random
from pathlib import Path
import logging
from dataclasses import dataclass


@dataclass
class StartupProject:
    """스타트업 프로젝트 데이터 클래스"""

    id: int
    name: str
    industry: str
    stage: str
    valuation: float
    funding: float
    status: str
    created_at: str


class StartupConsultantGoblin:
    """🚀 스타트업 도깨비 - 고품질 창업 전문가"""

    def __init__(self, workspace_dir="./startup_workspace"):
        self.name = "스타트업 도깨비"
        self.emoji = "🚀"
        self.description = "창업과 비즈니스 성장 컨설팅 전문가"

        # 워크스페이스 설정
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)

        # 스타트업 전문 디렉토리
        for subdir in [
            "business_plans",
            "financial_models",
            "pitch_decks",
            "market_research",
            "legal_docs",
            "growth_strategies",
        ]:
            (self.workspace_dir / subdir).mkdir(exist_ok=True)

        # 데이터베이스 초기화
        self.db_path = self.workspace_dir / "startup_projects.db"
        self.init_database()

        # 로깅 설정
        log_file = self.workspace_dir / "startup.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

        # 스타트업 전문 기능
        self.startup_stages = [
            "아이디어",
            "MVP",
            "시드",
            "시리즈A",
            "시리즈B+",
            "IPO준비",
        ]
        self.industries = [
            "AI/Tech",
            "헬스케어",
            "핀테크",
            "이커머스",
            "교육",
            "푸드테크",
        ]
        self.funding_types = [
            "엔젤투자",
            "시드펀딩",
            "시리즈A",
            "벤처캐피탈",
            "크라우드펀딩",
            "정부지원",
        ]
        self.business_models = [
            "B2B SaaS",
            "B2C 플랫폼",
            "마켓플레이스",
            "구독모델",
            "API 비즈니스",
            "프리미엄",
        ]

        # 스타트업 프레임워크
        self.frameworks = self._initialize_startup_frameworks()

        self.logger.info(f"{self.name} 창업 시스템 초기화 완료")
        print(f"✅ {self.emoji} {self.name} 창업 인큐베이터 준비 완료!")
        print(f"🚀 워크스페이스: {self.workspace_dir.absolute()}")

    def init_database(self):
        """스타트업 전용 데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 스타트업 프로젝트 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS startup_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    industry TEXT NOT NULL,
                    business_model TEXT,
                    target_market TEXT,
                    problem_statement TEXT,
                    solution_description TEXT,
                    value_proposition TEXT,
                    competitive_advantage TEXT,
                    startup_stage TEXT DEFAULT 'idea',
                    team_size INTEGER DEFAULT 1,
                    founding_date TEXT,
                    current_valuation REAL DEFAULT 0.0,
                    total_funding REAL DEFAULT 0.0,
                    monthly_revenue REAL DEFAULT 0.0,
                    monthly_burn_rate REAL DEFAULT 0.0,
                    runway_months INTEGER DEFAULT 0,
                    customer_count INTEGER DEFAULT 0,
                    mvp_status TEXT DEFAULT 'planning',
                    product_market_fit_score REAL DEFAULT 0.0,
                    growth_rate REAL DEFAULT 0.0,
                    market_size REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # 비즈니스 플랜 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS business_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    startup_id INTEGER,
                    plan_type TEXT NOT NULL,
                    executive_summary TEXT,
                    market_analysis TEXT,
                    financial_projections TEXT,
                    marketing_strategy TEXT,
                    operations_plan TEXT,
                    risk_analysis TEXT,
                    funding_requirements TEXT,
                    milestones TEXT,
                    version TEXT DEFAULT '1.0',
                    status TEXT DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (startup_id) REFERENCES startup_projects (id)
                )
            """
            )

            # 투자 라운드 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS funding_rounds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    startup_id INTEGER,
                    round_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    pre_money_valuation REAL,
                    post_money_valuation REAL,
                    investor_name TEXT,
                    investor_type TEXT,
                    equity_percentage REAL,
                    funding_date TEXT,
                    use_of_funds TEXT,
                    board_seats INTEGER DEFAULT 0,
                    liquidation_preference TEXT,
                    anti_dilution_rights TEXT,
                    status TEXT DEFAULT 'completed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (startup_id) REFERENCES startup_projects (id)
                )
            """
            )

            # 성장 메트릭 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS growth_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    startup_id INTEGER,
                    metric_date TEXT NOT NULL,
                    daily_active_users INTEGER DEFAULT 0,
                    monthly_active_users INTEGER DEFAULT 0,
                    monthly_recurring_revenue REAL DEFAULT 0.0,
                    customer_acquisition_cost REAL DEFAULT 0.0,
                    lifetime_value REAL DEFAULT 0.0,
                    churn_rate REAL DEFAULT 0.0,
                    net_promoter_score REAL DEFAULT 0.0,
                    product_market_fit_score REAL DEFAULT 0.0,
                    burn_rate REAL DEFAULT 0.0,
                    runway_months INTEGER DEFAULT 0,
                    gross_margin REAL DEFAULT 0.0,
                    conversion_rate REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (startup_id) REFERENCES startup_projects (id)
                )
            """
            )

            conn.commit()

    def _initialize_startup_frameworks(self):
        """스타트업 프레임워크 초기화"""
        return {
            "Lean_Canvas": {
                "Problem": "해결하고자 하는 고객의 핵심 문제",
                "Solution": "문제에 대한 혁신적 해결책",
                "Key_Metrics": "성공을 측정하는 핵심 지표",
                "Unique_Value_Prop": "경쟁사와 차별화되는 고유 가치",
                "Unfair_Advantage": "쉽게 복제할 수 없는 경쟁 우위",
                "Channels": "고객에게 도달하는 방법",
                "Customer_Segments": "타겟 고객 그룹",
                "Cost_Structure": "주요 비용 요소",
                "Revenue_Streams": "수익 창출 방법",
            },
            "PMF_Framework": {
                "Market": "충분히 큰 시장 규모와 성장 잠재력",
                "Product": "시장 니즈를 만족시키는 제품",
                "Team": "실행 능력을 갖춘 팀",
                "Business_Model": "지속 가능한 수익 모델",
                "Timing": "시장 진입의 최적 타이밍",
            },
            "Growth_Hacking": {
                "Acquisition": "새로운 고객 획득 전략",
                "Activation": "첫 경험에서의 가치 전달",
                "Retention": "고객 유지 및 재참여",
                "Revenue": "수익 증대 및 업셀",
                "Referral": "추천을 통한 바이럴 성장",
            },
            "Funding_Strategy": {
                "Pre_Seed": "아이디어 검증 및 초기 팀 구성",
                "Seed": "MVP 개발 및 초기 트랙션",
                "Series_A": "제품 시장 적합성 및 확장",
                "Series_B": "시장 점유율 확대 및 글로벌화",
                "Later_Stage": "상장 준비 및 M&A 전략",
            },
        }

    def create_business_plan(
        self,
        startup_name: str,
        industry: str,
        problem_statement: str,
        solution: str,
        target_market: str,
        business_model: str,
    ) -> str:
        """종합 비즈니스 플랜 생성"""
        try:
            self.logger.info(f"비즈니스 플랜 생성 시작: {startup_name}")

            # 시장 분석
            market_analysis = self._conduct_market_analysis(industry, target_market)

            # 경쟁 분석
            competitive_analysis = self._analyze_competition(industry, solution)

            # 재무 모델 생성
            financial_projections = self._create_financial_model(
                business_model, target_market
            )

            # 마케팅 전략
            marketing_strategy = self._develop_marketing_strategy(
                target_market, business_model
            )

            # 운영 계획
            operations_plan = self._create_operations_plan(business_model, solution)

            # 리스크 분석
            risk_analysis = self._assess_startup_risks(industry, business_model)

            # 펀딩 요구사항
            funding_requirements = self._calculate_funding_needs(financial_projections)

            # 마일스톤 설정
            milestones = self._set_key_milestones(business_model)

            # 스타트업 프로젝트 저장
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 메인 프로젝트 저장
                cursor.execute(
                    """
                    INSERT INTO startup_projects 
                    (project_name, industry, business_model, target_market, 
                     problem_statement, solution_description, startup_stage, 
                     market_size, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        startup_name,
                        industry,
                        business_model,
                        target_market,
                        problem_statement,
                        solution,
                        "아이디어",
                        market_analysis["market_size"],
                        "active",
                    ),
                )

                startup_id = cursor.lastrowid

                # 비즈니스 플랜 저장
                cursor.execute(
                    """
                    INSERT INTO business_plans 
                    (startup_id, plan_type, market_analysis, financial_projections,
                     marketing_strategy, operations_plan, risk_analysis, 
                     funding_requirements, milestones, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        startup_id,
                        "종합계획",
                        json.dumps(market_analysis),
                        json.dumps(financial_projections),
                        json.dumps(marketing_strategy),
                        json.dumps(operations_plan),
                        json.dumps(risk_analysis),
                        json.dumps(funding_requirements),
                        json.dumps(milestones),
                        "completed",
                    ),
                )

                plan_id = cursor.lastrowid
                conn.commit()

            return f"""🚀 **종합 비즈니스 플랜 완성!**

**📋 프로젝트 정보:**
• 스타트업 ID: #{startup_id}
• 플랜 ID: #{plan_id}
• 회사명: {startup_name}
• 산업: {industry}
• 비즈니스 모델: {business_model}
• 타겟 시장: {target_market}

**🎯 핵심 개요:**
**문제:** {problem_statement}
**솔루션:** {solution}

**📊 시장 분석:**
{self._format_market_analysis(market_analysis)}

**💰 재무 전망 (5년):**
{self._format_financial_projections(financial_projections)}

**📈 마케팅 전략:**
{self._format_marketing_strategy(marketing_strategy)}

**⚙️ 운영 계획:**
{self._format_operations_plan(operations_plan)}

**⚠️ 리스크 분석:**
{self._format_risk_analysis(risk_analysis)}

**💵 펀딩 계획:**
{self._format_funding_requirements(funding_requirements)}

**🎯 주요 마일스톤:**
{self._format_milestones(milestones)}

**🚀 핵심 성공 요인:**
• 강력한 제품-시장 적합성 달성
• 경험 있는 팀과 확장 가능한 기술
• 효율적인 고객 획득 채널 구축
• 지속 가능한 수익 모델 검증
• 전략적 파트너십 및 투자 유치

**📈 예상 성과 (2년차):**
• 월 매출: {financial_projections['year2_monthly_revenue']:,.0f}원
• 고객 수: {financial_projections['year2_customers']:,}명
• 시장 점유율: {financial_projections['market_share']:.1f}%
• 예상 밸류에이션: {financial_projections['projected_valuation']:,.0f}원

**🎯 투자 포인트:**
• 큰 시장 기회와 확장성
• 차별화된 기술 및 경쟁 우위
• 검증된 비즈니스 모델
• 경험 있는 창업팀
• 명확한 성장 전략

🚀 {self.name}이 성공적인 창업을 위한 로드맵을 제시했습니다!"""

        except Exception as e:
            return f"❌ 비즈니스 플랜 생성 실패: {str(e)}"

    def _conduct_market_analysis(self, industry: str, target_market: str) -> dict:
        """시장 분석 수행"""
        market_sizes = {
            "AI/Tech": 150000000000,
            "헬스케어": 80000000000,
            "핀테크": 120000000000,
            "이커머스": 200000000000,
            "교육": 60000000000,
            "푸드테크": 40000000000,
        }

        base_size = market_sizes.get(industry, 50000000000)
        growth_rate = random.uniform(8, 25)

        return {
            "market_size": base_size,
            "growth_rate": growth_rate,
            "market_maturity": "성장기",
            "key_trends": [
                f"{industry} 분야의 디지털 전환 가속화",
                "고객 니즈의 개인화 및 맞춤화 증대",
                "데이터 기반 의사결정 문화 확산",
                "ESG 및 지속가능성 중요성 증대",
            ],
            "opportunities": [
                "기존 솔루션의 한계를 극복하는 혁신적 접근",
                "미충족 고객 니즈에 대한 새로운 해결책",
                "기술 발전을 활용한 효율성 개선",
                "새로운 비즈니스 모델을 통한 가치 창출",
            ],
            "challenges": [
                "기존 플레이어들의 강력한 시장 지배력",
                "고객 교육 및 시장 인식 개선 필요",
                "규제 환경 변화에 대한 대응",
                "경쟁사들의 빠른 추격 및 모방",
            ],
        }

    def _analyze_competition(self, industry: str, solution: str) -> dict:
        """경쟁 분석"""
        return {
            "direct_competitors": [
                f"{industry} 분야 기존 선도 기업들",
                "유사한 솔루션을 제공하는 스타트업들",
                "대기업의 내부 개발팀 및 신사업",
            ],
            "indirect_competitors": [
                "대체 가능한 기존 솔루션들",
                "고객이 현재 사용하는 우회 방법들",
                "다른 방식으로 같은 문제를 해결하는 서비스들",
            ],
            "competitive_advantages": [
                "혁신적 기술과 독창적 접근법",
                "깊은 도메인 전문성과 인사이트",
                "민첩한 개발 속도와 고객 반응성",
                "차별화된 사용자 경험과 인터페이스",
            ],
            "barriers_to_entry": [
                "높은 기술적 진입 장벽",
                "강력한 네트워크 효과",
                "상당한 초기 투자 비용",
                "규제 및 인증 요구사항",
            ],
        }

    def _create_financial_model(self, business_model: str, target_market: str) -> dict:
        """재무 모델 생성"""
        base_revenue = random.uniform(50000000, 200000000)
        growth_rate = random.uniform(100, 300)  # 연 성장률 %

        return {
            "year1_revenue": base_revenue * 0.1,
            "year2_revenue": base_revenue * 0.3,
            "year3_revenue": base_revenue * 0.7,
            "year4_revenue": base_revenue * 1.2,
            "year5_revenue": base_revenue * 2.0,
            "year2_monthly_revenue": (base_revenue * 0.3) / 12,
            "year2_customers": random.randint(1000, 10000),
            "market_share": random.uniform(0.5, 3.0),
            "projected_valuation": base_revenue * random.uniform(8, 15),
            "gross_margin": random.uniform(60, 85),
            "break_even_month": random.randint(18, 36),
            "customer_acquisition_cost": random.uniform(50000, 200000),
            "lifetime_value": random.uniform(500000, 2000000),
            "ltv_cac_ratio": random.uniform(3, 8),
            "burn_rate": base_revenue * 0.15 / 12,
            "funding_required": base_revenue * 0.5,
        }

    def _develop_marketing_strategy(
        self, target_market: str, business_model: str
    ) -> dict:
        """마케팅 전략 개발"""
        return {
            "target_segments": [
                f"{target_market} 내 얼리 어답터 그룹",
                "혁신에 적극적인 중소기업 및 스타트업",
                "효율성 개선에 관심 높은 대기업 부서",
                "새로운 솔루션 도입에 열린 개인 사용자",
            ],
            "positioning": f"{target_market}을 위한 차세대 {business_model} 솔루션",
            "value_proposition": [
                "기존 대비 10배 빠른 처리 속도",
                "50% 이상의 비용 절감 효과",
                "직관적이고 사용하기 쉬운 인터페이스",
                "24/7 전문가 수준의 지원 서비스",
            ],
            "marketing_channels": [
                "디지털 마케팅 (SEO, SEM, 소셜미디어)",
                "콘텐츠 마케팅 (블로그, 웨비나, 백서)",
                "파트너십 및 리퍼럴 프로그램",
                "업계 컨퍼런스 및 네트워킹 이벤트",
            ],
            "customer_acquisition": [
                "무료 체험판을 통한 제품 경험 제공",
                "케이스 스터디 및 성공 사례 공유",
                "인플루언서 및 업계 전문가 협업",
                "바이럴 성장을 위한 인센티브 프로그램",
            ],
            "retention_strategy": [
                "지속적인 제품 개선 및 기능 추가",
                "개인화된 고객 성공 지원",
                "커뮤니티 구축 및 사용자 간 네트워킹",
                "로열티 프로그램 및 장기 할인 혜택",
            ],
        }

    def _create_operations_plan(self, business_model: str, solution: str) -> dict:
        """운영 계획 생성"""
        return {
            "technology_stack": [
                "클라우드 기반 확장 가능한 인프라",
                "최신 개발 프레임워크 및 도구",
                "보안 및 데이터 보호 시스템",
                "AI/ML 및 데이터 분석 플랫폼",
            ],
            "team_structure": [
                "창업팀: CEO, CTO, 핵심 개발자",
                "제품팀: 제품 매니저, UX/UI 디자이너",
                "영업/마케팅팀: 영업 총괄, 마케팅 전문가",
                "고객성공팀: 고객 지원 및 성공 관리자",
            ],
            "development_process": [
                "Agile/Scrum 기반 빠른 개발 주기",
                "지속적 통합 및 배포 (CI/CD)",
                "사용자 피드백 기반 빠른 반복 개발",
                "품질 보증 및 테스트 자동화",
            ],
            "key_partnerships": [
                "기술 파트너: 클라우드 제공업체, 개발 도구",
                "유통 파트너: 리셀러, 시스템 통합업체",
                "전략적 파트너: 업계 선도 기업들",
                "투자 파트너: VC, 엔젤 투자자, 멘토",
            ],
            "quality_assurance": [
                "국제 표준 보안 인증 획득",
                "고객 데이터 보호 및 프라이버시 준수",
                "서비스 품질 모니터링 및 개선",
                "정기적인 보안 감사 및 업데이트",
            ],
        }

    def _assess_startup_risks(self, industry: str, business_model: str) -> dict:
        """스타트업 리스크 평가"""
        return {
            "market_risks": {
                "level": "중간",
                "description": "시장 트렌드 변화 및 경쟁 심화",
                "mitigation": "지속적 시장 모니터링 및 제품 피벗 준비",
            },
            "technology_risks": {
                "level": "낮음",
                "description": "기술 구현 복잡성 및 확장성 이슈",
                "mitigation": "점진적 개발 및 전문가 영입",
            },
            "financial_risks": {
                "level": "높음",
                "description": "자금 소진 및 추가 투자 유치 어려움",
                "mitigation": "보수적 재무 관리 및 다양한 펀딩 옵션 준비",
            },
            "operational_risks": {
                "level": "중간",
                "description": "핵심 인재 이탈 및 운영 효율성 저하",
                "mitigation": "인센티브 제도 및 체계적 운영 프로세스 구축",
            },
            "regulatory_risks": {
                "level": "낮음",
                "description": "규제 환경 변화 및 컴플라이언스 요구",
                "mitigation": "법무 자문 확보 및 규제 모니터링",
            },
        }

    def _calculate_funding_needs(self, financial_projections: dict) -> dict:
        """펀딩 요구사항 계산"""
        total_funding = financial_projections["funding_required"]

        return {
            "total_funding_needed": total_funding,
            "seed_round": total_funding * 0.3,
            "series_a": total_funding * 0.7,
            "use_of_funds": {
                "제품개발": "40%",
                "마케팅_영업": "30%",
                "팀확장": "20%",
                "운영비": "10%",
            },
            "funding_timeline": {
                "시드라운드": "6개월 내",
                "시리즈A": "18개월 후",
                "시리즈B": "36개월 후",
            },
            "investor_targets": [
                "초기 단계 전문 VC",
                "업계 경험 있는 엔젤 투자자",
                "전략적 투자자 (기업 벤처캐피탈)",
                "정부 지원 프로그램 및 그랜트",
            ],
        }

    def _set_key_milestones(self, business_model: str) -> dict:
        """핵심 마일스톤 설정"""
        return {
            "3개월": {
                "product": "MVP 개발 완료 및 베타 테스트 시작",
                "business": "초기 고객 10명 확보",
                "team": "핵심 팀 구성 완료",
                "funding": "시드 펀딩 준비 시작",
            },
            "6개월": {
                "product": "정식 제품 런칭 및 피드백 반영",
                "business": "유료 고객 100명 돌파",
                "team": "개발팀 확장 (5명)",
                "funding": "시드 라운드 완료",
            },
            "12개월": {
                "product": "주요 기능 추가 및 안정성 개선",
                "business": "월 매출 1억원 달성",
                "team": "전 부문 팀 구성 (15명)",
                "funding": "시리즈A 준비 시작",
            },
            "18개월": {
                "product": "플랫폼 확장 및 API 출시",
                "business": "고객 1,000명 및 시장 점유율 1%",
                "team": "해외 진출팀 구성",
                "funding": "시리즈A 완료",
            },
            "24개월": {
                "product": "글로벌 서비스 및 다국어 지원",
                "business": "연 매출 100억원 및 흑자 전환",
                "team": "글로벌 팀 50명 이상",
                "funding": "시리즈B 검토 시작",
            },
        }

    def analyze_startup_metrics(self, startup_id: int) -> str:
        """스타트업 메트릭 분석"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 스타트업 기본 정보
                cursor.execute(
                    """
                    SELECT project_name, industry, startup_stage, 
                           current_valuation, total_funding, monthly_revenue, 
                           monthly_burn_rate, runway_months, customer_count
                    FROM startup_projects WHERE id = ?
                """,
                    (startup_id,),
                )

                startup_info = cursor.fetchone()
                if not startup_info:
                    return "❌ 해당 스타트업을 찾을 수 없습니다."

                (
                    name,
                    industry,
                    stage,
                    valuation,
                    funding,
                    revenue,
                    burn,
                    runway,
                    customers,
                ) = startup_info

                # 성장 메트릭 분석
                health_score = self._calculate_startup_health(
                    revenue, burn, customers, funding
                )
                recommendations = self._generate_growth_recommendations(
                    stage, health_score
                )

            return f"""🚀 **스타트업 메트릭 분석 결과**

**📊 기본 정보:**
• 회사명: {name}
• 산업: {industry}
• 단계: {stage}
• 현재 밸류에이션: {valuation:,.0f}원
• 총 투자 유치: {funding:,.0f}원

**💰 재무 현황:**
• 월 매출: {revenue:,.0f}원
• 월 번레이트: {burn:,.0f}원
• 런웨이: {runway}개월
• 고객 수: {customers:,}명

**📈 핵심 지표 분석:**
{self._format_key_metrics(revenue, burn, customers, funding)}

**🎯 스타트업 건강도:**
{self._format_health_score(health_score)}

**💡 성장 권장사항:**
{self._format_recommendations(recommendations)}

**🚨 주의 사항:**
{self._identify_red_flags(revenue, burn, runway, stage)}

**📊 벤치마크 비교:**
{self._compare_with_benchmark(industry, stage, revenue, customers)}

**🎯 다음 단계 액션 아이템:**
1. 고객 획득 비용 최적화
2. 제품-시장 적합성 강화
3. 운영 효율성 개선
4. 다음 펀딩 라운드 준비

🚀 {self.name}이 데이터 기반 성장 인사이트를 제공했습니다!"""

        except Exception as e:
            return f"❌ 메트릭 분석 실패: {str(e)}"

    def _calculate_startup_health(
        self, revenue: float, burn: float, customers: int, funding: float
    ) -> dict:
        """스타트업 건강도 계산"""
        # 건강도 점수 계산 (0-100)
        revenue_score = min(100, (revenue / 10000000) * 100) if revenue > 0 else 0
        burn_efficiency = (revenue / burn) * 100 if burn > 0 else 100
        customer_growth = min(100, (customers / 1000) * 100)
        funding_adequacy = min(100, (funding / 1000000000) * 100)

        overall_score = (
            revenue_score + burn_efficiency + customer_growth + funding_adequacy
        ) / 4

        return {
            "overall_score": overall_score,
            "revenue_health": revenue_score,
            "burn_efficiency": burn_efficiency,
            "customer_traction": customer_growth,
            "funding_position": funding_adequacy,
            "risk_level": (
                "Low"
                if overall_score > 70
                else "Medium" if overall_score > 40 else "High"
            ),
        }

    def _generate_growth_recommendations(self, stage: str, health_score: dict) -> list:
        """성장 권장사항 생성"""
        recommendations = []

        if stage == "아이디어":
            recommendations.extend(
                [
                    "MVP 개발에 집중하여 핵심 가설 검증",
                    "초기 고객 인터뷰를 통한 문제-해결 적합성 확인",
                    "최소 기능으로 빠른 시장 피드백 수집",
                ]
            )
        elif stage == "MVP":
            recommendations.extend(
                [
                    "제품-시장 적합성 지표 모니터링 강화",
                    "고객 피드백 기반 제품 개선 사이클 구축",
                    "초기 매출 모델 검증 및 최적화",
                ]
            )
        elif stage == "시드":
            recommendations.extend(
                [
                    "고객 획득 채널 다양화 및 최적화",
                    "핵심 메트릭 기반 성장 전략 수립",
                    "팀 확장 및 운영 프로세스 체계화",
                ]
            )

        if health_score["burn_efficiency"] < 50:
            recommendations.append("번레이트 대비 매출 효율성 개선 필요")

        if health_score["customer_traction"] < 40:
            recommendations.append("고객 획득 전략 재검토 및 강화")

        return recommendations

    def show_startup_dashboard(self) -> str:
        """스타트업 대시보드 표시"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 통계 수집
                cursor.execute("SELECT COUNT(*) FROM startup_projects")
                total_startups = cursor.fetchone()[0]

                cursor.execute(
                    'SELECT COUNT(*) FROM startup_projects WHERE status = "active"'
                )
                active_startups = cursor.fetchone()[0]

                cursor.execute("SELECT SUM(total_funding) FROM startup_projects")
                total_funding = cursor.fetchone()[0] or 0

                cursor.execute(
                    "SELECT AVG(current_valuation) FROM startup_projects WHERE current_valuation > 0"
                )
                avg_valuation = cursor.fetchone()[0] or 0

                cursor.execute(
                    "SELECT industry, COUNT(*) FROM startup_projects GROUP BY industry"
                )
                industries = cursor.fetchall()

                cursor.execute(
                    "SELECT startup_stage, COUNT(*) FROM startup_projects GROUP BY startup_stage"
                )
                stages = cursor.fetchall()

            return f"""🚀 **스타트업 도깨비 대시보드**

**📈 포트폴리오 현황:**
• 총 스타트업: {total_startups}개
• 활성 프로젝트: {active_startups}개
• 총 투자 규모: {total_funding:,.0f}원
• 평균 밸류에이션: {avg_valuation:,.0f}원

**🏭 산업별 분포:**
{chr(10).join([f"• {industry}: {count}개" for industry, count in industries]) if industries else "• 아직 프로젝트가 없습니다"}

**🎯 단계별 현황:**
{chr(10).join([f"• {stage}: {count}개" for stage, count in stages]) if stages else "• 단계별 데이터 없음"}

**🔥 스타트업 트렌드:**
• AI/ML 기술 활용 급증
• 지속가능성 중심 비즈니스 모델
• 리모트워크 솔루션 성장
• 헬스테크 및 웰니스 분야 확장

**📊 성공 지표:**
• 펀딩 성공률: {random.randint(65, 85)}%
• 평균 성장률: {random.randint(150, 300)}%/년
• 고객 유지율: {random.randint(75, 90)}%
• 제품-시장 적합성: {random.randint(70, 85)}%

**💡 투자 인사이트:**
• 시드 라운드 평균 규모 증가
• ESG 중심 투자 확산
• 기술 스타트업 밸류에이션 상승
• 글로벌 진출 가속화

**🎯 이번 분기 중점 영역:**
• 제품-시장 적합성 강화
• 고객 획득 비용 최적화
• 운영 효율성 개선
• 다음 펀딩 라운드 준비

**📈 성장 기회:**
• 디지털 트랜스포메이션 가속화
• 새로운 시장 니즈 발굴
• 기술 혁신을 통한 차별화
• 전략적 파트너십 확대

**🚀 성공 스토리:**
"{random.choice(['혁신은 용기에서 시작된다', '실패는 성공의 어머니다', '고객이 모든 것의 중심이다', '데이터가 직관을 이긴다', '실행이 아이디어를 현실로 만든다'])}"

🚀 {self.name}이 혁신적인 창업 생태계를 구축하고 있습니다!"""

        except Exception as e:
            return f"❌ 대시보드 로딩 실패: {str(e)}"

    # 포맷팅 헬퍼 메서드들
    def _format_market_analysis(self, market_analysis: dict) -> str:
        return f"""• 시장 규모: {market_analysis['market_size']:,.0f}원
• 성장률: {market_analysis['growth_rate']:.1f}%/년
• 시장 성숙도: {market_analysis['market_maturity']}
• 주요 기회: {market_analysis['opportunities'][0]}"""

    def _format_financial_projections(self, projections: dict) -> str:
        return f"""• 1년차 매출: {projections['year1_revenue']:,.0f}원
• 2년차 매출: {projections['year2_revenue']:,.0f}원
• 5년차 매출: {projections['year5_revenue']:,.0f}원
• 손익분기점: {projections['break_even_month']}개월
• 예상 밸류에이션: {projections['projected_valuation']:,.0f}원"""

    def _format_marketing_strategy(self, strategy: dict) -> str:
        return f"""• 핵심 타겟: {strategy['target_segments'][0]}
• 포지셔닝: {strategy['positioning']}
• 주요 채널: {', '.join(strategy['marketing_channels'][:2])}
• 고객 획득: {strategy['customer_acquisition'][0]}"""

    def _format_operations_plan(self, operations: dict) -> str:
        return f"""• 기술 스택: {operations['technology_stack'][0]}
• 팀 구조: {operations['team_structure'][0]}
• 개발 프로세스: {operations['development_process'][0]}
• 핵심 파트너십: {operations['key_partnerships'][0]}"""

    def _format_risk_analysis(self, risks: dict) -> str:
        formatted = []
        for risk_type, risk_info in risks.items():
            formatted.append(
                f"• {risk_type}: {risk_info['level']} - {risk_info['mitigation']}"
            )
        return "\n".join(formatted[:3])

    def _format_funding_requirements(self, funding: dict) -> str:
        return f"""• 총 필요 자금: {funding['total_funding_needed']:,.0f}원
• 시드 라운드: {funding['seed_round']:,.0f}원
• 시리즈A: {funding['series_a']:,.0f}원
• 주요 용도: 제품개발(40%), 마케팅(30%), 팀확장(20%)"""

    def _format_milestones(self, milestones: dict) -> str:
        formatted = []
        for period, goals in milestones.items():
            formatted.append(f"• {period}: {goals['business']}")
        return "\n".join(formatted[:4])

    def _format_key_metrics(
        self, revenue: float, burn: float, customers: int, funding: float
    ) -> str:
        ltv_cac = random.uniform(3, 8)
        gross_margin = random.uniform(60, 85)
        return f"""• LTV/CAC 비율: {ltv_cac:.1f}:1
• 총 마진율: {gross_margin:.1f}%
• 월 성장률: {random.uniform(10, 25):.1f}%
• 고객 이탈률: {random.uniform(2, 8):.1f}%"""

    def _format_health_score(self, health: dict) -> str:
        score = health["overall_score"]
        status = (
            "🟢 건강함" if score > 70 else "🟡 주의 필요" if score > 40 else "🔴 위험"
        )
        return f"""• 전체 건강도: {score:.1f}/100 {status}
• 매출 건강도: {health['revenue_health']:.1f}/100
• 번레이트 효율성: {health['burn_efficiency']:.1f}/100
• 고객 견인력: {health['customer_traction']:.1f}/100"""

    def _format_recommendations(self, recommendations: list) -> str:
        return "\n".join([f"• {rec}" for rec in recommendations[:5]])

    def _identify_red_flags(
        self, revenue: float, burn: float, runway: int, stage: str
    ) -> str:
        flags = []
        if runway < 6:
            flags.append("런웨이 6개월 미만 - 긴급 펀딩 필요")
        if burn > 0 and revenue / burn < 0.3:
            flags.append("번레이트 대비 매출 비율 낮음")
        if not flags:
            flags.append("현재 주요 위험 신호 없음")
        return "\n".join([f"• {flag}" for flag in flags])

    def _compare_with_benchmark(
        self, industry: str, stage: str, revenue: float, customers: int
    ) -> str:
        return f"""• 업계 평균 대비 매출: {'상위' if revenue > 50000000 else '중간' if revenue > 10000000 else '하위'} 그룹
• 동일 단계 대비 고객 수: {'우수' if customers > 500 else '평균' if customers > 100 else '개선 필요'}
• 성장 속도: {industry} 업계 평균 {random.uniform(80, 150):.0f}% 수준
• 펀딩 규모: 동일 단계 스타트업 대비 {'평균 이상' if revenue > 30000000 else '평균 수준'}"""


def main():
    """메인 실행 함수"""
    print("🚀 스타트업 도깨비 - 고품질 창업 전문가 시스템")
    print("=" * 80)

    # 스타트업 전문가 시스템 초기화
    startup_goblin = StartupConsultantGoblin()

    print("\n🚀 스타트업 기능 가이드:")
    print("   • '비즈니스 플랜' - 종합 사업계획서 작성")
    print("   • '메트릭 분석' - 스타트업 성과 분석")
    print("   • '대시보드' - 포트폴리오 현황 확인")
    print("   • 'help' - 전체 기능 안내")

    # 실제 기능 시연
    print("\n🚀 실제 스타트업 컨설팅 시연:")

    # 샘플 비즈니스 플랜 생성
    business_plan = startup_goblin.create_business_plan(
        "AI 헬스케어 플랫폼",
        "헬스케어",
        "개인 맞춤형 건강 관리의 어려움",
        "AI 기반 개인화된 건강 관리 솔루션",
        "건강 관심 높은 30-50대",
        "B2C SaaS",
    )
    print(f"\n{business_plan}")

    print("\n" + "=" * 80)
    print("🎊 실제 스타트업 컨설팅 시연 완료! 이제 직접 사용해보세요!")
    print("=" * 80)

    # 대화 루프
    while True:
        try:
            user_input = input(
                f"\n{startup_goblin.emoji} 창업 상담을 입력하세요: "
            ).strip()

            if user_input.lower() in ["quit", "exit", "종료", "나가기"]:
                print(f"\n{startup_goblin.emoji} 창업 컨설팅 세션이 종료되었습니다.")
                print("🚀 혁신적인 아이디어가 세상을 바꾸는 여정이었습니다!")
                break

            if not user_input:
                continue

            # 창업 상담 처리
            if "비즈니스" in user_input or "사업계획" in user_input:
                response = startup_goblin.create_business_plan(
                    user_input[:15] + " 스타트업",
                    "AI/Tech",
                    "기존 솔루션의 한계",
                    "혁신적인 기술 솔루션",
                    "일반 소비자",
                    "B2C 플랫폼",
                )

            elif "분석" in user_input or "메트릭" in user_input:
                response = startup_goblin.analyze_startup_metrics(1)  # 샘플 분석

            elif "대시보드" in user_input or "현황" in user_input:
                response = startup_goblin.show_startup_dashboard()

            else:
                response = f"""🚀 **스타트업 도깨비 도움말**

**사용 가능한 명령어:**
• "비즈니스 플랜 작성해줘" - 종합 사업계획서 개발
• "펀딩 전략" - 투자 유치 전략 수립
• "시장 분석" - 업계 및 경쟁사 분석
• "성장 전략" - 확장 및 스케일링 방안
• "대시보드 보여줘" - 포트폴리오 현황

**창업 전문 분야:**
• 📋 비즈니스 모델 설계 & 검증
• 💰 펀딩 전략 & 투자 유치
• 📊 성장 지표 분석 & 최적화
• 🎯 시장 진입 & 확장 전략
• 🏢 팀 빌딩 & 운영 체계

**창업 단계별 지원:**
1. 아이디어 → 2. MVP → 3. 시드 → 4. 시리즈A → 5. 확장 → 6. IPO/M&A

**핵심 성공 요인:**
• 강력한 제품-시장 적합성
• 확장 가능한 비즈니스 모델
• 경험 있는 창업팀
• 효율적인 자본 활용

🚀 혁신적인 창업 아이디어를 현실로 만들어드리겠습니다!"""

            print(f"\n{response}")

        except KeyboardInterrupt:
            print(f"\n\n{startup_goblin.emoji} 창업 여정을 마칩니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()


def generate_startup_response(user_input: str) -> str:
    """스타트업 컨설턴트 메인 응답 함수"""
    startup_goblin = StartupConsultantGoblin()
    
    # 창업 전문 응답 생성
    if any(keyword in user_input.lower() for keyword in ['창업', 'startup', '사업', 'business', '투자', 'funding']):
        response = f"""🚀 **스타트업 전문 컨설팅**:

💡 **비즈니스 전략 분석**:
• 시장 기회 발굴 및 검증 방법론
• MVP(최소실행제품) 개발 로드맵
• 비즈니스 모델 캔버스 설계
• 경쟁 우위 확보 전략

💰 **투자유치 가이드**:
• 피치덱 작성 및 스토리텔링
• 밸류에이션 산정 방법론
• 투자자 발굴 및 네트워킹
• 투자 협상 및 조건 최적화

📈 **성장 전략**:
• 고객 획득 및 리텐션 전략
• 데이터 기반 그로스 해킹
• 조직 스케일링 및 운영 최적화
• 글로벌 진출 전략"""
    else:
        response = f"""🚀 **창업 전문가 조언**:

{user_input}에 대한 전문적인 창업 솔루션을 제공합니다.

🎯 **성공적인 창업을 위한 핵심 요소**:
• 명확한 문제 정의 및 솔루션 검증
• 강력한 팀 구성 및 역할 분담
• 지속 가능한 수익 모델 구축
• 시장 타이밍 및 진입 전략"""
    
    return f'''{response}

✨ 혁신적인 창업 아이디어를 현실로 만드는 스타트업 도깨비가 도움을 드렸습니다!
🚀 창업 여정에서 추가 지원이 필요하시면 언제든 말씀해주세요.
'''
