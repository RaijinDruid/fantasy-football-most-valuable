from requests import get
import json
from os import path


class Player():
    def __init__(self, name, points, id, history):
        self.name = name
        self.points = float(points)
        self.id = id
        self.cost = history['start_cost'] / \
            10 if history and 'start_cost' in history else 0.0
        self.ppm = round(float(
            points)/(history['start_cost']/10), 2) if history and 'start_cost' in history else 0.0

    def __repr__(self):
        return f"{self.name}| pts: {self.points} | ppm: {self.ppm} | cost: {self.cost}"
        # return self.name


def generate_data():
    if not path.exists('data.txt'):
        response_data = get(
            "https://fantasy.premierleague.com/api/bootstrap-static/").json()
        with open('data.txt', 'w') as outfile:
            json.dump(response_data['elements'], outfile, ensure_ascii=False)

        if not path.exists('player_history.txt'):
            player_history = {}
            for player in response_data['elements']:
                fetch_history = get(
                    f"https://fantasy.premierleague.com/api/element-summary/{player['id']}/").json()
                player_history[f"{player['first_name']} {player['second_name']}"] = fetch_history

            with open('player_history.txt', 'w') as outfile:
                json.dump(player_history, outfile, ensure_ascii=False)


def best_value_players():
    with open('data.txt') as player_file:
        with open('player_history.txt', encoding='utf-8',) as ph_file:
            players_data = json.load(player_file)
            player_history_data = json.load(ph_file)
            players = []
            for player in players_data:
                p_name = f"{player['first_name']} {player['second_name']}"
                history = [history for history in player_history_data[p_name]
                           ['history_past'] if history['season_name'] == "2019/20"]
                p = Player(p_name, player['total_points'],
                           player['id'], history[0] if history else None)
                players.append(p)

            return sorted(players, key=lambda p: p.ppm, reverse=True)


generate_data()
highest_players = best_value_players()
for player in highest_players[0:100]:
    print(player)
