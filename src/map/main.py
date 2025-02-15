# imports
from os.path import join
from pathlib import Path

# relative imports
from data_utils import GeoJSONreader, GeoJSONwriter
from process import process_rails, process_rivers, extract_coordinates_as_lines

ABS_PATH = str(Path(__file__).parents[2])
DATA_PATH = join(ABS_PATH, "data")

OUT_PATH_RIVERS = join(ABS_PATH, "out/rivers.geojson")
OUT_PATH_RAILS = join(ABS_PATH, "out/rails.geojson")

if __name__ == "__main__":
    gjson_reader = GeoJSONreader(DATA_PATH)

    gjson_rivers = GeoJSONwriter(OUT_PATH_RIVERS)
    gjson_rails = GeoJSONwriter(OUT_PATH_RAILS)

    data = gjson_reader.read_data()

    rivers = extract_coordinates_as_lines(data["WGS_vodni_tok"])
    process_rivers(rivers["features"], gjson_rivers, 0.00021)
    process_rails(data["WGS_koleje2"]["features"], gjson_rails, 0.00031)
