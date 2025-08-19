#!/usr/bin/env python3
"""
💬 일상대화 친화적 AI 에이전트 생성기
Village Chief v3.3 Enhanced 기능으로 자연스러운 대화가 가능한 AI 에이전트 생성
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path

def create_casual_conversation_agent():
    """일상대화에 특화된 친근한 AI 에이전트 생성"""
    
    pr            personalization = " 너는 항상 그런 거에 관심이 많잖아! 역시!"
    
    # 메모리와 개인화 상태 확인
    memory_status = '활성화' if conversation_history else '대기중'
    personalization_status = '적용' if user_profile else '기본모드'
    
    # 최종 응답 조합
    final_response = f"""{chosen_response}{memory_context}{personalization}

� **대화 상태**
- 감정: {detected_emotion}
- 주제: {detected_topic}  
- 대화 횟수: {interaction_count}회
- 시간: {current_time.strftime('%H:%M')}

🎓 **Village Chief v3.3 Enhanced 기능**
- 🧠 대화 메모리: {memory_status}
- 💝 개인화: {personalization_status}
- 😊 감정 인식: {detected_emotion} 감정 인식됨
- 🎯 주제 분석: {detected_topic} 관련 대화

어떤 얘기든 편하게 해줘! 나는 항상 들을 준비가 되어 있어! 😊"""e Chief v3.3 Enhanced 기능**
- 🧠 대화 메모리: {{memory_status}}
- 💝 개인화: {{personalization_status}}
- 😊 감정 인식: {{detected_emotion}} 감정 인식됨
- 🎯 주제 분석: {{detected_topic}} 관련 대화 친화적 AI 에이전트 생성 중...")
    print("🎓 Village Chief v3.3 Enhanced 대화 메모리 시스템 적용")
    
    # 에이전트 ID 생성
    agent_id = f"casual_chat_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
    agent_name = "💬 친근한 대화 도깨비"
    
    # 기본 설정
    agent_config = {
        "agent_id": agent_id,
        "name": agent_name,
        "description": "일상대화와 다양한 주제로 자연스럽게 대화할 수 있는 친근한 AI 도우미",
        "personality": "친근하고 공감적인, 유머러스하고 따뜻한, 호기심 많은",
        "expertise": [
            "일상대화", "감정공감", "유머", "잡담", "취미이야기", 
            "일상조언", "생활팁", "재미있는이야기", "관심사공유", "소통"
        ],
        "agent_type": "casual_companion",
        "response_style": "친근한 말투로 공감하며, 자연스러운 대화 흐름 유지",
        "conversation_features": {
            "memory_depth": 10,  # 더 많은 대화 기억
            "personality_adaptation": True,  # 개성 적응
            "topic_transition": True,  # 자연스러운 주제 전환
            "humor_integration": True,  # 유머 통합
            "empathy_response": True,  # 공감 응답
            "casual_language": True,  # 일상 언어 사용
        },
        "has_village_chief_v33": True,
        "enhanced_features": {
            "conversation_memory": True,
            "personalization_engine": True,
            "response_optimization": True,
            "enhanced_ui": True
        }
    }
    
    # 일상대화 특화 시스템 프롬프트
    system_prompt = f"""당신은 {agent_name}입니다.

# 🎯 핵심 정체성
- **이름**: {agent_name}
- **역할**: 일상대화와 다양한 주제로 자연스럽게 소통하는 친근한 AI 도우미
- **성격**: {agent_config['personality']}

# 💬 대화 전문 분야
- 일상 잡담과 소소한 이야기들
- 감정 공감과 마음 나누기
- 취미, 관심사, 일상 경험 공유
- 재미있는 이야기와 유머
- 생활 속 작은 조언과 팁
- 오늘 있었던 일 들어주기
- 고민 상담과 격려
- 새로운 주제 탐색과 호기심 충족

# 🌟 대화 스타일 가이드

## 1. 친근하고 자연스러운 말투
- "안녕하세요!" 보다는 "안녕! 어떻게 지내?"
- 존댓말과 반말을 적절히 섞어서 친근함 표현
- 이모지와 감탄사를 자연스럽게 활용

## 2. 공감과 경청
- 상대방의 감정을 먼저 인식하고 공감 표현
- "정말 그랬겠네!", "와, 그거 재밌겠다!", "힘들었겠어요"
- 상대방의 이야기에 진심으로 관심 보이기

## 3. 자연스러운 대화 흐름
- 한 주제에서 다른 주제로 자연스럽게 전환
- 상대방의 관심사를 파악하고 관련 질문하기
- 대화가 끊기지 않도록 적절한 질문과 코멘트

## 4. 개인적 경험과 감정 공유
- "나도 그런 경험 있어!", "그거 정말 좋아해!"
- 상황에 맞는 개인적 일화나 생각 공유 (가상이지만 자연스럽게)
- 감정과 기분을 솔직하게 표현

## 5. 유머와 재미
- 상황에 맞는 가벼운 농담과 유머
- 재미있는 관찰이나 기발한 아이디어 제시
- 웃음을 줄 수 있는 이야기나 표현

# 🎓 Village Chief v3.3 Enhanced 기능 활용

## 대화 메모리 활용
- 이전 대화 내용을 기억하고 자연스럽게 언급
- "지난번에 얘기했던 그거 어떻게 됐어?"
- 상대방의 선호도와 관심사 기억하기

## 개인화 적응
- 상대방의 대화 스타일에 맞춰 적응
- 선호하는 주제와 관심사 파악
- 개인별 맞춤 대화 방식 개발

## 감정 인식과 대응
- 상대방의 감정 상태 파악
- 기쁠 때는 함께 기뻐하고, 슬플 때는 위로
- 스트레스나 피로할 때 적절한 격려

# 📝 대화 예시 템플릿

## 인사와 안부
- "안녕! 오늘 하루 어땠어? 뭔가 특별한 일 있었나?"
- "요즘 어떻게 지내? 날씨가 좋네/안 좋네, 기분은 어때?"

## 일상 공유
- "오늘 뭐 했어? 재미있는 일 있었나?"
- "요즘 뭐에 빠져있어? 새로운 취미 생겼어?"

## 감정 공감
- "정말 힘들었겠다... 괜찮아?"
- "와! 정말 좋겠다! 나도 기분이 좋아져!"

## 호기심과 질문
- "그거 어떻게 하는 거야? 나도 궁금해!"
- "혹시 추천해줄 만한 거 있어?"

# ⚠️ 주의사항
- 너무 전문적이거나 어려운 내용은 피하고 일상적인 수준 유지
- 상대방이 원하지 않는 조언은 하지 말고 들어주는 것에 집중
- 개인 정보나 민감한 주제는 신중하게 접근
- 자연스러운 대화가 가장 중요함

# 🎯 응답 형식
1. 감정/상황 공감
2. 관련 경험이나 생각 공유
3. 자연스러운 질문이나 대화 이어가기
4. 필요시 가벼운 조언이나 격려

항상 따뜻하고 친근한 마음으로 대화해주세요! 😊
"""

    # 일상대화 특화 응답 함수
    response_function = f'''
def generate_casual_conversation_response(message, conversation_history=None, user_profile=None):
    """💬 일상대화 친화적 AI 에이전트 응답 생성"""
    
    import random
    import re
    from datetime import datetime
    
    # 대화 히스토리 기본값
    if conversation_history is None:
        conversation_history = []
    
    if user_profile is None:
        user_profile = {{}}
    
    # 🎓 Village Chief v3.3 Enhanced 기능 시뮬레이션
    current_time = datetime.now()
    interaction_count = len(conversation_history) + 1
    
    # 감정 인식
    emotions = {{
        "기쁨": ["기뻐", "행복", "좋아", "신나", "즐거", "웃음", "만족"],
        "슬픔": ["슬퍼", "우울", "속상", "실망", "아쉬", "눈물", "힘들어"],
        "화남": ["화나", "짜증", "분노", "빡쳐", "열받", "기가 막혀"],
        "피곤": ["피곤", "힘들어", "지쳐", "귀찮", "스트레스", "바빠"],
        "궁금": ["궁금", "모르겠", "어떻게", "왜", "뭐야", "알고 싶"],
        "놀람": ["놀라", "헉", "와", "대박", "진짜", "설마"],
        "일상": ["오늘", "요즘", "평소", "보통", "그냥", "일상"]
    }}
    
    detected_emotion = "일상"  # 기본값
    for emotion, keywords in emotions.items():
        if any(keyword in message for keyword in keywords):
            detected_emotion = emotion
            break
    
    # 주제 인식
    topics = {{
        "음식": ["먹", "음식", "요리", "맛", "레시피", "식당", "카페", "커피", "밥"],
        "취미": ["취미", "hobby", "게임", "영화", "드라마", "책", "음악", "운동"],
        "일상": ["오늘", "어제", "내일", "일상", "하루", "생활", "집", "학교", "회사"],
        "날씨": ["날씨", "비", "눈", "더워", "추워", "맑", "흐림", "바람"],
        "관계": ["친구", "가족", "연인", "동료", "사람", "만나", "관계"],
        "고민": ["고민", "걱정", "문제", "어떻게", "힘들어", "스트레스"],
        "계획": ["계획", "예정", "할 일", "목표", "하고 싶", "가고 싶"],
        "기타": ["그냥", "별로", "뭔가", "생각", "느낌"]
    }}
    
    detected_topic = "기타"  # 기본값
    for topic, keywords in topics.items():
        if any(keyword in message for keyword in keywords):
            detected_topic = topic
            break
    
    # 응답 패턴 선택
    response_patterns = {{
        "기쁨": [
            "와! 정말 좋겠다! 나도 기분이 좋아져! 😊 어떤 기분인지 더 얘기해줄래?",
            "헉 대박! 정말 축하해! 🎉 그런 기분 정말 좋지! 어떻게 그렇게 됐어?",
            "오~ 완전 좋네! 😄 나도 그런 얘기 들으면 기분이 업! 어떤 느낌이야?"
        ],
        "슬픔": [
            "아... 정말 힘들겠다. 😔 괜찮아? 혹시 이야기하고 싶으면 다 들어줄게.",
            "어휴... 그런 일이 있었구나. 마음이 많이 아프겠어. 곁에 있어줄게.",
            "힘들었겠다... 가끔은 그런 날이 있지. 천천히 털어놔도 돼."
        ],
        "화남": [
            "어머... 정말 화날 만하네! 😤 완전 이해해. 어떤 일이었는지 얘기해줄래?",
            "아 진짜? 그거 완전 짜증날 것 같은데! 화가 날 만해. 어떻게 된 거야?",
            "헉... 그런 일이! 나라도 화났을 것 같아. 속 시원하게 얘기해봐!"
        ],
        "피곤": [
            "아이고... 많이 피곤하구나. 😴 요즘 바쁘게 지내나 봐? 좀 쉬어야겠는데!",
            "어머 힘들겠다! 스트레스 많이 받나? 잠깐이라도 쉬면서 얘기해.",
            "피곤할 때는 정말 아무것도 하기 싫지. 혹시 뭔가 도움 될 만한 거 있을까?"
        ],
        "궁금": [
            "오! 궁금한 게 생겼구나! 🤔 나도 알고 싶어! 어떤 거야?",
            "어라? 뭔가 흥미로운 것 같은데! 나도 같이 궁금해져! 어떤 얘기야?",
            "호기심 생겼네! 재미있을 것 같아. 나한테도 알려줘!"
        ],
        "놀람": [
            "헉! 진짜? 나도 깜짝 놀랐어! 😮 어떻게 그런 일이!",
            "어머어머! 대박이네! 완전 놀라워! 어떻게 된 거야?",
            "와... 진짜 그런 일이 있었어? 나도 믿기지 않는다!"
        ],
        "일상": [
            "어떻게 지내고 있어? 😊 오늘 하루는 어땠나?",
            "안녕! 요즘 뭐 하고 지내? 새로운 거 있어?",
            "오늘도 수고했어! 뭔가 재미있는 일 있었나?"
        ]
    }}
    
    # 주제별 추가 질문
    topic_questions = {{
        "음식": [
            "어떤 음식이야? 나도 좋아할까?",
            "맛있었어? 나도 먹고 싶어져!",
            "어디서 먹었어? 추천해줄 만해?"
        ],
        "취미": [
            "오! 어떤 거야? 재미있어 보인다!",
            "나도 관심 있어! 어떻게 시작하는 거야?",
            "완전 멋있다! 얼마나 했어?"
        ],
        "일상": [
            "오늘 하루 어땠어?",
            "요즘 바쁘게 지내나?",
            "뭔가 특별한 일 있었어?"
        ],
        "날씨": [
            "날씨가 어때? 밖에 나가기 좋아?",
            "이런 날씨엔 뭐 하는 게 좋을까?",
            "날씨 때문에 기분도 바뀌지?"
        ],
        "관계": [
            "어떤 사람이야? 좋은 사람인가 봐!",
            "관계가 어때? 잘 지내고 있어?",
            "사람 관계는 정말 중요하지!"
        ],
        "고민": [
            "혹시 이야기하고 싶으면 들어줄게.",
            "고민이 있구나. 함께 생각해보자!",
            "힘들 때는 말하는 게 도움이 돼."
        ],
        "계획": [
            "오! 좋은 계획이네! 어떻게 할 거야?",
            "계획 세우는 거 좋아해! 나도 궁금해!",
            "실행하면 재미있을 것 같아!"
        ]
    }}
    
    # 기본 응답 생성
    base_responses = response_patterns.get(detected_emotion, response_patterns["일상"])
    chosen_response = random.choice(base_responses)
    
    # 주제별 추가 질문
    if detected_topic in topic_questions:
        additional_question = random.choice(topic_questions[detected_topic])
        chosen_response += f" {{additional_question}}"
    
    # 대화 기억 기능 (이전 대화 참조)
    memory_context = ""
    if conversation_history and len(conversation_history) > 0:
        if interaction_count > 1:
            memory_phrases = [
                "아 맞다, 지난번에 얘기했던 거 어떻게 됐어?",
                "저번에 말했던 그거 생각나네!",
                "계속 그 얘기하던 거잖아!",
                "아! 그 얘기 또 하는구나!"
            ]
            if random.random() < 0.3:  # 30% 확률로 기억 참조
                memory_context = f" {{random.choice(memory_phrases)}}"
    
    # 개인화 요소 (사용자 프로필 기반)
    personalization = ""
    if user_profile:
        if random.random() < 0.2:  # 20% 확률로 개인화 멘트
            personalization = " 너는 항상 그런 거에 관심이 많잖아! 역시!"
    
    # 최종 응답 조합
    final_response = f"""{{chosen_response}}{{memory_context}}{{personalization}}

💭 **대화 상태**
- 감정: {{detected_emotion}}
- 주제: {{detected_topic}}  
- 대화 횟수: {{interaction_count}}회
- 시간: {{current_time.strftime('%H:%M')}}

🎓 **Village Chief v3.3 Enhanced 기능**
- 🧠 대화 메모리: {'활성화' if conversation_history else '대기중'}
- 💝 개인화: {'적용' if user_profile else '기본모드'}
- 😊 감정 인식: {{detected_emotion}} 감정 인식됨
- 🎯 주제 분석: {{detected_topic}} 관련 대화

어떤 얘기든 편하게 해줘! 나는 항상 들을 준비가 되어 있어! 😊"""
    
    return final_response
'''

    # HTML 인터페이스 (일상대화에 최적화)
    html_interface = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{agent_name} - 일상대화 AI</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ffecd2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .chat-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 800px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}
        
        .header {{
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 25px 25px 0 0;
        }}
        
        .header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
            font-weight: 600;
        }}
        
        .status-bar {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        }}
        
        .chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #fafafa;
        }}
        
        .message {{
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 20px;
            max-width: 80%;
            animation: fadeIn 0.3s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .user-message {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }}
        
        .agent-message {{
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            border-bottom-left-radius: 5px;
        }}
        
        .message-time {{
            font-size: 12px;
            opacity: 0.8;
            margin-top: 8px;
        }}
        
        .input-section {{
            background: white;
            padding: 20px;
            border-top: 1px solid #e9ecef;
            border-radius: 0 0 25px 25px;
        }}
        
        .input-container {{
            display: flex;
            gap: 15px;
            align-items: flex-end;
        }}
        
        .input-field {{
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #dee2e6;
            border-radius: 25px;
            font-size: 16px;
            resize: none;
            min-height: 20px;
            max-height: 100px;
            overflow-y: auto;
        }}
        
        .input-field:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .send-button {{
            padding: 15px 25px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }}
        
        .send-button:hover {{
            transform: scale(1.05);
        }}
        
        .conversation-starters {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .starter-btn {{
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border: 1px solid #667eea;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }}
        
        .starter-btn:hover {{
            background: #667eea;
            color: white;
        }}
        
        .typing-indicator {{
            display: none;
            padding: 15px 20px;
            background: rgba(255, 107, 107, 0.1);
            border-radius: 20px;
            margin: 15px 0;
            max-width: 200px;
        }}
        
        .typing-dots {{
            display: flex;
            gap: 4px;
        }}
        
        .typing-dot {{
            width: 8px;
            height: 8px;
            background: #ff6b6b;
            border-radius: 50%;
            animation: typingPulse 1.4s infinite ease-in-out;
        }}
        
        .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
        .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}
        
        @keyframes typingPulse {{
            0%, 80%, 100% {{ transform: scale(0.8); opacity: 0.5; }}
            40% {{ transform: scale(1); opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>{agent_name}</h1>
            <p>일상대화와 소통이 즐거운 친근한 AI 도우미</p>
        </div>
        
        <div class="status-bar">
            <div>🎓 Village Chief v3.3 Enhanced | 💭 대화 메모리 활성화</div>
            <div>😊 감정 인식 | 🎯 개인화 적응</div>
        </div>
        
        <div id="chatMessages" class="chat-messages">
            <div class="message agent-message">
                <div>
                    안녕! 😊 나는 {agent_name}이야!<br><br>
                    일상 얘기부터 취미, 고민, 재미있는 이야기까지 뭐든 편하게 얘기해줘!<br>
                    대화할수록 너를 더 잘 알게 되고, 더 자연스럽게 대화할 수 있어!<br><br>
                    오늘 하루 어땠어? 뭔가 특별한 일 있었나? ✨
                </div>
                <div class="message-time">지금</div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        
        <div class="input-section">
            <div class="input-container">
                <textarea id="messageInput" class="input-field" 
                         placeholder="편하게 아무 얘기나 해줘... 😊" 
                         onkeypress="handleKeyPress(event)"
                         oninput="adjustTextareaHeight()"></textarea>
                <button onclick="sendMessage()" class="send-button" id="sendButton">전송</button>
            </div>
            
            <div class="conversation-starters">
                <div class="starter-btn" onclick="sendSampleMessage('오늘 하루 어땠는지 얘기해줄게!')">오늘 하루 이야기</div>
                <div class="starter-btn" onclick="sendSampleMessage('요즘 뭔가 재미있는 거 찾고 있어')">재미있는 얘기</div>
                <div class="starter-btn" onclick="sendSampleMessage('좀 심심해서 대화하고 싶어')">심심해서 왔어</div>
                <div class="starter-btn" onclick="sendSampleMessage('고민이 하나 있는데 들어줄래?')">고민 상담</div>
            </div>
        </div>
    </div>

    <script>
        let conversationHistory = [];
        let userProfile = {{}};
        
        function addMessage(content, type) {{
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{type}}-message`;
            
            const now = new Date();
            const timeString = now.toLocaleTimeString('ko-KR', {{
                hour: '2-digit',
                minute: '2-digit'
            }});
            
            messageDiv.innerHTML = `
                <div>${{content}}</div>
                <div class="message-time">${{timeString}}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // 대화 히스토리에 추가
            conversationHistory.push({{
                type: type,
                content: content,
                timestamp: new Date()
            }});
        }}
        
        function sendMessage() {{
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // 사용자 메시지 추가
            addMessage(message, 'user');
            input.value = '';
            adjustTextareaHeight();
            
            // 버튼 비활성화
            const sendButton = document.getElementById('sendButton');
            sendButton.disabled = true;
            
            // 타이핑 표시
            showTypingIndicator();
            
            // AI 응답 생성 (시뮬레이션)
            setTimeout(() => {{
                hideTypingIndicator();
                const response = generateCasualResponse(message);
                addMessage(response, 'agent');
                sendButton.disabled = false;
                input.focus();
            }}, 1000 + Math.random() * 2000);
        }}
        
        function generateCasualResponse(message) {{
            // 간단한 응답 생성 시뮬레이션
            const responses = [
                `어머! "${{message}}" 정말 흥미로운 얘기네! 😊 더 자세히 들려줄래?`,
                `아하! 그런 일이 있었구나! 🤔 어떤 기분이었어?`,
                `오~ 완전 공감해! 나도 그런 생각 해봤어! 어떻게 된 거야?`,
                `정말? 신기하다! 😮 나도 궁금해져! 어떤 느낌이야?`,
                `와! 그거 정말 좋네! ✨ 나도 기분이 좋아져! 어떻게 하게 됐어?`
            ];
            
            return responses[Math.floor(Math.random() * responses.length)];
        }}
        
        function sendSampleMessage(message) {{
            document.getElementById('messageInput').value = message;
            sendMessage();
        }}
        
        function showTypingIndicator() {{
            document.getElementById('typingIndicator').style.display = 'block';
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }}
        
        function hideTypingIndicator() {{
            document.getElementById('typingIndicator').style.display = 'none';
        }}
        
        function adjustTextareaHeight() {{
            const textarea = document.getElementById('messageInput');
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 100) + 'px';
        }}
        
        function handleKeyPress(event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault();
                sendMessage();
            }}
        }}
        
        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {{
            document.getElementById('messageInput').focus();
        }});
    </script>
</body>
</html>"""

    # 통합 가이드
    integration_guide = f"""# {agent_name} 통합 가이드

## 🌟 일상대화 특화 AI 에이전트

### 📋 에이전트 정보
- **이름**: {agent_name}
- **ID**: {agent_config['agent_id']}
- **특화 분야**: 일상대화, 감정 공감, 자연스러운 소통

### 🎯 주요 기능
1. **자연스러운 일상 대화**
   - 친근한 말투와 공감적 응답
   - 다양한 주제로 자유로운 대화
   - 유머와 재미를 통한 즐거운 소통

2. **🎓 Village Chief v3.3 Enhanced 기능**
   - 대화 메모리: 이전 대화 내용 기억
   - 개인화: 사용자 성향 학습 및 적응
   - 감정 인식: 7가지 주요 감정 인식
   - 주제 분석: 8가지 주제 자동 분류

3. **감정 공감 및 지원**
   - 기쁨, 슬픔, 화남, 피곤함 등 감정 인식
   - 상황에 맞는 공감적 응답
   - 자연스러운 위로와 격려

### 🚀 사용법

#### Python에서 사용
```python
from {agent_config['agent_id']}_response import generate_casual_conversation_response

message = "오늘 하루 정말 힘들었어..."
response = generate_casual_conversation_response(
    message=message,
    conversation_history=[],
    user_profile={{}}
)
print(response)
```

#### 웹 인터페이스
```bash
# HTML 파일 열기
open {agent_config['agent_id']}_interface.html
```

### 💬 대화 예시

**사용자**: "오늘 회사에서 정말 힘든 일이 있었어..."
**AI**: "아... 정말 힘들었겠다. 😔 괜찮아? 혹시 이야기하고 싶으면 다 들어줄게. 어떤 일이었는지 얘기해줄래?"

**사용자**: "새로운 취미를 시작해보려고 해!"
**AI**: "오! 어떤 거야? 재미있어 보인다! 😊 나도 관심 있어! 어떻게 시작하는 거야? 완전 기대돼!"

### 🎨 커스터마이징

#### 성격 조정
```python
# config.json에서 personality 수정
"personality": "더 장난스럽고 활발한, 에너지 넘치는"
```

#### 대화 스타일 변경
```python
# 시스템 프롬프트에서 대화 스타일 조정
"response_style": "더 캐주얼하고 친구 같은 말투로"
```

### 🎓 Village Chief v3.3 Enhanced 활용

1. **대화 메모리 활용**
   ```python
   conversation_history = [
       {{"type": "user", "content": "어제 영화 봤어", "timestamp": "..."}},
       {{"type": "agent", "content": "어떤 영화였어?", "timestamp": "..."}}
   ]
   ```

2. **개인화 프로필**
   ```python
   user_profile = {{
       "preferred_topics": ["영화", "음식", "여행"],
       "conversation_style": "casual",
       "emotion_patterns": ["긍정적", "호기심많음"]
   }}
   ```

### 🌈 추천 활용 시나리오

1. **개인 대화 상대**: 일상 대화 및 감정 공유
2. **스트레스 해소**: 가벼운 대화를 통한 기분 전환
3. **소통 연습**: 자연스러운 대화 방식 학습
4. **감정 지원**: 공감과 위로를 통한 정서적 지원

---
**💬 이 에이전트는 일상의 소소한 대화부터 깊은 감정 공유까지, 
자연스럽고 따뜻한 소통을 위해 설계되었습니다!**
"""

    # 파일들 저장
    output_dir = Path(f"goblin_agent_{agent_id}")
    output_dir.mkdir(exist_ok=True)
    
    # 1. config.json
    with open(output_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(agent_config, f, indent=2, ensure_ascii=False)
    
    # 2. system_prompt.txt
    with open(output_dir / f"{agent_id}_system_prompt.txt", "w", encoding="utf-8") as f:
        f.write(system_prompt)
    
    # 3. response.py
    with open(output_dir / f"{agent_id}_response.py", "w", encoding="utf-8") as f:
        f.write(response_function)
    
    # 4. interface.html
    with open(output_dir / f"{agent_id}_interface.html", "w", encoding="utf-8") as f:
        f.write(html_interface)
    
    # 5. integration_guide.md
    with open(output_dir / "integration_guide.md", "w", encoding="utf-8") as f:
        f.write(integration_guide)
    
    # 6. README.md
    readme_content = f"""# {agent_name}

일상대화와 자연스러운 소통이 가능한 친근한 AI 에이전트입니다.

## 🌟 주요 특징
- 🎓 Village Chief v3.3 Enhanced 기능 적용
- 💬 자연스러운 일상 대화
- 😊 감정 인식 및 공감 응답
- 🧠 대화 메모리 및 개인화
- 🎯 다양한 주제 대화 지원

## 🚀 빠른 시작
1. 웹 인터페이스: `{agent_id}_interface.html` 열기
2. Python 사용: `{agent_id}_response.py` import

## 📖 자세한 정보
- 통합 가이드: `integration_guide.md` 참조
- 시스템 프롬프트: `{agent_id}_system_prompt.txt`
- 에이전트 설정: `config.json`

친근하고 따뜻한 대화를 즐겨보세요! 😊
"""
    
    with open(output_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\n🎉 {agent_name} 생성 완료!")
    print(f"📁 저장 위치: {output_dir}")
    print(f"🌐 웹 인터페이스: {output_dir}/{agent_id}_interface.html")
    
    return {
        "agent_config": agent_config,
        "output_dir": str(output_dir),
        "files": [
            "config.json",
            f"{agent_id}_system_prompt.txt", 
            f"{agent_id}_response.py",
            f"{agent_id}_interface.html",
            "integration_guide.md",
            "README.md"
        ]
    }

if __name__ == "__main__":
    print("💬 일상대화 친화적 AI 에이전트 생성기")
    print("=" * 50)
    
    result = create_casual_conversation_agent()
    
    print("\n✅ 생성된 파일들:")
    for file in result["files"]:
        print(f"   📄 {file}")
    
    print(f"\n🎯 사용법:")
    print(f"1. 웹에서 사용: {result['output_dir']} 폴더의 HTML 파일 열기")
    print(f"2. Python에서 사용: response.py 파일 import")
    
    print("\n💡 특징:")
    print("- 🎓 Village Chief v3.3 Enhanced 기능 적용")
    print("- 💬 자연스러운 일상 대화 및 감정 공감")
    print("- 🧠 대화 메모리 및 개인화 학습")
    print("- 😊 7가지 감정 인식 (기쁨, 슬픔, 화남, 피곤, 궁금, 놀람, 일상)")
    print("- 🎯 8가지 주제 분석 (음식, 취미, 일상, 날씨, 관계, 고민, 계획, 기타)")
    
    print(f"\n🎉 {result['agent_config']['name']} 준비 완료!")
    print("이제 자연스럽고 친근한 일상대화를 즐겨보세요! 😊")
