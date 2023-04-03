import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
apikey = os.getenv('API_KEY')

weather_df = pd.DataFrame()

city_list = ['Paris', 'Lille', 'Marseilles', 'Rouen', 'Bordeaux','Cambrai','Nantes','Metz','Toulouse','Montpellier','Nice','Brest','Arras','Lyon','Strasbourg','Angers','Rennes','Dijon','Grenoble','Caen']

# long_lat= requests.get("http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={apikey}")
# print(long_lat.text)

for city in city_list:
    long_lat= requests.get("http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={apikey}")
    lat = long_lat[0('lat')]
    long = long_lat[0('long')]
    response=requests.get("https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}")