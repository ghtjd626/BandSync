# BandSync - 밴드 매칭 플랫폼 🎸

BandSync는 밴드와 뮤지션을 연결해주는 웹 기반 플랫폼입니다. 악기, 장르, 지역 등 다양한 조건을 기반으로 자신에게 맞는 밴드나 멤버를 찾을 수 있으며, 연습실 정보도 공유할 수 있습니다.

## 주요 기능 ✨

### 1. 밴드/뮤지션 매칭

- 상세한 프로필 설정 (악기, 장르, 실력 수준 등)
- 머신러닝 기반 추천 시스템
- 조건별 검색 및 필터링
- 지역 기반 매칭

### 2. 메시지 시스템

- 밴드 가입 신청
- 멤버 초대
- 실시간 알림
- 메시지 상태 관리 (대기중/수락/거절)

### 3. 연습실 정보 공유

- 지역별 연습실 검색
- 가격대별 필터링
- 리뷰 및 평점 시스템
- 편의시설 정보
- 위치 정보 (네이버 지도 연동)

### 4. 대시보드

- 최근 활동 내역
- 가입한 밴드 정보
- 밴드 멤버 관리
- 메시지 알림

## 기술 스택 🛠

### Backend

- Python 3.8+
- Flask 2.0.1
- SQLAlchemy 1.4.23
- Flask-Login (인증)
- Flask-SQLAlchemy (ORM)
- Flask-WTF (폼 처리)
- Scikit-learn (추천 시스템)

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap 5.1.3
- Jinja2 템플릿

### Database

- SQLite (개발)
- PostgreSQL (배포)

## 설치 방법 📦

1. 저장소 클론

```bash
git clone https://github.com/yourusername/BandSync.git
cd BandSync
```

2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 필요한 설정 입력
```

5. 데이터베이스 초기화

```bash
flask db upgrade
```

6. 개발 서버 실행

```bash
flask run
```

## 프로젝트 구조 📁

```
BandSync/
├── app.py              # 메인 애플리케이션
├── recommender.py      # 추천 시스템
├── requirements.txt    # 의존성 목록
├── static/
│   ├── css/           # 스타일시트
│   └── js/            # 자바스크립트
├── templates/          # HTML 템플릿
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── ...
└── migrations/        # 데이터베이스 마이그레이션
```

## 주요 기능 스크린샷 📸

### 메인 페이지

![메인 페이지](screenshots/main.png)

### 밴드/뮤지션 검색

![검색 페이지](screenshots/search.png)

### 연습실 정보

![연습실 정보](screenshots/practice-room.png)

## 기여 방법 🤝

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 향후 계획 🚀

- [ ] 모바일 앱 개발
- [ ] 실시간 채팅 기능
- [ ] 공연 정보 공유 기능
- [ ] 장비 거래/대여 기능
- [ ] 연습실 예약 시스템
- [ ] SNS 로그인 연동
- [ ] API 개발

## 라이선스 📝

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 개발자 정보 👨‍💻

- 이름: [Your Name]
- 이메일: [Your Email]
- GitHub: [@yourusername](https://github.com/yourusername)

## 감사의 글 🙏

이 프로젝트는 다음과 같은 오픈소스 프로젝트들의 도움을 받았습니다:

- Flask
- Bootstrap
- SQLAlchemy
- 그 외 requirements.txt에 명시된 모든 패키지
