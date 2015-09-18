'''This is intended to be run as a dialy job (e.g. with cron) to build up a
data picture of the landing sites from a given launch site(s) over time'''
import json
import urllib2
from pprint import pprint
import os
import time
import datetime as dt

def long_conv(longitude): # deal with -ve longitude
    if longitude > 180:
        return -1 * (360 -longitude)
    else:
        return longitude

def retrieve_prediction(lat,lon,day,hour): # run request against web API
    response = urllib2.urlopen("http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(lat)+"&launch_longitude="+str(lon)+"&launch_datetime=2015-09-"+str(day)+"T"+str(hour)+"%3A00%3A00%2B01:00&ascent_rate=5&burst_altitude=30000&descent_rate=5")
    pprint('Running prediction for ' + str(lat)+','+str(lon))
    return response


now = dt.datetime.now()
LAUNCH_DAY = now.day
TODAY = str(now.day) + ":" + str(now.month) + ":" + str(now.year)
pprint(TODAY)
CWD = os.getcwd()
FILENAME='prediction.csv'
file = open(FILENAME, "a")
LAUNCH_LAT_1=52.403048 # first launch site
LAUNCH_LONG_1=-1.504792
LAUNCH_LAT_2 =51.895712 # second launch site
LAUNCH_LONG_2 = 0.492113
LAUNCH_HOUR_M=11 #Local Time
LAUNCH_HOUR_A=15 #Local Time
# list of sites
launch_sites=[(1,LAUNCH_LAT_1,LAUNCH_LONG_1),(2,LAUNCH_LAT_2,LAUNCH_LONG_2)]
hours = (LAUNCH_HOUR_M, LAUNCH_HOUR_A)
for LAUNCH_SITE in launch_sites:
    pprint(LAUNCH_SITE)
    LAUNCH_LAT = LAUNCH_SITE[1]
    LAUNCH_LONG = LAUNCH_SITE[2]
    if LAUNCH_LONG < 0:
        LAUNCH_LONG = 360 + LAUNCH_LONG
    for HOUR in hours:

        response = retrieve_prediction(LAUNCH_LAT,LAUNCH_LONG,LAUNCH_DAY,HOUR)
        d = json.load(response)

        lat_land = d["prediction"][1]["trajectory"][-1]["latitude"]
        long_land =  d["prediction"][1]["trajectory"][-1]["longitude"]
        long_land = long_conv(long_land)

        lat_burst = d["prediction"][0]["trajectory"][-1]["latitude"]
        long_burst =  d["prediction"][0]["trajectory"][-1]["longitude"]
        long_burst = long_conv(long_burst)
        prediction=(TODAY,HOUR,LAUNCH_SITE[0],lat_burst, long_burst, lat_land,long_land)
        counter = 1
        for entry in prediction:
            if counter < 7:
                file.write(str(entry)+',')
                counter+=1
            else:
                file.write(str(entry) + '\n')
        time.sleep(1)
file.close()
