# 메이플스토리 디스코드 봇

## Project Info
- maple.gg에서 유저 정보 크롤링후 정보 제공 
- maple api를 사용해 패치 정보 제공
## Change Logs
- 1.0 mapel.gg에서 유저 정보 크롤링후 제공하는 기능 추가
- 1.01 크롤링시 서버 부하를 줄이기 위해 코드 최적화
- 1.1 공식 홈페이지에서 이벤트 정보 크롤링 후 제공하는 기능 추가 
- 1.11 명령어 최적화
- 1.2 maple api사용 패치정보 제공하는 기능 추가
## Need to fix
- 파싱 함수 최적화
## Bugs
- 
```
# Used package
- asyncio: 비동기 통신을 위해 사용됨
- requsets: maple.gg에서 유저 정보및 공홈 이벤트 정보를 크롤링 하기 위해 사용됨
- bs4: 크롤링 데이터를 파싱하기 위해 사용됨
- zeep: SOAP기반 메이플api를 이용하기 위해 사용됨
- discord: 디스코드 못을 만들기 위해 사용됨
- os: 배포시 편리를 위해 사용됨
```
## Authors
- 김윤철
## License
This project is licensed under the MIT License
