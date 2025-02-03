# 서울의 현재 날씨 중 온도만 출력
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
    
    # 키 값 출력
    print(json_response.keys())
    
    # 캘빈 온도 출력
    temperature = json_response['main']['temp']
    print(f'캘빈 온도: {temperature}K')
    
    # 섭씨 온도는 (캘빈 - 273.15)
    temperature_celsius = temperature - 273.15
    print(f'섭씨 온도: {temperature_celsius}')
    

if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_seoul_weather()
    
    pprint.pprint(result)