# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

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

@app.route("/", methods=["POST"])
def webhook():
    # 어떤 이벤트/메시지든 자동응답 + 상담 자동완료 처리
    return jsonify({
        "event": "send",
        "textContent": {"text": AUTO_REPLY},
        "complete": "true"   # 🔥 상담목록 자동 제거
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
