class FormRatingSystem:
    def __init__(self, form_file="recent_form.txt", elo_file="teams.txt", form_decay_rate=20):
        """Initialize Form Rating system with paths to form and Elo files, and form decay rate."""
        self.form_file = form_file
        self.elo_file = elo_file
        self.form_decay_rate = form_decay_rate
        self.recent_form_history = {}  # Store last 6 match results for each team
        self.elo_ratings = {}
        self.load_form()
        self.load_elo()

    def load_form(self):
        """Load recent form history and final form score from a text file."""
        try:
            with open(self.form_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        # Split the first element (form score) and the rest (team name and history)
                        parts = line.split()
                        form_score = float(parts[0])  # Convert form score to float
                        
                        # Find where the team name ends and form history starts
                        for i in range(1, len(parts)):
                            try:
                                # If we can convert this part to a float, it's part of the form history
                                float(parts[i])
                                team_name_end = i
                                break
                            except ValueError:
                                continue
                        
                        # Extract team name and form history
                        team = ' '.join(parts[1:team_name_end])
                        form_history = [float(f) for f in parts[team_name_end:]]
                        
                        self.recent_form_history[team] = (form_score, form_history)
        except FileNotFoundError:
            print(f"File {self.form_file} not found. Starting with empty form data.")

    def save_form(self):
        """Save updated recent form history and form score to a text file."""
        with open(self.form_file, 'w') as file:
            for team, (form_score, form_history) in self.recent_form_history.items():
                # Save form score followed by the team name and form history
                form_str = ' '.join([f"{f:.2f}" for f in form_history])
                file.write(f"{form_score:.2f} {team} {form_str}\n")

    def load_elo(self):
        """Load Elo ratings from the Elo file."""
        try:
            with open(self.elo_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        *team_parts, rating, matches_played = line.split()
                        team = ' '.join(team_parts)
                        self.elo_ratings[team] = [float(rating), int(matches_played)]
        except FileNotFoundError:
            print(f"File {self.elo_file} not found. Please create it with team ratings.")

    def save_elo(self):
        """Save updated Elo ratings to the Elo file."""
        with open(self.elo_file, 'w') as file:
            for team, (rating, matches_played) in self.elo_ratings.items():
                file.write(f"{team} {int(rating)} {matches_played}\n")

    def get_team_data(self, team):
        """Get the recent form history and Elo rating for a team, initializing if not present."""
        if team not in self.recent_form_history:
            self.recent_form_history[team] = (0, [])  # Initialize form score to 0 and empty history
        if team not in self.elo_ratings:
            self.elo_ratings[team] = [1500, 0]  # Default Elo: 1500, 0 matches played
        return self.recent_form_history[team], self.elo_ratings[team]

    def calculate_total_recent_form(self, form_history):
        """Calculate the total recent form score based on the last 6 matches."""
        # Use only the last 6 matches, sum them up to calculate the total
        return sum(form_history[-6:])

    def update_form(self, team_a, team_b, result):
        """Update recent form for both teams based on match result and Elo difference."""
        (form_score_a, form_a), (elo_a, _) = self.get_team_data(team_a)
        (form_score_b, form_b), (elo_b, _) = self.get_team_data(team_b)

        # Calculate Elo difference
        elo_diff = (elo_b - elo_a) / 100  # Normalize Elo difference

        if result == "win_a":
            form_change_a = 10 + elo_diff  # Weaker team gains more for a win
            form_change_b = -10 - elo_diff  # Stronger team loses more for a loss
        elif result == "win_b":
            form_change_a = -10 + elo_diff  # Stronger team loses less
            form_change_b = 10 - elo_diff   # Weaker team gains more
        else:  # Draw case
            form_change_a = -5 + elo_diff  # Stronger team loses some points
            form_change_b = 5 - elo_diff   # Weaker team gains some points

        # Update form history for team_a (append the result and keep max 6)
        form_a.append(form_change_a)
        if len(form_a) > 6:
            form_a.pop(0)  # Remove the oldest match after 6 matches

        # Update form history for team_b (append the result and keep max 6)
        form_b.append(form_change_b)
        if len(form_b) > 6:
            form_b.pop(0)  # Remove the oldest match after 6 matches

        # Calculate total recent form for both teams
        total_form_a = self.calculate_total_recent_form(form_a)
        total_form_b = self.calculate_total_recent_form(form_b)

        # Update form score and history
        self.recent_form_history[team_a] = (total_form_a, form_a)
        self.recent_form_history[team_b] = (total_form_b, form_b)

    def update_elo(self, team_a, team_b, result):
        """Update Elo ratings based on match result using standard Elo formula."""
        elo_a, matches_a = self.get_team_data(team_a)[1]
        elo_b, matches_b = self.get_team_data(team_b)[1]

        # Set up result scoring: 1 for win, 0 for loss, 0.5 for draw
        if result == "win_a":
            score_a, score_b = 1, 0
        elif result == "win_b":
            score_a, score_b = 0, 1
        else:  # Draw case
            score_a, score_b = 0.5, 0.5

        # Elo calculation
        expected_a = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
        expected_b = 1 - expected_a
        k_factor = 30  # You can modify the K-factor as needed

        new_elo_a = elo_a + k_factor * (score_a - expected_a)
        new_elo_b = elo_b + k_factor * (score_b - expected_b)

        # Update Elo ratings and match counts
        self.elo_ratings[team_a] = [new_elo_a, matches_a + 1]
        self.elo_ratings[team_b] = [new_elo_b, matches_b + 1]

    def update_match(self, team_a, team_b, result):
        """Update both recent form and Elo after a match."""
        # Update recent form
        self.update_form(team_a, team_b, result)

        # Update Elo ratings
        self.update_elo(team_a, team_b, result)

        # Save the updated form and Elo data
        self.save_form()
        self.save_elo()

# Example usage
if __name__ == "__main__":
    form_system = FormRatingSystem()

    # Example match results
    match_results = [
        ("West Ham", "Chelsea", "win_b"),
    ]

    # Update form and Elo for each match
    for team_a, team_b, result in match_results:
        form_system.update_match(team_a, team_b, result)

    # Check updated recent form after processing match results
    print("Updated Recent Form:")
    for team, (total_form, form_history) in form_system.recent_form_history.items():
        print(f"{team}: Recent Form = {total_form:.2f}")
