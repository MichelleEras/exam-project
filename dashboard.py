import streamlit as st
import psycopg as pg
import folium
from streamlit_folium import st_folium
import datetime
from streamlit_card import card
CONNECTION_STRING = f"user=postgres password=Mamicris04 dbname=project"
with pg.connect(CONNECTION_STRING) as connection:
    cursor = connection.cursor()
    cursor.execute('select city_name from cities')
    result = cursor.fetchall()
    cities= []
    for row in result:
        cities.append(row[0])
#cities =['leuven', 'boortmeerbeek', 'antwerp', 'quito', 'misagualli'] 
st.write("hello welcome to streamlit")
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
        while current_date <= stop_date:
            current_day_month=current_date.strftime('%d_%m')  # Do your action here
            cursor.execute('Select season, avg_temp_c, min_temp_c, max_temp_c, precipitation_mm, snow_depth_mm, avg_wind_speed_kmh, sunshine_total_min from weather where city_name=%s and day_month=%s',(selected_city,current_day_month))
            season, avg_temp_c, min_temp_c, max_temp_c, precipitation_mm, snow_depth_mm, avg_wind_speed_kmh, sunshine_total_min  = cursor.fetchone()
            
            card(title=season,text=f""" average temperature: {avg_temp_c:.2f}°C 
                 Max temperature{max_temp_c:.2f}°C 
                   Min temperature{min_temp_c:.2f}°C""")
            current_date += datetime.timedelta(days=1)