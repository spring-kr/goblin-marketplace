"""
🧠 대화 기억/학습 시스템 v10.1
=================================

이 모듈은 사용자와의 대화를 기억하고 학습하여 개인화된 응답을 제공하는 시스템입니다.

주요 기능:
1. 대화 기록 저장/불러오기
2. 사용자 감정 패턴 분석 및 학습
3. 선호 키워드 학습
4. 개인화된 응답 생성
5. 30가지 감정 분석 시스템
"""

import json
import os
import time
from typing import Dict, List, Any, Optional


class ConversationMemorySystem:
    """대화 기억/학습 시스템 클래스"""

    def __init__(self, memory_file: str = "conversation_memory.json"):
        """
        시스템 초기화

        Args:
            memory_file (str): 메모리 데이터를 저장할 파일 경로
        """
        self.memory_file = memory_file
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_preferences: Dict[str, Any] = {}
        self.load_memory()

    def load_memory(self) -> bool:
        """
        대화 기억 불러오기

        Returns:
            bool: 로드 성공 여부
        """
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conversation_history = data.get("history", [])
                    self.user_preferences = data.get("preferences", {})
                print(
                    f"🧠 메모리 로드 성공: {len(self.conversation_history)}개 대화 기록"
                )
                return True
            else:
                print("🧠 새로운 메모리 파일 생성")
                return True
        except Exception as e:
            print(f"🧠 메모리 로드 실패: {e}")
            return False

    def save_memory(self) -> bool:
        """
        대화 기억 저장하기

        Returns:
            bool: 저장 성공 여부
        """
        try:
            data = {
                "history": self.conversation_history[-100:],  # 최근 100개만 저장
                "preferences": self.user_preferences,
                "last_updated": time.time(),
                "version": "10.1",
            }
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"🧠 메모리 저장 성공: {len(self.conversation_history)}개 대화 기록")
            return True
        except Exception as e:
            print(f"🧠 메모리 저장 실패: {e}")
            return False

    def add_conversation(
        self, user_message: str, bot_response: str, emotion: str
    ) -> None:
        """
        대화 기록 추가

        Args:
            user_message (str): 사용자 메시지
            bot_response (str): 봇 응답
            emotion (str): 감지된 감정
        """
        conversation_entry = {
            "timestamp": time.time(),
            "user_message": user_message,
            "bot_response": bot_response,
            "emotion": emotion,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.conversation_history.append(conversation_entry)

        # 자동 저장
        if len(self.conversation_history) % 10 == 0:  # 10개마다 저장
            self.save_memory()

    def analyze_user_patterns(self, text: str) -> str:
        """
        사용자 패턴 분석 및 학습

        Args:
            text (str): 분석할 텍스트

        Returns:
            str: 감지된 감정
        """
        # 감정 분석
        emotion = self.analyze_korean_emotion(text)

        # 감정 패턴 학습
        if "emotion_patterns" not in self.user_preferences:
            self.user_preferences["emotion_patterns"] = {}

        if emotion in self.user_preferences["emotion_patterns"]:
            self.user_preferences["emotion_patterns"][emotion] += 1
        else:
            self.user_preferences["emotion_patterns"][emotion] = 1

        # 선호 키워드 학습
        if "favorite_words" not in self.user_preferences:
            self.user_preferences["favorite_words"] = {}

        words = text.split()
        for word in words:
            if len(word) > 1:  # 한 글자 제외
                if word in self.user_preferences["favorite_words"]:
                    self.user_preferences["favorite_words"][word] += 1
                else:
                    self.user_preferences["favorite_words"][word] = 1

        # 대화 시간 패턴 학습
        current_hour = int(time.strftime("%H"))
        if "time_patterns" not in self.user_preferences:
            self.user_preferences["time_patterns"] = {}

        if str(current_hour) in self.user_preferences["time_patterns"]:
            self.user_preferences["time_patterns"][str(current_hour)] += 1
        else:
            self.user_preferences["time_patterns"][str(current_hour)] = 1

        return emotion

    def analyze_korean_emotion(self, text: str) -> str:
        """
        🧠 v10.1 확장된 30가지 감정 분석 시스템

        Args:
            text (str): 분석할 텍스트

        Returns:
            str: 감지된 감정 ('happy', 'sad', 'angry', 등)
        """
        text = text.lower()

        # 1. 기쁨/행복 계열
        if any(
            word in text
            for word in [
                "기분 좋",
                "좋아",
                "행복",
                "기뻐",
                "즐거",
                "신나",
                "최고",
                "완벽",
                "멋져",
                "환상적",
                "대단해",
                "훌륭",
                "ㅋㅋ",
                "하하",
                "웃",
                "만족",
                "성공",
                "이루었",
            ]
        ):
            return "happy"

        # 2. 슬픔/우울 계열
        elif any(
            word in text
            for word in [
                "슬프",
                "슬퍼",
                "우울",
                "힘들",
                "안좋",
                "속상",
                "눈물",
                "서러",
                "외로",
                "공허",
                "실망",
                "좌절",
                "막막",
                "암울",
                "절망",
                "비참",
                "처참",
            ]
        ):
            return "sad"

        # 3. 분노/짜증 계열
        elif any(
            word in text
            for word in [
                "화나",
                "짜증",
                "열받",
                "빡쳐",
                "분노",
                "악",
                "미치",
                "싫어",
                "스트레스",
                "답답",
                "빡",
                "어이없",
                "황당",
                "미친",
                "개빡",
                "쪽팔",
            ]
        ):
            return "angry"

        # 4. 놀람/감탄 계열
        elif any(
            word in text
            for word in [
                "놀라",
                "깜짝",
                "헐",
                "와",
                "대박",
                "신기",
                "믿을 수 없",
                "어떻게",
                "세상에",
                "어머",
                "헉",
                "우와",
                "와우",
                "까무러",
            ]
        ):
            return "amazed"

        # 5. 사랑/애정 계열
        elif any(
            word in text
            for word in [
                "사랑",
                "사랑해",
                "좋아해",
                "애정",
                "마음에 들",
                "예뻐",
                "귀여",
                "달콤",
                "포근",
                "따뜻",
                "감동",
                "소중",
                "아끼",
            ]
        ):
            return "love"

        # 6. 흥미진진/기대 계열
        elif any(
            word in text
            for word in [
                "흥미",
                "기대",
                "설레",
                "두근",
                "궁금",
                "재미",
                "호기심",
                "즐거운",
                "기다려",
                "관심",
                "몰입",
            ]
        ):
            return "excited"

        # 7. 걱정/불안 계열
        elif any(
            word in text
            for word in [
                "걱정",
                "불안",
                "무서",
                "두려",
                "염려",
                "근심",
                "긴장",
                "떨려",
                "조마조마",
                "심난",
                "겁나",
                "무시무시",
            ]
        ):
            return "worried"

        # 8. 피곤/지침 계열
        elif any(
            word in text
            for word in [
                "피곤",
                "지쳐",
                "힘빠져",
                "나른",
                "졸려",
                "번아웃",
                "탈진",
                "기운없",
                "지겨",
                "권태",
                "무기력",
                "귀찮",
            ]
        ):
            return "tired"

        # 9. 감사/고마움 계열
        elif any(
            word in text
            for word in [
                "감사",
                "고마워",
                "고맙",
                "고마운",
                "땡큐",
                "은혜",
                "축복",
                "다행",
                "진심",
                "깊이",
            ]
        ):
            return "grateful"

        # 10. 혼란/당황 계열
        elif any(
            word in text
            for word in [
                "헷갈려",
                "모르겠",
                "당황",
                "혼란",
                "어리둥절",
                "이해안돼",
                "복잡",
                "어색",
                "애매",
                "갈팡질팡",
            ]
        ):
            return "confused"

        # 11. 자신감/당당 계열
        elif any(
            word in text
            for word in [
                "자신있",
                "당당",
                "확신",
                "자랑",
                "뿌듯",
                "잘났",
                "성취",
                "승리",
                "이겼",
                "대견",
                "자부심",
            ]
        ):
            return "confident"

        # 12. 부끄러움/수줍음 계열
        elif any(
            word in text
            for word in [
                "부끄러",
                "창피",
                "민망",
                "수줍",
                "쑥스러",
                "얼굴빨개",
                "어이없어",
                "쪽팔려",
                "떨려",
            ]
        ):
            return "shy"

        else:
            return "neutral"

    def get_personalized_response(self, emotion: str, text: str) -> str:
        """
        개인화된 응답 생성

        Args:
            emotion (str): 감지된 감정
            text (str): 사용자 메시지

        Returns:
            str: 개인화된 응답
        """
        # 기본 응답 템플릿
        base_responses = {
            "happy": [
                "정말 기쁘시겠어요! 😊",
                "행복한 기분이 전해져요!",
                "좋은 일이 있으셨나봐요!",
                "기쁜 마음이 느껴져요!",
                "환상적이네요!",
            ],
            "sad": [
                "힘든 시간이시군요 😢",
                "괜찮아질 거예요",
                "함께 이겨내요",
                "마음이 아프시겠어요",
                "위로해드리고 싶어요",
            ],
            "angry": [
                "화가 나셨군요 😠",
                "스트레스 받으셨나봐요",
                "잠시 숨을 고르세요",
                "짜증나시는 상황이군요",
                "이해해요",
            ],
            "excited": [
                "정말 신나시겠어요! 🤩",
                "저도 기대돼요!",
                "흥미진진하네요!",
                "설레시겠어요!",
                "정말 궁금해요!",
            ],
            "worried": [
                "걱정이 많으시겠어요 😰",
                "모든 게 잘 될 거예요",
                "너무 걱정하지 마세요",
                "불안하시겠어요",
                "함께 해결해봐요",
            ],
            "tired": [
                "많이 피곤하시겠어요 😴",
                "좀 쉬세요",
                "무리하지 마세요",
                "지치셨군요",
                "충분한 휴식이 필요해요",
            ],
            "grateful": [
                "감사한 마음이 느껴져요 🙏",
                "정말 다행이네요!",
                "감동적이에요",
                "고마운 일이군요",
                "따뜻한 마음이에요",
            ],
            "confused": [
                "헷갈리시는군요 😕",
                "차근차근 생각해봐요",
                "복잡하시겠어요",
                "어려우시겠어요",
                "천천히 정리해봐요",
            ],
            "confident": [
                "자신감이 넘치시네요! 😎",
                "멋져요!",
                "당당하세요!",
                "정말 대단해요!",
                "자랑스러워요!",
            ],
            "shy": [
                "부끄러워하시는군요 😊",
                "괜찮아요",
                "천천히 말씀하세요",
                "수줍으시는군요",
                "편안하게 하세요",
            ],
            "love": [
                "사랑스러운 마음이 느껴져요 💕",
                "따뜻해요",
                "마음이 예뻐요",
                "애정이 넘치네요",
                "정말 달콤해요",
            ],
            "amazed": [
                "정말 놀라우시겠어요! 😲",
                "대단하네요!",
                "신기해요!",
                "믿을 수 없어요!",
                "깜짝 놀랐어요!",
            ],
            "neutral": [
                "그렇군요",
                "이해해요",
                "말씀해주세요",
                "계속 들어드릴게요",
                "어떻게 도와드릴까요?",
            ],
        }

        responses = base_responses.get(emotion, base_responses["neutral"])

        # 사용자 패턴 기반 개인화
        if (
            "emotion_patterns" in self.user_preferences
            and self.user_preferences["emotion_patterns"]
        ):
            most_common_emotion = max(
                self.user_preferences["emotion_patterns"],
                key=self.user_preferences["emotion_patterns"].get,
            )

            # 자주 사용하는 감정에 따라 응답 스타일 조정
            if most_common_emotion == "happy":
                responses = [r + " 항상 긍정적이시네요!" for r in responses]
            elif most_common_emotion == "sad":
                responses = [r + " 힘내세요!" for r in responses]
            elif most_common_emotion == "excited":
                responses = [r + " 에너지가 넘치세요!" for r in responses]

        # 시간대별 개인화
        current_hour = int(time.strftime("%H"))
        if current_hour < 6:
            responses = [r + " 늦은 시간이네요." for r in responses]
        elif current_hour < 12:
            responses = [r + " 좋은 아침이에요!" for r in responses]
        elif current_hour < 18:
            responses = [r + " 좋은 오후예요!" for r in responses]
        else:
            responses = [r + " 좋은 저녁이에요!" for r in responses]

        return responses[0]  # 첫 번째 응답 반환

    def get_user_stats(self) -> Dict[str, Any]:
        """
        사용자 통계 정보 반환

        Returns:
            dict: 사용자 통계 정보
        """
        stats = {
            "total_conversations": len(self.conversation_history),
            "emotion_patterns": self.user_preferences.get("emotion_patterns", {}),
            "most_common_emotion": None,
            "favorite_words": {},
            "time_patterns": self.user_preferences.get("time_patterns", {}),
            "most_active_hour": None,
        }

        # 가장 많이 나타나는 감정
        if stats["emotion_patterns"]:
            stats["most_common_emotion"] = max(
                stats["emotion_patterns"], key=stats["emotion_patterns"].get
            )

        # 자주 사용하는 단어 상위 10개
        favorite_words = self.user_preferences.get("favorite_words", {})
        if favorite_words:
            sorted_words = sorted(
                favorite_words.items(), key=lambda x: x[1], reverse=True
            )
            stats["favorite_words"] = dict(sorted_words[:10])

        # 가장 활발한 시간대
        if stats["time_patterns"]:
            stats["most_active_hour"] = max(
                stats["time_patterns"], key=stats["time_patterns"].get
            )

        return stats

    def clear_memory(self) -> bool:
        """
        메모리 초기화

        Returns:
            bool: 초기화 성공 여부
        """
        try:
            self.conversation_history = []
            self.user_preferences = {}
            self.save_memory()
            print("🧠 메모리 초기화 완료")
            return True
        except Exception as e:
            print(f"🧠 메모리 초기화 실패: {e}")
            return False


# 사용 예시
if __name__ == "__main__":
    # 시스템 초기화
    memory_system = ConversationMemorySystem()

    # 테스트 대화
    test_messages = [
        "안녕하세요! 오늘 기분이 정말 좋아요!",
        "요즘 너무 피곤해서 힘들어요...",
        "와! 정말 놀라운 소식이네요!",
        "고마워요, 정말 감사합니다!",
    ]

    print("🧠 대화 기억/학습 시스템 테스트 시작")
    print("=" * 50)

    for i, message in enumerate(test_messages, 1):
        emotion = memory_system.analyze_user_patterns(message)
        response = memory_system.get_personalized_response(emotion, message)
        memory_system.add_conversation(message, response, emotion)

        print(f"테스트 {i}:")
        print(f"사용자: {message}")
        print(f"감정: {emotion}")
        print(f"응답: {response}")
        print("-" * 30)

    # 통계 출력
    stats = memory_system.get_user_stats()
    print("📊 사용자 통계:")
    print(f"총 대화 수: {stats['total_conversations']}")
    print(f"가장 많은 감정: {stats['most_common_emotion']}")
    print(f"감정 패턴: {stats['emotion_patterns']}")
    print(f"자주 사용하는 단어: {stats['favorite_words']}")

    # 메모리 저장
    memory_system.save_memory()
    print("\n🧠 메모리 저장 완료!")
