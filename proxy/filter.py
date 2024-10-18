from mitmproxy import http
from module import *
import json


def filtering_prompt(flow: http.HTTPFlow, FILTER_KEYWORDS)-> None:
    """
    gpt에게 하는 질문을 필터링 하는 함수
    필터링 되는 단어가 포함되어 있을 경우 '차단된 프롬프트입니다' 메시지 생성

    :param: flow, keyword_list
    :return: None
    """
    # 요청 본문 확인 프롬프트 데이터가 들어있는 JSON checking
    if flow.request.headers.get("Content-Type") == "application/json":
        try:
            data = flow.request.json()

            # prompt filtering
            if checking_human_message(data, FILTER_KEYWORDS):
                print("-----------"*3)
                print(data)
                flow.response = block_prompt(flow)

            # no problem
            else:
                pass

        except Exception as e:
            print(f"Error processing request: {e}")

    else: 
        pass
