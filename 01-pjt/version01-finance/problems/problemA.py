import os
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


json_response = get_seoul_weather()

print(json_response.keys())
