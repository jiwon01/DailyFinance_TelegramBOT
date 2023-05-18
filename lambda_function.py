import json
import http.client
import requests
import os
from bs4 import BeautifulSoup as bs


def lambda_handler(event, context):
    # TODO implement
    print("event : ", event)
    print("context : ", context)

    # 변수 선언
    value = 0

    # 분류하는 곳
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

    # kospi, kosdaq, nasdaq, usd, jpy, eur if는 배열로도 구현가능할듯
    if chats == "코스피" or chats == "kospi" or chats == '테스트':
        print("코스피 들어옴")
        choose = "코스피"
        value = get_infos("ch_kospi")
    elif chats == "코스닥" or chats == "kosdaq":
        print("코스닥 들어옴")
        choose = "코스닥"
        value = get_infos("ch_kosdaq")
    elif chats == "나스닥" or chats == "nasdaq":
        print("나스닥 들어옴")
        choose = "나스닥"
        value = get_infos("ch_nasdaq")
    elif chats == "달러" or chats == "usd":
        print("달러 들어옴")
        choose = "달러<i>(USD)</i>"
        value = get_infos("ch_usd")
    elif chats == "엔화" or chats == "jpy":
        print("엔화 들어옴")
        choose = "엔화<i>(JPY)</i>"
        value = get_infos("ch_jpy")
    elif chats == "유로" or chats == "eur":
        print("유로 들어옴")
        choose = "유로<i>(EUR)</i>"
        value = get_infos("ch_eur")
    elif chats == "금" or chats == "gold":
        print("금 입력됨")
        choose = "국내 금<i>(Gold)</i>"
        value = get_infos("ch_gold")
    elif chats == "종합":
        result = get_everyinfos()
        return {
            'statusCode': 200,
            'body': result
        }
    elif chats == "도움말" or chats == "help" or chats == "/help":
        value = "None"
    else:
        print("오류임")
        value = 0

    print("밸류값:", value)
    # 파라미터 (채팅 내용)
    if value == 0:
        print("명령어 타입이 아님.")
        # msg = '<strong>잘못된 명령어</strong>입니다.\n\n<strong>지원되는 명령어:</strong>\n<i>코스피, 코스닥, 나스닥, 달러, 엔화, 유로</i>'
        # httppost_infos("sendMessage", msg, "HTML")
    else:
        print("param 정상 처리")
        msg = ''.join([getsenderid, "\n", choose, "의 현재 시세는 <strong>", value, "원</strong> 입니다. <a href=\"https://finance.naver.com\"><i>자세히 보기</i></a>\n전달 대비 등략율: XX (XX%)"])
        # msg = "앙기모링"
        print(msg)
        httppost_infos("sendMessage", msg, "HTML")

    return {
        'statusCode': 200,
        'body': chats
    }


# ********************
# 정보 가져오는 함수
# ********************
def get_infos(choosed):
    # 링크들 변수
    url_korea = 'https://finance.naver.com/sise/'  # 네이버 금융 한국시장
    url_world = 'https://finance.daum.net/global'  # 네이버 금융 세계시장 (추후에 바꿔야할듯)
    url_marketindex = 'https://finance.naver.com/marketindex/'  # 네이버 금융 시장지표

    # (네이버 금융 파싱)
    if choosed == "ch_kospi" or choosed == "ch_kosdaq":
        pages_kr = bs(requests.get(url_korea).text, 'html.parser')
        if choosed == "ch_kospi":  # 코스피
            return pages_kr.select_one('#KOSPI_now').get_text()
        elif choosed == "ch_kosdaq":  # 코스닥
            return pages_kr.select_one('#KOSDAQ_now').get_text()
        else:
            return 0
    elif choosed == "ch_nasdaq":
        pages_world = bs(requests.get(url_world).text, 'html.parser')
        if choosed == "ch_nasdaq":  # 나스닥
            return pages_world.select_one('#boxDashboard > div.box_contents > div.map.nAmerica > span.box > table > tbody > tr:nth-child(2) > td:nth-child(2)').get_text()
        else:
            return 0
    elif choosed == "ch_usd" or choosed == "ch_jpy" or choosed == "ch_eur" or choosed == "ch_gold":
        pages_marketindex = bs(requests.get(url_marketindex).text, 'html.parser')
        if choosed == "ch_usd":  # 미국 달러
            return pages_marketindex.select_one('#exchangeList > li.on > a.head.usd > div > span.value').get_text()
        elif choosed == "ch_jpy":  # 엔화
            return pages_marketindex.select_one(
                '#exchangeList > li:nth-child(2) > a.head.jpy > div > span.value').get_text()
        elif choosed == "ch_eur":  # 유로
            return pages_marketindex.select_one(
                '#exchangeList > li:nth-child(3) > a.head.eur > div > span.value').get_text()
        elif choosed == "ch_gold":  # 국내 금
            return pages_marketindex.select_one(
                '#oilGoldList > li:nth-child(4) > a.head.gold_domestic > div > span.value').get_text()

    # 에러 발생시 0 리턴
    else:
        print("error occured")
        return 0

    # value 값 리턴
    return 0


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
