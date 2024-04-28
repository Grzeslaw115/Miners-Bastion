import json

def load_scores():
    with open("scoreHistory.json", "r") as infile:
        return json.load(infile)

def save_score(score, player="Ty"):
    try:
        data = load_scores()
    except FileNotFoundError:
        data = []

    if player not in data:
        data[player] = score
    elif data[player] < score:
        data[player] = score

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    sorted_data_dict = {item[0]: item[1] for item in sorted_data}

    with open("scoreHistory.json", "w") as outfile:
        json.dump(sorted_data_dict, outfile, indent=4)