import os
import pprint
import requests
from dotenv import load_dotenv

load_dotenv()

# 응답 중 정기예금 상품들의 옵션 리스트를 출력하도록 구성합니다.
# 이 때, 원하는 데이터만 추출하여 새로운 리스트를 만들어 반환하는 함수를 작성하시오.
# [힌트] 아래와 같은 순서로 데이터를 출력하며 진행합니다.
# 1. 응답을 json 형식으로 변환합니다.
# 2. key 값이 "result" 인 데이터를 출력합니다.
# 3. 위의 결과 중 key 값이 "optionList" 인 데이터를 변수에 저장합니다.
# 4. 3번에서 저장된 값을 반복하며, 원하는 데이터만 추출 및 가공하여 결과 리스트에 저장합니다.

def get_deposit_products():
    # 본인의 API KEY 로 수정합니다.
    api_key = os.getenv('FINANCE_APIKEY')

    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?'
    params = {'auth' : api_key,
              'topFinGrpNo':'020000',
              'pageNo':'1'}

    result = requests.get(url=url, params=params).json()

    target_data = result['result']['optionList']

    eng_to_kor = {
        'fin_prdt_cd':'금융상품코드',
        'intr_rate':'저축 금리',
        'save_trm':'저축 기간',
        'intr_rate_type':'저축 금리 유형',
        'intr_rate_type_nm':'저축 금리 유형명',
        'intr_rate2':'최고 우대금리'
    }

    result_list = []

    for target in target_data:
        new_dict = dict()

        for key, value in target.items():
            if key in eng_to_kor:
                new_dict[eng_to_kor[key]] = value
        
        result_list.append(new_dict)

    return result_list

    
# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_deposit_products()
    # prrint.prrint(): json 을 보기 좋은 형식으로 출력
    pprint.pprint(result)

    


