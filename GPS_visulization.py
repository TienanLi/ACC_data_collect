import folium
import os
import numpy as np
import branca.colormap as cm

def read_data_from_csv(file_name,Lat_column,Lon_column,speed_column):
    location=[]
    fo = open(os.path.dirname(__file__)+file_name, 'r')
    fo.readline()
    line_num=0
    while True:
        line_num+=1
        line = fo.readline()
        if not line:
            break
        tmp = line.split(',')
        if len(tmp) < max([Lat_column,Lon_column,speed_column]):
            break
        location.append([float(tmp[Lat_column]),float(tmp[Lon_column]),float(tmp[speed_column])])
    fo.close()
    return location

def map_visulization(location):
    m = folium.Map(location=[np.mean([location[i][0] for i in range(len(location))]), np.mean([location[i][1] for i in range(len(location))])],zoom_start=13)
    colorscale = cm.LinearColormap(('r','y','g'),vmin=0,vmax=20)
    for l in location:
        folium.Circle(
            location=[l[0], l[1]],
            radius=1,
            color = colorscale(l[2]),
            fill=True
        ).add_to(m)
    colorscale.caption = 'Speed (m/s)'
    m.add_child(colorscale)
    m.save('test.html')

if __name__=='__main__':
    location=read_data_from_csv('/output15132642.csv',2,3,5)
    map_visulization(location)

