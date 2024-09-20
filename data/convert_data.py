import csv

def convert_match_result(ht, at, FTR):
    """Convert match result into the desired format."""
    
    if FTR == "H":
        return f'("{ht}", "{at}", "win_a"),'
    elif FTR == "A":
        return f'("{ht}", "{at}", "win_b"),'
    else:
        return f'("{ht}", "{at}", "draw"),'

def process_match_file(file_path):
    """Process the match file and overwrite it with the formatted results."""
    formatted_results = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if there is one
        
        for row in reader:
            Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR,HS,AS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR,B365H,B365D,B365A,BWH,BWD,BWA,IWH,IWD,IWA,PSH,PSD,PSA,WHH,WHD,WHA,VCH,VCD,VCA,MaxH,MaxD,MaxA,AvgH,AvgD,AvgA,B365a,B365at,pa,pb,Ma,Mb,Avga,Avgb,AHh,B365AHH,B365AHA,PAHH,PAHA,MaxAHH,MaxAHA,AvgAHH,AvgAHA,B365CH,B365CD,B365CA,BWCH,BWCD,BWCA,IWCH,IWCD,IWCA,PSCH,PSCD,PSCA,WHCH,WHCD,WHCA,VCCH,VCCD,VCCA,MaxCH,MaxCD,MaxCA,AvgCH,AvgCD,AvgCA,B365ca,B365cb,PCa,PCb,MaxCa,MaxCb,AvgCa,AvgCb,AHCh,B365CAHH,B365CAHA,PCAHH,PCAHA,MaxCAHH,MaxCAHA,AvgCAHH,AvgCAHA = row
            formatted_result = convert_match_result(HomeTeam, AwayTeam, FTR)
            formatted_results.append(formatted_result)
    
    # Overwrite the original file with the formatted results
    with open(file_path, 'w') as file:
        for result in formatted_results:
            file.write(result + '\n')

# Path to your file
file_path = "Spanish data 2022.txt"

# Process the file
process_match_file(file_path)
