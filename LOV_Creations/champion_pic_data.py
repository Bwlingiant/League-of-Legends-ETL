import os
import json
import requests

# --- Load any one champion file to get the patch version ---
with open("ddragon_champions/Aatrox.json", "r", encoding="utf-8") as f:
    version = json.load(f)["version"]

# --- Directories ---
CHAMPION_DIR = "/home/bwlingiant/python_projects/League-of-Legends-ETL/LOV Creations/ddragon_champions"
ICON_DIR = "/home/bwlingiant/python_projects/League-of-Legends-ETL/LOV Creations/champion_icons"
os.makedirs(ICON_DIR, exist_ok=True)

# --- Download loop ---
for filename in os.listdir(CHAMPION_DIR):
    if not filename.endswith(".json"):
        continue

    with open(os.path.join(CHAMPION_DIR, filename), "r", encoding="utf-8") as f:
        data = json.load(f)
        champ = list(data["data"].values())[0]
        champ_id = champ["id"]

        icon_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champ_id}.png"
        icon_path = os.path.join(ICON_DIR, f"{champ_id}.png")

        if not os.path.exists(icon_path):
            response = requests.get(icon_url)
            if response.status_code == 200:
                with open(icon_path, "wb") as img_file:
                    img_file.write(response.content)
                print(f"✅ Downloaded: {champ_id}.png")
            else:
                print(f"⚠️ Failed to download: {champ_id} (HTTP {response.status_code})")
        else:
            print(f"🔁 Skipped (already exists): {champ_id}.png")

print("🎉 All champion icons downloaded.")
