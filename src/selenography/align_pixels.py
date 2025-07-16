# Standard Libraries
import os
from pathlib import Path

# Dependencies
import numpy as np
import rasterio as rio
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling


def align_pixels(
    ref_path: str | os.PathLike,
    targ_path: str | os.PathLike
) -> None:
    """
    Aligns the pixels of a geo-located target image to the pixels of a
    geo-located reference image and saves a new image that is that same width
    and height of the source image, but with the aligned data from the target
    image.
    """
    ref_path = Path(ref_path)
    targ_path = Path(targ_path)
    save_path = Path(targ_path.with_name(f"{targ_path.stem}_aligned.tif"))

    with rio.open(ref_path, "r") as ref, rio.open(targ_path, "r") as targ:
        transform = from_origin(
            ref.bounds.left,
            ref.bounds.top,
            abs(ref.transform.a),
            abs(ref.transform.e)
        )

        rio_kwargs = {
            'crs': ref.crs,
            'transform': transform,
            'width': ref.width,
            'height': ref.height,
            'count': targ.count,
            'dtype': np.float32,
            'driver': "GTiff",
            'nodata': -999
        }

        with rio.open(save_path, "w", **rio_kwargs) as dst:
            for i in range(1, targ.count+1):
                reproject(
                    source=rio.band(targ, i),
                    destination=rio.band(dst, i),
                    src_transform=ref.transform,
                    src_crs=ref.crs,
                    dst_transform=transform,
                    dst_crs=ref.crs,
                    resampling=Resampling.bilinear,
                    dst_nodata=-999
                )
