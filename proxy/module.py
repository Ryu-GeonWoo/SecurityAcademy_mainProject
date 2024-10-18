from mitmproxy import http
import json
from module import *
from filter import *
from datetime import datetime

def filterd_target_from_file(file_path: str) -> list:
    """
    필터링할 단어 및 url txt 파일을 리스트로 불러오기

    :param: file_path
    :return: list
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 각 줄에서 URL을 읽어와 리스트로 반환
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

def find_value(json_data, target_key):
    """
    재귀적으로 json 데이터에서 target의 존재 여부 검사
    
    :param: json_data, target dictionary
    :return: target json dictionary
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                return value
            if isinstance(value, (dict, list)):
                result = find_value(value, target_key)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_value(item, target_key)
            if result is not None:
                return result
    return None

def response_make(code=404, message="Filtered page", data={"Content-Type": "text/html"}) -> http.Response:
    """
    반환할 응답을 생성하는 코드
    
    :param: code=404, message="Filtered page", data={"Content-Type": "text/html"} 
    :return: http.response
    """
    return http.Response.make(
        code,
        message.encode(),
        data
    )

# 연결 안되어 있을경우 반환하는 오류 패킷을 활용하여 금지된 prompt라는 오류가 발생되도록 활용 예정
def block_prompt(flow: http.HTTPFlow) -> http.Response:
    """
    요청 데이터에서 필터링 키워드가 있는지 확인하고,
    키워드가 발견되면 차단된 메시지로 응답을 수정합니다.

    :param data: 요청 데이터 (JSON 형식)
    :return: http.Response
    """
    # current_time = datetime.utcnow().isoformat() + "Z"  # ISO 8601 형식으로 현재 시간
    
    # # 차단된 프롬프트 메시지 생성
    # response_data = {
    #     "ops": [
    #         {
    #             "op": "add",
    #             "path": "/logs/StrOutputParser/final_output",
    #             "value": {"output": "사용할 수 없는 키워드입니다."}
    #         },
    #         {
    #             "op": "add",
    #             "path": "/logs/StrOutputParser/end_time",
    #             "value": current_time  # 현재 시간을 동적으로 추가
    #         }
    #     ]
    # }
    
    # # 응답 수정
    # return http.Response.make(
    #     200,  # HTTP 상태 코드
    #     json.dumps(response_data).encode(),  # JSON 데이터
    #     {"Content-Type": "text/event-stream"}  # 헤더
    # )

    return None

def checking_human_message(data, FILTER_KEYWORDS):
    """
    요청 데이터에서 사용자의 요청 메시지에서 필터링 키워드가 있는지 확인하고,
    키워드가 발견되면 차단된 메시지로 응답을 수정합니다.

    :param data: 요청 데이터 (JSON 형식)
    :return: http.Response
    """
    try:
        # JSON 문자열을 파이썬 객체로 변환
        message_data = data['input']['messages1']
        for message in message_data:
            content = message['content']
            if message['type'] == "human":
                if keyword_checking(content, FILTER_KEYWORDS):
                    print("filtered")
                    return True
                    
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return False

def keyword_checking(checking_content, FILTER_KEYWORDS):
    """
    content에 filtering 해야하는 키워드가 있는지 확인합니다.

    :param data: content, keyword_list
    :return: boolean
    """
    for i in FILTER_KEYWORDS:
        if i in checking_content:
            return True
    else:
        return False
