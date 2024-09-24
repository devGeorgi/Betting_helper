def sort_teams_by_form(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Split and store each team's recent form data
    team_data = []
    for line in lines:
        line = line.strip()
        if line:
            form_score, *team_info = line.split()
            form_score = float(form_score)
            team_data.append((form_score, ' '.join(team_info)))

    # Sort the data by the recent form score in descending order
    sorted_data = sorted(team_data, key=lambda x: x[0], reverse=True)

    # Write sorted data to the output file
    with open(output_file, 'w') as file:
        for form_score, team_info in sorted_data:
            file.write(f"{form_score:.2f} {team_info}\n")

    print(f"Teams sorted by recent form and saved to {output_file}")


input_file = "recent_form.txt"  # The file with unsorted data
output_file = "recent_form_sorted.txt"  # The file to store sorted data
sort_teams_by_form(input_file, output_file)
