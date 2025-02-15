# imports
from os.path import join
from pathlib import Path

# relative imports
from data_utils import GeoJSONreader, GeoJSONwriter
from process import process_rails, extract_coordinates_as_lines

ABS_PATH = str(Path(__file__).parents[2])
DATA_PATH = join(ABS_PATH, "data")
OUT_PATH = join(ABS_PATH, "out/outfile.geojson")

if __name__ == "__main__":
    gjson_reader = GeoJSONreader(DATA_PATH)
    gjson_writer = GeoJSONwriter(OUT_PATH)

    data = gjson_reader.read_data()

    #process_rails(data["WGS_koleje2"]["features"], gjson_writer)

    rivers = extract_coordinates_as_lines(data["WGS_vodni_tok"])
    process_rails(rivers["features"],gjson_writer,0.00021)

