import geojson


def read_geojson(path):
    with open(path, 'r') as file:
        return geojson.load(file)

def merge(GeoJSONwriter1 ,GeoJSONwriter2):

        return{
            "type": "FeatureCollection",
            "features": GeoJSONwriter1["features"] + GeoJSONwriter2["features"]
        }