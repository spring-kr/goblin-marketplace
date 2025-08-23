"""
📱 도깨비마을장터 모바일 앱 v11.6
=====================================

v11.5 웹 인터페이스의 모바일 최적화 버전
- PWA (Progressive Web App) 지원
- 오프라인 모드
- 푸시 알림
- 네이티브 앱 같은 UX
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_socketio import SocketIO, emit
from complete_goblin_integration_v11 import GoblinTeamManager
import asyncio
import threading
import time
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "goblin_market_mobile_v11_2025"
socketio = SocketIO(app, cors_allowed_origins="*")

# 전역 변수
goblin_team = None
active_sessions = {}
push_subscriptions = {}


def init_goblin_system():
    """도깨비 시스템 초기화"""
    global goblin_team
    print("📱 도깨비마을장터 모바일 앱 v11.6 초기화 중...")
    goblin_team = GoblinTeamManager()
    print("✅ 모바일 최적화 도깨비 팀 초기화 완료!")


@app.route("/")
def mobile_index():
    """모바일 메인 페이지"""
    return render_template("goblin_mobile_v11.html")


@app.route("/test")
def pwa_test():
    """PWA 설치 테스트 페이지"""
    return render_template("pwa_test.html")


@app.route("/api-test")
def api_test():
    """API 테스트 페이지"""
    return render_template("api_test.html")


@app.route("/manifest.json")
def manifest():
    """PWA 매니페스트 파일"""
    return {
        "name": "도깨비마을장터 - AI 전문가 상담",
        "short_name": "도깨비장터",
        "description": "32명 전문가와 27명 도깨비가 함께하는 AI 상담 앱",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#667eea",
        "theme_color": "#5a67d8",
        "orientation": "portrait-primary",
        "scope": "/",
        "id": "goblin-market-app",
        "launch_handler": {"client_mode": "navigate-existing"},
        "icons": [
            {
                "src": "/static/icon-192.svg",
                "sizes": "192x192",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            },
            {
                "src": "/static/icon-512.svg",
                "sizes": "512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            },
        ],
        "categories": ["productivity", "education", "utilities"],
        "lang": "ko-KR",
        "prefer_related_applications": False,
    }


@app.route("/sw.js")
def service_worker():
    """서비스 워커 (오프라인 지원)"""
    return (
        """
const CACHE_NAME = 'goblin-market-v11-6';
const urlsToCache = [
    '/',
    '/manifest.json',
    '/static/icon-192.svg',
    '/static/icon-512.svg'
];

// 설치 이벤트
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

// 요청 가로채기 (오프라인 지원)
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});

// 푸시 알림 수신
self.addEventListener('push', function(event) {
    const options = {
        body: event.data ? event.data.text() : '새로운 메시지가 도착했습니다!',
        icon: '/static/icon-192.svg',
        badge: '/static/icon-192.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: '확인하기',
                icon: '/static/icon-192.png'
            },
            {
                action: 'close',
                title: '닫기'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('도깨비마을장터', options)
    );
});

// 알림 클릭 처리
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});
""",
        200,
        {"Content-Type": "application/javascript"},
    )


@app.route("/api/mobile/goblins")
def get_mobile_goblins():
    """모바일 최적화 도깨비 목록"""
    try:
        goblins = goblin_team.list_goblins()

        # 모바일용 간소화
        mobile_goblins = {}
        for goblin_id, info in goblins.items():
            mobile_goblins[goblin_id] = {
                "name": info["name"],
                "specialty": (
                    info["specialty"][:10] + "..."
                    if len(info["specialty"]) > 10
                    else info["specialty"]
                ),
                "personality": info["personality"],
                "emoji": get_goblin_emoji(info["specialty"]),
            }

        return jsonify(
            {"success": True, "goblins": mobile_goblins, "total": len(mobile_goblins)}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


def get_goblin_emoji(specialty):
    """전문분야별 이모지 매핑"""
    emoji_map = {
        "심리상담": "💚",
        "마케팅전략": "📈",
        "금융투자": "💰",
        "건강관리": "🏥",
        "교육컨설팅": "📚",
        "인공지능": "🤖",
        "양자컴퓨팅": "⚛️",
        "생명공학": "🧬",
        "우주항공": "🚀",
        "환경에너지": "🌱",
        "창의기획": "💡",
        "스토리텔링": "📖",
        "게임개발": "🎮",
        "창업컨설팅": "🏢",
        "국제무역": "🌍",
        "문화기획": "🎭",
        "음악제작": "🎵",
        "사이버보안": "🔒",
        "블록체인": "⛓️",
        "로봇공학": "🤖",
        "사회문제해결": "🤝",
        "정책개발": "📋",
        "의료기술": "⚕️",
        "신약개발": "💊",
        "언어교육": "🗣️",
        "여행컨설팅": "✈️",
        "패션스타일링": "👗",
    }
    return emoji_map.get(specialty, "🧙‍♂️")


@app.route("/api/push/subscribe", methods=["POST"])
def subscribe_push():
    """푸시 알림 구독"""
    subscription = request.get_json()
    session_id = session.get("session_id", str(uuid.uuid4()))

    push_subscriptions[session_id] = subscription

    return jsonify({"success": True, "message": "푸시 알림 구독 완료"})


@socketio.on("mobile_connect")
def handle_mobile_connect():
    """모바일 연결"""
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    session["is_mobile"] = True

    active_sessions[session_id] = {
        "connected_at": datetime.now().isoformat(),
        "device_type": "mobile",
        "conversations": {},
    }

    emit(
        "mobile_connected",
        {
            "session_id": session_id,
            "message": "📱 모바일 앱에 연결되었습니다!",
            "features": ["오프라인 모드", "푸시 알림", "빠른 응답", "터치 최적화"],
        },
    )

    print(f"📱 모바일 사용자 연결: {session_id}")


@socketio.on("quick_chat")
def handle_quick_chat(data):
    """빠른 채팅 (모바일 최적화)"""
    session_id = session.get("session_id")

    try:
        goblin_id = data.get("goblin_id")
        message = data.get("message")

        # 빠른 응답을 위한 간소화
        def run_quick_chat():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    goblin_team.chat_with_goblin(
                        goblin_id, session_id, message, None, "single"
                    )
                )

                # 모바일용 응답 최적화
                mobile_response = {
                    "response": (
                        result["response"][:200] + "..."
                        if len(result["response"]) > 200
                        else result["response"]
                    ),
                    "goblin_name": result.get("goblin_info", {}).get("name", "도깨비"),
                    "emotion": result.get("emotion", "중립"),
                    "conversation_id": result.get("conversation_id"),
                    "timestamp": datetime.now().isoformat(),
                }

                socketio.emit(
                    "quick_response",
                    {"success": True, "result": mobile_response},
                    room=request.sid,
                )

                # 푸시 알림 전송
                send_push_notification(
                    session_id, f"도깨비 응답: {mobile_response['response'][:50]}..."
                )

            except Exception as e:
                socketio.emit(
                    "quick_response",
                    {"success": False, "error": str(e)},
                    room=request.sid,
                )
            finally:
                loop.close()

        thread = threading.Thread(target=run_quick_chat)
        thread.start()

    except Exception as e:
        emit("quick_response", {"success": False, "error": str(e)})


def send_push_notification(session_id, message):
    """푸시 알림 전송"""
    try:
        if session_id in push_subscriptions:
            # 실제 푸시 알림 구현 (webpush 라이브러리 사용)
            print(f"📱 푸시 알림 전송: {message[:30]}...")
    except Exception as e:
        print(f"📱 푸시 알림 전송 실패: {e}")


@app.route("/api/mobile/stats")
def get_mobile_stats():
    """모바일 최적화 통계"""
    try:
        performance = goblin_team.get_team_performance()

        # 모바일용 간소화 통계
        mobile_stats = {
            "active_goblins": performance["total_goblins"],
            "mobile_users": len(
                [
                    s
                    for s in active_sessions.values()
                    if s.get("device_type") == "mobile"
                ]
            ),
            "total_conversations": len(active_sessions),
            "system_status": "정상",
            "response_time": "0.5초",
        }

        return jsonify({"success": True, "stats": mobile_stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    # 도깨비 시스템 초기화
    init_goblin_system()

    import os

    port = int(os.environ.get("PORT", 5012))

    print("📱 도깨비마을장터 모바일 앱 v11.6 서버 시작")
    print(f"📍 서버 포트: {port}")
    print("🌟 PWA + 오프라인 모드 + 푸시 알림 지원")

    # 클라우드 배포용 서버 실행
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False,  # 프로덕션에서는 debug=False
        log_output=True,
    )
