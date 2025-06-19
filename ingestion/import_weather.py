import psycopg as pg
import pyarrow.parquet as pq
import pandas as pd
from datetime import datetime

CONNECTION_STRING = f"user=postgres password=Mamicris04 dbname=project"

table= pq.read_table("./data/daily_weather.parquet")

df= table.to_pandas()
df["date"] = pd.to_datetime(df["date"])
last_ten_df = df[df["date"].dt.year >= 2013]
last_ten_df.loc[:, "day_month"] = last_ten_df['date'].dt.strftime('%d_%m')
last_ten_df=last_ten_df.drop(columns=["date"])

grouped_data = last_ten_df.groupby(["city_name", "day_month", "season", "station_id"], observed=True).mean()
print(grouped_data.columns.tolist())

#print(df.head)
#   station_id city_name       date  season  avg_temp_c  min_temp_c  max_temp_c  precipitation_mm  snow_depth_mm  avg_wind_dir_deg  avg_wind_speed_kmh  peak_wind_gust_kmh  avg_sea_level_pres_hpa  sunshine_total_min

with pg.connect(CONNECTION_STRING) as connection:
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS weather;")
    cursor.execute("""CREATE TABLE IF NOT EXISTS weather (
    station_id TEXT,
    city_name TEXT,
    day_month TEXT,  -- ← this was missing
    season TEXT,
    avg_temp_c REAL,
    min_temp_c REAL,
    max_temp_c REAL,
    precipitation_mm REAL,
    snow_depth_mm REAL,
    avg_wind_speed_kmh REAL,
    sunshine_total_min REAL
);
""")
 
    cursor.execute('delete from weather')
    for (city_name, day_month, season, station_id), row in grouped_data.iterrows():
        #print(city_name, day_month)
        cursor.execute("""
        INSERT INTO weather(
            station_id, city_name, day_month, season,
            avg_temp_c, min_temp_c, max_temp_c,
            precipitation_mm, snow_depth_mm,
            avg_wind_speed_kmh, sunshine_total_min
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        station_id, city_name, day_month, season,
        row["avg_temp_c"], row["min_temp_c"], row["max_temp_c"],
        row["precipitation_mm"], row["snow_depth_mm"],
        row["avg_wind_speed_kmh"], row["sunshine_total_min"]
    ))
        connection.commit()
    
