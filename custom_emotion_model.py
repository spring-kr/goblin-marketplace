"""
🎯 사용자 맞춤형 감정분석 모델 로더
사용자가 직접 학습시킨 모델 파일을 로드하여 감정분석을 수행하는 시스템
"""

import os
import pickle
import joblib
import json
import numpy as np
import torch
from typing import Dict, List, Tuple, Optional, Any
import warnings

warnings.filterwarnings("ignore")


class CustomEmotionModelLoader:
    """사용자 맞춤형 감정분석 모델 로더"""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.tokenizer = None
        self.vectorizer = None
        self.label_encoder = None
        self.model_type = None
        self.is_loaded = False
        self.config = None

        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def load_model(self, model_path: str) -> bool:
        """다양한 형태의 모델 파일 로드"""
        try:
            print(f"🔄 모델 로드 시도: {model_path}")

            # 파일 확장자에 따른 로드 방식 결정
            file_ext = os.path.splitext(model_path)[1].lower()

            if file_ext == ".pkl":
                return self._load_pickle_model(model_path)
            elif file_ext == ".joblib":
                return self._load_joblib_model(model_path)
            elif file_ext == ".json":
                return self._load_json_config(model_path)
            elif os.path.isdir(model_path):
                return self._load_model_directory(model_path)
            else:
                print(f"⚠️ 지원하지 않는 파일 형식: {file_ext}")
                return False

        except Exception as e:
            print(f"❌ 모델 로드 실패: {e}")
            return False

    def _load_pickle_model(self, model_path: str) -> bool:
        """Pickle 파일 로드 (PyTorch 모델 포함)"""
        try:
            with open(model_path, "rb") as f:
                model_data = pickle.load(f)

            # PyTorch 모델인지 확인
            if hasattr(model_data, 'state_dict') or isinstance(model_data, torch.nn.Module):
                self.model = model_data
                self.model_type = "pytorch"
                # 평가 모드로 설정
                if hasattr(self.model, 'eval'):
                    self.model.eval()
                print("✅ PyTorch 모델 로드 성공!")
            # 단일 모델인지 여러 컴포넌트가 포함된 딕셔너리인지 확인
            elif isinstance(model_data, dict):
                # PyTorch 모델이 딕셔너리에 포함된 경우
                if 'model' in model_data and hasattr(model_data['model'], 'state_dict'):
                    self.model = model_data.get("model")
                    self.tokenizer = model_data.get("tokenizer")
                    self.config = model_data.get("config")
                    self.model_type = "pytorch"
                    if hasattr(self.model, 'eval'):
                        self.model.eval()
                    print("✅ PyTorch 모델 (딕셔너리) 로드 성공!")
                else:
                    self.model = model_data.get("model")
                    self.vectorizer = model_data.get("vectorizer")
                    self.label_encoder = model_data.get("label_encoder")
                    self.model_type = model_data.get("model_type", "custom")
                    print("✅ 커스텀 모델 로드 성공!")
            else:
                self.model = model_data
                self.model_type = "sklearn"
                print("✅ Scikit-learn 모델 로드 성공!")

            self.is_loaded = True
            return True

        except Exception as e:
            print(f"❌ Pickle 모델 로드 실패: {e}")
            return False

    def _load_joblib_model(self, model_path: str) -> bool:
        """Joblib 파일 로드 (파이프라인 포함)"""
        try:
            model_data = joblib.load(model_path)

            # Pipeline 객체인지 확인
            if hasattr(model_data, 'named_steps'):
                # Scikit-learn Pipeline
                self.model = model_data
                self.model_type = "pipeline"
                print("✅ Scikit-learn 파이프라인 로드 성공!")
            elif isinstance(model_data, dict):
                self.model = model_data.get("model")
                self.vectorizer = model_data.get("vectorizer")
                self.label_encoder = model_data.get("label_encoder")
                self.model_type = model_data.get("model_type", "custom")
                print("✅ 딕셔너리 모델 로드 성공!")
            else:
                self.model = model_data
                self.model_type = "sklearn"
                print("✅ Scikit-learn 모델 로드 성공!")

            self.is_loaded = True
            return True

        except Exception as e:
            print(f"❌ Joblib 모델 로드 실패: {e}")
            return False

    def _load_json_config(self, config_path: str) -> bool:
        """JSON 설정 파일에서 모델 경로 정보 로드"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            model_file = config.get("model_path")
            vectorizer_file = config.get("vectorizer_path")

            if model_file and os.path.exists(model_file):
                if model_file.endswith(".pkl"):
                    with open(model_file, "rb") as f:
                        self.model = pickle.load(f)
                elif model_file.endswith(".joblib"):
                    self.model = joblib.load(model_file)

            if vectorizer_file and os.path.exists(vectorizer_file):
                if vectorizer_file.endswith(".pkl"):
                    with open(vectorizer_file, "rb") as f:
                        self.vectorizer = pickle.load(f)
                elif vectorizer_file.endswith(".joblib"):
                    self.vectorizer = joblib.load(vectorizer_file)

            self.model_type = config.get("model_type", "custom")
            self.is_loaded = True
            print("✅ JSON 설정 기반 모델 로드 성공!")
            return True

        except Exception as e:
            print(f"❌ JSON 설정 로드 실패: {e}")
            return False

    def _load_model_directory(self, model_dir: str) -> bool:
        """모델 디렉토리에서 파일들 자동 탐지 후 로드"""
        try:
            # 일반적인 모델 파일명 패턴들
            model_patterns = [
                "model.pkl",
                "model.joblib", 
                "emotion_model.pkl",
                "emotion_model.joblib",
                "classifier.pkl",
                "classifier.joblib",
                "korean_bert_emotion.pkl",  # 추가된 패턴
                "*emotion*.pkl",  # 감정 관련 패턴
                "*bert*.pkl",     # BERT 관련 패턴
            ]

            vectorizer_patterns = [
                "vectorizer.pkl",
                "vectorizer.joblib",
                "tfidf.pkl",
                "tfidf.joblib",
                "count_vectorizer.pkl",
                "count_vectorizer.joblib",
            ]

            # 실제 디렉토리의 모든 .pkl 파일 검색
            import glob
            pkl_files = glob.glob(os.path.join(model_dir, "*.pkl"))
            pth_files = glob.glob(os.path.join(model_dir, "*.pth"))  # PyTorch 모델
            
            print(f"🔍 발견된 모델 파일들: {pkl_files + pth_files}")

            # 모델 파일 찾기 - 직접 검색
            for pkl_file in pkl_files:
                file_name = os.path.basename(pkl_file).lower()
                if any(keyword in file_name for keyword in ["emotion", "bert", "model", "classifier"]):
                    print(f"🎯 모델 파일 로드 시도: {pkl_file}")
                    try:
                        if pkl_file.endswith(".pkl"):
                            with open(pkl_file, "rb") as f:
                                model_data = pickle.load(f)
                            
                            # PyTorch 모델인지 확인
                            if hasattr(model_data, 'state_dict') or isinstance(model_data, torch.nn.Module):
                                self.model = model_data
                                self.model_type = "pytorch"
                                print(f"✅ PyTorch 모델 로드 성공: {pkl_file}")
                            elif isinstance(model_data, dict):
                                self.model = model_data.get("model")
                                self.tokenizer = model_data.get("tokenizer")
                                self.config = model_data.get("config")
                                self.model_type = "pytorch" if hasattr(self.model, 'state_dict') else "sklearn"
                                print(f"✅ 딕셔너리 모델 로드 성공: {pkl_file}")
                            else:
                                self.model = model_data
                                self.model_type = "sklearn"
                                print(f"✅ Scikit-learn 모델 로드 성공: {pkl_file}")
                            break
                    except Exception as e:
                        print(f"⚠️ {pkl_file} 로드 실패: {e}")
                        continue

            # 벡터라이저 파일 찾기
            for pattern in vectorizer_patterns:
                vec_path = os.path.join(model_dir, pattern)
                if os.path.exists(vec_path):
                    if pattern.endswith(".pkl"):
                        with open(vec_path, "rb") as f:
                            self.vectorizer = pickle.load(f)
                    else:
                        self.vectorizer = joblib.load(vec_path)
                    break

            if self.model:
                self.is_loaded = True
                print("✅ 모델 디렉토리 로드 성공!")
                return True
            else:
                print("❌ 디렉토리에서 모델 파일을 찾을 수 없습니다.")
                return False

        except Exception as e:
            print(f"❌ 모델 디렉토리 로드 실패: {e}")
            return False

    def predict_emotion(self, text: str) -> Dict[str, Any]:
        """사용자 모델로 감정 예측"""
        if not self.is_loaded or not self.model:
            return self._fallback_emotion_analysis(text)

        try:
            # 텍스트 전처리
            processed_text = self._preprocess_text(text)

            # PyTorch 모델 처리
            if self.model_type == "pytorch":
                return self._predict_with_pytorch(processed_text)
            
            # Pipeline 모델 처리
            elif self.model_type == "pipeline":
                return self._predict_with_pipeline(processed_text)
            
            # 벡터화 (vectorizer가 있는 경우만 처리)
            if self.vectorizer:
                try:
                    text_vector = self.vectorizer.transform([processed_text])
                except Exception as e:
                    print(f"⚠️ 벡터화 실패: {e}")
                    return self._fallback_emotion_analysis(processed_text)
            else:
                # 벡터라이저가 없으면 모델 사용 불가, 폴백 사용
                print("⚠️ 벡터라이저 없음, 폴백 분석 사용")
                return self._fallback_emotion_analysis(processed_text)

            # 예측 수행 (벡터라이저가 있는 경우만)
            if hasattr(self.model, "predict_proba") and self.model_type != "pytorch":
                # 확률 예측이 가능한 scikit-learn 모델
                try:
                    probabilities = self.model.predict_proba(text_vector)[0]
                    prediction = self.model.predict(text_vector)[0]

                    # 클래스 이름 가져오기
                    if hasattr(self.model, "classes_"):
                        classes = self.model.classes_
                    else:
                        classes = [f"감정_{i}" for i in range(len(probabilities))]

                    # 결과 구성
                    emotion_scores = dict(zip(classes, probabilities))
                    primary_emotion = str(prediction)
                    confidence = float(max(probabilities))
                except Exception as e:
                    print(f"⚠️ Scikit-learn 모델 예측 실패: {e}")
                    return self._fallback_emotion_analysis(processed_text)

            else:
                # 단순 예측만 가능한 모델
                try:
                    prediction = self.model.predict(text_vector)[0]
                    primary_emotion = str(prediction)
                    confidence = 0.8  # 기본값
                    emotion_scores = {primary_emotion: confidence}
                except Exception as e:
                    print(f"⚠️ 모델 예측 실패: {e}")
                    return self._fallback_emotion_analysis(processed_text)

            # 강도 계산
            intensity = (
                "높음" if confidence > 0.7 else "보통" if confidence > 0.4 else "낮음"
            )

            return {
                "primary_emotion": primary_emotion,
                "confidence": confidence,
                "intensity": intensity,
                "all_emotions": emotion_scores,
                "analysis_method": f"Custom_{self.model_type}",
                "model_info": {
                    "type": self.model_type,
                    "has_vectorizer": self.vectorizer is not None,
                    "model_class": type(self.model).__name__,
                },
            }

        except Exception as e:
            print(f"❌ 사용자 모델 예측 실패: {e}")
            return self._fallback_emotion_analysis(text)

    def _predict_with_pytorch(self, text: str) -> Dict[str, Any]:
        """PyTorch 모델로 감정 예측"""
        try:
            # 기본 감정 클래스 (config에서 로드하거나 기본값 사용)
            emotion_classes = [
                "불안", "우울", "분노", "두려움", "슬픔",
                "기쁨", "안도", "희망", "감사", "중립"
            ]
            
            if self.config and "emotion_categories" in self.config:
                emotion_classes = self.config["emotion_categories"]["class_labels"]

            # 간단한 토큰화 (실제로는 tokenizer 사용)
            if self.tokenizer:
                # BERT 토크나이저 사용
                inputs = self.tokenizer(
                    text, 
                    max_length=512, 
                    padding='max_length', 
                    truncation=True, 
                    return_tensors='pt'
                )
                
                # 모델 예측
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    if hasattr(outputs, 'logits'):
                        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                    else:
                        predictions = torch.nn.functional.softmax(outputs, dim=-1)
                
                # 결과 처리
                probabilities = predictions[0].cpu().numpy()
                emotion_scores = dict(zip(emotion_classes, probabilities))
                
                # 가장 높은 확률의 감정 찾기
                max_idx = int(torch.argmax(predictions[0]).item())
                primary_emotion = emotion_classes[max_idx] if max_idx < len(emotion_classes) else "중립"
                confidence = float(probabilities[max_idx])
                
                # 강도 계산
                intensity = (
                    "높음" if confidence > 0.7 else "보통" if confidence > 0.4 else "낮음"
                )
                
                return {
                    "primary_emotion": primary_emotion,
                    "confidence": confidence,
                    "intensity": intensity, 
                    "all_emotions": emotion_scores,
                    "analysis_method": "Custom_PyTorch_BERT",
                    "model_info": {
                        "type": "pytorch_bert",
                        "has_tokenizer": True,
                        "model_class": type(self.model).__name__,
                    },
                }
                
            else:
                # 토크나이저가 없는 경우 폴백
                return self._fallback_emotion_analysis(text)

        except Exception as e:
            print(f"❌ PyTorch 모델 예측 실패: {e}")
            return self._fallback_emotion_analysis(text)

    def _predict_with_pipeline(self, text: str) -> Dict[str, Any]:
        """Scikit-learn 파이프라인으로 감정 예측"""
        try:
            # 파이프라인 직접 사용 (벡터화 + 예측 통합)
            prediction = self.model.predict([text])[0]
            
            # 확률 예측 (가능한 경우)
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba([text])[0]
                
                # 클래스 라벨 가져오기
                if hasattr(self.model, 'classes_'):
                    classes = self.model.classes_
                else:
                    # 파이프라인의 분류기에서 클래스 가져오기
                    classifier = self.model.named_steps.get('classifier')
                    if hasattr(classifier, 'classes_'):
                        classes = classifier.classes_
                    else:
                        classes = ["기쁨", "슬픔", "분노", "불안", "중립"]
                
                emotion_scores = dict(zip(classes, probabilities))
                confidence = float(max(probabilities))
            else:
                # 확률 예측이 불가능한 경우
                emotion_scores = {str(prediction): 0.8}
                confidence = 0.8
            
            # 강도 계산
            intensity = (
                "높음" if confidence > 0.7 else "보통" if confidence > 0.4 else "낮음"
            )
            
            return {
                "primary_emotion": str(prediction),
                "confidence": confidence,
                "intensity": intensity,
                "all_emotions": emotion_scores,
                "analysis_method": "Scikit_Learn_Pipeline",
                "model_info": {
                    "type": "pipeline",
                    "has_vectorizer": True,
                    "model_class": type(self.model).__name__,
                },
            }

        except Exception as e:
            print(f"❌ 파이프라인 예측 실패: {e}")
            return self._fallback_emotion_analysis(text)

    def _preprocess_text(self, text: str) -> str:
        """텍스트 전처리"""
        # 기본적인 전처리 (사용자가 원하는 방식으로 수정 가능)
        import re

        # 불필요한 문자 제거
        text = re.sub(r"[^\w\s가-힣]", "", text)
        # 공백 정리
        text = " ".join(text.split())
        # 소문자 변환 (한글은 해당 없음)

        return text

    def _fallback_emotion_analysis(self, text: str) -> Dict[str, Any]:
        """백업용 규칙 기반 감정분석"""
        emotion_keywords = {
            "기쁨": ["기쁘", "행복", "좋아", "즐거", "웃음", "신나"],
            "슬픔": ["슬프", "우울", "힘들", "아프", "눈물"],
            "분노": ["화나", "짜증", "분노", "열받"],
            "불안": ["걱정", "불안", "무서", "두려"],
            "중립": ["그냥", "보통", "평범"],
        }

        text_lower = text.lower()
        emotion_scores = {}

        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score / len(keywords)  # 정규화

        primary_emotion = max(emotion_scores.keys(), key=lambda k: emotion_scores[k])
        confidence = emotion_scores[primary_emotion]

        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "intensity": "보통",
            "all_emotions": emotion_scores,
            "analysis_method": "Fallback_Rule_Based",
        }

    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        return {
            "is_loaded": self.is_loaded,
            "model_type": self.model_type,
            "has_model": self.model is not None,
            "has_vectorizer": self.vectorizer is not None,
            "model_class": type(self.model).__name__ if self.model else None,
        }


# 사용자 모델 경로 설정 (여러 가능성 시도)
def find_user_model() -> Optional[str]:
    """사용자 모델 파일 자동 탐지"""
    possible_paths = [
        "./emotion_model.pkl",
        "./emotion_model.joblib",
        "./model.pkl",
        "./model.joblib",
        "./models/",
        "../models/",
        "./my_emotion_model.pkl",
        "./korean_emotion_model.pkl",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"🔍 사용자 모델 발견: {path}")
            return path

    return None


# 전역 사용자 모델 로더
user_model_path = find_user_model()
custom_emotion_loader = CustomEmotionModelLoader(user_model_path)


def analyze_emotion_with_user_model(text: str) -> Dict[str, Any]:
    """사용자 모델을 사용한 감정분석 (외부 호출용)"""
    return custom_emotion_loader.predict_emotion(text)


if __name__ == "__main__":
    # 테스트
    print("🎯 사용자 맞춤형 감정분석 모델 테스트\n")

    # 모델 정보 출력
    info = custom_emotion_loader.get_model_info()
    print("모델 정보:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

    # 테스트 문장들
    test_texts = [
        "오늘 정말 기분이 좋아요!",
        "너무 슬프고 우울해요...",
        "정말 화가 나요!",
        "걱정이 많아서 잠을 못 자겠어요",
        "그냥 평범한 하루였어요",
    ]

    for text in test_texts:
        result = analyze_emotion_with_user_model(text)
        print(f"입력: {text}")
        print(f"감정: {result['primary_emotion']} (확신도: {result['confidence']:.2f})")
        print(f"방법: {result['analysis_method']}")
        print("-" * 50)
