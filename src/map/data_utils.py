import geojson

import os


class GeoJSONreader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = {}

    def __read_geojson__(self, path):
        with open(path, 'r') as file:
            return geojson.load(file)

    def read_data(self):
        for file in os.listdir(self.data_path):
            if file == ".gitkeep": # ignore gitkeep
                continue

            file_path_abs = os.path.join(self.data_path, file)

            file_name = file.replace(".geojson", "")
            print(f"Processed {file_name}")
            file_content = self.__read_geojson__(file_path_abs)

            self.data[file_name] = file_content

        return self.data
