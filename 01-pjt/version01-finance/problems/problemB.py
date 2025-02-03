# 날씨 데이터 중 다음 조건에 해당하는 값만 딕셔너리 형태로 반환

import os
import requests
import pprint

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


json_response = get_seoul_weather()

new_dict = dict()
new_dict['main'] = json_response['main']
new_dict['weather_data'] = json_response['weather']

pprint.pprint(new_dict)