class InternationalEloRatingSystem:
    def __init__(self, k_factor=30, file_path="international_teams.txt"):
        self.k_factor = k_factor
        self.ratings = {}
        self.file_path = file_path
        self.load_ratings()

    def load_ratings(self):
        """Load international team ratings and matches played from a text file"""
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        # Split team name, rating, and matches played
                        *team_parts, rating, matches_played = line.split()  # Split into components
                        team = ' '.join(team_parts)  # Join team parts back together
                        self.ratings[team] = [float(rating), int(matches_played)]
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Please create it with international team ratings.")

    def save_ratings(self):
        """Save international team ratings and matches played to a text file"""
        with open(self.file_path, 'w') as file:
            for team, (rating, matches_played) in self.ratings.items():
                file.write(f"{team} {int(rating)} {matches_played}\n")

    def get_rating(self, team):
        """Get rating and matches played for an international team, initialize to 1500 and 0 if not present"""
        if team not in self.ratings:
            self.ratings[team] = [1500, 0]  # Default rating 1500, 0 matches played
        return self.ratings[team]

    def expected_score(self, team_a, team_b):
        """Calculate expected score for two international teams based on their ratings"""
        rating_a = self.get_rating(team_a)[0]  # Get only the rating (ignoring matches played)
        rating_b = self.get_rating(team_b)[0]
        expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        expected_b = 1 - expected_a
        return expected_a, expected_b

    def update_ratings(self, team_a, team_b, result):
        """Update Elo ratings and matches played for two international teams based on the match result"""
        expected_a, expected_b = self.expected_score(team_a, team_b)
        
        if result == "win_a":
            score_a, score_b = 1, 0
        elif result == "win_b":
            score_a, score_b = 0, 1
        elif result == "draw":
            score_a, score_b = 0.5, 0.5
        
        # Get ratings and match counts for both teams
        rating_a, matches_a = self.get_rating(team_a)
        rating_b, matches_b = self.get_rating(team_b)
        
        # Update ratings
        new_rating_a = rating_a + self.k_factor * (score_a - expected_a)
        new_rating_b = rating_b + self.k_factor * (score_b - expected_b)
        
        # Increment match counts
        matches_a += 1
        matches_b += 1
        
        # Update the ratings and match counts in the system
        self.ratings[team_a] = [new_rating_a, matches_a]
        self.ratings[team_b] = [new_rating_b, matches_b]
        
        # Save updated ratings and match counts to file
        self.save_ratings()

    def predict_match(self, team_a, team_b):
        """Predict probabilities for match outcome between two international teams"""
        
        # Check if both teams exist in the ratings
        if team_a not in self.ratings or team_b not in self.ratings:
            print(f"One or both teams ({team_a}, {team_b}) do not exist in the international database.")
            return None
        expected_a, expected_b = self.expected_score(team_a, team_b)
        
        # Calculate the absolute difference between the expected scores
        skill_gap = abs(expected_a - expected_b)
        
        # Adjust draw probability based on the skill gap
        max_draw_prob = 0.3  # Maximum probability of a draw when teams are evenly matched
        min_draw_prob = 0.05  # Minimum probability of a draw when there is a large skill gap
        
        # Linear interpolation between min and max draw probability
        draw_prob = max_draw_prob - skill_gap * (max_draw_prob - min_draw_prob)
        
        # Recalculate win probabilities with the new dynamic draw probability
        win_a_prob = expected_a * (1 - draw_prob)
        win_b_prob = expected_b * (1 - draw_prob)
        
        return {"win_a": win_a_prob, "draw": draw_prob, "win_b": win_b_prob}


# Initialize the InternationalEloRatingSystem
international_elo_system = InternationalEloRatingSystem()

# Example match results (international team_a, team_b, result)
international_match_results = [
    ("Petersburg", "Club Brugge KV", "win_b"),
("FK Dynamo Kyiv", "Juventus FC", "win_b"),
("Stade Rennais FC 1901", "FK Krasnodar", "draw"),
("SS Lazio", "Borussia Dortmund", "win_a"),
("FC Barcelona", "Ferencvárosi TC", "win_a"),
("Germain FC", "Manchester United FC", "win_b"),
("RB Leipzig", "Medipol Başakşehir FK", "win_a"),
("FC Red Bull Salzburg", "FK Lokomotiv Moskva", "draw"),
("Real Madrid CF", "FK Shakhtar Donetsk", "win_b"),
("FC Bayern München", "Club Atlético de Madrid", "win_a"),
("FC Internazionale Milano", "Borussia Mönchengladbach", "draw"),
("Manchester City FC", "FC Porto", "win_a"),
("PAE Olympiakos SFP", "Olympique de Marseille", "win_a"),
("AFC Ajax", "Liverpool FC", "win_b"),
("FC Midtjylland", "Atalanta BC", "win_b"),
("FK Lokomotiv Moskva", "FC Bayern München", "win_b"),
("Club Atlético de Madrid", "FC Red Bull Salzburg", "win_a"),
("Borussia Mönchengladbach", "Real Madrid CF", "draw"),
("Olympique de Marseille", "Manchester City FC", "win_b"),
("FC Porto", "PAE Olympiakos SFP", "win_a"),
("Liverpool FC", "FC Midtjylland", "win_a"),
("Atalanta BC", "AFC Ajax", "draw"),
("FK Krasnodar", "Chelsea FC", "win_b"),
("Medipol Başakşehir FK", "Paris Saint", "win_b"),
("Sevilla FC", "Stade Rennais FC 1901", "win_a"),
("Borussia Dortmund", "FK Zenit Sankt", "win_a"),
("Club Brugge KV", "SS Lazio", "draw"),
("Juventus FC", "FC Barcelona", "win_b"),
("Ferencvárosi TC", "FK Dynamo Kyiv", "draw"),
("Manchester United FC", "RB Leipzig", "win_a"),
("FK Lokomotiv Moskva", "Club Atlético de Madrid", "draw"),
("FK Shakhtar Donetsk", "Borussia Mönchengladbach", "win_b"),
("FC Red Bull Salzburg", "FC Bayern München", "win_b"),
("Real Madrid CF", "FC Internazionale Milano", "win_a"),
("Manchester City FC", "PAE Olympiakos SFP", "win_a"),
("FC Porto", "Olympique de Marseille", "win_a"),
("Atalanta BC", "Liverpool FC", "win_b"),
("FC Midtjylland", "AFC Ajax", "win_b"),
("Petersburg", "SS Lazio", "draw"),
("Medipol Başakşehir FK", "Manchester United FC", "win_a"),
("Chelsea FC", "Stade Rennais FC 1901", "win_a"),
("Sevilla FC", "FK Krasnodar", "win_a"),
("Club Brugge KV", "Borussia Dortmund", "win_b"),
("FC Barcelona", "FK Dynamo Kyiv", "win_a"),
("Ferencvárosi TC", "Juventus FC", "win_b"),
("RB Leipzig", "Paris Saint", "win_a"),
("Stade Rennais FC 1901", "Chelsea FC", "win_b"),
("FK Krasnodar", "Sevilla FC", "win_b"),
("Borussia Dortmund", "Club Brugge KV", "win_a"),
("SS Lazio", "FK Zenit Sankt", "win_a"),
("Juventus FC", "Ferencvárosi TC", "win_a"),
("FK Dynamo Kyiv", "FC Barcelona", "win_b"),
("Manchester United FC", "Medipol Başakşehir FK", "win_a"),
("Germain FC", "RB Leipzig", "win_a"),
("Borussia Mönchengladbach", "FK Shakhtar Donetsk", "win_a"),
("PAE Olympiakos SFP", "Manchester City FC", "win_b"),
("FC Bayern München", "FC Red Bull Salzburg", "win_a"),
("FC Internazionale Milano", "Real Madrid CF", "win_b"),
("Olympique de Marseille", "FC Porto", "win_b"),
("Liverpool FC", "Atalanta BC", "win_b"),
("AFC Ajax", "FC Midtjylland", "win_a"),
("FK Lokomotiv Moskva", "FC Red Bull Salzburg", "win_b"),
("FK Shakhtar Donetsk", "Real Madrid CF", "win_a"),
("Club Atlético de Madrid", "FC Bayern München", "draw"),
("Borussia Mönchengladbach", "FC Internazionale Milano", "win_b"),
("Olympique de Marseille", "PAE Olympiakos SFP", "win_a"),
("Liverpool FC", "AFC Ajax", "win_a"),
("Atalanta BC", "FC Midtjylland", "draw"),
("FK Krasnodar", "Stade Rennais FC 1901", "win_a"),
("Medipol Başakşehir FK", "RB Leipzig", "win_b"),
("Sevilla FC", "Chelsea FC", "win_b"),
("Borussia Dortmund", "SS Lazio", "draw"),
("Club Brugge KV", "FK Zenit Sankt", "win_a"),
("Juventus FC", "FK Dynamo Kyiv", "win_a"),
("Ferencvárosi TC", "FC Barcelona", "win_b"),
("Manchester United FC", "Paris Saint", "win_b"),
("Petersburg", "Borussia Dortmund", "win_b"),
("SS Lazio", "Club Brugge KV", "draw"),
("Chelsea FC", "FK Krasnodar", "draw"),
("Stade Rennais FC 1901", "Sevilla FC", "win_b"),
("FC Barcelona", "Juventus FC", "win_b"),
("FK Dynamo Kyiv", "Ferencvárosi TC", "win_a"),
("RB Leipzig", "Manchester United FC", "win_a"),
("AFC Ajax", "Atalanta BC", "win_b"),
("FC Midtjylland", "Liverpool FC", "draw"),
("Germain FC", "Medipol Başakşehir FK", "win_a"),
("FC Bayern München", "FK Lokomotiv Moskva", "win_a"),
("FC Red Bull Salzburg", "Club Atlético de Madrid", "win_b"),
("Real Madrid CF", "Borussia Mönchengladbach", "win_a"),
("Manchester City FC", "Olympique de Marseille", "win_a"),
("PAE Olympiakos SFP", "FC Porto", "win_b"),
("RB Leipzig", "Liverpool FC", "win_b"),
("FC Barcelona", "Paris Saint", "win_b"),
("FC Porto", "Juventus FC", "win_a"),
("Sevilla FC", "Borussia Dortmund", "win_b"),
("SS Lazio", "FC Bayern München", "win_b"),
("Club Atlético de Madrid", "Chelsea FC", "win_b"),
("Borussia Mönchengladbach", "Manchester City FC", "win_b"),
("Atalanta BC", "Real Madrid CF", "win_b"),
("Borussia Dortmund", "Sevilla FC", "draw"),
("Liverpool FC", "RB Leipzig", "win_a"),
("Germain FC", "FC Barcelona", "draw"),
("Manchester City FC", "Borussia Mönchengladbach", "win_a"),
("Real Madrid CF", "Atalanta BC", "win_a"),
("FC Bayern München", "SS Lazio", "win_a"),
("Chelsea FC", "Club Atlético de Madrid", "win_a"),
("Manchester City FC", "Borussia Dortmund", "win_a"),
("Real Madrid CF", "Liverpool FC", "win_a"),
("FC Porto", "Chelsea FC", "win_b"),
("FC Bayern München", "Paris Saint", "win_b"),
("Chelsea FC", "FC Porto", "win_b"),
("Germain FC", "FC Bayern München", "win_b"),
("Borussia Dortmund", "Manchester City FC", "win_b"),
("Real Madrid CF", "Chelsea FC", "draw"),
("Germain FC", "Manchester City FC", "win_b"),
("Manchester City FC", "Paris Saint", "win_a"),
("Chelsea FC", "Real Madrid CF", "win_a"),
("Manchester City FC", "Chelsea FC", "win_b"),

]

# Update Elo ratings for each international match
for team_a, team_b, result in international_match_results:
    international_elo_system.update_ratings(team_a, team_b, result)

# Check updated international ratings after processing all match results
print("Updated International Elo Ratings:")
for team, (rating, matches) in international_elo_system.ratings.items():
    print(f"{team}: {rating} after {matches} matches")

# # Predict the outcome of an international match 
# international_match_prediction = international_elo_system.predict_match("Brazil", "Germany")

# # Only print predictions if both teams exist (i.e., match_prediction is not None)
# if international_match_prediction:
#     print(f"Predicted international match outcome probabilities:")
#     print(f"Home team win: {international_match_prediction['win_a']:.2%}")
#     print(f"Draw: {international_match_prediction['draw']:.2%}")
#     print(f"Away team win: {international_match_prediction['win_b']:.2%}")
# else:
#     print("International match prediction could not be performed due to missing team(s).")
