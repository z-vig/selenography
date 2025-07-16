# Standard Libraries
from pathlib import Path
import os

# Dependencies
import rasterio as rio
import numpy as np

# Top-Level Imports
from selenography.utils import normalize_image


def convert_to_gtif(
    src: str | os.PathLike,
) -> None:
    """
    Converts any Rasterio-compatible format to a GeoTIFF.
    """
    src = Path(src)
    with rio.open(src) as ds:
        profile = ds.profile
        profile.update(driver="GTiff")

        save_path = src.with_suffix(".tif")
        print(f"Saved as: {save_path}")
        with rio.open(save_path, 'w', **profile) as dst:
            dst.write(ds.read())


def convert_to_8bit_2D(
    src: str | os.PathLike
) -> None:
    """
    Converts and Rasterio-compatible format to a 2D 8-bit image to be read by
    OpenCV.
    """
    src = Path(src)
    with rio.open(src) as ds:
        band = ds.read(1)
        band = normalize_image(band, min_val=0, max_val=255)
        band = band.astype(np.uint8)

        profile = ds.profile
        profile.update(driver="GTiff", dtype='uint8', nodata=0, count=1)

        save_path = src.with_name(f"{src.stem}_8bit.tif")
        print(f"Saved as: {save_path}")
        with rio.open(save_path, 'w', **profile) as dst:
            dst.write(band, 1)
