import json
import networkx as nx
from shapely.geometry import LineString, Point
from scipy.spatial import KDTree
import numpy as np
from utils import merge, add_point

def load_geojson(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def build_graph(geojson_data):
    G = nx.Graph()
    edges = []
    points = []
    
    for feature in geojson_data['features']:
        coords = feature['geometry']['coordinates']
        line = LineString(coords)
        start, end = Point(coords[0]), Point(coords[-1])
        
        G.add_edge(tuple(coords[0]), tuple(coords[-1]), geometry=line)
        edges.append(line)
        points.extend([tuple(coords[0]), tuple(coords[-1])])
    
    return G, edges, points

def find_nearest_node(points, target_point):
    tree = KDTree(points)
    dist, idx = tree.query(target_point)
    return points[idx]

def find_shortest_path(G, points, start_point, end_point):
    start_node = find_nearest_node(points, start_point)
    end_node = find_nearest_node(points, end_point)
    
    try:
        path = nx.shortest_path(G, source=start_node, target=end_node, weight=lambda u, v, d: d['geometry'].length)
    except nx.NetworkXNoPath:
        return None
    
    return path

def extract_geojson_path(G, path):
    features = []
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        line = G[u][v]['geometry']
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": list(line.coords)
            },
            "properties": {}
        })
    
    return {"type": "FeatureCollection", "features": features}

def main(geojson_data, start, end):
    G, edges, points = build_graph(geojson_data)
    path = find_shortest_path(G, points, start, end)
    
    if path:
        result_geojson = extract_geojson_path(G, path)
        print(f"Route saved")
        return result_geojson
    else:
        print("No path found between the points.")

def track(input_geojson,start=(13.3227427651515, 49.7070727727273),end=(13.4308351203704, 49.6997400462963)):

    print(start)
    print(end)
    geojson = main(input_geojson,start,end)
    try:
        end_point = geojson["features"][0]["geometry"]["coordinates"]
        start_point = geojson["features"][-1]["geometry"]["coordinates"]
    except:
        print("no path")

    print(add_point(np.array(start)))
    
    geojson["features"].append(add_point(np.array(start)))
    geojson["features"].append(add_point(np.array(end)))
    
    
   

    # coords = np.array(start)
    # GeoJSONwriter.add_point(coords)
    # coords = np.array(end)
    # GeoJSONwriter.add_point(coords)
    print("done")
    return geojson,start_point,end_point

    


# Example usage:
# main('roads.geojson', (-73.9857, 40.7484), (-73.9780, 40.7527), 'route.geojson')
