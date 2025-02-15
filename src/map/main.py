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

    perar,start_points,end_points = track(river_data,(13.3767908,49.7320639),(13.3840758,49.7609489))

    print(start_points)
    print(end_points)

    return rails_data


if __name__ == "__main__"
    main()