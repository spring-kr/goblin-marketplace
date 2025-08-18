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

        # AI 서비스별 가상 링크 템플릿
        self.service_templates = {
            # AI 도메인들
            "medical-ai": {
                "name": "의료 AI 도메인",
                "base_url": "https://medical.hyojin.ai",
                "features": [
                    "진단 보조",
                    "의료 영상 분석",
                    "환자 데이터 관리",
                    "치료 계획",
                ],
                "demo_data": "medical_demo.json",
            },
            "finance-ai": {
                "name": "금융 AI 도메인",
                "base_url": "https://finance.hyojin.ai",
                "features": ["투자 분석", "리스크 관리", "사기 탐지", "신용 평가"],
                "demo_data": "finance_demo.json",
            },
            "education-ai": {
                "name": "교육 AI 도메인",
                "base_url": "https://education.hyojin.ai",
                "features": ["맞춤형 학습", "자동 채점", "콘텐츠 생성", "학습 분석"],
                "demo_data": "education_demo.json",
            },
            # AI 에이전트들
            "medical-doctor-ai": {
                "name": "닥터 김 AI",
                "base_url": "https://agents.hyojin.ai/doctor-kim",
                "features": ["증상 분석", "진단 보조", "치료 추천", "의료 상담"],
                "demo_data": "doctor_kim_demo.json",
            },
            "finance-analyst-ai": {
                "name": "애널리스트 박 AI",
                "base_url": "https://agents.hyojin.ai/analyst-park",
                "features": [
                    "투자 분석",
                    "포트폴리오 관리",
                    "리스크 평가",
                    "시장 예측",
                ],
                "demo_data": "analyst_park_demo.json",
            },
            # 번들 패키지들
            "starter-bundle": {
                "name": "스타터 번들",
                "base_url": "https://suite.hyojin.ai/starter",
                "features": [
                    "의료+금융+교육 AI",
                    "핵심 에이전트 5명",
                    "24/7 지원",
                    "월간 리포트",
                ],
                "demo_data": "starter_bundle_demo.json",
            },
            "business-bundle": {
                "name": "비즈니스 번들",
                "base_url": "https://suite.hyojin.ai/business",
                "features": [
                    "주요 AI 도메인 8개",
                    "전문 에이전트 10명",
                    "우선 지원",
                    "커스텀 기능",
                ],
                "demo_data": "business_bundle_demo.json",
            },
            "enterprise-bundle": {
                "name": "엔터프라이즈 번들",
                "base_url": "https://suite.hyojin.ai/enterprise",
                "features": [
                    "전체 AI 도메인",
                    "모든 에이전트",
                    "전담 지원",
                    "무제한 커스터마이징",
                ],
                "demo_data": "enterprise_bundle_demo.json",
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
