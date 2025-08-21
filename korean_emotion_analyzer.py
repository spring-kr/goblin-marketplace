"""
🎯 Korean BERT 감정분석 통합 시스템 + 사용자 맞춤형 모델 지원
사용자의 감정을 정확히 분석하여 도깨비들이 맞춤형 응답을 제공하는 시스템
"""

import re
import random
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


class KoreanEmotionAnalyzer:
    """Korean BERT 기반 감정분석기 + 사용자 모델 지원"""

    def __init__(self):
        self.emotion_model = None
        self.tokenizer = None
        self.custom_model = None
        self.emotion_labels = ["기쁨", "슬픔", "분노", "불안", "놀람", "혐오", "중립"]
        self.emotion_intensities = ["낮음", "보통", "높음"]

        # 사용자 맞춤형 모델 우선 로드 시도
        self._init_custom_model()

        # 사용자 모델이 없으면 BERT 모델 시도
        if not self.custom_model:
            self._init_emotion_model()

    def _init_custom_model(self):
        """사용자 맞춤형 모델 초기화"""
        try:
            from custom_emotion_model import CustomEmotionModelLoader
            
            # 모델 경로들 시도 (새 파이프라인 우선)
            model_paths = [
                "./models/korean_emotion_complete_pipeline.pkl",  # 새로 생성된 파이프라인
                "./models/korean_bert_emotion_pipeline.pkl",  # 대체 파이프라인
                "./models/korean_bert_emotion.pkl",  # 기존 모델
                "./models/",  # 디렉토리 경로
                "./models/trained_models/",  # 훈련된 모델 디렉토리
            ]
            
            for model_path in model_paths:
                try:
                    print(f"🔍 모델 로드 시도: {model_path}")
                    loader = CustomEmotionModelLoader(model_path)
                    if loader.is_loaded:
                        self.custom_model = loader
                        print(f"✅ 사용자 맞춤형 감정분석 모델 로드 성공! ({model_path})")
                        return True
                except Exception as e:
                    print(f"⚠️ {model_path} 로드 실패: {e}")
                    continue
            
            print("⚠️ 사용자 모델 없음, 기본 모델 사용")
            return False
            
        except ImportError:
            print("⚠️ 사용자 모델 로더 없음")
            return False

    def _init_emotion_model(self):
        """감정분석 모델 초기화 (BERT 백업)"""
        try:
            # Korean BERT 모델 로드 시도 (transformers가 있는 경우에만)
            try:
                import torch
                from transformers import (
                    AutoTokenizer,
                    AutoModelForSequenceClassification,
                )

                # 한국어 감정분석 모델 (예시: monologg/kobert)
                model_name = "monologg/kobert"  # 또는 다른 한국어 감정분석 모델

                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.emotion_model = AutoModelForSequenceClassification.from_pretrained(
                    model_name
                )
                print("✅ Korean BERT 감정분석 모델 로드 성공!")
            except Exception as e:
                print(f"⚠️ BERT 모델 로드 실패, 규칙기반 분석 사용: {e}")
                self.emotion_model = None

        except ImportError:
            print("⚠️ transformers 라이브러리 없음, 규칙기반 감정분석 사용")
            self.emotion_model = None

    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """텍스트의 감정을 분석 (사용자 모델 우선)"""
        # 1. 사용자 맞춤형 모델 우선 사용
        if self.custom_model and self.custom_model.is_loaded:
            try:
                result = self.custom_model.predict_emotion(text)
                print(f"🎯 사용자 모델 사용: {result.get('analysis_method', 'Custom')}")
                
                # 반환 값 구조 통일
                return {
                    "emotion": result.get("primary_emotion", result.get("emotion", "중립")),
                    "confidence": result.get("confidence", 0.5),
                    "intensity": result.get("intensity", "보통"),
                    "method": result.get("analysis_method", "Custom_Model"),
                    "emotion_scores": result.get("all_emotions", result.get("emotion_scores", {}))
                }
            except Exception as e:
                print(f"⚠️ 사용자 모델 실패, 백업 모델 사용: {e}")

        # 2. BERT 모델 사용
        if self.emotion_model and self.tokenizer:
            try:
                result = self._bert_emotion_analysis(text)
                return {
                    "emotion": result.get("primary_emotion", "중립"),
                    "confidence": result.get("confidence", 0.5),
                    "intensity": result.get("intensity", "보통"),
                    "method": result.get("analysis_method", "BERT"),
                    "emotion_scores": result.get("all_emotions", {})
                }
            except Exception as e:
                print(f"⚠️ BERT 모델 실패, 규칙 기반 사용: {e}")

        # 3. 최종 백업: 규칙 기반 분석
        result = self._rule_based_emotion_analysis(text)
        return {
            "emotion": result.get("primary_emotion", "중립"),
            "confidence": result.get("confidence", 0.5),
            "intensity": result.get("intensity", "보통"),
            "method": result.get("analysis_method", "Rule_Based"),
            "emotion_scores": result.get("all_emotions", {})
        }

    def _bert_emotion_analysis(self, text: str) -> Dict[str, Any]:
        """BERT 모델을 사용한 고급 감정분석"""
        try:
            import torch

            # 토큰화 및 예측 수행
            if self.tokenizer and self.emotion_model:
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=512,
                )

                # 감정 예측
                with torch.no_grad():
                    outputs = self.emotion_model(**inputs)
                    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

                # 결과 해석
                emotion_scores = predictions[0].numpy()
                primary_emotion_idx = np.argmax(emotion_scores)
                primary_emotion = self.emotion_labels[primary_emotion_idx]
                confidence = float(emotion_scores[primary_emotion_idx])

                # 강도 계산
                intensity = (
                    "높음"
                    if confidence > 0.7
                    else "보통" if confidence > 0.4 else "낮음"
                )

                return {
                    "primary_emotion": primary_emotion,
                    "confidence": confidence,
                    "intensity": intensity,
                    "all_emotions": dict(
                        zip(self.emotion_labels, emotion_scores.tolist())
                    ),
                    "analysis_method": "BERT",
                }
            else:
                raise Exception("BERT 모델 또는 토크나이저가 로드되지 않음")

        except Exception as e:
            print(f"BERT 분석 오류: {e}")
            return self._rule_based_emotion_analysis(text)

    def _rule_based_emotion_analysis(self, text: str) -> Dict[str, Any]:
        """규칙 기반 감정분석 (백업용)"""
        text = text.lower()

        # 감정별 키워드 정의
        emotion_keywords = {
            "기쁨": [
                "기쁘",
                "행복",
                "좋아",
                "즐거",
                "웃음",
                "신나",
                "최고",
                "굿",
                "좋네",
                "멋지",
                "완벽",
                "사랑",
            ],
            "슬픔": [
                "슬프",
                "우울",
                "힘들",
                "아프",
                "눈물",
                "괴로",
                "절망",
                "외로",
                "허무",
                "비참",
            ],
            "분노": [
                "화나",
                "짜증",
                "분노",
                "열받",
                "빡치",
                "싫어",
                "미워",
                "악",
                "개빡",
                "어이없",
            ],
            "불안": [
                "걱정",
                "불안",
                "무서",
                "두려",
                "떨려",
                "긴장",
                "스트레스",
                "압박",
                "고민",
            ],
            "놀람": [
                "놀라",
                "깜짝",
                "어머",
                "헉",
                "와",
                "대박",
                "진짜",
                "설마",
                "어떻게",
            ],
            "혐오": ["역겨", "징그", "더러", "끔찍", "싫", "거부감", "못참"],
            "중립": ["그냥", "보통", "평범", "일반", "음", "아", "네", "예"],
        }

        # 강도별 키워드
        intensity_keywords = {
            "높음": [
                "너무",
                "정말",
                "진짜",
                "완전",
                "엄청",
                "매우",
                "굉장히",
                "최고로",
                "극도로",
            ],
            "보통": ["좀", "조금", "약간", "어느정도", "그럭저럭"],
            "낮음": ["살짝", "가볍게", "약간", "조금만"],
        }

        # 감정 점수 계산
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            emotion_scores[emotion] = score

        # 주요 감정 결정
        if sum(emotion_scores.values()) == 0:
            primary_emotion = "중립"
            confidence = 0.5
        else:
            primary_emotion = max(
                emotion_scores.keys(), key=lambda k: emotion_scores[k]
            )
            total_matches = sum(emotion_scores.values())
            confidence = (
                emotion_scores[primary_emotion] / total_matches
                if total_matches > 0
                else 0.5
            )

        # 강도 결정
        intensity = "낮음"
        for level, keywords in intensity_keywords.items():
            if any(keyword in text for keyword in keywords):
                intensity = level
                break

        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "intensity": intensity,
            "all_emotions": emotion_scores,
            "analysis_method": "Rule-based",
        }


class EmotionalResponseGenerator:
    """감정 기반 응답 생성기"""

    def __init__(self):
        self.emotion_analyzer = KoreanEmotionAnalyzer()
        self.emotion_responses = self._init_emotion_responses()
        self.empathy_phrases = self._init_empathy_phrases()

    def _init_emotion_responses(self) -> Dict[str, Dict[str, List[str]]]:
        """감정별 응답 패턴"""
        return {
            "기쁨": {
                "greeting": [
                    "와! 정말 기쁜 마음이 전해져요! 😄",
                    "행복한 에너지가 느껴지네요! ✨",
                    "기분 좋은 소식인가 봐요! 🎉",
                ],
                "response": [
                    "저도 덩달아 기분이 좋아져요!",
                    "이런 긍정적인 에너지 정말 좋아해요!",
                    "함께 기뻐할 수 있어서 행복해요!",
                ],
            },
            "슬픔": {
                "greeting": [
                    "마음이 많이 힘드시겠어요... 💙",
                    "어려운 시간을 보내고 계시는군요... 🤗",
                    "많이 속상하셨을 것 같아요...",
                ],
                "response": [
                    "언제든 이야기하고 싶으시면 들어드릴게요.",
                    "혼자가 아니에요, 제가 여기 있어요.",
                    "천천히 마음을 털어놓으셔도 돼요.",
                ],
            },
            "분노": {
                "greeting": [
                    "많이 화가 나셨나 봐요... 😤",
                    "정말 답답하고 짜증나는 상황이었겠어요...",
                    "그런 기분 충분히 이해해요...",
                ],
                "response": [
                    "화가 나는 건 당연해요. 어떤 일이었는지 말씀해주세요.",
                    "분노의 원인을 찾아서 해결책을 생각해봐요.",
                    "스트레스 해소 방법을 함께 찾아볼까요?",
                ],
            },
            "불안": {
                "greeting": [
                    "걱정이 많으시겠어요... 😔",
                    "불안한 마음 정말 잘 알겠어요...",
                    "마음이 편하지 않으시죠...",
                ],
                "response": [
                    "천천히 호흡하며 차근차근 해결해봐요.",
                    "걱정을 나누면 부담이 줄어들 거예요.",
                    "함께 차근차근 정리해보면 괜찮을 거예요.",
                ],
            },
            "놀람": {
                "greeting": [
                    "와! 정말 놀라운 일이 있었나봐요! 😲",
                    "어떤 놀라운 일이 있었는지 궁금해요!",
                    "깜짝 놀라셨겠어요!",
                ],
                "response": [
                    "자세한 이야기가 정말 궁금해요!",
                    "어떤 일인지 더 들려주세요!",
                    "정말 흥미진진하네요!",
                ],
            },
            "중립": {
                "greeting": [
                    "안녕하세요! 편안한 마음으로 대화해요 😊",
                    "차분한 분위기네요. 좋아요!",
                    "평온한 마음으로 이야기 나눠봐요.",
                ],
                "response": [
                    "무엇이든 편하게 이야기해주세요.",
                    "궁금한 것이 있으시면 언제든지요.",
                    "천천히 대화해봐요.",
                ],
            },
        }

    def _init_empathy_phrases(self) -> Dict[str, List[str]]:
        """공감 표현"""
        return {
            "이해": [
                "정말 잘 이해해요",
                "그런 마음 충분히 공감해요",
                "당연히 그럴 수 있어요",
                "완전히 이해됩니다",
            ],
            "지지": [
                "항상 응원하고 있어요",
                "함께 해결해나가요",
                "혼자가 아니에요",
                "제가 도와드릴게요",
            ],
            "격려": ["잘 하고 계세요", "충분히 훌륭해요", "괜찮을 거예요", "힘내세요"],
        }

    def generate_emotional_response(
        self, text: str, agent_type: str, base_response: str
    ) -> str:
        """감정을 고려한 응답 생성"""
        # 감정 분석
        emotion_result = self.emotion_analyzer.analyze_emotion(text)
        primary_emotion = emotion_result["primary_emotion"]
        intensity = emotion_result["intensity"]
        confidence = emotion_result["confidence"]

        # 감정별 응답 패턴 가져오기
        emotion_patterns = self.emotion_responses.get(
            primary_emotion, self.emotion_responses["중립"]
        )

        # 감정 인사말
        emotional_greeting = ""
        if confidence > 0.3:  # 충분히 확실한 감정인 경우만
            greeting_options = emotion_patterns.get("greeting", [])
            if greeting_options:
                emotional_greeting = random.choice(greeting_options) + "\n\n"

        # 공감 표현 추가
        empathy_phrase = ""
        if primary_emotion in ["슬픔", "분노", "불안"] and confidence > 0.4:
            empathy_type = "이해" if primary_emotion == "슬픔" else "지지"
            empathy_options = self.empathy_phrases.get(empathy_type, [])
            if empathy_options:
                empathy_phrase = random.choice(empathy_options) + " "

        # 강도에 따른 응답 조정
        if intensity == "높음" and confidence > 0.6:
            base_response = self._intensify_response(base_response, primary_emotion)

        # 최종 응답 구성
        final_response = emotional_greeting + empathy_phrase + base_response

        # 감정별 마무리 문구
        emotion_endings = emotion_patterns.get("response", [])
        if emotion_endings and confidence > 0.4:
            ending = random.choice(emotion_endings)
            final_response += f"\n\n{ending}"

        return final_response

    def _intensify_response(self, response: str, emotion: str) -> str:
        """강한 감정에 대한 응답 강화"""
        if emotion == "기쁨":
            return response.replace("!", "!! 🎉").replace(".", "! ✨")
        elif emotion == "슬픔":
            return "정말 " + response + " 마음이 아파요..."
        elif emotion == "분노":
            return "완전히 이해해요. " + response + " 정말 화나실 만해요."
        elif emotion == "불안":
            return "걱정 마세요. " + response + " 함께 해결해봐요."
        else:
            return response


# 전역 인스턴스
emotional_responder = EmotionalResponseGenerator()


def get_emotional_response(
    text: str, agent_type: str, base_response: str
) -> Tuple[str, Dict[str, Any]]:
    """감정분석 기반 응답 생성 (외부 호출용)"""
    enhanced_response = emotional_responder.generate_emotional_response(
        text, agent_type, base_response
    )
    emotion_analysis = emotional_responder.emotion_analyzer.analyze_emotion(text)

    return enhanced_response, emotion_analysis


if __name__ == "__main__":
    # 테스트
    test_texts = [
        "오늘 정말 기분이 좋아요! 좋은 일이 있었거든요",
        "너무 슬프고 우울해요... 힘든 일이 있었어요",
        "정말 화가 나요! 이해할 수 없어요",
        "걱정이 너무 많아서 잠도 못 자겠어요",
        "안녕하세요, 도움이 필요해요",
    ]

    print("🎯 Korean BERT 감정분석 시스템 테스트\n")

    for text in test_texts:
        response, analysis = get_emotional_response(
            text, "counselor", "도움이 되도록 최선을 다하겠습니다."
        )

        print(f"입력: {text}")
        print(
            f"감정: {analysis['primary_emotion']} (확신도: {analysis['confidence']:.2f}, 강도: {analysis['intensity']})"
        )
        print(f"응답: {response}")
        print("-" * 80)
