# Initial data ingestion

The initial data ingestion was achieved using the dataset:

https://www.kaggle.com/code/nicholaspepera/weather-data-analysis

Creating a database name project

And by running the script 
        - ingestion/import_cities.py
        - ingestion/import_weather.py

Afterwards backup.sql and import_sql.py were created to make initializing the db for quoting the project easier.

# Installation

You will need a running postgres db server
Run pip3 install -r requirements.txt
Edit the .env file with your postgres username and password (do not change the openai key)
Run python3 import_sql.py
