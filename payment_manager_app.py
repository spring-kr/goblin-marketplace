"""
HYOJIN.AI 결제 관리 윈도우 앱
결제된 주문들을 실시간으로 모니터링하고 관리하는 데스크톱 애플리케이션
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import datetime
import sqlite3
import os
import threading
import time
from typing import Dict, List, Any
import webbrowser

try:
    import smtplib
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart

    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("이메일 기능을 사용할 수 없습니다. 기본 기능만 사용합니다.")


class PaymentDatabase:
    """결제 데이터베이스 관리"""

    def __init__(self, db_path="hyojin_payments.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 결제 테이블 생성
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_id TEXT UNIQUE NOT NULL,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_company TEXT,
                payment_method TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                items TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                notes TEXT
            )
        """
        )

        # 상품 테이블 생성
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id INTEGER,
                item_id TEXT NOT NULL,
                item_name TEXT NOT NULL,
                item_type TEXT NOT NULL,
                item_price REAL NOT NULL,
                FOREIGN KEY (payment_id) REFERENCES payments (id)
            )
        """
        )

        conn.commit()
        conn.close()

    def add_payment(self, payment_data: Dict[str, Any]) -> bool:
        """새 결제 추가"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.datetime.now().isoformat()

            cursor.execute(
                """
                INSERT INTO payments 
                (subscription_id, customer_name, customer_email, customer_company, 
                 payment_method, total_amount, status, items, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    payment_data["subscription_id"],
                    payment_data["customer_name"],
                    payment_data["customer_email"],
                    payment_data.get("customer_company", ""),
                    payment_data["payment_method"],
                    payment_data["total_amount"],
                    payment_data["status"],
                    json.dumps(payment_data["items"]),
                    now,
                    now,
                ),
            )

            payment_id = cursor.lastrowid

            # 주문 아이템 추가
            for item in payment_data["items"]:
                cursor.execute(
                    """
                    INSERT INTO order_items 
                    (payment_id, item_id, item_name, item_type, item_price)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (payment_id, item["id"], item["name"], item["type"], item["price"]),
                )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"결제 추가 오류: {e}")
            return False

    def get_all_payments(self) -> List[Dict[str, Any]]:
        """모든 결제 내역 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM payments ORDER BY created_at DESC
        """
        )

        payments = []
        for row in cursor.fetchall():
            payment = {
                "id": row[0],
                "subscription_id": row[1],
                "customer_name": row[2],
                "customer_email": row[3],
                "customer_company": row[4],
                "payment_method": row[5],
                "total_amount": row[6],
                "status": row[7],
                "items": json.loads(row[8]),
                "created_at": row[9],
                "updated_at": row[10],
                "notes": row[11] or "",
            }
            payments.append(payment)

        conn.close()
        return payments

    def update_payment_status(
        self, payment_id: int, status: str, notes: str = ""
    ) -> bool:
        """결제 상태 업데이트"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.datetime.now().isoformat()

            cursor.execute(
                """
                UPDATE payments 
                SET status = ?, notes = ?, updated_at = ?
                WHERE id = ?
            """,
                (status, notes, now, payment_id),
            )

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"상태 업데이트 오류: {e}")
            return False


class PaymentManagerApp:
    """결제 관리 메인 애플리케이션"""

    def __init__(self):
        self.db = PaymentDatabase()
        self.root = tk.Tk()
        self.setup_ui()
        self.load_payments()
        self.start_auto_refresh()

    def setup_ui(self):
        """UI 설정"""
        self.root.title("🛒 HYOJIN.AI 결제 관리 시스템")
        self.root.geometry("1400x800")
        self.root.configure(bg="#2c3e50")

        # 스타일 설정
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ecf0f1", foreground="#2c3e50")
        style.configure("Treeview.Heading", background="#3498db", foreground="white")

        # 메인 프레임
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 제목
        title_label = tk.Label(
            main_frame,
            text="🛒 HYOJIN.AI 결제 관리 대시보드",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white",
        )
        title_label.pack(pady=(0, 20))

        # 상단 통계 패널
        self.create_stats_panel(main_frame)

        # 툴바
        self.create_toolbar(main_frame)

        # 결제 목록 테이블
        self.create_payments_table(main_frame)

        # 하단 액션 패널
        self.create_action_panel(main_frame)

    def create_stats_panel(self, parent):
        """통계 패널 생성"""
        stats_frame = tk.Frame(parent, bg="#2c3e50")
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        # 통계 카드들
        self.total_orders_var = tk.StringVar(value="0")
        self.total_revenue_var = tk.StringVar(value="$0")
        self.pending_orders_var = tk.StringVar(value="0")
        self.active_subs_var = tk.StringVar(value="0")

        # 카드 생성
        cards = [
            ("총 주문수", self.total_orders_var, "#3498db"),
            ("총 매출", self.total_revenue_var, "#2ecc71"),
            ("대기중", self.pending_orders_var, "#f39c12"),
            ("활성 구독", self.active_subs_var, "#e74c3c"),
        ]

        for i, (title, var, color) in enumerate(cards):
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=2)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

            tk.Label(
                card, text=title, font=("Arial", 12, "bold"), bg=color, fg="white"
            ).pack(pady=5)
            tk.Label(
                card, textvariable=var, font=("Arial", 16, "bold"), bg=color, fg="white"
            ).pack(pady=5)

    def create_toolbar(self, parent):
        """툴바 생성"""
        toolbar = tk.Frame(parent, bg="#34495e", relief=tk.RAISED, bd=1)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        # 버튼들
        buttons = [
            ("🔄 새로고침", self.refresh_payments),
            ("➕ 테스트 주문 추가", self.add_test_order),
            ("📊 통계 보기", self.show_statistics),
            ("📤 데이터 내보내기", self.export_data),
            ("⚙️ 설정", self.show_settings),
        ]

        for text, command in buttons:
            btn = tk.Button(
                toolbar,
                text=text,
                command=command,
                bg="#3498db",
                fg="white",
                font=("Arial", 10),
                relief=tk.FLAT,
                padx=15,
                pady=5,
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # 검색 기능
        search_frame = tk.Frame(toolbar, bg="#34495e")
        search_frame.pack(side=tk.RIGHT, padx=10, pady=5)

        tk.Label(search_frame, text="검색:", bg="#34495e", fg="white").pack(
            side=tk.LEFT
        )
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)

    def create_payments_table(self, parent):
        """결제 목록 테이블 생성"""
        table_frame = tk.Frame(parent, bg="#2c3e50")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 테이블 헤더
        columns = (
            "ID",
            "구독ID",
            "고객명",
            "이메일",
            "회사",
            "결제방법",
            "금액",
            "상태",
            "생성일",
        )

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )

        # 컬럼 설정
        column_widths = [50, 120, 100, 200, 100, 80, 80, 80, 150]
        for i, (col, width) in enumerate(zip(columns, column_widths)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=50)

        # 스크롤바
        v_scroll = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        h_scroll = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # 레이아웃
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # 더블클릭 이벤트
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def create_action_panel(self, parent):
        """액션 패널 생성"""
        action_frame = tk.Frame(parent, bg="#2c3e50")
        action_frame.pack(fill=tk.X, pady=(10, 0))

        # 상태 변경 버튼들
        status_buttons = [
            ("✅ 활성화", "active", "#2ecc71"),
            ("⏳ 대기중", "pending", "#f39c12"),
            ("❌ 취소", "cancelled", "#e74c3c"),
            ("🔄 환불", "refunded", "#9b59b6"),
        ]

        for text, status, color in status_buttons:
            btn = tk.Button(
                action_frame,
                text=text,
                command=lambda s=status: self.change_payment_status(s),
                bg=color,
                fg="white",
                font=("Arial", 10, "bold"),
                relief=tk.FLAT,
                padx=20,
                pady=5,
            )
            btn.pack(side=tk.LEFT, padx=5)

        # 상세 정보 버튼
        detail_btn = tk.Button(
            action_frame,
            text="📋 상세 정보",
            command=self.show_payment_details,
            bg="#34495e",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=5,
        )
        detail_btn.pack(side=tk.RIGHT, padx=5)

    def load_payments(self):
        """결제 목록 로드"""
        # 기존 항목 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 새 데이터 로드
        payments = self.db.get_all_payments()

        for payment in payments:
            # 상태별 색상
            status_colors = {
                "active": "#2ecc71",
                "pending": "#f39c12",
                "cancelled": "#e74c3c",
                "refunded": "#9b59b6",
            }

            # 날짜 포맷
            created_at = datetime.datetime.fromisoformat(
                payment["created_at"]
            ).strftime("%Y-%m-%d %H:%M")

            item_id = self.tree.insert(
                "",
                "end",
                values=(
                    payment["id"],
                    payment["subscription_id"],
                    payment["customer_name"],
                    payment["customer_email"],
                    payment["customer_company"] or "-",
                    payment["payment_method"],
                    f"${payment['total_amount']}",
                    payment["status"],
                    created_at,
                ),
            )

            # 상태별 색상 적용
            if payment["status"] in status_colors:
                self.tree.set(item_id, "status", payment["status"])

        # 통계 업데이트
        self.update_statistics()

    def update_statistics(self):
        """통계 업데이트"""
        payments = self.db.get_all_payments()

        total_orders = len(payments)
        total_revenue = sum(
            p["total_amount"] for p in payments if p["status"] in ["active", "pending"]
        )
        pending_orders = len([p for p in payments if p["status"] == "pending"])
        active_subs = len([p for p in payments if p["status"] == "active"])

        self.total_orders_var.set(str(total_orders))
        self.total_revenue_var.set(f"${total_revenue:,.0f}")
        self.pending_orders_var.set(str(pending_orders))
        self.active_subs_var.set(str(active_subs))

    def on_search(self, *args):
        """검색 기능"""
        search_term = self.search_var.get().lower()

        # 모든 항목 숨기기
        for item in self.tree.get_children():
            self.tree.detach(item)

        # 검색 조건에 맞는 항목만 표시
        payments = self.db.get_all_payments()
        for i, payment in enumerate(payments):
            if (
                search_term in payment["customer_name"].lower()
                or search_term in payment["customer_email"].lower()
                or search_term in payment["subscription_id"].lower()
            ):

                created_at = datetime.datetime.fromisoformat(
                    payment["created_at"]
                ).strftime("%Y-%m-%d %H:%M")

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        payment["id"],
                        payment["subscription_id"],
                        payment["customer_name"],
                        payment["customer_email"],
                        payment["customer_company"] or "-",
                        payment["payment_method"],
                        f"${payment['total_amount']}",
                        payment["status"],
                        created_at,
                    ),
                )

    def on_item_double_click(self, event):
        """항목 더블클릭 이벤트"""
        self.show_payment_details()

    def show_payment_details(self):
        """결제 상세 정보 표시"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "결제 항목을 선택해주세요.")
            return

        item = self.tree.item(selection[0])
        payment_id = int(item["values"][0])  # 정수로 변환

        # 상세 정보 윈도우 생성
        self.create_detail_window(payment_id)

    def create_detail_window(self, payment_id):
        """상세 정보 윈도우 생성"""
        payments = self.db.get_all_payments()
        payment = next((p for p in payments if p["id"] == payment_id), None)

        if not payment:
            return

        # 새 윈도우
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"결제 상세 정보 - {payment['subscription_id']}")
        detail_window.geometry("600x700")
        detail_window.configure(bg="#ecf0f1")

        # 스크롤 가능한 프레임
        canvas = tk.Canvas(detail_window, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(
            detail_window, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 제목
        title_label = tk.Label(
            scrollable_frame,
            text=f"📋 {payment['subscription_id']}",
            font=("Arial", 16, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
        )
        title_label.pack(pady=20)

        # 고객 정보
        self.create_info_section(
            scrollable_frame,
            "👤 고객 정보",
            [
                ("이름", payment["customer_name"]),
                ("이메일", payment["customer_email"]),
                ("회사", payment["customer_company"] or "-"),
            ],
        )

        # 결제 정보
        self.create_info_section(
            scrollable_frame,
            "💳 결제 정보",
            [
                ("결제 방법", payment["payment_method"]),
                ("총 금액", f"${payment['total_amount']}"),
                ("상태", payment["status"]),
                ("생성일", payment["created_at"]),
                ("수정일", payment["updated_at"]),
            ],
        )

        # 주문 상품
        items_text = "\n".join(
            [
                f"• {item['name']} ({item['type']}) - ${item['price']}"
                for item in payment["items"]
            ]
        )
        self.create_info_section(
            scrollable_frame,
            "🛍️ 주문 상품",
            [
                ("상품 목록", items_text),
                ("상품 수", str(len(payment["items"]))),
            ],
        )

        # 메모
        notes_frame = tk.LabelFrame(
            scrollable_frame,
            text="📝 메모",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
        )
        notes_frame.pack(fill=tk.X, padx=20, pady=10)

        notes_text = tk.Text(notes_frame, height=4, width=50)
        notes_text.pack(padx=10, pady=10)
        notes_text.insert("1.0", payment["notes"])

        # 저장 버튼
        save_btn = tk.Button(
            notes_frame,
            text="💾 메모 저장",
            command=lambda: self.save_payment_notes(
                payment_id, notes_text.get("1.0", "end-1c")
            ),
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        save_btn.pack(pady=5)

        # 액션 버튼들
        action_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
        action_frame.pack(fill=tk.X, padx=20, pady=20)

        actions = [
            ("📧 이메일 보내기", lambda: self.send_email_to_customer(payment)),
            (
                "🌐 GitHub 페이지 열기",
                lambda: webbrowser.open("https://spring-kr.github.io/hyojin-ai-mvp/"),
            ),
            ("📊 상품 통계", lambda: self.show_item_statistics(payment)),
        ]

        for text, command in actions:
            btn = tk.Button(
                action_frame,
                text=text,
                command=command,
                bg="#2ecc71",
                fg="white",
                font=("Arial", 10),
            )
            btn.pack(side=tk.LEFT, padx=5)

        # 레이아웃
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_info_section(self, parent, title, items):
        """정보 섹션 생성"""
        frame = tk.LabelFrame(
            parent, text=title, font=("Arial", 12, "bold"), bg="#ecf0f1", fg="#2c3e50"
        )
        frame.pack(fill=tk.X, padx=20, pady=10)

        for label, value in items:
            row = tk.Frame(frame, bg="#ecf0f1")
            row.pack(fill=tk.X, padx=10, pady=2)

            tk.Label(
                row,
                text=f"{label}:",
                font=("Arial", 10, "bold"),
                bg="#ecf0f1",
                fg="#34495e",
                width=15,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                row,
                text=str(value),
                font=("Arial", 10),
                bg="#ecf0f1",
                fg="#2c3e50",
                anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X)

    def save_payment_notes(self, payment_id, notes):
        """결제 메모 저장"""
        payments = self.db.get_all_payments()
        payment = next((p for p in payments if p["id"] == payment_id), None)

        if payment:
            if self.db.update_payment_status(payment_id, payment["status"], notes):
                messagebox.showinfo("성공", "메모가 저장되었습니다.")
                self.refresh_payments()
            else:
                messagebox.showerror("오류", "메모 저장에 실패했습니다.")

    def change_payment_status(self, new_status):
        """결제 상태 변경"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "결제 항목을 선택해주세요.")
            return

        item = self.tree.item(selection[0])
        payment_id = int(item["values"][0])  # 정수로 변환

        if self.db.update_payment_status(payment_id, new_status):
            messagebox.showinfo("성공", f"상태가 '{new_status}'로 변경되었습니다.")
            self.refresh_payments()
        else:
            messagebox.showerror("오류", "상태 변경에 실패했습니다.")

    def refresh_payments(self):
        """결제 목록 새로고침"""
        self.load_payments()
        messagebox.showinfo("새로고침", "결제 목록이 업데이트되었습니다.")

    def add_test_order(self):
        """테스트 주문 추가"""
        test_data = {
            "subscription_id": f"sub_test_{int(time.time())}",
            "customer_name": "테스트 고객",
            "customer_email": "test@example.com",
            "customer_company": "테스트 회사",
            "payment_method": "card",
            "total_amount": 299.0,
            "status": "pending",
            "items": [
                {
                    "id": "medical-ai",
                    "name": "의료 AI 도메인",
                    "type": "domain",
                    "price": 199,
                },
                {
                    "id": "medical-doctor-ai",
                    "name": "닥터 김 AI",
                    "type": "agent",
                    "price": 89,
                },
            ],
        }

        if self.db.add_payment(test_data):
            messagebox.showinfo("성공", "테스트 주문이 추가되었습니다.")
            self.refresh_payments()
        else:
            messagebox.showerror("오류", "테스트 주문 추가에 실패했습니다.")

    def show_statistics(self):
        """통계 창 표시"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 결제 통계")
        stats_window.geometry("800x600")
        stats_window.configure(bg="#ecf0f1")

        # 통계 계산
        payments = self.db.get_all_payments()

        # 월별 매출
        monthly_revenue = {}
        for payment in payments:
            if payment["status"] in ["active", "pending"]:
                month = payment["created_at"][:7]  # YYYY-MM
                monthly_revenue[month] = (
                    monthly_revenue.get(month, 0) + payment["total_amount"]
                )

        # 결제 방법별 통계
        payment_methods = {}
        for payment in payments:
            method = payment["payment_method"]
            payment_methods[method] = payment_methods.get(method, 0) + 1

        # 상품 타입별 통계
        item_types = {}
        for payment in payments:
            for item in payment["items"]:
                item_type = item["type"]
                item_types[item_type] = item_types.get(item_type, 0) + 1

        # 통계 표시
        tk.Label(
            stats_window,
            text="📊 HYOJIN.AI 결제 통계",
            font=("Arial", 16, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # 월별 매출
        self.create_stats_section(stats_window, "월별 매출", monthly_revenue)
        self.create_stats_section(stats_window, "결제 방법별", payment_methods)
        self.create_stats_section(stats_window, "상품 타입별", item_types)

    def create_stats_section(self, parent, title, data):
        """통계 섹션 생성"""
        frame = tk.LabelFrame(parent, text=title, font=("Arial", 12, "bold"))
        frame.pack(fill=tk.X, padx=20, pady=10)

        for key, value in data.items():
            row = tk.Frame(frame)
            row.pack(fill=tk.X, padx=10, pady=2)

            tk.Label(row, text=f"{key}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            tk.Label(row, text=str(value), font=("Arial", 10)).pack(side=tk.RIGHT)

    def export_data(self):
        """데이터 내보내기"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if filename:
            payments = self.db.get_all_payments()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(payments, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("성공", f"데이터가 {filename}에 저장되었습니다.")

    def send_email_to_customer(self, payment):
        """고객에게 이메일 보내기"""
        if not EMAIL_AVAILABLE:
            messagebox.showinfo("이메일", "이메일 기능이 비활성화되어 있습니다.")
            return

        # 간단한 이메일 클라이언트 열기
        subject = f"HYOJIN.AI 구독 서비스 - {payment['subscription_id']}"
        body = f"""안녕하세요 {payment['customer_name']}님,

HYOJIN.AI 구독 서비스에 대해 문의주셔서 감사합니다.

구독 정보:
- 구독 ID: {payment['subscription_id']}
- 결제 금액: ${payment['total_amount']}
- 상태: {payment['status']}

문의사항이 있으시면 언제든 연락해주세요.

감사합니다.
HYOJIN.AI 팀"""

        webbrowser.open(
            f"mailto:{payment['customer_email']}?subject={subject}&body={body}"
        )

    def show_item_statistics(self, payment):
        """상품 통계 표시"""
        messagebox.showinfo(
            "상품 통계",
            f"주문 상품 수: {len(payment['items'])}\n"
            + "\n".join(
                [f"• {item['name']}: ${item['price']}" for item in payment["items"]]
            ),
        )

    def show_settings(self):
        """설정 창 표시"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ 설정")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#ecf0f1")

        tk.Label(
            settings_window,
            text="⚙️ 애플리케이션 설정",
            font=("Arial", 16, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # 자동 새로고침 설정
        auto_refresh_frame = tk.Frame(settings_window, bg="#ecf0f1")
        auto_refresh_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            auto_refresh_frame, text="자동 새로고침 간격 (초):", bg="#ecf0f1"
        ).pack(side=tk.LEFT)
        refresh_entry = tk.Entry(auto_refresh_frame, width=10)
        refresh_entry.pack(side=tk.LEFT, padx=10)
        refresh_entry.insert(0, "30")

        # 데이터베이스 경로
        db_frame = tk.Frame(settings_window, bg="#ecf0f1")
        db_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(db_frame, text="데이터베이스 경로:", bg="#ecf0f1").pack(anchor="w")
        tk.Label(db_frame, text=self.db.db_path, bg="#ecf0f1", fg="#7f8c8d").pack(
            anchor="w"
        )

        # 버전 정보
        version_frame = tk.Frame(settings_window, bg="#ecf0f1")
        version_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(
            version_frame,
            text="HYOJIN.AI 결제 관리 시스템 v1.0",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
        ).pack()
        tk.Label(
            version_frame,
            text="© 2024 HYOJIN.AI",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
        ).pack()

    def start_auto_refresh(self):
        """자동 새로고침 시작"""

        def auto_refresh():
            while True:
                time.sleep(30)  # 30초마다 새로고침
                try:
                    self.root.after(0, self.load_payments)
                except:
                    break

        refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
        refresh_thread.start()

    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()


if __name__ == "__main__":
    app = PaymentManagerApp()
    app.run()
