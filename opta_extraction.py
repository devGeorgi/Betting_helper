import requests
from bs4 import BeautifulSoup

# URL of the Opta Power Rankings page
url = "https://theanalyst.com/2024/08/who-are-the-best-football-team-in-the-world-opta-power-rankings"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to store the team names and points
    team_rankings = []

    # Find all the elements that contain the rankings
    ranking_items = soup.find_all('div', class_='rankings__team')

    # Loop through each item and extract the team name and points
    for item in ranking_items:
        team_name = item.find('div', class_='rankings__team-name').text.strip()
        points = item.find('div', class_='rankings__team-score').text.strip()
        team_rankings.append(f"{team_name} {points}")

    # Write the extracted data to a text file
    with open('opta_rankings.txt', 'w') as file:
        for team in team_rankings:
            file.write(f"{team}\n")

    print("Rankings have been extracted and saved to opta_rankings.txt.")
else:
    print("Failed to retrieve the webpage.")
