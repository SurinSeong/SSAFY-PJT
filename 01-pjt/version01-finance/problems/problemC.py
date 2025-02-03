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


eng_to_kor = {
    'feels_like':'체감온도',
    'humidity':'습도',
    'pressure':'기압',
    'temp':'온도',
    'temp_max':'최고온도',
    'temp_min':'최저온도',
    'description':'요약',
    'icon':'아이콘',
    'main':'핵심',
    'id':'식별자'
}

json_response = get_seoul_weather()

new_dict = dict()
new_dict['기본'] = json_response['main']
new_dict['날씨'] = json_response['weather']

print(new_dict)


# 키값을 변환하는 함수 만들기
def change_keyname(target_dict, change_dict):

    for key, value in target_dict.items():
        if key in change_dict:
            target_dict[change_dict[key]] = target_dict.pop(key)
        
        # 값이 딕셔너리면 재귀적으로 변경
        if isinstance(value, dict):
            change_dict(value, change_dict)
        
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    change_keyname(item, change_dict)


    return target_dict


result = change_keyname(new_dict['기본'], eng_to_kor)


pprint.pprint(result)