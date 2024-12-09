import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class BandMatcher:
    def __init__(self):
        self.users = pd.DataFrame()
        self.bands = pd.DataFrame()

    def add_user(self, name, skill, location, preferences):
        """Add a user with their attributes."""
        user_data = {
            'name': name,
            'skill': skill,
            'location': location,
            'preferences': preferences
        }
        self.users = pd.concat([self.users, pd.DataFrame([user_data])], ignore_index=True)

    def add_band(self, name, required_skill, location, preferences):
        """Add a band with their attributes."""
        band_data = {
            'name': name,
            'required_skill': required_skill,
            'location': location,
            'preferences': preferences
        }
        self.bands = pd.concat([self.bands, pd.DataFrame([band_data])], ignore_index=True)

    def match(self):
        """Match users to bands based on compatibility."""
        results = []
        for _, user in self.users.iterrows():
            for _, band in self.bands.iterrows():
                skill_match = user['skill'] == band['required_skill']
                location_match = user['location'] == band['location']
                preference_match = self._calculate_similarity(user['preferences'], band['preferences'])
                
                score = skill_match * 0.4 + location_match * 0.4 + preference_match * 0.2
                results.append((user['name'], band['name'], score))
        
        return sorted(results, key=lambda x: -x[2])  # Sort by compatibility score

    @staticmethod
    def _calculate_similarity(user_pref, band_pref):
        """Calculate similarity between user and band preferences."""
        user_vector = [int(x) for x in user_pref.split(",")]
        band_vector = [int(x) for x in band_pref.split(",")]
        return cosine_similarity([user_vector], [band_vector])[0][0]

# Example usage
if __name__ == "__main__":
    matcher = BandMatcher()
    matcher.add_user("Alice", "Guitar", "NY", "1,0,1")
    matcher.add_user("Bob", "Drums", "LA", "0,1,1")
    matcher.add_band("RockStars", "Guitar", "NY", "1,0,0")
    matcher.add_band("DrumKings", "Drums", "LA", "0,1,1")
    matches = matcher.match()
    print("Matches:", matches)
