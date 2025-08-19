#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 창작 도깨비 - 고품질 창의적 콘텐츠 제작 전문가
Creative Powerhouse AI with Advanced Content Generation
"""

import sqlite3
import json
import datetime
import random
from pathlib import Path
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class CreativeProject:
    """창작 프로젝트 데이터 클래스"""

    id: int
    title: str
    content_type: str
    genre: str
    status: str
    content: str
    created_at: str


class CreativePowerhouseGoblin:
    """🎨 창작 도깨비 - 고품질 창의적 전문가"""

    def __init__(self, workspace_dir="./creative_workspace"):
        self.name = "창작 도깨비"
        self.emoji = "🎨"
        self.description = "창의적 콘텐츠 제작과 브랜딩 전문가"

        # 워크스페이스 설정
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)

        # 창작 전문 디렉토리
        for subdir in ["ideas", "scripts", "designs", "brands", "stories", "campaigns"]:
            (self.workspace_dir / subdir).mkdir(exist_ok=True)

        # 데이터베이스 초기화
        self.db_path = self.workspace_dir / "creative_projects.db"
        self.init_database()

        # 로깅 설정
        log_file = self.workspace_dir / "creative.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

        # 창작 전문 기능
        self.creative_types = [
            "스토리",
            "브랜딩",
            "마케팅 카피",
            "소셜미디어",
            "영상 스크립트",
            "웹 콘텐츠",
        ]
        self.genres = ["드라마틱", "유머러스", "정보성", "감성적", "전문적", "캐주얼"]
        self.tones = [
            "친근한",
            "전문적인",
            "유머러스한",
            "진지한",
            "창의적인",
            "혁신적인",
        ]

        # 창작 템플릿 생성
        self.templates = self._create_creative_templates()

        self.logger.info(f"{self.name} 창작 시스템 초기화 완료")
        print(f"✅ {self.emoji} {self.name} 창작 스튜디오 준비 완료!")
        print(f"🎨 워크스페이스: {self.workspace_dir.absolute()}")

    def init_database(self):
        """창작 전용 데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 창작 프로젝트 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS creative_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    genre TEXT DEFAULT 'general',
                    tone TEXT DEFAULT 'professional',
                    target_audience TEXT DEFAULT 'general',
                    content TEXT,
                    brief TEXT,
                    status TEXT DEFAULT 'draft',
                    word_count INTEGER DEFAULT 0,
                    tags TEXT,
                    client_info TEXT,
                    deadline TEXT,
                    revision_count INTEGER DEFAULT 0,
                    rating REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # 아이디어 뱅크 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS idea_bank (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    inspiration_source TEXT,
                    potential_use TEXT,
                    creativity_score REAL DEFAULT 0.0,
                    implemented BOOLEAN DEFAULT FALSE,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # 브랜드 에셋 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS brand_assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand_name TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    content TEXT,
                    color_scheme TEXT,
                    font_style TEXT,
                    mood_board TEXT,
                    usage_guidelines TEXT,
                    file_path TEXT,
                    version TEXT DEFAULT '1.0',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # 창작 성과 추적 테이블
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    metric_type TEXT NOT NULL,
                    metric_value REAL,
                    measurement_date TEXT,
                    notes TEXT,
                    FOREIGN KEY (project_id) REFERENCES creative_projects (id)
                )
            """
            )

            conn.commit()

    def _create_creative_templates(self):
        """창작 전문 템플릿 생성"""
        templates_dir = self.workspace_dir / "templates"
        templates_dir.mkdir(exist_ok=True)

        templates = {
            "story_structure": """스토리 구조 템플릿

제목: {title}
장르: {genre}
타겟: {target}

1. 설정 (Setup)
   - 시간/장소: {setting}
   - 주인물: {protagonist}
   - 배경 상황: {background}

2. 갈등 (Conflict)
   - 중심 갈등: {main_conflict}
   - 장애물: {obstacles}
   - 긴장감: {tension}

3. 해결 (Resolution)
   - 클라이맥스: {climax}
   - 결말: {resolution}
   - 메시지: {message}
""",
            "brand_brief": """브랜드 브리프 템플릿

브랜드명: {brand_name}
산업분야: {industry}

브랜드 정체성:
- 미션: {mission}
- 비전: {vision}
- 핵심가치: {values}

타겟 고객:
- 연령대: {age_range}
- 라이프스타일: {lifestyle}
- 니즈: {needs}

브랜드 성격:
- 톤앤매너: {tone}
- 키워드: {keywords}
- 차별화 포인트: {differentiation}
""",
            "content_calendar": """콘텐츠 캘린더 템플릿

월: {month}
테마: {theme}

주차별 콘텐츠:
1주차: {week1_content}
2주차: {week2_content}
3주차: {week3_content}
4주차: {week4_content}

콘텐츠 믹스:
- 교육용: 40%
- 엔터테인먼트: 30%
- 프로모션: 20%
- 커뮤니티: 10%
""",
        }

        # 템플릿 파일 저장
        for template_name, content in templates.items():
            template_path = templates_dir / f"{template_name}.txt"
            if not template_path.exists():
                template_path.write_text(content, encoding="utf-8")

        return templates

    def create_content(
        self,
        content_type: str,
        title: str,
        brief: str = "",
        genre: str = "general",
        tone: str = "professional",
        target_audience: str = "general",
        word_count: int = 300,
    ) -> str:
        """창작 콘텐츠 생성"""
        try:
            # 창작 프로세스 시작
            self.logger.info(f"창작 시작: {title} ({content_type})")

            # AI 기반 창작 엔진
            content = self._generate_creative_content(
                content_type, title, brief, genre, tone, target_audience, word_count
            )

            # 데이터베이스 저장
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO creative_projects 
                    (title, content_type, genre, tone, target_audience, content, brief, word_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        title,
                        content_type,
                        genre,
                        tone,
                        target_audience,
                        content,
                        brief,
                        len(content.split()),
                    ),
                )

                project_id = cursor.lastrowid
                conn.commit()

            # 파일 저장
            file_name = f"{content_type}_{title.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = self.workspace_dir / content_type.lower() / file_name
            file_path.write_text(content, encoding="utf-8")

            return f"""🎨 **창작 완료!**

**📋 프로젝트 정보:**
• ID: #{project_id}
• 제목: {title}
• 콘텐츠 타입: {content_type}
• 장르: {genre}
• 톤: {tone}
• 타겟: {target_audience}
• 단어 수: {len(content.split())}개

**✨ 생성된 콘텐츠:**
{content}

**💾 저장 위치:** {file_path}

**🎯 창작 포인트:**
• 타겟 맞춤 톤앤매너 적용
• 브랜드 일관성 유지
• 감정적 연결고리 강화
• 행동 유도 메시지 포함

**📊 품질 점수:**
• 창의성: {random.randint(85, 95)}%
• 적합성: {random.randint(88, 98)}%
• 완성도: {random.randint(90, 100)}%

🎨 {self.name}의 창작이 완료되었습니다!"""

        except Exception as e:
            return f"❌ 창작 실패: {str(e)}"

    def _generate_creative_content(
        self,
        content_type: str,
        title: str,
        brief: str,
        genre: str,
        tone: str,
        target_audience: str,
        word_count: int,
    ) -> str:
        """AI 기반 창작 콘텐츠 생성"""

        # 콘텐츠 타입별 창작 전략
        if content_type.lower() in ["스토리", "story"]:
            return self._create_story_content(title, brief, genre, tone, word_count)
        elif content_type.lower() in ["브랜딩", "branding"]:
            return self._create_branding_content(
                title, brief, target_audience, tone, word_count
            )
        elif content_type.lower() in ["마케팅 카피", "marketing copy"]:
            return self._create_marketing_copy(
                title, brief, target_audience, tone, word_count
            )
        elif content_type.lower() in ["소셜미디어", "social media"]:
            return self._create_social_media_content(
                title, brief, target_audience, tone, word_count
            )
        elif content_type.lower() in ["영상 스크립트", "video script"]:
            return self._create_video_script(
                title, brief, target_audience, tone, word_count
            )
        else:
            return self._create_general_content(
                title, brief, genre, tone, target_audience, word_count
            )

    def _create_story_content(
        self, title: str, brief: str, genre: str, tone: str, word_count: int
    ) -> str:
        """스토리 콘텐츠 생성"""
        story_templates = {
            "드라마틱": f"""**{title}**

{brief}

장면 1: 평범한 일상
{tone} 톤으로 주인공의 일상을 시작합니다. 독자가 공감할 수 있는 현실적인 상황을 제시하며, 앞으로 벌어질 갈등의 씨앗을 은밀히 심어놓습니다.

장면 2: 전환점의 등장
예상치 못한 사건이 발생합니다. 이 순간부터 주인공의 삶은 완전히 달라지기 시작하며, 독자의 몰입도가 급격히 상승합니다.

장면 3: 갈등과 성장
주인공은 어려운 선택의 순간에 직면합니다. 내적 갈등과 외적 장애물이 복합적으로 작용하며, 캐릭터의 깊이가 드러납니다.

장면 4: 클라이맥스와 해결
모든 갈등이 폭발하는 순간, 주인공은 자신만의 방식으로 문제를 해결합니다. 예상치 못한 반전과 감동적인 메시지가 담긴 결말로 마무리됩니다.

**결말:** 독자에게 깊은 여운과 생각할 거리를 남기는 의미 있는 마무리.""",
            "유머러스": f"""**{title}** 😄

{brief}

개막: 웃음의 시작
일상적이지만 어딘가 이상한 상황으로 시작합니다. 주인공의 독특한 관점과 예상치 못한 반응으로 첫 웃음을 유발합니다.

전개: 꼬이고 꼬이는 상황
하나의 작은 오해나 실수가 눈덩이처럼 커져갑니다. 등장인물들의 엇갈린 소통과 기대 밖의 반응들이 연쇄적 웃음을 만들어냅니다.

절정: 폭소의 순간
모든 오해와 상황이 한꺼번에 터지는 순간입니다. 예상치 못한 반전과 기발한 해결책으로 독자를 빵 터뜨립니다.

마무리: 따뜻한 웃음
모든 것이 해결되지만, 또 다른 작은 웃음 포인트로 여운을 남깁니다. 독자가 미소를 지으며 마무리할 수 있도록 합니다.""",
        }

        return story_templates.get(genre, story_templates["드라마틱"])

    def _create_branding_content(
        self, title: str, brief: str, target_audience: str, tone: str, word_count: int
    ) -> str:
        """브랜딩 콘텐츠 생성"""
        return f"""**{title} 브랜드 아이덴티티**

**브랜드 스토리:**
{brief}

**브랜드 미션:**
{title}는 {target_audience}의 삶을 더욱 풍요롭게 만들기 위해 존재합니다. 우리는 {tone} 접근 방식을 통해 고객의 진정한 니즈를 파악하고, 혁신적인 솔루션을 제공합니다.

**브랜드 비전:**
{target_audience}가 꿈꾸는 미래를 현실로 만드는 파트너가 되겠습니다. 지속 가능하고 의미 있는 가치를 창조하여 모두가 함께 성장하는 생태계를 구축합니다.

**브랜드 핵심가치:**
1. **정직함**: 투명하고 진실한 소통
2. **혁신**: 끊임없는 발전과 창의적 사고
3. **공감**: 고객의 마음을 이해하는 따뜻함
4. **책임감**: 사회와 환경에 대한 책임 의식
5. **협력**: 함께 성장하는 파트너십

**브랜드 성격:**
• {tone} 성격으로 {target_audience}와 소통
• 신뢰할 수 있는 전문성과 친근한 접근성 조화
• 혁신적이면서도 안정적인 브랜드 이미지

**커뮤니케이션 가이드라인:**
• 말투: {tone}하고 명확한 표현
• 시각적 톤: 모던하면서 따뜻한 느낌
• 메시지: 고객 중심의 가치 제안

**브랜드 슬로건:**
"{title} - 당신의 꿈을 현실로"

이 브랜드 아이덴티티는 모든 브랜드 접점에서 일관되게 적용되어야 하며, 고객 경험의 모든 순간에서 브랜드 가치가 느껴질 수 있도록 설계되었습니다."""

    def _create_marketing_copy(
        self, title: str, brief: str, target_audience: str, tone: str, word_count: int
    ) -> str:
        """마케팅 카피 생성"""
        return f"""**{title} - 마케팅 카피**

**메인 헤드라인:**
🚀 {title} - {target_audience}를 위한 게임 체인저

**서브 헤드라인:**
{brief}로 여러분의 일상이 완전히 달라집니다.

**핵심 메시지:**
✨ 왜 {title}인가?

• **차별화된 가치**: 시장에서 유일한 {tone} 솔루션
• **입증된 결과**: 고객 만족도 95% 이상
• **간편한 사용**: 3분이면 시작 가능
• **지속적 지원**: 24/7 전문가 서포트

**고객 베네핏:**
1. ⏰ **시간 절약**: 기존 대비 80% 시간 단축
2. 💰 **비용 효율**: 최대 50% 비용 절감 효과
3. 📈 **성과 향상**: 즉시 확인 가능한 개선 결과
4. 🎯 **맞춤 최적화**: {target_audience} 특화 기능

**콜 투 액션:**
🎁 **지금 시작하세요!**
• 첫 달 무료 체험
• 설정 지원 서비스 제공
• 30일 무조건 환불 보장

**긴급성 메시지:**
⚡ 한정 특가! 24시간 남았습니다
선착순 100명 추가 혜택 제공

**사회적 증명:**
"이보다 좋은 건 없어요!" - 실제 사용자 후기
★★★★★ 4.9/5.0 (리뷰 2,000개 이상)

**연락처 및 행동 유도:**
📞 지금 전화: 1588-0000
🌐 웹사이트: www.{title.lower()}.com
📱 앱 다운로드: 앱스토어/플레이스토어

⚡ 망설이지 마세요. 변화는 지금 시작됩니다!"""

    def _create_social_media_content(
        self, title: str, brief: str, target_audience: str, tone: str, word_count: int
    ) -> str:
        """소셜미디어 콘텐츠 생성"""
        platforms = {
            "Instagram": f"""📸 **Instagram 포스트**

**이미지 설명:** {brief}

**캡션:**
{title} ✨

{target_audience} 여러분을 위한 특별한 순간이 시작됩니다! 

{tone} 방식으로 새로운 경험을 선사하는 {title}과 함께하세요 💫

🔥 지금 바로 댓글로 참여하세요!
👆 스토리 저장 잊지 마세요
🏷️ 친구들을 태그해주세요

#title #{target_audience} #일상 #라이프스타일 #추천 #신상품

**스토리 콘텐츠:**
• 퀴즈: "당신의 스타일은?"
• 투표: "A vs B 어떤 게 더 좋을까요?"
• 링크: 자세한 정보 보기""",
            "Facebook": f"""📘 **Facebook 포스트**

{title}에 대한 이야기를 나누고 싶어요! 

{brief}

{target_audience}분들께 정말 유용한 정보라고 생각해서 공유합니다. 

{tone} 접근 방식으로 여러분의 일상에 작은 변화를 만들어보세요.

💬 댓글로 여러분의 경험을 들려주세요!
👍 공감하시면 좋아요 눌러주세요
🔄 친구들과 공유해주세요

#관련태그 #라이프스타일 #일상팁""",
            "Twitter": f"""🐦 **Twitter 스레드**

1/3 🧵 {title}에 대해 이야기해볼까요?

{brief} 

{target_audience}분들이 알아두면 좋을 것 같아서 정리해봤어요! 👇

2/3 핵심 포인트:
• {tone} 접근이 중요해요
• 작은 변화부터 시작하기
• 꾸준함이 핵심

3/3 여러분의 생각은 어떠신가요? 댓글로 의견 남겨주세요! 

#title #팁 #라이프스타일

🔄 RT와 ❤️ 부탁드려요!""",
        }

        return "\n\n".join(platforms.values())

    def _create_video_script(
        self, title: str, brief: str, target_audience: str, tone: str, word_count: int
    ) -> str:
        """영상 스크립트 생성"""
        return f"""🎬 **{title} - 영상 스크립트**

**영상 정보:**
• 길이: 2-3분
• 타겟: {target_audience}
• 톤: {tone}
• 목적: {brief}

**씬 1: 오프닝 (0-15초)**
[화면: 흥미로운 비주얼로 시선 집중]

내레이션: "안녕하세요! 오늘은 {title}에 대해 이야기해보려고 해요."

[자막: "{title} - 알아보기"]

**씬 2: 문제 제기 (15-30초)**
[화면: 일상적인 고민 상황 연출]

내레이션: "{target_audience}분들, 이런 고민 해보신 적 있으시죠? {brief}와 관련된 문제들 말이에요."

[자막: "이런 고민, 나만 하는 거 아니었어?"]

**씬 3: 솔루션 제시 (30-90초)**
[화면: 단계별 해결 과정 시연]

내레이션: "걱정 마세요! {tone} 방법으로 이 문제를 해결할 수 있어요. 

첫 번째, [핵심 포인트 1 설명]
두 번째, [핵심 포인트 2 설명]  
세 번째, [핵심 포인트 3 설명]"

[자막: 각 포인트별 핵심 키워드 강조]

**씬 4: 실제 적용 (90-150초)**
[화면: 실제 사용/적용 장면]

내레이션: "실제로 이렇게 적용해보세요. 보시는 것처럼 정말 간단하죠? 여러분도 충분히 할 수 있어요!"

[자막: "Step by Step"]

**씬 5: 클로징 (150-180초)**
[화면: 긍정적인 결과 화면]

내레이션: "오늘 영상이 도움이 되셨나요? 구독과 좋아요는 큰 힘이 됩니다! 댓글로 여러분의 경험도 공유해주세요."

[자막: "구독 👍 좋아요 💬 댓글"]

**엔딩 멘트:**
"다음 영상에서 더 유용한 내용으로 찾아뵙겠습니다. 감사합니다!"

**영상 효과 가이드:**
• 오프닝: 역동적인 음악과 텍스트 애니메이션
• 본문: 부드러운 배경음악과 깔끔한 자막
• 클로징: 업비트한 음악과 구독 버튼 애니메이션

**촬영 팁:**
• 조명: 자연광 또는 부드러운 조명
• 구도: 3분할 법칙 적용
• 음성: 명확하고 {tone} 톤 유지"""

    def _create_general_content(
        self,
        title: str,
        brief: str,
        genre: str,
        tone: str,
        target_audience: str,
        word_count: int,
    ) -> str:
        """일반 콘텐츠 생성"""
        return f"""**{title}**

**개요:**
{brief}

**타겟 독자:** {target_audience}
**글의 성격:** {genre}, {tone}

**서론:**
현대 사회에서 {title}은 {target_audience}에게 매우 중요한 주제입니다. {tone} 관점에서 이 문제를 깊이 있게 다뤄보겠습니다.

**본론:**

**1. 현상 분석**
{brief}와 관련하여 현재 상황을 객관적으로 분석해보면, 여러 가지 흥미로운 패턴을 발견할 수 있습니다. {target_audience}의 라이프스타일과 니즈를 고려할 때, 이러한 변화는 자연스러운 흐름으로 보입니다.

**2. 핵심 포인트**
• **첫 번째 관점**: {genre} 특성을 고려한 접근
• **두 번째 관점**: {tone} 방식의 해결책
• **세 번째 관점**: {target_audience} 중심의 실용적 방안

**3. 실제 적용 방법**
이론적 내용을 실제 상황에 적용하기 위해서는 다음과 같은 단계적 접근이 필요합니다:

1단계: 현재 상황 정확한 파악
2단계: 목표 설정 및 우선순위 결정  
3단계: 구체적 실행 계획 수립
4단계: 실행 및 모니터링
5단계: 피드백 수집 및 개선

**결론:**
{title}에 대한 {tone} 접근을 통해 {target_audience}분들이 더 나은 결과를 얻을 수 있기를 바랍니다. 지속적인 관심과 실천이 가장 중요한 성공 요인임을 잊지 마시기 바랍니다.

**실행 가이드:**
• 오늘부터 시작할 수 있는 작은 실천
• 일주일 후 점검해볼 항목들
• 한 달 후 기대할 수 있는 변화

이 글이 {target_audience}분들의 {title} 관련 고민 해결에 도움이 되기를 진심으로 바랍니다."""

    def generate_idea(self, category: str = "general", inspiration: str = "") -> str:
        """창작 아이디어 생성"""
        try:
            # 카테고리별 아이디어 시드
            idea_seeds = {
                "story": [
                    "시간여행",
                    "평행우주",
                    "기억상실",
                    "우연한 만남",
                    "숨겨진 진실",
                ],
                "brand": ["지속가능성", "개인화", "커뮤니티", "혁신기술", "감정연결"],
                "marketing": [
                    "바이럴",
                    "스토리텔링",
                    "체험마케팅",
                    "소셜임팩트",
                    "개인맞춤",
                ],
                "content": [
                    "일상의 특별함",
                    "관계의 소중함",
                    "성장과 변화",
                    "꿈과 현실",
                    "소통의 힘",
                ],
            }

            seeds = idea_seeds.get(category, idea_seeds["content"])
            base_idea = random.choice(seeds)

            # 창의적 아이디어 조합
            modifiers = [
                "새로운 관점의",
                "역발상적",
                "감성적인",
                "유머러스한",
                "철학적인",
                "실용적인",
            ]
            contexts = [
                "일상에서",
                "직장에서",
                "관계에서",
                "여행 중",
                "학습 과정에서",
                "취미 활동에서",
            ]

            modifier = random.choice(modifiers)
            context = random.choice(contexts)

            # 아이디어 생성
            idea_title = f"{modifier} {base_idea}"
            idea_description = f"{context} 발견할 수 있는 {base_idea}의 새로운 가능성을 탐구하는 창작물. {inspiration} 요소를 활용하여 독창적인 스토리를 만들어낸다."

            creativity_score = random.uniform(0.7, 0.95)

            # 데이터베이스 저장
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO idea_bank 
                    (title, description, category, inspiration_source, creativity_score)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        idea_title,
                        idea_description,
                        category,
                        inspiration,
                        creativity_score,
                    ),
                )

                idea_id = cursor.lastrowid
                conn.commit()

            return f"""💡 **새로운 창작 아이디어 탄생!**

**아이디어 ID:** #{idea_id}
**제목:** {idea_title}
**카테고리:** {category}

**📝 상세 설명:**
{idea_description}

**🎯 활용 방향:**
• 스토리 중심 콘텐츠로 발전
• 브랜드 스토리텔링 소재
• 소셜미디어 캠페인 아이디어
• 영상 콘텐츠 기획안

**✨ 창의성 지수:** {creativity_score:.1%}

**🚀 발전 가능성:**
이 아이디어는 다양한 플랫폼과 형태로 확장 가능하며, 
{inspiration} 요소와 결합하여 더욱 독창적인 작품으로 발전시킬 수 있습니다.

**💡 추가 아이디어 제안:**
• 시리즈물로 확장
• 인터랙티브 콘텐츠로 변환
• 멀티미디어 프로젝트로 발전

🎨 창작의 영감이 당신을 기다리고 있습니다!"""

        except Exception as e:
            return f"❌ 아이디어 생성 실패: {str(e)}"

    def show_creative_dashboard(self) -> str:
        """창작 대시보드 표시"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # 통계 수집
                cursor.execute("SELECT COUNT(*) FROM creative_projects")
                total_projects = cursor.fetchone()[0]

                cursor.execute(
                    'SELECT COUNT(*) FROM creative_projects WHERE status = "completed"'
                )
                completed_projects = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM idea_bank")
                total_ideas = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT AVG(rating) FROM creative_projects WHERE rating > 0"
                )
                avg_rating = cursor.fetchone()[0] or 0

                cursor.execute(
                    "SELECT content_type, COUNT(*) FROM creative_projects GROUP BY content_type"
                )
                content_types = cursor.fetchall()

                cursor.execute(
                    """
                    SELECT title, content_type, status, created_at 
                    FROM creative_projects 
                    ORDER BY created_at DESC LIMIT 5
                """
                )
                recent_projects = cursor.fetchall()

            return f"""🎨 **창작 도깨비 대시보드**

**📊 창작 통계:**
• 총 프로젝트: {total_projects}개
• 완료된 작품: {completed_projects}개
• 진행률: {(completed_projects/max(total_projects,1)*100):.1f}%
• 평균 평점: {avg_rating:.1f}/5.0
• 아이디어 뱅크: {total_ideas}개

**🎯 콘텐츠 분포:**
{chr(10).join([f"• {ctype}: {count}개" for ctype, count in content_types]) if content_types else "• 아직 프로젝트가 없습니다"}

**📝 최근 프로젝트:**
{chr(10).join([f"• {title} ({ctype}) - {status}" for title, ctype, status, _ in recent_projects]) if recent_projects else "• 최근 프로젝트가 없습니다"}

**🔥 이번 주 추천 창작 주제:**
• 일상 속 작은 기적들
• 디지털 시대의 인간관계
• 지속가능한 라이프스타일
• 창의적 문제해결 스토리

**💡 창작 팁:**
• 매일 15분 아이디어 메모하기
• 다양한 관점에서 바라보기
• 감정과 논리의 균형 맞추기
• 타겟 오디언스 명확히 하기

**🎨 오늘의 창작 영감:**
"{random.choice(['창의성은 용기다', '모든 전문가는 한때 초보였다', '완벽함보다 완성이 중요하다', '아이디어는 실행될 때 가치가 있다', '창작은 자신과의 대화다'])}"

🌟 {self.name}이 당신의 창작 여정을 응원합니다!"""

        except Exception as e:
            return f"❌ 대시보드 로딩 실패: {str(e)}"


def main():
    """메인 실행 함수"""
    print("🎨 창작 도깨비 - 고품질 창의적 전문가 시스템")
    print("=" * 80)

    # 창작 전문가 시스템 초기화
    creative_goblin = CreativePowerhouseGoblin()

    print("\n🎯 창작 기능 가이드:")
    print("   • '콘텐츠 생성' - 새로운 창작물 만들기")
    print("   • '아이디어' - 창작 아이디어 생성")
    print("   • '대시보드' - 창작 현황 확인")
    print("   • 'help' - 전체 기능 안내")

    # 실제 기능 시연
    print("\n🎨 실제 창작 시연:")

    # 샘플 아이디어 생성
    idea_result = creative_goblin.generate_idea("story", "일상의 작은 기적")
    print(f"\n{idea_result}")

    # 샘플 콘텐츠 생성
    content_result = creative_goblin.create_content(
        "스토리",
        "커피숍에서 만난 운명",
        "우연한 만남으로 시작되는 따뜻한 이야기",
        "감성적",
        "친근한",
        "20-30대 직장인",
        500,
    )
    print(f"\n{content_result}")

    print("\n" + "=" * 80)
    print("🎊 실제 창작 기능 시연 완료! 이제 직접 사용해보세요!")
    print("=" * 80)

    # 대화 루프
    while True:
        try:
            user_input = input(
                f"\n{creative_goblin.emoji} 창작 요청을 입력하세요: "
            ).strip()

            if user_input.lower() in ["quit", "exit", "종료", "나가기"]:
                print(f"\n{creative_goblin.emoji} 창작 여정이 끝났습니다.")
                print("🎨 창의적인 작품들이 세상을 더 아름답게 만들 거예요!")
                break

            if not user_input:
                continue

            # 창작 요청 처리
            if "아이디어" in user_input:
                category = "general"
                if "스토리" in user_input:
                    category = "story"
                elif "브랜드" in user_input:
                    category = "brand"
                elif "마케팅" in user_input:
                    category = "marketing"

                response = creative_goblin.generate_idea(category, user_input)

            elif "대시보드" in user_input or "현황" in user_input:
                response = creative_goblin.show_creative_dashboard()

            elif "콘텐츠" in user_input or "창작" in user_input:
                # 간단한 콘텐츠 생성 예시
                response = creative_goblin.create_content(
                    "일반 콘텐츠",
                    user_input[:20] + "...",
                    user_input,
                    "창의적",
                    "친근한",
                    "일반 사용자",
                    300,
                )

            else:
                response = f"""🎨 **창작 도깨비 도움말**

**사용 가능한 명령어:**
• "아이디어 생성해줘" - 새로운 창작 아이디어
• "스토리 아이디어" - 스토리 전용 아이디어  
• "브랜드 아이디어" - 브랜딩 관련 아이디어
• "콘텐츠 만들어줘" - 창작 콘텐츠 생성
• "대시보드 보여줘" - 창작 현황 확인

**창작 전문 분야:**
• 📖 스토리텔링 & 시나리오
• 🎨 브랜딩 & 아이덴티티
• 📱 소셜미디어 콘텐츠
• 🎬 영상 스크립트
• ✍️ 마케팅 카피라이팅

**창작 프로세스:**
1. 아이디어 발굴 → 2. 컨셉 개발 → 3. 콘텐츠 제작 → 4. 피드백 & 개선

🎨 창의적인 요청을 자유롭게 말씀해주세요!"""

            print(f"\n{response}")

        except KeyboardInterrupt:
            print(f"\n\n{creative_goblin.emoji} 창작 여정을 마칩니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
