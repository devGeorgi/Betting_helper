# Define the function to sort teams by their rating and save to a new file
def sort_teams_by_rating(input_file_path, output_file_path):
    # Open the input file and read the content
    with open(input_file_path, 'r') as file:
        data = file.readlines()
    
    # Convert the input data into a list of tuples (team, rating, matches_played)
    team_data = [(line.rsplit(" ", 2)[0], float(line.rsplit(" ", 2)[1]), int(line.rsplit(" ", 2)[2])) for line in data if line.strip()]
    
    # Sort by rating in descending order
    sorted_teams = sorted(team_data, key=lambda x: x[1], reverse=True)
    
    # Write the sorted data to the output file
    with open(output_file_path, 'w') as file:
        for team, rating, matches_played in sorted_teams:
            file.write(f"{team} {int(rating)} {matches_played}\n")

# Specify the file paths
input_file_path = 'domestic_teams.txt'  # Input file (original file with team data)
output_file_path = 'domestic_teams_sorted.txt'  # Output file (sorted version)

# Call the function to sort by rating and update the output file
sort_teams_by_rating(input_file_path, output_file_path)

print(f"Teams sorted by rating and saved to {output_file_path}.")
