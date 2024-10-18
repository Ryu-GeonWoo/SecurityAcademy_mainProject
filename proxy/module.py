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

def response_make(code=399, message="Filltering your prompt", header={"Content-Type": "text/event-stream"}) -> http.Response:
    """
    500 Internal Server Error 응답을 생성하는 코드
    
    :param: code=500, message="Internal Server Error", header={"Content-Type": "text/event-stream"} 
    :return: http.Response
    """
    # 에러 이벤트 데이터 생성
    error_data = {
        "status_code": code,
        "message": message
    }

    # event-stream 형식으로 데이터 반환
    event_stream_data = f'event: error\ndata: {json.dumps(error_data)}\n\n'

    return http.Response.make(
        code,
        event_stream_data.encode(),
        header
    )


# 연결 안되어 있을경우 반환하는 오류 패킷을 활용하여 금지된 prompt라는 오류가 발생되도록 활용 예정
def block_prompt(flow: http.HTTPFlow) -> http.Response:
    """
    요청 데이터에서 필터링 키워드가 있는지 확인하고,
    키워드가 발견되면 차단된 메시지로 응답을 수정합니다.

    :param data: 요청 데이터 (JSON 형식)
    :return: http.Response
    """
    return response_make()

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
