# imports
from os.path import join
from pathlib import Path

from track import track

# relative imports
from utils import read_geojson, merge

ABS_PATH = str(Path(__file__).parents[2])

PATH_RIVERS = join(ABS_PATH, "processed_data/river_map.geojson")
PATH_RAIL = join(ABS_PATH, "processed_data/rail_map.geojson")


def main():
    river_data = read_geojson(PATH_RIVERS)
    rails_data = read_geojson(PATH_RAIL)

    koular = merge(river_data, rails_data)

    perar = track(river_data)

    return river_data


if __name__ == "__main__":
    main()