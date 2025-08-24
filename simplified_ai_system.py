"""
Vercel 환경 최적화를 위한 간단한 AI 시스템
"""
import random
from typing import Dict, List


class SimplifiedAIManager:
    """Vercel 환경용 간소화된 AI 관리자"""
    
    def __init__(self):
        self.experts = {
            "counselor": {"name": "💚 상담사", "field": "심리상담"},
            "marketing": {"name": "📈 마케터", "field": "마케팅전략"},
            "tech": {"name": "💻 개발자", "field": "기술개발"},
            "business": {"name": "💼 경영자", "field": "비즈니스전략"},
            "design": {"name": "🎨 디자이너", "field": "디자인"},
            "data": {"name": "📊 데이터분석가", "field": "데이터분석"},
            "finance": {"name": "💰 금융전문가", "field": "금융투자"},
            "education": {"name": "📚 교육자", "field": "교육컨설팅"}
        }
        
    def get_expert_response(self, expert_type: str, message: str) -> Dict:
        """전문가 응답 생성"""
        expert = self.experts.get(expert_type, self.experts["counselor"])
        
        # 간단한 키워드 기반 응답
        responses = {
            "counselor": [
                "마음이 힘드시군요. 차근차근 이야기해보세요.",
                "감정을 표현하는 것은 좋은 시작입니다.",
                "당신의 마음을 이해합니다. 함께 해결해나가요."
            ],
            "marketing": [
                "마케팅 전략에 대해 자세히 분석해드리겠습니다.",
                "타겟 고객 분석이 핵심입니다.",
                "브랜딩과 포지셔닝 전략을 고려해보세요."
            ],
            "tech": [
                "기술적 구현 방법을 제안드리겠습니다.",
                "최신 기술 트렌드를 반영한 솔루션입니다.",
                "확장성과 유지보수성을 고려해야 합니다."
            ],
            "default": [
                "전문적인 관점에서 분석해드리겠습니다.",
                "상황을 종합적으로 검토해보겠습니다.",
                "최적의 해결책을 찾아보겠습니다."
            ]
        }
        
        response_list = responses.get(expert_type, responses["default"])
        selected_response = random.choice(response_list)
        
        # 메시지 내용에 따른 맞춤 응답
        if "도움" in message or "help" in message.lower():
            selected_response = f"{expert['name']}으로서 최선을 다해 도와드리겠습니다. " + selected_response
        elif "감사" in message or "thank" in message.lower():
            selected_response = "도움이 되었다니 기쁩니다! " + selected_response
        
        return {
            "expert": expert["name"],
            "field": expert["field"],
            "response": selected_response,
            "confidence": 0.85,
            "timestamp": "2025-08-24"
        }
    
    def generate_response(self, message: str, expert_type: str = "counselor") -> str:
        """호환성을 위한 응답 생성 메서드"""
        result = self.get_expert_response(expert_type, message)
        return result["response"]
    
    def analyze_sentiment(self, text: str) -> str:
        """간단한 감정 분석"""
        positive_words = ["좋", "행복", "기쁨", "만족", "감사", "훌륭", "완벽"]
        negative_words = ["나쁘", "슬픔", "화남", "짜증", "실망", "걱정", "어려움"]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
