import geojson
import os
from shapely.geometry import mapping


def read_geojson(path):
    with open(path, 'r') as file:
        return geojson.load(file)


class GeoJSONreader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = {}

    def read_data(self):
        for file in os.listdir(self.data_path):
            if file == ".gitkeep": # ignore gitkeep
                continue
            if file == "data_web":
                continue

            file_path_abs = os.path.join(self.data_path, file)
            
            file_name = file.replace(".geojson", "")
            print(f"Processed {file_name}")
            file_content = read_geojson(file_path_abs)

            self.data[file_name] = file_content

        return self.data


class GeoJSONwriter:
    def __init__(self, out_file):
        # main header for GeoJSON
        self.data = {
            "type": "FeatureCollection",
            "features": []
        }
        self.out_file = out_file

    def add_polygon(self, np_array):
        polygon = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[]]
            },
            "properties": {}
        }
        for point in np_array:
            polygon["geometry"]["coordinates"][0].append(point.tolist())
        self.data["features"].append(polygon)

    def add_multipoint(self, np_array):
        multipoint = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": []
            },
            "properties": {}
        }
        for point in np_array:
            multipoint["geometry"]["coordinates"].append(point.tolist())
        self.data["features"].append(multipoint)

    def add_point(self, np_coords):
        point = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": np_coords.tolist()
            },
            "properties": {}
        }
        self.data["features"].append(point)

    def add_linestring(self, line):
        line_dict = {
            "type": "Feature",
            "geometry": mapping(line),
            "properties": {}
        }
        self.data["features"].append(line_dict)

    def write_data(self):
        with open(self.out_file, 'w') as outfile:
            geojson.dump(self.data, outfile)

    def clear_data_buffer(self):
        self.data = {
            "type": "FeatureCollection",
            "features": []
        }

    def merge(self,GeoJSONwriter):

        self.data = {
        "type": "FeatureCollection",
        "features": self.data["features"] + GeoJSONwriter.data["features"]
    }
