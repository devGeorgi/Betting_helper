import requests
from bs4 import BeautifulSoup

# Open the file to save the results
with open('team_rankings.txt', 'w', encoding='utf-8') as f:
    
    # Loop through the pages (from 1 to 50)
    for page_num in range(1, 27):
        # Construct the URL for each page
        url = f'https://footballdatabase.com/ranking/europe/{page_num}'
        
        # Send a request to fetch the webpage content
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table containing the teams and scores
            table = soup.find('table', {'class': 'table table-hover'})
            
            if table:
                # Find all rows in the table body
                rows = table.find('tbody').find_all('tr')
                
                # Extract team names and scores from each row
                for row in rows:
                    try:
                        # Find the team name
                        team_div = row.find('div', class_='limittext')
                        if team_div:
                            team_name = team_div.text.strip()
                        else:
                            print("Team name not found in this row. Skipping...")
                            continue

                        # Find the score (assuming it's the 3rd column)
                        score_td = row.find_all('td')[2]
                        if score_td:
                            score = score_td.text.strip()
                        else:
                            print("Score not found in this row. Skipping...")
                            continue
                        
                        # Write the team and score to the file
                        f.write(f"{team_name}, {score}\n")
                    except Exception as e:
                        print(f"Error processing row: {e}")
                        continue
            else:
                print(f"Table not found on page {page_num}.")
        else:
            print(f"Failed to retrieve data from page {page_num}. Status code: {response.status_code}")
    
    print("Data saved successfully to team_rankings.txt")
