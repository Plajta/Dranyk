# imports
from os.path import join
from pathlib import Path
from track import track

# relative imports
from data_utils import read_geojson
from data_gen.process import process_rails, process_rivers, extract_coordinates_as_lines
from pathfind import run_pathfind

ABS_PATH = str(Path(__file__).parents[2])

PATH_RIVERS = join(ABS_PATH, "processed_data/river_map.geojson")
PATH_RAIL = join(ABS_PATH, "processed_data/rail_map.geojson")

OUT_PATH_RIVERS = join(ABS_PATH, "out/rivers.geojson")
OUT_PATH_RAILS = join(ABS_PATH, "out/rails.geojson")

def main():
    river_data = read_geojson(PATH_RIVERS)
    rails_data = read_geojson(PATH_RAIL)

    data = gjson_reader.read_data()

    rivers = extract_coordinates_as_lines(data["WGS_vodni_tok"])
    process_rivers(rivers["features"], gjson_rivers, 0.0001)
    
    process_rails(data["WGS_koleje2"]["features"], data["WGS_budova"]["features"], gjson_rails, 0.00031)

    gjson_rails.write_data()
    gjson_rivers.write_data()

    return gjson_rivers.data

if __name__ == "__main__":
    main()
