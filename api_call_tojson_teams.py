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

# Liste pour stocker tous les matchs
all_teams = []

# Utiliser tqdm pour la barre d'avancement
with tqdm(total=total_requests, desc="Récupération des teams", unit="requête") as pbar:
    for competition, id_comp in competitions_dict.items():
        for year in range(2022, 2025):
            url = f"https://api.football-data.org/v4/competitions/{
                id_comp}/teams"
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
                team_data = {
                    "id": team["id"],
                    "name": team["name"],
                    'pays': team['area']['name'],
                    "short_name": team["shortName"],
                    "tla": team["tla"],
                    "founded": team.get("founded"),
                    "venue": team.get("venue"),
                    "coach": team.get("coach", {}).get("name"),
                    "players": []
                }
                
                for player in team.get('squad', []):
                    player_data = {
                        "id": player["id"],
                        "name": player["name"],
                        "position": player["position"],
                        "date_of_birth": player["dateOfBirth"],
                        "nationality": player["nationality"]
                    }
                    team_data["players"].append(player_data)
                
                all_teams.append(team_data)
            else:
                print('Erreur:', response.text)

            # Mettre à jour la barre d'avancement
            pbar.update(1)
            time.sleep(8)

df = pd.DataFrame(all_teams)
print(df)

with open('all_teams.json', 'w', encoding='utf-8') as file:
    json.dump(all_teams, file, indent=4)
