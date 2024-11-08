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

# Liste pour stocker tous les matchs
all_matches = []

# Calculer le nombre total de requêtes
total_requests = len(competitions_dict) * (2025 - 2022)

# Utiliser tqdm pour la barre d'avancement
with tqdm(total=total_requests, desc="Récupération des matchs", unit="requête") as pbar:
    for competition, id_comp in competitions_dict.items():
        for year in range(2022, 2025):
            url = f"https://api.football-data.org/v4/competitions/{
                id_comp}/matches"
            params = {
                "season": year
            }
            headers = {
                'X-Auth-Token': '7ee3394168a140f98a511dd870124818'
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                for match in data.get('matches', []):
                    match_data = {
                        "date": match["utcDate"][:11],
                        "id": match["id"],
                        'pays': match['area']['name'],
                        'competition': match['competition']['name'],
                        'eq_dom': match['homeTeam']['name'],
                        'eq_ext': match['awayTeam']['name'],
                        'score_mt_dom': match['score']['halfTime']['home'],
                        'score_mt_ext': match['score']['halfTime']['away'],
                        'score_fin_dom': match['score']['fullTime']['home'],
                        'score_fin_ext': match['score']['fullTime']['away']
                    }
                    all_matches.append(match_data)
            else:
                print('Erreur:', response.text)

            # Mettre à jour la barre d'avancement
            pbar.update(1)
            time.sleep(8)

df = pd.DataFrame(all_matches)
print(df)

with open('all_matches.json', 'w', encoding='utf-8') as file:
    json.dump(all_matches, file, indent=4)
