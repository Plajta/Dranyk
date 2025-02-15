from shapely.geometry import Point, LineString

from sklearn.cluster import DBSCAN
from scipy.spatial import Delaunay

import numpy as np
import networkx as nx

#                    Railway station        # Industry near railway station
EXCLUSION_REGIONS = ["32003010002264835", "32003010002268968", "32003010002268277"
                     # Another railway station # Industrial complex
                     "32003010002270746", "32003010002281137",
                     # Last industry
                     "32003010002140177", "32003010002140804"]

def __process_lines__(features,
                      gjson_writer,
                      esp=0.00031):
    multipoint_coords = []
    for feature in features:
        coords = feature["geometry"]["coordinates"]
        for coord in coords:
            multipoint_coords.append(coord)

    coords = np.array(multipoint_coords)
    dbscan = DBSCAN(eps=esp, min_samples=1)
    labels = dbscan.fit_predict(coords)

    unique_labels = set(labels)
    clustered_points = [
        coords[labels == label].mean(axis=0).tolist() for label in unique_labels if label != -1
    ]

    tri = Delaunay(clustered_points)
    edges = set()

    for simplex in tri.simplices:
        for i in range(3):
            p1, p2 = tuple(clustered_points[simplex[i]]), tuple(clustered_points[simplex[(i+1) % 3]])
            edges.add((p1, p2))

    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=np.linalg.norm(np.array(edge[0]) - np.array(edge[1])))

    mst = nx.minimum_spanning_tree(G)
    lines = [LineString([Point(p1), Point(p2)]) for p1, p2 in mst.edges]

    for line in lines:
        gjson_writer.add_linestring(line)
    


def process_rails(rail_features,
                  building_features,
                  gjson_writer,
                  esp=0.00031):
    ### TODO: add building processing

    __process_lines__(rail_features, gjson_writer, esp)


def process_rivers(river_features,
                   gjson_writer,
                   esp=0.00021):
    print(f"gjson writer: {type(gjson_writer)}")
    __process_lines__(river_features, gjson_writer, esp)
    river_features = gjson_writer.data["features"]
    gjson_writer.clear_data_buffer()
    print(gjson_writer.data)
    __process_lines__(river_features, gjson_writer, 0.0003)

    river_features = gjson_writer.data["features"]
    gjson_writer.clear_data_buffer()
    print(gjson_writer.data)
    __process_lines__(river_features, gjson_writer, 0.00055)

    gjson_writer.write_data()



def extract_coordinates_as_lines(data):
    line_strings = []

    for feature in data.get("features", []):
        geom = feature.get("geometry", {})
        if geom.get("type") == "Polygon":
            for ring in geom.get("coordinates", []):
                line_strings.append({"type": "LineString", "coordinates": ring})
        elif geom.get("type") == "MultiPolygon":
            for polygon in geom.get("coordinates", []):
                for ring in polygon:
                    line_strings.append({"type": "LineString", "coordinates": ring})

    return {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ls} for ls in line_strings]}
