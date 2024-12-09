import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class BandMatcher:
    def __init__(self, weights=None):
        """
        Initialize the BandMatcher with optional weights for matching criteria.
        Default weights:
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
        Add a user with their attributes.
        :param name: User's name
        :param skill: User's musical skill (e.g., Guitar, Drums)
        :param location: User's location
        :param session: Whether the user is available (True/False)
        :param genre: User's preferred genres as a comma-separated string
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
        Add a band with their attributes.
        :param name: Band's name
        :param required_skill: Skill the band is recruiting (e.g., Guitar, Drums)
        :param location: Band's location
        :param recruiting: Whether the band is actively recruiting (True/False)
        :param genre: Band's genre focus as a comma-separated string
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
        Match users to bands based on various conditions.
        Returns a sorted list of matches with scores.
        """
        results = []
        for _, user in self.users.iterrows():
            for _, band in self.bands.iterrows():
                # Check session and recruiting compatibility
                session_match = 1.0 if user['session'] and band['recruiting'] else 0.0

                # Check skill compatibility
                skill_match = 1.0 if user['skill'] == band['required_skill'] else 0.0

                # Check location compatibility
                location_match = 1.0 if user['location'] == band['location'] else 0.0

                # Calculate genre similarity
                genre_match = self._calculate_similarity(user['genre'], band['genre'])

                # Weighted score calculation
                score = (
                    self.weights['session'] * session_match +
                    self.weights['skill'] * skill_match +
                    self.weights['location'] * location_match +
                    self.weights['genre'] * genre_match
                )
                results.append((user['name'], band['name'], score))

        # Sort results by score (descending order)
        return sorted(results, key=lambda x: -x[2])

    @staticmethod
    def _calculate_similarity(user_genres, band_genres):
        """
        Calculate similarity between user and band genres using cosine similarity.
        :param user_genres: Comma-separated string of user genres
        :param band_genres: Comma-separated string of band genres
        """
        user_vector = [int(x) for x in user_genres.split(",")]
        band_vector = [int(x) for x in band_genres.split(",")]
        return cosine_similarity([user_vector], [band_vector])[0][0]

# Example usage
if __name__ == "__main__":
    matcher = BandMatcher()
    matcher.add_user("Alice", "Guitar", "NY", True, "1,0,1,0")  # Rock, Blues
    matcher.add_user("Bob", "Drums", "LA", False, "0,1,0,1")    # Jazz, Classical
    matcher.add_band("RockStars", "Guitar", "NY", True, "1,0,0,0")  # Rock
    matcher.add_band("JazzCats", "Drums", "LA", True, "0,1,0,1")    # Jazz, Classical

    matches = matcher.match()
    print("Matches:", matches)
