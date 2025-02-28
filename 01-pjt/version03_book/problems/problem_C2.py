import os
import requests
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 1. [ 환경 변수 로드 ]
load_dotenv()

MY_TTBKEY = os.getenv('ALADIN_TTBKEY') # 알라딘 API 가져오기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') # OpenAI API 가져오기

ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 2. OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)


# 3. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    url = ALADIN_SEARCH_URL

    params = {
        'TTBKey' : MY_TTBKEY,
        'Query' : topic,
        'MaxResults' : max_results,
        'Output' : 'JS',
        'Version' : '20131101',
    }

    # 서버에 데이터 요청
    data = requests.get(url=url, params=params)

    # JSON 데이터 변환
    json_data = json.loads(data.text)

    return json_data


# 4. 책 데이터를 ChatGPT로 분류하는 함수 정의 (습관, 시간관리, 독서법, 기타)
def classify_books_with_gpt(books):
    # 4.1 [ 분류할 책 제목들을 전달하기 편한 문자열로 취합 ]
    titles = ''

    for book in books:
        title = book['title'] + ', '
        titles += title
    
    titles = titles.strip(', ')

    # 4.2 [ ChatGPT 대화 메시지 설정 (프롬프트 작성) ]
    # 습관, 시간관리, 독서법, 기타 로 분류
    conversation_history = [
        {"role": "system", "content": "You are a professional expert about book classification."},      # 페르소나 작성
        {"role": "user", "content": """
                                    
                                    Please remember the book titles and categorize books I'd like to categorize based on the given criteria:
                                    1) Habit, 2) Time Management, 3) Reading Methods, 4) Others
                                    
                                    Return the answer in JSON.
                                    
                                    """} # 요청 프롬프트 작성
    ]
    conversation_history.append(
        {'role':'user', 'content':f'Book Titles : {titles}'}
    )

    # 4.3 [ 생성형 AI에 분류 요청 보내기 ]
    # API 호출 및 파라미터 설정
    # client.chat.completions.create() 호출 (example 코드 참고)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=conversation_history,
        # max_tokens=1000,
        temperature=0.5,
        top_p=1,
        n=1,
        seed=100
    )
    

    # 4.4 [ ChatGPT의 응답을 가져와 JSON 으로 추출 ]
    # ! 주의. JSON 형태로 프롬프팅을 하지 못하면 파싱에서 에러가 발생할 수 있습니다.
    # print(response.choices[0])
    ai_response = response.choices[0].message.content  # 응답에서 JSON 데이터를 추출하고 파싱
    # print(ai_response)
    
    classification = ai_response.strip('```json').strip('```').strip()
    # print(classification)

    return classification   # 분류 정보 반환


# 5. [ 데이터를 JSON 파일로 저장하는 함수 정의 ]
def save_to_json(data, filename):
    # json 타입으로 변경
    json_data = json.loads(data)
    
    # 해당 폴더가 있는지 확인하기
    current_path = Path.cwd()
    (current_path / 'output').mkdir(parents=True, exist_ok=True)
    
    # 폴더 생성하기
    with open(current_path /  filename, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    

# 6. '독서' 도서 데이터를 처리하는 함수 정의
def process_reading_books():
    # 6.1 [ '독서'와 관련된 도서 검색 (100개) ]
    books = fetch_books_by_topic('독서').get('item', [])  # fetch_books_by_topic() 호출

    # 6.2 [ 생성형 AI를 이용해 책 분류 ]
    classification = classify_books_with_gpt(books)  # classify_books_with_gpt() 호출
    
    # 6.3 [ 분류된 책 정보를 JSON 파일로 저장 ]
    # output/reading_habits.json 으로 저장하기
    filename = 'output/reading_habits.json'
    save_to_json(classification, filename)  # save_to_json() 호출
    

    # 완료 메시지 출력
    print("'output/reading_habits.json' 파일이 생성되었습니다.")


# 함수 실행
if __name__ == '__main__':
    process_reading_books()
