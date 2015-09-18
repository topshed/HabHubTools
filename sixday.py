import json
import urllib2
from pprint import pprint
import folium
import webbrowser
import os
import time
import datetime as dt
CWD = os.getcwd()
now = dt.datetime.now()
LAUNCH_DAY = now.day
odd_day = False
LAUNCH_HOUR_A = 14
LAUNCH_HOUR_M = 10
if now.hour > 10 and now.hour < 14:
    LAUNCH_HOUR_ODD = now.hour
    odd_day = True

if now.hour > 14:
    LAUNCH_DAY = now.day + 1
FILENAME='prediction.html'
LAUNCH_LAT=52.403048
LAUNCH_LONG=-1.504792
if LAUNCH_LONG < 0:
    LAUNCH_LONG = 360 + LAUNCH_LONG
sites=[]
if odd_day:

    for HOUR in (LAUNCH_HOUR_ODD,LAUNCH_HOUR_A):
        response = urllib2.urlopen("http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(LAUNCH_LAT)+"&launch_longitude="+str(LAUNCH_LONG)+"&launch_datetime=2015-09-"+str(LAUNCH_DAY)+"T"+str(HOUR)+"%3A00%3A00%2B01:00&ascent_rate=5&burst_altitude=30000&descent_rate=5")
        d = json.load(response)
        lat_land = d["prediction"][1]["trajectory"][-1]["latitude"]
        long_land = -1 * (360 - d["prediction"][1]["trajectory"][-1]["longitude"])
        landing=(LAUNCH_DAY,HOUR,lat_land,long_land)
        pprint(landing)
        sites.append(landing)
        time.sleep(1)
    LAUNCH_DAY = LAUNCH_DAY + 1

hours = (LAUNCH_HOUR_M, LAUNCH_HOUR_A)

for x in range(LAUNCH_DAY,LAUNCH_DAY + 6):
    for HOUR in hours:
        response = urllib2.urlopen("http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(LAUNCH_LAT)+"&launch_longitude="+str(LAUNCH_LONG)+"&launch_datetime=2015-09-"+str(x)+"T"+str(HOUR)+"%3A00%3A00%2B01:00&ascent_rate=5&burst_altitude=30000&descent_rate=5")
        d = json.load(response)
        lat_land = d["prediction"][1]["trajectory"][-1]["latitude"]
        long_land = -1 * (360 - d["prediction"][1]["trajectory"][-1]["longitude"])
        landing=(x,HOUR,lat_land,long_land)
        pprint(landing)
        sites.append(landing)
        time.sleep(1)

map_osm = folium.Map(location=[52, -1.3],zoom_start=8)

for y in sites:
    map_osm.simple_marker([y[2],y[3]], popup=str(y[0])+'-'+str(y[1])+":00Z")
    map_osm.create_map(path=FILENAME)
webbrowser.open_new('file://'+CWD+'/'+FILENAME)
