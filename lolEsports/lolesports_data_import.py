import psycopg
import os
import wget
import constants


conn = psycopg.connect(constants.db_connection)
curs = conn.cursor()

print('Connection established.')

# output_dir = 'C:\Users\Erica\Desktop\Personal Data Projects\Yrden DB\Riot API'

old_file = "C:/Users/Erica/Desktop/Personal Data Projects/Yrden DB/Riot API/2024_LoL_esports_match_data_from_OraclesElixir.csv"

if os.path.exists(old_file):
    os.remove(old_file)
    print(f"File {old_file} has been deleted")
else: 
	print('File does not exist.')


url = 'https://drive.google.com/uc?export=download&id=1IjIEhLc9n8eLKeY-yh_YigKVWbhgGBsN'

# try:
# 	wget.download(url)
# except:
#      print('download failed'
filename = wget.download(url)


curs.execute('''TRUNCATE "lol".esports_data;
             ''')

file = "C:/Users/Erica/Desktop/Personal Data Projects/2024_LoL_esports_match_data_from_OraclesElixir.csv"

copy_sql = '''COPY "lol".esports_data (gameid, 
	datacompleteness, 
	url, 
	league, 
	year, 
	split, 
	playoffs, 
	date, 
	game, 
	patch, 
	participantid, 
	side , 
	position , 
	playername , 
	playerid , 
	teamname , 
	teamid , 
	champion , 
	ban1 , 
	ban2 , 
	ban3 , 
	ban4 , 
	ban5 , 
	pick1 , 
	pick2 , 
	pick3 , 
	pick4 , 
	pick5 , 
	gamelength , 
	result , 
	kills , 
	deaths , 
	assists , 
	teamkills , 
	teamdeaths , 
	doublekills , 
	triplekills , 
	quadrakills , 
	pentakills , 
	firstblood , 
	firstbloodkill , 
	firstbloodassist , 
	firstbloodvictim , 
	"team kpm" , 
	ckpm , 
	firstdragon , 
	dragons , 
	opp_dragons , 
	elementaldrakes , 
	opp_elementaldrakes , 
	infernals , 
	mountains , 
	clouds , 
	oceans , 
	chemtechs , 
	hextechs , 
	"dragons (type unknown)" , 
	elders , 
	opp_elders , 
	firstherald , 
	heralds , 
	opp_heralds , 
	void_grubs , 
	opp_void_grubs , 
	firstbaron , 
	barons , 
	opp_barons , 
	firsttower , 
	towers , 
	opp_towers , 
	firstmidtower , 
	firsttothreetowers , 
	turretplates , 
	opp_turretplates , 
	inhibitors , 
	opp_inhibitors , 
	damagetochampions , 
	dpm , 
	damageshare , 
	damagetakenperminute , 
	damagemitigatedperminute , 
	wardsplaced , 
	wpm , 
	wardskilled , 
	wcpm , 
	controlwardsbought , 
	visionscore , 
	vspm , 
	totalgold , 
	earnedgold , 
	"earned gpm" , 
	earnedgoldshare , 
	goldspent , 
	gspd , 
	gpr , 
	"total cs" , 
	minionkills , 
	monsterkills , 
	monsterkillsownjungle , 
	monsterkillsenemyjungle , 
	cspm , 
	goldat10 , 
	xpat10 , 
	csat10 , 
	opp_goldat10 , 
	opp_xpat10 , 
	opp_csat10 , 
	golddiffat10 , 
	xpdiffat10 , 
	csdiffat10 , 
	killsat10 , 
	assistsat10 , 
	deathsat10 , 
	opp_killsat10 , 
	opp_assistsat10 , 
	opp_deathsat10 , 
	goldat15 , 
	xpat15 , 
	csat15 , 
	opp_goldat15 , 
	opp_xpat15 , 
	opp_csat15 , 
	golddiffat15 , 
	xpdiffat15 , 
	csdiffat15 , 
	killsat15 , 
	assistsat15 , 
	deathsat15 , 
	opp_killsat15 , 
	opp_assistsat15 , 
	opp_deathsat15 , 
	goldat20 , 
	xpat20 , 
	csat20 , 
	opp_goldat20 , 
	opp_xpat20 , 
	opp_csat20 , 
	golddiffat20 , 
	xpdiffat20 , 
	csdiffat20 , 
	killsat20 , 
	assistsat20 , 
	deathsat20 , 
	opp_killsat20 , 
	opp_assistsat20 , 
	opp_deathsat20 , 
	goldat25 , 
	xpat25 , 
	csat25 , 
	opp_goldat25 , 
	opp_xpat25 , 
	opp_csat25 , 
	golddiffat25 , 
	xpdiffat25 , 
	csdiffat25 , 
	killsat25, 
	assistsat25, 
	deathsat25, 
	opp_killsat25, 
	opp_assistsat25, 
	opp_deathsat25) FROM STDIN WITH CSV HEADER;'''

data = open(old_file, 'r', encoding='utf-8')

# new_data = csv.reader(file)
# print(new_data)

# for record in data:
#     print(record)
with curs.copy(copy_sql) as copy:
    for record in data:
        copy.write(record)

conn.commit()
conn.close()

print('The database connection has been closed.')