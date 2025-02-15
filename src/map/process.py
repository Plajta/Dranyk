from shapely import convex_hull
from shapely.geometry import Point, LineString

from sklearn.cluster import DBSCAN
from scipy.spatial import Delaunay

import numpy as np
import networkx as nx

def process_rails(rail_features, gjson_writer):
    multipoint_coords = []
    for feature in rail_features:
        coords = feature["geometry"]["coordinates"]
        for coord in coords:
            multipoint_coords.append(coord)

    coords = np.array(multipoint_coords)
    dbscan = DBSCAN(eps=0.00031, min_samples=1)
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
