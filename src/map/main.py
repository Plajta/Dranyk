# imports
from os.path import join
from pathlib import Path

from track import track

# relative imports
from utils import read_geojson, merge
from a_star_madness import main as astar_main

ABS_PATH = str(Path(__file__).parents[2])

PATH_RIVERS = join(ABS_PATH, "processed_data/river_map.geojson")
PATH_RAIL = join(ABS_PATH, "processed_data/rail_map.geojson")


def main():
    river_data = read_geojson(PATH_RIVERS)
    rails_data = read_geojson(PATH_RAIL)

    koular = merge(river_data, rails_data)

    start = (13.3767908,49.7320639)
    end = (13.3840758,49.7609489)

    perar,start_points,end_points = track(river_data, start, end)

    print(start_points)
    print(end_points)

    start_path = astar_main(start, end_points[1], 0.0005)
    end_path = astar_main(start_points[0], end, 0.0005)

    return rails_data


if __name__ == "__main__":
    main()