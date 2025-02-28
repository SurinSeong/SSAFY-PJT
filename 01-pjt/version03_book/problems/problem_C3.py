import os
import requests
import json
from pathlib import Path
from gtts import gTTS
from dotenv import load_dotenv

# 1. [ 환경 변수 로드 ]

load_dotenv()

# 알라딘 API KEY 저장
MY_TTBKEY = os.getenv('ALADIN_TTBKEY')
# 검색 url 저장
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 2. [ 최대 100개까지 주제별 도서 데이터를 가져오는 함수 정의 ]
def fetch_books_by_topic(topic, max_results=100):
    url = ALADIN_SEARCH_URL

    params = {
        'TTBKey' : MY_TTBKEY,
        'Query' : topic,
        'MaxResults' : max_results,
        'Output' : 'JS',
        'Version' : '20131101',
    }

    # 서버에 데이터 요청하기
    data = requests.get(url=url, params=params)

    # JSON 형식으로 변환
    json_data = json.loads(data.text)

    return json_data


# 3. [ 도서 정보를 텍스트 파일로 저장하는 함수 정의 ]
def save_books_info(books, filename):
    
    global root_path

    # 책 정보 저장할 리스트
    book_list = []

    for book in books:
        # 책 정보를 "제목, 저자, 소개" 형식으로 변환
        title = book['title']
        author = book['author']
        description = book['description']
        info = f'제목: {title}, 저자: {author}, 소개: {description}'
        
        # 리스트에 추가
        book_list.append(info)
    
    # 해당 폴더 있는지 확인하기
    Path(root_path+'/output').mkdir(parents=True, exist_ok=True)

    # txt 파일로 저장
    with open(root_path + '/' + filename, 'w', encoding='utf-8') as txt_file:
        for book_info in book_list:
            txt_file.write(book_info + '\n')

    # # 저장된 txt 파일 출력
    # print(Path(root_path + '/' + filename).read_text(encoding='utf-8'))

    print(f"{filename} 파일이 생성되었습니다.")


# 5. [ 텍스트 파일을 오디오 파일로 변환하는 함수 정의 ]
def create_audio_file(text_file, audio_file):

    global root_path

    tts = gTTS(text_file, lang='ko', slow=False)

    # 해당 폴더 있는지 확인하기
    Path(root_path+'/output').mkdir(parents=True, exist_ok=True)

    tts.save(root_path + '/' + audio_file)

    print(f"{audio_file} 파일이 생성되었습니다.")


# 6. [ 음악 관련 도서 데이터를 처리하는 함수 정의 ]
def process_music_books():
    # 6.1 [ '음악' 주제의 도서 데이터 수집 ]
    books = fetch_books_by_topic('음악', 10).get('item', [])

    # 6.2 [ 도서 정보를 텍스트 파일로 저장 ]
    txt_filename = 'output/music_books_info.txt'
    save_books_info(books, txt_filename)

    # 6.3 [ 텍스트 파일을 오디오 파일로 변환 ]
    audio_file = 'output/music_books.mp3'
    create_audio_file(root_path+'/'+txt_filename, audio_file)

    print("모든 작업이 완료되었습니다.")


root_path = 'C:/Users/SSAFY/Desktop/online-studyroom/pjt/버전3_도서/problems'

# 함수 실행
if __name__ == '__main__':
    process_music_books()
