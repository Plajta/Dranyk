import geojson


def read_geojson(path):
    with open('data.geojson', 'r') as file:
        return geojson.load(file)
