# imports
from os.path import join
from pathlib import Path
import matplotlib.pyplot as plt
from shapely.geometry import Point

# relative imports
from a_star_madness import CustomAStar, MIN
from utils import read_geojson

ABS_PATH = str(Path(__file__).parents[2])
DATA_PATH = join(ABS_PATH, "data")
OUT_PATH = join(ABS_PATH, "out/outfile.geojson")


if __name__ == "__main__":
    coefs = {"WGS_dalnice_silnice": 3, "WGS_vodni_tok": -1, "WGS_budova": 3, "WGS_chodnik": 4, "WGS_koleje": -1}
    colors = {"WGS_dalnice_silnice": "0.8", "WGS_vodni_tok": "b", "WGS_budova": "0.5", "WGS_chodnik": "0.3", "WGS_koleje": "g"}

    data = {}
    for key in coefs.keys():
        data[key] = read_geojson("/".join([DATA_PATH, key+".geojson"]))

    start = Point(13.35, 49.74)
    end = Point(13.37, 49.76)
    cell_size = 0.0001

    algorithm = CustomAStar(cell_size, data, coefs)
    path = algorithm.astar(start, end)

    print("LOL")

    plt.imshow(algorithm.obstacles, cmap='gray')

    xcoords, ycoords = [], []
    for p in path:
        xcoords.append(int((p.x-MIN[0])/cell_size))
        ycoords.append(algorithm.out_shape[0]-int((p.y-MIN[1])/cell_size))

    plt.plot(xcoords, ycoords, color="r")

    plt.show()
