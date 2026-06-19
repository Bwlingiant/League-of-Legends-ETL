import os
import requests
import json

# Get latest version
versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
version = requests.get(versions_url).json()[0]

# Get champion list
champion_index_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
champion_data = requests.get(champion_index_url).json()
champion_ids = champion_data["data"].keys()

# Create output directory
output_dir = "ddragon_champions"
os.makedirs(output_dir, exist_ok=True)

# Download each champion
for champ_id in champion_ids:
    champ_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champ_id}.json"
    r = requests.get(champ_url)
    if r.status_code == 200:
        with open(os.path.join(output_dir, f"{champ_id}.json"), "w", encoding="utf-8") as f:
            json.dump(r.json(), f, indent=2)
        print(f"Downloaded {champ_id}")
    else:
        print(f"Failed to download {champ_id} ({r.status_code})")
