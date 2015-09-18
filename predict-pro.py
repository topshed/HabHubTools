import json
import urllib2
from pprint import pprint
import folium
import webbrowser
import os
import time
CWD = os.getcwd()
FILENAME='prediction.html'
LAUNCH_LAT=52.403048
LAUNCH_LONG=-1.504792
LAUNCH_HOUR_M=11 #Local Time
LAUNCH_HOUR_A=15 #Local Time
sites=[]
hours = (LAUNCH_HOUR_M, LAUNCH_HOUR_A)
if LAUNCH_LONG < 0:
    LAUNCH_LONG = 360 + LAUNCH_LONG
for x in range(14,20):
    for HOUR in hours:
    #response = urllib2.urlopen("http://predict.cusf.co.uk/api/v1/?launch_latitude=52.403048&launch_longitude=358.49526&launch_datetime=2015-09-"+str(x)+"T00%3A00%3A00%2B01:00&ascent_rate=5&burst_altitude=30000&descent_rate=5")
        response = urllib2.urlopen("http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(LAUNCH_LAT)+"&launch_longitude="+str(LAUNCH_LONG)+"&launch_datetime=2015-09-"+str(x)+"T"+str(HOUR)+"%3A00%3A00%2B01:00&ascent_rate=5&burst_altitude=30000&descent_rate=5")
#data = json.load(response)
        d = json.load(response)

        lat_land = d["prediction"][1]["trajectory"][-1]["latitude"]
        long_land = -1 * (360 - d["prediction"][1]["trajectory"][-1]["longitude"])
#pprint(d["prediction"][1]["trajectory"][-1]) #final landing
#pprint(d["prediction"][0]["trajectory"][-1]) # burst
        landing=(x,HOUR,lat_land,long_land)
#pprint(long_land)
#pprint(lat_land)
        pprint(landing)
        sites.append(landing)
        time.sleep(1)

map_osm = folium.Map(location=[52, -1.3],zoom_start=8)

for y in sites:
    map_osm.simple_marker([y[2],y[3]], popup=str(y[0])+'-'+str(y[1])+":00Z")
    map_osm.create_map(path=FILENAME)
webbrowser.open_new('file://'+CWD+'/'+FILENAME)
