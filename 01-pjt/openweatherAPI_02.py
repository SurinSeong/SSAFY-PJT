# 특정 도시의 현재 날씨를 도시 이름으로 요청하여 모든 정보 출력
import os
import requests
import pprint
from dotenv import load_dotenv

load_dotenv()

def get_seoul_weather():
    # API KEY
    API_KEY = os.getenv('WEATHER_APIKEY')

    # 검색 조건
    city = 'Seoul,KR' # 다른 지역 : 'Tokyo,JP', 'New York,US'

    # API 요청 URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'

    # API 요청 보내기
    response = requests.get(url).json()

    return response


if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_seoul_weather()
    
    pprint.pprint(result)