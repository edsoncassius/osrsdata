import psycopg2
from sqlalchemy import create_engine
import urllib.request
import datetime
import pandas as pd

skills = [
'Overall',
'Attack',
'Defence',
'Strength',
'Hitpoints',
'Ranged',
'Prayer',
'Magic',
'Cooking',
'Woodcutting',
'Fletching',
'Fishing',
'Firemaking',
'Crafting',
'Smithing',
'Mining',
'Herblore',
'Agility',
'Thieving',
'Slayer',
'Farming',
'Runecrafting',
'Hunter',
'Construction'
]

activities = [
'League Points',
'Bounty Hunter - Hunter',
'Bounty Hunter - Rogue',
'Clue Scrolls (all)',
'Clue Scrolls (beginner)',
'Clue Scrolls (easy)',
'Clue Scrolls (medium)',
'Clue Scrolls (hard)',
'Clue Scrolls (elite)',
'Clue Scrolls (master)',
'LMS - Rank',
'PvP Arena - Rank',
'Soul Wars Zeal',
'Rifts closed',
'Abyssal Sire',
'Alchemical Hydra',
'Barrows Chests',
'Bryophyta',
'Callisto',
'Cerberus',
'Chambers of Xeric',
'Chambers of Xeric: Challenge Mode',
'Chaos Elemental',
'Chaos Fanatic',
'Commander Zilyana',
'Corporeal Beast',
'Crazy Archaeologist',
'Dagannoth Prime',
'Dagannoth Rex',
'Dagannoth Supreme',
'Deranged Archaeologist',
'General Graardor',
'Giant Mole',
'Grotesque Guardians',
'Hespori',
'Kalphite Queen',
'King Black Dragon',
'Kraken',
"Kree'Arra",
"K'ril Tsutsaroth",
'Mimic',
'Nex',
'Nightmare',
"Phosani's Nightmare",
'Obor',
'Sarachnis',
'Scorpia',
'Skotizo',
'Tempoross',
'The Gauntlet',
'The Corrupted Gauntlet',
'Theatre of Blood',
'Theatre of Blood: Hard Mode',
'Thermonuclear Smoke Devil',
'Tombs of Amascut',
'Tombs of Amascut: Expert Mode',
'TzKal-Zuk',
'TzTok-Jad',
'Venenatis',
"Vet'ion",
'Vorkath',
'Wintertodt',
'Zalcano',
'Zulrah'
]

stats_names = skills + activities

def get_stats(username):
    
    ### Get stats from OSRS API
    
    contents = urllib.request.urlopen(
        "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player="+username).read()
    contents = str(contents)[2:] # remove first 2 chars
    values = str(contents).split("\\n") # split by \\n
    dicti = dict(zip(stats_names, values)) # gather keys + values
    
    list1 = []
    list2 = []
    
    for i in skills: 
        list1.append(i+"_XP") #skill names
        list2.append(dicti[i].split(',')[2]) #XP values
        list1.append(i+"_Lvl") 
        list2.append(dicti[i].split(',')[1]) #Level values
        list1.append(i+"_Rank")
        list2.append(dicti[i].split(',')[0]) #Rank values

    for i in activities: 
        list1.append(i+"_KC") #activity names
        list2.append(dicti[i].split(',')[1]) #KC values
        list1.append(i+"_Rank")
        list2.append(dicti[i].split(',')[0]) #Rank values
    
    dict_df = dict(zip(list1, list2)) #merge 2 dicts

    dict_df['time'] = str(datetime.datetime.now()) # add time
    dict_df['player'] = username #add player name
    
    # Skills : rank, level, xp
    # Activities : rank, kc
    return dict_df

def get_con():
    conn_string = 'postgresql://postgres:postgres@127.0.0.1/osrs'
  
    db = create_engine(conn_string)

    conn = db.connect()
    return conn

def send_data(df):
    
    ### Connect and append data to db
    
    conn = get_con()
    df.to_sql('hiscores', con=conn, if_exists='append',
        index=False)
    conn.close()
    return True

def get_data():
    
    ### Connect and query to retrieve data from db
    conn = get_con()
    data = pd.read_sql_query ('''
                                   SELECT
                                   *
                                   FROM hiscores
                                   ''', conn)
    conn.close()
    return data

def get_max_ovr(username):
    
    ### Connect and query to retrieve data from db
    conn = get_con()
    data = pd.read_sql_query ('SELECT max("Overall_XP") FROM hiscores WHERE player = '+"'"+username+"'", conn)
    max_ovr = int(data.iloc[0])
    conn.close()
    return max_ovr

def run_data():
    
    users = ["zezima"]

    print(str(datetime.datetime.now())) #print time for log
    for username in users:
        df = pd.DataFrame()
        player = get_stats(username)
        df = pd.DataFrame({k: [v] for k, v in player.items()}) #insert dict into dataframe
        df.reset_index(drop=True)
        ovr = int(df.iloc[0][0]) #get ovr from api's df
        max_ovr = get_max_ovr(username) #get max ovr from db
        if(max_ovr != ovr): #if different send data to db
            send_data(df)
            print("New data for "+username)
        else:
            print("No change on Overall XP for "+username)

run_data()

# Postgresql table: osrs.hiscores