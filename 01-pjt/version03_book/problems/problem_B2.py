import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()  # .env 파일을 읽어 환경 변수로 설정합니다.

# 1. [ dotenv를 활용하여 알라딘 API 키 가져오기 ]
MY_TTBKEY = os.getenv('ALADIN_TTBKEY')
# 2. [ 공식 문서를 참고하여 알라딘 API 검색 URL 설정하기 ]
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 3. 주제별 도서 데이터를 가져오는 함수 정의
def fetch_books_by_topic(topic, max_results=30):
    url = ALADIN_SEARCH_URL
    # 3.1 [ API 요청에 필요한 파라미터 설정 (문서 참고하여 작성해보기) ]
    params = {
        'TTBKey' : MY_TTBKEY,
        'Query' : topic,
        'MaxResults' : max_results,
        'Output' : 'JS',
        'Version' : '20131101'
    }
    # 3.2 [ HTTP 요청 보내고 응답 데이터를 JSON 형식으로 반환하기 ]
    data = requests.get(url=url, params=params)

    json_data = json.loads(data.text)

    return json_data


# 4. 도서를 분류하고 파일에 저장하는 함수 정의
def classify_and_save_books():
    # 4.1 [ fetch_books_by_topic()을 호출하여 '경제' 관련 도서 검색하여 가져오기 ]
    economy_books = fetch_books_by_topic('경제', 50).get('item', [])

    # 분류하기 위한 리스트
    discounts = []
    regulars = []

    # 4.2 [ 할인 도서 분류하기 ]
    for book in economy_books:
        if book['priceSales'] < book['priceStandard']:
            discounts.append(book)
        else:
            regulars.append(book)

    # 4.3 [ output 폴더에 JSON 파일로 저장 ]
    root_path = 'C:/Users/SSAFY/Desktop/online-studyroom/pjt/버전3_도서/problems'
    
    # 해당 폴더가 없으면 생성하기
    if not os.path.exists(root_path + '/output'):
        Path(root_path + '/output').mkdir(parents=True, exist_ok=True)

    
    # 할인 중인 책 데이터를 "output/discounted_books.json"에 저장합니다.
    new_file_path = Path(root_path+'/output/discounted_books.json')

    with new_file_path.open('w', encoding='utf-8') as json_file:
        json.dump(discounts, json_file, ensure_ascii=False, indent=4)

    # 정가인 책 데이터를 "output/regular_priced_books.json"에 저장합니다.
    new_file_path = Path(root_path+'/output/regular_priced_books.json')

    with new_file_path.open('w', encoding='utf-8') as json_file:
        json.dump(regulars, json_file, ensure_ascii=False, indent=4)

    # 4.4 [ 분류 결과 출력 ]
    # 할인 중인 책과 정가인 책 개수를 출력합니다.
    print(f'할인 중인 책 {len(discounts)}개, 정가인 책 {len(regulars)}개를 저장했습니다.')


# 함수 실행
if __name__ == '__main__':
    classify_and_save_books()
    # print(fetch_books_by_topic('경제').get('item', []))