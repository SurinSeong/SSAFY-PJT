# 관통 프로젝트 2

- 최종 프로젝트에 쓴다고 생각하고 디자인 생각하기

- 개발자 포트폴리오 페이지 만들기
- seobility 사이트 확인해서 기본적인 SEO 체크 해보면서 만들어보기

- alt + shift + F : 주석 정리해줌.

## 반응형 적용하기

1. flex - 정렬
    - 가장 기본적인 반응형 레이아웃 구현

2. grid system : 내부적으로 flex로 구현됨
    - 반응형 레이아웃 구현 시,
    - 가로 한 줄을 12칸으로 나눠가지기
        - 각 요소들이 원하는 만큼 가져가기
    - 정해진 픽셀 이상에서 원하는 크기를 재 설정
        - breakpoint
            - col-{breakpoint}-{N}

3. 추가적인 반응형 css
    - breakpoint 외의 작업은?
    - 색 변경은?
    - @media
        - min-width, max-width : 조건 이상, 조건 이하 일 때 적용
        - orientation : 화면의 가로 세로 여부
            - portrait (세로), landscape (가로)

- Figma 사용해서 이미지 추출한 다음 GPT에게 물어보고 기본 틀 짜는 거에서 수정해도 좋다.
    - 내가 디자인하고 싶은 틀에 맞는 UI를 추출해준다.
    