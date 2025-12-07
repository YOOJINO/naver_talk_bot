# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import threading
import time
import requests

app = Flask(__name__)

AUTO_REPLY = """
1. 『배송안내』

해당 상품은 해외직구 상품이며, 배송일은 영업일 기준 10~14일 정도 소요됩니다.

ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ

2. 『배송조회』

- 세관 통관중
목록통관접수일 기준 영업일 4~5일 이내 배송완료 됩니다.

📌 조회 방법
1) https://unipass.customs.go.kr
2) [화물진행정보] → M B/L 또는 H B/L 선택
3) 운송장번호 입력 → 검색

- 세관 통관 후
📦 CJ대한통운 조회 : https://www.cjlogistics.com/

ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ

3. 『상품문의』

📱 연락처 : 010-5196-6466

👇 문자 발송 시 아래 내용 남겨주세요
1) 상품 링크
2) 문의 내용
3) 구매 수량

ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ

그 외 배송/반품/교환/기타 문의는
📞 고객센터 : 010-5196-6466 으로 연락 주시면 감사하겠습니다.

오늘도 행복한 하루 보내세요 😊
감사합니다.
"""


# 📌 5초 후 상담완료 처리
def complete_after_5s(callback_url):
    time.sleep(5)
    requests.post(callback_url, json={
        "event": "send",
        "textContent": {"text": ""},
        "complete": "true"
    })


# 📌 "완료", "상담끝", "고마워" 입력 시 상담종료
COMPLETE_KEYWORDS = ["완료", "상담끝", "끝", "고마워", "감사", "bye"]


def send_complete(callback_url):
    requests.post(callback_url, json={
        "event": "send",
        "textContent": {"text": ""},
        "complete": "true"
    })


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    callback_url = data.get("callbackUrl")
    text = data.get("textContent", {}).get("text", "").strip()

    # 📌 고객이 직접 완료 키워드 입력 시 종료
    if text and callback_url and any(k in text for k in COMPLETE_KEYWORDS):
        threading.Thread(target=send_complete, args=(callback_url,)).start()
        return jsonify({"event": "send", "textContent": {"text": "상담 도와드려 감사했습니다 😊"}})

    # 📌 기본 안내 메시지 응답
    reply = {
        "event": "send",
        "textContent": {"text": AUTO_REPLY}
    }

    # 📌 5초 뒤 자동 완료
    if callback_url:
        threading.Thread(target=complete_after_5s, args=(callback_url,)).start()

    return jsonify(reply)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
