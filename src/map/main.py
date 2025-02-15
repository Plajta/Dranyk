# imports
from os.path import join
from pathlib import Path

# relative imports
from data_utils import read_geojson
from data_gen.process import process_rails, process_rivers, extract_coordinates_as_lines
from pathfind import run_pathfind

ABS_PATH = str(Path(__file__).parents[2])

PATH_RIVERS = join(ABS_PATH, "processed_data/river_map.geojson")
PATH_RAIL = join(ABS_PATH, "processed_data/rail_map.geojson")


def main():
    river_data = read_geojson(PATH_RIVERS)
    rails_data = read_geojson(PATH_RAIL)

    run_pathfind(river_data, rails_data)

    return river_data


if __name__ == "__main__":
    main()
