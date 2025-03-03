import math
from collections.abc import Generator
from typing import Any, NamedTuple

import numpy as np
import rasterio
from astar import AStar
from shapely.geometry import LineString

MIN = (13.2, 49.65)
MAX = (13.5, 49.85)

class IntPoint(NamedTuple):
    x: int
    y: int


class CustomAStar(AStar):
    vectors: tuple[IntPoint] = (
        IntPoint(-1, 0),
        IntPoint(-1, 1),
        IntPoint(0, 1),
        IntPoint(1, 1),
        IntPoint(1, 0),
        IntPoint(1, -1),
        IntPoint(0, -1),
        IntPoint(-1, -1),
    )

    def __init__(self, price_map: np.ndarray, dist_coef: int) -> None:
        self.price_map = price_map
        self.map_shape = self.price_map.shape
        self.dist_coef = dist_coef

    def neighbors(self, n: IntPoint) -> Generator[IntPoint]:
        for v in self.vectors:
            n1 = IntPoint(n.x + v.x, n.y + v.y)
            if 0 <= n1.x < self.map_shape[1] and 0 <= n1.y < self.map_shape[0]:
                yield n1

    def distance_between(self, n1: IntPoint, n2: IntPoint) -> float:
        dist = math.sqrt((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) * self.dist_coef
        dist += self.price_map[n2.y, n2.x]
        return dist

    def heuristic_cost_estimate(self, current: IntPoint, goal: IntPoint) -> float:
        return math.sqrt((current.x - goal.x) ** 2 + (current.y - goal.y) ** 2) * self.dist_coef

    def is_goal_reached(self, current: IntPoint, goal: IntPoint) -> bool:
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
        transmat = dataset.transform

    start_p = IntPoint(*[round(c) for c in ~transmat * start])
    end_p = IntPoint(*[round(c) for c in ~transmat * end])

    algorithm = CustomAStar(raster, 1)
    plt.imshow(raster, interpolation="none", cmap="pink")

    path = algorithm.astar(start_p, end_p)
    line = LineString(path)
    line_recomputed = []

    xcoords, ycoords = [], []
    for p in line.coords:
        line_recomputed.append(transmat*p)
        xcoords.append(p[0])
        ycoords.append(p[1])

    plt.plot(xcoords, ycoords, color="b")
    plt.show()

    return LineString(line_recomputed)


if __name__ == "__main__":
    start = (13.3767908, 49.7320639)
    end = (13.3840758, 49.7609489)
    print(main(start, end))
