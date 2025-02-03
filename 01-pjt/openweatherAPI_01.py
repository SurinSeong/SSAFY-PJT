# openWeatherMap API 실습하기
# 특정 지역의 현재 날씨에 대한 기본 정보 출력

import os
import pprint
import requests

from dotenv import load_dotenv

load_dotenv()

def get_seoul_weather():
    API_KEY = os.getenv('WEATHER_APIKEY')
    # 서울의 위도
    lat = 37.56
    # 서울의 경도
    lon = 126.97

    # API 요청 URL
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'

    # API 요청 보내기
    response = requests.get(url).json()
    
    return response


if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_seoul_weather()
    ## pprint.pprint() : json을 보기 좋은 형식으로 출력
    pprint.pprint(result)