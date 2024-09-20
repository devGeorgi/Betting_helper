# Define the function to sort teams by their scores and save back to the file
def sort_teams_by_score(file_path):
    # Open the file and read the content
    with open(file_path, 'r') as file:
        data = file.readlines()
    
    # Convert the input data into a list of tuples (team, score)
    team_scores = [(line.rsplit(" ", 1)[0], int(line.rsplit(" ", 1)[1])) for line in data if line.strip()]
    
    # Sort by score in descending order
    sorted_teams = sorted(team_scores, key=lambda x: x[1], reverse=True)
    
    # Write the sorted data back to the file
    with open(file_path, 'w') as file:
        for team, score in sorted_teams:
            file.write(f"{team} {score}\n")

# Specify the file path
file_path = 'teams_sorted.txt'

# Call the function to sort and update the file
sort_teams_by_score(file_path)

print(f"Teams sorted by score and saved to {file_path}.")
