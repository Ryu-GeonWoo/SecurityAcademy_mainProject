from mitmproxy import http
import json
from module import *
from filter import *

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