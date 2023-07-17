import json
import http.client
import requests
import os
from bs4 import BeautifulSoup as bs

from get_infos import get_infos

# ********************
# 종합 정보 수집 함수
# ********************
def get_everyinfos():
    print("함수: 종합 정보 수집 또는 자동 처리")
    msg = ''.join(["<strong>일일 시장 상황</strong>\n", "코스피: ", get_infos("ch_kospi"), "\nUSD: ", get_infos("ch_usd"), "\nEUR: ", get_infos("ch_eur"), "\nJPY: ", get_infos("ch_jpy")])
    httppost_infos("sendMessage", msg, "HTML")
    return 1


# ********************
# HTTP POST 함수
# ********************
def httppost_infos(method, msg, parse_mode):
    print("메서드: ", method, "msg: ", msg, "파스모드: ", parse_mode)
    TELEGRAM_API_HOST = "api.telegram.org"
    TOKEN = os.environ['TOKEN']
    connection = http.client.HTTPSConnection(TELEGRAM_API_HOST)
    # 토큰과 메서명 지정
    # sendMessage
    url = f"/bot{TOKEN}/{method}"
    # HTTP 헤더
    headers = {'content-type': "application/json"}
    # 파라미터
    param = {
        'chat_id': '-1001845510920',
        'text': msg,
        'parse_mode': parse_mode,
        'disable_web_page_preview': 'True',
        'disable_notification': 'True',
    }
    # Http 요청
    connection.request("POST", url, json.dumps(param), headers)
    # 응답
    res = connection.getresponse()
    # 연결 끊기
    connection.close()


# ********************
# Lambda Handler
# ********************

def lambda_handler(event, context):
    # TODO implement
    print("event : ", event)
    print("context : ", context)

    # 필요 변수 선언
    value = 0
    commands = {
        "ch_kospi": ("코스피", "kospi", "KOSPI", "테스트"),
        "ch_kosdaq": ("코스닥", "kosdaq", "KOSDAQ"),
        "ch_nasdaq": ("나스닥", "nasdaq"),
        "ch_usd": ("달러", "usd", "USD"),
        "ch_jpy": ("엔화", "jpy", "JPY", "엔"),
        "ch_eur": ("유로", "eur", "EUR"),
        "ch_gold": ("금", "gold", "GOLD"),
        #"ch_help": ("도움말", "help"),
        #"ch_all": ("종합")
    }

    # 루틴대로 돌아가는지 분류함.
    try:
        if event["isroutine"] == True:
            result = get_everyinfos()
            return {
                'statusCode': 200,
                'body': result
            }
    except:
        print("정상 통과 (루틴 아님)")
        teleRes = json.loads(event['body'])
        chats = teleRes["message"]["text"]
        getsenderid = "".join(["@", teleRes["message"]["from"]["username"]])
        print("채팅내용:", chats)

    # 입력한 명령어가 commands에 있는지 확인
    for key, v in commands.items():
        if chats in v:
            choose = v[0]
            value = get_infos(key)
            break

    print("밸류값:", value)
    # 파라미터 (채팅 내용)
    if value == 0:
        print("명령어 타입이 아님.")
    else:
        print("param 정상 처리")
        msg = ''.join([getsenderid, "\n", choose, "의 현재 시세는 <strong>", value, "</strong> 입니다. <a href=\"https://finance.naver.com\"><i>자세히 보기</i></a>"])
        print(msg)
        httppost_infos("sendMessage", msg, "HTML")

    return {
        'statusCode': 200,
        'body': chats
    }