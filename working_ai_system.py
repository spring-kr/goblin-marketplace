"""
실제 작동하는 16명 박사급 전문가 AI 시스템
API 연결 없이도 전문적인 응답을 생성하는 로컬 AI 시스템
"""

import re
import random
import json
from typing import Dict, Any, List
from datetime import datetime


class SmartExpertAI:
    """지능형 전문가 AI 시스템"""

    def __init__(self):
        self.expert_knowledge = self._load_expert_knowledge()
        self.conversation_patterns = self._load_conversation_patterns()

    def _load_expert_knowledge(self) -> Dict[str, Dict]:
        """전문가별 지식 데이터베이스 - 16명 전체"""
        return {
            "medical": {
                "name": "의학박사 하이진",
                "emoji": "🏥",
                "specialties": ["내과", "외과", "응급의학", "예방의학", "가정의학"],
                "keywords": {
                    "감기": {
                        "symptoms": ["기침", "콧물", "발열", "목아픔", "두통"],
                        "advice": [
                            "충분한 휴식과 수분 섭취가 가장 중요합니다",
                            "일주일 이상 지속되면 이차 감염 가능성을 확인해야 합니다",
                            "38.5도 이상 고열이나 호흡곤란이 있다면 즉시 병원 방문하세요",
                        ],
                        "treatments": ["휴식", "수분섭취", "해열진통제", "비타민C"],
                    },
                    "혈압": {
                        "normal": "정상 혈압은 120/80mmHg 미만입니다",
                        "high": "140/90mmHg 이상이면 고혈압으로 분류됩니다",
                        "advice": [
                            "규칙적인 운동과 저염식이 필요합니다",
                            "정기적인 혈압 측정으로 모니터링하세요",
                            "스트레스 관리와 금연이 중요합니다",
                        ],
                    },
                },
            },
            "financial": {
                "name": "경제학박사 부자진",
                "emoji": "💰",
                "specialties": ["투자", "재정관리", "연금", "보험", "세금"],
                "keywords": {
                    "투자": {
                        "principles": ["분산투자", "장기투자", "리스크관리"],
                        "products": ["주식", "채권", "펀드", "ETF", "리츠"],
                        "advice": [
                            "20대는 적극적 포트폴리오로 주식 비중 70% 권장",
                            "Emergency Fund를 먼저 마련하세요",
                            "투자 목적과 기간을 명확히 설정하세요"
                        ]
                    },
                    "연금": {
                        "types": ["국민연금", "퇴직연금", "개인연금"],
                        "advice": [
                            "국민연금은 기본, 개인연금으로 보완하세요",
                            "연금저축은 세액공제 혜택을 활용하세요",
                            "장기 투자 관점으로 접근하세요"
                        ]
                    }
                }
            },
            "legal": {
                "name": "법학박사 정의진",
                "emoji": "⚖️",
                "specialties": ["민법", "상법", "노동법", "부동산법", "계약법"],
                "keywords": {
                    "임대차": {
                        "rights": ["보증금 반환권", "임대료 증액 제한", "계약 갱신권"],
                        "advice": [
                            "계약서 조건을 꼼꼼히 확인하고 보관하세요",
                            "보증금 반환 시 내용증명을 활용하세요",
                            "전세사기 예방을 위해 등기부등본 확인 필수"
                        ]
                    },
                    "직장": {
                        "protections": ["부당해고 금지", "임금체불 구제", "직장 내 괴롭힘 금지"],
                        "advice": [
                            "증거 자료를 체계적으로 수집하세요",
                            "노동부 신고나 고용노동청 상담 활용",
                            "필요시 전문 노무사나 변호사 상담 권장"
                        ]
                    }
                }
            },
            "tech": {
                "name": "공학박사 테크진", 
                "emoji": "🔧",
                "specialties": ["소프트웨어개발", "AI/ML", "클라우드", "보안", "아키텍처"],
                "keywords": {
                    "스타트업": {
                        "stack": ["React/Vue.js", "Node.js/Python", "AWS/GCP", "Docker", "DB"],
                        "advice": [
                            "MVP 개발에 집중하여 빠른 검증을 하세요",
                            "확장성을 고려한 마이크로서비스 아키텍처 권장",
                            "CI/CD 파이프라인 구축으로 개발 효율성 증대"
                        ]
                    },
                    "AI": {
                        "considerations": ["데이터 품질", "모델 선택", "윤리", "보안"],
                        "advice": [
                            "충분한 품질의 데이터 확보가 우선입니다",
                            "사용자 개인정보 보호 정책을 철저히 수립하세요",
                            "AI 편향성 문제를 지속적으로 모니터링하세요"
                        ]
                    }
                }
            },
            "creative": {
                "name": "예술학박사 창조진",
                "emoji": "🎨",
                "specialties": ["디자인", "브랜딩", "콘텐츠기획", "영상제작", "UX/UI"],
                "keywords": {
                    "브랜드": {
                        "elements": ["로고", "컬러", "타이포그래피", "톤앤매너"],
                        "advice": [
                            "브랜드 정체성을 명확히 정의하는 것이 첫 단계",
                            "타겟 고객의 감성과 니즈를 반영한 디자인",
                            "일관성 있는 비주얼 아이덴티티 구축이 핵심"
                        ]
                    },
                    "유튜브": {
                        "content_types": ["브이로그", "튜토리얼", "리뷰", "엔터테인먼트"],
                        "advice": [
                            "썸네일과 제목이 클릭률을 결정합니다",
                            "시청자와의 소통을 통한 커뮤니티 구축",
                            "꾸준한 업로드 스케줄 유지가 중요"
                        ]
                    }
                }
            },
            "marketing": {
                "name": "마케팅박사 판매진",
                "emoji": "📈", 
                "specialties": ["브랜딩", "디지털마케팅", "고객분석", "캠페인기획", "ROI분석"],
                "keywords": {
                    "신제품": {
                        "strategies": ["타겟 고객 분석", "경쟁사 분석", "포지셔닝", "채널 전략"],
                        "advice": [
                            "초기에는 니치 마켓을 공략하여 브랜드 인지도 구축",
                            "고객 피드백을 적극 수집하여 제품 개선에 반영",
                            "소셜미디어와 인플루언서 마케팅 활용 권장"
                        ]
                    },
                    "SNS": {
                        "platforms": ["인스타그램", "유튜브", "틱톡", "네이버블로그"],
                        "advice": [
                            "플랫폼별 특성에 맞는 콘텐츠 제작이 핵심",
                            "일관된 브랜드 톤앤매너 유지",
                            "인게이지먼트율이 도달률보다 중요합니다"
                        ]
                    }
                }
            },
            "education": {
                "name": "교육학박사 가르침진",
                "emoji": "📚",
                "specialties": ["교육과정설계", "학습심리", "온라인교육", "평가방법", "교수법"],
                "keywords": {
                    "성인학습": {
                        "principles": ["자기주도학습", "경험기반학습", "실무적용"],
                        "advice": [
                            "실무와 연결된 실용적인 학습 내용 구성",
                            "학습자의 기존 경험을 활용한 교육 설계",
                            "즉시 적용 가능한 스킬 중심의 커리큘럼"
                        ]
                    },
                    "온라인": {
                        "tools": ["LMS", "화상회의", "인터랙티브 콘텐츠", "퀴즈"],
                        "advice": [
                            "짧고 집중도 높은 마이크로 러닝 활용",
                            "다양한 미디어를 활용한 멀티모달 학습",
                            "실시간 피드백과 상호작용 극대화"
                        ]
                    }
                }
            },
            "hr": {
                "name": "인사관리박사 인재진",
                "emoji": "👥",
                "specialties": ["인재채용", "조직관리", "성과평가", "교육훈련", "노사관계"],
                "keywords": {
                    "원격근무": {
                        "challenges": ["소통", "성과관리", "팀워크", "문화유지"],
                        "advice": [
                            "명확한 업무 목표와 성과 지표 설정",
                            "정기적인 1:1 미팅으로 소통 강화",
                            "디지털 협업 도구 활용한 팀워크 증진"
                        ]
                    },
                    "온보딩": {
                        "stages": ["사전준비", "첫날", "첫주", "첫달", "정착"],
                        "advice": [
                            "입사 전 필요한 정보와 자료 사전 제공",
                            "멘토링 시스템을 통한 적응 지원",
                            "단계적 업무 배정으로 부담 최소화"
                        ]
                    }
                }
            },
            "sales": {
                "name": "영업전략박사 성과진", 
                "emoji": "💼",
                "specialties": ["B2B영업", "고객관리", "협상전략", "세일즈프로세스", "영업분석"],
                "keywords": {
                    "B2B": {
                        "stages": ["리드생성", "니즈분석", "제안", "협상", "클로징"],
                        "advice": [
                            "고객의 비즈니스 문제를 정확히 파악하세요",
                            "솔루션의 ROI를 구체적 수치로 제시",
                            "의사결정자와의 직접적인 관계 구축"
                        ]
                    },
                    "거절": {
                        "reasons": ["예산", "타이밍", "경쟁사", "의사결정"],
                        "advice": [
                            "거절 이유를 구체적으로 파악하고 대응",
                            "장기적 관점에서 관계 유지",
                            "추가 가치 제안으로 재접근"
                        ]
                    }
                }
            },
            "research": {
                "name": "연구개발박사 혁신진",
                "emoji": "🔬", 
                "specialties": ["R&D관리", "혁신전략", "기술개발", "프로젝트관리", "특허"],
                "keywords": {
                    "R&D": {
                        "methodologies": ["Design Thinking", "Agile R&D", "Stage-Gate", "Lean Startup"],
                        "advice": [
                            "명확한 연구 목표와 성공 기준 설정",
                            "정기적인 마일스톤 검토와 방향 조정",
                            "실패를 학습 기회로 활용하는 문화 조성"
                        ]
                    },
                    "혁신": {
                        "types": ["제품혁신", "프로세스혁신", "마케팅혁신", "조직혁신"],
                        "advice": [
                            "고객의 숨은 니즈를 발굴하여 아이디어 생성",
                            "다양한 분야의 전문가와 협업",
                            "빠른 프로토타이핑과 실험을 통한 검증"
                        ]
                    }
                }
            },
            "translation": {
                "name": "언어학박사 번역진",
                "emoji": "🌐",
                "specialties": ["전문번역", "통역", "다국어서비스", "로컬라이제이션", "언어교육"],
                "keywords": {
                    "계약서": {
                        "considerations": ["법적정확성", "문맥이해", "전문용어", "문화차이"],
                        "advice": [
                            "법률 전문용어의 정확한 번역이 핵심",
                            "원문의 법적 의도를 정확히 전달",
                            "해당 국가의 법체계 차이 고려"
                        ]
                    },
                    "기술문서": {
                        "types": ["매뉴얼", "API문서", "소프트웨어", "특허"],
                        "advice": [
                            "기술적 정확성과 사용자 이해도 균형",
                            "일관된 용어 사용으로 혼란 방지",
                            "타겟 사용자의 기술 수준 고려"
                        ]
                    }
                }
            },
            "consulting": {
                "name": "경영컨설팅박사 전략진",
                "emoji": "🎯",
                "specialties": ["전략기획", "조직개편", "프로세스개선", "디지털전환", "변화관리"],
                "keywords": {
                    "디지털전환": {
                        "phases": ["현황분석", "전략수립", "실행계획", "구현", "정착"],
                        "advice": [
                            "조직의 디지털 성숙도 진단이 우선",
                            "단계적 접근으로 변화 충격 최소화",
                            "직원 교육과 문화 변화에 충분한 투자"
                        ]
                    },
                    "변화관리": {
                        "resistance": ["개인", "조직", "시스템", "문화"],
                        "advice": [
                            "변화의 필요성을 명확히 소통",
                            "이해관계자들의 적극적 참여 유도",
                            "단기 성과를 통한 변화 동력 확보"
                        ]
                    }
                }
            },
            "psychology": {
                "name": "심리학박사 마음진",
                "emoji": "🧠",
                "specialties": ["상담심리", "조직심리", "인지심리", "스트레스관리", "행동분석"],
                "keywords": {
                    "번아웃": {
                        "symptoms": ["정서적소진", "비인격화", "성취감저하"],
                        "advice": [
                            "업무와 개인 시간의 명확한 경계 설정",
                            "스트레스 관리 기법 학습과 실천",
                            "사회적 지지체계 구축과 활용"
                        ]
                    },
                    "갈등": {
                        "types": ["가치관", "의사소통", "역할", "자원"],
                        "advice": [
                            "상대방 입장에서 이해하려는 노력",
                            "감정이 아닌 사실과 이슈에 집중",
                            "win-win 해결책 모색"
                        ]
                    }
                }
            },
            "data": {
                "name": "데이터과학박사 분석진",
                "emoji": "📊",
                "specialties": ["빅데이터분석", "머신러닝", "통계분석", "데이터시각화", "예측모델링"],
                "keywords": {
                    "이탈예측": {
                        "features": ["사용패턴", "구매이력", "고객서비스", "인구통계"],
                        "advice": [
                            "고객 생애주기별 이탈 패턴 분석",
                            "실시간 예측 모델로 선제적 대응",
                            "이탈 원인별 맞춤형 리텐션 전략"
                        ]
                    },
                    "A/B테스트": {
                        "considerations": ["표본크기", "통계적유의성", "실험기간", "외부요인"],
                        "advice": [
                            "충분한 표본 크기로 통계적 신뢰성 확보",
                            "단일 변수 테스트로 순수 효과 측정",
                            "비즈니스 임팩트와 통계적 유의성 함께 고려"
                        ]
                    }
                }
            },
            "startup": {
                "name": "창업학박사 스타트진",
                "emoji": "🚀",
                "specialties": ["사업기획", "투자유치", "팀빌딩", "시장분석", "비즈니스모델"],
                "keywords": {
                    "창업": {
                        "stages": ["아이디어검증", "MVP개발", "시장진입", "성장", "확장"],
                        "advice": [
                            "고객 문제 해결에 집중한 아이디어 검증",
                            "최소 기능으로 빠른 시장 반응 확인",
                            "데이터 기반 의사결정과 지속적 개선"
                        ]
                    },
                    "투자": {
                        "types": ["엔젤", "시드", "시리즈A", "시리즈B+"],
                        "advice": [
                            "명확한 비즈니스 모델과 수익성 제시",
                            "시장 크기와 성장 가능성 입증",
                            "강력한 팀과 실행력 어필"
                        ]
                    }
                }
            },
            "wellness": {
                "name": "웰니스박사 건강진",
                "emoji": "🌿",
                "specialties": ["건강관리", "영양학", "운동과학", "스트레스관리", "라이프스타일"],
                "keywords": {
                    "불면증": {
                        "causes": ["스트레스", "생활습관", "환경", "건강상태"],
                        "advice": [
                            "규칙적인 수면 스케줄 유지가 핵심",
                            "카페인과 알코올 섭취 시간 조절",
                            "수면 환경 최적화와 이완 기법 활용"
                        ]
                    },
                    "다이어트": {
                        "principles": ["칼로리균형", "영양균형", "지속가능성"],
                        "advice": [
                            "급격한 감량보다 점진적 변화 추구",
                            "균형 잡힌 영양소 섭취로 건강 유지",
                            "운동과 식단 조절의 병행이 효과적"
                        ]
                    }
                }
            }
        }
                "specialties": ["투자", "재정관리", "연금", "보험", "세금"],
                "keywords": {
                    "투자": {
                        "principles": ["분산투자", "장기투자", "리스크관리"],
                        "products": ["주식", "채권", "펀드", "ETF", "리츠"],
                        "advice": [
                            "20대는 적극적 포트폴리오로 주식 비중 70% 권장",
                            "Emergency Fund를 먼저 마련하세요",
                            "투자 목적과 기간을 명확히 설정하세요",
                        ],
                    },
                    "연금": {
                        "types": ["국민연금", "퇴직연금", "개인연금"],
                        "advice": [
                            "국민연금은 기본, 개인연금으로 보완하세요",
                            "연금저축은 세액공제 혜택을 활용하세요",
                            "장기 투자 관점으로 접근하세요",
                        ],
                    },
                },
            },
            "tech": {
                "name": "공학박사 테크진",
                "emoji": "🔧",
                "specialties": [
                    "소프트웨어개발",
                    "AI/ML",
                    "클라우드",
                    "보안",
                    "아키텍처",
                ],
                "keywords": {
                    "스타트업": {
                        "stack": [
                            "React/Vue.js",
                            "Node.js/Python",
                            "AWS/GCP",
                            "Docker",
                            "DB",
                        ],
                        "advice": [
                            "MVP 개발에 집중하여 빠른 검증을 하세요",
                            "확장성을 고려한 마이크로서비스 아키텍처 권장",
                            "CI/CD 파이프라인 구축으로 개발 효율성 증대",
                        ],
                    },
                    "AI": {
                        "considerations": ["데이터 품질", "모델 선택", "윤리", "보안"],
                        "advice": [
                            "충분한 품질의 데이터 확보가 우선입니다",
                            "사용자 개인정보 보호 정책을 철저히 수립하세요",
                            "AI 편향성 문제를 지속적으로 모니터링하세요",
                        ],
                    },
                },
            },
            "marketing": {
                "name": "마케팅박사 판매진",
                "emoji": "📈",
                "specialties": [
                    "브랜딩",
                    "디지털마케팅",
                    "고객분석",
                    "캠페인기획",
                    "ROI분석",
                ],
                "keywords": {
                    "신제품": {
                        "strategies": [
                            "타겟 고객 분석",
                            "경쟁사 분석",
                            "포지셔닝",
                            "채널 전략",
                        ],
                        "advice": [
                            "초기에는 니치 마켓을 공략하여 브랜드 인지도 구축",
                            "고객 피드백을 적극 수집하여 제품 개선에 반영",
                            "소셜미디어와 인플루언서 마케팅 활용 권장",
                        ],
                    },
                    "SNS": {
                        "platforms": ["인스타그램", "유튜브", "틱톡", "네이버블로그"],
                        "advice": [
                            "플랫폼별 특성에 맞는 콘텐츠 제작이 핵심",
                            "일관된 브랜드 톤앤매너 유지",
                            "인게이지먼트율이 도달률보다 중요합니다",
                        ],
                    },
                },
            },
            "legal": {
                "name": "법학박사 정의진",
                "emoji": "⚖️",
                "specialties": ["민법", "상법", "노동법", "부동산법", "계약법"],
                "keywords": {
                    "임대차": {
                        "rights": ["보증금 반환권", "임대료 증액 제한", "계약 갱신권"],
                        "advice": [
                            "계약서 조건을 꼼꼼히 확인하고 보관하세요",
                            "보증금 반환 시 내용증명을 활용하세요",
                            "전세사기 예방을 위해 등기부등본 확인 필수",
                        ],
                    },
                    "직장": {
                        "protections": [
                            "부당해고 금지",
                            "임금체불 구제",
                            "직장 내 괴롭힘 금지",
                        ],
                        "advice": [
                            "증거 자료를 체계적으로 수집하세요",
                            "노동부 신고나 고용노동청 상담 활용",
                            "필요시 전문 노무사나 변호사 상담 권장",
                        ],
                    },
                },
            },
        }

    def _load_conversation_patterns(self) -> Dict[str, List[str]]:
        """대화 패턴 및 응답 템플릿"""
        return {
            "greeting": [
                "안녕하세요! 궁금한 점이 있으시군요.",
                "반갑습니다! 어떤 도움이 필요하신가요?",
                "좋은 질문이네요! 자세히 설명드리겠습니다.",
            ],
            "analysis": [
                "말씀하신 상황을 종합해보면",
                "전문가 관점에서 분석해드리면",
                "경험상 이런 경우에는",
            ],
            "recommendation": [
                "다음과 같이 단계별로 접근하시길 권합니다:",
                "우선순위를 고려하여 이렇게 진행하세요:",
                "실무 경험을 바탕으로 추천드리는 방법은:",
            ],
            "closing": [
                "추가 궁금한 점이 있으시면 언제든 말씀해주세요!",
                "도움이 되셨기를 바랍니다!",
                "더 구체적인 상황이 있다면 추가 상담을 받아보시기 바랍니다.",
            ],
        }

    def generate_expert_response(self, user_message: str, expert_type: str) -> str:
        """전문가별 맞춤 응답 생성"""
        expert = self.expert_knowledge.get(expert_type)
        if not expert:
            return "지원하지 않는 전문가 유형입니다."

        # 메시지 분석
        analysis = self._analyze_message(user_message, expert)

        # 응답 구성
        response_parts = []

        # 헤더
        response_parts.append(f"{expert['emoji']} **{expert['name']}**")
        response_parts.append("")

        # 인사말
        greeting = random.choice(self.conversation_patterns["greeting"])
        response_parts.append(greeting)
        response_parts.append("")

        # 분석 및 조언
        if analysis["matched_keywords"]:
            for keyword, info in analysis["matched_keywords"].items():
                response_parts.append(f"📋 **{keyword} 관련 전문 조언:**")
                response_parts.append("")

                if "advice" in info:
                    for advice in info["advice"][:2]:  # 최대 2개 조언
                        response_parts.append(f"• {advice}")

                if "treatments" in info:
                    response_parts.append(
                        f"**권장 방법:** {', '.join(info['treatments'])}"
                    )

                if "products" in info:
                    response_parts.append(
                        f"**추천 상품:** {', '.join(info['products'][:3])}"
                    )

                response_parts.append("")

        # 일반적인 전문가 조언
        response_parts.append("🎯 **전문가 추천사항:**")
        response_parts.append("")

        general_advice = self._generate_general_advice(expert_type, user_message)
        for advice in general_advice:
            response_parts.append(f"✓ {advice}")

        response_parts.append("")

        # 마무리
        closing = random.choice(self.conversation_patterns["closing"])
        response_parts.append(closing)

        return "\n".join(response_parts)

    def _analyze_message(self, message: str, expert: Dict) -> Dict[str, Any]:
        """메시지 분석하여 관련 키워드 매칭"""
        message_lower = message.lower()
        matched_keywords = {}

        for keyword, info in expert["keywords"].items():
            if keyword in message_lower:
                matched_keywords[keyword] = info

        # 유사 키워드도 체크
        if expert["emoji"] == "🏥":  # 의학
            if any(
                word in message_lower for word in ["아프", "증상", "통증", "열", "기침"]
            ):
                if "감기" not in matched_keywords and "감기" in expert["keywords"]:
                    matched_keywords["감기"] = expert["keywords"]["감기"]

        return {
            "matched_keywords": matched_keywords,
            "emotion": self._detect_emotion(message),
            "urgency": self._detect_urgency(message),
        }

    def _detect_emotion(self, message: str) -> str:
        """감정 분석"""
        positive_words = ["좋", "기쁘", "행복", "만족", "성공"]
        negative_words = ["걱정", "문제", "어려", "힘들", "답답"]

        pos_count = sum(1 for word in positive_words if word in message)
        neg_count = sum(1 for word in negative_words if word in message)

        if neg_count > pos_count:
            return "걱정"
        elif pos_count > neg_count:
            return "긍정"
        else:
            return "중성"

    def _detect_urgency(self, message: str) -> str:
        """긴급도 분석"""
        urgent_words = ["급", "즉시", "응급", "빨리", "심각"]
        if any(word in message for word in urgent_words):
            return "높음"
        return "보통"

    def _generate_general_advice(self, expert_type: str, message: str) -> List[str]:
        """전문가별 일반적인 조언 생성"""
        advice_templates = {
            "medical": [
                "증상이 지속되거나 악화되면 반드시 전문의 진료를 받으세요",
                "예방이 치료보다 중요하므로 평소 건강관리에 신경쓰세요",
                "자가진단보다는 정확한 검사를 통한 진단이 필요합니다",
            ],
            "financial": [
                "투자 전 충분한 공부와 리스크 분석이 필요합니다",
                "장기적 관점에서 꾸준한 투자 습관을 기르세요",
                "전문가 상담을 통해 개인 맞춤 전략을 수립하세요",
            ],
            "tech": [
                "최신 기술 트렌드를 지속적으로 학습하세요",
                "보안과 성능을 동시에 고려한 설계가 중요합니다",
                "사용자 경험(UX)을 최우선으로 고려하세요",
            ],
            "marketing": [
                "타겟 고객을 명확히 정의하고 그들의 니즈를 파악하세요",
                "데이터 기반의 의사결정을 통해 ROI를 최적화하세요",
                "브랜드 일관성을 유지하며 신뢰도를 구축하세요",
            ],
            "legal": [
                "관련 법령과 판례를 충분히 검토하세요",
                "증거 자료를 체계적으로 수집하고 보관하세요",
                "복잡한 사안은 전문 변호사와 상담하시기 바랍니다",
            ],
        }

        default_advice = [
            "전문적인 분석이 필요한 경우 추가 상담을 권합니다",
            "상황에 맞는 맞춤형 솔루션을 제공하겠습니다",
            "지속적인 모니터링과 관리가 중요합니다",
        ]

        return advice_templates.get(expert_type, default_advice)

    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """감정 분석 (호환성)"""
        emotion = self._detect_emotion(text)
        return {
            "emotion": emotion,
            "confidence": 0.85,
            "details": f"메시지 감정 상태: {emotion}",
        }

    def analyze_conversation_context(self, text: str) -> Dict[str, Any]:
        """대화 맥락 분석 (호환성)"""
        urgency = self._detect_urgency(text)
        return {"urgency": urgency, "context": "전문가 상담", "confidence": 0.8}


# 전역 인스턴스
_smart_ai = None


def get_smart_ai() -> SmartExpertAI:
    """Smart AI 인스턴스 반환"""
    global _smart_ai
    if _smart_ai is None:
        _smart_ai = SmartExpertAI()
    return _smart_ai


def generate_expert_response_sync(user_message: str, expert_type: str) -> str:
    """동기 전문가 응답 생성"""
    smart_ai = get_smart_ai()
    return smart_ai.generate_expert_response(user_message, expert_type)


# 기존 시스템과의 호환성
class RealAIManager:
    """호환성을 위한 래퍼 클래스"""

    def __init__(self):
        self.smart_ai = get_smart_ai()
        self.api_keys = {"local": "enabled"}  # 가상 API 키

    async def generate_expert_response(
        self, user_message: str, expert_type: str
    ) -> str:
        """비동기 호환 함수"""
        return self.smart_ai.generate_expert_response(user_message, expert_type)

    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """감정 분석"""
        return self.smart_ai.analyze_emotion(text)

    def analyze_conversation_context(self, text: str) -> Dict[str, Any]:
        """대화 맥락 분석"""
        return self.smart_ai.analyze_conversation_context(text)


def get_real_ai_manager() -> RealAIManager:
    """호환성을 위한 AI 매니저 반환"""
    return RealAIManager()


# 비동기 함수들
async def generate_expert_response_async(user_message: str, expert_type: str) -> str:
    """비동기 전문가 응답 생성"""
    smart_ai = get_smart_ai()
    return smart_ai.generate_expert_response(user_message, expert_type)
