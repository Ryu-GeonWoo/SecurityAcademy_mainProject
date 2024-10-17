from mitmproxy import http
from module import *
import json

FILTER_KEYWORDS = filterd_target_from_file('filter/keyword.txt')


def filtering_prompt(flow: http.HTTPFlow)-> None:
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
            print("------------------------------------------------------------------------")
            print(data)
            flow.response = data_filtering()
            # data에서 입력값 파싱하는 코드 추가

            # 필터링 키워드 확인


            # 필터링에 걸렸을 경우 아래 함수 호출
            # flow.response = data_filtering(data)

        except Exception as e:
            print(f"Error processing request: {e}")

    else: 
        pass
