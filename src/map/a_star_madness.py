from collections.abc import Generator
from typing import Any, NamedTuple

import numpy as np
import rasterio
from astar import AStar
from shapely.geometry import LineString

MIN = (13.2, 49.65)
MAX = (13.5, 49.85)

class Point(NamedTuple):
    x: int
    y: int


class CustomAStar(AStar):
    vectors: tuple[Point] = (
        Point(-1, 0),
        Point(-1, 1),
        Point(0, 1),
        Point(1, 1),
        Point(1, 0),
        Point(1, -1),
        Point(0, -1),
        Point(-1, -1),
    )

    def __init__(self, price_map: np.ndarray, dist_coef: int) -> None:
        self.price_map = price_map
        self.map_shape = self.price_map.shape
        self.dist_coef = dist_coef

    def neighbors(self, n: Point) -> Generator[Point]:
        for v in self.vectors:
            n1 = Point(n.x + v.x, n.y + v.y)
            if 0 <= n1.x < self.map_shape[1] and 0 <= n1.y < self.map_shape[0]:
                yield n1

    def distance_between(self, n1: Point, n2: Point) -> int:
        dist = np.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) * self.dist_coef
        dist += self.price_map[n2.y, n2.x]
        return dist

    def heuristic_cost_estimate(self, current: Point, goal: Point) -> int:
        return np.sqrt((current.x - goal.x) ** 2 + (current.y - goal.y) ** 2) * self.dist_coef

    def is_goal_reached(self, current: Point, goal: Point) -> bool:
        return current == goal


def main(start: tuple[float, float], end: tuple[float, float]) -> LineString:
    from pathlib import Path

    import matplotlib.pyplot as plt

    ABS_PATH = Path(__file__).parents[2]
    TIFF_PATH = ABS_PATH / "out" / "raster.tiff"

    raster: np.ndarray
    bbox: Any
    reso: tuple
    with rasterio.open(TIFF_PATH, "r") as dataset:
        raster = dataset.read(1)
        bbox = dataset.bounds
        reso = dataset.res

    start_p = Point(x=round((start[0] - bbox.left) / reso[0]), y=round((bbox.top - start[1]) / reso[1]))
    end_p = Point(x=round((end[0] - bbox.left) / reso[0]), y=round((bbox.top - end[1]) / reso[1]))

    algorithm = CustomAStar(raster, 1)
    plt.imshow(raster, interpolation="none", cmap="pink")

    path = algorithm.astar(start_p, end_p)
    line = LineString(path)

    xcoords, ycoords = [], []
    for p in line.coords:
        xcoords.append(p[0])
        ycoords.append(p[1])

    plt.plot(xcoords, ycoords, color="b")
    plt.show()

    return line  # TODO @LosVocelos: Translate raster positions to latitude, longitude


if __name__ == "__main__":
    # print(main((13.35, 49.74), (13.39, 49.78)))
    start = (13.3767908, 49.7320639)
    end = (13.3840758, 49.7609489)
    print(main(start, end))
