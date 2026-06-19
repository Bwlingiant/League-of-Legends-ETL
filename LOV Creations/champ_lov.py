import os
import json
import psycopg
import constants as con
import sys

print(os.curdir)
# print('Fucking work')
# sys.exit()

# --- Database connection (use env vars or refactor later) ---
conn = psycopg.connect(con.db_connection)




# --- Champion directory ---
DATA_DIR = '/home/bwlingiant/python_projects/League-of-Legends-ETL/LOV Creations/ddragon_champions'

# --- SQL Insert Query ---
INSERT_QUERY = """
INSERT INTO "lollov".champions (
    id, key, name, title, blurb,
    info_attack, info_defense, info_magic, info_difficulty,
    tags, partype,
    hp, hpperlevel, mp, mpperlevel, movespeed,
    armor, armorperlevel, spellblock, spellblockperlevel,
    attackrange, hpregen, hpregenperlevel, mpregen, mpregenperlevel,
    crit, critperlevel, attackdamage, attackdamageperlevel,
    attackspeedperlevel, attackspeed, patch_version
)
VALUES (
    %(id)s, %(key)s, %(name)s, %(title)s, %(blurb)s,
    %(info_attack)s, %(info_defense)s, %(info_magic)s, %(info_difficulty)s,
    %(tags)s, %(partype)s,
    %(hp)s, %(hpperlevel)s, %(mp)s, %(mpperlevel)s, %(movespeed)s,
    %(armor)s, %(armorperlevel)s, %(spellblock)s, %(spellblockperlevel)s,
    %(attackrange)s, %(hpregen)s, %(hpregenperlevel)s, %(mpregen)s, %(mpregenperlevel)s,
    %(crit)s, %(critperlevel)s, %(attackdamage)s, %(attackdamageperlevel)s,
    %(attackspeedperlevel)s, %(attackspeed)s, %(patch_version)s
)
ON CONFLICT (id) DO UPDATE SET
    key = EXCLUDED.key,
    name = EXCLUDED.name,
    title = EXCLUDED.title,
    blurb = EXCLUDED.blurb,
    info_attack = EXCLUDED.info_attack,
    info_defense = EXCLUDED.info_defense,
    info_magic = EXCLUDED.info_magic,
    info_difficulty = EXCLUDED.info_difficulty,
    tags = EXCLUDED.tags,
    partype = EXCLUDED.partype,
    hp = EXCLUDED.hp,
    hpperlevel = EXCLUDED.hpperlevel,
    mp = EXCLUDED.mp,
    mpperlevel = EXCLUDED.mpperlevel,
    movespeed = EXCLUDED.movespeed,
    armor = EXCLUDED.armor,
    armorperlevel = EXCLUDED.armorperlevel,
    spellblock = EXCLUDED.spellblock,
    spellblockperlevel = EXCLUDED.spellblockperlevel,
    attackrange = EXCLUDED.attackrange,
    hpregen = EXCLUDED.hpregen,
    hpregenperlevel = EXCLUDED.hpregenperlevel,
    mpregen = EXCLUDED.mpregen,
    mpregenperlevel = EXCLUDED.mpregenperlevel,
    crit = EXCLUDED.crit,
    critperlevel = EXCLUDED.critperlevel,
    attackdamage = EXCLUDED.attackdamage,
    attackdamageperlevel = EXCLUDED.attackdamageperlevel,
    attackspeedperlevel = EXCLUDED.attackspeedperlevel,
    attackspeed = EXCLUDED.attackspeed,
    patch_version = EXCLUDED.patch_version;
"""

# --- Parse and insert data ---
with conn.cursor() as cur:
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                raw = json.load(f)
                patch_version = raw["version"]
                champ_data = list(raw["data"].values())[0]  # Unwrap single champ

                payload = {
                    "id": champ_data["id"],
                    "patch_version": patch_version,
                    "key": champ_data["key"],
                    "name": champ_data["name"],
                    "title": champ_data["title"],
                    "blurb": champ_data["blurb"],
                    "info_attack": champ_data["info"]["attack"],
                    "info_defense": champ_data["info"]["defense"],
                    "info_magic": champ_data["info"]["magic"],
                    "info_difficulty": champ_data["info"]["difficulty"],
                    "tags": champ_data["tags"],
                    "partype": champ_data["partype"],
                    **champ_data["stats"]  # Includes all stat fields
                }

                cur.execute(INSERT_QUERY, payload)
                print(f"Inserted/Updated: {champ_data['id']}")

print("✅ All champions processed.")
conn.commit()
conn.close()
