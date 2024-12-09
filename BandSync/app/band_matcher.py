import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class BandMatcher:
    def __init__(self):
        self.users = pd.DataFrame()
        self.bands = pd.DataFrame()

    def add_user(self, name, sessions, skills, location, genres, preferences):
        """Add a user with their attributes."""
        user_data = {
            'name': name,
            'sessions': sessions,  # List of possible sessions the user can play
            'skills': skills,      # Skill level (e.g., beginner, intermediate, advanced)
            'location': location,
            'genres': genres,      # List of preferred genres
            'preferences': preferences  # Preference vector for additional conditions
        }
        self.users = pd.concat([self.users, pd.DataFrame([user_data])], ignore_index=True)

    def add_band(self, name, recruiting_sessions, required_skills, location, genres, preferences):
        """Add a band with their attributes."""
        band_data = {
            'name': name,
            'recruiting_sessions': recruiting_sessions,  # List of sessions needed by the band
            'required_skills': required_skills,          # Skill level required
            'location': location,
            'genres': genres,        # List of band genres
            'preferences': preferences  # Preference vector for additional conditions
        }
        self.bands = pd.concat([self.bands, pd.DataFrame([band_data])], ignore_index=True)

    def match(self):
        """Match users to bands based on various conditions."""
        results = []
        for _, user in self.users.iterrows():
            for _, band in self.bands.iterrows():
                session_match = self._check_session_match(user['sessions'], band['recruiting_sessions'])
                skill_match = self._check_skill_match(user['skills'], band['required_skills'])
                location_match = user['location'] == band['location']
                genre_match = self._calculate_similarity(user['genres'], band['genres'])
                preference_match = self._calculate_similarity(user['preferences'], band['preferences'])

                # Weighting for different matching criteria
                score = (
                    session_match * 0.3 +
                    skill_match * 0.2 +
                    location_match * 0.2 +
                    genre_match * 0.2 +
                    preference_match * 0.1
                )
                results.append((user['name'], band['name'], score))
        
        return sorted(results, key=lambda x: -x[2])  # Sort by compatibility score

    @staticmethod
    def _check_session_match(user_sessions, band_sessions):
        """Check if at least one session matches."""
        return any(session in band_sessions for session in user_sessions)

    @staticmethod
    def _check_skill_match(user_skill, band_skill):
        """Check if user skill meets or exceeds band requirement."""
        skill_levels = ['beginner', 'intermediate', 'advanced']
        return skill_levels.index(user_skill) >= skill_levels.index(band_skill)

    @staticmethod
    def _calculate_similarity(user_features, band_features):
        """Calculate similarity between two feature sets."""
        user_vector = np.array(user_features)
        band_vector = np.array(band_features)
        if len(user_vector) == 0 or len(band_vector) == 0:
            return 0  # No similarity if either vector is empty
        return cosine_similarity([user_vector], [band_vector])[0][0]

# Example usage
if __name__ == "__main__":
    matcher = BandMatcher()
    matcher.add_user(
        name="Alice",
        sessions=["Guitar", "Vocals"],
        skills="advanced",
        location="NY",
        genres=[1, 0, 1, 1],  # Genre preferences as binary vector
        preferences=[1, 0, 0, 1]
    )
    matcher.add_user(
        name="Bob",
        sessions=["Drums"],
        skills="intermediate",
        location="LA",
        genres=[0, 1, 1, 0],
        preferences=[0, 1, 0, 1]
    )
    matcher.add_band(
        name="RockStars",
        recruiting_sessions=["Guitar", "Bass"],
        required_skills="intermediate",
        location="NY",
        genres=[1, 0, 1, 0],
        preferences=[1, 0, 0, 0]
    )
    matcher.add_band(
        name="DrumKings",
        recruiting_sessions=["Drums", "Vocals"],
        required_skills="advanced",
        location="LA",
        genres=[0, 1, 0, 1],
        preferences=[0, 1, 0, 1]
    )
    matches = matcher.match()
    print("Matches:", matches)
