import folium
import webbrowser
import os

CWD = os.getcwd()
colours = ['red','blue','green','orange','purple','pink','black']
INFILENAME='prediction.csv'
OUTFILENAME='prediction.html'
file = open(INFILENAME, "r")
map_osm = folium.Map(location=[52, -1.3],zoom_start=8)
while 1:
    line = file.readline()
    if not line:
        break
    data = line.split(",")
    DATE = data[0]
    HOUR = data[1]
    SITE = data[2]
    LAT_BURST=data[3]
    LONG_BURST=data[4]
    LAT_LAND=data[5]
    LONG_LAND=data[6]
    if int(SITE) < 8:
        COL = colours[int(SITE)-1]
    else:
        COL = 'white'
    map_osm.simple_marker([LAT_LAND,LONG_LAND], popup="Site: " + SITE + " " + str(DATE)+" "+str(HOUR)+":00Z",marker_icon='info-sign',marker_color=COL)
    map_osm.simple_marker([LAT_BURST,LONG_BURST], popup="Site: " + SITE + " " + str(DATE)+" "+str(HOUR)+":00Z",marker_icon='star-empty',marker_color=COL)
    '''map_osm.circle_marker(location=[LAT_LAND, LONG_LAND], radius=500,
                    popup='Laurelhurst Park', line_color='#735518',
                    fill_color='#3186cc')'''


    map_osm.create_map(path=OUTFILENAME)


webbrowser.open_new('file://'+CWD+'/'+OUTFILENAME)
