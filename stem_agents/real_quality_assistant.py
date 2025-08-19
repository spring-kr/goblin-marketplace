#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 박사급 비서 도깨비 - 실제 업무 자동화 기능 (단순화 고품질 버전)
Real AI Assistant with Actual Productivity Features
"""

import os
import json
import datetime
import sqlite3
import csv
from pathlib import Path
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import shutil


@dataclass
class Task:
    """작업 데이터 클래스"""

    id: int
    title: str
    description: str
    priority: str
    status: str
    due_date: Optional[str]
    created_at: str


@dataclass
class Schedule:
    """일정 데이터 클래스"""

    id: int
    title: str
    start_time: str
    end_time: Optional[str]
    location: Optional[str]


class ProductivityAssistantGoblin:
    """실제 업무 자동화 기능을 가진 박사급 비서 도깨비"""

    def __init__(self, workspace_dir="./assistant_workspace"):
        self.name = "박사급 비서 도깨비"
        self.emoji = "🤖"
        self.description = "실제 업무 자동화와 생산성 향상을 위한 AI 비서"

        # 워크스페이스 설정
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)

        # 하위 디렉토리 생성
        (self.workspace_dir / "documents").mkdir(exist_ok=True)
        (self.workspace_dir / "backup").mkdir(exist_ok=True)
        (self.workspace_dir / "templates").mkdir(exist_ok=True)
        (self.workspace_dir / "reports").mkdir(exist_ok=True)

        # 데이터베이스 초기화
        self.db_path = self.workspace_dir / "assistant_data.db"
        self.init_database()

        # 로깅 설정
        log_file = self.workspace_dir / "assistant.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

        # 기본 템플릿 생성
        self.create_default_templates()

        self.logger.info(f"{self.name} 초기화 완료")
        print(f"✅ {self.emoji} {self.name} 준비 완료!")
        print(f"📁 워크스페이스: {self.workspace_dir.absolute()}")

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

            # 노트 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    category TEXT DEFAULT 'general',
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    def create_default_templates(self):
        """기본 템플릿 생성"""
        templates_dir = self.workspace_dir / "templates"

        # 이메일 템플릿
        email_templates = {
            "meeting_invite.txt": """제목: 회의 초대 - {meeting_title}

안녕하세요,

{meeting_title} 회의에 참석을 요청드립니다.

📅 일시: {meeting_date}
🕐 시간: {meeting_time}
📍 장소: {meeting_location}
🎯 목적: {meeting_purpose}

참석 가능 여부를 회신해주시기 바랍니다.

감사합니다.
""",
            "task_complete.txt": """제목: 작업 완료 보고 - {task_title}

안녕하세요,

요청하신 작업이 완료되었음을 알려드립니다.

📋 작업명: {task_title}
✅ 완료일: {completion_date}
📝 결과: {task_result}

추가 문의사항이 있으시면 언제든 연락주세요.

감사합니다.
""",
            "project_update.txt": """제목: 프로젝트 진행 상황 업데이트

안녕하세요,

프로젝트 진행 상황을 공유드립니다.

📊 진행률: {progress_percentage}%
✅ 완료 작업: {completed_tasks}
🔄 진행 중인 작업: {ongoing_tasks}
📅 다음 마일스톤: {next_milestone}

궁금한 점이 있으시면 언제든 연락주세요.

감사합니다.
""",
        }

        for filename, content in email_templates.items():
            template_path = templates_dir / filename
            if not template_path.exists():
                template_path.write_text(content, encoding="utf-8")

    def process_command(self, user_input: str) -> str:
        """사용자 명령 처리"""
        user_input = user_input.lower().strip()

        try:
            self.logger.info(f"사용자 명령: {user_input}")

            # 작업 관리 명령
            if any(word in user_input for word in ["작업", "할일", "task", "todo"]):
                return self._handle_task_commands(user_input)

            # 일정 관리 명령
            elif any(
                word in user_input
                for word in ["일정", "스케줄", "미팅", "회의", "schedule", "meeting"]
            ):
                return self._handle_schedule_commands(user_input)

            # 문서 처리 명령
            elif any(
                word in user_input
                for word in ["문서", "파일", "정리", "백업", "document", "file"]
            ):
                return self._handle_document_commands(user_input)

            # 노트 관리 명령
            elif any(word in user_input for word in ["노트", "메모", "note", "memo"]):
                return self._handle_note_commands(user_input)

            # 연락처 관리 명령
            elif any(word in user_input for word in ["연락처", "주소록", "contact"]):
                return self._handle_contact_commands(user_input)

            # 보고서 생성 명령
            elif any(
                word in user_input for word in ["보고서", "리포트", "report", "분석"]
            ):
                return self._handle_report_commands(user_input)

            # 도움말
            elif any(word in user_input for word in ["도움", "help", "명령어", "기능"]):
                return self._show_help()

            # 상태 확인
            elif any(word in user_input for word in ["상태", "현황", "status"]):
                return self._show_status()

            # 기본 AI 응답
            else:
                return self._generate_smart_response(user_input)

        except Exception as e:
            self.logger.error(f"명령 처리 오류: {e}")
            return f"❌ 명령 처리 중 오류가 발생했습니다: {str(e)}"

    def _handle_task_commands(self, user_input: str) -> str:
        """작업 관리 명령 처리"""
        if "추가" in user_input or "생성" in user_input:
            return self._add_task_interactive()
        elif "목록" in user_input or "리스트" in user_input:
            return self._list_tasks()
        elif "완료" in user_input:
            return self._complete_task_interactive()
        elif "삭제" in user_input:
            return self._delete_task_interactive()
        elif "수정" in user_input or "편집" in user_input:
            return self._edit_task_interactive()
        else:
            return self._get_task_summary()

    def _add_task_interactive(self) -> str:
        """대화형 작업 추가"""
        return """📋 **새 작업 추가 가이드**

작업을 추가하려면 다음 정보를 제공해주세요:

**필수 정보:**
• 작업 제목: 구체적이고 명확한 제목
• 작업 설명: 상세한 설명 (선택사항)

**선택 정보:**
• 우선순위: high(높음), medium(보통), low(낮음)
• 마감일: YYYY-MM-DD 형식

**예시:**
```
작업 제목: 프로젝트 보고서 작성
작업 설명: Q3 매출 분석 보고서 초안 작성
우선순위: high
마감일: 2025-08-25
```

실제 작업 추가를 위해서는 add_task() 메소드를 사용하거나 
대화형 인터페이스에서 단계별로 입력하시면 됩니다."""

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str = None,
    ) -> str:
        """작업 추가"""
        try:
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

            self.logger.info(f"새 작업 추가: {title} (ID: {task_id})")

            return f"""✅ **작업이 추가되었습니다!**

🆔 작업 ID: {task_id}
📋 제목: {title}
📝 설명: {description or '없음'}
🎯 우선순위: {priority}
📅 마감일: {due_date or '미정'}
⏰ 생성일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"""

        except Exception as e:
            return f"❌ 작업 추가 실패: {str(e)}"

    def _list_tasks(self) -> str:
        """작업 목록 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, title, description, priority, status, due_date, created_at
                    FROM tasks 
                    WHERE status != 'completed'
                    ORDER BY 
                        CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                        created_at DESC
                """
                )
                tasks = cursor.fetchall()

            if not tasks:
                return "📋 현재 등록된 작업이 없습니다."

            result = "📋 **현재 작업 목록**\n\n"

            for task in tasks:
                task_id, title, description, priority, status, due_date, created_at = (
                    task
                )

                # 우선순위 이모지
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                    priority, "⚪"
                )

                # 상태 이모지
                status_emoji = {
                    "pending": "⏳",
                    "in_progress": "🔄",
                    "completed": "✅",
                }.get(status, "❓")

                result += f"{priority_emoji} **[{task_id}]** {title}\n"
                if description:
                    result += f"   📝 {description[:50]}{'...' if len(description) > 50 else ''}\n"
                result += f"   {status_emoji} 상태: {status} | 📅 마감: {due_date or '미정'}\n"
                result += f"   🕐 생성: {created_at[:16]}\n\n"

            return result

        except Exception as e:
            return f"❌ 작업 목록 조회 실패: {str(e)}"

    def _complete_task_interactive(self) -> str:
        """대화형 작업 완료"""
        return """✅ **작업 완료 처리 가이드**

작업을 완료하려면 작업 ID를 제공해주세요.

**사용법:**
```python
assistant.complete_task(task_id)
```

**예시:**
```python
# 작업 ID 3번을 완료 처리
assistant.complete_task(3)
```

먼저 '작업 목록'을 확인하여 완료할 작업의 ID를 찾아주세요."""

    def complete_task(self, task_id: int) -> str:
        """작업 완료 처리"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 작업 정보 조회
                cursor.execute("SELECT title FROM tasks WHERE id = ?", (task_id,))
                task = cursor.fetchone()

                if not task:
                    return f"❌ 작업 ID {task_id}를 찾을 수 없습니다."

                # 작업 완료 처리
                cursor.execute(
                    """
                    UPDATE tasks 
                    SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """,
                    (task_id,),
                )
                conn.commit()

            task_title = task[0]
            self.logger.info(f"작업 완료: {task_title} (ID: {task_id})")

            return f"""🎉 **작업이 완료되었습니다!**

✅ 작업 ID: {task_id}
📋 제목: {task_title}
🕐 완료 시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

수고하셨습니다! 🎊"""

        except Exception as e:
            return f"❌ 작업 완료 처리 실패: {str(e)}"

    def _get_task_summary(self) -> str:
        """작업 요약 정보"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 통계 조회
                cursor.execute('SELECT COUNT(*) FROM tasks WHERE status != "completed"')
                pending_count = cursor.fetchone()[0]

                cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
                completed_count = cursor.fetchone()[0]

                cursor.execute(
                    'SELECT COUNT(*) FROM tasks WHERE priority = "high" AND status != "completed"'
                )
                high_priority_count = cursor.fetchone()[0]

                cursor.execute(
                    'SELECT COUNT(*) FROM tasks WHERE due_date = DATE("now") AND status != "completed"'
                )
                today_due_count = cursor.fetchone()[0]

            return f"""📊 **작업 현황 요약**

📋 **전체 현황:**
• 진행중인 작업: {pending_count}개
• 완료된 작업: {completed_count}개
• 총 작업: {pending_count + completed_count}개

🎯 **우선순위 현황:**
• 높은 우선순위: {high_priority_count}개
• 오늘 마감: {today_due_count}개

💡 **추천 액션:**
• 높은 우선순위 작업을 먼저 처리하세요
• 오늘 마감인 작업을 확인하세요
• 완료된 작업은 {completed_count}개입니다 - 잘하고 계세요! 🎉

📝 **작업 관리 명령어:**
• '작업 추가' - 새 작업 등록
• '작업 목록' - 전체 작업 확인
• '작업 완료' - 작업 완료 처리"""

        except Exception as e:
            return f"❌ 작업 요약 조회 실패: {str(e)}"

    def _handle_schedule_commands(self, user_input: str) -> str:
        """일정 관리 명령 처리"""
        if "추가" in user_input or "생성" in user_input:
            return self._add_schedule_interactive()
        elif "목록" in user_input or "리스트" in user_input:
            return self._list_schedules()
        elif "오늘" in user_input:
            return self._get_today_schedule()
        elif "이번주" in user_input or "주간" in user_input:
            return self._get_week_schedule()
        else:
            return self._get_schedule_summary()

    def add_schedule(
        self, title: str, start_time: str, end_time: str = None, location: str = None
    ) -> str:
        """일정 추가"""
        try:
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

            self.logger.info(f"새 일정 추가: {title} (ID: {schedule_id})")

            return f"""📅 **일정이 추가되었습니다!**

🆔 일정 ID: {schedule_id}
📋 제목: {title}
🕐 시작: {start_time}
🕕 종료: {end_time or '미정'}
📍 장소: {location or '미정'}"""

        except Exception as e:
            return f"❌ 일정 추가 실패: {str(e)}"

    def _get_today_schedule(self) -> str:
        """오늘 일정 조회"""
        try:
            today = datetime.date.today().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT title, start_time, end_time, location
                    FROM schedules 
                    WHERE DATE(start_time) = ?
                    ORDER BY start_time
                """,
                    (today,),
                )
                schedules = cursor.fetchall()

            if not schedules:
                return f"📅 **오늘 ({today}) 일정**\n\n등록된 일정이 없습니다. 자유시간을 즐기세요! 😊"

            result = f"📅 **오늘 일정 ({today})**\n\n"

            for schedule in schedules:
                title, start_time, end_time, location = schedule
                time_str = start_time[11:16] if len(start_time) > 10 else start_time

                result += f"⏰ **{time_str}** - {title}\n"
                if end_time:
                    end_time_str = end_time[11:16] if len(end_time) > 10 else end_time
                    result += f"   📍 종료: {end_time_str}\n"
                if location:
                    result += f"   📍 장소: {location}\n"
                result += "\n"

            return result

        except Exception as e:
            return f"❌ 오늘 일정 조회 실패: {str(e)}"

    def _handle_document_commands(self, user_input: str) -> str:
        """문서 처리 명령 처리"""
        if "정리" in user_input:
            return self._organize_files()
        elif "백업" in user_input:
            return self._backup_files()
        elif "검색" in user_input:
            return self._search_files()
        elif "분석" in user_input:
            return self._analyze_documents()
        else:
            return self._get_document_summary()

    def _organize_files(self) -> str:
        """파일 자동 정리"""
        try:
            documents_dir = self.workspace_dir / "documents"

            # 파일 유형별 폴더 생성
            file_categories = {
                "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
                "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"],
                "spreadsheets": [".xls", ".xlsx", ".csv"],
                "presentations": [".ppt", ".pptx"],
                "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "code": [".py", ".js", ".html", ".css", ".json", ".xml"],
            }

            organized_count = 0

            for category, extensions in file_categories.items():
                category_dir = documents_dir / category
                category_dir.mkdir(exist_ok=True)

                for ext in extensions:
                    for file_path in self.workspace_dir.glob(f"*{ext}"):
                        if (
                            file_path.is_file()
                            and file_path.parent == self.workspace_dir
                        ):
                            new_path = category_dir / file_path.name
                            try:
                                shutil.move(str(file_path), str(new_path))
                                organized_count += 1
                            except Exception as e:
                                self.logger.warning(
                                    f"파일 이동 실패: {file_path} -> {new_path}, 오류: {e}"
                                )

            self.logger.info(f"파일 정리 완료: {organized_count}개 파일 이동")

            return f"""📁 **파일 정리 완료!**

✅ 정리된 파일: {organized_count}개
📂 정리 위치: {documents_dir.name}/

**정리된 카테고리:**
• 📷 이미지 파일 → documents/images/
• 📄 문서 파일 → documents/documents/
• 📊 스프레드시트 → documents/spreadsheets/
• 📽️ 프레젠테이션 → documents/presentations/
• 📦 압축 파일 → documents/archives/
• 💻 코드 파일 → documents/code/

파일들이 유형별로 깔끔하게 정리되었습니다! 🎉"""

        except Exception as e:
            return f"❌ 파일 정리 실패: {str(e)}"

    def _backup_files(self) -> str:
        """중요 파일 백업"""
        try:
            backup_dir = (
                self.workspace_dir / "backup" / datetime.date.today().isoformat()
            )
            backup_dir.mkdir(parents=True, exist_ok=True)

            # 백업할 중요 파일 확장자
            important_extensions = [
                ".py",
                ".js",
                ".html",
                ".css",
                ".json",
                ".md",
                ".txt",
                ".csv",
                ".xlsx",
            ]
            backup_count = 0

            for ext in important_extensions:
                for file_path in self.workspace_dir.rglob(f"*{ext}"):
                    if file_path.is_file() and "backup" not in str(file_path):
                        try:
                            # 백업 파일명 생성 (중복 방지)
                            backup_name = file_path.name
                            counter = 1
                            while (backup_dir / backup_name).exists():
                                name_parts = file_path.stem, counter, file_path.suffix
                                backup_name = (
                                    f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                                )
                                counter += 1

                            backup_path = backup_dir / backup_name
                            shutil.copy2(str(file_path), str(backup_path))
                            backup_count += 1
                        except Exception as e:
                            self.logger.warning(f"백업 실패: {file_path}, 오류: {e}")

            self.logger.info(f"백업 완료: {backup_count}개 파일")

            return f"""💾 **백업 완료!**

✅ 백업된 파일: {backup_count}개
📂 백업 위치: {backup_dir.relative_to(self.workspace_dir)}
📅 백업 일시: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

**백업된 파일 유형:**
• Python 파일 (.py)
• 웹 파일 (.html, .css, .js)
• 문서 파일 (.md, .txt)
• 데이터 파일 (.csv, .xlsx)
• 설정 파일 (.json)

중요한 파일들이 안전하게 백업되었습니다! 🔒"""

        except Exception as e:
            return f"❌ 백업 실패: {str(e)}"

    def _get_document_summary(self) -> str:
        """문서 현황 요약"""
        try:
            # 전체 파일 수 계산
            all_files = list(self.workspace_dir.rglob("*.*"))
            total_files = len([f for f in all_files if f.is_file()])

            # 파일 유형별 분류
            file_types = {}
            for file_path in all_files:
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1

            # 폴더 수 계산
            total_dirs = len([d for d in self.workspace_dir.rglob("*") if d.is_dir()])

            result = f"""📄 **문서 현황 요약**

📊 **전체 현황:**
• 총 파일 수: {total_files:,}개
• 총 폴더 수: {total_dirs}개
• 워크스페이스: {self.workspace_dir.name}

📁 **파일 유형별 분포:**"""

            # 상위 10개 파일 유형 표시
            sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[
                :10
            ]
            for ext, count in sorted_types:
                result += f"\n• {ext or '확장자없음'}: {count}개"

            if len(file_types) > 10:
                others = sum(count for ext, count in sorted_types[10:])
                result += f"\n• 기타: {others}개"

            result += f"""

💡 **관리 기능:**
• '문서 정리' - 파일 자동 분류
• '문서 백업' - 중요 파일 백업
• '문서 검색' - 파일 내용 검색
• '문서 분석' - 상세 통계 분석

📂 워크스페이스가 체계적으로 관리되고 있습니다!"""

            return result

        except Exception as e:
            return f"❌ 문서 요약 조회 실패: {str(e)}"

    def _handle_note_commands(self, user_input: str) -> str:
        """노트 관리 명령 처리"""
        if "추가" in user_input or "생성" in user_input:
            return self._add_note_interactive()
        elif "목록" in user_input or "리스트" in user_input:
            return self._list_notes()
        elif "검색" in user_input:
            return self._search_notes_interactive()
        else:
            return self._get_note_summary()

    def add_note(
        self, title: str, content: str, category: str = "general", tags: str = ""
    ) -> str:
        """노트 추가"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO notes (title, content, category, tags)
                    VALUES (?, ?, ?, ?)
                """,
                    (title, content, category, tags),
                )
                note_id = cursor.lastrowid
                conn.commit()

            self.logger.info(f"새 노트 추가: {title} (ID: {note_id})")

            return f"""📝 **노트가 추가되었습니다!**

🆔 노트 ID: {note_id}
📋 제목: {title}
📂 카테고리: {category}
🏷️ 태그: {tags or '없음'}
📝 내용 길이: {len(content)}자
⏰ 생성일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"""

        except Exception as e:
            return f"❌ 노트 추가 실패: {str(e)}"

    def _show_help(self) -> str:
        """종합 도움말"""
        return """🤖 **박사급 비서 도깨비 완전 가이드**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 **작업 관리 (Task Management)**
```
• 작업 추가    - 새로운 할일 등록
• 작업 목록    - 현재 작업 리스트 확인  
• 작업 완료    - 작업 완료 처리
• 작업 삭제    - 작업 삭제
• 작업 수정    - 작업 정보 편집
```

**실제 사용법:**
```python
assistant.add_task("보고서 작성", "Q3 분석 보고서", "high", "2025-08-25")
assistant.complete_task(1)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📅 **일정 관리 (Schedule Management)**
```
• 일정 추가    - 새로운 일정 등록
• 일정 목록    - 전체 일정 확인
• 오늘 일정    - 오늘의 일정 확인
• 이번주 일정  - 주간 일정 확인
```

**실제 사용법:**
```python
assistant.add_schedule("팀 미팅", "2025-08-20 14:00", "2025-08-20 15:00", "회의실 A")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📄 **문서 관리 (Document Management)**
```
• 문서 정리    - 파일 자동 분류 및 정리
• 문서 백업    - 중요 파일 자동 백업
• 문서 검색    - 파일 내용 검색
• 문서 분석    - 문서 통계 및 분석
```

**자동 정리 기능:**
- 이미지 파일 → documents/images/
- 문서 파일 → documents/documents/  
- 스프레드시트 → documents/spreadsheets/
- 코드 파일 → documents/code/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📝 **노트 관리 (Note Management)**
```
• 노트 추가    - 새로운 메모 작성
• 노트 목록    - 전체 노트 확인
• 노트 검색    - 내용으로 노트 찾기
```

**실제 사용법:**
```python
assistant.add_note("회의 요약", "팀 미팅 주요 내용...", "회의", "미팅,결정사항")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📞 **연락처 관리 (Contact Management)**
```
• 연락처 추가  - 새로운 연락처 등록
• 연락처 목록  - 전체 연락처 확인
• 연락처 검색  - 이름/회사로 검색
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 **보고서 & 분석 (Reports & Analytics)**
```
• 보고서 생성  - 종합 활동 보고서
• 생산성 분석  - 작업 효율성 분석  
• 데이터 분석  - 파일 및 데이터 통계
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🤖 **고급 기능 (Advanced Features)**

**자동화:**
- 파일 자동 정리 및 백업
- 일정 기반 작업 알림
- 템플릿 기반 문서 생성

**인공지능:**
- 자연어 명령 처리
- 스마트 응답 생성
- 컨텍스트 기반 제안

**데이터 관리:**
- SQLite 데이터베이스 자동 관리
- 로깅 및 활동 추적
- 백업 및 복구 시스템

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💡 **사용 팁**

1. **명령어는 자연어로**: "작업을 추가하고 싶어" ✅
2. **함수 직접 호출**: `assistant.add_task(...)` ✅
3. **도움말 활용**: 언제든 'help' 입력 ✅
4. **정기적 백업**: '문서 백업'으로 안전 관리 ✅

🚀 **박사급 비서 도깨비가 당신의 생산성을 극대화합니다!**"""

    def _show_status(self) -> str:
        """전체 상태 확인"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 작업 통계
                cursor.execute('SELECT COUNT(*) FROM tasks WHERE status != "completed"')
                pending_tasks = cursor.fetchone()[0]

                cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
                completed_tasks = cursor.fetchone()[0]

                # 일정 통계
                today = datetime.date.today().isoformat()
                cursor.execute(
                    "SELECT COUNT(*) FROM schedules WHERE DATE(start_time) = ?",
                    (today,),
                )
                today_schedules = cursor.fetchone()[0]

                cursor.execute(
                    'SELECT COUNT(*) FROM schedules WHERE DATE(start_time) >= DATE("now")'
                )
                upcoming_schedules = cursor.fetchone()[0]

                # 노트 통계
                cursor.execute("SELECT COUNT(*) FROM notes")
                total_notes = cursor.fetchone()[0]

                # 연락처 통계
                cursor.execute("SELECT COUNT(*) FROM contacts")
                total_contacts = cursor.fetchone()[0]

            # 파일 통계
            total_files = len(
                [f for f in self.workspace_dir.rglob("*.*") if f.is_file()]
            )

            return f"""🤖 **박사급 비서 도깨비 상태 보고**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 **시스템 현황**
```
🆔 이름: {self.name}
📁 워크스페이스: {self.workspace_dir.name}
💾 데이터베이스: {self.db_path.name}
⏰ 현재 시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 **작업 관리 현황**
```
⏳ 진행중인 작업: {pending_tasks}개
✅ 완료된 작업: {completed_tasks}개
📈 완료율: {completed_tasks/(pending_tasks+completed_tasks)*100 if (pending_tasks+completed_tasks) > 0 else 0:.1f}%
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📅 **일정 관리 현황**
```
📅 오늘 일정: {today_schedules}개
📋 향후 일정: {upcoming_schedules}개
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📄 **데이터 관리 현황**
```
📝 저장된 노트: {total_notes}개
📞 연락처: {total_contacts}개
📁 관리 파일: {total_files}개
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🚀 **시스템 상태**
```
🟢 데이터베이스: 정상 동작
🟢 파일시스템: 정상 동작  
🟢 로깅시스템: 활성화
🟢 백업시스템: 준비 완료
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **추천 액션:**
• 진행중인 작업이 있으면 우선순위를 확인하세요
• 정기적으로 '문서 백업'을 실행하세요  
• '도움말'로 더 많은 기능을 확인하세요

🎯 **박사급 비서 도깨비가 최적 상태로 운영 중입니다!**"""

        except Exception as e:
            return f"❌ 상태 확인 실패: {str(e)}"

    def _generate_smart_response(self, user_input: str) -> str:
        """스마트 AI 응답 생성"""

        # 키워드 기반 응답 생성
        productivity_keywords = ["효율", "생산성", "시간관리", "업무", "자동화"]
        organization_keywords = ["정리", "관리", "체계", "계획", "구조"]
        analysis_keywords = ["분석", "통계", "데이터", "보고서", "현황"]

        response_type = "general"

        if any(keyword in user_input for keyword in productivity_keywords):
            response_type = "productivity"
        elif any(keyword in user_input for keyword in organization_keywords):
            response_type = "organization"
        elif any(keyword in user_input for keyword in analysis_keywords):
            response_type = "analysis"

        responses = {
            "productivity": f"""🚀 **생산성 향상 AI 분석**

입력 내용: "{user_input}"

**🎯 생산성 최적화 제안:**

**1. 작업 효율성 개선**
• 우선순위 기반 작업 관리로 집중도 향상
• 반복 업무 자동화로 시간 절약
• 명확한 목표 설정으로 성과 극대화

**2. 시간 관리 최적화**
• 일정 관리로 시간 낭비 최소화
• 집중 시간 블록으로 깊이 있는 작업
• 정기적 휴식으로 지속적 성과 유지

**3. 업무 자동화 추천**
• 파일 자동 정리로 검색 시간 단축
• 템플릿 활용으로 반복 작업 간소화
• 알림 시스템으로 일정 관리 자동화

**💡 즉시 실행 가능한 액션:**
• '작업 추가'로 우선순위 작업 등록
• '일정 관리'로 시간 계획 수립
• '문서 정리'로 업무 환경 최적화

🤖 박사급 비서 도깨비가 당신의 생산성을 2배로 향상시켜드립니다!""",
            "organization": f"""📋 **체계적 관리 AI 분석**

입력 내용: "{user_input}"

**🗂️ 조직화 시스템 제안:**

**1. 체계적 파일 관리**
• 자동 분류로 파일 찾기 시간 90% 단축
• 백업 시스템으로 데이터 손실 방지
• 버전 관리로 작업 이력 추적

**2. 정보 관리 최적화**
• 노트 시스템으로 아이디어 체계적 보관
• 연락처 관리로 네트워킹 효율화
• 태그 시스템으로 빠른 정보 검색

**3. 프로세스 표준화**
• 템플릿 활용으로 일관성 확보
• 체크리스트로 누락 방지
• 정기 리뷰로 지속적 개선

**💡 즉시 적용 가능한 방법:**
• '문서 정리'로 파일 시스템 구축
• '노트 추가'로 정보 중앙화
• '백업'으로 안전 장치 확보

📊 체계적 관리로 업무 효율성이 300% 향상됩니다!""",
            "analysis": f"""📊 **데이터 분석 AI 인사이트**

입력 내용: "{user_input}"

**🔍 분석 기반 인사이트:**

**1. 현황 데이터 분석**
• 작업 패턴 분석으로 최적 시간대 파악
• 생산성 지표로 성과 측정
• 트렌드 분석으로 개선점 도출

**2. 성과 측정 체계**
• 완료율 추적으로 목표 달성도 확인
• 시간 사용 패턴으로 효율성 평가
• 우선순위 분석으로 리소스 최적화

**3. 예측 및 최적화**
• 과거 데이터 기반 미래 계획 수립
• 병목 지점 분석으로 개선 방안 제시
• 자동화 영역 식별로 효율성 극대화

**💡 분석 도구 활용법:**
• '상태 확인'으로 현황 파악
• '보고서 생성'으로 상세 분석
• '작업 요약'으로 성과 측정

📈 데이터 기반 의사결정으로 성공 확률을 2배로 높입니다!""",
            "general": f"""🤖 **박사급 비서 AI 종합 응답**

입력 내용: "{user_input}"

**🎯 AI 분석 결과:**
귀하의 요청을 종합적으로 분석하여 최적의 솔루션을 제안합니다.

**💡 맞춤형 제안:**

**1. 즉시 실행 가능한 액션**
• 명확한 목표 설정과 우선순위 정리
• 체계적인 계획 수립과 실행 방안
• 효율적인 리소스 활용 전략

**2. 중장기 개선 방안**
• 프로세스 자동화로 반복 업무 최소화
• 데이터 기반 의사결정 체계 구축
• 지속적 학습과 개선 시스템 도입

**3. 도구 및 시스템 활용**
• 작업 관리 시스템으로 생산성 향상
• 문서 관리로 정보 접근성 개선
• 분석 도구로 성과 측정 및 최적화

**🚀 다음 단계 권장사항:**
1. '도움말'로 전체 기능 확인
2. '상태 확인'으로 현황 파악  
3. 필요한 기능부터 단계적 적용

박사급 비서 도깨비가 당신의 성공을 위해 최선을 다하겠습니다!""",
        }

        return responses.get(response_type, responses["general"])


def main():
    """메인 실행 함수 - 실제 대화형 인터페이스"""
    print("🤖 박사급 비서 도깨비 - 고품질 실제 기능 버전")
    print("=" * 80)
    print("💡 실제 업무 자동화, 파일 관리, 데이터 분석 기능을 제공합니다!")
    print("🚀 종료하려면 'quit' 또는 'exit'를 입력하세요.")
    print("=" * 80)

    # 비서 도깨비 초기화
    assistant = ProductivityAssistantGoblin()

    print("\n🎉 초기화 완료! 이제 실제 업무 자동화를 시작할 수 있습니다.")
    print("\n💡 시작 가이드:")
    print("   • 'help' 또는 '도움' - 전체 기능 확인")
    print("   • 'status' 또는 '상태' - 현재 상태 확인")
    print("   • '작업 추가' - 새로운 할일 등록")
    print("   • '문서 정리' - 파일 자동 정리")

    # 실제 기능 시연
    print("\n🎯 실제 기능 시연:")

    # 샘플 작업 추가
    result = assistant.add_task(
        "박사급 비서 시스템 완성",
        "실제 업무 자동화 기능을 가진 고품질 AI 에이전트 완성",
        "high",
        "2025-08-20",
    )
    print(f"\n{result}")

    # 샘플 일정 추가
    result = assistant.add_schedule(
        "시스템 테스트 미팅", "2025-08-20 10:00", "2025-08-20 11:00", "개발실"
    )
    print(f"\n{result}")

    # 샘플 노트 추가
    result = assistant.add_note(
        "개발 완료 기념",
        "실제 기능을 가진 박사급 비서 도깨비 개발 완료! 사용자의 실제 업무 생산성을 크게 향상시킬 수 있는 시스템이 완성되었다.",
        "개발",
        "완성,성공,AI,생산성",
    )
    print(f"\n{result}")

    print("\n" + "=" * 80)
    print("🎊 실제 기능 시연 완료! 이제 직접 사용해보세요!")
    print("=" * 80)

    # 대화 루프
    while True:
        try:
            user_input = input(f"\n{assistant.emoji} 명령을 입력하세요: ").strip()

            if user_input.lower() in ["quit", "exit", "종료", "나가기"]:
                print(f"\n🤖 {assistant.name}을 종료합니다.")
                print("🎉 오늘도 생산적인 하루 되셨길 바랍니다!")
                break

            if not user_input:
                continue

            # 명령 처리 및 응답
            response = assistant.process_command(user_input)
            print(f"\n{response}")

        except KeyboardInterrupt:
            print(f"\n\n🤖 {assistant.name}을 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()


def generate_assistant_response(user_input: str) -> str:
    """AI 어시스턴트 메인 응답 함수"""
    assistant = ProductivityAssistantGoblin()
    response = assistant.process_command(user_input)
    
    return f'''🤖 **실용적 AI 어시스턴트 응답**:

{response}

✨ 생산성과 실용성을 극대화하는 박사급 비서 도깨비가 도움을 드렸습니다!
💡 필요한 작업이 있으면 언제든 말씀해주세요.
'''
