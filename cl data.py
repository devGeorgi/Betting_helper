import re

def determine_result(goals_a, goals_b):
    """Determine match result based on goals."""
    if goals_a > goals_b:
        return "win_a"
    elif goals_b > goals_a:
        return "win_b"
    else:
        return "draw"

def process_cl_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    formatted_matches = []
    
    for line in lines:
        # Only process lines that contain match data in the expected format with score
        match = re.search(r'([\w\s\'\.]+)\s+(\d+)-(\d+)\s+\([\d\s:\-]+\)\s+([\w\s\'\.]+)', line)
        if match:
            team_a = match.group(1).strip()
            goals_a = int(match.group(2))
            goals_b = int(match.group(3))
            team_b = match.group(4).strip()

            # Determine the result of the match
            result = determine_result(goals_a, goals_b)
            
            # Format the match result
            formatted_matches.append(f'("{team_a}", "{team_b}", "{result}")')
        else:
            # Skip non-match lines
            continue

    # Save the formatted results to a new file
    with open("formatted_cl_results.txt", 'w', encoding='utf-8') as output_file:
        for match in formatted_matches:
            output_file.write(match + '\n')

    print(f"Processed {len(formatted_matches)} matches. Check 'formatted_cl_results.txt' for results.")

# Path to your file
file_path = "cl.txt"

# Process the Champions League data
process_cl_data(file_path)
