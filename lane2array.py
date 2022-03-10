#!/usr/bin/env python
import matplotlib
import numpy as np
matplotlib.use('Agg')
import lanelet2
import tempfile
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d
from lanelet2.projection import UtmProjector
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import argparse
import math

# pass path by parameter
map_name = str("zhubei_map" + ".osm")
map_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res/", map_name)


def lane2array():
    # change lat and lon value base on the original/first point of the osm file
    # TODO: automatically obtain origin lat and lon 
    lat = 24.8
    lon = 121.0 
    # or the projector will crash
    projector = UtmProjector(lanelet2.io.Origin(lat, lon))
    
    map = lanelet2.io.load(map_file, projector)
    lanes = map.laneletLayer
    # print(len(lanes))
    # for elem in lanes:
    #     print(elem.attributes)
    polygons = []
    xs = []
    ys = []
    xs_3d = []
    ys_3d = []
    xys_3d = []

    for elem in lanes:
        polygons.append(elem.polygon2d())
        # print(elem.polygon2d()[0])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # get bbox of the map
    xmin = np.inf
    xmax = -np.inf
    ymin = np.inf
    ymax = -np.inf

    for polys in polygons:
        for p in polys:
            # print(p.attributes)
            # multiplied by 10 to fit the scale of 10  pixels/meter
            xs.append(round(10 * float(p.attributes["local_x"]), 2))
            ys.append(round(10 * float(p.attributes["local_y"]), 2))
        #repeat the first point to create a 'closed loop'
        xs.append(xs[0])
        ys.append(ys[0])
        # draw lanelet in a figure (show only)
        ax.fill(xs,ys, color='black')
        xs_3d.append(xs)
        ys_3d.append(ys)
        xs = []
        ys = []

    # find max and min
    xmax = max(max(xs_3d, key=max))
    xmin = min(min(xs_3d, key=min))
    ymax = max(max(ys_3d, key=max))
    ymin = min(min(ys_3d, key=min))
    
    # ax.plot(xmin, ymin, 'o', markersize=4)
    # ax.plot(xmax, ymax, 'o', markersize=4)
    print("xmax: " +  str(xmax))
    print("xmin: " +  str(xmin))
    print("ymax: " +  str(ymax))
    print("ymin: " +  str(ymin))
    
    width = int(math.ceil(xmax) - math.floor(xmin))
    height = int(math.ceil(ymax) - math.floor(ymin))

    img = Image.new('1', (width, height), 1)

    for i in range(len(xs_3d)):
        xys = []
        for j in range(len(xs_3d[i])):
            xys.append(int(xs_3d[i][j] - xmin))
            xys.append(int(ys_3d[i][j] - ymin))
        ImageDraw.Draw(img).polygon(xys, outline=0, fill=0)

    
    # ax.axis('off')
    # save picture name by parameter or get map name
    
    img_np = np.array(img)
    np.save(map_name[:-4], img_np)

    save_png = str(map_name[:-4] + ".png")
    img = img.save(save_png)
    
    save_fig = str(map_name[:-4] + "_fig.png")
    plt.savefig(save_fig, bbox_inches='tight', pad_inches=0)

if __name__ == '__main__':
    lane2array() 