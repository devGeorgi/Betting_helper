import pandas as pd

# Step 1: Read team rankings from the text file
def load_team_rankings(file_path):
    team_scores = {}
    with open(file_path, 'r') as file:
        for line in file:
            team, score = line.strip().split(', ')
            team_scores[team] = int(score)  # Store team name and its score as integer
    return team_scores

# Test loading rankings
team_scores = load_team_rankings('team_rankings.txt')
print(team_scores)
