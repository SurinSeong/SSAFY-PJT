import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# 1. [ 환경 변수 로드 ]
load_dotenv()

# APIKEY 설정
MY_TTBKEY = os.getenv('ALADIN_TTBKEY')
# 검색 url 변수 저장
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 2. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    url = ALADIN_SEARCH_URL

    params = {
        'TTBKey': MY_TTBKEY,
        'Query' : topic,
        'MaxResults' : max_results,
        'Output' : 'JS',
        'Version' : '20131101'
    }

    # 서버에 데이터 요청
    data = requests.get(url=url, params=params)

    # 요청 받은 데이터를 json 형식으로 변환
    json_data = json.loads(data.text)

    return json_data

# 3. '인공지능' 도서 데이터를 처리하는 함수 정의
def process_ai_books(max_results, filename):

    global root_path

    # 필터링된 책 저장 리스트
    book_list = []

    # 3.1 [ '인공지능' 관련 도서 검색 ]
    # fetch_books_by_topic()을 호출하여 '인공지능' 관련 도서를 100개 수집합니다.
    ai_books = fetch_books_by_topic('인공지능', max_results).get('item', [])
   

    # 3.2 [ 수집된 데이터에서 가격 정보가 있는 책 필터링 및 가격순 정렬 ]
    for book in ai_books:
        if 'priceSales' in book:
            book_list.append(book)
    
    # 가격순 정렬
    book_list.sort(key=lambda x:x['priceSales'], reverse=True)

    # 3.3 [ 상위 10개 도서 선택 ]
    top_10_books = book_list[:10]

    # 3.4 [ 상위 10개 도서 정보 출력 ]
    print('가격이 높은 순서대로 상위 10개 도서:')

    for i, book in enumerate(top_10_books, 1):
        title = book['title']
        price = book['priceSales']
        print(f'{i}. 제목 : {title}, 가격 : {price}원')

    # 3.5 [ JSON 파일로 저장할 데이터 준비 ]
    # 해당 파일이 있는지 확인하기
    Path(root_path + '/output').mkdir(parents=True, exist_ok=True)

    # output/ai_top10_books.json 파일로 저장
    new_file_path = Path(root_path + f'/output/{filename}')

    with new_file_path.open('w', encoding='utf-8') as json_file:
        json.dump(top_10_books, json_file, ensure_ascii=False, indent=4)

    # 3.6 [ 완료 메시지를 출력 ]
    print(f"'{filename}' 파일이 생성되었습니다.")

root_path = 'C:/Users/SSAFY/Desktop/online-studyroom/pjt/버전3_도서/problems'

# 함수 실행
if __name__ == '__main__':
    filename = 'ai_top10_books.json'
    process_ai_books(100, filename)
