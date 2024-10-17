import numpy as np
from itertools import product

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
                        *team_parts, rating, matches_played = line.split()
                        team = ' '.join(team_parts)
                        self.ratings[team] = [float(rating), int(matches_played)]
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Please create it with team ratings.")

    def get_rating(self, team):
        """Get rating and matches played for a team."""
        if team not in self.ratings:
            self.ratings[team] = [1500, 0]
        return self.ratings[team]

    def expected_score(self, team_a, team_b):
        """Calculate the expected score for two teams based on their ratings."""
        rating_a = self.get_rating(team_a)[0]
        rating_b = self.get_rating(team_b)[0]
        expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        expected_b = 1 - expected_a
        return expected_a, expected_b

def load_recent_form(file_path):
    """Load recent form data from a file."""
    recent_form = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            recent_form_value = float(parts[0])  # The first value is the recent form value
            team_name = ' '.join(parts[1:-6])    # Join everything from the second element up to the last 6 as team name
            form_scores = list(map(float, parts[-6:]))  # The last 6 values are the form scores
            recent_form[team_name] = form_scores
    return recent_form


def predict_weighted_outcome(team_a, team_b, elo_system, recent_form, weight_elo, weight_form):
    """Predict the match outcome using a weighted combination of Elo rating and recent form."""
    
    # Get Elo rating-based expected score
    expected_a_elo, expected_b_elo = elo_system.expected_score(team_a, team_b)
    
    # Get recent form-based expected score
    form_a = np.mean(recent_form.get(team_a, [0] * 6))  # Average recent form score of team_a
    form_b = np.mean(recent_form.get(team_b, [0] * 6))  # Average recent form score of team_b
    total_form = form_a + form_b if form_a + form_b != 0 else 1  # Avoid division by zero
    
    expected_a_form = form_a / total_form
    expected_b_form = form_b / total_form
    
    # Combine Elo and form with specified weights
    expected_a = weight_elo * expected_a_elo + weight_form * expected_a_form
    expected_b = weight_elo * expected_b_elo + weight_form * expected_b_form
    
    return expected_a, expected_b

def evaluate_accuracy(elo_system, recent_form, match_results, weight_elo, weight_form):
    """Evaluate the accuracy of predictions with a given weighting."""
    correct_predictions = 0
    total_matches = 0

    for team_a, team_b, actual_result in match_results:
        expected_a, expected_b = predict_weighted_outcome(team_a, team_b, elo_system, recent_form, weight_elo, weight_form)

        predicted_result = "draw"
        if expected_a > expected_b:
            predicted_result = "win_a"
        elif expected_b > expected_a:
            predicted_result = "win_b"
        
        # Compare predicted result with actual result
        if predicted_result == actual_result:
            correct_predictions += 1
        
        total_matches += 1
    
    return correct_predictions / total_matches  # Return accuracy

def find_best_weights(elo_system, recent_form, match_results):
    """Find the best combination of Elo and form weights."""
    best_accuracy = 0
    best_weights = (0, 0)

    # Try different combinations of weights
    weight_combinations = product(np.arange(0, 1.1, 0.1), repeat=2)  # Try weights from 0.0 to 1.0
    
    for weight_elo, weight_form in weight_combinations:
        if weight_elo + weight_form == 1:  # Ensure that weights sum to 1
            accuracy = evaluate_accuracy(elo_system, recent_form, match_results, weight_elo, weight_form)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_weights = (weight_elo, weight_form)
    
    return best_weights, best_accuracy

# Main process
elo_system = EloRatingSystem(file_path="teams.txt")
recent_form = load_recent_form("recent_form.txt")

# Example match results (team_a, team_b, result)
match_results = [
    ("Crystal Palace", "Liverpool", "win_b"),
    ("Arsenal", "Southampton", "win_a"),
    ("Brentford", "Wolves", "win_a"),
    ("Man City", "Fulham", "win_a"),
    ("West Ham", "Ipswich", "win_a"),
    ("Leicester City", "Bournemouth", "win_a"),
    ("Everton", "Newcastle", "draw"),
    ("Aston Villa", "Man United", "draw"),
    ("Chelsea", "Nottingham Forest", "draw"),
    ("Brighton", "Tottenham", "win_a"),
]

# Find the best weights
best_weights, best_accuracy = find_best_weights(elo_system, recent_form, match_results)
print(f"Best weights (Elo, Form): {best_weights}")
print(f"Best accuracy: {best_accuracy:.2%}")
