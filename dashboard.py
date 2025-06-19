import streamlit as st
import psycopg as pg
import folium
from streamlit_folium import st_folium
import datetime
import openai_planner
import math
import pandas as pd
from streamlit_card import card
import dotenv
import os

dotenv.load_dotenv()
CONNECTION_STRING = f"user={os.getenv("SQL_USER")} password={os.getenv("SQL_PASSWORD")} dbname=project"
with pg.connect(CONNECTION_STRING) as connection:
    cursor = connection.cursor()
    cursor.execute('Select city_name from cities')
    result = cursor.fetchall()
    cities= []
    for row in result:
        cities.append(row[0])
#cities =['leuven', 'boortmeerbeek', 'antwerp', 'quito', 'misagualli'] 
st.write("Hello welcome to streamlit")
selected_city = st.selectbox('select destination', cities)
with pg.connect(CONNECTION_STRING) as connection:
    cursor = connection.cursor()
    cursor.execute('select latitude, longitude from cities where city_name=%s',(selected_city,))
   
    coordinates = cursor.fetchone()
    city_map= folium.Map(coordinates,zoom_start=8)
    folium.Marker(
    coordinates, popup=selected_city, tooltip=selected_city).add_to(city_map)
    st_folium(city_map, width=725)
    st.write(coordinates)
    start_date= st.date_input("Departure Date:")
    stop_date=st.date_input("Return Date:")
    if start_date >  stop_date:
        st.write("Please select the departure date that is before the return date")


    if stop_date - start_date > datetime.timedelta(days=1):
        st.write("We are going in vacation!!!")
        current_date = start_date
        time_delta= stop_date - start_date
        days= time_delta.days
        rows=math.ceil(days/4) 

        for row_index in range(rows):
            card_columns= st.columns(4)
            for i,column in enumerate (card_columns):
                current_date = start_date + datetime.timedelta(days=row_index*4+i)
                current_day_month=current_date.strftime('%d_%m')  # Do your action here
                cursor.execute('Select season, avg_temp_c, min_temp_c, max_temp_c, precipitation_mm, snow_depth_mm, avg_wind_speed_kmh, sunshine_total_min from weather where city_name=%s and day_month=%s',(selected_city,current_day_month))
                season, avg_temp_c, min_temp_c, max_temp_c, precipitation_mm, snow_depth_mm, avg_wind_speed_kmh, sunshine_total_min  = cursor.fetchone()
                with column:
                    st.write(f"### {current_date.strftime("%d/%m/%Y")}")
                    if precipitation_mm and not pd.isna(precipitation_mm):
                        st.write(f"Rain {precipitation_mm} mm")
                    if snow_depth_mm and not pd.isna(snow_depth_mm):
                        st.write(f"Snow {snow_depth_mm} mm")
                    weather_image= "images/sun.png"
                    if precipitation_mm >2.5:
                        weather_image = "images/rain.png"
                    if snow_depth_mm >0:
                        weather_image= "images/snow.png"
                    st.image(weather_image)
                    st.write(f"average temperature: {avg_temp_c:.2f}°C")
                    st.write(f"Max temperature: {max_temp_c:.2f}°C ")
                    st.write(f"Min temperature: {min_temp_c:.2f}°C""")
        st.write('Loading AI travel plan....')
        travel_plan= openai_planner.planner_trip(selected_city, start_date,stop_date)
        st.write(travel_plan)
      
