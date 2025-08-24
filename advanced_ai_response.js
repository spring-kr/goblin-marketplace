        // 고급 AI 시뮬레이션 함수들
        function simulateAdvancedResponse(message, goblinId) {
            // 고급 AI 분석 함수들
            const analyzeMessage = (msg) => {
                const emotions = {
                    curious: ['뭐예요', '머예요', '란?', '이란?', '뭔지', '알려주세요', '궁금', '?'],
                    excited: ['!', '와', '대박', '신기', '재미', '좋다', '멋지'],
                    confused: ['모르겠', '헷갈', '어려워', '복잡', '이해 안'],
                    urgent: ['빨리', '급하', '지금', '당장', '도와주세요'],
                    polite: ['부탁', '감사', '죄송', '실례', '정중']
                };
                
                let detectedEmotion = 'neutral';
                for (const [emotion, keywords] of Object.entries(emotions)) {
                    if (keywords.some(keyword => msg.includes(keyword))) {
                        detectedEmotion = emotion;
                        break;
                    }
                }
                
                const complexity = msg.length > 10 ? 'complex' : 'simple';
                const questionType = msg.includes('?') || msg.includes('란') || msg.includes('뭐') ? 'question' : 'statement';
                
                return { emotion: detectedEmotion, complexity, questionType };
            };

            const generateDetailedResponse = (msg, analysis, goblinId) => {
                // 도깨비별 전문 지식 기반 상세 응답
                const expertResponses = {
                    1: { // AI전문가
                        intro: "🤖 AI 전문가로서 분석해드리겠습니다.",
                        knowledge: {
                            "인공지능": `인공지능(Artificial Intelligence)은 인간의 지능을 기계로 구현하는 기술입니다.

📍 **핵심 구성요소:**
• 머신러닝(Machine Learning): 데이터로부터 패턴을 학습
• 딥러닝(Deep Learning): 신경망을 통한 복잡한 학습
• 자연어처리(NLP): 인간의 언어를 이해하고 생성
• 컴퓨터 비전: 이미지와 영상을 인식하고 분석

🔬 **현재 활용 분야:**
• 의료진단, 자율주행, 추천시스템, 번역서비스
• 음성인식, 이미지생성, 게임AI, 로봇공학

💡 **미래 전망:**
AGI(일반인공지능) 개발을 통해 인간과 같은 범용적 사고능력을 갖춘 AI가 등장할 것으로 예상됩니다.`,
                            "머신러닝": `머신러닝은 데이터를 통해 컴퓨터가 스스로 학습하는 AI의 핵심 기술입니다.

🎯 **학습 방식:**
• 지도학습: 정답이 있는 데이터로 학습
• 비지도학습: 패턴 발견을 통한 자율학습
• 강화학습: 시행착오를 통한 최적화 학습

⚙️ **주요 알고리즘:**
• 선형회귀, 의사결정트리, 랜덤포레스트
• SVM, 클러스터링, 신경망

📊 **활용 예시:**
스팸메일 필터링, 주식 예측, 고객 세분화, 추천시스템 등`
                        }
                    },
                    2: { // 데이터과학박사
                        intro: "📊 데이터 과학 관점에서 심층 분석해드리겠습니다.",
                        knowledge: {
                            "데이터": `데이터는 현대 디지털 사회의 가장 중요한 자원입니다.

📈 **데이터 유형:**
• 정형데이터: 표 형태의 구조화된 데이터
• 반정형데이터: XML, JSON 같은 반구조화 데이터  
• 비정형데이터: 텍스트, 이미지, 영상 등

🔍 **분석 프로세스:**
1. 수집(Collection) → 2. 정제(Cleaning) → 3. 탐색(EDA) 
4. 모델링(Modeling) → 5. 검증(Validation) → 6. 배포(Deploy)

💹 **비즈니스 가치:**
데이터 기반 의사결정으로 매출 15-20% 증가, 비용 10-15% 절감 효과가 입증되었습니다.`
                        }
                    }
                };

                const expert = expertResponses[goblinId];
                if (!expert) {
                    return `전문가로서 "${msg}"에 대해 자세히 설명드리겠습니다. 이는 매우 흥미로운 주제이며, 실무 경험을 바탕으로 단계별로 접근해보겠습니다.`;
                }

                // 키워드 매칭으로 전문 지식 찾기
                for (const [keyword, content] of Object.entries(expert.knowledge)) {
                    if (msg.includes(keyword)) {
                        return `${expert.intro}

${content}

💬 더 궁금한 점이 있으시면 언제든 말씀해주세요!`;
                    }
                }

                return `${expert.intro}

"${msg}"에 대해 더 구체적으로 질문해주시면 전문 지식을 바탕으로 상세히 설명드리겠습니다.`;
            };

            // 메시지 분석
            const analysis = analyzeMessage(message);
            console.log('📊 메시지 분석 결과:', analysis);

            // 감정에 따른 응답 조정
            let responsePrefix = '';
            switch(analysis.emotion) {
                case 'curious':
                    responsePrefix = '🤔 궁금증이 느껴지는 질문이네요! ';
                    break;
                case 'excited':
                    responsePrefix = '🎉 열정적인 에너지가 전해집니다! ';
                    break;
                case 'confused':
                    responsePrefix = '😊 복잡해 보이지만 차근차근 설명해드릴게요! ';
                    break;
                case 'urgent':
                    responsePrefix = '⚡ 급하신 것 같으니 핵심부터 말씀드리겠습니다! ';
                    break;
            }

            // 상세한 응답 생성
            const detailedResponse = generateDetailedResponse(message, analysis, goblinId);
            const finalResponse = responsePrefix + detailedResponse;

            handleChatResponse({
                success: true,
                result: {
                    response: finalResponse,
                    conversation_id: 'sim_' + Date.now(),
                    goblin_id: goblinId,
                    timestamp: new Date().toISOString(),
                    analysis: analysis
                }
            });
        }
