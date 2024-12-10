import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import pandas as pd

class BandSyncRecommender:
    def __init__(self, users, messages, memberships):
        self.users = users
        self.messages = messages
        self.memberships = memberships
        self.user_features = None
        self.similarity_matrix = None
        self.user_id_to_index = None  # 사용자 ID와 인덱스 매핑을 저장
        
    def _create_user_features(self):
        """사용자 특성 벡터를 생성합니다."""
        features = defaultdict(lambda: {
            'genre_vector': np.zeros(10),  # 장르 원-핫 인코딩
            'location_vector': np.zeros(10),  # 지역 원-핫 인코딩
            'skill_level': 0,  # 실력 수준 (1-4)
            'activity_score': 0,  # 활동성 점수
            'success_rate': 0,  # 매칭 성공률
            'rating': 0  # 평균 평점
        })
        
        # 장르와 지역 인덱스 매핑 생성
        genres = list(set(user.genre for user in self.users if user.genre))
        locations = list(set(user.location for user in self.users if user.location))
        
        # 사용자별 특성 추출
        for user in self.users:
            # 장르 벡터
            if user.genre and user.genre in genres:
                features[user.id]['genre_vector'][genres.index(user.genre)] = 1
                
            # 지역 벡터
            if user.location and user.location in locations:
                features[user.id]['location_vector'][locations.index(user.location)] = 1
                
            # 실력 수준
            skill_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'professional': 4}
            features[user.id]['skill_level'] = skill_levels.get(user.skill_level, 0)
            
            # 활동성 점수 계산
            sent_messages = sum(1 for msg in self.messages if msg.sender_id == user.id)
            received_messages = sum(1 for msg in self.messages if msg.receiver_id == user.id)
            features[user.id]['activity_score'] = (sent_messages + received_messages) / 10
            
            # 매칭 성공률 계산
            total_messages = sum(1 for msg in self.messages 
                               if msg.sender_id == user.id or msg.receiver_id == user.id)
            successful_matches = sum(1 for member in self.memberships 
                                  if member.member_id == user.id or member.band_id == user.id)
            
            features[user.id]['success_rate'] = (successful_matches / total_messages) if total_messages > 0 else 0
            
        return features
    
    def _create_feature_matrix(self):
        """특성 벡터를 행렬로 변환합니다."""
        features = self._create_user_features()
        feature_matrix = []
        user_ids = []  # 사용자 ID 순서 저장
        
        for user_id in features:
            user_vector = np.concatenate([
                features[user_id]['genre_vector'],
                features[user_id]['location_vector'],
                [features[user_id]['skill_level']],
                [features[user_id]['activity_score']],
                [features[user_id]['success_rate']],
                [features[user_id]['rating']]
            ])
            feature_matrix.append(user_vector)
            user_ids.append(user_id)
            
        # 사용자 ID와 인덱스 매핑 생성
        self.user_id_to_index = {user_id: idx for idx, user_id in enumerate(user_ids)}
            
        return np.array(feature_matrix)
    
    def train(self):
        """추천 모델을 학습합니다."""
        # 특성 행렬 생성
        feature_matrix = self._create_feature_matrix()
        
        if len(feature_matrix) == 0:
            return
            
        # 특성 정규화
        scaler = StandardScaler()
        normalized_features = scaler.fit_transform(feature_matrix)
        
        # 코사인 유사도 계산
        self.similarity_matrix = cosine_similarity(normalized_features)
        self.user_features = feature_matrix
        
    def get_recommendations(self, user_id, n_recommendations=5, user_type_filter=None):
        """사용자에게 추천을 제공합니다."""
        # 사용자가 없거나 데이터가 충분하지 않은 경우 기본 추천
        if not self.users or len(self.users) < 2:
            return []
            
        if self.similarity_matrix is None:
            self.train()
            
        # 유사도 행렬이 비어있는 경우
        if self.similarity_matrix is None or len(self.similarity_matrix) == 0:
            return []
            
        # 현재 사용자의 인덱스 찾기
        if user_id not in self.user_id_to_index:
            return []
            
        user_idx = self.user_id_to_index[user_id]
        
        # 유사도 점수 가져오기
        similarity_scores = self.similarity_matrix[user_idx]
        
        # 추천 대상 필터링 (다른 유형의 사용자만)
        target_indices = []
        for user in self.users:
            if user.id in self.user_id_to_index and (not user_type_filter or user.user_type == user_type_filter):
                target_indices.append(self.user_id_to_index[user.id])
                
        # 유사도에 따라 정렬
        similar_indices = sorted(
            [(i, score) for i, score in enumerate(similarity_scores) if i in target_indices],
            key=lambda x: x[1],
            reverse=True
        )
        
        # 자기 자신 제외
        similar_indices = [(i, score) for i, score in similar_indices if i != user_idx]
        
        # 상위 N개 추천 반환
        recommended_users = []
        for idx, score in similar_indices[:n_recommendations]:
            user_id = [k for k, v in self.user_id_to_index.items() if v == idx][0]
            user = next((u for u in self.users if u.id == user_id), None)
            if user:
                recommended_users.append({
                    'user': user,
                    'similarity_score': score
                })
            
        return recommended_users 