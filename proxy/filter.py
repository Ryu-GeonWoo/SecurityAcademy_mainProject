from mitmproxy import http
import json
from module import *

FILTER_KEYWORDS = filterd_target_from_file('filter/keyword.txt')


def filter_gpt_prompt(flow: http.HTTPFlow)-> None:
    """
    gpt에게 하는 질문을 필터링 하는 함수
    필터링 되는 단어가 포함되어 있을 경우 '차단된 프롬프트입니다' 메시지 생성

    :param: flow 
    :return: None
    """
    # 요청 본문 확인 (프롬프트 데이터가 들어있는 JSON)
    if flow.request.headers.get("Content-Type") == "application/json":
        try:
            data = flow.request.json()

            # 프롬프트 필드에 특정 키워드가 포함되어 있는지 확인              
            content = find_value(data, "parts")
            if any(keyword in content for keyword in FILTER_KEYWORDS):
                # 프롬프트를 필터링할 경우, 사용자에게 경고 메시지 반환
                flow.response = response_make(404,json.dumps({"error": "차단된 프롬프트입니다. 요청이 거부되었습니다."}), {"Content-Type": "application/json"} )
        except Exception as e:
            print(f"Error processing request: {e}")
