import pandas as pd
import constants

from sqlalchemy import create_engine

engine = create_engine(f'postgresql://postgres:{constants.db_password}@{constants.db_ip}:{constants.db_port}/yrden')
engine.connect()

schema = 'lol'



df = pd.read_csv("C:/Users/Erica/Desktop/Personal Data Projects/Yrden DB/Riot API/2024_LoL_esports_match_data_from_OraclesElixir.csv")

# table_sql = df.head(n=0).to_sql(con=engine, name='esports_data', if_exists='replace')

# table_sql_with_schema = table_sql.replace('CREATE TABLE "esports_data"', f'CREATE TABLE "{schema}"."esports_data"')

# print(table_sql_with_schema)

print(pd.io.sql.get_schema(df, name='esports_data', con=engine))

# df.head(n=0).to_sql(con=engine, name='esports_data', if_exists='replace')