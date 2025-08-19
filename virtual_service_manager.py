"""
HYOJIN.AI 가상 서비스 링크 생성기
결제 완료 후 고객에게 제공할 AI 서비스 접속 링크 생성
"""

import uuid
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sqlite3


class VirtualServiceManager:
    """가상 AI 서비스 관리자"""

    def __init__(self):
        self.init_database()

        # AI 서비스별 가상 링크 템플릿 - 15명의 도깨비 에이전트들
        self.service_templates = {
            "medical-dokkaebi": {
                "name": "⚕️ 의료 도깨비",
                "base_url": "https://agents.hyojin.ai/medical-dokkaebi",
                "features": ["76기능 의료 분석", "3000질병 예측", "진단 보조", "치료 계획"],
                "demo_data": "medical_dokkaebi_demo.json",
            },
            "analyst-dokkaebi": {
                "name": "📊 애널리스트 도깨비",
                "base_url": "https://agents.hyojin.ai/analyst-dokkaebi",
                "features": ["데이터 분석", "비즈니스 인텔리전스", "시장 조사", "예측 모델링"],
                "demo_data": "analyst_dokkaebi_demo.json",
            },
            "writer-dokkaebi": {
                "name": "📚 작가 도깨비",
                "base_url": "https://agents.hyojin.ai/writer-dokkaebi",
                "features": ["창작 스토리 작성", "소설 플롯 구성", "캐릭터 개발", "콘텐츠 기획"],
                "demo_data": "writer_dokkaebi_demo.json",
            },
            "design-dokkaebi": {
                "name": "🎨 디자인 도깨비",
                "base_url": "https://agents.hyojin.ai/design-dokkaebi",
                "features": ["UI/UX 디자인", "브랜딩", "그래픽 디자인", "프로토타이핑"],
                "demo_data": "design_dokkaebi_demo.json",
            },
            "developer-dokkaebi": {
                "name": "💻 개발자 도깨비",
                "base_url": "https://agents.hyojin.ai/developer-dokkaebi",
                "features": ["풀스택 개발", "AI 모델 구현", "시스템 아키텍처", "코드 리뷰"],
                "demo_data": "developer_dokkaebi_demo.json",
            },
            "finance-dokkaebi": {
                "name": "💰 금융 도깨비",
                "base_url": "https://agents.hyojin.ai/finance-dokkaebi",
                "features": ["투자 분석", "리스크 관리", "재무 계획", "포트폴리오 최적화"],
                "demo_data": "finance_dokkaebi_demo.json",
            },
            "marketing-dokkaebi": {
                "name": "📢 마케팅 도깨비",
                "base_url": "https://agents.hyojin.ai/marketing-dokkaebi",
                "features": ["디지털 마케팅", "SNS 전략", "브랜드 관리", "광고 캠페인"],
                "demo_data": "marketing_dokkaebi_demo.json",
            },
            "education-dokkaebi": {
                "name": "🎓 교육 도깨비",
                "base_url": "https://agents.hyojin.ai/education-dokkaebi",
                "features": ["맞춤형 학습", "교육 콘텐츠 제작", "학습 평가", "진로 상담"],
                "demo_data": "education_dokkaebi_demo.json",
            },
            "legal-dokkaebi": {
                "name": "⚖️ 법무 도깨비",
                "base_url": "https://agents.hyojin.ai/legal-dokkaebi",
                "features": ["법률 자문", "계약서 검토", "규정 준수", "소송 지원"],
                "demo_data": "legal_dokkaebi_demo.json",
            },
            "hr-dokkaebi": {
                "name": "� 인사 도깨비",
                "base_url": "https://agents.hyojin.ai/hr-dokkaebi",
                "features": ["인재 채용", "성과 관리", "교육 프로그램", "조직 문화"],
                "demo_data": "hr_dokkaebi_demo.json",
            },
            "sales-dokkaebi": {
                "name": "🤝 영업 도깨비",
                "base_url": "https://agents.hyojin.ai/sales-dokkaebi",
                "features": ["영업 전략", "고객 관리", "제안서 작성", "협상 지원"],
                "demo_data": "sales_dokkaebi_demo.json",
            },
            "research-dokkaebi": {
                "name": "� 연구 도깨비",
                "base_url": "https://agents.hyojin.ai/research-dokkaebi",
                "features": ["학술 연구", "논문 분석", "실험 설계", "연구 방법론"],
                "demo_data": "research_dokkaebi_demo.json",
            },
            "translator-dokkaebi": {
                "name": "🌍 번역 도깨비",
                "base_url": "https://agents.hyojin.ai/translator-dokkaebi",
                "features": ["다국어 번역", "문서 현지화", "언어 교정", "문화적 적응"],
                "demo_data": "translator_dokkaebi_demo.json",
            },
            "consultant-dokkaebi": {
                "name": "💡 컨설턴트 도깨비",
                "base_url": "https://agents.hyojin.ai/consultant-dokkaebi",
                "features": ["경영 컨설팅", "전략 기획", "프로세스 개선", "변화 관리"],
                "demo_data": "consultant_dokkaebi_demo.json",
            },
            "creative-dokkaebi": {
                "name": "🎭 크리에이티브 도깨비",
                "base_url": "https://agents.hyojin.ai/creative-dokkaebi",
                "features": ["아이디어 발굴", "콘텐츠 기획", "크리에이티브 전략", "브레인스토밍"],
                "demo_data": "creative_dokkaebi_demo.json",
            },
        }

    def init_database(self):
        """가상 서비스 링크 데이터베이스 초기화"""
        conn = sqlite3.connect("hyojin_payments.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS service_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_id TEXT NOT NULL,
                service_id TEXT NOT NULL,
                service_name TEXT NOT NULL,
                access_token TEXT UNIQUE NOT NULL,
                service_url TEXT NOT NULL,
                demo_url TEXT NOT NULL,
                features TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )
        """
        )

        conn.commit()
        conn.close()

    def generate_service_links(
        self, subscription_id: str, items: List[Dict]
    ) -> List[Dict[str, Any]]:
        """구독 상품들에 대한 가상 서비스 링크 생성"""
        service_links = []

        for item in items:
            service_id = item["id"]
            if service_id in self.service_templates:
                template = self.service_templates[service_id]

                # 고유한 접속 토큰 생성
                access_token = self.generate_access_token(subscription_id, service_id)

                # 가상 서비스 URL 생성
                service_url = f"{template['base_url']}/access?token={access_token}"
                demo_url = (
                    f"http://localhost:8000/demo/{service_id}?token={access_token}"
                )

                # 만료일 설정 (30일 후)
                expires_at = (datetime.now() + timedelta(days=30)).isoformat()

                service_link = {
                    "subscription_id": subscription_id,
                    "service_id": service_id,
                    "service_name": template["name"],
                    "access_token": access_token,
                    "service_url": service_url,
                    "demo_url": demo_url,
                    "features": template["features"],
                    "expires_at": expires_at,
                    "status": "active",
                }

                # 데이터베이스에 저장
                self.save_service_link(service_link)
                service_links.append(service_link)

        return service_links

    def generate_access_token(self, subscription_id: str, service_id: str) -> str:
        """접속 토큰 생성"""
        # 구독ID + 서비스ID + 현재시간으로 고유 토큰 생성
        raw_data = f"{subscription_id}_{service_id}_{datetime.now().isoformat()}"
        token_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:32]
        return f"hyojin_{token_hash}"

    def save_service_link(self, service_link: Dict[str, Any]):
        """서비스 링크를 데이터베이스에 저장"""
        conn = sqlite3.connect("hyojin_payments.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO service_links 
            (subscription_id, service_id, service_name, access_token, 
             service_url, demo_url, features, created_at, expires_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                service_link["subscription_id"],
                service_link["service_id"],
                service_link["service_name"],
                service_link["access_token"],
                service_link["service_url"],
                service_link["demo_url"],
                json.dumps(service_link["features"]),
                datetime.now().isoformat(),
                service_link["expires_at"],
                1,
            ),
        )

        conn.commit()
        conn.close()

    def get_service_links_by_subscription(
        self, subscription_id: str
    ) -> List[Dict[str, Any]]:
        """구독 ID로 서비스 링크 조회"""
        conn = sqlite3.connect("hyojin_payments.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM service_links 
            WHERE subscription_id = ? AND is_active = 1
            ORDER BY created_at DESC
        """,
            (subscription_id,),
        )

        links = []
        for row in cursor.fetchall():
            link = {
                "id": row[0],
                "subscription_id": row[1],
                "service_id": row[2],
                "service_name": row[3],
                "access_token": row[4],
                "service_url": row[5],
                "demo_url": row[6],
                "features": json.loads(row[7]),
                "created_at": row[8],
                "expires_at": row[9],
                "is_active": row[10],
            }
            links.append(link)

        conn.close()
        return links

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """접속 토큰 검증"""
        conn = sqlite3.connect("hyojin_payments.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM service_links 
            WHERE access_token = ? AND is_active = 1
        """,
            (token,),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            # 만료일 확인
            expires_at = datetime.fromisoformat(row[9])
            if expires_at > datetime.now():
                return {
                    "valid": True,
                    "subscription_id": row[1],
                    "service_id": row[2],
                    "service_name": row[3],
                    "features": json.loads(row[7]),
                    "expires_at": row[9],
                }
            else:
                return {"valid": False, "error": "토큰이 만료되었습니다."}

        return {"valid": False, "error": "유효하지 않은 토큰입니다."}


# 서비스 매니저 인스턴스
virtual_service_manager = VirtualServiceManager()
