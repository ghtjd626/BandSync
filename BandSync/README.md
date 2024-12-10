# BandSync - 밴드 멤버 매칭 플랫폼

BandSync는 밴드와 뮤지션을 연결해주는 웹 기반 플랫폼입니다. 악기, 장르, 지역 등 다양한 조건을 기반으로 자신에게 맞는 밴드나 멤버를 찾을 수 있습니다.

## 주요 기능

- 사용자 프로필 생성 및 관리
- 밴드/멤버 검색 필터링
- 실시간 채팅
- 리뷰 및 평가 시스템
- 잼 세션 매칭

## 기술 스택

- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (Bootstrap)
- 추가 라이브러리: Flask-SQLAlchemy, Flask-Login, Flask-SocketIO

## 설치 방법

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

4. 애플리케이션 실행

```bash
python app.py
```

## 개발 환경 설정

1. 데이터베이스 초기화

```bash
flask db init
flask db migrate
flask db upgrade
```

2. 환경 변수 설정

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

프로젝트 관리자 - [@yourusername](https://github.com/yourusername)

프로젝트 링크: [https://github.com/yourusername/BandSync](https://github.com/yourusername/BandSync)
