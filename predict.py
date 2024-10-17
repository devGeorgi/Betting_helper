class EloRatingSystem:
    def __init__(self, k_factor=30, file_path="teams.txt"):
        """Initialize Elo rating system with a K-factor and file path for team ratings."""
        self.k_factor = k_factor
        self.ratings = {}
        self.file_path = file_path
        self.load_ratings()

    def load_ratings(self):
        """Load team ratings and matches played from a text file."""
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        # Split team name, rating, and matches played
                        *team_parts, rating, matches_played = line.split()  # Split into components
                        team = ' '.join(team_parts)  # Reconstruct team name from parts
                        self.ratings[team] = [float(rating), int(matches_played)]
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Please create it with team ratings.")

    def get_rating(self, team):
        """Get rating and matches played for a team. Initialize to 1500 and 0 matches if not present."""
        if team not in self.ratings:
            self.ratings[team] = [1500, 0]  # Default rating is 1500 with 0 matches played
        return self.ratings[team]

    def expected_score(self, team_a, team_b):
        """Calculate the expected score for two teams based on their ratings."""
        rating_a = self.get_rating(team_a)[0]  # Get team A's rating
        rating_b = self.get_rating(team_b)[0]  # Get team B's rating
        expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))  # Expected score for team A
        expected_b = 1 - expected_a  # Expected score for team B
        return expected_a, expected_b

    def predict_match(self, team_a, team_b):
        """Predict the outcome probabilities of a match between two teams."""
        
        # Check if both teams exist in the ratings
        if team_a not in self.ratings or team_b not in self.ratings:
            print(f"One or both teams ({team_a}, {team_b}) do not exist in the database.")
            return None
        
        expected_a, expected_b = self.expected_score(team_a, team_b)
        
        # Calculate skill gap between the two teams
        skill_gap = abs(expected_a - expected_b)
        
        # Adjust draw probability based on the skill gap
        max_draw_prob = 0.3  # Maximum draw probability when teams are evenly matched
        min_draw_prob = 0.05  # Minimum draw probability when there's a large skill gap
        draw_prob = max_draw_prob - skill_gap * (max_draw_prob - min_draw_prob)
        
        # Adjust win probabilities with the dynamic draw probability
        win_a_prob = expected_a * (1 - draw_prob)
        win_b_prob = expected_b * (1 - draw_prob)
        
        return {"win_a": win_a_prob, "draw": draw_prob, "win_b": win_b_prob}


# Initialize the EloRatingSystem
elo_system = EloRatingSystem()

# Example: Predict the outcome of a match
match_prediction = elo_system.predict_match("Crystal Palace", "Man United")

# Only print predictions if both teams exist (i.e., match_prediction is not None)
if match_prediction:
    print("Predicted outcome probabilities:")
    print(f"Home team win: {match_prediction['win_a']:.2%}")
    print(f"Draw: {match_prediction['draw']:.2%}")
    print(f"Away team win: {match_prediction['win_b']:.2%}")
