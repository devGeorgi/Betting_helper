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

    # Find the relevant data
    rankings = soup.find_all('div', class_='rankings')  # Update class name based on the actual HTML structure

    # Open a text file to write the rankings
    with open('opta_rankings.txt', 'w') as file:
        for ranking in rankings:
            team_name = ranking.find('h2').text.strip()  # Update the tag/class as necessary
            points = ranking.find('span', class_='points').text.strip()  # Update class name based on the actual HTML structure
            # Write to the file
            file.write(f"{team_name} {points}\n")

    print("Rankings have been extracted and saved to opta_rankings.txt.")
else:
    print("Failed to retrieve the webpage.")
