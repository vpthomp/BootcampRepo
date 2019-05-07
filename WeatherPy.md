
# WeatherPy
----

### Analysis
* As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
* There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
* There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.

---

#### Note
* Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.


```python
#Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import time
import random
import datetime
import seaborn as sns
from pprint import pprint

#Import API Keys
from api_keys import api_key

# Import citipy to determine city based on latitude and longitude
from citipy import citipy

```


```python
# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)
```

## Generate Cities List


```python
# List for holding lat_lngs and cities
lat_lngs = []
cities = []
lat_lng_list = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=2000)
lngs = np.random.uniform(low=-180.000, high=180.000, size=2000)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)
        lat_lng_list.append(lat_lng)

# Print the city count to confirm sufficient count
len(cities)
```




    747




```python
#Create dataframe with list of cities
df = pd.DataFrame(cities)
df = df.rename(columns={0: 'city'})

#Add lat and lngs to dataframe, create separate columns for lats and longs
df['lat_lngs'] = lat_lng_list
df['lat'] = df.lat_lngs.map(lambda x: str(x[0]))
df['long'] = df.lat_lngs.map(lambda x: str(x[1]))

df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>lat_lngs</th>
      <th>lat</th>
      <th>long</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>clyde river</td>
      <td>(72.215845599571, -82.83386044880689)</td>
      <td>72.215845599571</td>
      <td>-82.83386044880689</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ushuaia</td>
      <td>(-60.60988334022177, -54.90046397944134)</td>
      <td>-60.60988334022177</td>
      <td>-54.90046397944134</td>
    </tr>
    <tr>
      <th>2</th>
      <td>santa maria</td>
      <td>(17.365409661683884, -20.867597749978643)</td>
      <td>17.365409661683884</td>
      <td>-20.867597749978643</td>
    </tr>
    <tr>
      <th>3</th>
      <td>yellowknife</td>
      <td>(67.83096814055853, -112.9967641072887)</td>
      <td>67.83096814055853</td>
      <td>-112.9967641072887</td>
    </tr>
    <tr>
      <th>4</th>
      <td>jamestown</td>
      <td>(-21.923852961333196, -15.678871848189146)</td>
      <td>-21.923852961333196</td>
      <td>-15.678871848189146</td>
    </tr>
  </tbody>
</table>
</div>



### Perform API Calls
* Perform a weather check on each city using a series of successive API calls.
* Include a print log of each city as it'sbeing processed (with the city number and city name).



```python
api_key = '4228ba0bf4de028fe4647cb1b43ebc1b' 

#Create columns for data to be collecting from the API
df['temp'] = ""
df['max_temp'] = ""
df['humidity'] = ""
df['wind_speed'] = ""
df['clouds'] = ""

#Iterate over each row as index pairs
#Include a print log of each city as it'sbeing processed (with the city number and city name)
for index, row in df.iterrows():
    city = row['city']
    print(f"Processing Record {index + 1} | {city}")
    city = city.replace(" ", "&")
    url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=" + city + "&APPID=" + api_key
    print(url)
    weather = requests.get(url).json()
    try:
        df.loc[index, 'temp'] = weather['main']['temp']
        df.loc[index, 'max_temp'] = weather['main']['temp_max']
        df.loc[index, 'humidity'] = weather['main']['humidity']
        df.loc[index, 'wind_speed'] = weather['wind']['speed']
        df.loc[index, 'clouds'] = weather['clouds']['all']
    except:
        df.loc[index, 'temp'] = 'city not found'
        df.loc[index, 'humidity'] = 'city not found'
        df.loc[index, 'wind_speed'] = 'city not found'
        df.loc[index, 'clouds'] = 'city not found'
    time.sleep(.50)
    
print("----------------------")
print("Data Retrieval Complete")
print("-----------------------")
```

    Processing Record 1 | clyde river
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=clyde&river&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 2 | ushuaia
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ushuaia&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 3 | santa maria
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=santa&maria&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 4 | yellowknife
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yellowknife&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 5 | jamestown
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jamestown&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 6 | russell
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=russell&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 7 | naze
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=naze&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 8 | sitamarhi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sitamarhi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 9 | chara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 10 | busselton
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=busselton&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 11 | hilo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hilo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 12 | belushya guba
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=belushya&guba&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 13 | castro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=castro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 14 | aklavik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aklavik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 15 | hobart
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hobart&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 16 | port alfred
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&alfred&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 17 | bulungu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bulungu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 18 | quetzaltepec
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=quetzaltepec&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 19 | illoqqortoormiut
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=illoqqortoormiut&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 20 | new norfolk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=new&norfolk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 21 | mar del plata
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mar&del&plata&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 22 | namtsy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=namtsy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 23 | graaff-reinet
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=graaff-reinet&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 24 | axim
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=axim&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 25 | urubicha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=urubicha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 26 | gazni
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gazni&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 27 | cidreira
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cidreira&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 28 | pergamino
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pergamino&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 29 | georgetown
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=georgetown&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 30 | labrea
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=labrea&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 31 | peniche
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=peniche&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 32 | inta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=inta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 33 | bluff
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bluff&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 34 | grand river south east
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=grand&river&south&east&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 35 | chokurdakh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chokurdakh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 36 | taksimo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=taksimo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 37 | cape town
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cape&town&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 38 | nome
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nome&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 39 | rio gallegos
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rio&gallegos&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 40 | lamar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lamar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 41 | bojaya
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bojaya&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 42 | hobyo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hobyo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 43 | hermanus
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hermanus&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 44 | cabo san lucas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cabo&san&lucas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 45 | punta arenas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=punta&arenas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 46 | geraldton
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=geraldton&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 47 | nanortalik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nanortalik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 48 | taolanaro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=taolanaro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 49 | katsuura
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=katsuura&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 50 | gaoual
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gaoual&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 51 | karratha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=karratha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 52 | provideniya
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=provideniya&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 53 | tasiilaq
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tasiilaq&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 54 | mataura
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mataura&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 55 | puerto escondido
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&escondido&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 56 | avarua
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=avarua&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 57 | ponta do sol
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ponta&do&sol&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 58 | ronneby
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ronneby&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 59 | pevek
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pevek&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 60 | carnarvon
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=carnarvon&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 61 | lixourion
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lixourion&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 62 | roald
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=roald&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 63 | pleshanovo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pleshanovo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 64 | kapaa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kapaa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 65 | churapcha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=churapcha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 66 | riviere-au-renard
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=riviere-au-renard&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 67 | barawe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=barawe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 68 | rikitea
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rikitea&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 69 | shwebo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shwebo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 70 | hithadhoo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hithadhoo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 71 | kahului
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kahului&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 72 | luderitz
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=luderitz&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 73 | monte alegre
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=monte&alegre&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 74 | vila velha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vila&velha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 75 | airai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=airai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 76 | sentyabrskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sentyabrskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 77 | atuona
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=atuona&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 78 | narsaq
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=narsaq&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 79 | paciran
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=paciran&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 80 | buloh kasap
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=buloh&kasap&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 81 | upernavik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=upernavik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 82 | ahipara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ahipara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 83 | saskylakh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saskylakh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 84 | vanderhoof
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vanderhoof&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 85 | marienburg
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=marienburg&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 86 | japura
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=japura&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 87 | rexburg
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rexburg&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 88 | barrow
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=barrow&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 89 | pekan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pekan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 90 | ouallam
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ouallam&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 91 | port hedland
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&hedland&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 92 | lakes entrance
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lakes&entrance&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 93 | khatanga
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=khatanga&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 94 | hervey bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hervey&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 95 | bredasdorp
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bredasdorp&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 96 | lithgow
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lithgow&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 97 | riverton
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=riverton&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 98 | palmares do sul
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=palmares&do&sul&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 99 | arraial do cabo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=arraial&do&cabo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 100 | torbay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=torbay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 101 | strezhevoy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=strezhevoy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 102 | savinka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=savinka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 103 | saldanha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saldanha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 104 | barentsburg
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=barentsburg&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 105 | zhuzhou
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=zhuzhou&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 106 | rawannawi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rawannawi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 107 | puerto ayora
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&ayora&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 108 | avera
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=avera&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 109 | verkhovye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=verkhovye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 110 | gainesville
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gainesville&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 111 | fortuna
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fortuna&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 112 | lavrentiya
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lavrentiya&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 113 | cedar city
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cedar&city&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 114 | kavieng
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kavieng&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 115 | nizhneyansk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nizhneyansk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 116 | babanusah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=babanusah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 117 | wewak
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=wewak&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 118 | longyearbyen
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=longyearbyen&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 119 | petropavlovsk-kamchatskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=petropavlovsk-kamchatskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 120 | vaini
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vaini&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 121 | ternate
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ternate&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 122 | norman wells
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=norman&wells&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 123 | les cayes
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=les&cayes&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 124 | faanui
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=faanui&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 125 | vaitupu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vaitupu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 126 | port elizabeth
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&elizabeth&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 127 | mporokoso
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mporokoso&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 128 | san patricio
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&patricio&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 129 | flinders
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=flinders&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 130 | parabel
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=parabel&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 131 | lakatoro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lakatoro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 132 | palabuhanratu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=palabuhanratu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 133 | bengkulu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bengkulu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 134 | trairi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=trairi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 135 | dolores
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dolores&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 136 | saint george
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint&george&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 137 | albany
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=albany&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 138 | anadyr
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=anadyr&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 139 | puri
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puri&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 140 | kamaishi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kamaishi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 141 | tura
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tura&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 142 | nikolskoye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nikolskoye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 143 | menomonie
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=menomonie&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 144 | kuala lipis
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kuala&lipis&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 145 | kulhudhuffushi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kulhudhuffushi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 146 | fairbanks
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fairbanks&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 147 | cherskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cherskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 148 | erenhot
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=erenhot&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 149 | kununurra
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kununurra&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 150 | asmar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=asmar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 151 | butaritari
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=butaritari&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 152 | tuktoyaktuk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tuktoyaktuk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 153 | slave lake
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=slave&lake&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 154 | ponta delgada
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ponta&delgada&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 155 | bathsheba
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bathsheba&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 156 | huilong
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=huilong&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 157 | bijie
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bijie&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 158 | kirensk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kirensk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 159 | husavik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=husavik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 160 | shelburne
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shelburne&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 161 | banda aceh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=banda&aceh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 162 | qaanaaq
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=qaanaaq&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 163 | hasaki
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hasaki&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 164 | sitka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sitka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 165 | lagoa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lagoa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 166 | margate
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=margate&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 167 | pizarro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pizarro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 168 | kutum
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kutum&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 169 | bar harbor
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bar&harbor&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 170 | carpina
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=carpina&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 171 | yumen
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yumen&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 172 | tombouctou
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tombouctou&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 173 | tabiauea
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tabiauea&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 174 | pangnirtung
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pangnirtung&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 175 | samus
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=samus&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 176 | goundam
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=goundam&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 177 | portland
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=portland&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 178 | severo-kurilsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=severo-kurilsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 179 | sambava
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sambava&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 180 | ribeira grande
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ribeira&grande&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 181 | waycross
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=waycross&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 182 | college
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=college&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 183 | dunedin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dunedin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 184 | beringovskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=beringovskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 185 | victoria
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=victoria&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 186 | ereymentau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ereymentau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 187 | oussouye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=oussouye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 188 | babushkin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=babushkin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 189 | saint-joseph
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint-joseph&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 190 | tymovskoye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tymovskoye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 191 | las vegas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=las&vegas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 192 | pinawa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pinawa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 193 | port-gentil
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port-gentil&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 194 | ahuimanu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ahuimanu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 195 | toba
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=toba&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 196 | coihaique
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=coihaique&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 197 | pemberton
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pemberton&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 198 | tambura
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tambura&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 199 | shakawe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shakawe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 200 | bratsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bratsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 201 | san cristobal
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&cristobal&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 202 | xique-xique
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=xique-xique&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 203 | byron bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=byron&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 204 | harper
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=harper&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 205 | muros
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=muros&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 206 | touros
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=touros&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 207 | chimore
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chimore&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 208 | goulburn
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=goulburn&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 209 | salalah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=salalah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 210 | tiksi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tiksi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 211 | acajutla
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=acajutla&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 212 | mutsamudu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mutsamudu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 213 | san angelo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&angelo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 214 | nouadhibou
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nouadhibou&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 215 | paamiut
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=paamiut&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 216 | dikson
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dikson&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 217 | bethel
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bethel&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 218 | damghan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=damghan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 219 | sola
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sola&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 220 | elizabeth city
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=elizabeth&city&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 221 | tuatapere
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tuatapere&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 222 | palmer
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=palmer&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 223 | kruisfontein
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kruisfontein&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 224 | thompson
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=thompson&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 225 | luanda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=luanda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 226 | east london
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=east&london&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 227 | concordia
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=concordia&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 228 | krasnoyarsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=krasnoyarsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 229 | grindavik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=grindavik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 230 | soe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=soe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 231 | kazerun
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kazerun&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 232 | sinnamary
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sinnamary&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 233 | olafsvik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=olafsvik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 234 | toliary
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=toliary&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 235 | den helder
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=den&helder&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 236 | klaksvik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=klaksvik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 237 | port augusta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&augusta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 238 | jackson
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jackson&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 239 | port shepstone
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&shepstone&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 240 | raudeberg
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=raudeberg&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 241 | vikulovo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vikulovo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 242 | vadso
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vadso&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 243 | pouebo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pouebo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 244 | babeni
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=babeni&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 245 | dwarka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dwarka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 246 | dickson
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dickson&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 247 | intipuca
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=intipuca&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 248 | fort nelson
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fort&nelson&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 249 | chuy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chuy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 250 | baykit
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=baykit&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 251 | tumaco
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tumaco&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 252 | ilhabela
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ilhabela&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 253 | severobaykalsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=severobaykalsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 254 | pisco
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pisco&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 255 | lebu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lebu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 256 | nioro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nioro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 257 | vestmanna
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vestmanna&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 258 | aykhal
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aykhal&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 259 | iralaya
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=iralaya&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 260 | henties bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=henties&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 261 | khani
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=khani&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 262 | phalombe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=phalombe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 263 | dachau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dachau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 264 | wolmaranstad
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=wolmaranstad&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 265 | mount gambier
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mount&gambier&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 266 | revda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=revda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 267 | urupes
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=urupes&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 268 | svetlogorsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=svetlogorsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 269 | mys shmidta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mys&shmidta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 270 | ati
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ati&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 271 | huarmey
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=huarmey&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 272 | guerrero negro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=guerrero&negro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 273 | souillac
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=souillac&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 274 | salta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=salta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 275 | amderma
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=amderma&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 276 | namatanai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=namatanai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 277 | laguna
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=laguna&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 278 | kaohsiung
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kaohsiung&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 279 | esperance
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=esperance&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 280 | oranjemund
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=oranjemund&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 281 | praia da vitoria
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=praia&da&vitoria&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 282 | pacific grove
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pacific&grove&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 283 | biak
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=biak&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 284 | machakos
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=machakos&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 285 | adrar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=adrar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 286 | oktyabrskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=oktyabrskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 287 | bilma
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bilma&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 288 | lata
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lata&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 289 | olinda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=olinda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 290 | ranau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ranau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 291 | yarmouth
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yarmouth&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 292 | sao jose da coroa grande
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sao&jose&da&coroa&grande&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 293 | jian
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jian&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 294 | kangaatsiaq
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kangaatsiaq&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 295 | calama
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=calama&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 296 | maningrida
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=maningrida&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 297 | lazaro cardenas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lazaro&cardenas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 298 | mehamn
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mehamn&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 299 | podosinovets
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=podosinovets&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 300 | uni
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=uni&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 301 | aragarcas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aragarcas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 302 | yinchuan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yinchuan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 303 | vagur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vagur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 304 | hinton
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hinton&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 305 | vanavara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vanavara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 306 | puerto leguizamo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&leguizamo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 307 | gopalpur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gopalpur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 308 | sombrio
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sombrio&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 309 | vardo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vardo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 310 | grand gaube
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=grand&gaube&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 311 | buraydah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=buraydah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 312 | iqaluit
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=iqaluit&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 313 | wajir
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=wajir&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 314 | gouyave
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gouyave&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 315 | prince albert
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=prince&albert&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 316 | buqayq
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=buqayq&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 317 | tidore
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tidore&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 318 | kyzyl-suu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kyzyl-suu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 319 | tezu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tezu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 320 | azanka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=azanka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 321 | skalistyy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=skalistyy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 322 | mount isa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mount&isa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 323 | egvekinot
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=egvekinot&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 324 | padang
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=padang&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 325 | cayenne
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cayenne&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 326 | samarai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=samarai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 327 | clovis
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=clovis&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 328 | parana
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=parana&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 329 | mahebourg
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mahebourg&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 330 | santa cruz
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=santa&cruz&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 331 | kungalv
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kungalv&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 332 | inirida
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=inirida&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 333 | hamilton
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hamilton&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 334 | gold coast
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gold&coast&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 335 | pandan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pandan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 336 | ginda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ginda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 337 | manjeshwar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=manjeshwar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 338 | bubaque
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bubaque&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 339 | caltzontzin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=caltzontzin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 340 | saleaula
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saleaula&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 341 | tsihombe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tsihombe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 342 | vestbygda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vestbygda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 343 | tukan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tukan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 344 | huallanca
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=huallanca&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 345 | mola di bari
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mola&di&bari&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 346 | soyo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=soyo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 347 | acapulco
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=acapulco&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 348 | hastings
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hastings&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 349 | westport
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=westport&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 350 | decatur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=decatur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 351 | morant bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=morant&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 352 | lorengau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lorengau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 353 | itumbiara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=itumbiara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 354 | conakry
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=conakry&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 355 | talnakh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=talnakh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 356 | kitimat
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kitimat&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 357 | vicuna
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vicuna&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 358 | kohlu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kohlu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 359 | kawalu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kawalu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 360 | tyukhtet
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tyukhtet&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 361 | luxor
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=luxor&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 362 | auki
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=auki&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 363 | jiddah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jiddah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 364 | kimbe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kimbe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 365 | aksarka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aksarka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 366 | asau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=asau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 367 | carauari
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=carauari&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 368 | mbini
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mbini&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 369 | manta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=manta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 370 | poso
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=poso&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 371 | komsomolskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=komsomolskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 372 | ancud
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ancud&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 373 | mwandiga
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mwandiga&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 374 | sweetwater
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sweetwater&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 375 | koidu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=koidu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 376 | santa isabel do rio negro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=santa&isabel&do&rio&negro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 377 | mitsamiouli
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mitsamiouli&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 378 | poum
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=poum&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 379 | kodinsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kodinsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 380 | karolinka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=karolinka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 381 | fukue
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fukue&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 382 | praya
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=praya&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 383 | sidi bu zayd
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sidi&bu&zayd&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 384 | alvorada
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=alvorada&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 385 | buenos aires
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=buenos&aires&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 386 | twante
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=twante&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 387 | itarema
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=itarema&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 388 | jalu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jalu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 389 | uyuni
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=uyuni&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 390 | kodiak
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kodiak&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 391 | kendari
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kendari&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 392 | kieta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kieta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 393 | jabinyanah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jabinyanah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 394 | zhigansk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=zhigansk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 395 | belyy yar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=belyy&yar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 396 | luena
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=luena&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 397 | meyungs
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=meyungs&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 398 | marawi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=marawi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 399 | trinidad
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=trinidad&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 400 | taunggyi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=taunggyi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 401 | bereda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bereda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 402 | charlestown
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=charlestown&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 403 | alofi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=alofi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 404 | nang rong
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nang&rong&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 405 | pueblo nuevo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pueblo&nuevo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 406 | saint-louis
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint-louis&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 407 | kampot
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kampot&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 408 | atambua
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=atambua&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 409 | canutama
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=canutama&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 410 | soloneshnoye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=soloneshnoye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 411 | quatre cocos
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=quatre&cocos&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 412 | la primavera
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=la&primavera&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 413 | shitanjing
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shitanjing&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 414 | lasa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lasa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 415 | chapais
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chapais&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 416 | chikwawa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chikwawa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 417 | san juan de la maguana
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&juan&de&la&maguana&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 418 | ligayan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ligayan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 419 | solenzo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=solenzo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 420 | berlevag
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=berlevag&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 421 | fare
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fare&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 422 | ankang
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ankang&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 423 | monrovia
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=monrovia&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 424 | mayo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mayo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 425 | benjamin constant
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=benjamin&constant&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 426 | mogadishu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mogadishu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 427 | samusu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=samusu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 428 | nauta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nauta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 429 | kenai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kenai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 430 | korla
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=korla&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 431 | caravelas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=caravelas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 432 | sur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 433 | shatrovo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shatrovo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 434 | moindou
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=moindou&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 435 | tukrah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tukrah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 436 | te anau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=te&anau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 437 | sorland
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sorland&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 438 | vorobyevka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vorobyevka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 439 | uwayl
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=uwayl&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 440 | awjilah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=awjilah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 441 | gawler
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gawler&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 442 | moiyabana
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=moiyabana&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 443 | gouloure
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gouloure&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 444 | kerki
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kerki&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 445 | aksha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aksha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 446 | san policarpo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&policarpo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 447 | poronaysk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=poronaysk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 448 | colac
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=colac&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 449 | jiazi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jiazi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 450 | marsabit
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=marsabit&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 451 | mouila
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mouila&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 452 | okulovka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=okulovka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 453 | buchanan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=buchanan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 454 | shillong
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shillong&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 455 | aloleng
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aloleng&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 456 | whitehorse
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=whitehorse&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 457 | ilulissat
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ilulissat&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 458 | krasnyy chikoy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=krasnyy&chikoy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 459 | galveston
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=galveston&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 460 | morros
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=morros&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 461 | attawapiskat
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=attawapiskat&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 462 | nichinan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nichinan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 463 | kaitangata
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kaitangata&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 464 | ghanzi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ghanzi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 465 | gangotri
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gangotri&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 466 | yamethin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yamethin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 467 | baiyin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=baiyin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 468 | vila franca do campo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vila&franca&do&campo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 469 | bolshoy uluy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bolshoy&uluy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 470 | tupanatinga
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tupanatinga&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 471 | kyra
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kyra&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 472 | okha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=okha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 473 | calbuco
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=calbuco&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 474 | rab
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rab&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 475 | gushikawa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gushikawa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 476 | shingu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shingu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 477 | macaboboni
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=macaboboni&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 478 | khandbari
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=khandbari&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 479 | estevan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=estevan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 480 | namibe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=namibe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 481 | quedlinburg
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=quedlinburg&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 482 | yeppoon
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yeppoon&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 483 | marsa matruh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=marsa&matruh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 484 | sawakin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sawakin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 485 | afmadu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=afmadu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 486 | adiake
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=adiake&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 487 | naftalan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=naftalan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 488 | pierre
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pierre&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 489 | severnyy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=severnyy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 490 | tiarei
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tiarei&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 491 | kindu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kindu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 492 | shakhrinau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shakhrinau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 493 | ribas do rio pardo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ribas&do&rio&pardo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 494 | sao filipe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sao&filipe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 495 | rovnoye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rovnoye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 496 | san andres
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&andres&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 497 | kailua
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kailua&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 498 | saint-lo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint-lo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 499 | georgiyevka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=georgiyevka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 500 | luganville
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=luganville&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 501 | artyom
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=artyom&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 502 | coos bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=coos&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 503 | saurimo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saurimo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 504 | vila
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vila&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 505 | ust-kuyga
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ust-kuyga&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 506 | puerto madero
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&madero&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 507 | virginia beach
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=virginia&beach&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 508 | sept-iles
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sept-iles&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 509 | saint-philippe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint-philippe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 510 | tual
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tual&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 511 | dingle
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dingle&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 512 | san luis
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&luis&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 513 | dabakala
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dabakala&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 514 | zolotinka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=zolotinka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 515 | los llanos de aridane
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=los&llanos&de&aridane&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 516 | slimnic
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=slimnic&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 517 | hambantota
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hambantota&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 518 | jiangyou
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jiangyou&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 519 | arlit
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=arlit&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 520 | srednekolymsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=srednekolymsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 521 | polunochnoye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=polunochnoye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 522 | yaransk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yaransk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 523 | pimentel
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pimentel&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 524 | hofn
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hofn&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 525 | ulaangom
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ulaangom&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 526 | safaga
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=safaga&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 527 | san vicente
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&vicente&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 528 | nador
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nador&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 529 | nishihara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nishihara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 530 | hualmay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hualmay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 531 | abashiri
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=abashiri&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 532 | spearfish
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=spearfish&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 533 | seoul
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=seoul&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 534 | konstantinovka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=konstantinovka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 535 | simao
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=simao&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 536 | kelso
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kelso&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 537 | atasu
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=atasu&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 538 | sapao
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sapao&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 539 | chenghai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chenghai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 540 | verkh-suetka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=verkh-suetka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 541 | pokhara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pokhara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 542 | xai-xai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=xai-xai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 543 | cremona
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cremona&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 544 | bambous virieux
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bambous&virieux&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 545 | nuuk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nuuk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 546 | solnechnyy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=solnechnyy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 547 | panjab
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=panjab&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 548 | kushima
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kushima&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 549 | bandarbeyla
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bandarbeyla&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 550 | viedma
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=viedma&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 551 | meadville
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=meadville&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 552 | palwal
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=palwal&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 553 | oksfjord
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=oksfjord&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 554 | kamenka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kamenka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 555 | xining
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=xining&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 556 | dandong
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dandong&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 557 | high level
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=high&level&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 558 | dianopolis
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dianopolis&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 559 | mbandaka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mbandaka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 560 | sinkat
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sinkat&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 561 | cernavoda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cernavoda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 562 | harlingen
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=harlingen&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 563 | iranshahr
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=iranshahr&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 564 | hammerfest
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=hammerfest&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 565 | raiwind
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=raiwind&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 566 | broome
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=broome&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 567 | pembroke
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pembroke&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 568 | makakilo city
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=makakilo&city&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 569 | greenfield
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=greenfield&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 570 | vung tau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vung&tau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 571 | puerto rondon
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&rondon&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 572 | bure
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bure&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 573 | ovalle
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ovalle&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 574 | campeche
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=campeche&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 575 | kavaratti
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kavaratti&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 576 | puerto suarez
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&suarez&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 577 | bonfim
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bonfim&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 578 | richards bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=richards&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 579 | altea
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=altea&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 580 | the valley
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=the&valley&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 581 | penzance
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=penzance&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 582 | kloulklubed
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kloulklubed&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 583 | ippy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ippy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 584 | dolbeau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dolbeau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 585 | ludvika
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ludvika&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 586 | gwanda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gwanda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 587 | gat
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gat&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 588 | mogapi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mogapi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 589 | muravlenko
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=muravlenko&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 590 | weiser
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=weiser&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 591 | kopyevo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kopyevo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 592 | ocos
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ocos&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 593 | bijar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bijar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 594 | ciledug
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ciledug&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 595 | vercheres
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vercheres&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 596 | north platte
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=north&platte&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 597 | brandon
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=brandon&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 598 | necochea
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=necochea&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 599 | marion
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=marion&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 600 | bulgan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bulgan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 601 | frontera
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=frontera&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 602 | novyy buyan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=novyy&buyan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 603 | lima
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lima&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 604 | berbera
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=berbera&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 605 | mouzakion
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mouzakion&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 606 | san ramon
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&ramon&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 607 | bandarawela
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bandarawela&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 608 | zhanatas
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=zhanatas&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 609 | yukhnov
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yukhnov&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 610 | jaguaribe
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=jaguaribe&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 611 | ngunguru
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ngunguru&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 612 | bardiyah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bardiyah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 613 | campos sales
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=campos&sales&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 614 | carndonagh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=carndonagh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 615 | lahij
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lahij&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 616 | itarantim
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=itarantim&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 617 | careiro da varzea
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=careiro&da&varzea&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 618 | nhamunda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nhamunda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 619 | pontes e lacerda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pontes&e&lacerda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 620 | ola
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ola&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 621 | gaoua
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=gaoua&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 622 | kochevo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kochevo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 623 | stutterheim
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=stutterheim&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 624 | abu dhabi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=abu&dhabi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 625 | pinega
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pinega&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 626 | matara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=matara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 627 | sangar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sangar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 628 | viligili
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=viligili&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 629 | belaya gora
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=belaya&gora&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 630 | pochutla
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pochutla&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 631 | tuggurt
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tuggurt&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 632 | cairns
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cairns&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 633 | manacapuru
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=manacapuru&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 634 | townsville
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=townsville&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 635 | aktau
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aktau&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 636 | caibarien
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=caibarien&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 637 | alyangula
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=alyangula&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 638 | rio grande
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=rio&grande&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 639 | ogulin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ogulin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 640 | honningsvag
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=honningsvag&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 641 | tessalit
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tessalit&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 642 | yulara
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yulara&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 643 | kobayashi
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kobayashi&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 644 | yining
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yining&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 645 | mayskiy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mayskiy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 646 | faya
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=faya&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 647 | luoyang
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=luoyang&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 648 | davila
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=davila&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 649 | dvinskoy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dvinskoy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 650 | palencia
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=palencia&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 651 | saryg-sep
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saryg-sep&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 652 | sao jeronimo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sao&jeronimo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 653 | ayan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ayan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 654 | suntar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=suntar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 655 | beloha
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=beloha&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 656 | itoman
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=itoman&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 657 | imeni zhelyabova
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=imeni&zhelyabova&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 658 | tautira
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tautira&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 659 | nelson bay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nelson&bay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 660 | crestview
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=crestview&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 661 | togur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=togur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 662 | port keats
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&keats&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 663 | guarda
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=guarda&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 664 | san jeronimo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=san&jeronimo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 665 | puerto cortes
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=puerto&cortes&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 666 | phnum penh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=phnum&penh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 667 | yerbogachen
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yerbogachen&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 668 | bonavista
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bonavista&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 669 | kondinskoye
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kondinskoye&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 670 | nemuro
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nemuro&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 671 | andenes
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=andenes&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 672 | smolenka
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=smolenka&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 673 | troitsko-pechorsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=troitsko-pechorsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 674 | aljezur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=aljezur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 675 | ahmadpur sial
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ahmadpur&sial&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 676 | nyuksenitsa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nyuksenitsa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 677 | blois
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=blois&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 678 | nizhneudinsk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=nizhneudinsk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 679 | monterey
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=monterey&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 680 | vila do maio
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=vila&do&maio&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 681 | haines junction
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=haines&junction&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 682 | dinsor
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dinsor&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 683 | weinan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=weinan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 684 | chikmagalur
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=chikmagalur&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 685 | fort collins
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fort&collins&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 686 | carutapera
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=carutapera&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 687 | oncesti
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=oncesti&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 688 | bolungarvik
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bolungarvik&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 689 | mocuba
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mocuba&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 690 | yingcheng
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yingcheng&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 691 | waddan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=waddan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 692 | constitucion
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=constitucion&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 693 | saint anthony
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint&anthony&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 694 | bhuj
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=bhuj&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 695 | smithers
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=smithers&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 696 | peace river
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=peace&river&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 697 | yertsevo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=yertsevo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 698 | pontianak
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pontianak&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 699 | port lincoln
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&lincoln&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 700 | port blair
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&blair&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 701 | ukiah
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ukiah&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 702 | lovington
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lovington&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 703 | foumbot
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=foumbot&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 704 | lolua
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lolua&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 705 | isangel
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=isangel&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 706 | shache
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shache&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 707 | iquique
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=iquique&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 708 | black river
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=black&river&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 709 | cap malheureux
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cap&malheureux&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 710 | itambacuri
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=itambacuri&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 711 | sorvag
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sorvag&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 712 | saint-pierre
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=saint-pierre&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 713 | fomboni
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=fomboni&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 714 | asasa
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=asasa&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 715 | port hardy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=port&hardy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 716 | mecca
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mecca&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 717 | kupang
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kupang&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 718 | sabang
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sabang&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 719 | tumannyy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=tumannyy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 720 | shawinigan
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=shawinigan&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 721 | antofagasta
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=antofagasta&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 722 | barcelona
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=barcelona&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 723 | markova
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=markova&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 724 | iguape
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=iguape&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 725 | miraflores
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=miraflores&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 726 | djambala
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=djambala&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 727 | thinadhoo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=thinadhoo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 728 | mackay
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mackay&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 729 | leh
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=leh&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 730 | pointe michel
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pointe&michel&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 731 | mentok
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=mentok&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 732 | karaul
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=karaul&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 733 | severomuysk
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=severomuysk&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 734 | pecos
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=pecos&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 735 | santa vitoria do palmar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=santa&vitoria&do&palmar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 736 | whitecourt
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=whitecourt&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 737 | melito di porto salvo
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=melito&di&porto&salvo&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 738 | cockburn town
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=cockburn&town&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 739 | sarkand
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=sarkand&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 740 | redlands
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=redlands&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 741 | lompoc
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lompoc&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 742 | lodwar
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=lodwar&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 743 | punta cardon
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=punta&cardon&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 744 | kalmunai
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=kalmunai&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 745 | ortakoy
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=ortakoy&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 746 | menongue
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=menongue&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    Processing Record 747 | dalbandin
    http://api.openweathermap.org/data/2.5/weather?units=Imperial&q=dalbandin&APPID=4228ba0bf4de028fe4647cb1b43ebc1b
    ----------------------
    Data Retrieval Complete
    -----------------------
    

### Convert Raw Data to DataFrame
* Export the city data into a .csv.
* Display the DataFrame


```python
#Remove cities that could not be found from the dataframe
df = df[df.temp != 'city not found']

#Check that there are still 500+ records
len(df)
```




    662




```python
#Convert lat from string to float object
df.lat = df.lat.astype(float)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>lat_lngs</th>
      <th>lat</th>
      <th>long</th>
      <th>temp</th>
      <th>max_temp</th>
      <th>humidity</th>
      <th>wind_speed</th>
      <th>clouds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>clyde river</td>
      <td>(72.215845599571, -82.83386044880689)</td>
      <td>72.215846</td>
      <td>-82.83386044880689</td>
      <td>44.01</td>
      <td>44.01</td>
      <td>90</td>
      <td>4.79</td>
      <td>100</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ushuaia</td>
      <td>(-60.60988334022177, -54.90046397944134)</td>
      <td>-60.609883</td>
      <td>-54.90046397944134</td>
      <td>50.29</td>
      <td>51.8</td>
      <td>66</td>
      <td>31.09</td>
      <td>40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>santa maria</td>
      <td>(17.365409661683884, -20.867597749978643)</td>
      <td>17.365410</td>
      <td>-20.867597749978643</td>
      <td>82.52</td>
      <td>82.52</td>
      <td>80</td>
      <td>8.68</td>
      <td>100</td>
    </tr>
    <tr>
      <th>3</th>
      <td>yellowknife</td>
      <td>(67.83096814055853, -112.9967641072887)</td>
      <td>67.830968</td>
      <td>-112.9967641072887</td>
      <td>45.25</td>
      <td>46.99</td>
      <td>39</td>
      <td>17.22</td>
      <td>20</td>
    </tr>
    <tr>
      <th>4</th>
      <td>jamestown</td>
      <td>(-21.923852961333196, -15.678871848189146)</td>
      <td>-21.923853</td>
      <td>-15.678871848189146</td>
      <td>50.3</td>
      <td>50.3</td>
      <td>80</td>
      <td>5.17</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Export dataframe to CSV
df.to_csv("cities.csv", encoding="utf-8", index=False)
```


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>lat_lngs</th>
      <th>lat</th>
      <th>long</th>
      <th>temp</th>
      <th>max_temp</th>
      <th>humidity</th>
      <th>wind_speed</th>
      <th>clouds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>clyde river</td>
      <td>(72.215845599571, -82.83386044880689)</td>
      <td>72.215846</td>
      <td>-82.83386044880689</td>
      <td>44.01</td>
      <td>44.01</td>
      <td>90</td>
      <td>4.79</td>
      <td>100</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ushuaia</td>
      <td>(-60.60988334022177, -54.90046397944134)</td>
      <td>-60.609883</td>
      <td>-54.90046397944134</td>
      <td>50.29</td>
      <td>51.8</td>
      <td>66</td>
      <td>31.09</td>
      <td>40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>santa maria</td>
      <td>(17.365409661683884, -20.867597749978643)</td>
      <td>17.365410</td>
      <td>-20.867597749978643</td>
      <td>82.52</td>
      <td>82.52</td>
      <td>80</td>
      <td>8.68</td>
      <td>100</td>
    </tr>
    <tr>
      <th>3</th>
      <td>yellowknife</td>
      <td>(67.83096814055853, -112.9967641072887)</td>
      <td>67.830968</td>
      <td>-112.9967641072887</td>
      <td>45.25</td>
      <td>46.99</td>
      <td>39</td>
      <td>17.22</td>
      <td>20</td>
    </tr>
    <tr>
      <th>4</th>
      <td>jamestown</td>
      <td>(-21.923852961333196, -15.678871848189146)</td>
      <td>-21.923853</td>
      <td>-15.678871848189146</td>
      <td>50.3</td>
      <td>50.3</td>
      <td>80</td>
      <td>5.17</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>



### Plotting the Data
* Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
* Save the plotted figures as .pngs.

#### Latitude vs. Temperature Plot


```python
#Pull in today's date for graphs
date = datetime.date.today()
date = time.strftime("%m/%d/%Y")

sns.set()
plt.figure(figsize=(10,8))
plt.scatter(df['lat'], df['temp'])
plt.title(f"City Latitude vs. Temperature {date}", fontsize="18")
plt.xlabel("Latitude", fontsize="14")
plt.ylabel("Temperature (F)", fontsize="14")
plt.ylim(0, 120)

plt.savefig("Temperature.png")

plt.show()
```


![png](output_15_0.png)


#### Latitude vs. Humidity Plot


```python
plt.figure(figsize=(10,8))
plt.scatter(df['lat'], df['humidity'])                              
plt.title(f"City Latitude vs. Humidity {date}", fontsize="18")
plt.xlabel("Latitude", fontsize="14")
plt.ylabel("Humidity (%)", fontsize="14")

plt.ylim(0,120)

plt.savefig("Humidity.png")

plt.show()
```


![png](output_17_0.png)


#### Latitude vs. Cloudiness Plot


```python
plt.figure(figsize=(10,8))
plt.scatter(df['lat'], df['clouds'])                              
plt.title(f"City Latitude vs.Cloudiness {date}", fontsize="18")
plt.xlabel("Latitude", fontsize="14")
plt.ylabel("Wind Speed (mph)", fontsize="14")
plt.ylim(-20, 120)

plt.savefig("Cloudiness.png")

plt.show()
```


![png](output_19_0.png)


#### Latitude vs. Wind Speed Plot


```python
plt.figure(figsize=(10,8))
plt.scatter(df['lat'], df['wind_speed'])                              
plt.title(f"City Latitude vs. Wind Speed {date}", fontsize="18")
plt.xlabel("Latitude", fontsize="14")
plt.ylabel("Wind Speed (mph)", fontsize="14")

plt.ylim(-5,45)

plt.savefig("Wind_Speed.png")

plt.show()
```


![png](output_21_0.png)



```python

```
