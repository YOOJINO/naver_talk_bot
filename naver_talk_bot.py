# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

# 자동응답 문구
REPLY_AUTO = """
📦 『배송/조회/문의 안내』

아래 메뉴에서 원하시는 항목을 선택해주세요 😊
"""

# 개별 안내 텍스트
REPLY_INFO = {
    "배송안내": "📌 배송안내\n해당 상품은 해외직구 상품이며 배송은 영업일 기준 약 10~14일 소요됩니다.",
    "배송조회": "🔍 배송조회\nhttps://unipass.customs.go.kr → 화물진행정보 조회 후 송장 입력",
    "상담원 연결하기": "상담원 연결 요청이 접수되었습니다. 잠시만 기다려주세요! 😊"
}

# 메뉴 버튼 UI
MENU_MSG = {
    "event": "send",
    "textContent": {"text": REPLY_AUTO},
    "compositeContent": {
        "compositeList": [
            {
                "title": "📦 배송 안내",
                "description": "배송 기간 안내",
                "buttons": [{"text": "배송안내"}]
            },
            {
                "title": "🔍 배송조회",
                "description": "세관/국내 조회 안내",
                "buttons": [{"text": "배송조회"}]
            },
            {
                "title": "💬 상담원 연결",
                "description": "상담원이 도와드립니다",
                "buttons": [{"text": "상담원 연결하기"}]
            }
        ]
    }
}

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    event = data.get("event")
    text = data.get("textContent", {}).get("text", "")

    # 고객이 채팅방 열었을 때 → 메뉴만 보여줌 (상담목록에 등록 ❌)
    if event == "open":
        return jsonify(MENU_MSG)

    # 메뉴 선택 시 안내 메시지 응답 (자동응답 → 상담목록 등록 ❌)
    if text in REPLY_INFO and text != "상담원 연결하기":
        return jsonify({
            "event": "send",
            "textContent": {"text": REPLY_INFO[text]}
        })

    # 상담원 연결하기 선택 시 → 상담목록에 올라감 (🔵 상담원이 해야 할 일)
    if text == "상담원 연결하기":
        return jsonify({
            "event": "send",
            "textContent": {"text": REPLY_INFO[text]}
        })

    # 기타 입력 → 메뉴 다시 보여줌 (상담목록 등록 ❌ + 자동읽음 효과)
    return jsonify(MENU_MSG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
