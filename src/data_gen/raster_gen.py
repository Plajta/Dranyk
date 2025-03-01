from typing import Any

import numpy as np
import rasterio
from rasterio.features import rasterize
from shapely.geometry import shape

# dtype constant
DTYPE = rasterio.int8


def rasterize_polygons(
    poly_list: list,
    transform: tuple,
    shape: tuple[int, int],
    *,
    all_touched: bool = True,
) -> np.ndarray:

    # Perform the rasterization.
    return rasterize(
        shapes=poly_list,
        out_shape=shape,
        transform=transform,
        fill=0,
        all_touched=all_touched,
        dtype=DTYPE,  # You can change the data type if needed.
    )


def generate_raster(
    resolution: tuple[int, int],
    geojson_dict: dict[str, Any],
    coefficients: dict[str, int],
) -> (np.ndarray, tuple, tuple[int, int]):

    obs_polygons = {}
    xmin, ymin, xmax, ymax = float("inf"), float("inf"), float("-inf"), float("-inf")

    for name, coef in coefficients.items():
        shapes = []
        for f in geojson_dict[name]["features"]:
            geom = shape(f["geometry"])
            xmin = min(xmin, geom.bounds[0])
            ymin = min(ymin, geom.bounds[1])
            xmax = max(xmax, geom.bounds[2])
            ymax = max(ymax, geom.bounds[3])
            shapes.append((geom, coef))
        obs_polygons[name] = shapes.copy()

    print(xmin, ymin, xmax, ymax)

    # Compute raster size based on resolution
    width = int((xmax - xmin) / resolution[0])
    height = int((ymax - ymin) / resolution[1])
    # Define an affine transform that maps pixel coordinates to geographic coordinates.
    transform = rasterio.transform.from_bounds(xmin, ymin, xmax, ymax, width, height)
    final_rast = np.ones((height, width), dtype=DTYPE)

    for obs in obs_polygons.values():
        final_rast += rasterize_polygons(obs, transform, (height, width))

    return final_rast, transform, (height, width)


def save_tiff(
    raster: np.ndarray,
    transform: tuple,
    shape: tuple[int, int],
    config: str,
    output_tiff: str,
) -> None:

    with rasterio.open(
        output_tiff,
        "w",
        driver="GTiff",
        height=shape[0],
        width=shape[1],
        count=1,
        dtype=DTYPE,
        crs="EPSG:4326",  # WGS 84
        transform=transform,
    ) as dst:
        dst.write(raster, 1)
        dst.update_tags(config=config)

    print(f"GeoTIFF saved to {output_tiff}")


def main() -> None:
    from pathlib import Path

    import matplotlib.pyplot as plt
    from utils import read_geojson

    ABS_PATH = Path(__file__).parents[2]
    DATA_PATH = ABS_PATH / "data"
    CONF_PATH = ABS_PATH / "out" / "raster.json"
    OUT_PATH = ABS_PATH / "out" / "raster.tiff"

    if not Path.exists(CONF_PATH):
        "No config for raster generation!"

    config = read_geojson(
        CONF_PATH,
    )  # Colors are not used anymore, plotting whole geojsons was very slow.
    print(config)  # Maybe, in the future, I will make the TIFF file in full RGB colors.

    if Path.exists(OUT_PATH):
        with rasterio.open(OUT_PATH, "r") as dataset:
            metadata = dataset.tags()  # Read metadata tags

            if "config" in metadata and metadata["config"] == str(config):  # Maybe not the best way to compare these
                print("No change in config, skipping generation process.")
                print("Bounds:", dataset.bounds)
                print("Resolution:", dataset.res)
                print("Transform:", dataset.transform)
                print("CRS:", dataset.crs)

                plt.imshow(dataset.read(1), interpolation="none", cmap="pink")
                plt.show()
                return

    print("Config or structure has changed, generating new GeoTIFF")

    data = {}
    for key in config["coefs"]:
        data[key] = read_geojson(DATA_PATH / f"{key}.geojson")

    raster, transform, shape = generate_raster(
        config["resolution"],
        data,
        config["coefs"],
    )
    raster[raster < 0] = 0

    save_tiff(raster, transform, shape, str(config), str(OUT_PATH))

    plt.imshow(raster, interpolation="none", cmap="pink")
    plt.show()


if __name__ == "__main__":
    main()
