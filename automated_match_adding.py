from main import EloRatingSystem

def process_matches_in_batches(elo_system, match_file, batch_size=10):
    with open(match_file, 'r') as file:
        lines = file.readlines()

    for batch_number in range(0, len(lines), batch_size):
        batch = lines[batch_number:batch_number + batch_size]
        process_batch(elo_system, batch)

def process_batch(elo_system, batch):
    for line_number, line in enumerate(batch):
        line = line.strip().rstrip(',')
        if line.startswith("(") and line.endswith(")"):
            line = line[1:-1].replace('"', '').replace("'", "")
            try:
                team_a, team_b, result = [x.strip() for x in line.split(',')]
                print(f"Processing match: {team_a} vs {team_b} - Result: {result}")
                elo_system.update_ratings(team_a, team_b, result)
            except ValueError:
                print(f"Invalid format in line {line_number + 1}: {line}")
        else:
            print(f"Skipping invalid line format: {line}")

if __name__ == "__main__":
    match_file = "data/Spanish data 2023.txt"
    elo_system = EloRatingSystem()

    # Run batch processing with a batch size of 10
    process_matches_in_batches(elo_system, match_file, batch_size=1)

    print("Batch processing complete.")
