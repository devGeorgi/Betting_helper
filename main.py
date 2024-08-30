import os

def read_team_powers(filename="opta_rankings.txt"):
    """Read the teams and their powers from a file."""
    teams = {}
    with open(filename, "r") as file:
        for line in file:
            name, power = line.strip().split(",")
            teams[name.strip()] = float(power.strip())
    return teams

def calculate_probabilities(team1_power, team2_power):
    """Calculate the win, draw, and loss probabilities based on team powers."""
    total_power = team1_power + team2_power
    
    # Simplistic model for win, draw, and loss probabilities
    team1_win_probability = team1_power / total_power
    team2_win_probability = team2_power / total_power
    draw_probability = (1 - abs(team1_win_probability - team2_win_probability)) / 2
    
    return (team1_win_probability, draw_probability, team2_win_probability)

def get_percentiles(probabilities):
    """Convert probabilities to percentiles."""
    return [round(prob * 100, 2) for prob in probabilities]

def main():
    # Read the teams and their power ratings
    teams = read_team_powers()

    # Get the teams to compare
    team1 = input("Enter the name of the first team: ")
    team2 = input("Enter the name of the second team: ")

    # Ensure both teams are in the list
    if team1 not in teams or team2 not in teams:
        print("One or both teams not found in the list.")
        return

    # Calculate probabilities
    team1_power = teams[team1]
    team2_power = teams[team2]
    probabilities = calculate_probabilities(team1_power, team2_power)
    
    # Convert to percentiles
    percentiles = get_percentiles(probabilities)

    # Display the results
    print(f"Probability of {team1} winning: {percentiles[0]}%")
    print(f"Probability of a draw: {percentiles[1]}%")
    print(f"Probability of {team2} winning: {percentiles[2]}%")

if __name__ == "__main__":
    main()
