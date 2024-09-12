import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Read team rankings from the text file
def load_team_rankings(file_path):
    team_scores = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            team, score = line.strip().split(', ')
            team_scores[team] = int(score)  # Store team name and its score as integer
    return team_scores

# Step 2: Calculate the score difference between two teams
def calculate_score_diff(team1, team2, team_scores):
    score1 = team_scores.get(team1, 0)  # If team not found, assume score 0
    score2 = team_scores.get(team2, 0)
    return score1 - score2  # Return score difference

# Step 3: Prepare data for training
def prepare_training_data(matches, team_scores):
    X = []  # Features (score differences)
    y = []  # Target (match outcome: w1, d, w2)

    for match in matches:
        team1, team2 = match['team1'], match['team2']
        score_diff = calculate_score_diff(team1, team2, team_scores)

        X.append([score_diff])  # The feature is score difference
        y.append(match['result'])  # The target is the result (w1, d, w2)

    # Convert to DataFrame for convenience
    X = pd.DataFrame(X, columns=['score_diff'])
    return X, y

# Step 4: Train the classification model
def train_model(X, y):
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Use a Random Forest Classifier for classification
    model = RandomForestClassifier()

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    return model

# Main function to run the process
def main():
    # Load team rankings from file
    team_scores = load_team_rankings('team_rankings.txt')

    # Example matches with teams and results (w1 = team1 wins, d = draw, w2 = team2 wins)
    matches = [
        {'team1': 'Manchester United', 'team2': 'Fulham', 'result': 'w1'},
        {'team1': 'Ipswich', 'team2': 'Liverpool', 'result': 'w2'},
        {'team1': 'Arsenal', 'team2': 'Wolves', 'result': 'w1'},
        {'team1': 'Everton', 'team2': 'Brighton', 'result': 'w2'},
        {'team1': 'Newcastle', 'team2': 'Southampton', 'result': 'w1'},
        {'team1': 'Nottingham Forest', 'team2': 'Bournemouth', 'result': 'd'},
        {'team1': 'West Ham', 'team2': 'Aston Villa', 'result': 'w2'},
        {'team1': 'Brentford', 'team2': 'Crystal Palace', 'result': 'w1'},
        {'team1': 'Chelsea', 'team2': 'Manchester City', 'result': 'w2'},
        {'team1': 'Leicester City', 'team2': 'Tottenham', 'result': 'd'},
    ]

    # Prepare data for training
    X, y = prepare_training_data(matches, team_scores)

    # Train the model
    model = train_model(X, y)

# Run the main function
if __name__ == '__main__':
    main()
