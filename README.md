# Movie On Find - 취향에 맞는 나만의 영화 찾기

## 역할

- 사용한 프레임워크 & 언어
    - Django + VanillaJS
- 현탁
    - 영화데이터수집
    - 영화데이터 json화
    - card 기능 구현
    - review 기능 구현
    - card_collection기능 구현
    - 영화추천알고리즘 구현
    - 영화검색기능 구현
    - 기타 백엔드 구현

- 은경
    - 로그인(+소셜로그인)
    - 프로필 페이지 레이아웃 구현
    - 리뷰 페이지 레이아웃 구현
    - 기타 프론트엔드 구현

## 목표 서비스 구현 및 실제 구현 정도

- 무비온파인드란 유니온파인드가 루트노드를 찾는 것처럼 자신의 영화를 찾아가는 여정에서 만난 영화들을 사진으로 기록하고 다른 사람들과 공유해가며 또 한편으로 새로운 길을 찾아 자신의 영화를 찾는 과정을 의미하고 있습니다.
- 서비스 대상
    - 자기가 본 영화를 **포토티켓으로 수집**하고 싶은 사람!
    - 아카이빙 된 영화를 바탕으로 **새로운 영화를 추천**받고 싶은 사람!

| No. | 기능 | 기능 설명 | 구현도 |
| --- | --- | --- | --- |
| 1 | 로그인, 로그아웃, 회원가입, 회원탈퇴 | 사이트 로그인, 로그아웃, 회원가입, 회원탈퇴 기능 | ⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 2 | 프로필, 개인정보수정, 비밀번호변경 | 프로필,개인정보수정,비밀번호변경 기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 3 | 팔로잉, 팔로워 | 사용자간 팔로잉, 팔로워기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 4 | 소셜로그인(카카오톡, E-mail) | 소셜로그인(카카오톡, E-mail)기능 구현 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 5 | 개인별 interesting,watching,watched영화기능 | 영화상세 페이지에서 interesting, watching, watched버튼을 누르면 개인별 interesting, watching, watched영화목록 조회가능기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 6 | 카드CRUD | 내가 본영화에대한 포토카드 CRUD | ⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 7 | 카드좋아요 |  | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 8 | 리뷰CRUD | 영화에대한 리뷰 CRUD | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 9 | 리뷰좋아요 |  | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 10 | 리뷰코멘트생성,삭제,수정,좋아요 | 영화 리뷰에 대한 코멘트 CRUD, 좋아요기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 11 | 카드컬렉션CRUD | 내가 만든 카드를 가지고 포토북 CRUD | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 12 | 카드컬렉션 좋아요 | 포토북에대해 좋아요기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 13 | 영화조회 | 영화 장르, 평점, 인기도, 개봉일순으로 조회기능 | ⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 14 | 영화상세조회 | 영화에대한 상세정보조회기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 15 | 영화검색 | 키워드를 검색하여 해당키워드가 포함된 영화 조회기능 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 16 | 개인별 영화추천 | 회원가입시 입력한 장르를 바탕으로 영화장르와 비교하여 n개이상 일치할시 평점순으로 조회 기능 | ⭐⭐⭐⭐/⭐⭐⭐⭐⭐ |
| 17 | 영화배우별 출연리스트 | 시간부족으로 인해 미구현 | /⭐⭐⭐⭐⭐ |

## 컴포넌트

![Component.jpg](https://github.com/f1rstf1y9/movie_on_find/blob/main/readme/Component.jpg)

## ERD

![ERD.jpg](https://github.com/f1rstf1y9/movie_on_find/blob/main/readme/ERD.jpg)

## 영화추천 알고리즘

- 영화추천 서비스를 제공하기 위해 먼저 사용자가 회원가입시에 선호 장르를 선택할 수 있게 하였고 그 데이터를 바탕으로 사용자 맞춤 영화 추천 알고리즘을 구현하였다.
- 선택한 장르를 영화장르와 비교하여 교집합이 n개이상이면 해당 영화를 추천리스트에 담도록 구현하였다. 여기서는 파이썬 내장함수인 &을 사용하였다.
    - EX) 선호장르가 코메디, 액션, 판타지일때 여기서 2개이상 곂치는 영화를 추천리스트에 담아 서비스를 제공할 수 있도록 구현하였다.

## 서비스대표기능

| No. | 구분 | 기능 | 기능설명 |
| --- | --- | --- | --- |
| 1 | 로그인 | 카카오로그인 | 기존의 로그인 방식과 별도로 소셜로그인기능을 추가하였다. |
| 2 | 영화 | interesting,watching,watched, 팔로잉, 팔로워가능 | 개인별 interesting, watching, watched, 팔로잉, 팔로워가능 |
| 3 | 영화 | 개인맞춤 영화추천 | 각자가 좋아하는 장르를 바탕으로 다른영화와의 겹치는 장르의 갯수를 비교하여 추천하는 기능을 추가하였다. |
| 4 | 영화 | 영화장르별조회 | 장르별조회 및 평점, 인기도, 개봉일순정렬 |
| 5 | 카드 | 카드생성 | 나만의 카드제작 |
| 6 | 카드컬렉션 | 컬렉션 생성가능 | 내가만든 카드중에서 카드를 골라 컬렉션 생성가능 |

## 서비스구현과정에서 시행착오 및 해결방법

- 현탁
    - 카드컬렉션 : 처음에 일대다 관계인줄알고 구현했으나 나증에 다시 생각해보니 다대다 관계였었다. 모델을 수정하니 제대로 작동했다.
    - 영화데이터받기 : tmdb에서 받은 데이터에서 필요한 데이터만 따로 테이블에 저장하는 과정에서 누락시킨 데이블이 있어 오류가 발생했다. 테이블을 수정하니 제대로 작동했다.

## 기술적으로 아쉬웠던 부분

- 현탁
    - 최적화 : 영화를 조회 할때 응답속도를 좀 더 빠르게 하고 싶었지만 능력부족으로 해결하지 못함
    - 데이터모델생성 : 테이블명을 만드는데 필요이상으로 디테일 하게 테이블명을 정하면서 테이블명이 많이 길어졌다.
    - 코드 : 뭔가 기능을 구현하는데 집중하여 디테일 한 부분을 놓친것같다. 다음 프로젝트에는 좀더 디테일한 부분까지 생각해서 기능을 구현할 수 있도록 노력해야겠다고 생각했다.

- 은경
    - Vue 같은 프론트엔드 프레임워크를 쓰지 않고 작업을 하다보니 요소가 겹치는 부분이 많았음에도 계속 똑같은 코드를 반복해서 작성해주어야하는 번거로움이 있었다. 다음에는 프레임워크를 제대로 공부해서 이러한 비효율성을 줄이거 재사용성이 좋은 코드를 작성하고 싶다.

## 프로젝트 느낀점, 후기

- 현탁
    - 다시한번 내가 전반적으로 장고를 사용하는 데 있어 부족한점에 대해 깨닫는 시간이 었다. 모델구성부터 관계를 파악해 좀더 이해하기 쉬운 테이블명을 만들도록 해야겠다고 생각했다. 다음으로는 장고와 바닐라 자바스크립트로 프로젝트를 수행했는데 장고와 vue를 이용해 서버와 클라이언트를 구현할 수 있도록 다시한번 복습이 필요하다고 생각했다.

- 은경
    - 무작정 어떤 기능이 있었으면 좋겠다, 이런 기능이 있으면 좋아보이겠지하고 개발을 진행했는데 이 서비스를 사용할 사용자 입장에서 꼭 필요한 기능은 무엇일까 깊게 생각해보지 못한 점이 아쉬웠다.