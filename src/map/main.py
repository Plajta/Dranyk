# imports
from os.path import join
from pathlib import Path
from track import track

# relative imports
from data_utils import GeoJSONreader, GeoJSONwriter
from process import process_rails, process_rivers, extract_coordinates_as_lines

ABS_PATH = str(Path(__file__).parents[2])
DATA_PATH = join(ABS_PATH, "data")

OUT_PATH_RIVERS = join(ABS_PATH, "out/rivers.geojson")
OUT_PATH_RAILS = join(ABS_PATH, "out/rails.geojson")
OUT_PATH_TRACK = join(ABS_PATH, "out/track.geojson")

def main():
    gjson_reader = GeoJSONreader(DATA_PATH)

    gjson_rivers = GeoJSONwriter(OUT_PATH_RIVERS)
    gjson_rails = GeoJSONwriter(OUT_PATH_RAILS)
    gjson_track = GeoJSONwriter(OUT_PATH_TRACK)

    data = gjson_reader.read_data()

    rivers = extract_coordinates_as_lines(data["WGS_vodni_tok"])
    process_rivers(rivers["features"], gjson_rivers, 0.0001)
    print("reky")
    process_rails(data["WGS_koleje2"]["features"], data["WGS_budova"]["features"], gjson_rails, 0.00031)
    print("koleje")
    gjson_rails.write_data()
    gjson_rivers.write_data()
    gjson_track.write_data()

    gjson_rivers.merge(gjson_rails)

    return gjson_rivers.data

if __name__ == "__main__":
    main()
    
