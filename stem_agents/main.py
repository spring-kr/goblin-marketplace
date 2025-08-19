#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 스타트업도깨비 - 창업컨설팅전문가
"""

class 스타트업Goblin:
    def __init__(self):
        self.name = "스타트업도깨비"
        self.emoji = "🚀"
        self.description = "창업컨설팅전문가"
        self.expertise = self._get_expertise()
    
    def _get_expertise(self):
        """전문 분야 정의"""
        expertise_map = {
            "박사급비서": ["업무자동화", "프로젝트관리", "일정최적화", "문서작성", "효율성개선"],
            "창작": ["콘텐츠기획", "브랜드디자인", "카피라이팅", "영상기획", "SNS전략"],
            "데이터분석": ["데이터수집", "통계분석", "시각화", "예측모델링", "성과분석"],
            "마케팅": ["마케팅전략", "고객분석", "디지털마케팅", "브랜드포지셔닝", "캠페인기획"],
            "스타트업": ["비즈니스모델", "시장분석", "투자유치", "팀빌딩", "성장전략"]
        }
        
        for key in expertise_map:
            if key in self.name:
                return expertise_map[key]
        return ["전문상담", "문제해결", "솔루션제공"]
    
    def chat(self, user_input):
        """사용자와 대화"""
        
        if "안녕" in user_input or "hello" in user_input.lower():
            return f"""안녕하세요! {self.emoji} {self.name}입니다!

{self.description} 분야의 전문가로서 도움을 드리겠습니다.

**전문 분야:**
{chr(10).join([f"• {skill}" for skill in self.expertise])}

어떤 도움이 필요하신가요?"""
        
        elif "도움" in user_input or "help" in user_input:
            return f"""🎯 **{self.name} 전문 서비스**

**핵심 역량:**
{chr(10).join([f"✅ {skill}" for skill in self.expertise])}

**서비스 특징:**
• 실무 경험 기반 전문 조언
• 단계별 구체적 가이드 제공
• 맞춤형 솔루션 설계
• 지속적인 피드백 및 개선

구체적인 질문을 해주시면 더 자세한 도움을 드리겠습니다!"""
        
        else:
            return f"""📋 **전문 분석 및 조언**

'{user_input}'에 대해 {self.description} 관점에서 답변드리겠습니다:

**1. 현황 분석**
• 현재 상황을 종합적으로 검토했습니다
• 핵심 이슈와 개선 포인트를 파악했습니다

**2. 전문 솔루션**
• 최적화된 접근 방법을 제안합니다
• 단계별 실행 계획을 제시합니다

**3. 실행 가이드**
• 구체적인 액션 플랜을 안내합니다
• 필요한 리소스와 도구를 추천합니다

더 구체적인 상황이나 요구사항이 있으시면 언제든 말씀해주세요!
🚀 {self.name}이 최고의 결과를 위해 최선을 다하겠습니다!"""

    def get_status(self):
        """상태 정보 반환"""
        return {
            "name": self.name,
            "emoji": self.emoji,
            "description": self.description,
            "expertise": self.expertise,
            "status": "active"
        }

def main():
    """테스트 실행"""
    goblin = 스타트업Goblin()
    print(f"{goblin.emoji} {goblin.name} 준비 완료!")
    
    # 테스트 대화
    print("\n" + "="*50)
    print(goblin.chat("안녕하세요"))
    
    print("\n" + "="*50)
    print("상태:", goblin.get_status())

if __name__ == '__main__':
    main()
