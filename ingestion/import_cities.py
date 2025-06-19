import psycopg as pg
import pandas as pd
import os
import dotenv

dotenv.load_dotenv()


# configure the database connection string
# comment the right one for use with your setup and adapt accordingly
# CONNECTION_STRING = f"user=postgres dbname=python-data-developer options=--search_path={SCHEMA_NAME} passfile=pgpass.conf"
CONNECTION_STRING = f"user={os.getenv("SQL_USER")} password={os.getenv("SQL_PASSWORD")} dbname=project"

def insert_city(cursor,station_id, city_name, country, state, iso2, iso3, latitude, longitude):
    # Insert a city into the database
    cursor.execute(
        "INSERT INTO cities (station_id, city_name, country, state, iso2, iso3, latitude, longitude) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)",(station_id,city_name,country,state,iso2,iso3,latitude,longitude)
    )
# create the database connection
# executing part to
with pg.connect(CONNECTION_STRING) as connection:
    cursor = connection.cursor()
    #cursor.execute('DROP DATABASE IF EXISTS project;')
    #cursor.execute('CREATE DATABASE project;')
    #cursor.execute('GRANT ALL PRIVILEGES ON DATABASE project TO postgres;')
    #cursor.execute('ALTER DATABASE project OWNER TO postgres;')
    cursor.execute('create table IF NOT EXISTS cities (station_id text, city_name text,country text,state text,iso2 text,iso3 text,latitude double PRECISION,longitude double PRECISION);')              
    cursor.execute('delete from cities')
    cities_df = pd.read_csv('data/cities.csv')
    for index, row in cities_df.iterrows():
        insert_city(cursor,row['station_id'], row ['city_name'],row['country'], row['state'],row['iso2'],row['iso3'],row['latitude'],row['longitude'])

    
    connection.commit()

