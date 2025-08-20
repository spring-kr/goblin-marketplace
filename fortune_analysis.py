"""운세 분석을 위한 유틸리티 모듈"""

import random
from datetime import datetime


class FortuneAnalysis:
    @staticmethod
    def get_love_fortune(current_time: datetime) -> dict:
        """연애운 분석 - 시간과 상황에 따른 맥락적 해석 제공"""
        hour = current_time.hour
        weekday = current_time.weekday()
        month = current_time.month

        # 계절과 시간대를 고려한 운세 분석
        season_contexts = {
            (12, 1, 2): {"mood": "따뜻한 실내에서", "activity": "차분한 대화가"},
            (3, 4, 5): {"mood": "봄기운 가득한 곳에서", "activity": "새로운 시작이"},
            (6, 7, 8): {"mood": "시원한 카페에서", "activity": "활기찬 만남이"},
            (9, 10, 11): {"mood": "선선한 야외에서", "activity": "진지한 대화가"},
        }

        # 현재 계절 컨텍스트 가져오기
        current_season = next(
            (
                season
                for season, months in {
                    "winter": (12, 1, 2),
                    "spring": (3, 4, 5),
                    "summer": (6, 7, 8),
                    "fall": (9, 10, 11),
                }.items()
                if current_time.month in months
            ),
            "winter",
        )

        # 시간대별 세부 컨텍스트
        time_contexts = {
            "morning": {
                "energy": "상쾌한 에너지로",
                "opportunity": "새로운 인연을 만날 수 있는",
                "mood": "활기찬",
            },
            "afternoon": {
                "energy": "평온한 분위기에서",
                "opportunity": "편안한 대화가 이어지는",
                "mood": "안정적인",
            },
            "evening": {
                "energy": "로맨틱한 분위기에서",
                "opportunity": "특별한 만남이 기대되는",
                "mood": "낭만적인",
            },
        }

        # 시간대 결정
        if 5 <= hour <= 11:
            time_context = time_contexts["morning"]
        elif 12 <= hour <= 17:
            time_context = time_contexts["afternoon"]
        else:
            time_context = time_contexts["evening"]

        # 상황별 특성 분석
        situation_traits = {
            "소개팅": {
                "focus": "첫인상과 대화",
                "advice": "자연스러운 모습을 보여주세요",
                "key_point": "공통 관심사 찾기",
            },
            "데이트": {
                "focus": "즐거운 시간",
                "advice": "편안한 분위기를 만드세요",
                "key_point": "서로를 이해하기",
            },
            "일상": {
                "focus": "자연스러운 만남",
                "advice": "평소 모습을 보여주세요",
                "key_point": "진정성 있는 소통",
            },
        }

        # 타로 카드와 의미 매칭
        tarot_insights = {
            "연인": {
                "general": "새로운 인연과의 만남",
                "positive": "서로를 이해하고 받아들이는 시기",
                "caution": "성급한 판단은 피하세요",
            },
            "별": {
                "general": "희망적인 만남의 기운",
                "positive": "긍정적인 에너지가 가득한 시기",
                "caution": "현실적인 기대를 유지하세요",
            },
            "태양": {
                "general": "활기찬 대화와 즐거운 시간",
                "positive": "자신감 있는 모습이 매력적인 시기",
                "caution": "상대방의 페이스도 존중하세요",
            },
            "달": {
                "general": "로맨틱한 분위기",
                "positive": "감성적인 교감이 중요한 시기",
                "caution": "감정에 휘둘리지 마세요",
            },
            "운명의 수레바퀴": {
                "general": "의미 있는 인연과의 만남",
                "positive": "인연을 소중히 하는 시기",
                "caution": "조급해하지 마세요",
            },
        }

        chosen_card = random.choice(list(tarot_insights.keys()))
        card_info = tarot_insights[chosen_card]

        return {
            "time_context": time_context,
            "season_context": current_season,
            "situation_traits": random.choice(list(situation_traits.values())),
            "tarot_card": chosen_card,
            "card_insight": card_info,
            "is_weekend": weekday >= 5,
            "energy_flow": random.choice(
                ["상승세", "안정세", "균형잡힌", "변화의", "기회의"]
            ),
        }

    @staticmethod
    def get_business_fortune(current_time: datetime) -> dict:
        """사업운 분석"""
        month = current_time.month
        hour = current_time.hour

        # 계절별 운세
        season_fortunes = {
            "spring": "새로운 시작에 좋은",
            "summer": "적극적인 확장에 유리한",
            "fall": "안정적인 성장이 기대되는",
            "winter": "내실을 다지기 좋은",
        }

        # 현재 계절 확인
        if 3 <= month <= 5:
            season_fortune = season_fortunes["spring"]
        elif 6 <= month <= 8:
            season_fortune = season_fortunes["summer"]
        elif 9 <= month <= 11:
            season_fortune = season_fortunes["fall"]
        else:
            season_fortune = season_fortunes["winter"]

        # 시간대별 운세
        if 9 <= hour <= 11:
            time_fortune = "중요한 결정에 적합한 시간대"
        elif 14 <= hour <= 16:
            time_fortune = "협상과 미팅에 좋은 시간대"
        else:
            time_fortune = "차분한 계획 수립에 좋은 시간대"

        return {
            "season_fortune": season_fortune,
            "time_fortune": time_fortune,
            "prosperity_element": random.choice(["금", "목", "수", "화", "토"]),
        }

    @staticmethod
    def generate_fortune_advice(fortune_type: str, analysis: dict) -> str:
        """운세별 맞춤 조언 생성 - 상황과 맥락을 고려한 통찰력 있는 조언 제공"""
        if fortune_type == "연애운":
            time_ctx = analysis["time_context"]
            card_insight = analysis["card_insight"]
            situation = analysis["situation_traits"]

            return f"""{time_ctx['energy']} 시작되는 지금, 
타로카드 '{analysis['tarot_card']}'는 {card_insight['general']}을 보여줍니다.

특히 주목할 점은 {card_insight['positive']}라는 것입니다.
다만, {card_insight['caution']}

현재 {situation['focus']}에 집중하면 좋겠습니다.
조언 드리자면, {situation['advice']}.
핵심은 {situation['key_point']}입니다."""

        elif fortune_type == "사업운":
            return f"""현재는 {analysis['season_fortune']} 시기입니다.
{analysis['time_fortune']}이며, {analysis['prosperity_element']} 방향으로의 확장이 유리해 보입니다."""

        return "아직 준비되지 않은 운세 유형입니다."
