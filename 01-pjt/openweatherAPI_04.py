# 서울의 현재 날씨에 대한 설명 데이터만 출력
import os
import requests
import pprint
from dotenv import load_dotenv

load_dotenv()


def get_seoul_weather():
    # API KEY
    API_KEY = os.getenv('WEATHER_APIKEY')
    
    # 검색 조건
    city = 'Seoul,KR'
    
    # API 요청 URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    
    # API 요청 보내기
    json_response = requests.get(url).json()
    description = json_response['weather'][0]['description']
    
    return f'날씨 설명: {description}'


if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_seoul_weather()
    
    pprint.pprint(result)