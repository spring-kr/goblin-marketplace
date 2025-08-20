"""
📊 사용량 추적 및 통계 시스템
베타 서비스 사용 패턴 분석용
"""

import json
import datetime
import os
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter


class UsageTracker:
    def __init__(self, log_file="usage_log.json"):
        self.log_file = log_file
        self.ensure_log_file()

    def ensure_log_file(self):
        """로그 파일 초기화"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def log_usage(self, agent_type: str, question: str, response_success: bool = True, user_ip: Optional[str] = None):
        """사용량 로그 기록"""
        try:
            # 기존 로그 읽기
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)

            # 새 로그 엔트리
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "agent_type": agent_type,
                "question_length": len(question),
                "question_preview": question[:50] + "..." if len(question) > 50 else question,
                "response_success": response_success,
                "user_ip": user_ip,
                "weekday": datetime.datetime.now().strftime("%A"),
                "hour": datetime.datetime.now().hour
            }

            logs.append(log_entry)

            # 로그 저장 (최대 1000개 유지)
            if len(logs) > 1000:
                logs = logs[-1000:]

            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"로그 기록 오류: {e}")

    def get_statistics(self, days: int = 7) -> Dict[str, Any]:
        """사용 통계 생성"""
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)

            # 날짜 필터링
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
            recent_logs = [
                log for log in logs 
                if datetime.datetime.fromisoformat(log["timestamp"]) >= cutoff_date
            ]

            if not recent_logs:
                return {"message": "아직 사용 데이터가 없습니다.", "total_usage": 0}

            # 기본 통계
            total_usage = len(recent_logs)
            success_rate = sum(1 for log in recent_logs if log["response_success"]) / total_usage * 100

            # 에이전트별 사용량
            agent_usage = Counter(log["agent_type"] for log in recent_logs)
            
            # 시간대별 사용량
            hourly_usage = Counter(log["hour"] for log in recent_logs)
            
            # 요일별 사용량
            weekday_usage = Counter(log["weekday"] for log in recent_logs)
            
            # 일별 사용량
            daily_usage = Counter(log["date"] for log in recent_logs)

            # 에이전트 이름 매핑
            agent_names = {
                "math": "🧮 수학 도깨비",
                "physics": "⚛️ 물리학 도깨비", 
                "chemistry": "🧪 화학 도깨비",
                "biology": "🧬 생물학 도깨비",
                "engineering": "⚙️ 공학 도깨비",
                "assistant": "🤖 업무 도우미 도깨비",
                "marketing": "📈 마케팅 도깨비",
                "startup": "🚀 스타트업 도깨비"
            }

            return {
                "period": f"최근 {days}일",
                "total_usage": total_usage,
                "success_rate": round(success_rate, 1),
                "agent_usage": {agent_names.get(k, k): v for k, v in agent_usage.most_common()},
                "hourly_usage": dict(sorted(hourly_usage.items())),
                "weekday_usage": dict(weekday_usage.most_common()),
                "daily_usage": dict(sorted(daily_usage.items(), reverse=True)[:7]),
                "average_question_length": round(
                    sum(log["question_length"] for log in recent_logs) / total_usage, 1
                ),
                "peak_hour": max(hourly_usage, key=hourly_usage.get) if hourly_usage else "없음",
                "most_popular_agent": agent_names.get(
                    max(agent_usage, key=agent_usage.get), "없음"
                ) if agent_usage else "없음"
            }

        except Exception as e:
            return {"error": f"통계 생성 오류: {e}"}

    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """최근 활동 조회"""
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
            
            # 최근 활동만 반환
            recent = logs[-limit:] if len(logs) >= limit else logs
            recent.reverse()  # 최신순 정렬
            
            return recent

        except Exception as e:
            return [{"error": f"최근 활동 조회 오류: {e}"}]

    def export_statistics(self) -> str:
        """통계를 텍스트로 내보내기"""
        stats = self.get_statistics()
        
        if "error" in stats:
            return f"통계 오류: {stats['error']}"
        
        if "message" in stats:
            return stats["message"]
        
        report = f"""
📊 AI 도깨비마을 STEM 센터 사용 통계 리포트
생성일시: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
기간: {stats['period']}

🎯 전체 현황
- 총 사용량: {stats['total_usage']}회
- 성공률: {stats['success_rate']}%
- 평균 질문 길이: {stats['average_question_length']}자
- 가장 인기 있는 에이전트: {stats['most_popular_agent']}
- 피크 시간대: {stats['peak_hour']}시

👥 에이전트별 사용량:
"""
        
        for agent, count in stats['agent_usage'].items():
            percentage = round(count / stats['total_usage'] * 100, 1)
            report += f"  {agent}: {count}회 ({percentage}%)\n"
        
        report += f"""
📅 일별 사용량:
"""
        for date, count in stats['daily_usage'].items():
            report += f"  {date}: {count}회\n"
        
        report += f"""
🕐 시간대별 사용량:
"""
        for hour, count in stats['hourly_usage'].items():
            report += f"  {hour:02d}시: {count}회\n"
        
        return report


# 전역 인스턴스
usage_tracker = UsageTracker()
