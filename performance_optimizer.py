"""
성능 최적화 모듈
- 응답 캐싱
- 메모리 관리
- 응답 시간 단축
"""

import time
import json
import hashlib
from functools import wraps
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class ResponseCache:
    """응답 캐싱 시스템"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

    def _generate_key(self, user_message: str, expert_type: str) -> str:
        """캐시 키 생성"""
        content = f"{user_message}:{expert_type}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, user_message: str, expert_type: str) -> Optional[str]:
        """캐시에서 응답 조회"""
        key = self._generate_key(user_message, expert_type)

        if key in self.cache:
            cache_entry = self.cache[key]

            # TTL 체크
            if datetime.now() < cache_entry["expires_at"]:
                cache_entry["hits"] += 1
                return cache_entry["response"]
            else:
                # 만료된 캐시 삭제
                del self.cache[key]

        return None

    def set(self, user_message: str, expert_type: str, response: str):
        """캐시에 응답 저장"""
        key = self._generate_key(user_message, expert_type)

        # 캐시 크기 제한
        if len(self.cache) >= self.max_size:
            self._evict_oldest()

        self.cache[key] = {
            "response": response,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(seconds=self.ttl_seconds),
            "hits": 0,
        }

    def _evict_oldest(self):
        """가장 오래된 캐시 엔트리 제거"""
        if not self.cache:
            return

        # 히트 수가 가장 적은 것부터 제거
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: (self.cache[k]["hits"], self.cache[k]["created_at"]),
        )
        del self.cache[oldest_key]

    def get_stats(self) -> Dict[str, Any]:
        """캐시 통계 반환"""
        total_hits = sum(entry["hits"] for entry in self.cache.values())
        return {
            "cache_size": len(self.cache),
            "total_hits": total_hits,
            "avg_hits_per_entry": total_hits / len(self.cache) if self.cache else 0,
        }


class PerformanceMonitor:
    """성능 모니터링"""

    def __init__(self):
        self.response_times = []
        self.cache_hits = 0
        self.cache_misses = 0

    def record_response_time(self, response_time: float):
        """응답 시간 기록"""
        self.response_times.append(response_time)

        # 최근 100개만 유지
        if len(self.response_times) > 100:
            self.response_times.pop(0)

    def record_cache_hit(self):
        """캐시 히트 기록"""
        self.cache_hits += 1

    def record_cache_miss(self):
        """캐시 미스 기록"""
        self.cache_misses += 1

    def get_stats(self) -> Dict[str, Any]:
        """성능 통계 반환"""
        if not self.response_times:
            return {
                "avg_response_time": 0,
                "min_response_time": 0,
                "max_response_time": 0,
                "cache_hit_rate": 0,
            }

        total_requests = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0

        return {
            "avg_response_time": sum(self.response_times) / len(self.response_times),
            "min_response_time": min(self.response_times),
            "max_response_time": max(self.response_times),
            "total_requests": total_requests,
            "cache_hit_rate": cache_hit_rate * 100,
        }


# 전역 인스턴스
_response_cache = ResponseCache()
_performance_monitor = PerformanceMonitor()


def cached_response(func):
    """응답 캐싱 데코레이터"""

    @wraps(func)
    def wrapper(self, user_message: str, expert_type: str) -> str:
        start_time = time.time()

        # 캐시에서 조회
        cached_result = _response_cache.get(user_message, expert_type)
        if cached_result:
            _performance_monitor.record_cache_hit()
            response_time = time.time() - start_time
            _performance_monitor.record_response_time(response_time)
            return cached_result

        # 캐시 미스 - 실제 응답 생성
        _performance_monitor.record_cache_miss()
        result = func(self, user_message, expert_type)

        # 캐시에 저장
        _response_cache.set(user_message, expert_type, result)

        response_time = time.time() - start_time
        _performance_monitor.record_response_time(response_time)

        return result

    return wrapper


def get_performance_stats() -> Dict[str, Any]:
    """전체 성능 통계 반환"""
    cache_stats = _response_cache.get_stats()
    monitor_stats = _performance_monitor.get_stats()

    return {
        "timestamp": datetime.now().isoformat(),
        "cache": cache_stats,
        "performance": monitor_stats,
    }


def clear_cache():
    """캐시 초기화"""
    global _response_cache
    _response_cache = ResponseCache()


class OptimizedResponseGenerator:
    """최적화된 응답 생성기"""

    def __init__(self):
        self.common_patterns = {
            "investment": ["투자", "주식", "청약", "포트폴리오", "수익률"],
            "medical": ["당뇨", "혈압", "갱년기", "건강", "치료"],
            "ai": ["AI", "머신러닝", "딥러닝", "GPT", "Claude"],
            "legal": ["법률", "계약", "임대차", "권리", "소송"],
        }

    def detect_expert_type_fast(self, user_message: str) -> str:
        """빠른 전문가 타입 감지"""
        message_lower = user_message.lower()

        scores = {}
        for expert_type, keywords in self.common_patterns.items():
            score = sum(1 for keyword in keywords if keyword.lower() in message_lower)
            scores[expert_type] = score

        # 가장 높은 점수의 전문가 타입 반환
        if scores:
            best_match = max(scores, key=scores.get)
            if scores[best_match] > 0:
                return best_match

        return "general"  # 기본값


# 싱글톤 인스턴스
_optimizer = OptimizedResponseGenerator()


def get_optimizer() -> OptimizedResponseGenerator:
    """최적화기 인스턴스 반환"""
    return _optimizer
