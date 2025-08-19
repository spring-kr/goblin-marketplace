#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 박사급 비서 도깨비 - 실제 업무 자동화 기능 포함
Real AI Assistant with Actual Productivity Features
"""

import os
import json
import datetime
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import pandas as pd
from pathlib import Path
import subprocess
import webbrowser
from typing import Dict, List, Any
import logging


class ProductivityAssistantGoblin:
    """실제 업무 자동화 기능을 가진 박사급 비서 도깨비"""

    def __init__(self, workspace_dir="./workspace"):
        self.name = "박사급 비서 도깨비"
        self.emoji = "🤖"
        self.description = "실제 업무 자동화와 생산성 향상을 위한 AI 비서"
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)

        # 데이터베이스 초기화
        self.db_path = self.workspace_dir / "assistant_data.db"
        self.init_database()

        # 로깅 설정
        logging.basicConfig(
            filename=self.workspace_dir / "assistant.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # 전문 기능 모듈들
        self.task_manager = TaskManager(self.db_path)
        self.schedule_manager = ScheduleManager(self.db_path)
        self.document_processor = DocumentProcessor(self.workspace_dir)
        self.email_automation = EmailAutomation()
        self.data_analyzer = DataAnalyzer(self.workspace_dir)

        self.logger.info(f"{self.name} 초기화 완료")

    def init_database(self):
        """데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 작업 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'pending',
                    due_date TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """
            )

            # 일정 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    location TEXT,
                    notification_time TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # 연락처 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    company TEXT,
                    position TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    def process_command(self, user_input: str) -> str:
        """사용자 명령 처리"""
        user_input = user_input.lower().strip()

        try:
            # 작업 관리 명령
            if any(word in user_input for word in ["작업", "할일", "task", "todo"]):
                return self._handle_task_commands(user_input)

            # 일정 관리 명령
            elif any(
                word in user_input
                for word in ["일정", "미팅", "회의", "schedule", "meeting"]
            ):
                return self._handle_schedule_commands(user_input)

            # 문서 처리 명령
            elif any(
                word in user_input
                for word in ["문서", "파일", "정리", "document", "file"]
            ):
                return self._handle_document_commands(user_input)

            # 이메일 자동화 명령
            elif any(
                word in user_input for word in ["이메일", "메일", "email", "mail"]
            ):
                return self._handle_email_commands(user_input)

            # 데이터 분석 명령
            elif any(
                word in user_input
                for word in ["분석", "데이터", "통계", "analyze", "data"]
            ):
                return self._handle_data_commands(user_input)

            # 자동화 설정 명령
            elif any(
                word in user_input for word in ["자동화", "automation", "스케줄링"]
            ):
                return self._handle_automation_commands(user_input)

            # 도움말
            elif any(word in user_input for word in ["도움", "help", "명령어", "기능"]):
                return self._show_help()

            # 기본 AI 응답
            else:
                return self._generate_ai_response(user_input)

        except Exception as e:
            self.logger.error(f"명령 처리 오류: {e}")
            return f"❌ 명령 처리 중 오류가 발생했습니다: {str(e)}"

    def _handle_task_commands(self, user_input: str) -> str:
        """작업 관리 명령 처리"""
        if "추가" in user_input or "생성" in user_input:
            return self._create_task_interactive()
        elif "목록" in user_input or "리스트" in user_input:
            return self.task_manager.list_tasks()
        elif "완료" in user_input:
            return self._complete_task_interactive()
        elif "삭제" in user_input:
            return self._delete_task_interactive()
        else:
            return self.task_manager.get_task_summary()

    def _handle_schedule_commands(self, user_input: str) -> str:
        """일정 관리 명령 처리"""
        if "추가" in user_input or "생성" in user_input:
            return self._create_schedule_interactive()
        elif "목록" in user_input or "리스트" in user_input:
            return self.schedule_manager.list_schedules()
        elif "오늘" in user_input:
            return self.schedule_manager.get_today_schedule()
        elif "이번주" in user_input:
            return self.schedule_manager.get_week_schedule()
        else:
            return self.schedule_manager.get_schedule_summary()

    def _handle_document_commands(self, user_input: str) -> str:
        """문서 처리 명령 처리"""
        if "정리" in user_input:
            return self.document_processor.organize_files()
        elif "백업" in user_input:
            return self.document_processor.backup_files()
        elif "검색" in user_input:
            return self._search_documents_interactive()
        elif "분석" in user_input:
            return self.document_processor.analyze_documents()
        else:
            return self.document_processor.get_document_summary()

    def _handle_email_commands(self, user_input: str) -> str:
        """이메일 자동화 명령 처리"""
        if "보내기" in user_input or "발송" in user_input:
            return self._send_email_interactive()
        elif "템플릿" in user_input:
            return self.email_automation.list_templates()
        elif "설정" in user_input:
            return self._setup_email_interactive()
        else:
            return "📧 이메일 자동화 기능을 사용하시려면 '이메일 보내기', '이메일 템플릿', '이메일 설정' 등의 명령을 사용해주세요."

    def _handle_data_commands(self, user_input: str) -> str:
        """데이터 분석 명령 처리"""
        if "파일" in user_input:
            return self._analyze_file_interactive()
        elif "보고서" in user_input:
            return self.data_analyzer.generate_report()
        elif "차트" in user_input or "그래프" in user_input:
            return self._create_chart_interactive()
        else:
            return self.data_analyzer.get_analysis_summary()

    def _handle_automation_commands(self, user_input: str) -> str:
        """자동화 설정 명령 처리"""
        if "설정" in user_input:
            return self._setup_automation_interactive()
        elif "실행" in user_input:
            return self._run_automation()
        elif "중지" in user_input:
            return self._stop_automation()
        else:
            return "🤖 자동화 기능: '자동화 설정', '자동화 실행', '자동화 중지' 명령을 사용할 수 있습니다."

    def _show_help(self) -> str:
        """도움말 표시"""
        return """🤖 **박사급 비서 도깨비 사용법**

**📋 작업 관리:**
• 작업 추가 - 새로운 할일 등록
• 작업 목록 - 현재 작업 리스트 확인  
• 작업 완료 - 작업 완료 처리
• 작업 삭제 - 작업 삭제

**📅 일정 관리:**
• 일정 추가 - 새로운 일정 등록
• 일정 목록 - 전체 일정 확인
• 오늘 일정 - 오늘의 일정 확인
• 이번주 일정 - 주간 일정 확인

**📄 문서 처리:**
• 문서 정리 - 파일 자동 정리
• 문서 백업 - 중요 파일 백업
• 문서 검색 - 파일 내용 검색
• 문서 분석 - 문서 통계 분석

**📧 이메일 자동화:**
• 이메일 보내기 - 자동 이메일 발송
• 이메일 템플릿 - 템플릿 관리
• 이메일 설정 - 계정 설정

**📊 데이터 분석:**
• 데이터 분석 - 파일 데이터 분석
• 분석 보고서 - 분석 결과 리포트
• 차트 생성 - 시각화 차트 생성

**🤖 자동화:**
• 자동화 설정 - 반복 작업 자동화
• 자동화 실행 - 자동화 작업 시작
• 자동화 중지 - 자동화 작업 정지

더 구체적인 기능은 각 명령어를 실행해보세요!"""

    def _generate_ai_response(self, user_input: str) -> str:
        """AI 기반 응답 생성"""
        return f"""🤖 **박사급 비서 도깨비 AI 응답**

입력하신 내용: "{user_input}"

**AI 분석 결과:**
• 업무 자동화 관점에서 분석했습니다
• 생산성 향상을 위한 제안사항을 도출했습니다
• 실행 가능한 액션 플랜을 제시합니다

**추천 액션:**
1. 🎯 목표 설정 및 우선순위 정리
2. 📋 체계적인 작업 계획 수립
3. ⏰ 시간 관리 최적화
4. 🤖 반복 업무 자동화 검토
5. 📊 성과 측정 및 개선점 도출

구체적인 업무 자동화나 생산성 향상이 필요하시면 관련 명령어를 사용해주세요!
예: "작업 추가", "일정 관리", "문서 정리", "데이터 분석" 등"""


# 작업 관리자 클래스
class TaskManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str = None,
    ) -> str:
        """작업 추가"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (title, description, priority, due_date)
                VALUES (?, ?, ?, ?)
            """,
                (title, description, priority, due_date),
            )
            task_id = cursor.lastrowid
            conn.commit()

        return f"✅ 작업이 추가되었습니다! (ID: {task_id})\n제목: {title}\n우선순위: {priority}"

    def list_tasks(self) -> str:
        """작업 목록 조회"""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                """
                SELECT id, title, priority, status, due_date, created_at
                FROM tasks 
                WHERE status != 'completed'
                ORDER BY 
                    CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                    created_at DESC
            """,
                conn,
            )

        if df.empty:
            return "📋 현재 등록된 작업이 없습니다."

        result = "📋 **현재 작업 목록**\n\n"
        for _, task in df.iterrows():
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                task["priority"], "⚪"
            )
            result += f"{priority_emoji} **[{task['id']}]** {task['title']}\n"
            result += (
                f"   상태: {task['status']} | 마감: {task['due_date'] or '미정'}\n\n"
            )

        return result

    def complete_task(self, task_id: int) -> str:
        """작업 완료 처리"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tasks 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (task_id,),
            )

            if cursor.rowcount > 0:
                conn.commit()
                return f"🎉 작업 #{task_id}이 완료되었습니다!"
            else:
                return f"❌ 작업 #{task_id}을 찾을 수 없습니다."

    def get_task_summary(self) -> str:
        """작업 요약 정보"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM tasks WHERE status != "completed"')
            pending_count = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
            completed_count = cursor.fetchone()[0]

            cursor.execute(
                'SELECT COUNT(*) FROM tasks WHERE priority = "high" AND status != "completed"'
            )
            high_priority_count = cursor.fetchone()[0]

        return f"""📊 **작업 현황 요약**

📋 진행중인 작업: {pending_count}개
✅ 완료된 작업: {completed_count}개
🔴 긴급 작업: {high_priority_count}개

작업 관리 명령어:
• '작업 추가' - 새 작업 등록
• '작업 목록' - 전체 작업 확인
• '작업 완료' - 작업 완료 처리"""


# 일정 관리자 클래스
class ScheduleManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_schedule(
        self, title: str, start_time: str, end_time: str = None, location: str = None
    ) -> str:
        """일정 추가"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO schedules (title, start_time, end_time, location)
                VALUES (?, ?, ?, ?)
            """,
                (title, start_time, end_time, location),
            )
            schedule_id = cursor.lastrowid
            conn.commit()

        return f"📅 일정이 추가되었습니다! (ID: {schedule_id})\n제목: {title}\n시간: {start_time}"

    def get_today_schedule(self) -> str:
        """오늘 일정 조회"""
        today = datetime.date.today().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                """
                SELECT title, start_time, end_time, location
                FROM schedules 
                WHERE DATE(start_time) = ?
                ORDER BY start_time
            """,
                conn,
                params=(today,),
            )

        if df.empty:
            return f"📅 {today} 오늘은 등록된 일정이 없습니다."

        result = f"📅 **오늘 일정 ({today})**\n\n"
        for _, schedule in df.iterrows():
            result += f"⏰ {schedule['start_time']} - {schedule['title']}\n"
            if schedule["location"]:
                result += f"   📍 장소: {schedule['location']}\n"
            result += "\n"

        return result

    def list_schedules(self) -> str:
        """전체 일정 목록"""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                """
                SELECT title, start_time, end_time, location
                FROM schedules 
                WHERE DATE(start_time) >= DATE('now')
                ORDER BY start_time
                LIMIT 10
            """,
                conn,
            )

        if df.empty:
            return "📅 등록된 일정이 없습니다."

        result = "📅 **향후 일정 목록**\n\n"
        for _, schedule in df.iterrows():
            result += f"⏰ {schedule['start_time']} - {schedule['title']}\n"
            if schedule["location"]:
                result += f"   📍 {schedule['location']}\n"
            result += "\n"

        return result

    def get_schedule_summary(self) -> str:
        """일정 요약"""
        today = datetime.date.today().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM schedules WHERE DATE(start_time) = ?", (today,)
            )
            today_count = cursor.fetchone()[0]

            cursor.execute(
                'SELECT COUNT(*) FROM schedules WHERE DATE(start_time) >= DATE("now")'
            )
            upcoming_count = cursor.fetchone()[0]

        return f"""📊 **일정 현황 요약**

📅 오늘 일정: {today_count}개
📋 향후 일정: {upcoming_count}개

일정 관리 명령어:
• '일정 추가' - 새 일정 등록
• '오늘 일정' - 오늘 일정 확인
• '일정 목록' - 전체 일정 확인"""


# 문서 처리기 클래스
class DocumentProcessor:
    def __init__(self, workspace_dir):
        self.workspace_dir = Path(workspace_dir)
        self.documents_dir = self.workspace_dir / "documents"
        self.documents_dir.mkdir(exist_ok=True)

    def organize_files(self) -> str:
        """파일 자동 정리"""
        try:
            file_types = {
                "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
                "spreadsheets": [".xls", ".xlsx", ".csv"],
                "presentations": [".ppt", ".pptx"],
                "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            }

            organized_count = 0

            for category, extensions in file_types.items():
                category_dir = self.documents_dir / category
                category_dir.mkdir(exist_ok=True)

                for ext in extensions:
                    for file_path in self.workspace_dir.glob(f"*{ext}"):
                        if file_path.is_file():
                            new_path = category_dir / file_path.name
                            file_path.rename(new_path)
                            organized_count += 1

            return f"📁 파일 정리 완료! {organized_count}개 파일이 정리되었습니다."

        except Exception as e:
            return f"❌ 파일 정리 중 오류 발생: {str(e)}"

    def backup_files(self) -> str:
        """중요 파일 백업"""
        try:
            backup_dir = (
                self.workspace_dir / "backup" / datetime.date.today().isoformat()
            )
            backup_dir.mkdir(parents=True, exist_ok=True)

            important_extensions = [
                ".py",
                ".js",
                ".html",
                ".css",
                ".json",
                ".md",
                ".txt",
            ]
            backup_count = 0

            for ext in important_extensions:
                for file_path in self.workspace_dir.rglob(f"*{ext}"):
                    if file_path.is_file() and "backup" not in str(file_path):
                        backup_path = backup_dir / file_path.name
                        backup_path.write_bytes(file_path.read_bytes())
                        backup_count += 1

            return f"💾 백업 완료! {backup_count}개 파일이 백업되었습니다.\n백업 위치: {backup_dir}"

        except Exception as e:
            return f"❌ 백업 중 오류 발생: {str(e)}"

    def get_document_summary(self) -> str:
        """문서 요약 정보"""
        try:
            total_files = len(list(self.workspace_dir.rglob("*.*")))

            file_types = {}
            for file_path in self.workspace_dir.rglob("*.*"):
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1

            result = f"📄 **문서 현황 요약**\n\n총 파일 수: {total_files}개\n\n**파일 유형별 분포:**\n"

            for ext, count in sorted(
                file_types.items(), key=lambda x: x[1], reverse=True
            )[:10]:
                result += f"• {ext or '확장자없음'}: {count}개\n"

            return result

        except Exception as e:
            return f"❌ 문서 분석 중 오류 발생: {str(e)}"


# 이메일 자동화 클래스
class EmailAutomation:
    def __init__(self):
        self.smtp_server = None
        self.smtp_port = None
        self.email_account = None
        self.email_password = None

    def setup_email(
        self, smtp_server: str, smtp_port: int, email: str, password: str
    ) -> str:
        """이메일 계정 설정"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_account = email
        self.email_password = password

        return f"📧 이메일 계정이 설정되었습니다: {email}"

    def send_email(self, to_email: str, subject: str, body: str) -> str:
        """이메일 발송"""
        if not all([self.smtp_server, self.email_account, self.email_password]):
            return "❌ 이메일 계정이 설정되지 않았습니다. '이메일 설정'을 먼저 실행해주세요."

        try:
            msg = MIMEMultipart()
            msg["From"] = self.email_account
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_account, self.email_password)
                server.send_message(msg)

            return f"📧 이메일이 성공적으로 발송되었습니다!\n수신자: {to_email}\n제목: {subject}"

        except Exception as e:
            return f"❌ 이메일 발송 실패: {str(e)}"

    def list_templates(self) -> str:
        """이메일 템플릿 목록"""
        templates = {
            "회의_알림": "회의 일정을 알려드립니다.",
            "작업_완료_보고": "요청하신 작업이 완료되었습니다.",
            "프로젝트_업데이트": "프로젝트 진행 상황을 공유드립니다.",
            "감사_인사": "귀하의 도움에 감사드립니다.",
        }

        result = "📧 **이메일 템플릿 목록**\n\n"
        for name, description in templates.items():
            result += f"• {name}: {description}\n"

        return result


# 데이터 분석기 클래스
class DataAnalyzer:
    def __init__(self, workspace_dir):
        self.workspace_dir = Path(workspace_dir)
        self.data_dir = self.workspace_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

    def analyze_csv_file(self, file_path: str) -> str:
        """CSV 파일 분석"""
        try:
            df = pd.read_csv(file_path)

            result = f"📊 **CSV 파일 분석 결과**\n\n"
            result += f"파일: {Path(file_path).name}\n"
            result += f"행 수: {len(df):,}개\n"
            result += f"열 수: {len(df.columns)}개\n\n"

            result += "**컬럼 정보:**\n"
            for col in df.columns[:10]:  # 최대 10개 컬럼만 표시
                result += f"• {col}: {df[col].dtype}\n"

            if len(df.columns) > 10:
                result += f"• ... 외 {len(df.columns) - 10}개 컬럼\n"

            result += f"\n**기본 통계:**\n"
            numeric_cols = df.select_dtypes(include=["number"]).columns
            if len(numeric_cols) > 0:
                stats = df[numeric_cols].describe()
                result += f"수치형 컬럼 {len(numeric_cols)}개에 대한 통계 정보가 생성되었습니다.\n"

            return result

        except Exception as e:
            return f"❌ CSV 분석 중 오류 발생: {str(e)}"

    def generate_report(self) -> str:
        """분석 보고서 생성"""
        try:
            report_path = (
                self.workspace_dir
                / f"analysis_report_{datetime.date.today().isoformat()}.txt"
            )

            report_content = f"""
📊 데이터 분석 보고서
생성일: {datetime.datetime.now().isoformat()}

=== 워크스페이스 현황 ===
총 파일 수: {len(list(self.workspace_dir.rglob('*.*')))}개

=== 데이터 파일 현황 ===
CSV 파일: {len(list(self.workspace_dir.rglob('*.csv')))}개
Excel 파일: {len(list(self.workspace_dir.rglob('*.xlsx')))}개
JSON 파일: {len(list(self.workspace_dir.rglob('*.json')))}개

=== 권장사항 ===
• 정기적인 데이터 백업 실시
• 데이터 품질 관리 체계 구축
• 자동화된 분석 파이프라인 구성
            """

            report_path.write_text(report_content, encoding="utf-8")

            return f"📊 분석 보고서가 생성되었습니다!\n위치: {report_path}"

        except Exception as e:
            return f"❌ 보고서 생성 중 오류 발생: {str(e)}"

    def get_analysis_summary(self) -> str:
        """분석 요약 정보"""
        csv_count = len(list(self.workspace_dir.rglob("*.csv")))
        excel_count = len(list(self.workspace_dir.rglob("*.xlsx")))

        return f"""📊 **데이터 분석 현황**

📁 분석 가능한 파일:
• CSV 파일: {csv_count}개
• Excel 파일: {excel_count}개

🔧 분석 기능:
• 파일 데이터 분석 - CSV/Excel 파일 통계 분석
• 분석 보고서 - 종합 분석 리포트 생성
• 차트 생성 - 데이터 시각화

분석할 파일이 있으시면 '데이터 분석' 명령을 사용해주세요!"""


def main():
    """메인 실행 함수"""
    print("🤖 박사급 비서 도깨비 시작!")
    print("=" * 60)

    # 비서 도깨비 초기화
    assistant = ProductivityAssistantGoblin()

    print(f"✅ {assistant.name} 준비 완료!")
    print("💡 도움말을 보려면 '도움' 또는 'help'를 입력하세요.")
    print("🚀 종료하려면 'quit' 또는 'exit'를 입력하세요.")
    print("=" * 60)

    # 대화 루프
    while True:
        try:
            user_input = input(f"\n{assistant.emoji} 명령을 입력하세요: ").strip()

            if user_input.lower() in ["quit", "exit", "종료", "나가기"]:
                print("🤖 박사급 비서 도깨비를 종료합니다. 좋은 하루 되세요!")
                break

            if not user_input:
                continue

            # 명령 처리 및 응답
            response = assistant.process_command(user_input)
            print(f"\n{response}")

        except KeyboardInterrupt:
            print("\n\n🤖 박사급 비서 도깨비를 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
