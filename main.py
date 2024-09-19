class EloRatingSystem:
    def __init__(self, k_factor=30, file_path="teams.txt"):
        self.k_factor = k_factor
        self.ratings = {}
        self.file_path = file_path
        self.load_ratings()

    def load_ratings(self):
        """Load team ratings from a text file"""
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    # Split team name and rating correctly
                    team, rating = line.rsplit(' ', 1)
                    self.ratings[team] = float(rating)
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Please create it with team ratings.")

    def save_ratings(self):
        """Save team ratings to a text file"""
        with open(self.file_path, 'w') as file:
            for team, rating in self.ratings.items():
                file.write(f"{team} {int(rating)}\n")

    def get_rating(self, team):
        """Get rating for a team, initialize to 1500 if not present"""
        if team not in self.ratings:
            self.ratings[team] = 1500  # Default rating for new teams
        return self.ratings[team]

    def expected_score(self, team_a, team_b):
        """Calculate expected score for two teams based on their ratings"""
        rating_a = self.get_rating(team_a)
        rating_b = self.get_rating(team_b)
        expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        expected_b = 1 - expected_a
        return expected_a, expected_b

    def update_ratings(self, team_a, team_b, result):
        """Update Elo ratings for two teams based on the match result"""
        expected_a, expected_b = self.expected_score(team_a, team_b)
        
        if result == "win_a":
            score_a, score_b = 1, 0
        elif result == "win_b":
            score_a, score_b = 0, 1
        elif result == "draw":
            score_a, score_b = 0.5, 0.5
        
        rating_a = self.get_rating(team_a)
        rating_b = self.get_rating(team_b)
        
        # Update ratings
        new_rating_a = rating_a + self.k_factor * (score_a - expected_a)
        new_rating_b = rating_b + self.k_factor * (score_b - expected_b)
        
        self.ratings[team_a] = new_rating_a
        self.ratings[team_b] = new_rating_b
        
        # Save updated ratings to file
        self.save_ratings()

    def predict_match(self, team_a, team_b):
        """Predict probabilities for match outcome"""
        expected_a, expected_b = self.expected_score(team_a, team_b)
        
        draw_prob = 0.1  # Adjust based on real-world data if needed
        win_a_prob = expected_a * (1 - draw_prob)
        win_b_prob = expected_b * (1 - draw_prob)
        
        return {"win_a": win_a_prob, "draw": draw_prob, "win_b": win_b_prob}

# Initialize the EloRatingSystem
elo_system = EloRatingSystem()

# # List of match results (team_a, team_b, result)
# match_results = [
#     ("Fulham", "Arsenal", "win_b"),
# ]

# # Update Elo ratings for each match
# for team_a, team_b, result in match_results:
#     elo_system.update_ratings(team_a, team_b, result)

# # Check updated ratings after processing all match results
# print("Updated Premier League Elo Ratings:")
# for team, rating in elo_system.ratings.items():
#     print(f"{team}: {rating}")

# Predict the outcome of a match 
match_prediction = elo_system.predict_match("Man City", "Liverpool")

# Print the predicted probabilities for each outcome
print(f"Predicted outcome probabilities :")
print(f"Home team win: {match_prediction['win_a']:.2%}")
print(f"Draw: {match_prediction['draw']:.2%}")
print(f"Away team win: {match_prediction['win_b']:.2%}")