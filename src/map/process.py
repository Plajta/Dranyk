from shapely import convex_hull
from shapely.geometry import Polygon, MultiPoint

import numpy as np


def process_rails(rail_features, gjson_writer):
    for i, feature in enumerate(rail_features):
        coords = feature["geometry"]["coordinates"][0]
        area = feature["properties"]["Shape.STArea()"]
        length = feature["properties"]["Shape.STLength()"]

        """
        for coord in coords:
            x = coord[0]
            y = coord[1]
            #print(x, y)
        """

        hull = convex_hull(Polygon(coords))
        np_hull = np.array(hull.exterior.coords)
        gjson_writer.add_polygon(np_hull)

        print("Processed " + str(i))
    gjson_writer.write_data()
