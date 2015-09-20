#HabHubTools

This repo contains some Python tools for making use of the awesome [HabHub](http://predict.habhub.org/) API
for predicting the path of High Altitude balloon launches.

##dailypredict.py

####Requires:
json, urllib2, pprint, os, time, datetime

This is intended to be run as a daily job (e.g. with cron) to build up a
data picture of the landing locations from a given launch site(s) over time. Data is written to the file *prediction.csv* in the form:

Day:Month:Year, Hour, Site, Burst Lat, Burst Lon, Landing Lat, Landing Lon

e.g.

18:9:2015,11,2,51.9305930247,0.792177470789,51.9545616101,0.934571494099

####Usage:

Amend the LAUNCH_LAT and LAUNCH_LON variables to reflect your desired launch site. You can have as many sites as you like, but they must be included in the launch_sites list.

Run with:

python dailypredict.py

##maploader.py

####Requires:
folium, os, webbrowser

Reads the values from the *prediction.csv* results file produced by dailypredict.py and displays them on a map. The marker labls will show details of the flight.

####Usage:

Run with:

python maploader.py

##backtrack.py

####Requires:
json, urllib2, pprint, os, time, datetime, folium, LatLon

Useful to work out a potential launch location based on a desired landing site. Plots the coordinates on a map and dsiplays in browser.
####Marker colours:
Blue: Desired landing location

Red: Landing location if launched from desited site.

Pink: Guessed site based on backtracking

Green: Landing site if launched from guess (lfg)

So if you want your balloon to land at the blue marker, the code will backtrack to give you the pink launch site. The green marker then shows the landing site calculated by rolling the prediction forward.


####Usage:

Modify the DES_LAND_LAT and DES_LAND_LONG variables with the desired landing location.

Run with:

python backtrack.py

##sixday.py

####Requires:
json, urllib2, pprint, os, time, datetime, folium, LatLon

Runs a prediction for each day over the next 6 days and plots on a map.

####Usage:

Modify the LAUNCH_LAT and LAUNCH_LONG varaibles. Default is to predict based on a 10:00 and 14:00 launch time. Modify the LAUNCH_HOUR_M and LAUNCH_HOUR_A varaibles if you want different times.  

Run with:

python sixday.py
