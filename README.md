<div>
  <img src="/static/image/page1.png" width="75%"/>
</div>
# 📰 동아리타임
##### 🏆 피로그래밍 21기 최종 프로젝트 작품

### 📜 Contents
 1. [Overview](#-overview)
 2. [서비스 화면](#-서비스-화면)
 3. [주요 기능](#-주요-기능)
 4. [개발 환경](#%EF%B8%8F-개발-환경)
 5. [시스템 아키텍처](#-시스템-아키텍처)
 6. [기술 특이점](#-기술-특이점)
 7. [기획 및 설계 산출물](#-기획-및-설계-산출물)
 8. [Conventions](#-conventions)
 9. [팀원 소개](#-팀원-소개)
 
## ✨ Overview

> 동아리 부원들이 효과적이고 쉽게 소통하고 교류할 수 있는 웹서비스
<div>
  <img src="/static/image/page2.png" width="75%"/>
</div>
## ✨ 동아리타임의 배포 사이트
##### 🏆 [사이트](https://dongaritime.com/)



## ✨ 동아리타임의 소통 플랫폼 
##### 🏆 [노션](https://www.notion.so/4a62cbe2cba04313aa6b77d02c4eb374)
##### 🏆 [ZEP](https://zep.us/)


## 👀 서비스 화면
### ✨ 모든 페이지 `모바일 화면` 지원


### 홈
- '라인'의 랜딩페이지를 참고하여 접속시 애니메이션 효과로 화면이 변하게 구현했다.
- 로그인 및 회원가입 버튼을 누르수 있다
  
<div>
  <img src="/static/image/page3.png" width="75%"/>
  <img src="/static/image/page4.png" width="75%"/>
</div>


### 회원가입 & 로그인 & 로그아웃
- 유저 회원가입/로그인
- 로그인을 하면 동아리 생성/인증/선택 페이지로 넘어간다.
<div>
  <img src="/static/image/page5.png" width="75%"/>
  <img src="/static/image/page6.png" width="75%"/>
  <img src="/static/image/page7.png" width="75%"/>
</div>

### 동아리 생성 & 동아리 인증 & 동아리 선택
- 동아리를 생성하여 인증 코드를 생성하면 다른 사람이 해당 인증 코드를 통해 인증할 수 있다.
- 가입되어 있는 동아리 페이지를 선택하여 해당 동아리 메인 페이지로 이동한다.
<div>
  <img src="/static/image/page8-1.png" width="75%"/>
</div>
<div>
  <img src="/static/image/page8-2.png" width="75%"/>
</div>
<div>
  <img src="/static/image/page8.png" width="33%"/>
  <img src="/static/image/page9.png" width="33%"/>
  <img src="/static/image/page10.png" width="33%"/>
</div>

### 메인페이지
- 공지, 자유, 질문 게시판은 수정할 수 없고 게시판을 생성하거나 게시글 검색, 게시판 추가를 할 수 있다.

<div>
  <img src="/static/image/page11.png" width="75%"/>
</div>

### 마이페이지
- 닉네임, 비밀번호를 변경하거나 가입되어 있는 동아리를 관리할 수 있다.
- 내가 작성한 게시글, 내가 남긴 댓글, 스크랩한 게시글을 관리할 수 있다.
- 웹 알림 기능을 활성화하여 내 게시글에 댓글을 남기거나 대댓글이 달렸을 때 알림을 받을 수 있다.
<div>
  <img src="/static/image/page12-1.png" width="75%"/>
</div>
<div>
  <img src="/static/image/page12.png" width="75%"/>
</div>

### 내가 쓴 글
<div>
  <img src="/static/image/page16.png" width="75%"/>
</div>

### 내 댓글
<div>
  <img src="/static/image/page17.png" width="75%"/>
</div>

### 스크랩
<div>
  <img src="/static/image/page17.png" width="75%"/>
</div>

### 게시글 리스트(게시판)
- 게시글을 작성할 수 있다.
- 해당 게시판에 작성된 글을 보거나 베스트 게시글을 볼 수 있다.

<div>
  <img src="/static/image/page13.png" width="75%"/>
  <img src="/static/image/page14.png" width="75%"/>
</div>

### 게시글 작성
- Ajax를 이용한 게시글 작성으로 실시간으로 업로드가 가능하다.

<div>
  <img src="/static/image/page19.png" width="75%"/>
</div>

### 캘린더
- 동아리에 예정된 행사나 일정을 관리할 수 있다.
- 동아리원 모두가 생성 및 삭제할 수 있어 자유로운 일정관리가 가능하다.
<div>
  <img src="/static/image/page15-1.png" width="75%"/>
</div>

<div>
  <img src="/static/image/page15.png" width="75%"/>
</div>

  
## ✨ 주요 기능

- `동아리별 페이지`
	- 회원 1명이 여러 동아리에 가입되어 있어도 동아리 id로 필터링하여 동아리별로 커뮤니티를 가질 수 있다. 
	
- `웹 알림`
	- Django-Webpush 라이브러리를 사용하여 공지 게시판에 글이 올라오거나 게시글 작성 및 댓글 작성자에게 알림을 보낸다. 
  
- `일정 기능`
	- JS fullcalender를 사용하여 동아리 내의 모든 행사 및 일정을 추가하고 삭제하여 일정을 한 번에 관리할 수 있다.

- `아이디 찾기 및 비밀번호 재설정`
	- 회원가입할 때 작성한 사용자 이름과 이메일을 통해 아이디를 찾을 수 있다.
    - 회원가입할 때 작성한 이메일로 비밀번호 재설정 링크를 전송하여 비밀번호 재설정 기능을 도입하였다.


## 🖥️ 개발 환경

**Management Tool**
- 형상 관리 : Git
- 커뮤니케이션 : Zep, Notion, Discord
- 디자인 : Figma

**🐳 Backend**
- Python `3.8.0`
- Django `4.2.x`
- Django Rest Framework `3.12.x`
- pipenv (패키지 관리 도구)
- MySQL  `8.0.4`
- Oracle (WAS)
- Gunicorn `20.1.0` (배포용 WSGI 서버)


**🦊 Frontend**
- lang: HTML5, CSS3, JAVASCRIPT

**🖼️ Requirements.txt**
```plaintext
aiohappyeyeballs==2.3.5
aiohttp==3.10.3
aiosignal==1.3.1
asgiref==3.8.1
attrs==24.2.0
certifi==2024.7.4
cffi==1.17.0
charset-normalizer==3.3.2
cryptography==43.0.0
Django==5.0.7
django-environ==0.11.2
django-webpush==0.3.6
environ==1.0
frozenlist==1.4.1
http-ece==1.2.1
idna==3.7
multidict==6.0.5
django-webpush==0.3.6
frozenlist==1.4.1
http_ece==1.2.1
idna==3.7
multidict==6.0.5
mysql-connector-python==9.0.0
mysqlclient==2.2.4
pillow==10.4.0
py-vapid==1.9.1
pycparser==2.22
pywebpush==2.0.0
requests==2.32.3
six==1.16.0
sqlparse==0.5.1
tzdata==2024.1
urllib3==2.2.2
yarl==1.9.4
typing_extensions==4.12.2
urllib3==2.2.2
yarl==1.9.4
```

**🗂️ DB**
- MySQL `8.0.30`

**🌐 Server**
- AWS EC2 (Ubuntu `20.04`)
- Nginx `1.23` (Reverse Proxy)
- Gunicorn `20.1.0` (WSGI Application Server)
- Oracle (WAS)
- HTTPS (TLS `1.2`)

**🔨 IDE**
- VSCode `1.69.2`

## 💫 시스템 아키텍처

<div>
  <img src="/static/image/page20.png" width="75%"/>
</div>
<div>
  <img src="/static/image/page21.png" width="75%"/>
</div>

## ✨ ERD
<div>
  <img src="/static/image/page22.png" width="75%"/>
</div>


# 📂 기획 및 설계 산출물

### [💭 요구사항 정의 및 기능 명세](https://docs.google.com/spreadsheets/d/13E_o6jg15vNdrxVI8MzjdztVEvZe9d7lCpmCMvcBMrY/edit?gid=0#gid=02)

<div>
  <img src="/static/image/page23.png" width="75%"/>
</div>


### [🎨 화면 설계서](https://www.figma.com/design/rMTPVxIOu3Bx5OrPlzKjL8/%EB%8F%99%EC%95%84%EB%A6%AC%ED%83%80%EC%9E%84?node-id=211-61&node-type=canvas&t=aDmi6rF6sV0gPk1q-0)

<div>
  <img src="/static/image/page24.png" width="75%"/>
</div>



# 💞 팀원 소개
##### ❤️‍🔥 동아리타임을 개발한 `피로그래밍 21기` 팀원들을 소개합니다!

| **[나경원](https://github.com/kw601)** | **[강민석](https://github.com/min-soku)** | **[하동현](https://github.com/zkwlr)** | **[한라현](https://github.com/Rahyuni)** | **[황다예](https://github.com/imyyye)**
| :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: |
<img src="/static/image/nkw.jpeg" width="200"> | <img src="/static/image/kms.png" width="200"> | <img src="/static/image/hdh.png" width="200"> | <img src="/static/image/hrh.jpg.png" width="200"> |
<img src="/static//image/hdy.jpg" width="200"> |
| Leader & Backend & Frontend | Backend & Frontend | Backend & Frontend | Frontend & Backend | Frontend & Backend |



