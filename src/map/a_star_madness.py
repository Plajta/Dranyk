from shapely.geometry import LineString, Point, shape
from shapely import set_precision
from rtree import index
from astar import AStar
import numpy as np

MIN = (13.2, 49.65)
MAX = (13.5, 49.85)

import rasterio
from rasterio.features import rasterize
from shapely.geometry import shape


class CustomAStar(AStar):
    vectors = [Point(-1, 0), Point(-1, 1), Point(0, 1), Point(1, 1),
               Point(1, 0), Point(1, -1), Point(0, -1), Point(-1, -1)]

    def __init__(self, cell_size, obstacles, coefficients):
        self.cell_size = cell_size
        self.out_shape = (int((MAX[1]-MIN[1])/cell_size), int((MAX[0]-MIN[0])/cell_size))
        bounds = (13.2, 49.65, 13.5, 49.85)
        self.obstacles = np.ones(self.out_shape, dtype=np.int16)
        for name in coefficients:
            print(name)
            raster = self.rasterize_geojson(obstacles[name], self.out_shape, bounds, default_value=coefficients[name])
            print(raster.shape)
            self.obstacles += raster
        self.coefs = coefficients

    def rasterize_geojson(self, geojson, out_shape, bounds, default_value=1, fill_value=0, all_touched=True):
        # Prepare an iterable of (geometry, value) pairs.
        shapes = []
        for f in geojson["features"]:
            geom = shape(f['geometry'])
            shapes.append((geom, default_value))

        # Define an affine transform that maps pixel coordinates to geographic coordinates.
        # Note: Rasterio expects the width (number of columns) and height (number of rows) respectively.
        transform = rasterio.transform.from_bounds(*bounds, out_shape[1], out_shape[0])

        # Perform the rasterization.
        raster = rasterize(
            shapes=shapes,
            out_shape=out_shape,
            transform=transform,
            fill=fill_value,
            all_touched=all_touched,
            dtype=np.int16  # You can change the data type if needed.
        )

        return raster

    def neighbors(self, n):
        for v in self.vectors:
            n1 = Point(n.x + v.x * self.cell_size, n.y + v.y * self.cell_size)
            set_precision(n1,self.cell_size)
            yield n1

    def distance_between(self, n1, n2):
        # line = LineString([n1, n2])
        dist = n1.distance(n2)

        dist += self.obstacles[(self.out_shape[0]-int((n2.y-MIN[1])/self.cell_size), int((n2.x-MIN[0])/self.cell_size))] * dist
        return dist

    def heuristic_cost_estimate(self, current, goal):
        return current.distance(goal)*2

    def is_goal_reached(self, current, goal):
        return current.distance(goal) < 0.55 * self.cell_size


def main(start, end, cell_size):
    # imports
    from os.path import join
    from pathlib import Path
    import matplotlib.pyplot as plt
    from shapely.geometry import Point

    # relative imports
    from utils import read_geojson

    ABS_PATH = str(Path(__file__).parents[2])
    DATA_PATH = join(ABS_PATH, "data")
    OUT_PATH = join(ABS_PATH, "out/outfile.geojson")

    # coefficients
    coefs = {"WGS_provozni_komunikace": 3, "WGS_vodni_tok": -1, "WGS_budova": 3, "WGS_chodnik": 4, "WGS_koleje": -1}
    colors = {"WGS_provozni_komunikace": "0.8", "WGS_vodni_tok": "b", "WGS_budova": "0.5", "WGS_chodnik": "0.3",
              "WGS_koleje": "g"}

    data = {}
    for key in coefs.keys():
        data[key] = read_geojson("/".join([DATA_PATH, key + ".geojson"]))

    start = Point([*start])
    set_precision(start,cell_size)
    end = Point([*end])
    set_precision(end,cell_size)

    algorithm = CustomAStar(cell_size, data, coefs)
    path = algorithm.astar(start, end)
    line = LineString(path)
    plt.imshow(algorithm.obstacles, cmap='gray')

    xcoords, ycoords = [], []
    for p in line.coords:
        xcoords.append(int((p[0] - MIN[0]) / cell_size))
        ycoords.append(algorithm.out_shape[0] - int((p[1] - MIN[1]) / cell_size))

    plt.plot(xcoords, ycoords, color="r")
    plt.show()

    return line


if __name__ == '__main__':
    print(main((13.35, 49.74), (13.39, 49.78), 0.0001))
