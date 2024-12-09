import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class BandMatcher:
    def __init__(self):
        self.users = pd.DataFrame()
        self.bands = pd.DataFrame()
        self.weights = {
            "session": 0.3,
            "skill": 0.3,
            "location": 0.2,
            "genre": 0.2
        }

    def add_user(self, name, sessions, skill, location, genres):
        """Add a user with their attributes."""
        user_data = {
            'name': name,
            'sessions': sessions.split(","),
            'skill': skill,
            'location': location,
            'genres': genres.split(",")
        }
        self.users = pd.concat([self.users, pd.DataFrame([user_data])], ignore_index=True)

    def add_band(self, name, recruiting_sessions, required_skill, location, genres):
        """Add a band with their attributes."""
        band_data = {
            'name': name,
            'recruiting_sessions': recruiting_sessions.split(","),
            'required_skill': required_skill,
            'location': location,
            'genres': genres.split(",")
        }
        self.bands = pd.concat([self.bands, pd.DataFrame([band_data])], ignore_index=True)

    def match(self):
        """Match users to bands based on compatibility."""
        results = []
        for _, user in self.users.iterrows():
            for _, band in self.bands.iterrows():
                session_match = self._session_match(user['sessions'], band['recruiting_sessions'])
                skill_match = self._skill_match(user['skill'], band['required_skill'])
                location_match = self._location_match(user['location'], band['location'])
                genre_match = self._calculate_similarity(user['genres'], band['genres'])

                score = (
                    session_match * self.weights["session"] +
                    skill_match * self.weights["skill"] +
                    location_match * self.weights["location"] +
                    genre_match * self.weights["genre"]
                )
                results.append((user['name'], band['name'], score))
        
        return sorted(results, key=lambda x: -x[2])  # Sort by compatibility score

    @staticmethod
    def _session_match(user_sessions, band_sessions):
        """Check if any session matches."""
        return 1.0 if any(session in band_sessions for session in user_sessions) else 0.0

    @staticmethod
    def _skill_match(user_skill, band_skill):
        """Evaluate skill compatibility."""
        skill_levels = {"beginner": 1, "intermediate": 2, "advanced": 3}
        user_level = skill_levels.get(user_skill.lower(), 0)
        band_level = skill_levels.get(band_skill.lower(), 0)
        return 1.0 if user_level >= band_level else 0.0

    @staticmethod
    def _location_match(user_location, band_location):
        """Check if locations are the same."""
        return 1.0 if user_location == band_location else 0.0

    @staticmethod
    def _calculate_similarity(user_genres, band_genres):
        """Calculate genre similarity using cosine similarity."""
        user_vector = [1 if genre in user_genres else 0 for genre in user_genres + band_genres]
        band_vector = [1 if genre in band_genres else 0 for genre in user_genres + band_genres]
        return cosine_similarity([user_vector], [band_vector])[0][0]

# Example usage
if __name__ == "__main__":
    matcher = BandMatcher()
    matcher.add_user("Alice", "Guitar,Drums", "Intermediate", "NY", "Rock,Pop")
    matcher.add_user("Bob", "Vocals", "Beginner", "LA", "Jazz,Blues")
    matcher.add_band("RockStars", "Guitar,Drums", "Intermediate", "NY", "Rock,Blues")
    matcher.add_band("JazzKings", "Vocals,Piano", "Beginner", "LA", "Jazz,Pop")
    matches = matcher.match()
    print("Matches:", matches)
