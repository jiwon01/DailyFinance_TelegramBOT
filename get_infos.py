import json
import http.client
import requests
import os
from bs4 import BeautifulSoup as bs

# ********************
# 정보 가져오는 함수
# ********************
def get_infos(choosed):
    # 링크들 변수
    url_korea = 'https://finance.naver.com/sise/'  # 네이버 금융 한국시장
    url_world = 'https://finance.naver.com/world/'  # 네이버 금융 세계시장
    url_nasdaq = 'https://search.naver.com/search.naver?where=nexearch&query=%EB%82%98%EC%8A%A4%EB%8B%A5&sm=tab_stc'
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
        pages_world = bs(requests.get(url_nasdaq).text, 'html.parser')
        return pages_world.select_one('#_cs_root > div.ar_spot > div > h3 > a > span > strong').get_text()
    
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