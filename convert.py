import csv

def convert_match_result(home_team, away_team, home_goals, away_goals):
    """Convert match result into the desired format."""
    home_goals = int(home_goals)
    away_goals = int(away_goals)
    
    if home_goals > away_goals:
        return f'("{home_team}", "{away_team}", "win_a")'
    elif away_goals > home_goals:
        return f'("{home_team}", "{away_team}", "win_b")'
    else:
        return f'("{home_team}", "{away_team}", "draw")'

def process_match_file(file_path):
    """Process the match file and overwrite it with the formatted results."""
    formatted_results = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if there is one
        
        for row in reader:
            season, week, date, home_team, home_goals, away_goals, away_team, result = row
            formatted_result = convert_match_result(home_team, away_team, home_goals, away_goals)
            formatted_results.append(formatted_result)
    
    # Overwrite the original file with the formatted results
    with open(file_path, 'w') as file:
        for result in formatted_results:
            file.write(result + '\n')

# Path to your file
file_path = "matches.txt"

# Process the file
process_match_file(file_path)
