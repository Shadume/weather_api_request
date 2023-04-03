import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

st.title("Informations météorologiques")

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#          'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text("Done! (using st.cache_data)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(
#     data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# st.subheader(f'Map of all pickups at {hour_to_filter}:00')
# st.map(filtered_data)


city_json = pd.read_json('city.list.json.gz')
city_json = city_json[["name", "country"]]
city_json["city_country"] = city_json["name"] + " - " + city_json["country"]
city_list = city_json["city_country"].tolist()

load_dotenv()
API_KEY = str(os.getenv('API_KEY'))

option = st.selectbox(
    'Choisissez une ville pour avoir ses informations météorologiques',
    (city_list))

city_name = option.split(' - ')[0]

response= requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}")
temp = response.json()['main']['temp']
feels_like = response.json()['main']['feels_like']
temp_min = response.json()['main']['temp_min']
temp_max = response.json()['main']['temp_max']
pressure = response.json()['main']['pressure']
humidity = response.json()['main']['humidity']
wind_speed = response.json()['wind']['speed']
wind_deg = response.json()['wind']['deg']
sunrise = datetime.utcfromtimestamp(response.json()['sys']['sunrise']).strftime('%H:%M:%S')
sunset = datetime.utcfromtimestamp(response.json()['sys']['sunset']).strftime('%H:%M:%S')

# col1, col2, col3, col4 = st.columns(4)

# col1.metric(label="Temperature", value=f"{temp} °C")
# col2.metric(label="Temperature ressentie", value=f"{feels_like} °C")
# col3.metric(label="Temperature minimale", value=f"{temp_min} °C")
# col4.metric(label="Temperature maximale", value=f"{temp_max} °C")
# col1.metric(label="Pression", value=f"{pressure} hPa")
# col2.metric(label="Humidité", value=f"{humidity} %")
# col3.metric(label="Vitesse du vent", value=f"{wind_speed} m/s")
# col4.metric(label="Direction du vent", value=f"{wind_deg} °")
# col1.metric(label="Lever du soleil", value=sunrise)
# col2.metric(label="Coucher du soleil", value=sunset)

# Fonction pour récupérer les informations météorologiques pour une ville donnée
def get_weather_data(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Fonction pour récupérer les prévisions météorologiques pour une ville donnée
def get_forecast_data(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Récupération des informations météorologiques pour la ville de Paris
city = option
data = get_weather_data(API_KEY, city)

# Affichage des informations météorologiques actuelles
st.subheader("Conditions météorologiques actuelles")
st.write("Température : ", data["main"]["temp"], "°C")
st.write("Pression : ", data["main"]["pressure"], "hPa")
st.write("Humidité : ", data["main"]["humidity"], "%")
st.write("Vent : ", data["wind"]["speed"], "m/s")

# Récupération des prévisions météorologiques pour la ville de Paris
forecast_data = get_forecast_data(API_KEY, city)

# Affichage des prévisions météorologiques pour les 5 prochains jours
st.subheader("Prévisions météorologiques pour les 5 prochains jours")

# Création d'un dictionnaire pour stocker les prévisions météorologiques pour chaque jour
forecast_dict = {}

# Boucle sur les prévisions pour chaque période de 3 heures
for forecast in forecast_data["list"]:
    date = datetime.fromtimestamp(forecast["dt"], tz=pytz.UTC)
    day = date.strftime("%Y-%m-%d")
    if day not in forecast_dict:
        forecast_dict[day] = []
    forecast_dict[day].append(forecast)

# Boucle sur les prévisions pour chaque jour
for day in forecast_dict.keys():
    st.write("Date : ", day)
    st.write("Prévisions : ")
    for forecast in forecast_dict[day]:
        time = datetime.fromtimestamp(forecast["dt"], tz=pytz.UTC).strftime("%H:%M")
        st.write(time, " : ", forecast["main"]["temp"], "°C")

