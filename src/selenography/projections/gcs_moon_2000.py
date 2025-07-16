# Standard Libraries
import os
from pathlib import Path

# Dependencies
import numpy as np
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS


def gcs_moon_2000(
    src_path: str | os.PathLike,
    dst_path: str | os.PathLike | None = None
) -> os.PathLike:
    """
    Projects a Rasterio-compatible Datase path from its original coordinate
    system to the standard GCSMoon2000 (ESRI:104903) geographic coordinate
    system and saves it to the same location as the original file with the
    suffix "_gcs.tif".

    Parameters
    ----------
    """
    src_path = Path(src_path)

    with rio.open(src_path) as src:

        transform, width, height = calculate_default_transform(
            src_crs=src.crs,
            dst_crs=CRS.from_authority("ESRI", 104903),
            width=src.width,
            height=src.height,
            left=src.bounds.left,
            bottom=src.bounds.bottom,
            top=src.bounds.top,
            right=src.bounds.right
        )

        print(f"Shape of Dataset: {src.shape}")

        rio_kwargs = {
            'crs': CRS.from_authority("ESRI", 104903),
            'transform': transform,
            'width': width,
            'height': height,
            'count': src.count,
            'dtype': np.float32,
            'driver': "GTiff",
            'nodata': -999
        }

        if dst_path is None:
            save_path = src_path.with_name(f"{src_path.stem}_gcs.tif")
        else:
            save_path = Path(dst_path)
        with rio.open(save_path, "w", **rio_kwargs) as dst:
            for i in range(1, src.count+1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=src.transform,
                    dst_crs=CRS.from_authority("ESRI", 104903),
                    resampling=Resampling.bilinear,
                    dst_nodata=-999
                )

    print(f"Projected Raster saved to: {save_path}")
    return save_path
