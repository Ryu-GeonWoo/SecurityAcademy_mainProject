from mitmproxy import http
import json
from filter import *

from module import *

# mitmdump --ssl -s main.py --mode regular@8082

# 필터링할 키워드 목록
FILTER_URL = "geonwoo-ryu.iptime.org:9999/"

# request 
def request(flow: http.HTTPFlow) -> None:
    
    # URL FILTER
    # 허용되지 않은 url 접속 시 차단
    if FILTER_URL not in flow.request.pretty_url:
        flow.response = response_make()
    
    # ChatGPT와 관련된 요청을 필터링하기 위해 URL 확인 (예시 URL, 실제로는 OpenAI의 API URL 사용)
    if "chatgpt.com" in flow.request.pretty_url:
        filter_gpt_prompt(flow)


