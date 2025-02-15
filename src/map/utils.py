import geojson


def read_geojson(path):
    with open(path, 'r') as file:
        return geojson.load(file)
