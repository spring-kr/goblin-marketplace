"""
📱 도깨비마을장터 Vercel 최적화 v11.7
=====================================

Vercel 서버리스 환경에 최적화된 경량 버전
- 메모리 사용량 최소화
- 초기화 시간 단축
- 응답 데이터 압축
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "goblin_market_vercel_v11"

# 간소화된 도깨비 데이터
GOBLIN_DATA = {
    "counselor": {"name": "심리상담도깨비", "specialty": "심리상담", "personality": "친근한"},
    "marketing": {"name": "마케팅도깨비", "specialty": "마케팅전략", "personality": "창의적인"},
    "finance": {"name": "재테크도깨비", "specialty": "금융투자", "personality": "꼼꼼한"},
    "health": {"name": "건강관리도깨비", "specialty": "건강관리", "personality": "차분한"},
    "education": {"name": "교육도깨비", "specialty": "교육컨설팅", "personality": "전문적인"},
    "ai_expert": {"name": "인공지능박사도깨비", "specialty": "AI연구", "personality": "열정적인"},
    "economics_expert": {"name": "경제학박사도깨비", "specialty": "경제분석", "personality": "꼼꼼한"},
    "art_expert": {"name": "예술학박사도깨비", "specialty": "예술창작", "personality": "창의적인"},
    "data_expert": {"name": "데이터과학박사도깨비", "specialty": "데이터분석", "personality": "전문적인"},
    "hr_expert": {"name": "인사관리박사도깨비", "specialty": "인사관리", "personality": "친근한"},
}

@app.route("/")
def mobile_index():
    """모바일 메인 페이지"""
    return render_template("goblin_mobile_simple.html")

@app.route("/api/goblins")
def get_goblins():
    """도깨비 목록 API"""
    return jsonify({"success": True, "goblins": GOBLIN_DATA})

@app.route("/api/chat", methods=["POST"])
def chat_with_goblin():
    """간소화된 채팅 API"""
    try:
        data = request.get_json()
        goblin_id = data.get("goblin_id", "counselor")
        message = data.get("message", "")
        
        if goblin_id not in GOBLIN_DATA:
            return jsonify({"error": "도깨비를 찾을 수 없습니다."}), 400
        
        goblin = GOBLIN_DATA[goblin_id]
        
        # 간단한 응답 생성
        response = f"안녕하세요! {goblin['name']}입니다. {goblin['specialty']} 분야에서 '{message}'에 대해 도움드리겠습니다. 현재 Vercel 배포 테스트 중입니다!"
        
        return jsonify({
            "success": True,
            "response": response,
            "goblin_info": goblin,
            "timestamp": int(time.time())
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/manifest.json")
def manifest():
    """PWA 매니페스트"""
    manifest_data = {
        "name": "도깨비마을장터",
        "short_name": "도깨비장터",
        "description": "39명 전문가 도깨비와 채팅하세요",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4CAF50",
        "icons": [
            {
                "src": "/static/icon-192.svg",
                "sizes": "192x192",
                "type": "image/svg+xml"
            }
        ]
    }
    return jsonify(manifest_data)

@app.route("/sw.js")
def service_worker():
    """서비스 워커"""
    sw_code = """
const CACHE_NAME = 'goblin-marketplace-v1';
const urlsToCache = [
  '/',
  '/static/icon-192.svg',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
"""
    response = app.response_class(
        response=sw_code,
        status=200,
        mimetype='application/javascript'
    )
    return response

@app.route("/health")
def health_check():
    """헬스 체크"""
    return jsonify({"status": "ok", "version": "v11.7", "goblins": len(GOBLIN_DATA)})

# Vercel용 앱 객체 export
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
