import requests
import json
import time
import pandas as pd
from tqdm import tqdm

competitions_dict = {
    "Champions League": "CL",
    "Ligue 1": "FL1",
    "Bundesliga": "BL1",
    "Primera Division": "PD",
    "Primeira Liga": "PPL",
    "Serie A": "SA",
    "Premier League": "PL",
    "Eredivisie": "DED"
}

# Calculer le nombre total de requêtes
total_requests = len(competitions_dict) * (2025 - 2022)

# Lists to store team and player data
teams_list = []
players_list = []

with tqdm(total=total_requests, desc="Récupération des teams", unit="requête") as pbar:
    for competition, id_comp in competitions_dict.items():
        for year in range(2022, 2025):
            url = f"https://api.football-data.org/v4/competitions/{id_comp}/teams"
            params = {
                "season": year
            }
            headers = {
                'X-Auth-Token': '7ee3394168a140f98a511dd870124818'
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()

                for team in data.get('teams', []):
                    # Collecting team data
                    team_data = {
                        "team_id": team["id"],
                        "name": team["name"],
                        "country": team["area"]["name"],
                        "competition": id_comp,
                        "season": year,
                        "short_name": team["shortName"],
                        "tla": team["tla"],
                        "founded": team.get("founded"),
                        "venue": team.get("venue"),
                        "coach": team.get("coach", {}).get("name")
                    }
                    teams_list.append(team_data)
                    
                    # Collecting player data
                    for player in team.get('squad', []):
                        player_data = {
                            "player_id": player["id"],
                            "player_name": player["name"],
                            "position": player["position"],
                            "date_of_birth": player["dateOfBirth"],
                            "nationality": player["nationality"],
                            "team_id": team["id"],
                            "team_name": team["name"],
                            "competition": id_comp,
                            "season": year
                        }
                        players_list.append(player_data)
            else:
                print('Erreur:', response.text)

            # Update progress bar
            pbar.update(1)
            time.sleep(8)

# Create DataFrames for teams and players
teams_df = pd.DataFrame(teams_list)
players_df = pd.DataFrame(players_list)

#Enregistrer les données dans un fichier JSON
with open('outputs/all_teams.json', 'w', encoding='utf-16') as file:
    json.dump(teams_list, file, indent=4)

with open('outputs/all_players.json', 'w', encoding='utf-16') as file:
    json.dump(players_list, file, indent=4)


# Enregistrer les données dans un fichier CSV
teams_df.to_csv('outputs/all_teams.csv', index=False, encoding='utf-16', sep=';')
players_df.to_csv('outputs/all_players.csv', index=False, encoding='utf-16', sep=';')