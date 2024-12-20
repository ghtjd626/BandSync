# BandSync - 밴드 매칭 플랫폼 🎸

BandSync는 밴드와 뮤지션을 연결해주는 웹 기반 플랫폼입니다. 악기, 장르, 지역 등 다양한 조건을 기반으로 자신에게 맞는 밴드나 멤버를 찾을 수 있으며, 연습실 정보도 공유할 수 있습니다.

## 매칭 및 추천 시스템 🤖

BandSync는 고도화된 머신러닝 기반의 매칭 시스템을 사용하여 사용자에게 최적의 밴드 또는 멤버를 추천합니다.

### 추천 알고리즘

1. **하이브리드 추천 방식**

   - 콘텐츠 기반 필터링: 사용자의 프로필 정보 활용
   - 협업 필터링: 사용자 활동 데이터 기반
   - 가중치 기반 하이브리드 모델

2. **주요 매칭 요소**

   - 장르 적합도 (원-핫 인코딩)
   - 실력 수준 매칭
   - 지역 근접성
   - 활동 시간대
   - 선호 음악 스타일

3. **고려하는 특성**

   ```python
   features = {
       'genre_vector': [1, 0, 0, ...],  # 장르 원-핫 인코딩
       'location_vector': [0, 1, 0, ...],  # 지역 원-핫 인코딩
       'skill_level': 3,  # 1-4 수준
       'activity_score': 0.85,  # 활동성 점수
       'success_rate': 0.75,  # 매칭 성공률
   }
   ```

4. **매칭 점수 계산**
   - 코사인 유사도 기반 매칭
   - 표준화된 특성 벡터 사용
   - 동적 가중치 조정

### 매칭 프로세스

1. **프로필 분석**

   - 사용자 입력 정보 벡터화
   - 활동 데이터 수집 및 분석
   - 선호도 패턴 추출

2. **추천 생성**

   - 유사도 점수 계산
   - 상위 N개 추천 선정
   - 다양성 보장을 위한 필터링

3. **지속적 개선**
   - 사용자 피드백 반영
   - A/B 테스트를 통한 알고리즘 개선
   - 주기적인 모델 재학습

### 기술적 구현

```python
class BandSyncRecommender:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()

    def preprocess_features(self, user_data):
        # 특성 전처리 및 벡터화
        features = self._extract_features(user_data)
        return self.scaler.transform(features)

    def generate_recommendations(self, user_id, n_recommendations=5):
        # 추천 생성
        user_vector = self.get_user_vector(user_id)
        similarities = self.compute_similarities(user_vector)
        return self.filter_top_recommendations(similarities, n_recommendations)
```

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
git clone https://github.com/ghtjd626/BandSync.git
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

<img width="1511" alt="스크린샷 2024-12-11 오전 1 50 38" src="https://github.com/user-attachments/assets/80bffbb6-508c-4e48-a91f-cc072c5c5c47">
<img width="1512" alt="스크린샷 2024-12-11 오전 1 59 37" src="https://github.com/user-attachments/assets/68a11f1f-f8ba-444c-ab2d-c62c09bb4bad">
<img width="1512" alt="스크린샷 2024-12-11 오전 2 06 09" src="https://github.com/user-attachments/assets/8f1643e0-1a27-4358-b39a-aece787ab652">
<img width="1512" alt="스크린샷 2024-12-11 오전 2 06 22" src="https://github.com/user-attachments/assets/ed2c3d5d-2666-437f-9880-2d4fdbfd100c">
<img width="1509" alt="스크린샷 2024-12-11 오전 2 06 40" src="https://github.com/user-attachments/assets/81627cd5-6364-46f7-a016-408f647a50fb">
<img width="1512" alt="스크린샷 2024-12-11 오전 2 06 52" src="https://github.com/user-attachments/assets/c9b27d60-1026-4a09-941b-b70abe5e0eba">
<img width="786" alt="스크린샷 2024-12-11 오전 2 07 01" src="https://github.com/user-attachments/assets/e2089825-f0da-4b80-9f15-5d2a5ca68c9d">
<img width="1511" alt="스크린샷 2024-12-11 오전 2 07 15" src="https://github.com/user-attachments/assets/cc3292f2-cad2-42c3-99d4-125ef19cc03d">
<img width="1512" alt="스크린샷 2024-12-11 오전 2 07 24" src="https://github.com/user-attachments/assets/61374c2f-4d35-4f25-95fb-d2c4bec8fc8d">
<img width="1512" alt="스크린샷 2024-12-11 오전 2 08 07" src="https://github.com/user-attachments/assets/7cd3dda8-d11d-48c9-ac26-3438eb1bd01f">
<img width="1512" alt="스크린샷 2024-12-11 오전 2 08 26" src="https://github.com/user-attachments/assets/b0ac1f50-8614-4fb7-b323-e0589e15c039">
<img width="1509" alt="스크린샷 2024-12-11 오전 2 08 38" src="https://github.com/user-attachments/assets/1d60d64c-cf32-4a04-9044-1095e5f6c826">



## 향후 계획 🚀

- [ ] 모바일 앱 개발
- [ ] 실시간 채팅 기능
- [ ] 공연 정보 공유 기능
- [ ] 장비 거래/대여 기능
- [ ] 연습실 예약 시스템
- [ ] SNS 로그인 연동
- [ ] API 개발


## 개발자 정보 👨‍💻

- 이름: [전근호]
- 이메일: [ghtjd626@naver.com]
- GitHub: [@ghtjd626](https://github.com/ghtjd626)

## 라이선스 📝

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](https://github.com/ghtjd626/BandSync/blob/main/LICENSE) 파일을 참조하세요.

## 오픈소스 🙏

이 프로젝트는 다음과 같은 오픈소스 프로젝트들의 도움을 받았습니다:

- Flask
- Bootstrap
- SQLAlchemy
- 그 외 requirements.txt에 명시된 모든 패키지
