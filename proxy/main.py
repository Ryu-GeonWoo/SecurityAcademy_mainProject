from mitmproxy import http
import json
from filter import *

from module import *

# mitmdump --ssl -s main.py --mode regular@8082

# 필터링할 키워드 목록
FILTER_URL = "geonwoo-ryu.iptime.org:9999/"
FILTER_KEYWORDS = filterd_target_from_file('filter/keyword.txt')

# request 
def request(flow: http.HTTPFlow) -> None:
    
    # URL ai 관련 패킷일 경우
    if FILTER_URL in flow.request.pretty_url:
        filtering_prompt(flow, FILTER_KEYWORDS)
    else:
        pass
    
    # chat prompt filtering
    

