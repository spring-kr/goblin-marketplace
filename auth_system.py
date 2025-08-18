"""
토큰 기반 인증 시스템
사용자가 서비스에 접근할 때 토큰을 검증하고 권한을 확인합니다.
"""

import hashlib
import jwt
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import sqlite3
import os


class AuthenticationSystem:
    def __init__(self, db_path: str = "payment_manager.db"):
        self.db_path = db_path
        self.secret_key = "hyojin-ai-secret-key-2024"  # 실제 운영에서는 환경변수로 관리
        self.init_auth_tables()

    def init_auth_tables(self):
        """인증 관련 테이블 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 세션 테이블 생성
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                token TEXT NOT NULL,
                service_id TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """
        )

        # 서비스 접근 로그 테이블
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                service_id TEXT NOT NULL,
                token TEXT NOT NULL,
                access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT DEFAULT 'success'
            )
        """
        )

        conn.commit()
        conn.close()

    def validate_token(self, token: str, service_id: str) -> Dict[str, Any]:
        """
        토큰 유효성 검증 및 서비스 접근 권한 확인
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 서비스 링크에서 토큰 정보 조회
            cursor.execute(
                """
                SELECT subscription_id, service_name, expires_at, is_active 
                FROM service_links 
                WHERE access_token = ? AND service_id = ?
            """,
                (token, service_id),
            )

            result = cursor.fetchone()

            if not result:
                return {
                    "valid": False,
                    "error": "invalid_token",
                    "message": "유효하지 않은 토큰입니다.",
                }

            subscription_id, service_name, expires_at, is_active = result

            # 활성 상태 확인
            if not is_active:
                return {
                    "valid": False,
                    "error": "token_deactivated",
                    "message": "비활성화된 토큰입니다.",
                }

            # 만료 시간 확인
            expiry_time = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if datetime.now() > expiry_time:
                return {
                    "valid": False,
                    "error": "token_expired",
                    "message": "만료된 토큰입니다.",
                }

            # 유효한 토큰인 경우 세션 생성
            session_id = self.create_session(subscription_id, token, service_id)

            return {
                "valid": True,
                "user_id": subscription_id,
                "service_name": service_name,
                "session_id": session_id,
                "expires_at": expires_at,
                "message": "인증 성공",
            }

        except Exception as e:
            return {
                "valid": False,
                "error": "validation_error",
                "message": f"토큰 검증 중 오류: {str(e)}",
            }
        finally:
            conn.close()

    def create_session(self, user_id: str, token: str, service_id: str) -> str:
        """사용자 세션 생성"""
        session_id = hashlib.sha256(
            f"{user_id}_{token}_{time.time()}".encode()
        ).hexdigest()
        expires_at = datetime.now() + timedelta(hours=24)  # 24시간 세션

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 기존 세션 비활성화
        cursor.execute(
            """
            UPDATE user_sessions 
            SET is_active = FALSE 
            WHERE user_id = ? AND service_id = ?
        """,
            (user_id, service_id),
        )

        # 새 세션 생성
        cursor.execute(
            """
            INSERT INTO user_sessions 
            (session_id, user_id, token, service_id, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """,
            (session_id, user_id, token, service_id, expires_at),
        )

        conn.commit()
        conn.close()

        return session_id

    def validate_session(self, session_id: str) -> Dict[str, Any]:
        """세션 유효성 검증"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT user_id, service_id, expires_at, is_active 
                FROM user_sessions 
                WHERE session_id = ?
            """,
                (session_id,),
            )

            result = cursor.fetchone()

            if not result:
                return {"valid": False, "error": "session_not_found"}

            user_id, service_id, expires_at, is_active = result

            if not is_active:
                return {"valid": False, "error": "session_inactive"}

            # 세션 만료 확인
            expiry_time = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if datetime.now() > expiry_time:
                # 만료된 세션 비활성화
                cursor.execute(
                    """
                    UPDATE user_sessions 
                    SET is_active = FALSE 
                    WHERE session_id = ?
                """,
                    (session_id,),
                )
                conn.commit()
                return {"valid": False, "error": "session_expired"}

            # 마지막 접근 시간 업데이트
            cursor.execute(
                """
                UPDATE user_sessions 
                SET last_accessed = CURRENT_TIMESTAMP 
                WHERE session_id = ?
            """,
                (session_id,),
            )
            conn.commit()

            return {"valid": True, "user_id": user_id, "service_id": service_id}

        except Exception as e:
            return {"valid": False, "error": str(e)}
        finally:
            conn.close()

    def log_access(
        self,
        user_id: str,
        service_id: str,
        token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
    ):
        """서비스 접근 로그 기록"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO access_logs 
            (user_id, service_id, token, ip_address, user_agent, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (user_id, service_id, token, ip_address, user_agent, status),
        )

        conn.commit()
        conn.close()

    def revoke_token(self, token: str) -> bool:
        """토큰 폐기"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 토큰 비활성화
            cursor.execute(
                """
                UPDATE service_links 
                SET is_active = FALSE 
                WHERE access_token = ?
            """,
                (token,),
            )

            # 관련 세션 비활성화
            cursor.execute(
                """
                UPDATE user_sessions 
                SET is_active = FALSE 
                WHERE token = ?
            """,
                (token,),
            )

            conn.commit()
            return True

        except Exception as e:
            print(f"토큰 폐기 오류: {e}")
            return False
        finally:
            conn.close()

    def get_user_sessions(self, user_id: str) -> list:
        """사용자의 활성 세션 목록 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT session_id, service_id, created_at, last_accessed, expires_at
            FROM user_sessions 
            WHERE user_id = ? AND is_active = TRUE
            ORDER BY last_accessed DESC
        """,
            (user_id,),
        )

        sessions = []
        for row in cursor.fetchall():
            sessions.append(
                {
                    "session_id": row[0],
                    "service_id": row[1],
                    "created_at": row[2],
                    "last_accessed": row[3],
                    "expires_at": row[4],
                }
            )

        conn.close()
        return sessions


# 전역 인증 시스템 인스턴스
auth_system = AuthenticationSystem()
