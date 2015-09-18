import json
import urllib2
from pprint import pprint
import folium
import webbrowser
import os
import time
from LatLon import *
import datetime as dt

def long_conv(longitude):
    if longitude > 180:
        return -1 * (360 -longitude)
    else:
        return longitude

def calc_backbearing(bearing):
    pprint('Calculating backbearing')
    if bearing >= 180:
        backbearing = 180 - bearing
    else:
        backbearing = 180 + bearing
    return backbearing

def retrieve_prediction(lat,lon,day,hour):
    response = urllib2.urlopen("http://predict.cusf.co.uk/api/v1/?launch_latitude="+str(lat)+"&launch_longitude="+str(lon)+"&launch_datetime=2015-09-"+str(day)+"T"+str(hour)+"%3A00%3A00%2B01:00&ascent_rate=5&burst_altitude=30000&descent_rate=5")
    pprint('Running prediction for ' + str(lat)+','+str(lon))
    return response

def extract_results(response):
    d = json.load(response)
    # extraxt results
    lat = d["prediction"][1]["trajectory"][-1]["latitude"]
    lon =  d["prediction"][1]["trajectory"][-1]["longitude"]
    lon = long_conv(lon)
    return lat, lon

def how_close(a_lat,a_lon, b_lat, b_lon):
    a_latlon = LatLon(a_lat, a_lon)
    b_latlon = LatLon(b_lat, b_lon)
    dist = a_latlon.distance(b_latlon)
    bearing =  a_latlon.heading_initial(b_latlon)
    return dist, bearing

def makeMap(sites):
    pprint('Building map')
    map_osm = folium.Map(location=[52, -1.3],zoom_start=8)

    for y in sites:
        map_osm.simple_marker([y[2],y[3]], popup=str(y[0]),marker_color=str(y[4]))
        map_osm.create_map(path=FILENAME)
    webbrowser.open_new('file://'+CWD+'/'+FILENAME)

pprint('Starting')
now = dt.datetime.now()
LAUNCH_DAY = now.day
LAUNCH_HOUR = now.hour
CWD = os.getcwd()
FILENAME='backtrack.html'

# Initial desired landing site
DES_LAND_LAT=52.403048
DES_LAND_LONG=-1.504792
des_landing=('Desired',10,DES_LAND_LAT,DES_LAND_LONG,'blue')
loc_des = LatLon(DES_LAND_LAT,DES_LAND_LONG)

sites=[] # used for plotting markers
sites.append(des_landing)

if DES_LAND_LONG < 0:
    DES_LAND_LONG = 360 + DES_LAND_LONG

# Initial prediction for where a balloon launced from desired landing site would end up
response = retrieve_prediction(DES_LAND_LAT, DES_LAND_LONG, LAUNCH_DAY, LAUNCH_HOUR)

lat_land_from_des, long_land_from_des = extract_results(response)
landing=('Launch from desired',LAUNCH_HOUR,lat_land_from_des,long_land_from_des,'red')
pprint('Got landing - calculating distance and bearing')
sites.append(landing)
# Calc distance travelled and bearing
'''loc_lnd_from_des = LatLon(lat_land_from_des,long_land_from_des)
dist_from_des = loc_des.distance(loc_lnd_from_des)
bearing_from_des =  loc_des.heading_initial(loc_lnd_from_des)'''
dist_from_des, bearing_from_des = how_close(DES_LAND_LAT, DES_LAND_LONG,lat_land_from_des, long_land_from_des)
# Calc estimated launch site that will have a balloon land at desired landing site
new_launch = loc_des.offset(calc_backbearing(bearing_from_des),dist_from_des)
GUESS_LAT = float(new_launch.to_string('D')[0])
GUESS_LONG = float(new_launch.to_string('D')[1])
guess = ('guess',LAUNCH_HOUR,GUESS_LAT,GUESS_LONG,'purple')
sites.append(guess)
if GUESS_LONG < 0:
    GUESS_LONG = 360 + GUESS_LONG

#print new_launch.to_string('D')
# Now run prediction based on estimated landing site
response = retrieve_prediction(GUESS_LAT, GUESS_LONG, LAUNCH_DAY, LAUNCH_HOUR)

lat_land_from_guess, long_land_from_guess = extract_results(response)

landing_from_guess = ('lfg',LAUNCH_HOUR,lat_land_from_guess,long_land_from_guess,'green')
sites.append(landing_from_guess)

'''d, b = how_close(lat_land_from_guess, long_land_from_guess, DES_LAND_LAT, DES_LAND_LONG)
if d < 10:
    pprint('Close enough')
else:
    new_lat = '''
# Build map and plot markers
makeMap(sites)
