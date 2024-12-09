import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class BandMatcher:
    def __init__(self, weights=None):
        """
        BandMatcher를 초기화합니다. 매칭 기준에 대한 선택적 가중치를 설정할 수 있습니다.
        기본 가중치:
        - session: 0.3
        - skill: 0.3
        - location: 0.2
        - genre: 0.2
        """
        self.users = pd.DataFrame()
        self.bands = pd.DataFrame()
        self.weights = weights or {
            'session': 0.3,
            'skill': 0.3,
            'location': 0.2,
            'genre': 0.2
        }

    def add_user(self, name, skill, location, session, genre):
        """
        사용자를 속성과 함께 추가합니다.
        :param name: 사용자의 이름
        :param skill: 사용자의 음악적 기술 (예: 기타, 드럼)
        :param location: 사용자의 위치
        :param session: 사용자가 사용 가능한지 여부 (True/False)
        :param genre: 사용자가 선호하는 장르를 쉼표로 구분한 문자열
        """
        user_data = {
            'name': name,
            'skill': skill,
            'location': location,
            'session': session,
            'genre': genre
        }
        self.users = pd.concat([self.users, pd.DataFrame([user_data])], ignore_index=True)

    def add_band(self, name, required_skill, location, recruiting, genre):
        """
        밴드를 속성과 함께 추가합니다.
        :param name: 밴드의 이름
        :param required_skill: 밴드가 모집하는 기술 (예: 기타, 드럼)
        :param location: 밴드의 위치
        :param recruiting: 밴드가 적극적으로 모집 중인지 여부 (True/False)
        :param genre: 밴드의 장르 초점을 쉼표로 구분한 문자열
        """
        band_data = {
            'name': name,
            'required_skill': required_skill,
            'location': location,
            'recruiting': recruiting,
            'genre': genre
        }
        self.bands = pd.concat([self.bands, pd.DataFrame([band_data])], ignore_index=True)

    def match(self):
        """
        다양한 조건에 따라 사용자와 밴드를 매칭합니다.
        점수가 포함된 매칭 결과를 정렬된 리스트로 반환합니다.
        """
        results = []
        for _, user in self.users.iterrows():
            for _, band in self.bands.iterrows():
                # 세션 및 모집 호환성 확인
                session_match = 1.0 if user['session'] and band['recruiting'] else 0.0

                # 기술 호환성 확인
                skill_match = 1.0 if user['skill'] == band['required_skill'] else 0.0

                # 위치 호환성 확인
                location_match = 1.0 if user['location'] == band['location'] else 0.0

                # 장르 유사도 계산
                genre_match = self._calculate_similarity(user['genre'], band['genre'])

                # 가중치 점수 계산
                score = (
                    self.weights['session'] * session_match +
                    self.weights['skill'] * skill_match +
                    self.weights['location'] * location_match +
                    self.weights['genre'] * genre_match
                )
                results.append((user['name'], band['name'], score))

        # 점수에 따라 결과를 정렬 (내림차순)
        return sorted(results, key=lambda x: -x[2])

    @staticmethod
    def _calculate_similarity(user_genres, band_genres):
        """
        사용자와 밴드 장르 간의 유사도를 코사인 유사도를 사용하여 계산합니다.
        :param user_genres: 쉼표로 구분된 사용자 장르 문자열
        :param band_genres: 쉼표로 구분된 밴드 장르 문자열
        """
        user_vector = [int(x) for x in user_genres.split(",")]
        band_vector = [int(x) for x in band_genres.split(",")]
        return cosine_similarity([user_vector], [band_vector])[0][0]

# 예제 사용법
if __name__ == "__main__":
    matcher = BandMatcher()
    matcher.add_user("앨리스", "기타", "뉴욕", True, "1,0,1,0")  # 록, 블루스
    matcher.add_user("밥", "드럼", "로스앤젤레스", False, "0,1,0,1")  # 재즈, 클래식
    matcher.add_band("록스타즈", "기타", "뉴욕", True, "1,0,0,0")  # 록
    matcher.add_band("재즈캣츠", "드럼", "로스앤젤레스", True, "0,1,0,1")  # 재즈, 클래식

    matches = matcher.match()
    print("매칭 결과:", matches)
