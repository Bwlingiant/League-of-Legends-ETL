import constants
import psycopg
import polars as pl
import gspread
import time
from riotwatcher import LolWatcher, ApiError, RiotWatcher

API_KEY = constants.API_KEY_SERVICE
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)
lol_region = 'na1'

db_pass = constants.db_password
db_ip = constants.db_ip

db_connection = f'dbname = yrden user=postgres password={db_pass} host={db_ip}'

conn = psycopg.connect(db_connection)

cur = conn.cursor()
print('Connection Established')

data_query = '''SELECT * FROM "yrden".lol_game_data
WHERE game_id in 
(select game_id
from "yrden".lol_game_data
where 1=1
and queue_id in (440, 700)
group by game_id
having count(game_id) = 10)
ORDER BY GAME_PATCH DESC, GAME_ID, TEAMID, CASE WHEN LANE = 'TOP' THEN 1 WHEN LANE = 'JUNGLE' THEN 2 WHEN LANE = 'MIDDLE' THEN 3 WHEN LANE = 'BOTTOM' THEN 4 ELSE 5 END
;'''
with conn.cursor() as curs:
    curs.execute(data_query)

    col_names = [desc[0] for desc in curs.description]
    # uri = f'postgresql://postgres:{db_pass}@{db_ip}:5432/yrden'
    # df = pl.read_database_uri(query=data_query, uri=uri)
    rows = curs.fetchall()
    df = pl.DataFrame(rows, schema=col_names, orient='row')

# df.write_csv('flex_data.csv')

conn.close()
print('Connection closed.')

# print(df.schema)
# print(df['teamid'])

print(df.schema)

df = df.with_columns(
        [pl.when(pl.col('win')==True)
        .then(pl.lit("W"))
        .otherwise(pl.lit("L"))
        .alias("win"),
        pl.when(pl.col('teamid') ==100).then(pl.lit("Blue")).otherwise(pl.lit("Red")).alias("teamid"),
        pl.when(pl.col("deaths") == 0)
        .then(pl.col('kills') + pl.col('assists'))
        .otherwise((pl.col('kills')+pl.col('assists'))/pl.col('deaths'))
        .alias("KDA"),
        (pl.col('gold_earned') / (pl.col('game_duration')/60)).alias('Gold Per Minute'),
        ((pl.col('minions_killed') + pl.col('neutral_monsters_killed'))/ (pl.col('game_duration')/60)).alias('CS Per Minute'),
        pl.when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[0])
        .then(pl.lit('YRDEN'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[1])
        .then(pl.lit('YRDEN'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[2])
        .then(pl.lit('YRDEN'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[3])
        .then(pl.lit('YRDEN'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[4])
        .then(pl.lit('YRDEN'))
        .otherwise(pl.lit("Other"))
        .alias('Yrden Flag'),
        pl.when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[0])
        .then(pl.lit('TOP'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[1])
        .then(pl.lit('JUNGLE'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[2])
        .then(pl.lit('MIDDLE'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[3])
        .then(pl.lit('BOTTOM'))
        .when(pl.col('riot_puuid') == constants.yrden_lol_team_puuids[4])
        .then(pl.lit('UTILITY'))
        .otherwise(pl.col('lane'))
        .alias('lane')
        ]
    )

                    #   pl.when(pl.col('teamid') ==100).then("Blue").otherwise("Red").alias("teamid_calc")
# print(df["win"].unique())

df = df.select([pl.col('teamid'), pl.col('Yrden Flag'), pl.col('riot_id'), pl.col('champion_name'), pl.col('lane'), pl.col('win'), pl.col('kills'), pl.col('deaths'), pl.col('assists'), pl.col('KDA'),
                pl.col('game_duration'), pl.col('minions_killed'), pl.col('neutral_monsters_killed'), pl.col('CS Per Minute'), pl.col('gold_earned'), pl.col('Gold Per Minute'),
                pl.col('champion_damage'), pl.col('objective_damage'), pl.col('damage_healed'), pl.col('vision_score'), pl.col('summoner1_id'), pl.col('summoner1_casts'),
                pl.col('summoner2_id'), pl.col('summoner2_casts'),
                pl.col('control_wards_purchased'), pl.col('wards_killed'), pl.col('wards_placed'),
                pl.col('double_kills'), pl.col('triple_kills'), pl.col('quadra_kills'), pl.col('penta_kills'),
                pl.col('game_patch'), pl.col('game_id'), pl.col('keystone_rune_code'), pl.col('keystone_rune_var1'), 
                pl.col('keystone_rune_var2'), pl.col('keystone_rune_var3'), pl.col('primary_rune_code1'), 
                pl.col('primary_rune_code2'), pl.col('primary_rune_code3'), pl.col('primary_rune1_var1'),
                pl.col('primary_rune1_var2'), pl.col('primary_rune1_var3'), pl.col('primary_rune2_var1'), 
                pl.col('primary_rune2_var2'), pl.col('primary_rune3_var3'), pl.col('primary_rune2_var3'),
                pl.col('primary_rune3_var1'), pl.col('primary_rune3_var2'), 
                pl.col('secondary_rune_code1'), pl.col('secondary_rune_code2'), pl.col('secondary_rune1_var1'), pl.col('secondary_rune1_var2'),
                pl.col('secondary_rune1_var3'), pl.col('secondary_rune2_var1'), pl.col('secondary_rune2_var2'), pl.col('secondary_rune2_var3'),
                pl.col('largest_critical_strike'), pl.col('nexus_kills')])


# CODE TO ADD DATA TO GOOGLE SHEET START
#
# First spreadsheet is for Yrden group to analyze. Second spreadsheet is for me to import into Tableau a bit cleaner. 
spreadsheet_ids = ['1-evQTBBNkjEfL-oEDfdGneVjw_2AiC8puDiW7xs-XLc', '1tkENz6zKs9Q0-Dd771t0Or-fmL-uwOiGnU0tOxvvWIg']
for spreadsheet_id in spreadsheet_ids:
    sheet_name = 'API Stats'
    gc = gspread.service_account(filename='mercurial-song-447620-s8-68e9aa5a21f0.json')
    data_list = [df.columns] + df.to_numpy().tolist()
    sh = gc.open_by_key(spreadsheet_id)
    if spreadsheet_id == '1-evQTBBNkjEfL-oEDfdGneVjw_2AiC8puDiW7xs-XLc':
        sh_range = 'A2'
        format_range = "A3:BF1000"
    else:
        sh_range = 'A1'
        format_range = "A2:BF1000"
    worksheet = sh.worksheet(sheet_name)
    worksheet.clear()

    current_time = [f"Data updated at {time.ctime()} EST. If any issues exist, please message Bwlingiant on Discord."]

    worksheet.insert_row(current_time)
    worksheet.update(data_list, range_name=sh_range)
    # CODE TO ADD DATA TO GOOGLE SHEET END

    formats = [
        {
            "range": format_range,
            "format": {
                "textFormat": {
                    "bold": False
                },
            },
        },
    ]

    worksheet.batch_format(formats)