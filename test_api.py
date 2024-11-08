import requests
import json
from pprint import pprint

id_comp = "CL"
year = 2022
url = f"https://api.football-data.org/v4/competitions/{
    id_comp}/teams"
url
params = {
    "season": year
}
headers = {
    'X-Auth-Token': '7ee3394168a140f98a511dd870124818'
}

response = requests.get(url, headers=headers, params=params)

#afficher l'url de la requête
print(response.url)

#afficher le code de statut de la requête
print(response.status_code)