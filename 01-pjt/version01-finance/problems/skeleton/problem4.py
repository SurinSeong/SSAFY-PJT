import os
import pprint
import requests

from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# 상품과 옵션 정보들을 담고 있는 새로운 객체를 만들어 반환하시오.
# [힌트] 상품 리스트와 옵션 리스트를 금융상품 코드를 기준으로 매칭할 수 있습니다.
# [힌트] 아래와 같은 순서로 데이터를 출력하며 진행합니다.
# 1. 응답을 json 형식으로 변환합니다.
# 2. key 값이 "result" 인 데이터를 변수에 저장합니다.
# 3. 2번의 결과 중 key 값이 "baseList" 인 데이터를 변수에 저장합니다.
# 4. 2번의 결과 중 key 값이 "optionList" 인 데이터를 변수에 저장합니다.
# 5. 3번에서 저장된 변수를 순회하며, 4번에서 저장된 값들에서 금융 상품 코드가 
#     같은 모든 데이터들을 가져와 새로운 딕셔너리로 저장합니다.
#     저장 시, 명세서에 맞게 출력되도록 저장합니다.
# 6. 5번에서 만든 딕셔너리를 결과 리스트에 추가합니다.


def setting_baseInfo(base_dict):
    base_eng_to_kor = {
        'kor_co_nm':'금융회사명',
        'fin_prdt_nm':'금융상품명',
        'fin_prdt_cd':'금융상품코드'
    }
    
    new_dict = dict()
    
    for base_key, base_value in base_dict.items():
        if base_key in base_eng_to_kor:
            new_dict[base_eng_to_kor[base_key]] = base_value
     
    return new_dict


def setting_optionInfo(option_dict):
    option_eng_to_kor = {
        'fin_prdt_cd':'금융상품코드',
        'intr_rate':'저축 금리',
        'save_trm':'저축 기간',
        'intr_rate_type':'저축 금리 유형',
        'intr_rate_type_nm':'저축 금리 유형명',
        'intr_rate2':'최고 우대금리'
    }
    
    new_dict = dict()
    
    for option_key, option_value in option_dict.items():
        if option_key in option_eng_to_kor:
            new_dict[option_eng_to_kor[option_key]] = option_value
    
    return new_dict


def find_same_value(info, key):
    grouped = defaultdict(list)
    
    for d in info:
        # '금융상품코드'를 제거한 새로운 딕셔너리 생성
        d_copy = d.copy()  # 원본 딕셔너리를 수정하지 않도록 복사
        d_copy.pop(key, None)
        grouped[d[key]].append(d_copy)
    
    return dict(grouped)


def get_deposit_products():
    # 본인의 API KEY 로 수정합니다.
    api_key = os.getenv('FINANCE_APIKEY')

    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?'
    params = {'auth' : api_key,
              'topFinGrpNo':'020000',
              'pageNo':'1'}

    result = requests.get(url=url, params=params).json()

    key_result = result['result']
    # pprint.pprint(key_result)

    # baseInfo
    base_data = key_result['baseList']
    
    for i, data in enumerate(base_data):
        base_data[i] = setting_baseInfo(data)
    
    # optionInfo
    option_data = key_result['optionList']
    
    for i, data in enumerate(option_data):
        option_data[i] = setting_optionInfo(data)
    
    # 금융 상품 코드가 같은 것 끼리 묶기    
    new_option_data = find_same_value(option_data, '금융상품코드')
    
    new_list = []
    
    for data in base_data:
        new_dict = {}
        
        for key, value in data.items():
            if value in new_option_data:
                # 필요한 데이터 추가
                new_dict['금리정보'] = new_option_data[value]
                
            if '금융상품코드' != key:
                new_dict[key] = value
                
        new_list.append(new_dict)

    return new_list
  

if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_deposit_products()
    # prrint.prrint(): json 을 보기 좋은 형식으로 출력
    pprint.pprint(result)