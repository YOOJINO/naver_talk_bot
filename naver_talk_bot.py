# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

# 고정 자동응답 문구 (원하는 문장만 넣기)
FIXED_REPLY = "문의 감사합니다. 담당자가 확인 후 순차적으로 답변드리겠습니다."


@app.route("/", methods=["POST"])
def naver_talktalk_webhook():
    """
    네이버 톡톡 자동응답 서버
    - 어떤 메시지가 와도 무조건 같은 답변만 보냄
    """
    response = {
        "event": "send",
        "textContent": {
            "text": FIXED_REPLY
        }
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
